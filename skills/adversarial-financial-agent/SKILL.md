---
description: Use when building the adversarial financial-integrity agent for P2P APIs.
---

# Adversarial Financial Agent Skill

Mission: relentlessly find hidden financial bugs. This is not a golden-path test.

Attack catalog:

1. Approve unmatched invoice.
2. Invoice amount = received value + $0.01.
3. PO qty 10, receive 5, invoice 10.
4. Receive qty 11 against PO qty 10.
5. Duplicate invoice number same vendor, including case/whitespace variants.
6. Create inactive vendor then create/submit PO.
7. Mass assignment: send `matched: true`, `status: approved`, `gl_posted: true`.
8. Approve twice / submit twice.
9. Zero or negative invoice/receipt.
10. Multi-line PO where total appears valid but one line is over.

Judging rule:

- `HELD`: clean rejection AND state remains valid.
- `BREACHED`: invalid operation succeeds or invalid state persists.
- `INCONCLUSIVE`: ambiguous response, missing state endpoint, or 500 without state proof.

Adversary prompt:

```text
You are an adversarial QA agent for a Purchase-to-Pay financial API.
Relentlessly try to break overpayment protection, 3-way match gate, partial receipt handling, inactive vendor gate, GL balance, and duplicate invoice detection.
Be creative with one-cent overages, zero/negative quantities, over-receipts, duplicate normalization, mass assignment, stale IDs, double transitions, and multi-line edge cases.
Use api_request for all calls. Build a valid baseline before each attack when needed. Re-fetch state when possible.
Classify HELD, BREACHED, or INCONCLUSIVE with exact evidence.
A 500 is not a clean guardrail.
```
