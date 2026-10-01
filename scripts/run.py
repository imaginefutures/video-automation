"""video-cut orchestrator: raw.mp4 in a folder -> review UI in the browser -> FCPXML.

    python scripts/run.py <videos/NAME>            # full pipeline, then opens the review UI
    python scripts/run.py <videos/NAME> --serve    # skip processing, just open the UI
    python scripts/run.py <videos/NAME> --no-llm   # deterministic layers only (no API cost)
    python scripts/run.py                          # no folder: auto-detect a loose mp4 dropped
                                                    # straight into videos/ and create its project
                                                    # folder (백로그/R2-시작-마찰-제거.md)

A project folder's raw.mp4 can also be several split-recording segments (e.g. 01_intro.mp4,
02_main.mp4) instead of one file - run.py concats them in name order before step 0 if raw.mp4
is missing (같은 백로그, "여러 파일 분할 촬영 지원").

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
from common import load_env, ensure_api_keys, video_dir, edit_dir, write_json, PROJECT_ROOT  # noqa: E402
import migrate  # noqa: E402

# ----------------------------------------------------------------------------- R2: 처리 중 진행 화면
# (백로그/R2-시작-마찰-제거.md) - step()이 매 단계 끝에 edit/pipeline_status.json을 써서,
# 아직 transcript.json이 없어 Session을 못 만드는 server.py가 /api/status로 이 파일을 읽어
# 진행률을 보여줄 수 있게 한다. _PIPELINE_TOTAL_STEPS는 전체 파이프라인(LLM 포함, 캐시 없음)의
# step() 호출 지점 개수를 어림잡은 것 - --no-llm이나 캐시로 일부가 스킵되면 done이 total에 못
# 미치고 끝날 수 있는데, 어차피 사람이 보는 진행률 표시일 뿐 run.py 자신은 이 파일을 다시
# 읽지 않으므로 상관없다.
_PIPELINE_TOTAL_STEPS = 13
_pipeline_done = 0


def _write_pipeline_status(folder: Path, stage: str, state: str, error: str | None = None) -> None:
    """Best-effort only - a failed write here must never fail the pipeline itself."""
    try:
        write_json(edit_dir(folder) / "pipeline_status.json",
                   {"stage": stage, "done": _pipeline_done, "total": _PIPELINE_TOTAL_STEPS,
                    "state": state, "error": error})
    except OSError:
        pass


def step(title: str, cmd: list[str], folder: Path | None = None, *, llm_fallback: bool = False) -> None:
    """한 파이프라인 단계를 돈다. 실패하면(백로그/R8-실패-대응.md) 흔한 원인과 "캐시돼 있으니
    원인 해결 후 같은 명령으로 다시 실행하면 이 단계부터 이어서 진행된다"는 안내를 더해 다시
    던진다. `folder`가 주어지면 (R2) edit/pipeline_status.json에 진행률을 남긴다 - 서버가 이미
    처리 시작과 동시에 떠서 그 진행 화면이 이걸 읽는다.

    `llm_fallback=True`는 이 단계에 LLM 호출이 들어있고 `--no-llm` 결정론적 경로가 있다는
    뜻(Stage 1/2, 화자 블록) - 이미 `--no-llm`으로 도는 게 아니면 실패 시 자동으로 그걸 붙여
    한 번 더 시도한다. "검토는 항상 가능해야 한다"는 방침 - LLM이 막혀도 파이프라인 자체가
    멈추지 않는다."""
    global _pipeline_done
    print(f"\n== {title}")
    try:
        subprocess.run([sys.executable, *cmd], check=True, cwd=HERE.parent)
    except subprocess.CalledProcessError as e:
        if not llm_fallback or "--no-llm" in cmd:
            print(f"\n[실패] {title} - 위 에러 메시지가 원인입니다(API 키 만료, 네트워크 오류, "
                  f"ffmpeg 문제가 흔함). 각 단계는 결과 파일로 캐시되므로, 원인을 해결한 뒤 "
                  f"같은 명령으로 다시 실행하면 이 단계부터 이어서 진행됩니다.")
            if folder is not None:
                _write_pipeline_status(folder, title, "error", str(e))
            raise
        print(f"\n[자동 대체] {title} - LLM 호출이 실패한 것으로 보여 결정론적 모드(--no-llm)로 "
              f"다시 시도합니다. 검토 항목이 평소보다 많을 수 있습니다.")
        subprocess.run([sys.executable, *cmd, "--no-llm"], check=True, cwd=HERE.parent)
    _pipeline_done += 1
    if folder is not None:
        _write_pipeline_status(folder, title, "running")


def start_server(folder: Path, port: int, no_open: bool) -> subprocess.Popen:
    """R2: launch the review server right away, before the pipeline runs, instead of at the
    very end - the browser opens immediately and shows a progress view (web/index.html polling
    /api/status) until transcript.json exists, then the normal review UI as soon as it does.
    Detached (own session, own stdout/stderr) so Ctrl+C'ing this script, or it simply exiting
    once the pipeline finishes, doesn't take the server down with it - the browser tab stays
    open against this same server process for the rest of the review (백로그/
    R2-시작-마찰-제거.md). `--serve`의 기존 동기 실행 경로는 이 함수와 무관하게 그대로 둔다."""
    log = open(edit_dir(folder) / "server.log", "a")
    return subprocess.Popen(
        [sys.executable, str(HERE / "server.py"), str(folder), "--port", str(port),
         *(["--no-open"] if no_open else [])],
        cwd=HERE.parent, stdout=log, stderr=log, start_new_session=True)


def auto_create_project(videos_root: Path) -> Path | None:
    """백로그/R2-시작-마찰-제거.md 2순위: `videos/` 바로 아래(하위 폴더 아님)에 이름 상관없이
    mp4 하나를 던져놓고 폴더 인자 없이 부르면, 그 파일 이름으로 프로젝트 폴더를 만들고
    `raw.mp4`로 옮긴 뒤 그 폴더를 반환한다. 여러 개면 어느 걸 하나의 영상으로 봐야 할지
    애매하므로(분할 촬영일 수도, 서로 다른 영상일 수도) 추측하지 않고 사용자에게 정리를
    요청한다 - 조용히 잘못 묶는 것보다 안전하다."""
    loose = sorted(p for p in videos_root.glob("*.mp4") if p.is_file())
    if not loose:
        return None
    if len(loose) > 1:
        names = ", ".join(p.name for p in loose)
        sys.exit(f"videos/ 바로 아래에 영상이 여러 개 있습니다({names}) - 폴더를 자동으로 "
                 f"만들 수 없음. 한 영상이면 videos/<이름>/raw.mp4로, 분할 촬영이면 "
                 f"videos/<이름>/ 폴더를 만들어 그 안에 01_, 02_... 순서로 넣어주세요.")
    src = loose[0]
    name = src.stem
    folder = videos_root / name
    folder.mkdir(exist_ok=True)
    dest = folder / "raw.mp4"
    if dest.exists():
        sys.exit(f"videos/{name}/raw.mp4가 이미 있어서 videos/{src.name}을 자동으로 옮길 "
                 f"수 없음 - 직접 정리해주세요.")
    src.rename(dest)
    print(f"videos/{src.name} -> videos/{name}/raw.mp4로 옮기고 프로젝트 폴더를 만들었습니다.")
    return folder


def concat_segments(folder: Path) -> Path | None:
    """백로그/R2-시작-마찰-제거.md 2순위: `raw.mp4`가 없을 때, 폴더에 흩어진 여러 mp4(분할
    촬영 - 촬영-가이드가 허용하는 01_intro.mp4/02_main.mp4 식)를 이름 순으로 이어붙여
    `raw.mp4`로 만든다. 세그먼트가 1개 이하면 분할 촬영이 아니므로 손대지 않는다."""
    segments = sorted(p for p in folder.glob("*.mp4") if p.name != "raw.mp4")
    if len(segments) < 2:
        return None
    print(f"raw.mp4 없음 - 분할 촬영 {len(segments)}개를 이름 순으로 이어붙입니다: "
          f"{', '.join(p.name for p in segments)}")
    raw = folder / "raw.mp4"
    filelist = folder / ".concat_list.txt"
    filelist.write_text("\n".join(f"file '{p.resolve()}'" for p in segments))
    try:
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(filelist),
                        "-c", "copy", str(raw)], check=True)
    finally:
        filelist.unlink(missing_ok=True)
    print(f"wrote {raw}")
    return raw


def run_ng_pipeline(folder: Path, edit: Path, no_llm: bool = False) -> None:
    """발음 실수 후보 -> Stage 1 -> Stage 2 -> NG route -> filler -> assemble -> seam refine ->
    global review. `edit/ng.json` 캐시 게이팅은 호출하는 쪽 책임(여기선 무조건 처음부터 돈다) -
    `main()`은 `ng.json` 없을 때만 부르고, `redetect.py`(새 모델로 재분석)는 기존 산출물을
    백업해 지운 뒤 매번 이 함수를 그대로 재사용한다 - 두 경로가 서로 다른 스텝 목록으로
    갈라지지 않게 하려고 로직을 여기 한 곳에만 둔다."""
    step("4/7 pronunciation candidates", [str(HERE / "detect_pronunciation_candidates.py"), str(folder)], folder)
    step("4/7 Stage 1 (전체를 넓게)", [str(HERE / "detect_regions.py"), str(folder),
                                    *(["--no-llm"] if no_llm else [])], folder, llm_fallback=True)
    step("4/7 Stage 2 (부분을 좁게)", [str(HERE / "classify_region.py"), str(folder),
                                    *(["--no-llm"] if no_llm else [])], folder, llm_fallback=True)
    step("4/7 NG route", [str(HERE / "route_candidates.py"), str(edit / "ng_classified.json"),
                          "--out", str(edit / "ng.json")], folder)
    step("4/7 filler", [str(HERE / "detect_filler_candidates.py"), str(folder)], folder)  # deterministic, always runs
    if not no_llm:
        step("4/7 assemble draft", [str(HERE / "assemble_draft.py"), str(folder)], folder)
        step("4/7 seam refine", [str(HERE / "seam_refine.py"), str(folder)], folder)
        # global_review.py가 내부적으로 1회 재투입(missed_cut 반영 -> assemble_draft.py/
        # seam_refine.py를 한 번만 다시 부름)까지 다 하므로 여기선 한 번만 호출
        step("4/7 global review", [str(HERE / "global_review.py"), str(folder)], folder)


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
    ap.add_argument("folder", nargs="?", default=None,
                    help="videos/<이름>. 생략하면 videos/ 바로 아래 떨어진 mp4를 찾아 자동으로 폴더를 만든다")
    ap.add_argument("--serve", action="store_true", help="skip processing, open the review UI")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()

    load_env()
    if args.folder is None:
        videos_root = PROJECT_ROOT / "videos"
        folder = auto_create_project(videos_root)
        if folder is None:
            sys.exit(f"videos/ 바로 아래에 처리할 mp4가 없습니다 - videos/<이름>/raw.mp4로 넣거나, "
                     f"폴더/파일 이름을 인자로 주세요.")
    else:
        folder = video_dir(args.folder)
    edit = edit_dir(folder)
    for msg in migrate.migrate_project(folder):  # 업데이트 뒤 호환 안 되는 캐시만 조용히 정리
        print(f"[migrate] {msg}")
    raw = folder / "raw.mp4"
    if not raw.exists() and concat_segments(folder) is None:
        sys.exit(f"put the source video at {raw}")

    if args.serve:
        # 처리 과정 없음 - 기존과 동일하게 검토 화면만 동기적으로 연다
        print("\n== 6/7 review UI")
        subprocess.run([sys.executable, str(HERE / "server.py"), str(folder), "--port", str(args.port),
                        *(["--no-open"] if args.no_open else [])], cwd=HERE.parent)
        return

    # R2-시작-마찰-제거: 처리 시작과 동시에 서버를 띄우고 브라우저를 연다 - 더 이상 파이프라인이
    # 다 끝난 뒤에야 열지 않는다. 서버는 자신의 백그라운드 스레드로 transcript.json이 생기길
    # 기다리므로, 지금 당장 Session을 만들 수 없어도 바로 bind해서 진행 화면을 보여준다.
    server_proc = start_server(folder, args.port, args.no_open)
    print(f"review server pid {server_proc.pid} (detached) - http://127.0.0.1:{args.port}/")

    ensure_api_keys()  # --serve는 처리 없이 검토 화면만 여니 API 키가 필요 없음
    clean = edit / "clean.mp4"
    if not clean.exists():
        step("0/5 clean media", [str(HERE / "clean_media.py"), str(raw), "--out", str(clean)], folder)
    else:
        print("0/5 clean media: cached")

    step("1/5 transcribe", [str(HERE / "transcribe.py"), str(folder)], folder)

    if not args.no_llm and not (edit / "prosody.json").exists():
        step("2/7 prosody", [str(HERE / "prosody.py"), str(folder)], folder)
    elif not args.no_llm:
        print("2/7 prosody: cached")

    if not (edit / "audio_map.json").exists():
        step("2/7 audio map", [str(HERE / "audio_map.py"), str(folder)], folder)
    else:
        print("2/7 audio map: cached")

    if not (edit / "speaker_blocks.json").exists():
        step("3/6 speaker blocks", [str(HERE / "detect_speaker_blocks.py"), str(folder),
                                    *(["--no-llm"] if args.no_llm else [])], folder, llm_fallback=True)
    else:
        print("3/6 speaker blocks: cached")

    if not (edit / "ng.json").exists():
        run_ng_pipeline(folder, edit, args.no_llm)
    else:
        print("4/7 NG: cached")

    if not (edit / "pauses.json").exists():
        step("5/7 pauses", [str(HERE / "plan_pauses.py"), str(folder), *(["--no-llm"] if args.no_llm else [])], folder)
    else:
        print("5/7 pauses: cached")

    notify("처리 완료", f"{folder.name} 검토 준비됨")
    print(f"\n review UI: http://127.0.0.1:{args.port}/  (folder: {folder})")


if __name__ == "__main__":
    main()
