"""Project home (docs/백로그/R7-프로젝트-홈.md): `/`에 videos/ 밑 모든 영상의 상태를 한눈에
보여준다 - 처리 중 / 검토 중 N건 남음 / 확정(+확정일·검토 시간) / 미리보기 준비됨. 클릭하면
그 영상의 기존 검토 화면(server.py + web/index.html)으로 이어서 들어간다.

왜 별도 서버인가: scripts/server.py는 영상 하나를 대상으로 띄워지는 구조다(Handler.session이
프로세스 전체에서 폴더 하나만 가리킴 - serve()가 그 전제로 짜여 있다). 그 구조를 서버 쪽에서
다중 세션으로 확장하는 건 침습적이라, 이 홈 화면은:
  1. 상태 스캔은 이 파일이 직접, 가볍게 한다 - Session을 만들지 않고 ng.json/decisions.json/
     actions.log만 읽는다(ffprobe 등 무거운 초기화·media 의존 없음 - 처리 중인 영상도 안전하게
     건너뛸 수 있어야 해서).
  2. "이어서 검토"를 누르면 그 영상 전용 server.py를 새 포트에 띄우고(이미 떠 있으면 재사용)
     브라우저를 그 포트로 보낸다 - "검토 세션 하나당 서버 프로세스 하나"라는 기존 전제를 그대로
     유지하면서 홈 화면만 얹는 가장 덜 침습적인 방법.

Usage:
    python scripts/home_server.py [--port 8764] [--no-open]
"""
from __future__ import annotations
import argparse
import atexit
import getpass
import json
import mimetypes
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
WEB_DIR = PROJECT_ROOT / "web"
sys.path.insert(0, str(HERE))
from common import (  # noqa: E402
    api_keys_status, edit_dir, load_env, sanitize_project_name, write_env_keys,
    RESERVED_PROJECT_NAME_RE, RESERVED_PROJECT_NAME_SUFFIXES, REQUIRED_API_KEYS,
)

BACKUP_RE = RESERVED_PROJECT_NAME_RE  # common.py와 공유 - sanitize_project_name() 참고

# scripts/server.py Session의 개인화 상수와 반드시 같은 값이어야 한다 - 저쪽 숫자가 바뀌면
# 여기 '남은 건수'도 같이 틀어진다.
PREFS_MIN_SAMPLES = 3
PREFS_MIN_RATIO = 0.75


def videos_root() -> Path:
    """videos/ 루트. VIDEO_CUT_HOME_DIR로 바꿀 수 있다 - 실제 videos/(여러 세션이 공유하는
    사용자 데이터)를 안 건드리고 합성 픽스처로 상태 분기(확정/미리보기 등)를 검증할 때 씀."""
    override = os.environ.get("VIDEO_CUT_HOME_DIR")
    return Path(override).resolve() if override else PROJECT_ROOT / "videos"


def is_project_folder(p: Path) -> bool:
    """`videos/<이름>/raw.mp4`가 있는 폴더만 - *_final_gold, *.backup-* 접미사는 실제
    진행 중인 프로젝트가 아니라 평가용/과거 스냅샷이라 제외한다."""
    if not p.is_dir() or p.name.startswith("."):
        return False
    if p.name.endswith(RESERVED_PROJECT_NAME_SUFFIXES) or BACKUP_RE.search(p.name):
        return False
    return (p / "raw.mp4").exists()


def _read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return default


def _user_prefs() -> dict:
    """scripts/server.py의 prefs_path()/user_id()와 같은 경로 - 케이스별(A/B/E...) 누적
    cut/keep 비율로 REVIEW 항목을 사람 손 없이 미리 채우는 "정답지"(영상을 넘어 누적, 홈 화면
    쪽은 이걸 적용 안 하면 아직 한 번도 안 연 영상의 '남은 건수'가 실제 검토 화면보다 훨씬
    커 보인다 - BS183으로 직접 확인: 이 적용 없이는 33건, 적용하면 실제 화면과 같은 12건)."""
    user = os.environ.get("VIDEO_CUT_USER") or getpass.getuser()
    return _read_json(Path.home() / ".video-cut" / "prefs" / f"{user}.json", {"ng_case": {}})


