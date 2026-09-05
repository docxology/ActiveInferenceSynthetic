# `scripts/` — AGENTS.md

Thin orchestrators. All numerics live in `src/`; scripts coordinate rendering only.

## Files

| File | Role |
| --- | --- |
| `__init__.py` | Makes `scripts` importable so tests can call each `main()` |
| `generate_all_figures.py` | All seven figures via `src.figures.render_all`, then writes `manuscript_variables.json` and hydrates `output/manuscript/` |
| `generate_overview_figure.py` | `active_inference_overview.png` |
| `generate_belief_update_figure.py` | `belief_update.png` |
| `generate_trajectory_figure.py` | `worked_trajectories.png` |
| `generate_efe_figure.py` | `expected_free_energy.png` |
| `generate_policy_planning_figure.py` | `policy_planning.png` |
| `generate_markov_blanket_figure.py` | `markov_blanket.png` |
| `generate_steady_state_figure.py` | `steady_state_current.png` |
| `z_generate_manuscript_variables.py` | `output/data/manuscript_variables.json` + hydrated `output/manuscript/` |
| `00_preflight.py` | Manuscript preflight via the template `infrastructure` package |
| `CONVENTIONS.md` | Rules every script here must follow |

## Figure generators

Each `generate_*_figure.py` delegates to `src.figures.<panel>.render()`.
`generate_all_figures.py` calls `src.figures.render_all.render_all()`.

Outputs land in `output/figures/` via `src.project_paths.project_output_dirs()`.

## Manuscript variables

`z_generate_manuscript_variables.py` calls
`src.manuscript_variables.generate_variables()`, writes
`output/data/manuscript_variables.json`, and then hydrates
`output/manuscript/`. It prefers the template's
`infrastructure.rendering.manuscript_injection.write_resolved_manuscript_tree`
when importable and falls back to the standalone
`src.manuscript_variables.hydrate_manuscript` otherwise, so it works in both the
sidecar and the template checkout. It prints both output paths.

## Import bootstrap

Every figure script inserts the project root before importing `src`:

```python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
```

That makes them runnable directly (`uv run python scripts/<name>.py`) whether
or not the project is installed. Keep the bootstrap identical when adding a
script — see [`CONVENTIONS.md`](CONVENTIONS.md).

Two files differ, deliberately:

- `z_generate_manuscript_variables.py` binds the same path to `_PROJECT_ROOT`
  first (it reuses the value later) and inserts that.
- `00_preflight.py` resolves and inserts the *template* repo root instead
  (below), not the project root.

## Preflight

`00_preflight.py` runs the manuscript preflight over `docs/manuscript/`:

1. `_find_repo_root()` walks upward from this file for the first ancestor
   containing an `infrastructure/` directory. The upward search (rather than a
   fixed `parents[N]`) is what makes it work through the
   `projects/working/<name>` symlink into the private sidecar; it uses
   `absolute()`, not `resolve()`, so the symlinked ancestors survive.
2. It inserts that root on `sys.path` and calls
   `infrastructure.rendering.preflight.run_manuscript_preflight`.

Exit codes: `0` pass, `1` preflight failure (message on stderr), `2` the
template checkout is absent or the helper cannot be imported. Running it from
the private sidecar alone therefore returns `2` by design.

## Adding a figure

1. Add builder under `src/figures/`.
2. Register in `src/figures/render_all.py`.
3. Add a thin script alias here, using the standard import bootstrap.
4. Extend `tests/test_figures.py` (manifest length and the parametrised list)
   and `tests/test_generate_demonstration_figures.py`.
5. Register the figure in
   [`../docs/manuscript/figure_registry.yaml`](../docs/manuscript/figure_registry.yaml).

## See Also

- [`CONVENTIONS.md`](CONVENTIONS.md) — rules every script must follow
- [`../src/figures/AGENTS.md`](../src/figures/AGENTS.md) — the builders these wrap
- [`../src/AGENTS.md`](../src/AGENTS.md) — the numerical cores
- [`../docs/rendering_pipeline.md`](../docs/rendering_pipeline.md) — where these fit in the render pipeline
