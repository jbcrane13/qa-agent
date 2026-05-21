#!/usr/bin/env python3
"""PreToolUse(Bash) guardrail. Reads Claude Code hook JSON from stdin and blocks
dangerous or non-local commands by exiting 2 (stderr is fed back to Claude)."""
import json
import re
import sys

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_input = payload.get("tool_input") or {}
cmd = str(tool_input.get("command") or "")

blocked = [
    r"rm\s+-rf\s+/",
    r"git\s+push\s+.*--force",
    r"curl\s+.*https?://(?!localhost|127\.0\.0\.1)",
    r"(dropdb|DROP\s+DATABASE)",
]

if any(re.search(p, cmd, re.I) for p in blocked):
    print("Blocked by qa-agent guardrail: dangerous or non-local command", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
