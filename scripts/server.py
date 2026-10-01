"""Local review server (PLAN.md 3.3/3.4): the one place cut decisions are made.

Serves web/index.html, the media with HTTP Range support (browser seeking), the session
data (transcript + NG items + pause plan + speaker blocks + current decisions), records
every decision to <folder>/edit/decisions.json as it happens, and on confirm writes the
FCPXML into the folder and renders preview.mp4 in the background.

Standard library only - nothing to install for the review step.

Usage:
    python scripts/server.py <videos/NAME> [--port 8765] [--no-open]
"""
from __future__ import annotations
import argparse
import copy
import getpass
import json
import mimetypes
import os
import re
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from common import load_env, video_dir, edit_dir, source_media, load_transcript, words_only, write_json
from build_edl import compute_kept_segments, BOUNDARY_PAD_SEC
from plan_pauses import PRESETS, PROTECT_SEC, recommended_keep, trim_for_keep, usable_range
from pattern_suggest import check as check_pattern, MIN_TRIGGER as PATTERN_MIN_TRIGGER
from transcript_search import search as search_transcript
import audio_map as am
import migrate
import redetect

WEB_DIR = Path(__file__).resolve().parent.parent / "web"

# ----------------------------------------------------------------------------- (removed) personalization
#
# 2026-10-01: cross-video per-user auto-apply (prefs.json 기반 _pref_action_for_case/_record_pref)
# 전면 폐기 - docs/채택하지-않은-것.md, docs/기획/04-지식-층과-학습.md 참고. 사용자의 모든
# 복원/추가삭제를 "개인 취향"으로 똑같이 취급했는데, 실제로는 상당수가 엔진이 보편적으로 틀린
# 것(접속사 삼킴 버그 사례)이라 구분이 안 됐다 - 보편적 버그가 개인 계정 통계에 조용히 흡수돼
# 묻히는 결함. 사용자 피드백은 이제 구조적 의심 탐지(docs/남은-개발.md)로만 쓴다 - 자동 라우팅은
# 바꾸지 않는다. (counting-only 절충안도 검토됐으나 기획/04 3장의 구조적 태그 기반 탐지로
# 완전히 대체하기로 함 - _record_structural_signal 참고, prefs.json 자체를 더 안 씀.)
UNDO_LIMIT = 200  # decision snapshots kept for ⌘Z (each is a few KB)

# ----------------------------------------------------------------------------- 두 관점 평가 배지
# (docs/기획/03-두-관점-평가.md 5장, docs/기획/05-검토-화면.md 3장) - global_review.py는 PD/시청자
# 지적을 구조화된 필드가 아니라 ng.json의 route_reason 텍스트에 역전파한다(세미콜론으로 이어붙인
# 로그). 카드 배지는 그 문장들 중 이 세 가지 알려진 형태만 파싱한다 - 모르는 문장은 그냥 무시되고
# (크래시 없음), 아무 것도 못 찾으면 "전체 루프가 돌았는데 이 항목은 안 걸렸다"는 뜻으로 ✓를 보여
# 준다(global_review.json 자체가 없으면 그마저도 안 보여준다 - 평가 자체가 없었던 것과 "통과"는
# 달라야 한다).
_PD_NEW_RE = re.compile(r"^전체 루프 PD 평가: (.+) \(confidence=([\d.]+)\) - 복원 후보로 자름$")
_PD_OVERCUT_RE = re.compile(r"^전체 루프 PD: 정보 손실 의심 - (.+)$")
_VIEWER_RE = re.compile(r"^전체 루프 시청자: (jump|unclear|rushed|dragging|repetition|boring) - (.+)$")
VIEWER_LABEL_KO = {"jump": "끊김", "unclear": "이해불가", "rushed": "급함",
                    "dragging": "늘어짐", "repetition": "반복", "boring": "지루함"}


def user_id() -> str:
    return os.environ.get("VIDEO_CUT_USER") or getpass.getuser()


def history_path() -> Path:
    """백로그/R1-결과-영수증.md: 확정마다 한 줄씩 쌓이는 채널 전체 기록 - 영상을 넘어서므로
    사용자 홈(~/.video-cut/)에 둔다."""
    d = Path.home() / ".video-cut"
    d.mkdir(parents=True, exist_ok=True)
    return d / "history.jsonl"


def bad_cut_reports_path() -> Path:
    """백로그/R3-신뢰-장치.md의 '오삭제 신고'가 쌓이는 곳. 정식 gold fixture 포맷은 아직
    미정이라, 지금은 나중에 그 설계가 나오면 바로 소비할 수 있을 만큼만(영상·케이스·본문·시각) 남긴다."""
    d = Path.home() / ".video-cut"
    d.mkdir(parents=True, exist_ok=True)
    return d / "reported_bad_cuts.jsonl"


# ----------------------------------------------------------------------------- session

