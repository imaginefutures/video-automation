"""세션에서 배우기 (docs/기획/04-지식-층과-학습.md의 L1 실현 방법, 2026-09-29 두 번째 결정).

처음엔 LLM이 "일반화할 수 있는 규칙 후보"를 제안하고 사람이 승인해야 적용되는 L1 계층
(`rule_candidates`, 승인 화면 필요)을 따로 만들려 했다. 그런데 `server.py`가 검토 화면을 도는
동안 이미 자체적으로 `_pref_action_for_case()`를 만들어 뒀다는 걸 뒤늦게 발견함 - NG 케이스별
cut/keep 횟수를 세다가 표본이 충분하고(`PREFS_MIN_SAMPLES`) 한쪽으로 확실히 쏠리면
(`PREFS_MIN_RATIO`) 승인 화면 없이 그 자리에서 바로 적용한다. 목적이 완전히 겹쳤고 이미 실제
검토 세션마다 자동으로 돌고 있어 검증도 더 되어 있었다 - 그래서 승인 대기 규칙(`rule_candidates`)
계층은 폐기하고 그 쪽으로 통합했다 (원칙 3: 기존 기능 대체 시 흔적을 같은 작업에서 지운다).

이 스크립트가 지금 하는 일 둘만 남았다:
  1. `decisions.json`의 모든 실제 사람 결정(ng 항목 + range override)을 `fewshot.py`의 L2
     사례로 저장한다 - `classify_candidates.py`가 다음 영상 분류 때 바로 검색해 쓴다. 승인 불필요
     (L2는 few-shot 참고자료일 뿐 자동 판단을 뒤집지 않는다).
  2. 사람이 읽는 "이번 영상에서 뭘 배웠는지" 요약을 LLM 한 번으로 만들어
     `~/.video-cut/learning-log/<사용자>.md`에 영상마다 한 섹션씩 남긴다.
  3. 증거가 부족하면(결정 < MIN_EVIDENCE) 요약할 것도 마땅치 않으니 LLM을 아예 안 부른다.

NG 케이스별 cut/keep 성향 자체는 이 스크립트가 아니라 `server.py`가 검토 중에 실시간으로,
즉시(다음 REVIEW 항목부터) 배운다 - 이 스크립트를 따로 돌리지 않아도 이미 작동한다.

Usage:
    python scripts/learn_from_session.py <videos/NAME>
"""
from __future__ import annotations
import argparse
import json
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel

from common import load_env, video_dir, edit_dir, words_only, load_transcript
import fewshot

MODEL = "claude-sonnet-5"          # pattern_suggest.py와 같은 티어 - "일반화되는가" 판단은 NG 분류급
MIN_EVIDENCE = 3                   # server.py의 PREFS_MIN_SAMPLES와 동일 기준, 하드 플로어


def user_id() -> str:
    import os, getpass
    return os.environ.get("VIDEO_CUT_USER") or getpass.getuser()


def log_path() -> Path:
    d = Path.home() / ".video-cut" / "learning-log"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{user_id()}.md"


# --------------------------------------------------------------------------------- 수집

def collect_ng_decisions(decisions: dict, ng_items: list[dict]) -> list[dict]:
    out = []
    for i_str, dec in decisions.get("ng", {}).items():
        if dec.get("by") != "user":
            continue
        i = int(i_str)
        if i >= len(ng_items):
            continue
        item = ng_items[i]
        clf = item.get("llm_classification") or {}
        out.append({
            "kind": "ng", "case": clf.get("case") or item.get("label"),
            "auto_route": item.get("route"), "auto_flag": item.get("flag"),
            "auto_reason": item.get("route_reason", ""), "auto_confidence": clf.get("confidence"),
            "text": item.get("deleted_text", ""),
            "user_action": dec.get("action"),
            "agreed_with_auto": (dec.get("action") == "cut") == (item.get("flag") is not None or item.get("route") == "CUT"),
        })
    return out


def collect_overrides(decisions: dict, ng_items: list[dict], words: list[dict]) -> list[dict]:
    """모든 range override는 정의상 사람이 한 것 - decisions.json의 overrides 리스트 전체."""
    out = []
    for ov in decisions.get("overrides", []):
        wi_s, wi_e = ov.get("wi_start"), ov.get("wi_end")
        text = None
        if wi_s is not None and wi_e is not None:
            seg = [w for w in words if wi_s <= w["wi"] <= wi_e]
            text = " ".join(w["text"] for w in seg) if seg else None
        # 이 구간을 자동이 이미 뭐라고 제안했었는지 찾기(있으면)
        matched = None
        if wi_s is not None:
            for it in ng_items:
                if it["raw_word_index_start"] <= wi_s < it["raw_word_index_end"]:
                    matched = it
                    break
        out.append({
            "kind": "override", "op": ov.get("op"), "text": text,
            "start": ov.get("start"), "end": ov.get("end"),
            "auto_route": matched.get("route") if matched else None,
            "auto_flag": matched.get("flag") if matched else None,
            "auto_reason": matched.get("route_reason", "") if matched else "(자동 제안과 무관한 수동 편집)",
        })
    return out


# --------------------------------------------------------------------------------- LLM

class SessionLearning(BaseModel):
    summary: str


