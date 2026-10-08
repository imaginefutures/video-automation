"""Stage 2 (하향식 재설계, 2026-09-30) - "부분을 좁게" 본다. detect_regions.py(Stage 1)가
표시한 구간마다 확대해서 정확한 단어 경계와 case(A~F)/신뢰도를 정한다. 대략적인 구간을 정밀한
컷으로 좁히는 단계 - classify_candidates.py를 대체(같은 케이스 taxonomy·few-shot·모델 티어링·
음향 증거 구조는 그대로 재사용, 새로 필요한 건 "구간을 보고 정확한 경계를 스스로 정하는 것"뿐).

두 종류의 후보를 같은 방식으로 판정한다:
  - Stage 1의 `precise=False` 구간(전체 맥락 LLM 스캔이 찾음): 대략적인 범위만 있으므로 앞뒤
    여유 컨텍스트를 단어 id와 함께 보여주고, 정확한 wi_start/wi_end를 이 단계에서 처음 확정한다.
  - `precise=True` 후보(로컬 힌트, 발음 실수 탐지): 경계가 이미 정확하므로 LLM이 뭘 답하든
    원래 경계를 그대로 쓴다(case/신뢰도만 판정에 쓴다) - 이미 결정론적으로 확정된 경계를 LLM이
    "도와준답시고" 흔드는 걸 막는다.

RESTART 구간에 ref_wi_start/end(같은 내용을 다시 말한 "다른 쪽" 위치)가 있으면 그 텍스트도
같이 보여준다 - "먼 재진술인데 비교 대상이 안 보임"(기존 whole_context_review.py 09-30 진단의
근본 원인)을 구조적으로 없앤다.

**배치 분류를 시도했다가 되돌림 (2026-09-30)**: 맞닿지 않은 근접 후보(예: 재시작 사슬의 CUT
판정 바로 뒤 "-을수록 더~" 같은 정상 구문)를 한 호출로 묶어 문맥을 공유시키면 서로 상충하는
판정을 줄일 수 있을 거라 보고 `batch_nearby()`(단어 간격 25 이내 묶음)를 시도했다. BS167로
재검증한 결과 **정밀도 0.748→0.716, 재현율(보정) 0.764→0.726로 명백히 악화** - 배치가 커질수록
(최대 10개 후보/호출) 모델이 A~F 세부 taxonomy를 정교하게 적용하지 못하고 손쉬운 case=OTHER로
몰리는 현상을 확인(122건 중 47건이 OTHER, 배치 전에는 이 정도로 몰린 적이 없었음) - 여러 후보를
한 번에 보여주는 것 자체가 판단 품질을 떨어뜨렸다. 여기서 얻은 정확한 case별 오판(예시 10)만
few-shot으로 남기고, 배치 자체는 되돌려 그 전(각 후보를 독립적으로 판정)으로 복귀했다.

Usage:
    python scripts/classify_region.py <video-edit/NAME> [--no-llm]
"""
from __future__ import annotations
import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Literal, Optional

import anthropic
from pydantic import BaseModel

from common import load_env, video_dir, edit_dir, load_transcript, words_only, write_json, thinking_kwargs, log_llm_usage
from prosody import load_prosody, span_evidence
from audio_map import load_audio_map, breath_before
import fewshot

MODEL_STANDARD = "claude-sonnet-5"
MODEL_ESCALATE = "claude-opus-5-5"
ESCALATE_CONF_BELOW = 0.80
ALWAYS_ESCALATE_CASES = {"B"}
MAX_WORKERS = 6
WINDOW_PAD = 12   # 판별 대상 구간 앞뒤로 이 정도 단어를 더 보여줘서 경계를 조정할 여지를 준다
REF_PAD = 8        # 참고용 재진술 위치는 더 좁게

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

**아래 [판별 구간(단어 id 포함)]에서 실제로 잘라야 할 정확한 wi_start/wi_end를 답으로 채워라** -
반열림 구간(wi_end는 포함 안 됨). "[의심되는 대략적 범위]"는 참고용이고, 실제 경계는 텍스트를
읽고 네가 다시 정하라 - 재시작/실수의 시작과 끝을 단어 단위로 정확히 짚어라. "경계가 이미
확정됨"이라고 적힌 경우는 그 값 그대로 wi_start/wi_end에 채워라.

