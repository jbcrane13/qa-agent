#!/usr/bin/env python3
"""PreToolUse(Read|Write|Edit) guardrail. Reads Claude Code hook JSON from stdin
and blocks operations touching obvious secret-file patterns."""
import json
import sys

SECRET_TOKENS = (".env", "id_rsa", "id_ed25519", "secrets.json")

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_input = payload.get("tool_input") or {}
# Check the fields the file tools actually use: file_path (Read/Write/Edit),
# plus content/old_string/new_string for completeness.
text = " ".join(
    str(tool_input.get(k) or "")
    for k in ("file_path", "path", "content", "old_string", "new_string")
)

for token in SECRET_TOKENS:
    if token in text:
        print(f"Blocked by qa-agent guardrail: secret file pattern {token}", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
