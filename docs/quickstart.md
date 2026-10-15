# Quick start

## Choose a starting point

- **Read/watch:** open the [root PDF](../ActiveInferenceSynthetic_Revised.pdf) or
  [video](../ActiveInferenceSynthetic_20min.mp4). No installation is required.
- **Run models:** use Python 3.10+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).
- **Verify native proofs:** prepare [Lean and pinned dependencies](../formal/README.md).
- **Render the paper:** use [the research template workflow](rendering_pipeline.md).
- **Replay the lecture:** extract [the frozen replay bundle](lecture.md), which
  includes recordings and its own scoped runtime.

## Install a Git checkout

```bash
git clone https://github.com/docxology/ActiveInferenceSynthetic.git
cd ActiveInferenceSynthetic
uv sync --locked --extra dev
```

Omit `--extra dev` if you only need the numerical package. Include it for the
test, lint and type tools. A plain source ZIP has no Git index; use a checkout
for `scripts/verify_publication.py`, which checks the tracked inventory.

For GitVault sessions, use the canonical mounted checkout and the runtime/cache
bindings in [the agent guide](../AGENTS.md). Keep existing checkouts and environments
intact when creating a separate verification environment.

## Run a real example

```python
from active_inference_synthetic.synthetic_agent import synthetic_agent_demo

episode = synthetic_agent_demo(observation=1)
assert episode.commitment.choice == 1
```

The informative observation changes the subsequent commitment. Use
`synthetic_agent_demo(observation=1, informative=False)` for the matched
uninformative-cue control. [Methods](methods.md) explains the carrier and limits.

## Generate outputs and check the repository

From the project root:

```bash
uv run python scripts/verify_publication.py
uv run ruff check src scripts tests
uv run mypy src
uv run python scripts/generate_all_figures.py
uv run python scripts/run_teaching_experiments.py
uv run pytest tests/ --cov=src --cov-fail-under=90
```

Figures go to `output/figures/`, hydrated sections to `output/manuscript/`,
and the source-bound decision report to `output/data/teaching_experiments.json`.
These operations do not render a new PDF or replace the root video.

When Lake is on PATH, the full suite invokes native Lean builds and
false-proposition controls. Missing Lake produces explicit skips; a present but
broken toolchain fails. The [Python CI job](../.github/workflows/README.md)
does not install Lean; prepare it separately to claim native proof verification.

## Build and verify an installed wheel

```bash
uv build --out-dir build/distributions
uv run --isolated --no-project --with build/distributions/*.whl python -c "from active_inference_synthetic.synthetic_agent import synthetic_agent_demo; assert synthetic_agent_demo(observation=1).commitment.choice == 1"
```

The Python package contains numerical/figure modules and license metadata.
The full paper, video, authored manuscript and replay inputs are distributed
through the repository and release archives rather than as Python package data.

## Render or extend

See [STANDALONE.md](../STANDALONE.md) for execution boundaries,
[CONTRIBUTING.md](../CONTRIBUTING.md) for changes and checks, and
[troubleshooting](troubleshooting.md) for failures.

Paper rendering runs from a linked `docxology/template` checkout:

```bash
uv run python scripts/pipeline/stage_03_render.py \
  --project working/ActiveInferenceSynthetic
```

Follow the full [rendering guide](rendering_pipeline.md) for prerequisites,
hydration, validation and visual inspection.
