"""Shared helpers for the video-cut pipeline: paths, .env loading, transcript access."""
from __future__ import annotations
import getpass
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2026-09-30: 스킬을 설치한 다른 사용자를 위한 온보딩 - 키가 없으면 여기서 물어봐서 .env에
# 저장한다. (키, 설명, 발급 페이지) 튜플 목록.
REQUIRED_API_KEYS = [
    ("ANTHROPIC_API_KEY", "Claude API 키 - NG 판별·분류·전체 검토에 씀", "https://console.anthropic.com/settings/keys"),
    ("ELEVENLABS_API_KEY", "ElevenLabs API 키 - Scribe 전사에 씀", "https://elevenlabs.io/app/settings/api-keys"),
]
# 없어도 컷편집·분할은 돈다 - 설정 게이트·영상 생성 검사에서 빠진다. 분할의 인트로 이미지 생성에만 쓴다.
OPTIONAL_API_KEYS = [
    ("GEMINI_API_KEY", "Gemini API 키 (선택) - 분할 편마다 인트로 이미지 생성에 씀", "https://aistudio.google.com/apikey"),
]

# 채널 공통 이미지 - 사용자 브랜드 자산이라 git에서 뺀다(.gitignore의 brand/). 홈 환경설정에서 올린다.
BRAND_DIR = PROJECT_ROOT / "brand"
BRAND_OUTRO = BRAND_DIR / "outro.png"

# 10-01 (홈 화면 영상 생성): *_final_gold/*.backup-*는 평가용/과거 스냅샷 접미사라 실제
# 프로젝트로 취급하지 않는다 - scripts/home_server.py의 is_project_folder()와 여기
# sanitize_project_name()이 같은 규칙을 공유해야, 웹에서 만든 이름이 우연히 이 패턴과 겹쳐
# "카드에 안 뜨는 유령 프로젝트"가 되는 사고를 막는다.
RESERVED_PROJECT_NAME_SUFFIXES = ("_final_gold",)
RESERVED_PROJECT_NAME_RE = re.compile(r"\.backup-")


def sanitize_project_name(raw: str) -> str:
    """홈 화면 "영상 생성" 폼의 제목 -> `video-edit/<name>` 폴더명. 경로 탈출·예약 패턴을 막는다
    (기존에 이런 검증 함수가 없었음 - video_dir() 등은 전부 사람이 직접 만든 폴더명을 그대로
    신뢰하는 전제라 새로 만듦)."""
    name = raw.strip()
    if not name:
        raise ValueError("제목을 입력하세요")
    if len(name) > 150:
        raise ValueError("제목이 너무 깁니다 (150자 이하)")
    if "/" in name or "\\" in name or ".." in name:
        raise ValueError("폴더 이름에 쓸 수 없는 문자가 있습니다 (/, \\, ..)")
    if name.startswith("."):
        raise ValueError("점(.)으로 시작하는 이름은 쓸 수 없습니다")
    if name.endswith(RESERVED_PROJECT_NAME_SUFFIXES) or RESERVED_PROJECT_NAME_RE.search(name):
        raise ValueError("이 이름은 내부적으로 예약돼 있어 쓸 수 없습니다 - 다른 제목을 입력하세요")
    return name


# pyproject.toml 의존성(+librosa가 끌고 오는 numpy)의 import 이름 - 하나라도 없으면 프로젝트
# 환경(.venv)이 아닌 파이썬으로 실행된 것이다.
_REQUIRED_MODULES = ("anthropic", "pydantic", "requests", "librosa", "numpy")


