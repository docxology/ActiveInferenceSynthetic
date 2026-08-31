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
| `test_generate_*.py` / `test_preflight_standalone.py` | Script smoke tests |
| `test_manuscript_variables.py` | `src/manuscript_variables.py` |
| `test_policy_planning.py` | `src/policy_planning.py` |
| `test_formal_lean.py` | `formal/` Lean sources + real `lake build` |
| `test_project_paths.py` | `src/project_paths.py` |

## Running

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
```

`conftest.py` locates the template repo (sibling `template/` checkout) when the
project runs from the private sidecar.
