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
Prepare Python 3.14 for Template and the interpreter selected by the project's
[`.python-version`](../.python-version). Put Pandoc, its matching pandoc-crossref,
XeLaTeX and BibTeX on PATH. Install DejaVu Sans Mono for the portable monospace
fallback when JuliaMono is unavailable. See the [pinned setup guide](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/docs/RUN_GUIDE.md).

Start at the root of your Synthetic checkout. This creates a disposable copy
of its current commit inside Template's `projects/working/` directory. Stage 03
requires that physical Git checkout to read the manuscript during hydration.

```bash
source_checkout="$(pwd -P)"
source_commit="$(git rev-parse HEAD)"
render_workspace="$(mktemp -d)"
git clone --filter=blob:none --sparse https://github.com/docxology/template.git "$render_workspace/template"
cd "$render_workspace/template"
git switch --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
git sparse-checkout set docs infrastructure scripts
uv sync --locked --no-dev --python 3.14

project=projects/working/ActiveInferenceSynthetic
mkdir -p projects/working
git clone --no-local --no-checkout "$source_checkout" "$project"
git -C "$project" switch --detach "$source_commit"

(
  cd "$project"
  uv sync --locked --extra dev
  uv run --locked --no-sync python scripts/generate_all_figures.py
  uv run --locked --no-sync python scripts/run_teaching_experiments.py
)
```

Run both stages from the Template root with its own environment.

```bash
uv run --locked --no-sync --python 3.14 python scripts/pipeline/stage_03_render.py \
  --project working/ActiveInferenceSynthetic
uv run --locked --no-sync --python 3.14 python scripts/pipeline/stage_04_validate.py \
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
After source edits, use the render command above so hydration runs on the current sources.
Stage 04 validates the generated artifacts and writes
`output/reports/rendered_provenance.json`, binding source, configuration,
composition, and output fingerprints. A successful render alone does not replace
this validation receipt or visual review of the actual PDF and HTML.

Inspect `output/pdf/ActiveInferenceSynthetic_combined.pdf` and
`output/web/index.html` in the project checkout. The [lecture](lecture.md)
retains its separate frozen sources and delivery receipt.

Do not edit generated files under `output/pdf/`, `output/web/`, or
`output/figures/`; change sources and rerun the relevant stage.
