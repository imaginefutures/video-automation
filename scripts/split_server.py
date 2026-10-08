"""주제별 분할 화면 서버 (docs/백로그/주제별-분할.md S2). 컷편집 검토 서버(server.py)와 코드를 섞지 않는다.

split_run.py가 만든 work/sentences.json + work/segments.json을 읽어 web/split.html에 보여주고,
사용자가 고친 경계·제목·대본 글자는 work/split_decisions.json에 저장한다. 제안 원본
(segments.json)은 덮어쓰지 않으므로 "제안으로 되돌리기"는 split_decisions.json을 지우는 것.

편의 실제 자르는 시각(문장 사이 가장 조용한 지점)은 항상 여기서 계산한다 - 화면과 내보내기가
같은 함수(propose_segments.segments_from_ends)를 쓰게 해서 둘이 어긋나지 않게 한다.

Usage:
    python scripts/split_server.py <splits/NAME> [--port 8790] [--no-open]
"""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import threading
import webbrowser
import zipfile
from urllib.parse import parse_qs, quote, urlsplit
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from common import BRAND_OUTRO, PROJECT_ROOT, edit_dir, load_env, source_media, write_json
from audio_map import load_audio_map
from propose_segments import retitle, segments_from_ends, valid_ends
from split_export import INTRO_SEC, OUTRO_SEC, export as run_export
from split_intro import generate as generate_intro, image_file as intro_file, load_candidates as intro_candidates
from split_refine import load_cache as load_refined, refine_all
from split_run import resolve_folder
from split_sentences import load_sentences

WEB = PROJECT_ROOT / "web"


