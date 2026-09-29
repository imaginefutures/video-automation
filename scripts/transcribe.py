"""Transcribe a video folder's media with ElevenLabs Scribe (word-level, diarized).

Writes <folder>/edit/transcript.json. Cached: skipped if that file already exists.
Uses edit/clean.mp4 when present (run clean_media.py first), else raw.mp4.

Usage:
    python scripts/transcribe.py <videos/NAME or folder> [--language kor] [--num-speakers N] [--force]
"""
from __future__ import annotations
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

from common import load_env, video_dir, edit_dir, source_media

SCRIBE_URL = "https://api.elevenlabs.io/v1/speech-to-text"


def extract_audio(video: Path, dest: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video), "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000",
         "-c:a", "pcm_s16le", str(dest)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def call_scribe(audio: Path, api_key: str, language: str | None, num_speakers: int | None) -> dict:
    data = {
        "model_id": "scribe_v1",
        "diarize": "true",
        "tag_audio_events": "true",
        "timestamps_granularity": "word",
    }
    if language:
        data["language_code"] = language
    if num_speakers:
        data["num_speakers"] = str(num_speakers)
    with open(audio, "rb") as f:
        resp = requests.post(SCRIBE_URL, headers={"xi-api-key": api_key},
                             files={"file": (audio.name, f, "audio/wav")}, data=data, timeout=1800)
    if resp.status_code != 200:
        raise RuntimeError(f"Scribe returned {resp.status_code}: {resp.text[:500]}")
    return resp.json()


def transcribe(folder: Path, language: str | None = "kor", num_speakers: int | None = None,
               force: bool = False) -> Path:
    out = edit_dir(folder) / "transcript.json"
    if out.exists() and not force:
        print(f"cached: {out}")
        return out
    load_env()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        sys.exit("ELEVENLABS_API_KEY not set (put it in the project .env)")
    media = source_media(folder)
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "audio.wav"
        print(f"extracting audio from {media.name}")
        extract_audio(media, wav)
        print(f"uploading to Scribe ({wav.stat().st_size / 1e6:.1f} MB)")
        payload = call_scribe(wav, api_key, language, num_speakers)
    out.write_text(__import__("json").dumps(payload, ensure_ascii=False, indent=2))
    n_words = sum(1 for w in payload.get("words", []) if w.get("type") == "word")
    print(f"wrote {out} ({n_words} words)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--language", default="kor")
    ap.add_argument("--num-speakers", type=int, default=None)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    transcribe(video_dir(args.folder), args.language, args.num_speakers, args.force)


if __name__ == "__main__":
    main()
