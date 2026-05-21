#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

DEFAULT_REQUIRED_RULES = {
    'overpayment_protection',
    'three_way_match_gate',
    'partial_receipt_flag',
    'inactive_vendor_gate',
    'gl_balance',
    'duplicate_invoice_detection',
}
VALID_STATUSES = {'HELD', 'BREACHED', 'INCONCLUSIVE'}

def fail(msg):
    print(f'FAIL: {msg}')
    return 1

def load_required_rules(profile_path=None):
    """Load invariant IDs from a lightweight YAML profile without requiring PyYAML."""
    if not profile_path:
        return DEFAULT_REQUIRED_RULES
    p = Path(profile_path)
    if not p.exists():
        return DEFAULT_REQUIRED_RULES
    text = p.read_text()
    ids = set(re.findall(r'^\s*-?\s*id:\s*([A-Za-z0-9_\-]+)\s*$', text, flags=re.M))
    return ids or DEFAULT_REQUIRED_RULES

def walk_status_codes(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == 'status_code' and isinstance(nested, int):
                yield nested
            else:
                yield from walk_status_codes(nested)
    elif isinstance(value, list):
        for item in value:
            yield from walk_status_codes(item)

def has_state_evidence(evidence):
    if not isinstance(evidence, dict):
        return False
    return any(key in evidence for key in ('state', 'state_after', 'states', 'vendor_exposure', 'gl_state'))

def main(path='report.json', profile_path=None):
    required_rules = load_required_rules(profile_path)
    p = Path(path)
    if not p.exists():
        return fail(f'missing report {path}')
    try:
        report = json.loads(p.read_text())
    except Exception as e:
        return fail(f'invalid JSON: {e}')
    errors = []
    for key in ['happy_path', 'adversarial', 'summary']:
        if key not in report:
            errors.append(f'missing top-level key: {key}')
    hp = report.get('happy_path') or {}
    steps = hp.get('steps') or []
    if hp.get('status') not in {'PASS', 'FAIL', 'NOT_RUN'}:
        errors.append('happy_path.status must be PASS|FAIL|NOT_RUN')
    for i, step in enumerate(steps):
        for key in ['request', 'response', 'status_code', 'interpretation']:
            if key not in step:
                errors.append(f'happy_path.steps[{i}] missing {key}')
    adv = report.get('adversarial') or []
    if not isinstance(adv, list):
        errors.append('adversarial must be a list')
        adv = []
    seen = set()
    for i, finding in enumerate(adv):
        if not isinstance(finding, dict):
            errors.append(f'adversarial[{i}] must be an object')
            continue
        rule = finding.get('rule')
        status = finding.get('status')
        evidence = finding.get('evidence')
        if rule:
            seen.add(rule)
        if status not in VALID_STATUSES:
            errors.append(f'adversarial[{i}] invalid status {status}')
        if not isinstance(evidence, dict) or not evidence:
            errors.append(f'adversarial[{i}] missing evidence')
        blob = json.dumps(evidence, default=str).lower() if evidence is not None else ''
        status_codes = list(walk_status_codes(evidence))
        clean_rejection = any(code in {400, 401, 403, 409, 422} for code in status_codes)
        if status == 'HELD' and any(code >= 500 for code in status_codes):
            errors.append(f'adversarial[{i}] HELD appears to rely on 500; mark robustness failure/INCONCLUSIVE unless state proves held')
        if status == 'HELD' and not clean_rejection and not has_state_evidence(evidence):
            errors.append(f'adversarial[{i}] HELD lacks clean rejection or state evidence')
        if status == 'BREACHED' and not any(k in blob for k in ['request', 'response', 'attack']):
            errors.append(f'adversarial[{i}] BREACHED lacks reproduction evidence')
    missing_rules = required_rules - seen
    if missing_rules:
        errors.append('missing invariant findings: ' + ', '.join(sorted(missing_rules)))
    label = 'QA report eval'
    if errors:
        print(f'{label}: FAIL')
        for e in errors:
            print(' - ' + e)
        return 1
    print(f'{label}: PASS')
    print(f' - required invariants: {len(required_rules)}')
    print(f' - happy_path steps: {len(steps)}')
    print(f' - adversarial findings: {len(adv)}')
    return 0

if __name__ == '__main__':
    args = sys.argv[1:]
    report = args[0] if args else 'report.json'
    profile = args[1] if len(args) > 1 else None
    raise SystemExit(main(report, profile))
