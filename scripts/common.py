"""Shared helpers for the video-cut pipeline: paths, .env loading, transcript access."""
from __future__ import annotations
import getpass
import json
import os
import re
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

# 10-01 (홈 화면 영상 생성): *_final_gold/*.backup-*는 평가용/과거 스냅샷 접미사라 실제
# 프로젝트로 취급하지 않는다 - scripts/home_server.py의 is_project_folder()와 여기
# sanitize_project_name()이 같은 규칙을 공유해야, 웹에서 만든 이름이 우연히 이 패턴과 겹쳐
# "카드에 안 뜨는 유령 프로젝트"가 되는 사고를 막는다.
RESERVED_PROJECT_NAME_SUFFIXES = ("_final_gold",)
RESERVED_PROJECT_NAME_RE = re.compile(r"\.backup-")


def sanitize_project_name(raw: str) -> str:
    """홈 화면 "영상 생성" 폼의 제목 -> `videos/<name>` 폴더명. 경로 탈출·예약 패턴을 막는다
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
        {"key": k, "desc": desc, "url": url, "set": bool(os.environ.get(k))}
        for k, desc, url in REQUIRED_API_KEYS
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
