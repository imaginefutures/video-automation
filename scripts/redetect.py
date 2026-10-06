"""다시 분석 — 모델이 업데이트됐을 때 사용자가 (웹 버튼으로) 직접 트리거하는 NG 재탐지.

업데이트가 모델 교체를 포함하면(Anthropic/ElevenLabs 모델 버전이 바뀌거나, 탐지 로직 자체가
바뀌거나), 이미 분석해 둔 영상도 새 모델로 다시 돌리고 싶을 수 있다 - 하지만 자동으로는 절대
안 하고(API 비용 발생, "계획과 실행 분리" 원칙), 사용자가 웹 화면에서 명시적으로 눌러야 한다.

트랜스크립트·화자블록·무음 지도는 그대로 둔다(모델 교체와 무관한 레이어) - NG 탐지~전체 루프
블록(`run.py`의 `run_ng_pipeline()`, 코드 중복 없이 그대로 재사용)만 처음부터 다시 돈다. 기존
산출물은 지우지 않고 `edit/.redetect-backup-<timestamp>/`로 옮겨 둔다(migrate.py의 백업 원칙과
동일 - 삭제 대신 보관).

**사용자 결정 보존은 이 스크립트가 직접 구현하지 않는다.** `server.py`의
`Session._reconcile_ng()`/`_reconcile_blocks()`가 이미 "ng.json/speaker_blocks.json이 처음부터
다시 만들어졌을 때 word-index 겹침(raw_word_index_start/end)으로 사람 결정(by=user/
pattern_suggestion/gold)을 새 배열에 재배치"하는 로직을 갖고 있다 - 이 스크립트가 할 일은 그
재배치가 일어날 조건(ng.json이 통째로 새로 생김)을 만들어 주는 것뿐이고, 실제 재배치는 이
스크립트가 끝난 뒤 `Session(folder)`를 다시 만드는 쪽(웹 버튼의 서버 핸들러)이 트리거한다 -
50% 미만 겹치는 항목은 사람이 다시 봐야 하는 REVIEW로 자연히 떨어진다(그 로직도 이미 있음).

Usage:
    python scripts/redetect.py <videos/NAME> [--no-llm]
"""
from __future__ import annotations
import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import load_env, ensure_api_keys, video_dir, edit_dir  # noqa: E402
import run as run_module  # noqa: E402 - run_ng_pipeline()을 그대로 재사용, 두 경로가 갈라지지 않게

# run_ng_pipeline()이 처음부터 다시 쓰는 산출물 전부 - 하나라도 빠지면 그 단계만 옛 모델의
# 결과를 그대로 재사용하게 되어 "새 모델로 다시 분석"이 반쪽짜리가 된다.
NG_STAGE_FILES = [
    "ng_candidates.json", "regions.json", "ng_classified.json", "ng.json",
    "draft_cuts.json", "seams.json", "final_cuts.json", "global_review.json",
]


def backup_and_clear(edit: Path) -> Path | None:
    present = [edit / name for name in NG_STAGE_FILES if (edit / name).exists()]
    if not present:
        return None
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_dir = edit / f".redetect-backup-{ts}"
    backup_dir.mkdir()
    for p in present:
        shutil.move(str(p), str(backup_dir / p.name))
    return backup_dir


def redetect(folder: Path, no_llm: bool = False) -> Path | None:
    """기존 NG 단계 산출물을 백업하고 run_ng_pipeline()을 처음부터 다시 돈다. 호출 뒤에는
    반드시 `Session(folder)`를 새로 만들어야 사람 결정 재배치(_reconcile_ng)가 적용된다 -
    이 함수 자체는 server.py를 import하지 않는다(server.py는 이 스크립트를 subprocess로
    부르는 쪽이라 순환 참조가 되고, 웹 서버가 아닌 CLI 단독 실행에서는 Session을 만들 필요도
    없다)."""
    edit = edit_dir(folder)
    backup_dir = backup_and_clear(edit)
    run_module.run_ng_pipeline(folder, edit, no_llm)
    # run_ng_pipeline의 step()들이 pipeline_status.json을 running으로 남긴다 - 끝났다고 안 쓰면
    # 검토 서버를 다시 띄울 때 "처리 미완료"로 보고 검토 화면 대신 진행/오류 화면을 연다(10-06
    # server.py _try_build_session 게이트). 실패하면 step()이 error를 남기고, 그땐 진행 화면의
    # "다시 시도"(run.py가 지워진 NG 단계부터 다시 돎)가 복구 경로다.
    run_module._write_pipeline_status(folder, "재분석 완료", "done")
    return backup_dir


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--no-llm", action="store_true")
    args = ap.parse_args()

    load_env()
    folder = video_dir(args.folder)
    ensure_api_keys()
    backup_dir = redetect(folder, args.no_llm)
    if backup_dir:
        print(f"\n이전 산출물은 {backup_dir}에 보관했습니다. 검토 화면을 다시 열면(서버 재시작 또는"
              " 웹 버튼) 사람이 직접 결정했던 항목은 word-index 겹침으로 자동 재배치됩니다 - 새"
              " 분석 결과와 50% 미만 겹치는 항목만 다시 검토 대상(REVIEW)으로 남습니다.")
    else:
        print("\n기존 NG 산출물이 없어 처음 분석과 동일하게 진행했습니다.")


if __name__ == "__main__":
    main()
