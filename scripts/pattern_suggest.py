"""Live pattern-generalization suggestions during review (PLAN.md 사용자 프로세스 LLM 적용 #2).

When the user makes the same cut/keep call on the same NG case (A-F/OTHER) enough times in
one session, this asks the LLM whether that's actually a safe, describable rule - and if so,
which of the STILL-UNDECIDED same-case REVIEW items it should apply to. The user still clicks
accept/dismiss in the UI (server.py never applies this on its own) - the LLM's job is only to
write a good suggestion and pick honest candidates, never to make the cut itself (PLAN.md 2.4:
plan and execution stay separate).

Model: claude-sonnet-5 (PLAN.md 12장/모델 선택 tier) - deciding whether a correction pattern
generalizes is the same order of semantic judgment as NG classification itself, not a lexical
check, but this only runs a handful of times per session at most.

Runs through claude_cli.py (`claude -p`, the user's paid Claude Code subscription) rather than
the Anthropic API SDK - this fires at most once per NG case per session, so the extra latency
that carries is a fine trade for not needing a separate metered API key here.
"""
from __future__ import annotations

from pydantic import BaseModel, ValidationError

from claude_cli import call_json

MODEL = "claude-sonnet-5"
MIN_TRIGGER = 3  # same case, same direction, this many user decisions before we even ask


class PatternSuggestion(BaseModel):
    generalizable: bool
    rule_text: str            # one Korean sentence for the banner
    confidence: float
    candidate_ids: list[int]  # subset of the given candidate ids the rule should also apply to


SYSTEM = """\
너는 한국어 강의 영상 편집 보조자다. 사용자가 방금 같은 NG 케이스에 대해 같은 방향(삭제/유지)으로
연속 결정을 내렸다. 이게 우연이 아니라 일반화할 수 있는 규칙인지 판단하라.

- 트리거가 된 사례들의 실제 텍스트·판별 근거를 보고, 정말 같은 이유로 같은 결정을 내린 것인지 확인하라
  (예: 전부 조사만 바뀐 형태론적 수정이라 삭제했다면 일반화 가능. 우연히 같은 case로 분류됐을 뿐
  내용이 서로 다르면 일반화 불가 - generalizable=false)
- 일반화 가능하면, 아직 결정되지 않은 후보 중 정말 같은 패턴에 해당하는 것만 candidate_ids에 담아라.
  애매한 후보는 넣지 마라 - 넣지 않은 항목은 그대로 사람이 검토한다, 손해가 아니다
- rule_text는 배너에 그대로 노출된다. 사용자가 한 줄로 이해할 수 있게 써라.
  예: "고유명사를 반복해 발음을 고르는 경우는 앞 시도를 삭제"
- 확신 없으면 generalizable=false, candidate_ids=[]로 답하라. 사람이 계속 하나씩 검토하는 것이
  기본값이고, 이 판단은 그 기본값을 건너뛸지 말지를 정하는 것뿐이다
"""


def check(case: str, action: str, trigger_items: list[dict], candidate_items: list[dict]) -> PatternSuggestion | None:
    """trigger_items: the user's own recent decisions - that's what makes this generalizable
    or not, not what the LLM originally guessed. candidate_items: still-undecided REVIEW items
    of the same case, each carrying an 'id' key matching its ng.json index."""
    if not candidate_items:
        return None

    def fmt(it: dict, with_id: bool) -> str:
        clf = it.get("llm_classification") or {}
        prefix = f"[id={it['id']}] " if with_id else "- "
        return f"{prefix}\"{it['deleted_text']}\" (근거: {clf.get('reasoning', '')})"

    prompt = f"""\
[케이스] {case}  [사용자가 내린 방향] {action.upper()}

[트리거 - 사용자가 실제로 이렇게 결정한 사례들]
{chr(10).join(fmt(it, False) for it in trigger_items)}

[아직 결정 안 된 같은 케이스 후보들]
{chr(10).join(fmt(it, True) for it in candidate_items)}

JSON 스키마: {{"generalizable": bool, "rule_text": str, "confidence": float, "candidate_ids": [int]}}
"""
    data = call_json(SYSTEM, prompt, MODEL)
    if not data:
        return None
    try:
        out = PatternSuggestion(**data)
    except ValidationError as e:
        print(f"pattern_suggest: bad JSON from claude -p: {e}")
        return None
    if not out.generalizable or not out.candidate_ids:
        return None
    valid_ids = {it["id"] for it in candidate_items}
    out.candidate_ids = [i for i in out.candidate_ids if i in valid_ids]
    return out if out.candidate_ids else None
