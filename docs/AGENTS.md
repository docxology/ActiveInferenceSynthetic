# `docs/` technical index

These guides describe the live ActiveInferenceSynthetic tree. Keep commands
valid from the project root unless a guide explicitly says “template root.”

## Sources of truth

- Public Python API: [`../src/__init__.py`](../src/__init__.py)
- Figure registry: [`../src/figures/render_all.py`](../src/figures/render_all.py)
- Manuscript order: [`../manuscript/`](../manuscript/)
- Package version: [`../pyproject.toml`](../pyproject.toml)
- Render metadata: [`../manuscript/config.yaml`](../manuscript/config.yaml)
- Formal modules: [`../formal/ActiveInferenceFormal/`](../formal/ActiveInferenceFormal/)

Do not copy measured test counts into long-lived prose. State the configured
coverage floor (90%) and measure current results with the documented command.

## Verification

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src scripts tests
uv run mypy src
uv run python scripts/generate_all_figures.py
(cd formal && lake build)
```
