"""Seam-level partial loop (docs/기획/02-품질-루프.md 2장) - replaces self_critique.py.

For every draft cut span (assemble_draft.py's output):

  1. **대안 생성** (결정론): 원안 + 앞/뒤 한 단어씩 축소·확장한 대안들. 각 대안의 경계는
     audio_map.py로 실제 쉼(gap) 안의 조용한 지점을 찾아 정한다(옛 15ms 고정 패딩 대신) - 그
     경계가 발화 중이면(조용한 지점을 못 찾으면) 15ms 패딩으로 안전하게 되돌아간다. 이 단계에서
     이미 "말소리 걸침"(G1)과 "숨소리 반토막"(G3)을 거른다.
  2. **G2 재전사 잔여음 검사** (결정론+Scribe, LLM 아님): 각 컷이 최종 선택된 뒤, 그 경계로
     실제 이어붙인 오디오(앞 4단어+뒤 4단어)를 렌더링해 다시 전사하고, 기대 단어 수와 비교한다.
     여러 이음새를 하나의 오디오로 묶어 Scribe 호출 1회로 처리한다.
  3. **내용 판정** (LLM, judge != maker): 통과한 대안들 중에서 문법·중복·지시어·정보손실을
     확인한다. 관문(G1/G3)만 통과했다고 다 판정하지 않는다 - 조용해도 내용이 이상할 수 있다.
  4. **선택**: 관문+판정을 모두 통과한 대안 중 **가장 많이 지우는 것**을 고른다(최대 삭제 방침).
     하나도 못 넘으면 원안으로 되돌아가 flag만 붙인다 - 컷 자체를 취소하지 않는다.
  5. **재투입** (최대 3회): 어떤 컷의 경계나 flag가 바뀌면, 그 앞뒤에 붙은 이음새는 문맥이
     바뀐 것이므로 패킷을 다시 만들어 재판정한다. 바뀐 게 없으면 그 자리에서 멈춘다.

A cut is never fully cancelled - failing every check keeps the content and flags it as a
"삭제 후보"(flag=delete) instead, so nothing silently disappears either way (최대 삭제 방침,
서비스-개요와-철학.md 원칙 4).

2026-09-29 2차 구현 - "축소분 제대로 구현해" 반영: 대안 탐색(위 1,4)·G2(2)·재투입(5) 전부 새로
구현. 알려진 축소(디스클로즈): G2는 최종 선택된 대안 하나에만 돈다(대안마다 돌면 Scribe 호출이
대안 수만큼 늘어나 비용·시간이 커짐) - 선택 자체는 G1/G3+judge만으로 하고, G2는 그 위에 얹는
마지막 안전망이다.

Writes <folder>/edit/seams.json (이음새별 최종 선택 + 판정 근거) and
<folder>/edit/final_cuts.json (the refined cut spans build_edl.py actually applies).

Usage:
    python scripts/seam_refine.py <videos/NAME> [--max-rounds 3]
"""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel

from common import (load_env, video_dir, edit_dir, load_transcript, words_only, write_json, source_media, norm,
                    trace_to_ng_indices, apply_flag_to_ng, thinking_kwargs)
import audio_map as am
from plan_pauses import PRESETS
from transcribe import call_scribe

CONTEXT_PAD_WORDS = 12
JUDGE_BATCH = 20
G2_WORDS_EACH_SIDE = 4          # 재전사 검사에 쓸 경계 앞뒤 단어 수
G2_WORD_COUNT_TOLERANCE = 1     # 기대 단어 수 대비 이 이상 차이나면 잔여음/절단 의심

