"""업데이트·마이그레이션 (docs/업데이트와-마이그레이션.md): 플러그인 코드가 업데이트된 뒤에도
이미 쌓인 영상별 `edit/*.json`과 전역 `~/.video-cut/` 데이터가 깨지지 않게 한다.

버전은 `plugin.json`의 semver(기능 버전)와 분리된 **파일별 스키마 버전**이다
(`common.SCHEMA_VERSIONS`). 각 `edit/` 폴더 옆에 `.schema_versions.json` 사이드카를 두고,
`common.write_json()`이 쓸 때마다 "지금 코드가 이 파일을 쓰면 몇 버전인가"를 거기 기록한다.

이 스크립트가 하는 일은 둘뿐이다:
  1. **부트스트랩**: 사이드카가 아직 없는 폴더(이 체계를 도입하기 전부터 있던 프로젝트)는, 지금
     있는 파일들을 전부 "현재 버전과 호환됨"으로 간주하고 사이드카를 새로 만든다 - 실제로 아직
     스키마가 바뀐 적이 없으므로 깨진 게 하나도 없는 게 맞다. 이 단계에서는 아무것도 지우거나
     옮기지 않는다.
  2. **버전 비교**: 사이드카가 있으면 기록된 버전과 `CURRENT`를 비교한다. 뒤처진 파일은
     `MIGRATIONS`에 변환 함수가 있으면 그 자리에서 변환하고, 없으면(아직 한 번도 없었던 케이스)
     **삭제가 아니라 `edit/.backup/`로 옮긴다** - 이후 `run.py`의 기존 캐시 로직(파일이 없으면
     그 단계부터 다시 돈다)이 자연히 재생성을 유도한다. 비싼 단계(트랜스크립션 등)라도 스키마가
     안 바뀌었으면 손대지 않는다.

전역 `~/.video-cut/` 쪽(`prefs/`, `history.jsonl`, `cases/`)은 전부
사람이 쌓은 데이터라 "재생성"이라는 개념이 없다 - 그래서 버전이 안 맞아도 지우거나 옮기지 않고,
변환 함수가 없으면 경고만 출력하고 그대로 둔다. 원칙(`docs/서비스-개요와-철학.md`): 정정 데이터는
사람이 쌓은 것이고, 자동으로 손대지 않는다.

Usage:
    python scripts/migrate.py <videos/NAME 절대경로>   # 그 영상 폴더 + 전역 데이터 둘 다 확인
    python scripts/migrate.py --global-only            # 전역 데이터만
"""
from __future__ import annotations
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import SCHEMA_VERSIONS as CURRENT, edit_dir  # noqa: E402

GLOBAL_CURRENT: dict[str, int] = {
    "prefs": 1,
    "history": 1,
    "cases": 1,
}

# (파일명, 이전 버전, 다음 버전) -> 그 자리에서 data를 변환해 반환하는 함수. 지금은 스키마가
# 한 번도 안 바뀌어서 비어 있다 - 다음에 어떤 파일의 CURRENT를 올릴 때 여기 짝을 추가한다.
MIGRATIONS: dict[tuple[str, int, int], Callable[[dict | list], dict | list]] = {}


def _manifest_path(dir_: Path) -> Path:
    return dir_ / ".schema_versions.json"


def _read_manifest(dir_: Path) -> dict[str, int]:
    p = _manifest_path(dir_)
    return json.loads(p.read_text()) if p.exists() else {}


def _write_manifest(dir_: Path, manifest: dict[str, int]) -> None:
    _manifest_path(dir_).write_text(json.dumps(manifest, ensure_ascii=False, indent=2))


