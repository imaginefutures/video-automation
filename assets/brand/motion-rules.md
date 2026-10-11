# Motion-graphic rules for 베싸TV inserts

These rules are injected into every motion-graphic request (`scripts/inserts.py`). Each rule says why — models follow
rules with a reason more reliably. Sources: docs/인서트-가이드.md, external research notes (HyperFrames design guide,
Anthropic prompting guide, creator feedback logs), 2026-10-12.

## Tokens (use these exact numbers)

| token | value | use |
|---|---|---|
| background | #FAF9F5 warm cream | every frame - the channel's paper. Not pure white |
| main | #4A1B6C deep violet | the ONE focal element, headings |
| soft | #EFE9F3, #CBBAD8 | secondary shapes, panels, inactive states |
| accent | #FFC800 gold | at most 1-2 tiny points (a dot, an underline) - it is a highlighter, not a fill |
| ink | #141413 | body text, thin lines |
| font | "Pretendard" 800 headings / 700 labels | the only font. Injected locally |
| heading size | 64-96px | lecture video is watched on phones too - web sizes (16-24px) are unreadable |
| label size | 36-48px, never below 36px | same reason |

Why fixed tokens: every insert must look like the same channel. Colors outside this set read as stock or "AI-made".

## Composition

- ONE focal point per moment. If two things compete, the viewer reads neither. Secondary elements are soft violet or ink at reduced weight.
- Text budget: at most ~20 Korean characters per text block, at most 2 blocks on screen at once (caption lines given by the editor excepted). The narrator is already speaking - the screen shows, it does not transcribe.
- Bottom 15% stays empty: burned-in subtitles live there.
- Background is never an empty slide: give it quiet depth (a very soft violet shape, a faint paper grain, a soft vignette at 3-5% opacity). Empty cream reads as a placeholder.
- Leave 8% margin on every side. Nothing touches the frame edge unless it is deliberately entering.
- People are flat silhouettes or simple shapes, never realistic faces - the channel does not depict real children or parents.

## Motion

- The test: muted and without subtitles, a viewer must still get the point. Motion must explain (change, sequence, cause, comparison), not decorate.
- seek(0) is already a composed, readable frame - the clip may be cut in at any point and the first frame is the thumbnail of the moment.
- Vary easing: entrances easeOutCubic/easeOutQuart, exits easeInCubic, emphasis a critically damped spring. Using one curve for every tween looks mechanical.
- Vary entry directions and stagger 60-120ms between related elements. Everything sliding up from the bottom at once is the most common "AI template" look.
- Give each beat a hold: after something arrives, let it rest at least 0.8s before the next change. Constant motion is tiring in a lecture.
- Something still moves gently at all times (a slow drift, a breathing scale of 1-2%) so the frame never freezes - but never flicker: no element may appear/disappear/swap faster than 0.2s, and nothing alternates back and forth between two states.
- Timings are numbers: write durations and delays in seconds in code comments (e.g. `// beat 2: 1.4s-2.6s`), and end all motion by D-0.5s.

## Never (these are the "AI-made" tells)

- Purple-to-blue or rainbow gradients, neon, glow, lens flares, glassmorphism, drop shadows heavier than 8% opacity
- Numbered badges ①②③ in circles, pill-shaped label chips everywhere, a table-of-contents layout with a giant centred title
- Side-by-side "A vs B" split as the default answer to everything - use it only when the passage really compares two things
- Bouncy overshoot, elastic or wobble easing, spinning, 3D card flips
- Emoji, icons from icon fonts, stock-illustration clichés (lightbulbs for ideas, gears for process, puzzle pieces) unless the lecture literally uses them
- Copying the reference's colors, fonts, language or pixels - borrow only its structure, motion and pacing

## Self-check before returning the HTML

Write a short comment block at the top of the HTML: the one point of the clip, the beat timeline in seconds, and the focal element of each beat. If a beat has no clear focal element or more than ~20 characters of new text, simplify it.
