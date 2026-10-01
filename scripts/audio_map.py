"""Whole-video acoustic map (docs/기획/01-처리-과정.md 3단계): RMS envelope, breath
candidates, and per-boundary snap targets, computed once and reused by route_candidates.py's
downstream consumer (build_edl.py) and by seam_refine.py's gates.

Local computation only (librosa), no API cost - same reasoning as prosody.py, but at frame
resolution instead of per-word: a cut boundary needs to land in a genuinely quiet moment, and
"quiet" has to be judged at ~10ms resolution, not per-word.

Cached: <folder>/edit/audio_map.json. The array fields (rms_db) are large for a 20+ minute
video (~10ms hop -> ~150k frames) but still a few MB of JSON - acceptable for a local tool.

Usage:
    python scripts/audio_map.py <videos/NAME>
"""
from __future__ import annotations
import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from common import video_dir, edit_dir, write_json, source_media

SR = 16000
HOP_SEC = 0.01          # 10ms frames - fine enough for an 80ms snap search window
FRAME_SEC = 0.03        # 30ms analysis window per frame
BREATH_MIN_SEC = 0.15
BREATH_MAX_SEC = 0.5
VOICED_ZCR_MAX = 0.15   # frames with zero-crossing rate above this read as breath/noise, not voice


def load_audio(folder: Path):
    """Same extraction path as prosody.py (librosa can't open the mp4 container directly)."""
    import librosa
    media = source_media(folder)
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "audio.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(media), "-map", "0:a:0", "-vn", "-ac", "1", "-ar", str(SR),
             "-c:a", "pcm_s16le", str(wav)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        y, sr = librosa.load(str(wav), sr=SR, mono=True)
    return y, sr


def compute_frames(y: np.ndarray, sr: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    import librosa
    hop_len = int(HOP_SEC * sr)
    frame_len = int(FRAME_SEC * sr)
    rms = librosa.feature.rms(y=y, frame_length=frame_len, hop_length=hop_len, center=True)[0]
    zcr = librosa.feature.zero_crossing_rate(y=y, frame_length=frame_len, hop_length=hop_len, center=True)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_len)
    return rms, zcr, times


def find_breaths(rms_db: np.ndarray, zcr: np.ndarray, times: np.ndarray, room_tone_db: float) -> list[dict]:
    """Breath candidate: quieter than speech but above room tone, low zero-crossing-rate
    energy is not required (breath is broadband, higher ZCR than voiced speech) - the signal
    used here is actually the OPPOSITE of voicing: highish ZCR + low-but-not-silent RMS,
    sustained 150-500ms. This is a coarse heuristic (no dedicated breath classifier), good
    enough to avoid slicing a cut boundary through an audible inhale/exhale."""
    hop = times[1] - times[0] if len(times) > 1 else HOP_SEC
    quiet_hi = room_tone_db + 10.0   # breath is louder than pure room tone...
    quiet_lo = room_tone_db + 2.0    # ...but this is a soft floor, not a hard one
    candidate = (rms_db > quiet_lo) & (rms_db < quiet_hi) & (zcr > VOICED_ZCR_MAX)

    breaths = []
    i = 0
    n = len(candidate)
    while i < n:
        if not candidate[i]:
            i += 1
            continue
        j = i
        while j < n and candidate[j]:
            j += 1
        dur = (j - i) * hop
        if BREATH_MIN_SEC <= dur <= BREATH_MAX_SEC:
            breaths.append({"start": round(float(times[i]), 3), "end": round(float(times[min(j, n - 1)]), 3)})
        i = j
    return breaths


def compute(folder: Path) -> Path:
    print("loading audio for acoustic map...")
    y, sr = load_audio(folder)
    print("computing RMS/ZCR envelope (10ms hop)...")
    rms, zcr, times = compute_frames(y, sr)
    rms_db = 20 * np.log10(np.maximum(rms, 1e-8))
    room_tone_db = float(np.percentile(rms_db, 10))  # 10th percentile stands in for "silence floor"
    speech_db = float(np.percentile(rms_db, 60))

    breaths = find_breaths(rms_db, zcr, times, room_tone_db)

    out = edit_dir(folder) / "audio_map.json"
    write_json(out, {
        "hop_sec": round(float(times[1] - times[0]), 5) if len(times) > 1 else HOP_SEC,
        "room_tone_db": round(room_tone_db, 2),
        "speech_db": round(speech_db, 2),
        "rms_db": [round(float(v), 2) for v in rms_db],
        "breaths": breaths,
    })
    print(f"wrote {out} ({len(rms_db)} frames, room tone {room_tone_db:.1f}dB, "
          f"speech ~{speech_db:.1f}dB, {len(breaths)} breath candidate(s))")
    return out


