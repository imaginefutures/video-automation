"""주제별 분할 2단계 - 강의를 여러 편으로 나눌 경계를 제안한다 (docs/백로그/주제별-분할.md).

원본 전체를 빈틈·겹침 없이 N편으로 나눈다. LLM에게는 "각 편의 마지막 문장 번호"만 받는다 -
시작은 앞 편 끝 다음 문장으로 자동으로 정해지므로 빈틈·겹침이 구조적으로 생길 수 없다.

LLM 출력이 규칙(번호 증가, 범위 안)을 어기면 1회 다시 묻고, 그래도 어기거나 --no-llm이면
쉼 길이만 보는 결정론적 분할로 대체한다 (R8: LLM 실패해도 멈추지 않는다).

Writes <folder>/work/segments.json (제안 원본 - 사용자 수정은 split_decisions.json에 따로).

Usage:
    python scripts/propose_segments.py <auto-split/NAME> [--min-minutes 3] [--max-minutes 10] [--no-llm]
"""
from __future__ import annotations
import argparse
from pathlib import Path

from pydantic import BaseModel

from common import load_env, edit_dir, write_json, thinking_kwargs, log_llm_usage
from split_sentences import load_sentences

MAKER_MODEL = "claude-opus-5-5"   # 전체 강의를 한 번에 읽고 구조를 잡는 판단 - detect_regions.py와 같은 급
DEFAULT_MIN_MIN = 3.0
DEFAULT_MAX_MIN = 10.0


# --------------------------------------------------------------------------------- 구간 계산 (화면·내보내기 공용)

def cut_time(sents: list[dict], k: int, amap: dict | None) -> float:
    """k번째 문장과 k+1번째 문장 사이에서 실제로 자를 시각 = 그 쉼 안의 가장 조용한 지점.
    쉼이 거의 없으면(말이 붙어 있으면) 앞 문장 끝."""
    end, nxt = sents[k]["end"], sents[k + 1]["start"]
    if nxt - end <= 0.02:
        return round(end, 3)
    if amap:
        from audio_map import min_energy_in
        return min_energy_in(amap, end, nxt)[0]
    return round((end + nxt) / 2, 3)


def segments_from_ends(ends: list[int], sents: list[dict], duration: float, amap: dict | None,
                       refined: dict | None = None) -> list[dict]:
    """편별 끝 문장 번호 → 편 목록. 1편은 0초부터, 마지막 편은 영상 끝까지 - 이어 붙이면 원본.
    refined(split_refine.py 캐시)에 그 경계가 있으면 화면 신호로 다듬은 시각을 쓰고, 없으면 소리 기준.
    cut_reason: 그 편의 끝 경계를 무엇에 맞췄는지 (black/scene/caption/audio, 아직 계산 전이면 pending)."""
    out, start_sent, start_t = [], 0, 0.0
    for n, e in enumerate(ends):
        last = e == len(sents) - 1
        r = (refined or {}).get(str(e))
        end_t = duration if last else (r["t"] if r else cut_time(sents, e, amap))
        reason = None if last else (r["reason"] if r else ("pending" if refined is not None else "audio"))
        out.append({"n": n + 1, "start_sent": start_sent, "end_sent": e, "cut_reason": reason,
                    "start": round(start_t, 4), "end": round(end_t, 4), "duration": round(end_t - start_t, 3)})
        start_sent, start_t = e + 1, end_t
    return out


def valid_ends(ends: list[int], n_sents: int) -> bool:
    return bool(ends) and all(0 <= e < n_sents for e in ends) and all(a < b for a, b in zip(ends, ends[1:]))


# --------------------------------------------------------------------------------- 결정론적 분할 (대체 경로)

def fallback_ends(sents: list[dict], duration: float, lo: float, hi: float) -> list[int]:
    """쉼 길이만 본다: 목표 길이 범위 안에서 끝낼 수 있는 문장 중 뒤 쉼이 가장 긴 곳에서 끊는다."""
    ends, start_t, k0 = [], 0.0, 0
    while duration - start_t > hi:
        cands = [k for k in range(k0, len(sents) - 1) if lo <= sents[k]["end"] - start_t <= hi]
        if not cands:  # 범위 안에 문장 끝이 없으면(한 문장이 너무 길면) 목표 중간에 가장 가까운 곳
            mid = start_t + (lo + hi) / 2
            cands = [min(range(k0, len(sents) - 1), key=lambda k: abs(sents[k]["end"] - mid))]
        k = max(cands, key=lambda k: sents[k]["gap_after"])
        ends.append(k)
        start_t, k0 = sents[k + 1]["start"], k + 1
        if k0 >= len(sents) - 1:
            break
    ends.append(len(sents) - 1)
    return sorted(set(ends))


