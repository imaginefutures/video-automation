---
name: video-cut
description: 강의 원본의 러프컷을 교정 표시된 원고처럼 읽고 확정하는 로컬 검토 도구
colors:
  proof-white: "#ffffff"
  margin-gray: "#fafafa"
  galley-gray: "#f5f5f5"
  press-ink: "#171717"
  pencil-gray: "#666666"
  hairline: "#ebebeb"
  rule-gray: "#a1a1a1"
  struck-gray: "#a1a1a1"
  query-wash: "#ffefcf"
  query-amber: "#ab570a"
  gauge-track: "#f0f0f0"
  gauge-fill: "#d4d4d4"
  approval-blue: "#0070f3"
  approval-wash: "#d3e5ff"
  approval-deep: "#0058c0"
  delete-red: "#ee0000"
  delete-wash: "#f7d4d6"
  chip-tint: "rgba(0,0,0,0.045)"
  chip-tint-hover: "rgba(0,0,0,0.08)"
typography:
  manuscript:
    fontFamily: "-apple-system, Geist, Inter, Pretendard, Apple SD Gothic Neo, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.85
  body:
    fontFamily: "-apple-system, Geist, Inter, Pretendard, Apple SD Gothic Neo, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
  headline:
    fontFamily: "-apple-system, Geist, Inter, Pretendard, Apple SD Gothic Neo, sans-serif"
    fontSize: "16px"
    fontWeight: 700
    lineHeight: 1.4
  title:
    fontFamily: "-apple-system, Geist, Inter, Pretendard, Apple SD Gothic Neo, sans-serif"
    fontSize: "14px"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "-0.01em"
  label:
    fontFamily: "-apple-system, Geist, Inter, Pretendard, Apple SD Gothic Neo, sans-serif"
    fontSize: "11px"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.04em"
  numeric:
    fontFamily: "Geist Mono, ui-monospace, SFMono-Regular, Menlo, Monaco, monospace"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "tnum"
rounded:
  sm: "6px"
  md: "8px"
  lg: "12px"
  panel: "14px"
  full: "9999px"
components:
  button-confirm:
    backgroundColor: "{colors.approval-blue}"
    textColor: "{colors.proof-white}"
    rounded: "{rounded.full}"
    padding: "10px 9px"
    typography: "{typography.body}"
  button-secondary:
    backgroundColor: "{colors.margin-gray}"
    textColor: "{colors.press-ink}"
    rounded: "{rounded.md}"
    padding: "7px 14px"
  button-icon:
    backgroundColor: "{colors.chip-tint}"
    textColor: "{colors.press-ink}"
    rounded: "{rounded.full}"
    size: "26px"
  button-icon-hover:
    backgroundColor: "{colors.chip-tint-hover}"
  input-search:
    backgroundColor: "{colors.margin-gray}"
    textColor: "{colors.press-ink}"
    rounded: "{rounded.sm}"
    padding: "6px 9px"
  card-project:
    backgroundColor: "{colors.margin-gray}"
    textColor: "{colors.press-ink}"
    rounded: "{rounded.lg}"
    padding: "14px 18px"
  badge-pending:
    backgroundColor: "{colors.query-wash}"
    textColor: "{colors.query-amber}"
    rounded: "{rounded.full}"
    padding: "3px 10px"
  badge-confirmed:
    backgroundColor: "{colors.approval-wash}"
    textColor: "{colors.approval-deep}"
    rounded: "{rounded.full}"
    padding: "3px 10px"
  badge-failed:
    backgroundColor: "{colors.press-ink}"
    textColor: "{colors.proof-white}"
    rounded: "{rounded.full}"
    padding: "3px 10px"
  badge-neutral:
    backgroundColor: "{colors.chip-tint}"
    textColor: "{colors.pencil-gray}"
    rounded: "{rounded.full}"
    padding: "3px 10px"
  modal:
    backgroundColor: "{colors.proof-white}"
    textColor: "{colors.press-ink}"
    rounded: "{rounded.panel}"
    padding: "22px 26px"
  toast:
    backgroundColor: "{colors.press-ink}"
    textColor: "{colors.proof-white}"
    padding: "9px 16px"
---

# Design System: video-cut

## Overview

**Creative North Star: "The Editor's Proof Sheet" (편집자의 교정지)**

화면은 교정 표시가 된 원고다. 흰 종이 위에 검은 글자로 강의 대본이 놓이고, 자동 처리가 남긴 판단은 모두 교정 기호처럼 그 위에 얹힌다. 잘린 말은 회색 취소선, 사람이 판단해야 할 곳은 호박색 질의 표시, 확정과 선택은 파란 펜, 지우는 동작은 빨간 펜. 기호마다 뜻이 하나씩이라, 사용자는 색만 보고도 원고의 상태를 읽는다.

