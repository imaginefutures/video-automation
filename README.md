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
- **[uv](https://docs.astral.sh/uv/)** — 없으면 스킬을 아예 실행할 수 없어 자동 확인이 안 됩니다.
  미리 설치해 두세요(`curl -LsSf https://astral.sh/uv/install.sh | sh`). 나머지 파이썬
  라이브러리는 `uv run`이 알아서 설치합니다
- **ffmpeg / ffprobe**, **API 키 두 개** — 아래 설치 2단계(`scripts/setup.py`)가 확인해 줍니다.
  미리 안 해둬도 되고, 빠뜨려도 Claude Code가 처음 스킬을 부를 때 알아서 확인합니다
  - [Anthropic](https://console.anthropic.com/settings/keys) — NG 판별·전체 검토에 씀
  - [ElevenLabs](https://elevenlabs.io/app/settings/api-keys) — 음성 전사(Scribe)에 씀
- **영상 넣을 폴더** — 따로 안 만들어도 됩니다. 아래 설치 2단계가 프로젝트 폴더 안에 `videos/`
  폴더와 안내 파일을 자동으로 만들어 줍니다

## 설치

**1. 스킬로 설치** (Claude Code):

```bash
git clone https://github.com/imaginefutures/video-automation.git <설치할 위치>
ln -sfn <설치할 위치> ~/.claude/skills/video-cut
```

Claude Code에서 "이 GitHub 저장소를 스킬로 설치해줘"라고 GitHub 주소만 줘도 됩니다 —
`.claude-plugin/plugin.json`도 있어서 플러그인 형태로 설치하는 것도 가능합니다.

**2. 환경설정** — 설치 직후, 첫 영상을 넣기 전에 프로젝트 폴더를 정하고 한 번 해두세요:

```bash
uv run python scripts/setup.py <프로젝트 폴더 절대경로>   # 생략하면 현재 디렉터리
```

`ffmpeg`/`ffprobe` 확인(없으면 설치 명령만 알려주고 자동 설치는 안 함), API 키 확인(터미널에서
직접 돌렸을 때 없으면 그 자리에서 물어봐서 `.env`에 저장), 그 프로젝트 폴더 안에 `videos/` 폴더와
안내 파일(`videos/README.md`) 생성까지 한 번에 끝납니다. **이 단계를 건너뛰어도 됩니다** — Claude
Code에서 스킬을 처음 부를 때 빠진 게 있으면 Claude가 대화 중에 알아서 확인하고 처리해주는 보완
절차가 있습니다(누락 방지용 안전망이지, 이게 주 경로는 아닙니다).

**스크립트만 직접 실행** (Claude Code 없이):

```bash
uv run python scripts/run.py <영상 폴더 절대경로>
```

## 사용법

1. 위 설치 2단계(`scripts/setup.py`)가 프로젝트 폴더 아래 `videos/`를 이미 만들어 뒀습니다 —
   `<프로젝트 폴더>/videos/<이름>/raw.mp4`로 원본 영상만 넣으면 됩니다(이름은 자유, 한글도
   가능). 이 스킬이 설치된 폴더 안일 필요 없습니다. API 키(`.env`)만 스킬 설치 폴더에 공용으로
   남아있고, 영상 데이터는 원하는 곳에 둘 수 있습니다.
2. Claude Code에서 "<그 절대경로> 컷편집 해줘"라고 요청합니다(또는 위 명령을 절대경로와 함께
   직접 실행).
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
