"""Shared helpers for the video-cut pipeline: paths, .env loading, transcript access."""
from __future__ import annotations
import getpass
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 2026-09-30: 스킬을 설치한 다른 사용자를 위한 온보딩 - 키가 없으면 여기서 물어봐서 .env에
# 저장한다. (키, 설명, 발급 페이지) 튜플 목록.
REQUIRED_API_KEYS = [
    ("ANTHROPIC_API_KEY", "Claude API 키 - NG 판별·분류·전체 검토에 씀", "https://console.anthropic.com/settings/keys"),
    ("ELEVENLABS_API_KEY", "ElevenLabs API 키 - Scribe 전사에 씀", "https://elevenlabs.io/app/settings/api-keys"),
]


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


def ensure_api_keys() -> None:
    """`load_env()`로 이미 있는 키는 그대로 쓰고, 없는 키만 채운다.

    두 가지 실행 맥락을 구분한다:
    - **사람이 직접 터미널에서 실행** (`python scripts/run.py ...`를 손으로 침): 표준입력이
      진짜 터미널이라 `getpass`로 그 자리에서 대화식으로 물어보고 `.env`에 저장한다.
    - **에이전트(클로드 코드)가 스킬로 대신 실행**: Bash 도구는 표준입력이 터미널이
      아니라서(`sys.stdin.isatty()`가 항상 False, 2026-09-30 직접 확인) `getpass`가 아예
      작동하지 않는다 - 예전엔 여기서 조용히 넘어가 버려서 한참 뒤 `transcribe.py`가 뜬금없이
      에러를 냈다. 지금은 **필요한 키·설명·발급 링크·`.env`의 절대경로를 명확히 출력하고 즉시
      종료**한다 - 에이전트가 이 출력을 읽고 사용자에게 대화로 물어본 뒤 그 경로에 직접
      `.env`를 써주는 게 실제 온보딩 경로다(`SKILL.md` "에이전트가 지킬 것" 참고)."""
    load_env()
    missing = [(k, desc, url) for k, desc, url in REQUIRED_API_KEYS if not os.environ.get(k)]
    if not missing:
        return

    env_path = PROJECT_ROOT / ".env"

    if not sys.stdin.isatty():
        lines = [f"필요한 API 키가 없습니다 - {env_path}에 아래 형식으로 한 줄씩 추가해야 합니다:"]
        for key, desc, url in missing:
            lines.append(f"  {key}=<값>   # {desc}, 발급: {url}")
        sys.exit("\n".join(lines))

    print("\n처음 실행하시는군요 - 필요한 API 키를 한 번만 물어볼게요. 저장되면 다음부터는 안 물어봅니다.\n")
    lines = env_path.read_text().splitlines() if env_path.exists() else []
    for key, desc, url in missing:
        print(f"- {key}: {desc}\n  발급: {url}")
        value = ""
        while not value:
            value = getpass.getpass(f"  {key} 입력(화면에 안 보임): ").strip()
        lines.append(f"{key}={value}")
        os.environ[key] = value
    env_path.write_text("\n".join(lines) + "\n")
    print(f"\n{env_path}에 저장했습니다. 다음부터는 안 물어봅니다.\n")


def video_dir(name_or_path: str | Path) -> Path:
    """Resolve `videos/<name>` or an explicit folder path."""
    p = Path(name_or_path)
    if p.is_dir():
        return p.resolve()
    candidate = PROJECT_ROOT / "videos" / str(name_or_path)
    if candidate.is_dir():
        return candidate.resolve()
    raise SystemExit(f"video folder not found: {name_or_path} (looked in {candidate})")


def edit_dir(folder: Path) -> Path:
    d = folder / "edit"
    d.mkdir(exist_ok=True)
    return d


def source_media(folder: Path) -> Path:
    """clean.mp4 when it exists (FCP-compatible, faststart), else raw.mp4."""
    clean = folder / "edit" / "clean.mp4"
    if clean.exists():
        return clean
    raw = folder / "raw.mp4"
    if raw.exists():
        return raw
    raise SystemExit(f"no raw.mp4 in {folder}")


def load_transcript(folder: Path) -> dict:
    return json.loads((folder / "edit" / "transcript.json").read_text())


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
