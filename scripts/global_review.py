"""전체 루프 (docs/기획/03-두-관점-평가.md) - 이음새 부분 루프(seam_refine.py)가 컷 하나하나의
매끄러움만 보는 것과 달리, 결과 전체를 두 관점에서 읽는다.

  - PD 평가 (원본 + 잘린 부분 + 이유를 다 보고 판단): 맥락상 더 잘랐어야 하는데 안 잘린 곳
    (missed_cut - NG/화자 이탈이 아직 남아있음)과, 맥락상 필요한데 잘려서 결과가 이상해질
    구간(over_cut)을 양방향으로 찾는다.
  - 시청자 평가 (결과 텍스트만 봄, 무엇이 잘렸는지 모름): "이 글이 그 자체로 완결된 내용으로
    읽히는가"를 순수하게 판정한다 - 흐름 단절(jump), 이해 불가(unclear), 과밀/지루함 등.

만드는 모델과 판정 모델이 다르다는 원칙(seam_refine.py와 동일)에 더해, PD와 시청자도 서로 다른
모델이다.

2026-09-29 2차 구현 - "축소분 제대로 구현해" 반영:
  - **ng.json 역전파**: `draft_cuts.json`의 `sources`(각 병합 컷이 어느 ng 항목/화자블록 줄에서
    왔는지)를 거슬러 올라가, over_cut·시청자 jump/unclear를 실제 ng 항목의 flag까지
    반영한다. 이제 검토 화면에 뜬다(ng.json을 읽는 건 이미 server.py가 하니까).
  - **재투입, 정확히 1회** (2026-09-30 하향식 재설계로 단순화 - 예전엔 최대 2라운드 재투입이었으나
    세션에 걸쳐 반복 실행하면 ng.json에 판단이 누적되는 문제를 겪어 "끝나면 한 번 더"로 단순화):
    missed_cut으로 새 후보가 생기면 assemble_draft.py -> seam_refine.py를 1회만 다시 돌려
    반영하고 종료한다 - PD·시청자를 다시 부르지 않는다.

Usage:
    python scripts/global_review.py <videos/NAME> [--max-rounds 2]
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel

from common import (load_env, video_dir, edit_dir, load_transcript, words_only, write_json,
                    trace_to_ng_indices, apply_flag_to_ng, thinking_kwargs, log_llm_usage)

PD_MODEL = "claude-opus-5-5"
VIEWER_MODEL = "claude-fable-5-1"
VIEWER_FALLBACK_MODEL = "claude-sonnet-5"
HERE = Path(__file__).resolve().parent


# --------------------------------------------------------------------------------- views

def build_pd_view(words: list[dict], final_cuts: list[dict]) -> str:
    """원본 전체를 컷이 인라인으로 보이는 형태로, 줄마다 단어 id 구간을 표시한다(missed_cut을
    찾았을 때 정확한 wi_start/wi_end를 답하려면 모델이 참조할 id가 텍스트에 직접 있어야 한다 -
    없으면 모델이 추측한 값을 내놓고 대부분 틀린다). 잘린 부분도 그대로 보여준다(PD는 뭐가 왜
    잘렸는지 알아야 판단할 수 있음)."""
    from detect_speaker_blocks import split_lines
    cuts_sorted = sorted(final_cuts, key=lambda c: c["wi_start"])
    cut_at_start = {c["wi_start"]: c for c in cuts_sorted}

    lines = split_lines(words)
    out = []
    for ln in lines:
        seg = words[ln["wi_start"]:ln["wi_end"] + 1]
        pieces = []
        i = 0
        while i < len(seg):
            wi = seg[i]["wi"]
            if wi in cut_at_start:
                c = cut_at_start[wi]
                text = " ".join(w["text"] for w in words[c["wi_start"]:c["wi_end"]])
                pieces.append(f"⟦CUT id={c['cut_id']} flag={c.get('flag') or '없음'}⟧{text}⟦/CUT⟧")
                i += c["wi_end"] - wi
            else:
                pieces.append(seg[i]["text"])
                i += 1
        out.append(f"[{ln['wi_start']}-{ln['wi_end']}] {' '.join(pieces)}")
    return "\n".join(out)


def gap_mark(gap: float) -> str:
    if gap >= 0.8:
        return " ··· "
    if gap >= 0.4:
        return " ·· "
    if gap >= 0.15:
        return " · "
    return " "


def build_viewer_view(words: list[dict], final_cuts: list[dict]) -> tuple[str, list[dict]]:
    """잘린 부분은 전혀 안 보여준다. 결과에 남는 단어만, 쉼 표시와 함께. 이음새(컷 경계)마다
    구간 번호(⟦S N⟧)를 매겨 시청자가 위치를 지목할 수 있게 하되, 무엇이 잘렸는지는 드러내지
    않는다 - 구간이 끊긴다는 사실 자체는 시청자도 체감하는 것이라 숨기지 않는다."""
    cut_ranges = sorted([(c["wi_start"], c["wi_end"]) for c in final_cuts])
    segments: list[dict] = []
    cur: list[dict] = []
    seg_id = 0

    def flush():
        nonlocal cur, seg_id
        if cur:
            segments.append({"id": seg_id, "wi_start": cur[0]["wi"], "wi_end": cur[-1]["wi"] + 1,
                             "words": cur})
            seg_id += 1
            cur = []

    cut_set = set()
    for s, e in cut_ranges:
        cut_set.update(range(s, e))
    for w in words:
        if w["wi"] in cut_set:
            flush()
            continue
        cur.append(w)
    flush()

    out = []
    for seg in segments:
        ws = seg["words"]
        piece = [f"⟦S{seg['id']}⟧"]
        for k, w in enumerate(ws):
            piece.append(w["text"])
            if k + 1 < len(ws):
                piece.append(gap_mark(ws[k + 1]["start"] - w["end"]))
        out.append(" ".join(piece))
    return " ".join(out), segments


# --------------------------------------------------------------------------------- PD

class PDFinding(BaseModel):
    type: Literal["missed_cut", "over_cut"]
    cut_id: Optional[int] = None      # over_cut: final_cuts의 cut_id
    wi_start: Optional[int] = None    # missed_cut: 원본 단어 id (반열림)
    wi_end: Optional[int] = None
    final_attempt_wi_start: Optional[int] = None  # missed_cut 안에 실패한 시도가 여럿이고 그중
    # 하나가 완성된 문장으로 끝났다면 그 시작 단어 id (classify_region.py와 같은 안전장치,
    # 2026-09-30 BS167 실측 버그 - wi_end가 이 값을 넘으면 완성된 문장 앞부분까지 잘림)
    reason: str
    confidence: float
    severity: Literal["high", "medium", "low"]


class PDReview(BaseModel):
    findings: list[PDFinding]


PD_SYSTEM = """\
너는 과학·논문 근거 기반 육아 강의 채널의 전담 편집자다. 이 채널 원칙: 재촬영은 마지막 시도만
남긴다. 강조 반복과 교육적 재진술은 살린다. 카메라 밖 대화(촬영 지시 등)는 모두 지운다.