def ensure_project_python() -> None:
    """진입점(home_server.py/run.py/server.py)이 맨 처음 부른다. 프로젝트 의존성이 없는 파이썬
    (예: `uv run` 없이 `python3 scripts/home_server.py`)으로 실행됐으면 `uv run --project`로
    자기 자신을 다시 실행해 .venv로 갈아탄다.

    10-06 실제 사고(다른 컴퓨터): 홈 서버가 시스템 파이썬으로 떠 있었는데 홈 서버 자체는
    표준 라이브러리만 써서 멀쩡히 돌았다. 그런데 자식(run.py 단계들, server.py)을 전부
    sys.executable로 띄우므로 - "정리"는 통과하고 "전사"는 requests가 없어 종료 코드 1, 검토
    서버는 numpy가 없어 시작 직후 종료. 증상이 단계마다 엉뚱하게 흩어져 원인을 찾기 어려웠다."""
    migrate_work_dirs()
    import importlib.util
    missing = [m for m in _REQUIRED_MODULES if importlib.util.find_spec(m) is None]
    if not missing:
        return
    import shutil
    uv = shutil.which("uv")
    if os.environ.get("VIDEO_CUT_REEXEC") or uv is None:
        # 이미 uv로 다시 실행했는데도 없음(설치 실패 등), 또는 uv 자체가 없음 - 루프 대신 멈춘다
        sys.exit(f"필요한 파이썬 라이브러리가 없습니다({', '.join(missing)}) - 현재 파이썬: {sys.executable}\n"
                 + ("uv를 설치한 뒤(`brew install uv`) " if uv is None else "")
                 + f"`uv run --project {PROJECT_ROOT} python {sys.argv[0]}`로 실행하세요.")
    print(f"[env] 프로젝트 환경이 아닌 파이썬({sys.executable})으로 실행됨 - 없는 라이브러리: "
          f"{', '.join(missing)}. uv로 다시 실행합니다.", flush=True)
    os.environ["VIDEO_CUT_REEXEC"] = "1"
    os.execvp(uv, [uv, "run", "--project", str(PROJECT_ROOT), "python",
                   str(Path(sys.argv[0]).resolve()), *sys.argv[1:]])


def load_env() -> None:
    """Load PROJECT_ROOT/.env into os.environ without overriding existing values."""
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def api_keys_status() -> list[dict]:
    """홈 화면 설정 패널의 `GET /api/setup`이 쓰는 상태 조회 - 값 자체는 절대 포함하지 않는다
    (네트워크 응답/devtools에 비밀값이 찍히는 걸 막음, `set`만 알려줌)."""
    load_env()
    return [
        {"key": k, "desc": desc, "url": url, "set": bool(os.environ.get(k)), "optional": optional}
        for keys, optional in ((REQUIRED_API_KEYS, False), (OPTIONAL_API_KEYS, True))
        for k, desc, url in keys
    ]


def write_env_keys(pairs: dict[str, str]) -> None:
    """`.env`에 키=값들을 쓴다 - 같은 키로 시작하는 기존 줄은 새 값으로 치환(단순 append가
    아님, 웹 설정 폼에서 키를 바꿀 때마다 중복 줄이 쌓이는 걸 막음), 없던 키만 새 줄로 추가.
    `os.environ`에도 즉시 반영한다. `ensure_api_keys()`의 CLI 저장 블록과
    `POST /api/setup/keys`(home_server.py)가 이 함수 하나를 공유 - `.env` 파싱/쓰기 로직이
    두 곳에 따로 생기지 않게."""
    env_path = PROJECT_ROOT / ".env"
    lines = env_path.read_text().splitlines() if env_path.exists() else []
    remaining = dict(pairs)
    out_lines = []
    for line in lines:
        stripped = line.strip()
        key = None
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
        if key and key in remaining:
            out_lines.append(f"{key}={remaining.pop(key)}")
        else:
            out_lines.append(line)
    for key, value in remaining.items():
        out_lines.append(f"{key}={value}")
    env_path.write_text("\n".join(out_lines) + "\n")
    for key, value in pairs.items():
        os.environ[key] = value


