# Scripts

Thin command-line orchestrators over `src/`. Each script does only path
bootstrap, logging, and a single delegated call; all numerics and plotting
live in `src/`.

| Script | Purpose | Delegates to | Run command |
| --- | --- | --- | --- |
| `generate_all_figures.py` | All ten figures, then the variables + hydration tail | `src.figures.render_all.render_all`; tail via `z_generate_manuscript_variables.py` | `uv run python scripts/generate_all_figures.py` |
| `generate_overview_figure.py` | `active_inference_overview.png` | `src.figures.overview.render` | `uv run python scripts/generate_overview_figure.py` |
| `generate_belief_update_figure.py` | `belief_update.png` | `src.figures.belief.render` | `uv run python scripts/generate_belief_update_figure.py` |
| `generate_trajectory_figure.py` | `worked_trajectories.png` | `src.figures.trajectories_figure.render` | `uv run python scripts/generate_trajectory_figure.py` |
| `generate_efe_figure.py` | `expected_free_energy.png` | `src.figures.efe.render` | `uv run python scripts/generate_efe_figure.py` |
| `generate_policy_planning_figure.py` | `policy_planning.png` | `src.figures.policy_planning.render` | `uv run python scripts/generate_policy_planning_figure.py` |
| `generate_markov_blanket_figure.py` | `markov_blanket.png` | `src.figures.blanket.render` | `uv run python scripts/generate_markov_blanket_figure.py` |
| `generate_steady_state_figure.py` | `steady_state_current.png` | `src.figures.steady_state.render` | `uv run python scripts/generate_steady_state_figure.py` |
| `z_generate_manuscript_variables.py` | `output/data/manuscript_variables.json` + hydrated `output/manuscript/`; prefers the template injector when importable | `src.manuscript_variables`; `infrastructure.rendering.manuscript_injection` when available | `uv run python scripts/z_generate_manuscript_variables.py` |
| `00_preflight.py` | Manuscript preflight; needs the template checkout and exits `2` without it | `infrastructure.rendering.preflight.run_manuscript_preflight` | `uv run python scripts/00_preflight.py` |

## More information

`run_teaching_experiments.py` emits a source-bound decision-value report with
informative, uninformative and irrelevant-payoff controls.
`generate_decision_value_figure.py` renders the corresponding accuracy sweep.

See [AGENTS.md](AGENTS.md) for the thin-orchestrator contract, the import
bootstrap, and gotchas; [CONVENTIONS.md](CONVENTIONS.md) for the rules every
script follows.

The closed-loop and hierarchical panels are built by
`src/figures/synthetic_agent.py` and `src/figures/hierarchy.py`, with the thin
`generate_synthetic_agent_figure.py` and `generate_hierarchy_figure.py` scripts.
