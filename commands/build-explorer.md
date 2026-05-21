# Build P2P API Explorer Agent

Argument: `$ARGUMENTS` is the base URL, default `http://localhost:8000`.

Build or update these files using Claude Agent SDK:

- `qa_agents/api_tool.py` — shared deterministic `api_request` custom tool and evidence log.
- `qa_agents/p2p_explorer_agent.py` — explorer/happy-path agent only.

Do **not** put adversarial testing in this file. The adversary is a separate agent so its objective and prompt stay clean.

Requirements:

1. Read `qa_agents/domain_profile.yaml` if present. Treat it as the source of project-specific entities, workflow, invariants, judge policy, and safety settings.
2. Create a narrow `api_request` custom tool using `claude_agent_sdk.tool` and `create_sdk_mcp_server`.
3. Tool inputs: `method`, `path`, optional `json_body`.
4. Tool rejects absolute remote URLs; only relative paths against the configured base URL.
5. Tool logs structured evidence: method, path, request, status_code, response, elapsed_ms.
6. Add explorer prompt from the `api-explorer-agent` skill, parameterized by the domain profile.
7. Agent discovers required entities/workflow from the domain profile and live API responses, builds happy path, logs interpretation after every call.
8. Add bounded self-healing: validation error → smallest corrected payload → max 3 retries.
9. Configure `ClaudeAgentOptions` with `tools=[]`, `allowed_tools=["mcp__p2p_api__api_request"]`, `permission_mode="dontAsk"`, and `strict_mcp_config=True`.
10. CLI: `--base-url`, `--profile qa_agents/domain_profile.yaml`, `--out explorer_report.json`.

After coding:

```bash
python -m py_compile qa_agents/api_tool.py qa_agents/p2p_explorer_agent.py
python qa_agents/p2p_explorer_agent.py --base-url ${ARGUMENTS:-http://localhost:8000} --profile qa_agents/domain_profile.yaml --out explorer_report.json
```

Narrate while working: deterministic execution, Claude reasoning, bounded self-healing, evidence log.
