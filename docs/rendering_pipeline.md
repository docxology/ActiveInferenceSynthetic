# Rendering pipeline

## Figures

```bash
uv run python scripts/generate_all_figures.py
```

`src.figures.render_all()` writes the seven registered PNGs under
`output/figures/`. Individual `scripts/generate_*_figure.py` wrappers regenerate
one figure.

## Manuscript

From the public template checkout:

```bash
uv run python scripts/pipeline/stage_03_render.py \
  --project working/ActiveInferenceSynthetic
```

Metadata and enabled formats come from `docs/manuscript/config.yaml`. Manuscript
sources are ordered by filename. Figure declarations live in
`docs/manuscript/figure_registry.yaml`.

Do not edit generated files under `output/pdf/`, `output/web/`, or
`output/figures/`; change sources and rerun the relevant stage.
