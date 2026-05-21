---
description: Scaffold a reusable QA-agent harness (domain profile, agent contracts, api tool, evals) into the current repo
argument-hint: [domain-name]
---

# Create Reusable QA Agent Scaffold

Argument: `$ARGUMENTS` is the domain name, default `api_domain`.

Create a reusable QA-agent scaffold that can be adapted to the current repo.

Files to create:

```text
qa_agents/
  domain_profile.yaml
  agent_contracts.md
  api_tool.py
  p2p_explorer_agent.py              # or <domain>_explorer_agent.py if renaming is safe
  p2p_adversarial_agent.py           # or <domain>_adversarial_agent.py
  p2p_judge.py                       # or <domain>_judge.py
  evals/eval_report.py
```

Use plugin templates:

```bash
mkdir -p qa_agents/evals
cp "${CLAUDE_PLUGIN_ROOT}/templates/domain_profile.yaml" qa_agents/domain_profile.yaml
cp "${CLAUDE_PLUGIN_ROOT}/templates/agent_contracts.md" qa_agents/agent_contracts.md
cp "${CLAUDE_PLUGIN_ROOT}/scripts/eval_report.py" qa_agents/evals/eval_report.py
```

Then customize `qa_agents/domain_profile.yaml` for the current project.

Design rules:

1. Keep project-specific business rules in `domain_profile.yaml`.
2. Keep role behavior in `agent_contracts.md` and prompts.
3. Keep HTTP mechanics in `api_tool.py`.
4. Keep final grading in `p2p_judge.py` / judge agent.
5. Make the P2P domain look like a config instance, not hardcoded architecture.

Narration:

> I’m starting by creating the reusable scaffold. For a different API, I’d keep the evidence harness and three-agent pattern, then swap the domain profile: entities, workflow, invariants, and judge policy.
