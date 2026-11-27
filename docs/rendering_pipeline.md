# Rendering pipeline

## Figures

```bash
uv run python scripts/generate_all_figures.py
```

`src.figures.render_all()` writes the registered PNGs under
`output/figures/`. Individual `scripts/generate_*_figure.py` wrappers regenerate
one figure.

## Manuscript

Use [docxology/template at the pinned
revision](https://github.com/docxology/template/tree/87704feae0a4490ef7dad9c931d268e8c30273c2).
Install its locked environment and put Pandoc, its matching pandoc-crossref,
XeLaTeX and BibTeX on PATH. Install DejaVu Sans Mono for the portable
monospace fallback when JuliaMono is unavailable. From an isolated project
checkout, install the
project and produce the native figure and teaching outputs:

```bash
uv sync --locked --extra dev
uv run --no-sync python scripts/generate_all_figures.py
uv run --no-sync python scripts/run_teaching_experiments.py
export PROJECT_ROOT="$(pwd -P)"
export TEMPLATE_ROOT=/path/to/template
git -C "$TEMPLATE_ROOT" rev-parse HEAD
mkdir -p "$TEMPLATE_ROOT/projects/working"
ln -s "$PROJECT_ROOT" "$TEMPLATE_ROOT/projects/working/ActiveInferenceSynthetic"
```

Check that HEAD is the pin and the link resolves to the intended checkout.
From the Template root:

```bash
cd "$TEMPLATE_ROOT"
uv run --no-sync python scripts/pipeline/stage_03_render.py \
  --project working/ActiveInferenceSynthetic
uv run --no-sync python scripts/pipeline/stage_04_validate.py \
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

Inspect `output/pdf/ActiveInferenceSynthetic_combined.pdf` and
`output/web/index.html` in the project checkout. The [lecture](lecture.md)
retains its separate frozen sources and delivery receipt.

Do not edit generated files under `output/pdf/`, `output/web/`, or
`output/figures/`; change sources and rerun the relevant stage.
