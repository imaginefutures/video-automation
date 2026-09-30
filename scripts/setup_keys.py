"""API 키만 확인/설정한다 - 영상 폴더 없이 "키 설정해줘"라고만 요청받았을 때 쓴다.

`common.ensure_api_keys()`와 같은 로직을 그대로 쓴다: 사람이 터미널에서 직접 돌리면 대화식으로
물어서 `.env`에 저장하고, 이미 다 있으면 조용히 확인만 하고 끝낸다. 에이전트가 도구로 대신
실행했을 때(표준입력이 터미널이 아님) 키가 없으면 필요한 키·설명·발급 링크·`.env`의 절대경로를
출력하고 종료 코드 1로 끝난다 - 에이전트는 그 출력을 보고 대화로 물어서 직접 `.env`에 써준다
(`SKILL.md` "에이전트가 지킬 것" 참고).

Usage:
    python scripts/setup_keys.py
"""
from __future__ import annotations

from common import ensure_api_keys, load_env, PROJECT_ROOT, REQUIRED_API_KEYS
import os


def main() -> None:
    ensure_api_keys()
    load_env()
    have = [k for k, _, _ in REQUIRED_API_KEYS if os.environ.get(k)]
    print(f"확인됨: {', '.join(have)} ({PROJECT_ROOT / '.env'})")


if __name__ == "__main__":
    main()
