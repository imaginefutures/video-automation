"""Classify NG candidates with Claude (PLAN.md 4.3 step 3, 4.1 case taxonomy, 12장/모델 선택).

Takes the output of detect_ng_candidates.py and asks Claude to assign each candidate
a case label (A-F) with a recommended action. This is a LABELING step only - it never
executes a cut (PLAN.md 2.4: plan and execution are always separate).

Model tiering (PLAN.md 12장 "가장 비용대비 효율이 좋은 모델"):
  - claude-sonnet-5 classifies every candidate first. It's the cost-effective default for
    this task - the taxonomy is well-specified and few-shot examples do most of the work.
  - claude-opus-5-5 re-checks only the subset that's actually hard: case B ("같은 내용을 더
    잘 말하기" - PLAN.md 4.1 "B 케이스가 가장 어렵고 가장 중요하다") is always double-checked
    regardless of confidence, and anything else Sonnet itself was unsure about
    (confidence < ESCALATE_CONF_BELOW). This keeps the expensive model off the easy
    majority (C/D/most of A) and onto exactly the cases the taxonomy itself calls hardest.

Evidence given to the LLM, text AND audio (PLAN.md 4.2):
  - text context, auto-detected signals (word fragment, internal repetition, similarity)
  - acoustic evidence from prosody.py (F0 reset, F0-curve similarity, energy ratio) when
    edit/prosody.json exists - this was designed in PLAN.md 4.2 but never actually wired
    into the prompt until now (PLAN.md 12.A)
  - a handful of worked examples per case (PLAN.md 12.B: few-shot was designed in 4.3 step 3
    but the prompt shipped with zero of them)

Calls run in parallel (PLAN.md 12.E) since each candidate is judged independently.

Usage:
    python scripts/classify_candidates.py <candidates.json> --transcript <source_transcript.json> \
        [--prosody edit/prosody.json] [--out OUT.json]
"""
from __future__ import annotations
import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Literal, Optional

import anthropic
from pydantic import BaseModel

from common import load_env, words_only, thinking_kwargs
from prosody import load_prosody, span_evidence
import fewshot

MODEL_STANDARD = "claude-sonnet-5"   # default for every candidate (12장)
MODEL_ESCALATE = "claude-opus-5-5"   # only for case B and low-confidence Sonnet calls
ESCALATE_CONF_BELOW = 0.80
ALWAYS_ESCALATE_CASES = {"B"}        # PLAN.md 4.1: "B 케이스가 가장 어렵고 가장 중요하다"
MAX_WORKERS = 6

