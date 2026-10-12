# `tests/` — AGENTS.md

No mock frameworks. Every assertion uses real numerics or subprocess/tool execution.

## Module map

| Test file | Covers |
| --- | --- |
| `test_prob.py` | `src/_prob.py` |
| `test_ou_model.py` | `src/ou_model.py` |
| `test_free_energy_flow.py` | `src/free_energy_flow.py` |
| `test_generative_model.py` | `src/generative_model.py` |
| `test_trajectories.py` | `src/trajectories.py` |
| `test_expected_free_energy.py` | `src/expected_free_energy.py` |
| `test_markov_blanket.py` | `src/markov_blanket.py` |
| `test_steady_state.py` | `src/steady_state.py` |
| `test_figures.py` | `src/figures/` |
| `test_generate_overview_figure.py` | `scripts/generate_overview_figure.py` |
| `test_generate_demonstration_figures.py` | The six other `scripts/generate_*_figure.py` wrappers |
| `test_preflight_standalone.py` | `scripts/00_preflight.py` outside a template checkout |
| `test_manuscript_variables.py` | `src/manuscript_variables.py` |
| `test_policy_planning.py` | `src/policy_planning.py` |
| `test_formal_lean.py` | `formal/` Lean sources + real `lake build` |
| `test_project_paths.py` | `src/project_paths.py` |

New behavioral tests cover `synthetic_agent`, `hierarchical_model`,
`planning_bridge`, and the exact canonical native Gaussian fixture. Formal tests
check both new adapters and their negative controls. Figure/script tests cover
all registered PNGs.

## Running

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
```

`conftest.py` forces `MPLBACKEND=Agg` and adds only the project root and `src/`
to `sys.path`. No template discovery is needed. `test_standalone_collection.py`
exercises a real pytest subprocess with numerical code in a checkout without
infrastructure. `test_formal_lean.py` checks the immutable upstream dependency,
complete axiom output, boundary witnesses, and native rejection of a false claim.

Figure tests monkeypatch `src.project_paths._DEFAULT_ROOT` to a `tmp_path`, so a
test run never writes into the real `output/` tree.

## Conventions

See [`PATTERNS.md`](PATTERNS.md). In short: no mock frameworks, compare against
independent formulas or hand calculations, assert invariants (normalization,
orthogonality, detailed-balance limits), and exercise script wrappers through
their real `main()`.

## See Also

- [`../src/AGENTS.md`](../src/AGENTS.md) — the modules under test
- [`../src/figures/AGENTS.md`](../src/figures/AGENTS.md) — the `build_figure()`/`render()` split that makes figures testable
- [`../formal/AGENTS.md`](../formal/AGENTS.md) — what `test_formal_lean.py` audits
- [`../docs/testing_philosophy.md`](../docs/testing_philosophy.md) — why the suite is built this way
