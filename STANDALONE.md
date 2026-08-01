# Standalone and sidecar use

ActiveInferenceSynthetic is a private sidecar project linked into the public
template checkout as `projects/working/ActiveInferenceSynthetic`.

## Self-contained surfaces

- Scientific Python package under `src/`
- Project tests under `tests/`
- Figure generation under `src/figures/` and `scripts/`
- Lean 4 development under `formal/`
- Manuscript sources and metadata under `manuscript/`

## Template-dependent surfaces

- `scripts/00_preflight.py`
- PDF/HTML rendering and validation
- Pipeline discovery and final output copying

## Local verification

```bash
uv sync
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src scripts tests
uv run mypy src
uv run python scripts/generate_all_figures.py
(cd formal && lake build)
```

## Template rendering

From the template checkout:

```bash
uv run python scripts/pipeline/stage_03_render.py \
  --project working/ActiveInferenceSynthetic
```

Commit and publish the project through its private repository, not the public
template repository.
