# `src/` — AGENTS.md

Active Inference numerical cores and figure builders.

## Public API

Re-exported from `src/__init__.py`:

- Flow: `free_energy`, `grad_free_energy`, `flow_field`, `solenoidal_is_conservative`
- Perception: `joint`, `evidence`, `surprise`, `posterior`, `variational_free_energy`,
  `vfe_components`, `minimize_free_energy` → `BeliefDescent`
- Trajectories: `integrate_trajectory`, `free_energy_along`, `net_rotation`
- Action: `predicted_outcomes`, `predicted_posteriors`, `pragmatic_value`,
  `epistemic_value`, `expected_free_energy`, `select_policy` → `PolicySelection`
- Blanket: `covariance_from_precision`, `conditional_covariance`, `partial_correlation`,
  `correlation_matrix`, `is_markov_blanket`
- Steady state: `drift_matrix`, `stationary_covariance`, `probability_current`,
  `entropy_production_rate`, `current_circulation`
- Model: `IsotropicOU`

## Internal helpers

| Module | Purpose |
| --- | --- |
| `_prob.py` | `as_prob_vector`, `as_distribution`, `as_column_stochastic`, `kl_divergence` |
| `demos.py` | Shared figure/test fixtures (`PRIOR`, `LIKELIHOOD`, `FLOW`, …) |
| `figures/` | Matplotlib panels; call `render_all()` for the full manifest |

## Conventions

- Deterministic: no RNG in cores.
- Typed returns: prefer `BeliefDescent` / `PolicySelection` over bare dicts.
- `IsotropicOU` owns `precision`, `gamma`, `omega`; steady-state paths require `gamma > 0`.
