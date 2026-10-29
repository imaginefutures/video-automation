"""바탕화면에 "홈 서버 켜기" / "홈 서버 끄기" 아이콘(.app) 두 개를 만든다. 맥 전용.

아이콘은 AppleScript 앱(osacompile)이고, 누르면 `scripts/home_on.sh` / `home_off.sh`를 부른다.
스킬 설치 위치는 사람마다 다르고 플러그인을 업데이트하면 바뀔 수도 있어서, 앱이 저장소를 직접
가리키지 않고 `~/Library/Application Support/video-cut/launch.sh`를 거친다. 이 파일이 기록된
저장소 경로를 먼저 보고, 없어졌으면 플러그인 설치 폴더에서 가장 최근 것을 찾는다. 그것도
없으면 다시 설치하라는 안내를 띄운다. 이 스크립트를 다시 돌리면 경로 기록과 아이콘이 갱신된다.

Usage:
    uv run python scripts/install_desktop_icons.py [--dest 아이콘을 둘 폴더]   # 기본값: 바탕화면
"""
from __future__ import annotations
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SUPPORT = Path(os.environ.get("VIDEO_CUT_SUPPORT") or Path.home() / "Library" / "Application Support" / "video-cut")  # 시험할 때 바꾼다
LAUNCH = SUPPORT / "launch.sh"

LAUNCH_SH = """#!/bin/bash
# 바탕화면 아이콘이 거치는 길잡이. install_desktop_icons.py가 만든다 - 직접 고치지 않는다.
# 사용: launch.sh on|off
WHICH="$1"
REPO="$(cat "$(dirname "$0")/repo" 2>/dev/null)"
if [ ! -x "$REPO/scripts/home_$WHICH.sh" ]; then
  # 플러그인 업데이트로 경로가 바뀌었을 수 있다 - 설치 폴더에서 가장 최근 것을 찾는다
  FOUND="$(ls -t "$HOME"/.claude/plugins/cache/*/video-cut/*/scripts/home_"$WHICH".sh "$HOME"/.claude/skills/video-cut/scripts/home_"$WHICH".sh 2>/dev/null | head -1)"
  [ -n "$FOUND" ] && REPO="$(cd "$(dirname "$FOUND")/.." && pwd)"
fi
if [ ! -x "$REPO/scripts/home_$WHICH.sh" ]; then
  echo "video-cut 설치 위치를 찾지 못했어요 - Claude Code에서 '바탕화면 아이콘 만들어줘'를 다시 실행해 주세요"
  exit 1
fi
exec "$REPO/scripts/home_$WHICH.sh"
"""

# 켜기는 화면이 브라우저에서 열리니 성공하면 조용히, 실패만 알린다. 끄기는 결과 문장을 보여 준다
APPS = {
    "홈 서버 켜기": """try
	do shell script {launch} & " on"
on error errMsg
	display dialog errMsg buttons {{"확인"}} default button "확인" with icon stop
end try
""",
    "홈 서버 끄기": """try
	set msg to do shell script {launch} & " off || true"
	display dialog msg buttons {{"확인"}} default button "확인"
on error errMsg
	display dialog errMsg buttons {{"확인"}} default button "확인" with icon stop
end try
""",
}


def applescript_string(s: str) -> str:
    """AppleScript 문자열 리터럴로 만든다. 경로의 공백은 셸이 쪼개지 않게 작은따옴표로 감싼다."""
    quoted = "'" + s.replace("'", "'\\''") + "'"
    return '"' + quoted.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dest", type=Path, default=Path.home() / "Desktop", help="아이콘을 둘 폴더(기본값: 바탕화면)")
    args = ap.parse_args()

    if sys.platform != "darwin":
        print("맥에서만 쓸 수 있어요")
        return 1
    if not shutil.which("osacompile"):
        print("osacompile을 찾지 못했어요 - macOS 기본 도구라 보통 있어야 합니다")
        return 1
    args.dest.mkdir(parents=True, exist_ok=True)

    SUPPORT.mkdir(parents=True, exist_ok=True)
    (SUPPORT / "repo").write_text(str(REPO) + "\n", encoding="utf-8")
    LAUNCH.write_text(LAUNCH_SH, encoding="utf-8")
    LAUNCH.chmod(0o755)

    for name, template in APPS.items():
        app = args.dest / f"{name}.app"
        if app.exists():
            shutil.rmtree(app)  # 같은 이름의 옛 아이콘은 새로 덮는다
        with tempfile.NamedTemporaryFile("w", suffix=".applescript", delete=False, encoding="utf-8") as f:
            f.write(template.format(launch=applescript_string(str(LAUNCH))))
        try:
            subprocess.run(["osacompile", "-o", str(app), f.name], check=True)
        finally:
            Path(f.name).unlink(missing_ok=True)
        print(f"만들었어요: {app}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
