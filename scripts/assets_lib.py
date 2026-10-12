"""공통 자산 - 모든 영상이 같이 쓰는, 사용자가 올린 파일 (docs/백로그/공통-자산.md).

~/.video-cut/assets/ 에 종류별 하위 폴더 + 목록(assets.json)을 둔다. 코드 폴더 밖이라 플러그인을 다시
설치해도 남는다. 영상 쪽은 id만 기록하고(inserts.json의 sfx 등), 내보낼 때 path()로 실제 파일을 찾는다.

종류는 KINDS 표 한 줄로 늘린다. 칸 모양은 두 가지:
  list   - 여러 개 (효과음)
  single - 하나만, 새로 올리면 바꿈 (아웃트로)
"""
from __future__ import annotations
import json
import re
import shutil
import subprocess
import threading
import uuid
from pathlib import Path

from common import PROJECT_ROOT, write_json

ASSETS_DIR = Path.home() / ".video-cut" / "assets"
INDEX = ASSETS_DIR / "assets.json"
LEGACY_DIR = PROJECT_ROOT / "brand"  # 1.24.0까지의 자리 - 처음 한 번 복사만 하고 지우지 않는다

AUDIO_KEEP = {".mp3", ".wav", ".m4a", ".aif", ".aiff", ".caf", ".aac"}  # FCP가 그대로 읽는 형식
OUTRO_W, OUTRO_H = 1920, 1080

KINDS = {
    "sfx": {"label": "효과음", "mode": "list", "media": "audio", "max_mb": 100},
    "outro": {"label": "아웃트로 이미지", "mode": "single", "media": "image", "max_mb": 30},
}
_lock = threading.Lock()


def _kind(kind: str) -> dict:
    if kind not in KINDS:
        raise ValueError(f"없는 자산 종류입니다: {kind}")
    return KINDS[kind]


def _load() -> dict:
    _migrate()
    try:
        return json.loads(INDEX.read_text())
    except (OSError, ValueError):
        return {}


def _save(data: dict) -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(INDEX, data)


def _migrate() -> None:
    """옛 brand/(코드 폴더 안)에 있던 아웃트로·효과음을 처음 한 번 복사한다."""
    if INDEX.exists() or not LEGACY_DIR.is_dir():
        return
    data: dict = {}
    if (LEGACY_DIR / "outro.png").exists():
        (ASSETS_DIR / "outro").mkdir(parents=True, exist_ok=True)
        shutil.copy2(LEGACY_DIR / "outro.png", ASSETS_DIR / "outro" / "outro.png")
        data["outro"] = [{"id": "outro", "name": "아웃트로", "file": "outro.png"}]
    try:
        old = json.loads((LEGACY_DIR / "sfx" / "sfx.json").read_text())["items"]
    except (OSError, ValueError, KeyError):
        old = []
    if old:
        (ASSETS_DIR / "sfx").mkdir(parents=True, exist_ok=True)
        for s in old:
            if (LEGACY_DIR / "sfx" / s["file"]).exists():
                shutil.copy2(LEGACY_DIR / "sfx" / s["file"], ASSETS_DIR / "sfx" / s["file"])
        data["sfx"] = old
    _save(data)


def items(kind: str) -> list[dict]:
    """파일이 실제로 있는 것만."""
    _kind(kind)
    return [s for s in _load().get(kind, []) if (ASSETS_DIR / kind / s["file"]).exists()]


def get(kind: str, sid: str = "") -> dict | None:
    lst = items(kind)
    if KINDS[kind]["mode"] == "single":
        return lst[0] if lst else None
    return next((s for s in lst if s["id"] == sid), None)


def path(kind: str, sid: str = "") -> Path | None:
    s = get(kind, sid)
    return ASSETS_DIR / kind / s["file"] if s else None


def outro_path() -> Path | None:
    return path("outro")


def _probe_audio(f: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                        "stream=sample_rate,channels:format=duration", "-of", "json", str(f)], capture_output=True, text=True)
    j = json.loads(r.stdout or "{}")
    st = (j.get("streams") or [{}])[0]
    dur = float((j.get("format") or {}).get("duration") or 0)
    if not st or dur <= 0:
        raise ValueError("소리가 들어 있는 파일이 아닙니다")
    return {"duration": round(dur, 3), "rate": int(st.get("sample_rate") or 48000), "channels": int(st.get("channels") or 2)}


