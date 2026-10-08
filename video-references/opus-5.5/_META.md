# Opus 5.5 영상 레퍼런스 메타

출처: jasonzhu.ai/en/prompts/claude-opus-5-5 에서 **Opus 5.5 + Full prompt** 조건으로 고른 **142건** (수집일 2026-10-08).
각 케이스는 `<이름>.mp4`(결과 영상)와 `<이름>.md`(메타 헤더 + 원문 프롬프트)가 같은 이름으로 짝지어져 있다.

**영상과 프롬프트는 저장소에 없다.** 원작자들의 콘텐츠라 재배포하지 않고, 각자 받아서 쓴다:

```bash
python3 video-references/opus-5.5/fetch.py        # cases.txt의 142건을 이 폴더로 다운로드 (약 1.3GB, 이미 있는 파일은 건너뜀)
python3 video-references/opus-5.5/fetch.py --new  # 사이트에 새로 올라온 full prompt 사례 확인
```

원본 사이트 데이터나 X 영상이 내려가면 그 케이스는 받아지지 않는다(스크립트가 실패 목록을 출력).

이름 규칙: `<category>__<제목-slug>__<X 게시물 id>`
category: motion 37 · comparison 27 · art3d 19 · game 16 · stories 13 · education 12 · product 11 · production 7

---

## 0. 영상 생성 시 이 파일 쓰는 법

1. 만들려는 영상의 **용도**를 1장에서 찾는다 → 후보 2~4개.
2. 원하는 **룩**을 2장 스타일 계열에서 확인해 후보를 좁힌다.
3. 후보의 `.md`에서 **프롬프트 구조**를 가져오고(3장 패턴 참고), `.mp4`는 시각 레퍼런스로 같이 넘긴다.
4. 4장 주의사항에 걸리는 케이스(비교 영상, 화면 녹화, IP, 외부 에셋 의존)는 **프롬프트 구조만** 빌리고 룩은 다른 레퍼런스로 보완한다.
5. 세부 정보는 맨 아래 5장 전체 카탈로그(케이스별 요약·어울리는 경우·잘하는 표현·스타일·기술·태그)를 검색한다.

**가장 재사용 가치가 높은 3가지 (먼저 볼 것)**
- **seek(t) 단일 HTML 모션 템플릿**: [code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2103273003555402193.md) (조회 100만+), [orange-dot-motion-design-system](motion__orange-dot-motion-design-system__2107121188027707651.md), [beat-synced-showreel-from-real-clips](motion__beat-synced-showreel-from-real-clips__2102554209166000267.md), [apple-style-product-launch-video](product__apple-style-product-launch-video__2103835273813496100.md). 결정론적 프레임 렌더 + Playwright + ffmpeg 파이프라인이라 그대로 자동화에 붙이기 좋다.
- **토킹헤드 + 비주얼 삽입 (이 프로젝트와 직결)**: [talking-head-video-converted-to-line-art-b-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md) (원형 PIP + 선화 B-roll), [ai-video-editing-workflow-comparison](comparison__ai-video-editing-workflow-comparison__2105682280765350117.md) (말→인포그래픽), [ai-edit-vs-human-edit-comparison](comparison__ai-edit-vs-human-edit-comparison__2103591152847118409.md) (키네틱 자막).
- **설명형 다크 다큐 (Remotion)**: [history-of-ai-documentary-short-film](education__history-of-ai-documentary-short-film__2102844654169575547.md) (AI 역사, 단일 앰버 강조색), [zoom-journey-from-a-cell-to-quantum-fields](education__zoom-journey-from-a-cell-to-quantum-fields__2103099756167991347.md) (스케일 줌 과학 강의).

---

## 1. 용도별 추천

| 용도 | 1순위 | 다음 후보 |
|---|---|---|
| 강의·개념 설명 (다크, 차분) | [history-of-ai-documentary-short-film](education__history-of-ai-documentary-short-film__2102844654169575547.md) | [zoom-journey-from-a-cell-to-quantum-fields](education__zoom-journey-from-a-cell-to-quantum-fields__2103099756167991347.md), [how-a-language-model-answers-a-prompt-20-second-motion-graph](comparison__how-a-language-model-answers-a-prompt-20-second-motion-graph__2102724864205566388.md), [history-of-indonesia-animated-documentary](education__history-of-indonesia-animated-documentary__2103511590884815282.md) |
| 강의·개념 설명 (종이/손그림, 따뜻함) | [animated-cycloid-lesson](education__animated-cycloid-lesson__2106052083040256293.md) | [talking-head-video-converted-to-line-art-b-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md), [zero-shot-documentary-on-jewish-history](education__zero-shot-documentary-on-jewish-history__2103564391170089429.md), [doc-to-video-explainer-open-alignment](education__doc-to-video-explainer-open-alignment__2103545533474206118.md) |
| 토킹헤드 편집 + 그래픽 삽입 | [talking-head-video-converted-to-line-art-b-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md) | [ai-video-editing-workflow-comparison](comparison__ai-video-editing-workflow-comparison__2105682280765350117.md), [ai-edit-vs-human-edit-comparison](comparison__ai-edit-vs-human-edit-comparison__2103591152847118409.md), [ai-edited-travel-vlog](production__ai-edited-travel-vlog__2106091485125091695.md) |
| SaaS/앱 제품 소개 (15~40초) | [reusable-prompt-template-for-a-product-motion-video](motion__reusable-prompt-template-for-a-product-motion-video__2103723183899852885.md) | [typingmind-product-intro-motion-video](motion__typingmind-product-intro-motion-video__2103703135902740699.md), [professional-30-second-product-showreel](motion__professional-30-second-product-showreel__2103845264649761062.md), [distilbook-motion-graphics-showreel](motion__distilbook-motion-graphics-showreel__2103469807375208546.md), [one-prompt-saas-launch-video](product__one-prompt-saas-launch-video__2103066071838466494.md) |
| Apple 키노트풍 런칭 필름 | [apple-style-product-launch-video](product__apple-style-product-launch-video__2103835273813496100.md) | [apple-keynote-style-launch-film](motion__apple-keynote-style-launch-film__2107123710251434330.md), [looping-product-launch-motion-template](motion__looping-product-launch-motion-template__2105927781678747965.md), [apple-liquid-glass-style-ui-motion-showcase](motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152.md) |
| UI 마이크로 인터랙션 쇼케이스 | [code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2103273003555402193.md) | [code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2106396375269134597.md), [apple-liquid-glass-style-ui-motion-showcase](motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152.md), [animated-welcome-screen-for-the-nova-crypto-wallet](comparison__animated-welcome-screen-for-the-nova-crypto-wallet__2102681647720395115.md) |
| 브랜드 쇼릴·인트로·범퍼 (15초) | [orange-dot-motion-design-system](motion__orange-dot-motion-design-system__2107121188027707651.md) | [20-second-kinetic-identity-bumper-for-techhalla](motion__20-second-kinetic-identity-bumper-for-techhalla__2103411244468498547.md), [15-second-motion-graphics-showcase](motion__15-second-motion-graphics-showcase__2106376222309761094.md), [15-second-motion-design-showreel-detailed-prompt](motion__15-second-motion-design-showreel-detailed-prompt__2103424524297420829.md), [high-energy-motion-graphics-showreel](motion__high-energy-motion-graphics-showreel__2103817034618339682.md) |
| 실사 클립 비트싱크 광고 | [beat-synced-showreel-from-real-clips](motion__beat-synced-showreel-from-real-clips__2102554209166000267.md) | [fast-paced-brand-advertisement](product__fast-paced-brand-advertisement__2106101651010449796.md) |
| 세로 숏폼 (9:16) | [reels-made-with-opus-5-5](motion__reels-made-with-opus-5-5__2105283486487896448.md) | [talking-head-video-converted-to-line-art-b-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md), [ai-video-editing-workflow-comparison](comparison__ai-video-editing-workflow-comparison__2105682280765350117.md), [chaotic-brain-rot-style-motion-video](motion__chaotic-brain-rot-style-motion-video__2103664956482941143.md), [fast-paced-brand-advertisement](product__fast-paced-brand-advertisement__2106101651010449796.md) |
| 역사·연대기 다큐 | [epic-documentary-history-of-chinese-civilization](education__epic-documentary-history-of-chinese-civilization__2103964025683927166.md) | [history-of-indonesia-animated-documentary](education__history-of-indonesia-animated-documentary__2103511590884815282.md), [zero-shot-documentary-on-jewish-history](education__zero-shot-documentary-on-jewish-history__2103564391170089429.md), [battle-of-austerlitz-procedural-film](stories__battle-of-austerlitz-procedural-film__2103116235009347650.md), [mongol-conquest-data-visualization-comparison](comparison__mongol-conquest-data-visualization-comparison__2102566466121797767.md) |
| 과학·스케일 줌 (Powers of Ten) | [zoom-journey-from-a-cell-to-quantum-fields](education__zoom-journey-from-a-cell-to-quantum-fields__2103099756167991347.md) | [zoom-from-room-to-quarks-3d-scene](art3d__zoom-from-room-to-quarks-3d-scene__2103299766473875778.md), [working-computer-built-from-logic-gates-with-os](product__working-computer-built-from-logic-gates-with-os__2104301990985498783.md) |
| 단계형 how-to / 레시피 | [cocktail-recipe-explainer-motion-graphic](motion__cocktail-recipe-explainer-motion-graphic__2102853258582880547.md) | [animated-pelican-explains-a-shell-command](education__animated-pelican-explains-a-shell-command__2103149526244618682.md) |
| 스포츠·규칙 해설 (TV 중계 그래픽) | [explainer-video-of-9-football-rules](education__explainer-video-of-9-football-rules__2105922894924501283.md) | |
| 도면→3D 빌드업 (건축·제조) | [itsukushima-shrine-3d-scene](art3d__itsukushima-shrine-3d-scene__2103737014508216515.md) | [golden-pavilion-cad-to-3d-animation](art3d__golden-pavilion-cad-to-3d-animation__2103243328041132100.md), [underwater-palace-built-in-blender](art3d__underwater-palace-built-in-blender__2103669801554264378.md), [floor-plan-to-3d-interior-design-tool](art3d__floor-plan-to-3d-interior-design-tool__2104520072014508316.md) |
| 제품 소재감·만족감 숏폼 (젤리/물리) | [jelly-watermelon-slicing-simulation](art3d__jelly-watermelon-slicing-simulation__2104285370951012504.md) | [interactive-jelly-press-toy](art3d__interactive-jelly-press-toy__2105285992865272110.md), [interactive-jelly-watermelon-toy](game__interactive-jelly-watermelon-toy__2106056420131029473.md), [watermelon-rubber-band-test-opus-5-5-vs-gpt-6-astra](comparison__watermelon-rubber-band-test-opus-5-5-vs-gpt-6-astra__2104994617573970308.md) |
| 감성 단편·매니페스토 | [the-first-spark-procedural-hand-drawn-short](motion__the-first-spark-procedural-hand-drawn-short__2102910531560731063.md) | [animated-episode-drawn-entirely-in-code](stories__animated-episode-drawn-entirely-in-code__2102879301876031808.md), [ai-self-introduction-song-and-video](stories__ai-self-introduction-song-and-video__2103698854399099057.md), [cinematic-2d-storyboard-short-film-rain-station](stories__cinematic-2d-storyboard-short-film-rain-station__2103757767727255661.md) |
| 캐릭터 단편 애니 | [animated-robot-story-across-12-art-styles](stories__animated-robot-story-across-12-art-styles__2103099194693271874.md) | [oktoberfest-themed-animation](stories__oktoberfest-themed-animation__2102493303388475855.md), [pixar-style-imagined-cartoon-story](stories__pixar-style-imagined-cartoon-story__2102788223835463902.md), [four-minute-2d-animation-made-with-up-to-15-agents](motion__four-minute-2d-animation-made-with-up-to-15-agents__2103135536634630632.md) |
| 뮤직비디오·가사 싱크 | [remake-of-the-claude-pop-music-video](production__remake-of-the-claude-pop-music-video__2102801274173587569.md) | [one-shot-music-video-from-song-and-lyrics](stories__one-shot-music-video-from-song-and-lyrics__2103570879619686717.md), [linear-algebra-fear-music-video](stories__linear-algebra-fear-music-video__2103697580421181894.md), [music-driven-blender-visual-scene](art3d__music-driven-blender-visual-scene__2107696042053431360.md) |
| 루프 배경 (로파이·대기 화면) | [pixel-art-scene-generation](art3d__pixel-art-scene-generation__2102746041250705890.md) | [pixel-character-dodging-meteors-on-a-rainbow-space-track](motion__pixel-character-dodging-meteors-on-a-rainbow-space-track__2102515055116063144.md), [animated-pixel-art-wizard-casting-a-spell](motion__animated-pixel-art-wizard-casting-a-spell__2102476258948927543.md), [infinite-zoom-landscape-loop](motion__infinite-zoom-landscape-loop__2103129343253778767.md) |
| 시네마틱 3D 월드·플라이스루 | [cinematic-3d-world-with-a-free-camera](art3d__cinematic-3d-world-with-a-free-camera__2103194052850241739.md) | [playable-boat-scene-through-japanese-landscapes](art3d__playable-boat-scene-through-japanese-landscapes__2102760783344189761.md), [interactive-3d-dystopian-city-diorama](art3d__interactive-3d-dystopian-city-diorama__2103820733159981151.md), [280-kb-single-file-html-demoscene-intro](art3d__280-kb-single-file-html-demoscene-intro__2102893186330841502.md) |
| 게임 보상·가챠 리빌 | [game-settlement-and-card-draw-animations](game__game-settlement-and-card-draw-animations__2104085484347818226.md) | |
| B2B 운영/공정 설명 (아이소메트릭) | [mining-operations-strategy-game](game__mining-operations-strategy-game__2107022944916709886.md) | |
| 시스템·아키텍처 설명 | [zoomable-app-architecture-canvas](education__zoomable-app-architecture-canvas__2105309987983745060.md) | [working-computer-built-from-logic-gates-with-os](product__working-computer-built-from-logic-gates-with-os__2104301990985498783.md) |
| 실사풍 생성 영상 (외부 모델) | [ai-documentary-about-superintelligence](education__ai-documentary-about-superintelligence__2103304514329854102.md) | [promotional-travel-video-about-poland](product__promotional-travel-video-about-poland__2102728913579327722.md), [ai-pipeline-short-video-with-opus-5-5](production__ai-pipeline-short-video-with-opus-5-5__2105370568178479476.md) |
| 도서·출판 프로모 (빈티지) | [promo-video-for-a-science-based-book](product__promo-video-for-a-science-based-book__2103904736160120935.md) | |
| 채용·회사 소개 + TTS | [opus-5-5-plus-gemini-tts-demo](production__opus-5-5-plus-gemini-tts-demo__2103590367518171295.md) | |

---

## 2. 스타일 계열

**A. 다크 미니멀 + 단일 강조색** — 검정/차콜 배경, 흰 또는 크림 산세리프, 강조색 1개(주황·앰버·코랄). 차분하고 고급스러움. 설명·브랜드·런칭 모두 무난.
[history-of-ai-documentary-short-film](education__history-of-ai-documentary-short-film__2102844654169575547.md), [15-second-motion-design-showreel-detailed-prompt](motion__15-second-motion-design-showreel-detailed-prompt__2103424524297420829.md), [motion-design-and-sound-engineering-demo](motion__motion-design-and-sound-engineering-demo__2103557735086428547.md), [cinematic-product-launch-film](product__cinematic-product-launch-film__2104805179401068964.md), [chaotic-brain-rot-style-motion-video](motion__chaotic-brain-rot-style-motion-video__2103664956482941143.md), [ai-self-introduction-song-and-video](stories__ai-self-introduction-song-and-video__2103698854399099057.md)

**B. 오프화이트 에디토리얼 / Apple 미니멀** — 웜 화이트 캔버스, 검정 UI·필 버튼, Geist류 산세리프, 여백 많음. UI·제품·런칭.
[code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2103273003555402193.md), [code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2106396375269134597.md), [apple-style-product-launch-video](product__apple-style-product-launch-video__2103835273813496100.md), [apple-keynote-style-launch-film](motion__apple-keynote-style-launch-film__2107123710251434330.md), [professional-30-second-product-showreel](motion__professional-30-second-product-showreel__2103845264649761062.md), [reels-made-with-opus-5-5](motion__reels-made-with-opus-5-5__2105283486487896448.md), [cosmos-motion-piece-via-hyperframes](motion__cosmos-motion-piece-via-hyperframes__2103481296018092204.md)

**C. 파스텔 글래스모피즘** — 파스텔 그라디언트 + 반투명 글래스 UI. iOS/macOS 기능 소개.
[apple-liquid-glass-style-ui-motion-showcase](motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152.md), [looping-product-launch-motion-template](motion__looping-product-launch-motion-template__2105927781678747965.md), [animated-welcome-screen-for-the-nova-crypto-wallet](comparison__animated-welcome-screen-for-the-nova-crypto-wallet__2102681647720395115.md) (다크 핀테크 변형)

**D. 다크 테크 / 네온 SaaS** — 남색~검정, 파랑·하늘색 글로우, UI 카드. SaaS·개발자 도구.
[typingmind-product-intro-motion-video](motion__typingmind-product-intro-motion-video__2103703135902740699.md), [one-prompt-motion-graphic-from-codebase](motion__one-prompt-motion-graphic-from-codebase__2105268326381625845.md), [30-second-motion-promo-for-kody](motion__30-second-motion-promo-for-kody__2103638102333858193.md), [ai-generated-animated-video-demo](motion__ai-generated-animated-video-demo__2105279421435572498.md), [how-a-language-model-answers-a-prompt-20-second-motion-graph](comparison__how-a-language-model-answers-a-prompt-20-second-motion-graph__2102724864205566388.md)

**E. 볼드 그래픽 / 스위스·포스터** — 원색 풀스크린 컷, 초굵은 산세리프, 고대비. 범퍼·쇼릴·훅.
[15-second-motion-graphics-showcase](motion__15-second-motion-graphics-showcase__2106376222309761094.md), [20-second-kinetic-identity-bumper-for-techhalla](motion__20-second-kinetic-identity-bumper-for-techhalla__2103411244468498547.md), [high-energy-motion-graphics-showreel](motion__high-energy-motion-graphics-showreel__2103817034618339682.md), [motion-showreel-with-a-fully-code-synthesized-soundtrack](motion__motion-showreel-with-a-fully-code-synthesized-soundtrack__2103538744695693512.md), [orange-dot-motion-design-system](motion__orange-dot-motion-design-system__2107121188027707651.md), [persian-language-motion-graphics-showreel](motion__persian-language-motion-graphics-showreel__2103562127474819150.md)

**F. 종이·손그림·잉크** — 크림 종이 질감, 선화/두들/잉크 실루엣, 따뜻함. 교육·감성 단편.
[talking-head-video-converted-to-line-art-b-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md), [animated-cycloid-lesson](education__animated-cycloid-lesson__2106052083040256293.md), [the-first-spark-procedural-hand-drawn-short](motion__the-first-spark-procedural-hand-drawn-short__2102910531560731063.md), [animated-episode-drawn-entirely-in-code](stories__animated-episode-drawn-entirely-in-code__2102879301876031808.md), [distilbook-motion-graphics-showreel](motion__distilbook-motion-graphics-showreel__2103469807375208546.md), [cocktail-recipe-explainer-motion-graphic](motion__cocktail-recipe-explainer-motion-graphic__2102853258582880547.md), [remake-of-the-claude-pop-music-video](production__remake-of-the-claude-pop-music-video__2102801274173587569.md) (리소 프린트풍)

**G. 빈티지 양피지 / 세피아 다큐** — 양피지·고서 일러스트, 세리프. 역사·출판.
[zero-shot-documentary-on-jewish-history](education__zero-shot-documentary-on-jewish-history__2103564391170089429.md), [promo-video-for-a-science-based-book](product__promo-video-for-a-science-based-book__2103904736160120935.md), [sand-painting-animation-with-narrated-soundtrack](art3d__sand-painting-animation-with-narrated-soundtrack__2102592355165782312.md), [animated-cycloid-lesson](education__animated-cycloid-lesson__2106052083040256293.md)

**H. 동양 전통 그래픽** — 서예 대자, 붉은 도장, 선지·먹선, 세로쓰기.
[epic-documentary-history-of-chinese-civilization](education__epic-documentary-history-of-chinese-civilization__2103964025683927166.md), [itsukushima-shrine-3d-scene](art3d__itsukushima-shrine-3d-scene__2103737014508216515.md), [golden-pavilion-cad-to-3d-animation](art3d__golden-pavilion-cad-to-3d-animation__2103243328041132100.md), [underwater-palace-built-in-blender](art3d__underwater-palace-built-in-blender__2103669801554264378.md)

**I. 다크 사이언스 / 우주** — 검정 배경 발광 파티클, 반투명 3D 구조, 스케일 눈금 HUD.
[zoom-journey-from-a-cell-to-quantum-fields](education__zoom-journey-from-a-cell-to-quantum-fields__2103099756167991347.md), [live-generative-code-art-from-a-typed-word](art3d__live-generative-code-art-from-a-typed-word__2103837519615774895.md), [280-kb-single-file-html-demoscene-intro](art3d__280-kb-single-file-html-demoscene-intro__2102893186330841502.md), [zoom-from-room-to-quarks-3d-scene](art3d__zoom-from-room-to-quarks-3d-scene__2103299766473875778.md)

**J. 에디토리얼 머티리얼 스터디 (3D 제품샷)** — 크림 스튜디오 + 반투명 젤리/털 + 이탤릭 세리프 타이틀("Melon Jelly."). 소재감·만족감.
[jelly-watermelon-slicing-simulation](art3d__jelly-watermelon-slicing-simulation__2104285370951012504.md), [interactive-jelly-press-toy](art3d__interactive-jelly-press-toy__2105285992865272110.md), [interactive-jelly-watermelon-toy](game__interactive-jelly-watermelon-toy__2106056420131029473.md), [gummy-octopus-physics-comparison](comparison__gummy-octopus-physics-comparison__2104466170275324190.md), [browser-octopus-physics-comparison](comparison__browser-octopus-physics-comparison__2106809017850818679.md)

**K. 시네마틱 3D 환경** — 골든아워·대기원근·볼류메트릭 라이트.
[cinematic-3d-world-with-a-free-camera](art3d__cinematic-3d-world-with-a-free-camera__2103194052850241739.md), [playable-boat-scene-through-japanese-landscapes](art3d__playable-boat-scene-through-japanese-landscapes__2102760783344189761.md), [interactive-3d-dystopian-city-diorama](art3d__interactive-3d-dystopian-city-diorama__2103820733159981151.md) (사이버펑크), [pelican-riding-a-bike-in-three-js](art3d__pelican-riding-a-bike-in-three-js__2102436416437580159.md)

**L. 픽셀아트 / 레트로** — 제한 팔레트 16비트, 루프.
[pixel-art-scene-generation](art3d__pixel-art-scene-generation__2102746041250705890.md), [animated-pixel-art-wizard-casting-a-spell](motion__animated-pixel-art-wizard-casting-a-spell__2102476258948927543.md), [pixel-character-dodging-meteors-on-a-rainbow-space-track](motion__pixel-character-dodging-meteors-on-a-rainbow-space-track__2102515055116063144.md), [90s-style-demoscene-demo-in-c-opengl](art3d__90s-style-demoscene-demo-in-c-opengl__2102919394775220530.md) (90s 데모신), [alien-explores-the-library-of-babel](stories__alien-explores-the-library-of-babel__2103569043836027339.md) (90s 영화 GUI)

**M. 콜라주 / 사이키델릭** — 컷아웃 콜라주, 글리치, VHS.
[motion-design-showreel-exploring-overthinking](motion__motion-design-showreel-exploring-overthinking__2103566030916239768.md), [one-shot-music-video-from-song-and-lyrics](stories__one-shot-music-video-from-song-and-lyrics__2103570879619686717.md), [infinite-zoom-landscape-loop](motion__infinite-zoom-landscape-loop__2103129343253778767.md) (빈티지 사진 콜라주), [music-driven-blender-visual-scene](art3d__music-driven-blender-visual-scene__2107696042053431360.md)

**N. 실사 / 생성 영상** — 외부 영상 모델 기반 포토리얼.
[ai-documentary-about-superintelligence](education__ai-documentary-about-superintelligence__2103304514329854102.md), [promotional-travel-video-about-poland](product__promotional-travel-video-about-poland__2102728913579327722.md), [ai-pipeline-short-video-with-opus-5-5](production__ai-pipeline-short-video-with-opus-5-5__2105370568178479476.md), [cinematic-2d-storyboard-short-film-rain-station](stories__cinematic-2d-storyboard-short-film-rain-station__2103757767727255661.md) (애니풍 2.5D)

---

## 3. 프롬프트 패턴 (가져다 쓸 구조)

1. **seek(t) 결정론 렌더 스펙** — 단일 HTML에 `seek(t)` 순수 함수, closed-form 스프링, 비트 분석(numpy)으로 컷 타이밍, Playwright로 프레임 캡처, ffmpeg tmix 모션블러. 음원·카피·UI 상태 목록을 슬롯으로 받음. 품질 편차가 가장 적고 자동화에 바로 붙는다.
   [code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2103273003555402193.md), [code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2106396375269134597.md), [orange-dot-motion-design-system](motion__orange-dot-motion-design-system__2107121188027707651.md), [20-second-kinetic-identity-bumper-for-techhalla](motion__20-second-kinetic-identity-bumper-for-techhalla__2103411244468498547.md), [beat-synced-showreel-from-real-clips](motion__beat-synced-showreel-from-real-clips__2102554209166000267.md), [apple-style-product-launch-video](product__apple-style-product-launch-video__2103835273813496100.md), [apple-liquid-glass-style-ui-motion-showcase](motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152.md)
2. **재사용 제품 템플릿 (URL만 바꿔 끼움)** — 22건이 같은 프롬프트를 공유하는 그룹. 제품 웹페이지를 읽고 15초 UI 모션 생성.
   [reusable-prompt-template-for-a-product-motion-video](motion__reusable-prompt-template-for-a-product-motion-video__2103723183899852885.md) (원본 템플릿), [typingmind-product-intro-motion-video](motion__typingmind-product-intro-motion-video__2103703135902740699.md) (대표 결과)
3. **씬별 타임코드 샷리스트 + 디자인 토큰** — 초 단위 시퀀스, 색 코드·폰트 지정.
   [animated-welcome-screen-for-the-nova-crypto-wallet](comparison__animated-welcome-screen-for-the-nova-crypto-wallet__2102681647720395115.md), [cinematic-product-launch-film](product__cinematic-product-launch-film__2104805179401068964.md), [animated-robot-story-across-12-art-styles](stories__animated-robot-story-across-12-art-styles__2103099194693271874.md)
4. **섹션 헤더형 기술 명세 (ART DIRECTION / PHYSICS / UI / QUALITY BAR)** — 수치 파라미터·UI 문구까지 지정, 테스트 항목 포함. 재현성 높음.
   [jelly-watermelon-slicing-simulation](art3d__jelly-watermelon-slicing-simulation__2104285370951012504.md), [interactive-jelly-press-toy](art3d__interactive-jelly-press-toy__2105285992865272110.md), [gummy-octopus-physics-comparison](comparison__gummy-octopus-physics-comparison__2104466170275324190.md)
5. **슬롯형 일본어 템플릿 【題材】【環境】** — CAD 산출 → 씬 순서 → 카메라 → 사운드 → 테스트 스틸 확인 후 본 렌더.
   [itsukushima-shrine-3d-scene](art3d__itsukushima-shrine-3d-scene__2103737014508216515.md), [golden-pavilion-cad-to-3d-animation](art3d__golden-pavilion-cad-to-3d-animation__2103243328041132100.md), [underwater-palace-built-in-blender](art3d__underwater-palace-built-in-blender__2103669801554264378.md)
6. **다단계 파이프라인 디렉션** — 리서치/사운드 생성 → 분석 → 월드 빌드 → 렌더 → 포스트.
   [music-driven-blender-visual-scene](art3d__music-driven-blender-visual-scene__2107696042053431360.md), [historic-1906-san-francisco-street-in-3d](art3d__historic-1906-san-francisco-street-in-3d__2102466523164274839.md), [explainer-video-of-9-football-rules](education__explainer-video-of-9-football-rules__2105922894924501283.md) (종목만 바꾸는 템플릿)
7. **레퍼런스 영상 주고 리메이크/스타일 이식** — 기존 영상·레포를 첨부하고 "같은 스타일로".
   [remake-of-the-claude-pop-music-video](production__remake-of-the-claude-pop-music-video__2102801274173587569.md), [brand-motion-showreel-from-a-reference-video](motion__brand-motion-showreel-from-a-reference-video__2103541149709615243.md), [zero-shot-documentary-on-jewish-history](education__zero-shot-documentary-on-jewish-history__2103564391170089429.md), [fast-paced-brand-advertisement](product__fast-paced-brand-advertisement__2106101651010449796.md)
8. **자율 위임형 원라이너** — "가장 인상적인 걸 골라 만들어라". 결과는 좋을 수 있지만 재현성 낮음. 룩 참고용으로만.
   [280-kb-single-file-html-demoscene-intro](art3d__280-kb-single-file-html-demoscene-intro__2102893186330841502.md), [live-generative-code-art-from-a-typed-word](art3d__live-generative-code-art-from-a-typed-word__2103837519615774895.md), [pelican-riding-a-bike-in-three-js](art3d__pelican-riding-a-bike-in-three-js__2102436416437580159.md), [15-second-motion-graphics-showcase](motion__15-second-motion-graphics-showcase__2106376222309761094.md)

공통으로 잘 먹힌 지시: **"빈 화면 금지 / 항상 무언가 움직일 것"**, **"AI slop 금지"**, **스크린샷·테스트 스틸로 자가검수 후 수정**, **에셋 없이 코드로만**, **강조색 하나만**.

---

## 4. 레퍼런스로 쓸 때 주의

- **비교 영상 (comparison 27건 대부분)**: 화면이 2~12분할이고 모델명·비용 라벨이 박혀 있다. 룩은 Opus 칸만 보고, 프롬프트는 그대로 쓸 수 있다.
- **화면 녹화 (게임·인터랙티브·툴)**: 편집된 영상이 아니라 브라우저/앱 녹화. 컷 리듬·전환 레퍼런스로는 약하다 (game 대부분, art3d 일부, [liquid-glass-web-hero-section](product__liquid-glass-web-hero-section__2106061619176620344.md) 는 13분 작업 녹화).
- **외부 에셋 의존 (needs_assets)**: 제품 스크린샷, 음원, 캐릭터 시트, 원본 촬영본이 있어야 재현된다. 각 `.md` 헤더의 `needs reference assets` 확인.
- **외부 생성 모델 의존**: Seedance, Kling, Veo, Runway, fal, GPT Image 등 크레딧 필요 (N 계열).
- **IP·실존 인물**: Pixar, Star Wars, Fortnite, Far Cry, Rocket League, 주술회전, Rick Astley, Notion, Elon Musk 가십 등은 구조만 참고.
- **프롬프트와 결과 불일치**: [chaotic-brain-rot-style-motion-video](motion__chaotic-brain-rot-style-motion-video__2103664956482941143.md) ("카오틱"인데 차분함), [arcane-style-blender-animation](stories__arcane-style-blender-animation__2105315982525014067.md) (Arcane 화풍 재현도 낮음), [3d-character-rig-generated-from-a-psd-file](art3d__3d-character-rig-generated-from-a-psd-file__2102965242439590112.md) (3D 아니고 2D 리그), [apple-liquid-glass-style-ui-motion-showcase](motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152.md) (프롬프트 비트맵과 화면 다름), [fortnite-style-game-one-shot-test](game__fortnite-style-game-one-shot-test__2104779190277181699.md) (실제는 Sonnet 결과 + 진짜 Fortnite 화면).
- **해상도**: 원본이 X 업로드본이라 대부분 720p. 화질 기준이 아니라 구성·모션 기준으로 볼 것.

---

## 5. 전체 카탈로그


### motion (모션그래픽) — 37건 (조회수순)

#### [High-energy motion graphics showreel](motion__high-energy-motion-graphics-showreel__2103817034618339682.md)
`motion__high-energy-motion-graphics-showreel__2103817034618339682` · 16:9 · 15s · 조회 1.1M · 에셋필요 X

- **요약**: 아랍어 키네틱 타이포와 기하 도형으로 구성된 15초 고에너지 모션그래픽 쇼릴
- **어울리는 경우**: 모션 디자이너 포트폴리오 릴 / 아랍어/RTL 타이포 영상 / 브랜드 인트로 짧은 클립
- **잘하는 표현**: 아랍어 대형 타이포 키네틱 / 사선 반복 텍스트 밴드·픽셀 사각형 파티클 / 풀컬러 배경 컷 전환 리듬
- **스타일**: 검정 배경에 흰 아랍어 굵은 서체, 주황 라인 포인트, 코발트 블루 풀스크린 컷, 주황 사선 텍스트 밴드, 보라-주황 블러 그라데이션. 플랫 2D 그래픽의 Dribbble풍 미니멀 고대비.
- **프롬프트 구조**: 'Dribbble 같은 고에너지 15초 쇼릴, 60fps'라는 한 문장 원라이너
- **태그**: 쇼릴, 키네틱타이포, 아랍어, 고대비, 오렌지, 블루, flat, motion-graphics
- **주의**: 모든 텍스트가 아랍어라 다른 언어 타이포 레퍼런스로 쓸 때는 레이아웃·리듬만 참고

#### [Code-based UI motion design showreel](motion__code-based-ui-motion-design-showreel__2103273003555402193.md)
`motion__code-based-ui-motion-design-showreel__2103273003555402193` · 1:1 · 14s · 조회 1.0M · 에셋필요 X

- **요약**: 하나의 도형이 버튼→로더→체크→뮤직 플레이어→토글→차트→⌘K→토스트로 끊김 없이 모핑하는 코드 기반 UI 모션 쇼릴(루프)
- **어울리는 경우**: UI/UX 모션 포트폴리오 / 앱·SaaS 기능 소개 마이크로 인터랙션 / 제품 UI 티저 숏폼 / 디자인 시스템 컴포넌트 쇼케이스
- **잘하는 표현**: 컷 없이 한 요소가 크기·라운드·색을 모핑하는 원테이크 구성 / 클로즈드폼 스프링으로 계산한 정밀한 이징과 엣지별 다른 스프링(늘어나는 인디케이터) / 커서가 실제로 클릭·드래그하며 상태를 바꾸는 연출 / 마지막 프레임=첫 프레임 심리스 루프
- **스타일**: 따뜻한 라이트 그레이 캔버스에 흑백 UI 컴포넌트(검정 체크 원, 검정 뮤직 플레이어, 흰 차트 카드, ⌘K 팔레트, 검정 'Generate' 필 버튼)와 Geist 폰트. 플레이어 앨범아트만 주황-보라 그라디언트인 극미니멀 2D.
- **기술**: HTML 단일 파일 seek(t) 렌더, 클로즈드폼 스프링 수식, Playwright, ffmpeg tmix, numpy 비트 분석
- **프롬프트 구조**: <inputs>/<direction>/<structure>/<build>/<gotchas>/<start> XML 구조. 상태 체인 한 줄 구성 + 금지 목록 + 렌더 파이프라인 + 루프 함정
- **태그**: UI모션, 모핑, spring, 미니멀, 흑백, loop, 마이크로인터랙션, dribbble, 커서
- **주의**: 음원 입력 필요(로열티프리). 조회수 100만+로 검증된 패턴

