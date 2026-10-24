"""주제별 분할 - 편마다 앞에 붙일 인트로 이미지 후보를 만든다 (docs/백로그/주제별-분할.md "인트로·아웃트로").

1. Claude가 그 편의 제목·대본을 읽고 서로 다른 장면 4개를 구상한다 (영어 이미지 프롬프트)
2. Nano Banana 2(Gemini 이미지)가 4장을 동시에 그린다. 제목 글자도 이미지 안에 그리게 한다 -
   설치된 ffmpeg에 drawtext 필터가 없고(10-08 확인), 글자를 코드로 얹으려면 새 의존성이 필요하다.
   한글이 틀리게 그려질 수 있으니 사용자가 4장 중에서 고를 때 글자도 같이 확인한다
   아웃트로 이미지는 참고로 보내지 않는다 - 인트로는 아웃트로와 무관하게 편 내용으로만 만든다 (10-08 사용자 결정)

후보는 <folder>/work/intros/에 쌓이고, 어느 편 것인지는 intros/candidates.json에 "시작문장-끝문장"
키로 남긴다 (경계를 옮기면 그 편의 후보 목록은 사라지지만, 이미 고른 인트로는 split_decisions.json의
intros 배열에 남는다).

Usage (확인용):
    python scripts/split_intro.py <auto-split/NAME> <편 번호(1부터)>
"""
from __future__ import annotations
import argparse
import base64
import json
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel

import claude_cli
from common import edit_dir, load_env, log_llm_usage, write_json

IMAGE_MODEL = "gemini-3.1-flash-image"   # Nano Banana 2 - 1K 한 장 약 $0.067 (10-08)
PROMPT_MODEL = "claude-opus-5-5"   # 대본을 읽고 핵심을 집어내는 판단 - sonnet은 모호한 상징(톱니·원)으로 흘렀다 (10-08)
N_CANDIDATES = 4
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{IMAGE_MODEL}:generateContent"
FILE_RE = re.compile(r"^[0-9]{8}-[0-9]{6}-[0-9a-f]{6}-[0-9]\.(png|jpg)$")


class Scene(BaseModel):
    idea_ko: str    # 이 그림이 강의의 무엇을 보여주는지 한 줄 - 고르는 화면에 그대로 보인다
    prompt: str


class Concepts(BaseModel):
    title_promise_ko: str   # 제목이 시청자에게 약속하는 것 (예: "위험·원인·문제"인지 "방법·해법"인지) - 장면의 기준
    core_ko: str    # 이 편의 핵심 메시지 한 문장
    scenes: list[Scene]


# ---------------------------------------------------------------- 베싸TV 브랜드 블록 (항상 들어감)
# 출처: ~/Projects/babyscience-landing-web 의 PRODUCT.md, design-system/베싸 컬러 시스템.dc.html,
# guide/작업_프로세스/카피_작성_가이드.md(§5 이미지·§6 톤), 베싸TV 썸네일 3장 (10-08 조사).
# 두 부분으로 나눈다 - 장면 구상(Claude)이 지킬 브랜드 규칙, 그리고 그림(Nano Banana)에 매번 그대로 붙는
# 고정 스타일. 장면 프롬프트는 "무엇을 그리나"만, 스타일·색·글자 배치는 고정 블록이 정한다 - 그래야 편마다
# 같은 시리즈로 보이고 결과가 들쭉날쭉하지 않다.

BRAND_CONTEXT = """About the channel - 베싸TV ("과학과 Fact로 육아하기"):
- Run by 베싸 (박정은), an evidence-based parenting educator who reads research papers and explains them to parents.
  Viewers are thoughtful, self-directed parents who want a principle to return to, not a ready-made answer.
- Brand feeling: calm, warm, trustworthy, editorial, unhurried. The parent should feel relief, trust and competence.
- Never: fear or guilt (crying or distressed children, anxious parents), judging parents or children, clinical/medical
  imagery, authority props (lab coats, diplomas, trophies), hype or "perfect solution" symbols, unrelated stock people."""

