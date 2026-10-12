"""효과음 라이브러리 - 모든 영상이 함께 쓰는 효과음 (10-12 사용자 요청).

brand/sfx/ 에 파일과 목록(sfx.json)을 둔다. 아웃트로 이미지(brand/outro.png)처럼 채널 공통 자산이라
영상 폴더가 아니라 여기에 있고, git에는 올리지 않는다(/brand/).
인서트에 연결하면 인서트가 시작하는 순간 파일 전체를 그대로 재생한다 - 자르거나 늘리지 않는다.
"""
from __future__ import annotations
import json
import re
import subprocess
import threading
import uuid
from pathlib import Path

from common import BRAND_DIR, write_json

SFX_DIR = BRAND_DIR / "sfx"
INDEX = SFX_DIR / "sfx.json"
EXTS = {".mp3", ".wav", ".m4a", ".aif", ".aiff", ".caf", ".aac"}  # FCP가 그대로 읽는 형식 - 그대로 둔다
# 그 밖의 형식(mov·mp4·flac·ogg 등)은 소리만 뽑아 wav로 바꿔 둔다. mov를 그대로 두면 FCP에서 화면까지 같이 붙는다
MAX_BYTES = 100 * 1024 * 1024
_lock = threading.Lock()


def _load() -> list[dict]:
    try:
        return json.loads(INDEX.read_text())["items"]
    except (OSError, ValueError, KeyError):
        return []


def _save(items: list[dict]) -> None:
    SFX_DIR.mkdir(parents=True, exist_ok=True)
    write_json(INDEX, {"items": items})


def items() -> list[dict]:
    """파일이 실제로 있는 것만."""
    return [s for s in _load() if (SFX_DIR / s["file"]).exists()]


def get(sid: str) -> dict | None:
    return next((s for s in items() if s["id"] == sid), None)


def path(sid: str) -> Path | None:
    s = get(sid)
    return SFX_DIR / s["file"] if s else None


def _probe(f: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                        "stream=sample_rate,channels:format=duration", "-of", "json", str(f)], capture_output=True, text=True)
    j = json.loads(r.stdout or "{}")
    st = (j.get("streams") or [{}])[0]
    dur = float((j.get("format") or {}).get("duration") or 0)
    if not st or dur <= 0:
        raise ValueError("소리가 들어 있는 파일이 아닙니다")
    return {"duration": round(dur, 3), "rate": int(st.get("sample_rate") or 48000), "channels": int(st.get("channels") or 2)}


def add(filename: str, data: bytes) -> dict:
    ext = Path(filename).suffix.lower()
    if len(data) > MAX_BYTES:
        raise ValueError("파일이 너무 큽니다 (100MB 이하)")
    sid = uuid.uuid4().hex[:8]
    SFX_DIR.mkdir(parents=True, exist_ok=True)
    if ext in EXTS:
        f = SFX_DIR / f"{sid}{ext}"
        f.write_bytes(data)
    else:
        src = SFX_DIR / f"{sid}.src{ext}"
        src.write_bytes(data)
        f = SFX_DIR / f"{sid}.wav"
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-map", "0:a:0", "-c:a", "pcm_s16le", str(f)],
                           capture_output=True)
        src.unlink(missing_ok=True)
        if r.returncode:
            f.unlink(missing_ok=True)
            raise ValueError("소리가 들어 있는 파일이 아닙니다")
    try:
        info = _probe(f)
    except Exception:
        f.unlink(missing_ok=True)
        raise
    name = re.sub(r"\s+", " ", Path(filename).stem).strip()[:40] or sid
    item = {"id": sid, "name": name, "file": f.name, **info}
    with _lock:
        lst = _load()
        lst.append(item)
        _save(lst)
    return item


def rename(sid: str, name: str) -> dict:
    with _lock:
        lst = _load()
        for s in lst:
            if s["id"] == sid:
                s["name"] = name.strip()[:40] or s["name"]
                _save(lst)
                return s
    raise ValueError("없는 효과음입니다")


def delete(sid: str) -> None:
    with _lock:
        lst = _load()
        hit = [s for s in lst if s["id"] == sid]
        if not hit:
            raise ValueError("없는 효과음입니다")
        (SFX_DIR / hit[0]["file"]).unlink(missing_ok=True)
        _save([s for s in lst if s["id"] != sid])