def _pref_action_for_case(case: str | None, prefs: dict) -> str | None:
    """scripts/server.py Session._pref_action_for_case()와 동일 - 같이 고칠 것."""
    if not case:
        return None
    counts = prefs.get("ng_case", {}).get(case)
    if not counts:
        return None
    total = counts.get("cut", 0) + counts.get("keep", 0)
    if total < PREFS_MIN_SAMPLES:
        return None
    cut_ratio = counts.get("cut", 0) / total
    if cut_ratio >= PREFS_MIN_RATIO:
        return "cut"
    if cut_ratio <= 1 - PREFS_MIN_RATIO:
        return "keep"
    return None


def _display_route(item: dict) -> str:
    """scripts/server.py의 Session._display_route()와 같은 규칙이어야 한다(route/flag를
    AUTO_SAFE/REVIEW/KEEP으로 바꾸는 09-29 max-delete 라우팅) - 저쪽이 바뀌면 여기도 같이
    고친다. Session 전체를 만들진 않는다: ffprobe로 media를 프로브하는 등 '몇 건 남았나'
    하나 보자고 하기엔 무거운 초기화가 많고, 처리 중/미디어가 아직 없는 영상도 있어서다."""
    route = item.get("route")
    if route == "KEEP":
        return "KEEP"
    return "REVIEW" if item.get("flag") == "restore" else "AUTO_SAFE"


def _ng_pending(ng: list[dict], dec: dict, prefs: dict) -> int:
    """scripts/server.py Session._review_estimate()의 ng 쪽과 같은 셈 - REVIEW로 분류됐지만
    아직 사람이 손대지 않은(skip도 아닌) 항목 수. decisions.json에 그 인덱스가 아직 없으면(=
    한 번도 열어본 적 없는 영상, 또는 그 뒤에 새로 생긴 항목) Session._default_decisions()와
    같은 길로 개인화 정답지를 라이브로 적용해야 한다 - 이미 저장된 decisions.json은 그 안의
    'by' 값을 그대로 믿는다(한 번 'auto'로 저장되면 그 뒤 정답지가 쌓여도 다시 안 바뀐다 -
    server.py _merge_defaults()가 실제로 그렇게 동작함)."""
    n = 0
    ng_dec = dec.get("ng", {})
    for i, item in enumerate(ng):
        if _display_route(item) != "REVIEW":
            continue
        d = ng_dec.get(str(i))
        if d is None:
            case = (item.get("llm_classification") or {}).get("case")
            by = "personalized" if _pref_action_for_case(case, prefs) else "auto"
        else:
            if d.get("skipped"):
                continue
            by = d.get("by")
        if by in ("personalized", "pattern_suggestion", "user", "gold"):
            continue
        n += 1
    return n


def _block_pending(blocks: list[dict], dec: dict) -> int:
    n = 0
    block_dec = dec.get("blocks", {})
    for b in blocks:
        bd = block_dec.get(str(b.get("id")))
        if not bd:
            n += 1
            continue
        if bd.get("skipped"):
            continue
        if not bd.get("decided"):
            n += 1
    return n


def _review_started_at(log_path: Path) -> datetime | None:
    """scripts/server.py Session.review_started_at()과 동일 - actions.log의 첫 'decision'
    이벤트 시각. 결정이 하나도 없으면(정답지 대조로 바로 확정한 경우 등) None."""
    if not log_path.exists():
        return None
    for line in log_path.read_text().splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("event") == "decision":
            try:
                return datetime.fromisoformat(rec["at"])
            except ValueError:
                return None
    return None