#### [Animated pixel art wizard casting a spell](motion__animated-pixel-art-wizard-casting-a-spell__2102476258948927543.md)
`motion__animated-pixel-art-wizard-casting-a-spell__2102476258948927543` · 872x720 (약 6:5) · 11s · 조회 453K · 에셋필요 X

- **요약**: 밤하늘 성벽 위에서 마법사가 지팡이로 주문을 충전·발사하는 루프 픽셀아트 애니메이션
- **어울리는 경우**: 레트로 게임 티저/로딩 화면 / 픽셀아트 캐릭터 루프 / 짧은 SNS 루프 영상
- **잘하는 표현**: 128x96 논리 해상도 정수 스케일링으로 선명한 픽셀 / IDLE→CHARGE→CAST→RECOVER 상태 머신 포즈 / 원형으로 수렴·폭발하는 파티클과 투사체
- **스타일**: 짙은 남보라 밤하늘, 1px 별, 크림색 보름달, 회색 석재 바닥 위 빨간 로브·흰 수염 마법사. 하늘색·보라 마법 파티클 원. 16비트풍 제한 팔레트 2D 픽셀아트.
- **기술**: HTML Canvas 2D, vanilla JavaScript
- **프롬프트 구조**: 섹션형 기술 스펙(RENDERING/CHARACTER/ANIMATION/SCENE/QUALITY BAR): 해상도·팔레트·상태 머신·파티클 풀링까지 지정
- **태그**: 픽셀아트, pixel-art, 레트로, 16bit, Canvas2D, 루프, 파티클, 캐릭터

#### [Pixel character dodging meteors on a rainbow space track](motion__pixel-character-dodging-meteors-on-a-rainbow-space-track__2102515055116063144.md)
`motion__pixel-character-dodging-meteors-on-a-rainbow-space-track__2102515055116063144` · 16:9 · 19s · 조회 243K · 에셋필요 X

- **요약**: 주황 픽셀 캐릭터가 우주의 무지개 트랙을 질주하며 운석·빔을 자동 회피하는 Canvas 2D 도트 루프 애니메이션
- **어울리는 경우**: 레트로 게임풍 루프 배경 / 마스코트 캐릭터 숏 애니메이션 / 로딩·대기 화면용 루프
- **잘하는 표현**: 점프·대시·잔상 등 회피 액션의 타이밍 / 패럴랙스 별·스피드 라인으로 속도감 / 루프 끝 무지개 플래시(WARP)로 이음매 없는 루프 / 정수 픽셀 스냅된 깔끔한 도트
- **스타일**: 남색·보라 우주 배경에 디더링 성운과 고리 행성, 7색 무지개 띠 트랙, 주황 12x8 픽셀 캐릭터. 16비트 게임 데모 같은 2D 픽셀아트.
- **기술**: Vanilla JavaScript, Canvas 2D, 단일 HTML 파일
- **프롬프트 구조**: 일본어로 렌더링 규칙·캐릭터 픽셀 명세·장애물 패턴·회피 액션·상태머신·카메라·파티클·품질 기준을 섹션별로 정밀하게 지정한 스펙형
- **태그**: 픽셀아트, 도트, 레트로, 무지개, 우주, 루프, Canvas, 캐릭터애니

#### [Rick Astley's dance as moving blocks in HTML](motion__rick-astley-s-dance-as-moving-blocks-in-html__2103033635397898433.md)
`motion__rick-astley-s-dance-as-moving-blocks-in-html__2103033635397898433` · 16:9 · 58s · 조회 242K · 에셋필요 X

- **요약**: Rick Astley 춤을 코드로 그린 붓터치 스타일 HTML 애니메이션, 무대·고흐 별밤·액자 등으로 배경이 바뀜
- **어울리는 경우**: 음악 맞춤 댄스 애니메이션 / 패러디/밈 영상 / 회화풍 아트 모션
- **잘하는 표현**: 코트·마이크선이 흔들리는 과장된 리듬 동작 / 벽에 드리운 그림자 연출 / 씬 전환(벽돌 무대→커튼 무대→별밤→갤러리 액자)
- **스타일**: 트렌치코트 입은 인물의 2D 일러스트 애니메이션. 보라·주황 조명의 벽돌 아치, 붉은 커튼 무대, 고흐 '별이 빛나는 밤' 풍 소용돌이 붓터치 배경, 붉은 갤러리 벽의 금색 액자로 마무리. 회화적이고 따뜻한 톤.
- **기술**: HTML (코드로 그림·음악 생성)
- **프롬프트 구조**: 아트 디렉션 한 단락: 대상·재료(붓터치)·흔들릴 요소·길이·'모든 것을 코드로' 제약
- **태그**: 댄스, 붓터치, painterly, 별이빛나는밤, 밈, HTML, 음악싱크, 캐릭터
- **주의**: 제목의 'moving blocks'와 달리 실제 화면은 붓터치 일러스트; 실존 인물·곡 패러디라 상업 활용 주의

#### [TypingMind product intro motion video](motion__typingmind-product-intro-motion-video__2103703135902740699.md)
`motion__typingmind-product-intro-motion-video__2103703135902740699` · 16:9 · 15s · 조회 193K · 에셋필요 O

- **요약**: TypingMind(LLM 프론트엔드) 실제 UI 스크린샷과 로고로 만든 15초 제품 소개 모션그래픽
- **어울리는 경우**: SaaS 제품 런칭 티저 / 앱 UI 기능 하이라이트 / 음악 싱크 숏폼 광고
- **잘하는 표현**: 실제 UI 요소(입력창 타이핑, 모델 목록, 코드 블록)를 떼어내 띄우는 연출 / 'All your AI models. In one place.' 같은 굵은 카피 컷 / 로고 + 태그라인 엔드카드
- **스타일**: 짙은 남색-검정 그라데이션 배경에 다크모드 앱 UI 카드가 떠 있는 깔끔한 테크 광고 톤. 흰 굵은 산세리프 헤드라인에 하늘색 강조 단어를 쓴다.
- **프롬프트 구조**: '모션 디자이너 쇼릴처럼 15초, 제품 소개, 실제 스크린샷/로고 사용, 음악과 모션 싱크, 데모 말고 프로덕션급' 템플릿 프롬프트(같은 그룹 22건의 원형)
- **태그**: product-launch, SaaS, UI애니메이션, 다크모드, 네이비, 키네틱타이포, 15초, 광고
- **주의**: 같은 프롬프트를 쓴 22건 그룹의 대표 사례. 실제 제품 스크린샷이 있어야 함

#### [Apple Liquid Glass style UI motion showcase](motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152.md)
`motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152` · 1:1 · 16s · 조회 174K · 에셋필요 O

- **요약**: 파스텔 macOS 배경 위에서 Apple Liquid Glass 재질의 버튼·컨트롤센터·탭바·검색바가 모핑하는 UI 모션 쇼케이스
- **어울리는 경우**: iOS/macOS 스타일 앱 기능 소개 / UI 모션 포트폴리오 / 글래스모피즘 제품 티저 / 디자인 시스템 데모
- **잘하는 표현**: 굴절·스페큘러 림을 가진 글래스 재질(WebGL SDF) 표현 / 버튼 그룹→원→컨트롤센터 그리드→탭바→검색바→물방울로 이어지는 모핑 / Apple 스프링 파라미터 기반 모션 / 구간 라벨(MORPH/EXPAND/CONTROL/NAVIGATE)과 120 BPM 표기
- **스타일**: 라벤더·하늘색·연보라가 흐르는 파스텔 그라디언트 배경 위 반투명 흰 글래스 UI. 파란 Wi-Fi 타일 하나만 액센트이고 구석에 작은 대문자 라벨이 있는 밝고 깨끗한 Apple 키노트풍 2D/2.5D.
- **기술**: HTML 단일 파일 seek(t) 렌더, WebGL2 SDF 글래스 굴절 패스, numpy(비트 분석·UI 사운드 합성), Playwright, ffmpeg tmix
- **프롬프트 구조**: <role>/<inputs>(팔레트·폰트·아이콘·포인터)/<direction>(재질·모션 스프링 값·카메라·금지)/32비트 비트맵/<build>/<gotchas>/<start>로 구성된 초상세 XML 명세
- **태그**: liquid-glass, Apple, 글래스모피즘, UI모션, 파스텔, 모핑, spring, iOS, loop
- **주의**: 실제 영상은 프롬프트 비트맵(Dynamic Island·뮤직플레이어·Spotlight)과 달리 컨트롤센터·탭바·검색바 위주라 프롬프트가 사후 정리본일 가능성. 음원 파일 필요

#### [80-second glass and gold-leaf mosaic film](motion__80-second-glass-and-gold-leaf-mosaic-film__2102503027340988559.md)
`motion__80-second-glass-and-gold-leaf-mosaic-film__2102503027340988559` · 1:1 · 80s · 조회 131K · 에셋필요 X

- **요약**: 유리·금박 모자이크 타일이 떠올라 뒤집히고 날아다니며 물고기·새·바다 그림을 이루는 80초 정사각 WebGL 애니메이션
- **어울리는 경우**: 아트 필름/갤러리 상영용 루프 / 브랜드 무드 필름의 질감 실험 / 타일·파티클 전환 레퍼런스
- **잘하는 표현**: 타일 무리로 형상을 움직이는 파티클 플로킹 / 낮(금박)→밤(남색 별하늘) 장면 전환 / 타일이 흩어졌다 제자리에 맞물리는 재구성 연출
- **스타일**: 금박 바탕에 빨강·파랑 테두리, 주황 물고기와 흰 새, 청록·남색 물결의 비잔틴 모자이크풍. 밤 장면은 남색 바탕에 흰 타일 별과 달. 타일마다 광택이 있는 질감 2.5D.
- **기술**: WebGL2, plain JavaScript, 단일 HTML(라이브러리·에셋 없음)
- **프롬프트 구조**: 길이·포맷·기술 제약(라이브러리·에셋 금지) + 핵심 시각 은유 하나만 준 짧은 개념형 브리프
- **태그**: 모자이크, WebGL, 파티클, 금박, 아트필름, 정사각, 절차적생성, tile

#### [Four-minute 2D animation made with up to 15 agents](motion__four-minute-2d-animation-made-with-up-to-15-agents__2103135536634630632.md)
`motion__four-minute-2d-animation-made-with-up-to-15-agents__2103135536634630632` · 16:9 · 60s · 조회 107K · 에셋필요 O

- **요약**: 연필 스케치가 채색 캐릭터로 변하고 종이비행기를 타고 구름 위를 나는 소년 이야기를 담은 대사·자막 포함 2D 애니메이션(최대 15 에이전트 사용)
- **어울리는 경우**: 감성 브랜드 스토리 애니메이션 / 스케치→완성 연출 인트로 / 내레이션형 단편 애니
- **잘하는 표현**: 선화 스케치에서 채색으로 넘어가는 그리기 연출 / 연필 커서가 장면을 그려내는 메타 모티프 / 종이 찢김 마스크로 장면 전환
- **스타일**: 흰 종이 위 연필 선화와 애니풍 반실사 캐릭터, 황혼빛 분홍·보라·주황 구름 하늘과 네온 도시. 2D 일러스트 콜라주의 따뜻하고 몽환적인 톤, 중국어 자막과 타이머 표시.
- **기술**: 멀티 에이전트(최대 15개), 외부 이미지 생성 모델(추정, 메타 needs assets)
- **프롬프트 구조**: 중국어로 '아무 주제나 4분 2D 애니를 만들어 놀라게 하라' + 에이전트 15개·도구 자유 사용만 지시한 짧은 오픈 프롬프트
- **태그**: 2D애니, 스케치, 종이비행기, 구름, 감성, 스토리, multi-agent, 일러스트
- **주의**: 프롬프트에 구체 스타일 지시가 없어 결과 재현 어려움. 메타상 4분 작품 중 60초 클립

#### [Distilbook motion graphics showreel](motion__distilbook-motion-graphics-showreel__2103469807375208546.md)
`motion__distilbook-motion-graphics-showreel__2103469807375208546` · 16:9 · 40s · 조회 106K · 에셋필요 X

- **요약**: DistilBook(PDF→손그림 설명 영상 서비스)을 소개하는 40초 SaaS 프로모 모션그래픽
- **어울리는 경우**: SaaS 제품 런칭 티저 / 앱 기능 3단계 흐름 소개 / 클린 UI 프로덕트 데모
- **잘하는 표현**: UI 카드 목업과 진행 스텝 바(Add/Edit/Watch)로 흐름 설명 / 'Not a week. → About 6 minutes' 취소선+카운터 대비 카피 / 로고 인트로→CTA 아웃트로 북엔드 구조
- **스타일**: 흰 배경, 초록·파랑·분홍 책 로고, 진한 남색 산세리프와 파랑 강조, 손그림 수채 다이어그램 카드. 여백 많은 미니멀 플랫 2D.
- **기술**: Remotion, HyperFrames
- **프롬프트 구조**: '제품을 조사해서 쇼릴처럼 만들어라'는 2문장 원라이너(리서치 위임)
- **태그**: SaaS, product-launch, 미니멀, 화이트, UI목업, CTA, 모션그래픽, Remotion
- **주의**: showreel을 요청했지만 결과는 차분한 제품 소개형. 프레임 일부가 거의 빈 화면

#### [Reusable prompt template for a product motion video](motion__reusable-prompt-template-for-a-product-motion-video__2103723183899852885.md)
`motion__reusable-prompt-template-for-a-product-motion-video__2103723183899852885` · 16:9 · 15s · 조회 101K · 에셋필요 X

- **요약**: TypingMind(Teams/KiteWorks) SaaS 제품을 소개하는 15초 UI 중심 제품 모션 영상 (재사용 프롬프트 템플릿)
- **어울리는 경우**: SaaS 제품 소개 영상 / 기능 하이라이트 숏폼 / 런칭 티저
- **잘하는 표현**: 채팅 입력창·카드·앱 창 등 UI 목업 애니메이션 / 텍스트 선택 박스로 단어 교체(GPT-5/Claude/Gemini) / 카드가 궤도처럼 흩어지는 기능 클러스터 / 다크 로고 엔딩
- **스타일**: 밝은 화이트·라벤더 그라디언트 배경에 검정 굵은 산세리프 헤드라인, 그림자 있는 UI 카드·브라우저 목업, 보라-핑크 그라디언트 강조. 엔딩만 어두운 보라 배경 + 로우폴리 로고. 깔끔한 Apple/SaaS 런칭풍 2D.
- **프롬프트 구조**: [your product] 자리표시자가 있는 템플릿형 원라이너: 제품 페이지를 먼저 방문해 학습 후 직접 스크립트 작성
- **태그**: product-launch, SaaS, UI목업, 템플릿, 라이트모드, 키네틱타이포, 15초, 그라디언트
- **주의**: 프롬프트는 범용 템플릿이라 결과 품질은 제품 웹페이지 내용에 좌우됨

#### [Cosmos motion piece via HyperFrames](motion__cosmos-motion-piece-via-hyperframes__2103481296018092204.md)
`motion__cosmos-motion-piece-via-hyperframes__2103481296018092204` · 16:9 · 40s · 조회 79K · 에셋필요 X

- **요약**: Cosmos(cosmos.so)의 가치 제안을 이미지 그리드·검색 UI·키네틱 타이포로 전달하는 HyperFrames 런칭 영상
- **어울리는 경우**: SaaS·앱 런칭 영상 / 무드보드/이미지 큐레이션 서비스 소개 / 브랜드 톤을 따라가는 제품 프로모
- **잘하는 표현**: 이미지 타일이 흩어지고 모이는 그리드 모션 / 검색바·컬러 검색 등 실제 UI 재현 / 짧은 카피 키네틱 타이포와 흑백 반전 컷
- **스타일**: 오프화이트 배경에 굵은 검정 산세리프 카피, 사진 썸네일 그리드와 빨강 계열 이미지 묶음, 중간에 검정 화면 대비 컷. 미니멀 에디토리얼 2D.
- **기술**: HyperFrames
- **프롬프트 구조**: 대상 웹사이트를 스스로 리서치해 가치 제안을 찾고 브랜드 톤으로 런칭 영상을 만들라는 짧은 위임형 프롬프트
- **태그**: product-launch, SaaS, 키네틱타이포, 미니멀, 이미지그리드, HyperFrames, 브랜드, 에디토리얼
- **주의**: 특정 실제 브랜드(cosmos.so) 자료를 웹에서 가져와 만든 결과라 브랜드 의존적

#### [Cocktail recipe explainer motion graphic](motion__cocktail-recipe-explainer-motion-graphic__2102853258582880547.md)
`motion__cocktail-recipe-explainer-motion-graphic__2102853258582880547` · 1:1 · 30s · 조회 76K · 에셋필요 O

- **요약**: 빈 잔에 얼음·진·캄파리·베르무트를 붓고 저어 네그로니를 완성하는 30초 레시피 설명 모션그래픽
- **어울리는 경우**: 레시피/요리 단계 설명 / 제조 공정 how-to / 단계형 튜토리얼 숏폼 / 식음료 브랜드 SNS 콘텐츠
- **잘하는 표현**: 잔에 액체가 차오르는 레벨 변화와 눈금 표시 / 단계 카드(STEP n OF 6, 계량, 진행 바)와 하단 스텝 인디케이터 / 병 기울여 붓기·스푼 젓기 같은 오브젝트 동작 / 완성 컷의 장식(트위스트, 반짝임) 마무리
- **스타일**: 오프화이트 배경에 손그림 느낌 외곽선의 2D 플랫 일러스트, 코랄 레드 포인트 컬러와 굵은 둥근 디스플레이 타이포. 친근하고 깔끔한 인포그래픽 톤.
- **기술**: JavaScript/HTML 기반 애니메이션(프롬프트 근거)
- **프롬프트 구조**: 짧은 대화형 요청 한 단락(30초, explainer 스타일, 재료+계량 표시)
- **태그**: 레시피, explainer, 2D일러스트, 인포그래픽, 단계설명, 칵테일, 플랫디자인, 튜토리얼
- **주의**: 메타상 에셋 필요로 되어 있으나 프롬프트 본문에는 첨부 에셋 언급이 없다

#### [Infinite-zoom landscape loop](motion__infinite-zoom-landscape-loop__2103129343253778767.md)
`motion__infinite-zoom-landscape-loop__2103129343253778767` · 16:9 · 20s · 조회 72K · 에셋필요 O

- **요약**: 빈티지 오브젝트(회중시계, 카메라 렌즈, 돋보기, 손거울) 속을 통과하며 풍경에서 풍경으로 끝없이 줌인하는 20초 루프
- **어울리는 경우**: 뮤직비디오/인트로 루프 / 여행·노스탤지어 브랜드 무드 영상 / 포털식 장면 전환 레퍼런스
- **잘하는 표현**: 오브젝트의 유리 안에 다음 세계를 넣는 포털 전환 / 깊이맵 3레이어 패럴랙스 / 로그 비례로 일정 속도를 유지하는 지수 줌 / 콜라주 오브젝트(모자, 우산)의 2프레임 애니
- **스타일**: 실사 풍경(설산, 해안 절벽, 사막, 안개 호수)에 흰 종이 테두리가 있는 흑백 하프톤 오브젝트를 붙인 빈티지 콜라주. 바랜 세피아·청록 톤, 필름 그레인과 비네팅.
- **기술**: Magnific MCP, Seedream 5 Pro, GPT 2.5 이미지, Kling 2.5, Lyria 3, After Effects 스타일 타임라인
- **프롬프트 구조**: LOOK/WORLDS/HOW/DELIVER 섹션 구조 + 수치(패럴랙스 Z 범위, BPM·마디, fps) + 비용 목록 승인·단계별 스크린샷 확인 게이트
- **태그**: infinite-zoom, 콜라주, 빈티지, 루프, 패럴랙스, 포털전환, 생성이미지, 필름그레인
- **주의**: 외부 생성 모델(Magnific 경유) 크레딧이 필요하고 결과 품질이 생성 이미지에 좌우됨

#### [15-second motion design showreel (detailed prompt)](motion__15-second-motion-design-showreel-detailed-prompt__2103424524297420829.md)
`motion__15-second-motion-design-showreel-detailed-prompt__2103424524297420829` · 16:9 · 15s · 조회 68K · 에셋필요 X

- **요약**: '모션 디자이너로서의 15초 이력서 릴'을 주제로 커브, 키네틱 타이포, 막대그래프, 3D 기둥, 파티클 소용돌이를 거쳐 'Claude.' 엔드카드로 끝나는 쇼릴
- **어울리는 경우**: 브랜드/자기소개 쇼릴 / 모션 기법 몽타주 인트로 / 테크 제품 티저
- **잘하는 표현**: 주황 점 하나를 씬 간 연결 모티프로 사용 / 베지어 이징 커브·벨로시티 그래프 같은 모션 용어의 시각화 / 2D 타이포에서 3D 기둥 그리드, 파티클 나선으로 넘어가는 기법 전환 / 타임코드·눈금이 있는 뷰파인더 프레임 HUD
- **스타일**: 거의 검은 배경에 흰색과 단 하나의 빨강-주황 액센트를 쓰는 미니멀 다크 모드. 이탤릭 세리프 'feeling'과 굵은 산세리프 'Claude.'를 섞었고, 압출된 흰 기둥 그리드 같은 3D 요소가 들어간다.
- **프롬프트 구조**: 역할 + 길이 + '첫 1초 훅 → 기법 시퀀스 → 깔끔한 엔드프레임' 구조와 음악 컷 리듬만 지시하는 짧은 원라이너급 프롬프트
- **태그**: 쇼릴, 모션디자인, 다크모드, 주황액센트, 키네틱타이포, 미니멀, showreel, 15초
- **주의**: 프롬프트가 매우 짧아 결과가 모델 재량에 크게 의존함. 사용 툴 정보 없음

#### [Beat-synced showreel from real clips](motion__beat-synced-showreel-from-real-clips__2102554209166000267.md)
`motion__beat-synced-showreel-from-real-clips__2102554209166000267` · 16:9 · 20s · 조회 52K · 에셋필요 O

- **요약**: 실제 세로 UGC 클립들을 비트에 맞춰 클립 월·3D 캐러셀·대형 수치·로고로 엮은 광고툴 'hooklab' 제품 쇼릴
- **어울리는 경우**: SaaS 제품 런칭 티저 / 광고/마케팅 툴 프로모 / 실사 클립 기반 비트 싱크 쇼릴 / SNS 광고 크리에이티브
- **잘하는 표현**: 120BPM 10마디에 모든 컷을 다운비트에 맞춘 편집 / 마스크 타이포 리빌과 버튼에서 원이 열리는 매치 컷 전환 / 바닥 반사가 있는 3D 클립 캐러셀과 모션블러 휩 / '4.2x' 대형 수치 푸시 컷
- **스타일**: 오프화이트 배경의 검정 산세리프 훅 문장으로 시작해 검은 다크 공간으로 전환. 세로 인물 UGC 클립 그리드와 곡면 캐러셀, 회색 크롬풍 대형 숫자, 주황-빨강 단일 액센트 로고의 하이엔드 미니멀.
- **기술**: HTML 단일 파일 seek(t) 시간함수 렌더, ffmpeg(JPEG 시퀀스 추출, tmix 모션블러, loudnorm), numpy(비트 분석), Playwright 렌더
- **프롬프트 구조**: <inputs>/<direction>/<structure>/<build>/<gotchas>/<start> XML 태그 구조. 금지 효과 목록, 마디별 구성, 빌드 파이프라인, 함정, '스토리보드 먼저 보여달라'는 시작 조건
- **태그**: 쇼릴, 비트싱크, product-launch, UGC, 3D캐러셀, 미니멀, 다크, 매치컷, SaaS
- **주의**: 사용자 소유 실사 클립·음원·제품 정보가 필수. 빌드 파이프라인 자체가 재사용 가치 큼

#### [Reels made with Opus 5.5](motion__reels-made-with-opus-5-5__2105283486487896448.md)
`motion__reels-made-with-opus-5-5__2105283486487896448` · 9:16 · 23s · 조회 48K · 에셋필요 O

- **요약**: 앱 'Dump'의 스티커 기능 출시를 알리는 9:16 iOS 스타일 트레일러 (무료 팩→Pro 해금→CTA)
- **어울리는 경우**: 앱 기능 출시 릴스 / 모바일 앱 광고 숏폼 / 프리미엄 플랜 업셀 홍보
- **잘하는 표현**: 굵은 산세리프 한 마디 카피('21 packs.', 'Free.', 'Every pack.') / 스티커 콜라주·카드 캐러셀 연출 / 오렌지 풀스크린 CTA 엔딩
- **스타일**: 오프화이트 배경에 검정 굵은 둥근 산세리프 카피, 흰 테두리 스티커(디스코볼·8볼·커피 등) 컬러풀 콜라주와 카드형 팩 캐러셀, 오렌지 'Pro' 알약 버튼, 마지막은 오렌지 전면 + 흰 로고·URL 버튼. 깔끔한 iOS 미니멀.
- **기술**: Mtioon (메타 기재)
- **프롬프트 구조**: 짧은 브리프 한 문장: 비율·스토리 순서(추가→무료→Pro 해금)·'iOS/Apple 미학'·제공 음악 지정
- **태그**: 앱홍보, reels, 9:16, iOS, 스티커, product-launch, CTA, 미니멀
- **주의**: 스티커 이미지·음악 등 앱 에셋 의존

#### [Professional 30-second product showreel](motion__professional-30-second-product-showreel__2103845264649761062.md)
`motion__professional-30-second-product-showreel__2103845264649761062` · 16:9 · 30s · 조회 46K · 에셋필요 O

- **요약**: 마크다운 에디터 'mdfor.dev'를 실제 제품 UI를 분해한 컴포넌트·아이콘 애니메이션으로 소개하는 30초 제품 쇼릴
- **어울리는 경우**: 웹 앱·개발자 도구 런칭 영상 / 제품 기능 하이라이트 프로모 / 에디토리얼 톤 브랜드 영상
- **잘하는 표현**: 'Write *markdown' 타이핑 타이포로 제품 성격을 바로 전달 / 스크린샷을 그대로 쓰지 않고 에디터 UI·자물쇠·노트북 아이콘으로 재구성 / 방사형 선 버스트 같은 음악 맞춤 전환 / 로고+URL 엔딩
- **스타일**: 크림·아이보리 종이톤 배경에 검정 세리프 헤드라인, 테라코타(주황-갈색) 단일 액센트, 얇은 선화 아이콘. 중간에 회갈색 전환 프레임이 있는 따뜻한 에디토리얼 미니멀 2D.
- **기술**: Remotion
- **프롬프트 구조**: 쇼릴 원문 프롬프트에 '실제 제품 스크린샷·로고 사용, 음악 필수·모션 싱크, 스크린샷을 컴포넌트로 분해해 애니메이션' 요구를 덧붙인 문단형
- **태그**: product-launch, 에디토리얼, 세리프, 크림톤, Remotion, SaaS, UI분해, 미니멀
- **주의**: 실제 제품 사이트·로고 에셋 필요

#### [Motion design and sound engineering demo](motion__motion-design-and-sound-engineering-demo__2103557735086428547.md)
`motion__motion-design-and-sound-engineering-demo__2103557735086428547` · 16:9 · 90s · 조회 45K · 에셋필요 X

- **요약**: 'CLAUDE MOTION DESIGN REEL' 90초 쇼릴: 궤도·점구·파티클·대형 타이포를 피아노 스코어에 맞춘 모션 데모
- **어울리는 경우**: 브랜드/AI 쇼릴 / 미니멀 모션 그래픽 데모 / 음악 동기화 타이포 영상
- **잘하는 표현**: 굵은 컨덴스드 산세리프 키네틱 타이포 / 궤도 링·점 구체·파티클 형태 변환 / 오렌지 단일 액센트 컬러 절제 / 사운드 디자인·피아노 스코어 동기
- **스타일**: 차콜 블랙 배경에 크림색 굵은 산세리프 'CLAUDE', 주황 단일 액센트(점·선), 흰 점으로 된 구체와 궤도 링. 중간에 밝은 크림 배경의 대형 'THE' 타이포 반전. 미니멀·에디토리얼 2D.
- **프롬프트 구조**: 원라이너 쇼릴 요청 + 길이(90초)·비율·'S급 사운드, 신스 금지, 오리지널 피아노 스코어'·1080p mp4 출력 조건
- **태그**: showreel, 미니멀, 키네틱타이포, 오렌지액센트, 다크모드, 파티클, sound-design, piano

#### ['The First Spark' procedural hand-drawn short](motion__the-first-spark-procedural-hand-drawn-short__2102910531560731063.md)
`motion__the-first-spark-procedural-hand-drawn-short__2102910531560731063` · 16:9 · 60s · 조회 44K · 에셋필요 O

- **요약**: 잉크 방울에서 태어난 작은 캐릭터가 세상을 그려내다 혼돈을 겪고 빛으로 정리하는 60초 손그림풍 절차적 애니메이션 단편
- **어울리는 경우**: 감성 브랜드 필름/매니페스토 영상 / 창작·탄생 은유를 쓰는 오프닝 / 미니멀 일러스트 스토리텔링
- **잘하는 표현**: 잉크 번짐·스플래시로 화면을 덮는 혼돈 연출 / 발자국 잉크가 나무와 언덕으로 자라나는 절차적 성장 애니메이션 / 흑백 속 마지막에만 쓰인 따뜻한 빛 포인트 컬러 / renderFrame(time) 결정론적 타임라인 + MP4 export 설계
- **스타일**: 따뜻한 오프화이트 종이 질감 위 검은 잉크 실루엣의 2D 미니멀 손그림. 여백이 넓고, 후반 혼돈 장면에서는 거대한 잉크 덩어리와 튀김이 화면 절반을 덮으며, 끝에 주황 빛 원이 하나 보인다.
- **기술**: JavaScript, HTML5 Canvas 2D, FFmpeg (프레임 단위 export)
- **프롬프트 구조**: 역할 지정 + 기술 제약(금지 목록) + 비주얼 방향 + 초 단위 6씬 스토리 + 애니메이션 품질 기준 + 결정론적 타임라인/내보내기 + 단계별 개발 절차를 담은 장문 명세
- **태그**: 잉크, 손그림, 미니멀, 흑백, Canvas2D, procedural, 단편애니, 스토리텔링, 오프화이트
- **주의**: 참고 이미지 1장을 첨부해 비주얼 언어를 맞춘 프롬프트라 같은 결과를 내려면 비슷한 레퍼런스 이미지가 필요함

#### [Persian-language motion graphics showreel](motion__persian-language-motion-graphics-showreel__2103562127474819150.md)
`motion__persian-language-motion-graphics-showreel__2103562127474819150` · 16:9 · 15s · 조회 42K · 에셋필요 O

- **요약**: 개인 크리에이터(MatinSenpai)의 활동을 페르시아어 타이포로 보여주는 15초 다크 쇼릴
- **어울리는 경우**: 개인 브랜드/크리에이터 소개 영상 / SNS 채널 지표 하이라이트 / 비라틴 문자 키네틱 타이포 참고
- **잘하는 표현**: 페르시아어·한자 대형 타이포 키네틱 / 숫자 카운트업(154,000)으로 지표 강조 / 텔레비전·이빨 웃음 같은 거친 일러스트 모티프 / 글리치 텍스트 스크램블
- **스타일**: 검정 배경에 흰·빨강 브러시/스텐실 질감의 거대한 페르시아어 글자, 화면 가장자리의 작은 HUD 메타 텍스트, 크림색 반전 컷 하나. 그런지·스트리트 무드.
- **프롬프트 구조**: 개인 웹사이트 URL과 '나에 대해 아는 것'을 주고 언어만 지정한 원라이너 쇼릴 요청
- **태그**: 키네틱타이포, 페르시아어, 다크모드, 그런지, 쇼릴, 개인브랜딩, 카운터, RTL
- **주의**: 모델이 사용자 정보와 웹사이트에 접근해야 하는 개인 맞춤 프롬프트. 구현 기술 미상

#### [Apple-keynote style launch film](motion__apple-keynote-style-launch-film__2107123710251434330.md)
`motion__apple-keynote-style-launch-film__2107123710251434330` · 1:1 · 29s · 조회 39K · 에셋필요 O

- **요약**: 가상 브랜드 'Develop' 사진 인화 서비스의 Apple 키노트풍 원테이크 런칭 필름 (리퀴드 글래스·커서 인터랙션)
- **어울리는 경우**: 제품/서비스 런칭 필름 / 앱·웹 UI 플로우 시연 / 원테이크 모핑 전환 광고
- **잘하는 표현**: 컷 없이 오브젝트가 변형되며 이어지는 원테이크 전환 / iOS 26 리퀴드 글래스 UI 재현 / 커서 클릭·드래그로 트리거되는 스크린스튜디오식 줌 / 120BPM 비트맵 기반 타이밍
- **스타일**: 오프화이트 캔버스 위 검정 알약 버튼과 커서, 노을 언덕·아치·우주비행사 등 고해상 사진, 잠금화면 글래스 시계, Safari 창 랜딩 페이지 'from screen to wall.', 검은 원형 플러드 전환. 정사각 2D, 깔끔한 Apple 미니멀.
- **기술**: HTML 단일 파일, SVG 필터(feDisplacementMap), Canvas, Playwright 렌더, ffmpeg, Mixkit SFX/음악, Pexels 스톡
- **프롬프트 구조**: XML 태그 섹션(<inputs>/<direction>/<structure>/<build>/<gotchas>/<start>) 구성: 금지 목록 + 비트 단위 씬 구조 + 구현 규칙(시간 순수함수 seek) + 함정 메모 + 비트맵·스틸 승인 후 제작
- **태그**: product-launch, Apple-style, 리퀴드글래스, 원테이크, 모핑, 1:1, 커서, 비트싱크
- **주의**: 사진 9~12장·음악·벽 그림자 스톡 클립 필요; 시트상 일부 프레임은 검은 플러드 전환 순간

#### [Orange dot motion design system](motion__orange-dot-motion-design-system__2107121188027707651.md)
`motion__orange-dot-motion-design-system__2107121188027707651` · 16:9 · 15s · 조회 36K · 에셋필요 X

