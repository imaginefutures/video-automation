"""Detect NG (restart) candidates two ways (PLAN.md 4.3, 4.4a):

1. Alignment mode (--edited given): diff a raw take's transcript against its human-edited
   cut to auto-derive labels from what the editor actually removed.
2. Standalone mode (--edited omitted): scan a single transcript for the same self-contained
   signals (word fragments, internal repetition) without a reference edit to compare against.
   `following_text_in_raw`/`similarity_to_following` come from a sliding window over the same
   transcript instead of the editor's cut.

Usage:
    python scripts/detect_ng_candidates.py <raw_transcript.json> --edited <edited_transcript.json> [--out-dir DIR]
    python scripts/detect_ng_candidates.py <transcript.json> [--out-dir DIR]
"""
from __future__ import annotations
import argparse
import json
import difflib
from pathlib import Path

PAUSE_MAX_DUR = 1.2       # seconds: a deleted run this short with no restart pattern -> pause/tighten
RESTART_SIM_MIN = 0.55    # difflib ratio: deleted block vs the words that follow it


def load_words(path: Path) -> list[dict]:
    d = json.loads(path.read_text())
    return [w for w in d["words"] if w["type"] == "word"]


def norm(text: str) -> str:
    return text.strip().rstrip(".,!?~…。，").lower()


def has_word_fragment(words: list[dict]) -> bool:
    """Scribe marks a self-interrupted, truncated word with a trailing '--'."""
    return any(w["text"].strip().endswith("--") for w in words)


def has_internal_repetition(words: list[dict]) -> bool:
    """Same normalized token appears twice within a short window inside the deleted span
    itself (stutter/restart), independent of what follows."""
    toks = [norm(w["text"]) for w in words if norm(w["text"])]
    for i, t in enumerate(toks):
        if not t:
            continue
        for j in range(i + 1, min(i + 4, len(toks))):
            if toks[j] == t:
                return True
    return False


