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

## Source modules (`src/`)

| Module | Role |
| --- | --- |
| `_prob.py` | Shared probability-vector validation and KL |
| `ou_model.py` | `IsotropicOU` — precision/gamma/omega flow model |
| `demos.py` | Shared demonstration parameters for figures and tests |
| `free_energy_flow.py` | Gaussian free energy and Helmholtz flow field |
| `generative_model.py` | Discrete generative model, VFE, `BeliefDescent` |
| `trajectories.py` | RK4 integration, net rotation |
| `expected_free_energy.py` | EFE, pragmatic/epistemic value, `PolicySelection` |
| `markov_blanket.py` | Gaussian blanket / partial correlation |
| `steady_state.py` | NESS current, entropy production |
| `figures/` | Matplotlib figure builders + `render_all()` |
| `project_paths.py` | `project_output_dirs()` |

## Scripts

| Script | Output |
| --- | --- |
| `generate_all_figures.py` | All six PNGs under `output/figures/` |
| `generate_overview_figure.py` | `active_inference_overview.png` |
| `generate_belief_update_figure.py` | `belief_update.png` |
| `generate_trajectory_figure.py` | `worked_trajectories.png` |
| `generate_efe_figure.py` | `expected_free_energy.png` |
| `generate_markov_blanket_figure.py` | `markov_blanket.png` |
| `generate_steady_state_figure.py` | `steady_state_current.png` |
| `00_preflight.py` | Manuscript preflight via infrastructure |

## Commands

```bash
# From project root (private sidecar or template symlink):
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/generate_all_figures.py

# Render PDF from template checkout:
uv run python scripts/pipeline/stage_03_render.py --project working/ActiveInferenceSynthetic

# Lean formal layer:
cd formal && lake build
```

## Version

Manuscript and package version: **0.5.0** (`manuscript/config.yaml`, `pyproject.toml`).
