"""Self-evaluation against real gold data (2026-09-29: "이미 정답지가 있는 파일이잖아" - use the
human-edited finished video as ground truth instead of waiting on a synthetic mutation-based
eval harness). Diffs the raw transcript against the finished/edited video's transcript
(difflib, same technique detect_ng_candidates.py's alignment mode uses) to get the real,
human-decided cut/keep label for every raw word, then compares the automated pipeline's
final_cuts.json against it.

The critical number is **오삭제** (false positive): a raw word the human KEPT in the finished
video that the automated pipeline cut anyway. A flagged false positive would have been caught
in review; an UNFLAGGED one is the "경고 없는 복원" failure the whole redesign exists to avoid
(docs/기획/06-검증과-측정.md 4장) - so this script reports those two cases separately, not just
one aggregate precision number.

Two follow-up analyses (2026-09-29, "정확성을 더 높일 수 있는 아이디어" 1번·2번), both reusing
this same gold pair rather than needing new data:

  1. FN triage (--classify-fn): a raw-vs-finished word diff also counts every paraphrase or
     unrelated content trim the human made as a "missed NG" - which understates how the NG
     pipeline is actually doing. Sends each FN span (plus its aligned position in the finished
     video) to an LLM to label it "missed_ng" (a real restart/mistake/filler the pipeline
     should have caught) vs "editorial_other" (a rewrite/paraphrase/content trim unrelated to
     self-repair), and reports an adjusted recall using only the former.
  2. Judge validity (--seams): cross-tabulates seam_refine.py's own signals (audio boundary
     uncertainty, content-judge verdicts) against which cuts actually turned out to be real
     false positives here - i.e. does a "restore" flag's REASON actually predict trouble, or
     is it just noise research would show hurts precision without helping safety. No new
     model calls, pure bookkeeping over files that already exist.

Requires a gold pair: <gold_raw_transcript.json>, <gold_finished_transcript.json>, whose word
sequence must match videos/<NAME>/edit/transcript.json 1:1 (same source recording, same ASR
run) - verified at the top before comparing indices.

Usage:
    python scripts/eval_against_gold.py <videos/NAME> \
        --gold-raw <Reference/.../BS145_raw.json> --gold-finished <Reference/.../BS145.json> \
        [--classify-fn] [--seams edit/seams.json]
"""
from __future__ import annotations
import argparse
import difflib
import json
from collections import Counter
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel

from common import load_env, video_dir, edit_dir, load_transcript, words_only, write_json, norm

FN_JUDGE_MODEL = "claude-sonnet-5"
FN_JUDGE_BATCH = 20


def _char_map(words: list[dict]) -> tuple[str, list[int]]:
    """Concatenate every word's normalized text with no separator, plus a parallel array
    mapping each character position back to its source word index - the shared building block
    for character-level alignment (see diff_opcodes/gold_deleted_mask docstrings)."""
    chars: list[str] = []
    char_to_word: list[int] = []
    for wi, w in enumerate(words):
        t = norm(w["text"])
        chars.append(t)
        char_to_word.extend([wi] * len(t))
    return "".join(chars), char_to_word


def diff_opcodes(raw_words: list[dict], finished_words: list[dict]):
    """Word-range opcodes (i1,i2,j1,j2 in word indices - what finished_context_for's callers
    expect), computed via character-level alignment internally: raw and finished come from two
    INDEPENDENT Scribe runs on the same spoken audio, and Korean word-segmentation for compound
    words/numerals isn't stable across runs ("하루 종일" vs "하루종일", "일 년" vs "1년") - a
    plain word-token diff treats every such case as a phantom edit. Loose word-boundary mapping
    here is fine (this feeds only the human-readable "what the finished video says nearby"
    context in classify_fn_spans) - the scoring-critical mask is gold_deleted_mask, which does
    its own precise per-word majority vote instead of trusting these boundaries."""
    raw_chars, raw_c2w = _char_map(raw_words)
    fin_chars, fin_c2w = _char_map(finished_words)
    char_opcodes = difflib.SequenceMatcher(None, raw_chars, fin_chars, autojunk=False).get_opcodes()
    word_opcodes = []
    for tag, ci1, ci2, cj1, cj2 in char_opcodes:
        i1 = raw_c2w[ci1] if ci1 < len(raw_c2w) else len(raw_words)
        i2 = (raw_c2w[ci2 - 1] + 1) if ci2 > ci1 else i1
        j1 = fin_c2w[cj1] if cj1 < len(fin_c2w) else len(finished_words)
        j2 = (fin_c2w[cj2 - 1] + 1) if cj2 > cj1 else j1
        word_opcodes.append((tag, i1, i2, j1, j2))
    return word_opcodes


