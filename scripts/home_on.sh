#!/bin/bash
# 바탕화면 "홈 서버 켜기" - 홈 서버가 꺼져 있으면 띄우고 홈 화면을 연다. 이미 떠 있으면 화면만 연다.
REPO="$(cd "$(dirname "$0")/.." && pwd)"  # 설치 위치가 사람마다 달라서 스크립트 자기 위치로 정한다
PORT=8764
LOG="$HOME/Library/Logs/video-automation-home.log"  # 앱으로 띄우면 터미널이 없어서 로그를 파일로 남긴다
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"  # 앱으로 띄우면 PATH가 거의 비어 있다

if ! curl -s -o /dev/null --max-time 2 "http://localhost:$PORT/"; then
  UV="$(command -v uv)" || { echo "uv가 없어요 - 터미널에서 curl -LsSf https://astral.sh/uv/install.sh | sh 를 먼저 실행해 주세요"; exit 1; }
  mkdir -p "$(dirname "$LOG")"
  cd "$REPO" || exit 1
  nohup "$UV" run --directory "$REPO" python scripts/home_server.py --no-open >> "$LOG" 2>&1 < /dev/null &
  for _ in $(seq 1 40); do
    sleep 0.5
    curl -s -o /dev/null --max-time 1 "http://localhost:$PORT/" && break
  done
  if ! curl -s -o /dev/null --max-time 1 "http://localhost:$PORT/"; then
    echo "홈 서버를 켜지 못했어요 - 로그: $LOG"
    exit 1
  fi
fi
open "http://localhost:$PORT/"
