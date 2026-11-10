# Opus 5.5 영상 레퍼런스 메타

출처: jasonzhu.ai/en/prompts/claude-opus-5-5 에서 **Opus 5.5 + Full prompt** 조건으로 고른 **294건** (1차 142건 2026-10-08, 2차 152건 2026-11-10) + yihui-dev/awesome-opus5-5-videos에서 영상까지 받은 **13건** (extra, 2026-10-20). 합계 307건.
새로 올라온 것을 받는 절차(출처·선택 조건·이름 규칙·동기화 기록)는 [_SYNC.md](_SYNC.md).
각 케이스는 `<이름>.mp4`(결과 영상)와 `<이름>.md`(메타 헤더 + 원문 프롬프트)가 같은 이름으로 짝지어져 있다.

**영상과 프롬프트는 저장소에 없다.** 원작자들의 콘텐츠라 재배포하지 않고, 각자 받아서 쓴다:

```bash
python3 video-references/opus-5.5/fetch.py        # cases.txt의 307건을 이 폴더로 다운로드 (약 2.5GB, 이미 있는 파일은 건너뜀. extra 13건은 yt-dlp 필요)
python3 video-references/opus-5.5/fetch.py --new  # 사이트에 새로 올라온 full prompt 사례 확인
python3 video-references/opus-5.5/fetch.py --sync # 그것들을 cases.txt에 넣고 받기 (이후 카탈로그 작성은 _SYNC.md)
```

원본 사이트 데이터나 X 영상이 내려가면 그 케이스는 받아지지 않는다(스크립트가 실패 목록을 출력).

이름 규칙: `<category>__<제목-slug>__<X 게시물 id>`
category: comparison 92 · art3d 52 · motion 49 · stories 23 · game 22 · education 20 · product 19 · production 17 (+ extra 13)

---

## 0. 영상 생성 시 이 파일 쓰는 법

1. 만들려는 영상의 **용도**를 1장에서 찾는다 → 후보 2~4개.
2. 원하는 **룩**을 2장 스타일 계열에서 확인해 후보를 좁힌다.
3. 후보의 `.md`에서 **프롬프트 구조**를 가져오고(3장 패턴 참고), `.mp4`는 시각 레퍼런스로 같이 넘긴다.
4. 4장 주의사항에 걸리는 케이스(비교 영상, 화면 녹화, IP, 외부 에셋 의존)는 **프롬프트 구조만** 빌리고 룩은 다른 레퍼런스로 보완한다.
5. 세부 정보는 맨 아래 5장 전체 카탈로그(케이스별 요약·어울리는 경우·잘하는 표현·스타일·기술·태그)를 검색한다.

**가장 재사용 가치가 높은 3가지 (먼저 볼 것)**
- **seek(t) 단일 HTML 모션 템플릿**: [code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2103273003555402193.md) (조회 100만+), [orange-dot-motion-design-system](motion__orange-dot-motion-design-system__2107121188027707651.md), [beat-synced-showreel-from-real-clips](motion__beat-synced-showreel-from-real-clips__2102554209166000267.md), [apple-style-product-launch-video](product__apple-style-product-launch-video__2103835273813496100.md). 결정론적 프레임 렌더 + Playwright + ffmpeg 파이프라인이라 그대로 자동화에 붙이기 좋다.
- **토킹헤드 + 비주얼 삽입 (이 프로젝트와 직결)**: [talking-head-video-edited-into-a-motion-graphics-cut](production__talking-head-video-edited-into-a-motion-graphics-cut__2109454493415023080.md) (얼굴 추적 카메라 카드 + 단어 타이밍 목록·숫자·도표, Remotion), [talking-head-video-converted-to-line-art-b-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md) (원형 PIP + 선화 B-roll), [ai-video-editing-workflow-comparison](comparison__ai-video-editing-workflow-comparison__2105682280765350117.md) (말→인포그래픽), [ai-edit-vs-human-edit-comparison](comparison__ai-edit-vs-human-edit-comparison__2103591152847118409.md) (키네틱 자막).
- **설명형 다크 다큐 (Remotion)**: [history-of-ai-documentary-short-film](education__history-of-ai-documentary-short-film__2102844654169575547.md) (AI 역사, 단일 앰버 강조색), [zoom-journey-from-a-cell-to-quantum-fields](education__zoom-journey-from-a-cell-to-quantum-fields__2103099756167991347.md) (스케일 줌 과학 강의).

---

## 1. 용도별 추천

| 용도 | 1순위 | 다음 후보 |
|---|---|---|
| 강의·개념 설명 (다크, 차분) | [history-of-ai-documentary-short-film](education__history-of-ai-documentary-short-film__2102844654169575547.md) | [zoom-journey-from-a-cell-to-quantum-fields](education__zoom-journey-from-a-cell-to-quantum-fields__2103099756167991347.md), [how-a-language-model-answers-a-prompt-20-second-motion-graph](comparison__how-a-language-model-answers-a-prompt-20-second-motion-graph__2102724864205566388.md), [history-of-indonesia-animated-documentary](education__history-of-indonesia-animated-documentary__2103511590884815282.md) |
| 강의·개념 설명 (종이/손그림, 따뜻함) | [animated-cycloid-lesson](education__animated-cycloid-lesson__2106052083040256293.md) | [talking-head-video-converted-to-line-art-b-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md), [zero-shot-documentary-on-jewish-history](education__zero-shot-documentary-on-jewish-history__2103564391170089429.md), [doc-to-video-explainer-open-alignment](education__doc-to-video-explainer-open-alignment__2103545533474206118.md), [menu-scanning-taste-matching-app-demo](product__menu-scanning-taste-matching-app-demo__2112191630266761382.md) |
| 토킹헤드 편집 + 그래픽 삽입 | [talking-head-video-edited-into-a-motion-graphics-cut](production__talking-head-video-edited-into-a-motion-graphics-cut__2109454493415023080.md) | [talking-head-video-converted-to-line-art-b-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md), [automated-branded-video-edit-with-voice-sync](production__automated-branded-video-edit-with-voice-sync__2110019799342260630.md), [common-video-editing-effects-showcase](production__common-video-editing-effects-showcase__2111678979413598560.md), [ai-video-editing-workflow-comparison](comparison__ai-video-editing-workflow-comparison__2105682280765350117.md), [ai-edit-vs-human-edit-comparison](comparison__ai-edit-vs-human-edit-comparison__2103591152847118409.md), [ai-edited-travel-vlog](production__ai-edited-travel-vlog__2106091485125091695.md) |
| SaaS/앱 제품 소개 (15~40초) | [reusable-prompt-template-for-a-product-motion-video](motion__reusable-prompt-template-for-a-product-motion-video__2103723183899852885.md) | [typingmind-product-intro-motion-video](motion__typingmind-product-intro-motion-video__2103703135902740699.md), [professional-30-second-product-showreel](motion__professional-30-second-product-showreel__2103845264649761062.md), [distilbook-motion-graphics-showreel](motion__distilbook-motion-graphics-showreel__2103469807375208546.md), [one-prompt-saas-launch-video](product__one-prompt-saas-launch-video__2103066071838466494.md), [launch-film-for-a-web-product](product__launch-film-for-a-web-product__2109019765134213540.md) |
| Apple 키노트풍 런칭 필름 | [apple-style-product-launch-video](product__apple-style-product-launch-video__2103835273813496100.md) | [apple-keynote-style-launch-film](motion__apple-keynote-style-launch-film__2107123710251434330.md), [looping-product-launch-motion-template](motion__looping-product-launch-motion-template__2105927781678747965.md), [apple-liquid-glass-style-ui-motion-showcase](motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152.md) |
| UI 마이크로 인터랙션 쇼케이스 | [code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2103273003555402193.md) | [code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2106396375269134597.md), [apple-liquid-glass-style-ui-motion-showcase](motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152.md), [animated-welcome-screen-for-the-nova-crypto-wallet](comparison__animated-welcome-screen-for-the-nova-crypto-wallet__2102681647720395115.md), [code-based-ui-motion-design-loop](motion__code-based-ui-motion-design-loop__2111814234090693110.md) |
| 브랜드 쇼릴·인트로·범퍼 (15초) | [orange-dot-motion-design-system](motion__orange-dot-motion-design-system__2107121188027707651.md) | [20-second-kinetic-identity-bumper-for-techhalla](motion__20-second-kinetic-identity-bumper-for-techhalla__2103411244468498547.md), [15-second-motion-graphics-showcase](motion__15-second-motion-graphics-showcase__2106376222309761094.md), [15-second-motion-design-showreel-detailed-prompt](motion__15-second-motion-design-showreel-detailed-prompt__2103424524297420829.md), [high-energy-motion-graphics-showreel](motion__high-energy-motion-graphics-showreel__2103817034618339682.md) |
| 실사 클립 비트싱크 광고 | [beat-synced-showreel-from-real-clips](motion__beat-synced-showreel-from-real-clips__2102554209166000267.md) | [fast-paced-brand-advertisement](product__fast-paced-brand-advertisement__2106101651010449796.md) |
| 세로 숏폼 (9:16) | [reels-made-with-opus-5-5](motion__reels-made-with-opus-5-5__2105283486487896448.md) | [talking-head-video-converted-to-line-art-b-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md), [ai-video-editing-workflow-comparison](comparison__ai-video-editing-workflow-comparison__2105682280765350117.md), [chaotic-brain-rot-style-motion-video](motion__chaotic-brain-rot-style-motion-video__2103664956482941143.md), [fast-paced-brand-advertisement](product__fast-paced-brand-advertisement__2106101651010449796.md) |
| 역사·연대기 다큐 | [epic-documentary-history-of-chinese-civilization](education__epic-documentary-history-of-chinese-civilization__2103964025683927166.md) | [history-of-indonesia-animated-documentary](education__history-of-indonesia-animated-documentary__2103511590884815282.md), [zero-shot-documentary-on-jewish-history](education__zero-shot-documentary-on-jewish-history__2103564391170089429.md), [battle-of-austerlitz-procedural-film](stories__battle-of-austerlitz-procedural-film__2103116235009347650.md), [mongol-conquest-data-visualization-comparison](comparison__mongol-conquest-data-visualization-comparison__2102566466121797767.md), [al-capone-documentary-film](education__al-capone-documentary-film__2119350502961889592.md) |
| 과학·스케일 줌 (Powers of Ten) | [zoom-journey-from-a-cell-to-quantum-fields](education__zoom-journey-from-a-cell-to-quantum-fields__2103099756167991347.md) | [zoom-from-room-to-quarks-3d-scene](art3d__zoom-from-room-to-quarks-3d-scene__2103299766473875778.md), [working-computer-built-from-logic-gates-with-os](product__working-computer-built-from-logic-gates-with-os__2104301990985498783.md) |
| 단계형 how-to / 레시피 | [cocktail-recipe-explainer-motion-graphic](motion__cocktail-recipe-explainer-motion-graphic__2102853258582880547.md) | [animated-pelican-explains-a-shell-command](education__animated-pelican-explains-a-shell-command__2103149526244618682.md) |
| 스포츠·규칙 해설 (TV 중계 그래픽) | [explainer-video-of-9-football-rules](education__explainer-video-of-9-football-rules__2105922894924501283.md) | |
| 도면→3D 빌드업 (건축·제조) | [itsukushima-shrine-3d-scene](art3d__itsukushima-shrine-3d-scene__2103737014508216515.md) | [golden-pavilion-cad-to-3d-animation](art3d__golden-pavilion-cad-to-3d-animation__2103243328041132100.md), [underwater-palace-built-in-blender](art3d__underwater-palace-built-in-blender__2103669801554264378.md), [floor-plan-to-3d-interior-design-tool](art3d__floor-plan-to-3d-interior-design-tool__2104520072014508316.md), [blueprint-to-animated-pirate-ship](art3d__blueprint-to-animated-pirate-ship__2109043294911291886.md), [apartment-drafted-in-cad-then-built-in-3d](art3d__apartment-drafted-in-cad-then-built-in-3d__2111880621954081240.md), [fictional-rocket-cad-drawings-and-launch-animation](art3d__fictional-rocket-cad-drawings-and-launch-animation__2109515393220083912.md), [da-vinci-workshop-3d-build-gemini-vs-opus](comparison__da-vinci-workshop-3d-build-gemini-vs-opus__2110121002332295599.md) |
| 제품 소재감·만족감 숏폼 (젤리/물리) | [jelly-watermelon-slicing-simulation](art3d__jelly-watermelon-slicing-simulation__2104285370951012504.md) | [interactive-jelly-press-toy](art3d__interactive-jelly-press-toy__2105285992865272110.md), [interactive-jelly-watermelon-toy](game__interactive-jelly-watermelon-toy__2106056420131029473.md), [watermelon-rubber-band-test-opus-5-5-vs-gpt-6-astra](comparison__watermelon-rubber-band-test-opus-5-5-vs-gpt-6-astra__2104994617573970308.md), [jelly-slice-material-test-comparison](comparison__jelly-slice-material-test-comparison__2109424502237016076.md), [gummy-bear-soft-body-physics-scene](comparison__gummy-bear-soft-body-physics-scene__2110131790136401989.md) |
| 감성 단편·매니페스토 | [the-first-spark-procedural-hand-drawn-short](motion__the-first-spark-procedural-hand-drawn-short__2102910531560731063.md) | [animated-episode-drawn-entirely-in-code](stories__animated-episode-drawn-entirely-in-code__2102879301876031808.md), [ai-self-introduction-song-and-video](stories__ai-self-introduction-song-and-video__2103698854399099057.md), [cinematic-2d-storyboard-short-film-rain-station](stories__cinematic-2d-storyboard-short-film-rain-station__2103757767727255661.md) |
| 캐릭터 단편 애니 | [animated-robot-story-across-12-art-styles](stories__animated-robot-story-across-12-art-styles__2103099194693271874.md) | [oktoberfest-themed-animation](stories__oktoberfest-themed-animation__2102493303388475855.md), [pixar-style-imagined-cartoon-story](stories__pixar-style-imagined-cartoon-story__2102788223835463902.md), [four-minute-2d-animation-made-with-up-to-15-agents](motion__four-minute-2d-animation-made-with-up-to-15-agents__2103135536634630632.md) |
| 뮤직비디오·가사 싱크 | [remake-of-the-claude-pop-music-video](production__remake-of-the-claude-pop-music-video__2102801274173587569.md) | [one-shot-music-video-from-song-and-lyrics](stories__one-shot-music-video-from-song-and-lyrics__2103570879619686717.md), [linear-algebra-fear-music-video](stories__linear-algebra-fear-music-video__2103697580421181894.md), [music-driven-blender-visual-scene](art3d__music-driven-blender-visual-scene__2107696042053431360.md) |
| 루프 배경 (로파이·대기 화면) | [pixel-art-scene-generation](art3d__pixel-art-scene-generation__2102746041250705890.md) | [pixel-character-dodging-meteors-on-a-rainbow-space-track](motion__pixel-character-dodging-meteors-on-a-rainbow-space-track__2102515055116063144.md), [animated-pixel-art-wizard-casting-a-spell](motion__animated-pixel-art-wizard-casting-a-spell__2102476258948927543.md), [infinite-zoom-landscape-loop](motion__infinite-zoom-landscape-loop__2103129343253778767.md) |
| 시네마틱 3D 월드·플라이스루 | [cinematic-3d-world-with-a-free-camera](art3d__cinematic-3d-world-with-a-free-camera__2103194052850241739.md) | [playable-boat-scene-through-japanese-landscapes](art3d__playable-boat-scene-through-japanese-landscapes__2102760783344189761.md), [interactive-3d-dystopian-city-diorama](art3d__interactive-3d-dystopian-city-diorama__2103820733159981151.md), [280-kb-single-file-html-demoscene-intro](art3d__280-kb-single-file-html-demoscene-intro__2102893186330841502.md), [wwii-mountain-fortress-in-a-blizzard-blender-scene](comparison__wwii-mountain-fortress-in-a-blizzard-blender-scene__2113119946599272680.md), [storm-in-a-bottle-blender-comparison](comparison__storm-in-a-bottle-blender-comparison__2112184796419883354.md), [interactive-weather-world-in-a-glass-box](art3d__interactive-weather-world-in-a-glass-box__2108159248148611292.md) |
| 게임 보상·가챠 리빌 | [game-settlement-and-card-draw-animations](game__game-settlement-and-card-draw-animations__2104085484347818226.md) | |
| B2B 운영/공정 설명 (아이소메트릭) | [mining-operations-strategy-game](game__mining-operations-strategy-game__2107022944916709886.md) | |
| 시스템·아키텍처 설명 | [zoomable-app-architecture-canvas](education__zoomable-app-architecture-canvas__2105309987983745060.md) | [working-computer-built-from-logic-gates-with-os](product__working-computer-built-from-logic-gates-with-os__2104301990985498783.md) |
| 작동 원리·내부 구조 (엔진·모터·분해도) | [radial-engine-animation-comparison](comparison__radial-engine-animation-comparison__2116606788241969445.md) | [electric-motor-animation-model-comparison](comparison__electric-motor-animation-model-comparison__2110065587279798719.md), [relaxing-generative-visual-made-with-jig-and-opus-5-5](art3d__relaxing-generative-visual-made-with-jig-and-opus-5-5__2109943963536998694.md), [procedural-robotic-giant-squid-teardown](art3d__procedural-robotic-giant-squid-teardown__2119392067646345249.md), [3d-jet-engine-model-comparison](comparison__3d-jet-engine-model-comparison__2112897791022264814.md), [tesla-roadster-explainer-video](education__tesla-roadster-explainer-video__2111440772998599022.md), [interactive-lamborghini-fl3-tractor-diesel-engine](education__interactive-lamborghini-fl3-tractor-diesel-engine__2112130961714385214.md) |
| 과학 개념·사고실험 (캐릭터·칠판 글자) | [infographic-explainer-animation](education__infographic-explainer-animation__2117602113509294520.md) | [what-if-the-sun-vanished-explainer](education__what-if-the-sun-vanished-explainer__2119489762134295014.md) |
| 논문·수식 해설 | [explainer-video-on-jem-self-supervised-learning-paper](education__explainer-video-on-jem-self-supervised-learning-paper__2114676265093664978.md) | |
| AI·컴퓨터비전 원리 (검출 HUD) | [surveillance-style-subject-analysis-loop](motion__surveillance-style-subject-analysis-loop__2112590477144797190.md) | |
| 로드맵·단계 흐름 (목차·커리큘럼) | [animated-minecraft-treasure-map-graphic](motion__animated-minecraft-treasure-map-graphic__2113248976984068329.md) | [stickman-survival-thriller](stories__stickman-survival-thriller__2115786060231770351.md) (규칙·단계를 긴장감 있게) |
| 작업 과정 STEP 설명 (코드 카드 + 결과) | [rigged-rowing-game-character-from-a-concept-sheet](art3d__rigged-rowing-game-character-from-a-concept-sheet__2117273092284112963.md) | |
| 반복 개선·비포/애프터 | [frost-fortress-fantasy-scene](art3d__frost-fortress-fantasy-scene__2116533061495947270.md) | [voxel-island-on-a-flying-sea-turtle](art3d__voxel-island-on-a-flying-sea-turtle__2116169391301607810.md) |
| 핵심 문장 키네틱 타이포 | [beat-synced-k-pop-motion-graphics-music-video](motion__beat-synced-k-pop-motion-graphics-music-video__2110001964402831512.md) | [automated-branded-video-edit-with-voice-sync](production__automated-branded-video-edit-with-voice-sync__2110019799342260630.md) |
| 실사풍 생성 영상 (외부 모델) | [ai-documentary-about-superintelligence](education__ai-documentary-about-superintelligence__2103304514329854102.md) | [promotional-travel-video-about-poland](product__promotional-travel-video-about-poland__2102728913579327722.md), [ai-pipeline-short-video-with-opus-5-5](production__ai-pipeline-short-video-with-opus-5-5__2105370568178479476.md) |
| 도서·출판 프로모 (빈티지) | [promo-video-for-a-science-based-book](product__promo-video-for-a-science-based-book__2103904736160120935.md) | |
| 채용·회사 소개 + TTS | [opus-5-5-plus-gemini-tts-demo](production__opus-5-5-plus-gemini-tts-demo__2103590367518171295.md) | |

---

## 2. 스타일 계열

**A. 다크 미니멀 + 단일 강조색** — 검정/차콜 배경, 흰 또는 크림 산세리프, 강조색 1개(주황·앰버·코랄). 차분하고 고급스러움. 설명·브랜드·런칭 모두 무난.
[history-of-ai-documentary-short-film](education__history-of-ai-documentary-short-film__2102844654169575547.md), [15-second-motion-design-showreel-detailed-prompt](motion__15-second-motion-design-showreel-detailed-prompt__2103424524297420829.md), [motion-design-and-sound-engineering-demo](motion__motion-design-and-sound-engineering-demo__2103557735086428547.md), [cinematic-product-launch-film](product__cinematic-product-launch-film__2104805179401068964.md), [chaotic-brain-rot-style-motion-video](motion__chaotic-brain-rot-style-motion-video__2103664956482941143.md), [ai-self-introduction-song-and-video](stories__ai-self-introduction-song-and-video__2103698854399099057.md), [radial-engine-animation-comparison](comparison__radial-engine-animation-comparison__2116606788241969445.md), [launch-film-for-a-web-product](product__launch-film-for-a-web-product__2109019765134213540.md), [beat-synced-k-pop-motion-graphics-music-video](motion__beat-synced-k-pop-motion-graphics-music-video__2110001964402831512.md), [talking-head-video-edited-into-a-motion-graphics-cut](production__talking-head-video-edited-into-a-motion-graphics-cut__2109454493415023080.md)

**B. 오프화이트 에디토리얼 / Apple 미니멀** — 웜 화이트 캔버스, 검정 UI·필 버튼, Geist류 산세리프, 여백 많음. UI·제품·런칭.
[code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2103273003555402193.md), [code-based-ui-motion-design-showreel](motion__code-based-ui-motion-design-showreel__2106396375269134597.md), [apple-style-product-launch-video](product__apple-style-product-launch-video__2103835273813496100.md), [apple-keynote-style-launch-film](motion__apple-keynote-style-launch-film__2107123710251434330.md), [professional-30-second-product-showreel](motion__professional-30-second-product-showreel__2103845264649761062.md), [reels-made-with-opus-5-5](motion__reels-made-with-opus-5-5__2105283486487896448.md), [cosmos-motion-piece-via-hyperframes](motion__cosmos-motion-piece-via-hyperframes__2103481296018092204.md), [code-based-ui-motion-design-loop](motion__code-based-ui-motion-design-loop__2111814234090693110.md), [relaxing-generative-visual-made-with-jig-and-opus-5-5](art3d__relaxing-generative-visual-made-with-jig-and-opus-5-5__2109943963536998694.md), [procedural-robotic-giant-squid-teardown](art3d__procedural-robotic-giant-squid-teardown__2119392067646345249.md), [automated-branded-video-edit-with-voice-sync](production__automated-branded-video-edit-with-voice-sync__2110019799342260630.md)

**C. 파스텔 글래스모피즘** — 파스텔 그라디언트 + 반투명 글래스 UI. iOS/macOS 기능 소개.
[apple-liquid-glass-style-ui-motion-showcase](motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152.md), [looping-product-launch-motion-template](motion__looping-product-launch-motion-template__2105927781678747965.md), [animated-welcome-screen-for-the-nova-crypto-wallet](comparison__animated-welcome-screen-for-the-nova-crypto-wallet__2102681647720395115.md) (다크 핀테크 변형)

**D. 다크 테크 / 네온 SaaS** — 남색~검정, 파랑·하늘색 글로우, UI 카드. SaaS·개발자 도구.
[typingmind-product-intro-motion-video](motion__typingmind-product-intro-motion-video__2103703135902740699.md), [one-prompt-motion-graphic-from-codebase](motion__one-prompt-motion-graphic-from-codebase__2105268326381625845.md), [30-second-motion-promo-for-kody](motion__30-second-motion-promo-for-kody__2103638102333858193.md), [ai-generated-animated-video-demo](motion__ai-generated-animated-video-demo__2105279421435572498.md), [how-a-language-model-answers-a-prompt-20-second-motion-graph](comparison__how-a-language-model-answers-a-prompt-20-second-motion-graph__2102724864205566388.md), [surveillance-style-subject-analysis-loop](motion__surveillance-style-subject-analysis-loop__2112590477144797190.md), [electric-motor-animation-model-comparison](comparison__electric-motor-animation-model-comparison__2110065587279798719.md), [explainer-video-on-jem-self-supervised-learning-paper](education__explainer-video-on-jem-self-supervised-learning-paper__2114676265093664978.md), [apartment-drafted-in-cad-then-built-in-3d](art3d__apartment-drafted-in-cad-then-built-in-3d__2111880621954081240.md), [tesla-roadster-explainer-video](education__tesla-roadster-explainer-video__2111440772998599022.md)

**E. 볼드 그래픽 / 스위스·포스터** — 원색 풀스크린 컷, 초굵은 산세리프, 고대비. 범퍼·쇼릴·훅.
[15-second-motion-graphics-showcase](motion__15-second-motion-graphics-showcase__2106376222309761094.md), [20-second-kinetic-identity-bumper-for-techhalla](motion__20-second-kinetic-identity-bumper-for-techhalla__2103411244468498547.md), [high-energy-motion-graphics-showreel](motion__high-energy-motion-graphics-showreel__2103817034618339682.md), [motion-showreel-with-a-fully-code-synthesized-soundtrack](motion__motion-showreel-with-a-fully-code-synthesized-soundtrack__2103538744695693512.md), [orange-dot-motion-design-system](motion__orange-dot-motion-design-system__2107121188027707651.md), [persian-language-motion-graphics-showreel](motion__persian-language-motion-graphics-showreel__2103562127474819150.md), [claude-made-showreel](motion__claude-made-showreel__2116296321313521795.md)

**F. 종이·손그림·잉크** — 크림 종이 질감, 선화/두들/잉크 실루엣, 따뜻함. 교육·감성 단편.
[talking-head-video-converted-to-line-art-b-roll](production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956.md), [animated-cycloid-lesson](education__animated-cycloid-lesson__2106052083040256293.md), [the-first-spark-procedural-hand-drawn-short](motion__the-first-spark-procedural-hand-drawn-short__2102910531560731063.md), [animated-episode-drawn-entirely-in-code](stories__animated-episode-drawn-entirely-in-code__2102879301876031808.md), [distilbook-motion-graphics-showreel](motion__distilbook-motion-graphics-showreel__2103469807375208546.md), [cocktail-recipe-explainer-motion-graphic](motion__cocktail-recipe-explainer-motion-graphic__2102853258582880547.md), [remake-of-the-claude-pop-music-video](production__remake-of-the-claude-pop-music-video__2102801274173587569.md) (리소 프린트풍), [menu-scanning-taste-matching-app-demo](product__menu-scanning-taste-matching-app-demo__2112191630266761382.md), [motion-short-about-task-delegation](motion__motion-short-about-task-delegation__2108199183983497433.md), [paper-collage-momotaro-animation](stories__paper-collage-momotaro-animation__2110931024469540979.md)

**G. 빈티지 양피지 / 세피아 다큐** — 양피지·고서 일러스트, 세리프. 역사·출판.
[zero-shot-documentary-on-jewish-history](education__zero-shot-documentary-on-jewish-history__2103564391170089429.md), [promo-video-for-a-science-based-book](product__promo-video-for-a-science-based-book__2103904736160120935.md), [sand-painting-animation-with-narrated-soundtrack](art3d__sand-painting-animation-with-narrated-soundtrack__2102592355165782312.md), [animated-cycloid-lesson](education__animated-cycloid-lesson__2106052083040256293.md), [animated-minecraft-treasure-map-graphic](motion__animated-minecraft-treasure-map-graphic__2113248976984068329.md), [da-vinci-workshop-3d-build-gemini-vs-opus](comparison__da-vinci-workshop-3d-build-gemini-vs-opus__2110121002332295599.md), [al-capone-documentary-film](education__al-capone-documentary-film__2119350502961889592.md)

**H. 동양 전통 그래픽** — 서예 대자, 붉은 도장, 선지·먹선, 세로쓰기.
[epic-documentary-history-of-chinese-civilization](education__epic-documentary-history-of-chinese-civilization__2103964025683927166.md), [itsukushima-shrine-3d-scene](art3d__itsukushima-shrine-3d-scene__2103737014508216515.md), [golden-pavilion-cad-to-3d-animation](art3d__golden-pavilion-cad-to-3d-animation__2103243328041132100.md), [underwater-palace-built-in-blender](art3d__underwater-palace-built-in-blender__2103669801554264378.md), [paper-collage-momotaro-animation](stories__paper-collage-momotaro-animation__2110931024469540979.md), [japanese-shrine-scene-comparison](comparison__japanese-shrine-scene-comparison__2110014604524896392.md)

**I. 다크 사이언스 / 우주** — 검정 배경 발광 파티클, 반투명 3D 구조, 스케일 눈금 HUD.
[zoom-journey-from-a-cell-to-quantum-fields](education__zoom-journey-from-a-cell-to-quantum-fields__2103099756167991347.md), [live-generative-code-art-from-a-typed-word](art3d__live-generative-code-art-from-a-typed-word__2103837519615774895.md), [280-kb-single-file-html-demoscene-intro](art3d__280-kb-single-file-html-demoscene-intro__2102893186330841502.md), [zoom-from-room-to-quarks-3d-scene](art3d__zoom-from-room-to-quarks-3d-scene__2103299766473875778.md)

**J. 에디토리얼 머티리얼 스터디 (3D 제품샷)** — 크림 스튜디오 + 반투명 젤리/털 + 이탤릭 세리프 타이틀("Melon Jelly."). 소재감·만족감.
[jelly-watermelon-slicing-simulation](art3d__jelly-watermelon-slicing-simulation__2104285370951012504.md), [interactive-jelly-press-toy](art3d__interactive-jelly-press-toy__2105285992865272110.md), [interactive-jelly-watermelon-toy](game__interactive-jelly-watermelon-toy__2106056420131029473.md), [gummy-octopus-physics-comparison](comparison__gummy-octopus-physics-comparison__2104466170275324190.md), [browser-octopus-physics-comparison](comparison__browser-octopus-physics-comparison__2106809017850818679.md), [jelly-slice-material-test-comparison](comparison__jelly-slice-material-test-comparison__2109424502237016076.md), [interactive-jelly-dam-simulation](art3d__interactive-jelly-dam-simulation__2114512807500615723.md), [interactive-lamborghini-fl3-tractor-diesel-engine](education__interactive-lamborghini-fl3-tractor-diesel-engine__2112130961714385214.md), [3d-canal-and-windmill-scene-model-comparison](comparison__3d-canal-and-windmill-scene-model-comparison__2110329593441796383.md)

**K. 시네마틱 3D 환경** — 골든아워·대기원근·볼류메트릭 라이트.
[cinematic-3d-world-with-a-free-camera](art3d__cinematic-3d-world-with-a-free-camera__2103194052850241739.md), [playable-boat-scene-through-japanese-landscapes](art3d__playable-boat-scene-through-japanese-landscapes__2102760783344189761.md), [interactive-3d-dystopian-city-diorama](art3d__interactive-3d-dystopian-city-diorama__2103820733159981151.md) (사이버펑크), [pelican-riding-a-bike-in-three-js](art3d__pelican-riding-a-bike-in-three-js__2102436416437580159.md), [wwii-mountain-fortress-in-a-blizzard-blender-scene](comparison__wwii-mountain-fortress-in-a-blizzard-blender-scene__2113119946599272680.md), [storm-in-a-bottle-blender-comparison](comparison__storm-in-a-bottle-blender-comparison__2112184796419883354.md), [interactive-weather-world-in-a-glass-box](art3d__interactive-weather-world-in-a-glass-box__2108159248148611292.md), [low-poly-japanese-railway-station-diorama](comparison__low-poly-japanese-railway-station-diorama__2111965632338292943.md)

**L. 픽셀아트 / 레트로** — 제한 팔레트 16비트, 루프.
[pixel-art-scene-generation](art3d__pixel-art-scene-generation__2102746041250705890.md), [animated-pixel-art-wizard-casting-a-spell](motion__animated-pixel-art-wizard-casting-a-spell__2102476258948927543.md), [pixel-character-dodging-meteors-on-a-rainbow-space-track](motion__pixel-character-dodging-meteors-on-a-rainbow-space-track__2102515055116063144.md), [90s-style-demoscene-demo-in-c-opengl](art3d__90s-style-demoscene-demo-in-c-opengl__2102919394775220530.md) (90s 데모신), [alien-explores-the-library-of-babel](stories__alien-explores-the-library-of-babel__2103569043836027339.md) (90s 영화 GUI), [pixel-art-baseball-game-comparison](comparison__pixel-art-baseball-game-comparison__2118281844181369210.md), [pixel-art-basketball-court-diorama-with-weather](art3d__pixel-art-basketball-court-diorama-with-weather__2112989996366102944.md), [pixel-art-floating-island-lido-across-four-models](comparison__pixel-art-floating-island-lido-across-four-models__2115595806665240630.md)

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

- **비교 영상 (comparison 92건 대부분)**: 화면이 2~12분할이고 모델명·비용 라벨이 박혀 있다. 룩은 Opus 칸만 보고(2차 수집분은 각 항목 주의에 Opus 칸 위치를 적음), 프롬프트는 그대로 쓸 수 있다.
- **비슷하거나 같은 영상**: 젤리 디오라마·젤리 생물 시리즈(vib3coded)는 수십 건이 거의 같은 룩이라 J 계열 대표 1~2건만 보면 된다. 같은 결과 영상이 두 케이스에 있는 경우: [golden-hour-japanese-temple-3d-scene](art3d__golden-hour-japanese-temple-3d-scene__2110657641831956870.md) = [code-only-three-js-temple-at-dusk](art3d__code-only-three-js-temple-at-dusk__2112545748944556038.md) (앞이 원본), [electric-motor-animation-model-comparison](comparison__electric-motor-animation-model-comparison__2110065587279798719.md) = [electric-motor-3d-animation-comparison](comparison__electric-motor-3d-animation-comparison__2111513156589629941.md) (Opus 칸).
- **Opus 단독 아님**: 메타 models에 fable-5.5 등이 함께 적힌 케이스(2차 수집분 일부)는 결과가 Opus만의 것이 아닐 수 있다. 각 항목 주의 참고.
- **화면 녹화 (게임·인터랙티브·툴)**: 편집된 영상이 아니라 브라우저/앱 녹화. 컷 리듬·전환 레퍼런스로는 약하다 (game 대부분, art3d 일부, [liquid-glass-web-hero-section](product__liquid-glass-web-hero-section__2106061619176620344.md) 는 13분 작업 녹화).
- **외부 에셋 의존 (needs_assets)**: 제품 스크린샷, 음원, 캐릭터 시트, 원본 촬영본이 있어야 재현된다. 각 `.md` 헤더의 `needs reference assets` 확인.
- **외부 생성 모델 의존**: Seedance, Kling, Veo, Runway, fal, GPT Image 등 크레딧 필요 (N 계열).
- **IP·실존 인물**: Pixar, Star Wars, Fortnite, Far Cry, Rocket League, 주술회전, Rick Astley, Notion, Elon Musk 가십 등은 구조만 참고.
- **프롬프트와 결과 불일치**: [chaotic-brain-rot-style-motion-video](motion__chaotic-brain-rot-style-motion-video__2103664956482941143.md) ("카오틱"인데 차분함), [arcane-style-blender-animation](stories__arcane-style-blender-animation__2105315982525014067.md) (Arcane 화풍 재현도 낮음), [3d-character-rig-generated-from-a-psd-file](art3d__3d-character-rig-generated-from-a-psd-file__2102965242439590112.md) (3D 아니고 2D 리그), [apple-liquid-glass-style-ui-motion-showcase](motion__apple-liquid-glass-style-ui-motion-showcase__2103510103622308152.md) (프롬프트 비트맵과 화면 다름), [fortnite-style-game-one-shot-test](game__fortnite-style-game-one-shot-test__2104779190277181699.md) (실제는 Sonnet 결과 + 진짜 Fortnite 화면).
- **해상도**: 원본이 X 업로드본이라 대부분 720p. 화질 기준이 아니라 구성·모션 기준으로 볼 것.

---

## 5. 전체 카탈로그


### motion (모션그래픽) — 49건 (조회수순)


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

#### [Animated pixel art Halloween diorama](motion__animated-pixel-art-halloween-diorama__2116832762912973220.md)
`motion__animated-pixel-art-halloween-diorama__2116832762912973220` · 16:9 · 13s · 조회 116K · 에셋필요 X

- **요약**: 비 내리는 밤, 떠 있는 섬 위 집과 모닥불·창문 불빛이 반짝이는 픽셀아트 할로윈 디오라마를 로파이 음악 커버용 무한 루프로 만든 영상
- **어울리는 경우**: 로파이·공부용 배경 루프 / 강의 인트로·쉬는 시간 대기 화면 / 계절(할로윈·가을) 분위기 전환 컷 / 게임·레트로 주제 챕터 표지
- **잘하는 표현**: 차가운 밤 대 따뜻한 불빛의 색온도 대비 / 비·불꽃 파티클·굴뚝 연기·깜빡이는 조명 같은 앰비언트 이펙트 / 번개 순간 플래시 / 끊김 없는 루프
- **스타일**: 짙은 남보라 밤하늘과 보름달, 구름 아래 떠 있는 섬에 주황 창문빛·모닥불·청록 버섯 발광이 점처럼 박힌 정적인 측면 구도의 픽셀아트. 잔잔하고 아늑한 로파이 무드.
- **기술**: TypeScript, Sprite Fusion API, MCP
- **프롬프트 구조**: 용도(10시간 로파이 커버)·팔레트 원칙(냉온 대비)·넣을 이펙트·해상도와 루프 조건을 한 문단에 담은 짧은 요청
- **태그**: 픽셀아트, pixel-art, 할로윈, 로파이, 루프, 디오라마, 비·파티클, 야경
- **주의**: 카메라가 거의 고정된 앰비언트 루프라 정보 전달용 모션은 거의 없음

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

#### [Drone-style cliff camera work without a drone](motion__drone-style-cliff-camera-work-without-a-drone__2111448458079133856.md)
`motion__drone-style-cliff-camera-work-without-a-drone__2111448458079133856` · 3:4 · 25s · 조회 71K · 에셋필요 O

- **요약**: 패로 제도 절벽에서 달리는 등산객을 쫓다 절벽 아래로 떨어져 협곡·폭포·해식 아치를 관통하는 FPV 드론 시점 실사풍 생성 영상
- **어울리는 경우**: 여행·자연 주제 오프닝 / 속도감·몰입감을 강조하는 전환 컷 / 세로형 숏폼 훅 / "도전·도약" 같은 은유 장면
- **잘하는 표현**: FPV 드론의 급강하·근접 비행 카메라 / 모션블러가 강한 연속 동선 / 폭포 물보라와 무지개 같은 자연광 효과 / 샷 리스트 기반 장면 연결
- **스타일**: 선명한 초록 풀밭, 짙은 바다색 대서양, 검은 현무암 절벽과 역광 햇빛의 실사 항공 촬영 룩. 텍스트 없이 밝고 시원한 시네마틱 다큐 분위기.
- **기술**: Fish Creative MCP(Fish Audio 도구)
- **프롬프트 구조**: 영상 형식(세로·FPV·무자막)과 한 줄짜리 동선 아이디어를 주고, 샷 리스트를 먼저 보여 승인받은 뒤 제작하라는 2단계 요청
- **태그**: FPV, 드론, 실사, 생성영상, 자연, 절벽, 폭포, 세로영상, 시네마틱
- **주의**: 코드 모션그래픽이 아니라 외부 생성 영상 모델 결과물(실사 생성). 인서트 제작 시 재현하려면 영상 생성 API가 필요

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

#### [Anime opening edit of a martial arts clip](motion__anime-opening-edit-of-a-martial-arts-clip__2110119492076404869.md)
`motion__anime-opening-edit-of-a-martial-arts-clip__2110119492076404869` · 16:9 · 32s · 조회 38K · 에셋필요 O

- **요약**: 무술 동작 클립을 불꽃 이펙트·한자 타이틀·분할 컷이 들어간 애니메이션 오프닝처럼 재편집한 영상
- **어울리는 경우**: 시리즈·챕터 오프닝 타이틀 / 강렬한 키워드 등장 컷 / 액션·스포츠 하이라이트 편집 / 캐릭터 소개 인트로
- **잘하는 표현**: 불꽃 궤적 VFX와 컬러 그레이딩 / 대형 한자·영문 타이틀 카드('炎舞', 'IGNITE') / 사선 패널 분할 컷과 만화풍 임팩트 프레임 / 비트 맞춘 다이내믹 컷
- **스타일**: 남색·보라 어두운 배경에 핫핑크·주황 불꽃이 강하게 빛나는 셀 애니메이션 룩, 흰 바탕 핑크 잉크의 만화 임팩트 컷과 세리프·스텐실 혼합 일본어 타이포. 열정적이고 극적인 아니메 OP 무드.
- **기술**: Seedance 2.5
- **프롬프트 구조**: 원본 영상을 주고 '애니 오프닝 스타일'로 그레이딩·컷·트랜지션·VFX·모션그래픽을 더하라는 한 문단 편집 요청
- **태그**: 애니메이션, anime-OP, 무술, 불꽃VFX, 한자타이포, 타이틀시퀀스, 다이내믹컷, 핫핑크
- **주의**: 원본 클립(에셋)과 외부 생성 영상 모델(Seedance) 기반. 순수 코드 모션그래픽이 아님

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

#### [Three poster-grid music video variations](motion__three-poster-grid-music-video-variations__2114167098284839305.md)
`motion__three-poster-grid-music-video-variations__2114167098284839305` · 1:1 · 39s · 조회 32K · 에셋필요 O

- **요약**: 수묵 늑대·검객 애니 영상을 얇은 회색 선 격자 셀로 나눠 셀마다 다른 효과·타이포·아이콘을 비트에 맞춰 터뜨리는 정사각 포스터그리드 뮤직비디오 3종
- **어울리는 경우**: 음악·비트 중심 하이라이트 몽타주 / 한 장면을 여러 버전으로 변주해 보여주는 '스타일 비교' 컷 / 강렬한 챕터 전환 / SNS용 정사각 클립
- **잘하는 표현**: 격자 셀별 독립 처리(하프톤·픽셀화·라인아트·색반전) / 비트 동기 플래시와 연쇄 전파 효과 / 한자 스탬프 타이포('風', '斬', '墨狼')와 HUD 아이콘·바코드·타임코드 / 시간 오프셋·프레임 반복
- **스타일**: 흑백 수묵 톤 화면 위 빨간 강조색과 금색 포인트, 셀마다 번호·라벨·타임코드가 달린 테크 포스터 그리드. 밀도 높고 공격적인 일본풍 그래픽 디자인 무드.
- **기술**: Python, FFmpeg
- **프롬프트 구조**: 같은 골격(1:1·음악 길이 일치·회색 격자·중앙 6셀 동기)을 유지한 채 변주 방식(셀별 처리/연쇄 파동/시간 변주)만 바꾼 프롬프트 3개 묶음
- **태그**: 포스터그리드, 그리드, 뮤직비디오, 비트싱크, 수묵, 한자타이포, 하프톤, 정사각, 글리치
- **주의**: 원본 영상·음악 에셋이 필요. 화면 밀도가 매우 높아 강의 인서트로는 짧게 끊어 써야 함

#### [Beat-synced K-pop motion graphics music video](motion__beat-synced-k-pop-motion-graphics-music-video__2110001964402831512.md)
`motion__beat-synced-k-pop-motion-graphics-music-video__2110001964402831512` · 16:9 · 231s · 조회 31K · 에셋필요 O

- **요약**: AI 시대 '인간 노동자' 주제의 가사를 거대한 볼드 키네틱 타이포와 인사카드·폰 화면·카운트다운 같은 UI 소품, 생성 K팝 아이돌 캐릭터 컷으로 엮은 4분짜리 비트싱크 뮤직비디오
- **어울리는 경우**: 핵심 문장 한 줄을 크게 박는 키네틱 타이포 컷 / AI·일자리·미래 담론 강의의 강조 인서트 / 숫자·카운트다운 강조 / 가사·인용구 리릭 비디오
- **잘하는 표현**: 화면 가득 찬 초대형 콘덴스드 산세리프 키네틱 타이포 / 사원증·SNS 피드·진행바·디지털 시계 등 UI 소품 연출 / 주황 단일 강조색으로 단어 하이라이트 / 세리프 체크박스 같은 정적 대비 컷
- **스타일**: 검정·짙은 회색 배경에 흰색 초대형 볼드 산세리프와 비비드 주황 강조, 경고 테이프 사선·HUD 모노 메타데이터. 다크 미니멀 + 단일 강조색의 긴장감 있는 사이버 무드.
- **프롬프트 구조**: 무드보드·주인공 캐릭터 시트·백업 댄서를 첨부하고 음악 스타일·가사 자리표시자를 붙인 짧은 '전력을 다해 만들어라' 요청
- **태그**: 키네틱타이포, kinetic-type, 뮤직비디오, 비트싱크, K팝, 다크미니멀, 주황강조, UI소품, 리릭비디오
- **주의**: 캐릭터 시트·무드보드·음원 에셋 필요. 실사풍 아이돌 캐릭터 컷은 생성 이미지·립싱크 기반이라 재현 시 외부 생성 모델 필요. 타이포 컷만 참고하면 좋음

#### [Live streaming UI built on generated video](motion__live-streaming-ui-built-on-generated-video__2109915723074097287.md)
`motion__live-streaming-ui-built-on-generated-video__2109915723074097287` · 16:9 · 30s · 조회 29K · 에셋필요 O

- **요약**: 공포풍 인형 같은 스트리머 영상 위에 시청자 수·실시간 채팅·후원 알림·이모지 반응이 계속 갱신되는 라이브 방송 UI를 덧씌운 영상
- **어울리는 경우**: 라이브 방송·스트리머 문화 설명 / 실시간 반응·여론을 보여주는 장면 / 가짜 방송 화면 패러디 / 채팅 댓글을 인용하는 연출
- **잘하는 표현**: 맥락에 맞게 읽히는 실시간 채팅 스크롤 / 올라가는 시청자 수 카운터 / 후원·구독·레이드 알림 토스트 / 떠오르는 이모지 반응
- **스타일**: 어두운 초록 톤 방 안의 실사풍 생성 영상 위에 트위치형 반투명 다크 채팅 패널, 보라·주황·빨강 알림 배지. 점점 기괴해지는 호러 반전 무드.
- **기술**: Seedance 2.5
- **프롬프트 구조**: 원본 영상에 라이브 방송 UI 오버레이(시청자 수·반응·문맥형 채팅·읽히는 텍스트)를 더하라는 한 문단 요청
- **태그**: 라이브스트리밍, UI오버레이, 채팅, 알림, 호러, 패러디, 생성영상, 트위치
- **주의**: 배경 영상은 외부 생성 모델(Seedance) 결과물이고 원본 영상 에셋이 필요. 마지막에 괴물 얼굴로 변하는 호러 연출이 있어 강의용으로는 UI 레이어만 참고할 것

#### [Motion short about task delegation](motion__motion-short-about-task-delegation__2108199183983497433.md)
`motion__motion-short-about-task-delegation__2108199183983497433` · 16:9 · 20s · 조회 26K · 에셋필요 O

- **요약**: 종이비행기 업무 더미에 파묻힌 주황 블록 캐릭터 Opus가 노란 Haiku를 불러 일을 넘기고 해방되는 과정을 수채화 다락방 세계로 그린 20초 런칭 애니메이션
- **어울리는 경우**: 업무 위임·역할 분담 개념 설명 / 제품·모델 출시 소개 단편 / 스토리형 비유 인서트 / 엔드카드에 핵심 수치 한 줄 박기
- **잘하는 표현**: 얼굴 달린 블록 캐릭터의 표정 연기 / 종이 소품(종이비행기·도장·서류)으로 이야기 전달 / 아늑한 방을 세계로 쓰는 스테이징 / 사실 확인된 수치를 도장으로 찍는 엔드카드
- **스타일**: 다락방 나무 벽·칠판·전등의 따뜻한 갈색·남색 수채화 종이 질감, 주황·노랑 블록 캐릭터와 손글씨 느낌 세리프 카드. 손그림 동화 같은 아늑하고 유머러스한 무드.
- **기술**: Remotion, ffmpeg, ElevenLabs, GPT Image, Higgsfield
- **프롬프트 구조**: 아이디어·고정 조건·스타일 레퍼런스·사실 잠금(facts.json)·관객과 훅·도구표·작업 순서·검증 루프·스킬화·승인 게이트로 나눈 장문의 감독 브리프
- **태그**: 캐릭터애니메이션, 수채화, 손그림, 스토리텔링, 업무위임, 런칭필름, Remotion, 종이질감
- **주의**: 캐릭터·배경은 이미지 생성 모델(GPT Image/Higgsfield)로 만든 에셋 기반. Anthropic 모델명이 등장하는 홍보용 단편

#### [Claude-made showreel](motion__claude-made-showreel__2116296321313521795.md)
`motion__claude-made-showreel__2116296321313521795` · 16:9 · 90s · 조회 26K · 에셋필요 X

- **요약**: 'NOISE. ORDER.' 같은 거대 타이포와 1비트 디더링·홀로그램 파스텔 그라데이션·디더 구체로 '0과 1만으로도 감정을 느꼈다'를 말하는 90초 네오브루탈 스위스 에디토리얼 쇼릴
- **어울리는 경우**: 핵심 단어·문장을 크게 박는 타이포 강조 컷 / 디지털·데이터·노이즈 개념 설명 / 큰 숫자 하나를 보여주는 통계 컷 / 강의·채널 브랜딩 인트로
- **잘하는 표현**: 초대형 울트라볼드 그로테스크 타이포와 디더 텍스처 채움 / 1비트 비트맵 디더링·체커 그리드 전환 / 무지갯빛 파스텔 그라데이션 블롭 / 모노스페이스 메타데이터와 모듈 그리드 가이드선
- **스타일**: 오프화이트 배경에 검정 초대형 산세리프, 얇은 모듈 그리드와 모노 메타 텍스트, 사이사이 홀로그램 파스텔 그라데이션과 하프톤 디더 구체. 정돈되고 감성적인 Y2K 스위스 에디토리얼.
- **프롬프트 구조**: '꿈의 직장에 보낼 쇼릴'이라는 목표와 긴 스타일 키워드 나열(네오브루탈 스위스·디더링·Y2K)·사운드 조건·출력 사양을 한 문단에 담은 요청
- **태그**: 스위스타이포, 네오브루탈, 디더링, dithering, Y2K, 키네틱타이포, 오프화이트, 그라데이션, 쇼릴
- **주의**: 90초 쇼릴이라 여러 장면이 이어짐. 인서트 참고 시 원하는 장면(타이포·숫자·구체) 하나만 골라 볼 것

#### [15-Second Motion Graphics Showcase](motion__15-second-motion-graphics-showcase__2106376222309761094.md)
`motion__15-second-motion-graphics-showcase__2106376222309761094` · 16:9 · 15s · 조회 25K · 에셋필요 X

- **요약**: 'MOTION' 타이틀로 시작해 리듬·타입·타이밍·안무 챕터를 거쳐 'CLAUDE.'로 끝나는 15초 모션그래픽 쇼릴
- **어울리는 경우**: 모션 디자이너 포트폴리오 릴 / 브랜드 아이덴티티 티저 / 챕터형 짧은 오프닝 타이틀
- **잘하는 표현**: 대형 볼드 산세리프와 도형(빨간 원)을 결합한 키네틱 타이포 / 챕터 번호·진행 바 HUD로 구조화된 리듬 / 3D 젤리 구체·구슬 체인 등 2D/3D 혼합 오브젝트 / 강한 원색 배경 컷 전환
- **스타일**: 검정·빨강·코발트 블루·크림 단색 배경을 교차하는 스위스/바우하우스풍 볼드 그래픽. 크림색 굵은 산세리프, 빨강 원 포인트, 광택 3D 빨강 구체와 빨강·파랑·흰 구슬 체인, 상하단 작은 라벨 HUD.
- **프롬프트 구조**: 중국어로 된 '15초 쇼릴, 도구 자유, 대담한 아트 디렉션으로 전력' 짧은 자율 위임형 프롬프트
- **태그**: 쇼릴, 키네틱타이포, 볼드, 원색, 스위스스타일, 3D, motion-reel, 챕터
- **주의**: 프롬프트에 도구·스타일 지시가 없어 재현성 낮음. 사용 도구 미상

#### [Surveillance-style subject analysis loop](motion__surveillance-style-subject-analysis-loop__2112590477144797190.md)
`motion__surveillance-style-subject-analysis-loop__2112590477144797190` · 약 1:2.00 (720x1440) · 15s · 조회 23K · 에셋필요 O

- **요약**: 인물 일러스트 한 장을 CCTV 포착→실루엣 검출→와이어프레임·포즈 골격→특징 콜아웃→색상 팔레트 추출→타깃 고정 순으로 분석하는 감시카메라 HUD 루프
- **어울리는 경우**: 컴퓨터 비전·AI 인식 원리 설명 / 이미지 한 장을 단계별로 분석하는 연출 / 인물·캐릭터 소개 카드 / 색 팔레트·디자인 분석 콘텐츠
- **잘하는 표현**: 검출 박스와 신뢰도 점수 / 에지·삼각 메시 와이어프레임과 포즈 스켈레톤 / 타이핑되는 라벨 콜아웃 / k-means 색상 스와치 패널과 단계 진행 패널
- **스타일**: 탈색된 CCTV 화면과 검은 그리드 배경, 흰 모노스페이스 HUD에 금빛 노랑 단일 강조색, 마지막은 RGB 글리치. 차갑고 분석적인 감시·테크 무드.
- **프롬프트 구조**: 15초 루프를 ACQUIRE~IDENTIFY 6단계로 나눠 단계별 화면을 지정하고, 원본 보존·HUD 규칙·출력 형식을 덧붙인 번호 목록형 스펙
- **태그**: HUD, 감시카메라, CCTV, 컴퓨터비전, 와이어프레임, 포즈추정, 색상팔레트, 세로영상, 루프
- **주의**: 입력 이미지가 필요하며 예시 인물은 스타워즈풍 캐릭터(라이트세이버) 팬아트라 IP 주의. 세로 1:2 비율

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

#### [Liquid chrome motion showreel](motion__liquid-chrome-motion-showreel__2116612471880610054.md)
`motion__liquid-chrome-motion-showreel__2116612471880610054` · 16:9 · 90s · 조회 17K · 에셋필요 X

- **요약**: 검은 공간에 액체 크롬·무지갯빛 유막 반사의 구체·토러스·블롭과 'LIQUID', 'LIGHT', 'FEEL' 크롬 타이포가 떠오르는 90초 Y3K 쇼릴
- **어울리는 경우**: 프리미엄 제품·기술 티저 / 고급스러운 키워드 타이틀 컷 / 분자·네트워크 구조 은유(구체 군집) / 강의 오프닝 브랜딩
- **잘하는 표현**: 크롬·수은 재질과 무지갯빛 오일 반사 / 부풀린 3D 블롭 타이포와 녹아내리는 변형 / 극단적 여백 속 하나의 오브젝트 / 얇은 HUD 메타데이터 오버레이
- **스타일**: 깊은 검정 배경에 은색 크롬과 초록·보라·분홍 무지갯빛 반사가 도는 3D 오브젝트, 얇은 모노스페이스 HUD 텍스트. 넓은 여백의 고요하고 고급스러운 제품 렌더 무드.
- **프롬프트 구조**: 'Claude-made showreel'과 같은 쇼릴 템플릿에 스타일 키워드(Y3K 액체 크롬·HDR)와 사운드 목록·HDR 출력 사양만 바꿔 넣은 한 문단 요청
- **태그**: 크롬, liquid-chrome, Y3K, 3D, 무지갯빛, 다크, 블롭타이포, 쇼릴, 제품렌더
- **주의**: 화면이 매우 어두워 일반 SDR 재생에서는 오브젝트가 작고 흐리게 보일 수 있음. 90초 쇼릴이라 장면 하나만 골라 참고할 것

#### [Animated Minecraft treasure map graphic](motion__animated-minecraft-treasure-map-graphic__2113248976984068329.md)
`motion__animated-minecraft-treasure-map-graphic__2113248976984068329` · 16:9 · 19s · 조회 15K · 에셋필요 O

- **요약**: 양피지 지도가 화면 위로 들려 올라와 마인크래프트 섬 지도가 드러나고, 1번 장소부터 금빛으로 빛나는 보물 지점까지 경로가 그려지는 애니메이션 지도 그래픽
- **어울리는 경우**: 강의 커리큘럼·로드맵 단계 안내 / 여정·순서 흐름 설명 / 게임·모험 주제 영상의 목차 / 최종 목표 지점 강조
- **잘하는 표현**: 지도 등장(들어 올림·서서히 드러남) 연출 / 점선 경로가 장소를 순서대로 잇는 애니메이션 / 마지막 장소 금빛 글로우와 카메라 줌·흔들림 임팩트 / 핀 라벨 팝인
- **스타일**: 어두운 나무 배경 위 오래된 양피지 테두리, 안쪽은 파란 바다와 초록·회색 블록 지형의 마인크래프트 지도, 빨간 번호 핀과 노란 픽셀 폰트 라벨. 따뜻하고 모험적인 게임 무드.
- **프롬프트 구조**: 참고 이미지 4장을 주고 등장 방식·경로 순서·마지막 장소 강조·VFX·카메라 연출을 차례로 지시한 한 문단 요청
- **태그**: 지도, 보물지도, 경로애니메이션, 로드맵, 마인크래프트, 양피지, 게임, 픽셀
- **주의**: 참고 이미지 4장 필요. 마인크래프트 IP 화풍이라 그대로 쓰기보다 '지도+경로' 연출만 차용할 것

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

#### [Code-based UI motion design loop](motion__code-based-ui-motion-design-loop__2111814234090693110.md)
`motion__code-based-ui-motion-design-loop__2111814234090693110` · 1:1 · 14s · 조회 14K · 에셋필요 X

- **요약**: 버튼 하나가 로더→뮤직 플레이어→볼륨 슬라이더→토글→탭→차트→⌘K 검색→토스트로 끊김 없이 모핑되며 커서가 직접 조작하는 120BPM 비트싱크 UI 모션 루프
- **어울리는 경우**: 앱·서비스 기능 소개 / UI·UX 디자인 강의의 인터랙션 예시 / 하나의 개념이 여러 형태로 변하는 은유 / 깔끔한 제품 데모 인서트
- **잘하는 표현**: 하나의 요소가 크기·라운드·색을 바꾸는 연속 모핑 / 미세 오버슈트 스프링 이징 / 커서 클릭·드래그 직접 조작과 숫자 카운트업·차트 드로잉 / 서브프레임 모션블러와 완벽 루프
- **스타일**: 밝은 웜그레이 배경에 검정·흰색 UI 컴포넌트와 Geist 산세리프, 앨범아트에만 주황·보라 그라데이션. 군더더기 없는 Apple/Dribbble풍 미니멀.
- **기술**: Playwright, ffmpeg, NumPy, 단일 HTML 파일(seek(t) 시간 함수 렌더)
- **프롬프트 구조**: inputs·direction·structure·build·gotchas·start 태그로 나눠 상태 시퀀스·금지 사항·결정적 렌더 방식·함정까지 명시한 XML 태그형 스펙
- **태그**: UI모션, 모핑, 스프링, micro-interaction, 미니멀, 오프화이트, 루프, Playwright, 비트싱크
- **주의**: 프롬프트는 BPM 120 음원 등 입력을 먼저 물어보게 되어 있음(음원은 사용자 제공)

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

### product (제품 프로모) — 19건 (조회수순)


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

#### [Cross-platform disk cleanup app](product__cross-platform-disk-cleanup-app__2115870373300326503.md)
`product__cross-platform-disk-cleanup-app__2115870373300326503` · 16:9 · 35s · 조회 171K · 에셋필요 O

- **요약**: Claude Code로 만든 맥·윈도우 디스크 정리 앱 'Cleanly'가 실제 모니터와 노트북에서 돌아가는 모습을 휴대폰으로 찍어 화면을 넘겨 보여 주는 영상
- **어울리는 경우**: "AI로 데스크톱 앱을 끝까지 만들었다" 사례 소개 / 앱 개발 과정 강의의 결과물 시연 컷 / 글래스 대시보드 UI 레퍼런스
- **잘하는 표현**: 큰 숫자 하나를 중심에 둔 홈 대시보드(229 MB, 15.7 GB) / 빨강·초록·파랑·청록 그라데이션 라이브 카드 4개 / 버블 공간 지도·목록 화면으로 이어지는 앱 화면 흐름
- **스타일**: 핑크·하늘색 안개 그라데이션 위에 흰 글래스 패널을 얹은 밝은 애플풍 2D UI. 실제 책상 위 모니터와 노트북을 손으로 찍은 실사 촬영이라 주변 방이 함께 보인다.
- **기술**: Claude Code, Electron, React, TypeScript, Vite, WebGL, GitHub Actions
- **프롬프트 구조**: 작업 순서(디자인 시안 3개→공유 타입→서브에이전트 병렬 빌드→안전 에이전트→통합)·스택·기능·안전 규칙·디자인 언어·패키징·완료 조건을 마크다운 섹션으로 나눈 제품 개발 스펙
- **태그**: 데스크톱앱, 대시보드, glassmorphism, Electron, 앱시연, Apple풍, 실사촬영, 에이전트개발
- **주의**: 편집한 모션그래픽이 아니라 모니터를 폰으로 찍은 시연 영상이라 화면이 흔들리고 기울어져 있음. 프롬프트가 CleanMyMac 스크린샷을 품질 기준으로 첨부함

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

#### [Menu-scanning taste-matching app demo](product__menu-scanning-taste-matching-app-demo__2112191630266761382.md)
`product__menu-scanning-taste-matching-app-demo__2112191630266761382` · 약 1:1.14 (720x822) · 5s · 조회 39K · 에셋필요 O

- **요약**: 메뉴판 사진을 읽는 동안 와인병이 잔에 와인을 따르는 라인아트 로딩이 돌고, 이어서 음료가 'weighty–refreshing / fruity–bitter' 4분면 맵에 아이콘으로 흩어져 자리 잡는 앱 화면
- **어울리는 경우**: 2축 사분면으로 항목을 분류하는 개념 설명 / 분석 중 로딩 상태 연출 / 음식·와인·취향 주제 인서트
- **잘하는 표현**: 단색 라인아트 아이콘의 따르기 마이크로 애니메이션 / 흐림에서 또렷하게 바뀌며 점이 제자리를 찾는 사분면 산점도 / 항목마다 라벨이 붙은 작은 글리프
- **스타일**: 크림색 종이 배경에 울트라마린 잉크 선과 버건디 와인색 채움만 쓴 2색 2D. 가는 세리프 타이틀 'Map the menu'와 작은 자간 넓은 라벨이 차분한 인쇄물 느낌.
- **기술**: Lovable
- **프롬프트 구조**: 앱 기능·배색(크림 종이+울트라마린 잉크)·글리프·축 규칙을 한 문단에 담은 짧은 요청
- **태그**: 사분면, scatter-plot, 라인아트, 2색인쇄, 로딩애니메이션, 와인, 앱UI, 미니멀
- **주의**: 5초짜리 앱 화면 녹화로 메뉴 사진 입력이 필요함. 실제 메뉴 분석은 외부 모델(Claude) 호출

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

#### [Launch film for a web product](product__launch-film-for-a-web-product__2109019765134213540.md)
`product__launch-film-for-a-web-product__2109019765134213540` · 16:9 · 44s · 조회 35K · 에셋필요 X

- **요약**: 음성 받아쓰기 맥 앱 'tabi' 출시 영상으로, 어두운 3D 키보드가 주황빛으로 켜지고 "Hold fn. Say it." 같은 짧은 문구와 메시지 앱·글 읽기 UI 시연이 이어진 뒤 고양이 아이콘 로고로 끝난다
- **어울리는 경우**: 앱·서비스 런칭 티저 / "말하면 글이 된다" 같은 기능 하나 소개 / 짧은 카피를 끊어 보여 주는 제품 소개 인서트
- **잘하는 표현**: 키가 하나씩 주황으로 빛나는 3D 키보드 클로즈업과 키캡 분해 / 회색 문장 중 핵심 단어만 주황으로 바뀌는 카피 / 받아쓴 말이 깔끔한 문장으로 다시 써지는 UI 전후 비교
- **스타일**: 거의 검은 배경에 따뜻한 주황 하나만 강조색으로 쓰는 다크 미니멀. 산세리프 흰 카피, 얕은 심도의 3D 렌더, 픽셀아트 고양이 키캡이 귀여운 포인트.
- **기술**: Claude Code, Blender, Remotion, Mistral Voxtral, ElevenLabs
- **프롬프트 구조**: 스타일 지시 없이 "백만 달러짜리 앱처럼, 매 초 놀랍게"라는 목표와 길이·음성 도구만 준 열린 요청
- **태그**: 런칭영상, 제품티저, 다크미니멀, 3D키보드, Blender, Remotion, 키네틱카피, 단일강조색
- **주의**: 프롬프트에 스타일 지시가 거의 없어 결과 스타일은 모델 판단임. 3D는 Blender 렌더라 재현하려면 Blender 환경이 필요함

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

#### [Tesla Roadster promo video](product__tesla-roadster-promo-video__2111333150018171231.md)
`product__tesla-roadster-promo-video__2111333150018171231` · 9:16 · 68s · 조회 22K · 에셋필요 O

- **요약**: 테슬라 로드스터의 가속·추진 장치·흡입 팬·버전별 제원·가격을 터키어 내레이션에 맞춰 차량 사진과 큰 숫자, 단어 강조 자막으로 넘기는 세로 릴스
- **어울리는 경우**: 제품 제원·수치를 빠르게 훑는 숏폼 / "0.81초" 같은 큰 숫자 하나로 치고 들어가는 훅 / 챕터 번호를 단 기술 분석 인서트
- **잘하는 표현**: 화면을 꽉 채우는 굵은 콘덴스드 숫자와 빨간 단위 / 말하는 단어에 빨간 박스가 따라붙는 자막 / 상단 고정 브레드크럼(01 — 가속)으로 챕터 구분 / 진행 바·스펙 비교 블록
- **스타일**: 검정·차콜 배경에 흰색과 빨강만 쓰는 다크 미니멀, 굵은 콘덴스드 산세리프와 모노 라벨. 은색 차체 사진·연기·지구 사진을 어둡게 깔아 자동차 광고처럼 묵직하다.
- **기술**: ElevenLabs
- **프롬프트 구조**: 먼저 조사해 대본을 쓰고, 음성을 받은 뒤 그 음성에 맞춰 9:16 모션 영상을 만들라는 두 단계 짧은 요청(터키어)
- **태그**: 릴스, 세로영상, 자동차, 스펙설명, 큰숫자, 단어강조자막, 다크미니멀, 빨강강조
- **주의**: 실제 테슬라 차량 사진·렌더를 써서 브랜드 IP가 화면 대부분을 차지함. 사진 에셋 없이는 같은 결과가 나오지 않음

#### [Animated bento feature grid for a product site](product__animated-bento-feature-grid-for-a-product-site__2115393082472681875.md)
`product__animated-bento-feature-grid-for-a-product-site__2115393082472681875` · 약 1.47:1 (1060x720) · 20s · 조회 13K · 에셋필요 X

- **요약**: 브라우저 확장 기능 8개를 보여 주는 벤토 그리드에서 커서를 올릴 때마다 타일 속 작은 와이어프레임 장면(창 띄우기, 미리보기, 탭 전환, 언어 목록)이 다시 재생되는 웹페이지 화면 녹화
- **어울리는 경우**: 기능 여러 개를 한 화면에 나열해 소개할 때 / "클릭하면 이렇게 된다" 같은 작은 동작 설명 / 제품 기능 요약 슬라이드 대용
- **잘하는 표현**: 행동→결과를 2~4동작으로 보여 주는 추상 와이어프레임 미니 장면 / 헤어라인 셀과 동심 라운드 코너 / 호버 시 블러로 지우고 다시 재생하는 리플레이
- **스타일**: 흰 바탕에 1px 헤어라인과 아주 옅은 사선 텍스처, 회색 텍스트 바와 파랑 강조 한 점만 있는 조용한 2D UI. 이탤릭 세리프 'Small things that add up.' 제목이 에디토리얼한 느낌.
- **프롬프트 구조**: 작업 전 확인(스택·룩 선택·기능 선정)→재질 토큰(반경·색·그림자 수치)→장면 규칙→재생 규칙→다크모드→전달을 번호 섹션으로 정리한 컴포넌트 스펙
- **태그**: bento-grid, 기능소개, 마이크로인터랙션, 와이어프레임, 오프화이트, 헤어라인, UI애니메이션, 웹
- **주의**: 웹페이지를 커서로 조작한 화면 녹화라 일부 프레임은 그리드가 잘려 있고 끝에 데스크톱 배경이 비침

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

#### [Cinematic 3D scrolling brand website](product__cinematic-3d-scrolling-brand-website__2116972762514207070.md)
`product__cinematic-3d-scrolling-brand-website__2116972762514207070` · 9:16 · 9s · 조회 11K · 에셋필요 X

- **요약**: Higgsfield와 함께 만든 의류 브랜드 'Try the Look.' 웹사이트를 보라 조명 방의 노트북과 모니터에서 띄워 손으로 넘기며 폰으로 찍은 짧은 홍보 클립
- **어울리는 경우**: 생성 이미지를 쓴 패션 쇼핑몰 랜딩 사례 / "AI로 브랜드 사이트를 만들었다" 소개 컷 / 모델 라인업 룩북 레퍼런스
- **잘하는 표현**: 흰 스튜디오에 모델들이 일렬로 선 룩북 히어로 / 스크롤에 따라 인물이 바뀌는 라인업 / 큰 모니터와 노트북 이중 화면 연출
- **스타일**: 흰 배경의 미니멀 패션 사이트와 데님·니트 차림 모델 사진, 그 주변은 보라 네온 조명의 실제 방. 상단에 'Opus 5.5 + Higgsfield = 🔥', 빨간 'Check caption…' 자막이 얹혀 있다.
- **기술**: Higgsfield
- **프롬프트 구조**: 첨부 사진·링크의 브랜드로 스크롤이 이야기를 이끄는 3D 원페이지 사이트를 만들라는 한 문단 지시(핀 장면·카메라·조명·CTA·접근성 포함)
- **태그**: 웹사이트, 패션, 룩북, 랜딩페이지, 실사촬영, 생성이미지, Higgsfield, 세로영상
- **주의**: 프롬프트는 3D 회전·변형 스크롤을 요구하지만 영상에는 평면 룩북 페이지만 보임(프롬프트≠결과). 모델 사진은 외부 생성 모델(Higgsfield) 산출물이고 나이키 로고가 보여 IP 주의. 모니터를 폰으로 찍은 영상이라 인서트 참고 가치는 낮음

#### [Interactive frontend artifact](product__interactive-frontend-artifact__2106843514772639995.md)
`product__interactive-frontend-artifact__2106843514772639995` · 약 16:9 (1242x720) · 42s · 조회 9K · 에셋필요 O

- **요약**: igloo.inc 수준을 목표로 만든 가상 회사 'ERG'의 3D 인터랙티브 웹사이트를 스크롤하며 보여주는 화면 녹화
- **어울리는 경우**: 프리미엄 랜딩페이지/웹 3D 쇼케이스 / 브랜드 사이트 히어로 연출 참고 / 웹 에이전시 포트폴리오
- **잘하는 표현**: 사막 위 검은 모놀리스가 보로노이 균열 발광, 유리 큐브로 바뀌는 오브젝트 연출 / 텍스트 스크램블 효과(깨진 글자가 문장으로 정리) / 도트 매트릭스·하프톤과 파티클 모래시계
- **스타일**: 베이지 사막 실사풍 3D 배경과 짙은 갈색-검정 다크 섹션을 오가는 에디토리얼 웹 디자인. 굵은 그로테스크 산세리프 헤드라인, 주황 발광 포인트, 넓은 여백이 특징이다.
- **프롬프트 구조**: 참고 사이트 분석 후 '비슷한 수준, 복제 금지' + 독립 서브에이전트 채점 80% 이상까지 반복하라는 짧은 품질 루프형 지시
- **태그**: 웹사이트, 랜딩페이지, 3D웹, 모놀리스, 사막, 텍스트스크램블, 하프톤, editorial, interactive
- **주의**: 영상이 아니라 웹사이트 스크롤 녹화. 참고 사이트(igloo.inc) 분석이 전제이고, 사용 기술은 명시되지 않음

#### [2D cartoon story ad drawn in code](product__2d-cartoon-story-ad-drawn-in-code__2119554953018773795.md)
`product__2d-cartoon-story-ad-drawn-in-code__2119554953018773795` · 9:16 · 50s · 조회 7K · 에셋필요 X

- **요약**: 게임을 10초만 더 하려는 아이와 막으려는 엄마의 카운트다운 이야기를 캔버스 코드로만 그린 2D 카툰 숏폼으로, 게임패스 '+10 SECONDS' 구매 장면과 가짜 댓글창으로 끝나는 숨은 광고
- **어울리는 경우**: 아이·게임·가족 소재의 유머 숏폼 / 카운트다운 긴장감 연출 / 이야기 속에 제품을 숨기는 광고형 콘텐츠
- **잘하는 표현**: 상단 타이머 HUD(0:10→0:01)와 'SECOND 10' 카드 팝인 / 한두 단어씩 튀어나오는 굵은 외곽선 자막과 색 강조 단어 / 선버스트·코인 폭발·불꽃 같은 과장 효과 / 표정이 크게 바뀌는 캐릭터 반응
- **스타일**: 진한 남색 외곽선과 포화된 평면색(보라 밤 침실, 초록 잔디, 금색 코인)의 2D 카툰. 각진 블록형 머리 캐릭터와 게임 UI 패널이 섞인 어린이 게임 채널 분위기.
- **기술**: HTML Canvas, Python(NumPy·SciPy·Pillow), Playwright, Chromium, FFmpeg, ElevenLabs, faster-whisper
- **프롬프트 구조**: inputs(제품·장르·음성 도구 질문)→direction(광고 공식·캐릭터 리그·세트·폰트·자막·HUD·모션 규칙)→structure(초 단위 비트 표)→build→gotchas→start를 XML 태그로 나눈 대형 제작 레시피
- **태그**: 카툰, 2D, 숏폼, 숨은광고, 카운트다운, 게임UI, 키네틱자막, canvas
- **주의**: 프롬프트는 형사 이야기를 예로 들고 "로블록스 느낌 금지"라 했지만 결과는 블록형 캐릭터·오비·게임패스가 나오는 로블록스풍 게임 이야기(프롬프트≠결과). 내레이션은 ElevenLabs 음성

#### [3D Find My interface concept](product__3d-find-my-interface-concept__2118665193479659569.md)
`product__3d-find-my-interface-concept__2118665193479659569` · 9:16 · 16s · 조회 6K · 에셋필요 O

- **요약**: 손으로 그린 '나의 찾기' 앱 스케치(왼쪽 'Drawing')와 그것을 Three.js로 구현한 3D 프로토타입(오른쪽 'Opus 5.5')을 나란히 놓고, 도시 지도→길 찾기→탁자 위 열쇠 발견까지 넘기는 영상
- **어울리는 경우**: 스케치에서 완성품으로 가는 과정 설명 / 지도·위치 추적 서비스 소개 / 물건 찾기·내비게이션 단계 시연
- **잘하는 표현**: 위에서 내려다보는 절차 생성 3D 도시와 경로 하이라이트 / 거리(14 m→6 m→1 m)와 화살표가 줄어드는 근접 탐색 / 초록 동심원 성공 표시 / 스케치와 결과의 좌우 대응
- **스타일**: 검정 배경 위 왼쪽 흑백 펜 스케치, 오른쪽 자연광이 드는 따뜻한 베이지·초록 3D 장면과 흰 iOS 카드. 깔끔한 애플 시스템 UI 감성.
- **기술**: Figma, React, Vite, Three.js, React Three Fiber, Drei, Motion, Lucide
- **프롬프트 구조**: ROLE→MISSION→01~07 번호 섹션(비주얼·4단계 UX·인터랙션·스택·성능·디자인 금지 사항·전달)과 성공 기준으로 짠 프로토타입 스펙
- **태그**: 3D지도, Three.js, 스케치투앱, 비교레이아웃, iOS, 내비게이션, 프로토타입, 세로영상
- **주의**: 스케치 대 결과 비교 구성으로 오른쪽 패널이 Opus 결과. 하단에 'Comment "OPUS" for guide' 문구가 계속 붙어 있음. 애플 'Find My' 아이콘·이름을 그대로 써서 IP 주의. 손 스케치가 입력 에셋

### education (교육/설명) — 20건 (조회수순)


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

#### [What if the Sun vanished explainer](education__what-if-the-sun-vanished-explainer__2119489762134295014.md)
`education__what-if-the-sun-vanished-explainer__2119489762134295014` · 16:9 · 67s · 조회 105K · 에셋필요 X

- **요약**: 쿠르츠게작트풍 코드 애니메이션 레시피로 만든 '해적은 왜 안대를 썼을까' 설명 영상으로, 해적 선장과 작은 로봇 마스코트가 갑판과 어두운 선창을 오가며 눈의 암적응(23분)을 보여 준다
- **어울리는 경우**: "왜 그럴까" 질문형 과학 상식 강의 / 시청자를 "YOU" 캐릭터로 끌어들이는 2인칭 설명 / 밝음과 어둠의 대비가 핵심인 개념
- **잘하는 표현**: 귀여운 평면 캐릭터와 마스코트의 표정 연기 / 원형 게이지 타이머(23 MIN) / 둥근 알약 캡션 '대문자+자간' / 연도 숫자 슬램 인(2007)과 마지막 제목 카드
- **스타일**: 외곽선 없는 둥근 평면 벡터, 하늘색 바다·주황 태양·남색 밤하늘의 부드러운 파스텔 팔레트. Fredoka 계열 둥근 글씨와 남색 반투명 캡션 알약, 비네트와 은은한 그레인.
- **기술**: HTML Canvas, WebGL, ElevenLabs, kokoro-onnx, faster-whisper, Playwright, Edge, libx264
- **프롬프트 구조**: inputs→direction(색 코드까지 지정한 우주·태양·지구·마스코트)→structure(초 단위 비트, 다른 주제에도 쓰는 공통 뼈대)→build→gotchas→start를 XML 태그로 나눈 레시피
- **태그**: 과학설명, Kurzgesagt풍, 플랫벡터, 마스코트, 캐릭터애니메이션, 질문형, 2D, 파스텔
- **주의**: 프롬프트 기본 주제는 '태양이 사라지면'이지만 영상은 같은 뼈대로 만든 '해적 안대' 편(프롬프트≠결과). 태양 소멸 버전은 infographic-explainer-animation 쪽이 가깝다

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

#### [Infographic explainer animation](education__infographic-explainer-animation__2117602113509294520.md)
`education__infographic-explainer-animation__2117602113509294520` · 16:9 · 62s · 조회 63K · 에셋필요 O

- **요약**: '태양이 사라지면 8분 20초 뒤에야 어두워진다'를 공원·천문대·교실·우주·설원 장면으로 이어 가며, 표지판과 칠판에 글자가 타이핑되는 인포그래픽 채널풍 플랫 일러스트 설명 영상
- **어울리는 경우**: 과학 사실이나 사고실험을 장면 전환으로 풀 때 / 오해를 바로잡는 "흔한 착각 vs 사실" 설명 / 숫자·시간을 표지판에 띄우는 강의 인서트
- **잘하는 표현**: 장면 속 표지판·칠판·현수막에 직접 타이핑되는 글자 / 2~4초마다 바뀌는 장소와 연기하는 캐릭터 / 좌상단 날짜 카드(1 WEEK, 1 YEAR)와 온도계 / 궤도 도식과 표지판으로 된 수치
- **스타일**: 외곽선 없는 플랫 벡터에 한 단계 어두운 면 음영, 하늘색·청록·베이지·남색의 차분한 팔레트, 큰 머리와 점 눈 캐릭터. 굵은 Montserrat 글씨가 장면 안 물체 위에만 놓인다.
- **기술**: Python, Playwright, Chromium, FFmpeg, faster-whisper, OpenCV, Pillow, librosa, GPT Image 2
- **프롬프트 구조**: 주제·이미지 모델·음성 확인→direction(그림체·글자 규칙·금지)→structure(초 단위 서사 뼈대)→build(크로마키 컷아웃·IK 팔·걷기·렌더·사운드)→gotchas로 짠 레시피
- **태그**: 인포그래픽, 설명영상, 플랫일러스트, 캐릭터, 타이핑텍스트, 과학, 장면전환, 2D
- **주의**: 배경 판과 캐릭터 시트를 외부 이미지 생성 모델(GPT Image 2)로 만들고 코드는 합성·애니메이션만 맡음. 참고 채널 프레임을 스타일 참조로 넣음

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

#### [Al Capone documentary film](education__al-capone-documentary-film__2119350502961889592.md)
`education__al-capone-documentary-film__2119350502961889592` · 16:9 · 322s · 조회 37K · 에셋필요 O

- **요약**: 알 카포네의 일생을 지도·신문·머그샷·서류가 놓인 하나의 큰 책상 위를 카메라가 끊김 없이 미끄러지며 따라가는 5분짜리 코드 다큐멘터리
- **어울리는 경우**: 인물사·사건사 강의 / 연도와 장소를 오가는 타임라인 서사 / 기사·문서를 근거로 보여 주는 탐사형 설명
- **잘하는 표현**: 컷 없이 이어지는 원 테이크 카메라 이동(밀고 당기기) / 지도 위 빨간 핀과 지역 하이라이트 / 사진·신문 스크랩이 물체처럼 떨어지는 배치 / 하단 자막의 핵심 단어 노란 하이라이트
- **스타일**: 어두운 갈색 책상 배경에 세피아·흑백 사진, 크림색 종이와 청록 바다 지도, 빨간 핀·도장 포인트. 굵은 콘덴스드 연도 숫자, 그레인·비네트의 빈티지 탐사 다큐 톤.
- **기술**: HTML Canvas
- **프롬프트 구조**: 입력(음성·사진·스타일 참고·포맷)→스타일(원 테이크 월드 카메라)→가독성 규칙 6개→과정(비트 표 먼저, 렌더 전 자체 점검)으로 짠 템플릿형 요청
- **태그**: 다큐멘터리, 역사, 인물, 지도, 신문스크랩, 원테이크카메라, 빈티지, 타임라인
- **주의**: 실존 인물(알 카포네)의 실제 사진·신문 자료와 별도 내레이션 음성이 필요함

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

#### [Explainer video on JEM self-supervised learning paper](education__explainer-video-on-jem-self-supervised-learning-paper__2114676265093664978.md)
`education__explainer-video-on-jem-self-supervised-learning-paper__2114676265093664978` · 16:9 · 1561s · 조회 34K · 에셋필요 O

- **요약**: 자기지도학습 논문 JEM의 구조와 세 가지 손실을 고양이 사진·인코더 도식·수식·벤치마크 표로 기초부터 풀어 주는 26분짜리 논문 해설 영상
- **어울리는 경우**: AI·머신러닝 논문 해설 강의 / 수식을 직관과 연결해 설명할 때 / 모델 구조(교사·학생 인코더) 도식 인서트 / 결과 비교 표
- **잘하는 표현**: 이미지→인코더→패치 표현으로 흐르는 블록 도식 / LaTeX 수식의 항마다 색 주석 달기 / 패치 격자·막대그래프로 손실 개념 시각화 / 두 모델 성능 비교 표
- **스타일**: 짙은 남색·차콜 배경에 청록 인코더 블록, 주황·초록 강조, 흰 LaTeX 수식과 얇은 라벨. 좌상단 챕터명, 하단 두 줄 자막의 차분한 다크 강의 슬라이드형 2D.
- **프롬프트 구조**: 논문 링크와 "수학을 몰라도 처음부터" 요청 뒤, 수식 설명이 빠졌으니 직관과 수식을 연결해 달라는 후속 요청이 붙은 짧은 대화형
- **태그**: 논문해설, 머신러닝, 수식, 도식, 다이어그램, 강의영상, 다크, 장편
- **주의**: 26분 장편이라 인서트 참고는 개별 장면 단위로만 볼 것. 예시 사진(고양이) 등 이미지 에셋 사용, 도구 정보 없음

#### [Interactive Lamborghini FL3 tractor diesel engine](education__interactive-lamborghini-fl3-tractor-diesel-engine__2112130961714385214.md)
`education__interactive-lamborghini-fl3-tractor-diesel-engine__2112130961714385214` · 약 1.60:1 (1152x720) · 42s · 조회 32K · 에셋필요 O

- **요약**: 람보르기니 트랙터용 FL3 디젤 엔진을 절차 생성 3D로 만든 인터랙티브 '벤치 스터디' 페이지에서 시동·단면·분해·냉각을 차례로 눌러 보는 화면 녹화
- **어울리는 경우**: 기계·엔진 작동 원리 설명 / 부품을 분해해 이름을 붙이는 구조 설명 / 계기판·그래프가 실시간으로 반응하는 시뮬레이션 데모
- **잘하는 표현**: 하늘색 엔진의 단면 보기와 부품 분해(exploded view)와 라벨 / 회전계·지시선도 같은 라이브 계기 / 하단 청사진풍 선화 4컷 / 인쇄물 레이아웃 안에 놓인 3D
- **스타일**: 아이보리 종이에 주황·하늘색·검정 3색 잉크를 쓴 1960년대 이탈리아 기술 매뉴얼풍. 커다란 Bodoni 'FL3'(3만 주황), 등록 마크와 이중 프레임, 뒤에 흐린 하늘색 숫자 3.
- **기술**: Three.js
- **프롬프트 구조**: 하드 룰→공개 제원(사실과 '모델링' 가정 구분)→아트 디렉션(종이·잉크·서체·레이아웃·카피)→3D 부품 목록→움직이는 내부 부품 순으로 쌓은 초상세 스펙
- **태그**: 엔진, 기계구조, exploded-view, Three.js, 기술도판, 2색인쇄, 인터랙티브, 에디토리얼
- **주의**: 편집 영상이 아니라 웹페이지 조작 화면 녹화. 람보르기니 이름이 나오지만 로고는 쓰지 않도록 지시됨

#### [Nobel Prize science explainer video](education__nobel-prize-science-explainer-video__2108143447496679553.md)
`education__nobel-prize-science-explainer-video__2108143447496679553` · 16:9 · 780s · 조회 27K · 에셋필요 X

- **요약**: 2026년 노벨 과학상 수상자와 업적을 13분 동안 장마다 다른 그래픽 스타일(바우하우스 표지, HUD 터미널, 스티커 콜라주, 글래스 그라데이션, 분자 선화)로 바꿔 가며 해설하는 영상
- **어울리는 경우**: 여러 인물·업적을 차례로 소개하는 강의 / 장마다 분위기를 바꿔야 하는 긴 설명 / 키랄성 같은 과학 개념을 사물 비유로 보여 줄 때
- **잘하는 표현**: 장갑 두 짝 같은 사물 비유 / 이름표 스티커·종이 카드·인용문 카드 콜라주 / 돋보기로 확대하는 분자 군집 / 어두운 HUD 패널 속 데이터 막대와 라벨
- **스타일**: 크림 종이 위 빨강·파랑·노랑 기하 도형과 굵은 산세리프의 바우하우스·스티커 장면과, 남색·보라 그라데이션 위 청록·핑크 네온 선의 다크 장면이 번갈아 나온다.
- **기술**: Claude Code
- **프롬프트 구조**: 최고 수준 유튜버·감독·과학 커뮤니케이터 역할을 겹쳐 주고 콜라주·등각 2.5D·HUD·글래스·바우하우스 등 스타일 키워드 15개를 나열한 짧은 중국어 요청
- **태그**: 노벨상, 과학해설, 멀티스타일, 바우하우스, 스티커콜라주, HUD, 장편, 인물소개
- **주의**: 13분 장편이라 장면 단위로 참고할 것. 실존·가상 수상자 이름과 인용문이 나옴. 화면 구석에 'agent.space' 표기

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

#### [Tesla Roadster explainer video](education__tesla-roadster-explainer-video__2111440772998599022.md)
`education__tesla-roadster-explainer-video__2111440772998599022` · 9:16 · 174s · 조회 13K · 에셋필요 X

- **요약**: 테슬라 로드스터를 '흡(흡입)·분(분사)·피(외피)·장(약속 장부)' 같은 한 글자 장으로 나눠 3D 분해도와 계산식·제원 비교표로 해부하는 세로형 중국어 해설 영상
- **어울리는 경우**: 제품을 부품별로 뜯어 설명하는 분해 강의 / 공식으로 수치를 직접 계산해 보이는 장면 / 약속과 현실 수치를 비교하는 표 / 세로 숏폼 기술 해설
- **잘하는 표현**: 부품이 층층이 떨어져 나오는 3D 분해도와 지시선 라벨 / 투명 차체 속 질소 탱크·노즐 분사 / 화살표 힘 도식과 kPa 계산 / 연도별 취소선이 그어지는 비교표, 궤도 도식
- **스타일**: 짙은 차콜 배경에 베이지 로폴리 3D 차량, 흰 글씨와 주황빨강 강조 한 색. 굵은 한자 장 제목 옆 작은 영문 대문자, 중·영 2줄 자막이 정돈된 다크 테크 인포그래픽.
- **기술**: Claude Code
- **프롬프트 구조**: 최고 수준 역할 나열, 5분 '만물 분해' 모션그래픽 주제, 스타일 키워드 후보, 확산·비즈니스 모델 고민까지 담은 짧은 중국어 요청(확인 후 착수)
- **태그**: 분해도, exploded-view, 자동차, 3D, 데이터시각화, 이중자막, 세로영상, 다크테크
- **주의**: 실제 테슬라 제품 이야기라 브랜드 IP 주의. 끝 장면에 Agent.Space 제작 크레딧이 나옴

#### [Cartoon animal facts vertical short](education__cartoon-animal-facts-vertical-short__2118149077842133334.md)
`education__cartoon-animal-facts-vertical-short__2118149077842133334` · 9:16 · 34s · 조회 11K · 에셋필요 X

- **요약**: 그린란드 상어의 수명·느린 속도·눈 기생충·먹이·식용 이야기를 마이크 든 후드티 진행자 캐릭터가 장면마다 튀어나와 소개하는 카툰 동물 상식 숏폼
- **어울리는 경우**: 동물·자연 상식 숏폼 / 점점 세지는 사실 나열(갈수록 더 충격) / 진행자 캐릭터가 등장하는 가벼운 설명 / 사실마다 분장 개그를 붙이는 구성
- **잘하는 표현**: 사실마다 바뀌는 동물 분장(수염 노인, 가발, 교정기) / 이름을 말할 때 그려지는 빨간 마커 타원 / 굵은 외곽선 큰 제목과 노란 키워드 알약 자막 / 엑스레이 투시 장면
- **스타일**: 두꺼운 짙은 갈색 외곽선과 평면색, 단순한 셀 음영, 큰 눈 캐릭터의 2D 카툰. 1.5~3초마다 바다·생일파티·교실·바이킹 술집 등 따뜻하고 진한 색의 배경이 바뀐다.
- **기술**: Python, Playwright, FFmpeg, OpenCV, Pillow, NumPy, ElevenLabs, Kokoro, GPT Image 2
- **프롬프트 구조**: inputs(주제·이미지 모델·음성)→direction(진행자·동물 포즈 9종·제목·자막 수치)→structure(초 단위 비트)→build 순의 XML 태그 레시피
- **태그**: 카툰, 동물상식, 숏폼, 세로영상, 진행자캐릭터, 키네틱자막, 2D, 개그
- **주의**: 메타는 에셋필요 X지만 프롬프트는 외부 이미지 생성 모델(GPT Image 2 등)로 그림 4장을 만들게 함. 그림체는 특정 동물 상식 채널을 따라 한 것

### production (제작 파이프라인) — 17건 (조회수순)


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

#### [Talking-head video edited into a motion-graphics cut](production__talking-head-video-edited-into-a-motion-graphics-cut__2109454493415023080.md)
`production__talking-head-video-edited-into-a-motion-graphics-cut__2109454493415023080` · 16:9 · 379s · 조회 93K · 에셋필요 O

- **요약**: 포르투갈어 토킹헤드 원본을 컷편집하고, 얼굴을 피해 화면 반쪽에 리스트·숫자·도표·비교 카드를 띄우는 Remotion 모션그래픽 유튜브 영상으로 완성한 사례
- **어울리는 경우**: 토킹헤드 강의에 설명 그래픽을 붙일 때(이 프로젝트와 가장 직접적) / 말하는 항목마다 리스트가 하나씩 드러나는 설명 / 숫자·전후 비교·인용 카드 / 카메라 카드↔풀프레임 레이아웃 전환
- **잘하는 표현**: 얼굴 추적 기반 카메라 카드 배치와 반대편 그래픽 / 단어 타임스탬프에 맞춘 리빌 / 세리프 이탤릭 강조어가 섞인 에디토리얼 타이포 / 점프컷 줌 1.0↔1.075 교차
- **스타일**: 어두운 웜 차콜(#14120F) 무대에 아이보리 텍스트, 클레이 오렌지 단일 강조색 이탤릭. Fraunces 세리프 + 모노 라벨, 그레인과 은은한 글로우의 차분한 에디토리얼 2D.
- **기술**: Remotion, ffmpeg, ElevenLabs Scribe(또는 Whisper), Python, Apple Vision/MediaPipe 얼굴 추적
- **프롬프트 구조**: INPUT·STACK → 번호 단계(컷 계획·프레임 정확 컷·얼굴 추적·디자인 시스템·비트시트 JSON·Remotion 빌드·사운드·렌더 검증) → RULES의 파이프라인 명세
- **태그**: 토킹헤드, 강의, Remotion, 모션그래픽, 에디토리얼, 단일강조색, 컷편집, 얼굴추적
- **주의**: 원본 토킹헤드 영상이 필요(실존 인물 얼굴). 6분 분량의 완성 유튜브 영상이라 인서트 참고 시 그래픽 패널 부분만 볼 것

#### [Automated branded video edit with voice sync](production__automated-branded-video-edit-with-voice-sync__2110019799342260630.md)
`production__automated-branded-video-edit-with-voice-sync__2110019799342260630` · 9:16 · 74s · 조회 73K · 에셋필요 O

- **요약**: ElevenLabs 보이스에 맞춰 단어마다 텍스트·로고·터미널 카드가 뜨는, "Claude Code가 내 영상을 만들었다"는 터키어 세로 모션 디자인 영상
- **어울리는 경우**: 툴·워크플로 소개 쇼츠 / 내레이션 단어에 정확히 맞춘 키네틱 타이포 / 로고 그리드로 쓰는 도구 나열 / 코드·터미널 화면을 깔끔하게 보여줄 때
- **잘하는 표현**: 볼드 산세리프 + 오렌지 이탤릭 세리프 강조어 조합 / 맥 창 스타일 터미널·코드 카드 / 단어 타임라인·파형 시각화 / 앱 아이콘 로고 그리드
- **스타일**: 오프화이트 크림 배경과 검정 다크 씬이 교차, 오렌지 단일 강조색. 둥근 모서리 카드·부드러운 그림자의 Apple풍 미니멀 2D, 도입부에만 실사 인물 컷.
- **기술**: Claude Code, ElevenLabs, Remotion, HyperFrames
- **프롬프트 구조**: 터키어 한 문장 지시(보이스에 맞춰 텍스트·로고가 그 단어에 등장, 실제 로고 사용, MP4 렌더)
- **태그**: 키네틱타이포, 보이스싱크, Remotion, HyperFrames, 오프화이트, 오렌지강조, 쇼츠, 로고
- **주의**: 보이스 음성 파일과 실제 브랜드 로고 에셋 필요. 터키어 텍스트, 실존 인물 등장

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

#### [Beat-synced manga-style music edit](production__beat-synced-manga-style-music-edit__2113764485429125125.md)
`production__beat-synced-manga-style-music-edit__2113764485429125125` · 4:3 · 27s · 조회 26K · 에셋필요 O

- **요약**: 애니 원본 영상을 잉크선·스크린톤·빨강/노랑 두 강조색만 남긴 살아있는 만화 페이지로 바꾸고 비트에 맞춰 하드컷한 뮤직 에디트
- **어울리는 경우**: 영상 클립을 만화 컷 스타일로 재해석할 때 / 강렬한 장면 전환·임팩트 인서트 / 일본어 의성어 타이포 연출 / 짧은 팬 에디트
- **잘하는 표현**: XDoG 잉크선 + 하프톤 스크린톤 / 동심원·집중선·단색 그래픽 배경 위 컷아웃 / 의성어('ズッ'·'バッ') 타이포 / 비트 고정 하드컷
- **스타일**: 종이 흰색·잉크 검정에 진홍 빨강·노랑 하이라이트만 쓰는 엄격한 4색 팔레트. 흑백 만화 원고 같은 2D 그래픽, 강렬하고 쿨한 무드.
- **기술**: rembg(isnet-anime), XDoG/DoG
- **프롬프트 구조**: INPUTS(빈칸 템플릿) → GOAL → 번호 단계(소재 분석·룩 고정·샷 어휘 설계·…) 상세 파이프라인
- **태그**: 만화, 스크린톤, 잉크선, 비트싱크, 뮤직에디트, 빨강노랑, 의성어, 애니
- **주의**: 원본 애니 클립·음악 필요. 원본은 기존 애니 캐릭터(체인소맨 마키마로 보임) IP

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

#### [Manga panel music video edit](production__manga-panel-music-video-edit__2114477295574425988.md)
`production__manga-panel-music-video-edit__2114477295574425988` · 16:9 · 35s · 조회 22K · 에셋필요 O

- **요약**: 두 개의 격투 애니 클립을 흰 거터로 나뉜 비대칭 만화 패널 레이아웃에 섞어 넣고, 비트마다 패널이 재배치되는 고에너지 뮤직비디오
- **어울리는 경우**: 여러 소스를 한 화면에 동시에 보여줄 때 / 액션·하이라이트 몽타주 / 코믹 패널 스타일 전환 / 강의의 요약 몽타주
- **잘하는 표현**: 기울어진 비대칭 패널 분할과 비트 재배치 / 패널 간 스타일 감염(흑백·선화·색반전) / 임팩트 별빛·집중선 / 시간 오프셋 모션 에코
- **스타일**: 흰 거터 위 다크 그레이·청록·주황 화염 톤의 애니 패널, 일부 패널은 흑백 실루엣·선화로 변주. 텍스트 없는 역동적 2D 만화 그리드.
- **프롬프트 구조**: EDITING·GRID STRUCTURE·VISUAL EFFECTS·CREATIVE DIRECTION·AUDIO 대문자 섹션별 지시
- **태그**: 만화패널, 그리드, 뮤직비디오, 액션, 비트싱크, 스타일감염, 애니
- **주의**: 원본 애니 클립 2개·음악·패널 레퍼런스 이미지 필요

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

#### [Satoru Gojo temporal grid video edit](production__satoru-gojo-temporal-grid-video-edit__2115118260060656126.md)
`production__satoru-gojo-temporal-grid-video-edit__2115118260060656126` · 16:9 · 33s · 조회 12K · 에셋필요 O

- **요약**: 화면을 20×12 셀 격자로 나누고 각 셀이 같은 영상의 다른 시점을 재생하며 체커보드·파동처럼 시간이 어긋나는 고죠 사토루 뮤직 에디트
- **어울리는 경우**: 글리치·디지털 붕괴 전환 / "시간이 어긋난다" 메타포 / 한 장면을 강조하는 하이라이트 인서트
- **잘하는 표현**: 셀 단위 타임 오프셋·체커보드 리버스 / 중앙 앵커 영역 유지 + 주변 시간 파동 / 화이트 플래시·집중선 임팩트 / 픽셀 블록 디스플레이스먼트
- **스타일**: 차가운 하늘색·화이트 톤에 가는 회색 격자선, 검은 실루엣 캐릭터. 모자이크 픽셀 블록과 폭발광이 섞인 쿨한 2D 글리치 무드.
- **기술**: Seedance 2.5
- **프롬프트 구조**: GRID STRUCTURE·TEMPORAL CHOREOGRAPHY·VISUAL EFFECTS(효과 목록)·RHYTHMIC EDITING·VISUAL COHERENCE 섹션별 지시
- **태그**: 템포럴그리드, 글리치, 뮤직에디트, 모자이크, 비트싱크, 애니, 블루톤
- **주의**: 원본 클립은 Seedance 생성 영상. 주술회전 고죠 사토루 IP

#### [Satoru Gojo AMV from still images and music](production__satoru-gojo-amv-from-still-images-and-music__2114745463736082828.md)
`production__satoru-gojo-amv-from-still-images-and-music__2114745463736082828` · 4:3 · 33s · 조회 12K · 에셋필요 O

- **요약**: Midjourney 스틸 이미지들을 패럴랙스·카메라 무브로 움직이고 변하는 만화 그리드에 배치해 만든 고죠 사토루 AMV
- **어울리는 경우**: 정지 이미지 몇 장으로 역동적 영상을 만들 때 / 인물·캐릭터 소개 몽타주 / 반복 패널로 디테일(눈·손) 강조
- **잘하는 표현**: 스틸 이미지의 패럴랙스·크롭 리프레이밍 / 동일 컷을 색만 바꿔 반복하는 패널(빨강·청록·흑백) / 소용돌이·눈빛 글로우 효과 / 기울어진 패널 분할
- **스타일**: 짙은 남색·빨강·흰 머리칼의 하이콘트라스트 애니 일러스트, 강한 블루·레드 글로우와 흑백 실루엣 패널. 화려한 애니 오프닝 무드.
- **기술**: Midjourney
- **프롬프트 구조**: EDITING & ANIMATION·DYNAMIC GRID·VISUAL EFFECTS·CREATIVE DIRECTION 섹션별 지시
- **태그**: AMV, 스틸이미지애니메이션, 패럴랙스, 만화그리드, 애니, 글로우, 비트싱크
- **주의**: Midjourney 이미지와 음악 필요. 주술회전 고죠 사토루 IP

#### [Beat-synced video edit](production__beat-synced-video-edit__2114356633849516157.md)
`production__beat-synced-video-edit__2114356633849516157` · 약 1:1.12 (720x810) · 59s · 조회 10K · 에셋필요 O

- **요약**: 광선검 결투 애니 클립에 충격 지점에서 번지는 색 필드·충격파 링·크로매틱 분리를 비트에 맞춰 입힌 뮤직 에디트로, 상하 두 버전(공격적/부드러운)을 쌓아 비교한 영상
- **어울리는 경우**: 같은 소스에 효과 강도 두 가지를 비교 시연 / 액션 장면 임팩트 강조 / 원본 타이밍을 유지한 채 스타일만 입힐 때
- **잘하는 표현**: 충돌 지점에서 퍼지는 스타일 감염(원형·와이프) / 크로매틱 스플릿·색반전 플래시 / 모션 에코·고스트 레이어 / 기하 심볼(원·사각·방사선) 오버레이
- **스타일**: 검은 배경에 네온 빨강·파랑 광선검 빛, 핑크·라임·주황으로 수시로 바뀌는 색 필드. 화려하고 공격적인 애니 VFX 무드.
- **기술**: Python, ffmpeg
- **프롬프트 구조**: 두 개의 프롬프트(상단용 공격적 버전, 'Bottom:' 부드러운 버전)를 같은 틀로 나란히 작성
- **태그**: 비트싱크, VFX, 광선검, 애니, 스타일감염, 크로매틱, 비교영상, 네온
- **주의**: 위아래 2단 비교 영상(위=공격적, 아래=부드러운 버전). 원본 클립·음악 필요, 광선검은 스타워즈 연상

#### [Code-generated music video](production__code-generated-music-video__2112006151885705553.md)
`production__code-generated-music-video__2112006151885705553` · 16:9 · 136s · 조회 10K · 에셋필요 O

- **요약**: Suno로 만든 곡에 맞춰 밤 들판 위 지평선을 따라 흐르는 빛의 선 하나가 산 능선과 달로 변해가는 코드 생성 뮤직비디오
- **어울리는 경우**: 차분한 오프닝·아웃트로 배경 / 오디오 반응형 앰비언트 비주얼 / "하나의 선이 변해 간다" 메타포 연출
- **잘하는 표현**: 하나의 아이디어(선)를 곡 전체에 걸쳐 변형 / 음악 분석 타이밍 맵 기반 동기화 / 수많은 풀잎 인스턴싱 들판 / 낮은 시점 얕은 심도
- **스타일**: 깊은 남색 별밤과 은백색 풀밭, 지평선의 주황 노을 띠와 하늘색 네온 선. 미니멀하고 고요한 시네마틱 3D.
- **기술**: Suno, Claude Code, GSAP, WebGL
- **프롬프트 구조**: 역할 부여 → 컨셉·룩·텍스트·납품 빈칸 → 작업 7단계(음악 분석·스토리보드·프레임 함수 렌더·비평 서브에이전트 검수 루프) → 합격 기준
- **태그**: 뮤직비디오, 오디오반응, WebGL, 들판, 밤하늘, 앰비언트, 미니멀, 시네마틱
- **주의**: 음악 파일(Suno 생성) 필요

#### [Common video editing effects showcase](production__common-video-editing-effects-showcase__2111678979413598560.md)
`production__common-video-editing-effects-showcase__2111678979413598560` · 9:16 · 17s · 조회 8K · 에셋필요 O

- **요약**: HeyGen 아바타가 말하는 동안 크래시 줌·휩팬·랙포커스 등 12가지 편집 효과를 미니 카드 데모와 번호 체크리스트로 보여주는 HyperFrames 홍보 쇼츠
- **어울리는 경우**: 토킹헤드 위에 목록형 설명 패널을 올릴 때 / 기능·효과 나열 소개 / 진행 항목 하이라이트 체크리스트 / 큰 숫자 강조 자막
- **잘하는 표현**: 화자 앞에 뜨는 미니 영상 카드 + 번호 목록 하이라이트 / 연두색 강조 키워드 자막 / 'text behind you' 등 효과 데모 / 엔딩 웹사이트 카드
- **스타일**: 벽돌벽 서재의 실사 토킹헤드 위에 반투명 화이트 카드와 민트 그린 강조, 굵은 흰 산세리프 자막. 깔끔한 테크 쇼츠 2D 오버레이.
- **기술**: HeyGen, HyperFrames
- **프롬프트 구조**: 한두 줄 요청 — HeyGen 아바타 사용 + 효과 12개 나열 + 참고 영상 학습 지시
- **태그**: 토킹헤드, 쇼츠, 체크리스트, 편집효과, 오버레이, 민트강조, HyperFrames
- **주의**: HeyGen AI 아바타(실존 인물 기반) 사용, HyperFrames 제품 홍보물

#### [Neon glitch video treatment](production__neon-glitch-video-treatment__2113344709682663503.md)
`production__neon-glitch-video-treatment__2113344709682663503` · 1:1 · 7s · 조회 7K · 에셋필요 O

- **요약**: 애니 캐릭터 영상을 배경을 지운 뒤 시안·보라·마젠타 3색으로 포스터라이즈하고 데이터모시 잔상과 세로 드립을 입힌 다크 네온 글리치 루프
- **어울리는 경우**: 사이버·해킹·디지털 붕괴 주제 인서트 / 짧은 루프 배경 / 인물 컷아웃에 스타일 입히기 시연
- **잘하는 표현**: rembg 컷아웃 + 3색 포스터라이즈 / 데이터모시 녹아내리는 잔상 / 세로 픽셀 드립·스크래치 라인 / 마젠타 림라이트
- **스타일**: 순수 검정 배경에 시안·바이올렛·마젠타 네온만 빛나는 베이퍼웨이브 글리치, 세로로 흘러내리는 줄무늬 질감.
- **기술**: Python, ffmpeg, rembg(isnet-anime·isnet-general-use)
- **프롬프트 구조**: 번호 단계 6개(컷아웃 → 포스터라이즈 팔레트 → 림라이트 → 데이터모시 → 드립 → 그레인)에 수치 파라미터 명시 + 사운드트랙 지시
- **태그**: 글리치, 네온, 데이터모시, 베이퍼웨이브, 포스터라이즈, 루프, 컷아웃
- **주의**: 원본 영상 필요. 7초 짧은 루프

### stories (단편/스토리) — 23건 (조회수순)


#### [Moss-Covered Giant Robot Awakens at Sunrise](stories__moss-covered-giant-robot-awakens-at-sunrise__2117169796290916732.md)
`stories__moss-covered-giant-robot-awakens-at-sunrise__2117169796290916732` · 약 1.84:1 (1328x720) · 81s · 조회 2.3M · 에셋필요 X

- **요약**: 안개 낀 숲에서 이끼로 뒤덮인 거대 로봇이 해 뜰 때 깨어나 일어서고 엔진을 점화해 황금빛 하늘로 날아오르는 지브리풍 2D 애니메 단편
- **어울리는 경우**: "오래 잠든 것이 깨어난다" 류의 감성 오프닝·챕터 전환 / 브랜드·제품 런칭 필름의 서사형 티저 / 자연·시간의 흐름을 말하는 강의 도입부 / 손그림 애니메 룩 구현 가능성 시연
- **잘하는 표현**: 과수채 느낌의 레이어드 숲 배경과 안개·역광 / 셀 셰이딩 메카에 이끼·꽃 웨더링 / 정적 홀드 → 진동 → 폭발적 이륙으로 쌓는 서사 페이싱 / 새떼·나뭇잎·흙 낙하 같은 이차 움직임
- **스타일**: 핑크·살구빛 새벽 하늘과 짙은 초록 숲, 크림·적갈색 도색이 벗겨진 로봇. 페인팅 배경 위 셀 컬러 캐릭터의 극장판 지브리 감성 2D, 텍스트 없음.
- **프롬프트 구조**: SCENE 서술 → ANIME QUALITY STANDARD(로봇·선화·채색·배경·조명·애니메이션·연출) → IT MUST NOT LOOK LIKE 금지 목록 → 무작위 프레임 자가검수 반복 지시
- **태그**: 지브리풍, 2D애니메, 메카, 숲, 일출, 시네마틱, 서사형, single-HTML
- **주의**: 메타의 모델 표기가 opus-5.5·fable-5.5 병기(그룹 2건)라 Opus 단독 결과인지 불분명. 지브리 '스타일 참조'를 명시한 프롬프트

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

#### [Red Fox Wakes a Forgotten Library](stories__red-fox-wakes-a-forgotten-library__2117224839010459987.md)
`stories__red-fox-wakes-a-forgotten-library__2117224839010459987` · 약 1.83:1 (1320x720) · 58s · 조회 409K · 에셋필요 X

- **요약**: 작은 여우가 잠든 도서관의 빈 책에 발을 올리자 책장이 종이새로 흩어져 거대한 새가 되고, 마지막 빈 페이지에 'Fable 5.5'가 붓글씨로 써지는 2D 애니메 런칭 필름
- **어울리는 경우**: 제품·모델 런칭 필름의 감성 서사형 엔딩 타이틀 / "모든 이야기는 빈 페이지에서 시작한다" 같은 메시지형 오프닝 / 책·지식·기록 주제 강의의 챕터 인트로 / 동물 캐릭터 우화형 설명
- **잘하는 표현**: 샷 단위(0:00–1:00) 타임코드 스토리보드 연출 / 달빛 블루→랜턴 앰버→황금 일출 조명 변화 / 종이 페이지가 소용돌이치며 새로 변하는 군집 연출 / 마지막 붓글씨 타이틀 + 도장 리빌
- **스타일**: 검은 레터박스 시네마 프레임 안에 보랏빛 밤 구름바다·어두운 서가·황금빛 하늘. 셀 컬러 여우와 과수채 배경의 지브리풍 2D, 텍스트는 마지막 종이 위 손글씨만.
- **기술**: Python, 단일 HTML 파일(사운드 포함)
- **프롬프트 구조**: 컨셉 한 줄 → Shot 1~9를 초 단위 타임코드로 서술 → 애니메 품질 기준 → SOUND 설계(피아노 모티프·현악·효과음) → 금지 목록 → 자가검수 지시
- **태그**: 지브리풍, 2D애니메, 런칭필름, 여우, 종이새, 도서관, 타이틀리빌, 스토리보드
- **주의**: 메타 모델 표기가 opus-5.5·fable-5.5 병기. 화면 상하에 두꺼운 검은 레터박스가 있음

#### [Clawd character animation](stories__clawd-character-animation__2110389810258968965.md)
`stories__clawd-character-animation__2110389810258968965` · 16:9 · 60s · 조회 183K · 에셋필요 X

- **요약**: 주황색 복셀 마스코트 Clawd가 터미널 화면에서 튀어나와 키보드 위를 걷고, 풀밭·나무로 나가 수많은 분신으로 증식하는 텍스트 없는 1분 3D 캐릭터 영상
- **어울리는 경우**: 브랜드 마스코트 소개 영상 / 개발툴·터미널 주제 강의의 무드 인서트 / "작은 것이 퍼져 나간다" 메타포 장면 / 텍스트 없는 브랜드 루프 영상
- **잘하는 표현**: 복셀 캐릭터의 귀여운 걸음·점프 / 키보드 키캡 매크로와 얕은 심도 / 디지털(터미널)→자연(풀밭) 장면 전환 / 수백 개 복제 캐릭터 군집
- **스타일**: 어두운 책상·키보드의 매크로 3D와 밝은 하늘·풀밭의 실사풍 자연 3D가 교차, 테라코타 주황 복셀 캐릭터가 단일 강조색. 텍스트·폰트 없음.
- **프롬프트 구조**: 짧은 자유 서술형 — 마스코트·3D 렌더·텍스트 금지·온라인 무료 사운드 사용·"slop 금지"만 지정한 열린 요청
- **태그**: Clawd, 마스코트, 복셀, 3D, 캐릭터애니메이션, 터미널, 키보드, 텍스트없음
- **주의**: Anthropic 마스코트(Clawd) IP. 사운드는 온라인 무료 에셋을 받아 씀

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

#### [Code-built vertical cartoon short](stories__code-built-vertical-cartoon-short__2118357912624005300.md)
`stories__code-built-vertical-cartoon-short__2118357912624005300` · 9:16 · 34s · 조회 66K · 에셋필요 X

- **요약**: 1932년 호주 '에뮤 전쟁' 실화를 Three.js 3D 들판과 캔버스로 그린 2D 캐릭터 카드로 만든 세로형 내레이션 카툰 쇼츠
- **어울리는 경우**: 역사·실화 썰 풀기 쇼츠 / 강의 속 "웃긴 실제 사례" 재연 인서트 / 내레이션 기반 교양 카툰 / 마지막 '공식 보고서' 같은 문서 펀치라인
- **잘하는 표현**: 3D 로우폴리 세트 + 평면 2D 캐릭터 혼합 / 표정 바뀌는 굵은 외곽선 캐릭터 / 수백 마리 에뮤 군집 부감샷 / 보이스오버 길이에 정확히 맞춘 샷 타이밍
- **스타일**: 황금빛 밀밭·붉은 흙길·푸른 하늘, 후반엔 노을빛 오렌지. 굵은 갈색 외곽선의 Cyanide&Happiness풍 2D 캐릭터와 낮은 채도의 3D 배경, 마지막은 타자기체 종이 보고서.
- **기술**: Three.js r160, Playwright·Chromium(swiftshader) 프레임 렌더, ffmpeg, Python·NumPy·Pillow, Node.js
- **프롬프트 구조**: JSON 스펙 — task·my_inputs(이야기·대본·보이스오버) → stages(대본 작성 규칙·녹음 안내·빌드) → setup 명령 → silencedetect 기반 대본-음성 정렬 타이밍 규칙 등
- **태그**: 카툰쇼츠, 실화, 역사, Three.js, 2D캐릭터, 내레이션, 세로영상, 코미디
- **주의**: 사용자의 보이스오버(ElevenLabs 권장)가 사실상 필요. 오디오는 silencedetect로 맞추는 방식

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

#### [Stickman survival thriller](stories__stickman-survival-thriller__2115786060231770351.md)
`stories__stickman-survival-thriller__2115786060231770351` · 9:16 · 83s · 조회 64K · 에셋필요 X

- **요약**: "내일의 내가 보낸 문자" 규칙을 따라가는 2인칭 졸라맨 서바이벌 스릴러 시리즈 1화로, 3D 로우폴리 아파트와 HUD 시계·룰 스티커·단어 자막으로 긴장을 쌓는 세로 쇼츠
- **어울리는 경우**: 규칙·단계 설명을 서스펜스로 풀 때 / 시리즈형 쇼츠 포맷 / "만약 당신이…" 가정형 훅 도입부 / 폰 화면 POV로 메시지를 보여주는 장면
- **잘하는 표현**: 시각이 흐르는 모노스페이스 HUD / 한두 단어씩 뜨는 굵은 키워드 강조 자막 / 'RULE #1' 기울어진 스티커 타이틀 / 어두운 실내의 단일 강조광(문틈·화면·복도등) 조명
- **스타일**: 남색·검정의 어두운 3D 로우폴리 실내에 흰 몸통·검은 외곽선의 평면 졸라맨, 노랑·연두 키워드 자막과 빨간 룰 스티커. 2D 폰 UI, 공포 스릴러 무드.
- **기술**: Claude Code, Three.js, cannon-es, Playwright, ffmpeg, ElevenLabs·Kokoro TTS, faster-whisper
- **프롬프트 구조**: XML 태그 섹션(<inputs>·<format>·<story>·<look>·<shots> 등)으로 포맷 규칙·스토리 구조·룩·샷 라이브러리를 정의한 시리즈 템플릿
- **태그**: 졸라맨, 스릴러, 쇼츠, HUD, 키워드자막, 3D로우폴리, 2인칭, 시리즈
- **주의**: 내레이션 TTS(ElevenLabs 또는 로컬 Kokoro) 사용

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

#### [Red panda Koda and the giant peach](stories__red-panda-koda-and-the-giant-peach__2109993586951663626.md)
`stories__red-panda-koda-and-the-giant-peach__2109993586951663626` · 약 1:1.11 (720x800) · 29s · 조회 40K · 에셋필요 O

- **요약**: 레서판다 Koda가 거대 복숭아를 따려다 덤불에 떨어지고, 대나무 사다리로 따낸 복숭아를 타고 언덕을 굴러 내려가는 픽사풍 3D 슬랩스틱 단편
- **어울리는 경우**: 캐릭터 시트 기반 생성 영상의 일관성 시연 / 시행착오→재도전 구조의 짧은 우화 / 아동·가족 콘텐츠 티저
- **잘하는 표현**: 캐릭터 시트 레퍼런스로 외형 일관성 유지 / 고정된 지형 안의 물리적 개그 연출 / 초 단위로 쪼갠 액션 비트 서술
- **스타일**: 햇살 가득한 초록 산비탈과 푸른 하늘, 주황 복숭아와 붉은 털의 극사실 털 질감 3D. 화면 아래에 흰 바탕 캐릭터 시트(컬러 팔레트·표정·포즈)가 상시 붙어 있음.
- **기술**: Seedance 2.5, Vidfield.ai
- **프롬프트 구조**: 캐릭터 외형 고정 지시 → 고정 지형 묘사 → 이야기 요약 → 0:00부터 초 단위 샷 서술
- **태그**: 레서판다, 픽사풍, 3D, 캐릭터시트, 슬랩스틱, 생성영상, Seedance
- **주의**: 코드 제작이 아니라 Seedance 생성 영상(Opus는 프롬프트 작성). 하단 절반은 캐릭터 시트 비교 패널, 상단에 Vidfield 워터마크

#### [Skit about overseas AI attitudes toward Chinese users](stories__skit-about-overseas-ai-attitudes-toward-chinese-users__2111111416120053953.md)
`stories__skit-about-overseas-ai-attitudes-toward-chinese-users__2111111416120053953` · 16:9 · 58s · 조회 19K · 에셋필요 O

- **요약**: Claude·GPT·Gemini·Grok를 의인화한 치비 소녀 캐릭터들이 각자의 집 앞에서 '대뚱어(중국 사용자)'를 대하는 태도를 보여주는 중국어 풍자 소극장
- **어울리는 경우**: AI 서비스 비교를 캐릭터 의인화로 풀 때 / 가벼운 풍자·밈 콘텐츠 / 대사 자막이 있는 짧은 콩트
- **잘하는 표현**: 서비스별 캐릭터·집(성·모던하우스·통나무집·클럽)으로 성격 대비 / 장면별 TTS 대사 + 이중 자막 / 원형 축소 엔딩 트랜지션
- **스타일**: 밝은 파스텔 하늘·꽃밭·유럽풍 저택, 클럽 장면은 보라 네온. 메이드복 치비 애니 일러스트 캐릭터, 하단 노란 중국어+영어 자막.
- **기술**: EdgeSpeak, Qwen3-TTS
- **프롬프트 구조**: 중국어 장면별 대본(Claude·GPT·Gemini·Grok 씬) — 각 씬의 배경·동작·대사와 TTS 음성 지정
- **태그**: 콩트, 의인화, 치비, 애니일러스트, AI비교, 풍자, 중국어, TTS
- **주의**: 캐릭터 일러스트·음성 모델·BGM 등 외부 에셋 필요. AI 서비스 의인화 풍자로 정치·국가 민감 소재

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

#### [Character video combining Midjourney and Seedance](stories__character-video-combining-midjourney-and-seedance__2110360021988982817.md)
`stories__character-video-combining-midjourney-and-seedance__2110360021988982817` · 16:9 · 32s · 조회 17K · 에셋필요 O

- **요약**: Midjourney·Seedance로 만든 두 소녀의 결투 애니메 클립에 Opus가 컬러 그레이딩·집중선·컷 편집·일본어 타이틀을 입힌 애니 오프닝풍 편집본
- **어울리는 경우**: 생성 영상 클립을 애니 오프닝처럼 다듬을 때 / 액션 하이라이트 편집 / "1화" 타이틀·'つづく' 엔딩 카드 연출
- **잘하는 표현**: 만화 집중선·임팩트 프레임 / 붉은 눈·입술 강조 그레이딩 / 빠른 컷과 꽃잎 파티클 / 일본어 타이틀·To Be Continued 카드
- **스타일**: 짙은 코발트 블루 배경에 핑크 드레스와 진홍 강조색, 셀 애니 일러스트 룩. 날카롭고 몽환적인 애니 오프닝 무드.
- **기술**: Midjourney, Seedance
- **프롬프트 구조**: 한 문장 편집 지시("컬러 그레이딩·다이내믹 컷·트랜지션·VFX·모션그래픽으로 애니 느낌")
- **태그**: 애니오프닝, 생성영상편집, 집중선, 컬러그레이딩, 액션, 핑크블루
- **주의**: 원본 클립은 Midjourney·Seedance 생성물(외부 생성 모델 필요). Opus는 편집만 담당

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

#### [Halloween trick-or-treat animated video](stories__halloween-trick-or-treat-animated-video__2110404428691808308.md)
`stories__halloween-trick-or-treat-animated-video__2110404428691808308` · 16:9 · 72s · 조회 14K · 에셋필요 X

- **요약**: Clawd가 할로윈 밤 다른 AI 봇(Grok·Codex 등)으로 분장하며 집집마다 사탕을 받으러 다니는, 장면마다 화풍이 바뀌는 코믹 애니메이션
- **어울리는 경우**: AI 도구들을 패러디로 소개할 때 / 시즌(할로윈) 이벤트 콘텐츠 / 한 영상 안에서 여러 화풍을 오가는 옴니버스 연출
- **잘하는 표현**: 장면별 화풍 전환(그림책·8비트 플랫포머·수묵·레고 복셀) / 상단 토큰 카운터 HUD 개그 / 집 문 앞 반복 구조의 코미디 리듬 / 손글씨 엔딩 타이틀
- **스타일**: 보랏빛 밤하늘·보름달 아래 질감 있는 그림책풍 2D 동네가 기본, 중간중간 픽셀 게임·흑백 수묵·복셀 3D로 전환. 따뜻하고 장난스러운 무드.
- **기술**: anidoodle
- **프롬프트 구조**: 짧은 한두 줄 요청 + "주요 캐릭터 스틸 먼저 보여주고 승인받기" 단계 지시
- **태그**: 할로윈, Clawd, 패러디, 2D애니메, 픽셀아트, 화풍전환, 코미디
- **주의**: anidoodle이라는 외부 애니메이션 도구에 의존. Clawd·타 AI 봇 브랜드 패러디(IP)

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

#### [Paper collage Momotaro animation](stories__paper-collage-momotaro-animation__2110931024469540979.md)
`stories__paper-collage-momotaro-animation__2110931024469540979` · 16:9 · 46s · 조회 10K · 에셋필요 O

- **요약**: 팝업 그림책이 열리며 와시 종이 오려붙이기 캐릭터·배경이 일어서는 일본 민담 모모타로 45초 페이퍼 콜라주 애니메이션
- **어울리는 경우**: 옛이야기·우화로 개념을 설명하는 강의 인서트 / 동양 전통·일본 문화 주제 / 그림책 넘기듯 챕터를 여는 도입부 / 아동 교육 콘텐츠
- **잘하는 표현**: 종이 레이어 패럴랙스·심도 블러·그림자로 만든 2.5D / 우키요에풍 파도와 종이 질감 / 의성어('どんぶらこ') 타이포 / 책 펼침·닫힘 북엔드 구성
- **스타일**: 어두운 배경 위 펼친 그림책, 남색 파도·석양빛 하늘·초록 들판의 와시 종이 질감. 오려낸 종이 캐릭터의 따뜻한 동양 그림책 감성.
- **기술**: Python(패럴랙스 애니메이션), Codex(이미지 생성), ElevenLabs(내레이션·BGM)
- **프롬프트 구조**: [Look]·[How to build it]·[Rules] 섹션 — 대본 승인 → 이미지 프롬프트 작성 → 사용자가 이미지 생성해 전달 → Python 애니메이션 → 장면별 스틸 확인 순서
- **태그**: 페이퍼콜라주, 키리에, 그림책, 일본민담, 2.5D, 패럴랙스, 동양전통, 나레이션
- **주의**: 캐릭터·배경 컷아웃 이미지는 외부 이미지 생성(Codex)으로 사용자가 만들어 넘겨야 함

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

### art3d (3D/아트) — 52건 (조회수순)


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

#### [3D walkthrough house from floor plan](art3d__3d-walkthrough-house-from-floor-plan__2110036224320884998.md)
`art3d__3d-walkthrough-house-from-floor-plan__2110036224320884998` · 16:9 · 14s · 조회 322K · 에셋필요 O

- **요약**: 평면도와 실사 사진을 바탕으로 Three.js로 지은 열대 해변 주택을 1인칭으로 걸어 다니며, 좌상단 평면도 미니맵과 함께 거실·테라스·수영장·주방을 둘러보는 워크스루 영상
- **어울리는 경우**: 부동산·인테리어·건축 강의의 공간 투어 컷 / 평면도→3D 공간 변환 설명 / 웹 기반 가상 투어·디지털 트윈 소개 / 빌더-크리틱 반복 루프 같은 에이전트 작업 방식 사례
- **잘하는 표현**: 실사에 가까운 자연광과 바닥에 떨어지는 긴 창 그림자 / 부드러운 1인칭 카메라 이동 / 평면도 미니맵 인셋으로 현재 위치를 함께 보여주는 구성
- **스타일**: 화이트·베이지 톤 모던 인테리어에 오크 바닥, 야자수와 청록 수영장이 보이는 밝은 오후 햇살. 아키텍처 비주얼라이제이션 같은 포토리얼 3D.
- **기술**: Three.js
- **프롬프트 구조**: 목표(사진과 일치하는 실측 워크스루)와 작업 방식(구역 분할, 구역마다 빌더와 새 맥락의 크리틱을 두고 사진 대조 반복)만 짧게 지시한 한 문단
- **태그**: 건축, 인테리어, 워크스루, 평면도, 포토리얼, 3D, Three.js, 가상투어, 에이전트루프
- **주의**: 실제 주택의 평면도와 사진이 있어야 재현 가능(외부 에셋 필수). 화면 녹화형 워크스루라 편집된 모션그래픽은 아님

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

#### [Code-only three.js temple at dusk](art3d__code-only-three-js-temple-at-dusk__2112545748944556038.md)
`art3d__code-only-three-js-temple-at-dusk__2112545748944556038` · 16:9 · 70s · 조회 123K · 에셋필요 O

- **요약**: 3D 모델·텍스처 없이 코드로만 만든 일본식 사찰(본전·오층탑·아치 다리·연못)을 등롱·연꽃·불상 얼굴 같은 소품 클로즈업에서 시작해 풀백하는 10컷 시네마틱 영상
- **어울리는 경우**: 동양 문화·역사·여행 강의의 분위기 인서트 / 강의 오프닝·챕터 전환용 시네마틱 B롤 / '디테일에서 전체로' 줌아웃 리빌 연출 / 멀티 에이전트 병렬 제작 사례 소개
- **잘하는 표현**: 클로즈업→가속 풀백→감속 정지의 이징이 있는 리빌 카메라 / 금박·주칠·청동 재질의 따뜻한 역광 / 연꽃 연못과 단풍 등 환경 디테일
- **스타일**: 노을빛 황금 햇살 아래 주홍 칠 목조 건물과 금박 장식, 푸른 하늘과 흰 구름, 붉은 단풍. 화려하고 따뜻한 시네마틱 3D.
- **기술**: Claude Code, Three.js, 서브에이전트 병렬 작업
- **프롬프트 구조**: 중국어 3단락(평면도 layout.js 먼저 정의 → 6개 서브에이전트가 구역별 병렬 시공, 공용 materials.js·고정 시드 → 10컷×7초 카메라 연출 규칙)
- **태그**: 사찰, 일본, 동양전통, 골든아워, 시네마틱, 풀백리빌, Three.js, 코드온리, 3D환경
- **주의**: 결과 영상이 'Golden hour Japanese temple 3D scene'(@LexnLin, 5일 먼저 게시) 케이스와 사실상 같은 영상(SSIM 0.99)이라, 이 프롬프트는 원작자의 것이 아니라 재구성일 가능성이 큼. 참고 사진 첨부가 전제

#### [Interactive 3D world built one-shot by Opus 5.5](art3d__interactive-3d-world-built-one-shot-by-opus-5-5__2109718931409699043.md)
`art3d__interactive-3d-world-built-one-shot-by-opus-5-5__2109718931409699043` · 약 2.39:1 (1718x720) · 56s · 조회 109K · 에셋필요 O

- **요약**: 비 내리는 네온 도시를 걷고 차를 몰며 미션 HUD·미니맵·속도계가 뜨는 사이버펑크풍 오픈월드 게임 플레이 화면 녹화
- **어울리는 경우**: AI로 게임 만들기 강의의 결과 시연 / 원샷 생성 능력 과장 없이 보여주는 데모 컷 / 미래 도시·야간 도시 분위기 B롤
- **잘하는 표현**: 젖은 아스팔트 반사와 짙은 안개·네온 빛 번짐 / 게임 HUD(미션 텍스트, 원형 미니맵, 속도계) 레이아웃 / 3인칭 주행 시점의 속도감
- **스타일**: 어두운 밤 도시에 청록·마젠타·노랑 네온 간판, 뿌연 안개와 빗물 반사, 노란 택시와 머슬카. 모션 블러가 강한 게임 엔진풍 다크 3D.
- **기술**: Three.js, Blender, Magnific(사운드)
- **프롬프트 구조**: "사이버펑크 2077 같은 게임을 만들어라, Blender만 쓰고 사운드는 Magnific" 한 줄 지시
- **태그**: 사이버펑크, 게임, 오픈월드, 네온, 비오는밤, HUD, 3D, 원샷
- **주의**: 실제 게임 플레이 화면 녹화이며 모션 블러·안개로 화질이 뿌연 구간이 많음. 프롬프트가 실존 게임 IP(Cyberpunk 2077)를 지목하고 Magnific 등 외부 툴을 씀. 한 줄 프롬프트로 이 결과가 나왔다는 주장은 검증 불가

#### [Blue whale jelly soft-body study](art3d__blue-whale-jelly-soft-body-study__2119542001775628299.md)
`art3d__blue-whale-jelly-soft-body-study__2119542001775628299` · 16:9 · 17s · 조회 90K · 에셋필요 X

- **요약**: 반투명 2겹 젤리로 만든 대왕고래를 잡아 늘리고 비틀면, 목주름이 부풀어 크릴을 삼키고 분수공으로 젤리 방울을 뿜는 Three.js 소프트바디 머티리얼 스터디
- **어울리는 경우**: 해양생물·동물 해부 강의의 귀여운 시각 인서트 / 물리 시뮬레이션·소프트바디 개념 설명 / 브랜드 마스코트·캐릭터 티저 / 'Material Studies' 시리즈 형식의 제품 쇼케이스
- **잘하는 표현**: 젤리 굴절과 Beer–Lambert 흡수로 속이 비치는 재질 / 꿀렁이는 변형과 부풀어 오르는 부피 변화 / 튀고 구르는 젤리 방울 파티클 / 오션·아틱·트와일라잇 색상 프리셋 전환
- **스타일**: 밝은 웜그레이 스튜디오 바닥(#E2DFDA)에 코발트·하늘색 반투명 고래, 이탤릭 세리프 'Blue Whale Jelly.' 마스트헤드와 우측 모노 컨트롤 패널. 미니멀 에디토리얼 제품사진풍 3D.
- **기술**: Three.js r170, WebGL2, 커스텀 ShaderMaterial, CPU XPBD 사면체 소프트바디, SDF 모델링
- **프롬프트 구조**: 형태(SDF)·내부 구조·물리·꿀꺽 동작·분수·소등 모드·렌더러·팔레트·카메라·UI를 소제목별 불릿으로 나눈 아주 상세한 스펙
- **태그**: 젤리, 고래, soft-body, Three.js, material-study, 에디토리얼, 인터랙티브, 3D, 해양생물
- **주의**: 상단에 'Claude Opus 5.5 · 7.61$' 모델명·비용 라벨이 붙은 화면 녹화. 화면에는 Opus 결과 한 패널만 나옴. 프롬프트의 소등(Lights out) 모드는 영상에서 확인되지 않음

#### [Live generative code art from a typed word](art3d__live-generative-code-art-from-a-typed-word__2103837519615774895.md)
`art3d__live-generative-code-art-from-a-typed-word__2103837519615774895` · 9:16 · 97s · 조회 84K · 에셋필요 X

- **요약**: 블랙홀·성운·은하·지구 일출을 거쳐 'and there was LIGHT' 타이포로 끝나는 세로형 우주 창세 제너러티브 아트
- **어울리는 경우**: 감성 오프닝/숏폼 훅 / 과학·우주 테마 인트로 / 브랜드 매니페스토 영상
- **잘하는 표현**: 블랙홀 강착원반·성운 등 셰이더형 우주 표현 / 미시→거시 스케일 서사 전개 / 별빛 텍스처가 채워진 마무리 타이포
- **스타일**: 검은 배경 위 주황 블랙홀, 보라·청록 성운, 나선 은하, 지구 대기권 일출 등 실사풍 우주 비주얼. 마지막은 이탤릭 세리프 'and there was' + 별무늬로 채운 굵은 'LIGHT' 레터링.
- **프롬프트 구조**: 'Wow하게, AI slop 금지, 마음대로' 식의 추상적 자유 위임 프롬프트
- **태그**: 우주, cosmic, generative-art, 블랙홀, 성운, 세로영상, 타이포, 다크
- **주의**: 프롬프트에 기술·장면 지정이 없어 재현성 낮음; 'typed word' 인터랙션은 시트에서 확인 안 됨

#### [Blueprint to animated pirate ship](art3d__blueprint-to-animated-pirate-ship__2109043294911291886.md)
`art3d__blueprint-to-animated-pirate-ship__2109043294911291886` · 16:9 · 24s · 조회 76K · 에셋필요 X

- **요약**: 양피지 위 세피아 잉크 갑판 도면에서 빛나는 와이어프레임이 솟아올라 용골·늑재·외판·돛 순서로 갈레온 해적선이 조립되고, 노을 바다에 띄워 대포를 쏜 뒤 '海賊船' 타이틀로 끝나는 Blender 영상
- **어울리는 경우**: 설계도→완성품으로 이어지는 '만드는 과정' 설명 / 역사·대항해 시대 강의 인서트 / 단계별 조립(구조 분해) 시각화 / 제품·프로젝트 소개 영상의 오프닝
- **잘하는 표현**: 2D 도면 선이 3D 와이어로 일어서는 전환 / 부품이 순서대로 쌓이는 빌드업 애니메이션 / 도면 무대에서 노을 바다로 바뀌는 장면 전환 / 대포 연기와 타이틀 카드 마무리
- **스타일**: 검은 배경 위 크림색 도면과 흰 와이어, 이어서 분홍·주황 노을과 잔잔한 바다 반사, 나무 갈색 선체와 황갈색 돛. 따뜻한 빈티지 톤의 시네마틱 3D.
- **기술**: Blender(EEVEE), Python, DXF 도면 생성, 파이썬 합성 사운드
- **프롬프트 구조**: 일본어로 【図面】(DXF 3종, 축척·도곽)·【動画】(6단계 장면 순서, 해상도·fps·음향)·【進め方】(미리보기 검수, 테스트 스틸, 렌더 시간 승인)을 나눈 제작 지시서
- **태그**: 해적선, 설계도, 와이어프레임, 조립애니메이션, Blender, 노을바다, 빈티지, 3D, 빌드업
- **주의**: 끝에 작가 로고 'Create by Ayuneo' 카드가 붙어 있음. 영상 속 첫 장면은 두루마리가 펼쳐지기보다 액자형 도면에 가깝게 보임

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

#### [Alpine lake scene built in code](art3d__alpine-lake-scene-built-in-code__2112560562609803311.md)
`art3d__alpine-lake-scene-built-in-code__2112560562609803311` · 약 2.39:1 (1720x720) · 60s · 조회 67K · 에셋필요 O

- **요약**: 참고 사진 10장을 코드만으로 재현한 청록빛 알프스 호수·침엽수림·폭포·암봉 환경을 드론 촬영처럼 6~7초마다 장소를 바꿔 보여주는 1분짜리 울트라와이드 시네마틱
- **어울리는 경우**: 자연·지리·여행 강의의 풍경 B롤 / 힐링·명상 콘텐츠 배경 / 절차적 환경 생성 능력 데모 / 바위 뒤에서 솟아오르며 전경을 드러내는 리빌 컷
- **잘하는 표현**: 투명한 터키석색 호수 물 표현 / 빽빽한 침엽수림과 원경까지 이어지는 디테일 / 근경 바위에서 상승해 전경을 여는 드론식 카메라 / 맑은 하늘과 뭉게구름 조명
- **스타일**: 쨍한 파란 하늘, 회색 화강암 봉우리, 짙은 녹색 숲과 에메랄드·청록 호수. 밝고 채도 높은 포토리얼 지향 3D 풍경.
- **프롬프트 구조**: 두 과제(환경 구축, 1분 영상)와 환경 항목(색·물·나무·산·바위·원경), 영상 연출, 작업 방식(라운드별 스크린샷, 승인 후 렌더)을 불릿으로 나열하고 '99.9% 닮을 때까지 반복'을 강조
- **태그**: 호수, 산, 숲, 자연풍경, 드론샷, 울트라와이드, 시네마틱, 코드온리, 3D환경
- **주의**: 참고 이미지 10장이 전제(외부 에셋). 사용 도구가 메타에 명시되지 않음. 가까이서 보면 나무가 CG 티가 나는 컷이 있음

#### [Pixel art scene generation](art3d__pixel-art-scene-generation__2102746041250705890.md)
`art3d__pixel-art-scene-generation__2102746041250705890` · 16:9 · 13s · 조회 61K · 에셋필요 X

- **요약**: 비 내리는 할로윈 밤, 떠 있는 섬 위 오두막을 그린 루프형 픽셀아트 디오라마(로파이 음악 커버용)
- **어울리는 경우**: 로파이/작업용 음악 롱폼 영상의 루프 배경 / 유튜브 라이브·대기 화면 앰비언트 배경 / 시즌(할로윈) 분위기 채널 아트
- **잘하는 표현**: 따뜻한 불빛 vs 차가운 밤의 색 대비 / 비·불꽃·연기·깜빡이는 빛 등 반복 파티클 효과 / 카메라 고정 상태에서 끊김 없는 루프
- **스타일**: 짙은 남보라 밤하늘에 보름달·구름, 공중에 뜬 흙섬 위 목조 오두막과 주황 창문·모닥불·우산, 청록 발광 수정이 박힌 2D 픽셀아트. 6프레임 내내 구도가 고정되고 빗줄기와 불빛만 미세하게 바뀌는 차분한 앰비언트 분위기.
- **프롬프트 구조**: 용도(10시간 로파이 루프 커버)·팔레트 원칙(웜/쿨 대비)·효과 목록만 적은 3문장 짧은 브리프
- **태그**: 픽셀아트, pixel-art, 루프, lofi, 할로윈, 앰비언트, 야경, 파티클, diorama
- **주의**: 구현 기술이 프롬프트에 없음(출처 블로그는 Sprite Fusion). 움직임이 거의 없어 모션 레퍼런스로는 약함

#### [Interactive weather world in a glass box](art3d__interactive-weather-world-in-a-glass-box__2108159248148611292.md)
`art3d__interactive-weather-world-in-a-glass-box__2108159248148611292` · 16:9 · 62s · 조회 60K · 에셋필요 X

- **요약**: 어두운 나무 테이블 위 황동 테 유리 상자 속 산·폭포·호수 미니어처 생태계에서 구름을 짜 비를 내리고, 번개·안개·눈·계절 변화를 실시간으로 일으키는 인터랙티브 데모
- **어울리는 경우**: 기후·날씨·물의 순환 설명 / 생태계·환경 강의의 미니어처 비유 / '작은 세계를 손으로 조작한다'는 시뮬레이션 콘셉트 / 계절 변화 타임랩스 인서트
- **잘하는 표현**: 유리 반사와 황동 프레임이 있는 디오라마 구도 / 비·번개·눈·안개 파티클 날씨 전환 / 지층 단면이 보이는 지형 블록 / 여름→가을→겨울 계절 전환
- **스타일**: 어두운 실내 배경에 스포트라이트를 받은 유리 진열장, 초록 숲과 청록 호수, 하얀 뭉게구름, 갈색 지층 단면. 차분하고 고급스러운 미니어처 3D.
- **프롬프트 구조**: 유리 상자 속 살아있는 풍경과 조작 가능한 날씨 목록, 품질 기대치(물·구름·유리·조명·파티클)를 한 문단으로 쓴 짧은 콘셉트형 지시
- **태그**: 디오라마, 미니어처, 날씨, 유리상자, 계절변화, 인터랙티브, 3D, 파티클, 생태계
- **주의**: 인터랙션 시연 화면 녹화라 조작 장면이 섞여 있음. 사용 도구가 메타에 명시되지 않음

#### [Physics-based falling oak tree](art3d__physics-based-falling-oak-tree__2115768888507941008.md)
`art3d__physics-based-falling-oak-tree__2115768888507941008` · 4:5 · 16s · 조회 58K · 에셋필요 X

- **요약**: 크림색 스튜디오 배경의 이끼 낀 흙더미 위 참나무가 세게 흔들리며 수천 장의 잎이 팔랑이며 떨어져 바닥에 쌓이는 Blender 물리 시뮬 영상
- **어울리는 경우**: 변화·상실·탈피 같은 개념의 은유 인서트 / 자연·계절·식물 강의 / 물리 시뮬레이션 능력 소개 / 세로형 숏폼의 차분한 루프 컷
- **잘하는 표현**: 가지의 휨과 되튐이 있는 자연스러운 흔들림 / 회전하며 좌우로 흩날리는 낙엽 파티클 / 바닥에 쌓이는 잎 카펫 / 제품사진 같은 소프트박스 조명과 접지 그림자
- **스타일**: 따뜻한 크림·오프화이트 무한 배경에 짙은 초록 참나무와 원형 이끼 받침. 미니멀하고 고요한 포토리얼 제품샷 3D.
- **기술**: Blender, Cycles, 베이크 물리
- **프롬프트 구조**: 배경·나무 디테일·조명·타임라인(0~3초 정지, 3초 흔들림…)·물리·사운드·포맷을 문단별로 서술한 영상 연출 스펙
- **태그**: 참나무, 낙엽, 물리시뮬, Blender, 스튜디오, 미니멀, 포토리얼, 세로영상, 자연
- **주의**: 화면에 '@MrTacticalX' 워터마크가 있음. 프롬프트의 '반쯤 벌거벗은 나무'와 달리 잎이 많이 남고 도토리는 잘 보이지 않음

#### [Interactive squishy jelly whale](art3d__interactive-squishy-jelly-whale__2114674922802782355.md)
`art3d__interactive-squishy-jelly-whale__2114674922802782355` · 약 1.60:1 (1152x720) · 18s · 조회 54K · 에셋필요 X

- **요약**: 젤리로 만든 혹등고래를 잡아 들어 올리고 흔들며, 오션·슬레이트·라군 색으로 바꾸고 분수공에서 젤리 방울을 뿜는 WebGPU 소프트바디 머티리얼 스터디
- **어울리는 경우**: 해양생물·동물 강의의 귀여운 인서트 / 소프트바디·물리 엔진 개념 설명 / 캐릭터·마스코트 티저 / 색상 옵션을 고르는 제품 컬러웨이 소개
- **잘하는 표현**: 들어 올렸을 때 축 늘어지는 말랑한 변형 / 반투명 젤리 속 우윳빛 층과 굴절 / 색상 프리셋 전환 / 바닥에 튀는 젤리 방울 파티클
- **스타일**: 밝은 웜그레이 스튜디오 배경에 파랑·회청·민트 반투명 고래, 이탤릭 세리프 'Whale Jelly.' 마스트헤드와 우측 컨트롤 패널. 미니멀 에디토리얼 제품사진풍 3D.
- **기술**: WebGPU, WGSL, XPBD 소프트바디, SDF·surface nets, 단일 HTML 파일
- **프롬프트 구조**: 지오메트리·시뮬레이션·룩(셰이더 디테일)·인터랙션·UI를 문단별로 압축 서술한 상세 기술 스펙
- **태그**: 젤리, 고래, soft-body, WebGPU, material-study, 에디토리얼, 인터랙티브, 3D
- **주의**: 상단에 'Opus 5.5 · 9.26$' 모델명·비용 라벨이 붙은 화면 녹화. 화면에는 Opus 결과 한 패널만 나옴. 같은 작가의 대왕고래 버전과 거의 같은 구성

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

#### [Apartment drafted in CAD then built in 3D](art3d__apartment-drafted-in-cad-then-built-in-3d__2111880621954081240.md)
`art3d__apartment-drafted-in-cad-then-built-in-3d__2111880621954081240` · 16:9 · 73s · 조회 51K · 에셋필요 X

- **요약**: AutoCAD풍 다크 화면에서 그리드·기둥·벽·문창·가구·치수 순으로 92㎡ 아파트 도면을 그린 뒤, 도면이 3D로 바뀌어 벽과 바닥이 세워지고 가구가 제자리에 떨어지는 단일 HTML 영상
- **어울리는 경우**: 건축·인테리어·설계 과정 설명 / '2D 계획이 3D 결과가 된다'는 개념 시각화 / CAD·설계 툴 튜토리얼 인트로 / 단계별 빌드업 과정 보여주기
- **잘하는 표현**: 실제 제도 순서를 따르는 선 그리기 애니메이션 / CAD UI(레이어 패널, 명령줄, 크로스헤어) 재현 / 도면→3D 전환과 단계별 시공 / 방 이름 라벨이 붙은 아이소메트릭 컷어웨이
- **스타일**: 짙은 차콜 CAD 화면에 흰·빨강·노랑 선, 이후 검은 배경 위 흰 벽과 노란 단열층, 오크 바닥의 깔끔한 3D 모형. 정밀하고 차분한 다크 테크 무드.
- **기술**: Three.js, WebCodecs, mp4-muxer, 단일 HTML 파일
- **프롬프트 구조**: 한 문단에 CAD 화면 연출(명령어·제도 순서·실측 치수) → 3D 시공 순서 → 단일 타임라인과 프레임 단위 MP4 렌더 버튼까지 순서대로 서술
- **태그**: 건축, CAD, 평면도, 도면, 3D전환, 빌드업, Three.js, 인테리어, 다크UI
- **주의**: 화면 UI 글자가 작아 축소 시 잘 안 읽힘. 'AutoCAD 스타일'은 실제 제품 UI를 흉내 낸 것

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

#### [Golden hour Japanese temple 3D scene](art3d__golden-hour-japanese-temple-3d-scene__2110657641831956870.md)
`art3d__golden-hour-japanese-temple-3d-scene__2110657641831956870` · 16:9 · 70s · 조회 46K · 에셋필요 O

- **요약**: 코드로만 지은 골든아워 일본 사찰을 10개 지점에서 7초씩, 소품 클로즈업에서 풀백해 전경을 드러내는 1분 남짓 Three.js 시네마틱 영상
- **어울리는 경우**: 동양 문화·역사·여행 강의의 분위기 인서트 / 오프닝·챕터 전환용 시네마틱 B롤 / 디테일에서 전체로 넓혀 가는 리빌 연출 / 코드만으로 만든 3D 환경 사례 소개
- **잘하는 표현**: 클로즈업→풀백 리빌 카메라 / 금박 장식과 주칠 목재의 따뜻한 역광 / 연꽃 연못·아치 다리·오층탑의 깊이감 있는 구도
- **스타일**: 황금빛 저녁 햇살 아래 주홍 칠 건물과 금박, 푸른 하늘과 흰 구름, 붉은 단풍. 화려하고 따뜻한 시네마틱 3D.
- **기술**: Three.js
- **프롬프트 구조**: 컷 구성(10지점×7초, 풀백), 골든아워·실사감·빛과 그림자, 참고 이미지 99.9% 일치까지 반복, 코드 전용(음악만 예외)을 짧은 문단으로 나열
- **태그**: 사찰, 일본, 동양전통, 골든아워, 시네마틱, 풀백리빌, Three.js, 코드온리, 3D환경
- **주의**: 참고 이미지 첨부가 전제이고 배경음악은 외부 무료 트랙. 'Code-only three.js temple at dusk' 케이스와 같은 결과 영상이며, 게시일로 보면 이쪽(@LexnLin)이 원본

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

#### [Interactive 3D jelly orange in browser](art3d__interactive-3d-jelly-orange-in-browser__2110665495221268915.md)
`art3d__interactive-3d-jelly-orange-in-browser__2110665495221268915` · 약 1.58:1 (1136x720) · 18s · 조회 23K · 에셋필요 X

- **요약**: 젤리로 만든 통오렌지를 나키리 칼로 잘라 원형 슬라이스·웨지·작은 조각으로 나누고, 조각마다 따로 흔들리며 블러드 오렌지 등 품종 색으로 바뀌는 WebGPU 소프트바디 스터디
- **어울리는 경우**: '쪼개서 본다'·분해·세분화 개념의 은유 인서트 / 음식·과일 제품 티저 / 단면·내부 구조 설명 / 물리 시뮬레이션 데모
- **잘하는 표현**: 칼질에 따라 실시간으로 생기는 단면과 과육 분절 / 조각별로 따로 흔들리는 젤리 물리 / 껍질·흰 속껍질·과육이 비치는 볼륨 재질 / 품종별 색 프리셋 전환
- **스타일**: 밝은 웜그레이 스튜디오 배경에 선명한 오렌지·루비 레드 반투명 조각, 이탤릭 세리프 'Whole Orange.' 타이틀과 우측 컨트롤 패널. 미니멀 에디토리얼 제품사진풍 3D.
- **기술**: WebGPU, WGSL, XPBD 소프트바디, SDF 절단, 단일 HTML 파일
- **프롬프트 구조**: 형태와 조각·해부 구조·물리·칼·렌더링·UI를 소제목별 불릿으로 나눈 매우 상세한 기술 스펙
- **태그**: 젤리, 오렌지, 칼질, 단면, soft-body, WebGPU, material-study, 에디토리얼, 인터랙티브
- **주의**: 상단에 'Claude Opus 5.5 · 11.5$' 모델명·비용 라벨이 붙은 화면 녹화. 화면에는 Opus 결과 한 패널만 나옴

#### [Relaxing generative visual made with Jig and Opus 5.5](art3d__relaxing-generative-visual-made-with-jig-and-opus-5-5__2109943963536998694.md)
`art3d__relaxing-generative-visual-made-with-jig-and-opus-5-5__2109943963536998694` · 약 1.21:1 (870x720) · 34s · 조회 21K · 에셋필요 X

- **요약**: 옆면을 걷어낸 에스컬레이터 내부 구조를 흰 라인 3D로 보여주고, 주황색으로 강조한 계단 한 칸이 레일을 따라 한 바퀴 도는 과정을 설명 카드와 함께 따라가는 인터랙티브 해부도
- **어울리는 경우**: 기계·제품의 작동 원리 설명 / '보이지 않는 내부'를 여는 해부도 인서트 / 한 요소를 하이라이트해 흐름을 따라가는 프로세스 설명 / 공학·과학 교육 콘텐츠
- **잘하는 표현**: 흰 단색 3D 위 단일 강조색(주황·노랑) 하이라이트 / 부품 하나를 카메라가 따라가는 추적 이동 / 단계별 설명 카드와 페이지 점 내비게이션 / 깔끔한 테크니컬 일러스트 렌더
- **스타일**: 오프화이트 배경에 흰·연회색 선형 3D 구조물, 노란 계단 가장자리와 주황 강조 블록, 하단 둥근 설명 카드. 밝고 정돈된 교과서형 테크니컬 일러스트.
- **기술**: Jig
- **프롬프트 구조**: "에스컬레이터를 해부도 스타일 Jig로, 카메라 무빙과 강조색으로 핵심 부품 표시" 한 줄 지시
- **태그**: 해부도, 작동원리, 에스컬레이터, 기계구조, 하이라이트, 설명카드, 3D, 교육, 오프화이트
- **주의**: Jig라는 외부 툴 위에서 만든 결과이고 앱 화면 녹화라 커서와 편집 버튼이 보임. 제목의 '릴랙싱 제너러티브 비주얼'과 달리 실제로는 설명형 해부도

#### [Pixel-art basketball court diorama with weather](art3d__pixel-art-basketball-court-diorama-with-weather__2112989996366102944.md)
`art3d__pixel-art-basketball-court-diorama-with-weather__2112989996366102944` · 약 1.60:1 (1152x720) · 18s · 조회 20K · 에셋필요 X

- **요약**: 떠 있는 도시 블록 위 길거리 농구 하프코트를 아이소메트릭 픽셀아트로 렌더링하고, AI 선수들이 2대2 경기를 하며 낮·노을·밤과 비·폭우로 날씨가 바뀌는 Three.js 디오라마
- **어울리는 경우**: 스포츠·게임 관련 강의 인서트 / 시간·날씨 변화를 한 장면으로 보여주는 컷 / 레트로 게임 감성의 귀여운 B롤 / 시뮬레이션·게임 AI 데모
- **잘하는 표현**: 3D를 저해상도 팔레트로 양자화한 픽셀아트 렌더 / 회전하는 아이소메트릭 디오라마 카메라 / 낮→밤 조명 전환과 비·물웅덩이 반사 / 절차적 캐릭터 애니메이션
- **스타일**: 연회색 배경에 떠 있는 잔디·흙 단면 블록, 청록·테라코타 코트와 벽돌 상점, 보라빛 노을 도시 벽화. 선명한 외곽선의 로우폴리 픽셀아트 아이소메트릭.
- **기술**: Three.js r160, 오소그래픽 카메라, OKLab 팔레트 양자화, 포스트 프로세싱
- **프롬프트 구조**: RENDER PIPELINE·SCENE·PLAYERS·GAME·WEATHER AND TIME·UI 대문자 섹션별로 렌더 방식과 게임 규칙까지 나열한 상세 스펙
- **태그**: 픽셀아트, 아이소메트릭, 디오라마, 농구, 날씨, 낮밤전환, Three.js, 레트로, 게임
- **주의**: 상단에 'Claude Opus 5.5 · 10.1$' 모델명·비용 라벨이 붙은 화면 녹화. 화면에는 Opus 결과 한 패널만 나옴

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

#### [Nanite-style WebGPU rendering engine](art3d__nanite-style-webgpu-rendering-engine__2118870207045529812.md)
`art3d__nanite-style-webgpu-rendering-engine__2118870207045529812` · 16:9 · 83s · 조회 15K · 에셋필요 X

- **요약**: Rust와 WebGPU로 만든 언리얼 Nanite·루멘풍 렌더링 엔진 데모로, 사막 협곡의 그리스식 신전과 불 켜진 석조 회랑을 디버그 패널을 띄운 채 비행하며 보여주는 화면 녹화
- **어울리는 경우**: 그래픽스·게임 엔진 기술 강의 / '브라우저에서 언리얼급 품질' 같은 기술 데모 소개 / 고대 유적·신전 분위기 B롤
- **잘하는 표현**: 실시간 전역 조명과 따뜻한 실내 불빛 / 고밀도 바위 지오메트리 / 역광 햇살과 안개의 대기 원근 / 낮·황혼 조명 전환
- **스타일**: 황갈색 사막 바위산과 파란 하늘, 대리석 기둥 신전, 주황 불빛의 사암 회랑. 반사실적 게임 엔진풍 3D에 좌우 상단 디버그 오버레이.
- **기술**: Rust, WebGPU
- **프롬프트 구조**: 언리얼의 조명·Nanite 원리를 따르는 라이브러리를 Rust+WebGPU로, 깔끔한 코드로 만들라는 3~4줄 목표 지시
- **태그**: 렌더링엔진, Nanite, WebGPU, Rust, 게임엔진, 신전, 사막, 기술데모, 3D
- **주의**: 엔진 실행 화면 녹화라 디버그 패널이 계속 보이고 편집된 영상이 아님. 짧은 프롬프트로 이 결과가 나왔다는 과정은 영상에서 확인 불가

#### [Foldable phone rebuilt part by part in code](art3d__foldable-phone-rebuilt-part-by-part-in-code__2113644365876691235.md)
`art3d__foldable-phone-rebuilt-part-by-part-in-code__2113644365876691235` · 약 1.27:1 (916x720) · 24s · 조회 15K · 에셋필요 X

- **요약**: 왼쪽 주황 코드 패널이 흐르는 동안 오른쪽 뷰포트에서 폴더블폰을 부품 단위로 조립·분해하고, 카메라 클로즈업과 접힘 각도·부품 수 같은 지표 카드를 함께 보여주는 코드 빌드 영상
- **어울리는 경우**: 하드웨어·제품 구조 설명 / 분해도(익스플로디드 뷰)로 내부 부품 소개 / '코드로 만든다' 과정 시각화 / 제품 런칭 티저
- **잘하는 표현**: 부품이 층층이 떠오르는 분해도 애니메이션 / 힌지가 접혔다 펴지는 동작 / 빛나는 케이블 궤적 / 실시간 지표 카드와 진행 바가 있는 대시보드 레이아웃
- **스타일**: 오프화이트 뷰포트에 크림색 폰 바디·검은 화면·주황 회로 기판, 왼쪽은 번트오렌지 코드 에디터와 'SUPERIOR' 로고. 깔끔한 제품 렌더와 레트로 터미널 UI의 혼합.
- **기술**: Claude Code, REA
- **프롬프트 구조**: 부품 목록 먼저 → 부품별 함수로 하나씩 배치 → 간섭·여유 검사 → 마지막에 움직임 애니메이션, '목록부터 보여주고 승인 전엔 코드 금지'의 4단계 템플릿
- **태그**: 폴더블폰, 분해도, 제품구조, 하드웨어, 코드빌드, 대시보드, 3D, 조립애니메이션
- **주의**: 작가 브랜드 'SUPERIOR' 로고가 화면에 있음. 프롬프트는 '[아무 기기]' 템플릿이라 실제 영상의 화면 구성(코드 패널·지표 카드)은 설명되지 않음. REA가 무엇인지 메타에 설명 없음

#### [Jelly peach specimen sheet](art3d__jelly-peach-specimen-sheet__2112240323560645092.md)
`art3d__jelly-peach-specimen-sheet__2112240323560645092` · 약 1.58:1 (1136x720) · 18s · 조회 15K · 에셋필요 X

- **요약**: 씨가 박힌 반쪽 복숭아 젤리를 잡아 흔들고 뒤집다가 씨를 떼어 내 빈 홈을 보여주는 WebGPU 소프트바디 'Material Studies' 표본 시트
- **어울리는 경우**: 음식·과일 제품 티저 / 단면·내부 구조 설명 / 분리·떼어내기 개념의 은유 인서트 / 소프트바디 물리 데모
- **잘하는 표현**: 반투명 과육과 씨 주변 붉은 링의 볼륨 재질 / 말랑한 변형과 뒤집힘 / 씨를 떼어 내는 접착·분리 동작 / 벨벳 질감 껍질의 노랑·빨강 블러시
- **스타일**: 밝은 웜그레이 스튜디오 배경(#E2DFDA)에 노랑·주황·루비 레드 반투명 복숭아와 갈색 씨, 이탤릭 세리프 'Peach Jelly.' 타이틀. 미니멀 에디토리얼 제품사진풍 3D.
- **기술**: WebGPU, WGSL, CPU XPBD 소프트바디, SDF·surface nets, 단일 HTML 파일
- **프롬프트 구조**: 표본 시트 레이아웃 지정 후 대상·지오메트리·물리·렌더링을 긴 문단별로 기술한 상세 스펙
- **태그**: 젤리, 복숭아, 과일, soft-body, WebGPU, material-study, 에디토리얼, 인터랙티브, 3D
- **주의**: 상단에 'Claude Opus 5.5 · 7.11$' 모델명·비용 라벨이 붙은 화면 녹화. 화면에는 Opus 결과 한 패널만 나옴

#### [Nested spinning hexagon ball physics simulation](art3d__nested-spinning-hexagon-ball-physics-simulation__2112189854234652746.md)
`art3d__nested-spinning-hexagon-ball-physics-simulation__2112189854234652746` · 16:9 · 28s · 조회 14K · 에셋필요 X

- **요약**: 서로 반대로 도는 3겹 육각기둥 케이지 안에서 공이 계속 늘어나며 튀다가 벽 패널을 깨고 바깥 칸으로 쏟아지는 Three.js 물리 시뮬레이션
- **어울리는 경우**: 복잡계·혼돈·연쇄 반응 개념 설명 / '틀을 깨고 나온다'·단계적 확장 비유 / AI 모델 코딩 벤치마크(회전 육각형 공 테스트) 소개 / 계층·중첩 구조 설명
- **잘하는 표현**: 중첩된 회전 와이어프레임 입체 / 다수 공의 충돌·퇴적 물리 / 벽 패널이 금 가고 파편으로 부서지는 연출 / 느린 오빗 카메라
- **스타일**: 연한 오프화이트 배경에 검은 윤곽선만 있는 옅은 민트 틴트 반투명 육각 케이지, 그 안에 파스텔·남색 계열의 작은 구슬이 가득 찬다. 깨끗한 일러스트풍 3D로 조용하고 정돈된 느낌.
- **기술**: Three.js, 자체 작성 물리, Web Audio API
- **프롬프트 구조**: 장면·물리 규칙·룩(툰 셰이딩·금지 목록)·카메라·사운드·UI를 문단별로 나눈 단일 HTML 스펙, '하지 말 것' 목록을 길게 명시
- **태그**: 물리시뮬, 육각형, 공튀기기, 중첩구조, Three.js, 와이어프레임, 미니멀, 오프화이트, 벤치마크
- **주의**: 프롬프트는 2~3단 툰 셰이딩·두꺼운 외곽선을 요구했지만 결과는 가는 윤곽선의 반투명 패널에 가까움. 공이 작아 축소 시 디테일이 잘 안 보임

#### [Floating island town from day to night, 3D short film](art3d__floating-island-town-from-day-to-night-3d-short-film__2115486834755035178.md)
`art3d__floating-island-town-from-day-to-night-3d-short-film__2115486834755035178` · 4:5 · 58s · 조회 14K · 에셋필요 O

- **요약**: 구름 위 떠 있는 섬마을이 집·나무·열기구로 채워진 뒤 낮에서 노을, 밤으로 넘어가 불빛과 풍등이 떠오르는 1분짜리 로우폴리 3D 단편
- **어울리는 경우**: 마을·도시·커뮤니티가 만들어지는 과정 비유 / 하루의 흐름·시간 경과 표현 / 감성적인 오프닝·엔딩 인서트 / 브랜드 세계관 소개
- **잘하는 표현**: 낮→노을→밤 조명 전환 / 오브젝트가 하나씩 생겨나며 장면이 채워지는 빌드업 / 창문·가로등·풍등의 따뜻한 발광 / 열기구·구름이 흐르는 느긋한 카메라 무브
- **스타일**: 베이지빛 하늘과 둥글둥글한 흰 로우폴리 구름, 선명한 초록 잔디에 빨강·파랑·노랑·보라 지붕의 장난감 같은 집들. 밤에는 남색 하늘에 주황 불빛이 번지는 아늑한 동화풍 3D.
- **기술**: Three.js
- **프롬프트 구조**: 첨부 이미지를 재현하라는 한 문단짜리 자유 지시, 텍스트 금지·'슬롭 금지'·창의성만 강조하고 세부 사양은 거의 없음
- **태그**: 떠있는섬, 로우폴리, 마을, 낮밤전환, 열기구, 풍등, Three.js, 동화풍, 시네마틱
- **주의**: 원작 섬 이미지(Skyhold) 첨부가 전제라 같은 결과를 내려면 참고 이미지가 필요. 58초로 길어 인서트로는 일부 구간만 쓰는 편이 맞음

#### [Rigged rowing-game character from a concept sheet](art3d__rigged-rowing-game-character-from-a-concept-sheet__2117273092284112963.md)
`art3d__rigged-rowing-game-character-from-a-concept-sheet__2117273092284112963` · 16:9 · 28s · 조회 14K · 에셋필요 O

- **요약**: 콘셉트 시트 → 4방향 이미지 분리 → Tripo 3D 모델 → Blender 리깅·웨이트 규칙 → 애니메이션 클립 → Unity 게임 화면까지 'BOAT KID' 캐릭터 제작 과정을 단계 카드로 보여주는 메이킹 영상
- **어울리는 경우**: AI 에이전트 작업 파이프라인을 단계별로 설명 / 게임·3D 캐릭터 제작 공정 소개 / '코드와 결과물을 나란히' 보여주는 튜토리얼 인서트 / 비포·애프터 공정 요약
- **잘하는 표현**: 왼쪽 터미널 코드 카드 + 오른쪽 결과 렌더의 2단 분할 레이아웃 / STEP 01~08 번호가 붙은 공정 내레이션 / 본·웨이트 색 구분 시각화 / 마지막 실제 게임 플레이 화면으로 마무리
- **스타일**: 짙은 남색 배경 위 macOS 창 버튼이 달린 'Claude Code · Opus 5.5' 터미널 카드에 주황 STEP 라벨과 흰 고딕 제목, 옆 칸은 회색 스튜디오의 사실적인 3D 아이 캐릭터. 끝은 푸른 밤 운하의 게임 화면.
- **기술**: Claude Code, Blender(headless Python), Tripo, Unity, Python
- **프롬프트 구조**: 리깅 작업을 1~6번 번호 단계(정리→관절 추출→아마추어→웨이트 규칙→포즈 테스트 반복→FBX 내보내기)로 지시하는 작업 지시서
- **태그**: 메이킹, 파이프라인, 리깅, Blender, Tripo, Unity, 캐릭터, 단계설명, 터미널UI
- **주의**: 3D 모델은 Tripo(외부 생성형 3D)로 만들었고 콘셉트 시트 원본이 필요. 프롬프트는 리깅 단계만 다루고 영상의 편집·카드 레이아웃은 프롬프트에 없음

#### [Voxel island on a flying sea turtle](art3d__voxel-island-on-a-flying-sea-turtle__2116169391301607810.md)
`art3d__voxel-island-on-a-flying-sea-turtle__2116169391301607810` · 약 1:1.40 (720x1008) · 12s · 조회 13K · 에셋필요 X

- **요약**: 구름 위를 헤엄치는 거대 바다거북 등껍질 위에 등대·오두막·단풍나무 섬이 있고 혹등고래가 주위를 도는 복셀 3D 장면을, 같은 프롬프트의 1차 시도와 최종 시도로 위아래 비교한 영상
- **어울리는 경우**: 반복 개선·프롬프트 다듬기 전후 비교 / '같은 요청, 다른 완성도' 사례 설명 / 판타지 세계관·동화 인서트 / 복셀·마인크래프트풍 소개
- **잘하는 표현**: 디테일이 크게 늘어나는 비포·애프터 대비 / 복셀 단위 생물(거북·고래) 애니메이션 / 등대 불빛·폭포·갈매기 같은 작은 생동감 요소 / 천천히 도는 시네마틱 오빗
- **스타일**: 위 칸은 흰 배경의 단순한 초록 블록 거북, 아래 칸은 하늘색→복숭아빛 그라데이션 하늘에 분홍·흰 복셀 구름, 빨강·흰 줄무늬 등대와 주황·금색 단풍. 장난감 같은 따뜻한 복셀 3D.
- **기술**: Three.js
- **프롬프트 구조**: 장면 → 섬 위 오브젝트 목록 → 생물 동작 → 조명·효과 순으로 쓴 한 문단 서술형, 마지막에 '최대한 디테일하게'
- **태그**: 복셀, voxel, 거북이, 떠있는섬, 고래, 판타지, 비포애프터, Three.js, 동화풍
- **주의**: 한 화면에 'Claude Opus 5.5 1st attempt'(위)와 'final attempt'(아래)가 상하로 쌓인 비교 영상. 스타일 참고는 아래 final 칸만 볼 것

#### [Fictional rocket CAD drawings and launch animation](art3d__fictional-rocket-cad-drawings-and-launch-animation__2109515393220083912.md)
`art3d__fictional-rocket-cad-drawings-and-launch-animation__2109515393220083912` · 16:9 · 24s · 조회 12K · 에셋필요 X

- **요약**: 어두운 바닥에 시안색 발사장 배치도가 그려지고, 선이 빛의 와이어로 솟아 발사대·타워·로켓이 쌓인 뒤 밤의 발사장으로 바뀌어 리프트오프하는 Blender 영상
- **어울리는 경우**: 설계도·기획이 실물이 되는 과정 비유 / 프로젝트 '발사'·런칭 발표 인서트 / 우주·공학 주제 강의 오프닝 / 2D 도면에서 3D로 전환되는 설명
- **잘하는 표현**: 청사진이 스캔되듯 그려지는 2D 라인 애니메이션 / 2D 선이 3D 와이어 구조로 솟아오르는 전환 / 빛 입자 소용돌이와 아래부터 실체화되는 빌드업 / 밤바다 반사·불꽃·연기의 발사 장면
- **스타일**: 검정·짙은 남색 배경에 시안 발광 선의 디지털 도면, 빛 링과 입자가 도는 홀로그램 단계를 지나 붉은 철탑과 흰 로켓, 가로등이 물에 비치는 차분한 밤 발사장. 일본어 소형 타이틀과 'Create by Ayuneo' 로고로 끝남.
- **기술**: Blender(EEVEE, Geometry Nodes), Python, DXF
- **프롬프트 구조**: 【図面】【動画】【進め方】(도면·영상·진행 방식) 섹션으로 나눈 일본어 스펙, 장면을 1~6 번호 순서로 쓰고 치수 모듈 공유·테스트 렌더 확인 절차까지 지정
- **태그**: 로켓, 청사진, blueprint, 홀로그램, 발사, Blender, 다크테크, 시안, 공학, 2D→3D
- **주의**: 화면 문구가 일본어이고 마지막에 작가 로고가 들어감. 발사 장면은 꽤 어둡고 작게 잡혀 축소 시 잘 안 보일 수 있음

#### [Sliceable jelly watermelon physics toy](art3d__sliceable-jelly-watermelon-physics-toy__2112638127483343162.md)
`art3d__sliceable-jelly-watermelon-physics-toy__2112638127483343162` · 약 1.58:1 (1136x720) · 17s · 조회 12K · 에셋필요 X

- **요약**: 반투명 젤리 수박 조각을 강철 칼이 내려와 썰고, 잘린 조각들이 각자 말랑하게 흔들리며 품종 색(크림슨·골든·로제)이 바뀌는 WebGPU 소프트바디 장난감
- **어울리는 경우**: '쪼개기'·분할·나누기 개념 설명 / 큰 문제를 작은 단위로 나누는 비유 / 말랑한 식품·디저트 제품 티저 / 물리 시뮬 인터랙션 데모
- **잘하는 표현**: 칼이 눌러 홈을 낸 뒤 관통해 갈라지는 절단 연출 / 반투명 젤리의 굴절·흡수·씨앗 내부 표현 / 조각마다 독립된 말랑한 흔들림 / 색상 프리셋 전환
- **스타일**: 밝은 웜그레이 종이 배경에 이탤릭 세리프 'Melon Jelly.' 타이틀과 우측 얇은 컨트롤 패널, 빨강·주황·분홍의 투명한 젤리와 초록 껍질. 매거진 화보 같은 깔끔한 머티리얼 스터디 3D.
- **기술**: WebGPU, WGSL, XPBD 소프트바디(CPU, 사면체 메시)
- **프롬프트 구조**: 지오메트리·시뮬·칼 도구 절단 알고리즘·렌더 패스·품종·컨트롤을 항목별로 쓴 고밀도 기술 스펙
- **태그**: 젤리, 수박, soft-body, 칼질, 자르기, WebGPU, 에디토리얼, material-study, 인터랙티브
- **주의**: 상단에 'Claude Opus 5.5 · 12.46$' 라벨이 붙은 웹 페이지 화면 녹화(UI 패널 포함). 같은 수박 젤리의 비교 영상 엔트리와 혼동 주의

#### [Interactive jelly dam simulation](art3d__interactive-jelly-dam-simulation__2114512807500615723.md)
`art3d__interactive-jelly-dam-simulation__2114512807500615723` · 약 1.60:1 (1152x720) · 18s · 조회 12K · 에셋필요 X

- **요약**: 댐·저수지·발전소가 있는 산골짜기를 젤리 블록으로 잘라낸 디오라마에서 수문이 열려 물이 쏟아지고 맛(색)이 바뀌며 폭우·월류까지 보여주는 WebGPU 시뮬레이션
- **어울리는 경우**: 댐·수자원·에너지 원리 설명 / 유입·유출·용량(병목) 같은 흐름 개념 비유 / 지형 단면·지층 구조 설명 / 재난(홍수) 시나리오 시각화
- **잘하는 표현**: 지층이 보이는 단면 블록 디오라마 / 수문 개방과 계단 방수로를 흐르는 흰 물살 / 물·젤리 색 프리셋 전환(초록·파랑·보라) / 폭풍으로 어두워지고 물이 넘치는 상태 변화
- **스타일**: 연회색 스튜디오 테이블 위 사각 지형 블록, 회색 암반 단면·짙은 침엽수·콘크리트 댐에 형광 초록·하늘색·보라 반투명 물. 좌상단 이탤릭 세리프 'Dam Jelly.'와 우측 유리 패널의 에디토리얼 UI.
- **기술**: WebGPU, WGSL, 얕은 물 높이장 시뮬, WebAudio, Playwright, SwiftShader
- **프롬프트 구조**: SCENE·SIMULATION·INTERACTIONS·LIFE·SOUND·RENDERING·UI·QUALITY 대문자 섹션으로 지형 요소와 수위 방정식까지 적은 초대형 스펙
- **태그**: 댐, 디오라마, 단면, 물시뮬, 젤리, WebGPU, 에디토리얼, material-study, 인터랙티브, 에너지
- **주의**: 상단에 'Opus 5.5 · 18.51$' 라벨이 붙은 웹 페이지 화면 녹화. 연어·새·사람 같은 작은 생물은 영상 해상도에서 거의 안 보임

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

#### [Blender pumpkin carving](art3d__blender-pumpkin-carving__2116471578812952836.md)
`art3d__blender-pumpkin-carving__2116471578812952836` · 4:5 · 16s · 조회 11K · 에셋필요 X

- **요약**: 크림색 스튜디오의 나무판 위 호박을 손 없는 칼이 날아와 뚜껑·눈·코·입을 파내고, 촛불이 들어가 조명이 꺼지며 잭오랜턴이 주황빛으로 빛나는 Blender Cycles 실사풍 영상
- **어울리는 경우**: 할로윈·시즌 이벤트 인서트 / '깎아내서 완성한다'(빼기로 만드는 디자인) 비유 / 조명 전환으로 분위기를 바꾸는 장면 / 만족감(satisfying) 숏폼
- **잘하는 표현**: 칼이 스스로 움직이는 절삭 애니메이션 / 잘린 조각이 물리적으로 굴러떨어지는 표현 / 밝은 주광에서 암전 후 내부 발광으로 바뀌는 조명 전환 / 사실적인 호박 껍질·과육 재질
- **스타일**: 따뜻한 크림색 벽과 짙은 나무 테이블, 실사에 가까운 주황 호박의 소프트 데이라이트 제품 사진풍. 후반은 검은 화면 속 주황빛으로 빛나는 얼굴만 남는 대비.
- **기술**: Blender, Cycles
- **프롬프트 구조**: 대상 외형 → 시작 → 절삭 순서 → 점등 → 카메라 → 사운드 → 렌더 사양을 짧은 문단으로 나열한 시나리오형 지시
- **태그**: 호박, 할로윈, 잭오랜턴, Blender, Cycles, 실사풍, 조각, 조명전환, 숏폼
- **주의**: 화면에 '@MrTacticalX' 워터마크가 계속 보임. 과육·씨앗 디테일은 프롬프트보다 단순하게 나옴

#### [Pixel-art 3D football yard simulation with kids and dog](art3d__pixel-art-3d-football-yard-simulation-with-kids-and-dog__2113037013326627200.md)
`art3d__pixel-art-3d-football-yard-simulation-with-kids-and-dog__2113037013326627200` · 약 1.60:1 (1152x720) · 19s · 조회 11K · 에셋필요 X

- **요약**: 떠 있는 섬 위 아파트 뒤뜰 미니 축구장에서 아이들이 3대3 경기를 하고, 여름·가을·겨울과 낮·밤이 바뀌는 아이소메트릭 픽셀아트 3D 웹 장난감 'Yard Box'
- **어울리는 경우**: 계절·시간 변화 표현 / 동네·일상·공동체 이야기 인서트 / 게임 개발·시뮬레이션 소개 / 레트로 게임풍 섹션 전환
- **잘하는 표현**: 3D를 저해상도로 렌더해 팔레트 양자화한 픽셀아트 룩 / 계절 프리셋 전환(잔디·단풍·눈) / 밤에 창문이 켜지는 조명 변화 / 90도 단위 카메라 회전과 단면(돌하우스) 보기
- **스타일**: 밝은 회백색 페이지 배경에 아이소메트릭 떠 있는 섬, 민트 펜스의 초록 구장과 회색 패널 아파트, 노란 단풍·흰 눈·남색 밤 버전. 픽셀 폰트 'YARD BOX' 로고와 우측 컨트롤 레일.
- **기술**: Three.js(r160), 커스텀 포스트 셰이더(OKLab 팔레트 양자화·깊이 외곽선)
- **프롬프트 구조**: RENDERING PIPELINE·LIGHT AND TIME·WORLD·PEOPLE AND DOG·GAME LOGIC·SEASONS·INPUT AND UI 대문자 섹션의 초상세 게임 스펙
- **태그**: 픽셀아트, 아이소메트릭, 디오라마, 축구, 계절변화, 낮밤, Three.js, 레트로, 인터랙티브
- **주의**: 상단에 'Claude Opus 5.5 · 6.06$' 라벨이 붙은 웹 화면 녹화. 선수·개는 작아서 축소 시 거의 점으로 보임

#### [Interactive jelly octopus soft-body study](art3d__interactive-jelly-octopus-soft-body-study__2115173334031737112.md)
`art3d__interactive-jelly-octopus-soft-body-study__2115173334031737112` · 약 1.58:1 (1136x720) · 17s · 조회 11K · 에셋필요 X

- **요약**: 반투명 젤리로 만든 문어가 다리를 꿈틀대며 늘어나고 들어 올려지며, 코랄·플럼·민트 색이 바뀌는 WebGPU 소프트바디 스터디
- **어울리는 경우**: 유연성·적응력 비유 / 여러 갈래로 뻗는 구조(멀티태스킹·분산) 설명 / 해양생물·자연 주제 인서트 / 말랑한 캐릭터 티저
- **잘하는 표현**: 여러 다리가 위상차를 두고 꿈틀대는 근육 변형 / 반투명 젤리의 굴절과 바닥에 비치는 색 그림자 / 드래그로 들어 올리는 탄성 반응 / 색상 프리셋 전환
- **스타일**: 밝은 웜그레이 스튜디오 바닥에 코랄·라벤더·민트 반투명 젤리 문어, 좌상단 이탤릭 세리프 'Octopus Jelly.'와 우측 얇은 패널. 미니멀 매거진풍 머티리얼 스터디 3D.
- **기술**: WebGPU, XPBD 사면체 소프트바디
- **프롬프트 구조**: 이전 시리즈(타이거 샤크 젤리) 스타일을 전제로 해부학 형태·다리 곡률 생성 방식·재질층·근육 동작·UI를 한 문단에 압축한 서술형
- **태그**: 젤리, 문어, soft-body, WebGPU, 해양생물, 에디토리얼, material-study, 인터랙티브
- **주의**: 상단에 'Claude Opus 5.5 · 5.17$' 라벨이 붙은 웹 화면 녹화. 프롬프트가 이전 작업 스타일을 참조하므로 단독으로는 같은 룩이 안 나올 수 있음

#### [Frost fortress fantasy scene](art3d__frost-fortress-fantasy-scene__2116533061495947270.md)
`art3d__frost-fortress-fantasy-scene__2116533061495947270` · 약 1:1.40 (720x1008) · 12s · 조회 9K · 에셋필요 X

- **요약**: 오로라가 뜬 밤 구름바다를 걷는 매머드 등 위에 얼음 수정이 빛나는 돌 요새가 있고, 얼음 용이 주위를 날아다니는 복셀 3D 장면을 1차 시도($0.07)와 최종 시도($0.75)로 위아래 비교한 영상
- **어울리는 경우**: 반복 개선·프롬프트 다듬기 전후 비교 / 비용 대비 결과 차이 설명 / 겨울·판타지 세계관 인서트 / 게임 아트 소개
- **잘하는 표현**: 단순 블록에서 고밀도 장면으로 바뀌는 비포·애프터 대비 / 복셀 생물(매머드·용) 애니메이션 / 눈보라·눈 입자 트레일 / 발광 수정·오로라 같은 차가운 광원
- **스타일**: 아래 칸은 남색 밤하늘에 청록 오로라와 달, 하늘색 복셀 구름, 갈색 털 매머드와 파랑·금색 담요 위 회청색 요새, 시안으로 빛나는 얼음 용. 위 칸은 흰 배경의 갈색 상자 매머드.
- **기술**: Three.js
- **프롬프트 구조**: 거북 섬 엔트리와 같은 틀로 장면 → 등 위 요새 구성 → 생물 동작 → 효과 순의 한 문단 서술형
- **태그**: 복셀, voxel, 매머드, 얼음용, 판타지, 오로라, 비포애프터, Three.js, 겨울
- **주의**: 'Claude Opus 5.5 1st attempt – 0.07$'(위)와 'final attempt – 0.75$'(아래)가 상하로 쌓인 비교 영상. 스타일 참고는 아래 칸만 볼 것

#### [Procedural robotic giant squid teardown](art3d__procedural-robotic-giant-squid-teardown__2119392067646345249.md)
`art3d__procedural-robotic-giant-squid-teardown__2119392067646345249` · 약 1.60:1 (1152x720) · 17s · 조회 8K · 에셋필요 X

- **요약**: 흰 광택 셸과 보라색 부품으로 된 로봇 대왕오징어가 렌즈·머리·팔·맨틀·사이펀 순서로 열리고 분해·재조립되는 과정을 텔레메트리 UI와 함께 보여주는 절차적 3D 제품 분해 페이지
- **어울리는 경우**: 제품·시스템 내부 구조 해부 설명 / 하드웨어·로봇 기술 소개 / 챕터별로 부품을 짚어가는 기술 리뷰 인서트 / 분해(익스플로드) 뷰가 필요한 설명
- **잘하는 표현**: 부품이 순차적으로 열리고 흩어지는 익스플로드 뷰 / 3D 부품에 점과 지시선으로 붙는 콜아웃 라벨 / 챕터 필·진행 바·텔레메트리 카드가 있는 제품 페이지 UI / 근접 매크로 카메라와 턴테이블
- **스타일**: 거의 흰색 배경에 옅은 라벤더 그라데이션, 리벳·구멍 디테일이 있는 흰 유광 셸과 검은 내부 기계, 바이올렛(#8a4dff) 강조와 은은한 발광. 깔끔한 산스+모노 폰트의 프리미엄 제품 시뮬레이터 느낌.
- **기술**: Three.js(r170), EffectComposer(GTAO·Bloom), Playwright 프레임 캡처, numpy·scipy 합성 사운드, H.264
- **프롬프트 구조**: LOOK·GEOMETRY TOOLKIT·MODEL·ARMS·RIG AND TIMELINE·UI·CAPTURE AND AUDIO 대문자 섹션, 결정적 stateAt(t) 타임라인과 렌더 캡처 절차까지 명시한 초대형 스펙
- **태그**: 분해도, teardown, 로봇, 오징어, 제품시뮬, 콜아웃, 화이트+바이올렛, Three.js, 하드서피스, 익스플로드뷰
- **주의**: 상단에 'Claude Opus 5.5 · 47.94$' 라벨이 붙음. UI 글자가 작아 인서트로 쓰면 라벨은 거의 안 읽힘

#### [Interactive pixel art swimming club](art3d__interactive-pixel-art-swimming-club__2114467181912322353.md)
`art3d__interactive-pixel-art-swimming-club__2114467181912322353` · 약 1.60:1 (1152x720) · 17s · 조회 8K · 에셋필요 X

- **요약**: 떠 있는 섬 위 야외 수영장(25m 레인풀·다이빙대·탈의실·파라솔)을 아이소메트릭 픽셀아트 3D로 만들고 카메라 회전과 낮·밤 전환을 보여주는 웹 디오라마 'Deep End'
- **어울리는 경우**: 여름·휴가·스포츠 주제 인서트 / 시설·공간 구성 소개(맵 투어) / 레트로 게임풍 섹션 전환 / 시뮬레이션 게임 개발 소개
- **잘하는 표현**: 팔레트 양자화된 픽셀아트 3D 디오라마 / 90도 단위 카메라 회전 / 낮·밤 조명 전환 / 물결이 비치는 청록 수면
- **스타일**: 밝은 회백색 배경에 아이소메트릭 떠 있는 섬, 청록 수영장과 회색 데크, 빨강·노랑·분홍 파라솔과 파란 지붕 탈의실, 짙은 침엽수. 픽셀 폰트 'DEEP END' 로고와 우측 컨트롤 패널.
- **기술**: Three.js, 높이장 파동 방정식 물 시뮬
- **프롬프트 구조**: 앞선 픽셀 디오라마 시리즈 엔진을 전제로 장소 구성·물 시뮬·다이빙 물리·심사 규칙·부가 생활 요소를 서술형 문단으로 나열
- **태그**: 픽셀아트, 아이소메트릭, 디오라마, 수영장, 다이빙, 낮밤, Three.js, 레트로, 인터랙티브
- **주의**: 상단에 'Claude Opus 5.5 · 11.14$' 라벨이 붙은 웹 화면 녹화. 프롬프트의 다이빙·채점 장면은 이 축소 해상도에서 거의 안 보임

#### [Rigged 3D shark with swim and bite animations](art3d__rigged-3d-shark-with-swim-and-bite-animations__2113934291818221665.md)
`art3d__rigged-3d-shark-with-swim-and-bite-animations__2113934291818221665` · 약 1.67:1 (1200x720) · 27s · 조회 7K · 에셋필요 O

- **요약**: Tripo로 만든 상어 모델을 Blender에서 리깅·웨이트 정리하고 헤엄·물기 애니메이션을 입힌 결과를 여러 뷰포트 화면으로 보여주는 작업 화면 녹화
- **어울리는 경우**: 3D 리깅·애니메이션 작업 과정 소개 / AI 에이전트가 툴을 다루는 장면 예시 / 기술 튜토리얼 B롤
- **잘하는 표현**: 같은 모델을 정면·측면·와이어프레임 등 여러 뷰로 동시에 보여주기 / 등뼈를 따라 흐르는 헤엄 파동 / 입을 벌려 무는 동작
- **스타일**: 어두운 회색 Blender UI 안에 청회색·회색 뷰포트가 여러 칸으로 나뉘고 회색 상어 모델이 움직임. 편집된 영상이 아니라 소프트웨어 작업 화면 그대로의 느낌.
- **기술**: Blender(headless Python, Blender MCP), Tripo, Omni 1.1(영상 생성)
- **프롬프트 구조**: Stage 1~6 단계로 리그 수정 → 절차적 헤엄 → 영상 모델용 기준 프레임 → 생성 영상 검사 → 물기 피팅 → 해부학 리타깃을 수치 기준과 합격 조건까지 적은 작업 매뉴얼
- **태그**: 리깅, 상어, Blender, 애니메이션, 화면녹화, Tripo, 3D모델, 작업과정
- **주의**: 편집 영상이 아닌 Blender 화면 녹화라 인서트 스타일 참고로는 약함. 모델은 Tripo, 물기 동작은 Omni/Seedance 계열 생성 영상에서 추출하는 외부 생성 모델 의존 파이프라인

#### [Interactive soft-body jelly marlin](art3d__interactive-soft-body-jelly-marlin__2115752978946687084.md)
`art3d__interactive-soft-body-jelly-marlin__2115752978946687084` · 16:9 · 17s · 조회 7K · 에셋필요 X

- **요약**: 반투명 젤리로 만든 청새치가 꼬리를 휘두르고 몸을 비틀며 코발트·라일락·미드나이트·선라이즈 색으로 바뀌는 WebGPU 소프트바디 스터디
- **어울리는 경우**: 속도·민첩성 비유 / 해양생물·낚시 주제 인서트 / 말랑한 캐릭터·굿즈 티저 / 물리 시뮬 데모
- **잘하는 표현**: 몸통을 따라가는 꼬리 휘두름·비틀림 변형 / 반투명 젤리 안의 줄무늬·은빛 배 표현 / 색상 팔레트 전환 / 떨어지며 튕기는 탄성
- **스타일**: 밝은 웜그레이 스튜디오 바닥에 파랑·보라·남색·주홍 반투명 젤리 청새치, 좌상단 이탤릭 세리프 'Marlin Jelly.'와 우측 얇은 패널. 미니멀 매거진풍 머티리얼 스터디 3D.
- **기술**: WebGPU, XPBD 사면체 소프트바디, SDF, surface nets
- **프롬프트 구조**: 이전 젤리 시리즈 스타일을 전제로 해부학 형태·재질층·무늬·근육 동작·팔레트·UI를 한 문단에 압축한 서술형
- **태그**: 젤리, 청새치, soft-body, WebGPU, 해양생물, 에디토리얼, material-study, 인터랙티브
- **주의**: 상단에 'Claude Opus 5.5 · 11.6$' 라벨이 붙은 웹 화면 녹화. 이전 작업 스타일 참조가 전제된 프롬프트

#### [Pool scene with jelly fish from earlier projects](art3d__pool-scene-with-jelly-fish-from-earlier-projects__2115912302272618696.md)
`art3d__pool-scene-with-jelly-fish-from-earlier-projects__2115912302272618696` · 약 1.55:1 (1114x720) · 16s · 조회 6K · 에셋필요 X

- **요약**: 햇빛 드는 야외 수영장에 젤리 청새치·혹등고래·범고래·귀상어를 떨어뜨리면 물결을 일으키며 헤엄치는 실시간 3D 수면·소프트바디 시뮬레이션 'Jelly Pool'
- **어울리는 경우**: 여름·휴식·청량감 인서트 / 여러 요소가 한 공간에서 움직이는 생태계·시스템 비유 / 물·파동 원리 설명 / 배경 루프 영상
- **잘하는 표현**: 위에서 내려다본 수영장 수면의 굴절·커스틱 / 손가락·동물이 만드는 잔물결 / 반투명 젤리 동물의 헤엄 파동 / 야자수 그림자가 흔들리는 데크
- **스타일**: 연한 석재 데크와 모자이크 타일 테두리의 청록 수영장을 위에서 비스듬히 내려다본 구도, 반짝이는 커스틱 무늬 위로 파란·검은 젤리 동물이 떠다님. 밝고 청량한 실사풍 3D.
- **기술**: Three.js(r128), WebGL2, Web Workers, XPBD 소프트바디, GPU 높이장 파동 시뮬
- **프롬프트 구조**: TECH·THE POOL·THE ANIMALS·JELLY RENDERING 섹션으로 워커 분산·패스 순서까지 적은 초대형 구현 스펙
- **태그**: 수영장, 물시뮬, 커스틱, 젤리, 해양생물, soft-body, Three.js, 청량, 탑뷰
- **주의**: 상단에 'Claude Opus 5.5 · 22,72$' 라벨이 붙은 웹 화면 녹화(하단 도구 바 포함). 동물이 작아 젤리 질감은 축소 시 잘 안 보임

### game (게임) — 22건 (조회수순)


#### [Sci-fi first-person shooter game](game__sci-fi-first-person-shooter-game__2118343870450954318.md)
`game__sci-fi-first-person-shooter-game__2118343870450954318` · 약 1.76:1 (1268x720) · 183s · 조회 1.6M · 에셋필요 O

- **요약**: 보랏빛 외계 행성 전장에서 빨간·흰 SF 총으로 로봇·거대 보스와 싸우는 브라우저 1인칭 슈팅 게임 플레이 녹화
- **어울리는 경우**: AI로 만든 게임 사례 소개 / 게임 개발·3D 웹 기술 강의 / 에이전트 반복 개선 결과 시연 / 액션감 있는 배경 B롤
- **잘하는 표현**: 1인칭 무기 뷰와 총구 화염·폭발·파티클 / 미션 목표·체력바·탄약·미니맵 HUD / 거대한 SF 구조물과 대기감 있는 하늘 / 보스전 연출
- **스타일**: 보라·자주 하늘과 붉은 흙의 외계 지형, 검은 첨탑 구조물과 형광 초록·분홍 발광 이펙트, 게임 HUD 오버레이. 콘솔 게임 같은 어둡고 장대한 SF 무드.
- **기술**: Three.js, Blender, Tripo, fal, Claude Code
- **프롬프트 구조**: 게임 자체 사양 없이 '독립 비평 에이전트로 기준 정의→영향도 순 개선 라운드→적대적 리뷰'를 시키는 개선 루프 지시 한 문단
- **태그**: FPS, 게임, 1인칭, SF, Three.js, 외계행성, 플레이영상, 슈팅
- **주의**: 편집된 모션그래픽이 아니라 게임 플레이 화면 녹화. 프롬프트는 기존 게임 개선 지시뿐이라 화면 내용을 설명하지 않음(prompt≠result 구조). 3D 모델은 Tripo·fal 생성 에셋

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

#### [Frog King browser simulator](game__frog-king-browser-simulator__2115878504067915826.md)
`game__frog-king-browser-simulator__2115878504067915826` · 16:9 · 34s · 조회 358K · 에셋필요 X

- **요약**: 눈 덮인 회색 폐허 도시에서 무장 분대가 엄폐·사격하며 진격하는 브라우저 3인칭 전술 전투 시뮬레이션 플레이 녹화
- **어울리는 경우**: AI 게임 개발 사례 소개 / 성능 최적화 전후 비교 설명 / 전술·군사 시뮬 B롤 / 웹 3D 기술 시연
- **잘하는 표현**: 3인칭 숄더뷰 엄폐 전투 / 연기·폭발·드롭쉽 같은 전장 이펙트 / 무전 로그·분대 상태·미니맵 HUD / 다수 AI 유닛 동시 시뮬
- **스타일**: 차갑고 탈색된 청회색 겨울 도시 폐허, 흰 연기와 주황 불빛 포인트, 작은 텍스트 HUD가 둘러싼 게임 화면. 사실적이고 긴장된 밀리터리 무드.
- **기술**: Three.js
- **프롬프트 구조**: '전투 시뮬 100회 관전→프레임·CPU·GPU 비용 추적→업계 표준 최적화 적용→화질 저하 시 전후 스크린샷 승인' 순서의 최적화 지시 한 문단
- **태그**: 게임, 3인칭슈터, 전술시뮬, 밀리터리, Three.js, 최적화, 플레이영상, 웹3D
- **주의**: 게임 플레이 화면 녹화. 제목의 'Frog King'과 달리 화면에 개구리 요소는 보이지 않으며, 프롬프트는 최적화 지시뿐이라 화면 내용과 직접 대응하지 않음

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

#### [Browser 3D action game with sketch-world theme](game__browser-3d-action-game-with-sketch-world-theme__2117253593371922601.md)
`game__browser-3d-action-game-with-sketch-world-theme__2117253593371922601` · 16:9 · 198s · 조회 34K · 에셋필요 O

- **요약**: 회색 스케치 세계를 주황 망토 소녀가 돌아다니며 색을 되살리고 몬스터·석상 보스와 싸우는, 중국어 UI의 브라우저 3D 액션 어드벤처 데모 플레이 녹화
- **어울리는 경우**: 행사·브랜드용 인터랙티브 데모 사례 / '색을 되찾는' 변화 전후 은유 / 생성 에셋 파이프라인 소개 / 밝고 귀여운 게임 B롤
- **잘하는 표현**: 흑백 스케치에서 컬러 세계로 바뀌는 전환 / 떠 있는 섬·풀밭·파스텔 노을의 판타지 환경 / 보스전과 결과 카드 UI / 이야기 컷인 일러스트 팝업
- **스타일**: 처음엔 연필 스케치풍 회색 구름 세계, 이후 선명한 초록 풀과 분홍·주황 노을 하늘의 파스텔 3D, 주황 포인트 중국어 UI. 밝고 동화 같은 캐주얼 판타지 무드.
- **기술**: Three.js, Claude Code, Tripo 3D, Miora, GPT Image 2.5, Seedance 2.5
- **프롬프트 구조**: 중국어로 행사용 데모 목적·에셋 위치·장르 선호(가벼운 전투·모험)·실행 환경(HTML+three.js)만 전한 짧은 의뢰
- **태그**: 게임, 3D액션, 어드벤처, 스케치월드, 파스텔, Three.js, 중국어UI, 플레이영상
- **주의**: 게임 플레이 화면 녹화이며 Miora 브랜드 IP 캐릭터 에셋과 여러 생성 모델(Tripo·GPT Image·Seedance) 사용. 화면 텍스트가 중국어

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

#### [3D game remake built with Opus 5.5](game__3d-game-remake-built-with-opus-5-5__2108735367331672201.md)
`game__3d-game-remake-built-with-opus-5-5__2108735367331672201` · 16:9 · 214s · 조회 28K · 에셋필요 O

- **요약**: 듄(Dune) 고전 게임을 드니 빌뇌브 영화풍 3인칭 3D 어드벤처로 리메이크해 궁전·사막·오니솝터·시에치 동굴을 오가는 플레이 녹화
- **어울리는 경우**: 레거시 리메이크·현대화 사례 소개 / AI 게임 제작 파이프라인 시연 / 시네마틱 사막 분위기 B롤 / 스토리 대화 장면 예시
- **잘하는 표현**: 거대한 건축물과 강한 빛줄기의 미니멀 시네마틱 조명 / 모래 먼지 낀 사막 대기 원근 / 자막형 NPC 대화 장면 / 장소 타이틀·목표 텍스트 UI
- **스타일**: 모래색·갈색·검정 단색조의 거대 콘크리트 실내와 사막, 역광 실루엣과 부드러운 안개, 작은 흰 산세리프 UI. 절제되고 장엄한 빌뇌브 영화풍 무드.
- **기술**: Godot, Blender, Tripo, Mixamo, Auto Rig Pro, ElevenLabs
- **프롬프트 구조**: 디컴파일한 원작을 개인 스킬(/ultimate-gauntlet-loop)로 3인칭 3D 리메이크하라는 지시에 원작 BGM 사용·캐릭터 3D화 경로·미술 레퍼런스만 붙인 짧은 요청
- **태그**: 게임, 리메이크, 3인칭, 시네마틱, 사막, Godot, 플레이영상, 영화풍
- **주의**: 게임 플레이 화면 녹화. 듄 IP(원작 게임·캐릭터명·영화 미술)와 원작 음원을 사용하므로 그대로 쓰지 말고 조명·톤만 참고할 것

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

#### [Pixel-art football stadium game](game__pixel-art-football-stadium-game__2116141712842293599.md)
`game__pixel-art-football-stadium-game__2116141712842293599` · 약 1.60:1 (1152x720) · 17s · 조회 13K · 에셋필요 X

- **요약**: 떠 있는 섬 위 소도시 축구장에서 11대11 경기·관중·조명이 돌아가는 three.js 3D 픽셀아트 축구 디오라마 화면 녹화
- **어울리는 경우**: 스포츠·전술 설명 배경 / 시뮬레이션·에이전트 행동 데모 / 아이소메트릭 디오라마 스타일 예시 / 게임 제작 사례 소개
- **잘하는 표현**: 저해상도 렌더+깊이 외곽선+64색 팔레트의 3D 픽셀아트 / 다수 선수·관중 인스턴싱 / 낮·저녁·야간 조명 전환 / 스탠드를 들어 올리는 인형집식 단면 뷰
- **스타일**: 줄무늬 초록 잔디와 빨간 관중석, 회색 주변 도로의 아이소메트릭 3D 픽셀아트, 오른쪽에 조작 패널이 붙은 밝은 회백색 웹 화면. 장난감 같고 정돈된 디오라마 무드.
- **기술**: Three.js, Web Audio
- **프롬프트 구조**: 경기 규칙·전술 AI·심판·경기장 구성·관중·조명·카메라·렌더링·UI를 한 문단에 촘촘히 나열한 초상세 기능 스펙
- **태그**: 픽셀아트, 3D픽셀아트, 축구, 디오라마, 아이소메트릭, Three.js, 시뮬레이션, 인스턴싱
- **주의**: 모델 비교 게시물에서 온 화면 녹화로 상단에 'Claude Opus 5.5 / 18.87$' 라벨이 붙어 있음(이 영상은 Opus 결과만 표시)

#### [Vault Street pixel-art bank heist diorama](game__vault-street-pixel-art-bank-heist-diorama__2114054716959215724.md)
`game__vault-street-pixel-art-bank-heist-diorama__2114054716959215724` · 약 1.58:1 (1136x720) · 17s · 조회 6K · 에셋필요 X

- **요약**: 떠 있는 아이소메트릭 마을 블록에서 은행 강도·경찰 추격·체포가 자동으로 반복되는 three.js 3D 픽셀아트 디오라마 화면 녹화
- **어울리는 경우**: 이야기 흐름·인과 관계를 장난감 마을로 보여주는 장면 / 도시·교통 시뮬레이션 설명 / 아이소메트릭 디오라마 스타일 예시 / 에이전트 자동 행동 데모
- **잘하는 표현**: 저해상도 렌더+OKLab 64색 양자화의 3D 픽셀아트 / 낮·황혼·밤 전환과 가로등·비 반사 / 지붕을 들어 내부를 보여주는 단면 / 차량·보행자 다수의 자동 스토리 루프
- **스타일**: 초록 잔디 섬 위 회색 도로 순환로와 은행·경찰서·도넛 가게가 있는 장난감 같은 아이소메트릭 3D 픽셀아트, 밝은 회백색 웹 패널 UI. 귀엽고 아기자기한 디오라마 무드.
- **기술**: Three.js(r160), 단일 HTML 파일, 포스트 셰이더(깊이 외곽선·Bayer 디더)
- **프롬프트 구조**: 렌더 방식·월드 구성·스토리 루프(→로 이은 사건 순서)·교통 규칙·UI를 문단별로 나눈 상세 스펙
- **태그**: 픽셀아트, 3D픽셀아트, 디오라마, 아이소메트릭, 은행강도, 시뮬레이션, Three.js, 장난감
- **주의**: 모델 비교 게시물에서 온 화면 녹화로 상단에 'Claude Opus 5.5 / 17.65$' 라벨이 붙어 있음(이 영상은 Opus 결과만 표시). 화면이 작아 세부 동작은 확대해 봐야 보임

### comparison (모델 비교) — 92건 (조회수순)


#### [Gummy bear soft-body physics scene](comparison__gummy-bear-soft-body-physics-scene__2110131790136401989.md)
`comparison__gummy-bear-soft-body-physics-scene__2110131790136401989` · 4:5 · 13s · 조회 632K · 에셋필요 X

- **요약**: 흰 테이블 위 반투명 젤리 곰들을 잡아 늘리고 던지고 쏟아붓는 Three.js 소프트바디 데모를 Opus 5.5와 Gemini Argon 4 결과로 위아래 비교한 영상
- **어울리는 경우**: 모델/툴 결과 비교 콘텐츠 / 젤리·구미 같은 말랑한 제품 티저 / 물리 시뮬레이션 인터랙션 설명 / 귀여운 오브젝트가 우르르 쏟아지는 강조 컷
- **잘하는 표현**: 잡아당기면 늘어났다 출렁이며 돌아오는 소프트바디 / 반투명 굴절·색 그림자가 있는 구미 재질 / 여러 개가 떨어져 쌓이는 젤리 더미 / 에디토리얼 제품 페이지형 UI
- **스타일**: 순백 배경에 체리 레드·오렌지·레몬·애플그린 반투명 젤리 곰, 바닥에 곰 색으로 물든 부드러운 그림자, 좌상단 이탤릭 세리프 'Gummy / Bears.' 타이틀과 우측 미니멀 카드. 밝고 깨끗한 제품 사진 같은 3D.
- **기술**: Three.js, 메타볼/마칭큐브 암시적 표면, 형상 보존 소프트바디, 단일 HTML 파일
- **프롬프트 구조**: 곰 외형·재질 / 물리(이게 핵심) / UI 세 블록으로 나눈 불릿 스펙, 상호작용별 기대 반응을 문장으로 나열
- **태그**: 젤리, 구미베어, soft-body, Three.js, 3D, 비교영상, 에디토리얼, 인터랙티브, material-study
- **주의**: 위(Opus 5.5 $7.2)·아래(Gemini Argon 4 $22) 분할 비교 영상으로 모델명·비용 라벨이 크게 붙어 있음. 아래쪽 Gemini 결과는 복셀처럼 각진 곰이라 스타일 참고는 위쪽 Opus 패널만 볼 것

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

#### [Electric motor animation model comparison](comparison__electric-motor-animation-model-comparison__2110065587279798719.md)
`comparison__electric-motor-animation-model-comparison__2110065587279798719` · 약 1:1.12 (720x810) · 40s · 조회 195K · 에셋필요 X

- **요약**: 테슬라식 영구자석 전기모터의 조립 외관 → 내부 부품 → 분해도 → 3상 전류·회전 자기장 → 냉각 흐름을 40초 고정 타임라인으로 설명하는 Three.js 시네마틱 애니메이션을 Gemini 4 Argon과 Opus 5.5로 비교한 영상
- **어울리는 경우**: 기계·전기 장치 작동 원리 설명 / 제품 내부 구조 분해도(exploded view) / 공학·과학 강의의 단계별 원리 인서트 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 축 방향으로 부품이 정렬된 채 분리·재조립되는 분해도 / 투명해지는 하우징 컷어웨이 / 코일 속 전류 펄스·자기장 라인 시각화 / 부품 라벨과 한 줄 설명 자막
- **스타일**: 짙은 남색~검정 스튜디오 배경에 브러시드 알루미늄·구리 코일·강철 PBR 재질, 강한 림라이트와 하이라이트 번짐, 무지개빛 자기장 라인과 얇은 산세리프 라벨. 프리미엄 자동차 엔지니어링 광고 같은 다크 테크 3D.
- **기술**: Three.js, PBR 재질, 고정 40초 결정적 타임라인(1200프레임)
- **프롬프트 구조**: 출력 사양(길이·해상도·fps)을 먼저 못박고 0–5s, 5–11s… 구간별 타임라인으로 장면·자막 문구를 지정한 뒤 VISUAL QUALITY·CAMERA·ANIMATION 요구사항을 나열한 벤치마크형 스펙
- **태그**: 전기모터, 작동원리, exploded-view, 컷어웨이, Three.js, 3D, 다크테크, 교육애니메이션, 비교영상
- **주의**: 위(Gemini 4 Argon $3.83)·아래(Claude Opus 5.5 $16.36) 분할 비교 영상으로 모델명·비용 라벨이 붙어 있음. 프롬프트는 16:9를 요구했지만 영상은 두 결과를 잘라 위아래로 쌓은 형태. 같은 Opus 결과가 'Electric motor 3D animation comparison'에도 재사용됨

#### [Voxel ship in a bottle](comparison__voxel-ship-in-a-bottle__2110136719827747181.md)
`comparison__voxel-ship-in-a-bottle__2110136719827747181` · 약 1:1.27 (720x912) · 18s · 조회 160K · 에셋필요 X

- **요약**: 병 속에 든 바다와 범선·등대·섬을 복셀 아트로 만든 WebGL 장면을 Gemini 4 Argon과 Opus 5.5로 위아래 비교한 영상
- **어울리는 경우**: 미니어처 디오라마형 오프닝·챕터 카드 / '작은 세계 안에 담긴' 은유 연출 / 낮·밤 분위기 전환 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 유리병 안에 갇힌 복셀 지형·파도 / 나무 책상 위 병의 반사와 하이라이트 / 밤 모드로 바뀌며 켜지는 등불·반딧불 같은 빛 입자 / 이름표('MARIGOLD · 1742') 같은 소품 디테일
- **스타일**: Opus 쪽은 따뜻한 나무 책상 위 투명 유리병 속에 청록 바다와 갈색 범선·초록 섬, 좌상단 이탤릭 세리프 'Marigold' 타이틀과 종이 톤 패널. 낮엔 밝은 하늘색, 밤엔 주황 등불이 점점이 빛나는 아늑한 복셀 디오라마.
- **기술**: WebGL, 단일 HTML 파일
- **프롬프트 구조**: 원하는 장면(병 속 복셀 범선·파도·물리·소품)과 단일 HTML 조건만 적은 짧은 한 문단 자유 서술
- **태그**: 복셀, ship-in-a-bottle, 디오라마, 미니어처, WebGL, 3D, 낮밤전환, 비교영상
- **주의**: 위(Gemini 4 Argon 0.19$)·아래(Claude Opus 5.5 12.06$) 분할 비교 영상으로 모델명·비용 라벨이 붙어 있음. 위쪽 Gemini는 검은 배경의 단순한 복셀이라 스타일 참고는 아래쪽 Opus 패널만 볼 것

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

#### [Jelly slice material test comparison](comparison__jelly-slice-material-test-comparison__2109424502237016076.md)
`comparison__jelly-slice-material-test-comparison__2109424502237016076` · 4:5 · 17s · 조회 145K · 에셋필요 X

- **요약**: 반달 모양 시트러스 젤리 조각을 잡아 늘리고 비틀면 출렁이며 돌아오는 WebGPU 소프트바디 머티리얼 스터디를 Opus 5.5와 ChatGPT-6 Astra로 번갈아 비교한 영상
- **어울리는 경우**: 젤리·과일 디저트 같은 말랑한 제품 티저 / 재질감(굴절·과육 질감)을 보여주는 클로즈업 / 색상 바리에이션(오렌지·블러드오렌지·레몬) 전환 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 과육·속껍질·겉껍질 3구역이 보이는 반투명 젤리 재질 / 늘이고 비틀면 크게 휘었다 복원되는 소프트바디 / 젤리 색으로 물든 부드러운 바닥 그림자 / 색상 프리셋 스와치 전환
- **스타일**: 따뜻한 베이지 사이클로라마 배경에 오렌지·루비 레드·레몬 옐로 반투명 젤리 조각, 좌상단 이탤릭 세리프 'Citrus Jelly.' 타이틀과 우측 작은 컨트롤 카드. 매거진 제품 사진 같은 미니멀 3D.
- **기술**: WebGPU, WGSL, XPBD 사면체 소프트바디, 단일 HTML 파일(라이브러리 없음)
- **프롬프트 구조**: Object / Physics / Rendering / UI 섹션으로 나눠 메시 생성 알고리즘·제약 조건·렌더 패스·UI 문구까지 구현 수준으로 지정한 상세 스펙
- **태그**: 젤리, 시트러스, soft-body, WebGPU, 3D, material-study, 에디토리얼, 비교영상, 인터랙티브
- **주의**: 위(Claude Opus 5.5 7.57$)·아래(ChatGPT-6 Astra 10.15$) 분할 비교 영상으로 모델명·비용 라벨이 붙어 있음. 메타에는 models에 fable-5.5가 적혀 있으나 영상 속 상대는 ChatGPT-6 Astra. 스타일 참고는 위쪽 Opus 패널 기준

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

#### [Orbit landing page with and without TasteSkill](comparison__orbit-landing-page-with-and-without-tasteskill__2110564814531797386.md)
`comparison__orbit-landing-page-with-and-without-tasteskill__2110564814531797386` · 16:9 · 53s · 조회 127K · 에셋필요 O

- **요약**: 소규모 팀용 프로젝트 관리 SaaS 'Orbit' 랜딩 페이지를 Opus 5.5가 TasteSkill 없이/있이 만든 두 결과를 좌우로 놓고 스크롤하며 비교한 화면 녹화
- **어울리는 경우**: 디자인 스킬·프롬프트 유무 전후 비교 / 다크 SaaS 제품 UI 소개 / 웹사이트 스크롤 쇼케이스 / 'AI 티 안 나는 디자인' 사례 설명
- **잘하는 표현**: 실제 같은 제품 UI 목업(작업 목록·주간 업데이트·상태 배지) / 큰 산세리프 헤드라인과 넓은 여백의 에디토리얼 구성 / 기록 사진을 섞은 히어로·섹션 / 요금제·FAQ까지 이어지는 긴 스크롤 흐름
- **스타일**: 거의 검정에 가까운 다크 그레이 배경, 흰색·회색 산세리프 타이포와 파란 단일 강조색 버튼·하이라이트. TasteSkill 쪽은 NASA 관제실·지구 사진 같은 흑백·실사 이미지를 크게 배치한 더 에디토리얼한 다크 미니멀.
- **기술**: Next.js, React, TypeScript, Tailwind CSS, TasteSkill v2
- **프롬프트 구조**: 제품 설명 → 기술 요구사항 → 참고 이미지 활용법(따라 할 것/베끼지 말 것) → 섹션 목록 → 'No purple gradient' 식 금지 목록 → 카피 원칙 순서로 쓴 디자인 브리프
- **태그**: 랜딩페이지, SaaS, 다크UI, 웹디자인, TasteSkill, 전후비교, 화면녹화, 에디토리얼
- **주의**: 편집된 영상이 아니라 두 웹페이지를 스크롤하는 화면 녹화. 좌(Without TasteSkill)·우(With TasteSkill) 모두 Opus 5.5 결과이며 상단에 라벨이 있음. 아트 디렉션용 참고 이미지가 필요(에셋필요 O)하고, 우측 결과에 NASA 공개 사진이 쓰임

#### [Interactive plush shark side-by-side](comparison__interactive-plush-shark-side-by-side__2107773295676227691.md)
`comparison__interactive-plush-shark-side-by-side__2107773295676227691` · 4:5 · 18s · 조회 118K · 에셋필요 X

- **요약**: 파란 천 재질의 봉제 상어 인형을 잡아 늘리고 먹이를 주면 헤엄쳐 쫓는 WebGPU 인터랙티브 데모를 Opus 5.5와 GPT-6 Astra로 번갈아 비교한 영상
- **어울리는 경우**: 귀여운 캐릭터·마스코트 등장 컷 / 봉제·패브릭 제품 티저 / 색상 팔레트 바리에이션 소개 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 보송한 패브릭·크림색 배 재질의 봉제 인형 / 둥둥 떠서 헤엄치는 아이들 모션과 그림자 / 파랑·네이비·핑크 팔레트 전환 / 에디토리얼 제품 페이지형 UI
- **스타일**: 따뜻한 오프화이트 배경에 하늘색·네이비·핑크 봉제 상어가 공중에 떠 있고 바닥에 부드러운 그림자, 좌상단 이탤릭 세리프 'Plush Shark.' 타이틀과 우측 설정 패널. 차분하고 귀여운 미니멀 3D.
- **기술**: WebGPU, 소프트바디, 단일 HTML 파일
- **프롬프트 구조**: 상어 외형·재질 서술 → 상호작용 불릿 목록 → 물리 품질 → 컨트롤 → UI 분위기 → 전달 조건 순서의 중간 길이 스펙
- **태그**: 봉제인형, 상어, 캐릭터, soft-body, WebGPU, 3D, 에디토리얼, 비교영상, 귀여움
- **주의**: 위(Claude Opus 5.5 10.35$)·아래(GPT-6 Astra 8.38$) 분할 비교 영상으로 모델명·비용 라벨이 붙어 있음. Opus 쪽은 부드럽고 단순한 실루엣, Astra 쪽은 큰 단추 눈·이빨이 있는 다른 디자인이니 패널을 구분해서 볼 것

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

#### [Radial engine animation comparison](comparison__radial-engine-animation-comparison__2116606788241969445.md)
`comparison__radial-engine-animation-comparison__2116606788241969445` · 1:1 · 11s · 조회 87K · 에셋필요 X

- **요약**: 9기통 성형 항공기 엔진의 피스톤·마스터 로드·흡배기 사이클을 남색 배경 2D 기술 도해 루프로 만든 결과를 Gemini Carbon·Gemini 4 Argon·Opus 5.5·6.1 Sol 네 모델로 2x2 비교한 영상
- **어울리는 경우**: 엔진·기계 장치 작동 원리 설명 / 순서·주기(사이클)가 있는 과정 시각화 / 공학·과학 강의의 단면도 인서트 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 하나의 크랭크 각도로 동기화된 피스톤·로드 연동 / 파란 혼합기→주황 연소→회색 배기의 색 코딩 / 점화 순서대로 원형을 따라 튀는 섬광 / 얇은 외곽선과 해칭의 단면 금속 표현
- **스타일**: 짙은 남색(#0b1220 계열) 배경 중앙에 밝은 스틸 그레이 2D 엔진 정면 단면, 파랑·주황·흰 섬광의 절제된 포인트 색. Opus 쪽은 파란 흡기관과 은은한 프로펠러 블러 원이 더해진 프리미엄 엔지니어링 설명 화면.
- **기술**: Three.js(메타 기준), Canvas/SVG
- **프롬프트 구조**: STYLE(strict) / THE ENGINE / THE CYCLE / ANIMATION / KEYBOARD / TECHNICAL 섹션으로 나눠 기계적 정확성과 점화 순서를 지정하고, 마지막에 직접 열어 검증하라는 체크 지시를 붙인 스펙
- **태그**: 성형엔진, 작동원리, 단면도, 2D, 기술도해, 루프, 다크네이비, 비교영상
- **주의**: 2x2 네 모델 비교 영상으로 각 칸 상단에 모델명 라벨이 있음. Opus 5.5는 좌하단 칸. 메타 tools는 Three.js지만 프롬프트는 Canvas/SVG 2D를 요구

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

#### [Gemini 4 Argon vs Opus 5.5 task comparison](comparison__gemini-4-argon-vs-opus-5-5-task-comparison__2110442447495127067.md)
`comparison__gemini-4-argon-vs-opus-5-5-task-comparison__2110442447495127067` · 16:9 · 15s · 조회 68K · 에셋필요 X

- **요약**: 폭포·바위·수련이 있는 살아있는 잉어 연못과 '먹이 주기' 버튼을 Three.js로 만든 결과를 Opus 5.5와 Gemini 4 Argon으로 좌우 비교한 영상
- **어울리는 경우**: 자연·정원 분위기의 휴식 컷 / 탑뷰 디오라마형 장면 전환 / 상호작용(먹이 → 물고기 반응) 데모 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 위에서 내려다보는 원형 연못과 바위 테두리 / 연못 속을 떼지어 헤엄치는 잉어 / 작은 폭포와 수면 물결 / 연잎·수련·풀숲 환경 디테일
- **스타일**: Opus 쪽은 연두 잔디와 회색 바위로 둘러싼 맑은 청록 연못, 밝은 낮 햇빛의 스타일라이즈드 3D. Gemini 쪽은 어두운 녹색 배경에 진한 청록 물과 주황 버튼 UI.
- **기술**: Three.js, 단일 HTML 파일
- **프롬프트 구조**: 원하는 장면 요소·살아있는 느낌·먹이 주기 동작·카메라 조작을 한 문단에 나열한 짧은 자유 서술
- **태그**: 잉어연못, 정원, 자연, Three.js, 3D, 탑뷰, 인터랙티브, 비교영상
- **주의**: 좌(Opus 5.5)·우(Gemini 4 Argon) 분할 비교 영상으로 하단에 모델명 라벨이 있음. 화면 녹화에 가깝고 카메라가 거의 고정

#### [Electric motor 3D animation comparison](comparison__electric-motor-3d-animation-comparison__2111513156589629941.md)
`comparison__electric-motor-3d-animation-comparison__2111513156589629941` · 약 1:1.27 (720x916) · 40s · 조회 65K · 에셋필요 X

- **요약**: 'Electric motor animation model comparison'과 같은 40초 전기모터 Three.js 프롬프트로 만든 결과를 DeepSeek V4.1 Flash 1017과 Opus 5.5로 위아래 비교한 영상
- **어울리는 경우**: 기계·전기 장치 작동 원리 설명 / 제품 분해도·컷어웨이 / 공학 강의의 단계별 원리 인서트 / 저가·고가 모델 결과 비교 콘텐츠
- **잘하는 표현**: 축을 따라 부품이 분리되는 분해도 / 반투명 하우징 속 코일·로터 노출 / 회전 자기장·전류를 색 라인으로 표시 / 단면 클로즈업과 냉각 흐름 표현
- **스타일**: 검정~짙은 남색 배경에 은색 알루미늄·구리 코일의 PBR 모터, 강한 화이트 림라이트와 무지개빛 자기장 라인, 좌상단 작은 섹션 라벨. 다크 테크 제품 광고 톤의 3D.
- **기술**: Three.js, PBR 재질, 고정 40초 타임라인
- **프롬프트 구조**: 출력 사양 고정 → 초 단위 구간별 장면·자막 → 비주얼·카메라·애니메이션 요구사항 순서의 벤치마크형 스펙(2110065587279798719와 동일 프롬프트)
- **태그**: 전기모터, 작동원리, exploded-view, 컷어웨이, Three.js, 3D, 다크테크, 비교영상
- **주의**: 위(DeepSeek V4.1 Flash 1017 $1.25)·아래(Opus 5.5 $16.36) 분할 비교 영상으로 모델명·비용 라벨이 붙어 있음. 아래 Opus 패널 영상은 2110065587279798719 사례와 같은 결과물이라 하나만 참고해도 됨

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

#### [Animated journey through five worlds](comparison__animated-journey-through-five-worlds__2112671240964219290.md)
`comparison__animated-journey-through-five-worlds__2112671240964219290` · 16:9 · 24s · 조회 56K · 에셋필요 X

- **요약**: 테라코타 주황 큐브 캐릭터가 바다·도시·우주·숲·네온 다섯 세계를 오가며 모습을 바꾸는 모션 디자인 영상을 Opus 5.5와 Sonnet 5.5로 좌우 비교한 영상
- **어울리는 경우**: 챕터·주제 전환 몽타주 / 마스코트 캐릭터가 여러 상황을 여행하는 오프닝 / 같은 대상이 맥락에 따라 변신하는 은유 / 모델 비교 콘텐츠
- **잘하는 표현**: 장면이 바뀌어도 이어지는 매치컷 전환 / 세계마다 소품(스노클·모자·헬멧·선글라스)으로 변신하는 캐릭터 / 장면별 뚜렷한 배경 팔레트 / 마지막 글자 등장 로고 리빌
- **스타일**: 크림색 화면에서 시작해 파란 바다·보랏빛 야경 도시·보라 우주·초록 숲·신스웨이브 네온 석양으로 바뀌는 플랫+그라데이션 2D 일러스트, 둥글고 귀여운 주황 큐브 캐릭터. 밝고 경쾌한 키즈 애니메이션 톤.
- **프롬프트 구조**: 영상 제목·캐릭터·다섯 세계·박자에 맞춘 매치컷 전환만 적은 세 문장짜리 짧은 브리프
- **태그**: 캐릭터, 마스코트, 매치컷, 장면전환, 2D, 모션디자인, 신스웨이브, 비교영상
- **주의**: 좌(Claude Opus 5.5 High, 36분)·우(Claude Sonnet 5.5 High, 26분) 분할 비교 영상으로 라벨과 '@MrTacticalX' 워터마크가 있음. 캐릭터가 Claude를 모티프로 한 마스코트라 그대로 쓰기보다 구성만 참고할 것

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

#### [Ember Vale 3D open-world action RPG](comparison__ember-vale-3d-open-world-action-rpg__2117222592536789149.md)
`comparison__ember-vale-3d-open-world-action-rpg__2117222592536789149` · 16:9 · 48s · 조회 49K · 에셋필요 X

- **요약**: 마을·숲·폐허·보스전이 있는 3D 오픈월드 액션 RPG 'Ember Vale'를 GPT-6.2 Astra·Fable 5.5·Opus 5.5·Fable 5.1 네 모델이 만든 게임 플레이를 2x2로 비교하고 점수표로 끝나는 영상
- **어울리는 경우**: 모델/툴 결과 비교·평가 콘텐츠 / 점수·순위 발표 카드 / 게임 개발 사례 소개 / 여러 결과를 한 화면에 묶는 그리드 구성
- **잘하는 표현**: 네 결과를 한 화면에 동시에 보여주는 2x2 그리드 / 칸마다 점수 배지 / 마지막의 큰 숫자 점수 카드(GAMEPLAY·VISUALS·PHYSICS·POLISH) / 마법 이펙트와 낮밤 조명
- **스타일**: 연보라 그라데이션 프레임 위에 둥근 모서리 카드 4개로 게임 화면을 배치, 게임은 스타일라이즈드 3D 숲·마을과 보라·주황 이펙트. 마지막 점수 카드는 반투명 보라 카드에 큰 흰 숫자.
- **프롬프트 구조**: WORLD / PLAYER / RPG / LOOK 섹션으로 게임 요소·조작키·적 AI·퀘스트·HUD를 불릿으로 정의한 게임 기획서형 스펙
- **태그**: 게임, RPG, 오픈월드, 3D, 2x2그리드, 점수카드, 모델평가, 비교영상, 화면녹화
- **주의**: 4개 모델 동시 비교로 각 칸에 모델명·점수가 있음. Opus 5.5는 좌하단(7.8/10). 편집된 모션그래픽이 아니라 게임 플레이 화면 녹화이며, 점수표에서 Opus는 1위가 아님

#### [Three.js Newton's cradle: Opus vs Astra 6](comparison__three-js-newton-s-cradle-opus-vs-astra-6__2108625335122026542.md)
`comparison__three-js-newton-s-cradle-opus-vs-astra-6__2108625335122026542` · 약 2:1 (1440x720) · 24s · 조회 47K · 에셋필요 O

- **요약**: 크롬 프레임에 매달린 다섯 개 강철 공이 충돌을 주고받는 뉴턴의 요람을 제품 촬영 스튜디오처럼 Three.js로 만든 결과를 Opus 5.5와 Astra 6로 좌우 비교한 영상
- **어울리는 경우**: 운동량 보존·충돌 같은 물리 개념 설명 / 인과·연쇄 반응 은유 컷 / 고급 제품 촬영 느낌의 정적 배경 루프 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 고정 카메라의 차분한 제품 사진 구도 / 크롬·스테인리스 반사 재질 / 공 아래 따라 움직이는 부드러운 그림자 / 1개·2개 공 모드의 정확한 진자 충돌
- **스타일**: Opus 쪽은 아주 밝은 아이보리~흰 무지 배경에 가는 은색 프레임과 회색 크롬 공, Astra 쪽은 더 따뜻한 베이지 배경. 하단에 작은 알약형 컨트롤 바만 있는 절제된 오프화이트 제품 사진 톤의 3D.
- **기술**: Three.js, 진자 물리 시뮬레이션, 절차적 반사 환경, 단일 HTML 파일
- **프롬프트 구조**: 구도·렌즈·카메라 → 구조물 치수 → 금속 재질·조명 → 물리 시뮬 규칙 → 컨트롤 → 금지 사항 → 완료 전 체크리스트 순서로 아주 길게 쓴 서술형 스펙
- **태그**: 뉴턴의요람, 물리, 충돌, 크롬, Three.js, 3D, 제품촬영, 오프화이트, 비교영상
- **주의**: 좌(Opus 5.5)·우(Astra 6) 분할 비교 영상으로 좌상단에 모델명 라벨이 있음. 구조 참고용 이미지가 첨부된 프롬프트(에셋필요 O)

#### [3D watermelon fur render comparison](comparison__3d-watermelon-fur-render-comparison__2111501344750059978.md)
`comparison__3d-watermelon-fur-render-comparison__2111501344750059978` · 4:5 · 15s · 조회 46K · 에셋필요 X

- **요약**: 긴 초록 털로 덮인 수박을 돌리고 확대하면 털이 휘고 갈라지는 Three.js 퍼 렌더링을 Opus 5.5와 Gemini 4 Argon으로 위아래 비교한 영상
- **어울리는 경우**: 털·잔디 같은 질감 재질 스터디 / 엉뚱한 초현실 오브젝트 티저 / 회전·확대로 디테일을 보여주는 제품 클로즈업 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 셸 텍스처링+가닥 털의 선명한 퍼 / 줄무늬가 털 끝까지 유지되는 색 표현 / 커서로 쓸면 갈라지는 털 / 근접 확대 시 털결 디테일
- **스타일**: 수박 과육 같은 연분홍 그라데이션 배경 한가운데 초록·진초록 줄무늬의 복슬복슬한 수박, 꼭지와 덩굴손 디테일. UI가 거의 없는 미니멀한 초현실 머티리얼 스터디 3D.
- **기술**: Three.js r147, 셸 텍스처링, 인스턴스드 가닥 털, Kajiya-Kay 하이라이트, 단일 HTML 파일
- **프롬프트 구조**: SCENE & LOOK / FUR / INTERACTION / UI & ROBUSTNESS 섹션으로 치수·색 코드·셸 수·털 개수까지 수치로 지정한 상세 스펙
- **태그**: 털, fur, 수박, 초현실, Three.js, 3D, material-study, 핑크배경, 비교영상
- **주의**: 위(Claude Opus 5.5 8.98$)·아래(Gemini 4 Argon 0.34$) 분할 비교 영상으로 모델명·비용 라벨이 붙어 있음. 스타일 참고는 위쪽 Opus 패널 기준

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

#### [Storm in a bottle Blender comparison](comparison__storm-in-a-bottle-blender-comparison__2112184796419883354.md)
`comparison__storm-in-a-bottle-blender-comparison__2112184796419883354` · 16:9 · 25s · 조회 42K · 에셋필요 X

- **요약**: 어두운 서재 책상 위 유리병 속 작은 바다에 폭풍이 일어 범선이 흔들리다 잦아드는 Blender 시네마틱 애니메이션을 GPT-6 Astra와 Opus 5.5로 좌우 비교한 영상
- **어울리는 경우**: 위기·혼란이 닥쳤다 잦아드는 감정 곡선 은유 / 미니어처 세계 오프닝 / 어둡고 아늑한 분위기의 이야기 도입 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 병 안의 거친 파도·비·번개 / 스탠드·촛불이 비추는 어두운 실내 조명 / 지도·나침반 같은 책상 소품 디테일 / 근접 샷과 와이드 샷을 오가는 카메라
- **스타일**: 어두운 남색 방과 나무 책상, 녹색 뱅커스 램프·촛불의 따뜻한 주황 빛, 병 속 청록 파도와 흰 돛의 범선. 사실적인 저조도 시네마틱 3D.
- **기술**: Blender
- **프롬프트 구조**: 장소·소품 → 시간에 따른 사건 전개(폭풍 고조 → 진정)를 한 문단으로 쓴 짧은 시나리오형 브리프
- **태그**: 폭풍, 병속의배, 미니어처, Blender, 시네마틱, 3D, 저조도, 비교영상
- **주의**: 좌(GPT-6 Astra High, 24분)·우(Claude Opus 5.5 High, 82분) 분할 비교 영상으로 상단에 모델명·제작시간 라벨이 있음

#### [Cozy village rendering comparison](comparison__cozy-village-rendering-comparison__2112848340224258550.md)
`comparison__cozy-village-rendering-comparison__2112848340224258550` · 16:9 · 40s · 조회 41K · 에셋필요 X

- **요약**: 강가 계곡 마을이 노을에서 푸른 저녁으로 바뀌며 가로등과 창이 하나씩 켜지는 Blender 시네마틱 애니메이션을 Team Sonnet 5.5(10 agents)와 Opus 5.5로 좌우 비교한 영상
- **어울리는 경우**: 따뜻하고 평화로운 분위기의 오프닝·엔딩 / 시간 흐름(낮→밤) 표현 / 공동체·마을 은유 컷 / 멀티에이전트 vs 단일 모델 비교 콘텐츠
- **잘하는 표현**: 노을에서 별밤으로 넘어가는 조명 변화 / 하나씩 켜지는 창문·전구 줄 / 풍차·물레방아·굴뚝 연기 같은 살아있는 디테일 / 드론처럼 마을 위를 도는 카메라
- **스타일**: 짙은 녹색 숲과 강, 빨간 지붕·목골조 집이 있는 유럽풍 마을, 해 질 녘 금빛에서 남색 밤과 따뜻한 노란 불빛으로. Opus 쪽은 안개가 낀 더 차분하고 사실적인 톤의 3D.
- **기술**: Blender
- **프롬프트 구조**: 마을 구성 요소 나열 → 움직이는 디테일 → 노을에서 밤으로의 시간 전개를 한 문단으로 쓴 시나리오형 브리프
- **태그**: 마을, 노을, 밤, Blender, 시네마틱, 3D, 시간경과, 비교영상
- **주의**: 좌(Team Sonnet 5.5 10 agents, 77분)·우(Claude Opus 5.5 High, 87분) 분할 비교 영상으로 모델명·제작시간 라벨과 '@MrTacticalX' 워터마크가 있음

#### [Haunted house at different effort levels](comparison__haunted-house-at-different-effort-levels__2112756630203011516.md)
`comparison__haunted-house-at-different-effort-levels__2112756630203011516` · 16:9 · 46s · 조회 39K · 에셋필요 X

- **요약**: 보름달 아래 언덕 위 낡은 유령의 집이 깨어나는(호박등·안개·박쥐·유령·열리는 문) Blender 애니메이션을 Opus 5.5의 Extra High와 Low 노력 수준으로 좌우 비교한 영상
- **어울리는 경우**: 같은 모델의 설정(노력 수준) 차이 비교 / 할로윈·공포 분위기 인서트 / 긴장감이 고조됐다 가라앉는 장면 / 시네마틱 3D 환경 참고
- **잘하는 표현**: 하나씩 켜지는 잭오랜턴의 주황 불빛 / 바닥을 깔리는 안개와 청록 문틈 빛 / 창가에 떠오르는 유령 실루엣 / 굴뚝에서 쏟아지는 박쥐 떼
- **스타일**: 짙은 청회색 밤하늘과 보름달, 검은 고목과 낡은 목조 집, 주황 호박등과 청록 유령 빛의 두 포인트 색. 어둡고 안개 낀 사실적 시네마틱 3D.
- **기술**: Blender
- **프롬프트 구조**: 장소·소품 → 사건이 차례로 일어나는 전개 → 고요한 밤으로 복귀를 한 문단으로 쓴 시나리오형 브리프
- **태그**: 유령의집, 할로윈, 공포, Blender, 시네마틱, 3D, 노력수준비교, 저조도
- **주의**: 좌(Claude Opus 5.5 Extra High, 142분)·우(Low, 16분) 분할 비교로 둘 다 Opus 결과이며 상단 라벨과 '@MrTacticalX' 워터마크가 있음. 화면이 매우 어두움

#### [Jelly pumpkin render comparison](comparison__jelly-pumpkin-render-comparison__2110746878040055904.md)
`comparison__jelly-pumpkin-render-comparison__2110746878040055904` · 4:5 · 14s · 조회 39K · 에셋필요 X

- **요약**: 잭오랜턴 얼굴이 빛나는 젤리 호박을 누르고 들어 올리고 사탕을 쏟는 Three.js 데모를 Opus 5.5와 Gemini Argon 4로 위아래 비교한 영상
- **어울리는 경우**: 할로윈 시즌 인서트 / 젤리·사탕 같은 말랑한 오브젝트 티저 / 버튼으로 표정(얼굴) 바꾸기 같은 상태 전환 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 속에서 빛이 새어 나오는 반투명 젤리 호박 / 줄기를 끌어 올렸다 떨어뜨리는 탄성 / 얼굴 모양 교체 / 위에서 쏟아지는 알록달록 사탕
- **스타일**: Opus 쪽은 흰 배경에 붉은 주황 광택 젤리 호박과 노란 발광 얼굴, 보라·초록 작은 호박, 좌상단 이탤릭 세리프 'Jelly / Pumpkin.' 타이틀. 밝고 달콤한 에디토리얼 제품 3D.
- **기술**: Three.js, 단일 HTML 파일
- **프롬프트 구조**: SCENE / INTERACTION / UI 섹션으로 '짧고 기본적으로' 만들라며 세그먼트 수·재질·버튼 동작을 구체적으로 지정한 간단 스펙
- **태그**: 젤리, 호박, 할로윈, Three.js, 3D, 인터랙티브, 에디토리얼, 비교영상
- **주의**: 위(Opus 5.5 $2.1)·아래(Gemini Argon 4 $4) 분할 비교 영상으로 모델명·비용 라벨이 크게 붙어 있음. 프롬프트는 투과·발광 없는 로우폴리·Arial·기본 버튼을 요구하지만 Opus 결과는 발광 젤리 재질과 세리프 타이틀이라 프롬프트와 결과가 다름(아래 Gemini 쪽이 프롬프트에 가까움)

#### [Jelly koi pond model comparison](comparison__jelly-koi-pond-model-comparison__2108256366879981677.md)
`comparison__jelly-koi-pond-model-comparison__2108256366879981677` · 4:5 · 21s · 조회 38K · 에셋필요 X

- **요약**: 연못 전체가 반투명 젤리로 된 미니 일본 정원(잉어·연잎·개구리)을 잡아 늘리면 출렁이는 인터랙티브 3D를 Opus 5.5와 GPT-6 Astra로 위아래 비교한 영상
- **어울리는 경우**: 동양 정원·자연 모티프의 귀여운 인서트 / 젤리·디저트형 제품 티저 / 민트·블루·핑크 색 바리에이션 소개 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 두께감 있는 반투명 젤리 슬래브 / 안에 갇힌 잉어·조약돌과 표면의 연잎·수련 / 늘리면 크게 휘었다 복원되는 소프트바디 / 색상 프리셋 전환
- **스타일**: 연한 세이지 그린 배경에 민트·블루·핑크 젤리 연못이 떠 있고, 좌상단 이탤릭 세리프 'Jelly Koi Pond.' 타이틀과 하단 작은 컨트롤 바. 파스텔 톤의 매거진형 미니멀 3D.
- **프롬프트 구조**: 장면 묘사 → 젤리 물리 상호작용 불릿 → 컨트롤 → 에디토리얼 레이아웃 → 절차적 생성·안정성 조건 순서의 중간 길이 스펙
- **태그**: 젤리, 잉어연못, 일본정원, soft-body, 3D, 파스텔, 에디토리얼, 비교영상
- **주의**: 위(Claude Opus 5.5 12.38$)·아래(GPT-6 Astra 15.57$) 분할 비교 영상으로 모델명·비용 라벨이 붙어 있음. Opus 쪽 젤리 가장자리가 흐릿하게 번져 보임

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

#### [Three-model one-shot build comparison](comparison__three-model-one-shot-build-comparison__2110454477027496395.md)
`comparison__three-model-one-shot-build-comparison__2110454477027496395` · 약 1.50:1 (1080x720) · 15s · 조회 33K · 에셋필요 O

- **요약**: 기존 앱 화면들의 분위기를 읽어 손으로 흔드는 마스코트가 있는 모바일 웰컴 화면을 만든 결과를 Opus 5.5·GPT-6.1 Sol·Gemini 4 Argon 세 모델로 아이폰 목업 3개에 나란히 비교한 영상
- **어울리는 경우**: 앱 온보딩·웰컴 화면 소개 / 귀여운 손그림 마스코트 등장 / 모바일 UI 결과 비교 / 따뜻한 감성의 인사 장면
- **잘하는 표현**: 'hello'가 손글씨로 써지는 타이핑 연출 / 아이폰 프레임 안 모바일 화면 구성 / 손 흔드는 마스코트 캐릭터 / 아래에서 올라오는 Get Started 버튼
- **스타일**: 흰 배경에 아이폰 목업 3대, 화면은 크림색 종이 톤과 손글씨 폰트, 올리브 그린 버튼. Opus 쪽은 화분·원형 러그 위 감자 같은 주황 새싹 마스코트의 파스텔 손그림 일러스트.
- **기술**: Appllama MCP, 앱 디자인 스킬
- **프롬프트 구조**: MCP로 참고 앱 화면을 읽고 웰컴 화면·마스코트·스와이프 인터랙션을 만들라는 한 문장 지시
- **태그**: 모바일앱, 온보딩, 마스코트, 손그림, 아이폰목업, 파스텔, 비교영상, UI
- **주의**: 좌(Opus 5.5)·중(GPT-6.1 Sol)·우(Gemini 4 Argon) 3분할 비교 영상으로 상단 라벨이 있음. 실제 앱(Bunpo, Cat on Chair, Grug) 화면을 참고 에셋으로 읽어 미감을 맞춘 결과라 재현하려면 참고 화면이 필요(에셋필요 O)

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

#### [DeepSeek vs Opus 5.5 Rubik's cube solve test](comparison__deepseek-vs-opus-5-5-rubik-s-cube-solve-test__2111754643604636049.md)
`comparison__deepseek-vs-opus-5-5-rubik-s-cube-solve-test__2111754643604636049` · 1:1 · 12s · 조회 30K · 에셋필요 X

- **요약**: 지정한 스크램블의 3x3 큐브를 화면에서 직접 맞추며 타이머·현재 수·수 카운터를 보여주는 Three.js 결과를 DeepSeek V4.1 Flash와 Opus 5.5로 좌우 비교한 영상
- **어울리는 경우**: 문제 해결·알고리즘 과정 시각화 / 타이머가 있는 도전·챌린지 컷 / 단계별 진행을 보여주는 스텝 카운터 / 모델 성공/실패 비교 콘텐츠
- **잘하는 표현**: 한 면씩 회전하는 큐브 애니메이션 / 큰 숫자 타이머와 현재 수(D2, R2…) 배지 / 완성 순간 초록색으로 바뀌는 타이머와 'SOLVED' / 밝은 무채색 배경의 깔끔한 정보 레이아웃
- **스타일**: 연회색 오프화이트 배경 위 원색(빨강·파랑·초록·노랑·주황·흰) 3D 큐브, 위쪽에 굵은 검정 타이머 숫자와 작은 검정 배지. 깔끔한 미니멀 제품 데모 톤.
- **기술**: Three.js, 단일 HTML 파일
- **프롬프트 구조**: 색 배치·스크램블·풀이 조건·애니메이션 타이밍·타이머 표시를 번호 매긴 6개 규칙으로 간결하게 정의
- **태그**: 루빅스큐브, 퍼즐, 타이머, 알고리즘, Three.js, 3D, 오프화이트, 비교영상
- **주의**: 좌(V4.1 Flash $0.20, not solved)·우(Opus 5.5 $0.81, solved) 분할 비교 영상으로 상단에 모델명·비용·성공 여부 라벨과 '@semichenkko' 워터마크가 있음. 왼쪽은 한 수 두고 멈춰 있음

#### [Voxel pagoda island model comparison](comparison__voxel-pagoda-island-model-comparison__2113687234448875770.md)
`comparison__voxel-pagoda-island-model-comparison__2113687234448875770` · 16:9 · 30s · 조회 30K · 에셋필요 X

- **요약**: 오층탑 같은 일본식 탑과 벚꽃·폭포·떠다니는 바위가 있는 공중 섬 복셀 디오라마를 Three.js+React로 만든 결과를 Kimi 3.1 Pro와 Opus 5.5로 좌우 비교한 영상
- **어울리는 경우**: 동양·일본 테마 오프닝 / 미니어처 세계관 소개 / 천천히 회전하는 디오라마 배경 루프 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 층층이 쌓인 곡선 지붕 탑과 등불 / 분홍 벚꽃·초록 숲이 빼곡한 복셀 섬 / 섬 아래로 떨어지는 폭포와 공중에 뜬 바위 / 주위를 나는 용·새와 흩날리는 꽃잎
- **스타일**: 연분홍~살구빛 노을 하늘과 흐린 바위 기둥 배경에 초록·분홍·주황의 정교한 복셀 공중 섬, 금빛 조명과 은은한 블룸. 따뜻하고 화사한 미니어처 디오라마 3D.
- **기술**: Three.js, React
- **프롬프트 구조**: 섬 지형 → 탑 → 식생 → 구조물 → 주변 요소 → 팔레트·조명 → 애니메이션 → 카메라 순서로 한 줄씩 나열한 장면 묘사형 프롬프트
- **태그**: 복셀, 탑, 일본, 벚꽃, 공중섬, 디오라마, Three.js, 3D, 비교영상
- **주의**: 좌(Kimi 3.1 Pro $5.71)·우(Opus 5.5 $17.13) 분할 비교 영상으로 모델명·비용 라벨이 붙어 있음. 두 결과 모두 프롬프트에 없는 용이 등장

#### [T-rex trying to ride a bicycle](comparison__t-rex-trying-to-ride-a-bicycle__2116973463378248107.md)
`comparison__t-rex-trying-to-ride-a-bicycle__2116973463378248107` · 1:1 · 12s · 조회 27K · 에셋필요 X

- **요약**: 팔이 짧아 핸들을 못 잡는 티라노가 자전거를 타며 버둥대는 12초 SVG 카툰 루프를 Gemini 4 Carbon·Gemini 4 Argon·Opus 5.5·6 Astra 네 모델로 2x2 비교한 영상
- **어울리는 경우**: 가벼운 유머·실패담 인서트 / '안 되는데 계속 시도하는' 상황 은유 / 캐릭터 루프 배경 / 모델/툴 결과 비교 콘텐츠
- **잘하는 표현**: 표정이 바뀌는 큰 머리 카툰 캐릭터 / 페달·체인·바퀴가 맞물려 도는 자전거 / 속도가 다른 레이어로 흐르는 패럴랙스 배경 / 머리에 내려앉는 새 같은 작은 개그
- **스타일**: Opus 쪽은 하늘색 하늘·흰 구름·초록 언덕과 전봇대가 있는 밝은 시골길에 연두색 티라노와 빨간 자전거, 깔끔한 외곽선과 부드러운 음영의 플랫 2D 카툰.
- **기술**: SVG, CSS, JavaScript
- **프롬프트 구조**: THE CHARACTER / THE BICYCLE / THE COMEDY / THE ANIMATION / THE BACKGROUND / REQUIREMENTS 섹션으로 캐릭터 연기와 개그 비트까지 지정한 애니메이션 연출 스펙
- **태그**: 티라노, 공룡, 자전거, 카툰, SVG, 2D, 루프, 패럴랙스, 비교영상
- **주의**: 2x2 네 모델 비교 영상으로 각 칸 상단에 모델명 라벨이 있음. Opus 5.5는 좌하단 칸

#### [Pixel-art tennis club diorama on a floating island](comparison__pixel-art-tennis-club-diorama-on-a-floating-island__2114758798845841679.md)
`comparison__pixel-art-tennis-club-diorama-on-a-floating-island__2114758798845841679` · 4:5 · 18s · 조회 27K · 에셋필요 X

- **요약**: 떠 있는 섬 위 테니스 클럽을 픽셀아트 아이소메트릭 3D 디오라마로 만들고 클레이·잔디·하드코트 전환과 랠리 시뮬을 Claude Opus 5.5와 ChatGPT-6.1 Sol 결과로 번갈아 비교한 영상
- **어울리는 경우**: 스포츠·경기 규칙 설명 인서트 / 공간·시설 배치를 한눈에 보여주는 장면 / 모델 결과 비교 콘텐츠 / 레트로 게임 감성의 오프닝
- **잘하는 표현**: 아이소메트릭 픽셀아트 디오라마(떠 있는 섬 단면) / 코트 표면·시간대 전환 / 작은 박스 인형들의 경기 애니메이션 / 카메라 90도 회전
- **스타일**: 오프화이트 페이지 배경에 떠 있는 흙섬, 주황 클레이·초록 잔디·파란 하드코트와 빨간 지붕 클럽하우스, 짙은 침엽수. 외곽선이 또렷한 저해상도 픽셀 3D로 밝고 장난감 같은 분위기.
- **기술**: Three.js, 직교 아이소메트릭 카메라, 저해상도 렌더 타깃, 깊이 외곽선, OKLab 64색 팔레트
- **프롬프트 구조**: 시리즈 엔진 설정을 괄호로 한 줄에 몰아 적고, 시설 목록 → 공 물리·선수 AI·경기 규칙 → 코트 위 생활 → 조작·UI 순으로 서술한 긴 문단형 스펙
- **태그**: 픽셀아트, isometric, 디오라마, 떠있는섬, 테니스, 스포츠시뮬, Three.js, 비교영상
- **주의**: 위(Claude Opus 5.5, 14.06$)·아래(ChatGPT-6.1 Sol, 3.55$) 분할 비교로 모델명·비용 라벨이 붙어 있음. Opus 쪽은 위 패널. 오른쪽에 컨트롤 패널이 함께 찍힌 웹페이지 캡처

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

#### [Galerie Nocturne CSS 3D museum walkthrough](comparison__galerie-nocturne-css-3d-museum-walkthrough__2110385278246654052.md)
`comparison__galerie-nocturne-css-3d-museum-walkthrough__2110385278246654052` · 16:9 · 43s · 조회 25K · 에셋필요 X

- **요약**: CSS 3D로 만든 야간 미술관 복도 'Galerie Nocturne'를 걸어 다니며 생성형 추상화 8점을 감상하는 화면을 Opus 5.5와 Gemini 4 Argon 결과로 좌우 비교한 브라우저 녹화
- **어울리는 경우**: 작품·사례를 차례로 보여주는 갤러리형 인서트 / 미술·디자인 강의의 작품 소개 / 1인칭 공간 이동(워크스루) 연출 / 모델 비교 콘텐츠
- **잘하는 표현**: 원근 복도를 따라가는 1인칭 카메라 이동 / 천장 스폿 조명과 바닥 반사 / 액자·캡션 카드가 붙은 작품 배치 / 몬드리안·컬러필드·옵아트 같은 생성 추상화
- **스타일**: 어두운 천장과 회갈색 벽, 흑백 체커보드 대리석 바닥(Opus) 위로 따뜻한 스폿 조명이 떨어지는 미술관 복도. 클래식 세리프 이탤릭 타이틀과 작은 대문자 캡션의 차분하고 고급스러운 야간 갤러리 무드.
- **기술**: CSS 3D 변환, canvas 생성 아트, 단일 HTML
- **프롬프트 구조**: 공간·재질·색상 코드 → 8점의 작품 종류 → 액자·캡션 → 내비게이션·미니맵 → 타이포·모바일 대응 순으로 짧게 나열한 한 문단 스펙
- **태그**: 미술관, gallery, CSS3D, 워크스루, 1인칭, 생성아트, 야간무드, 비교영상
- **주의**: 좌(Opus 5.5)·우(Argon) 분할 비교이며 브라우저 탭·주소창이 그대로 보이는 화면 녹화. 프롬프트의 '광택 대리석'은 Opus 쪽에서 흑백 체커보드로 나옴

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

#### [Gummy bear model comparison](comparison__gummy-bear-model-comparison__2114103699148800152.md)
`comparison__gummy-bear-model-comparison__2114103699148800152` · 16:9 · 56s · 조회 22K · 에셋필요 X

- **요약**: 흰 테이블 위 반투명 젤리 곰들을 잡아 늘리고 던지고 쏟아붓는 Three.js 소프트바디 데모를 Haiku 5.5·Sonnet 5.5·Opus 5.5·Fable 5.1 네 모델 결과로 2x2 동시 비교한 영상
- **어울리는 경우**: 여러 모델·도구 결과를 한 화면에서 비교 / 말랑한 제품·캔디 브랜드 티저 / 귀엽고 가벼운 분위기 전환 인서트
- **잘하는 표현**: 젤리 곰의 늘어남·튕김 소프트바디 / 색이 비치는 반투명 굴절 재질과 컬러 그림자 / 우르르 쏟아지는 더미 물리 / 에디토리얼 제품 페이지 UI
- **스타일**: 순백 배경에 체리·오렌지·레몬·사과·투명 파인애플 색 젤리 곰, 큰 이탤릭 세리프 'Gummy Bears.' 타이틀과 미니멀 카드 패널. 밝고 깨끗한 제품 광고 사진 같은 3D.
- **기술**: Three.js(CDN), 메타볼/마칭큐브 암시적 곡면, 형상 정합 소프트바디, ACES 톤매핑
- **프롬프트 구조**: 곰 외형·재질 → 물리(이게 핵심이라고 강조) → UI를 소제목 아래 불릿으로 나열한 단일 HTML 스펙
- **태그**: 젤리, 구미베어, soft-body, Three.js, 제품티저, 에디토리얼, material-study, 4분할비교
- **주의**: 4분할 비교 영상(좌상 Haiku, 우상 Sonnet, 좌하 Opus 5.5, 우하 Fable 5.1)으로 모델명 라벨이 붙어 있음. 메타 models에는 Fable 5.1이 빠져 있음

#### [Jelly cube spaceport comparison](comparison__jelly-cube-spaceport-comparison__2114132632166347208.md)
`comparison__jelly-cube-spaceport-comparison__2114132632166347208` · 4:5 · 18s · 조회 20K · 에셋필요 X

- **요약**: 열대 섬 우주기지를 젤리 블록 안에 담아 로켓 롤아웃·발사·부스터 귀환까지 돌리는 WebGPU 디오라마를 Claude Opus 5.5와 ChatGPT-6 Astra 결과로 번갈아 비교한 영상
- **어울리는 경우**: 로켓·우주 산업 설명 인서트 / 하나의 과정(발사→회수)을 미니어처로 보여주는 장면 / 모델 비교 콘텐츠
- **잘하는 표현**: 젤리 블록 단면 속 물·해저와 지층 / 출렁이는 얕은 물 시뮬과 커스틱 / 로켓 발사 연기·궤적과 카메라 상승 / 젤리 색상 프리셋(라임·퀴라소·블랙커런트) 전환
- **스타일**: 연회색 스튜디오 바닥 위 얇은 사각 젤리 판, 민트·파랑·보라로 바뀌는 투명 바다와 모래섬, 빨강·흰 발사탑. 이탤릭 세리프 'Launch Jelly.' 타이틀의 밝은 에디토리얼 머티리얼 스터디 3D.
- **기술**: WebGPU, WGSL, WebAudio, 단일 HTML
- **프롬프트 구조**: THE BLOCK·THE SCENE·WHAT HAPPENS·LIFE·RENDERING·CONTROLS & UI 대문자 섹션별로 사물과 사건 순서를 아주 촘촘히 나열한 시리즈형 스펙
- **태그**: 젤리디오라마, 로켓발사, 우주기지, WebGPU, 물시뮬, 단면, material-study, 비교영상
- **주의**: 위(Claude Opus 5.5, 23.51$)·아래(ChatGPT-6 Astra, 37.96$) 분할 비교. Opus 쪽은 위 패널이며 큐브라기보다 얇은 판 형태라 로켓·건물이 작게 보임

#### [Jelly dolphin physics comparison](comparison__jelly-dolphin-physics-comparison__2115015297195225283.md)
`comparison__jelly-dolphin-physics-comparison__2115015297195225283` · 4:5 · 18s · 조회 20K · 에셋필요 X

- **요약**: 두 겹 젤리로 만든 큰돌고래가 꼬리를 차고 분수공에서 젤리 방울을 뿜는 WebGPU 소프트바디 스터디를 Claude Opus 5.5와 GPT-6.1 Sol 결과로 번갈아 비교한 영상
- **어울리는 경우**: 해양 생물·동물 소개 인서트 / 말랑한 캐릭터·마스코트 티저 / 물리 시뮬 데모 / 모델 비교 콘텐츠
- **잘하는 표현**: 근육 변형으로 튀어 오르고 휘는 소프트바디 / 투명 젤리 속 우윳빛 배 층 / 튀어 흩어지는 작은 젤리 방울 / 색상 팔레트(청록·파랑·분홍) 전환
- **스타일**: 연베이지 스튜디오 스윕 배경에 청록·파랑·분홍 반투명 젤리 돌고래와 부드러운 그림자, 좌상단 이탤릭 세리프 'Dolphin Jelly.' 타이틀. 미니멀한 매거진 제품 사진 감성.
- **기술**: WebGPU, WGSL, XPBD 사면체 소프트바디, surface nets
- **프롬프트 구조**: 시리즈 엔진 기술을 한 문단에 요약한 뒤 형태 → 두 층 재질·무늬 → 인터랙션·UI를 해부학 용어로 촘촘히 적은 3문단 스펙
- **태그**: 젤리, 돌고래, soft-body, WebGPU, 해양생물, 에디토리얼, material-study, 비교영상
- **주의**: 위(Claude Opus 5.5, 5.19$)·아래(GPT-6.1 Sol, 2.92$) 분할 비교로 모델명·비용 라벨이 붙어 있음. Opus 쪽은 위 패널

#### [Da Vinci workshop 3D build: Gemini vs Opus](comparison__da-vinci-workshop-3d-build-gemini-vs-opus__2110121002332295599.md)
`comparison__da-vinci-workshop-3d-build-gemini-vs-opus__2110121002332295599` · 4:5 · 101s · 조회 19K · 에셋필요 X

- **요약**: 고서 속 레오나르도 다빈치 스케치 4점(비행기계·공중나사·장갑차·대형 석궁)을 클릭하면 작동하는 3D 모델로 살아나는 웹 경험을 Claude Opus 5.5와 Gemini 4 Argon 결과로 비교한 101초 영상
- **어울리는 경우**: 역사·발명품 강의 인서트 / 스케치가 입체 모델로 바뀌는 '설계도→실물' 연출 / 기계 작동 원리 설명 / 모델 비교 콘텐츠
- **잘하는 표현**: 양피지 책 페이지의 스케치 표현 / 나무 재질 기계 모델의 회전·작동 / 챕터 제목(01/04 등)으로 나눈 단계 구성 / 대비되는 청사진 홀로그램(Gemini 쪽)
- **스타일**: Opus 쪽은 어두운 공방 바닥 위 펼친 양피지 책과 따뜻한 나무색 기계 모델, 주황 계열 조명의 고풍스러운 3D. Gemini 쪽은 남색 배경에 시안 청사진 선과 HUD 패널로 대비됨.
- **기술**: Three.js, WebGL
- **프롬프트 구조**: 경험 이름 → 핵심 장치(고서) → 클릭 시 3D 전환 → 품질 요구를 4문장으로 짧게 적은 개념형 프롬프트
- **태그**: 다빈치, 발명품, 양피지, 스케치→3D, 기계작동, Three.js, 역사, 비교영상
- **주의**: 위(CLAUDE OPUS 5.5)·아래(GEMINI 4 ARGON) 분할에 VS 마크와 TECHHALLA 채널 로고가 붙은 편집 영상. 실존 인물(다빈치)의 실제 설계를 다룸

#### [Self-building mech comparison](comparison__self-building-mech-comparison__2112393665209303177.md)
`comparison__self-building-mech-comparison__2112393665209303177` · 16:9 · 25s · 조회 19K · 에셋필요 X

- **요약**: 어두운 격납고 바닥에 날아든 부품들이 스스로 조립되어 거대 메카가 되고, 눈·가슴 코어가 켜진 뒤 걸어 나와 히어로 포즈를 잡는 Blender 애니메이션을 Opus 5.5와 Sonnet 5.5로 좌우 비교한 영상
- **어울리는 경우**: '조각이 모여 완성된다'는 조립·구축 메타포 / 기술·로봇·제조 주제 오프닝 / 시스템 구성 요소 설명 / 모델 비교 콘텐츠
- **잘하는 표현**: 사방에서 날아와 맞물리는 부품 조립 / 전원이 들어오며 빛나는 코어·눈 / 증기 분출과 무게감 있는 걸음 / 클로즈업과 전신 샷을 섞은 시네마틱 카메라
- **스타일**: 검은 격납고에 시안 그리드 바닥과 흰 기둥 조명, 흰 장갑에 주황 포인트·청백색 발광 코어의 메카. 깔끔한 하드서피스 3D 렌더로 SF 애니 메카 감성.
- **기술**: Blender
- **프롬프트 구조**: 무대 → 조립 순서(발·다리·몸통·팔·머리) → 전원 켜짐 → 걸음과 히어로 포즈를 한 문단으로 적은 시간순 연출 프롬프트
- **태그**: 메카, 로봇, 자가조립, Blender, 시네마틱, 하드서피스, 다크테크, 비교영상
- **주의**: 좌(Claude Opus 5.5)·우(Claude Sonnet 5.5) 분할 비교로 모델명·제작 시간 라벨과 작성자 워터마크가 붙어 있음

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

#### [School yard futsal pixel-art diorama](comparison__school-yard-futsal-pixel-art-diorama__2116944633800368616.md)
`comparison__school-yard-futsal-pixel-art-diorama__2116944633800368616` · 4:5 · 17s · 조회 18K · 에셋필요 X

- **요약**: 떠 있는 섬 위 학교 운동장에서 5대5 풋살 경기가 열리는 픽셀아트 3D 디오라마를 Claude Sonnet 5.5와 Claude Opus 5.5 결과로 번갈아 비교한 영상
- **어울리는 경우**: 스포츠·팀 전술 설명 인서트 / 학교·동네 공간을 보여주는 장면 / 표면(재질) 바꾸기 비교 연출 / 모델 비교 콘텐츠
- **잘하는 표현**: 아이소메트릭 픽셀 디오라마와 철망 코트 / 코트 표면(고무·아스팔트·인조잔디·마루) 전환 / 작은 선수·관중 군중 애니메이션 / 섬 전체가 보이는 줌아웃
- **스타일**: Opus 쪽은 오프화이트 페이지에 밝은 연두 잔디·주황 테두리 파란 코트와 벽돌 학교 건물, 외곽선 또렷한 픽셀 3D. Sonnet 쪽은 파란 하늘 배경과 짙은 숲으로 더 선명한 색감.
- **기술**: Three.js r160, 직교 카메라, 저해상도 렌더 타깃, 깊이 외곽선, 양자화 팔레트
- **프롬프트 구조**: 렌더 방식 한 줄 → 장면 배치 → 경기 엔진·규칙 → 코트 표면별 물리 상수 → 페이지 레이아웃 순의 문단형 스펙
- **태그**: 픽셀아트, isometric, 디오라마, 풋살, 학교, 스포츠시뮬, Three.js, 비교영상
- **주의**: 위(Claude Sonnet 5.5, 57.07$)·아래(Claude Opus 5.5, 24.55$) 분할 비교로 Opus 쪽은 아래 패널. 컨트롤 패널이 함께 찍힌 웹페이지 캡처

#### [Interactive jelly hammerhead shark](comparison__interactive-jelly-hammerhead-shark__2115402023935893904.md)
`comparison__interactive-jelly-hammerhead-shark__2115402023935893904` · 4:5 · 19s · 조회 16K · 에셋필요 X

- **요약**: 두 겹 젤리로 만든 귀상어가 머리를 좌우로 훑고 꼬리를 흔드는 WebGPU 소프트바디 스터디를 Claude Opus 5.5와 GPT-6 Astra 결과로 번갈아 비교한 영상
- **어울리는 경우**: 해양 생물 소개 인서트 / 독특한 형태의 생물·캐릭터 쇼케이스 / 물리 시뮬 데모 / 모델 비교 콘텐츠
- **잘하는 표현**: 넓은 머리(두익)를 가진 형태의 소프트바디 변형 / 투명 젤리와 우윳빛 배 층 / 잡아 비틀고 뒤집는 인터랙션 / 색상 변형(파랑·주황·흰색)과 미끼 젤리 구슬
- **스타일**: 연회색 스튜디오 스윕 위 파랑·주황·흰색 반투명 젤리 상어와 옅은 그림자, 이탤릭 세리프 'Hammerhead Jelly.' 타이틀. 미니멀한 제품 사진 같은 머티리얼 스터디 3D.
- **기술**: WebGPU, SDF 모델링, XPBD 사면체 메시, Beer-Lambert 흡수
- **프롬프트 구조**: 형태(SDF·지느러미 레시피) → 재질·무늬 → 시뮬 → 근육 동작 → 인터랙션·표시값을 한 문단에 촘촘히 쓴 스펙
- **태그**: 젤리, 귀상어, soft-body, WebGPU, 해양생물, 에디토리얼, material-study, 비교영상
- **주의**: 위(Claude Opus 5.5, 9.22$)·아래(GPT-6 Astra, 10.8$) 분할 비교로 Opus 쪽은 위 패널

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

#### [Interactive koi pond side-by-side comparison](comparison__interactive-koi-pond-side-by-side-comparison__2108926847442378848.md)
`comparison__interactive-koi-pond-side-by-side-comparison__2108926847442378848` · 4:5 · 15s · 조회 15K · 에셋필요 X

- **요약**: 위에서 내려다본 청록 연못에 비단잉어를 떨어뜨리고 물결·소용돌이를 만드는 Three.js 인터랙티브 연못을 Claude Opus 5.5와 ChatGPT-6 Astra 결과로 번갈아 비교한 영상
- **어울리는 경우**: 차분한 휴식·명상 분위기 인서트 / 동양·정원 테마 배경 / '흐름·군집' 같은 개념의 은유 / 모델 비교 콘텐츠
- **잘하는 표현**: 탑다운 물 표면 커스틱과 굴절 / 헤엄치며 서로 피하는 잉어 군집 / 소용돌이와 퍼지는 물결 / 연잎·연꽃 장식
- **스타일**: Opus 쪽은 둥근 자갈 테두리 안 진한 청록 물, 초록 연잎과 분홍 연꽃, 빨강·노랑·흰 잉어가 떠 있는 사실적 탑다운 3D. Astra 쪽은 더 밝은 민트색 물에 잉어가 많음.
- **기술**: Three.js, WebGL, Web Audio
- **프롬프트 구조**: 시점·물 표현 → 하단 선택 패널 → 착수 연출 → 잉어 모델·행동 → 물 인터랙션·날씨 → 사운드 → 반응형 순의 문단형 요구 목록
- **태그**: 비단잉어, 연못, 탑다운, 물결, 커스틱, 군집, Three.js, 비교영상
- **주의**: 위(Claude Opus 5.5, 11.69$)·아래(ChatGPT-6 Astra, 12.25$) 분할 비교로 Opus 쪽은 위 패널

#### [3D canal and windmill scene model comparison](comparison__3d-canal-and-windmill-scene-model-comparison__2110329593441796383.md)
`comparison__3d-canal-and-windmill-scene-model-comparison__2110329593441796383` · 4:5 · 18s · 조회 15K · 에셋필요 X

- **요약**: 영국 운하의 갑문·오두막·풍차를 젤리 블록 단면에 담아 갑문 수위가 오르내리는 WebGPU 디오라마를 Claude Opus 5.5와 ChatGPT-6 Astra 결과로 번갈아 비교한 영상
- **어울리는 경우**: 갑문·수위차 같은 작동 원리 설명 / 마을·풍경을 미니어처로 보여주는 장면 / 단면으로 속을 보여주는 설명 인서트 / 모델 비교 콘텐츠
- **잘하는 표현**: 블록 앞면을 자른 단면 속 물과 지층 / 칸마다 다른 수위의 물 시뮬 / 풍차·오두막·벽돌 다리의 아기자기한 풍경 / 젤리 색상(노랑·보라) 전환
- **스타일**: 연회색 바닥 위 사각 젤리 블록, 연두 잔디 위 흰 오두막·흰 풍차·벽돌 갑문, 단면에 크림·분홍 지층과 노랑·보라 투명 물. 이탤릭 세리프 'Lock Jelly.' 타이틀의 밝은 미니어처 감성.
- **기술**: WebGPU, WGSL, 얕은 물 시뮬레이션, 단일 HTML
- **프롬프트 구조**: CONCEPT·LAYOUT·WATER·THE LOCK AND THE KEEPER 등 대문자 섹션에 배치와 갑문 작동 순서를 아주 상세히 적은 시리즈형 스펙
- **태그**: 젤리디오라마, 운하, 갑문, 풍차, 단면, WebGPU, material-study, 비교영상
- **주의**: 위(Claude Opus 5.5, 28.85$)·아래(ChatGPT-6 Astra, 19.83$) 분할 비교로 Opus 쪽은 위 패널. 메타 tools에 Gemini 4 Argon도 있지만 영상엔 두 모델만 나옴

#### [Soft-body jelly kiwi wedge simulation](comparison__soft-body-jelly-kiwi-wedge-simulation__2109932661204517203.md)
`comparison__soft-body-jelly-kiwi-wedge-simulation__2109932661204517203` · 약 1:1.27 (720x912) · 17s · 조회 15K · 에셋필요 X

- **요약**: 키위 단면 조각을 젤리로 만들어 잡아 늘리고 비트는 WebGPU 소프트바디 데모를 Claude Opus 5.5와 Claude Fable 5.1 결과로 번갈아 비교한 영상
- **어울리는 경우**: 과일·식품 브랜드 티저 / 말랑한 재질감 강조 인서트 / 물리 시뮬 데모 / 모델 비교 콘텐츠
- **잘하는 표현**: 씨앗과 방사 결이 비치는 반투명 과육 재질 / 들어 올리고 비틀 때의 소프트바디 변형 / 품종(그린·골드·루비) 색 전환 / 바닥에 번지는 컬러 그림자
- **스타일**: 연베이지 스튜디오 배경에 초록·노랑·빨강 반투명 키위 조각과 검은 씨, 이탤릭 세리프 'Kiwi Jelly.' 타이틀. 미니멀한 제품 사진 같은 머티리얼 스터디 3D.
- **기술**: WebGPU, WGSL, XPBD 사면체 소프트바디, PCSS 그림자
- **프롬프트 구조**: Object(형태·영역·씨앗) → Physics → Rendering → UI 섹션별로 수치와 셰이더 기법을 촘촘히 적은 스펙
- **태그**: 젤리, 키위, 과일, soft-body, WebGPU, 에디토리얼, material-study, 비교영상
- **주의**: 위(Claude Opus 5.5, 8.6$)·아래(Claude Fable 5.1, 24.04$) 분할 비교로 Opus 쪽은 위 패널. 메타에는 상대 모델이 적혀 있지 않음

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

#### [Whale image comparison: GPT-6 vs Opus](comparison__whale-image-comparison-gpt-6-vs-opus__2112487852156063849.md)
`comparison__whale-image-comparison-gpt-6-vs-opus__2112487852156063849` · 약 1:1.27 (720x912) · 18s · 조회 14K · 에셋필요 X

- **요약**: 털이 복슬한 봉제 고래를 잡아 늘리고 뒤집고 분수를 뿜게 하는 3D 인터랙티브 놀이터를 GPT-6 Astra와 Claude Opus 5.5 결과로 번갈아 비교한 영상
- **어울리는 경우**: 가볍고 웃긴 분위기 전환 인서트 / 캐릭터·마스코트 소개 / 장난감·굿즈 티저 / 모델 비교 콘텐츠
- **잘하는 표현**: 봉제 인형 털·천 재질 / 말랑하게 찌그러지는 소프트바디 / 큰 눈알의 코믹한 표정 / 색상 변형(파랑·분홍·흰색) 전환
- **스타일**: 따뜻한 연회색 스튜디오 배경에 파랑·분홍·흰색 털 인형 고래와 부드러운 그림자, 이탤릭 세리프 타이틀과 작은 컨트롤 패널. 귀엽고 촉감적인 머티리얼 스터디 3D.
- **프롬프트 구조**: 캐릭터 성격 → 물리·인터랙션 목록 → 재질 → 색상·조절값 → 페이지 연출을 짧은 문단 5개로 적은 개념형 프롬프트
- **태그**: 봉제인형, 고래, 털재질, soft-body, 코믹, 캐릭터, material-study, 비교영상
- **주의**: 위(GPT-6 Astra 'Plush Whale.', 9.12$)·아래(Claude Opus 5.5 'Derp Beluga.', 13.6$) 분할 비교로 Opus 쪽은 아래 패널. Opus는 프롬프트의 고래를 벨루가로 바꾸고 범고래 대신 분홍 색상을 넣음

#### [Pixel-art floating island lido across four models](comparison__pixel-art-floating-island-lido-across-four-models__2115595806665240630.md)
`comparison__pixel-art-floating-island-lido-across-four-models__2115595806665240630` · 약 1.58:1 (1140x720) · 18s · 조회 14K · 에셋필요 X

- **요약**: 떠 있는 섬 위 야외 수영장(다이빙대·레인 풀)을 픽셀아트 아이소메트릭 3D로 만든 결과를 Claude Sonnet·Claude Opus 5.5·GPT-6 Astra·GPT-6.1 Sol 네 모델로 2x2 동시 비교한 영상
- **어울리는 경우**: 여러 결과를 한 화면에 나란히 보여주는 비교 / 수영·다이빙 같은 스포츠 설명 / 여름·휴양 공간 소개 인서트
- **잘하는 표현**: 아이소메트릭 픽셀 디오라마(떠 있는 섬 단면) / 낮·노을·밤 시간대 전환 / 수영장 물 표면과 파라솔·탈의실 디테일 / 카메라 회전
- **스타일**: Opus 쪽은 오프화이트 배경에 갈색 흙섬, 청록 수영장 두 개와 파란 탈의실·알록달록 파라솔, 외곽선 픽셀 3D. 다른 패널은 파란 하늘(Sonnet), 크림 평면(Astra), 올리브 톤(Sol)으로 색감이 크게 다름.
- **기술**: Three.js, 직교 아이소메트릭 카메라, 저해상도 렌더 타깃, 깊이 외곽선, OKLab 64색 팔레트
- **프롬프트 구조**: 렌더 방식 한 줄 → 장면 → 다이빙 물리·채점 → 물 → 사람 → 조명·날씨·UI 순의 문단형 스펙
- **태그**: 픽셀아트, isometric, 디오라마, 수영장, 다이빙, 떠있는섬, Three.js, 4분할비교
- **주의**: 4분할 비교(좌상 Claude Sonnet 13.44$, 우상 Claude Opus 5.5 11.13$, 좌하 GPT-6 Astra 16.22$, 우하 GPT-6.1 Sol 5.01$)로 Opus 쪽은 오른쪽 위 패널

#### [Minecraft house and llama build comparison](comparison__minecraft-house-and-llama-build-comparison__2110807768550764628.md)
`comparison__minecraft-house-and-llama-build-comparison__2110807768550764628` · 4:5 · 19s · 조회 14K · 에셋필요 X

- **요약**: 마인크래프트 안에서 일본 민가풍 코티지가 4배속으로 지어진 뒤 노을빛 시네마틱 투어가 이어지는 장면을 Gemini 4 Argon과 Opus 5.5 결과로 번갈아 비교한 영상
- **어울리는 경우**: 단계적으로 쌓아 올리는 '구축 과정' 메타포 / 게임·마인크래프트 관련 강의 / 집·공간 설계 과정 설명 / 모델 비교 콘텐츠
- **잘하는 표현**: 블록이 쌓이며 집이 완성되는 타임랩스 / 노을빛 셰이더 조명과 안개 / 천천히 도는 시네마틱 카메라 투어 / 정원·울타리 소품 배치
- **스타일**: 마인크래프트 초원에 나무 블록 집과 침엽수, 옅은 보랏빛 하늘과 노을 역광, 부드러운 그림자. 셰이더를 얹은 듯한 따뜻하고 포근한 복셀 실사풍.
- **기술**: Minecraft Java Edition(네이티브, Blender 미사용)
- **프롬프트 구조**: 건물 스타일·재료 → 동물 → 조명 → 19초 구성(10초 4배속 빌드 + 9초 투어)과 금지 사항을 한 문장에 몰아 쓴 초단문 프롬프트
- **태그**: 마인크래프트, 복셀, 타임랩스, 건축, 노을, 시네마틱투어, 게임, 비교영상
- **주의**: 위(Gemini 4 Argon)·아래(Opus 5.5) 분할 비교로 Opus 쪽은 아래 패널. Opus 집은 단순한 나무 블록 위주로 흰 회벽·라마가 잘 안 보여 프롬프트 반영이 약함. 게임 화면이라 IP(마인크래프트) 확인 필요

#### [Offshore jelly cube diorama comparison](comparison__offshore-jelly-cube-diorama-comparison__2113401221910253853.md)
`comparison__offshore-jelly-cube-diorama-comparison__2113401221910253853` · 4:5 · 18s · 조회 14K · 에셋필요 X

- **요약**: 북해 해상 플랫폼과 풍력 발전기를 젤리 블록 바다에 담아 보급선·헬기·폭풍을 돌리는 WebGPU 디오라마를 Claude Opus 5.5와 GPT-6 Astra 결과로 번갈아 비교한 영상
- **어울리는 경우**: 에너지·해양 산업 설명 인서트 / 풍력·석유 플랫폼 구조 소개 / 날씨·파도 변화 연출 / 모델 비교 콘텐츠
- **잘하는 표현**: 넓은 젤리 바다의 파도·물보라 시뮬 / 해상 플랫폼·헬리데크·풍차 디테일 / 물 색상(청록·파랑·보라) 전환 / 수면 가까이 내려가는 카메라
- **스타일**: 연회색 스튜디오 바닥 위 얇고 넓은 사각 젤리 바다, 청록·파랑·보라 투명 물 위 흰 풍차와 주황·흰 플랫폼. 이탤릭 세리프 'Offshore Jelly.' 타이틀의 밝은 머티리얼 스터디 3D.
- **기술**: WebGPU, WGSL, WebAudio, 얕은 물 시뮬레이션, 단일 HTML
- **프롬프트 구조**: THE BLOCK·THE SCENE·WHAT HAPPENS·LIFE·CONTROLS & UI 대문자 섹션에 시설과 사건을 촘촘히 나열한 시리즈형 스펙
- **태그**: 젤리디오라마, 해상플랫폼, 풍력발전, 바다, 물시뮬, WebGPU, material-study, 비교영상
- **주의**: 위(Claude Opus 5.5, 14.2$)·아래(GPT-6 Astra, 12.09$) 분할 비교로 Opus 쪽은 위 패널. Opus 쪽은 바다 위주의 얇은 판이라 해저 단면이 거의 안 보임

#### [Arctic jelly iceberg diorama comparison](comparison__arctic-jelly-iceberg-diorama-comparison__2110517313413796092.md)
`comparison__arctic-jelly-iceberg-diorama-comparison__2110517313413796092` · 4:5 · 18s · 조회 13K · 에셋필요 X

- **요약**: 빙하·펭귄 서식지·연구기지가 있는 극지 만을 젤리 블록에 담아 빙산 붕괴와 쇄빙선을 돌리는 WebGPU 디오라마를 Claude Opus 5.5와 ChatGPT-6 Astra 결과로 번갈아 비교한 영상
- **어울리는 경우**: 기후·빙하 주제 설명 인서트 / 극지 생태 소개 / 자연 지형을 미니어처로 보여주는 장면 / 모델 비교 콘텐츠
- **잘하는 표현**: 빙하 절벽과 떠다니는 빙산 / 투명 젤리 바다의 물결·커스틱 / 물 색상(청록·파랑·보라) 전환 / 블록을 기울일 때 출렁임
- **스타일**: 연회색 종이 스튜디오 위 사각 젤리 블록, 검은 바위산과 흰 빙하, 청록·파랑·보라 투명 바다에 흰 빙산, 빨간 연구기지. 이탤릭 세리프 'Iceberg Jelly.' 타이틀의 깨끗한 머티리얼 스터디 3D.
- **기술**: WebGPU, WGSL, 얕은 물 시뮬레이션, 강체 빙산 부력
- **프롬프트 구조**: THE SCENE·PHYSICS·LIFE 대문자 섹션에 지형·빙산 물리·생물을 지질학 용어까지 촘촘히 적은 시리즈형 스펙
- **태그**: 젤리디오라마, 빙하, 극지, 펭귄, 빙산, WebGPU, material-study, 비교영상
- **주의**: 위(Claude Opus 5.5, 26.42$)·아래(ChatGPT-6 Astra, 30.33$) 분할 비교로 Opus 쪽은 위 패널

#### [Harbor jelly water physics comparison](comparison__harbor-jelly-water-physics-comparison__2109794326574227823.md)
`comparison__harbor-jelly-water-physics-comparison__2109794326574227823` · 약 1:1.27 (720x912) · 17s · 조회 13K · 에셋필요 X

- **요약**: 컨테이너 항구와 북유럽 마을을 젤리 바다 블록에 담아 배가 드나드는 WebGPU 디오라마를 ChatGPT-6 Astra와 Claude Opus 5.5 결과로 번갈아 비교한 영상
- **어울리는 경우**: 물류·무역·항만 설명 인서트 / 도시·마을을 미니어처로 보여주는 장면 / 모델 비교 콘텐츠
- **잘하는 표현**: 알록달록한 컨테이너 더미와 크레인 / 투명 젤리 바다의 물결·항적 / 빨강·흰 등대와 방파제 / 물 색상(청록·파랑·초록) 전환
- **스타일**: 따뜻한 연회색 배경 위 사각 젤리 블록, 파랑·청록·초록 투명 물과 색색 컨테이너, 북유럽 파스텔 집들과 등대. 이탤릭 세리프 'Harbor Jelly.' 타이틀의 밝은 미니어처 3D.
- **기술**: WebGPU, WGSL, 얕은 물 시뮬레이션, 단일 HTML
- **프롬프트 구조**: 시리즈 룩 규칙(배경·타이틀·패널 문구) → THE BLOCK → THE HARBOR 배치 → THE SHIP'S DAY 순환 순서로 적은 대문자 섹션형 스펙
- **태그**: 젤리디오라마, 항구, 컨테이너, 등대, 물시뮬, WebGPU, material-study, 비교영상
- **주의**: 위(ChatGPT-6 Astra, 20.36$)·아래(Claude Opus 5.5, 16.4$) 분할 비교로 Opus 쪽은 아래 패널

#### [Tidepool Jelly 3D coastal ecosystem comparison](comparison__tidepool-jelly-3d-coastal-ecosystem-comparison__2109015574177075610.md)
`comparison__tidepool-jelly-3d-coastal-ecosystem-comparison__2109015574177075610` · 4:5 · 18s · 조회 13K · 에셋필요 X

- **요약**: 해안 단면 미니어처 안 조수 웅덩이에 젤리 바다생물이 사는 Three.js 생태계를 Claude Opus 5.5와 ChatGPT-6 Astra 결과로 번갈아 비교한 영상
- **어울리는 경우**: 해양·생태계 교육 인서트 / 조수·물 순환 설명 / 생물을 클릭해 카드로 소개하는 장면 / 모델 비교 콘텐츠
- **잘하는 표현**: 해안 단면 블록과 지층 / 웅덩이 물의 커스틱·반사 클로즈업 / 젤리 같은 게·불가사리·말미잘 / 낮·밤(남색 배경) 전환
- **스타일**: 오프화이트 배경 위 모래·바위·잔디가 덮인 해안 단면 블록, 청록 투명 물과 파스텔 생물들. 밤 모드는 남회색 배경. 이탤릭 세리프 'Tidepool Jelly.' 타이틀의 부드럽고 촉촉한 미니어처 3D.
- **기술**: Three.js, 커스텀 셰이더, 직교 카메라
- **프롬프트 구조**: 장면 → 물(주인공) → 생물 행동 → 인터랙션 → 컨트롤 목록 → 타이포·레이아웃 순으로 쓴 서술형 요구 문단
- **태그**: 조수웅덩이, 해안, 젤리, 바다생물, 단면, Three.js, 에디토리얼, 비교영상
- **주의**: 위(Claude Opus 5.5, 29.08$)·아래(ChatGPT-6 Astra, 17.86$) 분할 비교로 Opus 쪽은 위 패널

#### [Geyser Jelly volcanic island diorama comparison](comparison__geyser-jelly-volcanic-island-diorama-comparison__2112554053175554078.md)
`comparison__geyser-jelly-volcanic-island-diorama-comparison__2112554053175554078` · 약 1:1.27 (720x912) · 18s · 조회 12K · 에셋필요 X

- **요약**: 화산·간헐천·온천·잔디집이 있는 아이슬란드풍 섬을 젤리 바다 블록에 담아 간헐천이 주기적으로 분출하는 WebGPU 디오라마를 Claude Opus 5.5와 ChatGPT-6 Astra 결과로 번갈아 비교한 영상
- **어울리는 경우**: 지리·화산 주제 설명 인서트 / 여행지·섬 소개 / 주기적으로 반복되는 현상(분출) 설명 / 모델 비교 콘텐츠
- **잘하는 표현**: 섬을 둘러싼 투명 젤리 바다와 흰 파도 / 화산 연기와 간헐천 물기둥 / 물 색상(청록·빨강·검보라) 전환 / 블록 기울임 출렁임
- **스타일**: 연회색 스튜디오 위 사각 젤리 블록, 초록 섬과 갈색 화산, 청록·빨강·검보라로 바뀌는 투명 바다와 흰 거품. 이탤릭 세리프 'Geyser Jelly.' 타이틀의 밝은 머티리얼 스터디 3D.
- **기술**: WebGPU, WGSL, 얕은 물 시뮬레이션, 단일 HTML
- **프롬프트 구조**: TECH → THE ISLAND(구역별 배치) → THE GEYSER(분출 주기 단계)를 대문자 섹션에 수치까지 적은 시리즈형 스펙
- **태그**: 젤리디오라마, 화산, 간헐천, 아이슬란드, 섬, WebGPU, material-study, 비교영상
- **주의**: 위(Claude Opus 5.5, 24.34$)·아래(ChatGPT-6 Astra, 25.44$) 분할 비교로 Opus 쪽은 위 패널

#### [Interactive 3D rooftop glass pool, two model versions](comparison__interactive-3d-rooftop-glass-pool-two-model-versions__2112978719069598181.md)
`comparison__interactive-3d-rooftop-glass-pool-two-model-versions__2112978719069598181` · 4:5 · 30s · 조회 12K · 에셋필요 X

- **요약**: 고층 빌딩 옥상의 유리벽 수영장에 해적선·플라밍고 튜브·고무오리가 떠 있고 노을에서 밤으로 넘어가는 3D 웹 장면을 Claude Opus 5.5와 Opus 5 결과로 비교한 30초 영상
- **어울리는 경우**: 시간 경과(낮→밤) 연출 / 휴양·여름 분위기 인서트 / 같은 프롬프트의 버전 차이 비교 / 도시 야경 배경
- **잘하는 표현**: 투명 유리벽 너머 수중 단면 / 노을 역광에서 야경으로 바뀌는 조명 / 물에 떠 흔들리는 장난감들 / 줄전구와 수중 조명의 밤 분위기
- **스타일**: Opus 5.5 쪽은 주황·분홍 노을 하늘과 원경 도시, 나무 데크, 청록 수영장 위 분홍 플라밍고·노란 오리가 밤이 되면 파란 수중 조명과 줄전구로 바뀌는 따뜻한 3D. 사실적이되 약간 장난감 같은 렌더.
- **프롬프트 구조**: 장면 핵심(옥상 유리 수영장) → 떠 있는 소품 목록 → 30초 시간 변화를 3문장으로 쓴 짧은 개념형 프롬프트
- **태그**: 수영장, 옥상, 노을, 야경, 시간경과, 3D웹, 유리, 버전비교
- **주의**: 위(Claude Opus 5.5 High, 68분 ~$14.39)·아래(Claude Opus 5 High, 128분 ~$68.42) 분할 비교로 Opus 5.5 쪽은 위 패널. 작성자 워터마크 있음. 사용 도구는 메타에 적혀 있지 않음

#### [3D jet engine model comparison](comparison__3d-jet-engine-model-comparison__2112897791022264814.md)
`comparison__3d-jet-engine-model-comparison__2112897791022264814` · 약 1:1.69 (720x1216) · 29s · 조회 12K · 에셋필요 X

- **요약**: 단면·엑스레이·분해 모드로 내부를 보여주는 3D 제트엔진 시각화를 DeepSeek V4.1 Flash·Opus 5.5·GPT-6.1 Sol 세 모델 결과로 위아래 3단 비교한 영상
- **어울리는 경우**: 기계·엔지니어링 구조 설명 / 제품 내부를 열어 보여주는 테크 쇼케이스 / 작동 순서(시동→점화) 설명 인서트 / 모델 비교 콘텐츠
- **잘하는 표현**: 외피가 열리며 드러나는 컷어웨이 단면 / 엑스레이 홀로그램 모드 / 점화된 코어의 주황 발광과 배기 흐름 / 부품 라벨 콜아웃
- **스타일**: Opus 쪽은 검은 배경에 흰 나셀·주황 포인트의 'KX-9' 엔진, 강한 렌즈 플레어와 주황·보라 배기 글로, 청색 엑스레이 링. 다크 프리미엄 테크 쇼케이스 감성의 3D.
- **기술**: Three.js, 단일 HTML
- **프롬프트 구조**: 목표·첫인상 강조 → 필수 조건 → 엔진 구성품 → 모드·인터랙션 → 애니메이션 → 시각 품질을 항목 나열로 적은 체크리스트형 프롬프트
- **태그**: 제트엔진, 컷어웨이, 엑스레이, 분해도, Three.js, 다크테크, 엔지니어링, 3단비교
- **주의**: 위(DeepSeek 4.1 flash 1017)·가운데(Opus 5.5)·아래(Sol 6.1) 3단 분할 비교로 Opus 쪽은 가운데 패널

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

#### [Blender campfire scene: Opus vs GPT-6](comparison__blender-campfire-scene-opus-vs-gpt-6__2111633479599272435.md)
`comparison__blender-campfire-scene-opus-vs-gpt-6__2111633479599272435` · 16:9 · 20s · 조회 11K · 에셋필요 X

- **요약**: 외부 에셋 없이 Blender에서 코드로 만든 밤 숲속 모닥불(불꽃·불티·연기·반딧불) 루프를 Claude Opus 5.5와 GPT-6 Astra 결과로 좌우 비교한 영상
- **어울리는 경우**: 차분한 마무리·휴식 구간의 배경 루프 / 이야기·회고 파트의 분위기 컷 / '불씨·시작' 같은 은유 장면 / 3D 툴 결과 비교 콘텐츠
- **잘하는 표현**: 절차적 불꽃·불티 파티클 / 피어오르는 연기 볼륨 / 따뜻한 불빛과 차가운 달밤의 대비 조명 / 끊김 없는 루프
- **스타일**: 짙은 남색 밤하늘과 별·달, 어두운 침엽수 실루엣 아래 주황빛 모닥불이 유일한 광원. 저채도 시네마틱 실사풍 3D이고 Opus 쪽은 통나무 더미와 작은 랜턴·버섯 소품, 더 어둡고 연기가 짙다.
- **기술**: Blender (Python 스크립트로 절차적 생성·애니메이션)
- **프롬프트 구조**: 외부 에셋 금지와 넣을 요소(불꽃·불티·연기·반딧불·루프)만 적은 두 문장짜리 짧은 지시
- **태그**: 모닥불, campfire, Blender, 파티클, 밤, 시네마틱, 루프, 비교영상, 3D
- **주의**: 좌 Claude Opus 5.5 / 우 GPT-6 Astra 분할 비교이고 상단 모델명 라벨과 작성자 워터마크가 있음. 왼쪽 패널만 참고

#### [Jelly kingdom scene: Opus vs GPT-6 Astra](comparison__jelly-kingdom-scene-opus-vs-gpt-6-astra__2108649845405929924.md)
`comparison__jelly-kingdom-scene-opus-vs-gpt-6-astra__2108649845405929924` · 4:5 · 18s · 조회 11K · 에셋필요 X

- **요약**: 젤리 호수 블록 위 동화 성·폭포·범선 디오라마 'Castle Jelly'를 WebGPU로 만든 결과를 Claude Opus 5.5와 ChatGPT-6 Astra로 번갈아 비교한 영상
- **어울리는 경우**: 세계관·장소를 미니어처로 소개하는 오프닝 / 단면(지층)으로 구조를 보여주는 설명 컷 / 동화·키즈 톤 브랜드 티저 / 모델 비교 콘텐츠
- **잘하는 표현**: 반투명 젤리 물 블록과 캔디 줄무늬 단면 / 폭포·물결 얕은물 시뮬 / 블록 기울이기 출렁임 / 물 색상 프리셋(블루·핑크·라일락) 전환
- **스타일**: 따뜻한 오프화이트 종이 스튜디오 배경에 하늘색·핑크·보라 반투명 젤리 블록, 크림색 성과 파스텔 원뿔 지붕. 좌상단 이탤릭 세리프 'Castle Jelly.' 타이틀과 우측 글래스 패널의 에디토리얼 머티리얼 스터디 3D.
- **기술**: WebGPU, WGSL, SDF·surface nets 메싱, 얕은물 시뮬, 단일 HTML 파일
- **프롬프트 구조**: 시리즈 스타일 지정 → 디오라마 요소 나열 → 인터랙션·슬라이더·플레이버 목록을 한 문단씩 빽빽하게 서술
- **태그**: 젤리, 디오라마, 성, 폭포, WebGPU, material-study, 에디토리얼, 파스텔, 비교영상
- **주의**: 상단에 모델명과 비용(Opus 13.30$ / Astra 12.62$) 라벨이 붙은 교차 편집 비교. 'Claude Opus 5.5' 라벨 구간만 참고하고, 실제 화면은 인터랙티브 페이지 녹화

#### [Plush pigeon soft-body squish toy](comparison__plush-pigeon-soft-body-squish-toy__2111106285126971770.md)
`comparison__plush-pigeon-soft-body-squish-toy__2111106285126971770` · 4:5 · 18s · 조회 11K · 에셋필요 X

- **요약**: 털 셰이더와 XPBD 소프트바디로 만든 통통한 봉제 비둘기 장난감 'Plush Pigeon'이 걷고 구구 울고 넘어지는 WebGPU 데모를 Opus 5.5와 ChatGPT-6 Astra로 비교한 영상
- **어울리는 경우**: 귀여운 캐릭터·마스코트 등장 컷 / 굿즈·봉제 인형 제품 티저 / 강의 중 가벼운 리액션·쉬어가기 인서트 / 모델 비교 콘텐츠
- **잘하는 표현**: 셸 퍼(fur) 보송한 털 질감 / 말랑한 몸통 소프트바디 변형 / 뒤뚱 걸음·넘어졌다 일어나기 같은 캐릭터 동작 / 팔레트(블루바·애시레드·스노) 전환
- **스타일**: 밝은 웜그레이 무지 스튜디오 바닥에 회백색 털뭉치 비둘기, 청록 머리와 보라 목띠·분홍 발. 좌상단 이탤릭 세리프 'Plush Pigeon.' 타이틀과 우측 얇은 컨트롤 패널의 미니멀 제품 사진풍 3D.
- **기술**: WebGPU, XPBD 소프트바디, 셸 퍼, SDF
- **프롬프트 구조**: 기존 엔진 재사용 선언 → 외형(형태·목띠·얼굴·날개·털 길이) → 동작(Strut·Coo·Flap·Topple·Finger) → 팔레트·리드아웃 순의 불릿 스펙
- **태그**: 봉제인형, plush, 비둘기, 털, soft-body, WebGPU, material-study, 캐릭터, 비교영상
- **주의**: 상단에 모델명·비용 라벨(Opus 10.17$ / Astra 17.83$)이 붙은 교차 편집. Opus 쪽은 더 동그랗고 털이 풍성한 쪽이며 'Claude Opus 5.5' 라벨 구간만 참고

#### [WWII mountain fortress in a blizzard, Blender scene](comparison__wwii-mountain-fortress-in-a-blizzard-blender-scene__2113119946599272680.md)
`comparison__wwii-mountain-fortress-in-a-blizzard-blender-scene__2113119946599272680` · 16:9 · 46s · 조회 11K · 에셋필요 X

- **요약**: 눈보라 치는 알프스 봉우리의 2차대전풍 산성 요새(탐조등·케이블카·증기기관차·대공포·오로라)를 Blender로 만든 시네마틱 애니메이션을 Claude Fable 5.1과 Opus 5.5로 좌우 비교한 영상
- **어울리는 경우**: 역사·전쟁사 강의의 장소 도입 컷 / 웅장한 오프닝·챕터 전환 / '요새·방어' 은유(보안 등) 시각화 / 3D 툴 결과 비교 콘텐츠
- **잘하는 표현**: 눈 덮인 산악 지형과 성채 모델링 / 탐조등 볼륨 빔과 눈보라 파티클 / 드론식 항공 촬영에서 케이블카·기차 클로즈업으로 이어지는 카메라 컷 / 폭풍이 걷힌 뒤 오로라 리빌
- **스타일**: 푸른빛 밤 설경에 회색 석조 요새, 창문의 노란 불빛과 흰 탐조등 빔, 마지막에 청록 오로라. 차갑고 장엄한 시네마틱 실사풍 3D.
- **기술**: Blender, Python
- **프롬프트 구조**: 장면 구성 요소 나열 → 시간 순 사건(눈보라·탐조등·케이블카·기차·대공포·오로라) → 깃발·문자 금지와 '공개 비교에 자랑할 만큼 다듬어라'는 품질 지시
- **태그**: 요새, 설산, 눈보라, Blender, 시네마틱, 탐조등, 오로라, 전쟁사, 비교영상
- **주의**: 좌 Claude Fable 5.1 / 우 Claude Opus 5.5 분할 비교이고 상단에 모델명·작업 시간·비용 라벨과 워터마크가 있음. 오른쪽 패널만 참고. 2차대전 소재라 맥락 주의

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

#### [Jelly lego bricks model comparison](comparison__jelly-lego-bricks-model-comparison__2110484619841958316.md)
`comparison__jelly-lego-bricks-model-comparison__2110484619841958316` · 약 1:1.27 (720x914) · 13s · 조회 10K · 에셋필요 X

- **요약**: 반투명 젤리 블록 장난감 'Jelly Bricks'를 쌓고 흔들고 무너뜨리는 Three.js 데모를 Gemini Argon 4와 Opus 5.5로 위아래 번갈아 비교한 영상
- **어울리는 경우**: '하나씩 쌓아 올린다'·'무너진다' 은유 컷 / 모듈·구성요소 조립 설명 / 키즈·장난감 톤 티저 / 모델 비교 콘텐츠
- **잘하는 표현**: 젤리 블록 착지 스쿼시·흔들림 / 탑이 푸딩처럼 흔들리다 무너지는 물리 / 원색 반투명 캔디 재질과 바닥 컬러 글로우
- **스타일**: 순백 배경에 빨강·주황·노랑·초록·파랑 반투명 젤리 블록, 부드러운 그림자. Opus 쪽은 좌상단 작은 'Jelly Bricks' 라벨과 우측 소형 패널만 있는 아주 미니멀한 3D.
- **기술**: Three.js, MeshPhysicalMaterial(transmission·clearcoat), 버텍스 셰이더 스쿼시, 단일 HTML 파일
- **프롬프트 구조**: LOOK·JELLY BEHAVIOUR·UI 대문자 섹션으로 재질·동작·문구를 불릿으로 나눈 스펙, 시작 상태와 60fps 조건으로 마무리
- **태그**: 젤리, 블록, 쌓기, 붕괴, Three.js, 3D, 장난감, 원색, 비교영상
- **주의**: 상단 모델명·비용 라벨(Gemini $3.45 / Opus $10.71) 교차 편집. 프롬프트의 큰 이탤릭 세리프 타이틀은 Gemini 쪽에만 있고 Opus 쪽은 작은 라벨뿐(프롬프트≠결과). 레고 연상 형태라 브랜드 노출 주의

#### [Pixel-art table tennis courtyard diorama](comparison__pixel-art-table-tennis-courtyard-diorama__2114842660829860045.md)
`comparison__pixel-art-table-tennis-courtyard-diorama__2114842660829860045` · 약 1:1.29 (720x930) · 17s · 조회 10K · 에셋필요 X

- **요약**: 떠 있는 섬 위 파스텔 아파트 단지 마당에서 이웃들이 탁구를 치는 아이소메트릭 디오라마 'King of the Table'을 Opus 5.5와 GPT-6.1 Terra로 비교한 영상
- **어울리는 경우**: 동네·생활 공간을 소개하는 장소 컷 / 시뮬레이션·에이전트(사람들이 각자 움직임) 개념 설명 / 낮→밤 시간 흐름 표현 / 모델 비교 콘텐츠
- **잘하는 표현**: 아이소메트릭 떠 있는 섬 디오라마 / 낮·노을·밤 조명 전환과 창문 불빛 / 작은 사람·아이·비둘기 군중 생활 묘사
- **스타일**: 밝은 회백 배경에 연노랑·분홍·하늘색 패널 아파트, 초록 잔디와 회색 보도블록, 섬 아래 흙 단면. 굵은 산세리프 대문자 'KING OF THE TABLE' 타이틀과 우측 컨트롤 레일의 플랫 셰이딩 로우폴리 3D.
- **기술**: Three.js r160, 저해상도 렌더 타깃, OKLab 64색 팔레트 양자화, 깊이 외곽선, A* 경로
- **프롬프트 구조**: 렌더링 방식 → 세계 구성 → 공 물리 → 게임 규칙·AI → 마당 생활 → UI를 한 문단씩 밀도 높게 나열한 대형 스펙
- **태그**: 디오라마, isometric, 아파트단지, 탁구, 픽셀아트, Three.js, 시뮬레이션, 낮밤전환, 비교영상
- **주의**: 상단 모델명·비용 라벨(Opus 14.17$ / Terra 1.23$) 교차 편집. 프롬프트는 픽셀아트지만 영상 해상도에서는 픽셀감이 약하고 깔끔한 로우폴리처럼 보임. 인터랙티브 페이지 화면 녹화

#### [Low-poly 3D horse animation comparison](comparison__low-poly-3d-horse-animation-comparison__2112103012638277944.md)
`comparison__low-poly-3d-horse-animation-comparison__2112103012638277944` · 약 1:1.13 (720x816) · 18s · 조회 10K · 에셋필요 X

- **요약**: 기본 도형으로 절차적으로 만든 로우폴리 말이 달리는 Three.js 루프를 Claude Opus 5.5와 DeepSeek V4.1로 위아래 번갈아 비교한 영상
- **어울리는 경우**: '질주·속도·전진' 은유 컷 / 동물 보행 사이클 같은 애니메이션 원리 설명 / 목가적 배경 루프 / 모델 비교 콘텐츠
- **잘하는 표현**: 절차적 다리·몸통·머리·꼬리 갤럽 사이클 / 흙먼지 날리는 달리기 / 스크롤되는 로우폴리 풍경과 울타리
- **스타일**: Opus 쪽은 초록 언덕 목장과 갈색 나무 울타리, 흰 로우폴리 말에 우측 반투명 다크 컨트롤 패널이 큼지막하게 겹친 밝은 대낮 로우폴리 3D. DeepSeek 쪽은 노을 사바나에 갈색 말과 'The Gallop' 세리프 타이틀.
- **기술**: Three.js, ES 모듈 멀티파일 구조
- **프롬프트 구조**: 무엇을 만들지 한 문장 → 파일 구조·실행 조건 → '다른 모델과 비교 평가되니 공들여라'는 짧은 지시
- **태그**: 말, horse, 로우폴리, low-poly, 달리기, 루프, Three.js, 3D, 비교영상
- **주의**: 화면 우상단에 손글씨풍 모델명 라벨('Claude Opus 5.5' / 'DeepSeek V4.1 1017')이 박힌 교차 편집. Opus 쪽은 컨트롤 패널이 화면 오른쪽을 크게 가림

#### [Harbor Jelly interactive diorama comparison](comparison__harbor-jelly-interactive-diorama-comparison__2112476644757639411.md)
`comparison__harbor-jelly-interactive-diorama-comparison__2112476644757639411` · 약 1:1.27 (720x912) · 18s · 조회 10K · 에셋필요 X

- **요약**: 젤리 바다 블록 안에 컨테이너 항구·크레인·등대·배를 넣은 WebGPU 디오라마 'Harbor Jelly'를 Gemini 4 Argon과 Opus 5.5로 위아래 번갈아 비교한 영상
- **어울리는 경우**: 물류·무역·공급망 강의의 개념 컷 / 항구 도시·지역 소개 / 단면으로 물속 구조를 보여주는 설명 / 모델 비교 콘텐츠
- **잘하는 표현**: 굴절·흡수·커스틱이 있는 반투명 젤리 물 / 컨테이너·크레인이 빽빽한 디테일 항구 / 물결·항적 얕은물 시뮬과 블록 기울이기 / 물 색 프리셋(청록·파랑·초록) 전환
- **스타일**: 웜 페이퍼 배경에 청록·코발트 블루·라임 반투명 물 블록, 형형색색 컨테이너와 빨간 크레인, 빨간 줄무늬 등대. Opus 쪽은 카메라가 물 위로 가까이 들어가는 클로즈업이 많고 이탤릭 세리프 'Harbor Jelly.' 타이틀의 에디토리얼 머티리얼 스터디 3D.
- **기술**: WebGPU, WGSL, 얕은물 시뮬(staggered grid), 라이브러리 없는 단일 HTML 파일
- **프롬프트 구조**: 시리즈 룩 지정 → THE BLOCK·THE HARBOR 등 대문자 섹션으로 물리·렌더링·배치를 상세 기술한 대형 스펙
- **태그**: 젤리, 항구, 컨테이너, 디오라마, WebGPU, 물시뮬, material-study, 에디토리얼, 비교영상
- **주의**: 상단 모델명·비용 라벨(Gemini 0.46$ / Opus 16.4$) 교차 편집. 'Claude Opus 5.5' 라벨 구간만 참고

#### [3D pixel-art streetball court comparison](comparison__3d-pixel-art-streetball-court-comparison__2115106186831823065.md)
`comparison__3d-pixel-art-streetball-court-comparison__2115106186831823065` · 4:5 · 17s · 조회 10K · 에셋필요 X

- **요약**: 벽돌 아파트 마당의 3대3 길거리 농구장 아이소메트릭 디오라마 'Courtyard Hoop'을 Opus 5.5와 GPT-6.1 Sol로 비교한 영상
- **어울리는 경우**: 팀워크·경쟁 은유 컷 / 동네 스포츠·생활 공간 소개 / 비 온 뒤·밤 등 날씨·시간 변화 표현 / 모델 비교 콘텐츠
- **잘하는 표현**: 아이소메트릭 떠 있는 섬 디오라마 / 파랑·주황 코트와 비 온 뒤 물웅덩이 반사 / 낮·밤 조명과 불 켜진 창문 / 작은 선수·주민 군중 움직임
- **스타일**: 크림 배경에 붉은 벽돌 아파트, 파란 코트와 주황 키 존, 초록 펜스와 미루나무, 섬 아래 흙 단면. 굵은 산세리프 대문자 'COURTYARD HOOP' 타이틀과 우측 레일의 플랫 로우폴리 3D.
- **기술**: Three.js(WebGL), 저해상도 정사영 렌더, OKLab 64색 팔레트, 깊이 외곽선
- **프롬프트 구조**: 장소 묘사 → 주변 소품 → 렌더링 → 공 물리 → AI → 규칙 → 마당 생활 → UI를 한 문단씩 나열한 대형 스펙
- **태그**: 디오라마, isometric, 농구, 아파트마당, 픽셀아트, Three.js, 날씨, 낮밤전환, 비교영상
- **주의**: 상단 모델명·비용 라벨(Opus 10.44$ / Sol 5.33$) 교차 편집. 프롬프트는 픽셀아트지만 영상에서는 로우폴리에 가깝게 보임. 인터랙티브 화면 녹화

#### [Japanese shrine scene comparison](comparison__japanese-shrine-scene-comparison__2110014604524896392.md)
`comparison__japanese-shrine-scene-comparison__2110014604524896392` · 약 1:1.27 (720x912) · 17s · 조회 10K · 에셋필요 X

- **요약**: 이쓰쿠시마풍 바다 위 도리이와 신사·오층탑 섬을 둥근 물 블록 안에 넣은 Three.js 디오라마 'Torii at High Tide'를 Opus 5.5와 ChatGPT-6 Astra로 비교한 영상
- **어울리는 경우**: 일본 문화·여행 강의의 장소 컷 / 계절·조수 변화 같은 순환 개념 설명 / 동양풍 브랜드 티저 / 모델 비교 콘텐츠
- **잘하는 표현**: 둥근 모서리 물 블록과 굴절·커스틱 / 주홍 도리이·신사 건축 절차적 모델링 / 물 색상·계절 프리셋 전환 / 카메라가 다가가는 인트로
- **스타일**: 따뜻한 와시 종이 배경에 짙은 초록 숲 언덕과 주홍 도리이, 청록·코발트·분홍·보라로 바뀌는 물 블록. 좌상단 이탤릭 세리프 'A gate that stands in the sea.' 헤드라인의 에디토리얼 미니어처 3D.
- **기술**: Three.js r160, 커스텀 ShaderMaterial(SSR·Beer–Lambert 흡수), GPU 파동 방정식, InstancedMesh, 단일 HTML 파일
- **프롬프트 구조**: CONCEPT·TERRAIN·ARCHITECTURE·VEGETATION·SEASONS·WATER·PARTICLES·KOI·TIME OF DAY·UI 대문자 섹션별로 수치까지 적은 초대형 기술 스펙
- **태그**: 도리이, 신사, 일본, 디오라마, 물, Three.js, 계절, 에디토리얼, 비교영상
- **주의**: 상단 모델명·비용 라벨(Opus 6.2$ / Astra 8.26$) 교차 편집. 프롬프트는 '젤리가 아닌 사실적인 물'을 요구했지만 Opus 쪽 물은 채도 높은 젤리 블록처럼 보임(프롬프트≠결과)

#### [Plush watermelon animation comparison](comparison__plush-watermelon-animation-comparison__2111428909203866089.md)
`comparison__plush-watermelon-animation-comparison__2111428909203866089` · 4:5 · 18s · 조회 9K · 에셋필요 X

- **요약**: 웃는 얼굴과 팔다리가 달린 수박 조각 봉제 인형 'Plush Watermelon'이 걷고 흔들고 넘어지는 WebGPU 소프트바디 데모를 Gemini 4 Argon과 Opus 5.5로 비교한 영상
- **어울리는 경우**: 여름·과일 소재 귀여운 캐릭터 컷 / 굿즈·키즈 제품 티저 / 강의 중 가벼운 리액션 인서트 / 모델 비교 콘텐츠
- **잘하는 표현**: 보송한 털 질감의 봉제 재질 / 손가락으로 누르면 찌그러지는 소프트바디 / 흔들흔들·넘어졌다 일어나는 캐릭터 동작 / 클래식·옐로·소르베 팔레트 전환
- **스타일**: 밝은 웜그레이 스튜디오 바닥에 분홍빛 빨강·노랑 과육, 흰 털 테두리와 초록 껍질, 볼터치 얼굴. 좌상단 이탤릭 세리프 'Plush Watermelon.' 타이틀의 미니멀 제품 사진풍 3D.
- **기술**: WebGPU, XPBD 소프트바디, 셸 퍼, SDF
- **프롬프트 구조**: 엔진 재사용 선언 → 형태(SDF 기하) → 부위별 재질 → 얼굴·팔다리 → 동작 → 팔레트·리드아웃 순의 불릿 스펙
- **태그**: 봉제인형, plush, 수박, 캐릭터, 털, soft-body, WebGPU, material-study, 비교영상
- **주의**: 상단 모델명·비용 라벨(Gemini 0.77$ / Opus 5.05$) 교차 편집. Opus 쪽은 얼굴이 웃는 둥근 쪽이며 손가락 도구가 화면에 등장함

#### [Claude and GPT backyard game comparison](comparison__claude-and-gpt-backyard-game-comparison__2113602050172785117.md)
`comparison__claude-and-gpt-backyard-game-comparison__2113602050172785117` · 4:5 · 18s · 조회 9K · 에셋필요 X

- **요약**: 차고 앞 아스팔트 마당에서 아이들이 분필로 그린 칸에서 공차기 '사각놀이'를 하는 아이소메트릭 디오라마 'Chalk Square'를 Opus 5.5와 GPT-6 Astra로 비교한 영상
- **어울리는 경우**: 규칙·순위 교체(왕 자리) 같은 게임 규칙 설명 / 어린 시절·동네 놀이 회상 컷 / 비·밤 날씨 변화 표현 / 모델 비교 콘텐츠
- **잘하는 표현**: 떠 있는 섬 아이소메트릭 디오라마 / 분필 선이 그려지는 바닥 텍스처 / 비·밤 조명 전환 / 작은 아이들 군중의 놀이 동작
- **스타일**: 연한 회청 배경에 회색 아스팔트 마당, 붉은 벽돌 변전실과 파란 차고 문, 초록 잔디 섬. 굵은 산세리프 대문자 'CHALK SQUARE' 타이틀의 플랫 로우폴리 3D.
- **기술**: Three.js r160, 저해상도 렌더 + texelFetch 업스케일, OKLab 팔레트, Bayer 디더, 깊이 외곽선, 투 본 IK
- **프롬프트 구조**: 렌더링 → 마당 소품 → 분필 데이터 텍스처 → 게임 규칙 → 공·AI → 아이 포즈 → 시간·날씨 → UI를 소제목과 불릿으로 정리한 대형 스펙
- **태그**: 디오라마, isometric, 놀이, 분필, 마당, 픽셀아트, Three.js, 날씨, 비교영상
- **주의**: 상단 모델명·비용 라벨(Opus 10.37$ / Astra 10.75$) 교차 편집. 프롬프트는 픽셀아트지만 영상에서는 로우폴리에 가깝게 보임

#### [Low-poly Japanese railway station diorama](comparison__low-poly-japanese-railway-station-diorama__2111965632338292943.md)
`comparison__low-poly-japanese-railway-station-diorama__2111965632338292943` · 4:5 · 18s · 조회 9K · 에셋필요 X

- **요약**: 벚꽃 핀 일본 시골 간이역 '春風駅' 로우폴리 디오라마(터널·건널목·통근열차·낮밤 전환)를 Gemini 4 Argon과 Opus 5.5로 비교한 영상
- **어울리는 경우**: 일본 여행·문화 강의의 장소 컷 / 봄·새 출발 분위기의 오프닝 / 교통·인프라 구성 설명 / 모델 비교 콘텐츠
- **잘하는 표현**: 툰 셰이딩 로우폴리 디오라마 블록 / 몽글한 분홍 벚꽃과 흩날리는 꽃잎 / 낮→밤 전환과 가로등·창문 불빛 / 천천히 도는 오빗 카메라
- **스타일**: 연하늘→분홍 파스텔 그라데이션 하늘에 연두 잔디 블록, 분홍 벚나무와 청록 지붕 집, 흙 단면. 밤 모드는 남보라 하늘과 별. 밝고 채도 높은 장난감 같은 로우폴리 3D.
- **기술**: Three.js(ES 모듈), MeshToonMaterial, OutlineEffect, 캔버스 텍스처, 클리핑 플레인
- **프롬프트 구조**: 스타일 → 장면 구성 → 애니메이션 → UI → 기술 조건 순으로 불릿을 정리한 중간 길이 스펙
- **태그**: 기차역, 벚꽃, 일본, 디오라마, low-poly, toon, Three.js, 낮밤전환, 비교영상
- **주의**: 상단 모델명·비용 라벨(Gemini 0.33$ / Opus 10.54$) 교차 편집. Opus 쪽은 터널 언덕이 크고 벚꽃이 더 몽글한 쪽

#### [Night shift horror game, two models compared](comparison__night-shift-horror-game-two-models-compared__2111421758691827905.md)
`comparison__night-shift-horror-game-two-models-compared__2111421758691827905` · 16:9 · 144s · 조회 9K · 에셋필요 X

- **요약**: 폐쇄된 90년대 어린이 TV 스튜디오에서 야간 경비로 버티는 브라우저 호러 게임 'Sunny Hollow: After Hours'를 DeepSeek V4.1 Flash와 Opus 5.5로 좌우 비교한 플레이 영상
- **어울리는 경우**: 공포·긴장감 연출 컷 / CCTV·감시 화면 같은 보안 개념 설명 / VHS·CRT 레트로 화면 효과 참고 / 게임 제작 결과 비교 콘텐츠
- **잘하는 표현**: VHS/CRT 후처리(스캔라인·노이즈·초록 틴트) / 감시 카메라 태블릿 UI와 미니맵 / 어두운 복도와 문틈의 빛나는 눈 / 전력 게이지 같은 게임 HUD
- **스타일**: 검은 화면에 초록빛 감도는 저조도 감시카메라 영상, 체커 바닥과 형광등, 녹색 모노 터미널 글자. 어둡고 음침한 저폴리 3D 호러 게임.
- **기술**: Three.js r128, 풀스크린 셰이더 후처리, 캔버스 절차적 텍스처, Web Audio API, 단일 HTML 파일
- **프롬프트 구조**: 컨셉 → 기술 → 후처리 → 코어 루프 수치 → 방·카메라·맵 → 적 캐릭터별 메커니즘을 마크다운 헤더로 나눈 초대형 게임 기획서
- **태그**: 호러, 게임, CCTV, VHS, CRT, 레트로, Three.js, 플레이영상, 비교영상
- **주의**: 좌 DeepSeek V4.1 Flash / 우 Opus 5.5 분할 비교. 편집된 영상이 아닌 2분 넘는 게임 플레이 녹화이고, FNAF 장르를 본뜬 호러라 강의 톤에 맞는지 확인할 것

#### [Pixel-art baseball game comparison](comparison__pixel-art-baseball-game-comparison__2118281844181369210.md)
`comparison__pixel-art-baseball-game-comparison__2118281844181369210` · 4:5 · 17s · 조회 8K · 에셋필요 X

- **요약**: 떠 있는 복셀 섬 위 야구장과 마을을 픽셀아트 3D로 렌더한 야구 경영 게임 'Marigold Park'를 Claude Opus 5.5와 Claude Sonnet 5.5로 비교한 영상
- **어울리는 경우**: 스포츠·데이터 분석 강의 도입 컷 / 경기장·도시를 내려다보는 장소 소개 / 경기 시뮬레이션 개념 설명 / 모델 비교 콘텐츠
- **잘하는 표현**: 복셀 떠 있는 섬과 폭포 / 줄무늬 캐노피 관중석·주차장 등 촘촘한 디테일 / 잔디·클레이 표면 전환과 낮·노을·밤 조명 / 줌인하는 TV 중계 카메라
- **스타일**: 하늘색 배경에 초록 잔디 줄무늬 구장, 파랑·흰 줄무늬 캐노피 관중석, 빨간 클레이 내야, 우측 네이비 다크 사이드 패널. 디더가 보이는 선명한 픽셀아트 복셀 3D.
- **기술**: Three.js r128, 저해상도 렌더, OKLab 90색 팔레트, Bayer 디더, 깊이 외곽선, Web Audio
- **프롬프트 구조**: LOOK·GAME·UI·QUALITY BAR 대문자 섹션에 구장 치수·물리·규칙·단축키·헤드리스 봇 테스트까지 적은 초대형 스펙
- **태그**: 야구, 경기장, 복셀, 픽셀아트, 떠있는섬, Three.js, 스포츠, 게임, 비교영상
- **주의**: 상단 모델명·비용 라벨(Opus 45.44$ / Sonnet 37.64$) 교차 편집. 'Claude Opus 5.5' 라벨 구간만 참고

#### [Marine lagoon browser scene, model comparison](comparison__marine-lagoon-browser-scene-model-comparison__2111888587360792982.md)
`comparison__marine-lagoon-browser-scene-model-comparison__2111888587360792982` · 약 1.58:1 (1136x720) · 16s · 조회 8K · 에셋필요 X

- **요약**: 몰디브풍 산호초 석호를 위에서 내려다보며 상어·고래·범고래·돌고래·거북·만타를 던져 넣는 Three.js 장면 'Reef Lagoon'을 네 모델(Opus 5.5·Gemini 4 Argon·GPT-6.1 Sol·GPT-6 Astra)로 4분할 비교한 영상
- **어울리는 경우**: 바다·해양생물 강의 컷 / 생태계·다양성 개념 설명 / 물결이 번지는 차분한 배경 루프 / 모델 비교 콘텐츠
- **잘하는 표현**: 탑뷰 물결 높이장 시뮬과 커스틱 / 굴절·프레넬 수면 렌더링 / 절차적 해양생물 헤엄 동작 / 던질 때 튀는 물보라·링
- **스타일**: 밝은 청록 얕은 바다와 황토·보라 산호, 어두운 실루엣의 해양생물을 위에서 내려다본 구도. 햇빛 반짝이는 사실적 수면의 탑다운 3D.
- **기술**: Three.js r128, GPU 리플 핑퐁 렌더 타깃, 커스텀 셰이더, InstancedBufferGeometry, 단일 HTML 파일
- **프롬프트 구조**: CAMERA·WATER SIMULATION·RENDERING·CREATURES 대문자 섹션에 수식·패스 순서·종별 형태까지 적은 초대형 그래픽스 스펙
- **태그**: 바다, 석호, 해양생물, 탑뷰, 물시뮬, 커스틱, Three.js, 3D, 비교영상
- **주의**: 2x2 분할 비교(좌상 Opus 5.5 / 우상 Gemini 4 Argon / 좌하 GPT-6.1 Sol / 우하 GPT-6 Astra)라 패널이 작고 상단에 모델명·비용 라벨이 있음. 좌상단 패널만 참고

#### [Pixel art winter hockey scene comparison](comparison__pixel-art-winter-hockey-scene-comparison__2114894485389791613.md)
`comparison__pixel-art-winter-hockey-scene-comparison__2114894485389791613` · 4:5 · 16s · 조회 8K · 에셋필요 X

- **요약**: 얼어붙은 강 위 눈벽 링크에서 마을 사람들이 하키를 하는 겨울 섬 아이소메트릭 디오라마 'Frozen Bend'를 Opus 5.5와 GPT-6.1 Terra로 비교한 영상
- **어울리는 경우**: 겨울·연말 분위기 컷 / 마을·공동체 소개 / 팀 스포츠·협업 은유 / 모델 비교 콘텐츠
- **잘하는 표현**: 눈 덮인 통나무집·전나무의 겨울 디오라마 / 스케이트 자국이 남는 얼음 링크 / 낮·밤 조명과 모닥불·가로등 불빛 / 작은 선수 군중 움직임
- **스타일**: 흰 배경에 눈 덮인 섬, 청회색 얼음 링크와 갈색 통나무집·초록 전나무, 섬 아래 흙과 고드름. 굵은 산세리프 대문자 'FROZEN BEND' 타이틀의 플랫 로우폴리 3D.
- **기술**: Three.js(WebGL), 저해상도 정사영 렌더, OKLab 64색 팔레트, 깊이 외곽선
- **프롬프트 구조**: 장소 → 렌더링 → 경기 규칙·스케이팅 물리 → AI → 등장인물 → 살아 있는 링크 → 마을 생활 → UI를 문단별로 서술한 대형 스펙
- **태그**: 하키, 겨울, 눈, 디오라마, isometric, 픽셀아트, Three.js, 마을, 비교영상
- **주의**: 상단 모델명·비용 라벨(Opus 16.67$ / Terra 2.98$) 교차 편집. 프롬프트는 픽셀아트지만 영상에서는 로우폴리에 가깝게 보임

#### [Rocket-assisted Roadster stunt animation comparison](comparison__rocket-assisted-roadster-stunt-animation-comparison__2113716424887661034.md)
`comparison__rocket-assisted-roadster-stunt-animation-comparison__2113716424887661034` · 16:9 · 16s · 조회 7K · 에셋필요 X

- **요약**: 야간 시험장의 수직 곡면 램프를 타고 올라 로켓 분사로 떠올랐다 착지하는 흰 로드스터 스턴트 시네마틱을 Opus 5.5와 Kimi K3.1 Pro로 좌우(세로 9:16 패널) 비교한 영상
- **어울리는 경우**: '도약·런칭' 은유 컷 / 신제품 공개 같은 과장된 티저 / 세로형 숏폼 인서트 / 모델 비교 콘텐츠
- **잘하는 표현**: 램프 질주→공중 분사→착지로 이어지는 샷 구성 / 분사 연기와 헤드라이트 블룸 / 고도·G값 원형 HUD 게이지
- **스타일**: 검은 배경 야간 시설에 회색 램프와 빨간 트랙 가장자리, 흰 차체와 강한 흰 블룸. Opus 쪽은 어둡고 하이라이트가 번져 형태가 흐릿한 단색조 3D.
- **프롬프트 구조**: 와이드 리빌 → 램프 상승 → 정점 클로즈업·분사 → 착지 → 풀백 순의 샷 리스트와 화질·HUD·길이(16초 9:16) 조건
- **태그**: 자동차, 스턴트, 로켓, 램프, 시네마틱, HUD, 야간, 세로영상, 비교영상
- **주의**: 좌 Opus 5.5 / 우 Kimi K3.1 Pro 분할 비교이고 상단 모델명·비용 라벨이 있음. 실존 차종(Tesla Roadster)을 명시한 프롬프트라 IP 주의. Opus 쪽은 블룸이 과해 차체가 잘 안 읽혀 품질 참고로는 약함

#### [Jelly eyeball model comparison](comparison__jelly-eyeball-model-comparison__2112923979002368406.md)
`comparison__jelly-eyeball-model-comparison__2112923979002368406` · 약 1:1.38 (720x992) · 32s · 조회 7K · 에셋필요 X

- **요약**: 시신경이 달린 젤리 눈알이 커서를 따라보고 늘어나고 굴러가는 Three.js 인터랙티브 장면 'Jelly / Eyeball.'을 MiniMax M3.1 Flash와 Opus 5.5로 위아래 번갈아 비교한 영상
- **어울리는 경우**: '시선·주목·관찰' 은유 컷 / 할로윈·호기심 톤의 가벼운 인서트 / 젤리 재질 제품 티저 / 모델 비교 콘텐츠
- **잘하는 표현**: 늘어나고 찌그러지는 젤리 소프트바디 / 반투명 공막·홍채 PBR 재질 / 로프처럼 끌리는 시신경 / 쏟아지는 젤리 캔디 파티클
- **스타일**: 순백 배경에 연분홍 반투명 눈알과 파랑·보라 홍채, 빨간 시신경, 주황·보라·민트 젤리 호박과 캔디. 좌상단 이탤릭 세리프 'Jelly / Eyeball.' 타이틀의 밝은 제품 렌더풍 3D.
- **기술**: Three.js, MeshPhysicalMaterial(transmission·clearcoat), 버텍스 셰이더 변형, 벌렛 로프, 단일 HTML 파일
- **프롬프트 구조**: Look → 소프트바디 인터랙션 8가지 번호 목록 → 2차 움직임 → UI 문구·가격표 순의 중간 길이 스펙
- **태그**: 젤리, 눈알, eyeball, soft-body, Three.js, 할로윈, 제품렌더, 에디토리얼, 비교영상
- **주의**: 상단 모델명·비용·작업시간 라벨(MiniMax $0.70 / Opus $3.00) 교차 편집. Opus 쪽은 눈알이 크고 흐릿하며 홍채가 옆을 보는 구간이 많음. 눈알 소재라 섬뜩하게 보일 수 있음

#### [Interactive plush penguin model comparison](comparison__interactive-plush-penguin-model-comparison__2109288662319919127.md)
`comparison__interactive-plush-penguin-model-comparison__2109288662319919127` · 4:5 · 18s · 조회 7K · 에셋필요 X

- **요약**: 털 셰이더와 XPBD 소프트바디로 만든 아기 펭귄 봉제 인형 'Plush Penguin'이 뒤뚱 걷고 미끄러지고 넘어지는 WebGPU 데모를 GPT-6 Astra와 Claude Opus 5.5로 비교한 영상
- **어울리는 경우**: 귀여운 캐릭터·마스코트 컷 / 겨울·동물 소재 가벼운 인서트 / '넘어져도 다시 일어난다' 은유 / 모델 비교 콘텐츠
- **잘하는 표현**: 보송한 셸 퍼 털 질감 / 말랑한 몸통 소프트바디와 천 날개 / 뒤뚱 걸음·점프·넘어졌다 일어나기 동작 / 팔레트 전환
- **스타일**: 밝은 웜그레이 무지 스튜디오 바닥에 회색 털 몸통과 검은 머리 아기 펭귄. 좌상단 이탤릭 세리프 'Plush Penguin.' 타이틀과 우측 얇은 표본 패널의 미니멀 제품 사진풍 3D.
- **기술**: WebGPU, XPBD 소프트바디, SDF + surface nets, 셸 퍼(alpha-to-coverage), 파티클 천
- **프롬프트 구조**: 페이지 레이아웃·문구 → 장난감 외형 → 물리·보행 방식 → 행동 목록 → 털·슬라이더·팔레트를 문단별로 서술한 스펙
- **태그**: 봉제인형, plush, 펭귄, 털, soft-body, WebGPU, material-study, 캐릭터, 비교영상
- **주의**: 상단 모델명·비용 라벨(Astra 13.07$ / Opus 11.05$) 교차 편집. Opus 쪽은 회색 털 아기 펭귄, Astra 쪽은 흰 배 청록 펭귄

#### [Jelly kiwi model comparison](comparison__jelly-kiwi-model-comparison__2114441029638410489.md)
`comparison__jelly-kiwi-model-comparison__2114441029638410489` · 약 1.55:1 (1114x720) · 18s · 조회 7K · 에셋필요 X

- **요약**: 잡아 늘리고 비틀 수 있는 젤리 키위 조각 'Kiwi Jelly Wedge' WebGPU 소프트바디 데모를 Opus 5.5·Fable 5.1·Sonnet 5.5·GPT-6.1 Sol 네 모델로 4분할 비교한 영상
- **어울리는 경우**: 과일·식품 소재 제품 티저 / 말랑한 재질 감각 표현 / 모델 비교 콘텐츠
- **잘하는 표현**: 반투명 젤리 과육과 씨앗·방사 결 디테일 / 잡아당기면 늘어나고 튕기는 소프트바디 / 초록·골드·루비 등 품종 색 프리셋 전환
- **스타일**: 밝은 무채색 스튜디오 배경에 초록·노랑·붉은 반투명 키위 조각과 갈색 껍질. 좌상단 이탤릭 세리프 'Kiwi Jelly.' 타이틀의 미니멀 에디토리얼 머티리얼 스터디 3D.
- **기술**: WebGPU, SDF, 라이브러리 없는 단일 HTML 파일
- **프롬프트 구조**: 오브젝트 기하(각도·반지름·두께) → 영역별 재질 → 씨앗 배치를 수치로 적은 상세 스펙
- **태그**: 젤리, 키위, 과일, soft-body, WebGPU, material-study, 에디토리얼, 비교영상
- **주의**: 2x2 분할 비교(좌상 Opus 5.5 / 우상 Fable 5.1 / 좌하 Sonnet 5.5 / 우하 GPT-6.1 Sol)라 패널이 작고 모델명·비용 라벨이 있음. 좌상단 패널만 참고

### extra (awesome-opus5-5-videos 추가분) — 13건

> 두 번째 출처(yihui-dev/awesome-opus5-5-videos)에서 영상까지 받은 것. 요약은 프롬프트와 영상 메타 기준으로 작성. 조회수 자료 없음.

#### [everestchris6-399895](3d__everestchris6-399895__2104965415164399895.md)
`3d__everestchris6-399895__2104965415164399895` · 16:9 · 40s · 조회 - · 에셋필요 -

- **요약**: 광고주 브리프(용도·시청자·CTA·브랜드·사실 파일)를 빈칸으로 받아 GSAP+Three.js로 모션 광고를 만드는 역할형 프롬프트 템플릿
- **어울리는 경우**: 제품·서비스 홍보 영상을 반복 제작 / 사실 파일 기반으로 화면 문구를 통제해야 할 때
- **잘하는 표현**: 역할+브리프 빈칸 구조 / 사실 파일 외 숫자·주장 금지 / 레퍼런스에 견주어 완성 판정
- **스타일**: GSAP 타임라인과 Three.js 3D를 섞은 코드 렌더 광고. 수치는 브리프 파일에서만.
- **태그**: 템플릿, 광고, gsap, three.js
- **주의**: 빈칸을 채워야 쓸 수 있는 템플릿. 영상은 한 사례일 뿐

#### [astrothewizard-618782](explainer__astrothewizard-618782__2103629247751618782.md)
`explainer__astrothewizard-618782__2103629247751618782` · 16:9 · 60s · 조회 - · 에셋필요 -

- **요약**: 광자의 여정을 동화풍으로 풀어낸 60초 설명 영상을 사용자 개입 없이 끝까지 자율 제작
- **어울리는 경우**: 질문 없이 맡기는 장편 설명 영상 / 캐릭터가 있는 과학 설명
- **잘하는 표현**: 자율 제작 지시(결정은 마지막에 보고) / 캐릭터 성격 부여 / 순수 JS 프레임 렌더
- **스타일**: 동화책풍 모션디자인 스튜디오 톤, 의인화한 광자 주인공.
- **태그**: 설명, 스토리북, 자율, canvas
- **주의**: AI 영상 생성기 없이 코드 렌더만

#### [woojinrad-455731](explainer__woojinrad-455731__2106083299462455731.md)
`explainer__woojinrad-455731__2106083299462455731` · 4:5 (1080x1350) · 65s · 조회 - · 에셋필요 -

- **요약**: 기사 하나를 읽고 핵심 3가지를 색연필 동화풍 25초 설명으로 만든다(프롬프트 기준, 실제 영상 65초)
- **어울리는 경우**: 글(기사·문서)을 SNS 세로형 설명 영상으로 바꿀 때
- **잘하는 표현**: 기사에서 뽑은 짧은 캡션 3개 / 원본 캐릭터 1명 / 스토리보드 먼저 확인 후 렌더 / Web Audio 합성 음악
- **스타일**: 색연필 스토리북 질감, 단순한 오리지널 캐릭터.
- **태그**: 설명, 캡션, 세로, canvas
- **주의**: 글 요약 → 장면 → 캡션 흐름이 자막 기반 인서트와 비슷

#### [egeberkina-949521](interactive__egeberkina-949521__2105029713445949521.md)
`interactive__egeberkina-949521__2105029713445949521` · 16:9 · 60s · 조회 - · 에셋필요 -

- **요약**: 지진이 일어나는 과정을 인터랙티브 지각판 샌드박스 시뮬레이션을 탐험하듯 보여 주는 60초 설명 영상
- **어울리는 경우**: 과학 개념을 슬라이드가 아닌 시뮬레이션처럼 보여 줄 때
- **잘하는 표현**: 응력 누적 → 단층 미끄러짐 → 지진계 반응으로 이어지는 인과 연출 / 실시간 시뮬레이션 느낌
- **스타일**: 3D 지각 단면, 응력 구간 발광, 지진계 UI.
- **태그**: 설명, 3D, 시뮬레이션, threejs
- **주의**: 화면 녹화처럼 보이게 만든 시뮬레이션

#### [tarunyadav9761-053244](interactive__tarunyadav9761-053244__2106435688292053244.md)
`interactive__tarunyadav9761-053244__2106435688292053244` · 16:9 · 53s · 조회 - · 에셋필요 -

- **요약**: 실제 앱 스크린샷을 찍어 나레이션·단어별 키네틱 캡션·합성 배경음으로 12장면 프로모를 Remotion에서 렌더
- **어울리는 경우**: 앱 프로모 / 나레이션+단어별 캡션 구조를 보고 싶을 때
- **잘하는 표현**: 대본·시간 맞춘 나레이션 / 단어 단위 키네틱 캡션 / 3D 기울임과 스프링 물리 / 1080p 60fps
- **스타일**: 실제 앱 화면(2x 레티나) 기반 프로모.
- **태그**: 프로모, 캡션, 나레이션, remotion
- **주의**: 프롬프트가 짧고 결과 수준은 영상으로 판단

#### [twoclipping-041659](interactive__twoclipping-041659__2107822293653041659.md)
`interactive__twoclipping-041659__2107822293653041659` · 4:3 (1440x1080) · 20s · 조회 - · 에셋필요 -

- **요약**: 음성 파일과 대본에 맞춰 컷하는 20초 필름: 삶을 요약하는 사물 10~12개와 열화상 실루엣, 마지막에 세 단어 강조
- **어울리는 경우**: 음성이 있는 영상에 컷·강조 단어를 맞출 때 / 입력 질문형 템플릿
- **잘하는 표현**: <inputs> 질문 + <direction> 구조 / 음성에 맞춘 컷 / 필름 그레인과 비네팅 / 강조할 단어 3개
- **스타일**: 종이색 바탕, 검정, 빨강, 노랑, Geist 서체, 쉬지 않는 핸드헬드 카메라.
- **태그**: 음성 동기, 템플릿, 키네틱, 입력질문
- **주의**: 음성·대본 파일이 있어야 재현 가능

#### [brainextends-606193](motion__brainextends-606193__2103801834930606193.md)
`motion__brainextends-606193__2103801834930606193` · 16:9 · 18s · 조회 - · 에셋필요 -

- **요약**: Spotify 테마의 완성형 18초 모션그래픽: 거의 검은 둥근 사각 스테이지 안에서 진행, 음악과 효과음 포함
- **어울리는 경우**: 음악 제품·앱 소개 모션 / 납품물과 연출 지시가 구체적인 완성형 프롬프트 예시
- **잘하는 표현**: 납품물 명세(해상도·fps·소스·반복 개선) / 아트 디렉션 수치 지정 / 스토리보드로 끝내지 말라는 지시
- **스타일**: 검정 라운드 스테이지가 캔버스의 약 80%x75%, 프리미엄 음악 제품 필름 톤.
- **태그**: 제품, 모션, 60fps, 사운드
- **주의**: 프롬프트 8천 자, 구조 참고용

#### [gdgtify-929495](motion__gdgtify-929495__2103458245213929495.md)
`motion__gdgtify-929495__2103458245213929495` · 1:1 (1080x1080) · 20s · 조회 - · 에셋필요 -

- **요약**: “BUILD THE FLOOR” 연설을 타이포만으로 연출한 20초 키네틱 필름, 마지막 선언이 앞 단어들이 쌓은 구조 위에 선다
- **어울리는 경우**: 짧은 대사·연설을 타이포 영상으로 만들 때 / 단일 HTML 키네틱 타이포
- **잘하는 표현**: 줄마다 프레임 구조가 바뀜 / 서체 역할 분리(연설용 세리프, 하중 단어용 그로테스크) / 정확한 색 지정
- **스타일**: 진초록 배경, 종이색, 호박색 포인트, 에디토리얼 기념비 톤. 오디오 없음.
- **태그**: 키네틱, 타이포, 정사각, svg
- **주의**: HTML 한 파일, 1080x1080 60fps 목표

#### [heyiamnick-119558](motion__heyiamnick-119558__2109174851412119558.md)
`motion__heyiamnick-119558__2109174851412119558` · 16:9 · 30s · 조회 - · 에셋필요 -

- **요약**: 연필선 하나가 흑연→청사진→빛으로 세 번 승격되며 화면을 떠나지 않는 30초 루프 쇼릴
- **어울리는 경우**: 컷 없이 변형으로만 이어지는 쇼릴 / 루프 영상
- **잘하는 표현**: 컷·페이드 없이 앞 장면이 다음 장면의 재료가 됨 / 단계별 포인트 색 계승 / Geist 서체 규칙
- **스타일**: 종이 크림, 청사진 파랑, 홀로그램 시안 팔레트.
- **태그**: 쇼릴, 루프, 변형, canvas
- **주의**: 한 줄 콘셉트로 구조를 잡는 방식이 재사용 가치 높음

#### [jake11moran-414633](motion__jake11moran-414633__2103237884564414633.md)
`motion__jake11moran-414633__2103237884564414633` · 16:9 · 27s · 조회 - · 에셋필요 -

- **요약**: Mac 데스크톱 위를 하나의 카메라가 이어서 지나가는 27초 제품 티저, 컷 없이 느린 푸시·팬
- **어울리는 경우**: 제품 UI 티저 / 화면 녹화풍 연속 카메라
- **잘하는 표현**: 1.5~3초 이징 카메라 무브 / 모션 블러와 필름 그레인 / 큰 macOS 커서 / 소문자 문구 단어별 등장
- **스타일**: HyperFrames로 제작, 오렌지 와이프 포인트, 오디오 없음.
- **태그**: 제품, 카메라, hyperframes, UI
- **주의**: 게시물의 UI·문구를 맞추라는 지시라 원문 영상 의존

#### [notdwd-766641](motion__notdwd-766641__2105031774904766641.md)
`motion__notdwd-766641__2105031774904766641` · 16:9 · 12s · 조회 - · 에셋필요 -

- **요약**: 프롬프트 입력창에 타이핑 → 12프레임 필름스트립이 박자에 찍히고 오렌지 공 바운스 플립북이 재생되는 12초 영상
- **어울리는 경우**: seek(t) 단일 HTML 모션 템플릿의 최소 예시 / 타이핑과 박자 연출
- **잘하는 표현**: seek(t) 한 함수 + Playwright + ffmpeg 렌더 / 키스트로크 리듬 / 120BPM에 맞춘 컷 / 합성 사운드
- **스타일**: 밝은 종이 배경, 어두운 알약 입력창, 오렌지 포인트.
- **태그**: seek, 타이핑, 박자, 프레임렌더
- **주의**: 우리 파이프라인과 구조가 같아 먼저 볼 것

#### [notdwd-998633](motion__notdwd-998633__2103995183255998633.md)
`motion__notdwd-998633__2103995183255998633` · 16:9 · 55s · 조회 - · 에셋필요 -

- **요약**: 브랜드의 5년 뒤 한 줄과 새로 만든 단어 하나를 가르치는 55초 브랜드 필름, 실제 아카이브 영상과 웹 페이지 사용
- **어울리는 경우**: 실제 소스와 나레이션을 섞은 브랜드 필름 / 입력 질문형 템플릿
- **잘하는 표현**: <inputs> 질문(로고·아카이브 클립·웹 페이지·곡·나레이터) / 기능 대신 감정 하나 / 스톡 영상 금지 / 캡션
- **스타일**: 공개 아카이브 영상과 웹 캡처, 100~120BPM 곡의 드롭에 맞춘 구성.
- **태그**: 브랜드, 아카이브, 나레이션, 캡션
- **주의**: 외부 소스(클립·곡·ElevenLabs 키)가 필요

#### [sab8a-475686](motion__sab8a-475686__2103144778481475686.md)
`motion__sab8a-475686__2103144778481475686` · 16:9 · 37s · 조회 - · 에셋필요 -

- **요약**: 원본 토킹헤드 클립을 자막·그래픽·음악이 들어간 경쾌한 편집으로 바꾼 37초 영상
- **어울리는 경우**: 토킹헤드에 자막과 그래픽을 입히는 편집 / 이 프로젝트와 가장 가까운 사례
- **잘하는 표현**: 자막+그래픽+음악 한 번에 / 원본 영상을 그대로 소스로 사용
- **스타일**: 빠른 컷의 펀치 있는 편집, 이미지 생성 소스 혼합.
- **태그**: 토킹헤드, 자막, 편집, ai-image
- **주의**: 프롬프트는 한 줄. 영상으로 룩을 판단할 것
