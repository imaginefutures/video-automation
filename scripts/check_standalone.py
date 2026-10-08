"""주제별 분할 3단계 - 각 편이 그 편만 봐도 이해되는지 판정한다 (docs/백로그/주제별-분할.md).

구간을 만든 모델과 다른 모델이 판정한다 (만든 쪽 ≠ 판정하는 쪽). 판정은 경고 라벨만 붙이고 경계를 고치지 않는다 - 고칠지는 사람이 분할 화면에서 정한다.

segments.json의 각 편에 "check": {"verdict": "ok"|"warn", "issues": [{"sent", "kind", "note"}]}를 더한다.

Usage:
    python scripts/check_standalone.py <splits/NAME>
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from common import load_env, edit_dir, write_json, thinking_kwargs, log_llm_usage
from split_sentences import load_sentences

# propose_segments.MAKER_MODEL(opus)과 다른 모델. seam_refine.JUDGE_FOR를 가져다 쓰지 않는 건 분할이
# 컷편집 파이프라인 코드에 묶이지 않게 하기 위함 (두 작업은 완전히 분리)
JUDGE_MODEL = "claude-sonnet-5"


class Issue(BaseModel):
    sent: int
    # boundary: 편 첫머리·끝 문제라 경계를 옮기면 풀릴 수 있다 / reference: 편 중간에서 다른 편이나
    # 지난 영상을 가리키는 것이라 경계로는 못 고친다 - 화면에서 둘을 다르게 보여줘 헛수고를 막는다
    kind: Literal["boundary", "reference"]
    note: str


class SegmentCheck(BaseModel):
    n: int
    verdict: Literal["ok", "warn"]
    issues: list[Issue]


class Checks(BaseModel):
    segments: list[SegmentCheck]


SYSTEM = """너는 강의 영상 시청자다. 긴 강의가 여러 편으로 나뉘었고, 너는 각 편을 **그 편 하나만** 본다고 가정한다.
편마다 그 편만 봐서 이해되는지 판정한다.

warn으로 판정할 것:
- 첫머리가 앞 편 내용을 전제한다: "그래서", "아까 말씀드린", "앞에서 본", 가리키는 대상이 이 편 안에 없는 "이/그/저" 지시어
- 이 편 안에서 설명되지 않은 개념·약어·실험을 이미 아는 것처럼 쓴다
- 끝이 정리 없이 끊기거나, 다음 편 내용 예고로 끝나 이 편의 결론이 없다

ok로 둘 것:
- 강의 안에서 "앞에서 말씀드렸듯이"로 이 편 안의 내용을 다시 가리키는 것
- 인사·채널 소개(첫 편), 맺음말·구독 안내(마지막 편)

issues마다:
- sent: 문제가 되는 문장 번호
- kind: "boundary" = 편의 첫머리나 끝에 있는 문제라 경계를 앞뒤로 옮기면 풀릴 수 있는 것 /
        "reference" = 편 중간에서 다른 편이나 지난 영상을 가리키는 것이라 경계를 옮겨도 안 풀리는 것
- note: 무엇이 왜 문제인지 한 문장
ok면 issues는 빈 목록."""


def build_doc(segs: list[dict], sents: list[dict]) -> str:
    parts = []
    for seg in segs:
        body = "\n".join(f"[{s['i']}] {s['text']}" for s in sents[seg["start_sent"]:seg["end_sent"] + 1])
        parts.append(f"=== {seg['n']}편: {seg.get('title', '')} ===\n{body}")
    return "\n\n".join(parts)


def check(folder: Path) -> Path:
    load_env()
    path = edit_dir(folder) / "segments.json"
    data = json.loads(path.read_text())
    segs, sents = data["segments"], load_sentences(folder)["sentences"]

    import anthropic
    client = anthropic.Anthropic()
    print(f"완결성 검사: {len(segs)}편 ({JUDGE_MODEL})")
    try:
        resp = client.messages.parse(model=JUDGE_MODEL, max_tokens=16000, system=SYSTEM,
                                     messages=[{"role": "user", "content": build_doc(segs, sents)}],
                                     output_format=Checks, **thinking_kwargs(JUDGE_MODEL, effort="medium"))
    except Exception as e:  # noqa: BLE001 - 검사는 보조 정보라 실패해도 분할 화면은 연다
        print(f"완결성 검사 실패 - 경고 없이 진행: {e}")
        return path
    log_llm_usage(folder, "check_standalone", JUDGE_MODEL, resp.usage)

    by_n = {c.n: c for c in resp.parsed_output.segments}
    for seg in segs:
        c = by_n.get(seg["n"])
        seg["check"] = ({"verdict": c.verdict, "issues": [i.model_dump() for i in c.issues]}
                        if c else {"verdict": "unknown", "issues": []})
    data["check_model"] = JUDGE_MODEL
    write_json(path, data)
    for seg in segs:
        ck = seg["check"]
        print(f"  {seg['n']:2d}. {ck['verdict']}" + "".join(f"\n      [{i['sent']}] {i['kind']}: {i['note']}" for i in ck["issues"]))
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    check(Path(args.folder).resolve())


if __name__ == "__main__":
    main()