# 2026-10-01 (docs/기획/02-품질-루프.md 2.5절, 남은-개발.md "부분 루프 점수 시스템"): 선택은
# 여전히 "가장 많이 지우는 대안" 우선이다(02 문서 2.6절 2번, 최대 삭제 방침) - 점수는 삭제량이
# 같은 대안끼리 묶였을 때만 쓰는 타이브레이커다. 그러니 이 점수 시스템은 접속사 삼킴류의 "한
# 단어 더 지우면 clean으로 통과하는" 문제 자체는 못 막는다 - 그건 route_candidates.py의 즉시
# 안전망(flag)과 info_lost 기반 flag 상향(아래 select_alt)이 담당한다. 이 점수가 실제로 효과를
# 내는 지점은 "삭제량이 같은 여러 대안 중 더 자연스러운 쪽 고르기"(예: 확장 1단어 vs 흡수 1단어가
# 똑같이 1단어를 추가로 지울 때, 음향·리듬이 더 매끄러운 쪽)와 진동 감지 시 "어느 쪽에 고정할지"다.
ACOUSTIC_WEIGHT = 0.4
CONTENT_WEIGHT = 0.4   # clean 필터(C1~C3 전부 통과)를 통과한 대안에만 이미 적용됨 - 늘 0.4
RHYTHM_WEIGHT = 0.2
RHYTHM_TARGET_SEC = PRESETS["NORMAL_INTER"]["target"]   # 0.25s - 문맥별 목표치(무음-리듬.md)가
# 아직 이음새 단위로 안 들어와 있어 일반 문맥 목표로 근사한다. 진짜 문맥별 목표는 "무음-리듬
# 재설계"(남은-개발.md)가 끝나야 가능.
RHYTHM_FALLOFF_SEC = 0.5        # 목표치에서 이만큼 벗어나면 리듬 점수 0

# 02 문서 2.3절 "잔여 조각 흡수" - 컷 바로 옆의 추임새·비전사 소리·2음절 이하 조각까지 포함하는
# 대안. 단순 expand_*(한 단어만 확장)와 달리 조건을 만족하는 한 여러 단어를 연속으로 삼킨다.
ABSORB_FILLER_VOCAB = {"음", "어", "아", "그", "저", "뭐", "그니까", "이제"}
ABSORB_MAX_SYLLABLES = 2
ABSORB_MAX_WORDS = 3            # 무한정 삼키지 않도록 상한


def _is_absorbable(text: str) -> bool:
    t = norm(text)
    return t in ABSORB_FILLER_VOCAB or len(t) <= ABSORB_MAX_SYLLABLES

# 경계 계산(quiet-snap vs flat pad, G1/G3 겸용)은 audio_map.choose_boundary로 이동 (2026-09-29) -
# server.py의 cut_spans()도 같은 구현을 쓴다.
choose_boundary = am.choose_boundary


# --------------------------------------------------------------------------------- 대안 생성

def _absorb_start(wi_s: int, prev_end: int, words: list[dict]) -> int:
    """wi_s 바로 앞쪽으로, 흡수 가능한(필러·짧은 조각) 단어가 연속되는 한 경계를 당긴다."""
    i = wi_s
    consumed = 0
    while i - 1 >= prev_end and consumed < ABSORB_MAX_WORDS and _is_absorbable(words[i - 1]["text"]):
        i -= 1
        consumed += 1
    return i


def _absorb_end(wi_e: int, next_start: int, words: list[dict]) -> int:
    i = wi_e
    consumed = 0
    while i < next_start and consumed < ABSORB_MAX_WORDS and _is_absorbable(words[i]["text"]):
        i += 1
        consumed += 1
    return i


def gen_alternatives(wi_s: int, wi_e: int, prev_end: int, next_start: int,
                     words: list[dict] | None = None) -> list[tuple[str, int, int]]:
    alts = [("original", wi_s, wi_e)]
    if wi_s + 1 < wi_e:
        alts.append(("shrink_start", wi_s + 1, wi_e))
    if wi_e - 1 > wi_s:
        alts.append(("shrink_end", wi_s, wi_e - 1))
    if wi_s - 1 >= prev_end:
        alts.append(("expand_start", wi_s - 1, wi_e))
    if wi_e + 1 <= next_start:
        alts.append(("expand_end", wi_s, wi_e + 1))
    if words is not None:
        absorbed_s = _absorb_start(wi_s, prev_end, words)
        if absorbed_s < wi_s:
            alts.append(("absorb_start", absorbed_s, wi_e))
        absorbed_e = _absorb_end(wi_e, next_start, words)
        if absorbed_e > wi_e:
            alts.append(("absorb_end", wi_s, absorbed_e))
    return alts