# --------------------------------------------------------------------------------- LLM

class SegmentPlan(BaseModel):
    end_sent: int
    title: str
    summary: str
    reason: str


class Proposal(BaseModel):
    segments: list[SegmentPlan]


SYSTEM = """너는 강의 영상 편집자다. 한 편으로는 너무 길어 지루한 강의를 여러 편의 짧은 강의로 나눈다.

반드시 지킬 것:
- 순서는 바꾸지 않고, 원본 전체를 빈틈없이 나눈다. 버리는 부분은 없다.
- 경계는 문장 끝에만 생긴다. 각 편의 마지막 문장 번호(end_sent)를 순서대로 답한다. 마지막 편의 end_sent는 반드시 맨 마지막 문장 번호다.
- 각 편은 주제 하나를 처음부터 끝까지 다뤄서, 그 편만 본 시청자도 이해할 수 있어야 한다.

좋은 경계:
- 새 편의 첫 문장은 앞 편을 몰라도 이해되는 문장이다. "그래서", "그럼", "아까 말씀드린", "이것도"나 가리키는 대상이 앞 편에 있는 "이/그" 지시어로 시작하는 문장에서 새 편을 시작하지 않는다.
- 편의 끝은 그 주제의 결론이나 정리다. "다음으로는…", "이제 …를 알아볼게요" 같은 다음 주제 예고 문장은 다음 편의 첫머리에 붙인다 (예고가 다음 편의 도입 역할을 한다).
- 인사·채널 소개는 1편에, 맺음말·구독 안내는 마지막 편에 포함한다.
- 각 문장 앞의 시각으로 길이를 계산한다. 목표 길이 범위를 지키되, 주제가 자연스럽게 끝나는 지점이 길이보다 우선이다. 범위를 벗어나야 하면 reason에 이유를 적는다.

각 편마다:
- title: 시청자가 그 편에서 무엇을 배우는지 드러나는 강의 제목, 20자 이내
- summary: 1~2문장 요약
- reason: 왜 여기서 끊었는지 (끝 문장과 다음 편 첫 문장의 역할)"""


def fmt_t(t: float) -> str:
    return f"{int(t // 60):02d}:{int(t % 60):02d}"


def build_doc(sents: list[dict], duration: float, lo: float, hi: float) -> str:
    lines = [f"전체 길이 {fmt_t(duration)}, 문장 {len(sents)}개 (번호 0~{len(sents) - 1}). "
             f"목표: 한 편 {lo / 60:g}~{hi / 60:g}분.", ""]
    for s in sents:
        pause = f" (쉼 {s['gap_after']:.1f}초)" if s["gap_after"] >= 1.0 else ""
        lines.append(f"[{s['i']}] {fmt_t(s['start'])} {s['text']}{pause}")
    return "\n".join(lines)


def ask_llm(folder: Path, doc: str, n_sents: int) -> list[SegmentPlan] | None:
    import anthropic
    client = anthropic.Anthropic()
    msg = doc
    for attempt in range(2):
        try:
            resp = client.messages.parse(model=MAKER_MODEL, max_tokens=16000, system=SYSTEM,
                                         messages=[{"role": "user", "content": msg}],
                                         output_format=Proposal, **thinking_kwargs(MAKER_MODEL, effort="high"))
        except Exception as e:  # noqa: BLE001 - 어떤 실패든 결정론적 분할로 넘어간다
            print(f"LLM 호출 실패: {e}")
            return None
        log_llm_usage(folder, "propose_segments", MAKER_MODEL, resp.usage)
        plans = resp.parsed_output.segments
        ends = [p.end_sent for p in plans]
        if plans and ends[-1] != n_sents - 1 and valid_ends(ends, n_sents):
            # 마지막 편이 끝까지 안 갔으면 남은 꼬리(대개 아웃트로)를 마지막 편에 붙인다
            print(f"마지막 편 끝({ends[-1]})을 마지막 문장({n_sents - 1})까지 늘림")
            plans[-1].end_sent = n_sents - 1
            ends[-1] = n_sents - 1
        if valid_ends(ends, n_sents):
            return plans
        print(f"LLM 출력이 규칙을 어김 (시도 {attempt + 1}): {ends}")
        msg = (doc + f"\n\n주의: 직전 답 {ends}은 규칙을 어겼다. end_sent는 0~{n_sents - 1} 범위에서 "
               f"엄격히 증가해야 하고 마지막은 {n_sents - 1}이어야 한다.")
    return None


