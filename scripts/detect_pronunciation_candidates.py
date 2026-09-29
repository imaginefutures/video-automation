"""발음 실수 탐지 (docs/미결-사항.md, 2026-09-29 착수) - 단어 유사도 기반 탐지가 구조적으로 못
잡는 case A(발음 실수 정정) 후보를 Scribe의 단어별 신뢰도(logprob)로 잡는다.

BS145 gold 대조에서 확인한 문제: "샐리그만→셀리그만", "속달변→숙달된"처럼 **틀린 발음과 맞는
발음이 텍스트로는 안 닮아서** `detect_ng_candidates.py`의 유사도 기반 탐지가 원리적으로 못 잡는다
(docs/현재-설계/검증-결과-BS145.md). 그런데 ASR은 이런 단어를 낮은 확신으로 전사한다 - BS145
실측(scripts/detect_pronunciation_candidates.py 개발 중 확인): "속달변" logprob=-0.39 vs
"숙달된" logprob=-0.0002, "샐리그만" logprob=-0.29/-0.15 vs "셀리그만" 대부분 -0.01 미만. 이
채널 전체 단어의 중앙값은 -0.00003으로 거의 확신 - **낮은 logprob 자체가 "이 단어는 잘 안 들렸거나
잘못 말해졌을 수 있다"는 신호**다.

임계값은 영상 전체 logprob 분포의 백분위(고정 절대값 아님) - 음향 게이트 재설계(QUIET_MARGIN_DB)
때와 같은 이유: 녹음 환경·화자마다 ASR 확신의 절대 수준이 다를 수 있어 상대 기준이 더 일반화된다.

결정론적 탐지일 뿐 - 실제로 이게 말실수 정정인지, 그냥 잡음 섞인 발화인지는 여느 NG 후보처럼
`classify_candidates.py`가 같은 케이스 체계(A~F)로 판정한다. 이 스크립트는 그 판정 대상을 하나
늘릴 뿐, 자체적으로 CUT/KEEP을 정하지 않는다(2.4 계획과 실행 분리).

edit/ng_candidates.json의 deleted_runs에 병합한다 - classify_candidates.py가 같은 배치로 판정.

Usage:
    python scripts/detect_pronunciation_candidates.py <videos/NAME>
"""
from __future__ import annotations
import argparse
import difflib
import json
from pathlib import Path

from common import video_dir, edit_dir, load_transcript, words_only, write_json, norm

LOGPROB_PERCENTILE = 3     # 이 영상 단어 전체 중 하위 N% 확신 - 절대값이 아니라 상대 기준
CLUSTER_GAP_WORDS = 2      # 이 안에서 낮은 확신 단어가 연속되면 하나의 후보로 묶음
MIN_WORD_LEN = 2           # 너무 짧은 단어(조사 등)는 확신이 원래 낮게 나오기 쉬워 제외
FOLLOW_PAD = 15


def percentile(values: list[float], p: float) -> float:
    s = sorted(values)
    idx = max(0, min(len(s) - 1, int(len(s) * p / 100)))
    return s[idx]


def already_covered(wi: int, covered: set[int]) -> bool:
    return wi in covered


def covered_word_indices(folder: Path) -> set[int]:
    """이미 다른 결정론적 탐지·화자 블록이 잡은 단어는 중복 보고하지 않는다."""
    covered: set[int] = set()
    cand_path = edit_dir(folder) / "ng_candidates.json"
    if cand_path.exists():
        for r in json.loads(cand_path.read_text()).get("deleted_runs", []):
            covered.update(range(r["raw_word_index_start"], r["raw_word_index_end"]))
    blocks_path = edit_dir(folder) / "speaker_blocks.json"
    if blocks_path.exists():
        for b in json.loads(blocks_path.read_text()).get("blocks", []):
            covered.update(range(b["wi_start"], b["wi_end"] + 1))
    return covered


def find_low_confidence_runs(words: list[dict], threshold: float, covered: set[int]) -> list[dict]:
    flagged = [w for w in words
               if w["logprob"] <= threshold and len(norm(w["text"])) >= MIN_WORD_LEN
               and not already_covered(w["wi"], covered)]
    if not flagged:
        return []
    runs, cur = [], [flagged[0]]
    for w in flagged[1:]:
        if w["wi"] - cur[-1]["wi"] <= CLUSTER_GAP_WORDS:
            cur.append(w)
        else:
            runs.append(cur)
            cur = [w]
    runs.append(cur)
    return runs


def build_candidates(folder: Path) -> list[dict]:
    words = words_only(load_transcript(folder))
    logprobs = [w["logprob"] for w in words]
    threshold = percentile(logprobs, LOGPROB_PERCENTILE)
    covered = covered_word_indices(folder)

    runs = find_low_confidence_runs(words, threshold, covered)
    print(f"logprob 임계값(하위 {LOGPROB_PERCENTILE}%): {threshold:.4f} - "
          f"낮은 확신 단어 클러스터 {len(runs)}개 (이미 다른 탐지가 잡은 곳 제외)")

    wmap = {w["wi"]: w for w in words}
    results = []
    for run_words in runs:
        i1, i2 = run_words[0]["wi"], run_words[-1]["wi"] + 1
        seg = [wmap[i] for i in range(i1, i2)]
        text = " ".join(w["text"] for w in seg)
        avg_lp = sum(w["logprob"] for w in run_words) / len(run_words)

        follow = [wmap[i] for i in range(i2, min(i2 + FOLLOW_PAD, len(words)))]
        follow_text = " ".join(w["text"] for w in follow)
        seg_norm = [norm(w["text"]) for w in seg]
        follow_norm = [norm(w["text"]) for w in follow]
        sim = difflib.SequenceMatcher(None, seg_norm, follow_norm, autojunk=False).ratio() if follow_norm else 0.0

        speakers = {w["speaker_id"] for w in seg}
        results.append({
            "raw_word_index_start": i1, "raw_word_index_end": i2,
            "follow_word_index_start": i2, "follow_word_index_end": i2 + len(follow),
            "start": seg[0]["start"], "end": seg[-1]["end"],
            "duration": round(seg[-1]["end"] - seg[0]["start"], 3),
            "n_words": len(seg), "deleted_text": text,
            "following_text_in_raw": follow_text, "similarity_to_following": round(sim, 3),
            "prefix_similarity": None,
            "dominant_speaker": next(iter(speakers)), "n_speakers_in_run": len(speakers),
            "has_word_fragment": any(w["text"].strip().endswith("--") for w in seg),
            "has_internal_repetition": False,
            "label": "LOW_CONFIDENCE_CANDIDATE",
            "reason": f"ASR 신뢰도 낮음(평균 logprob={avg_lp:.3f}, 영상 내 하위 {LOGPROB_PERCENTILE}%) - "
                      f"발음 실수·잘못 들림일 수 있어 판정 대상에 포함",
            "asr_logprob": round(avg_lp, 4),
        })
        print(f"  [{seg[0]['start']:.1f}s] logprob={avg_lp:.3f} :: {text}")
    return results


def detect(folder: Path) -> Path:
    cand_path = edit_dir(folder) / "ng_candidates.json"
    data = json.loads(cand_path.read_text()) if cand_path.exists() else {"deleted_runs": []}
    new_runs = build_candidates(folder)
    if new_runs:
        data["deleted_runs"].extend(new_runs)
        write_json(cand_path, data)
        print(f"{len(new_runs)}건을 {cand_path}에 병합함 (다음 classify 단계에서 함께 판정됨)")
    else:
        print("추가할 저확신 후보 없음")
    return cand_path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    detect(video_dir(args.folder))


if __name__ == "__main__":
    main()