# --------------------------------------------------------------------------- consumer helpers
# Used by build_edl.py (boundary snap) and seam_refine.py (gates G1/G3). Loaded once per
# process via load_audio_map(); the helpers below are pure functions over that dict so both
# callers share one implementation.

def load_audio_map(folder: Path) -> dict | None:
    p = edit_dir(folder) / "audio_map.json"
    if not p.exists():
        return None
    import json
    return json.loads(p.read_text())


def _frame_idx(amap: dict, t: float) -> int:
    hop = amap["hop_sec"]
    return max(0, min(len(amap["rms_db"]) - 1, round(t / hop)))


def energy_db_at(amap: dict, t: float) -> float:
    return amap["rms_db"][_frame_idx(amap, t)]


def snap_to_quiet(amap: dict, t: float, window_sec: float = 0.08) -> float:
    """Nearest local energy minimum within ±window_sec of t - only meaningful when t is
    already inside a real gap; do not use this centered on a WORD boundary timestamp, since
    that is by definition still-speech on at least one side (see min_energy_in below, which
    is what seam_refine.py actually uses for cut boundaries)."""
    hop = amap["hop_sec"]
    i0 = _frame_idx(amap, t)
    span = max(1, round(window_sec / hop))
    lo, hi = max(0, i0 - span), min(len(amap["rms_db"]) - 1, i0 + span)
    window = amap["rms_db"][lo:hi + 1]
    if not window:
        return t
    best = lo + window.index(min(window))
    return round(best * hop, 3)


def min_energy_in(amap: dict, lo: float, hi: float) -> tuple[float, float]:
    """Quietest point strictly within [lo, hi] (a one-sided search, not symmetric around a
    word edge) - returns (time, db). Used to find a real cut boundary: the caller anchors
    [lo, hi] so one edge is always the last point that must not be touched (the adjacent KEPT
    word's own boundary), guaranteeing kept content is never clipped no matter what the
    energy profile looks like."""
    i0, i1 = _frame_idx(amap, lo), _frame_idx(amap, hi)
    if i1 < i0:
        i0, i1 = i1, i0
    window = amap["rms_db"][i0:i1 + 1]
    if not window:
        return round((lo + hi) / 2, 3), amap["room_tone_db"]
    j = window.index(min(window))
    t = (i0 + j) * amap["hop_sec"]
    return round(t, 3), window[j]


def is_quiet_enough(amap: dict, t: float, margin_db: float = 6.0) -> bool:
    """G1: a cut boundary must sit at or below room-tone + margin, i.e. not mid-syllable."""
    return energy_db_at(amap, t) <= amap["room_tone_db"] + margin_db


ONSET_LAG_MAX_SEC = 0.2  # observed Scribe word-start lag on Korean plosive/fricative onsets
ONSET_MARGIN_DB = 6.0    # same margin as is_quiet_enough's G1 check


def true_onset(amap: dict, reported_t: float, max_pull_sec: float = ONSET_LAG_MAX_SEC,
               margin_db: float = ONSET_MARGIN_DB) -> float:
    """Pull a reported word-start time back to the real acoustic onset when the ASR timestamp
    already lands inside speech (energy above room tone + margin) - Scribe's word boundaries can
    trail the true onset by ~0.15-0.2s (user-reported, 2026-10-01), and plan_pauses.py's pause
    trim otherwise trusts that timestamp verbatim, clipping the start of almost every sentence.
    Walks backward frame-by-frame until energy drops back to room tone, capped at max_pull_sec
    so a timestamp that's already correct is left untouched."""
    threshold = amap["room_tone_db"] + margin_db
    if energy_db_at(amap, reported_t) <= threshold:
        return reported_t
    hop = amap["hop_sec"]
    rms_db = amap["rms_db"]
    i0 = _frame_idx(amap, reported_t)
    max_steps = max(1, round(max_pull_sec / hop))
    i = i0
    while i > 0 and i0 - i < max_steps and rms_db[i] > threshold:
        i -= 1
    return round(i * hop, 3)


def breath_at(amap: dict, t: float) -> dict | None:
    for b in amap.get("breaths", []):
        if b["start"] <= t < b["end"]:
            return b
    return None


def bisects_breath(amap: dict, start: float, end: float) -> bool:
    """G3: true if either new boundary lands strictly inside a breath span (cutting it in
    half) rather than outside it or spanning it whole."""
    for t in (start, end):
        b = breath_at(amap, t)
        if b and b["start"] < t < b["end"]:
            return True
    return False


