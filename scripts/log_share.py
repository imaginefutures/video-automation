"""홈 화면 "로그 공유" 창에 띄울 텍스트 한 덩어리를 만든다.

다른 컴퓨터에서 문제가 났을 때 사용자가 이 텍스트를 통째로 복사해 보내면 원인을 찾을 수 있게,
흩어져 있는 로그(영상별 edit/*.log·*.jsonl, 분할 work/*.log, 홈 서버 로그, ~/.video-cut/history.jsonl),
AI 제안과 최종 결정 비교, 실행 환경을 한곳에 모은다. 전부 로컬 파일을 읽기만 하고 어디로도 보내지 않는다.

- server.log의 정상 접속 줄(2xx/3xx)은 뺀다 - 파형 요청 등으로 수만 줄이 쌓여 오류가 묻힌다.
- llm_usage.jsonl은 호출마다 한 줄이라 단계별 합계로 줄인다.
- .env의 API 키 값이 어디에든 찍혀 있으면 가린다.
"""
from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import sys
import traceback
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from common import REQUIRED_API_KEYS, OPTIONAL_API_KEYS

HOME_LOG = Path.home() / ".video-cut" / "logs" / "home_server.log"  # home_server.py가 출력을 여기에도 쓴다
ACCESS_OK_RE =re.compile(r'^\S+ - - \[[^\]]+\] "[A-Z]+ [^"]*" [23]\d\d ')


def _read(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(errors="replace").strip() or None


def _ffmpeg_version() -> str:
    if not shutil.which("ffmpeg"):
        return "없음"
    try:
        out = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5).stdout
        return out.split("\n", 1)[0].removeprefix("ffmpeg version ").split(" ", 1)[0]
    except Exception as e:
        return f"확인 실패 ({e})"


def _env_section(version: str, sha: str) -> str:
    mac = platform.mac_ver()[0]
    keys = ", ".join(f"{k} {'O' if os.environ.get(k) else 'X'}" for k, _, _ in REQUIRED_API_KEYS + OPTIONAL_API_KEYS)
    return "\n".join([
        f"버전: {version} ({sha})",
        f"OS: {'macOS ' + mac if mac else platform.platform()} ({platform.machine()})",
        f"Python: {sys.version.split()[0]}",
        f"ffmpeg: {_ffmpeg_version()}",
        f"API 키: {keys}",
    ])


def _compact_json(path: Path) -> str | None:
    try:
        return json.dumps(json.loads(path.read_text()), ensure_ascii=False)
    except (OSError, json.JSONDecodeError):
        return _read(path)


def _server_log(path: Path) -> str | None:
    text = _read(path)
    if not text:
        return None
    kept = [ln for ln in text.splitlines() if not ACCESS_OK_RE.match(ln)]
    return "\n".join(kept).strip() or None


def _usage_summary(path: Path) -> str | None:
    text = _read(path)
    if not text:
        return None
    by_step: dict[tuple[str, str], list[float]] = defaultdict(lambda: [0, 0, 0, 0.0])
    first = last = None
    for ln in text.splitlines():
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            continue
        s = by_step[(r.get("step", "?"), r.get("model", "?"))]
        s[0] += 1
        s[1] += r.get("input_tokens") or 0
        s[2] += r.get("output_tokens") or 0
        s[3] += r.get("cost_usd") or 0
        first = first or r.get("at")
        last = r.get("at") or last
    rows = [f"{step} [{model}] 호출 {n}회, 입력 {i:,} / 출력 {o:,} 토큰, ${c:.3f}"
            for (step, model), (n, i, o, c) in sorted(by_step.items())]
    total = sum(v[3] for v in by_step.values())
    return "\n".join([f"기간 {first} ~ {last}, 합계 ${total:.2f}", *rows])


def _insert_errors(path: Path) -> str | None:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    out = []
    sg = data.get("suggest") or {}
    if sg.get("state") == "error":
        out.append(json.dumps({"suggest": sg}, ensure_ascii=False))
    for it in data.get("items") or []:
        if it.get("status") == "error":
            out.append(json.dumps({k: it.get(k) for k in ("id", "form", "status", "error", "error_info")},
                                  ensure_ascii=False))
    return "\n".join(out) or None


