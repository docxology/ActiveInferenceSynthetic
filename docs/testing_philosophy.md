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