**이 구간 안에 실패한 시도가 여럿이고 그중 하나가 결국 완성된 문장으로 끝났다면**, 그 완성된
시도가 시작하는 단어 id를 `final_attempt_wi_start`에 반드시 채워라. **wi_end가 그 값을 넘으면
안 된다** - 완성된 문장의 일부까지 자르면 안 되니까. (해당 없으면 비워둬도 된다.)

주어지는 것: 판별 대상 구간과 그 앞뒤 문맥(단어 id 포함), 참고용 재진술 위치(있다면), 자동 탐지된
신호, 음향 신호(피치·에너지·숨소리). 이 구간이 실제로 편집에서 잘렸는지는 알려주지 않는다 - 주어진
근거만으로 판단하라.

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
이유: 촬영 관련 대화, 강의 내용과 무관. 전체 맥락 검토로 넘김.

[예시 7 - case A, 발음 실수라 텍스트는 안 닮음]
판별 대상: "샐리그만"
자동 탐지 신호: ASR 신뢰도 낮음(logprob 하위 3%) - 발음 실수·잘못 들림일 수 있음
이어지는 문맥: "교수님에 따르면 자존감은..." (뒤이어 같은 인물을 "셀리그만"으로 여러 번 지칭)
-> case=A, action=CUT, confidence=0.75
이유: "샐리그만"과 "셀리그만"은 문자열로는 안 닮았지만(difflib 유사도 낮음), 같은 사람 이름을 가리키며
ASR 신뢰도가 유독 낮다 - 발음이 꼬였다가 스스로 고쳐 말한 경우다. **문자열 유사도가 낮다는 이유만으로
case를 정하지 마라** - ASR 저신뢰도 신호가 있고 문맥상 같은 지시 대상(사람·개념)을 가리키면 case A로
판단할 수 있다.

[예시 8 - RESTART, 먼 재진술]
[의심되는 대략적 범위]: 461-478 (표현이 다른 재진술로 의심됨)
[참고 - 나중에 같은 내용을 다시 말한 곳]: "997:부모가 998:아이가 999:일상 ... 선택지를 주는 게 중요하다"
판별 구간 실제 텍스트: "아이한테 자율성을 주려면..." (선택지를 준다는 같은 결론)
-> wi_start=461, wi_end=470(문장 실제 끝), case=B, same_content_as_following=true, action=CUT, confidence=0.6
이유: 표현은 다르지만 "선택지를 주는 게 자율성/실행 기능에 중요하다"는 같은 결론을 뒤(997행)에서
다시, 더 정리된 형태로 말한다 - 먼저 나온 쪽을 자른다(재촬영은 마지막 시도만 남긴다).

