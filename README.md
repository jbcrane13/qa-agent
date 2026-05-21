# qa-agent

A Claude Code plugin marketplace hosting **qa-agent**: a reusable QA-agent factory for API testing.

`qa-agent` packages everything needed to spin up a domain-aware QA workflow for any HTTP API — exploration, adversarial invariant testing, evidence-based judging, repeatable evals, and tool-use guardrails — all driven by a small `domain_profile.yaml`.

## Install

```bash
# Add this repo as a marketplace
/plugin marketplace add jbcrane13/qa-agent

# Install the plugin
/plugin install qa-agent@qa-agent
```

Restart Claude Code, then verify with `/plugin list` — you should see `qa-agent` enabled.

## What's inside

| Component | Path | Purpose |
|-----------|------|---------|
| Commands | `commands/` | `/create-scaffold`, `/build-explorer`, `/build-adversary`, `/build-judge`, `/build-evals`, `/run-evals`, `/interview-narration` |
| Agents | `agents/` | `api-explorer`, `invariant-adversary`, `qa-judge` — specialized subagents |
| Skills | `skills/` | `qa-agent-factory`, `api-explorer-agent`, `adversarial-financial-agent`, `judge-evals` |
| Hooks | `hooks/hooks.json` | `PreToolUse` guards on `Bash` and `Read`/`Write`/`Edit` |
| Scripts | `scripts/` | `guard_bash.py`, `guard_files.py`, `eval_report.py` |
| Templates | `templates/` | `domain_profile.yaml`, `agent_contracts.md` |
| Evals | `evals/` | `financial_invariants.md` reference rules |

## Quick start

After installing:

1. **Scaffold a QA harness** in your repo:
   ```
   /create-scaffold <your-domain>
   ```
2. **Edit `qa_agents/domain_profile.yaml`** to describe entities, workflow, invariants, and judge policy.
3. **Build the agents**:
   ```
   /build-explorer  http://localhost:8000
   /build-adversary http://localhost:8000
   /build-judge
   /build-evals
   ```
4. **Run evals against a report**:
   ```
   /run-evals report.json
   ```

## How it works

The plugin enforces a seven-layer agent contract: mission/invariant, narrow tools, evidence log, role split (explorer vs. adversary vs. judge), domain profile, evals, and guardrails. See `templates/agent_contracts.md` and `skills/qa-agent-factory/SKILL.md`.

Guardrail hooks block obviously unsafe bash and file operations via `scripts/guard_bash.py` and `scripts/guard_files.py`.

## Repository layout

```
.
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace manifest (lists qa-agent)
├── agents/
├── commands/
├── evals/
├── hooks/
├── scripts/
├── skills/
└── templates/
```

## License

MIT © Blake Crane
