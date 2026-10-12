# Paper-specific real-valued exposition

Selected `FepSketches` results, concrete boundary witnesses, correspondence
notes, and an axiom audit. The generic library is maintained by `fep_formal`.

Every name below is in namespace `ActiveInferenceFormal` and appears in
`Audit.lean` and the source/native test inventory.

| Adapter | Qualified principal declaration | Contract |
| --- | --- | --- |
| `GaussianBlanket.lean` | `ActiveInferenceFormal.ℝ_canonical_precision_entries` | Exact `Fin 4` transport of the upstream named-axis precision |
| `GaussianBlanket.lean` | `ActiveInferenceFormal.ℝ_canonical_gaussian_blanket` | Native Gaussian conditional independence plus marginal covariance `1/24` |
| `GaussianBlanket.lean` | `ActiveInferenceFormal.ℝ_canonical_conditional_rows` | Product endpoint conditional kernels, each variance `1/4` |
| `GaussianBlanket.lean` | `ActiveInferenceFormal.ℝ_coupled_gaussian_not_independent` | Coupled bivariate Gaussian negative control |
| `Planning.lean` | `ActiveInferenceFormal.ℝ_twoStep_terminal_history_bridge` | Upstream normalized history EFE equals terminal/history EFE plus `log 2` |
| `Planning.lean` | `ActiveInferenceFormal.cumulative_terminal_counterexample` | Static cumulative EFE differs from terminal-payoff EFE |
| `Planning.lean` | `ActiveInferenceFormal.revealing_history_information` | Repeating a perfect observation reveals one fair bit |

The planning source also exposes exact history predictive/posterior masses,
the fair zero-information witness and both terminal EFE evaluations. Read
the exact matrices, support assumptions and exclusions in [formal setup](../README.md)
before claiming a correspondence to another numerical example.

See [formal setup](../README.md) for the pinned dependency and commands,
[the section map](../../docs/positioning.md) for mathematical scope, and
[AGENTS.md](AGENTS.md) for editing rules.
