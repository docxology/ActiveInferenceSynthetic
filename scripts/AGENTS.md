# `scripts/` — AGENTS.md

Thin orchestrators. All numerics live in `src/`; scripts coordinate rendering only.

## Figure generators

Each `generate_*_figure.py` delegates to `src.figures.<panel>.render()`.
`generate_all_figures.py` calls `src.figures.render_all.render_all()`.

Outputs land in `output/figures/` via `src.project_paths.project_output_dirs()`.

## Preflight

`00_preflight.py` invokes `infrastructure.validation.cli prerender` on the
manuscript tree. Requires the template checkout on `PYTHONPATH`.

## Adding a figure

1. Add builder under `src/figures/`.
2. Register in `src/figures/render_all.py`.
3. Add a thin script alias here.
4. Extend `tests/test_figures.py`.
