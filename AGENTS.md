# ActiveInferenceSynthetic — AGENTS.md

Educational Active Inference overview project (private sidecar, symlinked from
`projects/working/ActiveInferenceSynthetic` in the template checkout).

## Layer contract

| Surface | Rule |
| --- | --- |
| `src/` | Pure numerical cores and figure builders — no `infrastructure` imports |
| `scripts/` | Thin orchestrators; may import `src/` and (for preflight) `infrastructure/` |
| `formal/` | Lean 4 proofs; independent of Python runtime |
| `tests/` | Real computation only; no mock frameworks |
| `docs/` | Guides plus `docs/manuscript/` — the authored manuscript sources |
| `data/` | Versioned inputs only (`claim_ledger.yaml`); never pipeline output |
| `output/` | Disposable generated artifacts; regenerate, never hand-edit |

Per-directory guides: [`src/`](src/AGENTS.md), [`src/figures/`](src/figures/AGENTS.md),
[`scripts/`](scripts/AGENTS.md), [`tests/`](tests/AGENTS.md),
[`formal/`](formal/AGENTS.md),
[`formal/ActiveInferenceFormal/`](formal/ActiveInferenceFormal/AGENTS.md),
[`formal/ActiveInferenceFormalℤ/`](formal/ActiveInferenceFormalℤ/AGENTS.md),
[`docs/`](docs/AGENTS.md), [`docs/manuscript/`](docs/manuscript/AGENTS.md),
[`data/`](data/AGENTS.md). Every one of those directories also carries a
`README.md` quick reference alongside its `AGENTS.md`.

## Root files

| File | Role |
| --- | --- |
| `README.md` / `AGENTS.md` | Project overview / this guide |
| `STANDALONE.md` | Which surfaces are self-contained vs template-dependent |
| `ISA.md` | Ideal-state artifact — purpose and completion criteria |
| `TODO.md` | Remaining candidate directions |
| `pyproject.toml` / `uv.lock` | Package metadata, dependencies, tool config |
| `experiment_plan.yaml` | Declared conditions, metrics, and expected figures |
| `domain_profile.yaml` | Domain, required packages, validation gates, output formats |
| `CITATION.cff`, `codemeta.json`, `.zenodo.json` | Citation and archival metadata |

## Source modules (`src/`)

| Module | Role |
| --- | --- |
| `_prob.py` | Shared probability-vector validation and KL |
| `ou_model.py` | `IsotropicOU` — precision/gamma/omega flow model |
| `demos.py` | Shared demonstration parameters for figures and tests |
| `free_energy_flow.py` | Gaussian free energy and Helmholtz flow field |
| `generative_model.py` | Discrete generative model, VFE, `BeliefDescent` |
| `trajectories.py` | RK4 integration, net rotation |
| `expected_free_energy.py` | One-step EFE, pragmatic/epistemic value, `PolicySelection` |
| `policy_planning.py` | Multi-step policies, `MultiStepSelection` (not re-exported by `src/__init__.py`) |
| `markov_blanket.py` | Gaussian blanket / partial correlation |
| `steady_state.py` | NESS current, entropy production |
| `figures/` | Matplotlib figure builders + `render_all()` |
| `project_paths.py` | `project_output_dirs()` |
| `manuscript_variables.py` | Live `{{TOKEN}}` map from demos + cores |

## Scripts

| Script | Output |
| --- | --- |
| `generate_all_figures.py` | All seven PNGs + hydrate manuscript tokens |
| `z_generate_manuscript_variables.py` | `output/data/manuscript_variables.json` + `output/manuscript/` |
| `generate_overview_figure.py` | `active_inference_overview.png` |
| `generate_belief_update_figure.py` | `belief_update.png` |
| `generate_trajectory_figure.py` | `worked_trajectories.png` |
| `generate_efe_figure.py` | `expected_free_energy.png` |
| `generate_policy_planning_figure.py` | `policy_planning.png` |
| `generate_markov_blanket_figure.py` | `markov_blanket.png` |
| `generate_steady_state_figure.py` | `steady_state_current.png` |
| `00_preflight.py` | Manuscript preflight via infrastructure |

## Commands

```bash
# From project root (private sidecar or template symlink):
uv sync
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/generate_all_figures.py
uv run python scripts/z_generate_manuscript_variables.py

# Lint and type-check (ruff and mypy come from the template's dev group, not
# from this project's pyproject.toml — run them where that group is installed):
uv run ruff check src scripts tests
uv run mypy src

# Render PDF from template checkout (cwd = the template repo root):
uv run python scripts/pipeline/stage_03_render.py --project working/ActiveInferenceSynthetic

# Lean formal layer (cwd = formal/):
cd formal && lake update && lake build          # both surfaces; ℝ needs fep_lean
cd formal && lake build ActiveInferenceFormalℤ  # ℤ surface alone, no dependencies
```

`pyproject.toml` declares `numpy`, `matplotlib`, `pyyaml` plus a `dev` extra of
`pytest` / `pytest-cov`; `[tool.ruff]` and the 90% branch-coverage gate are
configured here, but the ruff and mypy binaries themselves are not.

## Version

Manuscript and package version: **0.5.0** (`docs/manuscript/config.yaml`, `pyproject.toml`).
