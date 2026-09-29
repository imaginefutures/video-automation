"""Per-word prosody (F0 pitch + RMS energy) from the actual audio (PLAN.md 4.2, 12.A).

classify_candidates.py has always had a "음향 신호" section in its design (PLAN.md 4.2:
F0 reset on a restart's first word, F0-curve similarity between two takes, energy/length
increase on a corrected word) but never actually computed it - the LLM prompt was text
only. This module computes those numbers directly from clean.mp4 so they can be handed to
the LLM as real evidence instead of staying a paper design.

Local computation only (librosa) - no API cost (PLAN.md 12.2/A cost note).

Cached: <folder>/edit/prosody.json.

Usage:
    python scripts/prosody.py <videos/NAME>
"""
from __future__ import annotations
import argparse
import statistics
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from common import video_dir, edit_dir, load_transcript, words_only, write_json, source_media

FMIN, FMAX = 70, 400  # Hz: covers mixed adult speaker F0 range
F0_RESET_RATIO = 1.12  # first-word F0 this far above the speaker's median reads as a restart's pitch reset
F0_FLAT_RATIO = 1.05


def load_audio(folder: Path):
    """librosa.load hits soundfile directly and can't open an mp4/aac container on its own
    (confirmed against clean.mp4 - LibsndfileError: Format not recognised), so extract to a
    WAV first, the same way transcribe.py already does for Scribe."""
    import librosa
    media = source_media(folder)
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "audio.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(media), "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000",
             "-c:a", "pcm_s16le", str(wav)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        y, sr = librosa.load(str(wav), sr=16000, mono=True)
    return y, sr


def compute_f0_track(y: np.ndarray, sr: int):
    import librosa
    f0, _voiced_flag, _voiced_prob = librosa.pyin(y, fmin=FMIN, fmax=FMAX, sr=sr)
    times = librosa.times_like(f0, sr=sr)
    return f0, times


def word_f0(f0: np.ndarray, times: np.ndarray, start: float, end: float) -> float | None:
    mask = (times >= start) & (times < max(end, start + 0.02))
    vals = f0[mask]
    vals = vals[~np.isnan(vals)]
    return float(np.median(vals)) if len(vals) else None


def word_energy(y: np.ndarray, sr: int, start: float, end: float) -> float:
    i1, i2 = int(start * sr), max(int(end * sr), int(start * sr) + 1)
    seg = y[i1:i2]
    return float(np.sqrt(np.mean(seg.astype(np.float64) ** 2))) if len(seg) else 0.0


def compute(folder: Path) -> Path:
    words = words_only(load_transcript(folder))
    print(f"loading audio for prosody extraction ({len(words)} words)...")
    y, sr = load_audio(folder)
    print("estimating pitch track (librosa.pyin - can take a minute or two)...")
    f0, times = compute_f0_track(y, sr)

    per_word = []
    for w in words:
        per_word.append({"wi": w["wi"], "f0_hz": word_f0(f0, times, w["start"], w["end"]),
                         "rms": word_energy(y, sr, w["start"], w["end"])})

    by_speaker: dict[str, list[dict]] = {}
    for w, p in zip(words, per_word):
        by_speaker.setdefault(w.get("speaker_id", "?"), []).append(p)
    baseline = {}
    for spk, items in by_speaker.items():
        f0s = [p["f0_hz"] for p in items if p["f0_hz"]]
        rmss = [p["rms"] for p in items if p["rms"] > 0]
        baseline[spk] = {"median_f0": round(statistics.median(f0s), 1) if f0s else None,
                         "median_rms": round(statistics.median(rmss), 6) if rmss else None}

    out = edit_dir(folder) / "prosody.json"
    write_json(out, {"fmin": FMIN, "fmax": FMAX, "per_word": per_word, "speaker_baseline": baseline})
    n_voiced = sum(1 for p in per_word if p["f0_hz"])
    print(f"wrote {out} ({n_voiced}/{len(per_word)} words voiced)")
    return out


def load_prosody(folder: Path) -> dict | None:
    p = edit_dir(folder) / "prosody.json"
    if not p.exists():
        return None
    import json
    return json.loads(p.read_text())


def span_evidence(prosody: dict | None, words: list[dict], i1: int, i2: int,
                   follow_i1: int, follow_i2: int) -> str:
    """Human-readable acoustic evidence for the LLM prompt (PLAN.md 4.2/12.A).

    The LLM can't hear the audio, so numbers computed from it are translated into the same
    kind of natural-language evidence line the taxonomy's own research basis (PLAN.md 4.6:
    Levelt & Cutler 1983 - mistake repairs carry prosodic marking, fluent repetitions/
    emphasis don't) already describes.
    """
    if not prosody:
        return "- (음향 신호 없음: prosody.json 미생성 - 텍스트 근거만으로 판단)"

    pw = {p["wi"]: p for p in prosody["per_word"]}
    baseline = prosody["speaker_baseline"]

    def f0_list(rng):
        return [pw[i]["f0_hz"] for i in rng if i in pw and pw[i]["f0_hz"]]

    def rms_list(rng):
        return [pw[i]["rms"] for i in rng if i in pw and pw[i]["rms"]]

    lines = []
    first = pw.get(i1)
    spk = words[i1].get("speaker_id") if i1 < len(words) else None
    base_f0 = baseline.get(spk, {}).get("median_f0") if spk else None
    if first and first["f0_hz"] and base_f0:
        ratio = first["f0_hz"] / base_f0
        if ratio >= F0_RESET_RATIO:
            note = "문장 시작의 피치 리셋과 일치 (재시작 가능성)"
        elif ratio <= F0_FLAT_RATIO:
            note = "평이함 - 리셋 신호 없음"
        else:
            note = "약한 리셋, 판단 근거로는 약함"
        lines.append(f"- 판별 대상 구간 첫 단어 F0: {first['f0_hz']:.0f}Hz "
                     f"(이 화자 평균 {base_f0:.0f}Hz 대비 {ratio:.2f}배, {note})")

    span_f0, follow_f0 = f0_list(range(i1, i2)), f0_list(range(follow_i1, follow_i2))
    if len(span_f0) >= 2 and len(follow_f0) >= 2:
        n = min(len(span_f0), len(follow_f0))
        try:
            corr = float(np.corrcoef(span_f0[:n], follow_f0[:n])[0, 1])
        except Exception:
            corr = float("nan")
        if not np.isnan(corr):
            note = "평행한 운율 - 강조 반복(C)일 가능성" if corr >= 0.5 else "다른 운율 - 강조 반복 아닐 가능성"
            lines.append(f"- 판별 대상 구간과 이어지는 구간의 F0 곡선 유사도: {corr:.2f} ({note})")

    span_rms, follow_rms = rms_list(range(i1, i2)), rms_list(range(follow_i1, follow_i2))
    if span_rms and follow_rms:
        s_med, f_med = statistics.median(span_rms), statistics.median(follow_rms)
        if s_med > 0:
            ratio = f_med / s_med
            if ratio >= 1.2:
                lines.append(f"- 이어지는 구간의 에너지가 판별 대상 구간보다 {ratio:.2f}배 큼 "
                             f"(수정 단어 강조 마킹 - A/B 케이스 근거)")

    return "\n".join(lines) if lines else "- (이 구간은 음향 신호가 뚜렷하지 않음)"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    compute(video_dir(args.folder))


if __name__ == "__main__":
    main()
