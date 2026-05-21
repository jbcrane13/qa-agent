# Build P2P Financial Adversarial Agent

Argument: `$ARGUMENTS` is the base URL, default `http://localhost:8000`.

Create a **separate** `qa_agents/p2p_adversarial_agent.py` using Claude Agent SDK. Do not bury this as just a mode inside the explorer.

Also create or reuse:

- `qa_agents/api_tool.py` for the shared deterministic `api_request` evidence tool.
- `qa_agents/p2p_explorer_agent.py` only as a baseline/context producer.
- `qa_agents/p2p_judge.py` for final report classification if not already present.

Requirements:

1. Read `qa_agents/domain_profile.yaml`. Use its invariant catalog and judge policy as the source of truth for attacks.
2. Import/reuse the same `api_request` evidence tool, but give the adversary its own prompt, session, and output contract.
3. Add adversarial prompt from `adversarial-financial-agent` skill, parameterized by the domain profile.
4. Build baseline objects before attacks when needed, either by invoking explorer output or by local baseline factory helpers.
5. Attack every invariant/probe listed in the domain profile, plus reasonable variants. For P2P, include:
   - unmatched approval
   - overpayment + $0.01
   - partial receipt full invoice
   - over-receipt
   - inactive vendor PO
   - duplicate invoice normalization
   - mass assignment
   - double submit/approve
   - zero/negative quantities/amounts
6. Judge each finding as HELD, BREACHED, or INCONCLUSIVE.
7. HELD requires clean rejection and valid state when state is exposed; status code alone is insufficient.
8. Configure `ClaudeAgentOptions` with `tools=[]`, `allowed_tools=["mcp__p2p_api__api_request"]`, `permission_mode="dontAsk"`, and `strict_mcp_config=True`.
9. CLI: `--base-url`, `--profile qa_agents/domain_profile.yaml`, `--explorer-report explorer_report.json`, `--out adversarial_report.json`.

After coding:

```bash
python -m py_compile qa_agents/api_tool.py qa_agents/p2p_adversarial_agent.py qa_agents/p2p_judge.py
python qa_agents/p2p_adversarial_agent.py --base-url ${ARGUMENTS:-http://localhost:8000} --profile qa_agents/domain_profile.yaml --explorer-report explorer_report.json --out adversarial_report.json
python qa_agents/p2p_judge.py --happy-path explorer_report.json --adversarial adversarial_report.json --out report.json
```

Narrate: this is a separate specialist agent, not a mode switch. The explorer tries to make a valid workflow; the adversary tries to make wrong money move. Separate prompts/sessions prevent the adversary from inheriting happy-path bias.