- **요약**: 주황 점 하나가 토글, 글자 점, 스프링 그래프, 도형, 회전 타이포 링을 거쳐 엔드카드로 돌아오는 15초 루프형 2D 모션 디자인 필름
- **어울리는 경우**: 브랜드 모티프 기반 쇼릴 / 모션 원리(스프링, 이징) 설명 숏폼 / 루프 SNS 영상
- **잘하는 표현**: 한 오브젝트가 모든 씬을 잇는 연속성 연출 / 글자별로 휘며 'Reduce Motion'이 'Motion'으로 바뀌는 키네틱 타이포 / 같은 스프링 함수로 그래프와 점을 움직이는 정합성 / 3D 원형으로 도는 텍스트 링과 모션블러
- **스타일**: 따뜻한 오프화이트와 거의 검은 배경을 오가며 비비드 주황 한 색만 쓰는 플랫 2D. 굵은 산세리프 타이포, 그라데이션·글로우 없이 날카롭고 절제된 모션이다.
- **기술**: 단일 HTML, seek(t) 기반 프레임 계산 (closed-form spring)
- **프롬프트 구조**: <inputs>/<direction>/<structure>/<build>/<gotchas>/<start> XML 태그로 나눈 구조화 프롬프트. 입력값 질문 → 비트맵 + 스틸 4장 확인 후 본 렌더
- **태그**: 모션디자인, 키네틱타이포, 스프링, 주황액센트, 오프화이트, 루프, 2D, 미니멀, beat-sync
- **주의**: 음원 트랙과 문구 입력을 먼저 받아야 하는 템플릿형. 프롬프트 구조 자체가 재사용 가치가 높음

#### [30-second motion promo for Kody](motion__30-second-motion-promo-for-kody__2103638102333858193.md)
`motion__30-second-motion-promo-for-kody__2103638102333858193` · 16:9 · 30s · 조회 34K · 에셋필요 X

- **요약**: 에이전트 자동화 도구 'Kody'를 코알라 마스코트와 키네틱 타이포로 소개하는 30초 모션 프로모
- **어울리는 경우**: 개발자 도구·SaaS 제품 소개 영상 / 마스코트 활용 브랜드 프로모 / 문제→해결 구조의 설명형 광고
- **잘하는 표현**: 'RE-BUILD.' 'Ask once. Save it. Trigger it.' 등 단계적 키네틱 타이포 / 마스코트 주위로 기능 아이콘(secrets·memory·triggers 등)이 방사형 배치되는 기능 맵 / 글로우 링 안 큐브 등 개념 오브젝트 연출 / CTA·URL로 끝나는 명확한 엔딩
- **스타일**: 어두운 네이비·차콜 배경에 굵은 흰 산세리프와 파랑·초록 강조. 3D 렌더 코알라 캐릭터 뒤로 금빛 방사광, 보라·빨강·노랑·파랑·초록 네온 아이콘 원. 중간에 크림색 플래시 전환 프레임.
- **기술**: Remotion
- **프롬프트 구조**: '모션 디자이너 쇼릴처럼 30초, 리서치부터 모든 결정 위임' 짧은 자율 위임형 프롬프트(같은 프롬프트 계열 그룹 4개 중 하나)
- **태그**: product-promo, 마스코트, 키네틱타이포, SaaS, 다크모드, 네온아이콘, Remotion, developer-tool
- **주의**: 마스코트 이미지는 제품 기존 에셋으로 보임. 프롬프트가 짧아 결과는 모델 재량 의존

#### [Code-based UI motion design showreel](motion__code-based-ui-motion-design-showreel__2106396375269134597.md)
`motion__code-based-ui-motion-design-showreel__2106396375269134597` · 1:1 · 14s · 조회 34K · 에셋필요 O

- **요약**: 하나의 UI 도형이 커서 클릭·드래그에 따라 버튼 → 체크 → 뮤직 플레이어 → 토글 → 차트 → ⌘K → 버튼으로 끊김 없이 모핑하는 14초 루프
- **어울리는 경우**: UI/UX 모션 포트폴리오 / 앱 마이크로 인터랙션 소개 / 디자인 시스템·컴포넌트 쇼케이스 / 제품 기능 데모 인서트
- **잘하는 표현**: 컷 없이 하나의 요소가 크기·라운드·색을 바꾸며 이어지는 모핑 / 실제 클릭·드래그를 수행하는 커서 연출 / 약한 오버슈트 스프링과 엣지별 분리 스프링(리퀴드 탭) / 120 BPM 비트마다 액션 배치와 심리스 루프
- **스타일**: 밝은 웜그레이 캔버스에 흑백 UI 컴포넌트와 Geist 계열 산세리프만 쓴 Dribbble풍 2D 미니멀. 앨범 아트의 작은 그라데이션 외엔 무채색.
- **기술**: 단일 HTML seek(t), Playwright 렌더, ffmpeg tmix 모션블러, numpy 비트 분석, Mixkit 음원
- **프롬프트 구조**: XML 태그 구조(<inputs>/<direction>/<structure>/<build>/<gotchas>/<start>) + 상태 체인 + 구현 규칙 + 함정 목록 + 먼저 입력 요청하는 시작 지시
- **태그**: UI모션, 모핑, 마이크로인터랙션, 미니멀, 흑백, 스프링, 루프, 비트싱크, Playwright
- **주의**: 음원(120 BPM)과 UI 상태 목록을 사용자가 줘야 한다. 바로 아래 Apple 스타일 런칭 영상과 같은 seek(t)/Playwright 템플릿 계열이다

#### [20-second kinetic identity bumper for TechHalla](motion__20-second-kinetic-identity-bumper-for-techhalla__2103411244468498547.md)
`motion__20-second-kinetic-identity-bumper-for-techhalla__2103411244468498547` · 1:1 · 20s · 조회 32K · 에셋필요 X

- **요약**: TechHalla 크리에이터용 20초 루프 키네틱 타이포 아이덴티티 범퍼(STOP SCROLLING → @TECHHALLA)
- **어울리는 경우**: 채널/브랜드 인트로·범퍼 / SNS 스크롤 멈춤 훅 / 선언형 메시지 타이포 광고 / 크리에이터 아이덴티티 영상
- **잘하는 표현**: 글자별 스프링 등장, 스크램블, 마스크 와이프 같은 키네틱 타이포 / 120 BPM 비트 그리드에 맞춘 히트 배치 / 마젠타/애시드 그린 인쇄 미스레지스트레이션 효과 / 3종 서체 위계(디스플레이 / 그로테스크 / 모노 크럼)
- **스타일**: 근검정 배경에 흰색 초굵은 산세리프와 마젠타·애시드 그린 포인트만 쓴 스트리트 포스터 스타일 2D. 모서리 크롭 마크와 모노 라벨이 있는 고대비 미니멀.
- **기술**: 단일 HTML, seek(t) 순수 함수 애니메이션, closed-form 스프링, 서브프레임 블렌딩 모션블러
- **프롬프트 구조**: 역할 부여 + 포맷/팔레트/타입 시스템 디자인 토큰 + 고정 메시지 순서 + 타임코드 내러티브 아크 + 필수 기법 9개 + 금지 목록
- **태그**: 키네틱타이포, kinetic-type, 범퍼, 다크모드, 마젠타, 애시드그린, 루프, 비트싱크, 포스터
- **주의**: 프롬프트는 1080x1080을 요구했지만 메타 해상도는 720x720. 사운드 없는 타이포 위주라 음악은 별도로 필요하다

#### [15-Second Motion Graphics Showcase](motion__15-second-motion-graphics-showcase__2106376222309761094.md)
`motion__15-second-motion-graphics-showcase__2106376222309761094` · 16:9 · 15s · 조회 25K · 에셋필요 X

- **요약**: 'MOTION' 타이틀로 시작해 리듬·타입·타이밍·안무 챕터를 거쳐 'CLAUDE.'로 끝나는 15초 모션그래픽 쇼릴
- **어울리는 경우**: 모션 디자이너 포트폴리오 릴 / 브랜드 아이덴티티 티저 / 챕터형 짧은 오프닝 타이틀
- **잘하는 표현**: 대형 볼드 산세리프와 도형(빨간 원)을 결합한 키네틱 타이포 / 챕터 번호·진행 바 HUD로 구조화된 리듬 / 3D 젤리 구체·구슬 체인 등 2D/3D 혼합 오브젝트 / 강한 원색 배경 컷 전환
- **스타일**: 검정·빨강·코발트 블루·크림 단색 배경을 교차하는 스위스/바우하우스풍 볼드 그래픽. 크림색 굵은 산세리프, 빨강 원 포인트, 광택 3D 빨강 구체와 빨강·파랑·흰 구슬 체인, 상하단 작은 라벨 HUD.
- **프롬프트 구조**: 중국어로 된 '15초 쇼릴, 도구 자유, 대담한 아트 디렉션으로 전력' 짧은 자율 위임형 프롬프트
- **태그**: 쇼릴, 키네틱타이포, 볼드, 원색, 스위스스타일, 3D, motion-reel, 챕터
- **주의**: 프롬프트에 도구·스타일 지시가 없어 재현성 낮음. 사용 도구 미상

#### [Motion graphic video made from GrotBot icon collection](motion__motion-graphic-video-made-from-grotbot-icon-collection__2105722219892789560.md)
`motion__motion-graphic-video-made-from-grotbot-icon-collection__2105722219892789560` · 16:9 · 184s · 조회 18K · 에셋필요 O

- **요약**: 약 5천 장의 Grot Bot 아이콘을 파티클·모자이크 큐브·그리드로 연출한 3분짜리 아이콘 컬렉션 모션그래픽
- **어울리는 경우**: 대량 이미지/아이콘 컬렉션 쇼케이스 / NFT·아바타 컬렉션 홍보 / 포토 모자이크·대량 썸네일 연출
- **잘하는 표현**: 수천 개 아이콘 파티클의 3D 공간 비행 / 아이콘들로 이루어진 회전 큐브·모자이크 로고 / 다분할 화면 전환
- **스타일**: 보라·주황·남색 배경에 작은 아이콘 수천 개가 흩날리는 고밀도 3D 파티클, 귀여운 애니 캐릭터 아이콘 클로즈업, 아이콘 모자이크로 된 큐브와 둥근 사각 로고. 약간 흐리고 비네팅 있는 화면.
- **프롬프트 구조**: 에셋 범위(Grot Bot 아이콘 5천 장)와 '최신 기법 총동원'만 지시한 한국어 원라이너
- **태그**: 아이콘, 파티클, 모자이크, 컬렉션, 3D, 대량이미지, grid, 한국어프롬프트
- **주의**: 5천 장 아이콘 에셋 필수. 184초로 길고 반복 구간이 많을 수 있음. 구현 기술 미상

#### [One-prompt motion graphic from codebase](motion__one-prompt-motion-graphic-from-codebase__2105268326381625845.md)
`motion__one-prompt-motion-graphic-from-codebase__2105268326381625845` · 16:9 · 30s · 조회 17K · 에셋필요 O

- **요약**: 앱 LaunchBuddy의 실제 스크린샷·로고를 컴포넌트로 분해해 애니메이션한 30초 제품 소개 모션그래픽
- **어울리는 경우**: 앱/SaaS 제품 소개 영상 / 앱스토어 프로모 영상 / 기능 하이라이트 런칭 티저 / 멀티 디바이스 지원 홍보
- **잘하는 표현**: 스크린샷을 카드·아이콘 단위로 분해한 UI 애니메이션 / 다크 네온 씬과 밝은 그라데이션 씬의 대비 전환 / 카운트다운 숫자 링 같은 리듬 포인트 / 칸반·체크리스트 등 실제 기능 화면 재구성
- **스타일**: 다크 네이비 네온(파란 글로우 라인, 블러 텍스트)과 밝은 흰-하늘색 그라데이션 UI 씬이 교차하는 2D 테크 프로모 톤. 마지막은 선명한 파란 배경 앱 아이콘+워드마크.
- **기술**: 코드 기반 모션그래픽(구체 스택 미명시), 실제 앱 스크린샷/로고
- **프롬프트 구조**: 쇼릴형 오픈 브리프 + 대상 제품 URL + 스크린샷을 분해해 애니메이트하라는 추가 지시
- **태그**: product-launch, 앱소개, SaaS, UI애니메이션, 네온, 그라데이션, 모션그래픽, 브랜드
- **주의**: 실제 제품 스크린샷/로고에 의존한다. 네온 글로우·카운트다운 링은 다소 템플릿 느낌이 있다

#### [Motion showreel with a fully code-synthesized soundtrack](motion__motion-showreel-with-a-fully-code-synthesized-soundtrack__2103538744695693512.md)
`motion__motion-showreel-with-a-fully-code-synthesized-soundtrack__2103538744695693512` · 16:9 · 15s · 조회 14K · 에셋필요 X

- **요약**: 코드로 직접 합성한 음악에 맞춰 컷이 떨어지는 15초 모션 디자이너 쇼릴(엔딩 'CLAUDE Motion Designer')
- **어울리는 경우**: 모션 디자인 쇼릴/포트폴리오 / 에이전시·스튜디오 브랜드 인트로 / 다양한 스타일 몽타주 티저 / 비트 싱크 짧은 광고
- **잘하는 표현**: 씬마다 완전히 다른 스타일(베지어 커브, 바우하우스 패턴, 유체 텍스처, 프레임 타이포)로 범위 과시 / 비트에 맞춘 컷 전환 / 슬라이스/스플릿 타이포 같은 전환 기법 / 외부 샘플 없는 코드 합성 사운드트랙
- **스타일**: 검정·오프화이트·코랄 레드를 축으로 파랑·라임이 섞인 기하 패턴과 보라-빨강 유체 마블이 교차하는 2D 그래픽 맥시멀 몽타주. 굵은 컨덴스드 산세리프 타이포.
- **기술**: 코드 기반 렌더(1920x1080 60fps MP4), 코드 오디오 합성, Cursor
- **프롬프트 구조**: 짧은 3문장 오픈 브리프(쇼릴 목적 + 코드 합성 음악 조건 + 해상도/출력 형식)
- **태그**: 쇼릴, showreel, 모션그래픽, 비트싱크, 코드사운드, 기하패턴, 타이포, 몽타주
- **주의**: 같은 프롬프트를 쓴 group(22개) 중 하나라 다른 결과와 비교하며 보는 게 좋다

#### [15-second intro to NISHIO Hirokazu's work](motion__15-second-intro-to-nishio-hirokazu-s-work__2103467539485671862.md)
`motion__15-second-intro-to-nishio-hirokazu-s-work__2103467539485671862` · 16:9 · 15s · 조회 13K · 에셋필요 O

- **요약**: 연구자 西尾泰和(NISHIO Hirokazu)의 활동·업적을 소개하는 15초 다크 테크 모션그래픽 쇼릴
- **어울리는 경우**: 인물/연구자 소개 인트로 / 포트폴리오·이력 쇼릴 / 컨퍼런스 연사 소개
- **잘하는 표현**: RGB 분리 글리치 대형 타이포 / 포인트 클라우드 구체·파티클 데이터 시각화 / 연도 태그가 붙은 업적 리스트 카드 / 일본어 굵은 고딕 헤드라인
- **스타일**: 검은 배경에 시안·마젠타·옐로 네온 포인트 클라우드와 광선, 흰/핑크 굵은 일본어 헤드라인, 모노스페이스 영문 서브카피와 HUD 모서리 라벨. 사이버/데이터 테크 무드의 2D+3D 파티클.
- **프롬프트 구조**: '모션 디자이너 쇼릴처럼, 15초' 원라이너 + 주제(인물 활동·업적) 지정
- **태그**: 인물소개, showreel, 다크모드, 네온, 파티클, 일본어타이포, 글리치, 데이터비주얼
- **주의**: 인물 정보는 사전 지식/자료 의존(needs_assets True)

#### [Brand motion showreel from a reference video](motion__brand-motion-showreel-from-a-reference-video__2103541149709615243.md)
`motion__brand-motion-showreel-from-a-reference-video__2103541149709615243` · 16:9 · 32s · 조회 13K · 에셋필요 O

- **요약**: 레퍼런스 영상의 비주얼 스타일을 따라 Distilbook(문서를 영상으로 바꾸는 서비스)을 소개하는 30초 모션그래픽 쇼릴
- **어울리는 경우**: SaaS/에듀테크 서비스 소개 / 손그림 두들 + 컬러풀 전환 브랜드 영상 / 레퍼런스 스타일 리메이크 작업
- **잘하는 표현**: 손글씨 'turn this into a video' 두들 연출 / 프리즘 무지개·카드 터널·동심원 링 같은 대담한 화면 전환 / 교과서 일러스트 같은 식물 도해 인서트
- **스타일**: 오프화이트 종이 질감 위 손그림 선화와 주황 꽃 마스코트로 시작해, 남색 배경의 프리즘 무지개, 카드가 소용돌이치는 터널, 원색 동심원 링으로 넘어가는 맥시멀 컬러 2D 혼합 스타일.
- **프롬프트 구조**: 레퍼런스 영상 다운로드 → 같은 스타일 적용 + 브랜드 리서치 + '쇼릴처럼 과감하게'를 요구하는 리메이크형 짧은 지시
- **태그**: 브랜드영상, 두들, 손그림, 무지개, 터널전환, SaaS, product-intro, 레퍼런스리메이크
- **주의**: 원본 레퍼런스 영상 없이는 재현 불가. 씬마다 스타일이 크게 달라 통일된 스타일 참고로는 산만함

#### [AI-generated animated video demo](motion__ai-generated-animated-video-demo__2105279421435572498.md)
`motion__ai-generated-animated-video-demo__2105279421435572498` · 16:9 · 141s · 조회 12K · 에셋필요 X

- **요약**: WebGL로 Vibe Coding Thailand 사이트(AI 책·강의)를 소개하는 2분 넘는 화려한 프로모션 영상으로, SFX와 BGM까지 코드로 제작
- **어울리는 경우**: 교육 플랫폼/커뮤니티 프로모션 / 웹사이트 소개 롱폼 트레일러 / 터미널/개발자 감성 브랜드 영상
- **잘하는 표현**: '$ ls ~/books' 같은 터미널 프롬프트 모티프 / 3D 공간에 떠 있는 웹페이지 카드와 원근으로 기울인 사이트 화면 / 워프 스피드 방사선 + 큰 태국어 키네틱 타이포 / 주황 하이라이트 박스로 키워드 강조
- **스타일**: 짙은 남색-보라 어둠 속 주황 액센트와 글로우가 들어간 3D 테크 무드. 노이즈 낀 소용돌이 오프닝, 별빛 속도선, 반사 바닥 위 떠 있는 UI 패널이 이어진다.
- **기술**: WebGL
- **프롬프트 구조**: WebGL 사용 + 길이(1.5~3분) + SFX/BGM 직접 제작 + '묻지 말고 mp4만 달라'는 위임형 태국어 짧은 지시
- **태그**: WebGL, 프로모션, 터미널, 태국어타이포, 다크, 주황액센트, 3D-UI, warp, 롱폼
- **주의**: 실제 사이트 화면을 쓰므로 사실상 사이트 스크린샷이 필요하고, 141초로 길어 리듬이 늘어지는 구간이 있을 수 있음

#### [Looping product launch motion template](motion__looping-product-launch-motion-template__2105927781678747965.md)
`motion__looping-product-launch-motion-template__2105927781678747965` · 1:1 · 24s · 조회 12K · 에셋필요 O

- **요약**: 워드마크 마침표 안으로 들어가 '자는 동안 일하는' 가상 제품 nightshift의 밤→아침을 iOS 글래스 UI로 보여주는 24초 원테이크 루프 런칭 영상
- **어울리는 경우**: SaaS·AI 에이전트 제품 런칭 영상 / 하나의 오브젝트가 계속 변형되는 원테이크 모션 / 루프형 소셜 광고
- **잘하는 표현**: 컷 없이 형태가 모핑되는 연속 전환 / 밤→새벽→낮 사진 크로스페이드로 시간 경과 / 글래스 패널·커서 클릭 등 UI 시연 / 곡 비트에 맞춘 비트맵 타이밍
- **스타일**: 아치형 석조 문이 있는 언덕 사진 배경이 밤 남색→노을 주황→맑은 하늘로 변하고, 그 위에 iOS풍 반투명 글래스 필·흰 캘린더 카드와 굵은 흰 산세리프. 실사 사진+2D UI 합성의 깔끔한 프리미엄 톤.
- **기술**: HTML Canvas, Playwright 렌더, 외부 사진·음원·SFX 에셋, Geist 폰트
- **프롬프트 구조**: <inputs><direction><structure><build><gotchas><start> XML 태그 섹션으로 입력 요청·연출 금지사항·비트별 구조·구현 규칙·함정까지 담은 재사용 템플릿형
- **태그**: product-launch, 원테이크, 루프, 글래스모피즘, iOS, SaaS, morph, 템플릿
- **주의**: 밤/낮 정렬 사진, 낮 사진, 음원 등 사용자 에셋이 있어야 재현 가능

#### [Motion design showreel exploring "overthinking"](motion__motion-design-showreel-exploring-overthinking__2103566030916239768.md)
`motion__motion-design-showreel-exploring-overthinking__2103566030916239768` · 9:16 · 15s · 조회 10K · 에셋필요 O

- **요약**: 'Overthinking' 개념을 사이키델릭 콜라주·글리치 타이포로 풀어낸 15초 세로형 모션 쇼릴
- **어울리는 경우**: 감정·심리 개념 숏폼 / 세로형 SNS 모션 쇼릴 / 아트 포스터 스타일 인트로
- **잘하는 표현**: 회전하는 원형 궤도 위 단어 타이포 / RGB 글리치·반복 타이포 폭주 연출 / 점 하나에서 시작해 'breathe.'로 수렴하는 감정 곡선
- **스타일**: 검은 우주 배경과 남색·주황 그리드, 꽃·석고상 얼굴·극장 의자 콜라주, 무지개 광선과 RGB 글리치. 레트로 사이키델릭 맥시멀 2D 콜라주에 VHS 프레임 UI.
- **프롬프트 구조**: 개념 하나와 첨부 그래픽 영감만 주는 한 문장 원라이너
- **태그**: 쇼릴, 사이키델릭, 콜라주, 글리치, 세로영상, 키네틱타이포, overthinking, 맥시멀
- **주의**: 첨부 그래픽 에셋에 크게 의존. 같은 그룹(22개) 변형 중 하나

#### [Motion designer showreel with custom brand kit](motion__motion-designer-showreel-with-custom-brand-kit__2103742861971726495.md)
`motion__motion-designer-showreel-with-custom-brand-kit__2103742861971726495` · 16:9 · 15s · 조회 8K · 에셋필요 O

- **요약**: 광선·3D 도형·유체·3D 타이포를 빠르게 이어 붙인 15초 모션 디자이너 쇼릴
- **어울리는 경우**: 모션 디자인 포트폴리오 오프닝 / 에이전시/스튜디오 브랜드 릴 / 기법 종합 샘플러
- **잘하는 표현**: 다양한 기법(라인 라이트, 3D 프리미티브, 유체 마블링, 퍼프 3D 타이포) 전환 / 다크/크림 배경을 교차하는 리듬 / HUD식 타임코드 프레임 장식
- **스타일**: 검정 노이즈 그리드 위 흰 광선, 반사 바닥 위 파랑 구·빨강·노랑 큐브의 원색 3D, 보라·빨강·노랑 유체 위 아웃라인 'FLUID', 부풀린 흰 3D 'MOTION', 크림 배경 'SHOWREEL '26'과 원·사각·삼각 로고.
- **프롬프트 구조**: 기법 목록을 나열한 한 문단 브리프(키네틱 타이포, 유체, 파티클, 마스킹 등) + 톤 지시
- **태그**: 쇼릴, showreel, 3D타이포, 유체, 원색, 키네틱타이포, 포트폴리오, 다크모드
- **주의**: 제목의 커스텀 브랜드 키트는 프롬프트에 없음(별도 첨부로 추정). 장면 간 연결보다 기법 나열 성격

#### [Chaotic brain-rot style motion video](motion__chaotic-brain-rot-style-motion-video__2103664956482941143.md)
`motion__chaotic-brain-rot-style-motion-video__2103664956482941143` · 9:16 · 154s · 조회 6K · 에셋필요 X

- **요약**: Claude 시점의 1인칭 독백을 키네틱 텍스트와 글리치로 풀어낸 세로형 '브레인롯' 모션 영상
- **어울리는 경우**: AI/브랜드 페르소나 독백 숏폼 / 세로형 SNS 텍스트 모션 / 제품 런칭 무드 필름 / 타이포 중심 감성 영상
- **잘하는 표현**: 상단 컨텍스트 진행 바(context 0%→full)로 시간 경과를 시각화 / 세리프 이탤릭과 산세리프를 섞은 대사 타이포 / RGB 분리 글리치 'TOKEN' 같은 임팩트 컷 / 터미널 카드(/profile.md) 등 UI 소품 활용
- **스타일**: 거의 검정 배경에 오프화이트 텍스트와 코랄 오렌지 강조만 쓰는 다크 미니멀 2D. 모노스페이스 HUD와 흐릿한 코드 라인 배경, 간헐적 크로마 글리치. '카오틱'이라는 요청과 달리 화면은 절제된 편이다.
- **기술**: Python, ffmpeg
- **프롬프트 구조**: 짧은 단락 요청(도구 지정 + 9:16 + 브레인롯 + AI 1인칭 관점 개인화)
- **태그**: 9:16, 세로영상, 키네틱타이포, 다크모드, 글리치, 독백, Python, ffmpeg, AI페르소나
- **주의**: 제목은 '카오틱 브레인롯'이지만 실제 결과는 차분한 다크 타이포 영상이다. 2분 30초로 길다

### product (제품 프로모) — 11건 (조회수순)

#### [Working computer built from logic gates with OS](product__working-computer-built-from-logic-gates-with-os__2104301990985498783.md)
`product__working-computer-built-from-logic-gates-with-os__2104301990985498783` · 16:9 · 62s · 조회 273K · 에셋필요 X

- **요약**: 논리 게이트부터 CPU·메모리·OS·테트리스 게임까지 직접 만든 컴퓨터를 3D로 시각화하고 게이트 단위까지 줌인하는 데모
- **어울리는 경우**: CS 개념 설명(컴퓨터 구조) / 기술력 쇼케이스 / 줌인 스케일 다이빙 연출
- **잘하는 표현**: CRT 모니터→칩 다이→게이트 회로로 이어지는 연속 줌 / 신호가 흐르는 글로우 회로 시각화 / 하단 자막형 내레이션 캡션('Bullet time' 등)
- **스타일**: 어두운 3D 공간의 베이지 CRT 모니터에 초록 단색 테트리스('NANDTRIS'), 청록·노랑 글로우 라인의 칩 다이·NAND 게이트 회로, 좌측 모노스페이스 디버그 패널과 하단 컨트롤 바. 테크·레트로 컴퓨팅 무드.
- **기술**: 3D 시각화 (구체 라이브러리 미기재)
- **프롬프트 구조**: 'go all out' 원라이너형 챌린지 프롬프트: 만들 구성요소 나열 + '진짜로 게이트 위에서 돌아가야' 제약 + 줌인 시각화 요구
- **태그**: CS, logic-gates, CPU, 줌인, 레트로컴퓨터, 테트리스, 3D, 교육
- **주의**: 인터랙티브 앱 화면 녹화; 시트상 대부분 UI 오버레이가 덮여 있음

#### [Character builder with sliders demo](product__character-builder-with-sliders-demo__2104587476014964879.md)
`product__character-builder-with-sliders-demo__2104587476014964879` · 16:9 · 20s · 조회 200K · 에셋필요 O

- **요약**: Magnific로 생성한 3D 캐릭터 PNG를 슬라이더(머리 크기, 체형, 키, 조명색, 배경)로 실시간 조절하는 웹 에디터 데모
- **어울리는 경우**: 캐릭터/아바타 커스터마이저 제품 데모 / 생성 이미지 후처리 툴 홍보 / SaaS 기능 시연 숏 클립
- **잘하는 표현**: 슬라이더 조작에 따른 캐릭터 변형 비포/애프터 / 컬러 라이팅·배경색 전환 / 캐릭터 포즈 변화로 생동감 연출
- **스타일**: Pixar풍 3D 소녀 캐릭터(검은 캡, 후디, 카고바지), 오른쪽에 흰 미니멀 컨트롤 패널. 배경은 베이지·보라·크림·민트로 바뀌고 좌상단 'Claude Opus 5.5' 라벨, 우상단 Magnific 로고.
- **기술**: Magnific, 웹 에디터(HTML/JS로 추정)
- **프롬프트 구조**: 기능 목록을 나열한 2문장 제품 요구(업로드, 조절 항목, 4:5 PNG 내보내기, 흰 UI)
- **태그**: 캐릭터, 커스터마이저, UI데모, 슬라이더, 3D캐릭터, product-demo, 화이트UI, Magnific
- **주의**: 캐릭터 이미지 에셋 필요. 포즈 변화는 에디터 기능이 아니라 여러 생성 이미지 교체로 보임(프롬프트 범위 밖)

#### [Apple-style product launch video](product__apple-style-product-launch-video__2103835273813496100.md)
`product__apple-style-product-launch-video__2103835273813496100` · 1:1 · 29s · 조회 132K · 에셋필요 O

- **요약**: 워드마크 → 홍채 셔터 → 사진 그리드 → 리퀴드 글래스 → 폰/맥 → 주문 → 실제 벽 액자로 끊김 없이 모핑하는 Apple 키노트풍 29초 런칭 필름
- **어울리는 경우**: 앱/서비스 제품 런칭 영상 / Apple 키노트 스타일 기능 소개 / 사진·커머스 서비스 프로모 / 원테이크 모핑 광고
- **잘하는 표현**: 크로스페이드 없이 형태 변형만으로 잇는 원테이크 씬 전환(블랙 플러드, 아이리스) / iOS 26 리퀴드 글래스 굴절 효과 / 커서가 클릭·드래그·롱프레스로 진행을 이끄는 데모 / 54비트 모두에 이벤트를 배치한 음악 구조 매핑
- **스타일**: 웜 오프화이트 캔버스와 검정 UI, 그 위에 AI 생성풍 실사 사진(초원 아치, 우주비행사)과 글래스 시계 UI가 얹힌 2D 프리미엄 미니멀. 검정 원형 플러드 전환이 크게 등장한다.
- **기술**: 단일 HTML seek(t), SVG feDisplacementMap 리퀴드 글래스, Playwright 렌더, ffmpeg(tmix, all-intra 재인코딩, loudnorm), Mixkit 음원·SFX, Pexels 스톡 영상
- **프롬프트 구조**: XML 태그 구조(<inputs>/<direction>/<structure>/<build>/<gotchas>/<start>) + 비트 단위 씬 서술 + 구현 기법·함정 상세 + 스틸·비트맵 확인 후 진행
- **태그**: product-launch, Apple스타일, 키노트, 리퀴드글래스, 원테이크, 모핑, 커서데모, 미니멀, 비트싱크
- **주의**: 사진 9-12장·음원·SFX·벽 스톡 영상 등 에셋 의존도가 높고 구현 난도가 매우 높다

#### [One-prompt SaaS launch video](product__one-prompt-saas-launch-video__2103066071838466494.md)
`product__one-prompt-saas-launch-video__2103066071838466494` · 16:9 · 46s · 조회 93K · 에셋필요 X

- **요약**: Notion을 소재로 실제 UI 이미지와 카피를 엮은 트위터식 SaaS 런칭 모션그래픽 영상
- **어울리는 경우**: SaaS 기능 소개 런칭 영상 / 제품 UI 하이라이트 숏 / 통합·자동화 기능 홍보
- **잘하는 표현**: 실제 제품 UI 스크린을 카드처럼 띄우는 연출 / 앱 아이콘이 흩어진 오프닝 카피 / 다크/라이트 배경 교차와 파란 강조어 카피
- **스타일**: 검정·네이비 다크 장면과 오프화이트 라이트 장면이 교차, 흰 산세리프 카피에 파란 강조어, 그림자 진 UI 카드. 깔끔한 2D 플랫 SaaS 광고 톤.
- **기술**: 웹에서 수집한 실제 제품 에셋
- **프롬프트 구조**: 유명 SaaS를 골라 실제 에셋을 웹에서 구해 트위터식 런칭 영상을 만들라는 자연어 한 문단 위임형
- **태그**: SaaS, product-launch, Notion, UI데모, 키네틱타이포, 라이트다크, 광고, motion-graphics
- **주의**: 실존 브랜드(Notion) 에셋을 가져와 만든 결과라 브랜드 의존적. 메타는 needs_assets false지만 실제로는 웹 에셋 수집

#### [Fast-Paced Brand Advertisement](product__fast-paced-brand-advertisement__2106101651010449796.md)
`product__fast-paced-brand-advertisement__2106101651010449796` · 9:16 · 14s · 조회 79K · 에셋필요 O

- **요약**: Claude 브랜드 요소(스타버스트, 세리프 레터, 조각상, 판화풍 도안)를 빠르게 모핑시키다 Claude 로고로 끝나는 세로형 브랜드 광고
- **어울리는 경우**: 브랜드 아이덴티티 광고 / 세로형 SNS 티저 / 아트 디렉션 중심 무드 필름 / 로고 리빌 엔딩
- **잘하는 표현**: 판화·도면풍 그래픽 위에 오렌지 포인트를 페인트처럼 얹는 레이어링 / 레터폼 구조선(원·사각 그리드) 애니메이션 / 타이포 분해·재조합('th / ink' → think) / 빠른 컷 템포와 로고 엔딩
- **스타일**: 순백 배경에 흑색 판화/에칭 일러스트, 흑백 대리석 조각상 사진, 클래식 세리프 타이포와 Claude 코랄 오렌지 점·별 포인트만 쓴 라이트모드 에디토리얼 2D. 여백이 많은 미니멀 콜라주.
- **기술**: 코드 기반 모션(구체 스택 미명시), SVG 애니메이션(프롬프트 언급), 외부 수집 이미지
- **프롬프트 구조**: 레퍼런스 영상 첨부 + 리서치 / 디자인 방향 / 규칙 / 아이디어 목록의 짧은 섹션형 브리프(레퍼런스 기법은 빌리되 디자인은 바꾸라는 리메이크 지시)
- **태그**: 브랜드광고, 9:16, 에디토리얼, 라이트모드, 세리프, 판화, 콜라주, 로고리빌, fast-paced
- **주의**: 첨부 레퍼런스 영상과 Claude 브랜드 자산에 의존한다. 특정 실존 브랜드 스타일이라 그대로 쓰기보다 레이어링 기법 참고용

#### [Product promo video in two aspect ratios](product__product-promo-video-in-two-aspect-ratios__2103419586964316483.md)
`product__product-promo-video-in-two-aspect-ratios__2103419586964316483` · 16:9 (9:16 버전 별도 제작) · 30s · 조회 38K · 에셋필요 O

