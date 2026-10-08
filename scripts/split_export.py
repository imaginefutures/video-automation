"""주제별 분할 내보내기 (docs/백로그/주제별-분할.md S3) - 확정한 경계대로 편별 mp4 + 대본 txt를 만든다.

- 경계 시각은 분할 화면과 같은 함수(propose_segments.segments_from_ends)로 계산한다 - 화면에서 본
  길이와 실제 파일이 어긋나지 않게. 1편은 0초부터, 마지막 편은 영상 끝까지라 이어 붙이면 원본과 같다
- 재인코딩한다: 스트림 복사는 키프레임에서만 잘려 시작이 앞 문장 끝으로 밀릴 수 있다. Mac 하드웨어
  인코더로 원본과 같은 비트레이트를 줘서 손실이 눈에 안 보이게 한다
- 경계에서 소리가 툭 끊기지 않게 앞뒤 FADE_SEC 오디오 페이드
- 대본은 같은 경계에서 끊기고, 사용자가 화면에서 고친 글자(text_edits)가 반영된다
- 자막(NN_<제목>.srt)은 내보낸 영상 시간에 맞춘다 - 인트로가 붙은 편은 그만큼 뒤로 민다. 긴 문장은
  SRT_MAX_CHARS 안쪽으로 띄어쓰기에서 나누고 글자 수에 비례해 시간을 나눈다
- 편마다 고른 인트로 이미지(split_intro.py)를 앞에 INTRO_SEC, 공통 아웃트로(brand/outro.png)를 뒤에
  OUTRO_SEC 붙인다. 둘 다 검은 화면에서 FADE_IMG_SEC 동안 페이드 인·아웃, 그동안 소리는 무음. 인트로가 끝나며
  본편으로 넘어가는 페이드 아웃만 INTRO_FADE_OUT_SEC로 길게 - 0.2초는 너무 갑작스럽다(10-08 사용자)

Writes <folder>/out/NN_<제목>.mp4, NN_<제목>.txt, 목록.txt 와 work/export.json (내보낸 시각·파일).
out/은 내보낼 때마다 이 스크립트가 만든 파일만 지우고 새로 만든다 (제목이 바뀌면 옛 이름이 남지 않게).

Usage:
    python scripts/split_export.py <splits/NAME>
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Callable

from common import BRAND_OUTRO, edit_dir, source_media, write_json
from audio_map import load_audio_map
from propose_segments import segments_from_ends
from split_sentences import load_sentences

FADE_SEC = 0.03
INTRO_SEC = 3.0
OUTRO_SEC = 2.0
FADE_IMG_SEC = 0.2
INTRO_FADE_OUT_SEC = 0.8
MAIN_FADE_IN_SEC = 0.5      # 인트로 뒤 검은 화면에서 본편이 서서히 밝아지게 (화면만 - 첫 말소리가 묻히지 않게 소리는 그대로)
PARAGRAPH_GAP_SEC = 2.0        # 대본에서 이만큼 쉬면 문단을 나눈다
LIST_NAME = "목록.txt"
SRT_MAX_CHARS = 42


def fmt_clock(t: float) -> str:
    return f"{int(t // 60):02d}:{int(t % 60):02d}"


def fmt_len(t: float) -> str:
    return f"{int(t // 60)}:{int(round(t % 60)):02d}"


def safe_name(title: str, n: int) -> str:
    base = re.sub(r'[\\/:*?"<>|\n\r\t]', " ", title).strip().strip(".")
    base = re.sub(r"\s+", " ", base)[:60] or f"{n}편"
    return f"{n:02d}_{base}"


def video_bitrate(media: Path) -> int:
    """원본 영상 비트레이트(bps). 스트림 값이 없으면 전체 비트레이트의 95%."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=bit_rate:format=bit_rate", "-of", "json", str(media)],
                         capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    v = (d.get("streams") or [{}])[0].get("bit_rate")
    if v and v.isdigit():
        return int(v)
    f = d.get("format", {}).get("bit_rate")
    return int(int(f) * 0.95) if f and f.isdigit() else 12_000_000


def has_videotoolbox() -> bool:
    out = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
    return "h264_videotoolbox" in out


def load_decisions(work: Path) -> dict:
    p = work / "split_decisions.json"
    if p.exists():
        return json.loads(p.read_text())
    segs = json.loads((work / "segments.json").read_text())["segments"]
    return {"ends": [s["end_sent"] for s in segs], "titles": [s.get("title", "") for s in segs], "text_edits": {}}


