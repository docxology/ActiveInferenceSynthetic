# Formal verification (Lean 4)

A self-contained Lean 4 formalization of the mathematical core of *Active
Inference — A Synthetic Overview*. It machine-checks the theorems the Python
`src/` demonstrates numerically, from Lean's core axioms alone — **no mathlib,
no `sorry`**.

## Build

```bash
cd formal
lake build
```

The build finishes in about a second (no dependencies to fetch or compile) and
prints, via the `Audit` module, the axiom set of each headline theorem — every
one reports exactly `depends on axioms: [propept, Quot.sound]`, never `sorryAx`
and no `Classical.choice`.

## Layout

```
lakefile.lean                        no external `require` — Lean core only
lean-toolchain                       leanprover/lean4:v4.28.0
ActiveInferenceFormal.lean           library root (imports the modules)
ActiveInferenceFormal/
  Geometry.lean                      flow / steady-state facts (over ℤ)
  Information.lean                   perception / free-energy bound (over ℤ)
  Audit.lean                         `#print axioms` on every headline theorem
```

## What is proved

**Geometry** (`§1`, `§3`, `§6`):

- `solenoidal_orthogonal` — the antisymmetric current `Q g` is orthogonal to the
  gradient `g` (it does no work against free energy).
- `flow_work_eq_dissipation` — the work of the full flow is exactly `-γ‖g‖²`; the
  solenoidal part is free, so free energy is non-increasing.
- `detailed_balance_iff` — the current vanishes iff `ω = 0`.
- `entropyProduction_nonneg` / `entropyProduction_zero_iff` — the (denominator-
  cleared) entropy-production rate is `≥ 0`, and `= 0` iff `ω = 0`.

**Information** (`§2`):

- `relEntropy_nonneg` — Gibbs' inequality (relative entropy `≥ 0`).
- `freeEnergy_eq_surprise_add_relEntropy` — the decomposition `F = surprise +
  D(q‖posterior)`.
- `freeEnergy_ge_surprise` — variational free energy is an upper bound on
  surprise.
- `freeEnergy_eq_surprise_at_posterior` — the bound is tight at the posterior.

## Design notes

- **Over ℤ, not ℝ.** The results are polynomial identities and sign facts; the
  integers suffice and keep the project dependency-free. The real-valued
  instances live in `src/`.
- **The logarithm's properties are point hypotheses — and non-vacuity is
  proved.** Gibbs' inequality needs two facts about `ln`: additivity
  (`ln(ab)=ln a+ln b`) and the tangent bound (`ln x ≤ x-1`, cleared of
  denominators as `b-a ≤ b·(L b - L a)`). Stated *universally* over ℤ these are
  unsatisfiable (integer rounding breaks the tangent bound on `{2,3}`), which
  would make the theorems vacuously true. The development instead takes them only
  at the exact points each proof consumes, and `Sanity.lean` proves both a
  **negative control** (`relEntropy_can_be_negative`: the tangent hypothesis is
  necessary) and a **positive control** (`okL`: the hypotheses are satisfiable
  and the bound fires with a real gap `-16 ≤ -14`). So the results are faithful,
  not vacuous.
- **Counts, not normalized reals.** Positive integers cannot sum to `1`, so `q`
  and `r` are counts sharing a total mass and surprise scales by that total. The
  `ℤ` development proves `total·surprise ≤ F`; the normalized `F ≥ surprise` is
  its real-valued instance (dividing through by a positive total), on the Python
  side. `freeEnergy_ge_surprise_of_model` states the bound for a genuine model
  `jᵢ = rᵢ·E` with a log-additive `L` (the positive-control witness uses the
  2-adic valuation, which is really log-additive).

The Python suite verifies this project via `tests/test_formal_lean.py` (grep for
`sorry`, presence of the non-vacuity witnesses, and a real `lake build` with an
axiom-cleanliness check).
