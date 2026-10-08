"""주제별 분할 - 경계의 실제 자르는 시각을 화면 신호로 다듬는다 (docs/백로그/주제별-분할.md).

완성본은 문장 사이 쉼이 0.1~0.4초뿐이고 화면에 자막·전환 효과가 있어서, 소리만 보고 자르면
앞 편 끝에 다음 편 자막이 몇 프레임 비치거나 페이드 중간에서 잘린다 (10-08 "사고력 수학" 영상에서
6개 경계 중 2개가 그랬다). 경계 근처 프레임을 저해상도 흑백으로 읽어 우선순위대로 고른다:

  1 black   편집자가 넣은 검은 화면 전환 → 검은 구간 한가운데
  2 scene   장면 전환(화면 전체가 한 프레임에 바뀜) → 새 장면의 첫 프레임
  3 caption 화면 자막만 바뀜 → 새 자막이 처음 뜨는 프레임
  4 audio   위가 없으면 기존처럼 문장 사이 가장 조용한 지점 (propose_segments.cut_time)

말을 자르지 않게 2·3은 앞 문장 끝 직전 ~ 다음 문장 시작 직후 사이에서만 찾는다. 결과 시각은
프레임 시작보다 아주 조금 앞(FRAME_EPS)에 둬서 ffmpeg가 그 프레임을 뒤 편의 첫 프레임으로 넣게 한다.

결과는 work/cut_refine.json에 "앞 편 마지막 문장 번호" 단위로 캐시한다 (문장 시각은 바뀌지 않으므로).
"""
from __future__ import annotations
import json
import subprocess
import threading
from pathlib import Path

import numpy as np

from common import edit_dir, source_media, write_json

VERSION = 2  # 2: 검은 구간 안에서 가장 어두운 프레임 기준 (문구 카드 회피)
W, H = 192, 108
BLACK_LUMA = 12.0          # 평균 밝기가 이 아래면 검은 프레임
SCENE_DIFF = 30.0          # 화면 전체 평균 변화량이 이 위면 장면 전환 (평소 0~8, 페이드 중 최대 ~26)
CAPTION_DIFF = 8.0         # 자막 영역 변화량
CAPTION_RATIO = 3.0        # 자막 영역 변화가 화면 전체 변화의 이 배수 이상이어야 자막만 바뀐 것 (페이드·움직임 제외)
BLACK_REACH = 0.6          # 검은 구간은 문장 경계에서 이만큼 떨어져 있어도 찾는다 (페이드는 길다)
SPEECH_GUARD_BEFORE = 0.15 # 장면·자막 전환은 앞 문장 끝 이 정도 전까지만 허용 (전사 시각 오차)
SPEECH_GUARD_AFTER = 0.05
FRAME_EPS = 0.002

_lock = threading.Lock()


def video_fps(media: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                          "-of", "csv=p=0", str(media)], capture_output=True, text=True, check=True).stdout.strip()
    num, _, den = out.partition("/")
    return float(num) / float(den or 1)


def read_frames(media: Path, fps: float, t0: float, t1: float) -> tuple[float, np.ndarray]:
    """[t0, t1] 프레임들을 흑백 192x108로. 반환하는 시작 시각은 프레임 격자에 맞춘 값."""
    start = np.floor(t0 * fps) / fps
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{start:.4f}", "-i", str(media), "-t", f"{t1 - start:.3f}",
         "-vf", f"scale={W}:{H}", "-pix_fmt", "gray", "-f", "rawvideo", "-"],
        capture_output=True, check=True).stdout
    return float(start), np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)


def refine_cut(media: Path, fps: float, sents: list[dict], e: int, amap: dict | None) -> dict:
    """문장 e와 e+1 사이 경계의 자르는 시각 {t, reason}."""
    from propose_segments import cut_time
    prev_end, next_start = sents[e]["end"], sents[e + 1]["start"]
    lo, hi = prev_end - SPEECH_GUARD_BEFORE, max(next_start, prev_end) + SPEECH_GUARD_AFTER
    t0, a = read_frames(media, fps, prev_end - BLACK_REACH, next_start + BLACK_REACH)
    if len(a) >= 2:
        times = t0 + np.arange(len(a)) / fps
        luma = a.mean(axis=(1, 2))
        full = np.r_[0, np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))]
        band = a[:, int(H * 0.72):int(H * 0.95), int(W * 0.1):int(W * 0.9)]
        sub = np.r_[0, np.abs(np.diff(band, axis=0)).mean(axis=(1, 2))]

        # 1 검은 구간 - 경계에 가장 가까운 연속 구간의 가운데 프레임
        runs, i = [], 0
        while i < len(a):
            if luma[i] < BLACK_LUMA:
                j = i
                while j + 1 < len(a) and luma[j + 1] < BLACK_LUMA:
                    j += 1
                runs.append((i, j))
                i = j + 1
            else:
                i += 1
        if runs:
            mid_gap = (prev_end + next_start) / 2
            i, j = min(runs, key=lambda r: abs((times[r[0]] + times[r[1]]) / 2 - mid_gap))
            # 검은 바탕 위에 문구 카드가 잠깐 떠 있는 경우가 있다(10-08 실측: 카드 4프레임 → 완전한 검정) -
            # 가장 어두운 프레임들만 골라 그 가운데에서 자른다. 안 그러면 뒤 편이 문구 카드로 시작한다
            floor = luma[i:j + 1].min() + 1.0
            darkest = [k for k in range(i, j + 1) if luma[k] <= floor]
            k = darkest[(len(darkest)) // 2]
            return {"t": round(float(times[k]) - FRAME_EPS, 4), "reason": "black"}

        inside = [k for k in range(1, len(a)) if lo <= times[k] <= hi]
        # 2 장면 전환
        scenes = [k for k in inside if full[k] > SCENE_DIFF]
        if scenes:
            k = max(scenes, key=lambda k: full[k])
            return {"t": round(float(times[k]) - FRAME_EPS, 4), "reason": "scene"}
        # 3 자막만 바뀜
        caps = [k for k in inside if sub[k] > CAPTION_DIFF and sub[k] > CAPTION_RATIO * max(full[k], 0.5)]
        if caps:
            k = max(caps, key=lambda k: sub[k])
            return {"t": round(float(times[k]) - FRAME_EPS, 4), "reason": "caption"}

    return {"t": cut_time(sents, e, amap), "reason": "audio"}


def cache_path(folder: Path) -> Path:
    return edit_dir(folder) / "cut_refine.json"


def load_cache(folder: Path) -> dict:
    p = cache_path(folder)
    if not p.exists():
        return {}
    data = json.loads(p.read_text())
    return data.get("cuts", {}) if data.get("version") == VERSION else {}


def refine_all(folder: Path, ends: list[int], sents: list[dict], amap: dict | None) -> dict:
    """ends의 경계 중 캐시에 없는 것만 계산해 저장하고 전체 캐시를 돌려준다."""
    with _lock:
        cache = load_cache(folder)
        todo = [e for e in ends[:-1] if str(e) not in cache]
        if todo:
            media = source_media(folder)
            fps = video_fps(media)
            for e in todo:
                cache[str(e)] = refine_cut(media, fps, sents, e, amap)
            write_json(cache_path(folder), {"version": VERSION, "cuts": cache})
        return cache
