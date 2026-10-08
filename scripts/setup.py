"""전체 환경 점검/설정 - "설정해줘"/"키 설정해줘"라고 요청받았을 때, 또는 새 프로젝트 폴더를
시작할 때 한 번에 쓴다.

네 가지를 한 호출로 처리한다: API 키(`common.ensure_api_keys()`), `ffmpeg`/`ffprobe`(시스템
바이너리, `shutil.which`로 확인), 영상 프로젝트 폴더에 `video-edit/` + 안내 파일 생성. `uv` 자체는
여기서 확인 안 한다 - 이 스크립트가 실행됐다는 것 자체가 uv가 이미 있다는 뜻이라 부트스트랩
문제라서, uv 유무는 에이전트가 이 스크립트를 실행하기 *전에* `which uv`로 직접 확인해야 한다
(`SKILL.md` "에이전트가 지킬 것" 참고).

사람이 터미널에서 직접 돌리면 API 키는 대화식으로 물어서 저장하고, ffmpeg가 없으면 설치 명령만
알려준다(시스템 패키지 설치는 자동으로 안 함 - 사용자 확인 필요). 에이전트가 도구로 대신
실행했을 때(표준입력이 터미널이 아님) 키가 없으면 종료 코드 1로 멈추고 필요한 정보를 출력한다
(`ensure_api_keys()`가 이미 그렇게 함).

`video-edit/`는 인자로 받은 프로젝트 폴더(기본값: 현재 작업 디렉터리) 아래에 만든다 - 스킬 설치
위치(`PROJECT_ROOT`)가 아니라 사용자가 실제로 영상을 두고 싶어하는 곳이라, 에이전트가 항상
사용자의 작업 폴더 절대경로를 인자로 넘겨야 한다. 이미 있으면 손대지 않는다(안내 파일도 없을 때만
새로 씀 - 사용자가 지운 거면 존중).

Usage:
    python scripts/setup.py [프로젝트 폴더 절대경로]   # 생략하면 현재 작업 디렉터리
"""
from __future__ import annotations
import shutil
import sys

from common import VIDEO_EDIT_DIR, ensure_api_keys, load_env, migrate_work_dirs, PROJECT_ROOT, REQUIRED_API_KEYS
import os
from pathlib import Path

import migrate

FFMPEG_BINS = [
    ("ffmpeg", "brew install ffmpeg   # macOS. 다른 OS는 https://ffmpeg.org/download.html 참고"),
    ("ffprobe", "brew install ffmpeg   # ffmpeg에 포함돼 있어 따로 설치 안 해도 됨"),
]

VIDEOS_GUIDE = """# 여기에 원본 영상 넣기

영상마다 폴더를 하나 만들고 그 안에 `raw.mp4`로 넣으세요:

    video-edit/<이름>/raw.mp4

예: `video-edit/강의1/raw.mp4` (이름은 자유, 한글도 가능)

넣은 뒤 Claude Code에서 이렇게 요청하세요:

    video-edit/<이름> 컷편집 해줘
"""


def setup_videos_folder(project_dir: Path) -> None:
    migrate_work_dirs(project_dir)  # 예전 setup이 만든 <프로젝트>/videos/ -> video-edit/
    videos = project_dir / VIDEO_EDIT_DIR
    videos.mkdir(exist_ok=True)
    guide = videos / "README.md"
    if guide.exists():
        print(f"video-edit/ 확인됨 ({videos})")
        return
    guide.write_text(VIDEOS_GUIDE)
    print(f"video-edit/ 폴더를 만들었습니다: {videos}\n  -> 여기에 <이름>/raw.mp4로 원본을 넣으세요 (video-edit/README.md 참고)")


def install_git_hooks() -> None:
    """docs/교체-절차.md 5번: 매뉴얼/문서 동기화 필수 필드를 강제하는 commit-msg 훅을
    설치/갱신한다. .git/hooks는 버전관리 밖이라 setup.py 호출마다 다시 복사해야 최신으로
    유지된다. 스킬 저장소(PROJECT_ROOT)가 git 저장소가 아니면(예: 일부 배포 경로) 조용히 넘어간다."""
    git_dir = PROJECT_ROOT / ".git"
    src = PROJECT_ROOT / "scripts" / "hooks" / "commit-msg"
    if not git_dir.is_dir() or not src.exists():
        return
    dst = git_dir / "hooks" / "commit-msg"
    dst.parent.mkdir(exist_ok=True)
    dst.write_text(src.read_text())
    dst.chmod(0o755)
    print(f"commit-msg 훅 설치/갱신됨 ({dst})")


def main() -> None:
    project_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()

    install_git_hooks()
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

    setup_videos_folder(project_dir)

    for msg in migrate.migrate_global():  # 업데이트 뒤 ~/.video-cut/ 호환성 확인 (1회)
        print(f"[migrate] {msg}")


if __name__ == "__main__":
    main()
