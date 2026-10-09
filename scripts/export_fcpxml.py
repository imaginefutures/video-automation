"""Export an EDL (build_edl.py output) to FCPXML for Final Cut Pro (PLAN.md 5장). Verified on FCP 12.3 with version 1.11.

The rough-cut spine contains only the kept segments - source media is referenced, never
copied or re-encoded, so every cut is reversible by trimming in Final Cut (PLAN.md 2.1).

Markers (PLAN.md 5장):
  - REVIEW candidates -> to-do markers (completed="0", shows as FCP's checklist marker,
    the editor works through and checks off) - covers everything not yet auto-cleared:
    NG candidates below the confidence threshold, PAUSE_OR_TIGHTEN, and
    MULTI_SPEAKER_CONTEXT_CHECK spans (4.6a).
  - AUTO_SAFE cuts -> standard markers on the very start of the clip right after the cut,
    noting what text was removed and why, so the editor can see what happened without
    playing through - and can recover it by trimming the clip earlier (2.1).
  - AUTO_SAFE + KEEP -> no marker. Nothing happened here; no need to draw attention to it.

All times are expressed as exact multiples of the source frame duration (rational,
e.g. "45045/30000s") so nothing drifts under Final Cut's frame-accurate timeline.

By default the source media is referenced by a RELATIVE path from the .fcpxml's own
location (no file:// scheme) - this is what lets the .fcpxml and the video travel
together as one portable folder: drop both on another machine, in the same relative
layout, and it opens without editing anything. Pass --absolute-media-path to embed a
fixed file:// path instead (only correct on the machine it was generated on).

Usage:
    python scripts/export_fcpxml.py <edl.json> --source <video_path> --width 1920 --height 1080 \\
        --frame-duration 1001/30000 [--out out.fcpxml] [--absolute-media-path]
"""
from __future__ import annotations
import argparse
import json
from os.path import relpath
from pathlib import Path
from xml.sax.saxutils import escape as _escape


def escape(s: str) -> str:
    """escape() alone does not escape quotes, which corrupts XML attribute values."""
    return _escape(s, {'"': "&quot;", "'": "&apos;"})


def parse_frame_duration(s: str) -> tuple[int, int]:
    num, den = s.split("/")
    return int(num), int(den)


class RationalClock:
    """Snaps every time value to a whole number of source frames and renders FCPXML time strings."""

    def __init__(self, frame_num: int, frame_den: int):
        self.frame_num = frame_num  # e.g. 1001
        self.frame_den = frame_den  # e.g. 30000
        self.fps = frame_den / frame_num

    def frames(self, seconds: float) -> int:
        return round(seconds * self.fps)

    def time_str(self, seconds: float) -> str:
        return self.time_str_frames(self.frames(seconds))

    def duration_str(self, seconds: float) -> str:
        return self.time_str_frames(max(1, self.frames(seconds)))  # never emit a zero-duration element

    def time_str_frames(self, f: int) -> str:
        return f"{f * self.frame_num}/{self.frame_den}s"


def find_containing_segment(segments: list[dict], t: float) -> dict | None:
    for seg in segments:
        if seg["source_start"] - 0.001 <= t <= seg["source_end"] + 0.001:
            return seg
    return None


def _marker_duration_frames(clock: RationalClock, seg_end_frames: int, start_frames: int) -> int:
    """Marker's own duration, clamped so it never extends past its parent clip's end."""
    wanted = max(1, clock.frames(0.1))
    room = max(1, seg_end_frames - start_frames)
    return min(wanted, room)


