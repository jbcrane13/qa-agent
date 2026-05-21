# Financial Invariants Eval Checklist

Required invariants:

1. overpayment_protection — invoice amount must not exceed received goods value.
2. three_way_match_gate — invoice cannot approve unless matched.
3. partial_receipt_flag — partial receipt must be surfaced/not silently pass full invoice.
4. inactive_vendor_gate — inactive vendor cannot create/submit PO.
5. gl_balance — approved invoice GL entry debits equal credits.
6. duplicate_invoice_detection — same vendor + invoice_number rejected.

Hidden-bug probes:

- one-cent overage
- zero/negative qty or amount
- over-receipt
- duplicate invoice casing/whitespace
- mass assignment of status/matched/gl_posted
- double submit/approve
- stale/cross-vendor IDs
- multi-line line-level mismatch