def project_status(folder: Path) -> dict:
    """영상 폴더 하나의 상태를 읽기 전용으로 계산한다 - Session을 만들지 않으니 server.py가
    같은 폴더를 동시에 떠 있는 동안 호출해도 안전하다(둘 다 읽기만 함)."""
    edit = folder / "edit"
    ng_path = edit / "ng.json"
    info: dict = {"name": folder.name}

    # 정렬용 "마지막 활동 시각" - decisions.json(검토 중이면 매 결정마다 갱신) > actions.log >
    # ng.json(처리만 끝나고 아직 한 번도 안 연 경우) > raw.mp4(처리조차 시작 안 한 경우) 순으로
    # 존재하는 첫 파일의 mtime을 쓴다.
    last = None
    for c in (edit / "decisions.json", edit / "actions.log", ng_path, folder / "raw.mp4"):
        try:
            last = c.stat().st_mtime
        except OSError:
            continue
        break
    info["last_activity"] = last
    info["managed"] = _is_managed(folder.name)

    if not ng_path.exists():
        info["status"] = "processing"
        return info

    ng = _read_json(ng_path, [])
    dec = _read_json(edit / "decisions.json", {})
    confirmed_at = dec.get("confirmed_at")
    info["preview_ready"] = (folder / "preview.mp4").exists()

    if confirmed_at:
        info["status"] = "confirmed"
        info["confirmed_at"] = confirmed_at
        by_counts: dict[str, int] = {}
        for v in dec.get("ng", {}).values():
            by_counts[v.get("by", "auto")] = by_counts.get(v.get("by", "auto"), 0) + 1
        started = _review_started_at(edit / "actions.log")
        review_sec = None
        # by='gold'(정답지 대조 확정)가 섞여 있으면 actions.log의 첫 decision이 이번 검토의
        # 진짜 시작이 아닐 수 있다 - server.py의 receipt()와 같은 이유로 그럴 땐 null.
        if started and not by_counts.get("gold"):
            try:
                review_sec = round((datetime.fromisoformat(confirmed_at) - started).total_seconds())
            except ValueError:
                review_sec = None
        info["review_sec"] = review_sec
        return info

    blocks = _read_json(edit / "speaker_blocks.json", {"blocks": []}).get("blocks", [])
    info["status"] = "reviewing"
    info["pending"] = _ng_pending(ng, dec, _user_prefs()) + _block_pending(blocks, dec)
    info["total"] = sum(1 for it in ng if _display_route(it) == "REVIEW") + len(blocks)
    return info


def scan_projects() -> list[dict]:
    root = videos_root()
    if not root.is_dir():
        return []
    out = [project_status(p) for p in sorted(root.iterdir()) if is_project_folder(p)]
    out.sort(key=lambda r: r.get("last_activity") or 0, reverse=True)
    return out


# --------------------------------------------------------------------- "이어서 검토" (spawn)
# review 세션 하나당 server.py 프로세스 하나 - 이 홈 서버가 떠 있는 동안 이름별로 하나씩만
# 띄우고 재사용한다. 홈 서버가 죽으면 atexit으로 정리하지만, 터미널을 강제 종료하는 등 비정상
# 종료 시엔 기존에 `run.py --serve`를 손으로 띄울 때와 마찬가지로 고아 프로세스가 남을 수 있다.
_active_lock = threading.Lock()
_active: dict[str, dict] = {}
_uploading: set[str] = set()  # "영상 생성" 업로드가 진행 중인 이름 - 같은 제목 동시 생성 레이스 방지


def _is_managed(name: str) -> bool:
    """이 홈 서버가 그 이름의 server.py/run.py를 지금 살아서 띄우고 있는지 - project_status()가
    "처리 중" 카드를 클릭 가능하게 할지(막 업로드해서 아직 ng.json이 없는 경우) 판단하는 데 씀."""
    with _active_lock:
        a = _active.get(name)
        return bool(a and a["proc"].poll() is None)


def _port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def _port_listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        try:
            s.connect(("127.0.0.1", port))
            return True
        except OSError:
            return False


def _alloc_port() -> int:
    taken = {a["port"] for a in _active.values()}
    for port in range(8766, 8900):
        if port not in taken and _port_free(port):
            return port
    raise RuntimeError("빈 포트를 못 찾았습니다")


