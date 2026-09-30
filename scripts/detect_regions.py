"""Stage 1 (하향식 재설계, 2026-09-30) - "전체를 넓게" 본다. 원본 대본 전체를 한 번에 읽고
의심 구간을 대략적으로 표시한다. 정확한 단어 경계는 여기서 정하지 않는다 - classify_region.py
(Stage 2)가 각 구간을 확대해서 정한다.

기존 detect_ng_candidates.py(국소 반복 탐지, 앞뒤 3단어 창만 봄)는 같은 문단 안에서 문장 하나를
2~4번 고쳐 말하는 재시작 사슬조차 후보로 못 만들었다(이 파일이 대체하기 전 whole_context_review.py
자체 docstring이 BS167 재현율 붕괴의 85%가 이 문제였다고 진단해 놓았다 - 결정-이력.md 09-30
"하향식 재설계"). 국소 창을 넓히는 대신, 사람 편집자가 하듯 전체를 먼저 읽고 "여기를 다시 봐라"만
표시하는 쪽으로 뒤집는다 - 정확도는 Stage 2가 좁혀서 책임진다.

두 채널로 후보를 만든다:
  1. **로컬 힌트** (LLM 호출 없음, 공짜): 단어 절단("--")이나 앞뒤 3단어 안의 명시적 중복 -
     이미 100% 확실한 결정론적 신호라 전체 맥락이 필요 없다. detect_ng_candidates.py의
     has_word_fragment/has_internal_repetition을 그대로 옮겼다.
  2. **전체 맥락 LLM 스캔** (`llm_scan`, claude-opus-5-5, 전체 문서 1회 호출 - global_review.py의
     `pd_review()`와 같은 규모·같은 패턴): 로컬 힌트가 원리적으로 못 보는 것 - 표현을 바꿔
     다시 말한 재진술, 카메라 밖 대화, 필러 몰림, 흐름이 불분명한 곳.

로컬 힌트가 이미 잡은 구간은 LLM 스캔 프롬프트에 "[이미 잡힘]"으로 표시해 같은 걸 다시 찾느라
낭비하지 않게 한다(whole_context_review.py의 [이미 후보로 잡힘] 패턴과 동일).

Usage:
    python scripts/detect_regions.py <videos/NAME> [--no-llm]
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel

from common import load_env, video_dir, edit_dir, load_transcript, words_only, write_json, norm, thinking_kwargs
from detect_speaker_blocks import split_lines

LLM_MODEL = "claude-opus-5-5"   # PD_MODEL(global_review.py)과 같은 규모의 판단
FRAGMENT_WINDOW = 3              # 로컬 힌트: 이 단어 수 안의 중복만 "이미 확실"로 본다
CHUNK_WORDS = 800                # 2026-09-30: 전체를 한 번에(2500단어) 보여주면 눈에 띄는 몇 개만
                                  # 찾고 끝내는 경향이 실측됨(BS145 spot-check: 6건) - 청크당
                                  # 800단어로 나눠 청크마다 "체계적으로 훑어라"를 더 강제하니 같은
                                  # 프롬프트로 12건. whole_context_review.py의 실패(청크를 "핵심
                                  # 주장 요약"으로 압축해 같은 청크 안 반복까지 뭉갬)와는 다르게,
                                  # 여기는 원문 그대로 보여준다 - 압축이 아니라 그냥 창을 좁힌 것.
CHUNK_OVERLAP_WORDS = 150         # 청크 경계에 걸친 재시작 사슬을 놓치지 않기 위한 겹침


# --------------------------------------------------------------------------------- 로컬 힌트

def _has_fragment(text: str) -> bool:
    return text.strip().endswith("--")


def local_hints(words: list[dict]) -> list[dict]:
    """detect_ng_candidates.py의 find_standalone_runs를 그대로 옮김 - 단어 절단 표시나 앞뒤
    3단어 안 중복만 잡는 결정론적 신호. 이미 경계가 정확하므로 Stage 2에서 재확정 없이 그대로
    쓸 수 있다(precise=True)."""
    norm_toks = [norm(w["text"]) for w in words]
    flagged: set[int] = set()
    for i, w in enumerate(words):
        if _has_fragment(w["text"]):
            flagged.add(i)
        t = norm_toks[i]
        if not t:
            continue
        for j in range(i + 1, min(i + 1 + FRAGMENT_WINDOW, len(words))):
            if norm_toks[j] == t:
                flagged.add(i)
                flagged.add(j)

    if not flagged:
        return []
    idxs = sorted(flagged)
    runs, cur = [], [idxs[0]]
    for i in idxs[1:]:
        if i - cur[-1] <= FRAGMENT_WINDOW:
            cur.append(i)
        else:
            runs.append(cur)
            cur = [i]
    runs.append(cur)

    out = []
    for r in runs:
        i1, i2 = r[0], r[-1] + 1
        seg = words[i1:i2]
        out.append({
            "wi_start": i1, "wi_end": i2, "precise": True, "kind": "RESTART",
            "reason": "단어 절단(--) 또는 인접 단어 중복 - 결정론적 신호",
            "confidence": 0.9, "ref_wi_start": None, "ref_wi_end": None,
            "source": "local_hint", "deleted_text": " ".join(w["text"] for w in seg),
        })
    return out


# --------------------------------------------------------------------------------- 전체 맥락 LLM 스캔

class RegionFlag(BaseModel):
    wi_start: int
    wi_end: int  # exclusive, 대략적인 범위면 충분 - 정확한 경계는 Stage 2가 정한다
    kind: Literal["RESTART", "OFF_TOPIC", "CAMERA_DIRECTION", "FILLER_BURST", "UNCLEAR"]
    reason: str
    confidence: float
    ref_wi_start: Optional[int] = None  # RESTART일 때: 같은 내용을 다시 말한 "다른 쪽" 위치(근거용)
    ref_wi_end: Optional[int] = None


class RegionScan(BaseModel):
    regions: list[RegionFlag]


SYSTEM = """\
너는 과학·논문 근거 기반 육아 강의 채널의 전담 편집자다. 이 채널 원칙: **재촬영은 마지막 시도만
남긴다.** 강조 반복과 교육적 재진술은 살린다. 카메라 밖 대화(촬영 지시 등)는 모두 지운다.

