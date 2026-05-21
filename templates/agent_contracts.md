# Generic Agent Contracts

Use these contracts for any API domain. P2P, healthcare claims, billing, logistics, auth, and CRM all fit the same structure.

## Shared evidence harness

Purpose: deterministic execution and audit trail.

Required behavior:

- Accept `method`, `path`, optional `json_body`, optional `headers`.
- Reject absolute URLs unless target host is explicitly allowed.
- Log request, response, status code, elapsed time, and parse errors.
- Redact secrets.
- Return structured content to the agent.
- Never let the LLM perform hidden HTTP calls through shell.

## Explorer agent contract

Purpose: discover valid workflow and stable fixtures.

Inputs:

- base URL
- domain profile
- optional docs/OpenAPI/README

Outputs:

- discovered endpoints/resources
- happy-path steps
- created object IDs
- schema notes
- unresolved questions

Behavior:

- Prefer docs, then live responses, then validation-error inference.
- Retry schema adaptations with a cap.
- Record all failed attempts as evidence.
- Do not run destructive adversarial probes.

## Adversarial agent contract

Purpose: attack domain invariants.

Inputs:

- base URL
- domain profile invariant catalog
- explorer report / baseline fixtures

Outputs:

- finding per invariant/probe
- HELD/BREACHED/INCONCLUSIVE status
- exact request/response/state evidence

Behavior:

- Build or request valid baseline before each attack.
- Re-fetch state after critical mutations.
- Be creative within the invariant catalog.
- Do not optimize for happy-path success.

## Judge agent contract

Purpose: independent evidence classification.

Inputs:

- explorer report
- adversarial report
- domain profile judge policy

Outputs:

- final report JSON
- summary
- missing evidence list
- recommended regression tests

Behavior:

- Do not trust either agent's conclusion without evidence.
- HELD requires clean rejection and/or valid state after.
- BREACHED requires reproducible evidence.
- 500/timeouts are robustness failures or inconclusive, not clean guardrails.

## Reuse pattern

For a new project, change only:

1. `domain_profile.yaml`
2. endpoint discovery hints, if any
3. invariant catalog
4. auth/header setup in `api_tool.py`

Keep the explorer/adversary/judge contracts unchanged.