아래는 원본 전체 트랜스크립트다. 줄마다 맨 앞 [123-130] 같은 표시가 그 줄의 단어 id 구간이다
(반열림 - 130은 포함 안 됨). ⟦CUT id=N flag=...⟧잘린 텍스트⟦/CUT⟧ 표시가 이미 컷 결정이 내려진
구간이다. flag=복원후보는 사람이 검토할 예정, flag=없음은 이미 확정 적용된 컷이다.

다음을 찾아라(빈도 낮음 - 없으면 findings 빈 리스트). **이미 CUT 표시된 구간과 겹치는 위치는
missed_cut으로 다시 보고하지 마라** - 이미 처리 중이다.
- missed_cut: CUT 표시가 안 됐는데 남아있으면 안 되는 것 - 재시작의 앞 시도, 카메라 밖 대화,
  말버릇 반복. **반드시** wi_start/wi_end를 채워라 - 그 구간이 속한 줄 맨 앞의 [숫자-숫자] 표시를
  보고 실제 단어 위치로 답하라(대략 짐작하지 말고, 문제되는 단어들이 정확히 어디서 시작해서
  어디서 끝나는지 줄 안에서 세어라). wi_start/wi_end 없이는 이 finding을 적용할 수 없다.
  **이 구간 안에 실패한 시도가 여럿이고 그중 하나가 완성된 문장으로 끝났다면**, 그 시작 단어 id를
  final_attempt_wi_start에 채워라 - wi_end가 그 값을 넘으면 안 된다(완성된 문장 일부까지 자르면
  안 되니까).
