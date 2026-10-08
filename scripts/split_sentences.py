"""주제별 분할 1단계 - 대본을 문장 단위로 나눈다 (docs/백로그/주제별-분할.md).

대본 출처는 둘 중 하나:
  - source.srt가 있으면 자막 큐 (사람이 교정한 글이라 가장 정확, 전사 비용 0)
  - 없으면 work/transcript.json (Scribe 단어 단위 전사)

분할 경계는 문장 끝에서만 생긴다 - 문장 중간 절단을 구조적으로 막기 위함. 한국어 자막은
마침표가 없는 경우가 많아서 문장부호만 믿지 않고 종결어미 + 쉼으로도 끝을 판단한다.

Writes <folder>/work/sentences.json:
  {"source": "srt"|"transcript", "duration": 초, "sentences": [{i, start, end, text, gap_after}]}
  gap_after = 다음 문장 시작까지의 쉼(초). 마지막 문장은 영상 끝까지.

Usage:
    python scripts/split_sentences.py <auto-split/NAME>
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path

from common import edit_dir, words_only, write_json, load_transcript

SRT_NAME = "source.srt"
END_PUNCT_RE = re.compile(r"[.?!…。]['\"”’)\]]*$")
# 종결어미 - 문장부호가 없는 자막용. "다"는 "모두 다 같이"처럼 문장 중간에도 오므로 쉼을 함께 본다
END_EOMI_RE = re.compile(r"(다|요|죠|까|네|지|래|군|세)[~]*$")
EOMI_MIN_GAP = 0.3          # 종결어미로 끝나도 이만큼은 쉬어야 문장 끝으로 본다
HARD_GAP = 1.2              # 문장부호·어미가 없어도 이만큼 쉬면 문장 끝
MAX_SENTENCE_SEC = 30.0     # 끝없이 이어지는 문장은 이 길이 근처의 가장 긴 쉼에서 끊는다


def media_duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True, check=True).stdout
    return float(out.strip())


# --------------------------------------------------------------------------------- SRT

_TIME_RE = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)")


def _secs(h, m, s, ms) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, "0")[:3]) / 1000


def parse_srt(text: str) -> list[dict]:
    """큐 목록 [{start, end, text}]. 줄바꿈된 두 줄 자막은 공백으로 잇고, <i>·{\\an8} 같은 태그는 지운다."""
    cues = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("﻿", "").strip()):
        lines = block.strip().split("\n")
        for k, line in enumerate(lines):
            m = _TIME_RE.search(line)
            if m:
                body = " ".join(lines[k + 1:])
                body = re.sub(r"<[^>]+>|\{[^}]+\}", "", body)
                body = re.sub(r"\s+", " ", body).strip()
                if body:
                    cues.append({"start": _secs(*m.groups()[:4]), "end": _secs(*m.groups()[4:]), "text": body})
                break
    cues.sort(key=lambda c: c["start"])
    return cues


SRT_VOICED_MIN_RATIO = 0.8  # 큐 구간 중 이 비율 이상에 실제 목소리 에너지가 있어야 이 영상의 자막으로 본다


def check_srt_matches(folder: Path, cues: list[dict], duration: float) -> None:
    """다른 버전에서 내보낸 SRT를 막는다. 두 가지만 본다: 자막이 영상보다 길지 않은가, 자막이 떠
    있는 동안 실제로 소리가 나는가(audio_map). 한계: 배경음악이 계속 깔린 영상은 두 번째 검사가
    항상 통과하므로 몇 초 밀린 SRT는 못 잡는다 - 그 경우 분할 화면의 "시작 3초" 확인이 마지막 방어."""
    if cues[-1]["end"] > duration + 1.0:
        raise SystemExit(f"자막 파일이 이 영상과 맞지 않습니다 - 마지막 자막({cues[-1]['end']:.0f}초)이 "
                         f"영상 길이({duration:.0f}초)보다 깁니다")
    from audio_map import load_audio_map
    amap = load_audio_map(folder)
    if not amap:
        return
    hop, rms, floor = amap["hop_sec"], amap["rms_db"], amap["room_tone_db"] + 15
    voiced = 0
    for c in cues:
        window = rms[int(c["start"] / hop):int(c["end"] / hop) + 1]
        voiced += bool(window) and max(window) > floor
    ratio = voiced / len(cues)
    if ratio < SRT_VOICED_MIN_RATIO:
        raise SystemExit(f"자막 파일이 이 영상과 맞지 않습니다 - 자막이 떠 있는 구간 중 {ratio:.0%}에만 "
                         f"목소리가 있습니다 (기준 {SRT_VOICED_MIN_RATIO:.0%})")


# --------------------------------------------------------------------------------- 문장 묶기

def _is_end(text: str, gap: float, use_eomi: bool) -> bool:
    if gap >= HARD_GAP or END_PUNCT_RE.search(text):
        return True
    return use_eomi and gap >= EOMI_MIN_GAP and bool(END_EOMI_RE.search(text.rstrip(",")))


def group_units(units: list[dict], use_eomi: bool) -> list[dict]:
    """단어(전사) 또는 큐(SRT)를 문장으로 묶는다. units: [{start, end, text}] 시간순.
    use_eomi는 SRT에만 켠다 - Scribe 전사는 문장부호를 잘 달아서, 어미 규칙까지 쓰면 "하지 않고"의
    "하지" 같은 단어 끝을 문장 끝으로 오인한다."""
    sentences: list[list[dict]] = []
    cur: list[dict] = []
    for k, u in enumerate(units):
        cur.append(u)
        nxt = units[k + 1] if k + 1 < len(units) else None
        gap = (nxt["start"] - u["end"]) if nxt else 999.0
        if _is_end(u["text"], gap, use_eomi):
            sentences.append(cur)
            cur = []
    if cur:
        sentences.append(cur)

    out: list[list[dict]] = []
    for s in sentences:
        out.extend(_break_long(s))
    return [{"start": round(s[0]["start"], 3), "end": round(s[-1]["end"], 3),
             "text": " ".join(u["text"] for u in s)} for s in out]


def _break_long(units: list[dict]) -> list[list[dict]]:
    """MAX_SENTENCE_SEC를 넘는 문장은 가운데 근처의 가장 긴 쉼에서 둘로 나눈다 (재귀)."""
    if len(units) < 2 or units[-1]["end"] - units[0]["start"] <= MAX_SENTENCE_SEC:
        return [units]
    mid = (units[0]["start"] + units[-1]["end"]) / 2
    best_k, best_score = 0, -1.0
    for k in range(len(units) - 1):
        gap = units[k + 1]["start"] - units[k]["end"]
        score = gap - abs(units[k]["end"] - mid) / 100  # 쉼 우선, 같으면 가운데에 가까운 쪽
        if score > best_score:
            best_k, best_score = k, score
    return _break_long(units[:best_k + 1]) + _break_long(units[best_k + 1:])


def build(folder: Path) -> Path:
    from common import source_media
    duration = media_duration(source_media(folder))
    srt = folder / SRT_NAME
    if srt.exists():
        units = parse_srt(srt.read_text(encoding="utf-8", errors="replace"))
        source = "srt"
        if not units:
            raise SystemExit(f"{srt.name}에서 자막을 하나도 읽지 못했습니다 - SRT 형식인지 확인하세요")
        check_srt_matches(folder, units, duration)
    else:
        units = [{"start": w["start"], "end": w["end"], "text": w["text"]}
                 for w in words_only(load_transcript(folder))]
        source = "transcript"

    sents = group_units(units, use_eomi=(source == "srt"))
    for i, s in enumerate(sents):
        s["i"] = i
        s["gap_after"] = round((sents[i + 1]["start"] if i + 1 < len(sents) else duration) - s["end"], 3)

    out = edit_dir(folder) / "sentences.json"
    write_json(out, {"source": source, "duration": round(duration, 3), "sentences": sents})
    print(f"wrote {out} ({len(sents)} sentences from {source}, {duration / 60:.1f}분)")
    return out


def load_sentences(folder: Path) -> dict:
    return json.loads((edit_dir(folder) / "sentences.json").read_text())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    args = ap.parse_args()
    build(Path(args.folder).resolve())


if __name__ == "__main__":
    main()
