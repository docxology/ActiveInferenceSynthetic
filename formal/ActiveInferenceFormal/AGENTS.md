# `formal/ActiveInferenceFormal/` — AGENTS.md

The **ℝ surface** of the Lean 4 development: the manuscript-canonical,
machine-checked statements, imported and re-exported from the companion
**fep_lean** library (package `FepSketches`, mathlib-backed). Plus the bridge
documentation and the axiom audit that cover *both* surfaces.

The sibling package [`../ActiveInferenceFormalℤ/`](../ActiveInferenceFormalℤ/AGENTS.md)
holds the legacy ℤ surface, which proves the same structural statements from
Lean core alone.

## Files

| File | Content |
| --- | --- |
| `Geometry.lean` | ℝ Bayesian-mechanics flow geometry — imports `FepSketches.ness_flow` |
| `Information.lean` | ℝ perception / free-energy bound / EFE — imports `FepSketches.finite_information`, `FepSketches.finite_probability`, `FepSketches.active_inference` |
| `Bridge.lean` | Documentation-only module mapping the three evidence surfaces (Python ℝ, formal ℤ, formal ℝ) onto one another |
| `Audit.lean` | `#print axioms` over every headline theorem on both surfaces |

The library root is [`../ActiveInferenceFormal.lean`](../ActiveInferenceFormal.lean),
one directory up; it imports all four modules here plus all three in
`ActiveInferenceFormalℤ/`.

## Theorems re-exported by `Geometry.lean`

All in namespace `ActiveInferenceFormal`, all `ℝ_`-prefixed to mark the surface:

| Theorem | Statement |
| --- | --- |
| `ℝ_solenoidal_orthogonal` | The antisymmetric current `Q g` is orthogonal to the gradient `g` |
| `ℝ_flow_work_eq_dissipation` | The work of the full flow is exactly `-γ‖g‖²` |
| `ℝ_freeEnergy_non_increasing` | For `0 ≤ γ`, free energy is non-increasing along the flow |
| `ℝ_detailed_balance_iff` | For a non-zero gradient, the current vanishes iff `ω = 0` |
| `ℝ_entropyProduction_nonneg` | Entropy production is `≥ 0` |
| `ℝ_entropyProduction_eq_zero_iff` | Entropy production is `= 0` exactly at `ω = 0` |

## Theorems re-exported by `Information.lean`

| Theorem | Statement |
| --- | --- |
| `ℝ_finiteKL_nonneg` | Gibbs' inequality — relative entropy `≥ 0` |
| `ℝ_finiteKL_self` | Relative entropy of a law with itself is zero |
| `ℝ_finiteKL_eq_zero_iff` | Relative entropy vanishes iff the laws agree |
| `ℝ_entropy_nonneg` | Shannon entropy of a finite law is `≥ 0` |
| `ℝ_surprisal_le_VFE` | Variational free energy upper-bounds surprisal |
| `ℝ_VFE_at_posterior` | The bound is tight at the Bayesian posterior |
| `ℝ_negative_VFE_le_logEvidence` | Negative free energy is an evidence lower bound |
| `ℝ_EFE_decomposition` | Expected free energy splits into pragmatic and epistemic parts |
| `ℝ_EFE_minimizer_exists` | A minimising policy exists over the finite policy set |
| `ℝ_epistemicValue_nonneg` | Epistemic value is `≥ 0` |

## Build

```bash
cd formal && lake update && lake build   # from the project root
```

This surface needs the fep_lean checkout at the relative path declared in
[`../lakefile.lean`](../lakefile.lean). Without it, `lake build` of the
`ActiveInferenceFormal` target fails; the `ActiveInferenceFormalℤ` target still
builds standalone.

## Axioms

ℝ theorems carry the standard mathlib footprint (they print `Classical.choice`,
`propext`, `Quot.sound`). `Audit.lean` prints the exact set for each headline
result. `sorryAx` must never appear — `tests/test_formal_lean.py` greps the
sources for `sorry`/`admit` and inspects the audit output of a real `lake build`.

## Editing rules

- Keep the `ℝ_` prefix on every re-exported theorem; it is how the manuscript,
  `Audit.lean`, and the tests distinguish the two surfaces.
- Do not prove new mathematics here. Substantive ℝ proofs belong upstream in
  fep_lean; this package is the expositional re-export layer.
- Changing a theorem statement means updating the ℤ counterpart, the Python core
  it corresponds to, and the correspondence table in `Bridge.lean` together.

## See Also

- [`../AGENTS.md`](../AGENTS.md) — the `formal/` package as a whole
- [`../README.md`](../README.md) — what is proved, and why ℤ exists at all
- [`../ActiveInferenceFormalℤ/AGENTS.md`](../ActiveInferenceFormalℤ/AGENTS.md) — the legacy ℤ surface
- [`../../docs/manuscript/07_formal_verification.md`](../../docs/manuscript/07_formal_verification.md) — the manuscript section this backs
