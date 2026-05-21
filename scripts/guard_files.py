#!/usr/bin/env python3
import json, os, sys
raw = os.environ.get('CLAUDE_TOOL_INPUT', '{}')
try:
    data = json.loads(raw)
except Exception:
    data = {}
text = str(data)
for token in ['.env', 'id_rsa', 'id_ed25519', 'secrets.json']:
    if token in text:
        print(f'Blocked by qa-agent guardrail: secret file pattern {token}')
        sys.exit(2)
sys.exit(0)
