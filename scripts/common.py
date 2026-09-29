"""Shared helpers for the video-cut pipeline: paths, .env loading, transcript access."""
from __future__ import annotations
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


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


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


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
