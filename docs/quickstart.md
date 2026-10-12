# Quick start

See [project positioning](positioning.md) for the paper's scope and
[standalone boundaries](../STANDALONE.md) for the external Lean and render tools.
Test collection and numerical generation need no template.

From the project root:

```bash
uv sync --locked --extra dev
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/generate_all_figures.py
(cd formal && lake build)
```

To render the manuscript, run from the public template root:

```bash
uv run python scripts/pipeline/stage_03_render.py \
  --project working/ActiveInferenceSynthetic
```

See [`troubleshooting.md`](troubleshooting.md) if project-root discovery or
external tools fail.
