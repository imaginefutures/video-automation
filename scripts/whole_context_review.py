"""Whole-context review pass: one LLM call over the full transcript to catch what the local,
per-candidate passes structurally cannot -

  - DISTANT_RESTART: a restart of content said much earlier, far outside the local candidate
    detector's window (detect_ng_candidates.py compares a deleted run only against the next
    few words that follow it - a re-shoot minutes later never becomes a candidate at all, so
    it never even reaches the review queue; it just silently stays in the final cut)
  - OFF_TOPIC: off-camera direction/banter as a MONOLOGUE, not the back-and-forth dialogue
    shape detect_speaker_blocks.py requires (its _dialogue_span needs >=2 speaker switches -
    a single speaker talking to the crew with no reply has none)

Independent of and complementary to the local passes. This is a broad-recall net, not a
confirmed judgment, so findings always cut with a restore flag, never cleanly (최대 삭제
방침, docs/서비스-개요와-철학.md 원칙 2).

2026-09-29 recall improvement (against BS145 gold data - a distant restart of "셀리그만"
content was missed): the model has to notice a repeat buried in ~2500 words on its own, which
a single long-context pass can miss even when the text is technically present. Two cheap,
deterministic hints are now injected directly into the packed transcript instead of relying
on the model to find everything unaided:

  - "[참고: ... 와 단어 공유]" - a rare/salient word (proper noun, technical term - anything
    infrequent and >=3 chars) shared between two lines far apart gets both lines tagged with
    each other's location. Known limitation: this only catches REPEATED surface forms. A name
    the ASR transliterates differently each time it's said (BS145 has this - "Nathaniel" comes
    out as "나다님"/"나타니엘"/"나싸니엘"/"Nathaniel" across takes) won't share a token and
    won't be caught this way; that case still depends on the model noticing on its own.
  - "[음향 리셋]" - a line whose first word's F0 sits well above the speaker's median
    (prosody.py's own F0_RESET_RATIO). Tried as a standalone tag first and dropped: at
    BS145's word-level pitch variance, 24% of ALL words clear that ratio (46% of line-initial
    words) - a normal sentence starting a beat higher than a whole-video rolling median is
    just how speech prosody works, not a restart signal on its own. Rather than chasing a
    higher threshold number that happens to look better on this one video (exactly the
    overfitting risk to avoid), it's only surfaced as a SECONDARY tag on a line that ALREADY
    has a rare-token hint - two independent weak signals corroborating each other, which is a
    structural rule, not a video-specific number.

Neither hint is deterministic proof of anything - both are printed as hints in the prompt,
not filters, and the model is told explicitly that a hint is not a verdict. Deliberately NOT
implemented: splitting the transcript into sliding windows. That would lose exactly the
cross-window context distant-restart detection needs (a restart in window 3 of what was said
in window 1 requires window 3 to still see window 1) - it solves a token-length problem by
recreating the underlying recall problem, so hint-injection into one whole-transcript call was
chosen instead.

Model: claude-opus-5-5. One holistic long-context call per video where getting the read right
matters more than shaving cost - the absolute cost is negligible either way (~7k tokens per
video, well under $0.1).

Usage:
    python scripts/whole_context_review.py <videos/NAME>
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from common import load_env, video_dir, edit_dir, load_transcript, words_only, write_json, norm, thinking_kwargs
from detect_speaker_blocks import split_lines
from prosody import load_prosody, F0_RESET_RATIO

MODEL = "claude-opus-5-5"

RARE_FREQ_MAX = 5          # a token appearing at most this many times counts as "rare"
MIN_TOKEN_LEN = 3          # skip short function words/particles (Korean particles are usually 1-2 chars)
TOKEN_PREFIX_LEN = 3       # compare token prefixes, not full strings - survives a trailing particle
MIN_PAIR_GAP_WORDS = 300   # only hint pairs at least this far apart (closer repeats are the local pass's job)


class ContextFinding(BaseModel):
    wi_start: int
    wi_end: int  # exclusive
    kind: Literal["DISTANT_RESTART", "OFF_TOPIC"]
    reason: str
    confidence: float


class ContextReview(BaseModel):
    findings: list[ContextFinding]


SYSTEM = """\
너는 한국어 강의 영상의 편집자다. 아래는 영상 전체 트랜스크립트다(줄 단위, 단어 id(wi) 구간·시작초·화자 포함).
[이미 후보로 잡힘] 표시가 붙은 구간은 로컬 규칙(단어열 유사도 재시작 탐지, 대화 형태 화자 이탈 탐지)이
이미 찾았으니 다시 보고하지 마라.

