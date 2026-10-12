# `src/` — README

Numerical cores and figure builders for the Active Inference overview. Every
number in the manuscript, every figure, and every Lean theorem statement traces
back to a module here.

## Quick start

```python
from src import minimize_free_energy, posterior
from src.demos import BELIEF_OBS, LIKELIHOOD, PRIOR

descent = minimize_free_energy(LIKELIHOOD, PRIOR, BELIEF_OBS)
descent.beliefs[-1]        # converged belief — equals posterior(...)
descent.free_energy[-1]    # the surprise it bounds, at the posterior
```

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90   # from the project root
```

## Key features

- **Deterministic.** No RNG anywhere in the cores; every demonstration is
  reproducible byte-for-byte.
- **Single source of numbers.** `demos.py` holds the shared parameters that the
  figures, the tests, and the manuscript `{{TOKEN}}` values all consume.
- **Typed results.** Multi-field returns are frozen dataclasses
  (`BeliefDescent`, `PolicySelection`, `MultiStepSelection`, `PolicyEvaluation`).
- **No infrastructure coupling.** `src/` never imports the template
  `infrastructure` package. Only two scripts touch it:
  `scripts/00_preflight.py` (required) and
  `scripts/z_generate_manuscript_variables.py` (optional, with a standalone
  fallback).

## Modules

| Module | Role |
| --- | --- |
| `_prob.py` | Probability-vector validation and KL divergence |
| `ou_model.py` | `IsotropicOU` — `precision`, `gamma`, `omega` |
| `demos.py` | Shared demonstration parameters |
| `free_energy_flow.py` | Gaussian free energy, gradient, Helmholtz flow field |
| `generative_model.py` | Discrete generative model, VFE, `BeliefDescent` |
| `trajectories.py` | RK4 integration, net rotation |
| `expected_free_energy.py` | One-step EFE, pragmatic/epistemic value, `PolicySelection` |
| `policy_planning.py` | Multi-step policies, `MultiStepSelection` |
| `markov_blanket.py` | Gaussian blanket, partial correlation |
| `steady_state.py` | NESS current, entropy-production rate |
| `project_paths.py` | `project_output_dirs()` |
| `manuscript_variables.py` | Live `{{TOKEN}}` map and manuscript hydration |
| [`figures/`](figures/README.md) | Matplotlib builders for the ten figures |

The package-level public API is whatever [`__init__.py`](__init__.py)
re-exports; `policy_planning`, `project_paths`, and `manuscript_variables` are
imported from their own modules.

## More information

- [AGENTS.md](AGENTS.md) — module contracts and the full export surface
- [STYLE.md](STYLE.md) — source conventions
- [`figures/AGENTS.md`](figures/AGENTS.md) — the figure builder contract

Additional teaching cores: `synthetic_agent.py` (observation-sensitive commitment),
`hierarchical_model.py` (exact two-level inference), and `planning_bridge.py`
(normalized history carrier). Canonical native Gaussian fixture arrays live in
`demos.py` alongside the original numerical blanket fixture.
