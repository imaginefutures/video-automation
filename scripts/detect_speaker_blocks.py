"""Speaker-departure blocks (PLAN.md 4.6a): off-camera direction, PD notes, banter.

The primary speaker is whoever has the most words. Runs of words from anyone else are
merged into blocks (short interjections of the primary speaker inside a run are absorbed).
Each block becomes ONE review item ("카메라 밖 대화 141초 - 전체 삭제 제안") instead of
dozens of word-level candidates - this is what keeps the review queue short.

Diarization labels are not reliable across a long take (the same person can get a
different label in a different section), so a block is never applied automatically. With
an API key, one LLM call per block labels each line as off-camera DIRECTION, a presenter
ATTEMPT that was redone, or the presenter's FINAL take - the UI proposes deleting the
first two and keeping the last. Without a key, every line in the block is proposed for
deletion and the user decides in the expanded view.

Model: claude-sonnet-5 (PLAN.md 12장 모델 선택) - deciding which of several attempts is the
FINAL take is the same order of semantic judgment as NG case A/B, not a simple lexical
label, so this stays at the standard tier rather than dropping to Haiku.

Writes <folder>/edit/speaker_blocks.json.

Usage:
    python scripts/detect_speaker_blocks.py <videos/NAME> [--no-llm]
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from common import load_env, video_dir, edit_dir, load_transcript, words_only, write_json

MIN_LINES = 3            # a block is a back-and-forth: at least 3 lines, 2 speaker switches
MAX_LINE_WORDS = 25      # a line longer than this is monologue, not dialogue
MAX_LINE_GAP_SEC = 6.0   # lines further apart than this are not one exchange
MERGE_BLOCKS_SEC = 10.0  # exchanges this close together are one block


class LineLabel(BaseModel):
    line_id: int
    role: Literal["DIRECTION", "ATTEMPT", "FINAL", "CONTENT"]


class BlockLabels(BaseModel):
    lines: list[LineLabel]


SYSTEM = """\
너는 한국어 강의 영상의 편집자다. 아래는 화자가 2명 이상 번갈아 말하는 구간이다. 보통 카메라 밖의
PD/코치가 지시를 주고, 출연자가 같은 문장을 여러 번 다시 말하는 촬영 현장의 대화다.
화자 이름(화자A/화자B)은 임의 라벨이고 누가 출연자인지는 내용으로 판단하라.
각 줄을 다음 중 하나로 분류하라.

DIRECTION: 카메라 밖 지시·잡담·촬영 관련 말 ("여기를 봐봐", "다시 갈까요", 발음 논의). 삭제 대상.
ATTEMPT: 출연자가 말했지만 뒤에 같은 내용을 다시 말해서 버려질 시도. 삭제 대상.
FINAL: 같은 내용의 마지막 시도. 방송에 나갈 문장. 유지.
CONTENT: 재시도와 무관한 정상 강의 내용. 유지.