def ensure_api_keys() -> None:
    """`load_env()`로 이미 있는 키는 그대로 쓰고, 없는 키만 채운다.

    세 가지 실행 맥락을 구분한다:
    - **사람이 직접 터미널에서 실행** (`python scripts/run.py ...`를 손으로 침): 표준입력이
      진짜 터미널이라 `getpass`로 그 자리에서 대화식으로 물어보고 `.env`에 저장한다.
    - **홈 화면(웹) 설정 패널**: 10-01부터 1차 경로 - `web/home.html`의 설정 모달에서
      `POST /api/setup/keys`로 등록하면 `write_env_keys()`를 직접 불러 저장한다(이 함수를
      거치지 않음, 브라우저 폼 제출은 애초에 대화식 프롬프트가 필요 없다).
    - **에이전트(클로드 코드)가 스킬로 대신 실행, 또는 브라우저를 쓸 수 없는 환경**: Bash
      도구는 표준입력이 터미널이 아니라서(`sys.stdin.isatty()`가 항상 False, 2026-09-30 직접
      확인) `getpass`가 아예 작동하지 않는다 - 예전엔 여기서 조용히 넘어가 버려서 한참 뒤
      `transcribe.py`가 뜬금없이 에러를 냈다. 지금은 **필요한 키·설명·발급 링크·`.env`의
      절대경로·홈 화면 안내를 출력하고 즉시 종료**한다 - 에이전트는 이 출력을 읽으면 먼저
      "홈 화면을 열어 설정에서 등록해 주세요"라고 안내하고, 사용자가 브라우저를 쓸 수 없다고
      하면 대화로 물어서 직접 `.env`에 써주는 게 대안 경로다(`SKILL.md` "에이전트가 지킬 것"
      참고)."""
    load_env()
    missing = [(k, desc, url) for k, desc, url in REQUIRED_API_KEYS if not os.environ.get(k)]
    if not missing:
        return

    env_path = PROJECT_ROOT / ".env"

    if not sys.stdin.isatty():
        lines = [f"필요한 API 키가 없습니다 - 홈 화면(http://127.0.0.1:8764/) 설정 패널에서 등록하거나,"
                  f" {env_path}에 아래 형식으로 한 줄씩 직접 추가해야 합니다:"]
        for key, desc, url in missing:
            lines.append(f"  {key}=<값>   # {desc}, 발급: {url}")
        sys.exit("\n".join(lines))

    print("\n처음 실행하시는군요 - 필요한 API 키를 한 번만 물어볼게요. 저장되면 다음부터는 안 물어봅니다.\n")
    pairs = {}
    for key, desc, url in missing:
        print(f"- {key}: {desc}\n  발급: {url}")
        value = ""
        while not value:
            value = getpass.getpass(f"  {key} 입력(화면에 안 보임): ").strip()
        pairs[key] = value
    write_env_keys(pairs)
    print(f"\n{env_path}에 저장했습니다. 다음부터는 안 물어봅니다.\n")


# 작업 폴더 이름 (10-08 videos/ -> video-edit/, splits/ -> auto-split/ - 사용자 "폴더가 직관적이지 않다". video-edit는
# 컷편집뿐 아니라 앞으로 들어갈 비주얼 자막·영상/이미지 삽입까지 담는 영상 편집 전반이라 cut-edit 대신 이 이름).
# 옛 이름 폴더는 migrate_work_dirs()가 처음 실행될 때 새 이름으로 옮긴다.
VIDEO_EDIT_DIR = "video-edit"
SPLIT_DIR = "auto-split"
_LEGACY_DIRS = (("videos", VIDEO_EDIT_DIR), ("splits", SPLIT_DIR))


def migrate_work_dirs(base: Path = PROJECT_ROOT) -> None:
    """base 아래 옛 작업 폴더(videos/, splits/)를 새 이름으로 옮긴다. 새 이름이 이미 있으면 건드리지 않는다
    (둘 다 있으면 사용자가 정리해야 하니 경고만). 옮긴 뒤 분할 프로젝트의 source.mp4가 옛 컷편집 폴더를
    절대경로로 가리키는 링크면 새 경로로 다시 잇는다 - 상대 링크는 폴더째 옮겨도 그대로 맞는다."""
    for old, new in _LEGACY_DIRS:
        src, dst = base / old, base / new
        if src.is_dir() and not src.is_symlink():
            if dst.exists():
                print(f"[migrate] {src}와 {dst}가 둘 다 있습니다 - {old}/ 안의 프로젝트를 {new}/로 직접 옮겨 주세요",
                      file=sys.stderr)
                continue
            src.rename(dst)
            print(f"[migrate] {old}/ -> {new}/", file=sys.stderr)
    old_cut = str(base / "videos") + os.sep
    for link in (base / SPLIT_DIR).glob(f"*/{SPLIT_SOURCE_NAME}"):
        if link.is_symlink():
            target = os.readlink(link)
            if target.startswith(old_cut):
                link.unlink()
                link.symlink_to(str(base / VIDEO_EDIT_DIR) + os.sep + target[len(old_cut):])


