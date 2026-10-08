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
- **ffmpeg / ffprobe**, **API 키 두 개** — 아래 홈 화면의 설정 패널에서 등록·설치할 수 있습니다.
  미리 안 해둬도 되고, 빠뜨려도 Claude Code가 처음 스킬을 부를 때 알아서 확인합니다
  - [Anthropic](https://console.anthropic.com/settings/keys) — NG 판별·전체 검토에 씀
  - [ElevenLabs](https://elevenlabs.io/app/settings/api-keys) — 음성 전사(Scribe)에 씀
- **영상 넣을 폴더** — 따로 안 만들어도 됩니다. 홈 화면의 "+ 새 영상"이나 아래 CLI 환경설정이
  `video-edit/` 폴더와 안내 파일을 자동으로 만들어 줍니다

## 설치

**1. 스킬로 설치** (Claude Code):

```bash
claude plugin marketplace add imaginefutures/video-automation
claude plugin install video-cut@video-automation
```

Claude Code에서 "이 GitHub 저장소를 스킬로 설치해줘"라고 GitHub 주소만 줘도 됩니다. 플러그인
CLI를 못 쓰는 환경이라면 수동 설치도 가능합니다(이 경우 업데이트도 이 클론 위치에서 직접
`git pull`해야 합니다 — 아래 "업데이트" 참고):

```bash
git clone https://github.com/imaginefutures/video-automation.git <설치할 위치>
ln -sfn <설치할 위치> ~/.claude/skills/video-cut
```

**2. 환경설정 — 홈 화면에서 한 번에**:

```bash
uv run --directory <설치 위치> python scripts/home_server.py
```

브라우저가 자동으로 열리며 홈 화면(`http://127.0.0.1:8764`)이 뜹니다. **환경설정** 버튼으로
API 키 등록과 ffmpeg 설치(Homebrew가 있으면 버튼 클릭으로 설치)를 끝내면 준비가 끝납니다. Claude
Code에서 "컷편집 해줘"라고만 요청해도 에이전트가 필요할 때 이 화면을 띄워 안내합니다 — 이 단계를
미리 안 해둬도 됩니다.

터미널에서 직접 하고 싶거나, 영상 데이터를 스킬 설치 폴더가 아닌 다른 프로젝트 폴더에 두고 싶다면
`scripts/setup.py`도 그대로 쓸 수 있습니다:

```bash
uv run python scripts/setup.py <프로젝트 폴더 절대경로>   # 생략하면 현재 디렉터리
```

`ffmpeg`/`ffprobe` 확인(없으면 설치 명령만 알려주고 자동 설치는 안 함), API 키 확인(터미널에서
직접 돌렸을 때 없으면 그 자리에서 물어봐서 `.env`에 저장), 그 프로젝트 폴더 안에 `video-edit/` 폴더와
안내 파일(`video-edit/README.md`) 생성까지 한 번에 끝납니다.

**스크립트만 직접 실행** (Claude Code 없이):

```bash
uv run python scripts/run.py <영상 폴더 절대경로>
```

## 사용법

**더 쉬운 길 — 홈 화면**: 위에서 띄운 홈 화면에서 **+ 새 영상** 버튼을 누르고 제목을 입력한 뒤
원본 파일을 올리면, `video-edit/<제목>/raw.mp4`로 자동 저장되고 처리가 바로 시작됩니다(이 경로의
영상은 스킬 설치 폴더 자체의 `video-edit/` 아래에 쌓입니다). 처리 중인 영상·검토 중인 영상·확정된
영상이 모두 카드로 보이고, 클릭하면 이어서 검토할 수 있습니다.

**직접 하는 길 — CLI**: 영상 데이터를 원하는 위치에 두고 싶을 때 씁니다.

1. 위 `scripts/setup.py`가 프로젝트 폴더 아래 `video-edit/`를 이미 만들어 뒀습니다 —
   `<프로젝트 폴더>/videos/<이름>/raw.mp4`로 원본 영상만 넣으면 됩니다(이름은 자유, 한글도
   가능). 이 스킬이 설치된 폴더 안일 필요 없습니다. API 키(`.env`)만 스킬 설치 폴더에 공용으로
   남아있고, 영상 데이터는 원하는 곳에 둘 수 있습니다.
2. Claude Code에서 "<그 절대경로> 컷편집 해줘"라고 요청합니다(또는 위 명령을 절대경로와 함께
   직접 실행).

어느 길로 처리하든, 다음은 동일합니다:

3. 처리가 끝나면 브라우저가 자동으로 열리며 로컬 검토 화면이 뜹니다.
   - 취소선 = 이미 잘린 상태, 평범한 텍스트 = 유지. 왼쪽 사이드바의 "검토 필요" 큐에서 애매한
     항목만 살릴지 결정하면 됩니다.
   - `J`로 다음 검토 항목 이동, `Enter`로 확정, 드래그로 임의 구간 선택도 가능합니다. 전체 단축키는
     화면 우하단 `?` 버튼.
4. **확정** 버튼을 누르면 그 폴더에 `<이름>.fcpxml`과 `preview.mp4`가 생성됩니다.
5. Final Cut Pro에서 라이브러리를 열고 fcpxml 파일을 브라우저 패널로 드래그하면 타임라인이
   만들어집니다(`edit/clean.mp4`와 같은 폴더 구조를 유지해야 합니다).

## 업데이트

홈 화면의 **지금 업데이트** 버튼(커밋 안 된 변경사항이 있으면 자동으로 건너뜁니다), 또는
터미널에서:

```bash
claude plugin update video-cut
```

둘 다 적용되지 않는 수동 설치(`git clone`+`ln -sfn`)라면 그 클론 위치에서 직접 `git pull`합니다.
어느 경로든 업데이트 후에는 홈 서버를 재시작해야 반영됩니다.

## 처리 과정 (요약)

전사(ElevenLabs Scribe) → 음향 분석(피치·에너지·무음 지도, 로컬) → 화자 이탈(카메라 밖 대화) 탐지
→ NG 탐지(전체를 넓게 훑어 의심 구간을 찾고, 각 구간을 확대해 정확한 경계를 정하는 2단계 방식) →
이음새 경계를 조용한 지점으로 정밀화 + 문법·정보손실 교차 검증 → 결과 전체를 편집자/시청자 관점으로
한 번 더 통독 → 무음 리듬 다듬기 → 검토 화면.

각 단계는 `edit/` 폴더에 캐시되고, 다시 하려면 해당 파일만 지우면 됩니다. 자세한 단계별 설명과
아키텍처는 [`SKILL.md`](SKILL.md)와 [`docs/README.md`](docs/README.md)를 참고하세요.

## 문의

imaginefutures@imaginefutures.co