def open_review(name: str) -> dict:
    root = videos_root()
    folder = root / name
    if not is_project_folder(folder):
        raise ValueError(f"알 수 없는 영상: {name}")

    with _active_lock:
        active = _active.get(name)
        if active and active["proc"].poll() is None and _port_listening(active["port"]):
            return {"url": f"http://127.0.0.1:{active['port']}/"}

    # "영상 생성"으로 막 업로드돼 아직 ng.json이 없어도(= 파이프라인 처리 중), 이 홈 서버가
    # 이미 그 run.py를 띄워 관리 중이면 그 진행 화면으로 보낸다 - ng.json 유무 체크는 그 뒤,
    # 즉 "CLI로 raw.mp4만 떨궈놓고 아직 run.py를 한 번도 안 돌린" 레거시 케이스만 거른다.
    if not (folder / "edit" / "ng.json").exists() and name not in _active:
        raise ValueError("아직 처리 중입니다 - 처리가 끝난 뒤에 검토할 수 있어요")

    with _active_lock:
        active = _active.get(name)
        if active and active["proc"].poll() is None and _port_listening(active["port"]):
            return {"url": f"http://127.0.0.1:{active['port']}/"}

        port = _alloc_port()
        log_path = folder / "edit" / "server.log"
        log_f = open(log_path, "a")
        proc = subprocess.Popen(
            [sys.executable, str(HERE / "server.py"), str(folder), "--port", str(port), "--no-open"],
            cwd=str(PROJECT_ROOT), stdin=subprocess.DEVNULL, stdout=log_f, stderr=subprocess.STDOUT,
        )
        _active[name] = {"port": port, "proc": proc, "log": log_f}

    deadline = time.time() + 12
    while time.time() < deadline:
        if _active[name]["proc"].poll() is not None:
            raise RuntimeError(f"검토 서버가 바로 종료됐습니다 - {log_path} 확인")
        if _port_listening(port):
            return {"url": f"http://127.0.0.1:{port}/"}
        time.sleep(0.2)
    raise RuntimeError("검토 서버가 제시간에 뜨지 않았습니다")


# --------------------------------------------------------------------------- 영상 생성 (업로드)

def create_project(title: str, content_length: int, rfile) -> dict:
    """"영상 생성" 폼 하나를 처리한다 - 제목 검증 → API 키 보유 확인 → 중복 확인까지 전부
    바이트를 읽기 **전에** 끝낸 뒤에만 rfile을 청크 단위로 raw.mp4.part에 스트리밍 쓰기하고
    (대용량 영상을 한 번에 메모리에 올리지 않음), 완료되면 원자적 rename으로 raw.mp4를
    확정하고 run.py를 백그라운드로 기동한다. 실패는 ValueError(그대로 사용자에게 보여줄 메시지)
    또는 RuntimeError로 던진다."""
    name = sanitize_project_name(title)

    missing = [k["key"] for k in api_keys_status() if not k["set"]]
    if missing:
        raise ValueError(f"API 키가 없습니다 - 설정 패널에서 먼저 등록하세요 ({', '.join(missing)})")

    folder = videos_root() / name
    if (folder / "raw.mp4").exists():
        raise ValueError("이미 같은 이름의 영상이 있습니다 - 다른 제목을 입력하세요")

    with _active_lock:
        if name in _uploading:
            raise ValueError("이미 같은 이름으로 업로드가 진행 중입니다")
        _uploading.add(name)

    try:
        folder.mkdir(parents=True, exist_ok=True)
        part = folder / "raw.mp4.part"
        try:
            _stream_to_file(rfile, part, content_length)
            part.rename(folder / "raw.mp4")
        except Exception:
            part.unlink(missing_ok=True)
            try:
                if folder.is_dir() and not any(folder.iterdir()):
                    folder.rmdir()
            except OSError:
                pass
            raise

        edit_dir(folder)  # run.py가 edit/run.log를 열 수 있도록 미리 만들어 둠
        port = _alloc_port()
        log_path = folder / "edit" / "run.log"
        log_f = open(log_path, "a")
        proc = subprocess.Popen(
            [sys.executable, str(HERE / "run.py"), str(folder), "--port", str(port), "--no-open"],
            cwd=str(PROJECT_ROOT), stdin=subprocess.DEVNULL, stdout=log_f, stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        with _active_lock:
            _active[name] = {"port": port, "proc": proc, "log": log_f}
    finally:
        with _active_lock:
            _uploading.discard(name)

    deadline = time.time() + 15
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"처리가 바로 종료됐습니다 - {log_path} 확인")
        if _port_listening(port):
            return {"name": name, "url": f"http://127.0.0.1:{port}/"}
        time.sleep(0.2)
    raise RuntimeError("처리 서버가 제시간에 뜨지 않았습니다")


def _stream_to_file(rfile, dest: Path, length: int, chunk_size: int = 4 * 1024 * 1024) -> None:
    remaining = length
    with dest.open("wb") as f:
        while remaining > 0:
            chunk = rfile.read(min(chunk_size, remaining))
            if not chunk:
                raise ConnectionError("업로드가 중간에 끊겼습니다")
            f.write(chunk)
            remaining -= len(chunk)