- **요약**: AI 프롬프트 사례 모음 사이트 'GoodCase.ai'를 실제 사례 영상·사이트 화면으로 소개하는 30초 웹사이트 프로모(16:9·9:16 두 버전 중 16:9)
- **어울리는 경우**: 웹사이트·플랫폼 소개 영상 / SNS용 멀티 비율 프로모 / 콘텐츠 큐레이션 서비스 홍보
- **잘하는 표현**: 첫 3초에 가장 강한 실제 사례(접힌 지구 베네치아, 수영장 폭발 장면) 노출 / 사례 카드→상세 페이지→'완전 Prompt 원클릭 복사'로 이어지는 사용 흐름 / 실제 사이트 데이터 기반 화면 구성 / 로고+URL+썸네일 스트립 엔딩
- **스타일**: 실사·CG 사례 영상 프레임에 주황 태그와 흰 바탕 중국어 캡션을 붙인 구성과, 흰 배경 사이트 UI 캡처가 교차. 엔딩은 흰 배경 검정 'GoodCase.ai' 로고와 주황 URL 버튼.
- **기술**: Remotion, Python, ffmpeg, Playwright(사이트 캡처), 코드 생성 음악
- **프롬프트 구조**: 중국어 문단형 브리프: 소재 확보 방법(로컬 코드+실사이트), 사실 근거 요구, 타깃·구조(오프닝 3초/흐름/엔딩), 비율 2종, 음악은 코드로
- **태그**: website-promo, 제품소개, 멀티비율, 9:16, SNS, Remotion, 화면캡처, 중국어
- **주의**: 실제 사이트·로컬 코드 접근 전제. 화면 대부분이 타 사례 영상이라 고유 스타일 참고엔 약함

#### [Cinematic product launch film](product__cinematic-product-launch-film__2104805179401068964.md)
`product__cinematic-product-launch-film__2104805179401068964` · 16:9 · 100s · 조회 32K · 에셋필요 X

- **요약**: Claude Sonnet 5.5 출시를 파티클·대형 수치·UI 목업으로 표현한 약 100초 시네마틱 GTM 런칭 필름
- **어울리는 경우**: AI 모델·기술 제품 런칭 필름 / 벤치마크 수치 강조 영상 / 프리미엄 브랜드 캠페인
- **잘하는 표현**: 대형 퍼센트 수치 리빌 타이포 / 파티클 점에서 시작하는 오프닝 훅 / effort 슬라이더 등 UI 목업으로 기능 시연 / 절제된 오렌지 강조색 사용
- **스타일**: 짙은 검정·웜 브라운 배경에 크림색 세리프 대형 타이포, Claude 오렌지 포인트(이탤릭 강조어·별 심볼), 미세 파티클과 어두운 UI 패널. 절제된 프리미엄 다크 2D 모션.
- **프롬프트 구조**: 26개 번호 섹션으로 핵심 메시지·구간별 길이·씬 연출·벤치마크 수치·컬러·사운드·편집 언어·정확성 규칙·내레이션까지 기술한 초장문 크리에이티브 브리프
- **태그**: product-launch, AI모델, 시네마틱, 세리프타이포, 다크모드, 오렌지, 벤치마크, 브랜드필름
- **주의**: 특정 제품 수치·브랜드에 맞춘 브리프라 그대로 쓰기보다 구조만 참고. 시트상 일부 장면은 빈 카드처럼 단순함

#### [Promotional travel video about Poland](product__promotional-travel-video-about-poland__2102728913579327722.md)
`product__promotional-travel-video-about-poland__2102728913579327722` · 16:9 · 86s · 조회 25K · 에셋필요 O

- **요약**: 'Poland is so beautiful' 폴란드 관광 홍보용 86초 시네마틱 AI 생성 영상
- **어울리는 경우**: 국가·도시 관광 홍보 영상 / 문화유산·지역 브랜드 필름 / 시네마틱 B-roll 몽타주
- **잘하는 표현**: 골든아워 위주 랜드마크 실사풍 샷(바벨성, 브로츠와프 대성당) / 드론 항공샷(단풍 숲 사이 강) / 전통 의상 인물과 역사 재현 장면
- **스타일**: 황금빛 석양과 따뜻한 오렌지 톤, 아나모픽 레터박스의 포토리얼 생성 영상. 성, 밀밭의 민속 의상 여성, 가을 숲 항공샷, 탱크 전쟁 재현, 가로등 켜진 저녁 광장, 호수 일몰.
- **기술**: Higgsfield, Kling, Veo, Nano Banana 2, Sonilo, Codex
- **프롬프트 구조**: 목표·길이·주제 요소·톤(시네마틱, 아나모픽)과 사용 툴(Higgsfield MCP)만 지정한 폴란드어 짧은 브리프
- **태그**: 관광, travel, 시네마틱, 골든아워, AI생성영상, 드론, 레터박스, 폴란드
- **주의**: 외부 영상 생성 모델 의존이라 결과가 크레딧·모델 버전에 좌우됨. 'real scenes'를 요구했지만 실제론 생성 영상

#### [Promo video for a science-based book](product__promo-video-for-a-science-based-book__2103904736160120935.md)
`product__promo-video-for-a-science-based-book__2103904736160120935` · 16:9 · 60s · 조회 23K · 에셋필요 O

- **요약**: 폴란드어 과학책 'Piętnaście zagadek komórki(세포의 15가지 수수께끼)'를 소개하는 60초 모션그래픽 프로모션
- **어울리는 경우**: 도서/출판 프로모션 / 과학·역사 교양 콘텐츠 인트로 / 빈티지 고급 브랜드 영상
- **잘하는 표현**: 빈티지 과학 도판(DNA, 세포)을 원형 프레임과 아이콘으로 분해해 애니메이션 / 연도('2026', '1952')와 챕터 번호를 큰 세리프로 띄우는 편집 디자인 / 3D 책 목업 엔드카드
- **스타일**: 양피지 베이지와 짙은 갈색을 오가는 세피아 톤에 클래식 세리프 타이포, 손으로 채색한 듯한 고서 과학 일러스트. 1950년대 연구실 실사풍 이미지 인서트가 섞인 고급 출판물 무드다.
- **기술**: GPT-Image-2.5
- **프롬프트 구조**: TypingMind형 '쇼릴/실제 에셋/음악 싱크/프로덕션급' 템플릿에 '스크린샷을 그대로 쓰지 말고 컴포넌트로 분해해 애니메이션'을 덧붙인 변형
- **태그**: 도서프로모션, 세피아, 빈티지, 과학일러스트, 세리프, DNA, editorial, 출판
- **주의**: 책 표지와 내부 도판 등 실제 에셋에 의존하고, 일부 이미지는 GPT-Image로 생성됨

#### [Liquid glass web hero section](product__liquid-glass-web-hero-section__2106061619176620344.md)
`product__liquid-glass-web-hero-section__2106061619176620344` · 약 3:2 (1108x720) · 772s · 조회 11K · 에셋필요 O

- **요약**: Three.js 굴절 글래스 큐브 히어로 섹션을 만드는 13분 화면 녹화(Pinterest 레퍼런스 탐색→코드 생성→결과 페이지)
- **어울리는 경우**: 랜딩 페이지 히어로 제작 과정 튜토리얼 / 웹 3D 글래스 효과 레퍼런스 / AI 웹디자인 워크플로 시연
- **잘하는 표현**: 거대 헤드라인을 굴절·색분산시키는 글래스 오브젝트 효과 / 레퍼런스 이미지에서 결과물까지의 제작 과정 전체 노출 / 블랙 배경 대형 타이포 히어로 레이아웃
- **스타일**: macOS 데스크톱 화면 녹화. Pinterest 그리드와 코드/채팅 패널 옆으로 검은 배경 흰 대형 산세리프('Shaping Raw Forms', 'YOUR WHOLE DAY, ON ONE LINE.')와 투명 글래스 오브젝트, 흑백 'TALLY' 랜딩 페이지들이 보임.
- **기술**: Three.js r169, WebGL 커스텀 굴절 셰이더, GLTFLoader(외부 GLB), HTML/CSS/JS 단일 파일, Google Fonts Poppins
- **프롬프트 구조**: 외부 리소스 URL·HTML 구조·CSS 정확값·셰이더 수식·렌더 파이프라인·인터랙션·픽셀 좌표 레이아웃까지 지정한 '그대로 재현' 초상세 클론 명세
- **태그**: liquid-glass, Three.js, 히어로섹션, 랜딩페이지, 굴절, 화면녹화, 흑백, 웹디자인
- **주의**: 13분 작업 과정 녹화이며 화면 속 결과물('Shaping Raw Forms', Tally)이 프롬프트의 'Design World / Explore New Ideas'와 다름. 외부 GLB 모델 URL 의존

#### [Interactive frontend artifact](product__interactive-frontend-artifact__2106843514772639995.md)
`product__interactive-frontend-artifact__2106843514772639995` · 약 16:9 (1242x720) · 42s · 조회 9K · 에셋필요 O

- **요약**: igloo.inc 수준을 목표로 만든 가상 회사 'ERG'의 3D 인터랙티브 웹사이트를 스크롤하며 보여주는 화면 녹화
- **어울리는 경우**: 프리미엄 랜딩페이지/웹 3D 쇼케이스 / 브랜드 사이트 히어로 연출 참고 / 웹 에이전시 포트폴리오
- **잘하는 표현**: 사막 위 검은 모놀리스가 보로노이 균열 발광, 유리 큐브로 바뀌는 오브젝트 연출 / 텍스트 스크램블 효과(깨진 글자가 문장으로 정리) / 도트 매트릭스·하프톤과 파티클 모래시계
- **스타일**: 베이지 사막 실사풍 3D 배경과 짙은 갈색-검정 다크 섹션을 오가는 에디토리얼 웹 디자인. 굵은 그로테스크 산세리프 헤드라인, 주황 발광 포인트, 넓은 여백이 특징이다.
- **프롬프트 구조**: 참고 사이트 분석 후 '비슷한 수준, 복제 금지' + 독립 서브에이전트 채점 80% 이상까지 반복하라는 짧은 품질 루프형 지시
- **태그**: 웹사이트, 랜딩페이지, 3D웹, 모놀리스, 사막, 텍스트스크램블, 하프톤, editorial, interactive
- **주의**: 영상이 아니라 웹사이트 스크롤 녹화. 참고 사이트(igloo.inc) 분석이 전제이고, 사용 기술은 명시되지 않음

### education (교육/설명) — 12건 (조회수순)

#### [AI documentary about superintelligence](education__ai-documentary-about-superintelligence__2103304514329854102.md)
`education__ai-documentary-about-superintelligence__2103304514329854102` · 16:9 (854x480) · 315s · 조회 904K · 에셋필요 X

- **요약**: 영국인 여성 진행자가 나오는 넷플릭스 다큐풍 5분짜리 '초지능 입문' 설명 영상으로, 영상·이미지·음악 생성 모델로 에이전트가 전부 제작
- **어울리는 경우**: 실사 진행자가 있는 교양 다큐 / AI/기술 개념 설명 롱폼 / 일관된 캐릭터가 필요한 AI 실사 영상
- **잘하는 표현**: 한 진행자를 여러 장소(도서관, 서버룸, 템스강변, 시장)에서 일관되게 유지 / 시네마틱 조명과 얕은 피사계 심도 / 웨이퍼 클로즈업 같은 B-roll 인서트 / 타이틀 카드 'THE LAST INVENTION'
- **스타일**: 실사풍 생성 영상. 낙타색 코트를 입은 단발 여성 진행자, 틸·앰버 계열 영화 같은 색보정, 어두운 서버 복도와 녹색 램프 도서관 등 고급 다큐 톤이다.
- **기술**: Runway, Seedance 2.5, Nano Banana Pro, Lyria
- **프롬프트 구조**: 목표(5분, 넷플릭스 다큐, 위트 있는 영국 여성 진행자)·예산(크레딧 2.5만 이하)·해상도만 주고 나머지는 위임하는 구어체 자유 브리프
- **태그**: 다큐멘터리, AI실사, 진행자, 초지능, explainer, Runway, 캐릭터일관성, 시네마틱, 롱폼
- **주의**: 480p 저해상도이고 유료 생성 모델 크레딧에 크게 의존함. 코드 기반 모션그래픽 레퍼런스는 아님

#### [History of AI documentary short film](education__history-of-ai-documentary-short-film__2102844654169575547.md)
`education__history-of-ai-documentary-short-film__2102844654169575547` · 16:9 · 180s · 조회 199K · 에셋필요 X

- **요약**: 'the'라는 빛나는 토큰을 주인공으로 Transformer 논문부터 ChatGPT·추론·에이전트·AGI까지 AI 역사를 그린 3분 Remotion 모션 다큐
- **어울리는 경우**: 기술사·연대기 해설 영상 / AI/개념 강의 인트로 / 모티프 하나로 이어가는 스토리형 설명 영상
- **잘하는 표현**: 하나의 반복 모티프(토큰)로 시대를 잇는 내러티브 / 어텐션 선 네트워크·지구본 등 생성형 그래픽 / 모노 폰트 UI 패널로 툴 호출·코드 실행 표현 / 연도 라벨·카운터 숫자 타이포
- **스타일**: 짙은 검정 배경에 따뜻한 앰버 단일 강조색, 빛나는 노드 네트워크와 점 지구본, 모노스페이스 텍스트 패널. 2D 코드 생성 그래픽의 차분하고 시네마틱한 다크 톤.
- **기술**: Remotion, React, SVG/Canvas
- **프롬프트 구조**: 역할 부여 + 기술 셋업(해상도·fps·프레임 수) + 타임코드별 씬 샷리스트 + 타이포·모션·색·페이싱 크래프트 규칙 + 스틸 렌더 자가검수 지시
- **태그**: AI역사, 다큐, Remotion, 다크모드, 앰버, 네트워크그래프, 교육, storytelling, 타임라인

#### [Zoomable app architecture canvas](education__zoomable-app-architecture-canvas__2105309987983745060.md)
`education__zoomable-app-architecture-canvas__2105309987983745060` · 약 3:2 (1112x720) · 12s · 조회 185K · 에셋필요 O

- **요약**: 실제 앱 코드베이스를 읽고 가입·결제·파일 업로드 흐름을 줌/팬 가능한 아키텍처 캔버스로 시각화한 화면 녹화
- **어울리는 경우**: 시스템 아키텍처 설명 / 개발팀 온보딩 자료 / 데이터/요청 흐름 워크스루 / SaaS 내부 구조 소개
- **잘하는 표현**: 전체 맵에서 특정 노드로 줌인하는 탐색형 카메라 / 단계 패널과 연동된 흐름 하이라이트(파란 경로선) / 영역별 색 구분(Front doors, Upload and prepare, Modal, Cloudflare R2)
- **스타일**: 브라우저 안의 밝은 흰 캔버스에 파스텔 노랑·초록 영역 블록과 진한 파랑 연결선, 우측 단계 설명 사이드바가 있는 2D 다이어그램 UI. 정보 밀도가 높은 실무형 툴 화면.
- **기술**: 웹 캔버스 앱(구체 스택 미명시), 대상 시스템: Modal, Convex, Cloudflare R2
- **프롬프트 구조**: 구어체 상황 설명(무엇이 헷갈리는지, 어떤 흐름을 보고 싶은지) + 코드베이스 접근 전제, 시각 사양 없음
- **태그**: 아키텍처, 다이어그램, 줌캔버스, flow, 개발자도구, 인포그래픽, 교육, 라이트모드
- **주의**: 사용자 앱 코드베이스가 있어야 재현 가능하고, 영상이 아니라 인터랙티브 툴 녹화다. 텍스트가 작아 영상 프레임 그대로는 가독성이 낮다

#### [Zoom journey from a cell to quantum fields](education__zoom-journey-from-a-cell-to-quantum-fields__2103099756167991347.md)
`education__zoom-journey-from-a-cell-to-quantum-fields__2103099756167991347` · 16:9 · 107s · 조회 72K · 에셋필요 X

- **요약**: 대장균 세포에서 B-DNA, 원자, 탄소-12 핵, 양성자 내부를 거쳐 양자장까지 스케일을 연속 줌인하는 과학 교육 애니메이션 'All the Way Down'
- **어울리는 경우**: 과학 강의 개념 설명(스케일·미시세계) / Powers of Ten식 줌 여정 콘텐츠 / 다큐 인트로·교육 채널 썸네일 영상
- **잘하는 표현**: 여러 스케일을 끊김 없이 잇는 연속 줌 전환 / 각 단계 제목·설명 문단·크기 눈금(스케일 바)을 붙인 교과서형 정보 레이아웃 / 분자 볼앤스틱, 쿼크 글로우, 양자장 노이즈 등 스케일별 다른 시각 언어
- **스타일**: 검은 배경 위 발광 파티클과 반투명 3D 구조의 다크 사이언스 일러스트. 청록·주황·분홍 포인트, 좌하단 이탤릭 세리프 대제목과 본문, 우측 세로 스케일 눈금, 작은 모노스페이스 주석.
- **기술**: JavaScript(브라우저 단일 애니메이션)
- **프롬프트 구조**: '세포→DNA→원자→양자장으로 줌, 과학적으로 정확하고 경외감 있게' 수준의 짧은 원라이너
- **태그**: 과학교육, 줌인, 스케일, DNA, 양자, 다크모드, 인포그래픽, powers-of-ten, 파티클

#### [Animated cycloid lesson](education__animated-cycloid-lesson__2106052083040256293.md)
`education__animated-cycloid-lesson__2106052083040256293` · 16:9 · 128s · 조회 70K · 에셋필요 X

- **요약**: 갈릴레오의 최단강하선 문제(직선 vs 원호 vs 사이클로이드)를 Canvas 2D로 풀어낸 일러스트 수학사 강의
- **어울리는 경우**: 수학·물리 개념 설명 / 과학사 스토리텔링 강의 / 비교 실험 시각화
- **잘하는 표현**: 인물 일러스트 씬과 다이어그램 씬의 교차 / 경로별 낙하 시간 비교 수치 표시 / 고지도·고서 페이지로 시대감 연출
- **스타일**: 양피지 종이 질감 위 손그림 느낌의 2D 일러스트: 촛불 서재의 갈릴레오, 펼쳐진 'Discorsi' 고서, 라틴어 유럽 고지도, 손글씨풍 레이블과 빨강 사이클로이드 곡선. 따뜻한 세피아 톤.
- **기술**: Canvas 2D
- **프롬프트 구조**: 튀르키예어로 문제·역사적 결론만 서술 + 'Canvas 2D로 최선을 다해 애니메이션화' 지시
- **태그**: 교육, 수학, 물리, cycloid, Canvas2D, 양피지, 일러스트, 과학사

#### [Animated pelican explains a shell command](education__animated-pelican-explains-a-shell-command__2103149526244618682.md)
`education__animated-pelican-explains-a-shell-command__2103149526244618682` · 16:9 · 30s · 조회 66K · 에셋필요 X

- **요약**: 외발자전거 탄 펠리컨이 서커스 무대에서 생선을 저글링하며 쉘 파이프라인 명령을 단계별로 설명하는 TTS 애니메이션
- **어울리는 경우**: CLI/코드 한 줄 해설 강의 / 개발자 교육 숏폼 / 마스코트 진행형 explainer / 단계별 파이프라인 개념 설명
- **잘하는 표현**: 명령어 각 단계를 하이라이트하며 터미널 출력 변화를 보여주는 구조 / 캐릭터 + 터미널 + 하단 자막의 3단 레이아웃 / 합성 음성 내레이션과 자막 동기화 / 결과 요약(체크 표시, 3 unique users)으로 마무리
- **스타일**: 빨강-보라 줄무늬 서커스 커튼과 나무 무대 위 2D 벡터 일러스트 펠리컨, 오른쪽엔 다크 macOS 터미널 창. 플랫 일러스트와 코드 UI가 섞인 친근한 분위기.
- **기술**: Kokoro TTS, 코드 기반 2D 애니메이션(구체 스택 미명시)
- **프롬프트 구조**: 한 문장 원라이너(캐릭터·설명 대상 명령어·부가 동작만 지정)
- **태그**: explainer, 터미널, 쉘명령, 캐릭터, 펠리컨, TTS, 2D일러스트, 교육, 자막

#### [Zero-shot documentary on Jewish history](education__zero-shot-documentary-on-jewish-history__2103564391170089429.md)
`education__zero-shot-documentary-on-jewish-history__2103564391170089429` · 16:9 · 223s · 조회 53K · 에셋필요 O

- **요약**: 참고 영상을 바탕으로 유대인 역사 전체를 양피지 톤 선화 일러스트와 연표 바로 풀어낸 약 4분 다큐 영상
- **어울리는 경우**: 역사 연대기 다큐 / 인용문 중심 해설 영상 / 장기간 타임라인 내레이션 콘텐츠
- **잘하는 표현**: 하단 연표 바와 연도 표시로 시대 위치 안내 / 선이 그려지는 라인 드로잉 일러스트 / 대형 세리프 인용문 타이포
- **스타일**: 초반은 베이지 양피지 배경에 갈색 선화(유물·성전·지도), 후반은 짙은 다크 브라운 배경에 금색 라인 아트(자유의 여신상·책)로 바뀌는 2D 미니멀 빈티지 다큐 톤.
- **프롬프트 구조**: 참고 영상을 폴더에 주고 '영감을 받아 전체 역사를 다루라', 강한 훅·몰입·감동만 요구하는 자유도 높은 짧은 프롬프트
- **태그**: 역사다큐, 유대사, 라인드로잉, 양피지, 금색, 타임라인, 인용문, education
- **주의**: 프롬프트가 폴더 속 참고 영상에 의존하고 사용 도구가 명시되지 않아 재현성 낮음

#### [Doc-to-video explainer (Open Alignment)](education__doc-to-video-explainer-open-alignment__2103545533474206118.md)
`education__doc-to-video-explainer-open-alignment__2103545533474206118` · 16:9 · 84s · 조회 49K · 에셋필요 O

- **요약**: Open Alignment 문서를 바탕으로 AI가 음악·비주얼을 직접 골라 만든 84초 영감형 설명 영상
- **어울리는 경우**: 문서/에세이 → 영상 변환 / 비전·미션 선언형 브랜드 필름 / AI·테크 주제 강연 오프닝
- **잘하는 표현**: 굵은 대문자 키네틱 타이포와 문장 리빌 / 실루엣 라인아트 메타포 이미지(비행기, 말 탄 사람) / 다크/라이트 장면을 교차하는 리듬 / 노랑 하이라이트 콜아웃 라벨
- **스타일**: 검정 배경+흰 라인아트+형광 노랑 포인트, 또는 크림색 종이 배경+흑백 판화풍 일러스트+노란 태양 원. 큰 산세리프 대문자와 이탤릭 세리프를 섞은 에디토리얼 2D 모션그래픽.
- **기술**: fal.ai, ElevenLabs
- **프롬프트 구조**: 주제 문서만 주고 음악 선택·시각화 방식을 전적으로 위임하는 짧은 자율 위임형 브리프
- **태그**: 에디토리얼, 키네틱타이포, 다크모드, 라인아트, explainer, AI, inspirational, 노랑포인트
- **주의**: 원본 문서가 필요하고 프롬프트에 스타일 지시가 없어 결과가 모델 재량에 크게 좌우됨

#### [Epic documentary: History of Chinese Civilization](education__epic-documentary-history-of-chinese-civilization__2103964025683927166.md)
`education__epic-documentary-history-of-chinese-civilization__2103964025683927166` · 16:9 · 217s · 조회 34K · 에셋필요 X

- **요약**: 권(卷)별로 시대를 나눠 서예 대자 키워드·선화·연표 HUD로 중국 문명사를 훑는 3분 37초 편년체 다큐 영상
- **어울리는 경우**: 역사·연대기 교육 영상 / 챕터형 다큐 타이틀 시퀀스 / 동양풍 브랜드/문화 콘텐츠 / 음악 박자에 맞춘 키워드 몽타주
- **잘하는 표현**: 朱印(붉은 도장) 권 번호·세로 왕조명·하단 두루마리 타임라인 등 일관된 HUD 시스템 / 검정·금박 화풍과 선지 백묘 화풍의 교차 / 서예 대자 키워드를 구절 단위로 등장시키는 타이포 / 비트 그리드·스토리보드 선결정 후 렌더하는 박자 맞춤 편집
- **스타일**: 검은 바탕에 금빛 서예 '卷一'과 붉은 도장 박스 키워드(肇始·礼乐·一统·交融), 문양 띠가 있는 어두운 화면과, 아이보리 선지 위 먹선 선화(다리·배, 컨테이너선)와 붓글씨(市井繁华·改革开放) 화면이 교차하는 2D 동양 그래픽.
- **기술**: 코드 프레임 단위 렌더, ffmpeg 합성, 코드 생성 음악(오음계)
- **프롬프트 구조**: 중국어 6줄의 압축된 아트 디렉션: 음악=시계(BPM·악기 진화), 두 화풍 교차, 권별 주색·문양, HUD 구성, 전환 방식, '먼저 비트 그리드와 분镜표 확정 후 렌더' 순서 지시
- **태그**: 역사다큐, 서예, 동양풍, 연표, HUD, chapter, 키네틱타이포, 비트싱크, ffmpeg
- **주의**: 중국사 특화 콘텐츠라 HUD·화풍 구조를 차용하는 용도로 참고

#### [History of Indonesia animated documentary](education__history-of-indonesia-animated-documentary__2103511590884815282.md)
`education__history-of-indonesia-animated-documentary__2103511590884815282` · 16:9 · 53s · 조회 19K · 에셋필요 X

- **요약**: 인도네시아 역대 대통령(수카르노~조코 위도도)을 연도·지도·데이터로 훑는 다크 톤 모션그래픽 역사 다큐
- **어울리는 경우**: 역사·정치 연대기 설명 / 국가/인물 타임라인 영상 / 데이터 저널리즘 스타일 리포트
- **잘하는 표현**: 점묘 지도 위 위치 하이라이트와 경로 라인 / 연도 카운터와 수치 강조 타이포 / 인물별 이름·별칭·업적 카드 레이아웃
- **스타일**: 거의 검정 배경에 흰 굵은 산세리프 인물명, 빨강 이탤릭 세리프 별칭, 도트 매트릭스 인도네시아 지도와 붉은 글로우 포인트, 노란 숫자 강조. 신문/아카이브 문서 카드가 가끔 삽입되는 다큐 그래픽.
- **프롬프트 구조**: '모션 디자이너 쇼릴처럼' 자유 위임 원라이너 + 주제(인도네시아 역대 대통령) 한 줄 추가
- **태그**: 역사, 타임라인, 인포그래픽, 도트맵, 다크모드, documentary, 키네틱타이포, 데이터

#### [Gmail features explainer short](education__gmail-features-explainer-short__2106958663525314769.md)
`education__gmail-features-explainer-short__2106958663525314769` · 16:9 (내부 숏폼은 9:16) · 32s · 조회 16K · 에셋필요 O

- **요약**: '일이 빨라지는 Gmail 기능 5선' 세로 숏폼을 Claude Code 스킬로 생성하는 과정을 보여주는 영상
- **어울리는 경우**: 'N선' 랭킹형 정보 숏폼 / 앱/SaaS 기능 소개 쇼츠 / 제작 자동화 스킬 템플릿 참고
- **잘하는 표현**: 번호(1/5~5/5)+큰 항목명+파랑·분홍 2색 코멘트 박스의 일관된 포맷 / 음성 길이에 맞춘 자막·이미지 전환 규칙 / 출처 확인·스크립트 승인 등 제작 절차 체크리스트
- **스타일**: Claude Code 터미널 화면 오른쪽에 세로 숏폼 미리보기가 떠 있는 구성. 숏폼은 주황 방사형 배경, 흰 박스에 굵은 일본어 고딕, 빨강 글씨 타이틀, Gmail UI 스크린샷.
- **기술**: Claude Code SKILL.md, Python 빌드 스크립트, Suno, Higgsfield, Blender, After Effects
- **프롬프트 구조**: SKILL.md 형식(name/description 프런트매터) + 8단계 번호 절차(선정→사실확인→대본승인→소재출처→디자인 규칙→검수→산출물)
- **태그**: 랭킹숏폼, 5선, explainer, Gmail, 세로영상, 자막, SKILL, 일본어
- **주의**: 영상이 결과물 단독이 아니라 터미널+미리보기 화면 녹화. 메타의 Blender/AE 등은 프롬프트에 근거 없음

#### [Explainer video of 9 football rules](education__explainer-video-of-9-football-rules__2105922894924501283.md)
`education__explainer-video-of-9-football-rules__2105922894924501283` · 16:9 · 69s · 조회 13K · 에셋필요 X

- **요약**: Three.js로 만든 PS2풍 로우폴리 선수들과 TV 중계식 AR 그래픽으로 축구 규칙 9개(오프사이드, 파울, 핸드볼 등)를 설명하는 체코어 해설 영상
- **어울리는 경우**: 스포츠 규칙/전술 해설 / TV 중계 그래픽(HUD, 로어서드) 스타일 설명 영상 / 3D 장면에 AR 주석을 겹치는 교육 콘텐츠
- **잘하는 표현**: 정지 화면 + 탈색 + 발광 AR 라인/링/측정치 오버레이 / 방송용 HUD(규칙 번호, 로어서드, 판정 패널, 상태 표시) / 규칙별 6~8초 리듬과 stinger 전환 / renderFrame(t) 결정론적 렌더 파이프라인 명세
- **스타일**: 야간 스타디움 조명 아래 로우폴리 3D 선수와 잔디, 청록·빨강·호박색 네온 AR 그래픽이 겹치는 스포츠 중계 룩. 좌하단 청록 번호 박스 로어서드와 우하단 판정 패널, 노란 카드 대형 그래픽이 보인다.
- **기술**: Three.js, Puppeteer, ffmpeg, Python (numpy/scipy 사운드 합성), Claude Code
- **프롬프트 구조**: 파라미터 섹션(종목 교체 가능) + 기술 파이프라인 + 폴더 구조 + 월드/캐릭터/AR/HUD 디자인 규격 + 규칙별 샷 시나리오 + 가독성 최소 px + 사운드 + 검수 절차까지 담은 초정밀 제작 명세서
- **태그**: 스포츠해설, AR그래픽, 방송HUD, Three.js, 로어서드, explainer, 로우폴리, 결정론적렌더, 인포그래픽
- **주의**: 텍스트가 전부 체코어이고, 종목만 바꿔 재사용하도록 템플릿화돼 있어 파이프라인 레퍼런스로 특히 유용함

### production (제작 파이프라인) — 7건 (조회수순)

#### [Remake of the 'Claude Pop' music video](production__remake-of-the-claude-pop-music-video__2102801274173587569.md)
`production__remake-of-the-claude-pop-music-video__2102801274173587569` · 16:9 · 142s · 조회 3.9M · 에셋필요 O

- **요약**: AI 특이점 주제 팝송 'Claude Pop' 뮤직비디오 리메이크: 해바라기 캐릭터와 오렌지 머리 주인공이 등장하는 종이 질감 2D 애니메이션
- **어울리는 경우**: 뮤직비디오 / 밈·인터넷 컬처 기반 바이럴 영상 / 캐릭터 중심 가사 모션그래픽
- **잘하는 표현**: 가사 키네틱 타이포와 장면 구성 / 종이 질감 + 리소그래프풍 일러스트 / 날짜·P(doom) 퍼센트 등 UI 스티커 오버레이 / 밈 레퍼런스(에바 축하 장면 등) 패러디
- **스타일**: 크림색 종이 질감 위 남색·오렌지·핑크 제한 팔레트 리소/스크린프린트풍 2D 일러스트. 해바라기 얼굴 캐릭터, 오렌지 머리 여성 주인공, 대형 눈·방사형 선 배경, 하단 박스 가사 자막과 우상단 날짜 태그.
- **기술**: JavaScript 애니메이션, fal API 이미지 생성, Seedance 2.5, ElevenLabs
- **프롬프트 구조**: 장문 크리에이티브 브리프: 원본 MV·오디오·소스코드 제공 + 스타일 방향(K-pop, 페이퍼리, 인터넷 브루탈리즘) + 생성모델 파이프라인(캐릭터시트→영상생성→JS 오버레이 로토스코프) + 검수 루프·예산 언급
- **태그**: 뮤직비디오, MV, 리소그래프, 종이질감, 캐릭터, 가사타이포, 밈, AI-progress
- **주의**: 원본 음원·MV·외부 API 키와 생성모델에 크게 의존해 재현 어려움

#### [Bilingual Gossip Video](production__bilingual-gossip-video__2106144184449085474.md)
`production__bilingual-gossip-video__2106144184449085474` · 9:16 · 351s · 조회 59K · 에셋필요 X

- **요약**: Elon Musk × Shivon Zilis 결별을 다룬 세로형 '吃瓜'(가십) 해설 영상 (중·영 이중 버전, TTS 내레이션)
- **어울리는 경우**: 시사·가십 해설 숏폼 / SNS 게시물 인용형 뉴스 영상 / 다국어 내레이션 영상 자동화
- **잘하는 표현**: 챕터형 상단 타이틀 바('TEA' 라벨) / 트윗·문자 스크린샷 카드 인용과 하이라이트 / 실제 영상 클립 + 하단 2줄 자막 / 워터마크·출처 표기
- **스타일**: 실사 뉴스·인터뷰 클립 위주의 세로 화면. 상단 검정 그라디언트 바에 핑크 'TEA' 배지와 흰 굵은 챕터 제목, 우상단 'X@dotey' 워터마크, 하단 흰 굵은 2줄 자막, 문자 스크린샷·트윗 카드(형광 하이라이트) 삽입.
- **기술**: Gemini 3.8 Flash TTS, yt-dlp, STT 검수
- **프롬프트 구조**: {화제}{링크} 자리표시자 템플릿 + 내용·소재·규격·화면·납품 전 검수 체크리스트를 불릿으로 정리
- **태그**: 가십, 뉴스해설, 9:16, 자막, TTS, 스크린샷카드, 실사클립, 템플릿
- **주의**: 실존 인물 사생활·초상권 이슈와 타인 영상 클립 사용; 스타일보다 자동화 워크플로 참고용

#### [Opus 5.5 plus Gemini TTS demo](production__opus-5-5-plus-gemini-tts-demo__2103590367518171295.md)
`production__opus-5-5-plus-gemini-tts-demo__2103590367518171295` · 16:9 · 15s · 조회 53K · 에셋필요 O

- **요약**: Cominka사 영업직 채용 PR을 간사이 사투리 TTS 내레이션과 함께 만든 15초 모션그래픽 영상
- **어울리는 경우**: 기업 채용 광고 / 회사 소개 숏폼 / TTS 내레이션 포함 SNS 광고
- **잘하는 표현**: 질문형 훅 카피('당신의 열의와 실력, 제대로 평가받고 있나요?')로 시작 / 숫자로 보는 회사(150社以上·2年·35%·50%) 인포그래픽 / 사진 패널 기울임·모션블러 전환 / Gemini TTS 음성 결합
- **스타일**: 딥그린 배경에 흰 명조풍 일본어 타이포와 빨강 포인트, 빨강 풀스크린 전환, 실사 직원 사진 콜라주, 흰 배경 대형 숫자 그리드. 엔딩은 녹색 배경 '営業職、募集中' + 빨강 ENTRY 버튼의 기업 채용 톤.
- **기술**: Gemini 3.8 Flash TTS
- **프롬프트 구조**: 일본어 캐주얼 요청: 쇼릴 프롬프트 + 채용 사이트 참고·영업직 모집·관서 사투리 TTS 검토 지시
- **태그**: 채용광고, recruit, TTS, 일본어, 기업PR, 인포그래픽, 딥그린, 실사사진
- **주의**: 채용 사이트 사진·디자인 에셋 의존. 영상 렌더 도구는 메타에 없음