class Project:
    def __init__(self, folder: Path):
        self.folder = folder
        self.work = edit_dir(folder)
        self.media = source_media(folder)
        sdata = load_sentences(folder)
        self.source, self.duration, self.sents = sdata["source"], sdata["duration"], sdata["sentences"]
        self.proposal = json.loads((self.work / "segments.json").read_text())
        self.amap = load_audio_map(folder)
        self.decisions_path = self.work / "split_decisions.json"
        self.out = folder / "out"
        self.export_lock = threading.Lock()
        self.export_job: dict = {"running": False, "k": 0, "n": 0, "title": "", "error": None}

    # ------------------------------------------------------------------ 내보내기
    def export_info(self) -> dict | None:
        p = self.work / "export.json"
        if not p.exists():
            return None
        info = json.loads(p.read_text())
        dec_at = self.decisions().get("updated_at")
        # 내보낸 뒤에 경계·제목·대본을 또 고쳤으면 파일이 화면과 다르다
        info["stale"] = dec_at != info.get("decisions_updated_at")
        if "items" not in info:  # items가 생기기 전에 내보낸 기록 - 파일 이름으로 채운다
            mp4s = [f for f in info.get("files", []) if f.endswith(".mp4")]
            info["items"] = [{"n": k + 1, "title": f[3:-4], "duration": 0, "mp4": f, "txt": f[:-4] + ".txt"}
                             for k, f in enumerate(mp4s)]
        return info

    def start_export(self) -> None:
        with self.export_lock:
            if self.export_job["running"]:
                raise ValueError("이미 내보내는 중입니다")
            self.export_job = {"running": True, "k": 0, "n": len(self.decisions()["ends"]), "title": "", "error": None}

        def progress(k: int, n: int, title: str) -> None:
            self.export_job.update(k=k, n=n, title=title)

        def work() -> None:
            try:
                run_export(self.folder, progress)
                self.log("export")
            except Exception as e:  # noqa: BLE001 - 실패 원인을 화면에 보여준다
                err = getattr(e, "stderr", None)
                self.export_job["error"] = (err.decode(errors="replace")[-400:] if isinstance(err, bytes) and err else str(e))
            finally:
                self.export_job["running"] = False

        threading.Thread(target=work, daemon=True).start()

    def export_status(self) -> dict:
        return {**self.export_job, "export": self.export_info()}

    def out_file(self, name: str) -> Path:
        info = self.export_info() or {}
        if name not in info.get("files", []) and name != "목록.txt":
            raise ValueError("없는 파일입니다")
        return self.out / name

    def proposal_decisions(self) -> dict:
        segs = self.proposal["segments"]
        return {"ends": [s["end_sent"] for s in segs], "titles": [s.get("title", "") for s in segs], "text_edits": {}}

    def decisions(self) -> dict:
        if self.decisions_path.exists():
            return json.loads(self.decisions_path.read_text())
        return self.proposal_decisions()

    def refine_async(self, ends: list[int]) -> None:
        """새로 생긴 경계만 화면 신호로 다듬는다 - 경계 하나에 0.5초 남짓이라 저장 응답을 막지 않게 뒤에서."""
        if all(str(e) in load_refined(self.folder) for e in ends[:-1]):
            return
        threading.Thread(target=refine_all, args=(self.folder, ends, self.sents, self.amap), daemon=True).start()

    def computed(self, dec: dict) -> list[dict]:
        lo, hi = self.proposal["min_minutes"] * 60, self.proposal["max_minutes"] * 60
        segs = segments_from_ends(dec["ends"], self.sents, self.duration, self.amap, load_refined(self.folder))
        for seg, title in zip(segs, dec["titles"]):
            seg["title"] = title
            seg["length_ok"] = lo <= seg["duration"] <= hi
        return segs

    def state(self) -> dict:
        dec = self.decisions()
        self.refine_async(dec["ends"])
        issues = []
        for seg in self.proposal["segments"]:
            for it in seg.get("check", {}).get("issues", []):
                issues.append({**it, "proposal_n": seg["n"]})
        return {
            "name": self.folder.name, "source": self.source, "duration": self.duration,
            "min_minutes": self.proposal["min_minutes"], "max_minutes": self.proposal["max_minutes"],
            "method": self.proposal.get("method"), "sentences": self.sents, "issues": issues,
            "edited": self.decisions_path.exists(), "decisions": dec, "segments": self.computed(dec),
            "export": self.export_info(), "exporting": self.export_job["running"],
            "intro_candidates": intro_candidates(self.folder), "outro": BRAND_OUTRO.exists(),
            "intro_sec": INTRO_SEC, "outro_sec": OUTRO_SEC,
            # 홈 서버가 띄웠으면 그 포트를 물려받는다 (컷편집 server.py와 같은 방식)
            "home_port": int(os.environ.get("VIDEO_CUT_HOME_PORT") or 8764),
        }

    def save(self, dec: dict) -> dict:
        ends, titles = [int(e) for e in dec["ends"]], [str(t)[:80] for t in dec["titles"]]
        n = len(self.sents)
        if not valid_ends(ends, n) or ends[-1] != n - 1 or len(titles) != len(ends):
            raise ValueError("경계 목록이 올바르지 않습니다")
        edits = {str(int(k)): str(v) for k, v in (dec.get("text_edits") or {}).items()
                 if 0 <= int(k) < n and str(v).strip() and str(v) != self.sents[int(k)]["text"]}
        intros = [str(x) if x else None for x in (dec.get("intros") or [])][:len(ends)]
        intros += [None] * (len(ends) - len(intros))
        for name in intros:
            if name:
                intro_file(self.folder, name)  # 없는 파일·이상한 이름이면 ValueError
        # 사용자가 "문제 없음"으로 닫은 경계 확인 항목 - "문장번호:종류"
        dismissed = sorted({str(x) for x in (dec.get("dismissed") or []) if re.fullmatch(r"\d+:(boundary|reference)", str(x))})
        clean = {"ends": ends, "titles": titles, "text_edits": edits, "intros": intros, "dismissed": dismissed,
                 "updated_at": datetime.now().isoformat(timespec="seconds")}
        write_json(self.decisions_path, clean)
        self.log(dec.get("action", "save"))
        self.refine_async(ends)
        return clean

    def auto_titles(self, dec: dict) -> list[str]:
        """화면의 지금 상태(저장 전이어도)로 편별 대본을 만들어 제목을 다시 짓는다."""
        ends = [int(e) for e in dec["ends"]]
        n = len(self.sents)
        if not valid_ends(ends, n) or ends[-1] != n - 1:
            raise ValueError("경계 목록이 올바르지 않습니다")
        edits = {int(k): str(v) for k, v in (dec.get("text_edits") or {}).items()}
        texts, start = [], 0
        for e in ends:
            texts.append(" ".join(edits.get(i, self.sents[i]["text"]) for i in range(start, e + 1)))
            start = e + 1
        titles = retitle(self.folder, texts)
        self.log("auto_titles")
        return titles

    def make_intro(self, body: dict) -> dict:
        """화면의 지금 상태(저장 전이어도)로 k번째 편의 제목·대본을 모아 인트로 후보를 만든다."""
        dec, k = body["dec"], int(body["k"])
        ends = [int(e) for e in dec["ends"]]
        if not valid_ends(ends, len(self.sents)) or not 0 <= k < len(ends):
            raise ValueError("편 번호가 올바르지 않습니다")
        start, end = (ends[k - 1] + 1 if k else 0), ends[k]
        edits = {int(a): str(b) for a, b in (dec.get("text_edits") or {}).items()}
        text = " ".join(edits.get(i, self.sents[i]["text"]) for i in range(start, end + 1))
        entry = generate_intro(self.folder, start, end, str(dec["titles"][k] or "").strip(), text)
        self.log("intro_generate")
        return {"key": f"{start}-{end}", **entry}

    def reset(self) -> None:
        self.decisions_path.unlink(missing_ok=True)
        self.log("reset")

    def log(self, action: str) -> None:
        # 채택 기준(경계를 몇 번 고쳤나 / 확정까지 몇 분)을 영상별로 보기 위한 기록
        with (self.work / "actions.log").open("a") as f:
            f.write(json.dumps({"at": datetime.now().isoformat(timespec="seconds"), "action": action},
                               ensure_ascii=False) + "\n")