def _migrate_dir(dir_: Path, current: dict[str, int], backup_on_fail: bool) -> list[str]:
    """공유 로직: dir_ 안의 known 파일들을 current(파일명/논리명 -> 버전)에 맞춘다.
    backup_on_fail=True면 변환 못 하는 파일을 .backup/으로 옮긴다(프로젝트 캐시용).
    False면 옮기지 않고 경고만 한다(전역 사용자 데이터용 - 재생성 불가)."""
    if not dir_.exists():
        return []
    manifest_path = _manifest_path(dir_)
    msgs: list[str] = []

    if not manifest_path.exists():
        bootstrap = {}
        for name, version in current.items():
            if (dir_ / name).exists():
                bootstrap[name] = version
        if bootstrap:
            _write_manifest(dir_, bootstrap)
            msgs.append(f"{dir_}: 스키마 버전 기록을 새로 만들었습니다 (기존 파일은 전부 호환으로 간주)")
        return msgs

    manifest = _read_manifest(dir_)
    changed = False
    for name, want in current.items():
        path = dir_ / name
        if not path.exists():
            continue
        if name not in manifest:
            # 10-01 버그 수정: 매니페스트가 "생긴 뒤"에도 그 파일이 common.write_json()으로
            # 다시 써진 적이 없으면(이 버전 체계 도입 전부터 있던 파일) 매니페스트에 이름이
            # 아예 없다 - 이걸 이전 코드가 manifest.get(name, 0)으로 "v0=구버전"과 똑같이
            # 취급해서 멀쩡한 transcript.json/decisions.json(검토 진행 상태 포함) 등을
            # .backup/으로 옮겨버리는 사고가 났다(BS167, 10-01). 매니페스트가 아예 없는
            # 폴더의 부트스트랩(위 if not manifest_path.exists() 분기)과 같은 가정으로 -
            # "기록이 없다"는 "명시적으로 구버전"이 아니라 "한 번도 안 건드려서 모른다"는
            # 뜻이므로 호환으로 간주하고 매니페스트에 현재 버전으로 채워 넣는다. 진짜 구버전
            # (매니페스트에 더 낮은 숫자로 명시적으로 기록된 경우)만 아래 변환/백업 경로를 탄다.
            manifest[name] = want
            changed = True
            continue
        have = manifest[name]
        if have >= want:
            continue
        migrated = False
        for step_from in range(have, want):
            fn = MIGRATIONS.get((name, step_from, step_from + 1))
            if fn is None:
                break
            data = json.loads(path.read_text())
            path.write_text(json.dumps(fn(data), ensure_ascii=False, indent=2))
            have = step_from + 1
            migrated = True
        if have >= want:
            if migrated:
                manifest[name] = have
                changed = True
                msgs.append(f"{name}: v{manifest.get(name, 0)}로 자동 변환했습니다")
            continue
        if backup_on_fail:
            backup_dir = dir_ / ".backup"
            backup_dir.mkdir(exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            dest = backup_dir / f"{path.stem}.v{have}-{ts}{path.suffix}"
            path.rename(dest)
            manifest.pop(name, None)
            changed = True
            msgs.append(f"{name}이(가) 호환되지 않는 구버전(v{have}, 필요: v{want})이라 백업 후 제거했습니다"
                        f" ({dest}) - 다시 실행하면 해당 단계부터 재생성됩니다")
        else:
            msgs.append(f"{name}의 버전이 v{have}이고 필요한 건 v{want}인데 자동 변환 규칙이 없습니다 - "
                        f"손대지 않았습니다. 확인 필요: {path}")
    if changed:
        _write_manifest(dir_, manifest)
    return msgs


def migrate_project(folder: Path) -> list[str]:
    """`run.py`/`server.py`가 각 영상 폴더를 열기 전에 호출한다. 변환 못 하는 캐시 파일은
    백업 후 지워서 기존 "파일 없으면 그 단계부터 다시 돈다" 캐시 로직이 자연히 재생성하게 둔다."""
    return _migrate_dir(edit_dir(folder), CURRENT, backup_on_fail=True)


def migrate_global() -> list[str]:
    """`setup.py`가 환경설정 때 1회 호출한다. 사람이 쌓은 데이터라 재생성이 안 되므로, 변환
    규칙이 없으면 지우거나 옮기지 않고 경고만 한다."""
    return _migrate_dir(Path.home() / ".video-cut", GLOBAL_CURRENT, backup_on_fail=False)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?")
    ap.add_argument("--global-only", action="store_true")
    args = ap.parse_args()

    msgs: list[str] = []
    if not args.global_only:
        if not args.folder:
            sys.exit("영상 폴더 경로가 필요합니다 (또는 --global-only)")
        from common import video_dir  # noqa: E402
        msgs += migrate_project(video_dir(args.folder))
    msgs += migrate_global()

    if msgs:
        for m in msgs:
            print(f"[migrate] {m}")
    else:
        print("[migrate] 변경 없음 - 전부 최신 스키마")


if __name__ == "__main__":
    main()
