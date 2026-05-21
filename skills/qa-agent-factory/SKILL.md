---
name: qa-agent-factory
description: Use when asked to quickly create a QA agent for an API from project rules, reusable prompts, skills, memory/context files, evals, test harnesses, and guardrails.
---

# P2P QA Agent Factory

Build QA agents in seven visible layers:

1. **Mission/invariant** — state what the agent is proving.
2. **Narrow tools** — expose only `api_request(method, path, json_body)` for HTTP.
3. **Structured evidence** — every tool call returns request, response, status, latency, interpretation slot.
4. **Plan-act-observe-adapt prompt** — Claude reasons about next steps from evidence.
5. **Bounded self-healing** — schema adaptation from validation errors, max 3 retries.
6. **Judge/evals** — verify state and business invariants, not status code only.
7. **Regression handoff** — each breach becomes a deterministic test.

Tie concepts to practice:

- Project rules keep generated code aligned with repo conventions.
- Reusable prompts prevent vague, one-off LLM behavior.
- Skills encode the workflow so we do not repeat mistakes.
- Agents isolate specialist reasoning: explorer, adversary, judge.
- Memory/context files give Claude stable project facts without dumping noise.
- Evals prove outputs match business rules.
- Guardrails limit tools and block dangerous operations.

Opening line:

> I’ll build this in layers and run after each layer. Claude reasons over schemas and edge cases, but deterministic tools execute and log every action.