def compute_neighbor_bounds(cuts_sorted: list[dict], idx: int, n_words: int) -> tuple[int, int]:
    prev_end = cuts_sorted[idx - 1]["wi_end"] if idx > 0 else 0
    next_start = cuts_sorted[idx + 1]["wi_start"] if idx + 1 < len(cuts_sorted) else n_words
    return prev_end, next_start


# --------------------------------------------------------------------------------- 패킷 + 판정

def build_packet(words: list[dict], wi_s: int, wi_e: int) -> dict:
    before = " ".join(w["text"] for w in words[max(0, wi_s - CONTEXT_PAD_WORDS):wi_s])
    removed = " ".join(w["text"] for w in words[wi_s:wi_e])
    if len(removed) > 200:
        parts = removed.split()
        removed = " ".join(parts[:15]) + " … " + " ".join(parts[-15:]) + f" (총 {len(parts)}단어)"
    after = " ".join(w["text"] for w in words[wi_e:wi_e + CONTEXT_PAD_WORDS])
    return {"before": before, "removed": removed, "after": after}


class AltJudgment(BaseModel):
    cut_id: int
    alt: str
    grammar_ok: bool
    duplicate_left: bool
    reference_broken: bool
    info_lost: Literal["none", "minor", "major"]
    note: str


class AltJudgments(BaseModel):
    judgments: list[AltJudgment]


JUDGE_SYSTEM = """\
너는 한국어 강의 영상의 편집 결과를 검증하는 두 번째 편집자다. 다른 편집자(또는 규칙)가 이미
어떤 구간을 잘라내기로 정했고, 경계를 조금씩 다르게 잡은 대안이 여럿 있다 - 각 대안에 대해
"이렇게 자른 결과가 자연스러운가"를 판정하라.

각 (seam, 대안)마다 앞 문맥, 잘린 부분(참고용), 뒤 문맥이 주어진다. "앞 문맥 다음에 뒤 문맥이
바로 이어진다"고 가정하고 판정하라.

- grammar_ok: 앞 문맥 + 뒤 문맥이 문법적으로 자연스럽게 이어지는가
- duplicate_left: 잘린 부분에서 시도한 같은 말이 뒤 문맥에도 남아있어 결과가 같은 말을 두 번
  하는 것처럼 보이는가
- reference_broken: 앞 문맥의 지시어가 가리키던 대상이 잘린 부분에 있었고 뒤 문맥에는 없어서
  결과가 무엇을 가리키는지 알 수 없게 되는가
- info_lost: 잘린 부분에만 있던 정보(새 사실·수치·예시·조건)가 사라지는가 (none/minor/major)
- note: 한국어 한 문장 근거

모든 (cut_id, alt) 조합에 정확히 하나씩 답하라.
"""


def build_judge_prompt(items: list[dict]) -> str:
    blocks = []
    for it in items:
        p = it["packet"]
        blocks.append(f"[cut {it['cut_id']} alt={it['alt']}] (원본 생성: {it['made_by']})\n"
                       f"앞 문맥: …{p['before']}\n잘린 부분(참고용): {p['removed']}\n뒤 문맥: {p['after']}…")
    return "\n\n".join(blocks)


def judge_batch(client, model: str, items: list[dict]) -> dict[tuple[int, str], AltJudgment]:
    out: dict[tuple[int, str], AltJudgment] = {}
    for k in range(0, len(items), JUDGE_BATCH):
        part = items[k:k + JUDGE_BATCH]
        resp = client.messages.parse(model=model, max_tokens=8000, system=JUDGE_SYSTEM,
                                     messages=[{"role": "user", "content": build_judge_prompt(part)}],
                                     output_format=AltJudgments, **thinking_kwargs(model))
        for j in resp.parsed_output.judgments:
            out[(j.cut_id, j.alt)] = j
    return out