[예시 9 - RESTART 사슬 안에 완성된 시도가 섞임, final_attempt_wi_start 필수]
판별 구간(단어 id 포함): "288:이 289:실행 290:기능은 291:부모가 292:아이와의 ... 299:주느냐와
300:부모가 301:아이와의, 302:부모가 303:아이와의 304:일상에서 305:선택지를 306:얼마,
307:부모가 308:아이와의 309:일상에서 310:선택의 311:기회를 312:더 313:많이 314:줄수록
315:더 316:잘 317:자랄 318:수 319:있습니다."
-> wi_start=290, wi_end=307, final_attempt_wi_start=307, case=A, action=CUT, confidence=0.85
이유: 290-299가 미완성으로 끊긴 뒤 300-301, 302-306이 각각 짧게 무너진 재시도이고, **307부터
"부모가 아이와의 일상에서 선택의 기회를 더 많이 줄수록 더 잘 자랄 수 있습니다"로 완결된다** -
final_attempt_wi_start=307이므로 wi_end는 반드시 307 이하여야 한다(307 이상을 자르면 완성된
문장의 시작 부분까지 함께 잘려나간다 - 실제로 이 실수가 나서 정답지 대조로 발견됨).
"""
# 2026-09-30: 예시 10("-을수록 더~" 비례 구문, case C)을 여기 추가했다가 되돌렸다 - 추가한 직후
# 재검증에서 이 예시와 무관한 case E 항목 2건(BS145/BS167 각 1건)이 오삭제 flag 누락으로
# 나왔다(신뢰도가 임계값 바로 위로 올라감). 이 예시 내용과 직접 연관은 안 보이고 순수 샘플링
# 변동성일 가능성이 더 크지만, 안전 지표가 최우선이라 원인을 확실히 못 가른 채로는 프롬프트를
# 안 건드리는 쪽을 택했다. 다음에 다시 시도한다면 반드시 여러 번 재실행해 재현되는지 먼저
# 확인할 것 - 결정-이력.md 09-30 참고.


class RegionClassification(BaseModel):
    wi_start: int
    wi_end: int  # exclusive
    final_attempt_wi_start: Optional[int] = None  # 이 구간 안에 실패한 시도가 여럿이고 그중
    # 하나가 완성된 형태로 끝났다면, 그 완성된 시도가 시작하는 단어 id. wi_end는 절대 이 값을
    # 넘으면 안 된다 - 2026-09-30 BS167 실측 버그(reasoning은 "307번부터 완성됨"이라고 정확히
    # 판단했지만 wi_end는 312를 반환해 완성된 문장의 앞부분(307-311)까지 같이 잘림, 정답지 대조로
    # 확인) 재발 방지용 필드. 코드가 이 값으로 wi_end를 강제로 clamp한다 - 자기 근거와 반환값이
    # 어긋나도 근거 쪽을 믿는다.
    case: Literal["A", "B", "C", "D", "E", "F", "OTHER"]
    same_content_as_following: Optional[bool] = None
    recommended_action: Literal["CUT", "KEEP", "REVIEW"]
    confidence: float
    reasoning: str


def format_indexed(words: list[dict], lo: int, hi: int) -> str:
    return " ".join(f"{w['wi']}:{w['text']}" for w in words[lo:hi])


def build_prompt(words: list[dict], region: dict, audio_evidence: str, fewshot_block: str = "") -> tuple[str, int, int]:
    wi_start, wi_end = region["wi_start"], region["wi_end"]
    precise = region.get("precise", True)
    lo = max(0, wi_start - WINDOW_PAD)
    hi = min(len(words), wi_end + WINDOW_PAD)
    window = format_indexed(words, lo, hi)

    boundary_note = (f"경계가 이미 확정됨 - wi_start={wi_start}, wi_end={wi_end}로 답하라"
                      if precise else "정확한 경계는 위 창에서 네가 다시 판단해서 답하라")

    ref_block = ""
    ref_s, ref_e = region.get("ref_wi_start"), region.get("ref_wi_end")
    if ref_s is not None and ref_e is not None:
        rlo, rhi = max(0, ref_s - REF_PAD), min(len(words), ref_e + REF_PAD)
        ref_block = f"\n\n[참고 - 나중에(또는 먼저) 같은 내용을 다시 말한 곳 - 비교용, 자르지 않음]\n{format_indexed(words, rlo, rhi)}"

    prompt = f"""\
[판별 구간(단어 id 포함, {lo}-{hi})]
{window}

[의심되는 대략적 범위]
{wi_start}-{wi_end} ({boundary_note}) - 찾은 이유: {region.get('reason', '')}
{ref_block}

[자동 탐지 신호]
- 구간 종류: {region.get('kind', 'RESTART')}
- 출처: {region.get('source', 'llm')}

