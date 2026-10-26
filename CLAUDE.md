# video-cut

한국어 강의·토킹헤드 원본 영상의 NG(재시작·말실수)와 무음을 다듬은 러프컷을 만드는 Claude Code 스킬 플러그인이다. 파이썬(`uv run`), 로컬 검토 화면(`web/`), 출력은 FCPXML과 미리보기 mp4. 저장소 자체가 플러그인이라 [SKILL.md](SKILL.md)가 제품이다.

공통 개발 규칙(일하는 법·코드 규칙·팀 원칙·스킬)은 스튜디오 플러그인 팀 문서가 맡는다. 이 문서는 이 프로젝트의 값만 둔다.

## 일을 시작하기 전에

1. **[docs/README.md](docs/README.md)(문서 지도)를 본다.** 각 설계 문서가 스스로 진행 상태(✅/🔄/📝/⬜/⏳)를 표시한다.
2. **바뀌지 않는 원칙은 [docs/서비스-개요와-철학.md](docs/서비스-개요와-철학.md)다.** 핵심 안전 원칙: 오삭제는 항상 flag로 뜬다. 마무리(확정)는 사람이 한다.
3. **설치·사용법은 [README.md](README.md), 파이프라인과 에이전트 안내는 [SKILL.md](SKILL.md)다.**

## 검증 명령

자동 시험 묶음은 없다. NG 판별을 바꾸면 `scripts/eval_against_gold.py`로 정답지 대조를 돌리고 결과를 `docs/현재-설계/검증-결과-*.md`에 남긴다. 화면·스크립트 변경은 `uv run python scripts/home_server.py`로 띄워 확인한다.

## 지킬 것

- 확인받고 하는 일은 [CONTRIBUTING.md](CONTRIBUTING.md)다.
- 기존 기능을 대체하는 절차와 커밋 줄(`매뉴얼:`·`문서:`, `scripts/hooks/commit-msg`가 검사)은 [docs/교체-절차.md](docs/교체-절차.md)다.
- `edit/*.json` 구조를 바꾸면 [docs/업데이트와-마이그레이션.md](docs/업데이트와-마이그레이션.md) 절차(`SCHEMA_VERSIONS` + `MIGRATIONS`)를 따른다.

## 문서 지도

주제를 다루는 문서가 있으면 먼저 읽고 따른다. "스튜디오"는 스튜디오가 주인이라 이 저장소에서 고치지 않는다(고칠 일이면 그 저장소에서 고친다).

| 문서 | 주인 | 볼 때 |
|---|---|---|
| [README.md](README.md) | 프로젝트 | 설치·사용법 |
| [docs/README.md](docs/README.md) | 프로젝트 | 설계 문서 목록과 상태 |
| [docs/project.md](docs/project.md) | 프로젝트 | 스튜디오 팀 문서가 말하는 프로젝트 값이 있는 곳 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 프로젝트 | 하기 전에 확인받는 일 |
| 스튜디오 팀 문서 | 스튜디오 | 일하는 순서·커밋 줄·새 기능 점검표(work), 코드 규칙(code-rules), 서브에이전트(agents), 스킬 지도(skills), 화면·TS·SQL(web). 위치는 세션 시작 때 알림 |
<!-- dev-env:preset-docs -->
| [docs/결정-이력.md](docs/결정-이력.md) | 프로젝트 | 날짜별 결정과 사건(이 프로젝트는 `docs/adr/` 대신 이 기록을 쓴다) |