JUDGE_FOR = {"claude-sonnet-5": "claude-opus-5-5", "claude-opus-5-5": "claude-sonnet-5"}


def judge_model_for(made_by: str) -> str:
    return JUDGE_FOR.get(made_by, "claude-sonnet-5")


# --------------------------------------------------------------------------------- G2 재전사

def render_seam_clip(media: Path, out_wav: Path, s0: float, s1: float, e0: float, e1: float) -> None:
    """[s0,s1](경계 직전 유지 구간) + [e0,e1](경계 직후 유지 구간)을 이어붙인다 - 실제 편집
    결과가 이 경계에서 어떻게 들릴지 그대로 재현."""
    subprocess.run([
        "ffmpeg", "-y", "-ss", f"{s0:.3f}", "-to", f"{s1:.3f}", "-i", str(media),
        "-ss", f"{e0:.3f}", "-to", f"{e1:.3f}", "-i", str(media),
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
        "-map", "[out]", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(out_wav),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def g2_check(media: Path, selections: list[dict], api_key: str) -> dict:
    """selections: [{id, start, end, before_ws, after_ws}, ...] - 최종 선택된 경계와 그 앞/뒤
    문맥 단어(list[dict], 이미 잘라서 넘김 - 알고리즘 이음새라면 단어 인덱스로, 여러 종류가 섞인
    임의의 컷 경계라면 시간창으로 고르는 등 호출자마다 방식이 다를 수 있어 여기서 고정하지 않음).
    전부 이어붙여 Scribe 호출 1회로 처리한다. 반환: id -> {ok, expected, got, note}"""
    if not selections or not api_key:
        return {}
    gap_sec = 1.0
    results: dict = {}

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        clips_info = []
        for sel in selections:
            before_ws, after_ws = sel["before_ws"], sel["after_ws"]
            if not before_ws or not after_ws:
                continue  # 영상 맨 앞/끝이라 한쪽 문맥이 없음 - G2 대상에서 제외
            s0, s1 = before_ws[0]["start"], sel["start"]
            e0, e1 = sel["end"], after_ws[-1]["end"]
            if s1 <= s0 or e1 <= e0:
                continue
            clip = tmp / f"seam_{sel['id']}.wav"
            try:
                render_seam_clip(media, clip, s0, s1, e0, e1)
            except subprocess.CalledProcessError:
                continue
            expected = len(before_ws) + len(after_ws)
            clips_info.append({"id": sel["id"], "clip": clip, "expected": expected})

        if not clips_info:
            return {}

        # 무음 파일 하나 만들고 클립 사이사이에 끼워 이어붙인다 - 이후 결과 단어의 시간으로
        # 어느 클립 소속인지 구간을 나눈다
        silence = tmp / "silence.wav"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=16000:cl=mono",
                        "-t", f"{gap_sec}", "-c:a", "pcm_s16le", str(silence)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        filelist = tmp / "list.txt"
        offsets = []
        cursor = 0.0
        lines = []
        for i, ci in enumerate(clips_info):
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                        "-of", "csv=p=0", str(ci["clip"])],
                                       capture_output=True, text=True).stdout.strip() or 0)
            offsets.append((ci["id"], cursor, cursor + dur, ci["expected"]))
            lines.append(f"file '{ci['clip']}'")
            cursor += dur
            if i < len(clips_info) - 1:
                lines.append(f"file '{silence}'")
                cursor += gap_sec
        filelist.write_text("\n".join(lines))

        combined = tmp / "combined.wav"
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(filelist),
                        "-c", "copy", str(combined)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"G2: {len(clips_info)}개 경계를 하나의 오디오({cursor:.0f}s)로 묶어 재전사 중...")
        payload = call_scribe(combined, api_key, "kor", None)
        got_words = [w for w in payload.get("words", []) if w.get("type") == "word"]

        for id_, o_start, o_end, expected in offsets:
            in_range = sum(1 for w in got_words if o_start - 0.1 <= w["start"] < o_end + 0.1)
            diff = in_range - expected
            ok = abs(diff) <= G2_WORD_COUNT_TOLERANCE
            results[id_] = {"ok": ok, "expected": expected, "got": in_range,
                            "note": ("정상" if ok else
                                     f"기대 {expected}단어인데 {in_range}단어 전사됨 - "
                                     f"{'잔여음 의심(더 많이 들림)' if diff > 0 else '절단 의심(덜 들림)'}")}
    return results