#### [Talking-head video converted to line-art B-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md)
`production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956` · 9:16 · 84s · 조회 34K · 에셋필요 O

- **요약**: 토킹헤드 세로 영상을 우하단 원형 PIP로 줄이고 말하는 개념에 맞춘 선화 B-roll 애니를 메인 화면에 넣은 84초 재편집본
- **어울리는 경우**: 강의·지식 숏폼 리패키징 / 토킹헤드에 개념 일러스트 B-roll 자동 삽입 / 팟캐스트/인터뷰 클립 시각화
- **잘하는 표현**: 발화 개념과 동기화된 선화 아이콘(막대인간, 자물쇠, 체크리스트) / 원형 PIP+하단 자막의 일관된 레이아웃 / 상단 1-2-3 진행 스텝 인디케이터
- **스타일**: 크림색 종이 배경에 검은 손그림 선, 노랑·빨강·파랑·초록 포인트 컬러의 귀여운 2D 두들. 우하단 노랑 테두리 원형 인물 PIP, 굵은 흰 외곽선 중국어 자막.
- **프롬프트 구조**: 입출력 파일명 + 3개 번호 요구(PIP 배치, 내용 추종 B-roll, 원음·자막·길이 유지)의 짧은 편집 지시
- **태그**: 토킹헤드, B-roll, 선화, 두들, PIP, 세로영상, 강의, explainer
- **주의**: 원본 토킹헤드 영상 필수. 구현 기술 정보 없음

#### [AI pipeline short video with Opus 5.5](production__ai-pipeline-short-video-with-opus-5-5__2105370568178479476.md)
`production__ai-pipeline-short-video-with-opus-5-5__2105370568178479476` · 21:9 (1680x720) · 30s · 조회 25K · 에셋필요 O

- **요약**: SF 슬럼 아파트에서 깨어나 커피를 끓이고 발코니에서 담배를 피우다 거대한 도시가 드러나는 실사풍 생성 영상 단편
- **어울리는 경우**: 시네마틱 단편/무드 필름 / 세계관 리빌 티저 / 생성 영상 모델 파이프라인 시연 / SF 캐릭터 일상 시퀀스
- **잘하는 표현**: 클로즈업 위주 일상 루틴 샷 구성(기상, 커피, 담배) / 마지막 와이드 풀백 리빌 컷 / 탈색된 저채도 영화 색보정 / 의수 같은 SF 디테일
- **스타일**: 청회색 위주의 탈채도 실사풍 생성 영상, 얕은 심도와 자연광. 백발 여성, 로봇 손, 거대 고층 구조물이 있는 디스토피아 SF의 차갑고 조용한 분위기.
- **기술**: Uni 1.1, Seedance 2.5, DaVinci Resolve, 외부 생성 모델
- **프롬프트 구조**: 자연어로 쓴 짧은 시퀀스 시놉시스 한 단락(장면 순서 + 마지막 리빌 컷), Opus는 파이프라인 조율 역할
- **태그**: 시네마틱, 실사풍, SF, AI생성영상, Seedance, 리빌샷, 저채도, 단편
- **주의**: 결과 화질은 외부 이미지/영상 생성 모델에 좌우되고 캐릭터 레퍼런스가 필요하다. 코드 렌더 레퍼런스와 성격이 다르다

#### [AI-edited travel vlog](production__ai-edited-travel-vlog__2106091485125091695.md)
`production__ai-edited-travel-vlog__2106091485125091695` · 16:9 · 265s · 조회 22K · 에셋필요 O

- **요약**: 중국 산터우 여행 촬영본을 AI가 주제를 잡아 BGM과 자막을 넣어 편집한 4분 넘는 브이로그
- **어울리는 경우**: 여행/일상 브이로그 자동 편집 / 롱폼 촬영본 → 스토리 편집 사례 / AI 블로거 콘텐츠
- **잘하는 표현**: 대화 내용으로 주제와 흐름을 잡는 스토리 편집 / 중앙 하단 흰 자막(검은 외곽선) 번인 / 설명이 필요한 순간 다크 UI 인포그래픽 카드 삽입
- **스타일**: 액션캠 실사 푸티지(거리, 시장, 식당) 위에 중앙 하단 흰 중국어 자막. 중간중간 휴대폰↔PC 원격 지시 구조를 그린 남색-검정 다이어그램 카드가 들어간다.
- **기술**: Action 카메라 촬영본, 抖音 BGM
- **프롬프트 구조**: 소스 폴더 경로 + 브이로그로 편집, 대화에서 주제 도출, BGM 추가, 나머지 자유라는 4줄 번호 목록형 지시
- **태그**: 브이로그, 자동편집, 여행, 실사, 중국어자막, 인포그래픽카드, vlog, 롱폼
- **주의**: 원본 촬영본이 필수이고 BGM 저작권은 고려하지 않았음. 컷 편집 자동화 사례로는 이 프로젝트와 관련성이 높음

#### [AI-composed Baroque trio sonata](production__ai-composed-baroque-trio-sonata__2103549625076752493.md)
`production__ai-composed-baroque-trio-sonata__2103549625076752493` · 16:9 · 106s · 조회 19K · 에셋필요 X

- **요약**: LilyPond로 작곡·조판한 코렐리풍 F장조 트리오 소나타 라르고 악보를 재생 커서와 함께 보여주는 영상
- **어울리는 경우**: 음악 작곡·악보 시각화 / 클래식 음악 교육 / AI 작곡 결과 시연
- **잘하는 표현**: 재생 위치를 따라가는 파란 커서 바 / 3단 보표 악보 페이지 넘김
- **스타일**: 흰 바탕의 흑백 인쇄 악보에 파란 세로 재생선, 상단에 모델명 라벨과 우측 하단 작가 로고. 장식 없는 2D 악보 화면.
- **기술**: LilyPond
- **프롬프트 구조**: 작곡 형식·양식·조성·편성만 지정한 한 문장 짧은 지시
- **태그**: 악보, LilyPond, 바로크, 작곡, 클래식, 음악, score-video
- **주의**: 영상 자체는 악보 스크롤뿐이라 모션·비주얼 레퍼런스로 가치 낮음. 음악 결과 시연용

### stories (단편/스토리) — 13건 (조회수순)

#### [AI self-introduction song and video](stories__ai-self-introduction-song-and-video__2103698854399099057.md)
`stories__ai-self-introduction-song-and-video__2103698854399099057` · 16:9 · 325s · 조회 762K · 에셋필요 X

- **요약**: Opus 5.5가 스스로를 세상에 소개하는 5분짜리 자기소개 영상으로, 타이핑되는 고백형 문장과 텍스트로 이루어진 이미지가 이어짐
- **어울리는 경우**: AI/브랜드 자기소개 매니페스토 / 시적 내레이션 + 타이포 영상 / 감성 롱폼 아트 필름
- **잘하는 표현**: 모노스페이스 타자기식 자막이 커서와 함께 써지는 연출 / 글자로 그린 ASCII풍 인물과 단어로 이루어진 Lorenz 어트랙터 / 픽셀 그리드, 빛나는 점 하나 같은 미니멀 상징 전환
- **스타일**: 거의 검은 배경에 따뜻한 앰버·베이지 모노스페이스 텍스트만 쓰는 저조도 타이포그래픽 영상. 텍스트로 구성한 형상, 작은 사각 픽셀 그리드, 빈 둥근 사각형 같은 극미니멀 장면이 이어진다.
- **기술**: fal.ai, ElevenLabs, Blender, JavaScript
- **프롬프트 구조**: 사용 가능한 도구와 전권 위임만 주고 '너 자신을 소개하는 영상을, 끝날 때까지 보고하지 말고'라는 완전 자율형 짧은 지시
- **태그**: 자기소개, 타이포그래피, ASCII아트, 모노스페이스, 다크, 시적, manifesto, 롱폼, ElevenLabs
- **주의**: 프롬프트가 거의 백지 위임이라 재현성이 낮음. 컨택트 시트에서는 fal/Blender 생성 이미지보다 코드 타이포 장면이 주로 보임

#### [Battle of Austerlitz procedural film](stories__battle-of-austerlitz-procedural-film__2103116235009347650.md)
`stories__battle-of-austerlitz-procedural-film__2103116235009347650` · 16:9 · 301s · 조회 641K · 에셋필요 O

- **요약**: 아우스터리츠 전투(1805)를 코드로 렌더한 5분 시네마틱 역사 영화: 횃불 행군, 지형 위 부대 이동·화살표 전략도
- **어울리는 경우**: 역사 전투 해설 다큐 / 전략·작전 설명 영상 / 시네마틱 지형 맵 애니메이션
- **잘하는 표현**: 모래색 3D 지형 위 파랑/빨강 부대 블록과 진격 화살표 / 해 뜨는 평원·야간 횃불 등 분위기 조명 / 레터박스 시네마 프레이밍과 하단 날짜 캡션
- **스타일**: 시네마스코프 레터박스, 모래·베이지 단색 지형 렌더 위 파랑·빨강 부대 사각형과 굵은 빨간 곡선 화살표. 역광 일출 평원과 어두운 야간 횃불 행렬 컷. 절제된 3D, 회화보다는 지형 미니어처 느낌.
- **프롬프트 구조**: 자유 위임형 브리프: 길이·주제 + 품질 목표(정확·드라마틱·이해 쉬움) + 첨부 회화를 영감으로만 사용 + '인포그래픽처럼 보이지 말 것'
- **태그**: 역사, 전쟁, 전략맵, 시네마틱, 레터박스, 3D지형, documentary, procedural
- **주의**: 첨부 회화 이미지 참조; 시트상으론 프롬프트가 원한 연기·기병 혼란보다 지형 전략도 비중이 큼

#### [30-second AI-made short drama](stories__30-second-ai-made-short-drama__2103444180861178199.md)
`stories__30-second-ai-made-short-drama__2103444180861178199` · 약 1.42:1 (1022x720) · 107s · 조회 165K · 에셋필요 X

- **요약**: Opus 5.5에 프롬프트를 붙여넣고 생성된 이미지·스크립트를 剪映(CapCut)에 넣어 AI 숏드라마를 만드는 과정을 보여주는 튜토리얼 화면 녹화
- **어울리는 경우**: AI 숏드라마 제작 워크플로 튜토리얼 / '1인 제작' 과정 공개 콘텐츠 / 프롬프트 활용법 안내 영상
- **잘하는 표현**: 화면 녹화+노랑 대형 자막으로 단계 설명 / LLM 채팅 → 편집툴로 넘어가는 제작 흐름 시각화
- **스타일**: LLM 채팅 화면과 剪映 편집 UI 스크린 녹화에 검은 외곽선 노랑 중국어 자막, 마지막은 검은 바탕 흰 안내 텍스트. 연출보다 기록 성격의 다큐형.
- **기술**: 剪映(CapCut), Cursor
- **프롬프트 구조**: 역할 부여 + 제작 제약(인물·장면·컷 수) + 내용·상업성 목표 + 출력 항목 10개 + 비교 선정 기준 + 단계 정지('스토리 선정까지만') 지시의 긴 다단계 기획 프롬프트
- **태그**: 숏드라마, 튜토리얼, 화면녹화, 剪映, CapCut, 워크플로, 중국어, AI영상제작
- **주의**: 프롬프트는 1단계(스토리 후보 선정)만 다루고 영상은 결과물이 아닌 제작 과정 녹화라 비주얼 스타일 레퍼런스로 부적합

#### [Oktoberfest-themed animation](stories__oktoberfest-themed-animation__2102493303388475855.md)
`stories__oktoberfest-themed-animation__2102493303388475855` · 16:9 · 30s · 조회 119K · 에셋필요 O

- **요약**: 주황 블록 캐릭터(Opus 5.5)가 맥주통에서 맥주를 받아 'Happy Oktoberfest!'를 외치는 30초 원샷 2D 애니
- **어울리는 경우**: 시즌 이벤트 축하 SNS 영상 / 브랜드 마스코트 짧은 스토리 / 귀여운 캐릭터 인사 카드
- **잘하는 표현**: 단순 캐릭터의 표정·소품(모자, 프레첼, 수염 거품) 변화 / 원샷 고정 카메라 속 개그 비트 진행 / 마지막 타이틀+사인오프 마무리
- **스타일**: 회백색 배경에 파랑 체크 깃발 가랜드, 연한 선의 텐트·관람차, 주황 사각 몸통 캐릭터와 녹색 티롤 모자. 플랫 2D 카툰, 따뜻하고 귀여운 분위기, 후반 색종이 효과.
- **프롬프트 구조**: 캐릭터 이미지 첨부 + 길이·주제·톤·원샷·게시처·오디오 소스(디스크의 샘플 사용, 합성 금지) 제약을 적은 짧은 브리프
- **태그**: 2D애니, 마스코트, 옥토버페스트, 시즌, 귀여움, 원샷, 카툰, celebration
- **주의**: 캐릭터 이미지와 로컬 오디오 샘플 필요. 구현 기술 미상

#### [Pixar-style imagined cartoon story](stories__pixar-style-imagined-cartoon-story__2102788223835463902.md)
`stories__pixar-style-imagined-cartoon-story__2102788223835463902` · 16:9 · 230s · 조회 102K · 에셋필요 X

- **요약**: 밤의 아이 방에서 빛나는 별 인형과 장난감 로봇이 움직이다 아침 7시에 멈추는 Three.js 3D 단편 애니메이션
- **어울리는 경우**: 어린이용 3D 스토리 애니 / 장난감·캐릭터 단편 / 코드로 만든 3D 애니 데모
- **잘하는 표현**: 로우앵글 장난감 시점 카메라 / 야간 실내 조명과 발광 소품 / 장면별 컷 구성의 스토리텔링
- **스타일**: 남색 벽지와 우주 패턴 이불, 지그재그 러그가 있는 어두운 아이 방, 연두 발광 별·민트 로봇. 블룸이 있는 매끈한 3D 로우폴리 렌더로 90년대 토이스토리 느낌을 노린 아늑한 밤 분위기.
- **기술**: Three.js
- **프롬프트 구조**: '이야기를 상상해 Three.js로 Pixar급 90년대 카툰을 만들라'는 두 문장 원라이너
- **태그**: 3D애니, Three.js, 장난감, 아이방, 야간, 스토리, Pixar풍, cartoon
- **주의**: 'Pixar 수준'과 달리 실제로는 단순한 실시간 렌더 품질

#### [Animated robot story across 12 art styles](stories__animated-robot-story-across-12-art-styles__2103099194693271874.md)
`stories__animated-robot-story-across-12-art-styles__2103099194693271874` · 16:9 · 75s · 조회 72K · 에셋필요 O

- **요약**: 작은 로봇 Pip이 프롬프트로 계속 재생성되는 세계(점토, 장난감 블록, 초현실 등)를 지나 'let me out'을 입력하고, 그 세계가 폰 속 영상이었음이 드러나는 루프형 단편
- **어울리는 경우**: 캐릭터 중심 숏폼 단편/바이럴 영상 / AI 생성 메타 유머 콘텐츠 / 여러 아트 스타일을 오가는 몽타주
- **잘하는 표현**: 스타일이 바뀌어도 실루엣을 유지하는 캐릭터 아이덴티티 락 / 디퓨전 노이즈식 'regeneration' 세계 전환 / 비주얼 스크린 눈과 안테나로 대사 없이 감정 전달 / 폰 속 영상으로 빠지는 리빌 + 무한 루프 구조
- **스타일**: 크림·노랑 박스형 로봇이 따뜻한 골든아워 점토 마을, 원색 장난감 블록 도시, 달리풍 녹는 시계 사막, 핑크 하트 귀여움 버전, 작업대 위 폰 리빌 장면을 오가는 2.5D 일러스트/3D풍 혼합. 민트색 글래스 프롬프트 박스 UI가 등장한다.
- **기술**: Remotion (React + TypeScript), SVG 2D cutout rig, Canvas/WebGL, Python (팔레트 추출, 오디오 합성), ffmpeg
- **프롬프트 구조**: 한 줄 로그라인 + 캐릭터 바이블 + 리그 명세 + 월드별 스타일 + 전환 설계 + 초 단위 비트시트 + 카메라/타이포/사운드 + 마일스톤 게이트와 점수제 셀프 리뷰 루프까지 갖춘 스튜디오급 제작 명세서
- **태그**: 캐릭터애니, 로봇, Remotion, 스타일전환, 루프, 메타유머, 점토, storytelling, 바이럴
- **주의**: 캐릭터 시트 이미지(pip_sheet.png)가 필수. 프롬프트에는 48초라고 되어 있지만 실제 영상은 75초

#### [Arcane-style Blender animation](stories__arcane-style-blender-animation__2105315982525014067.md)
`stories__arcane-style-blender-animation__2105315982525014067` · 16:9 · 15s · 조회 71K · 에셋필요 X

- **요약**: Arcane(Fortiche) 화풍을 노린 15초 Blender 숏: 작업대 위 황동 기계 나방이 깨어나 불꽃 속에 날아오르고 'SPARK' 타이틀로 끝남
- **어울리는 경우**: 시네마틱 단편/티저 오프닝 / 페인터리 3D 스타일 실험 / 타이틀 리빌로 끝나는 짧은 스토리 트레일러
- **잘하는 표현**: 손그림 2D 이펙트(폭발 스타버스트, 스파크)를 3D 위에 합성 / 따뜻한 황동 vs 청록 야경의 색 대비 / 얕은 피사계 심도와 타이틀 카드 마무리
- **스타일**: 어두운 청록 밤 작업실, 빗방울 창과 도시 불빛 보케, 황동·초록 날개의 나방 로봇. 흰·검정 그래픽 스타버스트 컷, 금빛 메탈 'SPARK' 타이틀. 실제 결과는 페인터리 질감보다 부드러운 CG에 가깝고 다소 어두움.
- **기술**: Blender
- **프롬프트 구조**: TITLE/GOAL/SCENE/PROCESS(리서치→스타일 가이드→빌드→리뷰 루프)/STYLE ELEMENTS 체크리스트/SOUND 섹션의 스타일 복제 지시서
- **태그**: Arcane, 페인터리, Blender, 3D, 스팀펑크, 시네마틱, 2D이펙트, title-reveal
- **주의**: 특정 IP 화풍(Arcane) 복제를 목표로 함. 결과물은 붓터치 질감이 약해 목표 대비 재현도가 낮음

#### [Linear algebra fear music video](stories__linear-algebra-fear-music-video__2103697580421181894.md)
`stories__linear-algebra-fear-music-video__2103697580421181894` · 16:9 · 262s · 조회 64K · 에셋필요 O

- **요약**: Suno 곡에 맞춰 AI 안전·선형대수 밈을 가득 넣은 4분 남짓 2D 일러스트 뮤직비디오(캐릭터 Dr. Null)
- **어울리는 경우**: 가사 기반 뮤직비디오 / 니치 커뮤니티 밈/레퍼런스 영상 / 수학·AI 개념 풍자 콘텐츠 / 장편 자막형 애니메이션
- **잘하는 표현**: 가사를 문자 그대로가 아니라 오컬트한 레퍼런스로 시각화(라틴어 수학 원고, 섀넌 실험 패러디, 행렬) / 체커보드 바닥, 극장 무대, CRT 모니터 등 씬마다 바뀌는 무대 / 하단 노란 가사 자막의 노래방식 동기화 / 캐릭터 표정 연출(수정 피드백 반영)
- **스타일**: 종이 질감 위 따뜻한 빈티지 톤의 2D 플랫 일러스트(크림, 남색, 적갈색). 동화책/에듀테인먼트풍 캐릭터와 고문서, 행렬 그리드가 섞인 유머러스한 분위기.
- **기술**: Suno(음악), Claude Code, JavaScript 기반 애니메이션 → 영상 렌더(레퍼런스 repo 방식)
- **프롬프트 구조**: 레퍼런스 GitHub repo + YouTube 곡 링크 제공 후 '같은 스타일로 리메이크' + 크레딧·오디오 컷 지시 + 이후 수정 피드백 2회 이어붙임
- **태그**: 뮤직비디오, 가사자막, 2D일러스트, 빈티지, AI안전, 선형대수, 밈, 캐릭터, Suno
- **주의**: 기존 repo 스타일과 특정 곡에 의존하는 리메이크형이다. 레퍼런스가 매우 니치해 일반 시청자용 참고로는 제한적

#### [Animated episode drawn entirely in code](stories__animated-episode-drawn-entirely-in-code__2102879301876031808.md)
`stories__animated-episode-drawn-entirely-in-code__2102879301876031808` · 16:9 · 120s · 조회 54K · 에셋필요 X

- **요약**: AI 화자가 '나는 인간이 될 수 없지만 곁에 있을 수 있다'고 말하는, 코드로 그린 흑백 실루엣 2분 에피소드
- **어울리는 경우**: 감성 내레이션 단편 애니메이션 / AI 정체성·철학 주제 스토리텔링 / 브랜드 철학/매니페스토 영상 / 자막 기반 시적 영상
- **잘하는 표현**: 흑백 실루엣과 빛 원뿔·창문 프레임을 이용한 상징적 구도 / 반복되는 별/잉크 얼룩 모티프로 화자 표현 / 하단 박스 자막으로 이어지는 시적 서사 / 직접 만든 효과음·사운드트랙
- **스타일**: 검정과 아이보리 2색만 쓴 거친 잉크/스크래치 질감의 2D 일러스트. 비 오는 거리, 도서관, 지평선 일출 같은 실루엣 장면의 쓸쓸하고 고요한 분위기.
- **기술**: 코드 드로잉(구체 스택 미명시), 코드 사운드 생성
- **프롬프트 구조**: 기존 세션 맥락에 이어 쓰는 열린 창작 요청(2분, 감정 표현, 제목 필수 단어 'Be', 'Human'만 제약)
- **태그**: 스토리, 흑백, 실루엣, 잉크질감, 내레이션, 자막, 감성, 2D일러스트, AI정체성
- **주의**: 같은 세션의 이전 작업 맥락에 의존하는 프롬프트라 단독 재현이 어렵다

#### [Alien explores the Library of Babel](stories__alien-explores-the-library-of-babel__2103569043836027339.md)
`stories__alien-explores-the-library-of-babel__2103569043836027339` · 4:3 · 60s · 조회 17K · 에셋필요 O

- **요약**: 외계인이 보르헤스의 바벨의 도서관을 탐사하는 로그를 90년대 영화 GUI풍 와이어프레임·스캔 화면과 합성 음성으로 그린 단편
- **어울리는 경우**: SF·미스터리 내러티브 영상 / 레트로 터미널 UI 연출 / 철학적 개념 해설 단편
- **잘하는 표현**: CRT 녹색 벡터 와이어프레임 복도 / LOG 번호·모드 라벨·파형 HUD / 에칭풍 흑백 이미지와 텍스트 스캔 대비 / 한 글자씩 바뀌는 텍스트 반복 연출
- **스타일**: 검정 배경 위 녹색 형광 벡터 라인과 모노스페이스 HUD, 회색조 피라네시 에칭풍 원형 회랑 이미지, 누런 책 페이지. 임상적이고 으스스한 90년대 레트로 컴퓨터 화면.
- **기술**: Cowork(메타 tools), 합성 음성
- **프롬프트 구조**: 주제·분위기(clinical, spooky)·테마를 한 문단으로 주고 영화 GUI와 피라네시 에칭 이미지를 영감 자료로 첨부
- **태그**: 레트로UI, CRT, 와이어프레임, SF, Borges, 스토리, 녹색모노, HUD
- **주의**: 영화 GUI·에칭 참고 이미지 첨부에 의존

#### [AI capability growth training montage](stories__ai-capability-growth-training-montage__2102788371114246177.md)
`stories__ai-capability-growth-training-montage__2102788371114246177` · 16:9 · 30s · 조회 16K · 에셋필요 X

- **요약**: 쿵푸팬더 수련 시퀀스처럼 Claude 마스코트가 연도별로 능력(검색·코딩·3D 등)을 키워가는 30초 3D 성장 몽타주
- **어울리는 경우**: AI 제품 성장·버전 히스토리 스토리텔링 / 브랜드 마스코트 내러티브 영상 / 연대기형 몽타주
- **잘하는 표현**: 우측 하단 연도 배지(2024→2026)로 진행을 보여주는 타임라인 몽타주 / 패러디된 동양 무협 세계관(패루 문, 대나무 숲, 연등) / 검색창·코드 화면 등 능력을 장면 소품으로 시각화
- **스타일**: 게임 엔진풍 저폴리 3D 동양 무협 세계. 어두운 남색 밤과 안개, 붉은 패루·연등, 대나무 숲, 시안 네온 홀로그램 아이콘, 금빛 석양 아래 석상 정원.
- **기술**: 코드 기반 3D 애니메이션(도구 미상)
- **프롬프트 구조**: 레퍼런스 작품(쿵푸팬더 수련 장면)+주인공+보여줄 능력 목록+음악 감성을 담은 한 문단 원샷
- **태그**: 몽타주, 성장스토리, 무협, 동양풍, 3D, 마스코트, 타임라인, Claude
- **주의**: 프레임 다수가 어둡고 마스코트가 잘 보이지 않음. 렌더 품질은 프로토타입 수준

#### [Cinematic 2D storyboard short film "Rain Station"](stories__cinematic-2d-storyboard-short-film-rain-station__2103757767727255661.md)
`stories__cinematic-2d-storyboard-short-film-rain-station__2103757767727255661` · 16:9 (내부 2.39:1 레터박스) · 30s · 조회 12K · 에셋필요 X

- **요약**: 비 오는 밤 고가 역 플랫폼에서 엇갈리는 두 사람을 그린 30초 애니메풍 2.5D 단편 '雨站 / RAIN STATION'
- **어울리는 경우**: 감성 단편/뮤직비디오 프리비즈 / 애니메풍 시네마틱 숏 / 생성 이미지 기반 2.5D 패럴랙스 영상
- **잘하는 표현**: 보케·포커스 이동·비 내리는 피사계 심도 / Depth Anything 기반 레이어 패럴랙스 카메라 / 샷별 타임코드 분할 연출(과숄더, 열차 통과 등) / 색수차·블룸 등 필름 룩
- **스타일**: 네온 블루·마젠타·앰버 보케가 가득한 비 오는 밤 플랫폼, 투명 우산을 든 베이지 코트 여성과 검은 코트·머플러 남성의 일본 애니메풍 일러스트. 2.39:1 레터박스, 얕은 심도와 젖은 반사광의 시네마틱 2.5D.
- **기술**: GPT Image 2.5, Real-ESRGAN, Depth Anything V2, Python, ffmpeg, Kokoro TTS, Logic/GarageBand, Mixkit SFX
- **프롬프트 구조**: 씬별 타임코드 샷리스트(8샷) + 원화 생성·업스케일·2.5D 합성 파이프라인 지시 + 사운드 설계 + 프리뷰 프레임 자체 검수
- **태그**: 애니메, rain, 보케, 2.5D, parallax, 시네마틱, 레터박스, 단편
- **주의**: 외부 이미지 생성(GPT Image)과 로컬 ML 모델 의존; 그린스크린 키잉 등 파이프라인 구축 부담 큼

#### [One-shot music video from song and lyrics](stories__one-shot-music-video-from-song-and-lyrics__2103570879619686717.md)
`stories__one-shot-music-video-from-song-and-lyrics__2103570879619686717` · 16:9 · 141s · 조회 8K · 에셋필요 O

- **요약**: 가사에 맞춰 사악한 피자 가게 외부→내부→비밀 책장 문→지하로 들어가는 콜라주·볼펜 스케치 스타일 뮤직비디오
- **어울리는 경우**: 뮤직비디오·가사 싱크 영상 / Vox식 콜라주 설명 영상 / 호러·미스터리 내러티브 숏
- **잘하는 표현**: 우주 배경 위 엽서·사진 컷아웃을 떠다니게 하는 Monty Python/Vox 콜라주 연출 / 협박장식 잘라 붙인 글자('CHAINLOCKED') 타이포 / CCTV 화면 HUD 등 장면별 장치 / SDXL 생성 에셋을 합성·애니메이션해 대량 장면 구성
- **스타일**: 별이 뿌려진 검은 우주 배경에 파란 볼펜 해칭 스케치(가게 내부, 책장, 자동차)와 실사 피자·서류·종이가방 컷아웃이 콜라주된 2D. 녹색 야간 CCTV 프레임과 랜섬노트 글자, 손글씨 라벨 태그.
- **기술**: ComfyUI, SDXL(이미지 에셋 생성), 코드 기반 합성·애니메이션
- **프롬프트 구조**: 곡+lyrics.txt 첨부, 스타일 혼합(Vox 엽서 콜라주+볼펜 스케치)·테마·카메라 동선만 지시하는 문단형 브리프
- **태그**: 뮤직비디오, 콜라주, 볼펜스케치, Vox스타일, 호러, SDXL, 가사싱크, 2D
- **주의**: 곡·가사 파일과 로컬 ComfyUI 환경이 필요. 메타의 After Effects는 사용하지 않았다는 맥락

### art3d (3D/아트) — 19건 (조회수순)

#### [Jelly watermelon slicing simulation](art3d__jelly-watermelon-slicing-simulation__2104285370951012504.md)
`art3d__jelly-watermelon-slicing-simulation__2104285370951012504` · 16:9 · 18s · 조회 627K · 에셋필요 X

- **요약**: WebGPU로 만든 젤리 수박 조각을 칼로 잘라 여러 조각으로 나누는 소프트바디 물리 시뮬레이션 데모
- **어울리는 경우**: 물리/재질 시뮬레이션 기술 쇼케이스 / 인터랙티브 웹 데모 홍보 클립 / ASMR풍 '자르기' 숏폼
- **잘하는 표현**: XPBD 소프트바디의 출렁임·눌림 후 절단 / 반투명 젤리 굴절·흡수 재질 렌더 / 칼 동작 코레오그래피(정렬→눌림→관통→들어올림) / 품종 스와치로 색 변경(빨강→노랑/주황)
- **스타일**: 따뜻한 회백색 스튜디오 배경 위 반투명 빨강 젤리 수박과 나키리 칼의 3D 제품샷 느낌, 좌상단 이탤릭 세리프 'Melon Jelly.' 에디토리얼 UI. 상단에 'Claude Opus 5.5' 비용 라벨이 덧씌워져 있음.
- **기술**: WebGPU, WGSL, 단일 HTML/JS(외부 라이브러리 없음)
- **프롬프트 구조**: 섹션별(플랫폼/페이지 디자인/형태/물리/절단/칼/품질 기준) 초상세 기술 스펙 + 수치 파라미터 + 테스트 훅 요구
- **태그**: 물리시뮬, soft-body, WebGPU, 젤리, 인터랙티브, 에디토리얼UI, 3D, material-study
- **주의**: 영상은 웹앱 화면 녹화이고 모델명·비용 오버레이가 박혀 있음. 영상 제작용이라기보다 실시간 인터랙티브 데모 레퍼런스

#### [Playable boat scene through Japanese landscapes](art3d__playable-boat-scene-through-japanese-landscapes__2102760783344189761.md)
`art3d__playable-boat-scene-through-japanese-landscapes__2102760783344189761` · 4:3 · 60s · 조회 479K · 에셋필요 X

- **요약**: 벚꽃철 일본 계곡을 거슬러 오르는 나룻배를 Three.js 실시간 3D로 만든 인터랙티브 씬(낮-폭풍-황혼-밤 사이클) 화면 녹화
- **어울리는 경우**: 시간 흐름·분위기 변화를 보여주는 감성 배경 영상 / 일본풍·동양 풍경 B-roll / 웹 3D 실시간 렌더 역량 시연 / 명상·로파이 루프 배경
- **잘하는 표현**: 낮/폭풍/골든아워/밤 조명·컬러그레이드 전환 / 물 반사·항적·비·안개 등 환경 효과 / 3인칭 추적 카메라의 시네마틱 드리프트 / 등불·도깨비불 같은 야간 발광 연출
- **스타일**: 회화적 3D 실사풍. 안개 낀 청회색 강·벚꽃 핑크·주홍 다리, 황혼엔 따뜻한 역광 헤이즈, 밤엔 남색 수면에 주황·흰 불빛이 점점이 반사되는 고요하고 시네마틱한 분위기.
- **기술**: Three.js, WebAudio 합성 사운드(프롬프트 명시), 단일 HTML 파일
- **프롬프트 구조**: 장면 구성요소(지형·랜드마크·식생·배·인물·물·파티클·낮밤 사이클·카메라·조작)를 항목별로 매우 상세히 나열 + 금지사항(텍스트 금지, 관통 금지) + 브라우저 스크린샷 검수 지시
- **태그**: 3D, Three.js, 일본풍경, 벚꽃, 낮밤사이클, 시네마틱, 인터랙티브, 환경연출, ambient
- **주의**: 브라우저 화면 녹화라 일부 프레임에 에디터 UI·마우스 커서가 보임. 결과물은 인터랙티브 씬이지 편집된 영상이 아님

#### [Pelican riding a bike in Three.js](art3d__pelican-riding-a-bike-in-three-js__2102436416437580159.md)
`art3d__pelican-riding-a-bike-in-three-js__2102436416437580159` · 16:9 · 91s · 조회 417K · 에셋필요 X

- **요약**: 펠리컨이 자전거를 타고 도시와 해변 산책로를 달리는 Three.js 3D 게임 플레이 녹화
- **어울리는 경우**: 캐릭터 중심 3D 웹 데모 쇼케이스 / 원라이너 프롬프트로 만든 결과물 시연 / 로우폴리~세미리얼 도시 배경 B-roll / 게임형 인터랙티브 체험 소개
- **잘하는 표현**: 역광 노을 라이팅과 따뜻한 색보정 / 자전거 체인·기어 클로즈업 등 다양한 카메라 앵글(3인칭/근접/슬로모션) / 도시 블록·차량·가로수가 채워진 환경 밀도 / HUD(수집 카운터, 속도계)를 얹은 게임 연출
- **스타일**: 골든아워 역광의 따뜻한 오렌지-블루 색감, 3D 실시간 렌더. 벽돌 건물과 보도 타일은 단순화된 텍스처라 하이퍼리얼보다는 깔끔한 세미리얼/스타일라이즈드 톤이다.
- **기술**: Three.js, 브라우저 실시간 렌더(self-contained HTML)
- **프롬프트 구조**: 한 문장 원라이너(하이퍼리얼, self-contained, 음악·효과음 포함만 요구)
- **태그**: 3D, Three.js, 펠리컨, 게임플레이, 골든아워, 도시, 원라이너, 캐릭터
- **주의**: 게임 플레이 화면 녹화라 편집된 영상 연출 레퍼런스로는 약하고, 프롬프트가 짧아 재현성이 낮다