"같은 내용을 다시 말한" 여러 줄 중에서는 시간상 마지막 것만 FINAL이다. 단, 블록 이후에 이미 유지되는
부분이 같은 문장을 완성해서 말하고 있으면, 블록 안의 시도는 전부 ATTEMPT다. 모든 line_id에 답하라.
"""


def find_blocks(words: list[dict]) -> tuple[str, list[dict]]:
    """Blocks are DIALOGUE-shaped regions: short lines alternating between speakers.

    Diarization labels drift over a long take (the presenter was speaker_1 for the first
    three minutes of BS145 and speaker_0 afterwards), so "the minority speaker is the
    coach" is wrong. What is stable is the SHAPE of off-camera direction: rapid
    back-and-forth of short lines. A monologue - however it is labeled - has no switches.
    """
    counts: dict[str, int] = {}
    for w in words:
        counts[w.get("speaker_id", "?")] = counts.get(w.get("speaker_id", "?"), 0) + 1
    primary = max(counts, key=counts.get)

    lines = split_lines(words)
    for ln in lines:
        ln["n_words"] = ln["wi_end"] - ln["wi_start"] + 1

    regions: list[list[dict]] = []
    cur: list[dict] = []
    for ln in lines:
        fits = ln["n_words"] <= MAX_LINE_WORDS
        continues = bool(cur) and fits and (ln["start"] - cur[-1]["end"] <= MAX_LINE_GAP_SEC)
        if continues:
            cur.append(ln)
        else:
            span = _dialogue_span(cur)
            if span:
                regions.append(span)
            cur = [ln] if fits else []
    span = _dialogue_span(cur)
    if span:
        regions.append(span)

    merged: list[list[dict]] = []
    for r in regions:
        if merged and r[0]["start"] - merged[-1][-1]["end"] <= MERGE_BLOCKS_SEC:
            merged[-1].extend(r)
        else:
            merged.append(r)

    blocks = []
    for r in merged:
        seg_lines = [{**ln, "id": i} for i, ln in enumerate(r)]
        blocks.append({"id": len(blocks), "wi_start": r[0]["wi_start"], "wi_end": r[-1]["wi_end"],
                       "start": r[0]["start"], "end": r[-1]["end"],
                       "duration": round(r[-1]["end"] - r[0]["start"], 3),
                       "n_words": sum(ln["n_words"] for ln in r),
                       "speakers": sorted({ln["speaker"] for ln in r}),
                       "lines": seg_lines})
    return primary, blocks


def _dialogue_span(lines: list[dict]) -> list[dict] | None:
    """The exchange proper: from the line just before the first speaker switch to the line
    just after the last one. A monologue that merely precedes the exchange (same speaker,
    short lines) must not be swept in - the run of short lines is only the search window."""
    switch_idx = [i for i, (a, b) in enumerate(zip(lines, lines[1:])) if a["speaker"] != b["speaker"]]
    if len(switch_idx) < MIN_LINES - 1:
        return None
    span = lines[switch_idx[0]: switch_idx[-1] + 2]
    density = len(switch_idx) / max(1, len(span) - 1)
    if density < 0.4:  # label drift inside a monologue: rare flips, not a conversation
        return None
    return span


def split_lines(seg: list[dict]) -> list[dict]:
    """Group consecutive same-speaker words into lines (the unit the UI shows and the LLM labels)."""
    lines: list[dict] = []
    for w in seg:
        if lines and lines[-1]["speaker"] == w.get("speaker_id") and w["start"] - lines[-1]["end"] < 1.5:
            lines[-1]["wi_end"] = w["wi"]
            lines[-1]["end"] = round(w["end"], 3)
            lines[-1]["text"] += " " + w["text"]
        else:
            lines.append({"id": len(lines), "speaker": w.get("speaker_id"), "wi_start": w["wi"], "wi_end": w["wi"],
                          "start": round(w["start"], 3), "end": round(w["end"], 3), "text": w["text"]})
    return lines


def label_with_llm(primary: str, block: dict, after_lines: list[dict]) -> None:
    """`after_lines`: the lines right after the block, which stay in the cut. The real final
    take is often a long monologue line that falls OUTSIDE the block (too long to be
    "dialogue"); without seeing it the model promotes the last in-block attempt to FINAL."""
    import anthropic
    client = anthropic.Anthropic()
    names = {spk: f"화자{chr(65 + i)}" for i, spk in enumerate(block["speakers"])}
    body = "\n".join(f"[line {ln['id']}] ({names[ln['speaker']]}) {ln['text']}" for ln in block["lines"])
    if after_lines:
        body += "\n\n[블록 이후 — 이미 유지되는 부분, 분류 대상 아님]\n" + "\n".join(
            f"({names.get(ln['speaker'], '화자?')}) {ln['text']}" for ln in after_lines)
    resp = client.messages.parse(model="claude-sonnet-5", max_tokens=4000, system=SYSTEM,
                                 messages=[{"role": "user", "content": body}], output_format=BlockLabels,
                                 thinking={"type": "disabled"})
    roles = {l.line_id: l.role for l in resp.parsed_output.lines}
    for ln in block["lines"]:
        ln["role"] = roles.get(ln["id"], "DIRECTION")
        ln["proposed"] = "delete" if ln["role"] in ("DIRECTION", "ATTEMPT") else "keep"


def detect(folder: Path, use_llm: bool = True) -> Path:
    words = words_only(load_transcript(folder))
    primary, blocks = find_blocks(words)
    print(f"primary speaker: {primary}; blocks: {len(blocks)}, "
          f"{sum(b['duration'] for b in blocks):.1f}s total")

    labeled = False
    if use_llm and blocks:
        load_env()
        if os.environ.get("ANTHROPIC_API_KEY"):
            all_lines = split_lines(words)
            for b in blocks:
                after = [ln for ln in all_lines if ln["start"] > b["end"]][:2]
                label_with_llm(primary, b, after)
            labeled = True
        else:
            print("ANTHROPIC_API_KEY not set - proposing whole-block deletion without line roles")
    if not labeled:
        for b in blocks:
            for ln in b["lines"]:
                ln["role"] = None
                ln["proposed"] = "delete"  # whole exchange proposed; the user keeps lines in the expanded view

    for b in blocks:
        b["proposed_delete_sec"] = round(sum(ln["end"] - ln["start"] for ln in b["lines"] if ln["proposed"] == "delete"), 3)
        b["preview"] = " ".join(ln["text"] for ln in b["lines"])[:80]
        print(f"  block {b['id']}: {b['start']:.1f}-{b['end']:.1f}s, {len(b['lines'])} lines, "
              f"delete {b['proposed_delete_sec']:.1f}s :: {b['preview'][:50]}")

    out = edit_dir(folder) / "speaker_blocks.json"
    write_json(out, {"primary_speaker": primary, "llm_labeled": labeled, "blocks": blocks})
    print(f"wrote {out}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--no-llm", action="store_true")
    args = ap.parse_args()
    detect(video_dir(args.folder), use_llm=not args.no_llm)


if __name__ == "__main__":
    main()
