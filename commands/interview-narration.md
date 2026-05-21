# Interview Narration Cheat Sheet

Use this when asked to explain the workflow.

Say:

> I’m using a reusable QA-agent scaffold: shared evidence harness, domain profile, role-specific agents, evals, and guardrails. For this challenge, Purchase-to-Pay is just the domain profile — entities, workflow, invariants, and judge policy.

Then add:

> I’m using project rules, reusable prompts, skills, agents, memory/context files, evals, test harnesses, and guardrails — but only where they map to practical controls.

Translate buzzwords to engineering behavior:

- **Project rules:** keep Claude aligned with repo commands, test setup, and coding conventions.
- **Domain profile:** moves project-specific facts out of the agents: entities, workflows, invariants, judge policy.
- **Reusable prompts:** make the explorer/adversary/judge behavior repeatable across domains, not vibes.
- **Skills:** encode the agent-building workflow so we avoid repeated mistakes.
- **Agents:** isolate roles: explorer learns the API, adversary attacks invariants, judge verifies evidence.
- **Memory/context files:** persist stable project facts without dumping noise into every prompt.
- **Evals:** prove the report is complete and the judge did not confuse 500s/status codes with guardrails.
- **Test harness:** deterministic HTTP tool logs every action and makes bugs reproducible.
- **Guardrails:** narrow tools, permission limits, retry caps, blocked dangerous commands.

Key line:

> Claude is creative in deciding what to try, but conservative in what it is allowed to do.