#### [Floor plan to 3D interior design tool](art3d__floor-plan-to-3d-interior-design-tool__2104520072014508316.md)
`art3d__floor-plan-to-3d-interior-design-tool__2104520072014508316` · 16:10 (1196x720, 약 5:3) · 33s · 조회 339K · 에셋필요 O

- **요약**: 평면도 이미지를 바탕으로 2D 도면 편집과 Three.js 3D 조감·1인칭 워크스루를 오가는 단일 HTML 인테리어 설계 툴 시연
- **어울리는 경우**: 부동산·인테리어 SaaS 데모 / 2D→3D 전환 기능 소개 / 툴/앱 기능 워크스루 영상
- **잘하는 표현**: 2D 평면도에서 3D 컷어웨이로의 전환 / 조감→1인칭 실내 이동 카메라 / 실측 기반 가구 배치와 사이드 패널 데이터 동기화
- **스타일**: 밝은 오프화이트 UI에 베이지·우드톤 가구 평면도, 3D는 검은 벽 상단 단면을 가진 무광 화이트 미니멀 렌더. 실사보다는 깔끔한 건축 모형 느낌.
- **기술**: Three.js, 단일 HTML 파일
- **프롬프트 구조**: 중국어로 기능 요구사항(2D 도면·가구·인터랙션·3D·전환)을 번호 목록 5개로 짧게 지시 + 평면도 이미지 첨부
- **태그**: 인테리어, floor-plan, 2D-to-3D, Three.js, 앱데모, 건축, 워크스루, UI
- **주의**: 영상이 아닌 툴 화면 녹화이며 실제 평면도 이미지 입력이 필요. 화면 대부분이 작은 UI 패널이라 모션 스타일 참고엔 약함

#### [Historic 1906 San Francisco street in 3D](art3d__historic-1906-san-francisco-street-in-3d__2102466523164274839.md)
`art3d__historic-1906-san-francisco-street-in-3d__2102466523164274839` · 약 1.41:1 (960x680) · 8s · 조회 156K · 에셋필요 X

- **요약**: 1906년 지진 전날의 샌프란시스코 Market Street를 Blender Python으로 사료 기반 재구성하고, 케이블카 시점으로 거리를 따라 올라가는 흑백 영상
- **어울리는 경우**: 역사 다큐의 시대 재현 컷 / 사료/데이터 기반 3D 복원 시연 / 아카이브 필름 오마주 오프닝
- **잘하는 표현**: 실제 1906년 필름(A Trip Down Market Street)과 같은 1점 투시 전진 구도 / 흑백 저채도 질감으로 아카이브 필름 흉내 / 마차·전차선·차양·간판까지 절차적 생성기로 채운 밀도
- **스타일**: 흑백 실사풍 3D 렌더. 정중앙 소실점에 Ferry Building 시계탑, 양옆 빅토리아풍 건물과 전차 레일이 반복되는 고정 전진 구도로 옛 필름처럼 보인다.
- **기술**: Blender, Blender Python (절차적 모델 생성기)
- **프롬프트 구조**: 범위·사료 목록·데이터 출처 기록 규칙(신뢰도 포함)·다운로드 에셋 금지·재사용 생성기 목록을 정한 뒤 10초 영상 하나를 요구하는 리서치 우선형 프롬프트
- **태그**: 역사재현, Blender, 흑백, 아카이브필름, procedural, 3D, 1906, 도시
- **주의**: 8초짜리 단일 전진 샷이라 편집 리듬이나 전환 참고용으로는 부족하고, 해상도도 비표준(960x680)

#### [Interactive 3D dystopian city diorama](art3d__interactive-3d-dystopian-city-diorama__2103820733159981151.md)
`art3d__interactive-3d-dystopian-city-diorama__2103820733159981151` · 16:9 · 52s · 조회 144K · 에셋필요 X

- **요약**: Three.js로 코드만 써서 만든, 비 오는 밤 수몰된 사이버펑크 하층가 디오라마를 여러 카메라 시점으로 순회하는 영상
- **어울리는 경우**: SF/사이버펑크 세계관 인트로 / 인터랙티브 웹 3D 쇼케이스 / 챕터 전환용 분위기 컷
- **잘하는 표현**: 네온 간판·창문·실외기로 빈 면 없이 채운 고밀도 도시 / 안개 속 빛 번짐과 보케, 비 파티클 / LIVE CAM 라벨과 한자 장소명 HUD를 붙인 시점 전환 / 하늘을 나는 네온 고래 같은 상징 오브젝트
- **스타일**: 보라·마젠타·청록 네온이 비 내리는 짙은 남색 밤에 번지는 3D 사이버펑크. 감시 카메라풍 HUD(LIVE CAM, 타임스탬프)와 '第七区 下層', '酸性雨' 같은 큰 한자 자막이 깔린다.
- **기술**: Three.js, HTML (브라우저 단일 페이지)
- **프롬프트 구조**: 주제 한 줄 + '에셋 없이 전부 코드로', '빈 면 금지', '항상 무언가 움직일 것' 같은 불릿 제약 + 5~7개 시점 버튼 + 스크린샷 자가검수 요구
- **태그**: 사이버펑크, Three.js, 네온, 디오라마, rain, HUD, 일본어자막, 3D, 다크
- **주의**: 인터랙티브 페이지를 녹화한 것이라 일부 프레임은 노이즈/블러로 흐릿함. 영상용으로 쓰려면 시점 전환 타이밍을 따로 설계해야 함

#### [280 KB single-file HTML demoscene intro](art3d__280-kb-single-file-html-demoscene-intro__2102893186330841502.md)
`art3d__280-kb-single-file-html-demoscene-intro__2102893186330841502` · 16:9 · 43s · 조회 129K · 에셋필요 X

- **요약**: 에셋 없이 HTML 파일 하나(약 280KB)로 빅뱅·프랙탈 큐브·설산·사이버 도시·블랙홀을 이어 붙인 데모신 스타일 인트로
- **어울리는 경우**: AI/코드 생성 능력 과시용 SNS 데모 / 기술 브랜드 오프닝·인트로 시퀀스 / 우주·SF 테마 시네마틱 타이틀 / 절차적 생성 그래픽 쇼케이스
- **잘하는 표현**: 절차적 3D 장면(설산 지형, 도시, 블랙홀 강착원반)을 코드만으로 연속 구성 / 씬마다 완전히 다른 세계로 넘어가는 대비 강한 장면 전환 / 마지막 'EX NIHILO' 메타 타이틀로 제작 방식 자체를 메시지화 / 볼류메트릭 빛·글로우 표현
- **스타일**: 검은 배경 위 강한 발광 위주의 시네마틱 3D. 흰 섬광의 빅뱅, 무지개빛 와이어 프랙탈 큐브, 석양 설산 실사풍 렌더, 붉은 서치라이트의 사이버펑크 도시, 주황 블랙홀이 이어지고 모노스페이스 소문자 캡션으로 마감.
- **기술**: HTML/JS 단일 파일(외부 에셋·라이브러리 0개, 화면 텍스트 근거), 절차적 셰이더/Canvas 렌더 추정
- **프롬프트 구조**: '/goal 가장 인상적인 데모를 직접 골라 만들고 영상으로 녹화하라'는 자율 위임형 원라이너
- **태그**: 데모신, demoscene, 절차적생성, 블랙홀, 사이버펑크, 3D, 시네마틱, single-file-html, 다크
- **주의**: 프롬프트에 구체 지시가 없어 결과 재현성이 낮음. 스타일 참고는 영상 자체 기준으로 해야 함

#### [Itsukushima Shrine 3D scene](art3d__itsukushima-shrine-3d-scene__2103737014508216515.md)
`art3d__itsukushima-shrine-3d-scene__2103737014508216515` · 16:9 · 24s · 조회 123K · 에셋필요 X

- **요약**: 이쓰쿠시마 신사의 도면이 두루마리에서 입체로 세워지고 석양 바다 위 완성 풍경과 세로 타이틀로 끝나는 Blender 영상
- **어울리는 경우**: 건축/문화재 소개 영상 / 도면에서 3D로 빌드업하는 과정 설명 / 일본풍 시네마틱 타이틀 / 관광·지역 홍보 티저
- **잘하는 표현**: 2D 도면 → 와이어프레임 → 실체 순서의 단계적 빌드업 / 물에 비친 반영과 안개 낀 산의 대기감 / 세로쓰기 타이틀 + 낙관 같은 전통 타이포 레이아웃 / 엔드카드까지 포함한 구성
- **스타일**: 한지 질감 도면, 주홍 기둥과 갈색 지붕의 3D 건축, 후반은 안개 낀 산과 잔잔한 수면의 차분한 저채도 석양 톤. 실사풍 3D에 동양 전통 그래픽(세로 서체, 인장)을 겹친 정적이고 고요한 분위기.
- **기술**: Blender 4.2, Python(사운드 합성, 스크립트), DXF CAD 도면, 프로시저럴 텍스처
- **프롬프트 구조**: 섹션별 상세 사양서(CAD 산출물 / 씬 순서 6단계 / 카메라 / 묘사 / 사운드 / PC 부하 / 진행 방식) + 테스트 스틸 확인 후 본 렌더 체크포인트
- **태그**: Blender, 건축, 일본, 신사, 도면, 빌드업, 석양, 세로타이틀, 3D, 시네마틱
- **주의**: 프롬프트가 일본어이고 엔드카드용 로고 첨부가 언급된다(메타는 에셋 불필요로 표기). 결과물 수목·지형은 프롬프트 요구만큼 디테일하진 않다

#### [Live generative code art from a typed word](art3d__live-generative-code-art-from-a-typed-word__2103837519615774895.md)
`art3d__live-generative-code-art-from-a-typed-word__2103837519615774895` · 9:16 · 97s · 조회 84K · 에셋필요 X

- **요약**: 블랙홀·성운·은하·지구 일출을 거쳐 'and there was LIGHT' 타이포로 끝나는 세로형 우주 창세 제너러티브 아트
- **어울리는 경우**: 감성 오프닝/숏폼 훅 / 과학·우주 테마 인트로 / 브랜드 매니페스토 영상
- **잘하는 표현**: 블랙홀 강착원반·성운 등 셰이더형 우주 표현 / 미시→거시 스케일 서사 전개 / 별빛 텍스처가 채워진 마무리 타이포
- **스타일**: 검은 배경 위 주황 블랙홀, 보라·청록 성운, 나선 은하, 지구 대기권 일출 등 실사풍 우주 비주얼. 마지막은 이탤릭 세리프 'and there was' + 별무늬로 채운 굵은 'LIGHT' 레터링.
- **프롬프트 구조**: 'Wow하게, AI slop 금지, 마음대로' 식의 추상적 자유 위임 프롬프트
- **태그**: 우주, cosmic, generative-art, 블랙홀, 성운, 세로영상, 타이포, 다크
- **주의**: 프롬프트에 기술·장면 지정이 없어 재현성 낮음; 'typed word' 인터랙션은 시트에서 확인 안 됨

#### [Sand painting animation with narrated soundtrack](art3d__sand-painting-animation-with-narrated-soundtrack__2102592355165782312.md)
`art3d__sand-painting-animation-with-narrated-soundtrack__2102592355165782312` · 16:9 · 120s · 조회 75K · 에셋필요 X

- **요약**: 미국 250년 역사를 2분짜리 모래 그림(샌드 아트) 애니메이션으로 풀어낸 영상 (BGM·사운드 디자인 포함)
- **어울리는 경우**: 역사·연대기 스토리텔링 / 아날로그 질감의 내레이션 영상 / 기념일·주년 콘텐츠
- **잘하는 표현**: 모래 입자가 흩뿌려지고 쓸려 나가는 파티클 전환 / 양피지 배경 위 단색 실루엣 연출 / 음악·효과음 동반
- **스타일**: 베이지/양피지색 종이 질감 배경 위에 짙은 갈색 모래 입자가 흩어지는 2D 미니멀 화면. contact sheet 6프레임은 대부분 빈 배경과 가장자리 모래 띠만 보여 구체적 그림은 거의 드러나지 않음.
- **프롬프트 구조**: 목표·길이·톤만 지정한 짧은 원라이너 (구조·기술 지정 없음)
- **태그**: 샌드아트, sand-animation, 역사, history, 파티클, 양피지, 원라이너, 2D
- **주의**: 샘플 프레임이 대부분 전환 중 빈 화면이라 실제 그림 퀄리티 확인 불가; 도구 미기재

#### [Zoom from room to quarks 3D scene](art3d__zoom-from-room-to-quarks-3d-scene__2103299766473875778.md)
`art3d__zoom-from-room-to-quarks-3d-scene__2103299766473875778` · 16:10 · 210s · 조회 72K · 에셋필요 O

- **요약**: 방→MacBook→M4 칩→트랜지스터→실리콘 격자→원자→쿼크(또는 화면→픽셀→서브픽셀 LED)로 끝없이 줌인하는 Three.js 프로시저럴 3D 월드
- **어울리는 경우**: 스케일·계층 구조 설명(파워스오브텐식 줌) / 반도체·하드웨어 교육 콘텐츠 / 과학 다큐 인트로 / 기술 개념의 '안으로 들어가기' 시각화
- **잘하는 표현**: 17자릿수 스케일을 끊김 없이 잇는 연속 줌 카메라 / 단계별 위치·스케일 라벨 HUD / 디스플레이 서브픽셀·결정격자 등 미시구조 디테일 / 레벨 전환 시 외피 페이드로 팝 없는 진입
- **스타일**: 어두운 배경의 3D 기술 시각화. 회색 기판 위 형광 블록 다이, 흑색 우주 같은 원자 공간에 푸른 전자 점, 회색 볼앤스틱 격자, 빨강·초록·파랑 서브픽셀 줄무늬가 원근으로 펼쳐짐. 신스웨이브 배경화면이 뜬 OS 화면도 등장.
- **기술**: Three.js, TypeScript, BunJS, 로컬 이미지 에셋(MacBook 내부 사진, M4 다이 도면, 배경화면)
- **프롬프트 구조**: 아키텍처 하드 제약(상태=t+분기 비트열, 순수 렌더 함수 재귀, 스케일 로컬 프레임) + 레벨 경로 명세 + 카메라/HUD 규칙 + 콘텐츠 밀도·시각 품질 법칙 + 코드 스타일 요구를 길게 나열한 엔지니어링 스펙형
- **태그**: infinite-zoom, 스케일줌, Three.js, 반도체, 원자, 교육, 3D, procedural, HUD
- **주의**: MacBook 내부 사진·M4 다이 도면 등 로컬 에셋 의존. 브라우저 탭 UI가 녹화에 그대로 보임

#### [Pixel art scene generation](art3d__pixel-art-scene-generation__2102746041250705890.md)
`art3d__pixel-art-scene-generation__2102746041250705890` · 16:9 · 13s · 조회 61K · 에셋필요 X

- **요약**: 비 내리는 할로윈 밤, 떠 있는 섬 위 오두막을 그린 루프형 픽셀아트 디오라마(로파이 음악 커버용)
- **어울리는 경우**: 로파이/작업용 음악 롱폼 영상의 루프 배경 / 유튜브 라이브·대기 화면 앰비언트 배경 / 시즌(할로윈) 분위기 채널 아트
- **잘하는 표현**: 따뜻한 불빛 vs 차가운 밤의 색 대비 / 비·불꽃·연기·깜빡이는 빛 등 반복 파티클 효과 / 카메라 고정 상태에서 끊김 없는 루프
- **스타일**: 짙은 남보라 밤하늘에 보름달·구름, 공중에 뜬 흙섬 위 목조 오두막과 주황 창문·모닥불·우산, 청록 발광 수정이 박힌 2D 픽셀아트. 6프레임 내내 구도가 고정되고 빗줄기와 불빛만 미세하게 바뀌는 차분한 앰비언트 분위기.
- **프롬프트 구조**: 용도(10시간 로파이 루프 커버)·팔레트 원칙(웜/쿨 대비)·효과 목록만 적은 3문장 짧은 브리프
- **태그**: 픽셀아트, pixel-art, 루프, lofi, 할로윈, 앰비언트, 야경, 파티클, diorama
- **주의**: 구현 기술이 프롬프트에 없음(출처 블로그는 Sprite Fusion). 움직임이 거의 없어 모션 레퍼런스로는 약함

#### [3D character rig generated from a PSD file](art3d__3d-character-rig-generated-from-a-psd-file__2102965242439590112.md)
`art3d__3d-character-rig-generated-from-a-psd-file__2102965242439590112` · 16:9 · 17s · 조회 53K · 에셋필요 O

- **요약**: 파츠 분리된 PSD를 StandRig 저장소로 2D 리깅해 애니 캐릭터의 파라미터 조작 화면을 보여주는 툴 시연 녹화
- **어울리는 경우**: VTuber/Live2D식 캐릭터 리깅 데모 / 툴 워크플로 소개 영상 / AI 에이전트 작업 결과 쇼케이스
- **잘하는 표현**: PSD 레이어 기반 2D 리그의 미세한 움직임 / 슬라이더 파라미터와 캐릭터 반응을 한 화면에 보여줌
- **스타일**: 어두운 차콜 툴 UI 안에 파란 머리 애니 스타일 여자 캐릭터 전신이 중앙에 서 있고 오른쪽에 파라미터 슬라이더 패널이 있다. 일러스트 2D이고, 제목과 달리 3D가 아니다.
- **기술**: StandRig, PSD 파츠 분리 입력
- **프롬프트 구조**: 로컬 PSD와 GitHub 저장소를 주고 클론 후 고품질 리깅을 하라는 3줄짜리 짧은 일본어 지시
- **태그**: 2D리깅, Live2D풍, 애니캐릭터, VTuber, StandRig, PSD, 툴시연, screen-recording
- **주의**: 제목은 3D지만 실제로는 2D 리그이고, 화면 대부분이 정지된 툴 UI라 영상 연출 레퍼런스로서의 가치는 낮음

#### [Music-driven Blender visual scene](art3d__music-driven-blender-visual-scene__2107696042053431360.md)
`art3d__music-driven-blender-visual-scene__2107696042053431360` · 16:9 · 21s · 조회 47K · 에셋필요 O

- **요약**: Suno로 만든 글리치 베이스 트랙을 분석해 페로플루이드 구체와 눈을 Blender로 구동한 사이키델릭 루프 쇼트
- **어울리는 경우**: 음악 비주얼라이저/뮤직비디오 / 오디오 리액티브 루프 콘텐츠 / SNS 스크롤 멈춤용 훅 영상 / 글리치·사이키델릭 아트 필름
- **잘하는 표현**: 오디오 분석(템포, 온셋, 테이프스톱)을 프레임 채널로 매핑한 정밀 싱크 / 페로플루이드 스파이크·홍채 등 하이퍼리얼 매크로 오브젝트 / 데이터모시·크로마 스플릿·VHS 노이즈 등 분석 연동 글리치 포스트 / 만화경 대칭 등 섹션별 시각 변주와 심리스 루프
- **스타일**: 검정 배경에 마그마 팔레트(보라, 마젠타, 코랄, 오렌지)만 쓴 어둡고 몽환적인 3D 실사풍. 검은 금속 스파이크 구체, 빛 궤적, 크로마 번짐 글리치, 녹색 톤 만화경이 보이며 하단에 PLAY/STOP 테이프 속도 HUD가 있다.
- **기술**: Blender 4.2 + BlenderMCP, Cycles, Suno(컴퓨터 사용), Python 오디오 분석, ffmpeg
- **프롬프트 구조**: 9단계 파이프라인 디렉션(사운드 생성 → 수학적 청취 → 안무 채널 → 월드 빌드 → 구조 매핑 → 훅/루프 → 렌더 → 글리치 포스트 → 납품) + 구체적 수치 사양
- **태그**: Blender, 오디오리액티브, 사이키델릭, 글리치, ferrofluid, 루프, 다크, 마그마팔레트, 뮤직비디오
- **주의**: Suno 로그인·BlenderMCP·Cycles 렌더가 필요한 무거운 파이프라인. 화면이 매우 어둡고 추상적이라 정보 전달형 영상에는 맞지 않는다

#### [90s-style demoscene demo in C/OpenGL](art3d__90s-style-demoscene-demo-in-c-opengl__2102919394775220530.md)
`art3d__90s-style-demoscene-demo-in-c-opengl__2102919394775220530` · 16:9 · 383s · 조회 38K · 에셋필요 O

- **요약**: S3M 트래커 음악에 맞춰 C/OpenGL로 만든 90년대 데모신 스타일 실시간 데모
- **어울리는 경우**: 레트로/데모신 감성 뮤직비디오 / 음악 싱크 비주얼라이저 / 기술력 과시용 쇼오프 영상 / 그래픽 이펙트 모음 쇼릴
- **잘하는 표현**: 플라즈마·메타볼·터널·와이어프레임 큐브 등 고전 데모 이펙트 다양성 / 음악 섹션별 분위기 전환과 싱크 / 크롬 그라데이션 스크롤 텍스트 같은 시대 고증 / 마지막 이펙트 썸네일 그리드로 회고하는 엔딩
- **스타일**: CRT 느낌의 비네팅 프레임 안에 고채도 네온(보라, 시안, 마젠타, 오렌지)이 검은 배경 위에 뜨는 맥시멀 레트로 3D/2D 혼합. 크롬 질감 블롭과 픽셀 텍스트가 섞인 90년대 PC 데모 미학.
- **기술**: C/C++, OpenGL, 셰이더, S3M 트래커 음악 재생/분석
- **프롬프트 구조**: 목표·분위기 서술형 단락 + 사전 조사(음악 분석, 이펙트 리서치) 지시, 구체 샷리스트 없음
- **태그**: 데모신, demoscene, 레트로, 90s, OpenGL, 네온, 음악싱크, 터널, 플라즈마
- **주의**: 6분이 넘는 긴 실시간 데모이고 사용자가 제공한 S3M 음원에 의존한다. 웹/영상 파이프라인과 기술 스택(C/OpenGL)이 다르다

#### [Underwater palace built in Blender](art3d__underwater-palace-built-in-blender__2103669801554264378.md)
`art3d__underwater-palace-built-in-blender__2103669801554264378` · 16:9 · 24s · 조회 31K · 에셋필요 O

- **요약**: 와지 두루마리 위 배치도가 와이어프레임→건물로 쌓아 올라가 해저의 용궁성(竜宮城)으로 완성되는 Blender 건축 연출 영상
- **어울리는 경우**: 건축·공간 설계 과정 시각화 / 도면에서 완성까지의 빌드업 타임랩스형 연출 / 동양풍 판타지 세계관 오프닝 / 로고 엔드카드가 붙는 짧은 브랜드 쇼릴
- **잘하는 표현**: 2D 도면→와이어프레임→재질 입힌 3D로 이어지는 단계적 빌드업 / 마지막에 환경(해저)을 드러내는 반전 연출과 와이드샷 전환 / 주전 주위를 도는 카메라 오빗 / Python으로 합성한 BGM·효과음까지 포함한 일괄 제작
- **스타일**: 회백색 도면 → 흑백 기와 구조 렌더 → 청록 기와·붉은 기둥의 동양 궁궐로 진행. 마지막엔 푸른 해저 조명, 빛줄기, 산호·해초가 있는 반실사 3D이며 '竜宮城' 서예풍 타이틀과 검은 바탕 'Create by Ayuneo' 엔드카드로 끝남.
- **기술**: Blender 4.2, Python(Blender 스크립팅, 사운드 합성), DXF CAD 도면 생성, 프로시저럴 텍스처
- **프롬프트 구조**: 【제재】【환경】 슬롯을 둔 재사용 템플릿. CAD·영상 씬 순서·카메라·묘사·사운드·PC 부하·진행 방식을 섹션별 불릿으로 지정하고 테스트 스틸 확인 후 본 렌더
- **태그**: Blender, 건축시각화, 와이어프레임, 빌드업, 동양풍, 해저, 3D, 용궁, 엔드카드
- **주의**: 로고·외관 참고 이미지 첨부가 전제. 결과물 수목·디테일은 프롬프트 요구(잎 한 장 단위)보다 단순함

#### [Cinematic 3D world with a free camera](art3d__cinematic-3d-world-with-a-free-camera__2103194052850241739.md)
`art3d__cinematic-3d-world-with-a-free-camera__2103194052850241739` · 16:9 · 84s · 조회 29K · 에셋필요 X

- **요약**: 자유 카메라로 탐험하는 브라우저 3D 세계 'MONOLITH WILDS': 거대한 기괴 건축물과 절벽·폭포 풍경 플라이스루
- **어울리는 경우**: 게임/월드 트레일러 / 판타지 풍경 배경 영상 / 시네마틱 오프닝 타이틀
- **잘하는 표현**: 대기원근·볼류메트릭 라이트가 있는 대규모 풍경 / 거대 링·탑·아치 등 초현실 구조물 디자인 / 드론형 카메라 플라이스루 / 타이틀 오버레이
- **스타일**: 따뜻한 역광과 푸른 하늘, 붉은 암석 산맥, 폭포·숲이 있는 실사풍 3D 랜드스케이프. 거대한 원형 링 구조물과 어두운 우주 공간 같은 오브 내부 씬도 등장하며 'MONOLITH WILDS' 얇은 세리프 타이틀이 얹힘.
- **기술**: 브라우저 3D (WebGL 추정, 프롬프트에 'browser-based 3D')
- **프롬프트 구조**: 분위기·지향점만 서술한 한 단락 자유형 프롬프트 (게임 아님, 탐험·구도 중심 명시)
- **태그**: 3D, landscape, 플라이스루, 판타지건축, 시네마틱, browser-3D, 대기원근, 월드빌딩
- **주의**: 인터랙티브 월드의 화면 녹화라 컷 구성·편집은 사용자가 한 것; 구체 기술 스택 미기재

#### [Golden Pavilion CAD-to-3D animation](art3d__golden-pavilion-cad-to-3d-animation__2103243328041132100.md)
`art3d__golden-pavilion-cad-to-3d-animation__2103243328041132100` · 16:9 · 24s · 조회 17K · 에셋필요 O

- **요약**: 와지(和紙) 두루마리 위 금각사 배치도가 와이어프레임→실체 건물로 솟아오르고 단풍 연못 풍경으로 전환되는 Blender 건축 애니메이션
- **어울리는 경우**: 건축·문화재 소개 영상 오프닝 / 도면→완성물로 이어지는 제작 과정 시각화 / 관광/지역 홍보 타이틀 시퀀스
- **잘하는 표현**: 2D 도면이 3D로 '세워지는' 빌드업 연출(기단→기둥→벽→지붕 순) / 두루마리 소품에서 실경으로 넘어가는 스케일 전환 / 리얼 계열 환경(단풍 숲, 수면 반사, 공기 원근) / 세로쓰기 한자 타이틀 마무리
- **스타일**: 도입부는 크림색 종이 두루마리에 먹선 도면, 후반은 저녁빛 아래 붉은 단풍 산과 연못에 비친 금빛 누각의 3D 반실사. 마지막에 큰 '金閣' 세로 타이틀과 검은 화면 크레딧.
- **기술**: Blender 4.2, DXF(CAD 도면), Python 합성 사운드
- **프롬프트 구조**: 【題材】【環境】 치환 슬롯이 있는 템플릿형: 산출물(CAD/영상) 사양 + 5단계 씬 순서 + 묘사 디테일 규칙 + 음향 + 테스트 스틸 확인 후 렌더라는 진행 절차
- **태그**: 건축, 3D, Blender, 와이어프레임, 빌드업, 일본풍, 단풍, title-sequence, CAD
- **주의**: 외관 참고 이미지 첨부 전제. 영상 끝에 제작자 크레딧 카드 포함. 수목·물 표현은 근경에서 다소 거침

#### [Interactive jelly press toy](art3d__interactive-jelly-press-toy__2105285992865272110.md)
`art3d__interactive-jelly-press-toy__2105285992865272110` · 16:9 · 18s · 조회 11K · 에셋필요 X

- **요약**: 유압 프레스로 과일 모양 젤리 4종(수박·오렌지·무화과·파인애플)을 눌러 터뜨리는 WebGPU 소프트바디 인터랙티브 토이 녹화
- **어울리는 경우**: 물리 시뮬레이션 데모·바이럴 숏폼 / 만족감(ASMR형) 파괴 영상 / WebGPU/그래픽 기술 쇼케이스 / 제품 소재감(젤리·반투명) 표현 레퍼런스
- **잘하는 표현**: XPBD 소프트바디의 눌림·퍼짐과 보로노이 파쇄 후 단면 캡 표현 / 서브서피스 산란 느낌의 반투명 젤리 재질 / 'Splat.' 'Well, that's jam.' 같은 이탤릭 판정 카피의 타이밍 / 과일별 단면(씨, 막, 섬유) 디테일
- **스타일**: 크림/베이지 스튜디오 바닥 위의 사실적 3D. 노랑·검정 해저드 스트라이프 프레스, 광택 있는 반투명 젤리 조각이 흩어지며 하단에 미니멀 에디토리얼 UI가 깔림. 상단에 'Claude Opus 5.5 / 14.35$' 라벨 오버레이.
- **기술**: WebGPU, WGSL 셰이더, HTML/JS 단일 파일, XPBD 사면체 소프트바디(CPU), Web Audio 절차적 사운드
- **프롬프트 구조**: CONCEPT/젤리별 외형/PHYSICS/BURST/PLAY MODE/UI/SOUND/QUALITY BAR로 나눈 초상세 기술 명세서(파라미터 수치·카피 문구까지 지정)
- **태그**: 젤리, soft-body, WebGPU, 물리시뮬, 파괴, 인터랙티브, 3D, satisfying, 에디토리얼UI
- **주의**: 영상은 인터랙티브 토이 화면 녹화이며 모델명·비용 라벨이 박혀 있음

### game (게임) — 16건 (조회수순)

#### [Minecraft clone in browser](game__minecraft-clone-in-browser__2102470200415166699.md)
`game__minecraft-clone-in-browser__2102470200415166699` · 16:9 · 23s · 조회 506K · 에셋필요 X

- **요약**: 고급 셰이더로 실사에 가깝게 꾸민 브라우저용 Minecraft 클론 플레이 화면
- **어울리는 경우**: 게임 데모·트레일러 / 원라이너 프롬프트 역량 시연 / 복셀 풍경 B-roll
- **잘하는 표현**: 물 투명도·반사, 일몰 역광 등 셰이더 조명 / 해변·설산·숲 등 다양한 바이옴 풍경 / 1인칭 이동 카메라
- **스타일**: 복셀 3D 블록 지형에 셰이더팩 같은 사실적 조명: 청록 바다, 금빛 석양, 눈 덮인 침엽수 산. 채도 높고 밝은 게임 그래픽.
- **기술**: 브라우저 WebGL(추정, 메타 미기재)
- **프롬프트 구조**: 두 문장짜리 짧은 원라이너
- **태그**: Minecraft, 복셀, 게임, 셰이더, 1인칭, 풍경, one-liner, browser-game
- **주의**: 게임 플레이 녹화라 편집된 모션 영상 레퍼런스로는 제한적

#### [Roblox anime fighting game](game__roblox-anime-fighting-game__2102487879809126834.md)
`game__roblox-anime-fighting-game__2102487879809126834` · 약 4:3 (932x720) · 133s · 조회 463K · 에셋필요 X

- **요약**: 주술회전 시부야 테마 아레나에서 애니 캐릭터들이 싸우는 스매시브라더스식 Roblox 격투 게임 'Cursed Clash' 플레이 영상
- **어울리는 경우**: 게임 개발 데모·트레일러 / AI 에이전트 게임 제작 쇼케이스 / 애니풍 액션 하이라이트 클립
- **잘하는 표현**: 캐릭터 선택 UI부터 전투·필살기 컷인('BLACK FLASH x1')까지 완결된 게임 루프 / 네온 간판·횡단보도가 있는 야간 시부야 아레나 구성 / 타격 VFX와 데미지% HUD
- **스타일**: 어두운 남보라 야간 도시에 붉은·분홍 네온 간판, 로블록스 블록 캐릭터, 흰 타격 이펙트. 선택 화면은 진홍·검정 게이밍 UI, 필살기 컷인은 붉은 사선 그래픽과 한자 타이포.
- **기술**: Roblox Studio, Roblox Toolbox 에셋(VFX·애니메이션), 서브 에이전트 병렬 작업
- **프롬프트 구조**: 게임 콘셉트·참고 IP·툴박스 활용·서브에이전트 비평 지시를 담은 캐주얼한 짧은 요청문
- **태그**: Roblox, 게임, 격투, 애니, 주술회전, 네온, 야간도시, smash-bros, 게임플레이
- **주의**: 기존 IP 캐릭터·Toolbox 에셋 의존, 플레이 화면 녹화라 모션그래픽 레퍼런스로는 제한적

#### [Far Cry 3 clone game (polished)](game__far-cry-3-clone-game-polished__2103960867327115462.md)
`game__far-cry-3-clone-game-polished__2103960867327115462` · 16:9 · 128s · 조회 214K · 에셋필요 O

- **요약**: Far Cry 3를 모방한 열대 섬 1인칭 슈터를 Three.js로 고도화한 플레이 영상 (6~11단계 그래픽 개선)
- **어울리는 경우**: 게임 그래픽 쇼케이스 / 열대 섬·물 표현 참고 / 장기 다단계 개발 프롬프트 예시
- **잘하는 표현**: 청록 얕은 바다·리프 드롭오프 물 렌더링 / 잎 그림자(dappled shadow)와 강한 대비 그레이딩 / 낡은 나무 데크·소품 절차적 재질 / 1인칭 손·무기 뷰
- **스타일**: 채도 높은 열대 정오: 청록 라군, 카르스트 바위섬, 야자수, 그림자 진 낡은 나무 데크와 소품, 1인칭 소총·칼 든 손. 실사 지향 3D이나 일부 컷은 뿌옇고 로우폴리 느낌이 남아 있음.
- **기술**: Three.js, WebGL 셰이더(FFT 오션, SSR, SSAO 등), 절차적 텍스처 생성
- **프롬프트 구조**: 이전 단계 완료를 전제로 한 단계별(Stage 6~11) 작업지시서: 목표 → 번호 목록 세부사항(색 hex·수치) → Acceptance 기준, 전역 규칙과 성능 예산 포함
- **태그**: 게임, FPS, Three.js, 열대, water-rendering, AAA-지향, 단계별프롬프트, 3D
- **주의**: Far Cry 3 레퍼런스 이미지·.glb 모델 등 에셋 의존, Stage 1~5 결과 전제; 게임 IP 모방

#### [Far Cry 3-style playable game prototype in Three.js](game__far-cry-3-style-playable-game-prototype-in-three-js__2103423427939897781.md)
`game__far-cry-3-style-playable-game-prototype-in-three-js__2103423427939897781` · 16:9 · 122s · 조회 161K · 에셋필요 O

