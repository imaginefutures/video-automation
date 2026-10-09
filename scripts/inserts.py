"""인서트 편집 - 컷편집을 확정한 영상에 텍스트·이미지 인서트를 만들어 FCPXML 연결 클립으로 얹는다.

규칙(무엇을, 언제, 왜): docs/인서트-가이드.md. 자동화 설계: docs/백로그/자료-화면-삽입.md.

흐름: 사용자가 완성 대본(잘린 말 제외)에서 구간을 드래그 → create() → 백그라운드에서
  1) decide(): Opus 5.5가 구간·앞뒤 문맥·주변 인서트를 보고 형태(텍스트/이미지/영상/실물)를 정함
  2) generate(): 텍스트는 Pillow로 투명 PNG를 그림(즉시, 비용 0), 이미지는 Nano Banana 후보 여러 장
  → 사용자가 화면에서 승인/취소/다시 만들기/형태 바꾸기 → export 때 승인된 것만 FCPXML에 들어간다.

영상(모션그래픽)은 렌더러(Playwright)가 아직 없어 결정까지만 한다 - status "unsupported".
위치는 원본 단어 번호(wi)로만 저장한다. 컷을 다시 고쳐도 위치가 단어를 따라간다.
"""
from __future__ import annotations
import base64
import json
import os
import re
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from build_edl import compute_kept_segments
from common import log_llm_usage, thinking_kwargs, write_json
from split_intro import BRAND_CONTEXT  # 채널 소개 + "Never" 목록 - 인트로 이미지와 같은 규칙

DECIDE_MODEL = "claude-opus-5-5"
JUDGE_MODEL = "claude-sonnet-5"   # 만드는 모델(Gemini) ≠ 판정하는 모델 - 자료-화면-삽입.md 6장
IMAGE_MODEL = "gemini-nano-banana-2.1"   # 10-09 BS183 A/B: 화풍 일관성 좋음, 장당 약 $0.05, 실측 약 30초
IMAGE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{IMAGE_MODEL}:generateContent"
N_IMAGE_CANDIDATES = 3
GUIDE_PATH = Path(__file__).resolve().parent.parent / "docs" / "인서트-가이드.md"
FILE_RE = re.compile(r"^[A-Za-z0-9_\-]+\.(png|jpg|jpeg|mp4)$")
REF_DIR = Path(__file__).resolve().parent.parent / "video-references" / "opus-5.5"
REF_FRAME_CACHE = Path.home() / ".video-cut" / "ref-frames"
# 가이드 8-2: 인서트 내용 -> 레퍼런스 (구성·움직임만 빌리고 색은 채널 스타일)
MOTION_REFS = {
    "concept": ["education__animated-cycloid-lesson__2106052083040256293",
                "production__talking-head-video-converted-to-line-art-b-roll__2102827887732932956"],
    "steps": ["motion__cocktail-recipe-explainer-motion-graphic__2102853258582880547"],
    "compare": ["education__history-of-ai-documentary-short-film__2102844654169575547"],
    "system": ["education__zoomable-app-architecture-canvas__2105309987983745060"],
}
FPS_NUM, FPS_DEN = 30000, 1001

W, H = 1920, 1080
FONT_GOTHIC = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FONT_HEAVY_INDEX = 16       # Apple SD Gothic Neo Heavy
FONT_SERIF = "/System/Library/Fonts/Supplemental/AppleMyungjo.ttf"
WHITE = (255, 255, 255, 255)
YELLOW = (255, 224, 0, 255)  # 가이드 5장: 노란 코멘트 #FFE000~#FFFF5A
OUTLINE = (20, 20, 20, 255)

ILLUSTRATION_STYLE = """Style (fixed for the channel): clean modern editorial illustration - soft flat shapes, gentle shading,
subtle paper texture. Not a photo, not 3D, not cartoonish. Warm cream background (#FAF9F5). Deep violet #4A1B6C main accent
with soft violets (#EFE9F3, #CBBAD8); gold #FFC800 only as one or two tiny accents. Calm, bright, uncluttered, one clear subject.
People small, from the side or behind, no detailed realistic faces. 16:9 frame, full-bleed. No text, letters, numbers or logos anywhere."""

PHOTO_STYLE = """Style: natural documentary-style photograph, as if shot by a parenting magazine photographer in a real Korean
apartment living room. Soft window daylight, warm neutral tones, shallow depth of field, 35mm lens, candid moment, not posed.
Realistic skin, hands and fingers. Ordinary everyday clothes and toys. No text, letters, logos or readable writing anywhere
(blank labels, no brand names). 16:9 frame."""

FORMS = ("text", "image", "video", "asset")


class InsertDecision(BaseModel):
    form: Literal["text", "image", "video", "asset"]
    layer: Literal["구조", "요점", "근거", "장면", "목소리"]
    layout: Literal["top", "comment", "chapter", "quote", "list", "fullscreen", "side"] = Field(
        description="text: top(상단 요약·섹션 바) / comment(노란 코멘트) / chapter(어둡게+큰 제목) / quote(어둡게+명조 인용) / "
                    "list(좌상단 목록). image: fullscreen. asset: side(화자 옆) 또는 fullscreen. video: fullscreen")
    lines: list[str] = Field(description="화면에 올릴 한국어 글자, 줄 단위. text면 본문(1~2줄, 줄당 25자 이내 - quote만 4~8줄), "
                                         "image면 사진 위에 얹을 노란 대사·속마음(없으면 빈 배열)")
    source: str = Field(description="quote의 출처(저자, 연도). 없으면 빈 문자열")
    image_kind: Literal["illustration", "photo", "none"] = Field(description="image일 때 삽화/생성 사진, 아니면 none")
    must_show: list[str] = Field(description="image일 때만: 그림에서 틀리면 안 되는 시각적 사실, 영어, 1~3개. 대체·대비가 핵심이면 "
                                             "'무엇이 아닌지'까지 (예: 'the object in the child's hand is a plain straight twig - it has no spoon bowl, "
                                             "it is clearly NOT a spoon'). 아니면 빈 배열")
    scene: str = Field(description="image: 영어 장면 묘사(주제·구도만, 화풍·글자 지시 금지, 60단어 이내). "
                                   "video: 한국어로 장면별 움직임 구성. asset: 한국어로 사용자에게 받을 실물. text: 빈 문자열")
    reason: str = Field(description="이 형태를 고른 이유, 한국어 한두 문장. 가이드의 어느 규칙인지")
    motion_kind: Literal["concept", "steps", "compare", "system", "none"] = Field(
        description="video일 때만: concept(개념이 그림으로 변함) / steps(단계·과정) / compare(시대·두 대상 비교) / system(구조·관계). 아니면 none")
    alternatives: list[Literal["text", "image", "video", "asset"]] = Field(description="그다음으로 괜찮은 형태")
    warnings: list[str] = Field(description="한국어 주의사항: 넣지 않는 구간, 촘촘함, 사실 확인 필요 등. 없으면 빈 배열")


