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
uv run pytest tests/ --cov=src --cov-fail-under=90
```

The configured floor is 90% branch coverage. Current percentages are measured
results and should not be hard-coded in this guide.

## Hosted and native checks

[Python CI](../.github/workflows/README.md) runs the locked environment on Python
3.10 and 3.14, including the configured coverage floor, publication file/link
controls, lint/type checks, package construction and isolated wheel behavior.
It does not install Lean or render paper/video outputs. Existing native-test
skip conditions remain visible in the summary; source checks continue to run.

A local full run with the pinned Lean prerequisites supplies native proof evidence.
[Formal setup](../formal/README.md) documents the separate axiom and
false-proposition controls. Passing Python CI alone does not verify those proofs.