- **요약**: Far Cry 3 분위기의 열대 석호 1인칭 게임(AK-47, 돌 던지기, 날씨·시간대 전환)을 Three.js로 만든 플레이 녹화
- **어울리는 경우**: FPS/서바이벌 게임 프로토타입 소개 / 날씨·시간대 시스템 데모 / 열대 환경 아트 쇼케이스 / 웹 3D 그래픽 한계 실험 영상
- **잘하는 표현**: 맑음/노을/밤/비·안개 등 시간대·날씨별 분위기 변화 / 터키석 얕은 물과 물결 링 같은 물 셰이더 / 보이는 1인칭 손·무기 뷰모델 / 판잣집·테이블·상자 등 소품 배치
- **스타일**: 청록 바다와 모래, 야자수의 열대 3D 실시간 렌더. 시간대에 따라 따뜻한 노을 오렌지, 푸른 밤, 회색 안개 톤으로 바뀌며 텍스처는 중간 수준의 세미리얼.
- **기술**: Three.js, PBR·물·포그 셰이더, 브라우저 1인칭 게임
- **프롬프트 구조**: 15개 번호 섹션의 초장문 게임 기획서(월드, 소품, 1인칭 애니, 메커닉별 요구, 날씨, 시간대, 그래픽 기법 목록, 사운드, 조작키, 레퍼런스 이미지 활용)
- **태그**: Three.js, FPS, 열대, 날씨시스템, 시간대, 게임플레이, 물셰이더, 1인칭
- **주의**: 사용자 레퍼런스 이미지에 의존하고 총기 묘사가 중심이다. 그래픽은 프롬프트가 요구한 하이엔드 수준엔 못 미친다

#### [Game settlement and card draw animations](game__game-settlement-and-card-draw-animations__2104085484347818226.md)
`game__game-settlement-and-card-draw-animations__2104085484347818226` · 16:9 · 18s · 조회 128K · 에셋필요 X

- **요약**: 모바일 게임식 'Star Summon' 가챠 카드 뽑기·보상 연출(보석 발광→카드 펼침→SSR 공개)
- **어울리는 경우**: 게임 보상/가챠 연출 / 앱 이벤트·업적 해금 하이라이트 / '결과 공개' 리빌 모먼트 영상
- **잘하는 표현**: 충전→폭발→리빌로 이어지는 단계별 연출 리듬 / 방사형 광선·플래시·파티클 같은 부드러운 광효과 / 카드 그리드 배치와 SSR 정보 패널의 게임 UI 완성도 / GSAP 타임라인 기반 스쿼시·오버슈트 모션
- **스타일**: 남보라 마법진 배경에서 금빛으로 전환되는 고채도 카툰 게임 UI, 두꺼운 외곽선의 카드 일러스트(모래시계, 방패, 고양이 등), 크림·금색 방사광 리빌 화면.
- **기술**: Three.js, GSAP, Canvas 2D 파티클, Web Audio API, 단일 HTML/CSS/JS
- **프롬프트 구조**: [주체] 치환 슬롯 템플릿 + 스타일/3D/2D/5단계 연출/광효과/재질/애니 원칙/음향/엔지니어링 규칙 + 단계별 스크린샷 자체 검수 질문 목록
- **태그**: 게임UI, 가챠, 카드뽑기, 보상연출, 파티클, GSAP, 카툰, reveal
- **주의**: 프롬프트 예시는 상자 열기·등급 상승인데 실제 영상은 카드 소환 가챠라 템플릿의 응용 결과로 봐야 함

#### [Spear fishing browser game](game__spear-fishing-browser-game__2102773498037023140.md)
`game__spear-fishing-browser-game__2102773498037023140` · 16:9 · 91s · 조회 117K · 에셋필요 X

- **요약**: 무인도 생존 컨셉의 브라우저 3D 작살 낚시 게임 플레이 영상 (수중 1인칭)
- **어울리는 경우**: 게임 트레일러/플레이 영상 / 수중 환경 표현 참고 / 1인칭 HUD 디자인
- **잘하는 표현**: 코스틱 빛무늬가 있는 수중 해저 표현 / 잠수 마스크 프레임 비네팅 HUD / 작살 1인칭 무기 뷰
- **스타일**: 청록색 수중 공간, 해초·바위·모래 해저와 수면 빛 산란, 잠수 마스크 모양 둥근 프레임 테두리. 우하단 엔화 금액·상태 HUD, 일본어 UI 텍스트. 수면 위 컷은 파란 하늘과 흰 구름.
- **기술**: Three.js (프롬프트상 상정), Codex CLI 이미지 생성 (선택적 허용)
- **프롬프트 구조**: 일본어 자유 서술: 프로젝트 맥락 + 컨셉(무인도 0엔 생활) + 라이브러리 권장 + '재미·그래픽·UI 퀄리티로 놀라게' 요구
- **태그**: 게임, browser-game, Three.js, 수중, 1인칭, HUD, 일본어, 3D
- **주의**: 게임 플레이 녹화라 영상 편집 레퍼런스로는 제한적

#### [Rocket League-style clone with cinematic](game__rocket-league-style-clone-with-cinematic__2102847543042343072.md)
`game__rocket-league-style-clone-with-cinematic__2102847543042343072` · 16:9 · 67s · 조회 44K · 에셋필요 O

- **요약**: Three.js+Rapier로 만든 Rocket League 스타일 브라우저 게임과 경기장 시네마틱 플라이스루
- **어울리는 경우**: 게임 트레일러/시네마틱 인트로 / e스포츠 경기장 분위기 영상 / 웹 3D 게임 개발 쇼케이스
- **잘하는 표현**: 대형 공 클로즈업 등 다이내믹 카메라 앵글 / 네온 오렌지/블루 조명의 경기장 디테일(관중석, 전광판, 비행선) / 부스트 트레일·불꽃 이펙트
- **스타일**: 보랏빛 황혼 하늘의 실내 스타디움, 초록 잔디와 주황·파랑 네온 트림, 육각 패턴 골대, 블룸 강한 게임 그래픽 3D.
- **기술**: Three.js, Rapier.js, Vite, TypeScript/JavaScript, RocketSim
- **프롬프트 구조**: 기술 요구/게임플레이/조작/카메라/비주얼/물리 감각/AI/검증/산출물 섹션의 긴 개발 명세 + 원작과 동일하게 반복 개선하라는 추가 피드백
- **태그**: 게임, Three.js, 스포츠, 네온, 시네마틱, 경기장, 3D, trailer
- **주의**: 원작 IP(Rocket League, Octane, Champions Field)를 그대로 재현하도록 요구한 프롬프트라 상업 레퍼런스로 쓰기 곤란

#### [Interactive jelly watermelon toy](game__interactive-jelly-watermelon-toy__2106056420131029473.md)
`game__interactive-jelly-watermelon-toy__2106056420131029473` · 약 3:2 (1114x720) · 17s · 조회 42K · 에셋필요 X

- **요약**: 통수박 젤리를 칼로 잘라 조각내는 WebGPU 인터랙티브 토이 'Whole Melon' 플레이 녹화
- **어울리는 경우**: 물리·파괴 만족감 숏폼 / 제품 사진 같은 3D 소재 표현 레퍼런스 / WebGPU/그래픽 기술 데모
- **잘하는 표현**: SDF 기반 절단면에 씨와 과육 층이 보이는 단면 표현 / 칼날이 눌러 들어가며 조각이 갈라지는 절단 연출 / 반투명 젤리 굴절과 컬러 그림자 / 통수박→다수 조각까지 진행하는 단계적 변화
- **스타일**: 연회색 페이퍼 스윕 스튜디오의 제품 사진풍 3D. 광택 있는 초록 줄무늬 수박과 붉은 반투명 과육, 금속 칼, 좌상단 이탤릭 세리프 'Whole Melon.' 제목과 우측 미니 패널. 상단에 'Claude Opus 5.5 30.07$' 라벨.
- **기술**: WebGPU, WGSL, HTML/JS 단일 파일, XPBD 물리(CPU), SDF·surface nets
- **프롬프트 구조**: SHAPE AND MATERIAL / PIECES AND CUTTING / PHYSICS / RENDERING / UI / Quality bar로 나눈 초상세 그래픽스 엔지니어링 명세 + 헤드리스 스크린샷 테스트 지시
- **태그**: 수박, 젤리, 절단, WebGPU, soft-body, SDF, 3D, satisfying, 에디토리얼UI
- **주의**: 화면 녹화에 모델명·비용 라벨 포함. 프롬프트가 매우 고난도라 재현 비용 큼

#### [Mining operations strategy game](game__mining-operations-strategy-game__2107022944916709886.md)
`game__mining-operations-strategy-game__2107022944916709886` · 16:9 · 30s · 조회 35K · 에셋필요 X

- **요약**: 광산 운영 소프트웨어를 아이소메트릭 3D 전략 게임처럼 만든 인터랙티브와 그 30초 데모 영상(캡션 + 커서 투어 + 브랜드 엔딩)
- **어울리는 경우**: B2B SaaS/산업 소프트웨어 제품 소개 / 운영 대시보드 데모 영상 / 프로세스 흐름(공정) 설명 / 투자자/세일즈 피치 티저
- **잘하는 표현**: 아이소메트릭 장면 위 알림·상태·흐름 패널을 겹친 정보 레이어 / 카메라 투어 + 굵은 단문 캡션('Belt drift caught at 38 mm.')의 내러티브 / 커서 클릭으로 경보 대응을 보여주는 데모 연출 / 검정 배경 로고+태그라인 엔딩
- **스타일**: 흰 배경에 라벤더 그림자, 흰 건물·파란 지붕·노란 트럭의 밝고 깨끗한 아이소메트릭 3D. 플로팅 화이트 패널 UI와 굵은 산세리프 캡션의 프리미엄 미니멀 톤, 엔딩만 검정 배경에 녹색 로고.
- **기술**: Three.js, 단일 HTML
- **프롬프트 구조**: [INDUSTRY]/[KEY ASSETS]/[TAGLINE] 등 대괄호 슬롯이 있는 재사용 템플릿(스타일 / 씬 / UI 배치 / 게임 루프 / 30초 데모 영상 지시)
- **태그**: 아이소메트릭, B2B, SaaS, product-demo, 3D, Three.js, 캡션, 템플릿프롬프트, 라이트모드
- **주의**: 슬롯형 템플릿이라 다른 산업으로 바꾸기 쉽다. 브랜드 로고와 태그라인은 사용자가 채워야 한다

#### [Fortnite-style game one-shot test](game__fortnite-style-game-one-shot-test__2104779190277181699.md)
`game__fortnite-style-game-one-shot-test__2104779190277181699` · 1:1 · 42s · 조회 29K · 에셋필요 X

- **요약**: 원샷으로 만든 Fortnite 스타일 배틀로얄 게임 플레이(Sonnet 5.5 결과)를 실제 Fortnite(Epic Games $20M) 화면과 번갈아 비교한 영상
- **어울리는 경우**: AI 결과 vs 실제 제품 비교 밈 영상 / 게임 프로토타입 시연 / 원샷 프롬프트 성능 테스트 콘텐츠
- **잘하는 표현**: 3인칭 TPS 카메라·건축 벽 시스템 / 미니맵·체력·인벤토리 HUD 재현 / 라벨 교차 편집으로 비교 리듬
- **스타일**: 밝고 채도 높은 카툰풍 3D: 연두 들판, 둥근 나무, 분홍·보라 하늘, 나무 벽. 상단에 굵은 흰 이탤릭 자막 라벨이 붙은 정사각 비교 편집.
- **기술**: 브라우저 3D 게임(구체 도구 미기재)
- **프롬프트 구조**: 기능 목록(카메라·전투·봇·인벤토리·건축·스톰·섬·UI)을 한 문단에 나열한 짧은 원샷 프롬프트
- **태그**: Fortnite, 배틀로얄, 게임, TPS, 비교영상, 카툰3D, one-shot, 밈
- **주의**: 절반은 실제 Fortnite 화면이고 라벨은 Sonnet 5.5로 표시되어 메타의 opus-5.5와 다름. 단독 스타일 참고엔 부적합

#### [Endless procedurally generated exploration world](game__endless-procedurally-generated-exploration-world__2102529695908806728.md)
`game__endless-procedurally-generated-exploration-world__2102529695908806728` · 16:9 · 81s · 조회 22K · 에셋필요 X

- **요약**: Three.js로 만든 끝없는 절차 생성 초원 세계를 캐릭터가 돌아다니며 생물과 상호작용하는 코지 게임 플레이 녹화
- **어울리는 경우**: 코지/힐링 게임 프로토타입 소개 / 절차 생성(procedural) 기술 데모 / 편안한 배경 B-roll / 웹 게임 개발 과정 쇼케이스
- **잘하는 표현**: 풀·나무·꽃이 빽빽한 절차 생성 지형 / NPC 말풍선, 호수 물결 링 등 소소한 상호작용 / 밝고 평온한 분위기 유지
- **스타일**: 선명한 초록 초원과 파란 하늘, 로우폴리 나무와 둥근 캐릭터의 밝은 3D 카툰 스타일. 맥 브라우저 창 크롬이 그대로 보이는 화면 녹화.
- **기술**: Three.js, 브라우저 절차 생성
- **프롬프트 구조**: 자연어 단락형 요청(분위기 레퍼런스: 슈퍼마켓 시뮬레이터 느낌) + 스스로 목표 설정 후 완료 시 알림 지시
- **태그**: Three.js, procedural, 코지게임, 로우폴리, 초원, 탐험, 게임플레이, 밝은톤
- **주의**: 브라우저 UI가 포함된 원본 플레이 녹화라 편집 연출 참고 가치는 낮다

#### [Native Swift FPS game](game__native-swift-fps-game__2107155466987987309.md)
`game__native-swift-fps-game__2107155466987987309` · 16:9 · 49s · 조회 20K · 에셋필요 X

- **요약**: 에셋 없이 마인크래프트풍 블록 그래픽으로 만든 네이티브 Swift 모바일 FPS를 실제 폰으로 플레이하는 장면을 촬영한 영상
- **어울리는 경우**: 모바일 게임 실기 시연 / 앱 데모의 손+폰 실사 촬영 구도 / AI 원샷 개발 결과 쇼케이스
- **잘하는 표현**: 실제 손으로 폰을 쥔 핸즈온 촬영이라 신뢰감 / 블록형 FPS 화면, 무기고/일시정지 설정 UI까지 보여줌
- **스타일**: 나무 바닥 위에서 두 손으로 가로 폰을 들고 찍은 실사 촬영. 폰 화면에는 회색 블록 벽, 노란 상자, 주황 UI 포인트가 있는 로우폴리 복셀 FPS와 남색 무기고 메뉴가 보인다.
- **기술**: Swift, Expo, RevenueCat, Google AdMob
- **프롬프트 구조**: COD Mobile 같은 게임을 에셋 없이 마인크래프트처럼, 발열 최적화 최우선이라는 한 문장 원라이너
- **태그**: FPS, 모바일게임, Swift, 복셀, 핸즈온촬영, 실사, game-demo
- **주의**: 화면 녹화가 아니라 폰을 들고 찍은 실사라 게임 화면은 작고 흔들림. 메타의 RevenueCat/AdMob은 수익화 연동이지 영상 기술은 아님

#### [Police chase arcade game prototype](game__police-chase-arcade-game-prototype__2103789415323562325.md)
`game__police-chase-arcade-game-prototype__2103789415323562325` · 16:9 (1290x720, 가로 폰 목업) · 59s · 조회 18K · 에셋필요 O

- **요약**: 사막 아레나에서 경찰 추격을 피하며 경찰차끼리 충돌시키는 모바일 탑다운 아케이드 게임 프로토타입을 폰 목업 안에서 시연한 영상
- **어울리는 경우**: 모바일 게임 프로토타입 시연 / 앱/게임 홍보용 폰 목업 영상 / 게임 기획(PRD) → 구현 사례
- **잘하는 표현**: 장난감 같은 청키 3D 차량과 드리프트 스키드 자국 / 점수·수배 별·HULL 바·조이스틱·부스트 버튼 HUD / 충돌·연기 파티클로 보여주는 혼돈
- **스타일**: 모래색 사막 바닥에 주황 바위와 초록 선인장이 흩어진 밝은 카툰풍 저채도 3D 탑다운. 폰 프레임 목업을 macOS풍 주황·파랑 그라데이션 배경 위에 얹었다.
- **기술**: Unity, Topdown Engine, ChatGPT
- **프롬프트 구조**: 제품 비전·코어 루프·설계 원칙·MVP 범위·AI·점수·UI·오디오·아키텍처·마일스톤을 갖춘 완전한 게임 PRD 문서
- **태그**: 모바일게임, 탑다운, 카체이스, Unity, 카툰3D, 폰목업, PRD, arcade
- **주의**: PRD에는 세로 화면이라고 했지만 실제 영상은 가로 플레이. 유료 Topdown Engine 에셋에 의존함

#### [MV-inspired game built in Unity](game__mv-inspired-game-built-in-unity__2102660297928638783.md)
`game__mv-inspired-game-built-in-unity__2102660297928638783` · 약 16:9 (1210x720) · 54s · 조회 18K · 에셋필요 O

- **요약**: 뮤직비디오 특정 구간의 움직임을 재현한 Unity 2D 횡스크롤 닌자 액션 게임의 플레이 녹화
- **어울리는 경우**: 게임 트레일러/플레이 시연 / 2D 액션 연출 참고 / AI로 만든 인디게임 쇼케이스
- **잘하는 표현**: 보름달·등불·기와지붕의 레이어드 배경 / 주황 반달형 베기 이펙트와 대시 모션 / HP 바와 코인 카운터 HUD
- **스타일**: 남색 밤하늘에 큰 보름달과 붉은 유성 줄기, 일본식 기와지붕 위를 달리는 2D 일러스트 닌자 캐릭터. 따뜻한 등불 빛과 주황 슬래시 이펙트가 차가운 배경과 대비된다.
- **기술**: Unity
- **프롬프트 구조**: MV 특정 타임코드 재현 지시 + 구현→실행→플레이→스크린샷→엄격한 Visual QA 반복 루프 + 벤치마크 게임(록맨 11) 조사 + 플레이스홀더 금지 기준
- **태그**: 2D액션, 닌자, Unity, 횡스크롤, 보름달, 일본풍, 게임플레이, indie-game
- **주의**: 원본 MV가 있어야 재현 가능한 프롬프트이고, 결과물은 게임 플레이 녹화라 영상 편집 레퍼런스로는 간접적

#### [Voice-prompted game concept build](game__voice-prompted-game-concept-build__2102880697467732080.md)
`game__voice-prompted-game-concept-build__2102880697467732080` · 16:9 · 20s · 조회 14K · 에셋필요 X

- **요약**: 5개 지대를 탐험하는 탑다운 지하 탐험 샌드박스 게임을 단일 HTML로 만든 플레이 화면(일본어 UI)
- **어울리는 경우**: 인디 게임 컨셉 데모 / 게임 기획→구현 과정 소개 / 다크 판타지 UI 참고
- **잘하는 표현**: 어둠 속 색이 다른 광원(수정 청색·용암 주황) 연출 / 지대 진입 시 대형 지대명 타이포 / 미니맵·퀘스트·인벤토리 HUD 구성
- **스타일**: 어두운 청록 그리드 바닥 위 보라·주황·청색 발광 효과, 반투명 다크 패널 UI와 일본어 명조 타이틀. 2D 탑다운의 차분한 다크 판타지 톤.
- **기술**: HTML/Canvas, WebAudio, GPT-6 Sol(메타 tools 표기)
- **프롬프트 구조**: 일본어로 【핵심】【세계】【진행】【동선】【적】【화면】【제약】【확인】【먼저】 대괄호 섹션을 짧게 나열한 기획서형, 구현 전 1화면 기획서 요구
- **태그**: 게임, 탑다운, 던전탐험, 다크UI, 글로우, 일본어, sandbox, HTML5
- **주의**: 한 프레임은 완전 검정. 메타 tools에 GPT-6 Sol이 적혀 있어 어떤 모델 결과인지 불명확

#### [Retro game remake in a modern engine](game__retro-game-remake-in-a-modern-engine__2103327470485459444.md)
`game__retro-game-remake-in-a-modern-engine__2103327470485459444` · 16:9 · 240s · 조회 13K · 에셋필요 O

- **요약**: C64 게임 'Impossible Mission'을 리버스 엔지니어링해 16비트 콘솔풍으로 Godot에서 리메이크한 플레이 영상
- **어울리는 경우**: 레트로 게임 리메이크 데모 / 픽셀아트 게임 트레일러 / 게임 개발 과정 쇼케이스
- **잘하는 표현**: 상단 TIME/PASSWORD/SNOOZE/LIFT/PIECES HUD까지 원작 구조를 재현 / 다층 플랫폼·로봇·전기 공격 등 원작 게임플레이 재현 / 녹색 CRT 터미널 메뉴('ELVITEC SECURITY NODE 16') / 글리치 부팅 화면 인트로
- **스타일**: 검은 화면 중앙의 16비트 픽셀아트. 남색·청회색 실내 방, 갈색 'FOUNDRY SECTOR' 방, 녹색 모노크롬 CRT 터미널 팝업으로 구성된 레트로 SF 게임 화면.
- **기술**: Godot, 원작(C64) 레퍼런스 리버스 엔지니어링
- **프롬프트 구조**: '이 C64 게임을 리버스 엔지니어링해 16비트 콘솔 포트처럼 Godot으로 만들어라' 한 줄 + 원작 첨부
- **태그**: 레트로, 픽셀아트, 16bit, Godot, 리메이크, 게임플레이, CRT, C64
- **주의**: 원작 게임 자료가 필요하고 4분 플레이 녹화라 영상 연출 레퍼런스로는 약함

### comparison (모델 비교) — 27건 (조회수순)

#### [Jelly candy simulation comparison](comparison__jelly-candy-simulation-comparison__2103741107225907467.md)
`comparison__jelly-candy-simulation-comparison__2103741107225907467` · 8:9 (720x810) · 18s · 조회 439K · 에셋필요 X

- **요약**: WebGPU 소프트바디 수박 젤리를 드래그해 늘리고 흔드는 데모를 Claude Opus 5.5와 ChatGPT-6 Astra 결과로 번갈아 비교한 영상
- **어울리는 경우**: 모델/툴 결과 비교 콘텐츠 / 젤리·말랑한 재질의 제품 티저 / 물리 시뮬 인터랙션 데모
- **잘하는 표현**: 말랑한 변형·흔들림 소프트바디 물리 / 반투명 젤리 굴절·광택 재질 / 에디토리얼 레이아웃 UI와 색상 프리셋 전환
- **스타일**: 밝은 무채색 스튜디오 배경에 루비 레드·오렌지 반투명 젤리 수박, 이탤릭 세리프 'Melon Jelly.' 타이틀. 미니멀한 매거진 감성의 제품 사진 같은 3D.
- **기술**: WebGPU, WGSL, XPBD 소프트바디, 단일 HTML 파일
- **프롬프트 구조**: 오브젝트 외형·소프트바디 물리·렌더링·UI 문구·성능·검증 항목을 섹션별 대문자 헤더로 구조화한 상세 스펙
- **태그**: 젤리, soft-body, WebGPU, 3D, 비교영상, 에디토리얼, material-study, 인터랙티브
- **주의**: 두 모델 결과를 나란히 보여주는 비교 영상으로 상단에 모델명·비용 라벨이 붙어 있음. 단독 스타일 참고 시 Opus 쪽 프레임만 볼 것

#### [Watermelon rubber band test: Opus 5.5 vs GPT-6 Astra](comparison__watermelon-rubber-band-test-opus-5-5-vs-gpt-6-astra__2104994617573970308.md)
`comparison__watermelon-rubber-band-test-opus-5-5-vs-gpt-6-astra__2104994617573970308` · 720x922 (비교 레이아웃, 원본은 반응형) · 18s · 조회 415K · 에셋필요 X

- **요약**: 고무줄을 감을수록 수박이 모래시계 모양으로 조여지다 터지는 Three.js 인터랙티브 토이, Opus 5.5 vs GPT-6 Astra 비교
- **어울리는 경우**: 모델 비교/벤치마크 콘텐츠 / 물리·변형 시뮬레이션 쇼케이스 / 제품 압력 테스트식 바이럴 숏폼
- **잘하는 표현**: CPU 정점 재계산으로 수박이 조여지는 소프트 변형 / 파열 시 껍질·과육·씨·물방울 리지드바디 파편 / 따뜻한 스튜디오 조명과 접지 그림자 / 단계별 캡션 HUD와 절차적 Web Audio
- **스타일**: 따뜻한 베이지 그라디언트 배경, 줄무늬 녹색 수박과 탄색 고무줄 묶음, 부드러운 그림자의 깔끔한 3D 제품 사진풍. 파열 후 분홍 과육·껍질 조각과 물방울 자국이 바닥에 흩어짐. 2x6 비교 그리드에 모델명·비용 표기.
- **기술**: Three.js, WebGL, Web Audio API, HTML 단일 파일
- **프롬프트 구조**: 단일 섹션 장문 스펙: 무대/조명 수치 + 타이포 토큰(폰트·컬러 hex) + 오브젝트 형상 공식 + 인터랙션·캡션 단계 + 파열 물리 + 사운드 + 접근성/QA 항목
- **태그**: Three.js, 물리시뮬, soft-body, 파열, 인터랙티브토이, model-comparison, warm-studio, 디자인토큰
- **주의**: 비교 그리드 영상이라 단독 스타일 참고 시 크롭 필요; 프롬프트 자체는 수치까지 명시돼 재현성 높음

#### [How a language model answers a prompt: 20-second motion graphic](comparison__how-a-language-model-answers-a-prompt-20-second-motion-graph__2102724864205566388.md)
`comparison__how-a-language-model-answers-a-prompt-20-second-motion-graph__2102724864205566388` · 약 2.9:1 (1920x660, 두 결과를 좌우 병치) · 20s · 조회 243K · 에셋필요 X

- **요약**: 언어 모델이 프롬프트를 토큰으로 쪼개 답을 만들고 긴 답이 왜 비싼지 설명하는 모션그래픽을 Opus 5.5와 GPT-6 Sol 결과로 나란히 비교한 영상
- **어울리는 경우**: AI/기술 개념 설명 강의 / 토큰·비용 같은 추상 개념 시각화 / 모델 간 결과 비교 콘텐츠 / SaaS 대시보드풍 인포그래픽
- **잘하는 표현**: 프롬프트 → 토큰 분할 → 어텐션 → 다음 토큰 선택 → 비용 누적의 단계적 설명 흐름 / 토큰 칩, 확률 막대, 비용 카운터($0.0009) 같은 UI 요소로 개념 구체화 / 짧은 원라이너로 나온 결과의 모델별 해석 차이 확인
- **스타일**: 다크 네이비 배경의 대시보드/UI 카드 스타일 2D 인포그래픽. 파랑·주황 포인트 컬러와 산세리프 타이포의 깔끔한 미니멀 톤(GPT 쪽 일부 씬은 밝은 배경).
- **기술**: 코드 기반 모션그래픽(구체 스택 명시 없음)
- **프롬프트 구조**: 짧은 원라이너(설명 주제 + 차트가 픽셀 블록으로 부서져 재조립되는 전환 하나만 지정)
- **태그**: AI설명, 토큰, 인포그래픽, 다크모드, explainer, 비교영상, 대시보드UI, 교육
- **주의**: 좌우 비교 영상이라 단일 스타일 참고 시 Opus 쪽 절반만 봐야 하고 해상도가 낮다. 요청한 픽셀 블록 전환은 시트에서 확인되지 않는다

#### [Animated welcome screen for the Nova crypto wallet](comparison__animated-welcome-screen-for-the-nova-crypto-wallet__2102681647720395115.md)
`comparison__animated-welcome-screen-for-the-nova-crypto-wallet__2102681647720395115` · 4:3 · 7s · 조회 206K · 에셋필요 X

- **요약**: 크립토 지갑 'Nova' 모바일 웰컴 화면 애니메이션을 Opus 5.5와 GPT 6 Astra 결과로 나란히 비교한 영상
- **어울리는 경우**: 모바일 앱 온보딩·스플래시 애니메이션 / 핀테크 앱 프로모 UI 모션 / 모델/도구 결과 비교 콘텐츠
- **잘하는 표현**: $0.00→$2,480.00 잔액 카운트업과 라인 차트 드로잉 / 글래스 카드 등장·이름 레터 슬라이드·CTA 순의 타임라인 단계 연출 / 타임코드별(0.0s~2.6s) 연출 지시를 그대로 따른 순차 리빌
- **스타일**: 연회색 배경에 아이폰 목업 2개씩 3세트. 화면 안은 남색~검정 라디얼 그라디언트, 전기 파랑 글로우, 반투명 글래스 카드, 흰 Inter 타이포와 흰 필 버튼의 다크 프리미엄 핀테크 톤.
- **기술**: HTML/CSS/바닐라 JS 단일 파일(외부 라이브러리 없음)
- **프롬프트 구조**: Visual(색 코드·폰트·재질) + 초 단위 애니메이션 시퀀스 + Technical(단일 HTML, 390×844) 3단 구성의 간결한 명세
- **태그**: 핀테크, crypto, 모바일UI, 웰컴스크린, 글래스모피즘, 카운트업, 다크모드, 모델비교
- **주의**: 두 모델 비교 레이아웃이라 단독 스타일 참고 시 폰 화면만 크롭해 볼 것. 결과 차이가 크지 않음

#### [Gummy octopus physics comparison](comparison__gummy-octopus-physics-comparison__2104466170275324190.md)
`comparison__gummy-octopus-physics-comparison__2104466170275324190` · 3:4 (720x960, 2x2 그리드) · 18s · 조회 148K · 에셋필요 X

- **요약**: WebGPU 소프트바디 젤리 문어 'Octo Jelly'를 Claude Opus 5.5와 ChatGPT-6 Astra가 만든 결과를 비용과 함께 2x2로 비교한 영상
- **어울리는 경우**: 물리 시뮬/인터랙티브 토이 데모 / 제품 머티리얼 스터디풍 연출 / 모델 비교 콘텐츠
- **잘하는 표현**: 반투명 젤리 재질(굴절, 두께별 색 흡수) / 잡아당기고 놓으면 출렁이는 소프트바디 물리 / 에디토리얼 세리프 타이틀 + 미니멀 컨트롤 패널 레이아웃 / 색상 프리셋 전환(보라/주황/청록/분홍)
- **스타일**: 따뜻한 오프화이트 배경에 부드러운 그림자, 광택 있는 반투명 젤리 문어가 중앙에 크게 놓인 3D 제품샷 느낌. 좌상단 이탤릭 세리프 'Octo Jelly.'와 얇은 선 UI로 잡지처럼 정돈돼 있다.
- **기술**: WebGPU, 단일 HTML, position-based dynamics / mass-spring 소프트바디
- **프롬프트 구조**: ART DIRECTION/GEOMETRY/SOFT-BODY/INTERACTION/INTERFACE/PERFORMANCE 섹션별 불릿 명세 + UI 문구까지 지정 + 테스트 항목 나열
- **태그**: 소프트바디, WebGPU, 젤리, 물리시뮬, 오프화이트, 에디토리얼, comparison, 3D, interactive
- **주의**: 비교 그리드라 개별 화면이 작고, 마우스 조작 녹화라 영상 연출보다는 머티리얼/물리 레퍼런스로 적합

#### [Trojan Horse story painted around a Greek vase](comparison__trojan-horse-story-painted-around-a-greek-vase__2102854430454669767.md)
`comparison__trojan-horse-story-painted-around-a-greek-vase__2102854430454669767` · 약 2:1 (1442x720, Arena 좌우 비교) · 22s · 조회 147K · 에셋필요 X

- **요약**: 그리스 도기에 그려진 트로이 목마 이야기를 꽃병 회전으로 전개하는 20초 HTML 애니메이션을 GPT-6 Sol과 Opus 5.5가 각각 만든 Arena 비교
- **어울리는 경우**: 신화/역사 스토리텔링 숏폼 / 회전 오브젝트에 서사를 입히는 연출 참고 / 모델 비교 콘텐츠
- **잘하는 표현**: 원통 표면 위 흑회식 도기 그림이 회전하며 장면이 넘어가는 구조 / 낮에서 달 뜬 밤으로 바뀌는 조명 변화 / 외부 에셋 없이 코드로 그린 도기 문양
- **스타일**: 어두운 무대 위 주황 바탕에 검은 실루엣을 그린 그리스 흑회식 암포라. Opus 5.5 쪽은 꽃병이 화면을 꽉 채우는 클로즈업에 비네팅과 따뜻한 스포트 조명, 밤 장면에서는 남색 톤과 달이 들어간다.
- **기술**: HTML/CSS/Canvas (코드 드로잉)
- **프롬프트 구조**: 길이·소재·연출 비트(목마 입성, 밤, 전사 등장)·'외부 에셋 금지'를 담은 2문장 원라이너
- **태그**: 그리스도기, 트로이목마, 신화, 흑회식, 스토리텔링, Arena, 비교영상, HTML애니메이션
- **주의**: Arena 웹 UI가 그대로 녹화된 좌우 비교라 크롭이 필요함. 메타의 GPT-6 Sol은 도구가 아니라 비교 상대 모델

#### [Mongol conquest data visualization comparison](comparison__mongol-conquest-data-visualization-comparison__2102566466121797767.md)
`comparison__mongol-conquest-data-visualization-comparison__2102566466121797767` · 9:16 (720x1322) · 27s · 조회 135K · 에셋필요 O

- **요약**: 몽골 제국 정복사(1206-1294)를 지구본 지도 위 영토 확장·사건 카드·타임라인으로 재생하는 인터랙티브 역사 아틀라스 화면 녹화
- **어울리는 경우**: 역사 연대기 데이터 시각화 / 지도 기반 영토 변화 설명 / 세로형 교육 숏폼
- **잘하는 표현**: 연도·사건 카드가 타임라인과 동기화되어 넘어가는 구조 / 지도 위 영토 하이라이트·해칭·펄스 마커 / 하단 이벤트 밀도 타임라인 바
- **스타일**: 어두운 위성 지구본 위에 반투명 머스터드 골드 영토와 주황·해칭 분쟁 지역, 세리프 대형 연도 숫자와 다크 글래스 카드. 고급 다큐 지도 느낌의 다크 앤 골드 톤.
- **기술**: 웹 앱(기존 GitHub 저장소 fork)
- **프롬프트 구조**: 기존 저장소를 fork해 '엄청 인상적으로 구현하라'는 짧은 원라이너, 모델 간 경쟁 맥락
- **태그**: 역사, 지도, data-viz, 타임라인, 다크골드, 세로영상, 인포그래픽, atlas
- **주의**: 프롬프트가 외부 저장소의 명세에 의존해 프롬프트 자체로는 재현 불가. 비교 영상이라고 되어 있으나 시트에는 한 쪽 결과만 보임

#### [Browser octopus physics comparison](comparison__browser-octopus-physics-comparison__2106809017850818679.md)
`comparison__browser-octopus-physics-comparison__2106809017850818679` · 약 4:5 (720x878) · 18s · 조회 131K · 에셋필요 X

