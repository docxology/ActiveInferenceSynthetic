# `src/figures/`

Matplotlib builders for the registered manuscript figures.

## Quick start

```python
from src.figures import FIGURE_RENDERERS, render_all

manifest = render_all()                       # {filename: Path}, all registered figures
path = FIGURE_RENDERERS["belief_update.png"]()  # just one
```

```bash
uv run python scripts/generate_all_figures.py   # from the project root
```

## Key features

- Every module exposes `build_figure() -> plt.Figure` and `render() -> Path`.
- `render_all.py` holds `FIGURE_RENDERERS`, the single registry of figures.
- Okabe–Ito colourblind-safe palette in `palette.py`.
- Deterministic — no RNG, all numbers from `src.demos` and the tested cores.

## Modules

| Module | Role |
| --- | --- |
| `graphical_abstract.py` | `graphical_abstract.png` — cover |
| `synthetic_agent.py` | `synthetic_agent.png` — cue and commitment |
| `hierarchy.py` | `hierarchical_inference.png` — two-level inference |
| `overview.py` | `active_inference_overview.png` — equilibrium vs NESS flow |
| `belief.py` | `belief_update.png` — perception as VFE descent |
| `trajectories_figure.py` | `worked_trajectories.png` |
| `efe.py` | `expected_free_energy.png` — explore/exploit |
| `policy_planning.py` | `policy_planning.png` — multi-step planning |
| `blanket.py` | `markov_blanket.png` |
| `steady_state.py` | `steady_state_current.png` |
| `decision_value.py` | `value_of_information.png` — utility gain, cost and information |
| `render_all.py` | `FIGURE_RENDERERS`, `render_all()` |
| `palette.py` | Shared colour constants |
| `landscape.py` | Shared free-energy contour backdrop |
| `save.py` | `save_figure()` into `output/figures/` |

## More information

See [AGENTS.md](AGENTS.md) for the builder contract and how to add a figure.

The closed-loop and hierarchical panels are built by
`src/figures/synthetic_agent.py` and `src/figures/hierarchy.py`, with the thin
`generate_synthetic_agent_figure.py` and `generate_hierarchy_figure.py` scripts.
