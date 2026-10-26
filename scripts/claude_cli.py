"""모든 Claude 호출은 여기 한 곳을 거쳐 Claude Code CLI(`claude -p`)로 간다 - API 키 과금 대신
사용자의 Claude Code 구독으로 돈다 (10-24 사용자: "모든 것을 클로드 코드로 돌리게 해줘").

`parse()`는 예전 `anthropic.Anthropic().messages.parse()`와 같은 모양의 응답(.parsed_output, .usage,
.stop_reason)을 돌려줘서 호출부는 함수 이름만 바뀐다.

왜 이 플래그들인가 (10-24 실측):
  - 플래그 없이 부르면 사용자 설정(플러그인, MCP 연결, 메모리 등)을 통째로 실어 "2+3은?" 한 번에
    약 19만 토큰, 9초가 들었다. --safe-mode + --strict-mcp-config + --setting-sources "" +
    --system-prompt + --tools ""로 약 1,400 토큰, 4.7초가 된다. 구독 한도를 지키려면 꼭 필요하다.
  - --bare는 쓰지 않는다: --bare는 인증을 ANTHROPIC_API_KEY로만 해서 구독을 못 쓴다.
  - 이미지가 섞인 메시지는 --input-format stream-json으로 보낸다(이 형식은 출력도 stream-json이어야 한다).
  - 환경에서 ANTHROPIC_API_KEY를 지운다: 남아 있으면 CLI가 구독 대신 그 키로 과금한다.

계정 두 개 (10-26 사용자: "클로드 계정 2개를 연결하고 고르게, 한도가 차면 다른 계정으로 넘겨서 진행"):
  - 1번은 지금까지 쓰던 Claude Code 기본 로그인, 2번은 설정 폴더를 따로 둔(CLAUDE_CONFIG_DIR) 두 번째 로그인.
    설정 폴더가 다르면 로그인(macOS 키체인 항목)도 따로 잡힌다 (10-26 실측).
  - 고른 계정이 먼저, 사용량 한도("You've hit your limit"·"Usage limit reached"·429)나 로그인 풀림이면
    다른 계정으로 같은 요청을 다시 보낸다. 한도에 걸린 계정은 LIMIT_WAIT 동안 건너뛴다.
"""
from __future__ import annotations
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

CLAUDE_BIN = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")

# 이 키들이 환경에 있으면 CLI가 구독 대신 API로 과금한다
_BILLING_ENV = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")

ACCOUNTS = ("1", "2")
ACCOUNT_DIR = Path.home() / ".video-cut" / "claude-accounts"   # 2번 계정의 Claude Code 설정 폴더
PREFS = Path.home() / ".video-cut" / "prefs" / "claude_account.json"   # {"active": "1", "limited": {"1": 만료 시각}}
# 풀리는 시각이 문구마다 제각각(5시간·주간)이라 읽지 않고 한 시간 뒤 다시 시도한다 - 아직이면 또 넘어갈 뿐
LIMIT_WAIT = 3600
_LIMIT_RE = re.compile(r"hit your|usage limit|(session|weekly|opus|sonnet|fable|5-hour|daily|monthly) limit|rate_limit_error", re.I)
_AUTH_RE = re.compile(r"not logged in|please run /login|oauth token|authentication_error", re.I)


class ClaudeCLIError(RuntimeError):
    pass


class AccountUnavailable(ClaudeCLIError):
    """이 계정으로는 못 돈다 (한도·로그인) - 다른 계정으로 넘긴다."""
    def __init__(self, msg: str, limited: bool):
        super().__init__(msg)
        self.limited = limited


def _env(account: str) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in _BILLING_ENV}
    if account != "1":
        env["CLAUDE_CONFIG_DIR"] = str(ACCOUNT_DIR / account)
    return env


def _prefs() -> dict:
    try:
        p = json.loads(PREFS.read_text())
    except (OSError, ValueError):
        p = {}
    active = p.get("active") if p.get("active") in ACCOUNTS else "1"
    return {"active": active, "limited": dict(p.get("limited") or {})}


