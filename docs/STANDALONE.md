# Standalone paper and execution boundaries

Synthetic owns its paper, numerical examples, figures, tests, and publication
metadata. Linking it into the research template as
`projects/working/ActiveInferenceSynthetic` is an optional publication arrangement.
The [positioning guide](positioning.md) defines its relationship to `fep_formal`.

## Independent Python workflow

```bash
uv sync --locked --extra dev
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/generate_all_figures.py
```

Test collection requires only this checkout. After rendering the figures,
`generate_all_figures.py` calls the
[variable script](../scripts/z_generate_manuscript_variables.py). The project's
hydrator resolves `{{TOKEN}}` values from the numbered sections in
`docs/manuscript/` and writes `output/manuscript/` in both standalone and
Template-registered checkouts. Neither Python numerics nor generation imports
the upstream mathematical package.

The full pytest suite runs native formal checks if Lake is installed. The
formal prerequisites below must therefore be prepared for a zero-skip full run.
A machine without Lake can run the numerical checks, but skipped native checks
must be reported as unverified.

## External formal library

`formal/` imports `FepSketches` from a pinned `fep_formal` main revision. Lake
acquires the checkout and matching Mathlib dependencies into this project's own
`.lake/`; it does not need the neighboring upstream checkout. Follow
[formal/README.md](developer/formal.md) for toolchain setup, cache acquisition, build,
and axiom audit. First-run downloads require network access and substantial disk
space. The mathematical library is external; the paper is independently authored.

## Template publication tooling

`scripts/00_preflight.py`, PDF/HTML rendering and validation, pipeline discovery,
and final output copying use the research template. Stage 03 calls the project's
variable script before rendering. Stage 04 validates the rendered outputs.
From the template root:

```bash
uv run python scripts/pipeline/stage_03_render.py \
  --project working/ActiveInferenceSynthetic
```

Publish the paper through its own repository. Reused results retain upstream
attribution and revision; generic theorem changes belong upstream. Generated
paper outputs require separate review after source changes.


## Installed package and optional specification layer

`uv sync` installs the Python namespace `active_inference_synthetic`; use
`from active_inference_synthetic.synthetic_agent import synthetic_agent_demo`.
The repository's development scripts and tests still use local `src` imports.
`FepSketches` is acquired by Lake in the independent Lean workspace.
`fep_lean` and `gnn` are not Python runtime dependencies. Authored GNN inputs and the optional real-parser bridge are documented in
[the specification guide](gnn_specifications.md). Numerical execution does
not depend on GNN and parser success does not establish backend equivalence.