- over_cut: CUT 표시된 구간인데, 그 안에 결과에서 사라지면 안 되는 정보(새 사실·수치·예시·조건)가
  있어서 과하게 잘린 것. **반드시** 그 ⟦CUT id=N⟧의 N을 cut_id에 그대로 채워라.

각 finding: type, (해당 필드), reason(한국어 한 문장), confidence(0-1), severity(high/medium/low).
"""


def pd_review(pd_view: str, folder: Path) -> list[PDFinding]:
    import anthropic
    client = anthropic.Anthropic()
    resp = client.messages.parse(model=PD_MODEL, max_tokens=6000, system=PD_SYSTEM,
                                 messages=[{"role": "user", "content": pd_view}],
                                 output_format=PDReview, **thinking_kwargs(PD_MODEL))
    log_llm_usage(folder, "global_review_pd", PD_MODEL, resp.usage)
    return resp.parsed_output.findings


# 2026-10-01 (docs/기획/03-두-관점-평가.md 4장 "없음|repetition" 행): 시청자만 repetition을
# 지적하고 PD는 그 자리를 안 걸렸을 때, PD에게 "이거 missed_cut 맞냐"고 좁혀서 재질의한다.
# PDFinding/PDReview 스키마를 그대로 재사용 - 결과가 missed_cut이면 기존 missed_cut 처리
# 경로(new_ng_items)에 그대로 합류시킬 수 있다.
REPETITION_RECHECK_SYSTEM = """\
너는 같은 채널의 전담 편집자다. 시청자 평가가 아래 결과물의 특정 구간들을 "방금 들은 말을 또
듣는 느낌"이라고 지적했다 - PD(너)는 전체 검토에서 이 구간들을 놓쳤었다. 각 구간이 실제로
지웠어야 할 불필요한 재진술(missed_cut)인지, 의도된 강조·교육적 재진술이라 살려야 하는지
다시 판단하라.

지워야 한다고 판단되면 missed_cut finding 하나로 보고하라 - wi_start/wi_end는 주어진
"[구간, 단어 N-M]" 표시 그대로 채워라(반드시). 살려야 한다고 판단되면 그 구간에 대해 아무
finding도 내지 마라 - 이건 재질의 전용이니 다른 missed_cut/over_cut은 보고하지 마라.
"""


def recheck_repetitions(words: list[dict], repetition_vfs: list["ViewerFinding"],
                        seg_by_id: dict[int, dict], folder: Path) -> list[PDFinding]:
    blocks = []
    for vf in repetition_vfs:
        seg = seg_by_id.get(vf.segment_id)
        if not seg:
            continue
        before = " ".join(w["text"] for w in words[max(0, seg["wi_start"] - 40):seg["wi_start"]])
        text = " ".join(w["text"] for w in seg["words"])
        blocks.append(f"[구간, 단어 {seg['wi_start']}-{seg['wi_end']}]\n앞 맥락: …{before}\n"
                      f"지적된 구간: {text}\n시청자 지적: {vf.reason}")
    if not blocks:
        return []
    import anthropic
    client = anthropic.Anthropic()
    resp = client.messages.parse(model=PD_MODEL, max_tokens=3000, system=REPETITION_RECHECK_SYSTEM,
                                 messages=[{"role": "user", "content": "\n\n".join(blocks)}],
                                 output_format=PDReview, **thinking_kwargs(PD_MODEL))
    log_llm_usage(folder, "global_review_repetition_recheck", PD_MODEL, resp.usage)
    return resp.parsed_output.findings


# --------------------------------------------------------------------------------- viewer

class ViewerFinding(BaseModel):
    type: Literal["jump", "unclear", "rushed", "dragging", "repetition", "boring"]
    segment_id: int
    quote: str
    reason: str
    severity: Literal["high", "medium", "low"]


class ViewerOverall(BaseModel):
    flow: int
    pace: int
    comment: str


class ViewerReview(BaseModel):
    findings: list[ViewerFinding]
    overall: ViewerOverall


VIEWER_SYSTEM = """\
너는 3세 아이를 키우는 부모다. 퇴근길 지하철에서 휴대폰으로 육아 강의 영상을 1배속으로 보고 있다.
아래는 영상에서 들리는 말을 받아 적은 것이다. ⟦S번호⟧는 구간 표시, `·`은 짧은 쉼, `··`은 중간 쉼,
`···`은 긴 쉼이다.