def _save_prefs(p: dict) -> None:
    PREFS.parent.mkdir(parents=True, exist_ok=True)
    tmp = PREFS.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(p, ensure_ascii=False, indent=2))
    tmp.replace(PREFS)


def _set_limited(account: str, until: float | None) -> None:
    p = _prefs()
    if until:
        p["limited"][account] = until
    elif p["limited"].pop(account, None) is None:
        return
    _save_prefs(p)


def set_active(account: str) -> None:
    if account not in ACCOUNTS:
        raise ValueError("없는 계정입니다")
    p = _prefs()
    p["active"] = account
    _save_prefs(p)


def _configured(account: str) -> bool:
    """2번은 로그인을 한 번이라도 시작해야 설정 폴더가 생긴다 - 없으면 넘길 곳으로 치지 않는다."""
    return account == "1" or (ACCOUNT_DIR / account).is_dir()


def _order() -> list[str]:
    """고른 계정 먼저. 한도에 걸린 계정은 뒤로 미루되, 다 걸렸으면 그래도 순서대로 다시 해 본다."""
    p, now = _prefs(), time.time()
    order = [p["active"]] + [a for a in ACCOUNTS if a != p["active"] and _configured(a)]
    return [a for a in order if p["limited"].get(a, 0) <= now] + [a for a in order if p["limited"].get(a, 0) > now]


@dataclass
class Response:
    text: str
    parsed_output: Any = None
    usage: dict = field(default_factory=dict)
    stop_reason: str | None = None


def available() -> bool:
    return bool(shutil.which("claude") or os.path.exists(CLAUDE_BIN))


def _auth_status(account: str) -> dict:
    """`claude auth status` (약 0.2초). 2번을 아직 안 만들었으면 부르지 않는다 - 부르면 빈 설정 폴더가 생긴다."""
    if not _configured(account):
        return {}
    try:
        p = subprocess.run([CLAUDE_BIN, "auth", "status"], capture_output=True, text=True, timeout=15, env=_env(account))
        return json.loads(p.stdout)
    except Exception:
        return {}


def status() -> dict:
    """홈 환경설정이 쓰는 상태: 설치됐는지, 계정마다 로그인·한도, 고른 계정. claude_logged_in은 하나라도 되면 참."""
    if not available():
        return {"claude_installed": False, "claude_logged_in": False, "claude_accounts": []}
    p, now = _prefs(), time.time()
    accounts = []
    for a in ACCOUNTS:
        st = _auth_status(a)
        until = p["limited"].get(a, 0)
        accounts.append({"id": a, "logged_in": bool(st.get("loggedIn")), "email": st.get("email"),
                         "plan": st.get("subscriptionType"), "limited_until": until if until > now else None})
    return {"claude_installed": True, "claude_logged_in": any(x["logged_in"] for x in accounts),
            "claude_active": p["active"], "claude_accounts": accounts}


def require_login() -> None:
    """작업을 시작하기 전에 부른다 - 업로드가 다 끝난 뒤에야 첫 AI 단계에서 실패하지 않게."""
    st = status()
    if not st["claude_installed"]:
        raise ValueError("Claude Code가 설치돼 있지 않습니다 - 설치하고 로그인한 뒤 다시 시도하세요")
    if not st["claude_logged_in"]:
        raise ValueError("Claude Code에 로그인돼 있지 않습니다 - 환경설정에서 먼저 로그인하세요")


def _system_text(system) -> str:
    if isinstance(system, list):  # 예전 API식 블록 목록 (cache_control 등은 버린다)
        return "\n\n".join(b.get("text", "") for b in system)
    return system or ""


def _clean_block(b: dict) -> dict:
    return {k: v for k, v in b.items() if k != "cache_control"}


def _stream_input(messages: list[dict]) -> str:
    lines = []
    for m in messages:
        if m.get("role") != "user":
            raise ValueError("claude_cli는 user 메시지만 보낼 수 있다")
        content = m["content"]
        if isinstance(content, list):
            content = [_clean_block(b) for b in content]
        lines.append(json.dumps({"type": "user", "message": {"role": "user", "content": content}}, ensure_ascii=False))
    return "\n".join(lines) + "\n"


