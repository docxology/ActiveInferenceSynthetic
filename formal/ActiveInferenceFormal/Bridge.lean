/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/

/-!
# Bridge between three evidence surfaces

This module maps every lemma across the three surfaces --- Python ℝ (src/),
formal ℤ (GeometryZ, InformationZ), and formal ℝ (fep_lean) --- so the
manuscript's scientific claims are traceable to their formal machine-checked
counterpart and their quantitative Python demonstration.

## The three surfaces

| Layer | Domain | Tool | Dependency | Builds in |
|-------|--------|------|------------|-----------|
| Python | ℝ (float) | NumPy, matplotlib | — | seconds |
| Formal (ℤ) | ℤ (Int) | Lean core | no mathlib | seconds |
| Formal (ℝ) | ℝ (Real) | Lean + mathlib | fep_lean (3 GB) | minutes |

Each layer proves the same mathematical structures:

| Claim | Python demo | ℤ formal | ℝ formal (fep_lean) |
|-------|-------------|--------------|---------------------------|
| Gibbs' inequality (KL ≥ 0) | — | `relEntropy_nonneg` | `finiteKL_nonneg` |
| VFE bounds surprise | `src/generative_model.py` | `freeEnergy_ge_surprise` | `outcomeSurprisal_le_variationalFreeEnergy` |
| Solenoidal current does no work | `src/free_energy_flow.py` | `solenoidal_orthogonal` | `solenoidal_orthogonal` (FepSketches.ness_flow) |
| Detailed balance iff ω=0 | `src/free_energy_flow.py` | `detailed_balance_iff` | `detailed_balance_iff` (FepSketches.ness_flow) |
| Entropy production ≥ 0 | `src/steady_state.py` | `entropyProduction_nonneg` | `entropyProduction_nonneg` (FepSketches.ness_flow) |
| EFE = -(E[ln P] + I(s;o)) | `src/expected_free_energy.py` | — | `expectedFreeEnergy_eq_negPragmaticValuePlusEpistemicValue` |
| Markov blanket | `src/markov_blanket.py` | — | `conditional_internal_external_factorization` |
-/

namespace ActiveInferenceFormal.Bridge

/-!
## How to read this bridge

Each section below names one structural claim and lists every surface that
proves it.  The ℤ theorem is named (with its module and namespace), the
ℝ theorem is named (with its fep_lean module), and the Python line
reference is given.  All three use the same notation.

### Notation key

| Symbol | ℤ meaning | ℝ meaning | Python meaning |
|--------|---------------|---------------|----------------|
| `g = ∇F` | integer vector | `Fin 2 → ℝ` | 2-D numpy array |
| `ω` | integer | real | `float` |
| `γ` | integer | real | `float` |
| `D(q‖r)` | integer sum | ℝ sum | float sum |
| `F[q]` | integer sum | ℝ sum | float sum |
-/

end ActiveInferenceFormal.Bridge
