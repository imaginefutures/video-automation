"""Render preview.mp4 from an EDL (PLAN.md 5.2): kept segments, 720p, hardware encode.

Each kept segment is re-encoded on its own (so cuts land on exact frames, not keyframes),
then the pieces are concatenated without re-encoding. 30ms audio fades at every segment
edge avoid pops at the joins. On Apple Silicon `h264_videotoolbox` renders a 24-minute
1080p take to 720p in about a minute; pass --software to use libx264 elsewhere.

Usage:
    python scripts/render_preview.py <edl.json> --source <clean.mp4> --out <preview.mp4> [--height 720] [--software]
"""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

FADE = 0.03


def render(edl_path: Path, source: Path, out: Path, height: int = 720, software: bool = False) -> Path:
    edl = json.loads(edl_path.read_text())
    segments = edl["kept_segments"]
    vcodec = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23"] if software else \
             ["-c:v", "h264_videotoolbox", "-b:v", "4M"]

    with tempfile.TemporaryDirectory(prefix="preview_") as tmp:
        tmpdir = Path(tmp)
        parts = []
        for i, seg in enumerate(segments):
            start, end = seg["source_start"], seg["source_end"]
            dur = end - start
            if dur <= 0.01:
                continue
            part = tmpdir / f"part_{i:04d}.mp4"
            afade = f"afade=t=in:st=0:d={FADE},afade=t=out:st={max(0.0, dur - FADE):.3f}:d={FADE}"
            cmd = ["ffmpeg", "-y", "-loglevel", "error",
                   "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(source),
                   "-vf", f"scale=-2:{height}", *vcodec,
                   "-af", afade, "-c:a", "aac", "-b:a", "128k",
                   "-movflags", "+faststart", str(part)]
            subprocess.run(cmd, check=True)
            parts.append(part)
            print(f"  segment {i + 1}/{len(segments)} ({dur:.1f}s)", flush=True)

        concat_list = tmpdir / "list.txt"
        concat_list.write_text("".join(f"file '{p}'\n" for p in parts))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", str(concat_list), "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
    total = sum(s["source_end"] - s["source_start"] for s in segments)
    print(f"wrote {out} ({total:.1f}s, {len(parts)} segments)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("edl", type=Path)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--software", action="store_true")
    args = ap.parse_args()
    render(args.edl, args.source, args.out, args.height, args.software)


if __name__ == "__main__":
    main()
