"""구조적 태그 추출 (docs/기획/04-지식-층과-학습.md 3장, 2026-10-01).

개인화(사용자별 통계로 자동 라우팅을 바꾸는 것)를 전면 폐기하고 그 자리를 대체하는 "구조적 의심
탐지"의 1단계. 사람 취향과 무관하게 기계적으로 계산 가능한 특징만 NG 후보에 태그로 붙인다 - 이
태그는 자동 라우팅에 전혀 영향을 주지 않고(route_candidates.py는 그대로 CUT/KEEP+flag만 결정),
오직 server.py가 사용자 결정을 모아 "같은 태그에서 결정이 한쪽으로만 쏠리는지" 집계하는 데만
쓰인다 (structural_suspects.py 참고).

새 태그가 필요해지면(새로운 버그 패턴을 발견하면) 여기 함수만 추가하면 된다 - 케이스
taxonomy(A~F, classify_region.py)는 건드리지 않는다.
"""
from __future__ import annotations

# route_candidates.py의 접속사 삼킴 즉시 안전망과 같은 목록 - 이 리스트가 바뀌면 두 곳 다 갱신한다.
CONNECTIVE_VOCAB = {"그래서", "근데", "그러니까", "그런데", "그리고", "그러면", "그럼", "하지만", "그치만", "아무튼"}

NEAR_THRESHOLD_MARGIN = 0.03


def _norm(text: str) -> str:
    return text.strip().rstrip(".,!?~…。，").lower()


def boundary_followed_by_connective(item: dict, words: list[dict]) -> bool:
    """삭제 범위(wi_end) 바로 다음 단어가 접속사인가 - route_candidates.py의 안전망과 같은 신호를
    여기서도 태그로 남겨, 이 패턴이 반복되는지(개인 취향이 아니라 보편적 버그인지) 추적한다."""
    wi_end = item.get("raw_word_index_end")
    if wi_end is None or not words or not (0 <= wi_end < len(words)):
        return False
    return _norm(words[wi_end]["text"]) in CONNECTIVE_VOCAB


def source_llm_wide_scan(item: dict) -> bool:
    """Stage 1 전체 맥락 스캔이 찾아낸 구간인가 - route_candidates.py가 신뢰도 무관 항상 flag하는
    것과 같은 신호. 이미 늘 flag되므로 "복원됐다"는 사실 자체는 약한 신호지만, 같은 유형이 쌓이면
    Stage 1의 과다 탐지 경향 자체를 다시 봐야 한다는 근거가 된다."""
    return item.get("source") == "llm"


def near_cut_threshold(item: dict, cut_min: float, margin: float = NEAR_THRESHOLD_MARGIN) -> bool:
    """CUT 신뢰도가 자동 적용 임계값 바로 아래/위 경계에 있는가 - 임계값 자체가 잘못 그어져 있다는
    신호가 여기서 반복되면 route_candidates.py의 CUT_CONFIDENCE_MIN 재조정 근거가 된다."""
    clf = item.get("llm_classification") or {}
    if clf.get("recommended_action") != "CUT":
        return False
    conf = clf.get("confidence")
    if conf is None:
        return False
    return abs(conf - cut_min) <= margin


def tag_item(item: dict, words: list[dict], cut_confidence_min: float) -> list[str]:
    """이 NG 후보에 적용되는 구조적 태그 전부. 태그가 없으면 빈 리스트 - 구조적 의심 탐지 대상이
    아니라는 뜻일 뿐, 아무 문제도 없다."""
    tags = []
    if boundary_followed_by_connective(item, words):
        tags.append("boundary_followed_by_connective")
    if source_llm_wide_scan(item):
        tags.append("source_llm_wide_scan")
    if near_cut_threshold(item, cut_confidence_min):
        tags.append("near_cut_threshold")
    return tags
