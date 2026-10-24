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
"""
from __future__ import annotations
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from typing import Any

CLAUDE_BIN = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")

# 이 키들이 환경에 있으면 CLI가 구독 대신 API로 과금한다
_BILLING_ENV = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")


class ClaudeCLIError(RuntimeError):
    pass


@dataclass
class Response:
    text: str
    parsed_output: Any = None
    usage: dict = field(default_factory=dict)
    stop_reason: str | None = None


def available() -> bool:
    return bool(shutil.which("claude") or os.path.exists(CLAUDE_BIN))


def status() -> dict:
    """홈 환경설정이 쓰는 상태: 설치됐는지, 구독 계정으로 로그인돼 있는지 (`claude auth status`, 약 0.2초)."""
    if not available():
        return {"claude_installed": False, "claude_logged_in": False}
    env = {k: v for k, v in os.environ.items() if k not in _BILLING_ENV}
    try:
        p = subprocess.run([CLAUDE_BIN, "auth", "status"], capture_output=True, text=True, timeout=15, env=env)
        logged_in = bool(json.loads(p.stdout).get("loggedIn"))
    except Exception:
        logged_in = False
    return {"claude_installed": True, "claude_logged_in": logged_in}


def require_login() -> None:
    """작업을 시작하기 전에 부른다 - 업로드가 다 끝난 뒤에야 첫 AI 단계에서 실패하지 않게."""
    st = status()
    if not st["claude_installed"]:
        raise ValueError("Claude Code가 설치돼 있지 않습니다 - 설치하고 로그인한 뒤 다시 시도하세요")
    if not st["claude_logged_in"]:
        raise ValueError("Claude Code에 로그인돼 있지 않습니다 - 터미널에서 claude를 실행해 /login 하세요")


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
    env = {k: v for k, v in os.environ.items() if k not in _BILLING_ENV}
    env["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] = str(max(max_tokens or 0, 32000))
    try:
        proc = subprocess.run(cmd, input=_stream_input(messages), capture_output=True, text=True,
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