# --------------------------------------------------------------------------------- 제목 다시 짓기

TITLE_MODEL = MAKER_MODEL


class TitleItem(BaseModel):
    n: int
    title: str


class Titles(BaseModel):
    titles: list[TitleItem]


TITLE_SYSTEM = """너는 강의 영상 편집자다. 긴 강의를 여러 편으로 나눴고, 각 편의 대본이 주어진다.
각 편의 강의 제목을 짓는다.

- 시청자가 그 편에서 무엇을 배우는지 드러나게 쓴다 (예: "수면 퇴행은 왜 생기나", "칭찬이 자존감을 못 키우는 이유")
- 20자 이내
- 편끼리 겹치지 않게, 제목만 봐도 서로 구분되게
- 그 편 대본에 실제로 있는 내용만. 대본에 없는 약속·과장·낚시 표현 금지
- 편 번호, 이모지, 따옴표 넣지 않기"""


def retitle(folder: Path, seg_texts: list[str]) -> list[str]:
    """분할 화면의 "제목 자동 작성" - 사용자가 편집을 끝낸 경계·대본 기준으로 모든 편의 제목을 다시 짓는다."""
    import anthropic
    load_env()
    doc = "\n\n".join(f"=== {n}편 ===\n{t}" for n, t in enumerate(seg_texts, 1))
    resp = anthropic.Anthropic().messages.parse(
        model=TITLE_MODEL, max_tokens=8000, system=TITLE_SYSTEM,
        messages=[{"role": "user", "content": doc}], output_format=Titles,
        **thinking_kwargs(TITLE_MODEL, effort="low"))
    log_llm_usage(folder, "retitle", TITLE_MODEL, resp.usage)
    by_n = {t.n: t.title.strip().strip('"\'') for t in resp.parsed_output.titles}
    if len(by_n) != len(seg_texts) or any(not by_n.get(n) for n in range(1, len(seg_texts) + 1)):
        raise ValueError("제목을 일부 편에 대해 받지 못했습니다 - 다시 시도하세요")
    return [by_n[n][:80] for n in range(1, len(seg_texts) + 1)]


# --------------------------------------------------------------------------------- main

def propose(folder: Path, min_min: float = DEFAULT_MIN_MIN, max_min: float = DEFAULT_MAX_MIN,
            use_llm: bool = True) -> Path:
    from audio_map import load_audio_map
    data = load_sentences(folder)
    sents, duration = data["sentences"], data["duration"]
    lo, hi = min_min * 60, max_min * 60
    amap = load_audio_map(folder)

    plans = None
    if use_llm:
        load_env()
        print(f"구간 제안: 문장 {len(sents)}개 ({MAKER_MODEL})")
        plans = ask_llm(folder, build_doc(sents, duration, lo, hi), len(sents))

    if plans:
        method = "llm"
        ends = [p.end_sent for p in plans]
        meta = [{"title": p.title, "summary": p.summary, "reason": p.reason} for p in plans]
    else:
        method = "fallback"
        print("결정론적 분할 사용 (쉼 길이 기준)")
        ends = fallback_ends(sents, duration, lo, hi)
        meta = [{"title": f"{n + 1}편", "summary": "", "reason": "쉼 길이 기준 자동 분할"} for n in range(len(ends))]

    segs = segments_from_ends(ends, sents, duration, amap)
    for seg, m in zip(segs, meta):
        seg.update(m)
        seg["length_ok"] = lo <= seg["duration"] <= hi

    out = edit_dir(folder) / "segments.json"
    write_json(out, {"method": method, "model": MAKER_MODEL if method == "llm" else None,
                     "min_minutes": min_min, "max_minutes": max_min, "segments": segs})
    print(f"wrote {out} ({len(segs)}편, {method})")
    for s in segs:
        flag = "" if s["length_ok"] else "  ← 길이 범위 밖"
        print(f"  {s['n']:2d}. {fmt_t(s['start'])}~{fmt_t(s['end'])} ({s['duration'] / 60:.1f}분) "
              f"{s['title']}{flag}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--min-minutes", type=float, default=DEFAULT_MIN_MIN)
    ap.add_argument("--max-minutes", type=float, default=DEFAULT_MAX_MIN)
    ap.add_argument("--no-llm", action="store_true", help="쉼 길이 기준 결정론적 분할만")
    args = ap.parse_args()
    propose(Path(args.folder).resolve(), args.min_minutes, args.max_minutes, use_llm=not args.no_llm)


if __name__ == "__main__":
    main()