def _cut_review(edit: Path) -> str | None:
    """컷 품질("AI가 이상하게 잘랐다")을 따지려면 AI가 처음 뭘 제안했고 사람이 뭘 바꿨는지가 필요하다 -
    ng.json(제안) + decisions.json(최종)을 후보마다 한 줄로 맞대고, 사람과 갈린 곳만 AI 근거를 붙인다."""
    try:
        ng = json.loads((edit / "ng.json").read_text())
        dec = json.loads((edit / "decisions.json").read_text())
    except (OSError, json.JSONDecodeError):
        return None
    final = dec.get("ng") or {}
    by_count: dict[str, int] = defaultdict(int)
    rows, diffs = [], []
    for i, it in enumerate(ng):
        d = final.get(str(i)) or {}
        ai = (it.get("route") or "?").lower()
        act = d.get("action") or "미결정"
        by_count[d.get("by") or "미결정"] += 1
        differ = act in ("cut", "keep") and act != ai
        text = (it.get("deleted_text") or "").replace("\n", " ")
        rows.append(f"{'≠' if differ else ' '} #{i} {it.get('start', 0):.1f}-{it.get('end', 0):.1f}s {it.get('label', '')} "
                    f"AI={ai.upper()}{'(복원후보)' if it.get('flag') == 'restore' else ''} → {act}({d.get('by', '-')})"
                    f"{' 보류' if d.get('skipped') else ''} \"{text[:60]}{'…' if len(text) > 60 else ''}\"")
        if differ:
            diffs.append(f"#{i} {(it.get('route_reason') or '')[:400]}")
    overrides = dec.get("overrides") or []
    reported = dec.get("reported_bad_cuts") or []
    head = (f"후보 {len(ng)}개, AI와 다르게 결정 {len(diffs)}개(≠), 결정 주체 "
            + ", ".join(f"{k} {v}" for k, v in sorted(by_count.items()))
            + f", 수동 구간 수정 {len(overrides)}개, 잘못 잘림 신고 {len(reported)}개, 확정 {dec.get('confirmed_at') or '안 함'}")
    out = [head, *rows]
    if diffs:
        out += ["", "-- AI와 다르게 결정한 후보의 AI 근거 (route_reason) --", *diffs]
    if overrides:
        out += ["", "-- 수동 구간 수정 (overrides) --",
                *(f"{o.get('op')} {o.get('start', 0):.3f}-{o.get('end', 0):.3f}s" for o in overrides)]
    if reported:
        out += ["", "-- 잘못 잘림 신고 --", *(json.dumps(r, ensure_ascii=False) for r in reported)]
    return "\n".join(out)


def _client_errors(edit: Path) -> str | None:
    text = _read(edit / "actions.log")
    if not text:
        return None
    return "\n".join(ln for ln in text.splitlines() if '"event": "client_error"' in ln) or None


def _block(title: str, body: str | None) -> str:
    return f"### {title}\n{body}\n" if body else ""


def _video_section(folder: Path) -> str:
    edit = folder / "edit"
    parts = [
        _block("처리 상태 (pipeline_status.json)", _compact_json(edit / "pipeline_status.json")),
        _block("처리 로그 (run.log)", _read(edit / "run.log")),
        _block("화면 서버 로그 (server.log, 정상 접속 줄 제외)", _server_log(edit / "server.log")),
        _block("브라우저 오류 (actions.log의 client_error)", _client_errors(edit)),
        _block("인서트 오류 (inserts.json)", _insert_errors(edit / "inserts.json")),
        _block("AI 판단 vs 최종 결정 (ng.json + decisions.json)", _cut_review(edit)),
        _block("AI 사용량 (llm_usage.jsonl 단계별 합계)", _usage_summary(edit / "llm_usage.jsonl")),
        _block("검토 화면 조작 기록 (actions.log)", _read(edit / "actions.log")),
    ]
    body = "".join(parts) or "(로그 없음)\n"
    return f"## 영상: {folder.name}\n{body}"


def _split_section(folder: Path) -> str:
    work = folder / "work"
    body = (_block("처리 로그 (run.log)", _read(work / "run.log"))
            + _block("화면 서버 로그 (server.log, 정상 접속 줄 제외)", _server_log(work / "server.log")))
    return f"## 분할: {folder.name}\n" + (body or "(로그 없음)\n")


def _redact(text: str) -> str:
    for k, _, _ in REQUIRED_API_KEYS + OPTIONAL_API_KEYS:
        v = os.environ.get(k)
        if v and len(v) >= 8:
            text = text.replace(v, f"<{k}>")
    return text.replace(str(Path.home()), "~")


def build(videos: list[Path], splits: list[Path], version: str, sha: str, only: str | None = None) -> str:
    """only: None=전체, "video:<이름>" 또는 "split:<이름>"=그것만."""
    sections = [f"# video-cut 로그 ({datetime.now().isoformat(timespec='seconds')})\n",
                f"## 환경\n{_env_section(version, sha)}\n"]
    # 영상 하나의 로그 파일이 깨져 있어도(옛 버전 형식 등) 나머지 로그는 받아야 원인을 찾는다 -
    # 실패한 섹션 자리에 traceback을 대신 싣는다.
    for kind, folders, make in (("video", videos, _video_section), ("split", splits, _split_section)):
        for f in folders:
            if only in (None, f"{kind}:{f.name}"):
                try:
                    sections.append(make(f))
                except Exception:
                    sections.append(f"## {kind}: {f.name}\n### 로그 모으기 실패\n{traceback.format_exc()}")
    if only is None:
        home = _read(HOME_LOG)
        if home:
            home = "\n".join(home.splitlines()[-400:])
        sections.append(f"## 홈 서버 로그 (~/.video-cut/logs/home_server.log, 최근 400줄)\n{home or '(없음)'}\n")
        hist = _read(Path.home() / ".video-cut" / "history.jsonl")
        sections.append(f"## 확정 기록 (~/.video-cut/history.jsonl)\n{hist or '(없음)'}\n")
    return _redact("\n".join(sections))