class Session:
    def __init__(self, folder: Path):
        self.folder = folder
        self.name = folder.name
        self.edit = edit_dir(folder)
        self.media = source_media(folder)
        self.transcript = load_transcript(folder)
        self.words = words_only(self.transcript)
        self.duration = float(self.transcript.get("audio_duration_secs") or self.words[-1]["end"])
        self.ng = self._load("ng.json", [])
        pauses = self._load("pauses.json", {"presets": PRESETS, "gaps": []})
        self.pause_presets = pauses["presets"]
        self.gaps = pauses["gaps"]
        blocks = self._load("speaker_blocks.json", {"blocks": []})
        self.blocks = blocks["blocks"]
        self.structural_suspects = self._load("structural_suspects.json", {"tags": {}})
        self.decisions = self._merge_defaults(self._load("decisions.json", None))
        self.redo_stack: list[dict] = []  # popped overrides, replayable via "redo_override" - not persisted
        # Whole-decision snapshots so ⌘Z undoes the LAST decision of any kind (NG/block/range/
        # pause...), not just the last range override - see apply(). Session-only: after a
        # restart only the persisted overrides are undoable (the legacy path below).
        self.undo_snaps: list[dict] = []
        self.redo_snaps: list[dict] = []
        self.last_undo: dict | None = None
        # Live pattern-generalization suggestions (PLAN.md 12장/사용자 프로세스 #2) - session-only,
        # not persisted to decisions.json: a suggestion is a proposal about THIS session's
        # remaining queue, not a fact about the video worth remembering across restarts.
        self.suggestions: list[dict] = []
        self.suggested_cases: set[str] = set()  # ask at most once per NG case per session
        self._suggestion_seq = 0
        self.render_status = {"state": "idle"}
        self.lock = threading.Lock()
        self.probe = self._probe_media()
        self.log_path = self.edit / "actions.log"
        # Cut boundaries snap to genuinely quiet points instead of a flat pad when this is
        # present (see audio_map.choose_boundary) - None just means audio_map.py hasn't been
        # run for this video yet, in which case cut_spans() falls back to the flat pad exactly
        # like before.
        self.amap = am.load_audio_map(folder)
        # docs/기획/05-검토-화면.md 2장/3장 (두 층 큐 + PD·시청자 배지 + 번호 키 대안) - route/flag/
        # route_reason/draft_cuts/seams는 확정 전까지 바뀌지 않으므로 세션당 한 번만 계산해 캐시한다.
        self.global_review_ran = (self.edit / "global_review.json").exists()
        self._ng_to_cut_ids, self._cut_info_lost = self._load_seam_info()
        self._review_meta_cache: list[dict | None] = [self._review_meta(i, it) for i, it in enumerate(self.ng)]

    # ---- structural suspect detection (개인화 대체, docs/기획/04-지식-층과-학습.md 3장)

    def _record_structural_signal(self, i: int, action: str) -> None:
        """route_candidates.py/structural_tags.py가 이 NG 후보에 붙여둔 구조적 태그별로 사용자
        결정 방향(cut/keep)을 누적한다. 2회 이상 쌓였는데 전부 같은 방향이면 "버그일 수 있음"으로
        영수증에만 보여준다(receipt() 참고) - 이 집계는 어떤 경우에도 자동 라우팅을 바꾸지 않는다.
        개인화(_pref_action_for_case, 2026-10-01 제거)와의 결정적 차이: 여기서 쌓이는 건 사용자
        정답지가 아니라 "개발자가 봐야 할 패턴 후보"일 뿐이다."""
        if action not in ("cut", "keep") or not (0 <= i < len(self.ng)):
            return
        tags = self.ng[i].get("structural_tags") or []
        if not tags:
            return
        for tag in tags:
            bucket = self.structural_suspects["tags"].setdefault(tag, {"cut": 0, "keep": 0})
            bucket[action] = bucket.get(action, 0) + 1
        write_json(self.structural_suspects_path(), self.structural_suspects)

    def structural_suspects_path(self) -> Path:
        return self.edit / "structural_suspects.json"

    def flagged_structural_suspects(self) -> list[dict]:
        """2회 이상 쌓였고 전부 같은 방향인 태그만 - 하나라도 반대 방향이 섞이면 그냥 케이스별로
        갈리는 정상 판단이지 버그 의심이 아니다(04 문서 3.2)."""
        out = []
        for tag, counts in self.structural_suspects.get("tags", {}).items():
            cut, keep = counts.get("cut", 0), counts.get("keep", 0)
            total = cut + keep
            if total >= 2 and min(cut, keep) == 0:
                out.append({"tag": tag, "direction": "keep" if keep else "cut", "count": total})
        return out

    # ---- live pattern-generalization suggestions (PLAN.md 사용자 프로세스 LLM 적용 #2)

    def _maybe_suggest_pattern(self, case: str | None, action: str) -> None:
        """Fires once per (case) per session, the moment the user's own decisions on that
        case reach MIN_TRIGGER in the same direction. The LLM only writes the suggestion and
        picks candidates - the user still has to click accept in the UI (apply_suggestion)."""
        if not case or case in self.suggested_cases or action not in ("cut", "keep"):
            return
        triggers = []
        for i, item in enumerate(self.ng):
            clf = item.get("llm_classification") or {}
            if clf.get("case") != case:
                continue
            dec = self.decisions["ng"].get(str(i), {})
            if dec.get("by") == "user" and dec.get("action") == action:
                triggers.append(item)
        if len(triggers) < PATTERN_MIN_TRIGGER:
            return
        self.suggested_cases.add(case)  # ask at most once for this case, whatever the outcome
        candidates = []
        for i, item in enumerate(self.ng):
            clf = item.get("llm_classification") or {}
            if clf.get("case") != case or self._display_route(item) != "REVIEW":
                continue
            if self.decisions["ng"].get(str(i), {}).get("by") == "user":
                continue  # already decided by the user - not something to auto-fill
            candidates.append({**item, "id": i})
        if not candidates:
            return
        try:
            result = check_pattern(case, action, triggers, candidates)
        except Exception as e:
            print(f"pattern suggestion check failed: {e}")
            return
        if result:
            self._suggestion_seq += 1
            self.suggestions.append({
                "id": self._suggestion_seq, "case": case, "action": action,
                "rule_text": result.rule_text, "confidence": result.confidence,
                "candidate_ids": result.candidate_ids,
            })

    def apply_suggestion(self, sid: int, accept: bool) -> None:
        sug = next((s for s in self.suggestions if s["id"] == sid), None)
        if not sug:
            return
        self.suggestions.remove(sug)
        if accept:
            self.undo_snaps.append({"state": self._snapshot(), "desc": self._describe({"type": "suggestion"})})
            self.redo_snaps.clear()
            d = self.decisions
            for i in sug["candidate_ids"]:
                si = str(i)
                if d["ng"].get(si, {}).get("by") != "user":  # don't clobber a decision made meanwhile
                    d["ng"][si] = {"action": sug["action"], "by": "pattern_suggestion",
                                   "rule": sug["rule_text"], "skipped": False, "wi": self._ng_wi(i)}
            self.log("suggestion_accept", **sug)
            self.save()
        else:
            self.log("suggestion_dismiss", id=sid)

    def log(self, event: str, **detail) -> None:
        """Append-only dev trace of everything that happened in a session - both persisted
        decisions and UI-only events (playback, zoom, panel opens) that never touch
        decisions.json. One JSON object per line, newest last, safe to `tail -f`."""
        line = json.dumps({"at": datetime.now().isoformat(timespec="milliseconds"),
                           "event": event, **detail}, ensure_ascii=False)
        with open(self.log_path, "a") as f:
            f.write(line + "\n")

    def _load(self, name: str, default):
        p = self.edit / name
        return json.loads(p.read_text()) if p.exists() else default

    def _probe_media(self) -> dict:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,r_frame_rate", "-of", "json", str(self.media)],
            capture_output=True, text=True).stdout
        s = json.loads(out)["streams"][0]
        return {"width": s["width"], "height": s["height"], "frame_rate": s["r_frame_rate"]}

    def _display_route(self, item: dict) -> str:
        """Translate the 2026-09-29 max-delete route/flag pair (route: CUT/KEEP, flag:
        None/"restore") back into the review UI's original three-way AUTO_SAFE/REVIEW/KEEP
        vocabulary, so the browser and its stored decisions.json keep working unchanged while
        the pipeline itself now reasons in route+flag (docs/기획/01-처리-과정.md). A restore
        candidate IS today's REVIEW queue item; the UI redesign that shows flag-specific detail
        is separate follow-up work."""
        route = item.get("route")
        if route == "KEEP":
            return "KEEP"
        return "REVIEW" if item.get("flag") == "restore" else "AUTO_SAFE"

    # ---- docs/기획/05-검토-화면.md 2장/3장: 두 층 큐 + PD·시청자 배지 + 번호 키 대안
    #
    # global_review.py(건드리지 않음)는 PD/시청자 지적을 구조화된 필드가 아니라 ng.json의
    # route_reason에 세미콜론으로 이어붙인 문장으로 역전파한다(실제 산출물로 확인 - 09장 참고).
    # 여기서는 그 문장들 중 알려진 세 형태만 파싱하고, 모르는 문장은 조용히 무시한다.

    def _load_seam_info(self) -> tuple[dict[int, list[int]], dict[int, str]]:
        """ng.json 인덱스 -> 그 항목이 속한 final cut id들(draft_cuts.json의 sources를 거꾸로
        읽음), 그리고 cut id -> seam 판정의 info_lost(seams.json). 둘 다 "정보 손실 major" 정렬
        기준 계산에만 쓰는 읽기 전용 참고 데이터다 - seam_refine.py/global_review.py 자체는 전혀
        건드리지 않는다. 둘 중 하나라도 아직 안 돌았으면(옛 영상, 또는 처리 중) 빈 dict로 조용히
        빠진다 - 크래시하지 않는다."""
        ng_to_cuts: dict[int, list[int]] = {}
        for c in self._load("draft_cuts.json", {"cuts": []}).get("cuts", []):
            for src in c.get("sources", []):
                sid = src.get("source_id", "")
                if sid.startswith("ng["):
                    try:
                        ng_to_cuts.setdefault(int(sid[3:-1]), []).append(c["id"])
                    except ValueError:
                        pass
        info_lost: dict[int, str] = {}
        for s in self._load("seams.json", {"seams": []}).get("seams", []):
            j = s.get("judgment")
            if j and j.get("info_lost"):
                info_lost[s["cut_id"]] = j["info_lost"]
        return ng_to_cuts, info_lost

    def _worst_info_lost(self, ng_idx: int) -> str | None:
        order = {"major": 2, "minor": 1, "none": 0}
        best = None
        for cid in self._ng_to_cut_ids.get(ng_idx, []):
            lvl = self._cut_info_lost.get(cid)
            if lvl and (best is None or order.get(lvl, 0) > order.get(best, 0)):
                best = lvl
        return best

    def _split_point(self, item: dict) -> int | None:
        """A real internal pause inside this NG item's own word span, if there is one - the
        only grounded "alternative boundary" the pipeline actually gives us (seam_refine.py's
        alternatives themselves are NOT persisted beyond the one it already chose, see
        seams.json's `chosen_alt` - there is no multi-candidate list to offer). Picks the
        longest internal gap so the split lands on the most plausible phrase break; returns
        None when the item is a single word or has no internal pause, which is common (e.g. a
        lone filler "음.") - that card then simply has no numbered alternative, matching 05
        문서's "대안이 1~2개뿐일 수 있다"."""
        ws, we = item["raw_word_index_start"], item["raw_word_index_end"]
        if we - ws < 2:
            return None
        candidates = [g for g in self.gaps if ws <= g["prev_wi"] < we - 1]
        if not candidates:
            return None
        return max(candidates, key=lambda g: g["gap_end"] - g["gap_start"])["prev_wi"]

    def _review_signals(self, reason: str) -> dict:
        pd = None
        viewer = []
        for part in (reason or "").split("; "):
            m = _PD_NEW_RE.match(part)
            if m:
                pd = {"status": "new", "reason": m.group(1), "confidence": float(m.group(2))}
                continue
            m = _PD_OVERCUT_RE.match(part)
            if m:
                pd = {"status": "warn", "reason": m.group(1)}
                continue
            m = _VIEWER_RE.match(part)
            if m:
                viewer.append({"type": m.group(1), "label": VIEWER_LABEL_KO[m.group(1)], "reason": m.group(2)})
        return {"pd": pd, "viewer": viewer}

    def _review_meta(self, i: int, item: dict) -> dict | None:
        """None for anything not in the restore-candidate queue (AUTO_SAFE/KEEP) - those never
        show a card at all, so they need no layer/badge/alt computation."""
        if self._display_route(item) != "REVIEW":
            return None
        sig = self._review_signals(item.get("route_reason") or "")
        pd_badge = sig["pd"]
        if pd_badge is None and self.global_review_ran:
            pd_badge = {"status": "ok"}
        viewer_badges = sig["viewer"]
        viewer_ok = self.global_review_ran and not viewer_badges
        both_flagged = bool(pd_badge and pd_badge.get("status") == "warn") and bool(viewer_badges)
        info_lost = self._worst_info_lost(i)
        clf = item.get("llm_classification") or {}
        confidence = clf.get("confidence")
        mismatch = bool(clf.get("recommended_action")) and clf["recommended_action"] != "CUT"
        low_conf = isinstance(confidence, (int, float)) and confidence < 0.75
        # docs/기획/05-검토-화면.md 2.2절의 정렬 순위. "L2에서 자주 복원한 유형"과 "삭제 후보"
        # 두 단계는 뺐다 - 전자는 개인화 폐기(04 문서)와 경계가 애매해 피했고, 후자는 지금
        # 파이프라인에 그런 항목(기본이 KEEP인 재검토 카드)이 아예 없다(route/flag를 다 확인함) -
        # 없는 걸 있는 척 만들지 않는다(이번 작업 지시사항).
        if both_flagged:
            tier = 1
        elif info_lost == "major":
            tier = 2
        elif mismatch:
            tier = 3
        elif low_conf:
            tier = 4
        else:
            tier = 5
        # 빠른 확인 자격: 전체 루프가 실제로 돌았고 PD·시청자 둘 다 이 항목을 지적하지 않았으며,
        # 정보 손실 major가 아니고, 분류기 신뢰도도 충분하고, 판정이 엇갈리지도 않을 때만. 그 외
        # (전체 루프 미실행 포함)는 전부 판단 필요 층으로 - 평가되지 않은 항목을 안전한 쪽으로
        # 분류한다(경고 없는 복원 최우선 방지 원칙과 동일한 방향).
        is_quick = (self.global_review_ran and pd_badge is not None and pd_badge.get("status") == "ok"
                    and viewer_ok and info_lost != "major" and not mismatch and not low_conf)
        return {
            "layer": "quick" if is_quick else "judge", "tier": tier,
            "pd": pd_badge, "viewer": viewer_badges,
            "split_wi": self._split_point(item),
        }

    def _ng_status(self, i: int) -> str:
        """Python-side mirror of web/index.html's ngStatus() - used for the entry-banner estimate
        (R1), which needs a server-computed pending count before the browser has loaded S.decisions."""
        dec = self.decisions["ng"].get(str(i), {})
        if dec.get("skipped"):
            return "skipped"
        by = dec.get("by")
        if by == "pattern_suggestion":
            return "pattern"
        if by not in ("user", "gold"):  # 'gold' = 정답지 대조로 확정된 결정 (09-29, 결정-이력 참고)
            return "pending"
        return "done_cut" if dec.get("action") == "cut" else "done_keep"

    # ---- stable identity (survives a detect/route rerun, unlike array index/sequential id)
    #
    # transcript.json's word index never changes once written (transcribe.py skips re-running
    # if the file exists), so it's the one coordinate that still means the same thing after NG
    # detection, speaker-block detection or pause planning gets rerun with updated logic and
    # produces a different count/order of candidates. See _reconcile_ng/_reconcile_blocks.

    def _ng_wi(self, i: int) -> list[int]:
        item = self.ng[i]
        return [item["raw_word_index_start"], item["raw_word_index_end"]]

    def _block_wi(self, b: dict) -> list[int]:
        return [b["wi_start"], b["wi_end"]]

    def _gap_key(self, g: dict) -> str:
        """plan_pauses.py already uses this same (prev_wi, next_wi) pair internally to reuse
        LLM style labels across reruns (previous_labels()) - decisions.json should key gaps
        the same way instead of the positional g['id'], which shifts if build_gaps() finds a
        different number of gaps (SHOW_MIN/LLM_MIN tuning, audio_map changes, ...)."""
        return f"{g['prev_wi']}-{g['next_wi']}"

    def _reconcile_ng(self, saved: dict) -> None:
        """Re-anchor human ng decisions by word-index overlap when route_candidates.py/
        detect_filler_candidates.py has been rerun from scratch and ng.json's array no longer
        lines up with what this decisions.json last saw (see docstring above). A decision
        still at an index whose stored 'wi' matches the current item there is left alone -
        the common case, since within one run new items are only ever appended
        (detect_filler_candidates.py/global_review.py), never inserted/reordered."""
        saved_ng = saved.get("ng")
        if not saved_ng:
            return
        for k, v in saved_ng.items():
            i = int(k)
            if "wi" not in v and i < len(self.ng):
                v["wi"] = self._ng_wi(i)  # one-time migration - safe only up to the next rerun
        rerun_happened = any(
            int(k) >= len(self.ng) or tuple(v["wi"]) != tuple(self._ng_wi(int(k)))
            for k, v in saved_ng.items() if v.get("wi")
        ) or any(int(k) >= len(self.ng) for k in saved_ng)
        if not rerun_happened:
            return
        carried = [v for v in saved_ng.values()
                   if v.get("wi") and v.get("by") in ("user", "pattern_suggestion", "gold")]
        reconciled: dict[str, dict] = {}
        for i, item in enumerate(self.ng):
            cur_s, cur_e = item["raw_word_index_start"], item["raw_word_index_end"]
            best, best_ratio = None, 0.0
            for v in carried:
                s, e = v["wi"]
                inter = max(0, min(cur_e, e) - max(cur_s, s))
                ratio = inter / max(1, cur_e - cur_s)
                if ratio > best_ratio:
                    best, best_ratio = v, ratio
            if best and best_ratio >= 0.5:  # at least half of the new candidate was already judged
                reconciled[str(i)] = {**best, "wi": [cur_s, cur_e]}
        saved["ng"] = reconciled

    def _reconcile_blocks(self, saved: dict) -> None:
        """Same re-anchoring as _reconcile_ng, for detect_speaker_blocks.py reruns - block ids
        are assigned sequentially (id = len(blocks)) and shift the same way. wi_start/wi_end
        here are both inclusive (unlike ng's exclusive raw_word_index_end), see
        detect_speaker_blocks.py."""
        saved_blocks = saved.get("blocks")
        if not saved_blocks:
            return
        by_id = {b["id"]: b for b in self.blocks}
        for k, v in saved_blocks.items():
            bid = int(k)
            if "wi" not in v and bid in by_id:
                v["wi"] = self._block_wi(by_id[bid])
        rerun_happened = any(
            int(k) not in by_id or tuple(v["wi"]) != tuple(self._block_wi(by_id[int(k)]))
            for k, v in saved_blocks.items() if v.get("wi")
        ) or any(int(k) not in by_id for k in saved_blocks)
        if not rerun_happened:
            return
        carried = [v for v in saved_blocks.values() if v.get("wi") and v.get("decided")]
        reconciled: dict[str, dict] = {}
        for b in self.blocks:
            cur_s, cur_e = b["wi_start"], b["wi_end"]
            best, best_ratio = None, 0.0
            for v in carried:
                s, e = v["wi"]
                inter = max(0, min(cur_e, e) - max(cur_s, s) + 1)
                ratio = inter / max(1, cur_e - cur_s + 1)
                if ratio > best_ratio:
                    best, best_ratio = v, ratio
            if best and best_ratio >= 0.5:
                # the carried decision's per-line calls are keyed by the OLD block's line ids -
                # a line this block didn't have before falls back to the current proposal
                # instead of silently defaulting to "keep" (최대 삭제 원칙).
                lines = dict(best.get("lines", {}))
                for ln in b["lines"]:
                    lines.setdefault(str(ln["id"]), ln.get("proposed", "delete"))
                reconciled[str(b["id"])] = {**best, "wi": [cur_s, cur_e], "lines": lines}
        saved["blocks"] = reconciled

    def _migrate_gap_keys(self, gaps_dict: dict) -> None:
        """A decisions.json saved before gaps were keyed by (prev_wi,next_wi) used the
        positional g['id'] instead - rewrite to the stable form so pause-rhythm edits survive
        a plan_pauses.py rerun. A lone gap id (unlike ng/blocks) carries no other field to
        verify identity against, so this can only catch the unambiguous case: if the gap list
        shrank, any legacy id past the new end is unambiguously stale and dropped rather than
        guessed at. A rerun that changes gap COMPOSITION without shrinking the total count
        (e.g. SHOW_MIN tuning that drops one gap and reveals another elsewhere) can still
        silently migrate a decision onto the wrong gap - this is a known residual limitation,
        lower-stakes than ng/blocks since the worst case is a silence trim landing on an
        adjacent pause rather than a wrong keep/cut call."""
        legacy = [k for k in gaps_dict if k.lstrip("-").isdigit()]
        if legacy and max(int(k) for k in legacy) >= len(self.gaps):
            for k in legacy:
                del gaps_dict[k]
            return
        migrated = {}
        for g in self.gaps:
            stable, legacy_key = self._gap_key(g), str(g["id"])
            if stable in gaps_dict:
                migrated[stable] = gaps_dict[stable]
            elif legacy_key in gaps_dict:
                migrated[stable] = gaps_dict[legacy_key]
        gaps_dict.clear()
        gaps_dict.update(migrated)

    def _block_status(self, b: dict) -> str:
        bd = self.decisions["blocks"].get(str(b["id"]))
        if not bd:
            return "pending"
        if bd.get("skipped"):
            return "skipped"
        if not bd.get("decided"):
            return "pending"
        return "done_cut" if bd.get("approved") else "done_keep"

    def _review_estimate(self) -> dict:
        """docs/기획/05-검토-화면.md 2.3절: "검토 8건 · 예상 4분   빠른 확인 23건 (2분 릴)" - 두
        층을 따로 센다. 카드 유형별 평균 결정 시간(L2)이 아직 없어 판단 필요 카드는 20초로
        가정한다(사례가 쌓이면 history.jsonl 기반으로 바꿀 수 있다). 빠른 확인은 릴 재생 시간
        그대로(앞뒤 1.5초씩 이어붙이면 23건에 약 70초 - 같은 문서 4.3절 실측 어림값)."""
        judge_ng = sum(1 for i, it in enumerate(self.ng) if self._display_route(it) == "REVIEW"
                       and self._review_meta_cache[i]["layer"] == "judge" and self._ng_status(i) == "pending")
        quick_ng = sum(1 for i, it in enumerate(self.ng) if self._display_route(it) == "REVIEW"
                       and self._review_meta_cache[i]["layer"] == "quick" and self._ng_status(i) == "pending")
        pending = judge_ng + sum(1 for b in self.blocks if self._block_status(b) == "pending")
        return {"pending": pending, "estimated_sec": pending * 20,
                "quick_pending": quick_ng, "quick_estimated_sec": round(quick_ng * 70 / 23)}

    def _default_decisions(self) -> dict:
        ng = {}
        for i, item in enumerate(self.ng):
            wi = self._ng_wi(i)
            clf = item.get("llm_classification") or {}
            disp = self._display_route(item)
            if disp == "AUTO_SAFE":
                ng[str(i)] = {"action": "cut", "by": "auto", "skipped": False, "wi": wi}
                continue
            # REVIEW (route=CUT, flag=restore): the algorithm itself isn't sure. It starts CUT
            # (서비스-개요와-철학.md 원칙 4, 09-29 decision): the queue then only asks "restore
            # this?", so the user's job is to rescue good speech, not hunt for NGs. 2026-10-01:
            # no longer checks a per-user personalized default here - see "(removed)
            # personalization" above.
            if disp == "REVIEW":
                ng[str(i)] = {"action": "cut", "by": "auto", "skipped": False, "wi": wi}
            else:
                ng[str(i)] = {"action": "keep", "by": "auto", "skipped": False, "wi": wi}
        # speaker blocks follow the same rule: the proposed deletion starts applied
        blocks = {str(b["id"]): {"approved": True, "decided": False, "skipped": False, "wi": self._block_wi(b),
                                 "lines": {str(ln["id"]): ln.get("proposed", "delete") for ln in b["lines"]}}
                  for b in self.blocks}
        return {"ng": ng,
                "pause": {"enabled": True, "targets": {k: v["target"] for k, v in self.pause_presets.items()},
                          "gaps": {}},
                "blocks": blocks, "overrides": [], "reported_bad_cuts": [],
                "history": [], "confirmed_at": None}

    def _merge_defaults(self, saved: dict | None) -> dict:
        """A decisions.json written before a layer's output existed must not silently turn
        that layer off: fill in defaults for anything it doesn't mention, keep what it does."""
        defaults = self._default_decisions()
        if not saved:
            return defaults
        self._reconcile_ng(saved)
        self._reconcile_blocks(saved)
        for k, v in defaults["ng"].items():
            nd = saved.setdefault("ng", {}).setdefault(k, v)
            nd.setdefault("skipped", False)
            nd.setdefault("wi", v["wi"])
            # a REVIEW item still on the untouched 'auto' default follows the CURRENT default
            # (cut since 09-29) - older sessions saved it as keep; anything the user decided stays
            if nd.get("by") == "auto" and self._display_route(self.ng[int(k)]) == "REVIEW":
                nd["action"] = v["action"]
        for k, v in defaults["blocks"].items():
            bd = saved.setdefault("blocks", {}).setdefault(k, v)
            bd.setdefault("decided", False)
            bd.setdefault("skipped", False)
            bd.setdefault("wi", v["wi"])
            if not bd["decided"]:  # same for a block nobody has decided yet
                bd["approved"] = v["approved"]
        saved.setdefault("pause", defaults["pause"])
        for k, v in defaults["pause"]["targets"].items():
            saved["pause"].setdefault("targets", {}).setdefault(k, v)
        saved["pause"].setdefault("gaps", {})
        self._migrate_gap_keys(saved["pause"]["gaps"])
        saved["pause"].setdefault("enabled", True)
        for k in ("overrides", "reported_bad_cuts", "history"):
            saved.setdefault(k, [])
        saved.pop("outtakes", None)  # 2026-10-01: outtake 기능 전체 제거 (★ 버튼, 배지, 큐) - 남은
        # decisions.json에 옛 outtakes 리스트가 있어도 그냥 버린다, 안 읽는다
        for m in saved.pop("manual_cuts", []):  # pre-overrides format
            saved["overrides"].append({"op": "cut", "wi_start": m["wi_start"], "wi_end": m["wi_end"]})
        saved.setdefault("confirmed_at", None)
        return saved

    # ---- derived state

    def gap_rec(self, g: dict) -> float:
        """Recommended seconds to keep, under the CURRENT global targets."""
        return recommended_keep(g, self.decisions["pause"]["targets"])

    def gap_keep(self, g: dict) -> float:
        """Seconds actually kept: the user's value if they dragged the gauge, else the recommendation."""
        v = self.decisions["pause"]["gaps"].get(self._gap_key(g))
        if isinstance(v, (int, float)):
            return float(v)
        if v == "keep":  # legacy string: keep the whole pause
            us, ue = usable_range(g["gap_start"], g["gap_end"])
            return round(max(0.0, ue - us), 3)
        return self.gap_rec(g)

    def gap_view(self) -> list[dict]:
        out = []
        for g in self.gaps:
            us, ue = usable_range(g["gap_start"], g["gap_end"])
            out.append({"id": g["id"], "usable": round(max(0.0, ue - us), 3), "rec": self.gap_rec(g),
                        "keep": self.gap_keep(g), "user": isinstance(self.decisions["pause"]["gaps"].get(self._gap_key(g)), (int, float))})
        return out

    def cut_spans(self) -> list[dict]:
        spans = []
        d = self.decisions
        # NG is the finer-grained unit - it can sit anywhere, including inside a speaker
        # block's own DIRECTION/ATTEMPT lines. Its own decision (cut, or nothing if kept) is
        # authoritative for exactly its own words, whatever the surrounding block decides; see
        # the block loop below, which carves every NG item's span out before adding its own.
        # This used to be the other way round (block unconditionally added on top of NG), so a
        # user's own "살리기" on an NG item inside a block had no effect on the result even
        # though the sidebar card claimed it did (UX audit, 09-29 fix).
        ng_time_ranges = []
        for i, item in enumerate(self.ng):
            ng_time_ranges.append((item["start"], item["end"]))
            if d["ng"].get(str(i), {}).get("action") == "cut":
                b = am.choose_boundary(self.amap, self.words, item["raw_word_index_start"],
                                        item["raw_word_index_end"], self.duration)
                s, e = b["start"], b["end"]
                if e > s:
                    spans.append({"start": s, "end": e, "kind": "ng", "ref": f"ng:{i}",
                                  "audio_ok": b["audio_ok"], "boundary_method": b["method"]})
        if d["pause"]["enabled"]:
            for g in self.gaps:
                trim = trim_for_keep(g, self.gap_keep(g))
                if trim:
                    spans.append({**trim, "kind": "pause", "ref": f"gap:{g['id']}"})
        block_spans = []
        for b in self.blocks:
            bd = d["blocks"].get(str(b["id"]))
            if not bd or not bd["approved"]:
                continue
            for ln in b["lines"]:
                if bd["lines"].get(str(ln["id"])) == "delete":
                    bnd = am.choose_boundary(self.amap, self.words, ln["wi_start"], ln["wi_end"] + 1, self.duration)
                    s, e = bnd["start"], bnd["end"]
                    if e > s:
                        block_spans.append({"start": s, "end": e, "kind": "block", "ref": f"block:{b['id']}:{ln['id']}",
                                            "audio_ok": bnd["audio_ok"], "boundary_method": bnd["method"]})
        for s0, e0 in ng_time_ranges:
            block_spans = _subtract(block_spans, s0, e0)
        spans.extend(block_spans)
        # Range overrides from the transcript (drag -> 삭제/살리기) win over everything above,
        # in the order the user made them. A keep-override carves the words' own intervals
        # out of any span; pause trims BETWEEN those words are left alone.
        for k, ov in enumerate(d["overrides"]):
            span = self._override_span(ov)
            if not span:
                continue
            start_, end_ = span
            if ov["op"] == "cut":
                if end_ > start_:
                    spans.append({"start": start_, "end": end_, "kind": "manual", "ref": f"manual:{k}"})
            else:
                spans = _subtract(spans, start_, end_)
        spans.sort(key=lambda s: s["start"])
        merged: list[dict] = []
        for s in spans:
            if merged and s["start"] <= merged[-1]["end"]:
                merged[-1]["end"] = max(merged[-1]["end"], s["end"])
                merged[-1]["refs"].append(s["ref"])
                merged[-1]["audio_ok"] = _merge_audio_ok(merged[-1]["audio_ok"], s.get("audio_ok"))
            else:
                merged.append({"start": s["start"], "end": s["end"], "refs": [s["ref"]], "kind": s["kind"],
                               "audio_ok": s.get("audio_ok")})
        return merged

    def word_states(self) -> list[str]:
        """Per word, for the transcript colouring:
        keep · review (undecided NG candidate) · cut:ng · cut:block · cut:manual ·
        proposed:block (would be cut once the block is approved)."""
        states = ["keep"] * len(self.words)
        d = self.decisions
        ng_owned = set()  # every word that belongs to an NG item - the block loop below must
        # never touch these, whichever way that NG item's own decision goes (see cut_spans)
        for i, item in enumerate(self.ng):
            dec = d["ng"].get(str(i), {})
            if dec.get("action") == "cut":
                tag = "cut:ng"
            elif self._display_route(item) == "REVIEW" and dec.get("by") not in ("user", "pattern_suggestion"):
                tag = "review"
            else:
                tag = "keep"
            for wi in range(item["raw_word_index_start"], item["raw_word_index_end"]):
                ng_owned.add(wi)
                if tag != "keep" and states[wi] == "keep":
                    states[wi] = tag
        for b in self.blocks:
            bd = d["blocks"].get(str(b["id"]))
            if not bd:
                continue
            for ln in b["lines"]:
                if bd["lines"].get(str(ln["id"])) != "delete":
                    continue
                tag = "cut:block" if bd["approved"] else "proposed:block"
                for wi in range(ln["wi_start"], ln["wi_end"] + 1):
                    if wi in ng_owned:
                        continue  # this word's fate is its own NG item's call, not the block's
                    if tag == "proposed:block" and states[wi].startswith("cut"):
                        continue
                    states[wi] = tag
        for ov in d["overrides"]:
            tag = "cut:manual" if ov["op"] == "cut" else "keep"
            if ov.get("wi_start") is None or ov.get("wi_end") is None:
                # 정밀 삭제/복원 (a time range, no word indices): every word it covers end to
                # end changes state too - otherwise a precise cut of a whole word stayed
                # unstruck in the transcript. Words only partly covered are drawn client-side.
                span = self._override_span(ov)
                if not span:
                    continue
                s, e = span
                for wi, w in enumerate(self.words):
                    if w["start"] + BOUNDARY_PAD_SEC >= s - 0.005 and w["end"] - BOUNDARY_PAD_SEC <= e + 0.005:
                        states[wi] = tag
                continue
            for wi in range(int(ov["wi_start"]), int(ov["wi_end"]) + 1):
                states[wi] = tag
        return states

    def payload(self) -> dict:
        return {
            "name": self.name, "duration": self.duration, "media": self.probe, "user": user_id(),
            "words": [{"wi": w["wi"], "t": w["text"], "s": w["start"], "e": w["end"], "spk": w.get("speaker_id")}
                      for w in self.words],
            "ng": [{"i": i, "start": it["start"], "end": it["end"], "wi_start": it["raw_word_index_start"],
                    "wi_end": it["raw_word_index_end"], "label": it["label"], "route": self._display_route(it),
                    "route_reason": it.get("route_reason", ""), "text": it.get("deleted_text", ""),
                    "clf": it.get("llm_classification"),
                    "review": self._review_meta_cache[i]} for i, it in enumerate(self.ng)],
            "pause": {"presets": self.pause_presets, "gaps": self.gaps, "protect_sec": PROTECT_SEC,
                      "view": self.gap_view()},
            "pad_sec": BOUNDARY_PAD_SEC,
            "blocks": self.blocks,
            "decisions": self.decisions,
            "cut_spans": self.cut_spans(),
            "word_states": self.word_states(),
            "can_undo": self.can_undo(), "can_redo": self.can_redo(),
            "render": self.render_status,
            "suggestions": self.suggestions,
            "review_estimate": self._review_estimate(),
            "global_review_ran": self.global_review_ran,
        }

    # ---- mutations

    def _snapshot(self) -> dict:
        return {k: copy.deepcopy(v) for k, v in self.decisions.items() if k != "history"}

    def _restore(self, state: dict) -> None:
        history = self.decisions.get("history", [])
        self.decisions.clear()
        self.decisions.update(copy.deepcopy(state))
        self.decisions["history"] = history

    def _describe(self, msg: dict) -> dict:
        """What a decision touched, for the undo toast: a Korean label + where it is (seconds)."""
        t = msg.get("type")
        act = {"cut": "삭제", "keep": "살리기", "skip": "건너뛰기", "confirm": "검토 완료"}.get(msg.get("action") or msg.get("op"), "")
        if t == "ng":
            item = self.ng[int(msg["i"])] if 0 <= int(msg["i"]) < len(self.ng) else {}
            return {"label": f"NG {act}", "at": item.get("start")}
        if t == "block":
            b = next((b for b in self.blocks if str(b["id"]) == str(msg["block_id"])), None)
            return {"label": f"발화 블록 {act}", "at": b["lines"][0]["start"] if b and b.get("lines") else None}
        if t == "range":
            precise = msg.get("wi_start") is None
            return {"label": f"{'정밀 ' if precise else ''}{act}", "at": msg.get("start")}
        if t == "pause_gap":
            g = next((g for g in self.gaps if str(g["id"]) == str(msg["gap_id"])), None)
            return {"label": "쉼 조정", "at": g["gap_start"] if g else None}
        if t in ("pause_target", "pause_enabled"):
            return {"label": "무음 리듬 설정", "at": None}
        if t == "report_bad_cut":
            item = self.ng[int(msg["i"])] if 0 <= int(msg["i"]) < len(self.ng) else {}
            return {"label": "오삭제 신고", "at": item.get("start")}
        if t == "suggestion":
            return {"label": "패턴 적용", "at": None}
        return {"label": "편집", "at": None}

    def can_undo(self) -> bool:
        return bool(self.undo_snaps) or bool(self.decisions["overrides"])

    def can_redo(self) -> bool:
        return bool(self.redo_snaps) or bool(self.redo_stack)

    def apply(self, msg: dict) -> None:
        t = msg["type"]
        self.last_undo = None
        if t in ("undo_override", "redo_override"):
            src, dst = (self.undo_snaps, self.redo_snaps) if t == "undo_override" else (self.redo_snaps, self.undo_snaps)
            if src:
                snap = src.pop()
                dst.append({"state": self._snapshot(), "desc": snap["desc"]})
                self._restore(snap["state"])
                self.last_undo = snap["desc"]
                self.log("decision", **msg)
                self.save()
                return
            # no snapshot (e.g. after a server restart): fall back to the persisted overrides
            if t == "undo_override" and self.decisions["overrides"]:
                ov = self.decisions["overrides"][-1]
                self.last_undo = self._describe({"type": "range", **ov})
            return self._apply(msg)
        before = self._snapshot()
        self._apply(msg)
        self.undo_snaps.append({"state": before, "desc": self._describe(msg)})
        del self.undo_snaps[:-UNDO_LIMIT]
        self.redo_snaps.clear()

    def _apply(self, msg: dict) -> None:
        self.log("decision", **msg)
        d = self.decisions
        t = msg["type"]
        if t not in ("undo_override", "redo_override"):
            self.redo_stack.clear()  # any fresh action invalidates a pending redo, same as any editor
        if t == "ng":
            # 'skip' means "looked at it, decided nothing yet" - it must never touch the
            # existing action/by (which may already be a real cut/keep decision, or still the
            # untouched default), only tag it for the queue. A real cut/keep decision clears
            # that tag, since it supersedes "skipped for later".
            # 'confirm' means "whatever state this is in right now (default cut, or carved up
            # by precision range overrides) is correct - stop asking" - unlike cut/keep it never
            # rewrites `action`, so a partial 정밀 조정 edit isn't undone by leaving the queue.
            i = int(msg["i"]); action = msg["action"]
            if action == "skip":
                d["ng"][str(i)]["skipped"] = True
            elif action == "confirm":
                d["ng"][str(i)]["by"] = "user"
                d["ng"][str(i)]["skipped"] = False
                if 0 <= i < len(self.ng):
                    clf = self.ng[i].get("llm_classification") or {}
                    self._maybe_suggest_pattern(clf.get("case"), d["ng"][str(i)].get("action"))
                    self._record_structural_signal(i, d["ng"][str(i)].get("action"))
            else:
                d["ng"][str(i)] = {"action": action, "by": "user", "skipped": False, "wi": self._ng_wi(i)}
                if 0 <= i < len(self.ng):
                    clf = self.ng[i].get("llm_classification") or {}
                    self._maybe_suggest_pattern(clf.get("case"), action)
                    self._record_structural_signal(i, action)
        elif t == "pause_enabled":
            d["pause"]["enabled"] = bool(msg["enabled"])
        elif t == "pause_target":
            target = msg.get("target")
            if not isinstance(target, (int, float)) or target != target or target < 0:
                raise ValueError("목표치는 0 이상의 숫자여야 합니다")
            d["pause"]["targets"][msg["style"]] = round(float(target), 3)
        elif t == "block":
            # Same rule as ng above: 'skip' only sets the tag, never overwrites approved/decided.
            # 'confirm' leaves `approved` (and each line's proposed/delete call) exactly as-is.
            action = msg["action"]  # 'cut' | 'keep' | 'skip' | 'confirm'
            bd = d["blocks"][str(msg["block_id"])]
            if action == "skip":
                bd["skipped"] = True
            elif action == "confirm":
                bd["decided"] = True
                bd["skipped"] = False
            else:
                bd["approved"] = action == "cut"
                bd["decided"] = True
                bd["skipped"] = False
        elif t == "block_line":
            d["blocks"][str(msg["block_id"])]["lines"][str(msg["line_id"])] = msg["action"]
        elif t == "range":
            # A time range from the transcript (words and/or pause tokens). The client sends
            # start/end already padded at word edges; wi_start/wi_end are the words inside it
            # (None when only a pause was selected).
            op = msg["op"]
            start, end = float(msg["start"]), float(msg["end"])
            if op not in ("cut", "keep") or end <= start:
                raise ValueError("bad range")
            pruned = self._prune_contained(start, end)
            d["overrides"].append(self._build_range_override(op, start, end, msg.get("wi_start"), msg.get("wi_end"), pruned))
        elif t == "pause_gap":
            # keep_sec = seconds of the pause to keep (0 = delete it); null = back to the recommendation
            gap = next((g for g in self.gaps if g["id"] == int(msg["gap_id"])), None)
            if not gap:
                raise ValueError("bad gap id")
            key = self._gap_key(gap)
            v = msg.get("keep_sec")
            if v is None:
                d["pause"]["gaps"].pop(key, None)
            else:
                d["pause"]["gaps"][key] = round(max(0.0, float(v)), 3)
        elif t == "undo_override":
            if d["overrides"]:
                ov = d["overrides"].pop()
                self._revert_override(ov)
                self.redo_stack.append(ov)
        elif t == "redo_override":
            if self.redo_stack:
                prev = self.redo_stack.pop()
                # Re-derive the override (rather than replaying the stored one verbatim) so its
                # "prev" snapshot is captured fresh - valid because redo is only reachable right
                # after the matching undo, i.e. from the exact state the override originally saw.
                pruned = self._prune_contained(prev["start"], prev["end"])
                d["overrides"].append(self._build_range_override(prev["op"], prev["start"], prev["end"],
                                                                   prev.get("wi_start"), prev.get("wi_end"), pruned))
        elif t == "report_bad_cut":
            # 백로그/R3-신뢰-장치.md: 자동으로 잘못 잘렸다는 신고 - 복원 + 그 케이스를 한 단계
            # 보수적으로(평범한 살리기의 2배 가중 - 실수를 적극적으로 고친 신호라서) + 나중에
            # gold fixture로 쓸 수 있게 반례를 남긴다.
            i = int(msg["i"])
            if not (0 <= i < len(self.ng)):
                raise ValueError("bad ng index")
            item = self.ng[i]
            clf = item.get("llm_classification") or {}
            case = clf.get("case")
            d["ng"][str(i)] = {"action": "keep", "by": "user", "skipped": False, "wi": self._ng_wi(i)}
            record = {"video": self.name, "ref": f"ng:{i}", "case": case, "label": item.get("label"),
                      "text": item.get("deleted_text", ""), "route_reason": item.get("route_reason", ""),
                      "at": datetime.now().isoformat(timespec="seconds")}
            d["reported_bad_cuts"].append(record)
            self._record_structural_signal(i, "keep")
            self._record_structural_signal(i, "keep")  # 2배 가중 - 위 주석 참고
            try:
                with open(bad_cut_reports_path(), "a") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
            except OSError:
                pass
        else:
            raise ValueError(f"unknown decision type {t}")
        d["history"].append({**msg, "at": datetime.now().isoformat(timespec="seconds")})
        self.save()

    def _override_span(self, ov: dict) -> tuple[float, float] | None:
        """The [start, end] an override covers, computing it from word indices for the
        legacy word-only format that predates the start/end fields."""
        if "start" in ov:
            return ov["start"], ov["end"]
        if ov.get("wi_start") is None or ov.get("wi_end") is None:
            return None
        return (self.words[int(ov["wi_start"])]["start"] + BOUNDARY_PAD_SEC,
                self.words[int(ov["wi_end"])]["end"] - BOUNDARY_PAD_SEC)

    def _prune_contained(self, start: float, end: float) -> list[dict]:
        """Drop existing overrides fully inside the range a new one is about to cover, and
        return what was dropped. Without this, repeated fine adjustments (nudging a
        precision-zoom handle, redoing a drag) each append their own override forever -
        decisions.json grows unbounded and cut_spans()'s order-dependent replay becomes
        near-impossible to audit, even though a fully-contained older override can never
        change the final result once a later one covers the same ground. This keeps the list
        to one entry per still-meaningful edit.

        The pruned records are handed to the caller (not just discarded) so the incoming
        override can carry them in its own `prev` snapshot - otherwise a manual-only override
        (one that doesn't fully cover an ng/block item, so its only trace was this list entry)
        would be unrecoverable if the range that swallowed it is later undone: undo only
        replays what THAT override's own prev captured, which never included overrides pruned
        before it existed."""
        eps = 1e-3
        kept, pruned = [], []
        for ov in self.decisions["overrides"]:
            span = self._override_span(ov)
            if span and span[0] >= start - eps and span[1] <= end + eps:
                pruned.append(ov)  # fully superseded by the incoming override
            else:
                kept.append(ov)
        self.decisions["overrides"] = kept
        return pruned

    def _build_range_override(self, op: str, start: float, end: float, ws: int | None, we: int | None,
                               pruned: list[dict] | None = None) -> dict:
        """Apply a cut/keep range and return the override record, capturing what it overwrote
        so it can be undone (and, from that snapshot, redone) later. `pruned` is whatever
        _prune_contained just removed for this same range - carried in `prev` so undoing this
        override restores them too (see _prune_contained's docstring)."""
        d = self.decisions
        ov = {"op": op, "start": round(start, 3), "end": round(end, 3), "wi_start": ws, "wi_end": we,
              "prev": {"ng": {}, "lines": {}, "gaps": {}, "pruned": pruned or []}}
        if ws is not None and we is not None:
            # items the range fully covers are now decided by the user (drop from the review count)
            for i, item in enumerate(self.ng):
                if ws <= item["raw_word_index_start"] and item["raw_word_index_end"] - 1 <= we:
                    ov["prev"]["ng"][str(i)] = d["ng"].get(str(i))
                    d["ng"][str(i)] = {"action": op, "by": "user", "skipped": False, "wi": self._ng_wi(i)}
            for b in self.blocks:
                bd = d["blocks"][str(b["id"])]
                for ln in b["lines"]:
                    if ws <= ln["wi_start"] and ln["wi_end"] <= we:
                        key = f"{b['id']}:{ln['id']}"
                        ov["prev"]["lines"][key] = bd["lines"].get(str(ln["id"]))
                        bd["lines"][str(ln["id"])] = "delete" if op == "cut" else "keep"
        if op == "keep":  # restoring a range restores the pauses inside it in full
            for g in self.gaps:
                if start <= g["gap_start"] + 0.03 and g["gap_end"] - 0.03 <= end:
                    us, ue = usable_range(g["gap_start"], g["gap_end"])
                    key = self._gap_key(g)
                    ov["prev"]["gaps"][key] = d["pause"]["gaps"].get(key)
                    d["pause"]["gaps"][key] = round(max(0.0, ue - us), 3)
        return ov

    def _revert_override(self, ov: dict) -> None:
        d = self.decisions
        for k, v in ov.get("prev", {}).get("ng", {}).items():
            if v is None:
                d["ng"].pop(k, None)
            else:
                d["ng"][k] = v
        for key, v in ov.get("prev", {}).get("lines", {}).items():
            bid, lid = key.split(":")
            if v is None:
                d["blocks"][bid]["lines"].pop(lid, None)
            else:
                d["blocks"][bid]["lines"][lid] = v
        for k, v in ov.get("prev", {}).get("gaps", {}).items():
            if v is None:
                d["pause"]["gaps"].pop(k, None)
            else:
                d["pause"]["gaps"][k] = v
        # Restore whatever this override had pruned when it was applied (see
        # _prune_contained's docstring) - otherwise undoing this override would permanently
        # lose an older manual-only edit that had no other trace once pruned.
        pruned = ov.get("prev", {}).get("pruned")
        if pruned:
            d["overrides"].extend(pruned)

    def save(self) -> None:
        write_json(self.edit / "decisions.json", self.decisions)

    # ---- waveform (fine boundary trim: PLAN.md 미결사항 - text cut but audio remnant)

    def waveform(self, start: float, end: float, buckets: int = 320) -> dict:
        """Min/max amplitude per bucket over [start, end], decoded on demand with ffmpeg.
        No numpy: the range is a couple of seconds, so a plain struct loop is plenty fast."""
        import struct
        dur = max(0.05, end - start)
        sr = 16000  # high enough to resolve individual phoneme onsets when zoomed in tight
        proc = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(dur), "-i", str(self.media),
             "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
            capture_output=True, check=True)
        samples = struct.unpack(f"<{len(proc.stdout) // 2}h", proc.stdout)
        n = len(samples)
        peaks = []
        if n:
            per = max(1, n // buckets)
            for i in range(0, n, per):
                chunk = samples[i:i + per]
                peaks.append([min(chunk) / 32768, max(chunk) / 32768])
        return {"start": start, "end": end, "peaks": peaks}

    # ---- confirm

    def verify_boundaries(self, spans: list[dict]) -> list[dict]:
        """Final self-review, run once at confirm time on the actual spans about to ship - not
        an estimate from word timestamps like cut_spans()' choose_boundary, but the literal
        proof: render each boundary's real joined audio and re-transcribe it (Scribe). If more
        words come back than the kept context alone accounts for, a fragment of the cut phrase
        survived audibly - that's the direct cause of "확정본에 아주 일부 소리가 남아있다" bug
        reports, and unlike a raw energy threshold (tried first; false-positived on ~80% of
        BS145's ordinary mid-sentence cuts, since Korean speech rarely has a true silence gap
        at a word boundary - a loud edge there is completely normal, not evidence of anything
        left over) this only fires on cuts that actually sound wrong. Never blocks confirm -
        if a real residue is found, the fix is a human choosing a different boundary or
        restoring the phrase, not the pipeline silently cutting further into real speech
        (정상 발화 절대 보호) - it surfaces exactly which seconds to check instead."""
        api_key = os.environ.get("ELEVENLABS_API_KEY", "")
        if not api_key:
            return []
        import seam_refine
        n = seam_refine.G2_WORDS_EACH_SIDE
        # spans is sorted ascending by start (cut_spans() sorts before merging) and
        # non-overlapping, so a span's own neighbors bound how far its context can reach -
        # without this, two cut spans with little kept audio between them (10/225 pairs on
        # BS145 have under 0.5s) could pull a still-cut neighbor's words in as "expected"
        # context, which would also make render_seam_clip below splice in audio from the
        # OTHER removed span - corrupting the very check meant to catch residue.
        selections = []
        for i, s in enumerate(spans):
            floor = spans[i - 1]["end"] if i > 0 else 0.0
            ceil = spans[i + 1]["start"] if i + 1 < len(spans) else self.duration
            before_ws = [w for w in self.words if floor - 1e-3 <= w["end"] <= s["start"] + 1e-3][-n:]
            after_ws = [w for w in self.words if s["end"] - 1e-3 <= w["start"] <= ceil + 1e-3][:n]
            selections.append({"id": i, "start": s["start"], "end": s["end"],
                               "before_ws": before_ws, "after_ws": after_ws})
        results = seam_refine.g2_check(self.media, selections, api_key)
        return [{**spans[i], "note": r["note"]} for i, r in results.items() if not r["ok"]]

    # ---- R1: 결과 영수증 + history.jsonl (백로그/R1-결과-영수증.md)

    def review_started_at(self):
        """actions.log의 첫 'decision' 이벤트 시각 - 검토 시간 계산용. 결정이 하나도 없으면
        (예: 정답지 대조로 확정한 경우, 09-29 결정-이력 참고) None."""
        if not self.log_path.exists():
            return None
        for line in self.log_path.read_text().splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("event") == "decision":
                return datetime.fromisoformat(rec["at"])
        return None

    def receipt(self, spans: list[dict]) -> dict:
        """confirm() 시점의 요약 - 확정 모달과 history.jsonl 양쪽이 이 하나의 계산을 공유한다."""
        d = self.decisions
        removed = sum(s["end"] - s["start"] for s in spans)
        cuts_ng = sum(1 for v in d["ng"].values() if v.get("action") == "cut")
        cuts_pause = (sum(1 for g in self.gaps if self.gap_keep(g) < self.gap_rec(g) - 0.01)
                      if d["pause"]["enabled"] else 0)
        cuts_block = sum(1 for b in self.blocks
                         for ln in b["lines"]
                         if d["blocks"].get(str(b["id"]), {}).get("approved")
                         and d["blocks"][str(b["id"])]["lines"].get(str(ln["id"])) == "delete")
        cuts_manual = sum(1 for ov in d["overrides"] if ov["op"] == "cut")
        flagged = sum(1 for it in self.ng if self._display_route(it) == "REVIEW")
        restored = sum(1 for i, it in enumerate(self.ng) if self._display_route(it) == "REVIEW"
                       and d["ng"].get(str(i), {}).get("action") == "keep")
        # docs/기획/05-검토-화면.md 6.2절 영수증: "내 결정 복원 2/8건 · 빠른 확인 23건 통과" - 두
        # 층을 나눠서 보여준다("flagged"/"restored"는 하위 호환을 위해 전체 합으로 그대로 둔다).
        judge_flagged = sum(1 for i, it in enumerate(self.ng) if self._display_route(it) == "REVIEW"
                            and self._review_meta_cache[i]["layer"] == "judge")
        judge_restored = sum(1 for i, it in enumerate(self.ng) if self._display_route(it) == "REVIEW"
                             and self._review_meta_cache[i]["layer"] == "judge"
                             and d["ng"].get(str(i), {}).get("action") == "keep")
        quick_total = sum(1 for i, it in enumerate(self.ng) if self._display_route(it) == "REVIEW"
                          and self._review_meta_cache[i]["layer"] == "quick")
        by_counts: dict[str, int] = {}
        for v in d["ng"].values():
            by_counts[v.get("by", "auto")] = by_counts.get(v.get("by", "auto"), 0) + 1
        started = self.review_started_at()
        review_sec = None
        # by='gold'(정답지 대조 확정, 09-29 결정)가 하나라도 섞여 있으면 actions.log의 첫
        # 'decision' 이벤트는 진짜 이번 검토 세션의 시작이 아닐 수 있다(예: 예전 개발 중 테스트
        # 클릭) - 그런 시간차를 review_sec으로 잘못 보여주느니 아예 null로 둔다.
        if started and d.get("confirmed_at") and not by_counts.get("gold"):
            review_sec = round((datetime.fromisoformat(d["confirmed_at"]) - started).total_seconds())
        seams = self._load("seams.json", {"seams": []}).get("seams", [])
        seam_flag_rate = round(sum(1 for s in seams if s.get("flag")) / len(seams), 3) if seams else None
        # R8(백로그/R8-실패-대응.md) "영상당 처리 비용 추정" - scripts/common.py log_llm_usage()가
        # 6개 LLM 호출부에서 쌓은 edit/llm_usage.jsonl을 합산. --no-llm으로 돌리면 이 파일 자체가
        # 안 생기므로(기능이 아예 안 돈 것) 0이 아니라 None - seam_flag_rate와 같은 패턴.
        usage_path = self.edit / "llm_usage.jsonl"
        cost_est_usd = None
        if usage_path.exists():
            cost_est_usd = 0.0
            for line in usage_path.read_text().splitlines():
                try:
                    cost_est_usd += json.loads(line).get("cost_usd", 0) or 0
                except json.JSONDecodeError:
                    continue
            cost_est_usd = round(cost_est_usd, 4)
        return {
            "video": self.name, "confirmed_at": d.get("confirmed_at"),
            "raw_sec": round(self.duration, 1), "result_sec": round(self.duration - removed, 1),
            "cuts_ng": cuts_ng, "cuts_pause": cuts_pause, "cuts_block": cuts_block, "cuts_manual": cuts_manual,
            "flagged": flagged, "restored": restored,
            "judge_flagged": judge_flagged, "judge_restored": judge_restored, "quick_total": quick_total,
            "reported_bad_cuts": len(d.get("reported_bad_cuts", [])),
            "review_sec": review_sec, "seam_flag_rate": seam_flag_rate, "cost_est_usd": cost_est_usd,
            "decided_by": by_counts,
            # 2026-10-01: 개인화를 대체하는 구조적 의심 탐지(기획/04 3장) - 자동 라우팅엔 영향 없고
            # 영수증에만 보임. 빈 리스트가 정상(의심 패턴이 없다는 뜻).
            "structural_suspects": self.flagged_structural_suspects(),
        }

    def _last_history_entry(self, exclude_video: str | None = None) -> dict | None:
        """'지난 영상 대비' 비교용 - 채널 전체에서 가장 최근 확정, 이 영상 자신은 제외."""
        p = history_path()
        if not p.exists():
            return None
        last = None
        for line in p.read_text().splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if exclude_video and rec.get("video") == exclude_video:
                continue
            last = rec
        return last

    def confirm(self) -> dict:
        self.log("confirm")
        spans = self.cut_spans()
        boundary_warnings = self.verify_boundaries(spans)
        if boundary_warnings:
            self.log("confirm_boundary_warning", spans=boundary_warnings)
            print(f"자기 검토(G2 재전사): {len(boundary_warnings)}개 컷 경계에서 잔여음/절단 의심 - "
                  + ", ".join(f"{w['start']:.1f}s" for w in boundary_warnings))
        kept = compute_kept_segments([{"start": s["start"], "end": s["end"]} for s in spans], self.duration)
        edl = {"source_duration": self.duration, "boundary_pad_sec": BOUNDARY_PAD_SEC,
               "kept_segments": kept,
               "cut_spans": [{"start": s["start"], "end": s["end"], "n_source_runs": len(s["refs"]),
                              "refs": s["refs"], "kind": s["kind"]} for s in spans],
               "boundary_warnings": boundary_warnings,
               "markers": []}
        edl_path = self.edit / "edl.json"
        write_json(edl_path, edl)

        fcpxml_path = self.folder / f"{self.name}.fcpxml"
        num, den = self.probe["frame_rate"].split("/")
        subprocess.run([sys.executable, str(Path(__file__).parent / "export_fcpxml.py"), str(edl_path),
                        "--source", str(self.media), "--width", str(self.probe["width"]),
                        "--height", str(self.probe["height"]), "--frame-duration", f"{den}/{num}",
                        "--name", self.name, "--no-markers", "--transition-frames", "3",
                        "--out", str(fcpxml_path)], check=True)

        self.decisions["confirmed_at"] = datetime.now().isoformat(timespec="seconds")
        self.save()
        self.start_render(edl_path)
        removed = sum(s["end"] - s["start"] for s in spans)
        previous = self._last_history_entry(exclude_video=self.name)
        rc = self.receipt(spans)
        try:
            with open(history_path(), "a") as f:
                f.write(json.dumps(rc, ensure_ascii=False) + "\n")
        except OSError:
            pass
        return {"fcpxml": str(fcpxml_path), "kept_segments": len(kept), "removed_sec": round(removed, 1),
                "result_sec": round(self.duration - removed, 1), "boundary_warnings": boundary_warnings,
                "receipt": rc, "previous": previous}

    def start_render(self, edl_path: Path) -> None:
        out = self.folder / "preview.mp4"

        def run():
            self.render_status = {"state": "rendering", "started": time.time()}
            try:
                subprocess.run([sys.executable, str(Path(__file__).parent / "render_preview.py"), str(edl_path),
                                "--source", str(self.media), "--out", str(out)], check=True,
                               capture_output=True, text=True)
                self.render_status = {"state": "done", "path": str(out), "seconds": round(time.time() - self.render_status["started"])}
            except subprocess.CalledProcessError as e:
                self.render_status = {"state": "error", "detail": (e.stderr or "")[-800:]}

        threading.Thread(target=run, daemon=True).start()

def _merge_audio_ok(a: bool | None, b: bool | None) -> bool | None:
    """None means 'not audio-checked' (no audio_map, or a pause/manual span that never goes
    through choose_boundary) - that's the pre-existing baseline, not evidence of a problem, so
    it never overrides a real answer. False (a boundary that stayed loud even at its best snap)
    always wins so merging spans can't hide a bad edge behind a good neighbor's status."""
    if a is False or b is False:
        return False
    if a is True or b is True:
        return True
    return None


def _subtract(spans: list[dict], s: float, e: float) -> list[dict]:
    """Remove [s, e] from every span, splitting where needed."""
    out = []
    for sp in spans:
        if sp["end"] <= s or sp["start"] >= e:
            out.append(sp)
            continue
        if sp["start"] < s:
            out.append({**sp, "end": s})
        if sp["end"] > e:
            out.append({**sp, "start": e})
    return out


# ----------------------------------------------------------------------------- http

class Handler(BaseHTTPRequestHandler):
    session: Session | None = None  # None until transcript.json exists - see _try_build_session/serve()
    folder: Path  # set once in serve(); needed to read pipeline_status.json while session is None
    # A cut-heavy stretch makes the player seek rapidly (jump past each short cut in turn);
    # each seek aborts the in-flight /media request and opens a new one. Without a timeout, a
    # thread whose client already moved on can sit forever blocked on wfile.write() (the socket
    # never drains because nobody's reading any more), and enough of those piling up under a
    # long skip run is what left playback stuck - "playing" forever at one frozen timestamp
    # with no error anywhere (2026-09-29 fix). This bounds that: the thread gives up and frees
    # the connection instead of hanging, so a fresh request for the same range succeeds.
    timeout = 10

    def log_message(self, fmt, *args):  # quieter console: media range requests are constant noise
        if "/media" not in str(args[0] if args else ""):
            super().log_message(fmt, *args)

    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        # These never touch self.session - must work before processing has even reached
        # transcribe (R2: the server now binds and opens the browser before the pipeline
        # starts, see run.py/serve()).
        if path in ("/", "/index.html"):
            return self._file(WEB_DIR / "index.html", "text/html; charset=utf-8")
        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if path.startswith("/static/"):
            f = WEB_DIR / path[len("/static/"):]
            if f.is_file():
                return self._file(f, mimetypes.guess_type(str(f))[0] or "application/octet-stream")
            return self.send_error(404)
        if path == "/api/status":
            if self.session is not None:
                return self._json({"ready": True, "render": self.session.render_status,
                                   "cut_spans": self.session.cut_spans()})
            return self._json({"ready": False, **_pipeline_status(self.folder)})
        if self.session is None:  # everything below needs a built Session
            return self._json({"ok": False, "ready": False, "error": "아직 처리 중입니다"}, 503)
        if path == "/api/session":
            return self._json(self.session.payload())
        if path == "/media":
            return self._media()
        if path == "/api/waveform":
            from urllib.parse import urlsplit, parse_qs
            q = parse_qs(urlsplit(self.path).query)
            try:
                start = max(0.0, float(q["start"][0]))
                end = min(self.session.duration, float(q["end"][0]))
                return self._json(self.session.waveform(start, end))
            except Exception as e:
                return self._json({"error": str(e)}, 400)
        self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        if self.session is None:  # R2: every POST endpoint mutates/reads a built Session
            return self._json({"ok": False, "ready": False, "error": "아직 처리 중입니다"}, 503)
        try:
            if self.path == "/api/decision":
                with self.session.lock:
                    self.session.apply(body)
                return self._json({"ok": True, "cut_spans": self.session.cut_spans(),
                                   "word_states": self.session.word_states(), "decisions": self.session.decisions,
                                   "gap_view": self.session.gap_view(), "can_undo": self.session.can_undo(),
                                   "can_redo": self.session.can_redo(), "undone": self.session.last_undo,
                                   "suggestions": self.session.suggestions})
            if self.path == "/api/suggestion":
                with self.session.lock:
                    self.session.apply_suggestion(int(body["id"]), bool(body["accept"]))
                return self._json({"ok": True, "cut_spans": self.session.cut_spans(),
                                   "word_states": self.session.word_states(), "decisions": self.session.decisions,
                                   "can_undo": self.session.can_undo(), "can_redo": self.session.can_redo(),
                                   "suggestions": self.session.suggestions})
            if self.path == "/api/search":
                query = (body.get("query") or "").strip()
                if not query:
                    return self._json({"ok": True, "matches": []})
                matches = search_transcript(self.session.words, query)
                return self._json({"ok": True, "matches": matches})
            if self.path == "/api/confirm":
                with self.session.lock:
                    result = self.session.confirm()
                return self._json({"ok": True, **result})
            if self.path == "/api/redetect":
                # 새 모델로 다시 분석 - 사용자가 버튼으로 직접 트리거(계획과 실행 분리 원칙,
                # 자동으로는 절대 안 돎). edit/ng.json 등을 백업 후 처음부터 다시 만들고
                # Session을 새로 만든다 - Session.__init__의 _reconcile_ng()/_reconcile_blocks()가
                # 사람 결정(by=user/pattern_suggestion/gold)을 word-index 겹침으로 재배치한다.
                folder = self.session.folder
                with self.session.lock:
                    backup_dir = redetect.redetect(folder, no_llm=bool(body.get("no_llm")))
                    Handler.session = Session(folder)
                return self._json({"ok": True, "backup": str(backup_dir) if backup_dir else None,
                                   "cut_spans": self.session.cut_spans(), "word_states": self.session.word_states(),
                                   "decisions": self.session.decisions, "gap_view": self.session.gap_view(),
                                   "can_undo": self.session.can_undo(), "can_redo": self.session.can_redo(),
                                   "review_estimate": self.session._review_estimate(),
                                   "suggestions": self.session.suggestions})
            if self.path == "/api/log":
                action = body.pop("action", "ui")
                self.session.log(action, **body)
                return self._json({"ok": True})
        except Exception as e:  # surface to the UI instead of a silent 500
            return self._json({"ok": False, "error": str(e)}, 400)
        self.send_error(404)

    def _file(self, path: Path, ctype: str):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _media(self):
        """Range-aware file serving: without this the <video> element cannot seek."""
        path = self.session.media
        size = path.stat().st_size
        rng = self.headers.get("Range")
        start, end = 0, size - 1
        status = 200
        if rng and rng.startswith("bytes="):
            a, _, b = rng[6:].partition("-")
            start = int(a) if a else max(0, size - int(b))
            end = int(b) if (a and b) else end
            end = min(end, size - 1)
            status = 206
        length = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(length))
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with open(path, "rb") as f:
            f.seek(start)
            remaining = length
            try:
                while remaining > 0:
                    chunk = f.read(min(1 << 20, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
            except (BrokenPipeError, ConnectionResetError, TimeoutError, OSError):
                pass  # client already seeked elsewhere and abandoned this request - expected, not an error


def _try_build_session(folder: Path) -> Session | None:
    """None (never raises) until transcript.json exists AND Session() actually succeeds -
    covers both "pipeline hasn't reached transcribe yet" and "transcript.json is still being
    written" (a half-written file fails json.loads, same as missing). Every later-stage file
    (ng.json, pauses.json, ...) already has a safe default inside Session._load(), so this is
    the ONE real gate - see docs/백로그/R2-시작-마찰-제거.md."""
    if not (folder / "edit" / "transcript.json").exists():
        return None
    try:
        return Session(folder)
    except Exception as e:
        print(f"[server] {folder.name}: session not ready yet ({e})")
        return None


def _pipeline_status(folder: Path) -> dict:
    """Read-only progress readout written by run.py's step() after every pipeline stage - see
    run.py's `step()` and docstring there. Missing/unreadable file just means "processing
    hasn't written a status yet" (e.g. still in clean_media/transcribe), not an error."""
    p = folder / "edit" / "pipeline_status.json"
    default = {"stage": "처리 준비 중", "done": 0, "total": 0, "state": "running", "error": None, "stages": []}
    if not p.exists():
        return default
    try:
        data = json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return default
    return {"stage": data.get("stage", default["stage"]), "done": data.get("done", 0),
            "total": data.get("total", 0), "state": data.get("state", "running"),
            "error": data.get("error"), "stages": data.get("stages", [])}


def _session_watcher(folder: Path, interval: float = 1.0) -> None:
    """Background thread (R2): the server binds and answers requests immediately even when
    transcript.json doesn't exist yet (run.py now launches this server before the pipeline
    runs, not after - see run.py). This retries Session construction every `interval` seconds
    and swaps it into Handler.session the moment it succeeds, so every in-flight request before
    that either saw the static shell or a 503, and nothing crashes on an AttributeError."""
    while Handler.session is None:
        time.sleep(interval)
        sess = _try_build_session(folder)
        if sess is not None:
            Handler.session = sess
            print(f"[server] {folder.name}: session ready")
            return


def serve(folder: Path, port: int = 8765, open_browser: bool = True) -> None:
    for msg in migrate.migrate_project(folder):  # run.py도 호출하지만, server.py 단독 실행 대비
        print(f"[migrate] {msg}")
    Handler.folder = folder
    Handler.session = _try_build_session(folder)
    if Handler.session is None:
        print(f"[server] {folder.name}: still processing - serving progress view until transcript.json appears")
        threading.Thread(target=_session_watcher, args=(folder,), daemon=True).start()
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"review UI: {url}   (folder: {folder})")
    if open_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()
    load_env()  # ANTHROPIC_API_KEY for the pattern-suggestion and search endpoints (12장)
    serve(video_dir(args.folder), args.port, not args.no_open)


if __name__ == "__main__":
    main()
