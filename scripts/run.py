"""video-cut orchestrator: raw.mp4 in a folder -> review UI in the browser -> FCPXML.

    python scripts/run.py <videos/NAME>            # full pipeline, then opens the review UI
    python scripts/run.py <videos/NAME> --serve    # skip processing, just open the UI
    python scripts/run.py <videos/NAME> --no-llm   # deterministic layers only (no API cost)

Steps (each cached on its output file; delete a file in edit/ to redo that step):
  0 clean_media      raw.mp4 -> edit/clean.mp4      (tmcd/metadata stripped, faststart)
  1 transcribe       -> edit/transcript.json         (ElevenLabs Scribe)
  2 prosody          -> edit/prosody.json            (F0/energy per word, local, no API cost)
  2 audio map        -> edit/audio_map.json          (RMS/breath map, local, no API cost)
  3 speaker blocks   -> edit/speaker_blocks.json      (must run before context review, see below)
  4 NG detect        -> edit/ng_candidates.json       (word-similarity restart clusters)
  4 pronunciation    -> (merged into ng_candidates.json) (낮은 ASR 신뢰도 - 발음 실수 정정 후보,
                        2026-09-29 착수: docs/미결-사항.md "발음 실수 탐지 구조적 약점")
  4 NG classify      -> edit/ng_classified.json       (Sonnet/Opus, few-shot 정적 6개 + L2 사용자
                        사례 검색 - fewshot.py, 2026-09-29)
  4 NG route         -> edit/ng.json                  (route/flag, 최대 삭제)
  4 filler           -> (appended to ng.json)         (standalone 음/어/아, deterministic)
  4 context review   -> edit/context_review.json     (whole-transcript recall pass)
  4 assemble draft   -> edit/draft_cuts.json          (merge every route=CUT item, NG+blocks)
  4 seam refine      -> edit/seams.json, edit/final_cuts.json (docs/기획/02 부분 루프 -
                        boundary snap + judge!=maker content check; replaces self_critique.py)
  4 global review    -> edit/global_review.json        (docs/기획/03 전체 루프, 최대 2라운드 -
                        PD 평가 + 시청자 평가. missed_cut을 찾으면 내부적으로 assemble+seam을
                        다시 돌리고 재평가. ng.json 역전파로 over_cut/시청자 지적도 검토 화면에 뜸)
  5 pauses           -> edit/pauses.json
  6 server           review UI; confirm writes <NAME>.fcpxml + preview.mp4 into the folder

Speaker blocks run before the NG/context-review group because whole_context_review.py reads
speaker_blocks.json to skip spans the block detector already covers - running it after would
make every coaching block get reported twice. assemble_draft.py in turn needs BOTH ng.json and
speaker_blocks.json finalized (including filler/context review's appends to ng.json), so it
and seam_refine.py run last within the NG cache group, gated on the same ng.json existence
check as everything else in that group.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import load_env, video_dir, edit_dir  # noqa: E402


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
    raw = folder / "raw.mp4"
    if not raw.exists():
        sys.exit(f"put the source video at {raw}")

    if not args.serve:
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
            tr = edit / "transcript.json"
            step("4/6 NG detect", [str(HERE / "detect_ng_candidates.py"), str(tr), "--out-dir", str(edit)])
            (edit / "transcript_candidates.json").rename(edit / "ng_candidates.json")
            step("4/7 pronunciation candidates", [str(HERE / "detect_pronunciation_candidates.py"), str(folder)])
            if args.no_llm:
                classified = edit / "ng_candidates.json"
                import json
                runs = json.loads(classified.read_text())["deleted_runs"]
                (edit / "ng_classified.json").write_text(json.dumps(runs, ensure_ascii=False))
            else:
                step("4/6 NG classify", [str(HERE / "classify_candidates.py"), str(edit / "ng_candidates.json"),
                                         "--transcript", str(tr), "--out", str(edit / "ng_classified.json"),
                                         "--prosody", str(edit / "prosody.json")])
            step("4/7 NG route", [str(HERE / "route_candidates.py"), str(edit / "ng_classified.json"),
                                  "--out", str(edit / "ng.json")])
            step("4/7 filler", [str(HERE / "detect_filler_candidates.py"), str(folder)])  # deterministic, always runs
            if not args.no_llm:
                step("4/7 context review", [str(HERE / "whole_context_review.py"), str(folder)])
                step("4/7 assemble draft", [str(HERE / "assemble_draft.py"), str(folder)])
                step("4/7 seam refine", [str(HERE / "seam_refine.py"), str(folder)])
                # global_review.py가 내부적으로 최대 2라운드 재투입(missed_cut 반영 -> 내부에서
                # assemble_draft.py/seam_refine.py를 다시 부름)까지 다 하므로 여기선 한 번만 호출
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