def video_dir(name_or_path: str | Path) -> Path:
    """Resolve `video-edit/<name>` or an explicit folder path."""
    migrate_work_dirs()
    p = Path(name_or_path)
    if p.is_dir():
        return p.resolve()
    candidate = PROJECT_ROOT / VIDEO_EDIT_DIR / str(name_or_path)
    if candidate.is_dir():
        return candidate.resolve()
    raise SystemExit(f"video folder not found: {name_or_path} (looked in {candidate})")


SPLIT_SOURCE_NAME = "source.mp4"


def is_insert_only(folder: Path) -> bool:
    """10-09: 편집이 끝난 완성본에 인서트만 넣는 프로젝트 - 처리는 정리·전사까지만, 검토는 인서트 편집 화면으로."""
    try:
        return json.loads((folder / "edit" / "project.json").read_text()).get("mode") == "insert"
    except (OSError, ValueError):
        return False


def mark_insert_only(folder: Path) -> None:
    (folder / "edit").mkdir(parents=True, exist_ok=True)
    (folder / "edit" / "project.json").write_text(json.dumps({"mode": "insert"}))


def is_split_project(folder: Path) -> bool:
    """주제별 분할(docs/백로그/주제별-분할.md) 폴더인지 - 컷편집과 완전히 분리된 작업이라 폴더
    구조도 다르다(auto-split/<이름>/source.mp4 + work/). 전사·음향 지도 코드는 그대로 공유하므로
    작업 폴더와 원본 위치만 여기서 갈라 준다."""
    return (folder / SPLIT_SOURCE_NAME).exists()


def edit_dir(folder: Path) -> Path:
    d = folder / ("work" if is_split_project(folder) else "edit")
    d.mkdir(exist_ok=True)
    return d


def source_media(folder: Path) -> Path:
    """clean.mp4 when it exists (FCP-compatible, faststart), else raw.mp4. 분할 프로젝트는 source.mp4."""
    if is_split_project(folder):
        return folder / SPLIT_SOURCE_NAME
    clean = folder / "edit" / "clean.mp4"
    if clean.exists():
        return clean
    raw = folder / "raw.mp4"
    if raw.exists():
        return raw
    raise SystemExit(f"no raw.mp4 in {folder}")


def load_transcript(folder: Path) -> dict:
    return json.loads((edit_dir(folder) / "transcript.json").read_text())


def words_only(transcript: dict) -> list[dict]:
    """Spoken words in order, each tagged with its index into this list (`wi`)."""
    out = []
    for w in transcript["words"]:
        if w["type"] == "word":
            out.append({**w, "wi": len(out)})
    return out


def norm(text: str) -> str:
    return text.strip().rstrip(".,!?~…。，").lower()


# 업데이트·마이그레이션 (docs/업데이트와-마이그레이션.md): edit/ 산출물마다 "지금 코드가 이
# 파일을 쓰면 몇 버전이 되는가"를 기록해 둔다. 파일 안에 직접 못 넣는 이유는 ng.json처럼
# 최상위가 list인 산출물이 있어서다(dict 전용 필드로는 못 끼워 넣음) - 그래서 edit/ 폴더
# 옆에 .schema_versions.json 사이드카로 따로 둔다. 지금은 전부 1(이 체계를 도입하는 시점의
# 기준선 - 아직 스키마가 바뀐 적은 없음). 스키마를 바꾸는 변경이 생기면 그 파일의 숫자만
# 올리고 scripts/migrate.py의 MIGRATIONS에 변환 함수를 추가한다.
SCHEMA_VERSIONS: dict[str, int] = {
    "transcript.json": 1,
    "prosody.json": 1,
    "audio_map.json": 1,
    "speaker_blocks.json": 1,
    "ng_candidates.json": 1,
    "regions.json": 1,
    "ng_classified.json": 1,
    "ng.json": 1,
    "draft_cuts.json": 1,
    "seams.json": 1,
    "final_cuts.json": 1,
    "global_review.json": 1,
    "pauses.json": 1,
    "decisions.json": 1,
    "edl.json": 1,
}


def _stamp_schema_version(path: Path) -> None:
    version = SCHEMA_VERSIONS.get(path.name)
    if version is None:
        return  # 이 체계가 모르는 파일(임시 산출물 등) - 건드리지 않음
    manifest_path = path.parent / ".schema_versions.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest[path.name] = version
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    _stamp_schema_version(path)


