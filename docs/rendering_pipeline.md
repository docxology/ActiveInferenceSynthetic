# Rendering pipeline

## Figures

```bash
uv run python scripts/generate_all_figures.py
```

`src.figures.render_all()` writes the registered PNGs under
`output/figures/`. Individual `scripts/generate_*_figure.py` wrappers regenerate
one figure.

## Manuscript

From the `docxology/template` checkout whose
`projects/working/ActiveInferenceSynthetic` link resolves to this repository:

```bash
uv run python projects/working/ActiveInferenceSynthetic/scripts/00_preflight.py
uv run python -m infrastructure.validation.cli prerender \
  projects/working/ActiveInferenceSynthetic/docs/manuscript --repo-root .
uv run python scripts/pipeline/stage_03_render.py \
  --project working/ActiveInferenceSynthetic
uv run python scripts/pipeline/stage_04_validate.py \
  --project working/ActiveInferenceSynthetic
```

Metadata and enabled formats come from `docs/manuscript/config.yaml`. Manuscript
sources are ordered by filename. Figure declarations live in
`docs/manuscript/figure_registry.yaml`.

`generate_all_figures.py` also exports the authored figure metadata to
`output/figures/figure_registry.json`, the format consumed by template validation.

Stage 03 runs the project's variable generator, consumes the hydrated sections
under `output/manuscript/`, and uses template's `RenderManager`, Pandoc,
pandoc-crossref, XeLaTeX, and BibTeX to produce the combined PDF and HTML.
Use the ordinary command above after source edits; hydration must not be skipped.
Stage 04 validates the generated artifacts and writes
`output/reports/rendered_provenance.json`, binding source, configuration,
composition, and output fingerprints. A successful render alone does not replace
this validation receipt or visual review of the actual PDF and HTML.

The local template-render verification records are under
`output/reports/template-render-20261011/`. The lecture retains its separate
frozen sources and delivery receipt; regenerating the paper does not replace it.

Do not edit generated files under `output/pdf/`, `output/web/`, or
`output/figures/`; change sources and rerun the relevant stage.