def build_markers_xml(edl: dict, clock: RationalClock, kept_segments: list[dict],
                       seg_start_frames: list[int], seg_dur_frames: list[int]) -> dict[int, list[str]]:
    """Returns {segment_index: [marker_xml, ...]}.

    Marker <start> uses the SAME coordinate space as its parent asset-clip's own `start`
    attribute - i.e. absolute SOURCE-media time, not a position relative to the clip's
    timeline offset. (This is what lets a marker keep its correct position if the clip is
    later trimmed in Final Cut - the marker is anchored to the source, not the edit.)
    """
    by_segment: dict[int, list[str]] = {i: [] for i in range(len(kept_segments))}

    cut_spans = edl["cut_spans"]
    # kept_segments[i] (i >= 1) directly follows cut_spans[i-1] in this EDL's construction
    for i, span in enumerate(cut_spans):
        seg_idx = i + 1
        if seg_idx >= len(kept_segments):
            continue
        seg = kept_segments[seg_idx]
        start_frames = clock.frames(seg["source_start"])
        dur_frames = _marker_duration_frames(clock, start_frames + seg_dur_frames[seg_idx], start_frames)
        value = escape(f"[CUT] {span['n_source_runs']}개 구간 제거됨 ({span['end']-span['start']:.1f}s)")
        by_segment[seg_idx].append(
            f'<marker start="{clock.time_str_frames(start_frames)}" '
            f'duration="{clock.time_str_frames(dur_frames)}" value="{value}"/>'
        )

    for m in edl["markers"]:
        if m["route"] != "REVIEW":
            continue
        seg = find_containing_segment(kept_segments, m["start"])
        if seg is None:
            continue  # candidate fell inside a cut span - already covered by the CUT marker
        seg_idx = kept_segments.index(seg)
        seg_end_frames = clock.frames(seg["source_start"]) + seg_dur_frames[seg_idx]
        start_frames = min(clock.frames(m["start"]), seg_end_frames - 1)
        start_frames = max(start_frames, clock.frames(seg["source_start"]))
        dur_frames = _marker_duration_frames(clock, seg_end_frames, start_frames)
        clf = m.get("llm_classification") or {}
        case = clf.get("case", "-")
        text = (m.get("deleted_text") or "")[:60]
        value = escape(f"[REVIEW:{m['label']}/{case}] {text}")
        note = escape(m.get("route_reason", ""))
        by_segment[seg_idx].append(
            f'<marker start="{clock.time_str_frames(start_frames)}" '
            f'duration="{clock.time_str_frames(dur_frames)}" value="{value}" note="{note}" completed="0"/>'
        )
    return by_segment


