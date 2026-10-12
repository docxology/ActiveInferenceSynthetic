# `src/figures/` — AGENTS.md

Matplotlib builders for every manuscript figure. This package is the only place
in the project that draws; `scripts/` calls it and never draws itself, and the
numerical cores in `src/` never import matplotlib.

## Contract

Each figure module exposes exactly two functions:

| Function | Returns | Purpose |
| --- | --- | --- |
| `build_figure()` | `plt.Figure` | Compose the panels; no filesystem access |
| `render(project_root=None)` | `Path` | `build_figure()` then `save.save_figure(...)` |

Splitting the two is what makes the figures testable: `tests/test_figures.py`
can build a figure in memory and inspect it, and can render into `tmp_path`
without touching `output/`.

Figure modules pull *all* their numbers from `src.demos` and the tested cores
(`src.free_energy_flow`, `src.generative_model`, `src.expected_free_energy`,
`src.policy_planning`, `src.markov_blanket`, `src.steady_state`,
`src.trajectories`). A figure module must never re-derive a scientific quantity
locally — the same values feed the `{{TOKEN}}` hydration in
[`../manuscript_variables.py`](../manuscript_variables.py), so a private copy
would silently desynchronise the prose from the plots.

## File organization

### Figure modules (one per manuscript figure)

| Module | Output PNG | Manuscript section |
| --- | --- | --- |
| `overview.py` | `active_inference_overview.png` | §1 extended abstract |
| `belief.py` | `belief_update.png` | §2 generative model |
| `trajectories_figure.py` | `worked_trajectories.png` | §3 worked regimes |
| `efe.py` | `expected_free_energy.png` | §4 expected free energy |
| `policy_planning.py` | `policy_planning.png` | §8 planning |
| `blanket.py` | `markov_blanket.png` | §5 Markov blanket |
| `steady_state.py` | `steady_state_current.png` | §6 steady state |

### Shared support

| Module | Purpose |
| --- | --- |
| `__init__.py` | Re-exports `FIGURE_RENDERERS` and `render_all` |
| `render_all.py` | The `FIGURE_RENDERERS` name → `render` map and `render_all()` |
| `palette.py` | Okabe–Ito colourblind-safe constants: `BLUE`, `VERMILLION`, `GREEN`, `GREY`, `INK` |
| `landscape.py` | `draw_landscape()`, `style_spatial_panel()`, `draw_mode_marker()` — the shared free-energy contour backdrop |
| `save.py` | `save_figure()` — writes into `output/figures/` via `src.project_paths.project_output_dirs()` |

`render_all.py` is the registry of record. Its dict is what
`scripts/generate_all_figures.py` iterates, what `tests/test_figures.py`
enumerates, and what [`../../docs/manuscript/figure_registry.yaml`](../../docs/manuscript/figure_registry.yaml)
must agree with.

## Usage

```bash
# From the project root — every figure:
uv run python scripts/generate_all_figures.py

# One figure:
uv run python scripts/generate_overview_figure.py
```

```python
from src.figures import FIGURE_RENDERERS, render_all

manifest = render_all()               # {filename: Path} for all nine
one = FIGURE_RENDERERS["belief_update.png"]()
```

## Adding a figure

1. Add `src/figures/<name>.py` with `build_figure()` and `render()`.
2. Import it in `render_all.py` and add the `"<file>.png": <name>.render` entry.
3. Add a thin wrapper in [`../../scripts/`](../../scripts/AGENTS.md).
4. Extend `tests/test_figures.py` — it asserts the exact manifest length and
   parametrises over the per-module `render` functions, so both must be updated.
5. Register path, label, caption, and alt text in
   [`../../docs/manuscript/figure_registry.yaml`](../../docs/manuscript/figure_registry.yaml).

## Best practices

- Use `palette` constants; never a literal hex code in a figure module.
- Reuse `landscape.draw_landscape()` for any free-energy contour panel.
- Keep `build_figure()` free of I/O so it stays testable.
- Deterministic: no RNG, no timestamps, no `plt.show()`.
- Route every save through `save.save_figure()` so output paths stay uniform.

## See Also

- [`../AGENTS.md`](../AGENTS.md) — the numerical cores these builders consume
- [`../STYLE.md`](../STYLE.md) — source conventions
- [`../../scripts/AGENTS.md`](../../scripts/AGENTS.md) — the orchestrators
- [`../../tests/AGENTS.md`](../../tests/AGENTS.md) — `test_figures.py` coverage

The closed-loop and hierarchical panels are built by
`src/figures/synthetic_agent.py` and `src/figures/hierarchy.py`, with the thin
`generate_synthetic_agent_figure.py` and `generate_hierarchy_figure.py` scripts.