밀도는 높고 장식은 없다. 장시간 전사문을 읽고 ms 단위로 경계를 반복 조정하는 정밀 작업이라, 가독성과 상태 구분이 모든 장식보다 앞선다. 계층은 그림자가 아니라 종이의 결(흰 원고, 옅은 회색 여백, 조금 더 짙은 떠 있는 판)과 1px 선으로 만든다. 이전에 시도한 웜페이퍼(Notion풍)와 다크 커맨드 툴(Raycast풍)은 반려됐다. 다크는 반투명 accent와 근흑색 위 회색 선 때문에 상태가 안 보였다.

새 요소를 넣을 때는 하나만 묻는다. **"이건 원고 위의 어떤 표시인가?"** 대답이 기존 기호 중 하나면 그 색을 쓰고, 어느 것도 아니면 색을 쓰지 않는다.

**Key Characteristics:**
- 흰 원고(#ffffff) + 근흑색 잉크(#171717), 대비 약 17.9:1
- 브랜드 accent는 파랑 하나. 나머지 색은 모두 교정 기호
- 대본 본문은 17px / 줄 간격 1.85의 넉넉한 원고 조판
- 숫자(타임스탬프, 길이, 게이지)는 등폭 글꼴로 자릿수가 흔들리지 않게
- 그림자는 떠 있는 판에만, 계층의 주 수단은 색면과 1px 선
- 키보드 중심 조작. 단축키 표기는 작은 회색 `kbd`

## Colors

종이와 잉크의 무채색 위에, 뜻이 고정된 교정 기호 네 가지만 색을 갖는다.

### Primary
- **Approval Blue** (approval-blue): 확정, 선택, 재생헤드, 사용자가 조정한 게이지. 페이지 전체에서 "긍정/활성" 의미로만 쓰는 유일한 브랜드 accent. 확정 버튼처럼 solid로 채울 때만 흰 글자를 얹는다(대비 약 4.55:1, 버튼 글자를 이보다 작게 줄이지 않는다).
- **Approval Wash** (approval-wash): 텍스트 선택 하이라이트, 포커스 링, 확정됨 배지 배경. 옅은 배경 위엔 기본 잉크를 그대로 얹는다.
- **Approval Deep** (approval-deep): Approval Blue로는 대비가 모자랄 때 쓰는 진한 변형. Approval Wash 위 글자("검토 시작" 버튼, 확정됨 배지)와 16px 강조 숫자에 쓴다. 연파랑 위 5.2:1(10-06 audit에서 #0066dd → #0058c0, 이전 값은 4.16:1로 AA 미달). 새 의미를 만들지 않는다.

### Secondary
- **Query Amber** (query-amber) / **Query Wash** (query-wash): 사람이 확인해야 할 곳. 원고 여백에 연필로 단 "확인 바람" 질의 표시다. 검토 대기 하이라이트, 스크롤 진행률 바의 대기 틱, 홈 화면의 "검토 중" 배지, 파형의 **잔음 의심** 구간(호박색 해치 + 바닥 3px 막대, 10-06 audit 전엔 문서에 없던 주황빨강), 멈춘 처리·일시정지 안내.

### Tertiary
- **Delete Red** (delete-red) / **Delete Wash** (delete-wash): 삭제 동작 전용. 교정지의 빨간 펜이다.

### Neutral
- **Proof White** (proof-white): 원고(대본)와 페이지 배경, 모달.
- **Margin Gray** (margin-gray): 사이드바, 카드, 보조 버튼 배경. 원고 옆 여백.
- **Galley Gray** (galley-gray): 떠 있는 판(팝업, 게이지 트랙, 코드 조각) 배경.
- **Press Ink** (press-ink): 본문 글자. 토스트·툴팁·비디오 컨트롤 바의 배경으로도 쓴다(콘텐츠 위에 잠깐 뜨는 요소는 페이지와 무관하게 항상 최대 대비).
- **Pencil Gray** (pencil-gray): 보조 글자, 캡션, 단축키 표기. 흰 바탕 대비 약 5.7:1로 AA 통과. 작은 글자를 이보다 흐리게 내리지 않는다.
- **Hairline** (hairline): 기본 1px 경계선.
- **Rule Gray** (rule-gray): 강조 경계선, 해결된 검토 틱.
- **Struck Gray** (struck-gray): 잘린 단어의 취소선과 글자. 일부러 연하게 한 것이다. 대비 감사에서 제외한다.
- **Gauge Track / Gauge Fill**: 무음 리듬 게이지의 트랙과 규칙 기반 채움. 사용자가 조정한 게이지는 연한 파랑(#b9d6ff) 채움 + 오른쪽 끝 2px Approval Blue 선이고, 숫자는 채움과 상관없이 항상 잉크색이다(흰 숫자는 채움이 짧으면 트랙 위에서 안 보였다).
- **Chip Tint / Chip Tint Hover**: 아이콘 버튼과 중립 배지의 반투명 배경.

### Named Rules

**The One Pen Per Meaning Rule.** 파랑은 확정·선택, 호박색은 검토 대기, 빨강은 삭제 동작. 한 색이 두 뜻을 갖지 않는다. 특히 빨강은 실패·경고·강조에 쓰지 않는다.

**The Ink Note Rule.** 실패는 색이 아니라 검은 잉크와 그린 경고 아이콘으로 쓴다. 교정자가 검은 펜으로 남긴 메모다. 연한 배지들 사이에서 가장 진한 Press Ink 배지가 되고, 오류 문구는 잉크 글자에 경고 아이콘을 붙인다(2026-10-06 결정).

**The Token-Only Rule.** 새 컴포넌트는 `:root` 변수만 쓰고 hex를 직접 쓰지 않는다. 예외는 문서화된 것뿐이다: 토스트·툴팁·비디오 컨트롤 바의 Press Ink 고정 배경, CSS 변수를 못 읽는 파형 캔버스(파형 #4d4d4d, 재생헤드 Approval Blue, 잘림 회색 해치, 잔음 의심 Query 색 - 같은 값을 JS에 직접 두고, 바뀌면 양쪽 함께 갱신).

## Typography

**Body Font:** 시스템 산세리프 (-apple-system, Geist, Inter, 한글은 Pretendard → Apple SD Gothic Neo로 폴백)
**Numeric/Mono Font:** Geist Mono (ui-monospace, SFMono-Regular, Menlo로 폴백)

**Character:** 원고는 읽기 좋은 넉넉한 산세리프, 측정값은 흔들리지 않는 등폭. 웹폰트를 불러오지 않는다. 로컬 서버가 외부 요청 없이 동작하도록 시스템 폰트 스택만 쓴다.

### Hierarchy
- **Manuscript** (400, 17px, 1.85): 검토 화면의 대본 본문. 이 도구에서 가장 오래 읽히는 글자라 가장 넉넉하게 조판한다. 대본 열은 최대 880px. 문장을 한 줄에 맞추려고 줄일 때는 16px·15px 두 단계까지만 쓰고, 그래도 안 들어가면 절 경계에서 나눈다(10-06 audit 전엔 13~17px 사이 아무 크기나 써서 줄마다 들쭉날쭉했다).
- **Body** (400, 15px, 1.5): 기본 UI 글자.
- **Headline** (700, 16px): 모달 제목.
- **Title** (700, 14px, -0.01em): 사이드바 제목, 카드 이름(600, 15px).
- **Label** (700, 11px, 0.04em, 대문자): 사이드바 섹션 제목. 배지·캡션은 12~12.5px.
- **Numeric** (Geist Mono, tabular-nums): 타임스탬프, 길이, 게이지 값, 단축키 표기(11px).

### Named Rules

**The Steady Digits Rule.** 시간·길이·개수처럼 바뀌는 숫자는 항상 등폭(tabular-nums)으로. 자릿수가 바뀔 때 줄이 흔들리면 정밀 작업의 신뢰가 깎인다.

## Layout

검토 화면은 왼쪽 고정 사이드바(248px, Margin Gray) + 스크롤되는 대본 열 하나 + 오른쪽 위에 떠 있는 비디오 미리보기(폭 clamp(200px, 24vw, 420px))다. 여러 패널로 화면을 나누지 않는다. 판단은 팝업 없이 키보드로 바로 하고(10-02에 선택마다 뜨던 작업 패널을 없앴다), 파형은 문장마다 바로 아래 붙는 인라인 스트립으로 본다. 화면 위에 뜨는 것은 도움말 패널, 확정·오류 모달, 비디오 미리보기뿐이고, 도움말과 모달은 드래그 핸들로 옮길 수 있다.

반응형: 681~1700px에서는 대본 열이 비디오 폭만큼 오른쪽 여백을 비워 비디오 뒤로 글자가 숨지 않게 한다. 680px 이하에서는 비디오 미리보기를 숨긴다. 홈 화면은 가운데 정렬된 단일 열의 카드 목록(카드 간격 10px)이다.

간격은 토큰화돼 있지 않다. 관찰된 리듬은 6 / 10 / 12 / 14 / 16 / 22px 단계다.

## Elevation & Depth

계층은 색면이 만든다. Proof White(원고) → Margin Gray(여백) → Galley Gray(떠 있는 판)의 명도 단계와 1px Hairline이 주 수단이고, 그림자는 화면 위에 뜬 요소에만 보조로 쓴다. 새 rgba 값을 임의로 만들지 않고 아래 단계에서 고른다.

### Shadow Vocabulary
- **Float Small** (`box-shadow: 0 6px 16px -4px rgba(0,0,0,0.18)`): 작게 뜬 아이콘 버튼(도움말 버튼).
- **Float Medium** (`box-shadow: 0 20px 50px -12px rgba(0,0,0,0.22)`): 도움말 패널.
- **Float Large** (`box-shadow: 0 24px 60px -14px rgba(0,0,0,0.25)`): 확정·오류 모달.
- **Strip Lift** (`box-shadow: 0 10px 28px -16px rgba(0,0,0,0.3)`): 지금 조정 중인 문장의 파형 스트립을 주변 문장에서 띄운다.
- **Video Lift** (`box-shadow: 0 20px 50px -12px rgba(0,0,0,0.7), 0 0 0 1px var(--line)`): 플로팅 비디오만. 스크롤되는 대본 위에 늘 떠 있어 다른 판보다 강한 분리가 필요하다.
- **Card Hover** (`box-shadow: 0 6px 18px -10px rgba(0,0,0,0.18)`): 클릭할 수 있는 홈 카드의 호버 반응.

### Named Rules

**The Paper First Rule.** 표면은 쉬고 있을 때 평평하다. 그림자는 화면 위에 실제로 떠 있는 판이거나, 호버처럼 상태에 대한 반응일 때만 나타난다.

## Shapes

부드럽지만 둥글지 않은 모서리. 작은 입력은 6px, 버튼 기본은 8px, 홈 카드는 12px, 모달·도움말 패널·비디오처럼 큰 판은 14px.

### Named Rules

**The Pill Is Earned Rule.** 완전한 알약형(9999px)은 확정 버튼, 되돌리기/다시 실행·도움말 같은 원형 아이콘 버튼, 상태 배지에만 쓴다. 그 외 카드·입력·일반 버튼은 6~8px.

## Components

### Buttons
도구답게 조용하고, 확정만 또렷하다.
- **Confirm (확정):** Approval Blue 채움 + 흰 글자, 알약형, 600 굵기 13.5px, 사이드바 폭 전체. 호버는 밝기만 6% 올린다.
- **Secondary:** Margin Gray 배경, Hairline 테두리, 8px 모서리, 7px 14px 안쪽 여백. 모달의 취소·닫기.
- **Icon:** 26px 원형, Chip Tint 배경, 호버 시 Chip Tint Hover. 비활성은 40% 불투명도. `title`과 별도로 `aria-label`을 단다.

### Badges (홈 화면 상태)
- **Style:** 알약형, 12px 600, 3px 10px.
- **State:** 검토 중 = Query Wash/Query Amber, 확정됨 = Approval Wash/Approval Deep, 처리 중·처리 멈춤 = Chip Tint/Pencil Gray(멈춘 처리의 안내 문구는 Query Amber - 사용자를 기다림), 처리 실패 = Press Ink 배경 + Proof White 글자 + 경고 아이콘(The Ink Note Rule).

### Cards / Containers
- **Corner Style:** 12px (홈 카드)
- **Background:** Margin Gray
- **Shadow Strategy:** 쉴 때 없음, 클릭 가능한 카드만 호버 시 Card Hover + 테두리를 Rule Gray로
- **Border:** 1px Hairline
- **Internal Padding:** 14px 18px

### Inputs / Fields
- **Style:** Margin Gray 배경, 1px Hairline, 6px 모서리, 12.5px 글자.
- **Focus:** 테두리를 Approval Blue로, 바깥에 2px Approval Wash 링.

### Modals
화면을 막는 확정·오류·설정 창. Proof White 배경, 1px Hairline, 14px 모서리, 22px 26px 여백, Float Large 그림자, 위쪽 드래그 핸들. `role="dialog"` + `aria-modal="true"`, Esc로 닫힌다. 파괴적 확인은 브라우저 `confirm()`이 아니라 이 모달로 한다(브라우저의 "대화상자 더 표시 안 함"이 안전장치를 조용히 끈다).

### Pipeline Progress (처리 진행 화면)
영상 처리 중에 검토 화면 자리를 덮는 화면. Proof White 위 가운데 560px 열에 제목(16px 700) + 부제(Pencil Gray, 숫자만 등폭) + 단계 목록 + 동작 버튼 + 안내.
- **단계 목록:** Margin Gray 판, 1px Hairline, 12px 모서리. 완료 = 잉크 체크, 진행 중 = Approval Blue 회전 고리, 일시정지 = Query Amber 두 막대, 중단 = 잉크 정지 사각형, 남은 단계 = Rule Gray 빈 원. 아이콘은 모두 그린 SVG.
- **상태:** 처리 중(일시정지·중단), 일시정지됨(계속·중단 + Query Amber 안내), 중단됨(이어서 처리·홈으로), 실패(경고 아이콘 제목 + 로그 + 다시 시도·로그 복사·홈으로).
- **로그:** Galley Gray 판, Geist Mono 11.5px, 선택 가능, 열릴 때 맨 아래로 스크롤(파이썬 에러는 원인이 끝 줄).
- **버튼:** 8px 모서리. 주 동작(다시 시도·이어서 처리·계속)만 Approval Blue 채움, 나머지는 Secondary.
- **층:** 확인 모달(20)·토스트(30) 아래인 19. 떠 있는 동안 뒤의 도움말 버튼은 숨긴다.

### Toast
Press Ink 배경 + 흰 글자, 9px 모서리, 화면 아래 가운데. `role="status"` + `aria-live="polite"`.

### Manuscript Marks (signature)
대본 위의 교정 기호. 이 시스템의 정체성이다.
- **잘림:** Struck Gray 글자 + 같은 색 취소선. 클릭하면 선택된다.
- **검토 대기:** Query Wash 배경 위에 기본 잉크.
- **선택:** Approval Wash 배경.
- **파형 스트립:** 문장마다 바로 아래 붙는 인라인 파형. 조정 중인 스트립은 92px로 커지고 Approval Wash 2px 링과 Strip Lift 그림자로 떠오른다.
- **스크롤 진행률 바:** 대본 열 위에 고정된 3px 트랙(클릭 영역 24px), 미해결 검토 위치에 Query Amber 틱, 해결된 곳은 Rule Gray 틱.

## Do's and Don'ts

### Do:
- **Do** 새 요소마다 "원고 위의 어떤 표시인가?"를 묻고, 기존 교정 기호의 색만 쓴다.
- **Do** `:root` 변수(--bg, --panel, --surface-2, --ink, --muted, --line, --accent, --proposal-*, --danger 등)만 참조한다.
- **Do** 바뀌는 숫자는 Geist Mono + tabular-nums로 쓴다.
- **Do** 계층은 Proof White → Margin Gray → Galley Gray 색면과 1px 선으로 먼저 만든다.
- **Do** 아이콘 버튼에 `aria-label`, 모든 오버레이에 Esc 닫기를 붙인다.
- **Do** 실패는 Press Ink + 그린 경고 아이콘으로 표시한다(The Ink Note Rule).
- **Do** 확인이 필요한 동작은 브라우저 `confirm()`/`alert()`이 아니라 확인 모달과 토스트로 처리한다.

### Don't:
- **Don't** 빨강(Delete Red)을 삭제 동작 외에 쓰지 않는다. 실패 상태, 경고, 강조도 빨강이 아니다.
- **Don't** 유니코드 문자(●, ○, ❚❚ 등)를 아이콘 대신 쓰지 않는다. 아이콘은 한 가지 선 두께의 그린 SVG다.
- **Don't** 어두운 배경 화면을 만들지 않는다. 다크 테마는 상태 구분이 안 보여 반려됐다.
- **Don't** Struck Gray 잘린 단어를 대비 개선 대상으로 "고치지" 않는다. 의도된 연함이다.
- **Don't** 작은 글자를 Pencil Gray(#666666)보다 흐리게 내리지 않는다.
- **Don't** 외부 웹폰트나 CDN 요청을 추가하지 않는다. 로컬 서버는 외부 요청 없이 동작해야 한다.
- **Don't** 새 그림자 값을 만들지 않는다. Shadow Vocabulary에서 고른다.

### Known Drift
처리 진행 화면의 다크 배경, 홈 화면 실패 표시의 빨강, 홈 화면의 `--warn` 별칭은 2026-10-06 polish에서 맞췄다. 현재 남은 어긋남은 없다. (설계 감지기가 기존 검토 화면에 대해 보고하는 대비·글자 크기 경고는 `docs/design-system.md` 접근성 체크리스트에서 다룬다.)
