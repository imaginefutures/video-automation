"""Assemble every route=CUT item (NG/filler/context-review from ng.json, plus speaker-block
lines proposed for deletion) into one merged, word-index-normalized cut list - the unit the
seam-refinement loop (seam_refine.py) then works over (docs/기획/01-처리-과정.md 9단계).

ng.json items use an exclusive end index (raw_word_index_end = one past the last cut word,
matching Python slicing); speaker_blocks.json lines use an INCLUSIVE end index (wi_end is the
last word's own index) - this step normalizes both into the same (wi_start, wi_end_exclusive)
convention before merging, which is exactly the kind of index mismatch PLAN.md's own history
warns about (classify_candidates.py's load_words() docstring: "the three MUST agree on
indexing"). Overlapping/touching spans from different sources are merged into one cut entry
so the same stretch of audio isn't refined twice.

Only CUT-routed material is included here - KEEP items simply aren't cut, and pause trims are
handled separately by plan_pauses.py/build_edl.py (docs/기획/02-품질-루프.md 2.1: 부분 루프
대상은 쉼이 아닌 모든 이음새).

Usage:
    python scripts/assemble_draft.py <videos/NAME>
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from common import video_dir, edit_dir, load_transcript, words_only, write_json


def from_ng(ng_items: list[dict]) -> list[dict]:
    out = []
    for i, it in enumerate(ng_items):
        if it.get("route") != "CUT":
            continue
        clf = it.get("llm_classification") or {}
        out.append({
            "kind": "ng", "source_id": f"ng[{i}]",
            "wi_start": it["raw_word_index_start"], "wi_end": it["raw_word_index_end"],
            "flag": it.get("flag"), "flag_reason": it.get("route_reason", ""),
            "confidence": clf.get("confidence"),
            "made_by": it.get("llm_model") or "deterministic",
            "label": it.get("label"), "case": clf.get("case"),
            "evidence": clf.get("reasoning") or it.get("reason") or it.get("route_reason", ""),
        })
    return out


def from_speaker_blocks(blocks_doc: dict) -> list[dict]:
    made_by = "claude-sonnet-5" if blocks_doc.get("llm_labeled") else "deterministic"
    out = []
    for b in blocks_doc.get("blocks", []):
        for ln in b["lines"]:
            if ln.get("proposed") != "delete":
                continue
            out.append({
                "kind": "block_line", "source_id": f"block[{b['id']}].line[{ln['id']}]",
                "wi_start": ln["wi_start"], "wi_end": ln["wi_end"] + 1,  # inclusive -> exclusive
                "flag": "restore", "flag_reason": f"화자 이탈 블록 {b['id']} - {ln.get('role') or '역할 미분류'}",
                "confidence": None, "made_by": made_by,
                "label": f"SPEAKER_BLOCK_{ln.get('role') or 'UNLABELED'}", "case": None,
                "evidence": ln["text"],
            })
    return out


def merge(items: list[dict]) -> list[dict]:
    items = sorted(items, key=lambda x: (x["wi_start"], x["wi_end"]))
    merged: list[dict] = []
    for it in items:
        if merged and it["wi_start"] <= merged[-1]["wi_end"]:
            m = merged[-1]
            m["wi_end"] = max(m["wi_end"], it["wi_end"])
            m["sources"].append(it)
            if it.get("flag"):
                m["flag"] = "restore"
                m["flag_reasons"].append(it["flag_reason"])
        else:
            merged.append({"wi_start": it["wi_start"], "wi_end": it["wi_end"],
                           "flag": it.get("flag"), "flag_reasons": [it["flag_reason"]] if it.get("flag") else [],
                           "sources": [it]})
    return merged


def assemble(folder: Path) -> Path:
    words = words_only(load_transcript(folder))
    ng_path = edit_dir(folder) / "ng.json"
    ng_items = json.loads(ng_path.read_text()) if ng_path.exists() else []
    blocks_path = edit_dir(folder) / "speaker_blocks.json"
    blocks_doc = json.loads(blocks_path.read_text()) if blocks_path.exists() else {"blocks": []}

    raw = from_ng(ng_items) + from_speaker_blocks(blocks_doc)
    print(f"cut candidates before merge: {len(raw)} ({len(from_ng(ng_items))} ng, "
          f"{len(from_speaker_blocks(blocks_doc))} block lines)")

    merged = merge(raw)
    cuts = []
    for i, m in enumerate(merged):
        seg = words[m["wi_start"]:m["wi_end"]]
        if not seg:
            continue
        made_by_set = {s["made_by"] for s in m["sources"]}
        cuts.append({
            "id": i, "wi_start": m["wi_start"], "wi_end": m["wi_end"],
            "start": seg[0]["start"], "end": seg[-1]["end"],
            "text": " ".join(w["text"] for w in seg),
            "flag": m["flag"], "flag_reason": "; ".join(m["flag_reasons"]) or None,
            "made_by": next(iter(made_by_set)) if len(made_by_set) == 1 else "mixed",
            "n_sources": len(m["sources"]), "sources": m["sources"],
        })

    total_dur = sum(c["end"] - c["start"] for c in cuts)
    n_flagged = sum(1 for c in cuts if c["flag"])
    print(f"merged into {len(cuts)} cut span(s), {total_dur:.1f}s total "
          f"({n_flagged} flagged as restore candidates)")

    out = edit_dir(folder) / "draft_cuts.json"
    write_json(out, {"cuts": cuts})
    print(f"wrote {out}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    assemble(video_dir(args.folder))


if __name__ == "__main__":
    main()