def pid_alive(pid: int | None) -> bool:
    """run.py가 pipeline_status.json에 남긴 pid가 아직 살아있는지. 홈 서버가 띄운 run.py는
    죽어도 홈 서버가 poll()로 거둬가기 전까진 좀비로 남아 os.kill(pid, 0)이 성공한다 - 그래서
    ps로 상태가 'Z'인지까지 본다(10-06: 처리 프로세스가 죽었는데 진행 화면이 "처리 준비 중"
    스피너로 영원히 도는 문제)."""
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    try:
        stat = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True,
                              text=True, timeout=2).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return True  # 확인 못 하면 살아있다고 본다 - 멀쩡한 처리를 실패로 오표시하지 않게
    return bool(stat) and not stat.startswith("Z")


def pipeline_log_tail(folder: Path, max_lines: int = 60) -> str | None:
    """edit/run.log에서 실패한 단계의 출력만 - run.py step()이 단계마다 찍는 "== 제목" 줄부터
    끝까지. 그냥 마지막 N줄을 자르면 run.py 자신의 traceback만 남고 진짜 원인(ffmpeg/API 에러
    문구)은 그 위에 있어 잘려 나갔다. 진행 화면(server.py)과 홈 화면 오류 창(home_server.py)이
    같이 쓴다."""
    try:
        lines = (folder / "edit" / "run.log").read_text(errors="replace").splitlines()
    except OSError:
        return None
    starts = [i for i, ln in enumerate(lines) if ln.startswith("== ")]
    section = lines[starts[-1]:] if starts else lines
    return "\n".join(section[-max_lines:]) or None


def read_pipeline_status(folder: Path) -> dict | None:
    """run.py가 남긴 edit/pipeline_status.json - state는 running/paused/stopped/error/done(paused·
    stopped는 진행 화면의 일시정지·중단 버튼이 server.py에서 기록). 파일이 없거나 pid가
    없는 옛 형식(10-06 이전 run.py)이면 None - 그런 폴더는 예전 기준(전사·NG 파일 유무)대로
    다룬다. state가 running/paused인데 그 pid가 죽었으면 여기서 error로 바꿔 돌려준다 - 검토 서버와
    홈 서버가 같은 판정을 쓰게 한 곳에 둔다."""
    try:
        data = json.loads((folder / "edit" / "pipeline_status.json").read_text())
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or not data.get("pid"):
        return None
    if data.get("state") in ("running", "paused") and not pid_alive(data["pid"]):
        data["state"] = "error"
        data["error"] = "처리 프로세스가 예기치 않게 종료됐습니다"
    return data


# 점버전 모델(예: Opus 5.5, Fable 5.1)은 thinking.type.disabled를 거부하고 adaptive+effort만
# 받는다 - 버전 없는 모델(claude-sonnet-5 등)과는 다른 API 계약. global_review.py의 Fable
# 처리에서 먼저 발견됐고(2026-09-29), claude-opus-5 -> claude-opus-5-5로 모델 ID를 올린 뒤
# 실제로 opus 쪽 thinking-disabled 호출이 처음 돌아간 순간(seam_refine.py judge_batch,
# 2026-09-29) 같은 오류로 재발 - 그래서 개별 호출부마다 분기하는 대신 여기 한 곳에 모은다.
NEW_THINKING_CONTRACT_MODELS = {"claude-opus-5-5", "claude-fable-5-1"}


def thinking_kwargs(model: str, effort: str = "low") -> dict:
    """anthropic client.messages.parse()에 그대로 풀어 넣을 thinking(+output_config) kwargs."""
    if model in NEW_THINKING_CONTRACT_MODELS:
        return {"thinking": {"type": "adaptive"}, "output_config": {"effort": effort}}
    return {"thinking": {"type": "disabled"}}