CASE_TAXONOMY = """\
너는 한국어 강의 영상의 컷편집을 돕는 NG(재시작) 판별기다. 아래 케이스 중 하나로 분류하라.

A. 실수 → 제대로 말하기: 앞 시도에 오류(잘못된 단어·숫자·문장 붕괴)가 있고 뒤에서 고침. 두 시도의 내용이 충돌.
B. 말하기 → 더 잘 말하기: 앞 시도도 틀리지 않았지만 같은 내용을 더 잘 설명하려고 다시 말함.
   핵심: 두 시도가 전달하는 정보가 실제로 같은지 확인하라 (문자열이 아니라 의미로 판단).
   같은 내용(주장·수치·대상·결론이 같음) -> NG. 새 정보 추가/확장이면 -> NG 아님.
C. 강조 반복: "정말 정말", "많이 많이" 같은 의도적 반복. 어휘 범주가 부사/형용사/감탄사.
D. 교육적 재진술 / 정상 나열: "다시 말하면", "즉", "첫째·둘째" 등 담화 흐름 안의 정상적 반복.
E. 형태론적 수정: 조사·어미만 바뀜 ("하나의 -> 하나를"). 어간은 동일, 변경 폭이 접사 수준.
F. 미완성 후 방향 전환: 문장을 버리고 전혀 다른 내용으로 넘어감. 재시작이 아니라 단순 중단.
OTHER: 위 어느 것도 아님 (예: 촬영 관련 대화, 화면 밖 화자의 개입, 잡담 등 콘텐츠와 무관한 발화).

주어지는 것: 삭제/재시작 후보 구간의 텍스트, 그 앞뒤 문맥, 이어지는 텍스트, 화자 정보, \
자동 탐지된 신호(단어 절단 표시 `--`, 내부 반복 여부), 음향 신호(피치·에너지). \
이 구간이 실제로 편집에서 잘렸는지는 알려주지 않는다 - 주어진 근거만으로 판단하라.

# 예시 (few-shot)

[예시 1 - case A]
판별 대상: "그러니까 참여자가 한 삼십 명 정도"
이어지는 문맥: "아니 잘못 말씀드렸네요 참여자가 사십오 명이었는데"
-> case=A, action=CUT, confidence=0.95
이유: "아니"로 시작하는 명시적 정정, 숫자가 30->45로 충돌. 실수 수정.

[예시 2 - case B, 내용 동일]
판별 대상: "이 실험 결과는 아이들이 스트레스를 받을 때 코르티솔 수치가 올라간다는 걸 보여줍니다"
이어지는 문맥: "그러니까 이 연구가 말하는 건, 아이가 스트레스 상황에 놓이면 코르티솔이라는 스트레스 호르몬이 증가한다는 겁니다"
-> case=B, same_content_as_following=true, action=CUT, confidence=0.85
이유: 주장(스트레스->코르티솔 증가)이 동일. 뒤 시도가 더 쉬운 설명으로 재진술한 것뿐, 새 정보 없음.

[예시 3 - case B, 내용 다름 (NG 아님)]
판별 대상: "이 실험 결과는 아이들이 스트레스를 받을 때 코르티솔 수치가 올라간다는 걸 보여줍니다"
이어지는 문맥: "그리고 이 코르티솔 수치는 만 3세 이전에 더 크게 올라간다는 후속 연구도 있었죠"
-> case=B, same_content_as_following=false, action=KEEP, confidence=0.9
이유: 뒤 문장이 연령대라는 새 조건을 추가함 - 재진술이 아니라 확장. 둘 다 유지.

[예시 4 - case C]
판별 대상: "정말"
이어지는 문맥: "정말 중요한 부분인데요"
-> case=C, action=KEEP, confidence=0.9
이유: 강조 부사 반복, 사이 쉼 없음, 의미 충돌 없음. 정상 강조.

[예시 5 - case E, 경계 깨끗함]
판별 대상: "하나의"
이어지는 문맥: "하나를 예로 들어보면"
-> case=E, action=CUT, confidence=0.8
이유: 어간 "하나" 동일, 조사만 의/를로 교체. 앞 단어 뒤 쉼이 있고 완전한 단어로 끝남 - 경계 깨끗.

[예시 6 - OTHER]
판별 대상: "잠깐만요 조명 좀 봐주실 수 있어요"
이어지는 문맥: (강의 내용 재개)
-> case=OTHER, action=REVIEW, confidence=0.9
이유: 촬영 관련 대화, 강의 내용과 무관. 국소 판별기가 결정할 사안이 아니라 4.6a 전체 맥락 검토로 넘김.

[예시 7 - case A, 발음 실수라 텍스트는 안 닮음]
판별 대상: "샐리그만"
자동 탐지 신호: ASR 신뢰도 낮음(logprob 하위 3%) - 발음 실수·잘못 들림일 수 있음
이어지는 문맥: "교수님에 따르면 자존감은..." (뒤이어 같은 인물을 "셀리그만"으로 여러 번 지칭)
-> case=A, action=CUT, confidence=0.75
이유: "샐리그만"과 "셀리그만"은 문자열로는 안 닮았지만(difflib 유사도 낮음), 같은 사람 이름을 가리키며
ASR 신뢰도가 유독 낮다 - 발음이 꼬였다가 스스로 고쳐 말한 경우다. **문자열 유사도가 낮다는 이유만으로
case를 정하지 마라** - ASR 저신뢰도 신호가 있고 문맥상 같은 지시 대상(사람·개념)을 가리키면 case A로
판단할 수 있다.
"""


class NGClassification(BaseModel):
    case: Literal["A", "B", "C", "D", "E", "F", "OTHER"]
    same_content_as_following: Optional[bool] = None  # only meaningful for case B
    recommended_action: Literal["CUT", "KEEP", "REVIEW"]
    confidence: float  # 0.0-1.0
    reasoning: str  # one sentence, in Korean


def load_words(path: Path) -> list[dict]:
    """Same word-only, index-tagged view detect_ng_candidates.py used to build i1/i2 and
    prosody.py used to build wi - the three MUST agree on indexing (the previous version of
    this function filtered `type != "spacing"` instead of `type == "word"`, which silently
    misaligned indices whenever the transcript had audio_event entries)."""
    return words_only(json.loads(path.read_text()))


def build_context(words: list[dict], i1: int, i2: int, pad: int = 15) -> tuple[str, str, str]:
    before = " ".join(w["text"] for w in words[max(0, i1 - pad):i1])
    span = " ".join(w["text"] for w in words[i1:i2])
    after = " ".join(w["text"] for w in words[i2:i2 + pad])
    return before, span, after


