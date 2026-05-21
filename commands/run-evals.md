# Run P2P QA Agent Evals

Argument: `$ARGUMENTS` is the report path, default `report.json`.

Run the report eval script and summarize failures plainly.

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/eval_report.py" ${ARGUMENTS:-report.json} qa_agents/domain_profile.yaml
```

If evals fail:

- Fix report structure or agent judging logic.
- Do not paper over failures.
- Explain whether the issue is agent bug, API bug, or inconclusive evidence.
