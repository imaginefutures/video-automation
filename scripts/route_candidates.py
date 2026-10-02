"""Route classified NG candidates to CUT/KEEP + restore-candidate flag (docs/기획/01-처리-과정.md
5단계, "최대 삭제" 방침 — 2026-09-29 개편, PLAN.md 2.2-4 계열의 옛 AUTO_SAFE/REVIEW/KEEP 3분류를 대체).

Input is the output of classify_region.py (each record already carries an
`llm_classification` with case/action/confidence). This step never executes a cut - it only
assigns `route` ("CUT"/"KEEP") + `flag` (None/"restore") for the review queue; execution and
final boundary placement happen later (assemble_draft.py -> seam_refine.py -> server.py's
confirm()). Plan and execution stay separate (서비스-개요와-철학.md 원칙 3).

Decision table (docs/기획/01-처리-과정.md 5단계 표):
  - The DEFAULT direction is CUT. Content only stays route=KEEP when the classifier is
    confident it is genuine content (C/D/etc at high confidence) - if the classifier itself
    isn't sure, it's cheaper for the user to restore one clip than to hunt for a missed NG.
  - Anything the taxonomy doesn't treat as safe self-repair (case not in A/B/E), anything low
    confidence either direction, anything spanning >5s (mixed-span risk), and anything the
    LLM itself called REVIEW/OTHER all still get cut - just flagged "restore" so they surface
    in the review queue instead of disappearing silently.
  - Candidates whose `source` is `"llm"` (detect_regions.py's whole-document scan, 2026-09-30
    하향식 재설계) always get flagged when cut, regardless of confidence - unlike local hints
    or the pronunciation detector, the region's existence itself is the LLM's own inference,
    not an independently-verified mechanical signal (judge≠maker 원칙, BS167 실측 반례).

Usage:
    python scripts/route_candidates.py <classified.json> [--out routed.json]
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from common import load_transcript, words_only, norm

# 2026-10-01: 사용자가 기존 테스트 영상 여러 편에서 반복 확인한 패턴 - 삭제 구간(wi_end) 바로
# 다음에 접속사로 시작하는 새 문장이 오면, 그 접속사까지 삭제 범위에 같이 먹히는 경우가 있었다.
# classify_region.py의 final_attempt_wi_start 클램프와 같은 "경계가 실제보다 넘어간다" 버그
# 종류지만, 그건 재시도 사슬 전용이라 "삭제 뒤에 전혀 다른 새 문장이 이어지는" 이 구조에는 안
# 걸린다(docs/미결-사항.md). 근본 수정(부분 루프의 확장 대안+정보손실 교차판정, docs/남은-개발.md)
# 전까지의 즉시 안전망 - 신뢰도와 무관하게 항상 flag해서 "경고 없는 복원"만은 막는다.
CONNECTIVE_VOCAB = {"그래서", "근데", "그러니까", "그런데", "그리고", "그러면", "그럼", "하지만", "그치만", "아무튼"}

CUT_CONFIDENCE_MIN = 0.75      # action=CUT needs at least this confidence to apply with no flag
KEEP_CONFIDENCE_MIN = 0.55     # action=KEEP needs at least this to apply with no flag. 2026-09-30:
                               # lowered back from 0.80 (which the 09-29 design note raised on a priori
                               # reasoning - "KEEP has nothing to restore later, so it needs a higher
                               # bar than CUT" - untested against gold at the time). BS145+BS167 gold
                               # comparison showed the 0.80 bar was actively harmful: of the classifier's
                               # action=KEEP calls sitting in [0.55, 0.80) that got force-CUT-and-flagged
                               # under the old bar, 26/29 (90%) were gold-KEEP too - i.e. the classifier's
                               # own KEEP call is reliable even at "low" confidence, because genuine
                               # indecision already routes to action=REVIEW instead (a separate LLM
                               # signal, unaffected by this constant). Forcing a cut anyway was the
                               # single largest identified precision-loss pattern this session
                               # (결정-이력.md 09-30, "KEEP 임계값 완화").
MIXED_SPAN_DUR_MAX = 5.0       # seconds: longer CUT spans risk containing real content (mixed span)
SAFE_CUT_CASES = {"A", "B", "E"}  # cases the taxonomy treats as genuine self-repair


def boundary_swallows_connective(run: dict, words: list[dict] | None) -> bool:
    """True if the first kept word right after this cut's wi_end is a sentence-initial
    connective - a structural signal that the boundary may have overreached into the start
    of a different, surviving sentence rather than the deleted material itself."""
    if not words:
        return False
    wi_end = run.get("raw_word_index_end")
    if wi_end is None or not (0 <= wi_end < len(words)):
        return False
    return norm(words[wi_end]["text"]) in CONNECTIVE_VOCAB


def route_one(run: dict, words: list[dict] | None = None) -> dict:
    label = run["label"]
    clf = run.get("llm_classification")

    if label == "MULTI_SPEAKER_CONTEXT_CHECK":
        return {"route": "CUT", "flag": "restore",
                "route_reason": "화자 2명 이상 - 국소 분류기로 결정 안 함, 복원 후보로 자름"}

    if label == "PAUSE_OR_TIGHTEN":
        return {"route": "CUT", "flag": "restore",
                "route_reason": "결정론적 신호 없는 짧은 삭제 - 근거 부족, 복원 후보로 자름"}

    if clf is None:
        return {"route": "CUT", "flag": "restore", "route_reason": "LLM 분류 미실행 - 복원 후보로 자름"}

    action = clf["recommended_action"]
    case = clf["case"]
    conf = clf["confidence"]

    if action == "KEEP":
        if conf >= KEEP_CONFIDENCE_MIN:
            return {"route": "KEEP", "flag": None, "route_reason": f"KEEP, 신뢰도 {conf:.2f} - 유지"}
        return {"route": "CUT", "flag": "restore",
                "route_reason": f"KEEP이지만 신뢰도 낮음({conf:.2f} < {KEEP_CONFIDENCE_MIN}) - 복원 후보로 자름"}

    if action == "REVIEW":
        return {"route": "CUT", "flag": "restore",
                "route_reason": f"LLM 자체 판단 불확실 (case={case}, conf={conf:.2f}) - 복원 후보로 자름"}

    if action == "CUT":
        problems = []
        if case not in SAFE_CUT_CASES:
            problems.append(f"case={case} 자동 삭제 케이스 아님(A/B/E만)")
        if conf < CUT_CONFIDENCE_MIN:
            problems.append(f"신뢰도 낮음({conf:.2f} < {CUT_CONFIDENCE_MIN})")
        if run["duration"] > MIXED_SPAN_DUR_MAX:
            problems.append(f"구간 {run['duration']}s로 김(mixed-span 위험)")
        if run.get("source") == "llm":
            # 2026-09-30: detect_regions.py의 전체 맥락 LLM 스캔이 찾은 구간은 "구간의 존재
            # 자체"부터 LLM 자신의 추론이라, 국소 힌트(단어 절단·3단어 내 중복)나 발음 실수
            # 탐지(ASR logprob)처럼 독립적인 기계적 신호로 사전 검증되지 않았다. 이 상태에서
            # classify_region.py(같은 계열 모델)가 그 추론에 스스로 확신을 갖는 것은 judge≠maker
            # 원칙과 어긋난다 - BS167 실측: 이 경로로 conf=0.85·case=A가 나온 항목 하나가 실제로는
            # 서로 다른 문장인데 "같은 내용 재진술"로 잘못 판단돼, 신뢰도만으로는 걸러지지 않고
            # flag 없이 조용히 잘렸다(경고 없는 복원 위험 - 안전 지표 위반). whole_context_review.py
            # 시절의 원칙("넓은 회수망이라 항상 복원 후보로")을 그대로 적용: 신뢰도와 무관하게 항상
            # flag.
            problems.append("전체 맥락 LLM 스캔이 찾은 구간 - 신뢰도와 무관하게 항상 복원 후보로")
        if boundary_swallows_connective(run, words):
            problems.append("삭제 범위 바로 뒤가 접속사로 시작 - 다음 문장의 시작일 수 있어 항상 복원 후보로")
        if problems:
            return {"route": "CUT", "flag": "restore", "route_reason": "; ".join(problems) + " - 복원 후보로 자름"}
        return {"route": "CUT", "flag": None, "route_reason": f"CUT, case={case}, 신뢰도 {conf:.2f} - 그대로 적용"}

    return {"route": "CUT", "flag": "restore", "route_reason": f"알 수 없는 action: {action} - 복원 후보로 자름"}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("classified", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    runs = json.loads(args.classified.read_text())
    words: list[dict] | None = None
    try:
        folder = args.classified.resolve().parent.parent  # edit/ng_classified.json -> videos/<name>
        words = words_only(load_transcript(folder))
    except (FileNotFoundError, KeyError):
        print("  [warn] transcript.json을 못 찾음 - 접속사 경계 안전망 건너뜀")

    routed = []
    for run in runs:
        decision = route_one(run, words)
        item = {**run, **decision}
        routed.append(item)

    counts: dict[str, int] = {}
    for r in routed:
        key = r["route"] + ("+flag" if r.get("flag") else "")
        counts[key] = counts.get(key, 0) + 1
    print(f"routed {len(routed)} candidates:")
    for route, n in sorted(counts.items()):
        print(f"  {route}: {n}")

    flagged = sorted([r for r in routed if r.get("flag")], key=lambda r: r["start"])
    if flagged:
        print(f"\ncomplex/restore-flagged ({len(flagged)}), by timestamp:")
        for r in flagged:
            print(f"  [{r['start']:.1f}s] {r['route_reason']}")
            print(f"    {r['deleted_text'][:70]}")

    out_path = args.out or args.classified.with_name(args.classified.stem.replace("_classified", "") + "_routed.json")
    out_path.write_text(json.dumps(routed, ensure_ascii=False, indent=2))
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
