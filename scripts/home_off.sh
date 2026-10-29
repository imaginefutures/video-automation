#!/bin/bash
# 바탕화면 "홈 서버 끄기" - 홈 서버와 분할 화면 서버를 끈다. 영상 처리 중이면 끄지 않고 이유를 알린다.
PORT=8764

if ! curl -s -o /dev/null --max-time 2 "http://localhost:$PORT/"; then
  echo "홈 서버는 이미 꺼져 있어요"
  exit 0
fi

RES=$(curl -s -X POST --max-time 5 -H 'Content-Type: application/json' -d '{}' "http://localhost:$PORT/api/shutdown")
if ! echo "$RES" | python3 -c 'import json,sys; sys.exit(0 if json.load(sys.stdin).get("ok") else 1)' 2>/dev/null; then
  # 처리 중이면 서버가 이유를 JSON으로 돌려준다. 그 밖에는(옛 서버 등) 응답 원문을 그대로 보여준다
  echo "$RES" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("error", "끄지 못했습니다"))
except Exception: print("끄지 못했습니다 - 응답이 없거나 옛 버전 서버입니다")' 2>/dev/null || echo "끄지 못했습니다"
  exit 1
fi

for _ in $(seq 1 20); do
  sleep 0.5
  if ! curl -s -o /dev/null --max-time 1 "http://localhost:$PORT/"; then
    echo "홈 서버를 껐어요"
    exit 0
  fi
done
echo "끄는 중인데 아직 응답해요 - 잠시 뒤 다시 확인해 주세요"
exit 1
