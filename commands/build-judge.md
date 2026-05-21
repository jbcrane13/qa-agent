# Build P2P QA Judge Agent

Create a **separate** `qa_agents/p2p_judge.py` using Claude Agent SDK or deterministic Python checks plus an optional Claude reasoning pass.

Inputs:

- `qa_agents/domain_profile.yaml`
- `explorer_report.json`
- `adversarial_report.json`

Output:

- `report.json` matching the challenge schema:

```json
{
  "happy_path": {"status": "PASS|FAIL", "steps": []},
  "adversarial": [
    {"rule": "overpayment_protection", "status": "HELD|BREACHED|INCONCLUSIVE", "evidence": {}}
  ],
  "summary": "..."
}
```

Requirements:

1. Keep judge independent from explorer/adversary execution.
2. Read `qa_agents/domain_profile.yaml`; use its `invariants` and `judge_policy` instead of hardcoding P2P assumptions.
3. Validate report shape before writing final output.
4. Do not classify `HELD` from status code alone.
5. Treat HTTP 500 as robustness failure or `INCONCLUSIVE` unless state evidence proves no mutation.
6. Require reproduction evidence for every `BREACHED` finding.
7. Require every invariant in `domain_profile.yaml` to appear in the final report. For the included P2P profile, that means:
   - `overpayment_protection`
   - `three_way_match_gate`
   - `partial_receipt_flag`
   - `inactive_vendor_gate`
   - `gl_balance`
   - `duplicate_invoice_detection`

After coding:

```bash
python -m py_compile qa_agents/p2p_judge.py
python qa_agents/p2p_judge.py --profile qa_agents/domain_profile.yaml --happy-path explorer_report.json --adversarial adversarial_report.json --out report.json
python "${CLAUDE_PLUGIN_ROOT}/scripts/eval_report.py" report.json qa_agents/domain_profile.yaml
```

Narrate: the judge is its own agent/check because execution evidence and final classification are separate responsibilities. This prevents the same agent that ran a probe from grading its own homework.