def gold_deleted_mask(raw_words: list[dict], finished_words: list[dict]) -> list[bool]:
    """Character-level alignment (see diff_opcodes), then each raw word counts as gold-deleted
    only if a MAJORITY of its own characters fall in a delete/replace range - resolves the
    ambiguity of a diff boundary landing mid-word (exactly the segmentation-mismatch case this
    exists to fix) by majority vote instead of the old any-character-in-range rule, which used
    to count purely cosmetic re-segmentation ("공감해 주고" vs "공감해주고") as a real deletion
    and inflate FN (2026-09-30, found analyzing BS167's gold FN: 24/210 missed-NG words were
    this, not real edits)."""
    raw_chars, raw_c2w = _char_map(raw_words)
    fin_chars, _ = _char_map(finished_words)
    sm = difflib.SequenceMatcher(None, raw_chars, fin_chars, autojunk=False)
    char_deleted = [False] * len(raw_chars)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("delete", "replace"):
            for i in range(i1, i2):
                char_deleted[i] = True

    total_chars = Counter(raw_c2w)
    deleted_chars = Counter(wi for wi, d in zip(raw_c2w, char_deleted) if d)
    mask = [False] * len(raw_words)
    for wi in range(len(raw_words)):
        total = total_chars.get(wi, 0)
        if total and deleted_chars.get(wi, 0) / total > 0.5:
            mask[wi] = True
    return _reorder_tolerant_recheck(raw_words, fin_chars, mask)


REORDER_RECHECK_MIN_CHARS = 20  # 2026-09-30: BS183에서 발견 - difflib.SequenceMatcher는 순서
# 보존 가정이라, 완성본이 원본 앞부분을 "훅"으로 끌어와 앞에 다시 배치하는 식의 순서 재배열
# 편집을 "삭제"로 오판한다(실제로는 옮겨졌을 뿐, 완성본 어딘가에 그대로 있음). 위 선형 diff가
# "삭제"로 표시한 연속 구간마다, 그 구간의 정규화된 텍스트가 완성본 전체(위치 무관)에 그대로
# 있는지 한 번 더 확인해 있으면 삭제 판정을 취소한다. 20자(대략 5~7단어) 미만은 우연히 겹칠
# 흔한 짧은 구절일 위험이 커서 재검사 대상에서 제외한다.

def _reorder_tolerant_recheck(raw_words: list[dict], fin_chars: str, mask: list[bool]) -> list[bool]:
    mask = list(mask)
    n = len(mask)
    i = 0
    while i < n:
        if not mask[i]:
            i += 1
            continue
        j = i
        while j < n and mask[j]:
            j += 1
        run_text = "".join(norm(w["text"]) for w in raw_words[i:j])
        if len(run_text) >= REORDER_RECHECK_MIN_CHARS and run_text in fin_chars:
            for k in range(i, j):
                mask[k] = False
        i = j
    return mask


def finished_context_for(opcodes, raw_i: int, fin_words: list[dict], pad: int = 10) -> str:
    """The finished-video text aligned to raw word index raw_i, ± pad words - used to show the
    judge what the human actually kept/wrote at this point in the story, not just that
    something here was different."""
    anchor = None
    for tag, i1, i2, j1, j2 in opcodes:
        if i1 <= raw_i < i2:
            anchor = j1 + (raw_i - i1) if tag == "equal" else j1
            break
    if anchor is None:
        anchor = len(fin_words)
    lo, hi = max(0, anchor - pad), min(len(fin_words), anchor + pad)
    return " ".join(w["text"] for w in fin_words[lo:hi])


def automated_cut_mask(n_words: int, final_cuts: list[dict]) -> tuple[list[bool], list[bool]]:
    """Returns (cut_mask, flagged_mask) - flagged_mask[i] is only meaningful where cut_mask[i]."""
    cut = [False] * n_words
    flagged = [False] * n_words
    for c in final_cuts:
        for i in range(c["wi_start"], min(c["wi_end"], n_words)):
            cut[i] = True
            if c.get("flag"):
                flagged[i] = True
    return cut, flagged


def spans(mask: list[bool], words: list[dict]) -> list[dict]:
    spans_out = []
    i = 0
    n = len(mask)
    while i < n:
        if not mask[i]:
            i += 1
            continue
        j = i
        while j < n and mask[j]:
            j += 1
        spans_out.append({"wi_start": i, "wi_end": j, "start": words[i]["start"], "end": words[j - 1]["end"],
                          "text": " ".join(words[k]["text"] for k in range(i, j))})
        i = j
    return spans_out


