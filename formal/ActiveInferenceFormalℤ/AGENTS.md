# `formal/ActiveInferenceFormalℤ/` — AGENTS.md

The **legacy ℤ surface** of the Lean 4 development. It proves the same
structural statements as the ℝ surface over the integers, from Lean's core
axioms alone — no mathlib, no `sorry`, no external dependency. The point is
epistemic: the flow identities and the free-energy bound are *algebraic* facts,
not artefacts of real analysis.

The ℝ counterpart lives in
[`../ActiveInferenceFormal/`](../ActiveInferenceFormal/AGENTS.md).

## Files

| File | Content |
| --- | --- |
| `GeometryZ.lean` | ℤ Bayesian-mechanics flow identities — formal counterpart to `src/free_energy_flow.py`, `src/trajectories.py`, `src/steady_state.py` |
| `InformationZ.lean` | ℤ variational free-energy bound — formal counterpart to `src/generative_model.py` |
| `Sanity.lean` | Non-vacuity witnesses: positive and negative controls for `InformationZ` |

All three are declared as roots of the `ActiveInferenceFormalℤ` `lean_lib` in
[`../lakefile.lean`](../lakefile.lean), and are also imported by the library
root [`../ActiveInferenceFormal.lean`](../ActiveInferenceFormal.lean).

## `GeometryZ.lean`

Namespace `ActiveInferenceFormalℤ`. A two-component integer vector `Vec2` with
`dot`, `normSq`, and the flow decomposition `flow γ ω g = solenoidal ω g +
dissipative γ g`.

| Theorem | Statement |
| --- | --- |
| `normSq_nonneg` | `0 ≤ v.normSq` |
| `solenoidal_orthogonal` | `dot (solenoidal ω g) g = 0` — the current does no work against free energy |
| `flow_work_eq_dissipation` | The work of the full flow equals the dissipative part alone |
| `detailed_balance_iff` | For `g ≠ 0`, the solenoidal current vanishes iff `ω = 0` |
| `entropyProduction_nonneg` | `entropyProduction precision ω = 2·ω²·precision ≥ 0` for `0 ≤ precision` |
| `entropyProduction_zero_iff` | For `0 < precision`, it is zero exactly at `ω = 0` |

## `InformationZ.lean`

Definitions `relEntropy`, `freeEnergy`, `surprise`, all parameterised by an
abstract logarithm `L : Int → Int`.

| Theorem | Statement |
| --- | --- |
| `relEntropy_nonneg` | Gibbs' inequality |
| `relEntropy_self_zero` | Relative entropy of a law with itself is zero |
| `freeEnergy_eq_surprise_add_relEntropy` | `F = surprise + D(q‖posterior)` |
| `freeEnergy_ge_surprise` | The bound, total-scaled |
| `freeEnergy_ge_surprise_of_model` | The bound for a genuine generative model |
| `freeEnergy_eq_surprise_at_posterior` | The bound is tight at the posterior |

### Why the hypotheses are pointwise

The proofs need two properties of `ln`: additivity, and the tangent bound
`ln x ≤ x - 1`. Assumed *universally* over ℤ these are unsatisfiable, which
would make every theorem vacuously true. The development therefore takes them
only at the exact points each proof consumes. `Sanity.lean` is what closes that
hole — do not weaken it.

## `Sanity.lean`

| Declaration | Role |
| --- | --- |
| `badL`, `relEntropy_can_be_negative` | **Negative control** — without the tangent hypothesis, relative entropy really can go negative (`= -20`) |
| `okL`, `okL_joint0/1`, `okL_tangent0/1`, `okL_log0/1` | **Positive control** — a concrete `L` satisfying every hypothesis at the consumed points |
| `okL_gibbs_holds`, `okL_bound_holds`, `okL_bound_is_strict` | The theorems fire on that witness, with a real (strict) gap |

Every one of these is closed by `decide`, so they are checked by computation.

## Build

```bash
cd formal && lake build ActiveInferenceFormalℤ   # from the project root
```

This target has no dependency on fep_lean or mathlib and builds in seconds.
`lake build` alone builds both targets and therefore needs fep_lean.

## Axioms

A clean build reports only Lean's trusted core axioms for these theorems, and
never `sorryAx`. `../ActiveInferenceFormal/Audit.lean` prints the footprint;
`tests/test_formal_lean.py` audits the sources and inspects a real build.

## Editing rules

- No mathlib imports, ever. The dependency-free property *is* the contribution.
- No `sorry` / `admit`.
- Adding a theorem that consumes a new `L` fact means adding the matching
  witness to `Sanity.lean` in the same change.
- Keep statements structurally parallel to their `ℝ_`-prefixed counterparts in
  [`../ActiveInferenceFormal/`](../ActiveInferenceFormal/AGENTS.md);
  [`../ActiveInferenceFormal/Bridge.lean`](../ActiveInferenceFormal/Bridge.lean)
  — which lives on the ℝ side, not here — documents the correspondence.

## See Also

- [`../AGENTS.md`](../AGENTS.md) — the `formal/` package as a whole
- [`../README.md`](../README.md) — the two-surface design and design notes
- [`../ActiveInferenceFormal/AGENTS.md`](../ActiveInferenceFormal/AGENTS.md) — the ℝ surface
- [`../../docs/manuscript/07_formal_verification.md`](../../docs/manuscript/07_formal_verification.md) — the manuscript section this backs
