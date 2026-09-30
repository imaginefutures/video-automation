"""전체 환경 점검/설정 - 영상 폴더 없이 "설정해줘"/"키 설정해줘"라고만 요청받았을 때 쓴다.

세 가지를 확인한다: API 키(`common.ensure_api_keys()`), `ffmpeg`/`ffprobe`(시스템 바이너리,
`shutil.which`로 확인). `uv` 자체는 여기서 확인 안 한다 - 이 스크립트가 실행됐다는 것 자체가 uv가
이미 있다는 뜻이라 부트스트랩 문제라서, uv 유무는 에이전트가 이 스크립트를 실행하기 *전에*
`which uv`로 직접 확인해야 한다(`SKILL.md` "에이전트가 지킬 것" 참고).

사람이 터미널에서 직접 돌리면 API 키는 대화식으로 물어서 저장하고, ffmpeg가 없으면 설치 명령만
알려준다(시스템 패키지 설치는 자동으로 안 함 - 사용자 확인 필요). 에이전트가 도구로 대신
실행했을 때(표준입력이 터미널이 아님) 키가 없으면 종료 코드 1로 멈추고 필요한 정보를 출력한다
(`ensure_api_keys()`가 이미 그렇게 함).

Usage:
    python scripts/setup.py
"""
from __future__ import annotations
import shutil

from common import ensure_api_keys, load_env, PROJECT_ROOT, REQUIRED_API_KEYS
import os

FFMPEG_BINS = [
    ("ffmpeg", "brew install ffmpeg   # macOS. 다른 OS는 https://ffmpeg.org/download.html 참고"),
    ("ffprobe", "brew install ffmpeg   # ffmpeg에 포함돼 있어 따로 설치 안 해도 됨"),
]


def main() -> None:
    ensure_api_keys()  # 없으면 여기서 (대화식 또는 명확한 에러로) 처리하고 넘어옴
    load_env()
    have = [k for k, _, _ in REQUIRED_API_KEYS if os.environ.get(k)]
    print(f"API 키 확인됨: {', '.join(have)} ({PROJECT_ROOT / '.env'})")

    missing_bins = [(b, cmd) for b, cmd in FFMPEG_BINS if not shutil.which(b)]
    if missing_bins:
        print("\n다음 프로그램이 시스템에 없습니다 - 아래 명령으로 설치해야 합니다:")
        for b, cmd in missing_bins:
            print(f"  {b}: {cmd}")
    else:
        print("ffmpeg/ffprobe 확인됨")


if __name__ == "__main__":
    main()