# --------------------------------------------------------------------------------- 1. FN triage

class FNVerdict(BaseModel):
    fn_id: int
    kind: Literal["missed_ng", "editorial_other"]
    ng_case_guess: Optional[Literal["A", "B", "C", "D", "E", "F", "OTHER"]] = None
    reason: str


class FNVerdicts(BaseModel):
    verdicts: list[FNVerdict]


FN_JUDGE_SYSTEM = """\
너는 한국어 강의 영상의 편집 QA 담당자다. 아래는 자동 컷편집 파이프라인이 "놓친" 구간 후보들이다 -
원본에는 있지만 자동으로는 안 잘렸는데, 사람이 만든 완성본에는 이 자리에 다른 말이 있거나 아예 없다.

각 항목이 다음 중 무엇인지 분류하라.
- missed_ng: 재시작·말실수·군더더기 반복처럼, 이 프로젝트의 NG 판별기가 원래 잡았어야 할 진짜 편집 대상.
  케이스(A~F, 정의는 아래)를 추정해서 함께 답하라.
- editorial_other: NG가 아니라 사람이 표현을 바꿨거나(패러프레이즈), 내용 자체를 편집상 이유로
  들어냈거나, 말투를 다듬은 것. 재시작이나 실수가 아니다.

케이스 정의: A=실수→정정, B=같은 내용을 다시 말함, C=강조 반복, D=교육적 재진술/나열,
E=조사·어미만 바뀐 형태론적 수정, F=미완성 후 방향 전환, OTHER=그 외.

각 항목: fn_id, kind, (missed_ng면) ng_case_guess, reason(한국어 한 문장). 모든 fn_id에 답하라.
"""


def build_fn_prompt(items: list[dict]) -> str:
    blocks = []
    for it in items:
        blocks.append(f"[fn {it['fn_id']}] ({it['start']:.0f}s)\n"
                       f"원본 앞: …{it['before']}\n"
                       f"원본에서 사라진 부분: {it['text']}\n"
                       f"원본 뒤: {it['after']}…\n"
                       f"완성본에서 이 위치: …{it['finished_context']}…")
    return "\n\n".join(blocks)


def classify_fn_spans(fn_spans: list[dict], words: list[dict], opcodes, gold_fin: list[dict]) -> dict[int, FNVerdict]:
    import anthropic
    client = anthropic.Anthropic()
    items = []
    for i, s in enumerate(fn_spans):
        before = " ".join(w["text"] for w in words[max(0, s["wi_start"] - 10):s["wi_start"]])
        after = " ".join(w["text"] for w in words[s["wi_end"]:s["wi_end"] + 10])
        items.append({"fn_id": i, "start": s["start"], "text": s["text"], "before": before, "after": after,
                      "finished_context": finished_context_for(opcodes, s["wi_start"], gold_fin)})

    out: dict[int, FNVerdict] = {}
    for k in range(0, len(items), FN_JUDGE_BATCH):
        part = items[k:k + FN_JUDGE_BATCH]
        resp = client.messages.parse(model=FN_JUDGE_MODEL, max_tokens=6000, system=FN_JUDGE_SYSTEM,
                                     messages=[{"role": "user", "content": build_fn_prompt(part)}],
                                     output_format=FNVerdicts, thinking={"type": "disabled"})
        for v in resp.parsed_output.verdicts:
            out[v.fn_id] = v
    return out


# --------------------------------------------------------------------------------- 2. judge validity