# --------------------------------------------------------------------------------- 한 번의 판정 라운드

def evaluate_seam(amap, words, duration, wi_s, wi_e, prev_end, next_start, made_by, cut_id
                  ) -> tuple[list[dict], list[dict]]:
    """이 이음새의 모든 대안을 만들고 경계를 계산한다. 판정 대상(judge_items)과 대안 목록을
    반환 - 실제 judge 호출은 여러 이음새를 모아 배치로 하므로 여기선 준비만 한다."""
    alts = []
    for name, a_s, a_e in gen_alternatives(wi_s, wi_e, prev_end, next_start, words):
        b = choose_boundary(amap, words, a_s, a_e, duration)
        alts.append({"alt": name, "wi_start": a_s, "wi_end": a_e, **b,
                     "packet": build_packet(words, a_s, a_e)})
    judge_items = [{"cut_id": cut_id, "alt": a["alt"], "made_by": made_by, "packet": a["packet"]}
                   for a in alts]
    return alts, judge_items


def acoustic_continuity_score(alt: dict) -> float:
    """0~1. audio_ok=False(조용한 지점을 못 찾음)면 0 - 이런 대안은 애초에 clean 후보에서
    빠지지만(select_alt), 점수 함수 자체는 방어적으로 둔다. quiet_snap(실제 무음 지점을 찾음)이
    flat pad(안전하게 돌아간 추정치)보다 낫다고 본다."""
    if not alt.get("audio_ok"):
        return 0.0
    return 1.0 if alt.get("method") == "quiet_snap" else 0.7


def rhythm_score(alt: dict, words: list[dict]) -> float:
    """0~1. 이 대안을 택했을 때 결과물에 남는 이음새 쉼(컷 양옆에서 남는 두 조각의 합)이
    일반 문맥 목표치(RHYTHM_TARGET_SEC)에 가까울수록 높다. 문맥별(나열/인용 등) 목표는
    무음-리듬.md 재설계 전까지는 반영 안 됨 - 일반 목표로 근사."""
    a_s, a_e = alt["wi_start"], alt["wi_end"]
    pause = 0.0
    has_ref = False
    if a_s > 0:
        pause += max(0.0, alt["start"] - words[a_s - 1]["end"])
        has_ref = True
    if a_e < len(words):
        pause += max(0.0, words[a_e]["start"] - alt["end"])
        has_ref = True
    if not has_ref:
        return 1.0  # 영상 맨 앞/끝 - 비교할 이웃이 없음, 감점하지 않음
    return max(0.0, 1.0 - abs(pause - RHYTHM_TARGET_SEC) / RHYTHM_FALLOFF_SEC)


def composite_score(alt: dict, words: list[dict]) -> float:
    """02 문서 2.5절 가중합 - 문장 연결(C1~C3)은 clean 필터를 통과한 대안에 한해 늘 만점(0.4)이다
    (실패하면애초에 clean에 안 들어옴)."""
    return (CONTENT_WEIGHT
            + ACOUSTIC_WEIGHT * acoustic_continuity_score(alt)
            + RHYTHM_WEIGHT * rhythm_score(alt, words))