def parse(*, model: str, messages: list[dict], system="", output_format=None, effort: str = "low",
          max_tokens: int | None = None, timeout: int = 900) -> Response:
    """`output_format`(pydantic 모델)을 주면 그 스키마로 답을 받아 `.parsed_output`에 검증해 넣는다.
    없으면 `.text`만 채운다."""
    cmd = [CLAUDE_BIN, "-p", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose",
           "--model", model, "--effort", effort, "--system-prompt", _system_text(system) or "You are a helpful assistant.",
           "--tools", "", "--no-session-persistence", "--disable-slash-commands",
           "--safe-mode", "--strict-mcp-config", "--setting-sources", ""]
    if output_format is not None:
        cmd += ["--json-schema", json.dumps(output_format.model_json_schema(), ensure_ascii=False)]
    last = None
    for account in _order():
        try:
            resp = _run(cmd, _stream_input(messages), account, max_tokens, timeout, output_format)
        except AccountUnavailable as e:
            print(f"claude 계정 {account}번 사용 불가, 다른 계정으로 넘김: {e}")
            if e.limited:
                _set_limited(account, time.time() + LIMIT_WAIT)
            last = e
            continue
        _set_limited(account, None)  # 한도가 풀렸다
        return resp
    raise ClaudeCLIError(f"쓸 수 있는 Claude 계정이 없습니다 - {last}")