def breath_before(amap: dict | None, t: float, window_sec: float = 1.2) -> dict | None:
    """2026-09-30: 지금까지 숨소리는 경계 안전성 체크(G3)에만 쓰였다 - "재시작 신호"로는 어디에도
    안 들어갔다. 사람이 다시 말할 때 숨을 들이쉬고 시작하는 경우가 많다는 점을 classify_region.py의
    보강 신호로 쓴다(prosody.py의 F0 리셋과 같은 위상 - 독립 신호로는 노이즈지만 "이미 의심되는
    구간의 보강 신호"로는 유용할 가능성이 높다). t 직전 window_sec 안에 끝나는 숨소리 후보를 찾는다."""
    if not amap:
        return None
    for b in amap.get("breaths", []):
        if 0 <= t - b["end"] <= window_sec:
            return b
    return None


# --------------------------------------------------------------------------- boundary choice
#
# Moved here from seam_refine.py (2026-09-29) so every caller that turns a word-index range
# into an actual cut boundary - seam_refine.py's alternative search AND server.py's cut_spans()
# - shares one implementation instead of server.py re-deriving its own flat-pad-only version.
# Root cause of "confirmed edit still has a sliver of the cut phrase's sound": server.py never
# called this - it padded every NG/block cut inward by a flat 15ms regardless of where the
# audio actually went quiet, so up to 15ms of real (if flagged) sound routinely survived the
# cut on both edges. See docs/결정-이력.md 09-29 항목.

PAD_SEC = 0.015          # flat safety margin fallback - must match build_edl.BOUNDARY_PAD_SEC
GAP_SEARCH_EPS = 0.05
QUIET_MARGIN_DB = 15.0    # 잠정값, BS145 실측 기반 - docs/기획/06 정식 보정 전까지 사용


def plain_pad_boundary(words: list[dict], wi_start: int, wi_end: int) -> tuple[float, float]:
    return round(words[wi_start]["start"] + PAD_SEC, 3), round(words[wi_end - 1]["end"] - PAD_SEC, 3)


def quiet_boundary(amap: dict, words: list[dict], wi_start: int, wi_end: int, duration: float
                    ) -> tuple[float, float, float, float]:
    prev_end = words[wi_start - 1]["end"] if wi_start > 0 else 0.0
    lo1 = prev_end
    hi1 = words[wi_start]["start"] if words[wi_start]["start"] - prev_end > 0.01 else words[wi_start]["start"] + GAP_SEARCH_EPS
    t1, db1 = min_energy_in(amap, lo1, hi1)

    next_start = words[wi_end]["start"] if wi_end < len(words) else duration
    hi2 = next_start
    lo2 = words[wi_end - 1]["end"] if next_start - words[wi_end - 1]["end"] > 0.01 else words[wi_end - 1]["end"] - GAP_SEARCH_EPS
    t2, db2 = min_energy_in(amap, lo2, hi2)
    return t1, t2, db1, db2


def choose_boundary(amap: dict | None, words: list[dict], wi_start: int, wi_end: int, duration: float) -> dict:
    """Pick the actual cut boundary for word range [wi_start, wi_end). Searches for the
    quietest point in each adjacent gap (never crosses into a neighboring word - lo/hi are
    anchored at that word's own timestamp) and uses it if it beats the flat pad on both edges;
    otherwise falls back to the flat PAD_SEC pad. `audio_ok` tells the caller whether the
    boundary actually lands somewhere quiet enough to not leave an audible residue - False
    means neither the snap nor the pad found real silence, so the caller should not treat this
    as a safe automatic cut (G1/G3 are folded into "was a better boundary findable", not a
    separate hard gate)."""
    pad_s, pad_e = plain_pad_boundary(words, wi_start, wi_end)
    if not amap:
        return {"start": pad_s, "end": pad_e, "method": "pad", "audio_ok": None}

    pad_s_db, pad_e_db = energy_db_at(amap, pad_s), energy_db_at(amap, pad_e)
    q_s, q_e, q_s_db, q_e_db = quiet_boundary(amap, words, wi_start, wi_end, duration)
    threshold = amap["room_tone_db"] + QUIET_MARGIN_DB

    use_quiet = (q_s_db <= pad_s_db and q_e_db <= pad_e_db and q_s < q_e)
    if use_quiet and not bisects_breath(amap, q_s, q_e):
        start, end, s_db, e_db, method = q_s, q_e, q_s_db, q_e_db, "quiet_snap"
    else:
        start, end, s_db, e_db, method = pad_s, pad_e, pad_s_db, pad_e_db, "pad"

    audio_ok = s_db <= threshold and e_db <= threshold
    return {"start": round(start, 3), "end": round(end, 3), "method": method, "audio_ok": audio_ok,
            "start_db": round(s_db, 1), "end_db": round(e_db, 1)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    compute(video_dir(args.folder))


if __name__ == "__main__":
    main()
