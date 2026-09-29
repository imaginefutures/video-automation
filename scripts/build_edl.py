"""Build an EDL (cut list) from routed NG candidates (PLAN.md 3장 4'. EDL 생성).

Only AUTO_SAFE candidates whose LLM action is CUT are actually removed. Every other
candidate (REVIEW, KEEP, PAUSE_OR_TIGHTEN, MULTI_SPEAKER_CONTEXT_CHECK) stays in the
timeline untouched - this script never discards content a human hasn't cleared.

Boundary safety (PLAN.md 2.4 hard rule 4: 정상 발화 절대 보호):
each detected cut span is shrunk inward by BOUNDARY_PAD_SEC on both sides before
removal, so the actual edit never touches the word boundary Scribe reported - it
removes strictly less than what was flagged, never more.

Output edl.json:
  kept_segments: the complement of the cut spans over [0, source_duration] - what the
                 rough-cut timeline will actually contain, each with its source in/out.
  markers: every routed candidate, tagged with whether it was cut or left in, for
           export_fcpxml.py to place as FCP markers.

Usage:
    python scripts/build_edl.py <routed_candidates.json> --duration <source_seconds> [--out edl.json]
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

BOUNDARY_PAD_SEC = 0.015  # 15ms safety margin, inside PLAN.md's 10-20ms range


def compute_cut_spans(routed: list[dict]) -> list[dict]:
    """AUTO_SAFE + action=CUT candidates only, padded inward, merged if overlapping."""
    raw_spans = []
    for r in routed:
        clf = r.get("llm_classification")
        if r["route"] != "AUTO_SAFE" or not clf or clf["recommended_action"] != "CUT":
            continue
        start = r["start"] + BOUNDARY_PAD_SEC
        end = r["end"] - BOUNDARY_PAD_SEC
        if end <= start:
            continue  # span too short once padded - too risky, leave it in (falls through to markers only)
        raw_spans.append({"start": start, "end": end, "source_run": r})

    raw_spans.sort(key=lambda s: s["start"])
    merged: list[dict] = []
    for s in raw_spans:
        if merged and s["start"] <= merged[-1]["end"]:
            merged[-1]["end"] = max(merged[-1]["end"], s["end"])
            merged[-1]["source_runs"].append(s["source_run"])
        else:
            merged.append({"start": s["start"], "end": s["end"], "source_runs": [s["source_run"]]})
    return merged


def compute_kept_segments(cut_spans: list[dict], duration: float) -> list[dict]:
    """Complement of cut_spans over [0, duration]."""
    kept = []
    cursor = 0.0
    for span in cut_spans:
        if span["start"] > cursor:
            kept.append({"source_start": cursor, "source_end": span["start"]})
        cursor = max(cursor, span["end"])
    if cursor < duration:
        kept.append({"source_start": cursor, "source_end": duration})
    return [k for k in kept if k["source_end"] - k["source_start"] > 0.001]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("routed", type=Path)
    ap.add_argument("--duration", type=float, required=True, help="Source video duration in seconds")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    routed = json.loads(args.routed.read_text())
    cut_spans = compute_cut_spans(routed)
    kept_segments = compute_kept_segments(cut_spans, args.duration)

    total_cut = sum(s["end"] - s["start"] for s in cut_spans)
    print(f"source duration: {args.duration:.1f}s")
    print(f"cut spans (AUTO_SAFE + CUT, padded {BOUNDARY_PAD_SEC*1000:.0f}ms inward): "
          f"{len(cut_spans)} spans, {total_cut:.1f}s removed")
    print(f"kept segments: {len(kept_segments)}, {args.duration - total_cut:.1f}s remaining")
    print(f"markers to place: {len(routed)} (all routed candidates, none discarded from the record)")

    out_path = args.out or args.routed.with_name(args.routed.stem.replace("_routed", "") + "_edl.json")
    out_path.write_text(json.dumps({
        "source_duration": args.duration,
        "boundary_pad_sec": BOUNDARY_PAD_SEC,
        "kept_segments": kept_segments,
        "cut_spans": [{"start": s["start"], "end": s["end"],
                        "n_source_runs": len(s["source_runs"])} for s in cut_spans],
        "markers": routed,  # every candidate, executed or not - export step decides marker type
    }, ensure_ascii=False, indent=2))
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