def build_prompt(run: dict, before: str, after: str, audio_evidence: str, fewshot_block: str = "") -> str:
    return f"""\
[앞 문맥]
{before}

[판별 대상 구간]
{run['deleted_text']}

[이어지는 문맥]
{after}

[자동 탐지 신호]
- 구간 길이: {run['duration']}초, 단어 수: {run['n_words']}
- 화자: {run['dominant_speaker']} (구간 내 화자 수: {run['n_speakers_in_run']})
- 단어 절단 표시(--): {run['has_word_fragment']}
- 구간 내 단어 반복: {run['has_internal_repetition']}
- 뒤따르는 텍스트와의 유사도: {run['similarity_to_following']}

[음향 신호]
{audio_evidence}
{fewshot_block}"""


def classify_one(client: anthropic.Anthropic, model: str, prompt: str) -> NGClassification:
    # thinking disabled: claude-sonnet-5 defaults to extended thinking, which was consuming
    # the entire max_tokens budget before emitting the structured output (parsed_output=None,
    # stop_reason="max_tokens") - confirmed against a real BS145 call during 12장 implementation.
    # `reasoning` in the output schema already carries the one-sentence "why".
    response = client.messages.parse(
        model=model, max_tokens=2000, system=CASE_TAXONOMY,
        messages=[{"role": "user", "content": prompt}], output_format=NGClassification,
        **thinking_kwargs(model),
    )
    return response.parsed_output


def classify_with_escalation(client: anthropic.Anthropic, prompt: str) -> tuple[NGClassification, str]:
    clf = classify_one(client, MODEL_STANDARD, prompt)
    needs_escalation = clf.case in ALWAYS_ESCALATE_CASES or clf.confidence < ESCALATE_CONF_BELOW
    if needs_escalation:
        clf = classify_one(client, MODEL_ESCALATE, prompt)
        return clf, MODEL_ESCALATE
    return clf, MODEL_STANDARD


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("candidates", type=Path, help="Output of detect_ng_candidates.py")
    ap.add_argument("--transcript", type=Path, required=True,
                     help="The raw transcript JSON the candidates were extracted from (for context padding)")
    ap.add_argument("--prosody", type=Path, default=None,
                     help="Output of prosody.py (edit/prosody.json) - omit to classify on text alone")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--only-label", type=str, default=None,
                     help="Only classify runs with this label from the candidates file (e.g. NEEDS_HUMAN_REVIEW)")
    args = ap.parse_args()

    load_env()
    data = json.loads(args.candidates.read_text())
    words = load_words(args.transcript)
    prosody = json.loads(args.prosody.read_text()) if args.prosody and args.prosody.exists() else None
    client = anthropic.Anthropic()

    runs = data["deleted_runs"]
    if args.only_label:
        runs = [r for r in runs if r["label"] == args.only_label]

    # transcript.json is always <video>/edit/transcript.json - derive the video name so L2
    # few-shot retrieval excludes this video's own (not-yet-decided) cases (fewshot.py)
    video_name = args.transcript.resolve().parent.parent.name

    prompts = []
    n_with_fewshot = 0
    for run in runs:
        before, _span, after = build_context(words, run["raw_word_index_start"], run["raw_word_index_end"])
        fi1 = run.get("follow_word_index_start", run["raw_word_index_end"])
        fi2 = run.get("follow_word_index_end", run["raw_word_index_end"] + run["n_words"])
        evidence = span_evidence(prosody, words, run["raw_word_index_start"], run["raw_word_index_end"], fi1, fi2)
        similar = fewshot.retrieve(run["deleted_text"], stage="ng", exclude_video=video_name)
        if similar:
            n_with_fewshot += 1
        fewshot_block = fewshot.format_fewshot(similar)
        prompts.append(build_prompt(run, before, after, evidence, fewshot_block))

    print(f"classifying {len(runs)} candidates ({MODEL_STANDARD}, escalating case B / low-confidence "
          f"to {MODEL_ESCALATE}, {MAX_WORKERS} parallel workers, {n_with_fewshot} with L2 few-shot)...")

    results: list[Optional[dict]] = [None] * len(runs)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(classify_with_escalation, client, prompt): n
                   for n, prompt in enumerate(prompts)}
        done = 0
        for fut in as_completed(futures):
            n = futures[fut]
            clf, model = fut.result()
            run = runs[n]
            results[n] = {**run, "llm_classification": clf.model_dump(), "llm_model": model}
            done += 1
            print(f"  [{done}/{len(runs)}] [{run['start']:.1f}s] case={clf.case} action={clf.recommended_action} "
                  f"conf={clf.confidence:.2f} model={model.replace('claude-', '')} :: {run['deleted_text'][:50]}")

    out_path = args.out or args.candidates.with_name(args.candidates.stem + "_classified.json")
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    n_escalated = sum(1 for r in results if r["llm_model"] == MODEL_ESCALATE)
    print(f"\nwrote {out_path} ({n_escalated}/{len(results)} escalated to {MODEL_ESCALATE})")


if __name__ == "__main__":
    main()
