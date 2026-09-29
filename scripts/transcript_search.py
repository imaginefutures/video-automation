"""Semantic transcript search (PLAN.md 사용자 프로세스 LLM 적용 #4).

The review UI's search box does instant literal substring matching client-side first (free,
no latency, works for any exact phrase). Only when that finds zero hits does it fall back to
this: a whole-transcript semantic search for queries like "화자 이탈 구간만" or "숫자 나오는 데"
that describe content rather than quote it.

Model: claude-sonnet-5 - matching a natural-language description against transcript content
is the same semantic-judgment tier as NG classification, not a lexical lookup (PLAN.md 12장).

Runs through claude_cli.py (`claude -p`, the user's paid Claude Code subscription) rather than
the Anthropic API SDK - this only fires when the client-side literal search misses, so the
extra latency is a fine trade for not needing a separate metered API key here.
"""
from __future__ import annotations

from pydantic import BaseModel, ValidationError

from claude_cli import call_json

MODEL = "claude-sonnet-5"
MAX_MATCHES = 20


class SearchMatch(BaseModel):
    wi_start: int
    wi_end: int  # exclusive
    reason: str  # one short phrase, shown as a tooltip on the highlighted match


class SearchResult(BaseModel):
    matches: list[SearchMatch]


SYSTEM = """\
너는 한국어 강의 영상 트랜스크립트에서 사용자의 자연어 질의에 맞는 구간을 찾는다. 아래는 줄 단위
트랜스크립트다(단어 id(wi) 구간 [반열림]·시작초·화자 포함). 질의에 맞는 줄(들)을 찾아 시작/끝 단어
id와 왜 맞는지 짧은 근거를 답하라. 문자 그대로 일치가 아니라 의미로 찾아라
(예: "숫자 나오는 데" -> 숫자·통계가 언급된 줄, "화자 이탈" -> 화자가 2명 이상인 줄,
"셀리그만 얘기하는 부분" -> 그 인물이 언급되거나 그 이론을 설명하는 줄).
너무 많으면 가장 확실한 20개만 반환하고, 질의와 안 맞으면 matches를 빈 리스트로 반환하라.
"""


def search(words: list[dict], query: str) -> list[dict]:
    from detect_speaker_blocks import split_lines

    lines = split_lines(words)
    packed = "\n".join(f"[{ln['wi_start']}-{ln['wi_end']}] ({ln['start']:.0f}s, {ln['speaker']}) {ln['text']}"
                       for ln in lines)
    prompt = (f"[질의]\n{query}\n\n[트랜스크립트]\n{packed}\n\n"
              'JSON 스키마: {"matches": [{"wi_start": int, "wi_end": int, "reason": str}]}')
    data = call_json(SYSTEM, prompt, MODEL, timeout=90)
    if not data:
        return []
    try:
        out = SearchResult(**data)
    except ValidationError as e:
        print(f"transcript_search: bad JSON from claude -p: {e}")
        return []
    return [m.model_dump() for m in out.matches[:MAX_MATCHES]]