def find_standalone_runs(words: list[dict], norm_toks: list[str]) -> list[dict]:
    """No reference edit to diff against: flag self-contained candidates directly by
    scanning for fragment/repetition signals, then merge adjacent hits into runs."""
    flagged = set()
    for i, w in enumerate(words):
        if w["text"].strip().endswith("--"):
            flagged.add(i)
        t = norm_toks[i]
        if not t:
            continue
        for j in range(i + 1, min(i + 4, len(words))):
            if norm_toks[j] == t:
                flagged.add(i)
                flagged.add(j)

    if not flagged:
        return []

    idxs = sorted(flagged)
    runs, cur = [], [idxs[0]]
    for i in idxs[1:]:
        if i - cur[-1] <= 3:  # small gap tolerance: same disfluent burst
            cur.append(i)
        else:
            runs.append(cur)
            cur = [i]
    runs.append(cur)
    return [{"i1": r[0], "i2": r[-1] + 1, "opcode_idx": n, "tag": "candidate"} for n, r in enumerate(runs)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("raw", type=Path, help="Transcript JSON to scan (the take/source being edited)")
    ap.add_argument("--edited", type=Path, default=None,
                     help="Optional human-edited cut's transcript JSON, for alignment mode")
    ap.add_argument("--out-dir", type=Path,
                     default=Path("/Users/jiho-mac/Projects/video-automation/Reference/gold_data_v2"),
                     help="Where to write <stem>_candidates.json")
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    raw = load_words(args.raw)
    raw_norm = [norm(w["text"]) for w in raw]

    if args.edited:
        edited = load_words(args.edited)
        edited_norm = [norm(w["text"]) for w in edited]
        sm = difflib.SequenceMatcher(None, raw_norm, edited_norm, autojunk=False)
        opcodes = sm.get_opcodes()
        equal_words = sum((i2 - i1) for tag, i1, i2, j1, j2 in opcodes if tag == "equal")
        print(f"raw words: {len(raw)}  edited words: {len(edited)}  matched(equal): {equal_words}")
        deleted_runs = [{"i1": i1, "i2": i2, "opcode_idx": idx, "tag": tag}
                         for idx, (tag, i1, i2, j1, j2) in enumerate(opcodes) if tag in ("delete", "replace")]
        print(f"deleted/replaced runs in raw: {len(deleted_runs)}")
    else:
        equal_words = None
        deleted_runs = find_standalone_runs(raw, raw_norm)
        print(f"raw words: {len(raw)}  (standalone mode, no reference edit)")
        print(f"self-contained candidate runs: {len(deleted_runs)}")

    results = []
    for run in deleted_runs:
        i1, i2 = run["i1"], run["i2"]
        seg_words = raw[i1:i2]
        if not seg_words:
            continue
        text = " ".join(w["text"] for w in seg_words)
        start = seg_words[0]["start"]
        end = seg_words[-1]["end"]
        dur = round(end - start, 3)

        # look at what follows this deleted run in RAW (next up to len(seg) words, capped)
        follow_n = max(len(seg_words), 3)
        follow_words = raw[i2:i2 + follow_n]
        follow_text = " ".join(w["text"] for w in follow_words)
        follow_norm = [norm(w["text"]) for w in follow_words]
        seg_norm_list = raw_norm[i1:i2]
        sim = difflib.SequenceMatcher(None, seg_norm_list, follow_norm, autojunk=False).ratio()
        # prefix-only similarity: catches self-repair where only the sentence OPENING
        # repeats before the speaker diverges into a different continuation
        k = min(4, len(seg_norm_list), len(follow_norm))
        prefix_sim = (difflib.SequenceMatcher(None, seg_norm_list[:k], follow_norm[:k], autojunk=False).ratio()
                      if k else 0.0)

        speakers = {w["speaker_id"] for w in seg_words}
        dominant_speaker = max(speakers, key=lambda s: sum(1 for w in seg_words if w["speaker_id"] == s))
        fragment = has_word_fragment(seg_words)
        internal_rep = has_internal_repetition(seg_words)

        # classification heuristic
        # multi-speaker spans are NOT decided by local self-repair signals (4.6a):
        # word repetition across two speakers' back-and-forth is dialogue, not one
        # person's stutter. Route to the whole-context pass instead.
        if len(speakers) > 1:
            label = "MULTI_SPEAKER_CONTEXT_CHECK"
            reason = f"{len(speakers)} speakers in span -> route to 4.6a whole-context pass, not local NG rules"
        elif fragment or internal_rep:
            label = "NG_CANDIDATE"
            sig = []
            if fragment:
                sig.append("word fragment (--)")
            if internal_rep:
                sig.append("internal repetition")
            reason = f"self-contained self-repair signal: {', '.join(sig)}"
        elif sim >= RESTART_SIM_MIN or prefix_sim >= 0.9:
            label = "NG_CANDIDATE"
            reason = f"restart-like: block sim={sim:.2f}, prefix sim={prefix_sim:.2f}"
        elif dur <= PAUSE_MAX_DUR and len(seg_words) <= 3:
            label = "PAUSE_OR_TIGHTEN"
            reason = f"short deleted run ({dur}s, {len(seg_words)} words), no restart pattern"
        else:
            label = "NEEDS_HUMAN_REVIEW"
            reason = f"deleted {dur}s / {len(seg_words)} words, no clear pattern (sim={sim:.2f})"

        results.append({
            "raw_word_index_start": i1,
            "raw_word_index_end": i2,
            "follow_word_index_start": i2,
            "follow_word_index_end": i2 + len(follow_words),
            "start": start,
            "end": end,
            "duration": dur,
            "n_words": len(seg_words),
            "deleted_text": text,
            "following_text_in_raw": follow_text,
            "similarity_to_following": round(sim, 3),
            "prefix_similarity": round(prefix_sim, 3),
            "dominant_speaker": dominant_speaker,
            "n_speakers_in_run": len(speakers),
            "has_word_fragment": fragment,
            "has_internal_repetition": internal_rep,
            "label": label,
            "reason": reason,
        })

    by_label = {}
    for r in results:
        by_label.setdefault(r["label"], []).append(r)

    for label, items in by_label.items():
        total_dur = sum(r["duration"] for r in items)
        print(f"  {label}: {len(items)} runs, {total_dur:.1f}s total")

    mode = "alignment" if args.edited else "standalone"
    out_path = args.out_dir / f"{args.raw.stem}_candidates.json"
    out_path.write_text(json.dumps({
        "mode": mode,
        "raw_source": str(args.raw),
        "edited_source": str(args.edited) if args.edited else None,
        "raw_words": len(raw),
        "edited_words": len(edited) if args.edited else None,
        "matched_words": equal_words,
        "deleted_runs": results,
    }, ensure_ascii=False, indent=2))
    print(f"\nwrote {out_path} ({len(results)} runs, mode={mode})")


if __name__ == "__main__":
    main()