class ImagePrompt(BaseModel):
    point: str = Field(description="이 그림이 앞뒤 문맥 속에서 시청자에게 한눈에 전달해야 할 한 가지, 한국어 한 문장")
    image_kind: Literal["illustration", "photo"]
    subject: str = Field(description="등장인물과 나이를 구체적으로, 영어 (예: 'one Korean girl about 2 years old'). 사람이 없으면 'no people'")
    scene: str = Field(description="무엇을 그릴지 영어 80단어 이내: 누가, 무엇을 하며, 어떤 물건으로, 어디서, 어떤 구도로. "
                                   "흉내 내는 대상·비유의 단어는 쓰지 않고 실제로 그릴 것만")
    must_show: list[str] = Field(description="틀리면 안 되는 시각적 사실 1~3개, 영어. 대체·대비·변화가 핵심이면 차이가 보이게")
    avoid: list[str] = Field(description="이미지 모델이 잘못 그리기 쉬운 것, 영어 (예: 'a real spoon', 'crying child'). 없으면 빈 배열")


IMAGE_WRITER_SYSTEM = f"""You write one image-generation prompt for an insert shown during a Korean parenting lecture video.
The image model is literal and drifts toward familiar objects and stock clichés, so you must understand the lecture first.

{BRAND_CONTEXT}

Work in this order:
1. point: read the selected passage WITH its surrounding context. What is the lecturer actually explaining here, and what is the
   one thing a viewer should grasp from the picture at a glance? The picture shows that point - not a literal drawing of the words.
2. subject: who appears, with the age the lecture is talking about (유아기 = toddler age 1-3, 유치원생 = preschooler age 3-6,
   만 N세 = N years old). Korean family and home unless the lecture says otherwise. As few people as possible.
3. scene: one moment, one clear subject. Use the concrete objects and situations the lecturer actually mentions.
   - If the point is substitution / pretending / metaphor ("A as if it were B"), draw A only and make A's identity obvious;
     never name B as an object in the scene (writing "a stick like a spoon" makes the model draw a spoon).
   - If the point is a contrast or change, make the difference visible in this single frame (or say clearly which side this is).
   - Leave calm empty space near the top or beside the main person for a short Korean caption that is added later.
4. must_show: the facts a checker will verify; avoid: what the model is likely to get wrong (the imitated object, extra people,
   clichés, anything from the "Never" list).
Never put text, letters, numbers, signs or logos in the picture. Do not describe art style or colors - a fixed style block is appended."""


