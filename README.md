# video-cut

한국어 강의·토킹헤드 원본 영상을 넣으면 NG(재시작·말실수)와 무음 리듬을 자동으로 다듬은 러프컷을
만들어주는 [Claude Code](https://claude.com/claude-code) 스킬입니다. 자동 처리 결과는 브라우저의
텍스트 검토 화면에서 확인·수정하고, 확정하면 Final Cut Pro용 FCPXML과 미리보기 mp4가 나옵니다.

- 판단은 텍스트로: 스크립트를 취소선(잘림)/평범한 텍스트(유지)로 보여주고, 애매한 항목만 "검토 필요"
  큐에 올립니다. 자동으로 최종 mp4까지 만들지 않습니다 — 마무리는 항상 사람이 합니다.
- 잘못 잘릴 위험이 있는 항목은 반드시 표시됩니다("오삭제는 항상 flag로 뜬다"가 이 프로젝트의 핵심
  안전 원칙입니다).

## 필요한 것

- **Claude Code** (이 스킬을 실행하는 에이전트)
- **API 키 두 개** — 처음 실행할 때 없으면 대화식으로 물어보고 `.env`에 저장해 줍니다. 직접 미리
  만들어 둘 필요 없습니다.
  - [Anthropic](https://console.anthropic.com/settings/keys) — NG 판별·전체 검토에 씀
  - [ElevenLabs](https://elevenlabs.io/app/settings/api-keys) — 음성 전사(Scribe)에 씀
- **ffmpeg / ffprobe** (시스템에 설치돼 있어야 함, `brew install ffmpeg` 등)
- **[uv](https://docs.astral.sh/uv/)** (Python 의존성 관리 — 나머지 파이썬 라이브러리는 `uv run`이
  자동으로 설치합니다)

## 설치

**스킬로 설치** (Claude Code):

```bash
git clone https://github.com/imaginefutures/video-automation.git
cd video-automation
ln -sfn "$(pwd)" ~/.claude/skills/video-cut
```

설치 후 Claude Code에서 "컷편집 해줘", "이 영상 러프컷 만들어줘" 같은 요청으로 자연스럽게 불러 쓸 수
있습니다. `.claude-plugin/plugin.json`도 있어서 플러그인 형태로 설치하는 것도 가능합니다.

**스크립트만 직접 실행** (Claude Code 없이):

```bash
uv run python scripts/run.py videos/<이름>
```

## 사용법

1. `videos/<이름>/` 폴더를 만들고 원본 영상을 그 안에 `raw.mp4`로 넣습니다(이름은 자유, 한글도
   가능).
2. Claude Code에서 "videos/<이름> 컷편집 해줘"라고 요청합니다(또는 위 명령을 직접 실행).
3. 처리가 끝나면 브라우저가 자동으로 열리며 로컬 검토 화면(`http://127.0.0.1:8765`)이 뜹니다.
   - 취소선 = 이미 잘린 상태, 평범한 텍스트 = 유지. 왼쪽 사이드바의 "검토 필요" 큐에서 애매한
     항목만 살릴지 결정하면 됩니다.
   - `J`로 다음 검토 항목 이동, `Enter`로 확정, 드래그로 임의 구간 선택도 가능합니다. 전체 단축키는
     화면 우하단 `?` 버튼.
4. **확정** 버튼을 누르면 그 폴더에 `<이름>.fcpxml`과 `preview.mp4`가 생성됩니다.
5. Final Cut Pro에서 라이브러리를 열고 fcpxml 파일을 브라우저 패널로 드래그하면 타임라인이
   만들어집니다(`edit/clean.mp4`와 같은 폴더 구조를 유지해야 합니다).

## 처리 과정 (요약)

전사(ElevenLabs Scribe) → 음향 분석(피치·에너지·무음 지도, 로컬) → 화자 이탈(카메라 밖 대화) 탐지
→ NG 탐지(전체를 넓게 훑어 의심 구간을 찾고, 각 구간을 확대해 정확한 경계를 정하는 2단계 방식) →
이음새 경계를 조용한 지점으로 정밀화 + 문법·정보손실 교차 검증 → 결과 전체를 편집자/시청자 관점으로
한 번 더 통독 → 무음 리듬 다듬기 → 검토 화면.

각 단계는 `edit/` 폴더에 캐시되고, 다시 하려면 해당 파일만 지우면 됩니다. 자세한 단계별 설명과
아키텍처는 [`SKILL.md`](SKILL.md)와 [`docs/README.md`](docs/README.md)를 참고하세요.

## 문의

imaginefutures@imaginefutures.co