# ------------------------------------------------------------------------------ 설정: ffmpeg 설치
# brew install ffmpeg는 몇 분 걸릴 수 있어 POST로 기동만 하고(즉시 응답), 별도 스레드가
# proc.wait()하며 아래 상태를 갱신 - 프런트는 /api/setup/ffmpeg/status를 폴링한다
# (web/index.html의 pipelineBoot()와 같은 재귀 setTimeout 폴링 패턴).
_ffmpeg_install_lock = threading.Lock()
_ffmpeg_install_state: dict = {"running": False, "done": False, "ok": None, "error": None}


def ffmpeg_status() -> dict:
    return {"ffmpeg": shutil.which("ffmpeg") is not None,
            "ffprobe": shutil.which("ffprobe") is not None,
            "brew": shutil.which("brew") is not None}


def start_ffmpeg_install() -> dict:
    if shutil.which("brew") is None:
        raise ValueError("Homebrew가 설치돼 있지 않습니다 - https://brew.sh 에서 먼저 설치해주세요")
    with _ffmpeg_install_lock:
        if _ffmpeg_install_state["running"]:
            return {"started": True}  # 이미 진행 중 - 새로 기동하지 않고 그대로 진행 상태 알림
        _ffmpeg_install_state.update(running=True, done=False, ok=None, error=None)

    def _run():
        try:
            proc = subprocess.run(["brew", "install", "ffmpeg"], capture_output=True, text=True, timeout=600)
            ok = proc.returncode == 0 and shutil.which("ffmpeg") is not None
            with _ffmpeg_install_lock:
                _ffmpeg_install_state.update(running=False, done=True, ok=ok,
                                              error=None if ok else (proc.stderr or proc.stdout)[-800:])
        except Exception as e:
            with _ffmpeg_install_lock:
                _ffmpeg_install_state.update(running=False, done=True, ok=False, error=str(e))

    threading.Thread(target=_run, daemon=True).start()
    return {"started": True}


# ----------------------------------------------------------------------------------- 업데이트
# 이 저장소는 claude plugin 마켓플레이스 설치가 아니라 ~/.claude/skills/video-cut 심볼릭 링크의
# 실제 대상이다(SKILL.md "설치와 업데이트" 참고) - 그래서 "업데이트"는 곧 git pull. fetch는
# 네트워크 호출이라 폴링마다 부르지 않고 백그라운드 스레드가 5분 간격으로 갱신해 캐시한다.
_update_cache_lock = threading.Lock()
_update_cache: dict = {"behind": 0, "checked_at": None}
_pull_lock = threading.Lock()


def _run_git(args: list[str], timeout: int = 15) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=timeout)


def git_is_dirty() -> bool:
    r = _run_git(["status", "--porcelain"])
    return bool(r.stdout.strip())


def git_current() -> dict:
    r = _run_git(["log", "-1", "--pretty=format:%h|%s"])
    sha, _, subject = r.stdout.partition("|")
    return {"sha": sha, "subject": subject}


def git_recent_log(limit: int = 20) -> list[dict]:
    r = _run_git(["log", f"-{limit}", "--pretty=format:%h|%ad|%an|%s", "--date=short"])
    out = []
    for line in r.stdout.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            out.append({"sha": parts[0], "date": parts[1], "author": parts[2], "subject": parts[3]})
    return out


def _update_refresh_loop() -> None:
    while True:
        try:
            _run_git(["fetch", "origin"], timeout=30)
            r = _run_git(["rev-list", "--count", "HEAD..origin/main"])
            behind = int(r.stdout.strip() or 0)
            with _update_cache_lock:
                _update_cache.update(behind=behind, checked_at=datetime.now().isoformat(timespec="seconds"))
        except Exception:
            pass  # 네트워크 없음 등 - 다음 주기에 재시도, 배너는 그냥 안 뜬 채로 둠
        time.sleep(300)


def update_status() -> dict:
    with _update_cache_lock:
        cached = dict(_update_cache)
    cur = git_current()
    return {"dirty": git_is_dirty(), "behind": cached["behind"], "checked_at": cached["checked_at"],
            "current_sha": cur["sha"], "current_subject": cur["subject"]}