BRAND_STYLE = """Fixed style for every 베싸TV title card (follow exactly):
- Medium: clean modern editorial illustration - soft flat shapes, gentle shading, subtle paper texture. Not a photo, not 3D render, not cartoonish.
- Palette: warm cream background (#FAF9F5 to #F5F0E8). Deep violet #4A1B6C is the main accent, with soft violets (#EFE9F3, #CBBAD8).
  Gold #FFC800 only as one or two tiny accent points, never as a large area. Ink #141413 for dark details. No neon, no rainbow, no coral.
- Layout: the title sits in the left ~45% of the frame, vertically centered, left-aligned, at most 2 lines.
  The illustration sits in the right half and never overlaps or crosses the title.
- Title typography: very bold, heavy Korean sans-serif, deep violet-black #2A0F3E on the cream background, high contrast, generous letter spacing.
- People: if a child or parent appears, show them small, from behind, from the side, or as hands only - no detailed realistic faces.
- Mood: calm, bright, uncluttered, lots of breathing room. One clear subject, not a busy collage.
- Calm does not mean positive: if the scene describes a problem, risk or fading effect, draw exactly that state (no smiling success, no trophies, no happy ending)."""


PROMPT_SYSTEM = f"""You design a short title card shown before one episode of a Korean lecture series.
Given the episode title and transcript, write {N_CANDIDATES} image-generation prompts in English.

{BRAND_CONTEXT}

THE TITLE IS THE CONTRACT. The card is seen together with the title, so every picture must make the title's claim visible.
First decide title_promise_ko: what the title promises the viewer, in Korean, one sentence. Is it a risk or warning, a cause
("why does X disappear/fail"), a mistake, a contrast, or a method or solution? Transcripts usually spend their second half on the
solution or the happy ending; do NOT let that pull the pictures away from what the title promises.

Then read the transcript and decide:
- core_ko: the ONE message this episode wants parents to take away, one Korean sentence
- the most concrete, memorable material the lecturer actually uses for it: a specific experiment, a math problem,
  an everyday situation with a child, a before/after contrast

Then write {N_CANDIDATES} scenes. Every scene must depict that core message through concrete material from THIS transcript,
so that someone who watched the episode would say "that's the cups experiment" or "that's the 8+4 problem".
- Prefer literal, recognizable objects and situations from the lecture over abstract symbols.
  Do NOT use vague symbols (gears, circles, cycles, arrows, puzzle pieces, lightbulbs, plain balance scales) unless the lecturer uses them
- At least {N_CANDIDATES - 1} of the {N_CANDIDATES} scenes must show what the title promises. If the title names a risk, a cause of failure or a
  problem, show that problem state itself (overload, a method applied blindly, an effect fading or shrinking, a gap closing, a
  mismatch) and NOT the ideal outcome, a thriving child or a solved problem. At most one scene may show the remedy or resolution
- Test each prompt: if the same picture would fit a title that says the OPPOSITE (e.g. "why early learning is great"), rewrite it
- The brand rule against fear and guilt limits HOW the problem is shown (no crying children, no anxious parents), not WHETHER:
  convey tension through objects, composition and metaphor - a tower of blocks leaning, a bar chart whose early lead shrinks to
  nothing, one shortcut route next to a path that skips what matters - always in a calm tone
- The {N_CANDIDATES} scenes should use DIFFERENT material or a different moment of the episode, not variations of one picture
- For each scene, idea_ko: one short Korean line saying which part of the lecture it shows and how it makes the title's claim visible
- Describe only the subject and composition of the illustration. Do NOT specify art style, colors, fonts or title placement -
  a fixed brand style block is appended to every prompt. The illustration goes in the right half of the frame
- Do NOT write the title text itself in the prompt; it is added separately
- No logos, no other text in the image
- One paragraph per prompt, under 60 words"""


def candidates_path(folder: Path) -> Path:
    return edit_dir(folder) / "intros" / "candidates.json"