def select_alt(alts: list[dict], judgments: dict[tuple[int, str], AltJudgment], cut_id: int,
               base_flag: str | None, base_reason: str | None, words: list[dict]) -> tuple[dict, str | None, str | None]:
    clean, dirty = [], []
    for a in alts:
        j = judgments.get((cut_id, a["alt"]))
        if j is None:
            continue
        a["_judgment"] = j
        if a["audio_ok"] is False:
            dirty.append(a)  # 관문 미통과 - clean 후보에서 제외
            continue
        if j.grammar_ok and not j.duplicate_left and not j.reference_broken:
            clean.append(a)
        else:
            dirty.append(a)

    reasons = [base_reason] if base_reason else []
    if clean:
        # 02 문서 2.6절 2번: 가장 많이 지우는 대안이 우선, 삭제량이 같으면 점수(2.5절)로 고른다.
        chosen = max(clean, key=lambda a: (a["wi_end"] - a["wi_start"], composite_score(a, words)))
        flag = base_flag
        j = chosen["_judgment"]
        if j.info_lost != "none":
            flag = "restore"
            reasons.append(f"이음새 판정({chosen['alt']}): 정보 손실 가능성({j.info_lost}) - {j.note}")
        elif chosen["alt"] != "original":
            reasons.append(f"경계를 {chosen['alt']}로 조정함")
        return chosen, flag, "; ".join(reasons) or None

    original = next((a for a in alts if a["alt"] == "original"), alts[0])
    if dirty:
        best_dirty = min(dirty, key=lambda a: (a["audio_ok"] is False,
                         sum(getattr(a.get("_judgment"), k, False) for k in
                             ("duplicate_left", "reference_broken")) if a.get("_judgment") else 9))
        j = best_dirty.get("_judgment")
        reasons.append(f"이음새 판정 실패(대안 {best_dirty['alt']} 시도): "
                       f"{j.note if j else '경계 근처 조용한 지점 없음'}")
        return best_dirty, "restore", "; ".join(reasons)

    reasons.append("모든 대안이 판정 대상에서 제외됨(응답 누락) - 원안 유지, 확인 필요")
    return original, "restore", "; ".join(reasons)


# --------------------------------------------------------------------------------- main

