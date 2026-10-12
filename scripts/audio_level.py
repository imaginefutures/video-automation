"""소리 크기 측정 - 효과음을 영상 말소리에 맞춘 크기로 얹기 위해 (10-12 사용자 요청).

효과음 파일마다 크기가 제각각이고 영상마다 녹음 크기도 달라서, 고정 볼륨으로는 어떤 영상에선 묻히고 어떤 영상에선 튄다.
그래서 둘 다 재서 "말소리 대비 N%"가 되도록 효과음에 줄 증감(dB)을 계산한다.
결과는 파일 크기·수정 시각과 함께 캐시한다 - 같은 파일이면 다시 재지 않는다.
"""
from __future__ import annotations
import json
import math
import re
import subprocess
import threading
from pathlib import Path

from common import write_json

CACHE = Path.home() / ".video-cut" / "cache" / "audio_levels.json"
_lock = threading.Lock()

DEFAULT_PCT = 100      # 영상 기본값: 효과음 가장 큰 순간 = 말소리 큰 순간. 50%(-6dB)로 시작했다가 말에 묻혀 안 들림 (10-12 사용자 확인)
PEAK_CEIL = -1.0       # 효과음 최대치가 이 위로 가지 않게 (찢어지는 소리 방지)
GAIN_MIN, GAIN_MAX = -40.0, 20.0


METHOD = "v2"  # 재는 방법을 바꾸면 올린다 - 예전 캐시값을 다시 쓰지 않게


def _key(f: Path) -> str:
    st = f.stat()
    return f"{f.resolve()}|{st.st_size}|{int(st.st_mtime)}|{METHOD}"


def _ffmpeg_log(f: Path, af: str) -> str:
    return subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(f), "-vn", "-af", af, "-f", "null", "-"],
                          capture_output=True, text=True).stderr


def _measure(f: Path, hit: bool) -> dict:
    # hit=True(효과음): 가장 큰 순간(0.4초 창) - '탁' 하고 꼬리가 긴 소리는 평균을 내면 실제 들리는 것보다 작게 잡힌다.
    # hit=False(영상 말소리): 말하는 동안의 큰 순간(0.4초 창 상위 10%). 효과음의 '가장 큰 순간'과 같은 잣대로 비교해야 한다 -
    # 처음엔 전체 평균(integrated)과 비교했더니 효과음이 말보다 한참 작게 맞춰져 말소리에 묻혔다 (10-12).
    # 쉼·숨은 빼고 본다: 측정 규칙의 상대 게이트처럼 전체 평균보다 10 이상 작은 창은 버린다.
    err = _ffmpeg_log(f, "ebur128=peak=sample")
    peak = re.findall(r"Peak:\s*(-?[\d.]+|-inf)\s*dBFS", err)
    peak_db = float(peak[-1]) if peak and peak[-1] != "-inf" else PEAK_CEIL
    if hit:
        ms = [float(m) for m in re.findall(r"M:\s*(-?[\d.]+)", err)]
        lufs = max(ms) if ms else -120.0
    else:
        i = re.findall(r"I:\s*(-?[\d.]+)\s*LUFS", err)
        integrated = float(i[-1]) if i else -120.0
        ms = sorted(m for m in (float(x) for x in re.findall(r"M:\s*(-?[\d.]+)", err)) if m > max(-70.0, integrated - 10))
        lufs = ms[int(len(ms) * 0.9)] if ms else integrated
    if lufs <= -69:  # 0.4초보다 짧은 소리는 측정 창이 안 생긴다 - 평균 음량으로 대신
        mv = re.findall(r"mean_volume:\s*(-?[\d.]+)\s*dB", _ffmpeg_log(f, "volumedetect"))
        lufs = float(mv[-1]) if mv else -20.0
    return {"lufs": round(lufs, 1), "peak": round(peak_db, 1)}


def level(f: Path, hit: bool = False) -> dict:
    """{"lufs", "peak"}. 캐시에 있으면 바로, 없으면 잰다 (긴 영상은 수십 초 걸릴 수 있음)."""
    k = _key(f) + ("|hit" if hit else "")
    with _lock:
        try:
            cache = json.loads(CACHE.read_text())
        except (OSError, ValueError):
            cache = {}
    if k in cache:
        return cache[k]
    v = _measure(f, hit)
    with _lock:
        try:
            cache = json.loads(CACHE.read_text())
        except (OSError, ValueError):
            cache = {}
        cache[k] = v
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        write_json(CACHE, cache)
    return v


def cached(f: Path, hit: bool = False) -> dict | None:
    try:
        k = _key(f) + ("|hit" if hit else "")
        return json.loads(CACHE.read_text()).get(k)
    except (OSError, ValueError):
        return None


def gain_db(speech: dict, sfx: dict, pct: float) -> float:
    """효과음이 말소리의 pct%(진폭 기준, 50% = -6dB) 크기가 되도록 줄 증감. 최대치가 PEAK_CEIL을 넘지 않게 막는다."""
    if pct <= 0:
        return GAIN_MIN
    g = speech["lufs"] + 20 * math.log10(pct / 100) - sfx["lufs"]
    g = min(g, PEAK_CEIL - sfx["peak"])
    return round(max(GAIN_MIN, min(GAIN_MAX, g)), 1)
