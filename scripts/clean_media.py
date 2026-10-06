"""Strip metadata/data tracks that make Final Cut Pro reject otherwise-valid media (PLAN.md 5장).

Root cause (found 2026-09-28): a `tmcd` (QuickTime timecode) data track on real camera
footage made Final Cut Pro's importer silently refuse the file - it wouldn't even show up
in File > Import > Media, and any FCPXML referencing it failed every asset-clip with
"invalid edit with no respective media", regardless of how correct the XML itself was.

This does a lossless stream copy (video + audio only, no re-encode) with faststart, so it's
fast and produces no quality loss. Always run this before export_fcpxml.py; ASR/video-use
steps are unaffected by the tmcd track and don't need the cleaned file.

Usage:
    python scripts/clean_media.py <video.mp4> [--out cleaned.mp4]
"""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("--out", type=Path, default=None,
                     help="Default: <stem>_clean.mp4 next to the source")
    args = ap.parse_args()

    out_path = args.out or args.video.with_name(f"{args.video.stem}_clean.mp4")
    # 임시 이름에 쓰고 다 끝나면 rename - 10-06: 최종 이름에 바로 쓰다가 프로세스가 중간에 죽어
    # 반쪽짜리 clean.mp4가 남았고, run.py는 "파일이 있으니 정리 끝"으로 보고 매번 건너뛰어
    # 다음 단계(전사)가 ffmpeg Invalid data(종료 코드 183)로 계속 실패했다. 확장자는 .mp4로
    # 끝나야 ffmpeg가 출력 형식을 안다.
    tmp_path = out_path.with_name(f"{out_path.stem}.part.mp4")

    cmd = [
        "ffmpeg", "-y", "-i", str(args.video),
        "-map", "0:v:0", "-map", "0:a:0",
        "-map_metadata", "-1",
        "-c", "copy",
        "-movflags", "+faststart",
        str(tmp_path),
    ]
    print(f"cleaning {args.video.name} -> {out_path.name} (stream copy, lossless)")
    try:
        subprocess.run(cmd, check=True)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise
    tmp_path.replace(out_path)
    print(f"wrote {out_path} ({out_path.stat().st_size / 1e9:.2f} GB)")


if __name__ == "__main__":
    main()