def build_inserts_xml(inserts: list[dict], clock: RationalClock, kept_segments: list[dict], seg_offset_frames: list[int],
                      seg_dur_frames: list[int], out_path: Path, absolute: bool) -> tuple[list[str], dict[int, list[str]]]:
    """Approved inserts -> connected clips (docs/백로그/자료-화면-삽입.md 7장, verified on FCP 12.3 in V0).

    A connected clip lives INSIDE the spine clip that contains its timeline start, and its offset
    is in that parent's SOURCE time: child.offset = parent.start + (T - parent.offset). Each
    layer (e.g. image + yellow caption) gets its own lane above the speaker. Stills (PNG/JPG) use a
    format without a frame rate and asset duration 0s (verified in V0); motion clips (MP4) are
    rendered at the sequence rate and placed as asset-clips."""
    def timeline_frame(t: float) -> int:
        for i, seg in enumerate(kept_segments):
            if t < seg["source_start"]:
                return seg_offset_frames[i]  # starts inside a cut -> snap to the next kept frame
            if t < seg["source_end"]:
                return seg_offset_frames[i] + min(clock.frames(t - seg["source_start"]), seg_dur_frames[i] - 1)
        return seg_offset_frames[-1] + seg_dur_frames[-1] - 1

    resources = ['<format id="vautostill" name="FFVideoFormatRateUndefined" width="1920" height="1080" colorSpace="1-1-1 (Rec. 709)"/>']
    by_seg: dict[int, list[str]] = {}
    for n, ins in enumerate(inserts):
        t0 = timeline_frame(ins["start"])
        dur = max(timeline_frame(ins["end"]) - t0, clock.frames(1.0))
        i = max(k for k, off in enumerate(seg_offset_frames) if off <= t0)
        child_off = clock.frames(kept_segments[i]["source_start"]) + (t0 - seg_offset_frames[i])
        lane0 = int(ins.get("lane_base", 1))  # 구조 층(섹션 바)은 3부터 - 같은 때 뜨는 다른 인서트(1~2)와 겹치지 않게
        for k, layer in enumerate(ins["layers"]):
            f = Path(layer)
            ref = f"vins{n}_{k}"
            src = f.resolve().as_uri() if absolute else Path(relpath(f.absolute(), start=out_path.absolute().parent)).as_posix()
            if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
                resources.append(f'<asset id="{ref}" name="{escape(f.stem)}" start="0s" duration="0s" hasVideo="1" format="vautostill" videoSources="1">'
                                 f'<media-rep kind="original-media" src="{escape(src)}"/></asset>')
                by_seg.setdefault(i, []).append(
                    f'<video ref="{ref}" lane="{lane0 + k}" offset="{clock.time_str_frames(child_off)}" duration="{clock.time_str_frames(dur)}" '
                    f'role="{escape(ins["role"])}" name="{escape(ins["name"])}"/>')
            elif f.suffix.lower() in (".mp4", ".mov"):
                # motion inserts are rendered at the sequence frame rate (inserts.py FPS_*), video only
                import subprocess
                secs = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                            capture_output=True, text=True).stdout.strip() or 0)
                media_frames = max(1, clock.frames(secs))
                resources.append(f'<asset id="{ref}" name="{escape(f.stem)}" start="0s" duration="{clock.time_str_frames(media_frames)}" hasVideo="1" '
                                 f'format="vautofmt1" videoSources="1"><media-rep kind="original-media" src="{escape(src)}"/></asset>')
                by_seg.setdefault(i, []).append(
                    f'<asset-clip ref="{ref}" lane="{lane0 + k}" offset="{clock.time_str_frames(child_off)}" '
                    f'duration="{clock.time_str_frames(min(dur, media_frames))}" videoRole="{escape(ins["role"])}" name="{escape(ins["name"])}"/>')
            else:
                print(f"[inserts] {f.name}: unsupported layer type - skipped")
    return (resources if len(resources) > 1 else []), by_seg


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("edl", type=Path)
    ap.add_argument("--source", type=Path, required=True, help="Path to the source video file")
    ap.add_argument("--width", type=int, required=True)
    ap.add_argument("--height", type=int, required=True)
    ap.add_argument("--frame-duration", type=str, required=True, help="e.g. 1001/30000")
    ap.add_argument("--name", type=str, default=None, help="Project name (default: source file stem)")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--absolute-media-path", action="store_true",
                     help="Embed an absolute file:// path instead of the default relative "
                          "path (relative requires the video to sit next to the .fcpxml)")
    ap.add_argument("--fcpxml-version", type=str, default="1.11",
                     help="Declared FCPXML version (default 1.11, widely supported)")
    ap.add_argument("--no-markers", action="store_true",
                     help="Skip all markers - for isolating whether markers cause an import failure")
    ap.add_argument("--transition-frames", type=int, default=3,
                     help="Cross dissolve length at each join in frames (0 = hard cuts). Default 3 (~0.1s).")
    ap.add_argument("--inserts", type=Path, default=None,
                     help="inserts_manifest.json (scripts/inserts.py) - approved inserts placed as connected clips")
    args = ap.parse_args()

    out_path = args.out or args.edl.with_suffix(".fcpxml")

    edl = json.loads(args.edl.read_text())
    frame_num, frame_den = parse_frame_duration(args.frame_duration)
    clock = RationalClock(frame_num, frame_den)
    kept_segments = edl["kept_segments"]
    project_name = args.name or args.source.stem

    # Each segment's own duration is rounded to the nearest frame independently (like any
    # NLE); cumulative timeline offsets are then the EXACT integer sum of those rounded
    # frame-counts, never re-derived from raw seconds - otherwise independent rounding at
    # each step can drift the offset off the true cumulative sum by a frame, which Final
    # Cut would read as a gap or overlap between clips.
    # A sliver segment at the very end (e.g. 8ms after the last cut) rounds to a start frame
    # AT the media's last frame boundary; padding it to 1 frame then points past the media and
    # Final Cut rejects the clip ("invalid edit with no respective media"). Clamp every segment
    # to the media and drop the ones left with no whole frame.
    src_total_frames = clock.frames(edl["source_duration"])
    seg_dur_frames = []
    usable = []
    for seg in kept_segments:
        room = src_total_frames - clock.frames(seg["source_start"])
        d = min(max(1, clock.frames(seg["source_end"] - seg["source_start"])), room)
        if d >= 1:
            usable.append(seg)
            seg_dur_frames.append(d)
    kept_segments = usable
    seg_offset_frames = []
    acc = 0
    for d in seg_dur_frames:
        seg_offset_frames.append(acc)
        acc += d
    total_timeline_frames = acc

    markers_by_segment = build_markers_xml(edl, clock, kept_segments, seg_offset_frames, seg_dur_frames)
    insert_resources, inserts_by_segment = ([], {}) if args.inserts is None else build_inserts_xml(
        json.loads(args.inserts.read_text())["inserts"], clock, kept_segments, seg_offset_frames, seg_dur_frames,
        out_path, args.absolute_media_path)

    if args.absolute_media_path:
        src_ref = args.source.resolve().as_uri()
    else:
        # absolute(), not resolve(): a symlinked clean.mp4 must still be referenced by its
        # path inside the folder, or the fcpxml stops being portable with that folder
        rel = Path(relpath(args.source.absolute(), start=out_path.absolute().parent))
        src_ref = rel.as_posix()  # schemeless relative URI, resolved against the .fcpxml's own location
    asset_clips = []
    n_transitions = 0
    for i, seg in enumerate(kept_segments):
        markers_xml = "" if args.no_markers else "\n          ".join(markers_by_segment.get(i, []))
        # DTD order inside a clip: anchored (connected) clips come before markers
        markers_xml = "\n          ".join(inserts_by_segment.get(i, []) + ([markers_xml] if markers_xml else []))
        # A short cross dissolve at every join softens the jump cut and crossfades the audio.
        # It needs media handles on both sides (half the dissolve each), which the removed
        # region between two kept segments provides; skipped at the ends of the source.
        tf = args.transition_frames
        if i > 0 and tf > 0:
            prev = kept_segments[i - 1]
            half = (tf + 1) // 2
            left_ok = clock.frames(prev["source_end"]) + half <= src_total_frames
            right_ok = clock.frames(seg["source_start"]) - half >= 0
            if left_ok and right_ok and seg_dur_frames[i] > tf and seg_dur_frames[i - 1] > tf:
                t_off = seg_offset_frames[i] - half
                asset_clips.append(f'''        <transition name="Cross Dissolve" offset="{clock.time_str_frames(t_off)}" duration="{clock.time_str_frames(tf)}">
          <filter-video ref="vautofx1" name="Cross Dissolve"/>
        </transition>''')
                n_transitions += 1
        asset_clips.append(f'''        <asset-clip ref="vautoasset1" name="seg_{i+1:03d}" format="vautofmt1" offset="{clock.time_str_frames(seg_offset_frames[i])}"
          start="{clock.time_str(seg["source_start"])}" duration="{clock.time_str_frames(seg_dur_frames[i])}">
          {markers_xml}
        </asset-clip>''')

    fcpxml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="{args.fcpxml_version}">
  <resources>
    <format id="vautofmt1" name="FFVideoFormatCustom" frameDuration="{args.frame_duration}s"
      width="{args.width}" height="{args.height}" colorSpace="1-1-1 (Rec. 709)"/>
    <asset id="vautoasset1" name="{escape(args.source.stem)}" uid="VAUTOGEN0000000000000000000001" start="0/{frame_den}s"
      duration="{clock.duration_str(edl["source_duration"])}" hasVideo="1" format="vautofmt1"
      videoSources="1" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">
      <media-rep kind="original-media" src="{escape(src_ref)}"/>
    </asset>
    <effect id="vautofx1" name="Cross Dissolve" uid="FxPlug:4731E73A-8DAC-4113-9A30-AE85B1761265"/>{"".join(chr(10) + "    " + r for r in insert_resources)}
  </resources>
  <library>
    <event name="video-automation">
      <project name="{escape(project_name)} rough cut">
        <sequence format="vautofmt1" duration="{clock.time_str_frames(total_timeline_frames)}" tcStart="0/{frame_den}s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>
{chr(10).join(asset_clips)}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''

    out_path.write_text(fcpxml)

    n_review = sum(len(v) for k, v in markers_by_segment.items()) - len(edl["cut_spans"])
    print(f"kept segments: {len(kept_segments)}, timeline duration: {total_timeline_frames / clock.fps:.1f}s")
    print(f"cut markers: {len(edl['cut_spans'])}, review (to-do) markers: {n_review}, transitions: {n_transitions}")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