def _store_audio(src: Path, dest_stem: Path) -> tuple[Path, dict]:
    """FCP가 읽는 형식은 그대로, 그 밖(mov·mp4·flac·ogg 등)은 첫 오디오만 wav로 - mov를 그대로 두면 FCP에서 화면까지 붙는다."""
    ext = src.suffix.lower()
    if ext in AUDIO_KEEP:
        f = dest_stem.with_suffix(ext)
        src.replace(f)
    else:
        f = dest_stem.with_suffix(".wav")
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-map", "0:a:0", "-c:a", "pcm_s16le", str(f)],
                           capture_output=True)
        if r.returncode:
            f.unlink(missing_ok=True)
            raise ValueError("소리가 들어 있는 파일이 아닙니다")
    try:
        return f, _probe_audio(f)
    except Exception:
        f.unlink(missing_ok=True)
        raise


def _store_outro(src: Path, dest_stem: Path) -> tuple[Path, dict]:
    """1920x1080 PNG로 맞춘다 - 비율이 다르면 잘라내지 않고 검은 여백(로고·글자가 잘리면 안 되니까).
    분할 내보내기가 편마다 본편 해상도로 다시 맞춘다."""
    f = dest_stem.with_suffix(".png")
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-frames:v", "1", "-vf",
                        f"scale={OUTRO_W}:{OUTRO_H}:force_original_aspect_ratio=decrease,"
                        f"pad={OUTRO_W}:{OUTRO_H}:(ow-iw)/2:(oh-ih)/2,setsar=1", str(f)], capture_output=True)
    if r.returncode:
        f.unlink(missing_ok=True)
        raise ValueError("이미지로 읽을 수 없는 파일입니다 (PNG·JPG를 올려주세요)")
    return f, {}


_STORE = {"sfx": _store_audio, "outro": _store_outro}


def add(kind: str, filename: str, data: bytes) -> dict:
    k = _kind(kind)
    if not data:
        raise ValueError("빈 파일입니다")
    if len(data) > k["max_mb"] * 1024 * 1024:
        raise ValueError(f"파일이 너무 큽니다 ({k['max_mb']}MB 이하)")
    d = ASSETS_DIR / kind
    d.mkdir(parents=True, exist_ok=True)
    sid = uuid.uuid4().hex[:8]
    src = d / f".{sid}.upload{Path(filename).suffix.lower()}"
    src.write_bytes(data)
    try:
        f, info = _STORE[kind](src, d / sid)
    finally:
        src.unlink(missing_ok=True)
    name = re.sub(r"\s+", " ", Path(filename).stem).strip()[:40] or sid
    item = {"id": sid, "name": name, "file": f.name, **info}
    with _lock:
        all_ = _load()
        old = all_.get(kind, []) if k["mode"] == "list" else []
        if k["mode"] == "single":  # 바꿈 - 이전 파일은 지운다
            for s in all_.get(kind, []):
                if s["file"] != f.name:
                    (d / s["file"]).unlink(missing_ok=True)
        all_[kind] = old + [item]
        _save(all_)
    return item


def rename(kind: str, sid: str, name: str) -> dict:
    _kind(kind)
    with _lock:
        all_ = _load()
        for s in all_.get(kind, []):
            if s["id"] == sid:
                s["name"] = name.strip()[:40] or s["name"]
                _save(all_)
                return s
    raise ValueError("없는 자산입니다")


def delete(kind: str, sid: str = "") -> None:
    k = _kind(kind)
    with _lock:
        all_ = _load()
        lst = all_.get(kind, [])
        hit = lst if k["mode"] == "single" else [s for s in lst if s["id"] == sid]
        if not hit:
            raise ValueError("없는 자산입니다")
        for s in hit:
            (ASSETS_DIR / kind / s["file"]).unlink(missing_ok=True)
        all_[kind] = [s for s in lst if s not in hit]
        _save(all_)
