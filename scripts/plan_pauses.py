"""Pause rhythm layer (PLAN.md 2.4 table, 3.2 step 2).

Every gap between consecutive words of at least SHOW_MIN gets a RECOMMENDED keep length:

    NORMAL_INTER          keep 0.25s   ordinary gap between sentences (prev word ends with . ! ? …)
    NORMAL_INTRA          keep 0.15s   ordinary gap inside a sentence (no sentence-ending punctuation)
    ENUMERATION           keep 0.11s   items in a list - tighter
    QUOTE_TO_EXPLANATION  keep 0.40s   quoting then explaining - more air
    TRANSITION            keep all     topic change - intentional breath
    QUESTION_TO_ANSWER    keep all     rhetorical question then answer
    SPEAKER_CHANGE        keep all     handled by the speaker-block layer, not here

NORMAL_INTER vs NORMAL_INTRA is decided structurally (sentence-ending punctuation on the
preceding word), not by the LLM - the LLM's NORMAL label just means "no special discourse
function", and gets resolved to one of the two afterward (see `resolve_style`). This way the
two keep lengths each get their own lever in the review UI, instead of one NORMAL target that
had to compromise between mid-sentence breaths and sentence-boundary pauses.

Gaps of LLM_MIN or longer are classified by one LLM call (with a few words of context on
each side); shorter ones default to NORMAL. Model: claude-haiku-4-5 (PLAN.md 12장 모델 선택) - this
is high-volume categorical labeling driven almost entirely by lexical discourse markers
("다시 말하면", "첫째", question marks), not the harder semantic judgment NG classification
needs, so the cheapest tier is the cost-effective choice here. A wrong label only changes
how much silence is trimmed, never what's said, so the downside of a miss is small (PLAN.md
2.4 "정상 발화는 절대 잘리지 않는다" doesn't even apply to pauses - there's no speech here to
protect). In the review UI each gap is a gauge the user can
drag (down to 0 = delete the pause entirely) and double-click to return to this
recommendation. Changing a global target in the UI moves every recommendation with it.

The trim never touches speech: it removes a window from inside the gap, leaving the kept
length split around it, plus PROTECT_SEC after the previous word and before the next (2.4
hard rule 4: 10-20ms boundary protection). Where that window sits is not a geometric half-split
any more (2026-10-08, 현재-설계/무음-리듬.md 재설계): with an audio map available, it's centered
on the gap's quietest instant instead of its midpoint, and it steps aside for a whole breath
rather than slicing through one - a breath that would otherwise land in the removed middle
gets fully kept, even if that means removing a bit less than the target (see `trim_for_keep`).

Writes <folder>/edit/pauses.json. Existing labels are reused for unchanged gaps, so
re-running does not re-pay for classification.

Usage:
    python scripts/plan_pauses.py <videos/NAME> [--no-llm]
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from common import load_env, video_dir, edit_dir, load_transcript, words_only, write_json, log_llm_usage
from audio_map import load_audio_map, true_onset, min_energy_in

SHOW_MIN = 0.12       # below this a gap is articulation, not a pause; Scribe jitter is 50-100ms
LLM_MIN = 0.35        # gaps this long get context-classified; shorter ones default to NORMAL
PROTECT_SEC = 0.02    # never cut within this of a word boundary
MIN_TRIM = 0.05       # don't bother removing less than this
LONG_GAP_FALLBACK = 1.5  # without an LLM, gaps this long are assumed intentional
SENTENCE_ENDERS = (".", "!", "?", "…")
TRAILING_WRAPPERS = "\"'”’)]}」』》"  # closing quotes/parens that can follow sentence punctuation

PRESETS = {
    "NORMAL_INTER":         {"target": 0.25, "trim": True},
    "NORMAL_INTRA":         {"target": 0.15, "trim": True},
    "ENUMERATION":          {"target": 0.11, "trim": True},
    "QUOTE_TO_EXPLANATION": {"target": 0.40, "trim": True},
    "TRANSITION":           {"target": None, "trim": False},
    "QUESTION_TO_ANSWER":   {"target": None, "trim": False},
    "SPEAKER_CHANGE":       {"target": None, "trim": False},
}

Style = Literal["NORMAL", "ENUMERATION", "QUOTE_TO_EXPLANATION", "TRANSITION", "QUESTION_TO_ANSWER"]


def ends_sentence(text: str) -> bool:
    return text.rstrip(TRAILING_WRAPPERS).endswith(SENTENCE_ENDERS)


def resolve_style(style: str, gap: dict) -> str:
    """Split the LLM's/fallback's plain NORMAL into NORMAL_INTER/NORMAL_INTRA by sentence
    boundary. Already-split styles (reused from a prior run's pauses.json) pass through."""
    if style != "NORMAL":
        return style
    return "NORMAL_INTER" if gap["sentence_boundary"] else "NORMAL_INTRA"


class GapLabel(BaseModel):
    gap_id: int
    style: Style


class GapLabels(BaseModel):
    labels: list[GapLabel]


SYSTEM = """\
너는 한국어 강의 영상의 편집자다. 문장과 문장 사이의 쉼(무음)을 문맥에 따라 분류한다.
각 쉼에 대해 앞 문맥과 뒤 문맥이 주어진다. 다음 중 하나로 분류하라.

NORMAL: 일반적인 문장 사이. 특별한 의도 없는 쉼.
ENUMERATION: 나열 중 ("첫째... 둘째...", "A, B, C"). 항목 사이의 쉼.
QUOTE_TO_EXPLANATION: 인용·개념 제시 후 설명으로 넘어가는 지점 ("~라고 합니다. (쉼) 이게 무슨 뜻이냐면").
TRANSITION: 주제가 바뀌는 지점. 새 섹션·새 화제의 시작. 의도적 호흡.
QUESTION_TO_ANSWER: 청중에게 질문을 던지고 답하기 전의 쉼 ("왜 그럴까요? (쉼) 이유는").

판단이 애매하면 NORMAL. 모든 gap_id에 대해 정확히 하나씩 답하라.
"""


def usable_range(gap_start: float, gap_end: float) -> tuple[float, float]:
    return gap_start + PROTECT_SEC, gap_end - PROTECT_SEC


def recommended_keep(gap: dict, targets: dict[str, float | None]) -> float:
    """Seconds of silence to keep for this gap under the given per-style targets."""
    us, ue = usable_range(gap["gap_start"], gap["gap_end"])
    usable = max(0.0, ue - us)
    target = targets.get(gap["style"])
    if target is None or usable - target < MIN_TRIM:
        return round(usable, 3)
    return round(target, 3)


def removal_window(us: float, ue: float, rm: float, amap: dict | None) -> tuple[float, float]:
    """Where in [us, ue] to place the `rm`-second span to remove. Without an audio map this
    is just the geometric center (old behavior). With one: a breath anywhere in [us, ue] is
    never sliced - the window is confined to whichever side of the breath has room for it
    (preferring the side that already fits `rm`), and within whatever range it's confined to,
    it's centered on the quietest point rather than that range's midpoint, so the actual cut
    edges land on silence instead of wherever the math happens to fall."""
    if rm <= 0:
        return us, us
    if not amap:
        mid = (us + ue) / 2
        return mid - rm / 2, mid + rm / 2

    lo, hi = us, ue
    breath = next((b for b in amap.get("breaths", []) if b["start"] < ue and b["end"] > us), None)
    if breath:
        before, after = max(0.0, breath["start"] - us), max(0.0, ue - breath["end"])
        if after >= rm and after >= before:
            lo, hi = breath["end"], ue
        elif before > 0:
            lo, hi = us, breath["start"]
        # else: breath leaves no room on either side - fall through using the full [us, ue]
        # and accept that the removed window may end up shorter than `rm` once clamped below.

    center, _ = min_energy_in(amap, lo, hi)
    start, end = center - rm / 2, center + rm / 2
    if start < lo:
        start, end = lo, lo + rm
    if end > hi:
        start, end = hi - rm, hi
    return max(us, start), min(ue, end)


def trim_for_keep(gap: dict, keep_sec: float, amap: dict | None = None) -> dict | None:
    """The span to remove so that about `keep_sec` of the gap remains (None = nothing
    removed). `amap` is optional so this still works pre-audio_map.py (e.g. tests, or a
    video processed before it existed) - it just falls back to the old symmetric split."""
    us, ue = usable_range(gap["gap_start"], gap["gap_end"])
    usable = ue - us
    if usable <= 0 or keep_sec >= usable - 0.01:
        return None
    start, end = removal_window(us, ue, usable - max(0.0, keep_sec), amap)
    if end - start < 0.01:
        return None
    return {"start": round(start, 3), "end": round(end, 3)}


def build_gaps(words: list[dict], amap: dict | None = None) -> list[dict]:
    gaps = []
    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        raw_dur = b["start"] - a["end"]
        if raw_dur < SHOW_MIN:
            continue
        # Only correct the boundary of a gap that already qualifies as a real pause - running
        # true_onset() against every consecutive word pair (including ordinary mid-sentence
        # micro-gaps) reads continuous speech's own energy as "already started" almost
        # everywhere, the same 83%-false-positive failure mode docs/결정-이력.md 09-29 already
        # found with a flat dB threshold.
        # Clamp at a["end"]: true_onset() only knows the reported_t it's walking back from, not
        # this gap's start, so when no quiet point exists before max_pull_sec it (or even
        # ordinary continuous-speech energy right up to a["end"]) can walk past the previous
        # word's own boundary, producing a gap_end before gap_start (negative duration) - seen on
        # ~65% of real gaps in BS145/BS167 (2026-10-01 review). Floor it at a["end"] so duration
        # is never negative; those gaps just get duration 0 (no trim headroom) instead of nonsense.
        gap_end = max(a["end"], true_onset(amap, b["start"])) if amap else b["start"]
        dur = gap_end - a["end"]
        gaps.append({
            "id": len(gaps),
            "prev_wi": a["wi"], "next_wi": b["wi"],
            "gap_start": round(a["end"], 3), "gap_end": round(gap_end, 3),
            "duration": round(dur, 3),
            "speaker_change": a.get("speaker_id") != b.get("speaker_id"),
            "sentence_boundary": ends_sentence(a["text"]),
            "before": " ".join(w["text"] for w in words[max(0, i - 7):i + 1]),
            "after": " ".join(w["text"] for w in words[i + 1:i + 8]),
        })
    return gaps


def classify_with_llm(gaps: list[dict], folder: Path) -> dict[int, str]:
    import anthropic
    client = anthropic.Anthropic()
    labels: dict[int, str] = {}
    chunk = 120
    for k in range(0, len(gaps), chunk):
        part = gaps[k:k + chunk]
        lines = [f"[gap {g['id']}] ({g['duration']:.2f}s)\n  앞: …{g['before']}\n  뒤: {g['after']}…" for g in part]
        resp = client.messages.parse(
            model="claude-haiku-4-5-20251001", max_tokens=8000, system=SYSTEM,
            messages=[{"role": "user", "content": "\n\n".join(lines)}], output_format=GapLabels,
            thinking={"type": "disabled"})
        log_llm_usage(folder, "plan_pauses", "claude-haiku-4-5-20251001", resp.usage)
        for lab in resp.parsed_output.labels:
            labels[lab.gap_id] = lab.style
    return labels


def previous_labels(folder: Path) -> dict[tuple[int, int], str]:
    p = edit_dir(folder) / "pauses.json"
    if not p.exists():
        return {}
    old = json.loads(p.read_text())
    return {(g["prev_wi"], g["next_wi"]): g["style"] for g in old.get("gaps", []) if g.get("llm_labeled")}


def plan(folder: Path, use_llm: bool = True) -> Path:
    words = words_only(load_transcript(folder))
    amap = load_audio_map(folder)
    if not amap:
        print("no audio_map.json - pause trims will trust Scribe's word-start timestamps as-is "
              "(run audio_map.py first to correct for ASR onset lag)")
    gaps = build_gaps(words, amap)
    reuse = previous_labels(folder)

    labels: dict[int, str] = {}
    need = [g for g in gaps if not g["speaker_change"] and g["duration"] >= LLM_MIN]
    for g in need:
        key = (g["prev_wi"], g["next_wi"])
        if key in reuse:
            labels[g["id"]] = reuse[key]
    todo = [g for g in need if g["id"] not in labels]
    if use_llm and todo:
        load_env()
        if os.environ.get("ANTHROPIC_API_KEY"):
            print(f"classifying {len(todo)} gaps with claude-haiku-4-5 ({len(need) - len(todo)} reused)...")
            labels.update(classify_with_llm(todo, folder))
        else:
            print("ANTHROPIC_API_KEY not set - using conservative fallback labels")

    targets = {k: v["target"] for k, v in PRESETS.items()}
    for g in gaps:
        if g["speaker_change"]:
            style = "SPEAKER_CHANGE"
        elif g["id"] in labels:
            style = resolve_style(labels[g["id"]], g)
        elif g["duration"] >= LLM_MIN:
            style = "TRANSITION" if g["duration"] >= LONG_GAP_FALLBACK else resolve_style("NORMAL", g)
        else:
            style = resolve_style("NORMAL", g)
        g["style"] = style
        g["llm_labeled"] = g["id"] in labels
        g["rec_keep"] = recommended_keep(g, targets)
        g["trim"] = trim_for_keep(g, g["rec_keep"], amap)

    trimmed = [g for g in gaps if g["trim"]]
    removed = sum(g["trim"]["end"] - g["trim"]["start"] for g in trimmed)
    by_style: dict[str, int] = {}
    for g in gaps:
        by_style[g["style"]] = by_style.get(g["style"], 0) + 1
    print(f"gaps >= {SHOW_MIN}s: {len(gaps)}  " + ", ".join(f"{k}={v}" for k, v in sorted(by_style.items())))
    print(f"recommended trims: {len(trimmed)} gaps, {removed:.1f}s of silence removed")

    out = edit_dir(folder) / "pauses.json"
    write_json(out, {"presets": PRESETS, "show_min": SHOW_MIN, "llm_min": LLM_MIN,
                     "protect_sec": PROTECT_SEC, "gaps": gaps})
    print(f"wrote {out}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--no-llm", action="store_true")
    args = ap.parse_args()
    plan(video_dir(args.folder), use_llm=not args.no_llm)


if __name__ == "__main__":
    main()
