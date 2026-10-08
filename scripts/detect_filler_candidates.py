"""Standalone filler-word detection (PLAN.md §1 목표 "추임새 제거" 간극 메움, 12.1).

detect_ng_candidates.py만으로는 재시작 클러스터에 딸린 편집어만 잡히고, 클러스터 밖에서 단독으로
나오는 "음", "어", "아" 같은 필러는 아예 후보에 안 잡힌다. 이 스크립트가 그 빈 자리를 채운다.

결정론적, LLM 비용 없음. 의도적으로 보수적이다(2.4 "정상 발화는 절대 잘리지 않는다" — 자동화율보다
우선): 명백한 필러 3개(음/어/아)만 보고, 그나마도 Scribe가 쉼표·마침표로 따로 떼어 놓은 경우만
잡는다 — 이건 "이 단어가 독립된 짧은 발화처럼 들린다"는 신호를 ASR이 이미 준 것이나 마찬가지다.
"저"(그 사람 — 지시대명사)나 "네"(진짜 긍정 응답) 같은 단어는 필러로 흔히 오인되지만 일상 발화에서
실제 의미로도 매우 흔해 일부러 목록에서 뺐다 — 필러 하나 놓치는 비용보다 진짜 단어 하나 잘못 자르는
비용이 훨씬 크다(9.1: 오삭제 한 번이 신뢰를 무너뜨린다).

항상 REVIEW로만 라우팅한다(AUTO_SAFE 없음) — 필러는 화자의 말버릇일 수 있어 사람 확인이 먼저다.
case를 "FILLER"로 달아두는 것만으로 검토 화면의 패턴 제안(pattern_suggest.py)이 그대로 작동한다 —
같은 필러를 3번 연속 같은 방향으로 결정하면 자동으로 일반화를 제안받는다.

edit/ng.json을 그 자리에서 읽고 덧붙인다(whole_context_review.py와 같은 병합 방식) — NG
탐지·분류·라우팅이 끝난 뒤에 실행해야 같은 검토 큐에 합쳐진다.

Usage:
    python scripts/detect_filler_candidates.py <video-edit/NAME>
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from common import video_dir, edit_dir, load_transcript, words_only, write_json, norm

FILLER_VOCAB = {"음", "어", "아"}


def covered_word_indices(ng_items: list[dict], blocks: list[dict]) -> set[int]:
    covered: set[int] = set()
    for it in ng_items:
        covered.update(range(it["raw_word_index_start"], it["raw_word_index_end"]))
    for b in blocks:
        covered.update(range(b["wi_start"], b["wi_end"] + 1))
    return covered


def is_filler_token(raw_text: str) -> bool:
    """True only when Scribe itself segmented this word off with trailing punctuation
    ("음," / "어." / "아,") - the same cue that tells a human transcriber "this is its own
    little utterance", not a syllable fused into the next word."""
    stripped = raw_text.strip()
    if not stripped or stripped[-1] not in ",.":
        return False
    return norm(stripped) in FILLER_VOCAB


def detect(folder: Path) -> Path:
    words = words_only(load_transcript(folder))
    ng_path = edit_dir(folder) / "ng.json"
    ng_items = json.loads(ng_path.read_text()) if ng_path.exists() else []
    blocks_path = edit_dir(folder) / "speaker_blocks.json"
    blocks = json.loads(blocks_path.read_text())["blocks"] if blocks_path.exists() else []
    covered = covered_word_indices(ng_items, blocks)

    new_items = []
    for w in words:
        wi = w["wi"]
        if wi in covered or not is_filler_token(w["text"]):
            continue
        new_items.append({
            "raw_word_index_start": wi, "raw_word_index_end": wi + 1,
            "follow_word_index_start": wi + 1, "follow_word_index_end": wi + 1,
            "start": w["start"], "end": w["end"], "duration": round(w["end"] - w["start"], 3),
            "n_words": 1, "deleted_text": w["text"],
            "following_text_in_raw": "", "similarity_to_following": None, "prefix_similarity": None,
            "dominant_speaker": w.get("speaker_id"), "n_speakers_in_run": 1,
            "has_word_fragment": False, "has_internal_repetition": False,
            "label": "FILLER_CANDIDATE",
            "route": "CUT", "flag": "restore",  # 최대 삭제(2026-09-29): 말버릇일 수 있어 복원 후보로 자름
            "route_reason": f"단독 필러 후보('{w['text'].strip()}') - 말버릇일 수 있어 복원 후보. 반복되면 패턴 제안으로 일반화 가능",
            "llm_classification": {"case": "FILLER", "recommended_action": "CUT",
                                   "confidence": 0.6, "reasoning": "쉼표/마침표로 분리된 단독 필러"},
        })
        print(f"  [{w['start']:.1f}s] filler candidate :: {w['text']}")

    print(f"found {len(new_items)} standalone filler candidate(s)")
    if new_items:
        ng_items.extend(new_items)
        write_json(ng_path, ng_items)
        print(f"appended to {ng_path}")
    return ng_path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    detect(video_dir(args.folder))


if __name__ == "__main__":
    main()
