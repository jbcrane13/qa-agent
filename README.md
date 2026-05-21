# qa-agent

A Claude Code plugin marketplace hosting **qa-agent**: a reusable QA-agent factory for API testing.

`qa-agent` packages everything needed to spin up a domain-aware QA workflow for any HTTP API — exploration, adversarial invariant testing, evidence-based judging, repeatable evals, and tool-use guardrails — all driven by a small `domain_profile.yaml`.

## Install

Run these inside Claude Code, one command at a time:

```text
/plugin marketplace add jbcrane13/qa-agent
/plugin install qa-agent@qa-agent
```

Restart Claude Code, then verify:

```text
/plugin list
```

You should see `qa-agent` enabled.

## What's inside

| Component | Path | Purpose |
|-----------|------|---------|
| Commands | `commands/` | `/qa-agent:create-scaffold`, `/qa-agent:build-explorer`, `/qa-agent:build-adversary`, `/qa-agent:build-judge`, `/qa-agent:build-evals`, `/qa-agent:run-evals`, `/qa-agent:interview-narration` |
| Agents | `agents/` | `api-explorer`, `invariant-adversary`, `qa-judge` — specialized subagents |
| Skills | `skills/` | `qa-agent-factory`, `api-explorer-agent`, `adversarial-financial-agent`, `judge-evals` |
| Hooks | `hooks/hooks.json` | `PreToolUse` guards on `Bash` and `Read`/`Write`/`Edit` |
| Scripts | `scripts/` | `guard_bash.py`, `guard_files.py`, `eval_report.py` |
| Templates | `templates/` | `domain_profile.yaml`, `agent_contracts.md` |
| Evals | `evals/` | `financial_invariants.md` reference rules |

## Quick start

After installing, run these inside the API repo you want to test.

1. **Scaffold a QA harness** in your repo:
   ```text
   /qa-agent:create-scaffold <your-domain>
   ```

2. **Edit `qa_agents/domain_profile.yaml`** to describe the target API:
   - entities
   - happy-path workflow
   - invariants / business rules
   - judge policy
   - safety settings

3. **Build the agents**:
   ```text
   /qa-agent:build-explorer  http://localhost:8000
   /qa-agent:build-adversary http://localhost:8000
   /qa-agent:build-judge
   /qa-agent:build-evals
   ```

4. **Run evals against the final report**:
   ```text
   /qa-agent:run-evals report.json
   ```

## Example: Purchase-to-Pay practice flow

```text
/qa-agent:interview-narration
/qa-agent:create-scaffold purchase_to_pay
/qa-agent:build-explorer http://localhost:8000
/qa-agent:build-adversary http://localhost:8000
/qa-agent:build-judge
/qa-agent:build-evals
/qa-agent:run-evals report.json
```

## How it works

The plugin enforces a seven-layer agent contract:

1. Mission / invariant
2. Narrow tools
3. Evidence log
4. Role split: explorer, adversary, judge
5. Domain profile
6. Evals
7. Guardrails

See:

```text
templates/agent_contracts.md
skills/qa-agent-factory/SKILL.md
```

Guardrail hooks block obviously unsafe bash and file operations via:

```text
scripts/guard_bash.py
scripts/guard_files.py
```

## Repository layout

```text
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