# R8(백로그/R8-실패-대응.md) "남은 것: 영수증에 영상당 처리 비용 추정 표시" - USD/1M토큰 가격표.
# `claude-api` 스킬의 캐시된 가격표(2026-06-24)에서 이 파이프라인이 실제로 부르는 모델 문자열만
# 그대로 가져왔다 - 추측하지 않음. cache_write/cache_read는 ephemeral(5분) 프롬프트 캐시 단가 -
# 2026-10-01 현재 이 helper를 쓰는 6개 호출부 중 cache_control을 쓰는 곳은 없어서(grep으로 확인)
# 실제로는 안 쓰이지만, 나중에 캐싱을 넣었을 때 조용히 잘못 계산되는 걸 막기 위해 남겨 둔다.
# 새 호출부가 여기 없는 모델을 쓰게 되면 가격을 먼저 이 표에 추가할 것 - 추측해서 넣지 말 것.
LLM_PRICING_USD_PER_MTOK: dict[str, dict[str, float]] = {
    "claude-opus-5-5":           {"input": 4.00, "output": 20.00, "cache_write": 5.00, "cache_read": 0.20},
    "claude-sonnet-5":           {"input": 2.00, "output": 10.00, "cache_write": 2.50, "cache_read": 0.20},
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00, "cache_write": 1.25, "cache_read": 0.10},
    "claude-fable-5-1":          {"input": 10.00, "output": 50.00, "cache_write": 12.50, "cache_read": 1.00},
}


def log_llm_usage(folder: Path, step_label: str, model: str, usage) -> None:
    """Anthropic API 호출 하나의 토큰 사용량을 <folder>/edit/llm_usage.jsonl에 한 줄 추가한다
    (R8 영수증의 "영상당 처리 비용 추정"이 이 파일을 합산해서 보여줌, server.py Session.receipt()).

    `usage`는 보통 `client.messages.parse(...)` 응답의 `.usage` 객체지만(속성:
    input_tokens/output_tokens/cache_creation_input_tokens/cache_read_input_tokens), 테스트
    편의를 위해 같은 키를 가진 dict도 받는다. 가격표에 없는 모델은 비용을 추측하지 않고
    그냥 기록을 건너뛴다(잘못된 비용보다 누락이 낫다)."""
    pricing = LLM_PRICING_USD_PER_MTOK.get(model)
    if pricing is None:
        print(f"[llm_usage] 가격표에 없는 모델 '{model}' - 비용 기록 생략", file=sys.stderr)
        return

    def _get(key: str) -> int:
        val = usage.get(key) if isinstance(usage, dict) else getattr(usage, key, None)
        return val or 0

    input_tokens = _get("input_tokens")
    output_tokens = _get("output_tokens")
    cache_write_tokens = _get("cache_creation_input_tokens")
    cache_read_tokens = _get("cache_read_input_tokens")

    cost_usd = (
        input_tokens * pricing["input"]
        + output_tokens * pricing["output"]
        + cache_write_tokens * pricing["cache_write"]
        + cache_read_tokens * pricing["cache_read"]
    ) / 1_000_000

    row = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "step": step_label,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": round(cost_usd, 6),
    }
    with (edit_dir(folder) / "llm_usage.jsonl").open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def trace_to_ng_indices(cut_id: int, draft_cuts: list[dict]) -> list[int]:
    """draft_cuts.json의 병합된 컷(cut_id) -> 그 컷을 이룬 원본 소스들 중 kind=='ng'인 것들의
    ng.json 인덱스. "ng[17]" 형태의 source_id를 파싱한다. global_review.py의 over_cut/시청자
    역전파와 seam_refine.py의 이음새 판정 역전파가 공유한다."""
    draft = next((c for c in draft_cuts if c["id"] == cut_id), None)
    if not draft:
        return []
    out = []
    for src in draft.get("sources", []):
        sid = src.get("source_id", "")
        if sid.startswith("ng["):
            out.append(int(sid[3:-1]))
    return out


def apply_flag_to_ng(ng_items: list[dict], idx: int, reason: str) -> bool:
    """ng_items[idx]에 flag=restore와 사유를 backprop한다 - 검토 화면은 ng.json의 flag/
    route_reason만 읽으므로, final_cuts.json 쪽에서만 restore로 판정되고 ng.json에 반영되지
    않으면 사용자에게 조용히 안 보이는 복원 후보가 생긴다(경고 없는 복원, 최우선 위험).
    반환값: 실제로 flag가 바뀌었는지 (이미 restore였으면 False, 이유만 덧붙임 - 같은 문구가
    이미 있으면 중복 추가하지 않는다)."""
    if idx >= len(ng_items):
        return False
    it = ng_items[idx]
    changed = it.get("flag") != "restore"
    it["flag"] = "restore"
    if reason and reason not in (it.get("route_reason") or ""):
        it["route_reason"] = f"{it.get('route_reason', '')}; {reason}".strip("; ")
    return changed