def script_text(title: str, seg: dict, sents: list[dict], edits: dict) -> str:
    paras, cur = [], []
    for i in range(seg["start_sent"], seg["end_sent"] + 1):
        cur.append(edits.get(str(i), sents[i]["text"]))
        if sents[i]["gap_after"] >= PARAGRAPH_GAP_SEC and i != seg["end_sent"]:
            paras.append(" ".join(cur)); cur = []
    if cur:
        paras.append(" ".join(cur))
    head = f"{title}\n길이 {fmt_len(seg['duration'])} · 원본 {fmt_clock(seg['start'])}~{fmt_clock(seg['end'])}"
    return head + "\n\n" + "\n\n".join(paras) + "\n"


def video_shape(media: Path) -> tuple[int, int, bool]:
    """(가로, 세로, 소리 있음) - 이미지를 본편 크기에 맞추고 무음 길이를 같은 형식으로 만들려고."""
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height", "-of", "json",
                          str(media)], capture_output=True, text=True, check=True).stdout
    streams = json.loads(out).get("streams", [])
    v = next(s for s in streams if s.get("codec_type") == "video")
    return int(v["width"]), int(v["height"]), any(s.get("codec_type") == "audio" for s in streams)


def card_filter(idx: int, label: str, sec: float, w: int, h: int, fps: float, fade_out: float = FADE_IMG_SEC) -> str:
    """정지 이미지 -> 본편과 같은 크기·fps의 sec초 영상, 검은 화면에서 페이드 인·아웃. 비율이 다르면 여백."""
    fade, fade_out = min(FADE_IMG_SEC, sec / 3), min(fade_out, sec / 2)
    return (f"[{idx}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,"
            f"fps={fps:.6f},format=yuv420p,trim=end_frame={max(1, round(sec * fps))},setpts=PTS-STARTPTS,"
            f"fade=t=in:d={fade},fade=t=out:st={sec - fade_out:.3f}:d={fade_out}[{label}v]")