보다가 "어?" 하고 걸리는 곳, 너무 빨라서 따라가기 힘든 곳, 늘어져서 넘기고 싶은 곳, 같은 말을 또
듣는 느낌이 드는 곳, 지루해서 스킵하고 싶은 곳을 솔직하게 짚어라. 문제없으면 없다고 하라.

각 finding: type(jump/unclear/rushed/dragging/repetition/boring), segment_id(가장 가까운 ⟦S번호⟧),
quote(짧은 인용), reason(한 문장), severity. 마지막에 overall(flow 1-5, pace 1-5, comment 한 문장).
"""


def viewer_review(viewer_view: str, folder: Path) -> tuple[ViewerReview, str]:
    import anthropic
    client = anthropic.Anthropic()
    model = VIEWER_MODEL
    try:
        resp = client.messages.parse(model=model, max_tokens=4000, system=VIEWER_SYSTEM,
                                     messages=[{"role": "user", "content": viewer_view}],
                                     output_format=ViewerReview, **thinking_kwargs(model))
    except Exception as e:
        print(f"  {VIEWER_MODEL} 호출 실패({e}) - {VIEWER_FALLBACK_MODEL}로 대체")
        model = VIEWER_FALLBACK_MODEL
        resp = client.messages.parse(model=model, max_tokens=4000, system=VIEWER_SYSTEM,
                                     messages=[{"role": "user", "content": viewer_view}],
                                     output_format=ViewerReview, thinking={"type": "disabled"})
    log_llm_usage(folder, "global_review_viewer", model, resp.usage)
    return resp.parsed_output, model


# --------------------------------------------------------------------------------- 한 라운드

def one_round(folder: Path, words: list[dict], edit: Path) -> dict:
    ng_path = edit / "ng.json"
    ng_items = json.loads(ng_path.read_text()) if ng_path.exists() else []
    final_path = edit / "final_cuts.json"
    final_cuts = json.loads(final_path.read_text())["cuts"] if final_path.exists() else []
    draft_path = edit / "draft_cuts.json"
    draft_cuts = json.loads(draft_path.read_text())["cuts"] if draft_path.exists() else []

    pd_view = build_pd_view(words, final_cuts)
    viewer_view, segments = build_viewer_view(words, final_cuts)
    print(f"  PD 입력 {len(pd_view)}자 ({PD_MODEL}), 시청자 입력 {len(viewer_view)}자 "
          f"({len(segments)}구간, {VIEWER_MODEL} 시도)")

    pd_findings = pd_review(pd_view, folder)
    print(f"  PD 발견: {len(pd_findings)}건")
    for f in pd_findings:
        print(f"    {f.type} sev={f.severity} conf={f.confidence:.2f} :: {f.reason}")

    viewer_result, viewer_model_used = viewer_review(viewer_view, folder)
    print(f"  시청자 발견: {len(viewer_result.findings)}건 (flow={viewer_result.overall.flow} "
          f"pace={viewer_result.overall.pace})")
    for f in viewer_result.findings:
        print(f"    {f.type} sev={f.severity} S{f.segment_id} :: {f.reason}")

    seg_by_id = {s["id"]: s for s in segments}
    final_by_id = {c["cut_id"]: c for c in final_cuts}

    # repetition(시청자만 지적, PD는 놓침) -> PD에게 "missed_cut 맞냐"고 좁혀 재질의
    # (docs/기획/03-두-관점-평가.md 4장). 결과는 missed_cut이면 아래 new_ng_items 처리에 합류.
    repetition_vfs = [vf for vf in viewer_result.findings if vf.type == "repetition"]
    repetition_findings = recheck_repetitions(words, repetition_vfs, seg_by_id, folder) if repetition_vfs else []
    if repetition_vfs:
        print(f"  repetition 재질의: {len(repetition_vfs)}건 중 {len(repetition_findings)}건 missed_cut으로 확인")
    pd_findings = pd_findings + repetition_findings

    # missed_cut -> 새 ng 후보 (항상 flag=restore - 검증 안 된 새 경로라 보수적으로)
    # 2026-09-30: "이미 처리된 구간과 겹치면 버린다"는 가드를 시도했다가 되돌림 - ng_items가
    # 이 시점엔 이미 문서 전체에 밀도 높게 깔려 있어서, 진짜 missed_cut까지도 "근처에 뭔가
    # 있다"는 이유로 거의 다 버려짐(BS167 실측: 11건 전부 차단, 재현율 0.704→0.490으로 붕괴).
    # 되돌림 - 중복 재판정 문제는 아직 미해결로 남음, 다음에는 "겹침"이 아니라 "완전히 포함"
    # 같은 훨씬 좁은 기준으로 다시 시도해야 한다.
    new_ng_items = []
    for f in pd_findings:
        if f.type != "missed_cut" or f.wi_start is None or f.wi_end is None:
            continue
        wi_end = f.wi_end
        if f.final_attempt_wi_start is not None and wi_end > f.final_attempt_wi_start > f.wi_start:
            print(f"    [clamp] missed_cut wi_end {wi_end}->{f.final_attempt_wi_start} (완성된 시도 보호)")
            wi_end = f.final_attempt_wi_start
        seg = [w for w in words if f.wi_start <= w["wi"] < wi_end]
        if not seg:
            continue
        new_ng_items.append({
            "raw_word_index_start": f.wi_start, "raw_word_index_end": wi_end,
            "follow_word_index_start": wi_end, "follow_word_index_end": wi_end,
            "start": seg[0]["start"], "end": seg[-1]["end"],
            "duration": round(seg[-1]["end"] - seg[0]["start"], 3),
            "n_words": len(seg), "deleted_text": " ".join(w["text"] for w in seg),
            "following_text_in_raw": "", "similarity_to_following": None, "prefix_similarity": None,
            "dominant_speaker": seg[0].get("speaker_id"), "n_speakers_in_run": len({w.get("speaker_id") for w in seg}),
            "has_word_fragment": False, "has_internal_repetition": False,
            "label": "GLOBAL_REVIEW_MISSED_CUT",
            "route": "CUT", "flag": "restore",
            "route_reason": f"전체 루프 PD 평가: {f.reason} (confidence={f.confidence:.2f}) - 복원 후보로 자름",
            "llm_classification": None, "llm_model": PD_MODEL,
        })

    # over_cut (PD) -> final_cuts.json + ng.json 역전파
    flag_updates, ng_backprop = 0, 0
    for f in pd_findings:
        if f.type != "over_cut" or f.cut_id not in final_by_id:
            continue
        c = final_by_id[f.cut_id]
        reason = f"전체 루프 PD: 정보 손실 의심 - {f.reason}"
        if c.get("flag") != "restore":
            flag_updates += 1
        c["flag"] = "restore"
        c["flag_reason"] = f"{c.get('flag_reason') or ''}; {reason}".strip("; ")
        for idx in trace_to_ng_indices(f.cut_id, draft_cuts):
            if apply_flag_to_ng(ng_items, idx, reason):
                ng_backprop += 1

    # 시청자 jump/unclear -> 구조적으로 걸 수 있는 인접 컷에 flag (final_cuts + ng.json 역전파)
    for vf in viewer_result.findings:
        if vf.type not in ("jump", "unclear"):
            continue
        seg = seg_by_id.get(vf.segment_id)
        if not seg:
            continue
        for c in final_cuts:
            if c["wi_end"] == seg["wi_start"] or c["wi_start"] == seg["wi_end"]:
                reason = f"전체 루프 시청자: {vf.type} - {vf.reason}"
                if c.get("flag") != "restore":
                    flag_updates += 1
                c["flag"] = "restore"
                c["flag_reason"] = f"{c.get('flag_reason') or ''}; {reason}".strip("; ")
                for idx in trace_to_ng_indices(c["cut_id"], draft_cuts):
                    if apply_flag_to_ng(ng_items, idx, reason):
                        ng_backprop += 1

    if new_ng_items:
        ng_items.extend(new_ng_items)
    write_json(ng_path, ng_items)
    write_json(final_path, {"cuts": final_cuts})

    print(f"  적용: 새 컷 후보 {len(new_ng_items)}건, "
          f"final_cuts flag 갱신 {flag_updates}건, "
          f"ng.json 역전파 {ng_backprop}건(검토 화면에 반영됨)")

    return {
        "pd_model": PD_MODEL, "viewer_model": viewer_model_used,
        "pd_findings": [f.model_dump() for f in pd_findings],
        "viewer_findings": [f.model_dump() for f in viewer_result.findings],
        "viewer_overall": viewer_result.overall.model_dump(),
        "new_ng_items": len(new_ng_items), "flag_updates": flag_updates,
        "ng_backprop": ng_backprop,
        "repetition_rechecked": len(repetition_vfs), "repetition_confirmed": len(repetition_findings),
    }


def rerun_assemble_and_seam(folder: Path) -> None:
    for script in ("assemble_draft.py", "seam_refine.py"):
        subprocess.run([sys.executable, str(HERE / script), str(folder)], check=True)


def iterate(folder: Path) -> Path:
    """Stage 3 (하향식 재설계, 2026-09-30) - "끝나면 한 번 더", 정확히 1회. 예전엔 최대
    2라운드까지 재투입(매 라운드 assemble+seam을 다시 돌려 재평가)했는데, 이 재투입 루프를
    세션에 걸쳐 반복 실행하면 GLOBAL_REVIEW_MISSED_CUT이 ng.json에 계속 누적돼 A/B 비교가
    오염되는 문제를 실제로 겪었다(docs/기획/06-검증과-측정.md 6.1절). PD+시청자 리뷰는
    정확히 1회만 하고, 그 결과로 missed_cut이 나오면 assemble+seam을 1회만 더 돌려 반영한 뒤
    종료한다(재리뷰 없음) - "컷편집이 완료되면 마지막에 한 번 더 전체를 검수한다"는 설계
    그대로."""
    load_env()
    edit = edit_dir(folder)
    words = words_only(load_transcript(folder))

    print("=== 전체 루프 (1회 최종 통독) ===")
    result = one_round(folder, words, edit)
    if result["new_ng_items"] > 0:
        print("  missed_cut 반영 위해 assemble_draft -> seam_refine 1회만 재실행...")
        rerun_assemble_and_seam(folder)
    else:
        print("  새로 반영할 컷 없음")

    out = edit / "global_review.json"
    write_json(out, {"rounds": [result], "n_rounds": 1})
    print(f"wrote {out}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    iterate(video_dir(args.folder))


if __name__ == "__main__":
    main()