def judge_validity(folder: Path, fp_mask: list[bool]) -> dict | None:
    seams_path = edit_dir(folder) / "seams.json"
    if not seams_path.exists():
        return None
    seams = json.loads(seams_path.read_text())["seams"]

    def overlaps_fp(wi_start: int, wi_end: int) -> bool:
        return any(fp_mask[i] for i in range(wi_start, min(wi_end, len(fp_mask))))

    rows = []
    for s in seams:
        b = s["boundary"]
        j = s.get("judgment") or {}
        # reconstruct the word range this seam covers from its text length isn't reliable;
        # seams.json doesn't carry wi_start/wi_end directly on the top record, but final_cuts
        # does via cut_id - load that mapping instead
        rows.append({
            "cut_id": s["cut_id"],
            "audio_uncertain": b.get("audio_ok") is False,
            "judge_content_problem": bool(j) and (not j.get("grammar_ok", True) or j.get("duplicate_left")
                                                   or j.get("reference_broken") or j.get("info_lost", "none") != "none"),
            "flag": s.get("flag"),
        })

    final_cuts = {c["cut_id"]: c for c in json.loads((edit_dir(folder) / "final_cuts.json").read_text())["cuts"]}
    for r in rows:
        c = final_cuts.get(r["cut_id"])
        r["was_real_fp"] = overlaps_fp(c["wi_start"], c["wi_end"]) if c else False

    def rate(key: str) -> tuple[int, int, float]:
        flagged = [r for r in rows if r[key]]
        fp_among = sum(1 for r in flagged if r["was_real_fp"])
        return len(flagged), fp_among, (fp_among / len(flagged) if flagged else float("nan"))

    audio_n, audio_fp, audio_rate = rate("audio_uncertain")
    judge_n, judge_fp, judge_rate = rate("judge_content_problem")
    neither = [r for r in rows if not r["audio_uncertain"] and not r["judge_content_problem"]]
    neither_fp = sum(1 for r in neither if r["was_real_fp"])

    print(f"\n=== 이음새 판정 타당성 (기존 seams.json/final_cuts.json만 사용, 새 호출 없음) ===")
    print(f"경계 불확실(audio_ok=False)로 flag된 {audio_n}건 중 실제 오삭제와 겹침: {audio_fp}건 ({audio_rate:.0%})")
    print(f"내용 판정(judge)으로 flag된 {judge_n}건 중 실제 오삭제와 겹침: {judge_fp}건 ({judge_rate:.0%})")
    print(f"둘 다 문제없다고 본 {len(neither)}건 중 실제 오삭제와 겹침: {neither_fp}건 "
          f"({neither_fp/len(neither):.0%})" if neither else "(해당 없음)")
    print("(비율이 높을수록 그 신호가 실제 위험을 잘 짚는다는 뜻. 'flag 없음'인데도 오삭제와 겹치는 게 있으면 안전망에 구멍이 있다는 뜻)")

    return {"audio_flagged": audio_n, "audio_flagged_real_fp": audio_fp,
           "judge_flagged": judge_n, "judge_flagged_real_fp": judge_fp,
           "neither_flagged": len(neither), "neither_flagged_real_fp": neither_fp}


# --------------------------------------------------------------------------------- main