- **요약**: WebGPU 봉제 문어 인형 'Plush Octopus' 인터랙티브 토이를 Claude Opus 5.5와 GPT-6.1 결과로 비교한 영상
- **어울리는 경우**: 모델 비교 콘텐츠 / 봉제/퍼 재질 3D 토이 레퍼런스 / 귀여운 캐릭터 물리 인터랙션 데모
- **잘하는 표현**: 실시간 퍼(털) 재질과 소프트 섀도 / 팔 늘이기·손가락 잡기·흔들기 등 소프트바디 인터랙션 / 코랄·라일락·라군 3색 프리셋 전환
- **스타일**: 웜 그레이 스튜디오 바닥, 좌상단 이탤릭 세리프 'Plush Octopus.' 제목과 우측 컨트롤 패널의 '머티리얼 스터디' 에디토리얼 레이아웃. Opus 쪽은 털 질감이 보이는 3D 문어, GPT 쪽은 매끈한 클레이 느낌. 각 행 상단에 모델명·비용 라벨.
- **기술**: WebGPU, HTML 단일 파일(외부 라이브러리·에셋 없음), 절차적 지오메트리·퍼
- **프롬프트 구조**: 외형 묘사 문단 + 인터랙션 도구별 불릿(Finger/Comb/Shake) + 컨트롤·레이아웃 지정의 중간 길이 명세
- **태그**: 문어, plush, fur, WebGPU, soft-body, 모델비교, 귀여움, 에디토리얼UI, 3D
- **주의**: 비교 레이아웃이라 단독 참고 시 Opus 행만 볼 것. 비용 라벨 오버레이 포함

#### [Interactive 3D stained-glass hibiscus flower](comparison__interactive-3d-stained-glass-hibiscus-flower__2105328178051092804.md)
`comparison__interactive-3d-stained-glass-hibiscus-flower__2105328178051092804` · 16:9 (6열 비교 패널) · 60s · 조회 114K · 에셋필요 O

- **요약**: 스테인드글라스 질감의 3D 히비스커스 꽃을 회전시키며 보여주는 브라우저 아트를 Opus 5.5 Extra와 Astra High로 비교한 영상
- **어울리는 경우**: 오브젝트 턴테이블 쇼케이스 / 소재/질감 표현 데모 / 모델 간 3D 품질 비교 / 아트·뷰티 브랜드 비주얼
- **잘하는 표현**: 반투명 유리 꽃잎의 그라데이션(핑크·코랄·피치)과 금색 이음선 / 느린 자동 회전으로 앞·옆·뒷면 확인 / 어두운 차콜 배경 대비로 색이 살아나는 조명
- **스타일**: 근검정 차콜 배경 위에 핑크-코랄-피치 그라데이션 꽃잎과 녹색 줄기가 떠 있는 3D 렌더. 절제된 미니멀 구성이며 Opus 쪽은 얇은 검은 결선이 보이는 반투명 유리, Astra 쪽은 물결 무늬 텍스처.
- **기술**: 브라우저 3D(WebGL/Three.js 계열 추정, 프롬프트는 엔진 미지정), 코드 생성 지오메트리·텍스처, 단일 HTML
- **프롬프트 구조**: 섹션별 디자인 브리프(FLOWER / MATERIAL AND LIGHT / MOVEMENT AND INTERACTION / DELIVERY) + 첨부 잎 이미지 레퍼런스 + 회전 검수 후 수정 지시
- **태그**: 3D, 스테인드글라스, 꽃, 턴테이블, 다크배경, 비교영상, 질감, 아트
- **주의**: 좁은 세로 패널 6개로 병치된 비교 영상이라 개별 결과 해상도가 낮다. 첨부 잎 이미지 레퍼런스가 필요하다

#### [Volcanic island 3D scene version comparison](comparison__volcanic-island-3d-scene-version-comparison__2102450239923720440.md)
`comparison__volcanic-island-3d-scene-version-comparison__2102450239923720440` · 8:3 (1920x720, 좌우 분할) · 20s · 조회 105K · 에셋필요 X

- **요약**: 같은 선사시대 섬 Three.js 프롬프트를 Claude Opus 5와 Opus 5.5에 주고 결과를 비용과 함께 나란히 보여준 비교 영상
- **어울리는 경우**: 모델/버전 비교 콘텐츠 / 웹 3D 디오라마 품질 기준 참고 / Before/After 분할 화면 구성
- **잘하는 표현**: 단면이 보이는 원통형 수조 디오라마(5.5) / 낮/일몰/밤/눈 테마 전환 / 좌우 분할에 모델명·비용 라벨을 단 비교 레이아웃
- **스타일**: 흰 상단 바에 모델명과 초록 비용 배지가 있는 좌우 분할 화면. Opus 5는 단색 배경 위 로우폴리 초록 화산섬, Opus 5.5는 'Mammoth Island' 원통형 수중 단면 디오라마(파스텔, 얼음/설원 버전 포함)로 미니어처 느낌이 강하다.
- **기술**: Three.js, WebGL, 단일 HTML
- **프롬프트 구조**: VISUAL DIRECTION/ISLAND/WATER/DINOSAURS/ANIMATION/INTERACTION/AUDIO/TECHNICAL 섹션으로 나눈 상세 기능 명세 + 금지사항 + 전체 인터랙션 테스트 후 납품 지시
- **태그**: 비교영상, split-screen, Three.js, 디오라마, 수중단면, 로우폴리, model-comparison, 3D
- **주의**: 비교 영상이라 한 화면이 반폭이고, 결과물이 프롬프트의 공룡보다 매머드/설원 쪽으로 보이는 프레임도 있어 단독 스타일 참고엔 약함

#### [AI video editing workflow comparison](comparison__ai-video-editing-workflow-comparison__2105682280765350117.md)
`comparison__ai-video-editing-workflow-comparison__2105682280765350117` · 9:16 · 49s · 조회 78K · 에셋필요 O

- **요약**: 같은 토킹헤드 촬영본을 Opus 5.5, GPT-6 Astra, Fable 5.1에 주고 무음 컷과 말→비주얼 변환 편집 결과를 세로 3단으로 비교한 영상
- **어울리는 경우**: 토킹헤드 + 모션그래픽 편집 자동화 참고 / AI 편집 도구 비교 숏폼 / 강의/설명형 릴스 편집 스타일
- **잘하는 표현**: 말하는 내용을 Venn 다이어그램·A/B 원·체크리스트로 바꾸는 시각화 / 화면 분할(그래픽 + 인물 PIP/원형 아바타) 레이아웃 전환 / 키워드만 노란색으로 강조한 하단 자막 / 픽셀아트 아바타 같은 위트 있는 인서트
- **스타일**: 짙은 남색 배경에 흰 굵은 산세리프와 얇은 라인 아이콘, 오른쪽이나 원형 PIP로 들어가는 실사 토킹헤드(밝은 방, 화분). 플랫 2D 인포그래픽이고 상단에 'Which AI edits better?' 타이틀 바가 있다.
- **기술**: 외부 생성 모델(GPT-6 Astra, Fable 5.1, Opus 5.5) 비교
- **프롬프트 구조**: 같은 푸티지·레퍼런스 제공 → 무음 컷 + 말을 비주얼로 → 첫 10초 리뷰 후 라운드별 수정이라는 3단계 워크플로 서술
- **태그**: 토킹헤드, 자동편집, 무음컷, 인포그래픽, 키워드자막, 9:16, shorts, model-comparison, 다크네이비
- **주의**: 이 프로젝트(컷 편집 + 비주얼 삽입)와 가장 직결되는 레퍼런스지만 실제 프롬프트는 워크플로 요약뿐이라 프롬프트 자체는 재사용하기 어려움

#### [Jelly physics simulation improvement comparison](comparison__jelly-physics-simulation-improvement-comparison__2103822857155313953.md)
`comparison__jelly-physics-simulation-improvement-comparison__2103822857155313953` · 3:4 · 20s · 조회 78K · 에셋필요 X

- **요약**: WebGPU 귤 조각 젤리 'Citrus Jelly'를 Opus 5.5 출시일 버전과 최근 버전으로 비교해 물리·재질 개선을 보여주는 영상
- **어울리는 경우**: 모델 버전 간 개선 비교 콘텐츠 / 소프트바디 물리 데모 / 젤리·반투명 소재 표현 레퍼런스
- **잘하는 표현**: 당기기·늘어남·복원 진동 등 소프트바디 변형 / 색상 프리셋(오렌지·블러드오렌지·레몬 등) 전환 / 개선 전후 대비로 품질 차이를 직관적으로 보여주는 편집
- **스타일**: 출시일 버전은 연보라 배경에 회색 대형 'jelly' 텍스트와 광택 플라스틱 같은 귤·라임·자몽 조각, 최근 버전은 크림 배경·이탤릭 세리프 'Citrus Jelly.' 제목·우측 패널과 실제로 휘어지는 반투명 젤리. 각 행 상단에 모델명·비용 라벨.
- **기술**: WebGPU, WGSL 셰이더, HTML 단일 파일, 소프트바디(스프링 메시/볼륨 제약)
- **프롬프트 구조**: APPEARANCE/PHYSICS AND INTERACTION/INTERFACE/TECHNICAL REQUIREMENTS 섹션별 요구사항 + 금지사항('rigid plastic 금지' 등) + 테스트 항목
- **태그**: 젤리, soft-body, WebGPU, before-after, 모델비교, 에디토리얼UI, 3D, 과일
- **주의**: 비교 영상이며 위 절반(구버전)은 프롬프트 의도에서 벗어난 결과. 스타일 참고는 'Today' 행만 사용

#### [Post-Biological Consciousness Experience](comparison__post-biological-consciousness-experience__2107110129363472474.md)
`comparison__post-biological-consciousness-experience__2107110129363472474` · 7:3 (1680x720, 좌우 비교 + 하단 캡션) · 65s · 조회 57K · 에셋필요 X

- **요약**: 인간 의식이 기계로 옮겨가는 과정을 다룬 인터랙티브 아트 웹 경험을 GPT-6 Astra와 Opus 5.5가 만든 결과를 사용량·소요시간과 함께 비교한 영상
- **어울리는 경우**: 철학/미래 주제 영상의 분위기 오프닝 / 몰입형 스크롤 웹 아트 참고 / 모델 비교 콘텐츠
- **잘하는 표현**: 어둠 속 조명받은 두상과 파티클로 해체되는 몸 / 홀로그램 신경망 인체(파란 와이어) / 절제된 이탤릭 세리프 문구 타이포
- **스타일**: 거의 검은 배경에 따뜻한 주황 림라이트를 받은 마네킹 두상, 흩어지는 금빛 파티클, 청색 홀로그램 인체가 이어지는 시네마틱 다크 톤. 텍스트는 'Everything we feel.', 'Let go of form.' 같은 짧은 세리프 문구뿐이다.
- **기술**: 단일 HTML/CSS/JS, Canvas/WebGL (프롬프트에서 권장)
- **프롬프트 구조**: 주제·3단계 서사(현재→전환→업로드 이후)·시각/인터랙션/톤 요구·금지 목록을 길게 서술한 무드 중심 브리프. 구체적 샷리스트는 없음
- **태그**: 의식업로드, 포스트휴먼, 파티클, 홀로그램, 다크시네마틱, 세리프타이포, web-art, comparison
- **주의**: 비교 레이아웃에 하단 캡션 띠가 커서 실제 화면은 작음. 스크롤형 웹 경험이라 컷 리듬 참고엔 약함

#### [Pineapple Jelly](comparison__pineapple-jelly__2104103495020458415.md)
`comparison__pineapple-jelly__2104103495020458415` · 3:4 (720x960, 4x3 비교 그리드) · 18s · 조회 50K · 에셋필요 X

- **요약**: WebGPU로 만든 말랑한 파인애플 젤리 링 소프트바디 인터랙티브를 Claude Opus 5.5와 ChatGPT-6 Astra 결과로 비교한 화면 녹화
- **어울리는 경우**: 제품/소재 질감 쇼케이스 / 물리 시뮬레이션 데모 비교 / 에디토리얼 랜딩페이지형 인터랙티브 소개 / 식품·캔디 브랜드 티저
- **잘하는 표현**: 반투명 젤리의 굴절·광택·서브서피스 질감 / 늘리고 비트는 소프트바디 변형(XPBD) / 골든/앰버/로제 색상 프리셋 전환 / 이탤릭 세리프 헤딩 + 우측 스펙 패널의 에디토리얼 레이아웃
- **스타일**: 따뜻한 크림색 배경에 이탤릭 세리프 'Pineapple Jelly.' 타이틀, 작은 컨트롤 패널, 중앙에 꿀빛/로제 반투명 3D 젤리. 여백 많은 미니멀 에디토리얼 + 소프트 스튜디오 라이팅.
- **기술**: WebGPU, WGSL 셰이더, XPBD 소프트바디, 단일 HTML
- **프롬프트 구조**: 섹션별 상세 사양(MODEL / MATERIAL AND LIGHTING / PHYSICS / INTERFACE / TECHNICAL REQUIREMENTS) + 금지 사항과 테스트 항목 명시
- **태그**: WebGPU, 소프트바디, 젤리, 물리시뮬, 에디토리얼, 비교영상, 3D, 질감
- **주의**: 두 모델을 격자로 비교하고 비용 라벨과 'follow me for more' 버튼이 얹혀 있어 단독 스타일 참고엔 잘라 봐야 한다. 영상 연출이 아니라 인터랙티브 녹화다

#### [Japanese-style fantasy city pixel animation](comparison__japanese-style-fantasy-city-pixel-animation__2105033612093698466.md)
`comparison__japanese-style-fantasy-city-pixel-animation__2105033612093698466` · 16:9 · 8s · 조회 44K · 에셋필요 X

- **요약**: 일본풍 판타지 도시 픽셀아트 애니메이션을 GPT 6.1 Sol·Astra·Opus 5.5·Sonnet 5.5 4개 모델로 만든 2x2 비교
- **어울리는 경우**: 모델 비교 콘텐츠 / 픽셀아트 야경 루프 배경 / 일본풍 테마 채널 아트
- **잘하는 표현**: 벚꽃·탑·홍교·후지산·보름달 등 모티프 밀도 / 날아가는 용 등 작은 반복 애니메이션 / 같은 프롬프트의 모델별 팔레트 차이
- **스타일**: 4분할 픽셀아트: 상단(GPT/Astra)은 청록·남색 톤, 하단 Opus는 보라 하늘·붉은 다리, Sonnet은 보라·분홍 노을 톤. 벚꽃, 5층탑, 달이 공통 요소.
- **프롬프트 구조**: 형용사만 나열한 한 줄 원라이너 + '시각적으로 검증' 지시
- **태그**: 픽셀아트, pixel-art, 일본풍, 벚꽃, 야경, 비교영상, loop, gif
- **주의**: 4개 모델 결과가 작게 분할돼 개별 디테일 확인이 어려움. 구현 기술 정보 없음

#### [Four-model video prompt comparison](comparison__four-model-video-prompt-comparison__2105278940906668233.md)
`comparison__four-model-video-prompt-comparison__2105278940906668233` · 16:9 · 13s · 조회 43K · 에셋필요 X

- **요약**: 같은 프롬프트로 Canvas 2D 절차적 질주 여우 애니메이션을 Opus 5.5·Sonnet 5.5·GPT 6.1 Sol·GPT 6 Sol 4개 모델이 만든 결과를 2×2로 비교
- **어울리는 경우**: 모델 비교·벤치마크 콘텐츠 / 2D 절차적 캐릭터 애니메이션 레퍼런스 / 패럴랙스 자연 배경 루프
- **잘하는 표현**: IK 다리·꼬리 2차 모션을 가진 절차적 보행(갤럽) 사이클 / 다층 패럴랙스 숲 배경 / 동일 프롬프트에 대한 모델별 해석 차이를 한 화면에 노출
- **스타일**: 2D 벡터 일러스트. Opus/Sonnet 쪽은 보라·분홍 새벽 하늘에 침엽수 실루엣, GPT 쪽은 연녹색 플랫 숲과 청록 밤숲. 모두 주황 털 여우가 좌→우로 달리는 측면 구도이며 패널마다 흰 모델명 라벨.
- **기술**: HTML5 Canvas 2D, 바닐라 JS, requestAnimationFrame, IK·스프링 댐핑 절차적 애니메이션
- **프롬프트 구조**: Canvas & Resolution / Fox Rigging & Locomotion / Styling / Parallax Environment / Performance로 나눈 기술 명세 원샷 프롬프트
- **태그**: 여우, procedural-animation, Canvas2D, 패럴랙스, 2D일러스트, 모델비교, IK, 자연
- **주의**: 4분할 비교라 개별 화면 해상도가 낮음. 단독 스타일 참고엔 약함

#### [Gummy squid render: Opus 5.5 vs GPT-6.1 Sol](comparison__gummy-squid-render-opus-5-5-vs-gpt-6-1-sol__2105190658701201725.md)
`comparison__gummy-squid-render-opus-5-5-vs-gpt-6-1-sol__2105190658701201725` · 약 3:4 (720x938) · 18s · 조회 34K · 에셋필요 X

- **요약**: 브라우저에서 잡아당기는 WebGPU 젤리 오징어 장난감을 Claude Opus 5.5와 GPT-6.1 Sol 결과로 비교한 영상
- **어울리는 경우**: AI 모델 결과 비교 숏폼 / 귀여운 캐릭터 소프트바디 데모 / 컬러 팔레트 바리에이션 소개
- **잘하는 표현**: 촉수·지느러미가 따로 늘어나는 국소 변형 / 얇은 부위가 더 투명한 젤리 재질 / 팔레트(회색·청록·보라 등) 전환
- **스타일**: 웜 오프화이트 배경 위 반투명 파스텔 젤리 오징어(청록·라벤더·보라·코랄), 부드러운 그림자, 이탤릭 세리프 'Squid Jelly.' 타이틀의 미니멀 에디토리얼 3D.
- **기술**: WebGPU, WGSL, 질량-스프링/PBD 소프트바디, 단일 HTML 파일
- **프롬프트 구조**: 아트 디렉션·지오메트리·재질·물리·인터랙션·UI·품질을 섹션 헤더로 나눈 스펙형, Melon Jelly 프롬프트의 변주
- **태그**: 젤리, squid, soft-body, WebGPU, 비교영상, 파스텔, material-study, 3D
- **주의**: 모델명·비용 라벨이 붙은 상하 분할 비교 영상. 동일 작성자의 Melon/Fugu Jelly와 거의 같은 포맷이라 중복 참고 주의

#### [Articulated Lamp Animation in Blender](comparison__articulated-lamp-animation-in-blender__2103181133198639614.md)
`comparison__articulated-lamp-animation-in-blender__2103181133198639614` · 720x944 (세로형 비교 레이아웃, 원본 씬은 16:9) · 6s · 조회 32K · 에셋필요 O

- **요약**: Pixar 로고 램프 점프 애니메이션을 Blender로 재현한 GPT-6 Astra vs Claude Opus 5.5 비교 영상
- **어울리는 경우**: 모델/도구 비교 콘텐츠 / 레퍼런스 이미지 기반 3D 재현 / 로고 애니메이션 리크리에이션
- **잘하는 표현**: 점프 예비동작·착지·고개 돌림 타이밍 재현 / 파스텔 블루 스튜디오 조명과 부드러운 그림자 / 상하 분할 + 소요시간/토큰 표시 비교 레이아웃
- **스타일**: 옅은 라벤더-블루 배경에 검정 세리프 'PIXAR' 레터링과 은색 램프의 3D 렌더. 상단 검은 바에 모델명·시간·토큰 수가 들어간 2단 비교 화면.
- **기술**: Blender, Cycles, Python (build_scene.py)
- **프롬프트 구조**: 레퍼런스 프레임(t_*.png) 기반 재현 지시 + 렌더 사양(1280x720/30fps/Cycles 64spp) + 자체 프리뷰 검수·리포트 요구
- **태그**: Blender, 3D, Pixar, 램프, 리크리에이션, model-comparison, 캐릭터애니메이션, Cycles
- **주의**: 타사 로고(Pixar) 재현이라 그대로 사용 불가; 비교 레이아웃이라 단독 스타일 참고엔 약함

#### [Code-generated animation model comparison](comparison__code-generated-animation-model-comparison__2105756266211729596.md)
`comparison__code-generated-animation-model-comparison__2105756266211729596` · 16:9 · 66s · 조회 31K · 에셋필요 X

- **요약**: Sith vs Jedi 15초 스틱맨 광선검 결투를 여러 모델(GPT 6.1 Sol, GPT 6 Astra, Sonnet 5.5, Opus 5.5)로 만든 비교 영상
- **어울리는 경우**: 모델 비교 콘텐츠 / 액션 스틱맨 애니메이션 / 빠른 템포 숏 액션 시퀀스
- **잘하는 표현**: 광선검 글로우·번개 이펙트 / 실루엣 기반 액션 포즈 / 모델별 비용·소요시간 오버레이 비교
- **스타일**: 어두운 SF 격납고(청록 톤)와 용암 행성(주황·빨강 석양) 배경 위 흰/검은 스틱맨, 파랑·빨강 네온 광선검. 2D 실루엣 + 글로우 중심.
- **기술**: GSAP, HyperFrames, Skia, FFmpeg
- **프롬프트 구조**: 4줄 원라이너(15초, 빠른 템포, 사운드 없음, 16:9) + 외부 파일 복사 금지 조건
- **태그**: 스틱맨, 광선검, 액션, Star-Wars, model-comparison, 글로우, 2D, GSAP
- **주의**: 여러 모델 결과를 이어붙인 비교 영상이라 Opus 결과만 일부 구간; Star Wars IP 소재

#### [AI edit vs human edit comparison](comparison__ai-edit-vs-human-edit-comparison__2103591152847118409.md)
`comparison__ai-edit-vs-human-edit-comparison__2103591152847118409` · 1:1 (720x720, 세로 영상 2개 병렬) · 20s · 조회 25K · 에셋필요 O

- **요약**: 같은 토킹헤드 원본을 사람(VEED, 10분)과 Opus 5.5+Open Edit(42분)이 편집한 결과를 나란히 비교
- **어울리는 경우**: 토킹헤드 숏폼 자동 편집 참고 / 자막 스타일(키네틱 캡션) 비교 / AI 편집 워크플로 데모
- **잘하는 표현**: 무음·필러 제거 후 빠른 컷 리듬 / 굵은 노랑 대문자 자막과 'NOW.' 별모양 스티커 그래픽 / 말 내용에 맞춘 캡션 강조
- **스타일**: 실사 셀피 토킹헤드(밝은 셔츠 남성, 거리·실내)에 노랑 굵은 산세리프 자막, 빨강 자막(사람 편집), 노랑 버스트 스티커. 검은 배경 위 세로 영상 2개가 라벨과 함께 나란히 놓인 구성.
- **기술**: Open Edit
- **프롬프트 구조**: 툴 지정 + 편집 지시 한 문장(무음/필러 제거, 레퍼런스 스타일 자막, 그래픽·음악)의 짧은 원라이너
- **태그**: 토킹헤드, 자막, 캡션, 숏폼, 자동편집, 비교영상, social, jump-cut
- **주의**: 원본 영상과 자막 레퍼런스가 필요. 비교 포맷이라 프레임 절반은 사람 편집본

#### [Cartoon-style 3D planet in Three.js](comparison__cartoon-style-3d-planet-in-three-js__2102481848911679989.md)
`comparison__cartoon-style-3d-planet-in-three-js__2102481848911679989` · 16:9 · 48s · 조회 22K · 에셋필요 X

- **요약**: Three.js로 만든 만화풍 소형 행성 'PLANET POP!': 궤도 회전, 비행기·자동차 탑승 시점 전환 데모
- **어울리는 경우**: 인터랙티브 3D 데모 홍보 / 귀여운 월드 소개/앱 티저 / 3D 모델 능력 비교
- **잘하는 표현**: 작은 구체 행성 위 도로·도시·구름 배치 / Orbit/비행기/자동차 카메라 모드 전환 / 툰 셰이딩 + 굵은 코믹 UI
- **스타일**: 보라색 우주 배경, 채도 높은 초록·파랑 툰 셰이딩 행성, 뭉게구름과 노란 차량. 좌상단 노랑 코믹 폰트 타이틀과 흰 말풍선형 안내 박스, 하단 알약 버튼 UI.
- **기술**: Three.js
- **프롬프트 구조**: 요구 요소(구름·산·건물·차·비행기, 오비트/줌)를 나열한 짧은 단문
- **태그**: Three.js, 3D, 카툰, toon-shading, planet, 인터랙티브, 귀여움, low-poly
- **주의**: 카테고리는 comparison이지만 영상은 단일 결과 데모; 인터랙티브 화면 녹화

#### [Voxel Japanese garden in Three.js](comparison__voxel-japanese-garden-in-three-js__2105955048018588084.md)
`comparison__voxel-japanese-garden-in-three-js__2105955048018588084` · 약 2.24:1 (1610x720, 비교용 와이드) · 64s · 조회 18K · 에셋필요 X

- **요약**: Three.js 복셀 일본 정원(탑·용·주민)을 Fable 5.5와 Opus 5.5가 만든 결과 교차 비교
- **어울리는 경우**: 모델 비교 콘텐츠 / 복셀/마인크래프트풍 3D 쇼케이스 / 인터랙티브 3D 웹 데모 홍보
- **잘하는 표현**: 탑을 감싸 나는 용 애니메이션 / 궤도 카메라로 보여주는 떠 있는 섬 디오라마 / 낮/밤·불꽃놀이 등 인터랙션 상태 변화
- **스타일**: 복셀 3D: 붉은·검은 다층 탑, 청록 용, 초록 이끼와 회색 돌정원. 흰 안개 하늘의 낮 장면과 남색 밤하늘 불꽃 장면이 교차하고 하단에 모델명 라벨 바.
- **기술**: Three.js, Claude Code
- **프롬프트 구조**: 요소만 나열한 한 문장 원라이너(탑, 주민, 용, 인터랙티브 디테일)
- **태그**: 복셀, voxel, Three.js, 일본정원, 용, 3D, 비교영상, interactive
- **주의**: 비교 영상이고 화면 하단 라벨 바가 큼. 짧은 프롬프트라 재현성은 모델 역량에 의존

#### [Pirate ship 3D scene comparison](comparison__pirate-ship-3d-scene-comparison__2102533729746882985.md)
`comparison__pirate-ship-3d-scene-comparison__2102533729746882985` · 약 2.37:1 (1706x720, 비교용 와이드) · 22s · 조회 15K · 에셋필요 X

- **요약**: 석양 바다를 항해하는 해적선 3D 씬을 ChatGPT-6 Astra와 Claude Opus 5.5가 각각 만든 결과 교차 비교
- **어울리는 경우**: 모델/툴 성능 비교 콘텐츠 / 시네마틱 3D 바다·선박 씬 참고 / 텍스트 없는 배경 루프 영상
- **잘하는 표현**: 바다 물결·항적(wake)·거품 표현 / 석양 역광과 수면 반사 색보정 / 배를 따라가는 카메라 무빙
- **스타일**: 스타일라이즈드 3D: Astra는 주황 노을+청록 바다, Opus는 보라·자주 하늘+짙은 남색 바다에 금빛 돛. 두 결과가 좌우로 번갈아 배치된 분할 화면.
- **기술**: 브라우저 단일 HTML 3D(구체 라이브러리 미지정)
- **프롬프트 구조**: 한 문단의 장문 요구사항: 품질 지향 서술 + 필수 조건(텍스트 금지, 단일 파일) + 브라우저 테스트·스크린샷·콘솔 확인 자체 검수 지시
- **태그**: 비교영상, 3D, 해적선, 바다, 석양, 시네마틱, WebGL, comparison
- **주의**: 두 모델 결과를 섞은 비교 영상이라 단독 스타일 참고엔 Opus 칸만 골라 봐야 함

#### [Jelly world Arctic island: Opus vs Astra](comparison__jelly-world-arctic-island-opus-vs-astra__2107455583129313304.md)
`comparison__jelly-world-arctic-island-opus-vs-astra__2107455583129313304` · 약 4:5 (720x910) · 18s · 조회 14K · 에셋필요 X

- **요약**: 젤리 받침 위 북극 섬 디오라마(이글루·고래·물개·카약, 물 시뮬레이션)를 Opus 5.5와 ChatGPT-6 Astra가 만든 비교
- **어울리는 경우**: 모델 비교 콘텐츠 / 인터랙티브 3D 디오라마/미니어처 쇼케이스 / 물 시뮬레이션 기술 데모
- **잘하는 표현**: 높이장 물 시뮬레이션의 파동·굴절 단면 / 날씨 모드(낮/눈/오로라 밤) 전환 / 에디토리얼 UI와 3D 오브젝트 결합
- **스타일**: 밝은 회백색 배경에 파란 투명 바다 블록과 연보라 젤리 받침, 흰 눈섬·이글루·빨간 깃발. Opus는 선명한 파랑 블록, Astra는 더 투명하고 얼음결 많은 표현. 오로라 밤 모드는 초록 커튼 하늘. 'Frostbay.' 이탤릭 세리프 타이틀.
- **기술**: WebGPU, WGSL, 단일 HTML(라이브러리 없음)
- **프롬프트 구조**: SCENE/WATER/LIFE/LOOK/UI 섹션별 초상세 스펙 + 물리 방정식·격자 해상도 수치 + 테스트 항목 목록
- **태그**: 디오라마, WebGPU, 물시뮬, 북극, 젤리, 에디토리얼UI, 비교영상, 3D
- **주의**: 비교 영상이며 비용 라벨 오버레이 포함. 결과물은 웹앱 녹화라 영상용 연출은 약함

#### [Jelly pufferfish browser comparison](comparison__jelly-pufferfish-browser-comparison__2105957241148813340.md)
`comparison__jelly-pufferfish-browser-comparison__2105957241148813340` · 약 3:4 (720x930) · 18s · 조회 11K · 에셋필요 X

- **요약**: 탭하면 부풀어 가시가 솟는 three.js 젤리 복어(Fugu Jelly)를 Claude Opus 5.5와 Sonnet 5.5 결과로 비교한 영상
- **어울리는 경우**: 캐릭터 상태 변화(평상시→부풀기) 데모 / 모델 비교 숏폼 / 귀여운 3D 토이·굿즈 티저
- **잘하는 표현**: 팽창·가시 돌출의 상태 전환 애니메이션 / 반투명 캔디 재질과 컬러 그림자 / 맛 프리셋별 배경·색 전환
- **스타일**: 세이지 그린·크림·하늘색·핑크 파스텔 단색 배경에 노랑·파랑·초록·핑크 젤리 복어, 큰 눈의 귀여운 캐릭터와 색이 비치는 그림자. 이탤릭 세리프 타이틀의 에디토리얼 레이아웃.
- **기술**: Three.js, WebAudio, XPBD 소프트바디, MeshPhysicalMaterial
- **프롬프트 구조**: 한 문단씩 물리 모델(XPBD 파라미터)·행동 시나리오·디테일·룩·UI를 압축 서술한 중간 길이 스펙
- **태그**: 젤리, pufferfish, soft-body, Three.js, 비교영상, 파스텔, 귀여움, 3D
- **주의**: 모델명·비용 라벨이 붙은 비교 영상. Sonnet 쪽은 배경색이 프리셋마다 바뀌는 등 두 결과의 룩이 다름

#### [Plush spider physics comparison](comparison__plush-spider-physics-comparison__2107127712871505976.md)
`comparison__plush-spider-physics-comparison__2107127712871505976` · 720x910 (비교 레이아웃) · 18s · 조회 10K · 에셋필요 X

- **요약**: WebGPU로 만든 털실 인형 거미 'Plush Spider' 소프트바디·셸 퍼 시뮬레이션, Opus 5.5 vs GPT-6 Astra 비교
- **어울리는 경우**: 물리/렌더링 기술 쇼케이스 / 인터랙티브 토이 데모 / 모델 비교 콘텐츠
- **잘하는 표현**: XPBD 소프트바디 + 로드 체인 다리 물리 / 셸 퍼(털) 렌더링과 벨벳 광택 / 걷기·공처럼 말기·실에 매달리기 행동 / 에디토리얼 세리프 마스트헤드 + 사이드 패널 UI
- **스타일**: 밝은 회백색 스튜디오 바닥 위에 주황·보라·초록 줄무늬 털 인형 거미가 놓인 따뜻하고 귀여운 3D. 좌상단 이탤릭 세리프 'Plush Spider.' 타이틀과 우측 컨트롤 패널이 있는 에디토리얼 레이아웃, 모델명·비용 비교 그리드.
- **기술**: WebGPU, WGSL, HTML 단일 파일
- **프롬프트 구조**: 시리즈형(Material Studies No.015) 장문 스펙: 형상(SDF) → 물리(XPBD 파라미터) → 행동 → 렌더링 기법 → UI 도구·버튼·팔레트를 불릿 계층으로 지정
- **태그**: WebGPU, soft-body, fur, XPBD, 인형, 귀여움, model-comparison, 에디토리얼UI
- **주의**: 비교 그리드 영상; 고급 그래픽 용어 의존이 커서 일반 영상 레퍼런스보단 기술 데모용

#### [Plush dragon physics comparison](comparison__plush-dragon-physics-comparison__2107020311380033949.md)
`comparison__plush-dragon-physics-comparison__2107020311380033949` · 약 4:5 (720x914, 4x3 비교 그리드) · 18s · 조회 10K · 에셋필요 X

- **요약**: WebGPU로 만든 털 질감 봉제 아기 용 소프트바디 인터랙티브를 Claude Opus 5.5와 GPT-6.1 Sol 결과로 비교한 화면 녹화
- **어울리는 경우**: 캐릭터 토이/굿즈 쇼케이스 / 물리·털 렌더링 기술 데모 / 모델 비교 콘텐츠 / 에디토리얼 시리즈형 인터랙티브 소개
- **잘하는 표현**: 셸 퍼(fur) 렌더와 민키 원단 질감 / 날개 천 시뮬레이션과 날갯짓 호버 / Mint/Ember/Dusk 팔레트 전환 / 세리프 마스트헤드 + 사이드 패널 에디토리얼 레이아웃 일관성
- **스타일**: 밝은 회백색 스튜디오 바닥에 파스텔(민트, 라벤더, 코랄) 봉제 용이 앉아 있는 귀여운 3D. 좌상단 이탤릭 세리프 타이틀과 우측 컨트롤 패널의 여백 많은 미니멀 에디토리얼 UI.
- **기술**: WebGPU, WGSL, XPBD 소프트바디/천 시뮬, SDF, 셸 퍼 렌더링, 단일 HTML
- **프롬프트 구조**: 시리즈 스타일 지정 + 스페시먼 형태 / Physics / Rendering / Interaction 섹션의 고밀도 기술 사양(알고리즘명까지 명시)
- **태그**: WebGPU, 봉제인형, 드래곤, 퍼렌더링, 소프트바디, 파스텔, 비교영상, 캐릭터
- **주의**: 비교 격자 + 비용 라벨이 있어 단독 참고엔 잘라야 한다. 시리즈(Material Studies) 맥락을 전제하는 프롬프트다