def srt_clock(t: float) -> str:
    ms = max(0, round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def chunk_text(text: str, limit: int = SRT_MAX_CHARS) -> list[str]:
    out, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > limit:
            out.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    return out + ([cur] if cur else [])


def srt_text(seg: dict, sents: list[dict], edits: dict, offset: float) -> str:
    """편 영상 기준 시간의 자막. offset = 본편 앞에 붙은 인트로 길이."""
    cues, lo, hi = [], offset, offset + seg["duration"]
    for i in range(seg["start_sent"], seg["end_sent"] + 1):
        t0 = min(hi, max(lo, sents[i]["start"] - seg["start"] + offset))
        t1 = min(hi, max(t0, sents[i]["end"] - seg["start"] + offset))
        parts = chunk_text(edits.get(str(i), sents[i]["text"]))
        total, span = sum(len(x) for x in parts) or 1, t1 - t0
        for part in parts:
            d = span * len(part) / total
            cues.append((t0, t0 + d, part))
            t0 += d
    return "".join(f"{n}\n{srt_clock(a)} --> {srt_clock(b)}\n{txt}\n\n" for n, (a, b, txt) in enumerate(cues, 1) if b > a)


def encode(media: Path, start: float, dur: float, dest: Path, vbit: int, hw: bool, fps: float,
           shape: tuple[int, int, bool], intro: Path | None = None, outro: Path | None = None) -> None:
    """영상은 프레임 수로 자른다 - 길이(-t)만 주면 ffmpeg가 끝에 한 프레임을 더 넣는 경우가 있어
    (10-08 실측) 앞 편 마지막 프레임에 다음 편의 새 자막·새 장면이 찍혔다. 경계 시각은 split_refine이
    프레임 시작 바로 앞에 두므로 시작 프레임은 -ss로, 끝은 프레임 수(trim=end_frame)로 정확히 정해진다."""
    w, h, has_audio = shape
    n_frames = max(1, round(dur * fps))
    fade_out = max(0.0, dur - FADE_SEC)
    vcodec = (["-c:v", "h264_videotoolbox", "-b:v", str(vbit), "-maxrate", str(int(vbit * 1.5)),
               "-bufsize", str(vbit * 2)] if hw else ["-c:v", "libx264", "-crf", "16", "-preset", "medium"])
    # -ss를 -i 앞에 두면 빠르게 찾고, 재인코딩이라 프레임 단위로 정확하다
    inputs = ["-ss", f"{start:.4f}", "-t", f"{dur + 1:.4f}", "-i", str(media)]
    aform = "aformat=sample_rates=48000:channel_layouts=stereo"
    main_fade = f",fade=t=in:d={MAIN_FADE_IN_SEC}" if intro else ""
    graph = [f"[0:v]trim=end_frame={n_frames},setpts=PTS-STARTPTS,setsar=1,format=yuv420p{main_fade}[mv]",
             (f"[0:a]atrim=duration={dur:.4f},asetpts=PTS-STARTPTS,{aform},"
              f"afade=t=in:d={FADE_SEC},afade=t=out:st={fade_out:.3f}:d={FADE_SEC}[ma]") if has_audio
             else f"anullsrc=r=48000:cl=stereo,atrim=duration={dur:.4f}[ma]"]
    order = []
    for label, img, sec in (("i", intro, INTRO_SEC), ("m", None, dur), ("o", outro, OUTRO_SEC)):
        if label != "m" and not img:
            continue
        if img:
            idx = inputs.count("-i")
            inputs += ["-loop", "1", "-t", f"{sec + 1:.3f}", "-i", str(img)]
            graph.append(card_filter(idx, label, sec, w, h, fps, INTRO_FADE_OUT_SEC if label == "i" else FADE_IMG_SEC))
            graph.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={round(sec * fps) / fps:.4f}[{label}a]")
        order.append(label)
    graph.append("".join(f"[{l}v][{l}a]" for l in order) + f"concat=n={len(order)}:v=1:a=1[v][a]")
    part = dest.with_suffix(".part.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]",
         *vcodec, "-pix_fmt", "yuv420p", "-r", f"{fps:.6f}", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(part)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    part.rename(dest)


def intro_paths(folder: Path, dec: dict, n: int) -> list[Path | None]:
    """편마다 고른 인트로 이미지. 고르지 않았거나 파일이 사라졌으면 None (그 편은 인트로 없이)."""
    from split_intro import image_file
    names = list(dec.get("intros") or []) + [None] * n
    out: list[Path | None] = []
    for name in names[:n]:
        try:
            out.append(image_file(folder, name) if name else None)
        except ValueError:
            out.append(None)
    return out


def export(folder: Path, progress: Callable[[int, int, str], None] | None = None) -> dict:
    work = edit_dir(folder)
    media = source_media(folder)
    sdata = load_sentences(folder)
    sents, duration = sdata["sentences"], sdata["duration"]
    dec = load_decisions(work)
    amap = load_audio_map(folder)
    from split_refine import refine_all
    if progress:
        progress(0, len(dec["ends"]), "경계 다듬는 중")
    refined = refine_all(folder, dec["ends"], sents, amap)
    segs = segments_from_ends(dec["ends"], sents, duration, amap, refined)
    edits = {str(k): v for k, v in (dec.get("text_edits") or {}).items()}

    out = folder / "out"
    out.mkdir(exist_ok=True)
    prev = json.loads((work / "export.json").read_text()) if (work / "export.json").exists() else {}
    for name in prev.get("files", []) + [LIST_NAME]:  # 지난 내보내기가 만든 것만 지운다
        (out / name).unlink(missing_ok=True)
    for stale in out.glob("*.part.mp4"):
        stale.unlink()

    from split_refine import video_fps
    vbit, hw, fps, shape = video_bitrate(media), has_videotoolbox(), video_fps(media), video_shape(media)
    intros = intro_paths(folder, dec, len(segs))
    outro = BRAND_OUTRO if BRAND_OUTRO.exists() else None
    files, items, lines = [], [], [f"{folder.name} - {len(segs)}편", ""]
    for k, seg in enumerate(segs):
        title = dec["titles"][k] if k < len(dec["titles"]) and dec["titles"][k] else f"{k + 1}편"
        base = safe_name(title, k + 1)
        if progress:
            progress(k, len(segs), title)
        encode(media, seg["start"], seg["duration"], out / f"{base}.mp4", vbit, hw, fps, shape, intros[k], outro)
        (out / f"{base}.txt").write_text(script_text(title, seg, sents, edits), encoding="utf-8")
        (out / f"{base}.srt").write_text(srt_text(seg, sents, edits, INTRO_SEC if intros[k] else 0.0), encoding="utf-8")
        files += [f"{base}.mp4", f"{base}.txt", f"{base}.srt"]
        total = seg["duration"] + (INTRO_SEC if intros[k] else 0) + (OUTRO_SEC if outro else 0)
        items.append({"n": k + 1, "title": title, "duration": total, "mp4": f"{base}.mp4", "txt": f"{base}.txt", "srt": f"{base}.srt",
                      "intro": bool(intros[k]), "outro": bool(outro)})
        lines.append(f"{k + 1:2d}. {title}  ({fmt_len(seg['duration'])}, 원본 {fmt_clock(seg['start'])}~{fmt_clock(seg['end'])})")
    (out / LIST_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8")
    if progress:
        progress(len(segs), len(segs), "")

    info = {"at": datetime.now().isoformat(timespec="seconds"), "decisions_updated_at": dec.get("updated_at"),
            "count": len(segs), "files": files, "items": items, "encoder": "h264_videotoolbox" if hw else "libx264",
            "video_bitrate": vbit}
    write_json(work / "export.json", info)
    return info


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    from split_run import resolve_folder
    folder = resolve_folder(args.folder)
    info = export(folder, lambda k, n, t: print(f"[{k}/{n}] {t}"))
    print(f"wrote {folder / 'out'} ({info['count']}편, {info['encoder']})")


if __name__ == "__main__":
    main()
