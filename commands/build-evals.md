---
description: Build eval files (report schema, invariant list, eval_report.py) for the QA agent reports
---

# Build QA Agent Evals

Create eval files for the P2P QA agent.

Build:

- `qa_agents/evals/report_schema.json` for expected report shape.
- `qa_agents/evals/financial_invariants.md` listing the six auditor rules and hidden-bug probes.
- `qa_agents/evals/eval_report.py` or copy plugin `scripts/eval_report.py`.

Evals must check:

1. JSON report parses.
2. Required top-level keys exist.
3. All adversarial findings use HELD/BREACHED/INCONCLUSIVE.
4. All six financial rules are represented.
5. HELD findings do not rely solely on HTTP 500.
6. BREACHED findings include request/response evidence.
7. Happy path steps include request, response, status, interpretation.

Run:

```bash
python qa_agents/evals/eval_report.py report.json
```