def load_candidates(folder: Path) -> dict:
    p = candidates_path(folder)
    return json.loads(p.read_text()) if p.exists() else {}


def range_key(start_sent: int, end_sent: int) -> str:
    return f"{start_sent}-{end_sent}"


def image_file(folder: Path, name: str) -> Path:
    if not FILE_RE.match(name):
        raise ValueError("잘못된 이미지 이름입니다")
    p = edit_dir(folder) / "intros" / name
    if not p.exists():
        raise ValueError("없는 이미지입니다")
    return p


def scene_prompts(folder: Path, title: str, text: str, hint: str = "") -> tuple[str, list[Scene]]:
    resp = claude_cli.parse(
        model=PROMPT_MODEL, max_tokens=3000, system=PROMPT_SYSTEM,
        messages=[{"role": "user", "content": f"제목: {title}\n\n대본:\n{text[:12000]}"
                   + (f"\n\n사용자 추가 지시 (장면 구상에 우선 반영): {hint}" if hint else "")}],
        output_format=Concepts, effort="medium")
    log_llm_usage(folder, "split_intro", PROMPT_MODEL, resp.usage)
    out = resp.parsed_output
    scenes = [sc for sc in out.scenes if sc.prompt.strip()][:N_CANDIDATES]
    if not scenes:
        raise ValueError("장면 구상을 받지 못했습니다 - 다시 시도하세요")
    return out.core_ko.strip(), scenes


def draw(scene: str, title: str) -> tuple[bytes, str]:
    instr = (f"{scene}\n\nRender this Korean title text exactly once, large and bold, clearly legible, without quotation marks: \"{title}\". "
             "Spell every Korean character exactly as given. No other text anywhere in the image (no labels, signs, or writing on objects), no watermark, no logo."
             f"\n\n{BRAND_STYLE}")
    return _post_image([{"text": instr}])


def redraw(ref: bytes, ref_ext: str, instruction: str) -> tuple[bytes, str]:
    """고른 그림 한 장을 레퍼런스로 보내 지시한 부분만 고친 변형을 받는다 (Gemini 이미지 편집)."""
    instr = ("Edit the attached image. Change only this, keep everything else exactly the same - the layout, style, colors, "
             f"and the Korean title text spelled exactly as it is now: {instruction}. "
             "Do not add any other text, label, watermark or logo.")
    mime = "image/jpeg" if ref_ext == "jpg" else "image/png"
    return _post_image([{"inline_data": {"mime_type": mime, "data": base64.b64encode(ref).decode()}}, {"text": instr}])