def evaluate(folder: Path, gold_raw_path: Path, gold_finished_path: Path,
             do_classify_fn: bool = False) -> Path:
    words = words_only(load_transcript(folder))
    gold_raw = words_only(json.loads(gold_raw_path.read_text()))
    gold_fin = words_only(json.loads(gold_finished_path.read_text()))

    if len(words) != len(gold_raw) or any(w["text"] != g["text"] for w, g in zip(words[:50], gold_raw[:50])):
        raise SystemExit(f"word mismatch: {folder}/edit/transcript.json ({len(words)} words) vs "
                         f"{gold_raw_path} ({len(gold_raw)} words) - these must be the same source recording")

    opcodes = diff_opcodes(words, gold_fin)
    gold_cut = gold_deleted_mask(words, gold_fin)
    final_path = edit_dir(folder) / "final_cuts.json"
    final_cuts = json.loads(final_path.read_text())["cuts"] if final_path.exists() else []
    auto_cut, auto_flagged = automated_cut_mask(len(words), final_cuts)

    n = len(words)
    tp = sum(1 for i in range(n) if gold_cut[i] and auto_cut[i])
    fp = sum(1 for i in range(n) if not gold_cut[i] and auto_cut[i])
    fn = sum(1 for i in range(n) if gold_cut[i] and not auto_cut[i])
    tn = n - tp - fp - fn
    fp_unflagged = sum(1 for i in range(n) if not gold_cut[i] and auto_cut[i] and not auto_flagged[i])
    fp_flagged = fp - fp_unflagged

    precision = tp / (tp + fp) if (tp + fp) else float("nan")
    recall = tp / (tp + fn) if (tp + fn) else float("nan")

    gold_cut_spans = spans(gold_cut, words)
    auto_cut_spans = spans(auto_cut, words)
    fp_mask = [not gold_cut[i] and auto_cut[i] for i in range(n)]
    fp_spans = spans(fp_mask, words)
    fp_unflagged_mask = [not gold_cut[i] and auto_cut[i] and not auto_flagged[i] for i in range(n)]
    fp_unflagged_spans = spans(fp_unflagged_mask, words)
    fn_mask = [gold_cut[i] and not auto_cut[i] for i in range(n)]
    fn_spans = spans(fn_mask, words)

    gold_cut_sec = sum(s["end"] - s["start"] for s in gold_cut_spans)
    auto_cut_sec = sum(s["end"] - s["start"] for s in auto_cut_spans)

    print(f"=== gold comparison: {folder.name} ===")
    print(f"raw words: {n}")
    print(f"gold (사람 편집본 대비 삭제): {len(gold_cut_spans)}개 구간, {gold_cut_sec:.1f}s")
    print(f"automated (품질 루프 결과, flag 무관 전부 적용 가정): {len(auto_cut_spans)}개 구간, {auto_cut_sec:.1f}s")
    print()
    print(f"단어 단위: TP={tp} FP={fp} FN={fn} TN={tn}")
    print(f"precision (자른 것 중 실제로도 잘렸어야 함): {precision:.3f}")
    print(f"recall    (실제로 잘린 것 중 자동으로 잡은 비율): {recall:.3f}")
    print()
    print(f"오삭제(사람은 남겼는데 자동이 자름) - flag로 검토 큐에 뜸: {fp_flagged}단어, {len(fp_spans) - len(fp_unflagged_spans)}구간")
    print(f"오삭제 중 **flag 없이 조용히 잘림** (경고 없는 복원 위험): {fp_unflagged} 단어, {len(fp_unflagged_spans)}구간")
    if fp_unflagged_spans:
        print("  ⚠ 확인 필요:")
        for s in fp_unflagged_spans:
            print(f"    [{s['start']:.1f}s] {s['text']}")
    print()
    print(f"놓친 것(사람은 잘랐는데 자동은 안 잘림, FN): {fn} 단어, {len(fn_spans)}구간")
    for s in fn_spans[:10]:
        print(f"    [{s['start']:.1f}s] {s['text'][:60]}")

    result = {
        "video": folder.name, "n_words": n,
        "gold_cut_spans": len(gold_cut_spans), "gold_cut_sec": round(gold_cut_sec, 1),
        "automated_cut_spans": len(auto_cut_spans), "automated_cut_sec": round(auto_cut_sec, 1),
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": round(precision, 4) if precision == precision else None,
        "recall": round(recall, 4) if recall == recall else None,
        "fp_flagged_words": fp_flagged, "fp_unflagged_words": fp_unflagged,
        "fp_unflagged_spans": fp_unflagged_spans,
        "fn_spans": fn_spans,
    }

    if do_classify_fn and fn_spans:
        load_env()
        print(f"\n=== FN 정제: {len(fn_spans)}건을 진짜 NG인지 편집상 변경인지 분류 ({FN_JUDGE_MODEL}) ===")
        verdicts = classify_fn_spans(fn_spans, words, opcodes, gold_fin)
        missed_ng = [i for i, v in verdicts.items() if v.kind == "missed_ng"]
        editorial = [i for i, v in verdicts.items() if v.kind == "editorial_other"]
        print(f"missed_ng (진짜 놓친 NG): {len(missed_ng)}건")
        for i in missed_ng:
            v = verdicts[i]
            print(f"    [{fn_spans[i]['start']:.1f}s] case={v.ng_case_guess} :: {v.reason} — {fn_spans[i]['text'][:50]}")
        print(f"editorial_other (NG 아님, 표현/내용 편집): {len(editorial)}건")

        fn_words_missed = sum(fn_spans[i]["wi_end"] - fn_spans[i]["wi_start"] for i in missed_ng)
        adjusted_recall = tp / (tp + fn_words_missed) if (tp + fn_words_missed) else float("nan")
        print(f"\n조정된 재현율 (editorial_other 제외, 진짜 NG 기준): {adjusted_recall:.3f} "
              f"(기존 {recall:.3f}에서 분모 {fn}→{tp + fn_words_missed}단어)")

        result["fn_triage"] = {
            "missed_ng": len(missed_ng), "editorial_other": len(editorial),
            "adjusted_recall": round(adjusted_recall, 4) if adjusted_recall == adjusted_recall else None,
            "verdicts": [{"fn_id": i, **v.model_dump(), "span": fn_spans[i]} for i, v in verdicts.items()],
        }

    jv = judge_validity(folder, fp_mask)
    if jv:
        result["judge_validity"] = jv

    out = edit_dir(folder) / "gold_eval.json"
    write_json(out, result)
    print(f"\nwrote {out}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--gold-raw", type=Path, required=True)
    ap.add_argument("--gold-finished", type=Path, required=True)
    ap.add_argument("--classify-fn", action="store_true", help="LLM-audit each FN span: real missed NG vs editorial change")
    args = ap.parse_args()
    evaluate(video_dir(args.folder), args.gold_raw, args.gold_finished, do_classify_fn=args.classify_fn)


if __name__ == "__main__":
    main()
