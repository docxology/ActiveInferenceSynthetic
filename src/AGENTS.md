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

## Modules not re-exported at package level

Import these from their module, not from `src`:

| Module | Public names |
| --- | --- |
| `policy_planning.py` | `PolicyEvaluation`, `MultiStepSelection`, `enumerate_policies`, `evaluate_policy`, `select_multistep_policy` (its own `__all__`) |
| `project_paths.py` | `resolve_project_root`, `project_output_dirs` |
| `manuscript_variables.py` | `compute_claims`, `generate_variables`, `save_variables`, `manuscript_tokens`, `hydrate_manuscript`, `leftover_tokens` |

`policy_planning.py` extends the one-step `expected_free_energy.py` currency to
short action *sequences*: terminal pragmatic value plus cumulative epistemic
value, minimised over exhaustively enumerated branches — no sampling, no RNG.
It backs §8 of the manuscript and `src/figures/policy_planning.py`.

## Internal helpers

| Module | Purpose |
| --- | --- |
| `_prob.py` | `as_prob_vector`, `as_distribution`, `as_column_stochastic`, `kl_divergence` |
| `demos.py` | Shared figure/test fixtures (`PRIOR`, `LIKELIHOOD`, `FLOW`, `ACTIONS`, `PLANNING_HORIZON`, `BLANKET_PRECISION`, …) |
| `figures/` | Matplotlib panels; call `render_all()` for the full manifest — see [`figures/AGENTS.md`](figures/AGENTS.md) |

## Conventions

- Deterministic: no RNG in cores.
- Typed returns: prefer `BeliefDescent` / `PolicySelection` / `MultiStepSelection`
  over bare dicts.
- `IsotropicOU` owns `precision`, `gamma`, `omega`; steady-state paths require `gamma > 0`.
- Cores never import matplotlib; drawing lives in `figures/` only.
- `src/` never imports the template `infrastructure` package.

Full conventions: [`STYLE.md`](STYLE.md).

## See Also

- [`figures/AGENTS.md`](figures/AGENTS.md) — the figure builders
- [`../scripts/AGENTS.md`](../scripts/AGENTS.md) — the thin orchestrators over this package
- [`../tests/AGENTS.md`](../tests/AGENTS.md) — the test-to-module map
- [`../docs/architecture.md`](../docs/architecture.md) — layer boundaries
