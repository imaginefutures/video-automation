"""주제별 분할 진입점 - 완성본 하나를 강의 여러 편으로 나누는 제안까지 만든다
(docs/백로그/주제별-분할.md). 컷편집(run.py)과 완전히 분리된 작업이다.

폴더 구조:
    auto-split/<이름>/source.mp4   완성본 (필수)
    auto-split/<이름>/source.srt   자막 파일 (선택 - 있으면 전사 대신 대본으로 쓴다)

진행 상태는 work/split_status.json에 남긴다 (홈 화면 카드가 단계·실패를 보여줌). 목표 길이는
work/options.json에 저장돼 다시 시도할 때도 같은 값을 쓴다.

단계 (산출물이 이미 있으면 건너뛴다 - 다시 하려면 work/의 해당 파일을 지우거나 --redo):
    1 전사        transcribe.py        SRT가 없을 때만
    2 음향 지도    audio_map.py         경계를 문장 사이 가장 조용한 지점에 맞추는 데 사용
    3 문장        split_sentences.py
    4 구간 제안    propose_segments.py
    5 완결성 검사  check_standalone.py
    6 경계 다듬기  split_refine.py      검은 화면·장면 전환·자막 바뀜에 맞춰 자르는 시각을 프레임 단위로

Usage:
    python scripts/split_run.py <auto-split/NAME> [--min-minutes 3] [--max-minutes 10] [--no-llm] [--redo]
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from common import PROJECT_ROOT, SPLIT_DIR, is_split_project, edit_dir, migrate_work_dirs, write_json, SPLIT_SOURCE_NAME
from split_sentences import SRT_NAME

DEFAULT_MIN_MIN, DEFAULT_MAX_MIN = 3.0, 10.0


def set_status(work: Path, state: str, stage: str | None = None, error: str | None = None) -> None:
    write_json(work / "split_status.json", {"state": state, "stage": stage, "error": error, "pid": os.getpid(),
                                            "at": datetime.now().isoformat(timespec="seconds")})


def load_options(work: Path, min_min: float | None, max_min: float | None) -> tuple[float, float]:
    """CLI 인자 > 저장된 options.json > 기본값. 고른 값은 다시 저장해 재시도 때도 같게 한다."""
    p = work / "options.json"
    saved = json.loads(p.read_text()) if p.exists() else {}
    lo = min_min if min_min is not None else saved.get("min_minutes", DEFAULT_MIN_MIN)
    hi = max_min if max_min is not None else saved.get("max_minutes", DEFAULT_MAX_MIN)
    if not 0 < lo < hi:
        raise SystemExit(f"목표 길이가 올바르지 않습니다: {lo}~{hi}분")
    write_json(p, {"min_minutes": lo, "max_minutes": hi})
    return lo, hi


def resolve_folder(arg: str) -> Path:
    migrate_work_dirs()
    p = Path(arg)
    if not p.is_dir():
        p = PROJECT_ROOT / SPLIT_DIR / arg
    if not is_split_project(p):
        sys.exit(f"{p}에 {SPLIT_SOURCE_NAME}가 없습니다")
    return p.resolve()


def run(folder: Path, min_min: float | None, max_min: float | None, use_llm: bool, redo: bool) -> None:
    work = edit_dir(folder)
    min_min, max_min = load_options(work, min_min, max_min)
    if redo:
        for name in ("sentences.json", "segments.json"):
            (work / name).unlink(missing_ok=True)

    has_srt = (folder / SRT_NAME).exists()
    set_status(work, "running", "대본 준비")
    print(f"== 1 대본: {'자막 파일(' + SRT_NAME + ')' if has_srt else '전사'}")
    if not has_srt:
        from transcribe import transcribe
        transcribe(folder)

    set_status(work, "running", "음향 지도")
    print("== 2 음향 지도")
    if (work / "audio_map.json").exists():
        print("cached")
    else:
        from audio_map import compute
        compute(folder)

    set_status(work, "running", "문장 나누기")
    print("== 3 문장 나누기")
    if (work / "sentences.json").exists():
        print("cached")
    else:
        from split_sentences import build
        build(folder)

    set_status(work, "running", "구간 제안")
    print("== 4 구간 제안")
    seg_path = work / "segments.json"
    if seg_path.exists():
        print("cached")
    else:
        from propose_segments import propose
        propose(folder, min_min, max_min, use_llm=use_llm)

    set_status(work, "running", "완결성 검사")
    print("== 5 완결성 검사")
    data = json.loads(seg_path.read_text())
    if not use_llm:
        print("건너뜀 (--no-llm)")
    elif all("check" in s for s in data["segments"]):
        print("cached")
    else:
        from check_standalone import check
        check(folder)

    # 6 경계 다듬기 - 처음 화면을 열 때부터 화면 신호(검은 화면·장면·자막)에 맞춘 시각을 보여준다
    set_status(work, "running", "경계 다듬기")
    print("== 6 경계 다듬기")
    from audio_map import load_audio_map
    from split_refine import refine_all
    from split_sentences import load_sentences
    seg_data = json.loads(seg_path.read_text())
    cuts = refine_all(folder, [s["end_sent"] for s in seg_data["segments"]], load_sentences(folder)["sentences"],
                      load_audio_map(folder))
    print(", ".join(f"{e}:{c['reason']}" for e, c in cuts.items()))
    set_status(work, "done")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--min-minutes", type=float, default=None, help="기본: 저장된 값 또는 3")
    ap.add_argument("--max-minutes", type=float, default=None, help="기본: 저장된 값 또는 10")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--redo", action="store_true", help="문장·구간 제안을 다시 만든다 (전사·음향 지도는 유지)")
    args = ap.parse_args()
    folder = resolve_folder(args.folder)
    try:
        run(folder, args.min_minutes, args.max_minutes, not args.no_llm, args.redo)
    except (Exception, SystemExit) as e:  # noqa: BLE001 - 어떤 실패든 홈 카드에 원인을 남긴다
        if isinstance(e, SystemExit) and not isinstance(e.code, str) and not e.code:
            raise
        st = edit_dir(folder) / "split_status.json"
        stage = json.loads(st.read_text()).get("stage") if st.exists() else None
        set_status(edit_dir(folder), "error", stage, str(e.code if isinstance(e, SystemExit) else e) or type(e).__name__)
        raise


if __name__ == "__main__":
    main()
