"""Call Claude through the Claude Code CLI (`claude -p`) instead of the Anthropic API SDK -
for the two review-UI features the user wants billed through their existing paid Claude Code
subscription rather than a separate metered ANTHROPIC_API_KEY (사용자 프로세스 LLM 적용, "클로드는
과금해서 쓰고 있어").

Only used by pattern_suggest.py and transcript_search.py - both fire rarely (once per NG case
per session / only when a literal search misses), so the extra latency measured here is
tolerable there. Deliberately NOT used for the per-video batch pipeline (classify_candidates.py
and friends, 30+ calls per video): a real trivial call through this path took ~5.5s (vs <2s for
a direct API call with thinking disabled) because `claude -p` always loads the full Claude Code
system prompt fresh and has no flag to disable extended thinking. Multiplying that across dozens
of calls would turn a ~2-minute batch into many minutes for the same underlying Anthropic usage
either way, which is a bad trade for something that isn't a button click.
"""
from __future__ import annotations
import json
import re
import shutil
import subprocess
import tempfile

CLAUDE_BIN = shutil.which("claude") or "/Users/jiho-mac/.local/bin/claude"


def call_json(system: str, prompt: str, model: str, timeout: int = 60) -> dict | None:
    """Runs `claude -p` non-interactively and parses its reply as JSON.

    - `--permission-mode plan`: read-only, so a call that (for whatever reason) tried to use a
      tool could never edit or run anything - our prompts carry all needed context inline and
      shouldn't need tools at all, but this is the safety margin if one ever does.
    - cwd is a scratch temp dir, not the project: keeps this an isolated one-shot Q&A instead of
      Claude Code auto-loading this project's CLAUDE.md/file context, which would only add
      tokens and latency for no benefit here.
    - The CLI wraps the reply in an outer JSON envelope (`result` holds the actual text), and
      the model itself often fences its JSON in ```json ... ``` - both are stripped before the
      real parse. Returns None on any failure so callers can fall back to "no suggestion"
      rather than crash the request.
    """
    full_prompt = f"{system}\n\n{prompt}\n\n다른 설명 없이 JSON 객체 하나만 출력하라."
    try:
        proc = subprocess.run(
            [CLAUDE_BIN, "-p", full_prompt, "--output-format", "json",
             "--model", model, "--permission-mode", "plan"],
            capture_output=True, text=True, timeout=timeout, check=True, cwd=tempfile.gettempdir(),
        )
        outer = json.loads(proc.stdout)
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", outer.get("result", "").strip())
        return json.loads(text)
    except Exception as e:
        print(f"claude -p call failed: {e}")
        return None