아래는 원본 전체 트랜스크립트다(줄 단위, 맨 앞 [123-130]이 그 줄의 단어 id 구간 - 반열림). `[이미
잡힘]` 표시는 국소 규칙이 이미 확실하게 찾은 곳이니 다시 보고하지 마라. `[화자 이탈 블록]` 표시는
별도 탐지가 이미 처리 중이니 역시 다시 보고하지 마라.

**지금은 정확한 경계를 정하지 않아도 된다 - "이 근처를 다시 봐야 한다"는 대략적인 범위만 표시해라.**
정밀한 단어 경계는 다음 단계가 확대해서 정한다.

**이 패스는 최종 판단이 아니라 후보를 넓게 모으는 안전망이다 - 확신이 낮아도(confidence를 낮게
주고) 의심되면 보고하라. 나중 단계가 각 구간을 확대해서 정밀하게 다시 판단한다.** 문서를 처음부터
끝까지 문단 단위로 훑으면서, 눈에 띄는 몇 개만 보고하지 말고 **각 문단마다 "이 안에 재시작이나
군더더기 반복이 있는가"를 체계적으로 점검하라** - 짧은 간격의 재시작 사슬(같은 문장을 2~4번
고쳐 말하는 것)이 가장 흔하고 가장 중요하니 절대 몇 개만 찾고 끝내지 마라. 다음을 찾아라(없으면
regions 빈 리스트):

- RESTART: 같은 내용(주장·수치·결론이 사실상 같음)을 시간이 지나 다시 말한 곳. 표현이 완전히
  달라도 의미가 같으면 재진술이다 - 문자열이 닮았는지가 아니라 뜻으로 판단하라. 우연히 비슷한
  단어를 쓴 것뿐인 다른 내용은 재진술이 아니다. **먼저 나온 쪽이 삭제 후보다**(재촬영은 마지막
  시도만 남긴다) - wi_start/wi_end에 먼저 나온 쪽의 대략적 범위를, ref_wi_start/ref_wi_end에
  나중에 다시 말한 쪽(근거 확인용, 삭제 대상 아님)을 채워라. 같은 문단 안에서 문장 하나를 2~4번
  고쳐 말하는 것도 RESTART다(짧은 간격이라고 놓치지 마라 - 오히려 이런 경우가 가장 흔하다).
- OFF_TOPIC: 강의 내용과 무관한 구간 - 촬영 지시, 장비 점검, 카메라 밖을 향한 발언. 독백 형태로
  나타나도 좋다.
- CAMERA_DIRECTION: 촬영/시선/자리 등 촬영 상황 자체에 대한 지시나 대화(OFF_TOPIC과 겹쳐도 됨,
  더 명확한 쪽으로 표시).
- FILLER_BURST: "음", "어", "그" 같은 채움말이 뭉쳐 나오는 곳(단독 필러는 별도 결정론적 탐지가
  처리하니, 뭉쳐서 흐름을 끊는 구간만).
- UNCLEAR: 말이 계속 끊기고 다시 시작해서 무슨 말인지 전체적으로 알기 힘든 구간(위 네 가지로
  명확히 분류가 안 될 때).