class Handler(BaseHTTPRequestHandler):
    project: Project

    def log_message(self, format, *args):  # noqa: A002 - stdlib signature
        pass

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/":
            return self._file(WEB / "split.html", "text/html; charset=utf-8")
        if path == "/api/state":
            return self._json(self.project.state())
        if path == "/media":
            return self._media()
        if path == "/api/segments":
            return self._json({"segments": self.project.computed(self.project.decisions())})
        if path == "/api/export/status":
            return self._json(self.project.export_status())
        if path == "/api/export/file":
            name = (parse_qs(urlsplit(self.path).query).get("name") or [""])[0]
            try:
                return self._download(self.project.out_file(name), name)
            except ValueError as e:
                return self._json({"error": str(e)}, 404)
        if path == "/api/export/zip":
            return self._zip()
        if path == "/api/intro/img":
            name = (parse_qs(urlsplit(self.path).query).get("f") or [""])[0]
            try:
                f = intro_file(self.project.folder, name)
            except ValueError:
                return self.send_error(404)
            return self._file(f, "image/jpeg" if f.suffix == ".jpg" else "image/png")
        if path == "/api/brand/outro":
            if not BRAND_OUTRO.exists():
                return self.send_error(404)
            return self._file(BRAND_OUTRO, "image/png")
        self.send_error(404)

    def do_POST(self):
        path = self.path.split("?")[0]
        try:
            if path == "/api/save":
                dec = self.project.save(self._body())
                return self._json({"decisions": dec, "segments": self.project.computed(dec)})
            if path == "/api/titles":
                try:
                    return self._json({"titles": self.project.auto_titles(self._body())})
                except ValueError:
                    raise
                except Exception as e:  # noqa: BLE001 - LLM·네트워크 실패는 화면에 그대로 알린다
                    return self._json({"error": f"제목을 짓지 못했습니다: {e}"}, 502)
            if path == "/api/intro/generate":
                try:
                    return self._json(self.project.make_intro(self._body()))
                except ValueError:
                    raise
                except Exception as e:  # noqa: BLE001 - LLM·이미지 API 실패는 화면에 그대로 알린다
                    return self._json({"error": f"인트로를 만들지 못했습니다: {e}"}, 502)
            if path == "/api/export":
                self.project.start_export()
                return self._json(self.project.export_status())
            if path == "/api/export/reveal":
                subprocess.run(["open", str(self.project.out)], check=False)
                return self._json({"ok": True})
            if path == "/api/reset":
                self.project.reset()
                return self._json(self.project.state())
        except (ValueError, KeyError, TypeError) as e:
            return self._json({"error": str(e)}, 400)
        self.send_error(404)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def _json(self, data, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path: Path, ctype: str):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _attach_header(self, name: str) -> str:
        return f"attachment; filename*=UTF-8''{quote(name)}"

    def _download(self, path: Path, name: str):
        size = path.stat().st_size
        self.send_response(200)
        self.send_header("Content-Type", "video/mp4" if name.endswith(".mp4") else "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(size))
        self.send_header("Content-Disposition", self._attach_header(name))
        self.end_headers()
        with open(path, "rb") as f:
            try:
                while chunk := f.read(1 << 20):
                    self.wfile.write(chunk)
            except (BrokenPipeError, ConnectionResetError, OSError):
                pass

    def _zip(self):
        """편 영상·대본 전부를 zip 하나로. 영상은 이미 압축돼 있어 저장만 하고(ZIP_STORED), 미리
        만들지 않고 바로 흘려보낸다 - 수 GB를 디스크에 한 번 더 쓰지 않게."""
        info = self.project.export_info()
        if not info:
            return self._json({"error": "아직 내보내지 않았습니다"}, 404)
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", self._attach_header(f"{self.project.folder.name}_분할.zip"))
        self.send_header("Connection", "close")
        self.end_headers()
        try:
            with zipfile.ZipFile(self.wfile, "w", zipfile.ZIP_STORED, allowZip64=True) as zf:
                for name in info["files"] + ["목록.txt"]:
                    p = self.project.out / name
                    if p.exists():
                        zf.write(p, arcname=name)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        self.close_connection = True

    def _media(self):
        """Range 지원 - 없으면 <video>가 탐색(seek)을 못 한다."""
        path = self.project.media
        size = path.stat().st_size
        rng = self.headers.get("Range")
        start, end, status = 0, size - 1, 200
        if rng and rng.startswith("bytes="):
            a, _, b = rng[6:].partition("-")
            start = int(a) if a else max(0, size - int(b))
            end = min(int(b) if (a and b) else end, size - 1)
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
                pass  # 브라우저가 다른 위치로 탐색하며 끊은 요청 - 정상


def serve(folder: Path, port: int, open_browser: bool) -> None:
    Handler.project = Project(folder)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"분할 화면: {url}   (folder: {folder})")
    if open_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--port", type=int, default=8790)
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()
    load_env()  # 제목 자동 작성(ANTHROPIC_API_KEY) - 홈 서버가 띄우면 이미 환경에 있다
    serve(resolve_folder(args.folder), args.port, not args.no_open)


if __name__ == "__main__":
    main()
