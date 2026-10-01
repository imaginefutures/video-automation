"""컷 로직을 바꾼 뒤 gold로 재검증하는 절차를 스크립트 하나로 고정한다.

**왜 이게 필요해졌나** (2026-10-01): 사람이 손으로 "route_candidates.py부터 다시 시작, 정확히
한 번씩만"(docs/기획/06-검증과-측정.md "규칙" 절)을 매번 기억해서 실행하다가, 이미 한 번
처리된 edit/ 위에 seam_refine.py/global_review.py를 또 돌려버리는 실수를 두 번 저질렀다 - 둘 다
missed_cut이 라운드마다 누적돼(GLOBAL_REVIEW_MISSED_CUT 중복) 정밀도가 가짜로 폭락하는 결과를
냈다(BS167: 0.700 -> 0.578, 재확인해보니 실제로는 0.70대 그대로). 이 스크립트는 그 절차 자체를
코드로 굳혀서, 사람이 순서를 외우거나 백업을 깜빡하지 않아도 되게 한다.

**절차** (영상마다 독립적으로, 항상 이 순서 그대로):
  1. edit/ng_classified.json이 있는지 확인(Stage 1/2 캐시 - LLM 재호출 없이 재사용)
  2. edit/ 백업
  3. route_candidates.py -> ng.json (덮어씀 - 이전에 쌓인 모든 라운드 결과 제거, 깨끗한 시작)
  4. detect_filler_candidates.py
  5. assemble_draft.py
  6. seam_refine.py
  7. global_review.py (내부에서 자체 재투입 최대 1회 포함 - 이 스크립트가 또 돌리지 않는다)
  8. eval_against_gold.py (레지스트리의 gold 경로 사용)
  9. 알려진 기준선(GOLD_BASELINE)과 비교해 표로 출력
  10. **오삭제 flag 누락이 0이 아니면 무조건 실패**(하드 게이트) - 그 외엔 경고만 하고 계속
  11. 전부 통과하면 백업 삭제, 하나라도 실패하면 백업에서 자동 복원 + 백업은 보존(조사용)

새 gold 영상을 추가하려면 GOLD_BASELINE에 경로·기준 수치만 추가하면 된다.

Usage:
    uv run python scripts/revalidate.py BS145 BS167
    uv run python scripts/revalidate.py BS145 BS167 BS183 --keep-backup
    uv run python scripts/revalidate.py BS145 --accept-baseline   # 통과하면 이 수치를 새 기준선으로 기록
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASELINE_PATH = ROOT / "docs" / "현재-설계" / "gold_baseline.json"

# 09-30/10-01 문서(검증-결과-BS145.md/BS167.md/BS183.md)에 기록된, 사람이 검토해 확정한 마지막
# 수치. 노이즈 범위(PRECISION_RECALL_TOLERANCE)는 09-30 결정-이력에서 실측된 "같은 코드로도
# ±0.04~0.048 정도 흔들림"을 근거로 한다 - 그보다 크게 벗어나면 진짜 회귀일 가능성이 높다는 뜻이지
# 그 자체가 자동 실패 사유는 아니다(이 스크립트는 안전 지표만 하드 게이트로 본다).
GOLD_VIDEOS: dict[str, dict] = {
    "BS145": {
        "gold_raw": "Reference/videos/edit/transcripts/BS145_raw.json",
        "gold_finished": "Reference/videos/edit/transcripts/BS145.json",
    },
    "BS167": {
        "gold_raw": "videos/BS167/edit/transcript.json",
        "gold_finished": "videos/BS167_final_gold/edit/transcript.json",
    },
    "BS183": {
        "gold_raw": "videos/BS183/edit/transcript.json",
        "gold_finished": "videos/BS183_final_gold/edit/transcript.json",
        # BS183은 완성본이 원본을 재배열(훅 재배치)해서 raw recall이 애초에 비교 대상이 아니다
        # (검증-결과-BS183.md). precision만 기준선과 비교한다.
        "recall_not_comparable": True,
    },
}
PRECISION_RECALL_TOLERANCE = 0.05


def step(title: str, cmd: list[str]) -> None:
    print(f"  -- {title}")
    subprocess.run([sys.executable, *cmd], check=True, cwd=HERE)


def load_baseline() -> dict:
    if BASELINE_PATH.exists():
        return json.loads(BASELINE_PATH.read_text())
    return {}


def save_baseline(baseline: dict) -> None:
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n")


def backup_edit(video_dir: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = video_dir / f"edit.backup-revalidate-{ts}"
    shutil.copytree(video_dir / "edit", backup, symlinks=True)
    return backup


def restore_edit(video_dir: Path, backup: Path) -> None:
    edit = video_dir / "edit"
    shutil.rmtree(edit)
    shutil.copytree(backup, edit, symlinks=True)


def revalidate_one(name: str, keep_backup: bool, accept_baseline: bool) -> dict:
    cfg = GOLD_VIDEOS[name]
    video_dir = ROOT / "videos" / name
    edit = video_dir / "edit"
    ng_classified = edit / "ng_classified.json"
    if not ng_classified.exists():
        sys.exit(f"{name}: edit/ng_classified.json이 없음 - Stage 1/2(detect_regions.py/"
                 f"classify_region.py)부터 먼저 실행해야 함(이 스크립트는 그 뒤부터만 재실행함)")

    print(f"\n=== {name}: 백업 ===")
    backup = backup_edit(video_dir)
    print(f"  {backup}")

    try:
        print(f"=== {name}: 클린 재실행 (route_candidates부터 정확히 한 번씩) ===")
        step("route_candidates", [str(HERE / "route_candidates.py"), str(ng_classified),
                                  "--out", str(edit / "ng.json")])
        step("filler", [str(HERE / "detect_filler_candidates.py"), str(video_dir)])
        step("assemble_draft", [str(HERE / "assemble_draft.py"), str(video_dir)])
        step("seam_refine", [str(HERE / "seam_refine.py"), str(video_dir)])
        step("global_review", [str(HERE / "global_review.py"), str(video_dir)])

        print(f"=== {name}: gold 대조 ===")
        step("eval_against_gold", [str(HERE / "eval_against_gold.py"), str(video_dir),
                                   "--gold-raw", str(ROOT / cfg["gold_raw"]),
                                   "--gold-finished", str(ROOT / cfg["gold_finished"])])

        result = json.loads((edit / "gold_eval.json").read_text())
        unflagged = result["fp_unflagged_words"]
        if unflagged > 0:
            print(f"  !! {name}: 오삭제 flag 누락 {unflagged}단어 - 안전 지표 위반, 실패 처리")
            restore_edit(video_dir, backup)
            return {"video": name, "ok": False, "reason": "unflagged_fp", "result": result}

        baseline = load_baseline().get(name)
        delta_note = ""
        if baseline:
            dp = result["precision"] - baseline["precision"]
            dr = result["recall"] - baseline["recall"]
            flags = []
            if abs(dp) > PRECISION_RECALL_TOLERANCE:
                flags.append(f"정밀도 Δ{dp:+.3f} (노이즈 범위 ±{PRECISION_RECALL_TOLERANCE} 밖)")
            if not cfg.get("recall_not_comparable") and abs(dr) > PRECISION_RECALL_TOLERANCE:
                flags.append(f"재현율 Δ{dr:+.3f} (노이즈 범위 ±{PRECISION_RECALL_TOLERANCE} 밖)")
            delta_note = "; ".join(flags) if flags else "기준선과 노이즈 범위 안"

        if accept_baseline:
            all_baselines = load_baseline()
            all_baselines[name] = {"precision": result["precision"], "recall": result["recall"],
                                   "date": datetime.now().strftime("%Y-%m-%d")}
            save_baseline(all_baselines)

        if not keep_backup:
            shutil.rmtree(backup)
        return {"video": name, "ok": True, "result": result, "baseline": baseline, "delta_note": delta_note}

    except subprocess.CalledProcessError as e:
        print(f"  !! {name}: 파이프라인 실패({e}) - 백업에서 복원")
        restore_edit(video_dir, backup)
        return {"video": name, "ok": False, "reason": "pipeline_error", "error": str(e)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("videos", nargs="+", choices=list(GOLD_VIDEOS.keys()))
    ap.add_argument("--keep-backup", action="store_true", help="통과해도 백업을 안 지움(조사용)")
    ap.add_argument("--accept-baseline", action="store_true",
                    help="통과한 수치를 새 기준선으로 gold_baseline.json에 기록")
    args = ap.parse_args()

    results = [revalidate_one(v, args.keep_backup, args.accept_baseline) for v in args.videos]

    print("\n" + "=" * 60)
    print("재검증 결과 요약")
    print("=" * 60)
    all_ok = True
    for r in results:
        if not r["ok"]:
            all_ok = False
            print(f"  ✗ {r['video']}: 실패 ({r.get('reason')})")
            continue
        res = r["result"]
        line = f"  ✓ {r['video']}: 정밀도 {res['precision']:.3f} 재현율 {res['recall']:.3f} " \
               f"오삭제 flag 누락 {res['fp_unflagged_words']}건"
        if r.get("baseline"):
            line += f" (기준선 {r['baseline']['precision']:.3f}/{r['baseline']['recall']:.3f})"
        if r.get("delta_note"):
            line += f" - {r['delta_note']}"
        print(line)
    print("=" * 60)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