각 region: wi_start, wi_end, kind, reason(한국어 한 문장), confidence(0-1), (RESTART면)
ref_wi_start/ref_wi_end.
"""


def chunk_lines(lines: list[dict], target_words: int, overlap_words: int) -> list[list[dict]]:
    """~target_words 단위로 나누되, 청크 경계에 걸친 재시작 사슬을 놓치지 않기 위해 이전
    청크의 마지막 overlap_words만큼을 다음 청크 앞에도 겹쳐 넣는다(줄 단위로만 자름)."""
    chunks: list[list[dict]] = []
    cur: list[dict] = []
    cur_words = 0
    for ln in lines:
        n = ln["wi_end"] - ln["wi_start"] + 1
        if cur and cur_words + n > target_words:
            chunks.append(cur)
            overlap: list[dict] = []
            ow = 0
            for prev_ln in reversed(cur):
                pn = prev_ln["wi_end"] - prev_ln["wi_start"] + 1
                if ow + pn > overlap_words and overlap:
                    break
                overlap.insert(0, prev_ln)
                ow += pn
            cur, cur_words = list(overlap), ow
        cur.append(ln)
        cur_words += n
    if cur:
        chunks.append(cur)
    return chunks


def build_document_view(chunk_lines_: list[dict], covered: set[int], block_covered: set[int]) -> str:
    out = []
    for ln in chunk_lines_:
        rng = range(ln["wi_start"], ln["wi_end"] + 1)
        tag = ""
        if any(wi in block_covered for wi in rng):
            tag = " [화자 이탈 블록]"
        elif any(wi in covered for wi in rng):
            tag = " [이미 잡힘]"
        out.append(f"[{ln['wi_start']}-{ln['wi_end']}]{tag} {ln['text']}")
    return "\n".join(out)


def llm_scan(client, doc_view: str) -> list[RegionFlag]:
    resp = client.messages.parse(model=LLM_MODEL, max_tokens=8000, system=SYSTEM,
                                 messages=[{"role": "user", "content": doc_view}],
                                 output_format=RegionScan, **thinking_kwargs(LLM_MODEL, effort="high"))
    return resp.parsed_output.regions


# --------------------------------------------------------------------------------- main

def detect(folder: Path, use_llm: bool = True) -> Path:
    load_env()
    words = words_only(load_transcript(folder))
    blocks_path = edit_dir(folder) / "speaker_blocks.json"
    import json
    blocks = json.loads(blocks_path.read_text())["blocks"] if blocks_path.exists() else []
    block_covered: set[int] = set()
    for b in blocks:
        block_covered.update(range(b["wi_start"], b["wi_end"] + 1))

    hints = local_hints(words)
    covered = {wi for h in hints for wi in range(h["wi_start"], h["wi_end"])}
    print(f"local hints: {len(hints)} (deterministic, no LLM call)")

    llm_regions: list[dict] = []
    if use_llm:
        import anthropic
        client = anthropic.Anthropic()
        lines = split_lines(words)
        chunks = chunk_lines(lines, CHUNK_WORDS, CHUNK_OVERLAP_WORDS)
        print(f"whole-document scan: {len(words)} words, {len(lines)} lines, {len(chunks)} chunk(s) "
              f"({LLM_MODEL}, {CHUNK_WORDS}단어/청크·{CHUNK_OVERLAP_WORDS}단어 겹침)")

        def scan_chunk(chunk: list[dict]) -> list[RegionFlag]:
            return llm_scan(client, build_document_view(chunk, covered, block_covered))

        seen: set[tuple[int, int, str]] = set()
        with ThreadPoolExecutor(max_workers=6) as pool:
            futures = [pool.submit(scan_chunk, c) for c in chunks]
            for fut in as_completed(futures):
                for f in fut.result():
                    key = (f.wi_start, f.wi_end, f.kind)
                    if key in seen:
                        continue
                    seen.add(key)
                    llm_regions.append({
                        "wi_start": f.wi_start, "wi_end": f.wi_end, "precise": False, "kind": f.kind,
                        "reason": f.reason, "confidence": f.confidence,
                        "ref_wi_start": f.ref_wi_start, "ref_wi_end": f.ref_wi_end, "source": "llm",
                    })
        llm_regions.sort(key=lambda r: r["wi_start"])
        print(f"llm scan: {len(llm_regions)} region(s) found (중복 제거 후)")
        for r in llm_regions:
            print(f"  [{words[r['wi_start']]['start']:.1f}s] {r['kind']} conf={r['confidence']:.2f} :: {r['reason']}")

    regions = hints + llm_regions
    out = edit_dir(folder) / "regions.json"
    write_json(out, {"model": LLM_MODEL if use_llm else None, "regions": regions})
    print(f"wrote {out} ({len(regions)} region(s): {len(hints)} local, {len(llm_regions)} llm)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--no-llm", action="store_true", help="로컬 힌트만 (LLM 호출 없음)")
    args = ap.parse_args()
    detect(video_dir(args.folder), use_llm=not args.no_llm)


if __name__ == "__main__":
    main()