MOTION_SYSTEM = """You write ONE self-contained HTML file that renders a short motion-graphic insert for a Korean parenting
lecture video (베싸TV: calm, warm, evidence-based). We render it frame by frame with Playwright: for each frame we call
window.seek(t) (t in seconds) and screenshot a 1920x1080 viewport. The clip is cut into the lecture full-screen.

Hard contract:
- Define window.seek = function (t) {...} that fully draws the frame for time t. It must be a PURE function of t:
  no requestAnimationFrame, setTimeout/setInterval, CSS transitions/animations, Date, performance.now, Math.random
  (use a small seeded hash if you need variation). Calling seek in any order must give the same picture.
- Duration D seconds is given. seek(0) is already a composed frame. The key message is readable by ~0.6s and stays
  readable for most of the clip. Nothing important starts after D-0.5s.
- 1920x1080, margin 0, overflow hidden. DOM + inline SVG or a single <canvas>. No external resources at all
  (no web fonts, CDNs, images, network). Font: font-family "Apple SD Gothic Neo", sans-serif (weights 400/700/800).
- Channel style: background warm cream #FAF9F5; main accent deep violet #4A1B6C; soft violets #EFE9F3 and #CBBAD8;
  gold #FFC800 only as one or two tiny accents; ink #141413. Flat, editorial, uncluttered, one idea at a time.
  Easing is closed-form and gentle (easeOutCubic, critically damped springs) - no bouncy overshoot, no glows.
- Keep the bottom 15% of the frame empty (burned-in subtitles live there).
- Korean text: use word-break: keep-all; main text >= 56px, labels >= 36px; never overflow, overlap or get cut off.
  Use the given Korean caption lines verbatim when provided. Do not invent numbers, names or facts.
- Draw people simply (flat silhouettes / simple shapes), never realistic faces.
- Never an empty or frozen frame: something moves gently at all times, but motion must serve the explanation.

Return only the HTML, inside one ```html code block."""


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class InsertStore:
    """edit/inserts.json + edit/inserts/*.png. Session(server.py)이 하나씩 가진다."""

    def __init__(self, session):
        self.s = session
        self.folder: Path = session.folder
        self.path = session.edit / "inserts.json"
        self.dir = session.edit / "inserts"
        self.dir.mkdir(exist_ok=True)
        self.lock = threading.RLock()
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {"items": []}
        for it in self.data["items"]:  # 서버가 생성 도중 꺼졌으면 다시 만들 수 있게
            if it["status"] in ("deciding", "generating"):
                it["status"], it["error"] = "error", "서버가 다시 시작돼 중단됐습니다 - 다시 만들기를 누르세요"

    # ---- 시간 계산: 원본 시각 -> 편집본(타임라인) 시각

    def _kept(self) -> list[dict]:
        return compute_kept_segments([{"start": c["start"], "end": c["end"]} for c in self.s.cut_spans()], self.s.duration)

    @staticmethod
    def to_timeline(kept: list[dict], t: float) -> float:
        acc = 0.0
        for k in kept:
            if t <= k["source_start"]:
                return acc
            if t < k["source_end"]:
                return acc + t - k["source_start"]
            acc += k["source_end"] - k["source_start"]
        return acc

    def kept_words(self, kept: list[dict]) -> list[dict]:
        out, j = [], 0
        for w in self.s.words:
            mid = (w["start"] + w["end"]) / 2
            while j < len(kept) and kept[j]["source_end"] < mid:
                j += 1
            if j < len(kept) and kept[j]["source_start"] <= mid <= kept[j]["source_end"]:
                out.append(w)
        return out

    def payload(self) -> dict:
        kept = self._kept()
        words = self.kept_words(kept)
        with self.lock:
            items = json.loads(json.dumps(self.data["items"]))
        by_wi = {w["wi"]: w for w in self.s.words}
        for it in items:
            ws, we = by_wi.get(it["wi_start"]), by_wi.get(it["wi_end"])
            if ws and we:
                it["src_start"], it["src_end"] = ws["start"], we["end"]
                it["t_start"] = round(self.to_timeline(kept, ws["start"]), 2)
                it["t_end"] = round(self.to_timeline(kept, we["end"]), 2)
        return {
            "name": self.s.name, "media": self.s.probe, "duration_src": self.s.duration,
            "duration_out": round(sum(k["source_end"] - k["source_start"] for k in kept), 2),
            "cut_spans": [{"start": c["start"], "end": c["end"]} for c in self.s.cut_spans()],
            "words": [{"wi": w["wi"], "t": w["text"], "s": w["start"], "e": w["end"],
                       "o": round(self.to_timeline(kept, w["start"]), 2)} for w in words],
            "items": items,
        }

    # ---- 저장

    def _save(self) -> None:
        with self.lock:
            write_json(self.path, self.data)

    def _get(self, iid: str) -> dict:
        for it in self.data["items"]:
            if it["id"] == iid:
                return it
        raise ValueError("없는 인서트입니다")

    def _set(self, it: dict, **kw) -> None:
        with self.lock:
            it.update(kw)
            it["updated_at"] = _now()
            self._save()

    # ---- 생성 요청

    def create(self, wi_start: int, wi_end: int) -> dict:
        if wi_end < wi_start:
            wi_start, wi_end = wi_end, wi_start
        text = "".join(w["text"] + " " for w in self.s.words[wi_start:wi_end + 1]).strip()
        it = {"id": uuid.uuid4().hex[:8], "wi_start": wi_start, "wi_end": wi_end, "text": text,
              "status": "deciding", "created_at": _now(), "updated_at": _now(),
              "decision": None, "form": None, "files": [], "candidates": [], "chosen": None, "error": None}
        with self.lock:
            self.data["items"].append(it)
            self._save()
        threading.Thread(target=self._run, args=(it["id"], None), daemon=True).start()
        return it

    def _run(self, iid: str, force_form: str | None, note: str | None = None) -> None:
        it = self._get(iid)
        try:
            self._set(it, status="deciding", error=None, progress=None)
            if note:
                self._set(it, notes=(it.get("notes") or []) + [note])
            dec = self.decide(it, force_form)
            if dec["form"] == "image":
                dec.update(self.write_image_prompt(it, dec))
            self._set(it, decision=dec, form=dec["form"], status="generating", candidates=[], chosen=None, files=[])
            self.generate(it)
        except Exception as e:  # 화면에 그대로 보여 준다 - 조용히 실패하지 않게
            self._set(it, status="error", error=str(e)[:400], progress=None)

    # ---- 1) 형태 결정

    def _sentences(self, words: list[dict]) -> list[dict]:
        sents, cur = [], []
        for w in words:
            cur.append(w)
            if w["text"].endswith((".", "?", "!")):
                sents.append(cur)
                cur = []
        if cur:
            sents.append(cur)
        return [{"wi_start": s[0]["wi"], "wi_end": s[-1]["wi"], "text": " ".join(x["text"] for x in s)} for s in sents]

    def _context(self, it: dict, n_before: int = 5, n_after: int = 3) -> tuple[list[str], list[str]]:
        sents = self._sentences(self.kept_words(self._kept()))
        before = [s["text"] for s in sents if s["wi_end"] < it["wi_start"]][-n_before:]
        after = [s["text"] for s in sents if s["wi_start"] > it["wi_end"]][:n_after]
        return before, after

    def decide(self, it: dict, force_form: str | None) -> dict:
        import anthropic
        kept = self._kept()
        before, after = self._context(it)
        by_wi = {w["wi"]: w for w in self.s.words}
        t0 = self.to_timeline(kept, by_wi[it["wi_start"]]["start"])
        t1 = self.to_timeline(kept, by_wi[it["wi_end"]]["end"])
        near = []
        with self.lock:
            others = [o for o in self.data["items"] if o["id"] != it["id"] and o.get("decision") and o["status"] != "rejected"]
        for o in others:
            ot = self.to_timeline(kept, by_wi[o["wi_start"]]["start"])
            if abs(ot - t0) <= 30:
                d = o["decision"]
                near.append(f"- {ot - t0:+.0f}초: {d['form']}/{d['layout']} ({d['layer']}) \"{' / '.join(d['lines'])[:60]}\"")
        sections = [o["decision"]["lines"] for o in others
                    if o["decision"]["layer"] == "구조" and self.to_timeline(kept, by_wi[o["wi_start"]]["start"]) <= t0]
        total = sum(k["source_end"] - k["source_start"] for k in kept)
        user = f"""지정 구간 (편집본 {t0:.0f}~{t1:.0f}초, 길이 {t1 - t0:.1f}초, 영상 전체 {total / 60:.0f}분 중 {t0 / max(total, 1) * 100:.0f}% 지점):
"{it['text']}"

앞 문맥 (최대 5문장):
{chr(10).join(before) or '(영상 시작)'}

뒤 문맥 (최대 3문장):
{chr(10).join(after) or '(영상 끝)'}

현재 섹션 바: {' / '.join(sections[-1]) if sections else '(없음)'}
앞뒤 30초 안의 다른 인서트:
{chr(10).join(near) or '(없음)'}"""
        if it.get("notes"):
            prev = it.get("decision") or {}
            user += ("\n\n이전 결과에 대한 사용자 요청 (반드시 반영):\n" + "\n".join(f"- {n}" for n in it["notes"])
                     + (f"\n이전 장면 묘사: {prev.get('scene')}\n이전 글자: {' / '.join(prev.get('lines', []))}" if prev else ""))
        if force_form:
            user += f"\n\n사용자가 형태를 '{force_form}'(으)로 정했다. form은 반드시 {force_form}로 하고, 그 형태에 맞게 나머지를 채워라."
        system = ("너는 베싸TV(근거 기반 육아 강의 채널)의 영상 편집자다. 사용자가 인서트를 넣고 싶은 대본 구간을 지정했다. "
                  "아래 인서트 가이드(완성본 3편 분석)를 따라, 이 구간의 역할과 형태(텍스트/이미지/영상/실물)를 정하고 화면에 올릴 내용을 만든다. "
                  "가이드 8장의 판단 순서(역할 → 기본 형태 → 문맥 조정)를 그대로 따른다.\n"
                  "- 글자는 받아쓰기가 아니라 편집자가 다시 쓴 슬로건이다. 섹션 바(구조)는 시청자 말투 질문형 또는 결론형\n"
                  "- 숫자·연도·인명·연구 결과는 대본에 있는 것만 쓴다. 지어내지 않는다\n"
                  "- 실존 인물의 얼굴, 책 표지, 논문 화면, 실제 촬영 장면은 만들지 말고 form=asset으로 사용자에게 요청한다\n"
                  "- image의 scene은 영어로, 주제와 구도만 쓴다\n"
                  "- 이미지 모델은 익숙한 물건으로 끌려간다. 장면의 핵심이 '무엇을 무엇처럼'(대체·흉내·비교)이면, scene에서 흉내 내는 대상의 "
                  "이름을 그릴 물건처럼 쓰지 말고(예: 'stick like a spoon' 금지) 실제로 그릴 물건만 구체적으로 묘사하고, must_show에 '무엇이 아닌지'를 적는다\n"
                  "\n=== 인서트 가이드 ===\n" + GUIDE_PATH.read_text())
        resp = anthropic.Anthropic().messages.parse(
            model=DECIDE_MODEL, max_tokens=4000, system=system,
            messages=[{"role": "user", "content": user}],
            output_format=InsertDecision, **thinking_kwargs(DECIDE_MODEL, effort="medium"))
        log_llm_usage(self.folder, "insert_decide", DECIDE_MODEL, resp.usage)
        dec = resp.parsed_output.model_dump()
        if force_form:
            dec["form"] = force_form
        # 대본에 없는 숫자는 경고 (한국어 숫자 표기 "사십 년대"까지 대조할 수는 없어 막지는 않는다)
        digits = set(re.findall(r"\d+", " ".join(dec["lines"])))
        missing = sorted(d for d in digits if d not in it["text"])
        if missing:
            dec["warnings"].append(f"대본 구간에 없는 숫자: {', '.join(missing)} - 맞는지 확인하세요")
        return dec

    def write_image_prompt(self, it: dict, dec: dict) -> dict:
        """이미지 전용 프롬프트 단계 - 문맥에서 '한눈에 보여 줄 한 가지'를 먼저 정하고 그릴 것을 쓴다.
        10-09: 형태 결정 단계가 함께 쓴 장면("stick like a spoon")에서 이미지 모델이 진짜 숟가락을 그렸다."""
        import anthropic
        before, after = self._context(it, 8, 4)
        notes = "\n".join(f"- {n}" for n in it.get("notes") or [])
        user = f"""Selected passage (Korean): "{it['text']}"

Before (up to 8 sentences):
{chr(10).join(before) or '(start of video)'}

After (up to 4 sentences):
{chr(10).join(after) or '(end of video)'}

The editor's plan for this insert: layer={dec['layer']}, caption to overlay later={dec['lines']}, rough idea={dec.get('scene', '')}
Suggested kind: {dec.get('image_kind')}  (photo = realistic everyday scene, illustration = concept drawing)"""
        if notes:
            user += f"\n\nThe user reviewed earlier results and asked (must follow):\n{notes}"
        resp = anthropic.Anthropic().messages.parse(
            model=DECIDE_MODEL, max_tokens=3000, system=IMAGE_WRITER_SYSTEM,
            messages=[{"role": "user", "content": user}],
            output_format=ImagePrompt, **thinking_kwargs(DECIDE_MODEL, effort="medium"))
        log_llm_usage(self.folder, "insert_image_prompt", DECIDE_MODEL, resp.usage)
        ip = resp.parsed_output
        return {"point": ip.point, "image_kind": ip.image_kind, "subject": ip.subject,
                "scene": f"{ip.subject}. {ip.scene}", "must_show": ip.must_show, "avoid": ip.avoid}

    # ---- 2) 생성

    def generate(self, it: dict) -> None:
        dec, form = it["decision"], it["form"]
        if form == "text":
            name = f"{it['id']}_text_{int(time.time())}.png"
            render_text(dec["layout"], dec["lines"], dec.get("source", "")).save(self.dir / name)
            self._set(it, files=[name], status="ready")
        elif form == "image":
            self._generate_images(it)
        elif form == "video":
            self._generate_motion(it)
        else:  # asset
            self._set(it, status="needs_asset", error=None)

    def _generate_images(self, it: dict) -> None:
        import requests
        if not os.environ.get("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY가 없습니다 - 홈 화면 설정에서 등록하세요")
        dec = it["decision"]
        style = PHOTO_STYLE if dec["image_kind"] == "photo" else ILLUSTRATION_STYLE
        must = [m for m in dec.get("must_show") or [] if m.strip()]
        avoid = [a for a in dec.get("avoid") or [] if a.strip()]
        prompt = (f"{dec['scene']}\n" + "".join(f"\nMUST be unmistakable: {m}" for m in must)
                  + (f"\nDo NOT draw: {'; '.join(avoid)}" if avoid else "") + f"\n\n{style}")

        def one(k: int) -> str:
            body = {"contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9", "imageSize": "2K"}}}
            r = requests.post(IMAGE_URL, headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"]}, json=body, timeout=180)
            if r.status_code == 402:
                raise RuntimeError("Gemini 선불 크레딧이 없습니다 - AI Studio에서 충전하세요")
            if r.status_code != 200:
                raise RuntimeError(f"이미지 생성 실패 ({r.status_code}): {r.text[:200]}")
            for cand in r.json().get("candidates", []):
                for part in cand.get("content", {}).get("parts", []):
                    d = part.get("inlineData") or part.get("inline_data")
                    if d:
                        name = f"{it['id']}_img{k}_{int(time.time())}.jpg"
                        (self.dir / name).write_bytes(base64.b64decode(d["data"]))
                        return name
            raise RuntimeError("이미지가 응답에 없습니다 (안전 필터에 걸렸을 수 있습니다)")

        def batch(start: int) -> tuple[list[str], list[str]]:
            with ThreadPoolExecutor(N_IMAGE_CANDIDATES) as ex:
                futs = [ex.submit(one, start + k) for k in range(N_IMAGE_CANDIDATES)]
                names, errors = [], []
                for f in futs:
                    try:
                        names.append(f.result())
                    except Exception as e:
                        errors.append(str(e))
            if names:
                self._log_image_cost(len(names))
            return names, errors

        names, errors = batch(0)
        if not names:
            raise RuntimeError(errors[0] if errors else "이미지를 만들지 못했습니다")
        # 후보부터 저장 - 돈을 낸 이미지가 뒤 단계 실패로 사라지지 않게 (10-09: Pillow 누락으로 3장 유실될 뻔함)
        self._set(it, candidates=names, checks=[], chosen=0, files=[names[0]])
        checks = self._judge(it, names, must)
        if must and checks and not any(c["ok"] for c in checks):
            # 전부 조건을 못 맞추면 한 번만 더 - 판정 이유를 프롬프트에 넣어서 (자동 복구는 한 번까지, 원칙 3)
            fails = "; ".join(c["note"] for c in checks if c.get("note"))[:400]
            prompt += f"\n\nPrevious attempts were wrong: {fails}. Fix exactly this."
            more, errs2 = batch(N_IMAGE_CANDIDATES)
            errors += errs2
            if more:
                names += more
                checks += self._judge(it, more, must)
        # 통과한 후보를 앞으로
        order = sorted(range(len(names)), key=lambda k: (not (checks[k]["ok"] if k < len(checks) else True), k))
        names = [names[k] for k in order]
        checks = [checks[k] for k in order] if len(checks) == len(order) else []
        self._set(it, candidates=names, checks=checks, chosen=0, files=[names[0]])
        overlay = self._render_overlay(it)
        warn = None
        if checks and not checks[0]["ok"]:
            warn = f"판정 모델: 조건을 맞춘 후보가 없습니다 - {checks[0]['note']}. 요청을 적어 다시 만들어 보세요"
        elif errors:
            warn = f"{len(errors)}장 실패: {errors[0]}"
        self._set(it, files=[names[0]] + ([overlay] if overlay else []), status="ready", error=warn)

    def _judge(self, it: dict, names: list[str], must: list[str]) -> list[dict]:
        """다른 모델이 후보마다 must_show를 지켰는지 본다. 판정 실패는 생성을 막지 않는다(표시만)."""
        if not must:
            return []
        try:
            import anthropic
            import io
            from PIL import Image

            class Verdict(BaseModel):
                index: int
                ok: bool
                note: str = Field(description="틀렸으면 무엇이 틀렸는지 한국어 한 문장, 맞으면 빈 문자열")

            class Verdicts(BaseModel):
                verdicts: list[Verdict]

            content: list[dict] = [{"type": "text", "text": "이 장면을 위해 생성한 후보 이미지들이다. 각 후보가 아래 조건을 모두 만족하는지 엄격하게 판정하라. "
                                    "애매하면 ok=false.\n조건:\n" + "\n".join(f"- {m}" for m in must)
                                    + f"\n\n이 그림이 보여 줘야 할 것: {it['decision'].get('point', '')}\n장면: {it['decision'].get('scene', '')}"}]
            for k, n in enumerate(names):
                im = Image.open(self.dir / n).convert("RGB")
                im.thumbnail((1024, 1024))
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=85)
                content += [{"type": "text", "text": f"후보 {k}:"},
                            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                         "data": base64.b64encode(buf.getvalue()).decode()}}]
            resp = anthropic.Anthropic().messages.parse(
                model=JUDGE_MODEL, max_tokens=1500, messages=[{"role": "user", "content": content}],
                output_format=Verdicts, **thinking_kwargs(JUDGE_MODEL))
            log_llm_usage(self.folder, "insert_judge", JUDGE_MODEL, resp.usage)
            got = {v.index: {"ok": v.ok, "note": v.note} for v in resp.parsed_output.verdicts}
            return [got.get(k, {"ok": True, "note": ""}) for k in range(len(names))]
        except Exception as e:
            print(f"[inserts] judge failed: {e}")
            return []

    # ---- 영상(모션그래픽): Opus가 seek(t) HTML을 쓰고 Playwright로 프레임 렌더

    def _progress(self, it: dict, msg: str) -> None:
        self._set(it, progress=msg)

    def _ensure_renderer(self, it: dict) -> None:
        import subprocess
        import sys
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                p.chromium.launch().close()
            return
        except ImportError:
            raise RuntimeError("렌더러(playwright)가 설치되지 않았습니다 - 플러그인을 업데이트하세요")
        except Exception:
            pass
        self._progress(it, "렌더러 설치 중 (처음 한 번, 약 150MB)…")
        r = subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"렌더러 설치 실패: {r.stderr[-300:]}")

    def _ref_material(self, kind: str) -> tuple[str, list[bytes]]:
        """레퍼런스 프롬프트 원문 + 영상에서 뽑은 프레임 6장(JPEG). 라이브러리가 없으면 빈 값 - 없어도 만든다."""
        import subprocess
        for name in MOTION_REFS.get(kind) or MOTION_REFS["concept"]:
            md, mp4 = REF_DIR / f"{name}.md", REF_DIR / f"{name}.mp4"
            if not (md.exists() and mp4.exists()):
                continue
            text = md.read_text()
            prompt = text.split("## Prompt", 1)[-1][:2500]
            cache = REF_FRAME_CACHE / name
            if not cache.exists() or len(list(cache.glob("*.jpg"))) < 6:
                cache.mkdir(parents=True, exist_ok=True)
                dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                                           capture_output=True, text=True).stdout.strip() or 10)
                for k in range(6):
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{dur * (k + 0.5) / 6:.2f}", "-i", str(mp4), "-frames:v", "1",
                                    "-vf", "scale=640:-2", "-q:v", "4", str(cache / f"{k}.jpg")], check=False)
            frames = [f.read_bytes() for f in sorted(cache.glob("*.jpg"))][:6]
            return f"Reference '{name}' (borrow composition and motion ideas only, NOT its colors or language):\n{prompt}", frames
        return "", []

    def _write_motion_html(self, it: dict, dur: float, fix: tuple[str, str, list[bytes]] | None = None) -> str:
        import anthropic
        dec = it["decision"]
        before, after = self._context(it, 6, 3)
        ref_text, ref_frames = self._ref_material(dec.get("motion_kind") or "concept")
        notes = "\n".join(f"- {n}" for n in it.get("notes") or [])
        content: list[dict] = [{"type": "text", "text": f"""Lecture passage (Korean): "{it['text']}"
Before: {' '.join(before)[-900:]}
After: {' '.join(after)[:500]}

What this clip must make clear (editor's plan, Korean): {dec.get('scene', '')}
Korean caption lines to show (verbatim, may be empty): {dec.get('lines', [])}
Duration D = {dur:.2f} seconds.
{('User requests (must follow):' + chr(10) + notes) if notes else ''}

{ref_text}"""}]
        for b in ref_frames:
            content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(b).decode()}})
        if fix:
            old_html, problems, shots = fix
            content.append({"type": "text", "text": f"Your previous version had these problems - fix exactly these and keep the rest:\n{problems}\n\nPrevious HTML:\n```html\n{old_html}\n```\nIts rendered frames:"})
            for b in shots:
                content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(b).decode()}})
        client = anthropic.Anthropic()
        with client.messages.stream(model=DECIDE_MODEL, max_tokens=32000, system=MOTION_SYSTEM,
                                    messages=[{"role": "user", "content": content}],
                                    **thinking_kwargs(DECIDE_MODEL, effort="medium")) as stream:
            msg = stream.get_final_message()
        log_llm_usage(self.folder, "insert_motion_html", DECIDE_MODEL, msg.usage)
        text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
        m = re.search(r"```html\s*(.*?)```", text, re.S)
        html = (m.group(1) if m else text).strip()
        if "seek" not in html:
            raise RuntimeError("모션 HTML에 seek(t)가 없습니다 - 다시 만들어 보세요")
        return html

    def _shots(self, html_path: Path, times: list[float]) -> list[bytes]:
        from playwright.sync_api import sync_playwright
        out = []
        with sync_playwright() as p:
            b = p.chromium.launch()
            page = b.new_page(viewport={"width": W, "height": H})
            errors: list[str] = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(html_path.as_uri())
            page.wait_for_function("typeof window.seek === 'function'", timeout=10000)
            for t in times:
                page.evaluate(f"window.seek({t})")
                out.append(page.screenshot(type="jpeg", quality=85))
            b.close()
        if errors:
            raise RuntimeError(f"모션 HTML 실행 오류: {errors[0][:200]}")
        return out

    def _judge_motion(self, it: dict, shots: list[bytes], times: list[float]) -> tuple[bool, str]:
        import anthropic

        class MotionVerdict(BaseModel):
            ok: bool
            problems: str = Field(description="고칠 점을 영어로 구체적으로 (프레임 번호와 위치). 문제가 없으면 빈 문자열")

        dec = it["decision"]
        content: list[dict] = [{"type": "text", "text": (
            "These are frames of a motion-graphic insert for a Korean parenting lecture, at the given times. Judge strictly:\n"
            "1) any Korean text overflowing, overlapping, cut off at the edge, or too small to read (<36px)?\n"
            "2) anything drawn in the bottom 15% of the frame (reserved for subtitles)?\n"
            "3) empty/blank or broken-looking frames, garbled shapes, realistic faces?\n"
            f"4) does it clearly show this point: {dec.get('scene', '')}\n"
            f"5) are these caption lines shown correctly (if any): {dec.get('lines', [])}\n"
            "ok=true only if all pass.")}]
        for t, b in zip(times, shots):
            content += [{"type": "text", "text": f"t={t:.1f}s"},
                        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(b).decode()}}]
        resp = anthropic.Anthropic().messages.parse(model=JUDGE_MODEL, max_tokens=1500, messages=[{"role": "user", "content": content}],
                                                    output_format=MotionVerdict, **thinking_kwargs(JUDGE_MODEL))
        log_llm_usage(self.folder, "insert_motion_judge", JUDGE_MODEL, resp.usage)
        return resp.parsed_output.ok, resp.parsed_output.problems

    def _render_mp4(self, it: dict, html_path: Path, dur: float, out: Path) -> None:
        import subprocess
        from playwright.sync_api import sync_playwright
        n = max(1, round(dur * FPS_NUM / FPS_DEN))
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", f"{FPS_NUM}/{FPS_DEN}", "-c:v", "mjpeg",
                               "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "medium",
                               "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
        try:
            with sync_playwright() as p:
                b = p.chromium.launch()
                page = b.new_page(viewport={"width": W, "height": H})
                page.goto(html_path.as_uri())
                page.wait_for_function("typeof window.seek === 'function'", timeout=10000)
                for k in range(n):
                    page.evaluate(f"window.seek({k * FPS_DEN / FPS_NUM})")
                    ff.stdin.write(page.screenshot(type="jpeg", quality=95))
                    if k % 30 == 0:
                        self._progress(it, f"렌더링 {k}/{n} 프레임…")
                b.close()
        finally:
            ff.stdin.close()
            ff.wait()
        if ff.returncode != 0 or not out.exists():
            raise RuntimeError("영상 인코딩 실패")

    def _generate_motion(self, it: dict) -> None:
        self._ensure_renderer(it)
        by_wi = {w["wi"]: w for w in self.s.words}
        kept = self._kept()
        span = self.to_timeline(kept, by_wi[it["wi_end"]]["end"]) - self.to_timeline(kept, by_wi[it["wi_start"]]["start"])
        dur = min(20.0, max(3.0, span))
        stamp = int(time.time())
        html_path = self.dir / f"{it['id']}_motion_{stamp}.html"
        times = [dur * f for f in (0.12, 0.4, 0.7, 0.95)]
        self._progress(it, "레퍼런스를 보고 모션을 설계하는 중… (1~3분)")
        html = self._write_motion_html(it, dur)
        html_path.write_text(html)
        self._progress(it, "프레임 검사 중…")
        shots = self._shots(html_path, times)
        ok, problems = self._judge_motion(it, shots, times)
        if not ok:  # 한 번만 고친다 (원칙 3)
            self._progress(it, "검사에서 나온 문제를 고치는 중…")
            html = self._write_motion_html(it, dur, fix=(html, problems, shots))
            html_path = self.dir / f"{it['id']}_motion_{stamp}b.html"
            html_path.write_text(html)
            shots = self._shots(html_path, times)
            ok, problems = self._judge_motion(it, shots, times)
        keyframes = []
        for k, b in enumerate(shots):
            name = f"{it['id']}_key{k}_{stamp}.jpg"
            (self.dir / name).write_bytes(b)
            keyframes.append(name)
        self._set(it, candidates=keyframes, chosen=None)
        out = self.dir / f"{it['id']}_motion_{stamp}.mp4"
        self._render_mp4(it, html_path, dur, out)
        self._set(it, files=[out.name], status="ready", progress=None,
                  error=None if ok else f"판정 모델: {problems[:300]} - 요청을 적어 다시 만들 수 있어요")

    def _render_overlay(self, it: dict) -> str | None:
        lines = [l for l in it["decision"]["lines"] if l.strip()]
        if not lines:
            return None
        name = f"{it['id']}_overlay_{int(time.time())}.png"
        render_text("comment", lines, "").save(self.dir / name)
        return name

    def _log_image_cost(self, n: int) -> None:
        try:
            with open(self.s.edit / "llm_usage.jsonl", "a") as f:
                f.write(json.dumps({"ts": _now(), "step": "insert_image", "model": IMAGE_MODEL, "images": n,
                                    "cost_usd": round(0.05 * n, 3)}, ensure_ascii=False) + "\n")
        except OSError:
            pass

    # ---- 사용자 조작

    def update(self, iid: str, action: str, body: dict) -> dict:
        it = self._get(iid)
        if action in ("approve", "reject", "reopen"):
            if it["status"] not in ("ready", "approved", "rejected"):
                raise ValueError("아직 결과가 없어 승인할 수 없습니다")
            self._set(it, status={"approve": "approved", "reject": "rejected", "reopen": "ready"}[action])
        elif action == "delete":
            with self.lock:
                self.data["items"] = [o for o in self.data["items"] if o["id"] != iid]
                self._save()
            return {"deleted": iid}
        elif action == "regenerate":
            note = (body.get("note") or "").strip() or None
            threading.Thread(target=self._run, args=(iid, it["form"] if body.get("keep_form", True) else None, note),
                             daemon=True).start()
        elif action == "form":
            form = body.get("form")
            if form not in FORMS:
                raise ValueError("알 수 없는 형태입니다")
            threading.Thread(target=self._run, args=(iid, form), daemon=True).start()
        elif action == "choose":
            if it["form"] != "image":
                raise ValueError("이미지 인서트만 후보를 고를 수 있습니다")
            k = int(body["index"])
            if not (0 <= k < len(it["candidates"])):
                raise ValueError("없는 후보입니다")
            self._set(it, chosen=k, files=[it["candidates"][k]] + it["files"][1:])
        elif action == "edit_text":
            lines = [l for l in (body.get("lines") or []) if isinstance(l, str)]
            dec = dict(it["decision"] or {}, lines=lines)
            if "source" in body:
                dec["source"] = str(body["source"])
            if "layout" in body and it["form"] == "text":
                dec["layout"] = body["layout"]
            self._set(it, decision=dec)
            if it["form"] == "text":
                name = f"{it['id']}_text_{int(time.time())}.png"
                render_text(dec["layout"], lines, dec.get("source", "")).save(self.dir / name)
                self._set(it, files=[name], status="ready" if it["status"] != "approved" else "approved")
            elif it["form"] == "image" and it["files"]:
                overlay = self._render_overlay(it)
                self._set(it, files=[it["files"][0]] + ([overlay] if overlay else []))
        else:
            raise ValueError(f"알 수 없는 동작: {action}")
        return it

    def upload_asset(self, iid: str, filename: str, data: bytes) -> dict:
        """실물(책 표지·논문 캡처 등)을 받아 화자 옆 1/3 또는 전체 화면 PNG로 배치한다."""
        from PIL import Image
        import io
        it = self._get(iid)
        src = Image.open(io.BytesIO(data)).convert("RGBA")
        layout = (it.get("decision") or {}).get("layout", "side")
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if layout == "fullscreen":
            canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
            box = (W, H)
            src.thumbnail(box)
            canvas.paste(src, ((W - src.width) // 2, (H - src.height) // 2), src)
        else:  # side: 화면 오른쪽 1/3, 하단 자막 안전 영역(약 15%) 위
            src.thumbnail((int(W * 0.30), int(H * 0.72)))
            canvas.paste(src, (W - src.width - 120, (int(H * 0.85) - src.height) // 2 + 20), src)
        name = f"{iid}_asset_{int(time.time())}.png"
        canvas.save(self.dir / name)
        overlay = self._render_overlay(it) if it.get("decision") else None
        self._set(it, files=[name] + ([overlay] if overlay else []), status="ready", form="asset", error=None)
        return it

    def file(self, name: str) -> Path:
        if not FILE_RE.match(name) or not (self.dir / name).is_file():
            raise ValueError("없는 파일입니다")
        return self.dir / name

    def manifest(self) -> Path | None:
        """export_fcpxml.py --inserts 가 읽는 목록 (승인된 것만). 없으면 None."""
        by_wi = {w["wi"]: w for w in self.s.words}
        out = []
        with self.lock:
            items = [it for it in self.data["items"] if it["status"] == "approved" and it["files"]]
        for it in sorted(items, key=lambda x: by_wi[x["wi_start"]]["start"]):
            label = f"{it['form']} {' '.join((it.get('decision') or {}).get('lines', []))[:30] or it['text'][:30]}"
            out.append({"id": it["id"], "start": by_wi[it["wi_start"]]["start"], "end": by_wi[it["wi_end"]]["end"],
                        "name": label, "role": f"인서트.{ {'text': '텍스트', 'image': '이미지', 'video': '영상', 'asset': '실물'}[it['form']] }",
                        "layers": [str((self.dir / f).resolve()) for f in it["files"]]})
        if not out:
            return None
        p = self.s.edit / "inserts_manifest.json"
        write_json(p, {"inserts": out})
        return p


# ----------------------------------------------------------------------------- 텍스트 렌더 (가이드 5장 스타일)

def _font(size: int, serif: bool = False):
    from PIL import ImageFont
    return ImageFont.truetype(FONT_SERIF, size) if serif else ImageFont.truetype(FONT_GOTHIC, size, index=FONT_HEAVY_INDEX)


def _fit(draw, lines: list[str], size: int, max_w: int, serif: bool = False):
    while size > 24:
        f = _font(size, serif)
        if all(draw.textlength(l, font=f) <= max_w for l in lines):
            return f, size
        size -= 4
    return _font(size, serif), size


def render_text(layout: str, lines: list[str], source: str = ""):
    """투명 1920x1080 PNG. 화자 화면 위에 FCP 연결 클립으로 얹힌다."""
    from PIL import Image, ImageDraw
    lines = [l for l in lines if l.strip()] or [" "]
    dim = layout in ("chapter", "quote")
    im = Image.new("RGBA", (W, H), (0, 0, 0, 190 if dim else 0))
    d = ImageDraw.Draw(im)

    def center(f, size, y0, color, stroke):
        for i, l in enumerate(lines):
            w = d.textlength(l, font=f)
            d.text(((W - w) / 2, y0 + i * size * 1.3), l, font=f, fill=color, stroke_width=stroke, stroke_fill=OUTLINE)

    if layout == "top":          # 상단 한 줄 요약 / 섹션 바: 흰 초굵은 고딕 + 두꺼운 검정 외곽선, 화자 머리 위
        f, size = _fit(d, lines, 84, W - 200)
        center(f, size, 46, WHITE, max(6, size // 11))
    elif layout == "comment":    # 노란 코멘트: 흰 글씨보다 작게, 화자 머리 오른쪽 위
        f, size = _fit(d, lines, 60, int(W * 0.42))
        x = int(W * 0.56)
        for i, l in enumerate(lines):
            d.text((x, 150 + i * size * 1.3), l, font=f, fill=YELLOW, stroke_width=max(4, size // 14), stroke_fill=OUTLINE)
    elif layout == "chapter":    # 어둡게 + 가운데 큰 제목 (2~4초)
        f, size = _fit(d, lines, 128, W - 240)
        center(f, size, (H - len(lines) * size * 1.3) / 2, WHITE, 0)
    elif layout == "quote":      # 어둡게 + 명조 인용 + 우상단 출처
        f, size = _fit(d, lines, 56, W - 320, serif=True)
        center(f, size, (H - len(lines) * size * 1.5) / 2, WHITE, 0)
        if source.strip():
            sf = _font(30, serif=True)
            d.text((W - 120 - d.textlength(source, font=sf), 90), source, font=sf, fill=(230, 230, 230, 255))
    elif layout == "list":       # 좌상단 누적 목록
        f, size = _fit(d, lines, 64, int(W * 0.6))
        for i, l in enumerate(lines):
            d.text((90, 60 + i * size * 1.35), l, font=f, fill=WHITE, stroke_width=max(5, size // 12), stroke_fill=OUTLINE)
    else:                        # 알 수 없는 레이아웃은 상단 요약으로
        f, size = _fit(d, lines, 84, W - 200)
        center(f, size, 46, WHITE, max(6, size // 11))
    return im
