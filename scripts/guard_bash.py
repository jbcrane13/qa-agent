#!/usr/bin/env python3
import json, os, re, sys
raw = os.environ.get('CLAUDE_TOOL_INPUT', '{}')
try:
    data = json.loads(raw)
except Exception:
    data = {}
cmd = str(data.get('command') or data.get('cmd') or data)
blocked = [r'rm\s+-rf\s+/', r'git\s+push\s+.*--force', r'curl\s+.*https?://(?!localhost|127\.0\.0\.1)', r'(dropdb|DROP\s+DATABASE)']
if any(re.search(p, cmd, re.I) for p in blocked):
    print('Blocked by qa-agent guardrail: dangerous or non-local command')
    sys.exit(2)
sys.exit(0)