전체 흐름을 보고 로컬 규칙이 구조적으로 놓치는 두 가지만 찾아라. 둘 다 드물다 - 없으면 findings를 빈 리스트로 반환하라.

DISTANT_RESTART: 훨씬 앞에서 이미 설명한 내용과 사실상 같은 내용(주장·수치·결론이 같음)을
  시간이 많이 지난 뒤 다시 설명한 구간. 문자열이 아니라 의미로 판단하라. 둘 중 앞의 시도가 삭제 후보.
OFF_TOPIC: 강의 내용과 무관한 구간 - 촬영 지시, 장비 점검, 혼잣말로 하는 준비 확인, 카메라 밖을 향한
  발언. 상대가 대답하지 않는 독백 형태로 나타나도 좋다(그래서 화자 이탈 탐지가 놓친다).

두 가지 참고 표시가 있다 - 둘 다 힌트일 뿐 정답이 아니다. 표시가 없어도 재시작은 있을 수 있고, 표시가
있어도 재시작이 아닐 수 있다(우연히 같은 단어를 다른 맥락에서 썼을 뿐일 수 있음). 최종 판단은 항상 의미로 하라.
  [참고: N-M와 단어 공유] - 이 줄과 멀리 떨어진 다른 줄이 드문 단어(고유명사 등)를 공유한다. 같은 내용의
    재진술인지 그쪽 구간과 비교해서 확인해봐라.
  [음향 리셋] - 이 줄에 피치가 화자 평소보다 확 튀어 오르는 단어가 있다. 문장을 새로 시작할 때 흔한
    신호다.

