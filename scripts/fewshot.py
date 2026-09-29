"""L2 사용자 사례 저장·검색 (docs/기획/04-지식-층과-학습.md 5장) - 사용자가 실제로 결정한
사례를 few-shot으로 재사용한다.

L1(server.py의 `_pref_action_for_case` - NG 케이스별 cut/keep 성향이 충분히 쌓이고 한쪽으로
쏠리면 검토 화면 자체를 건너뛰게 만듦, 2026-09-29 두 번째 결정으로 이게 L1의 실제 구현이 됨)과
다르다 - L1은 자동 판단을 뒤집지만 통계 임계값을 넘어야만 적용되고, L2는 LLM에게 "참고 사례"로
보여주는 것뿐이라 판단 자체를 덮어쓰지 않는다. 그래서 승인 절차 없이 쌓이는 대로 바로 쓴다 - 문서
5장: "L2는 규칙이 아니라 few-shot·통계의 재료로만 쓴다."

저장: ~/.video-cut/cases/<사용자>.jsonl. 한 줄 = 결정 하나 (learn_from_session.py가 씀).
검색: 케이스(A~F)가 아니라 **텍스트 유사도**로 찾는다 - 지금 분류하려는 후보가 어떤 케이스일지는
아직 모르는 상태에서 호출되므로("이게 케이스 E다"는 결과지 입력이 아니다), "비슷한 문구를 과거에
어떻게 결정했는지"가 케이스 라벨보다 먼저 쓸 수 있는 유일한 단서다.

유사도가 SIM_MIN 밑이면 억지로 안 채운다 - 2026-09-29 프로소디 힌트 과적합 교훈과 같은 원칙:
관련 없는 예시를 넣으면 판단을 오히려 왜곡시킬 수 있으니, 신호가 없으면 없는 채로 둔다(정적
few-shot만 남는다). 최소 표본(SIM_MIN 이상 유사) 없이 아무 예시나 채우는 게 오히려 위험하다는
"학습"에 대한 이 프로젝트 전체의 입장과 일치한다.
"""
from __future__ import annotations
import difflib
import json
import os
import getpass
from pathlib import Path

from common import norm

SIM_MIN = 0.35       # 이 밑이면 "비슷한 사례 없음" - 억지로 안 채움
MAX_EXAMPLES = 3
DIRECTION_KEY = "user_action"  # "cut" | "keep" - 반대 방향 최소 1개 보장에 씀


def user_id() -> str:
    return os.environ.get("VIDEO_CUT_USER") or getpass.getuser()


def cases_path() -> Path:
    d = Path.home() / ".video-cut" / "cases"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{user_id()}.jsonl"


def append_case(case: dict) -> None:
    with open(cases_path(), "a") as f:
        f.write(json.dumps(case, ensure_ascii=False) + "\n")


def replace_video_cases(video: str, new_cases: list[dict]) -> None:
    """이 영상의 기존 L2 사례를 전부 새 것으로 교체한다 - learn_from_session.py를 같은 영상에
    재실행해도(예: 확정 후 추가로 수정하고 다시 학습) 같은 결정이 중복으로 쌓이지 않는다."""
    p = cases_path()
    kept = [c for c in load_cases() if c.get("video") != video]
    with open(p, "w") as f:
        for c in kept + new_cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")


def load_cases(stage: str | None = None, exclude_video: str | None = None) -> list[dict]:
    p = cases_path()
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        try:
            c = json.loads(line)
        except json.JSONDecodeError:
            continue
        if stage and c.get("stage") != stage:
            continue
        if exclude_video and c.get("video") == exclude_video:
            continue
        out.append(c)
    return out


def _sim(a: str, b: str) -> float:
    an, bn = norm(a).split(), norm(b).split()
    if not an or not bn:
        return 0.0
    return difflib.SequenceMatcher(None, an, bn, autojunk=False).ratio()


def retrieve(text: str, stage: str, exclude_video: str | None, k: int = MAX_EXAMPLES) -> list[dict]:
    """text와 비슷한 과거 사례 최대 k개, 최근 것 우선. 반대 방향(cut vs keep) 사례가 상위 k 안에
    하나도 없으면 하나 끼워 넣는다 - 한 방향 예시만 주면 모델이 그쪽으로 쏠린다(문서 5.1 규칙3)."""
    pool = load_cases(stage=stage, exclude_video=exclude_video)
    if not pool:
        return []
    scored = []
    for i, c in enumerate(pool):  # 파일에 쓰인 순서 = 시간 순, i가 클수록 최근
        packet_text = c.get("packet", {}).get("text", "")
        if not packet_text:
            continue
        sim = _sim(text, packet_text)
        if sim < SIM_MIN:
            continue
        recency = i / max(1, len(pool) - 1)  # 0~1, 최근일수록 1에 가까움
        scored.append((sim + recency * 0.1, sim, c))
    if not scored:
        return []
    scored.sort(key=lambda x: -x[0])

    seen_text, picked = set(), []
    for _, sim, c in scored:
        key = norm(c.get("packet", {}).get("text", ""))
        if key in seen_text:
            continue
        seen_text.add(key)
        picked.append(c)
        if len(picked) >= k:
            break

    directions = {p.get(DIRECTION_KEY) for p in picked}
    if len(directions) < 2:
        missing_dir = "keep" if "cut" in directions else "cut"
        for _, sim, c in scored:
            if c.get(DIRECTION_KEY) == missing_dir and c not in picked:
                if len(picked) >= k:
                    picked[-1] = c  # 마지막 자리를 반대 방향으로 교체
                else:
                    picked.append(c)
                break
    return picked


def format_fewshot(cases: list[dict], title: str = "이 채널 운영자의 실제 결정") -> str:
    if not cases:
        return ""
    lines = [f"\n# {title} (참고용 - 정답이 아니라 과거 판단 사례, 최종 판단은 지금 근거로 직접 하라)"]
    for c in cases:
        p = c.get("packet", {})
        auto = c.get("auto", {})
        lines.append(f'- 대상: "{p.get("text", "")}"')
        if auto.get("route"):
            lines.append(f"  자동 판단: {auto.get('route')}/{auto.get('flag')} (근거: {auto.get('reason', '')})")
        lines.append(f"  운영자 결정: {c.get('user_action')}")
    return "\n".join(lines)
