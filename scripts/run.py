"""video-cut orchestrator: raw.mp4 in a folder -> review UI in the browser -> FCPXML.

    python scripts/run.py <videos/NAME>            # full pipeline, then opens the review UI
    python scripts/run.py <videos/NAME> --serve    # skip processing, just open the UI
    python scripts/run.py <videos/NAME> --no-llm   # deterministic layers only (no API cost)

Steps (each cached on its output file; delete a file in edit/ to redo that step):
  0 clean_media      raw.mp4 -> edit/clean.mp4      (tmcd/metadata stripped, faststart)
  1 transcribe       -> edit/transcript.json         (ElevenLabs Scribe)
  2 prosody          -> edit/prosody.json            (F0/energy per word, local, no API cost)
  2 audio map        -> edit/audio_map.json          (RMS/breath map, local, no API cost)
  3 speaker blocks   -> edit/speaker_blocks.json      (must run before Stage 1, see below)
  4 pronunciation    -> edit/ng_candidates.json      (낮은 ASR 신뢰도 - 발음 실수 정정 후보,
                        음성학적 유사도 기반이라 Stage 1이 원래 잘 못 잡는 별도 채널)
  4 Stage 1 (전체를 넓게)   -> edit/regions.json      (detect_regions.py, 2026-09-30 하향식
                        재설계 - 원문 전체를 한 번에 읽고 의심 구간을 대략적으로 표시. 로컬
                        힌트(단어 절단/3단어 내 중복, 공짜)+전체 맥락 LLM 스캔(claude-opus-5-5,
                        전체 문서 1회))
  4 Stage 2 (부분을 좁게)   -> edit/ng_classified.json (classify_region.py - 표시된 구간마다
                        확대해서 정확한 단어 경계·case(A~F)·신뢰도를 정함. Sonnet/Opus 티어링,
                        few-shot 정적 6개 + L2 사용자 사례 검색 - fewshot.py)
  4 NG route         -> edit/ng.json                  (route/flag, 최대 삭제 - route_candidates.py
                        그대로 유지)
  4 filler           -> (appended to ng.json)         (standalone 음/어/아, deterministic)
  4 assemble draft   -> edit/draft_cuts.json          (merge every route=CUT item, NG+blocks)
  4 seam refine      -> edit/seams.json, edit/final_cuts.json (docs/기획/02 부분 루프 -
                        boundary snap(파형 정밀화) + judge!=maker content check)
  4 global review    -> edit/global_review.json        (Stage 3 "끝나면 한 번 더" - PD 평가 +
                        시청자 평가를 정확히 1회 통독. missed_cut을 찾으면 assemble+seam을 1회만
                        더 돌려 반영하고 종료. ng.json 역전파로 over_cut/시청자 지적도 검토
                        화면에 뜸)
  5 pauses           -> edit/pauses.json
  6 server           review UI; confirm writes <NAME>.fcpxml + preview.mp4 into the folder
                        (확정 시 learn_from_session.py를 fire-and-forget으로 호출해 few-shot
                        학습 데이터를 자동으로 채운다)

Speaker blocks run before Stage 1 because detect_regions.py reads speaker_blocks.json to skip
spans the block detector already covers - running it after would make every coaching block get
reported twice. assemble_draft.py in turn needs BOTH ng.json and speaker_blocks.json finalized
(including filler's appends to ng.json), so it and seam_refine.py run last within the NG cache
group, gated on the same ng.json existence check as everything else in that group.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import load_env, ensure_api_keys, video_dir, edit_dir  # noqa: E402
import migrate  # noqa: E402


def step(title: str, cmd: list[str]) -> None:
    print(f"\n== {title}")
    subprocess.run([sys.executable, *cmd], check=True, cwd=HERE.parent)


def notify(title: str, message: str) -> None:
    """백로그/R2-시작-마찰-제거.md: 전사·분류가 끝나면 macOS 알림 - 처리 중 다른 일을 하다
    잊어버리는 이탈 순간(백로그/왜-이탈하는가.md) 대응. macOS가 아니거나 알림 권한이 없어도
    파이프라인 자체를 막지 않는다."""
    if sys.platform != "darwin":
        return
    script = f'display notification {json.dumps(message)} with title {json.dumps(title)} sound name "Glass"'
    try:
        subprocess.run(["osascript", "-e", script], check=False, capture_output=True)
    except OSError:
        pass


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--serve", action="store_true", help="skip processing, open the review UI")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()

    load_env()
    folder = video_dir(args.folder)
    edit = edit_dir(folder)
    for msg in migrate.migrate_project(folder):  # 업데이트 뒤 호환 안 되는 캐시만 조용히 정리
        print(f"[migrate] {msg}")
    raw = folder / "raw.mp4"
    if not raw.exists():
        sys.exit(f"put the source video at {raw}")

    if not args.serve:
        ensure_api_keys()  # --serve는 처리 없이 검토 화면만 여니 API 키가 필요 없음
        clean = edit / "clean.mp4"
        if not clean.exists():
            step("0/5 clean media", [str(HERE / "clean_media.py"), str(raw), "--out", str(clean)])
        else:
            print("0/5 clean media: cached")

        step("1/5 transcribe", [str(HERE / "transcribe.py"), str(folder)])

        if not args.no_llm and not (edit / "prosody.json").exists():
            step("2/7 prosody", [str(HERE / "prosody.py"), str(folder)])
        elif not args.no_llm:
            print("2/7 prosody: cached")

        if not (edit / "audio_map.json").exists():
            step("2/7 audio map", [str(HERE / "audio_map.py"), str(folder)])
        else:
            print("2/7 audio map: cached")

        if not (edit / "speaker_blocks.json").exists():
            step("3/6 speaker blocks", [str(HERE / "detect_speaker_blocks.py"), str(folder),
                                        *(["--no-llm"] if args.no_llm else [])])
        else:
            print("3/6 speaker blocks: cached")

        if not (edit / "ng.json").exists():
            step("4/7 pronunciation candidates", [str(HERE / "detect_pronunciation_candidates.py"), str(folder)])
            step("4/7 Stage 1 (전체를 넓게)", [str(HERE / "detect_regions.py"), str(folder),
                                            *(["--no-llm"] if args.no_llm else [])])
            step("4/7 Stage 2 (부분을 좁게)", [str(HERE / "classify_region.py"), str(folder),
                                            *(["--no-llm"] if args.no_llm else [])])
            step("4/7 NG route", [str(HERE / "route_candidates.py"), str(edit / "ng_classified.json"),
                                  "--out", str(edit / "ng.json")])
            step("4/7 filler", [str(HERE / "detect_filler_candidates.py"), str(folder)])  # deterministic, always runs
            if not args.no_llm:
                step("4/7 assemble draft", [str(HERE / "assemble_draft.py"), str(folder)])
                step("4/7 seam refine", [str(HERE / "seam_refine.py"), str(folder)])
                # global_review.py가 내부적으로 1회 재투입(missed_cut 반영 -> assemble_draft.py/
                # seam_refine.py를 한 번만 다시 부름)까지 다 하므로 여기선 한 번만 호출
                step("4/7 global review", [str(HERE / "global_review.py"), str(folder)])
        else:
            print("4/7 NG: cached")

        if not (edit / "pauses.json").exists():
            step("5/7 pauses", [str(HERE / "plan_pauses.py"), str(folder), *(["--no-llm"] if args.no_llm else [])])
        else:
            print("5/7 pauses: cached")

        notify("처리 완료", f"{folder.name} 검토 준비됨 - 브라우저가 곧 열립니다")

    print("\n== 6/7 review UI")
    subprocess.run([sys.executable, str(HERE / "server.py"), str(folder), "--port", str(args.port),
                    *(["--no-open"] if args.no_open else [])], cwd=HERE.parent)


if __name__ == "__main__":
    main()