def _run(cmd: list[str], stdin: str, account: str, max_tokens, timeout: int, output_format) -> Response:
    env = _env(account)
    env["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] = str(max(max_tokens or 0, 32000))
    try:
        proc = subprocess.run(cmd, input=stdin, capture_output=True, text=True,
                              timeout=timeout, env=env, cwd=tempfile.gettempdir())
    except subprocess.TimeoutExpired:
        raise ClaudeCLIError(f"claude -p timed out after {timeout}s")
    result = None
    for line in proc.stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            result = ev
    if result is None:
        raise ClaudeCLIError(f"claude -p failed (exit {proc.returncode}): {(proc.stderr or proc.stdout)[-1500:]}")
    if result.get("is_error"):
        msg = str(result.get("result"))[:500]
        if result.get("api_error_status") == 429 or _LIMIT_RE.search(msg):
            raise AccountUnavailable(msg, limited=True)
        if result.get("api_error_status") == 401 or _AUTH_RE.search(msg):
            raise AccountUnavailable(msg, limited=False)
        raise ClaudeCLIError(f"claude -p error ({result.get('subtype')}, status={result.get('api_error_status')}): "
                             f"{str(result.get('result'))[:1500]}")
    resp = Response(text=result.get("result") or "", usage=result.get("usage") or {},
                    stop_reason=result.get("stop_reason"))
    if output_format is not None:
        data = result.get("structured_output")
        resp.parsed_output = output_format.model_validate(data) if data is not None else None
    return resp


def call_json(system: str, prompt: str, model: str, timeout: int = 60) -> dict | None:
    """스키마 없이 JSON 객체 하나를 받는다 (pattern_suggest, transcript_search). 실패하면 None -
    호출부는 "제안 없음"으로 넘어간다."""
    try:
        resp = parse(model=model, system=system, timeout=timeout,
                     messages=[{"role": "user", "content": f"{prompt}\n\n다른 설명 없이 JSON 객체 하나만 출력하라."}])
        return json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", resp.text.strip()))
    except Exception as e:
        print(f"claude -p call failed: {e}")
        return None


# --------------------------------------------------------------------------- 웹 로그인
# 홈 화면 "로그인" 버튼이 `claude auth login --claudeai`를 백그라운드로 띄운다 (10-25 실측):
#   - CLI가 브라우저를 직접 열고 localhost에서 응답을 기다린다 - 그 브라우저에서 로그인을 마치면 코드 없이 끝난다.
#   - 브라우저가 안 열렸을 때를 위해 수동 링크를 출력하고 "Paste code here" 상태로 stdin을 기다린다 -
#     그 링크로 받은 코드를 웹 칸에 붙이면 stdin으로 넘긴다.
#   - 틀린 코드면 "Login failed: ..."를 찍고 종료 코드 1로 끝난다 - 다시 시작해야 한다.
_LOGIN_URL_RE = re.compile(r"https://\S+/oauth/authorize\?\S+")
_login_lock = threading.Lock()
_login: dict = {"proc": None, "account": "1", "out": "", "url": None, "done": False, "ok": None, "error": None}


def _login_reader(proc: subprocess.Popen, account: str) -> None:
    for chunk in iter(lambda: proc.stdout.read1(4096), b""):
        with _login_lock:
            _login["out"] += chunk.decode(errors="replace")
            if not _login["url"] and (m := _LOGIN_URL_RE.search(_login["out"])):
                _login["url"] = m.group(0)
    code = proc.wait()
    ok = code == 0 and bool(_auth_status(account).get("loggedIn"))
    with _login_lock:
        if _login["proc"] is proc:
            m = re.findall(r"(?:Login failed|Error)[^\n]*", _login["out"])  # 앞에 붙은 "Paste code here >" 프롬프트는 뺀다
            _login.update(done=True, ok=ok, error=None if ok else (m[-1].strip() if m else f"종료 코드 {code}"))


def login_start(account: str = "1") -> dict:
    """이미 진행 중이면 그 상태를 돌려준다 (버튼을 두 번 눌러도 브라우저 탭이 하나만 열리게)."""
    if account not in ACCOUNTS:
        raise ValueError("없는 계정입니다")
    with _login_lock:
        p = _login["proc"]
        if p is not None and p.poll() is None:
            if _login["account"] == account:
                return login_state()
            p.kill()  # 다른 계정 로그인이 떠 있었다 - 그건 접고 새로 연다
    if not available():
        raise ValueError("Claude Code가 설치돼 있지 않습니다")
    if account != "1":
        (ACCOUNT_DIR / account).mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen([CLAUDE_BIN, "auth", "login", "--claudeai"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=_env(account))
    with _login_lock:
        _login.update(proc=proc, account=account, out="", url=None, done=False, ok=None, error=None)
    threading.Thread(target=_login_reader, args=(proc, account), daemon=True).start()
    for _ in range(40):  # 링크가 찍힐 때까지 최대 약 4초
        with _login_lock:
            if _login["url"] or proc.poll() is not None:
                break
        time.sleep(0.1)
    return login_state()


def login_code(code: str) -> dict:
    code = code.strip()
    with _login_lock:
        p = _login["proc"]
        if not code or p is None or p.poll() is not None:
            raise ValueError("진행 중인 로그인이 없습니다 - 다시 시작하세요")
        p.stdin.write((code + "\n").encode())
        p.stdin.flush()
    return login_state()


def login_cancel() -> None:
    with _login_lock:
        p = _login["proc"]
        _login.update(proc=None, done=False, ok=None, error=None, url=None)
    if p is not None and p.poll() is None:
        p.kill()


def login_state() -> dict:
    with _login_lock:
        p = _login["proc"]
        return {"running": p is not None and p.poll() is None and not _login["done"], "url": _login["url"],
                "account": _login["account"], "done": _login["done"], "success": _login["ok"], "error": _login["error"]}


def logout(account: str) -> None:
    """2번만 뺄 수 있다 - 1번은 이 컴퓨터의 Claude Code 로그인 자체라 여기서 건드리지 않는다."""
    if account == "1" or account not in ACCOUNTS:
        raise ValueError("1번 계정은 여기서 로그아웃하지 않습니다")
    if _configured(account):
        subprocess.run([CLAUDE_BIN, "auth", "logout"], capture_output=True, text=True, timeout=30, env=_env(account))
    _set_limited(account, None)
    if _prefs()["active"] == account:
        set_active("1")