SYSTEM = """\
너는 이 채널 운영자의 편집 취향을 분석하는 어시스턴트다. 아래는 이번 영상에서 사람이 실제로 내린
결정과, 그때 자동 시스템이 뭐라고 왜 제안했는지를 짝지은 목록이다. 자동과 같은 결정(자동 판단이
맞았음을 확인)과 다른 결정(자동이 틀렸거나 애매했음)이 섞여 있다.

summary 하나만 써라: 사람이 읽을 "이번 영상에서 무엇을 배웠는지" 한두 문단. 통계 나열 말고, 실제로
어떤 판단 성향이 보였는지 서술하라. 이 요약은 기록용이지 자동 판단에 반영되지 않는다 - 성향이 뚜렷한
게 보여도 "다음부터 이렇게 하겠다" 식으로 규칙을 만들어 제안하지 말고 관찰만 서술하라.
"""


def build_prompt(evidence: list[dict]) -> str:
    lines = []
    for i, e in enumerate(evidence):
        if e["kind"] == "ng":
            lines.append(f"[{i}] NG case={e['case']} 자동제안={e['auto_route']}/{e['auto_flag']} "
                         f"(신뢰도={e['auto_confidence']}, 근거: {e['auto_reason']})\n"
                         f"    텍스트: {e['text'][:80]}\n"
                         f"    사람 결정: {e['user_action']} ({'자동과 일치' if e['agreed_with_auto'] else '자동과 다름'})")
        else:
            lines.append(f"[{i}] 수동 편집 op={e['op']} 자동제안={e['auto_route']}/{e['auto_flag']} "
                         f"(근거: {e['auto_reason']})\n    텍스트: {e['text'][:80] if e['text'] else '(범위 정보 없음)'}")
    return "\n".join(lines)


def learn(evidence: list[dict]) -> SessionLearning:
    import anthropic
    client = anthropic.Anthropic()
    resp = client.messages.parse(model=MODEL, max_tokens=3000, system=SYSTEM,
                                 messages=[{"role": "user", "content": build_prompt(evidence)}],
                                 output_format=SessionLearning, thinking={"type": "disabled"})
    return resp.parsed_output


# --------------------------------------------------------------------------------- 저장

def save_fewshot_cases(folder: Path, evidence: list[dict]) -> int:
    """모든 사람 결정을 L2 사례로 저장한다(fewshot.py) - LLM 규칙 요약이 표본 부족으로 안
    돌아도, 개별 사례는 표본 1개짜리 few-shot으로는 여전히 쓸모 있다(규칙 일반화와 few-shot
    재사용은 필요한 확신 수준이 다르다 - 문서 상단 설명 참고). 같은 영상을 다시 돌리면(예: 확정
    후 더 수정하고 재학습) 이 영상의 예전 사례를 전부 새 것으로 교체한다 - append만 하면 재실행
    때마다 같은 결정이 중복으로 쌓인다(미결 사항으로 지적됨)."""
    now = datetime.now().isoformat(timespec="seconds")
    cases = []
    for e in evidence:
        text = e.get("text")
        if not text:
            continue
        user_action = e.get("user_action") if e["kind"] == "ng" else e.get("op")
        if user_action not in ("cut", "keep"):
            continue
        cases.append({
            "video": folder.name, "ts": now, "stage": "ng",
            "case": e.get("case"),
            "packet": {"text": text},
            "auto": {"route": e.get("auto_route"), "flag": e.get("auto_flag"), "reason": e.get("auto_reason")},
            "user_action": user_action,
        })
    fewshot.replace_video_cases(folder.name, cases)
    if cases:
        print(f"L2 사례 {len(cases)}건을 {fewshot.cases_path()}에 반영함(이 영상의 예전 사례는 교체됨, few-shot 검색에 바로 쓰임, 승인 불필요)")
    return len(cases)


def save(folder: Path, evidence: list[dict], result: SessionLearning | None) -> None:
    save_fewshot_cases(folder, evidence)
    now = datetime.now().isoformat(timespec="seconds")

    if result:
        body = f"{result.summary}\n\n"
    else:
        body = (f"사람이 직접 내린 결정이 {len(evidence)}건뿐이라({MIN_EVIDENCE}건 미만) 이번엔 요약을 "
                f"건너뜀. LLM을 부르지 않음 — 적은 데이터로 억지로 서술하지 않는 게 원칙.\n\n")
    section = f"## {folder.name} — {now[:10]}\n\n{body}"

    lp = log_path()
    existing = lp.read_text() if lp.exists() else ""
    sections = [s for s in existing.split("---\n\n") if s.strip()]
    marker = f"## {folder.name} — "
    sections = [s for s in sections if not s.startswith(marker)]  # 이 영상의 예전 섹션 제거(재실행 시 중복 방지)
    sections.append(section)
    lp.write_text("---\n\n".join(sections) + "---\n\n")
    print(f"학습 기록을 {lp}에 반영함(이 영상의 예전 섹션은 교체됨)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    load_env()
    folder = video_dir(args.folder)
    edit = edit_dir(folder)

    decisions = json.loads((edit / "decisions.json").read_text())
    ng_items = json.loads((edit / "ng.json").read_text()) if (edit / "ng.json").exists() else []
    words = words_only(load_transcript(folder))

    evidence = collect_ng_decisions(decisions, ng_items) + collect_overrides(decisions, ng_items, words)
    print(f"사람이 내린 결정: {len(evidence)}건 (ng 직접결정 + 수동 override 전체)")

    if len(evidence) < MIN_EVIDENCE:
        print(f"  {MIN_EVIDENCE}건 미만 - LLM 호출 없이 종료")
        save(folder, evidence, None)
        return

    result = learn(evidence)
    print(f"\n요약: {result.summary}")

    save(folder, evidence, result)


if __name__ == "__main__":
    main()