def refine(folder: Path, max_rounds: int = 3) -> Path:
    load_env()
    import anthropic
    import os

    words = words_only(load_transcript(folder))
    transcript = load_transcript(folder)
    duration = float(transcript.get("audio_duration_secs") or words[-1]["end"])
    draft = json.loads((edit_dir(folder) / "draft_cuts.json").read_text())
    cuts = sorted(draft["cuts"], key=lambda c: c["wi_start"])
    ng_path = edit_dir(folder) / "ng.json"
    ng_items = json.loads(ng_path.read_text()) if ng_path.exists() else []
    amap = am.load_audio_map(folder)
    if not amap:
        print("WARNING: no audio_map.json - boundaries fall back to the plain 15ms pad for every cut")

    client = anthropic.Anthropic()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")

    # 이음새별 현재 상태 (라운드 사이 유지). `seen`은 02 문서 2.7절 진동 감지용 - 이 이음새가
    # 지금까지 거쳐온 (wi_start, wi_end) 조합을 전부 기록해, 전에 봤던 조합으로 되돌아오면(A->B->A)
    # 진동으로 보고 점수 높은 쪽에 고정한다.
    state = {c["id"]: {"wi_start": c["wi_start"], "wi_end": c["wi_end"], "made_by": c["made_by"],
                       "flag": c.get("flag"), "flag_reason": c.get("flag_reason"),
                       "chosen_alt": "original", "boundary": None,
                       "seen": {(c["wi_start"], c["wi_end"])}}
             for c in cuts}
    to_process = {c["id"] for c in cuts}  # 첫 라운드는 전부
    locked: set[int] = set()  # 진동 감지로 고정돼 더 이상 재검사 안 하는 이음새

    for r in range(1, max_rounds + 1):
        if not to_process:
            print(f"라운드 {r}: 바뀐 이음새 없음 - 종료")
            break
        print(f"=== 이음새 라운드 {r}/{max_rounds}: {len(to_process)}개 처리 ===")

        cuts_by_id = {c["id"]: c for c in cuts}
        all_alts: dict[int, list[dict]] = {}
        judge_items: list[dict] = []
        for cid in to_process:
            c = cuts_by_id[cid]
            idx = cuts.index(c)
            prev_end, next_start = compute_neighbor_bounds(cuts, idx, len(words))
            alts, items = evaluate_seam(amap, words, duration, state[cid]["wi_start"], state[cid]["wi_end"],
                                        prev_end, next_start, state[cid]["made_by"], cid)
            all_alts[cid] = alts
            judge_items.extend(items)

        groups: dict[str, list[dict]] = {}
        for it in judge_items:
            groups.setdefault(judge_model_for(it["made_by"]), []).append(it)
        judgments: dict[tuple[int, str], AltJudgment] = {}
        for model, items in groups.items():
            print(f"  judging {len(items)} (cut,alt) pair(s) with {model}...")
            judgments.update(judge_batch(client, model, items))

        changed = set()
        for cid in to_process:
            prev_wi = (state[cid]["wi_start"], state[cid]["wi_end"], state[cid]["flag"])
            chosen, flag, reason = select_alt(all_alts[cid], judgments, cid,
                                              state[cid]["flag"], None, words)
            new_key = (chosen["wi_start"], chosen["wi_end"])

            if new_key in state[cid]["seen"] and new_key != prev_wi[:2]:
                # 진동: 전에 거쳐간 조합으로 되돌아옴. 지금 고른 것과 "직전 라운드 상태"(=이번
                # 라운드의 original 대안) 중 점수 높은 쪽으로 고정하고 더 안 건드린다.
                original_alt = next((a for a in all_alts[cid] if a["alt"] == "original"), None)
                prev_score = composite_score(original_alt, words) if original_alt and original_alt.get("_judgment") else -1
                new_score = composite_score(chosen, words)
                final = chosen if new_score >= prev_score or original_alt is None else original_alt
                final_reason = (f"대안 사이를 오가는 진동 감지 - 점수 높은 쪽({final['alt']})으로 고정"
                               + (f"; {reason}" if reason else ""))
                j = final.get("_judgment")
                state[cid].update({"wi_start": final["wi_start"], "wi_end": final["wi_end"],
                                   "flag": "restore", "flag_reason": final_reason, "chosen_alt": final["alt"],
                                   "boundary": {"start": final["start"], "end": final["end"],
                                               "method": final["method"], "audio_ok": final["audio_ok"]},
                                   "judgment": j.model_dump() if j else None})
                locked.add(cid)
                if (state[cid]["wi_start"], state[cid]["wi_end"], state[cid]["flag"]) != prev_wi:
                    changed.add(cid)
                continue

            j = chosen.get("_judgment")
            state[cid].update({"wi_start": chosen["wi_start"], "wi_end": chosen["wi_end"],
                               "flag": flag, "flag_reason": reason, "chosen_alt": chosen["alt"],
                               "boundary": {"start": chosen["start"], "end": chosen["end"],
                                           "method": chosen["method"], "audio_ok": chosen["audio_ok"]},
                               "judgment": j.model_dump() if j else None})
            state[cid]["seen"].add(new_key)
            if (state[cid]["wi_start"], state[cid]["wi_end"], state[cid]["flag"]) != prev_wi:
                changed.add(cid)

        print(f"  라운드 {r}: {len(changed)}개 이음새 변경"
              + (f" ({len(locked)}개 진동 고정)" if locked else ""))
        if r == max_rounds or not changed:
            break
        # 바뀐 이음새의 바로 이웃(문맥이 달라졌을 수 있음)만 다음 라운드 대상 - 진동으로 고정된
        # 건 이웃이 다시 바뀌어도 더 이상 재검사하지 않는다(그래야 진동이 끝난다).
        to_process = set()
        for cid in changed:
            idx = cuts.index(cuts_by_id[cid])
            if idx > 0:
                to_process.add(cuts[idx - 1]["id"])
            if idx + 1 < len(cuts):
                to_process.add(cuts[idx + 1]["id"])
        to_process -= changed  # 자기 자신은 이미 이번 라운드에 반영됨
        to_process -= locked

    # G2: 최종 선택에 대해서만, 한 번에
    selections = [{"id": cid, "start": s["boundary"]["start"], "end": s["boundary"]["end"],
                  "before_ws": words[max(0, s["wi_start"] - G2_WORDS_EACH_SIDE):s["wi_start"]],
                  "after_ws": words[s["wi_end"]:s["wi_end"] + G2_WORDS_EACH_SIDE]}
                 for cid, s in state.items()]
    g2_results = g2_check(source_media(folder), selections, api_key)
    n_g2_bad = 0
    for cid, res in g2_results.items():
        if not res["ok"]:
            n_g2_bad += 1
            if state[cid]["flag"] != "restore":
                state[cid]["flag"] = "restore"
            state[cid]["flag_reason"] = f"{state[cid]['flag_reason'] or ''}; G2 재전사: {res['note']}".strip("; ")
    print(f"G2: {len(g2_results)}개 검사, {n_g2_bad}개 잔여음/절단 의심")

    # ng.json 역전파: 이 라운드에서 이음새 루프 스스로 restore로 판정한 것(대안 전부 실패,
    # 정보 손실 의심, G2 잔여음/절단 의심)은 ng.json에도 반영해야 검토 화면에 실제로 뜬다 -
    # final_cuts.json만 갱신하면 원래 flag 없이 조용히 자동 삭제되던 항목은 화면에 안 보인다
    # (server.py는 ng.json만 읽는다). global_review.py가 이미 쓰는 같은 메커니즘(common.py).
    n_backprop = 0
    for c in cuts:
        s = state[c["id"]]
        if s["flag"] != "restore" or not s["flag_reason"]:
            continue
        reason = f"이음새 부분 루프: {s['flag_reason']}"
        for idx in trace_to_ng_indices(c["id"], cuts):
            if apply_flag_to_ng(ng_items, idx, reason):
                n_backprop += 1
    write_json(ng_path, ng_items)
    print(f"ng.json 역전파: {n_backprop}건 (검토 화면에 반영됨)")

    # 출력
    seams_out, final_cuts = [], []
    for c in cuts:
        s = state[c["id"]]
        seams_out.append({"cut_id": c["id"], "text": c["text"], "made_by": s["made_by"],
                          "chosen_alt": s["chosen_alt"], "boundary": s["boundary"],
                          "judgment": s.get("judgment"),
                          "g2": g2_results.get(c["id"]), "flag": s["flag"], "flag_reason": s["flag_reason"]})
        final_cuts.append({"start": s["boundary"]["start"], "end": s["boundary"]["end"],
                           "wi_start": s["wi_start"], "wi_end": s["wi_end"],
                           "flag": s["flag"], "flag_reason": s["flag_reason"],
                           "made_by": s["made_by"], "boundary_method": s["boundary"]["method"],
                           "chosen_alt": s["chosen_alt"], "cut_id": c["id"]})

    n_clean = sum(1 for s in seams_out if not s["flag"])
    n_changed_boundary = sum(1 for s in seams_out if s["chosen_alt"] != "original")
    print(f"\nresult: {n_clean}/{len(seams_out)} clean, {n_changed_boundary} boundary changed from original "
          f"(shrink/expand/snap), none cancelled (max-delete policy)")

    write_json(edit_dir(folder) / "seams.json", {"seams": seams_out})
    write_json(edit_dir(folder) / "final_cuts.json", {"cuts": final_cuts})
    print(f"wrote {edit_dir(folder) / 'seams.json'}")
    print(f"wrote {edit_dir(folder) / 'final_cuts.json'}")
    return edit_dir(folder) / "final_cuts.json"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--max-rounds", type=int, default=3)
    args = ap.parse_args()
    refine(video_dir(args.folder), max_rounds=args.max_rounds)


if __name__ == "__main__":
    main()