def git_pull() -> dict:
    if not _pull_lock.acquire(blocking=False):
        raise ValueError("이미 업데이트가 진행 중입니다")
    try:
        if git_is_dirty():
            raise ValueError("커밋되지 않은 변경사항이 있어 건너뜁니다 - 터미널에서 직접 정리한 뒤 다시 시도하세요")
        r = _run_git(["pull", "--ff-only"], timeout=60)
        if r.returncode != 0:
            raise ValueError((r.stderr or r.stdout).strip()[-800:] or "git pull 실패")
        with _update_cache_lock:
            _update_cache.update(behind=0, checked_at=datetime.now().isoformat(timespec="seconds"))
        return {"output": r.stdout.strip()}
    finally:
        _pull_lock.release()


@atexit.register
def _cleanup_children() -> None:
    with _active_lock:
        for a in _active.values():
            if a["proc"].poll() is None:
                a["proc"].terminate()


# --------------------------------------------------------------------------------- HTTP

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002 - stdlib signature
        pass  # 백그라운드 스캔 화면이라 기본 접속 로그로 터미널을 채우지 않는다

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/home.html"):
            return self._file(WEB_DIR / "home.html", "text/html; charset=utf-8")
        if path == "/api/projects":
            return self._json({"projects": scan_projects()})
        if path == "/api/setup":
            return self._json({"keys": api_keys_status(), **ffmpeg_status()})
        if path == "/api/setup/ffmpeg/status":
            with _ffmpeg_install_lock:
                return self._json(dict(_ffmpeg_install_state))
        if path == "/api/update/status":
            try:
                return self._json(update_status())
            except Exception as e:
                return self._json({"error": str(e)}, 500)
        if path == "/api/update/log":
            q = parse_qs(urlsplit(self.path).query)
            limit = int((q.get("limit") or ["20"])[0])
            return self._json({"commits": git_recent_log(limit)})
        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if path.startswith("/static/"):
            f = WEB_DIR / path[len("/static/"):]
            if f.is_file():
                return self._file(f, mimetypes.guess_type(str(f))[0] or "application/octet-stream")
        self.send_error(404)

    def do_POST(self):
        path = self.path.split("?")[0]
        if path == "/api/videos/create":
            return self._handle_create_project()

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        if path == "/api/open":
            try:
                result = open_review(str(body.get("name", "")))
                return self._json({"ok": True, **result})
            except Exception as e:  # surface to the UI instead of a silent 500
                return self._json({"ok": False, "error": str(e)}, 400)
        if path == "/api/setup/keys":
            valid_keys = {key for key, _, _ in REQUIRED_API_KEYS}
            pairs = {k: v for k, v in body.items()
                     if k in valid_keys and isinstance(v, str) and v.strip() and "\n" not in v}
            if not pairs:
                return self._json({"ok": False, "error": "등록할 키가 없습니다"}, 400)
            write_env_keys({k: v.strip() for k, v in pairs.items()})
            return self._json({"ok": True, "keys": api_keys_status(), **ffmpeg_status()})
        if path == "/api/setup/ffmpeg/install":
            try:
                return self._json({"ok": True, **start_ffmpeg_install()})
            except ValueError as e:
                return self._json({"ok": False, "error": str(e)}, 400)
        if path == "/api/update/pull":
            try:
                return self._json({"ok": True, **git_pull()})
            except ValueError as e:
                return self._json({"ok": False, "error": str(e)}, 409)
        self.send_error(404)

    def _handle_create_project(self):
        q = parse_qs(urlsplit(self.path).query)
        title = (q.get("title") or [""])[0]
        length = int(self.headers.get("Content-Length", 0))
        try:
            result = create_project(title, length, self.rfile)
            return self._json({"ok": True, **result})
        except ValueError as e:
            return self._json({"ok": False, "error": str(e)}, 400)
        except Exception as e:
            return self._json({"ok": False, "error": str(e)}, 500)

    def _json(self, data, status: int = 200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def _file(self, path: Path, ctype: str):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


def serve(port: int, open_browser: bool) -> None:
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"project home: {url}   (videos: {videos_root()})")
    threading.Thread(target=_update_refresh_loop, daemon=True).start()
    if open_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8764)
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()
    load_env()
    serve(args.port, not args.no_open)


if __name__ == "__main__":
    main()
