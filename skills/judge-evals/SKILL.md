---
description: Use when creating evals and judge checks for API QA agent reports.
---

# Judge and Evals Skill

The judge exists to prevent fake confidence.

Required report shape:

```json
{
  "happy_path": {"status": "PASS|FAIL", "steps": []},
  "adversarial": [
    {"rule": "overpayment_protection", "status": "HELD|BREACHED|INCONCLUSIVE", "evidence": {}}
  ],
  "summary": "..."
}
```

Eval checklist:

- Report parses as JSON.
- Contains `happy_path`, `adversarial`, `summary`.
- Every step has request, response, status code, interpretation.
- Every stated financial invariant has at least one adversarial finding.
- Negative case `HELD` includes evidence of clean rejection and/or valid state after.
- 500 responses are not treated as clean `HELD` guardrails.
- Any `BREACHED` finding includes reproduction evidence.
- Critical mutations re-fetch state where endpoint exists.

Use `scripts/eval_report.py report.json` to run basic structural evals.