def _post_image(parts: list[dict]) -> tuple[bytes, str]:
    import requests
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9", "imageSize": "1K"}}}
    r = requests.post(GEMINI_URL, headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"]}, json=body, timeout=120)
    if r.status_code == 402:
        raise RuntimeError("Gemini 선불 크레딧이 없습니다 - AI Studio API 키 화면의 '선불 결제 설정'에서 충전하세요")
    if r.status_code != 200:
        raise RuntimeError(f"이미지 생성 실패 ({r.status_code}): {r.text[:300]}")
    for cand in r.json().get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            data = part.get("inlineData") or part.get("inline_data")
            if data:
                ext = "jpg" if "jpeg" in data.get("mimeType", data.get("mime_type", "")) else "png"
                return base64.b64decode(data["data"]), ext
    raise RuntimeError("이미지가 응답에 없습니다 (안전 필터에 걸렸을 수 있습니다)")


_cand_lock = threading.Lock()


def generate(folder: Path, start_sent: int, end_sent: int, title: str, text: str, hint: str = "") -> dict:
    """후보 N장을 만들어 candidates.json에 기록하고 그 항목을 돌려준다. 일부만 실패하면 성공한 것만."""
    load_env()
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY가 없습니다 - 홈 화면 환경설정에서 등록하세요")
    if not title.strip():
        raise ValueError("편 제목을 먼저 정하세요 - 인트로에 제목이 들어갑니다")
    core, scenes = scene_prompts(folder, title, text, hint.strip()[:500])
    with ThreadPoolExecutor(len(scenes)) as pool:
        results = list(pool.map(lambda sc: _try(draw, sc.prompt, title), scenes))
    out_dir = edit_dir(folder) / "intros"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + os.urandom(3).hex()
    files, captions, errors = [], [], []
    for i, res in enumerate(results):
        if isinstance(res, Exception):
            errors.append(str(res))
            continue
        data, ext = res
        name = f"{stamp}-{i}.{ext}"
        (out_dir / name).write_bytes(data)
        files.append(name)
        captions.append(scenes[i].idea_ko.strip())
    if not files:
        raise RuntimeError(errors[0] if errors else "이미지를 만들지 못했습니다")
    entry = {"title": title, "files": files, "captions": captions, "core": core, "at": datetime.now().isoformat(timespec="seconds"),
             "model": IMAGE_MODEL, "failed": len(errors)}
    with _cand_lock:  # 여러 편을 동시에 만들 때 읽고-쓰는 사이에 서로의 항목을 덮어쓰지 않게
        allc = load_candidates(folder)
        allc[range_key(start_sent, end_sent)] = entry
        write_json(candidates_path(folder), allc)
    return entry


N_EDITS = 2   # 고치기 한 번에 받는 변형 수 - 말이 안 먹힐 때를 대비해 한 장보다 두 장


def edit(folder: Path, start_sent: int, end_sent: int, src: str, instruction: str) -> dict:
    """후보 한 장(src)을 레퍼런스로 지시대로 고친 변형 N_EDITS장을 같은 편 후보에 덧붙이고 그 항목을 돌려준다."""
    load_env()
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY가 없습니다 - 홈 화면 환경설정에서 등록하세요")
    instruction = instruction.strip()[:500]
    if not instruction:
        raise ValueError("고칠 내용을 적어주세요")
    ref_path = image_file(folder, src)
    ref, ref_ext = ref_path.read_bytes(), ref_path.suffix[1:]
    key = range_key(start_sent, end_sent)
    if src not in load_candidates(folder).get(key, {}).get("files", []):
        raise ValueError("이 편의 후보가 아닙니다 - 새로 만든 뒤 고쳐주세요")
    with ThreadPoolExecutor(N_EDITS) as pool:
        results = list(pool.map(lambda _: _try(redraw, ref, ref_ext, instruction), range(N_EDITS)))
    out_dir = edit_dir(folder) / "intros"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + os.urandom(3).hex()
    files, errors = [], []
    for i, res in enumerate(results):
        if isinstance(res, Exception):
            errors.append(str(res))
            continue
        data, ext = res
        name = f"{stamp}-{i}.{ext}"
        (out_dir / name).write_bytes(data)
        files.append(name)
    if not files:
        raise RuntimeError(errors[0] if errors else "이미지를 만들지 못했습니다")
    with _cand_lock:
        allc = load_candidates(folder)
        entry = allc[key]
        entry["files"] += files
        entry["captions"] = list(entry.get("captions") or []) + [f"고침: {instruction}"] * len(files)
        entry["failed"] = len(errors)
        write_json(candidates_path(folder), allc)
    return {**entry, "added": len(files)}


def _try(fn, *args):
    try:
        return fn(*args)
    except Exception as e:  # noqa: BLE001 - 4장 중 일부 실패는 나머지로 계속
        return e


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("n", type=int)
    args = ap.parse_args()
    from split_run import resolve_folder
    from split_export import load_decisions
    from split_sentences import load_sentences
    folder = resolve_folder(args.folder)
    dec = load_decisions(edit_dir(folder))
    sents = load_sentences(folder)["sentences"]
    k = args.n - 1
    start = dec["ends"][k - 1] + 1 if k else 0
    end = dec["ends"][k]
    text = " ".join(dec.get("text_edits", {}).get(str(i), sents[i]["text"]) for i in range(start, end + 1))
    entry = generate(folder, start, end, dec["titles"][k] or f"{args.n}편", text)
    print(json.dumps(entry, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
