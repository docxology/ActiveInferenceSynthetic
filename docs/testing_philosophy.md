# Testing philosophy

Tests evaluate real mathematics, files, figures, and Lean builds. Mock
frameworks are not used.

## Test map

- `_prob.py`, `ou_model.py`: shared boundary tests
- Each scientific core: dedicated analytic-reference tests
- `src/figures/`: PNG rendering into `tmp_path`
- Script wrappers: real entry-point smoke tests
- `formal/`: source audits and `lake build`

Run from the project root:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90 -ra
```

The configured floor is 90% branch coverage. Current percentages are measured
results and should not be hard-coded in this guide.

## Hosted and native checks

The [Python workflow](developer/github_workflows.md) configures locked jobs
on Python 3.14 and 3.15. These jobs cover the configured coverage floor,
publication file and link controls, lint and type checks, package construction
and isolated wheel behavior.
It does not install Lean or render paper/video outputs.

Local pytest runs include the formal source audits. When Lake is absent,
pytest skips the native Lean build, axiom audit and false-claim rejection
checks. The `-ra` test summary reports the skip reasons.

A local full run with the pinned Lean prerequisites supplies native proof evidence.
[Formal setup](developer/formal.md) documents the separate axiom and
false-proposition controls. Passing Python CI alone does not verify those proofs.