각 finding: 시작/끝 단어 id(wi_start, wi_end - 반열림 구간), 종류, 근거(한국어 한 문장), confidence(0-1).
확신 없으면 보고하지 마라 - 이 패스는 확정이 아니라 사람 검토 대상을 넓히는 안전망이다.
"""


# --------------------------------------------------------------------------------- hints

def salient_tokens(text: str) -> set[str]:
    out = set()
    for w in text.split():
        n = norm(w)
        if len(n) >= MIN_TOKEN_LEN:
            out.add(n[:TOKEN_PREFIX_LEN] if len(n) > TOKEN_PREFIX_LEN else n)
    return out


def rare_token_hints(lines: list[dict]) -> dict[int, list[tuple[int, int]]]:
    """line index -> [(other line's wi_start, other line's wi_end), ...] for lines far apart
    that share a rare token. Deterministic, no LLM - see module docstring for what this does
    and does not catch."""
    per_line_tokens = [salient_tokens(ln["text"]) for ln in lines]
    freq: Counter[str] = Counter()
    for toks in per_line_tokens:
        for t in toks:
            freq[t] += 1
    rare_per_line = [{t for t in toks if freq[t] <= RARE_FREQ_MAX} for toks in per_line_tokens]

    hints: dict[int, list[tuple[int, int]]] = {}
    for i in range(len(lines)):
        if not rare_per_line[i]:
            continue
        for j in range(i + 1, len(lines)):
            if lines[j]["wi_start"] - lines[i]["wi_end"] < MIN_PAIR_GAP_WORDS:
                continue
            if rare_per_line[i] & rare_per_line[j]:
                hints.setdefault(i, []).append((lines[j]["wi_start"], lines[j]["wi_end"]))
                hints.setdefault(j, []).append((lines[i]["wi_start"], lines[i]["wi_end"]))
    return hints


def prosody_reset_words(prosody: dict | None, words: list[dict]) -> set[int]:
    """Word indices whose F0 sits at/above F0_RESET_RATIO over their speaker's median - the
    same signal classify_candidates.py already uses per-candidate, reused here as a whole-
    transcript hint (prosody.py's own threshold, not a new one). prosody.json stores F0 per
    word index but not the speaker, so the speaker comes from the transcript's own words."""
    if not prosody:
        return set()
    pw = {p["wi"]: p["f0_hz"] for p in prosody["per_word"] if p["f0_hz"]}
    baseline = prosody["speaker_baseline"]
    out = set()
    for w in words:
        f0 = pw.get(w["wi"])
        base = baseline.get(w.get("speaker_id"), {}).get("median_f0")
        if f0 and base and f0 / base >= F0_RESET_RATIO:
            out.add(w["wi"])
    return out


def pack_transcript(words: list[dict], covered: set[int], prosody: dict | None) -> str:
    lines = split_lines(words)
    hints = rare_token_hints(lines)
    reset_wis = prosody_reset_words(prosody, words)

    out = []
    for i, ln in enumerate(lines):
        tags = []
        if any(wi in covered for wi in range(ln["wi_start"], ln["wi_end"] + 1)):
            tags.append("[이미 후보로 잡힘]")
        pair_hints = hints.get(i, [])[:2]  # cap to keep the prompt from ballooning on a hub line
        for (s, e) in pair_hints:
            tags.append(f"[참고: {s}-{e}와 단어 공유]")
        # 음향 리셋은 독립 신호로 쓰기엔 너무 잦다(모듈 docstring 참고) - rare-token 힌트가 이미
        # 있는 줄에서만 보강 신호로 덧붙인다
        if pair_hints and ln["wi_start"] in reset_wis:
            tags.append("[음향 리셋]")
        tag_str = (" " + " ".join(tags)) if tags else ""
        out.append(f"[{ln['wi_start']}-{ln['wi_end']}] ({ln['start']:.0f}s, {ln['speaker']}){tag_str} {ln['text']}")
    return "\n".join(out)


def covered_word_indices(ng_items: list[dict], blocks: list[dict]) -> set[int]:
    covered: set[int] = set()
    for it in ng_items:
        covered.update(range(it["raw_word_index_start"], it["raw_word_index_end"]))
    for b in blocks:
        covered.update(range(b["wi_start"], b["wi_end"] + 1))
    return covered


def review(folder: Path) -> Path:
    load_env()
    import anthropic

    words = words_only(load_transcript(folder))
    ng_path = edit_dir(folder) / "ng.json"
    ng_items = json.loads(ng_path.read_text()) if ng_path.exists() else []
    blocks_path = edit_dir(folder) / "speaker_blocks.json"
    blocks = json.loads(blocks_path.read_text())["blocks"] if blocks_path.exists() else []
    covered = covered_word_indices(ng_items, blocks)
    prosody = load_prosody(folder)

    packed = pack_transcript(words, covered, prosody)
    n_pair_hints = sum(1 for line in packed.split("\n") if "참고:" in line)
    print(f"whole-context review: {len(words)} words, {len(packed)} chars packed, model={MODEL} "
          f"({n_pair_hints} 줄에 희귀 단어 힌트{'(prosody 없어 음향 리셋 보강 없음)' if not prosody else ''})")

    client = anthropic.Anthropic()
    resp = client.messages.parse(model=MODEL, max_tokens=4000, system=SYSTEM,
                                 messages=[{"role": "user", "content": packed}],
                                 output_format=ContextReview, **thinking_kwargs(MODEL))
    findings = resp.parsed_output.findings
    print(f"raw findings: {len(findings)}")

    kept = [f for f in findings if not any(wi in covered for wi in range(f.wi_start, f.wi_end))]
    print(f"not already covered by local passes: {len(kept)}")

    new_ng_items = []
    for f in kept:
        seg = [w for w in words if f.wi_start <= w["wi"] < f.wi_end]
        if not seg:
            continue
        new_ng_items.append({
            "raw_word_index_start": f.wi_start, "raw_word_index_end": f.wi_end,
            "follow_word_index_start": f.wi_end, "follow_word_index_end": f.wi_end,
            "start": seg[0]["start"], "end": seg[-1]["end"],
            "duration": round(seg[-1]["end"] - seg[0]["start"], 3),
            "n_words": len(seg), "deleted_text": " ".join(w["text"] for w in seg),
            "following_text_in_raw": "", "similarity_to_following": None, "prefix_similarity": None,
            "dominant_speaker": seg[0].get("speaker_id"), "n_speakers_in_run": len({w.get("speaker_id") for w in seg}),
            "has_word_fragment": False, "has_internal_repetition": False,
            "label": f"CONTEXT_REVIEW_{f.kind}",
            "route": "CUT", "flag": "restore",  # 최대 삭제(2026-09-29): 넓은 회수망이라 항상 복원 후보로
            "route_reason": f"전체 맥락 검토: {f.reason} (confidence={f.confidence:.2f}) - 복원 후보로 자름",
            "llm_classification": None, "llm_model": MODEL,
        })
        print(f"  [{seg[0]['start']:.1f}s] {f.kind} conf={f.confidence:.2f} :: {f.reason}")

    out = edit_dir(folder) / "context_review.json"
    write_json(out, {"model": MODEL, "findings": [f.model_dump() for f in findings], "kept": len(kept)})

    if new_ng_items and ng_path.exists():
        ng_items.extend(new_ng_items)
        write_json(ng_path, ng_items)
        print(f"appended {len(new_ng_items)} item(s) to {ng_path}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    review(video_dir(args.folder))


if __name__ == "__main__":
    main()
