"""채널 글꼴 - 인서트(docs/인서트-가이드.md 5장)에 쓰는 글꼴을 사용자 컴퓨터에 준비한다.

세 글꼴 모두 저장소 assets/fonts/에 들어 있다(프로젝트 사용, 판매 안 함 - assets/fonts/README.md).
파일이 빠져 있을 때만 공개 npm 미러 두 곳에서 같은 버전을 받아 파일 지문(sha256)을 확인한 뒤
~/.video-cut/fonts/에 둔다. 글꼴을 따로 설치하지 않은 사용자도 같은 모양이 나온다.

받지 못하면(오프라인 등) 대체 글꼴로 그리되 조용히 넘어가지 않는다 - missing()으로 화면에 알리고,
그 글꼴로 만든 인서트에는 표시가 남는다(inserts.py font_fallback).

Usage (확인용): python scripts/fonts.py   # 받고 상태 출력
"""
from __future__ import annotations
import hashlib
import sys
import threading
import time
from pathlib import Path

FONT_DIR = Path.home() / ".video-cut" / "fonts"
BUNDLED_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

# key: (파일 이름, sha256, 미러 주소들). 버전 고정 - 글꼴이 바뀌면 영상마다 모양이 달라진다
FONTS = {
    "gangwon": ("gangwonedupowerextrabolda-normal.woff",  # 강원교육튼튼체 - 얼굴 위 자막
                "a3b08f6cb6a05dd56e1b4fb8ca3cef98941eda4597f06139f4ad4f306dceb5ba",
                ["https://cdn.jsdelivr.net/npm/@noonnu/gangwon-edu-power-extra-bold-a@0.1.0/fonts/gangwonedupowerextrabolda-normal.woff",
                 "https://unpkg.com/@noonnu/gangwon-edu-power-extra-bold-a@0.1.0/fonts/gangwonedupowerextrabolda-normal.woff"]),
    "jeju": ("jeju-myeongjo-400.ttf",  # 제주명조 - 어둡게 깔고 읽어 주는 인용
             "41dfe08357bf3b57068e07a5ba3ed8d318e2b197324c1e147cb57d43e1028bf7",
             ["https://cdn.jsdelivr.net/npm/@noonnu/jeju-myeongjo@0.1.0/fonts/jeju-myeongjo-400.ttf",
              "https://unpkg.com/@noonnu/jeju-myeongjo@0.1.0/fonts/jeju-myeongjo-400.ttf"]),
    "pretendard": ("Pretendard-ExtraBold.otf",  # 프리텐다드 - 삽화 노란 글씨, 모션그래픽
                   "c35fe941b7568d52a96010561540e47f9d3948dfde66ba25bc1908233e0a40cd",
                   ["https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/public/static/Pretendard-ExtraBold.otf",
                    "https://unpkg.com/pretendard@1.3.9/dist/public/static/Pretendard-ExtraBold.otf"]),
    "pretendard_bold": ("Pretendard-Bold.otf",
                        "2e91915fab54df71cc9598ebf608b2bdb54c6fe3c066ac61dff0bc44fca71cc7",
                        ["https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/public/static/Pretendard-Bold.otf",
                         "https://unpkg.com/pretendard@1.3.9/dist/public/static/Pretendard-Bold.otf"]),
}
LABELS = {"gangwon": "강원교육튼튼체", "jeju": "제주명조", "pretendard": "프리텐다드", "pretendard_bold": "프리텐다드"}

_lock = threading.Lock()
_failed: dict[str, str] = {}  # key -> 마지막 실패 이유 (화면 안내용)
_failed_at: dict[str, float] = {}
RETRY_AFTER_SEC = 300  # 실패 직후엔 다시 받지 않는다 - 글자 크기 맞추기가 한 장에 수십 번 path()를 부른다


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def path(key: str, force: bool = False) -> Path | None:
    """글꼴 파일 경로. 없으면 받는다. 끝내 못 받으면 None. 최근에 실패했으면 force일 때만 다시 시도."""
    name, sha, urls = FONTS[key]
    if (BUNDLED_DIR / name).exists():
        return BUNDLED_DIR / name
    dest = FONT_DIR / name
    if dest.exists():
        return dest
    with _lock:
        if dest.exists():
            return dest
        if not force and time.time() - _failed_at.get(key, 0) < RETRY_AFTER_SEC:
            return None
        import requests
        reasons = []
        for url in urls:
            try:
                r = requests.get(url, timeout=60)
                r.raise_for_status()
                if _sha(r.content) != sha:
                    reasons.append(f"{url.split('/')[2]}: 파일 지문이 다름")
                    continue
                FONT_DIR.mkdir(parents=True, exist_ok=True)
                tmp = dest.with_suffix(dest.suffix + ".part")
                tmp.write_bytes(r.content)
                tmp.replace(dest)
                _failed.pop(key, None)
                return dest
            except Exception as e:
                reasons.append(f"{url.split('/')[2]}: {type(e).__name__}")
        _failed[key] = "; ".join(reasons)
        _failed_at[key] = time.time()
        print(f"[fonts] '{key}' 받기 실패 - {_failed[key]}", file=sys.stderr)
        return None


def ensure_all(force: bool = True) -> dict[str, bool]:
    return {k: path(k, force) is not None for k in FONTS}


def missing() -> list[str]:
    """아직 없는 글꼴 (받기를 시도하지 않는다 - 화면 상태 표시용)."""
    return [k for k, (name, _, _) in FONTS.items() if not ((BUNDLED_DIR / name).exists() or (FONT_DIR / name).exists())]


def missing_labels() -> list[str]:
    return sorted({LABELS[k] for k in missing()})


def last_errors() -> dict[str, str]:
    return dict(_failed)


if __name__ == "__main__":
    for k, ok in ensure_all().items():
        print(f"{'✓' if ok else '✗'} {LABELS[k]} ({FONTS[k][0]})" + ("" if ok else f" - {_failed.get(k, '')}"))