[음향 신호]
{audio_evidence}
{fewshot_block}"""
    return prompt, lo, hi


def classify_one(client: anthropic.Anthropic, model: str, prompt: str, folder: Path) -> RegionClassification:
    response = client.messages.parse(
        model=model, max_tokens=2000, system=CASE_TAXONOMY,
        messages=[{"role": "user", "content": prompt}], output_format=RegionClassification,
        **thinking_kwargs(model),
    )
    log_llm_usage(folder, "classify_region", model, response.usage)
    return response.parsed_output


def classify_with_escalation(client: anthropic.Anthropic, prompt: str, folder: Path) -> tuple[RegionClassification, str]:
    clf = classify_one(client, MODEL_STANDARD, prompt, folder)
    needs_escalation = clf.case in ALWAYS_ESCALATE_CASES or clf.confidence < ESCALATE_CONF_BELOW
    if needs_escalation:
        clf = classify_one(client, MODEL_ESCALATE, prompt, folder)
        return clf, MODEL_ESCALATE
    return clf, MODEL_STANDARD


def consolidate(regions: list[dict]) -> list[dict]:
    """2026-09-30 BS167 실측 - Stage 1(전체 스캔)·발음 실수 탐지·(나중에) global_review의 추가
    항목이 같은 재시작 덩어리를 각자 따로 찾아내면, 사람 눈엔 하나인 NG가 서로 겹치는 여러 개의
    ng.json 항목/검토 카드로 쪼개진다(예: 267 wi 85-95 하나가 실제로는 76/77/78/144/145/146
    까지 7개로 나뉜 사례). 분류하기 전에 겹치거나 맞닿은 후보를 하나로 합쳐, Stage 2 호출도
    한 번만 하고 ng.json에도 하나만 남긴다. 참고 근거(reason)는 전부 이어붙여 Stage 2 프롬프트에
    다 전달되게 한다 - 정보 손실 없이 개수만 줄인다."""
    regions = sorted(regions, key=lambda r: (r["wi_start"], r["wi_end"]))
    merged: list[dict] = []
    for r in regions:
        if merged and r["wi_start"] <= merged[-1]["wi_end"]:
            m = merged[-1]
            m["wi_start"] = min(m["wi_start"], r["wi_start"])
            m["wi_end"] = max(m["wi_end"], r["wi_end"])
            m["precise"] = m["precise"] and r.get("precise", True)
            m["_sources"].append(r)
        else:
            merged.append({**r, "_sources": [r]})
    for m in merged:
        sources = m.pop("_sources")
        if len(sources) == 1:
            continue
        # LLM 전체 스캔 출신을 대표로 삼는다(존재했는지부터 판단이 필요했던 쪽이라 더 많은 맥락을
        # 담고 있음) - 없으면 신뢰도가 가장 높은 쪽. 나머지 근거는 이어붙여 정보를 안 버린다.
        best = max(sources, key=lambda s: (s.get("source") == "llm", s.get("confidence", 0)))
        m["kind"] = best["kind"]; m["source"] = best.get("source")
        m["ref_wi_start"] = best.get("ref_wi_start"); m["ref_wi_end"] = best.get("ref_wi_end")
        m["confidence"] = max(s.get("confidence", 0) for s in sources)
        m["reason"] = " / ".join(dict.fromkeys(s["reason"] for s in sources if s.get("reason")))
    return merged


def load_regions(edit: Path) -> list[dict]:
    """Stage 1(detect_regions.py)의 regions.json + 발음 실수 탐지(별도 채널, ng_candidates.json)를
    합친 전체 분류 대상 목록 - 겹치거나 맞닿은 것은 classify하기 전에 하나로 합친다(consolidate)."""
    out: list[dict] = []
    regions_path = edit / "regions.json"
    if regions_path.exists():
        out.extend(json.loads(regions_path.read_text())["regions"])
    cand_path = edit / "ng_candidates.json"
    if cand_path.exists():
        for r in json.loads(cand_path.read_text()).get("deleted_runs", []):
            out.append({
                "wi_start": r["raw_word_index_start"], "wi_end": r["raw_word_index_end"],
                "precise": True, "kind": "PRONUNCIATION", "reason": r.get("reason", ""),
                "confidence": 0.7, "ref_wi_start": None, "ref_wi_end": None,
                "source": "pronunciation", "deleted_text": r["deleted_text"],
            })
    return consolidate(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--no-llm", action="store_true", help="LLM 호출 없이 그대로(경계는 대략치 그대로 - --no-llm 파이프라인용)")
    args = ap.parse_args()

    load_env()
    folder = video_dir(args.folder)
    edit = edit_dir(folder)
    words = words_only(load_transcript(folder))
    regions = load_regions(edit)
    print(f"classifying {len(regions)} region(s)")

    out_path = args.out or edit / "ng_classified.json"

    if args.no_llm:
        results = []
        for r in regions:
            seg = words[r["wi_start"]:r["wi_end"]]
            if not seg:
                continue
            results.append({
                "raw_word_index_start": r["wi_start"], "raw_word_index_end": r["wi_end"],
                "start": seg[0]["start"], "end": seg[-1]["end"],
                "duration": round(seg[-1]["end"] - seg[0]["start"], 3), "n_words": len(seg),
                "deleted_text": " ".join(w["text"] for w in seg),
                "label": f"REGION_{r['kind']}", "llm_classification": None, "llm_model": None,
                "source": r.get("source"),
            })
        write_json(out_path, results)
        print(f"wrote {out_path} (--no-llm, {len(results)} candidate(s), 분류 없음)")
        return

    prosody = load_prosody(folder)
    amap = load_audio_map(folder)
    client = anthropic.Anthropic()
    video_name = folder.name

    # 2026-10-01: L2 사용자 사례 few-shot을 껐다가(개인화 폐기 방침) BS167 gold 재검증에서 재현율이
    # 0.704~0.764 -> 0.515로 폭락(정밀도도 0.748->0.699)하는 걸 실측 - 노이즈 범위(±0.04, 06
    # 검증 문서)를 한참 벗어나는 진짜 회귀라 되돌렸다. "개인화(사용자별로 다르게 적용)"와 "few-shot
    # 예시 자체가 재현율에 기여"는 별개 문제였다 - 이 예시들을 사용자별 저장소가 아니라 공유
    # 저장소로 재설계하는 건 남은 과제로 남긴다(docs/남은-개발.md, docs/미결-사항.md).
    n_with_fewshot = 0
    prompts, windows = [], []
    for r in regions:
        seg = words[r["wi_start"]:r["wi_end"]]
        query_text = r.get("deleted_text") or " ".join(w["text"] for w in seg)
        follow_i1 = r["wi_end"]
        follow_i2 = min(len(words), r["wi_end"] + max(3, r["wi_end"] - r["wi_start"]))
        evidence_lines = [span_evidence(prosody, words, r["wi_start"], r["wi_end"], follow_i1, follow_i2)]
        if seg:
            breath = breath_before(amap, seg[0]["start"])
            if breath:
                evidence_lines.append(f"- 구간 시작 {seg[0]['start'] - breath['end']:.2f}초 전에 숨소리 감지됨 (재시작 가능성 보강 신호)")
        similar = fewshot.retrieve(query_text, stage="ng", exclude_video=video_name)
        if similar:
            n_with_fewshot += 1
        fewshot_block = fewshot.format_fewshot(similar)
        prompt, lo, hi = build_prompt(words, r, "\n".join(evidence_lines), fewshot_block)
        prompts.append(prompt)
        windows.append((lo, hi))

    print(f"classifying with {MODEL_STANDARD} (escalating case B / low-confidence to {MODEL_ESCALATE}, "
          f"{MAX_WORKERS} parallel workers, {n_with_fewshot} with L2 few-shot)...")

    results: list[Optional[dict]] = [None] * len(regions)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(classify_with_escalation, client, prompt, folder): n
                   for n, prompt in enumerate(prompts)}
        done = 0
        for fut in as_completed(futures):
            n = futures[fut]
            clf, model = fut.result()
            r = regions[n]
            lo, hi = windows[n]
            if r.get("precise", True):
                wi_start, wi_end = r["wi_start"], r["wi_end"]
            else:
                wi_start, wi_end = clf.wi_start, clf.wi_end
                if not (lo <= wi_start < wi_end <= hi):
                    print(f"  [skip] LLM이 창 밖의 경계를 답함({wi_start}-{wi_end}, 허용 {lo}-{hi}) - "
                          f"대략적 범위로 되돌림")
                    wi_start, wi_end = r["wi_start"], r["wi_end"]
            # 2026-09-30 BS167 실측 버그 재발 방지: reasoning은 "N번부터 완성됨"이라고 정확히
            # 판단했는데 wi_end가 그 N을 넘어 완성된 문장의 앞부분까지 잘랐던 사례를 정답지 대조로
            # 발견 - final_attempt_wi_start가 있으면 자기 근거를 신뢰해 wi_end를 강제로 clamp한다.
            if clf.final_attempt_wi_start is not None and wi_end > clf.final_attempt_wi_start > wi_start:
                print(f"  [clamp] wi_end {wi_end}->{clf.final_attempt_wi_start} "
                      f"(완성된 시도 보호, final_attempt_wi_start)")
                wi_end = clf.final_attempt_wi_start
            seg = words[wi_start:wi_end]
            if not seg:
                done += 1
                continue
            results[n] = {
                "raw_word_index_start": wi_start, "raw_word_index_end": wi_end,
                "start": seg[0]["start"], "end": seg[-1]["end"],
                "duration": round(seg[-1]["end"] - seg[0]["start"], 3), "n_words": len(seg),
                "deleted_text": " ".join(w["text"] for w in seg),
                "label": f"REGION_{r['kind']}",
                "llm_classification": clf.model_dump(), "llm_model": model,
                "source": r.get("source"),
            }
            done += 1
            print(f"  [{done}/{len(regions)}] [{seg[0]['start']:.1f}s] case={clf.case} action={clf.recommended_action} "
                  f"conf={clf.confidence:.2f} model={model.replace('claude-', '')} :: {results[n]['deleted_text'][:50]}")

    results = [r for r in results if r is not None]
    write_json(out_path, results)
    n_escalated = sum(1 for r in results if r["llm_model"] == MODEL_ESCALATE)
    print(f"\nwrote {out_path} ({n_escalated}/{len(results)} escalated to {MODEL_ESCALATE})")


if __name__ == "__main__":
    main()
