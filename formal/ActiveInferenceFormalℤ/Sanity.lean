/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/
import ActiveInferenceFormalℤ.InformationZ

/-!
# Non-vacuity witnesses for the ℤ-valued formal surface

Every theorem in the legacy ℤ surface (``InformationZ``, ``GeometryZ``)
has a concrete witness that its hypotheses are satisfiable and necessary.
These are the formal analogue of positive and negative controls in an
experiment: they prove the theorems are genuine, not vacuous.

The ℤ theorems are also proved in the ℝ-valued exposition modules
(``Geometry``, ``Information``) via fep_lean imports, but the ℤ witnesses
are kept here as a separate curiosity.
-/

namespace ActiveInferenceFormalℤ

open ActiveInferenceFormalℤ

/-! ## Negative control — the tangent hypothesis is necessary -/

/-- A concrete "anti-log", increasing the wrong way, so it breaks the tangent bound. -/
def badL : Int → Int := fun n => if n = 1 then 10 else 0

/-- With `q = (3,1)`, `r = (1,3)` (equal totals) and `badL`, relative entropy is
`-20 < 0`. So `relEntropy_nonneg`'s conclusion fails for a function that violates
the tangent bound — the hypothesis is necessary, not decoration. -/
theorem relEntropy_can_be_negative : relEntropy badL 3 1 1 3 = -20 := by decide

/-! ## Positive control — a genuine generative model satisfies the hypotheses -/

/-- The 2-adic valuation on `{1,2,4,8}` — a genuinely log-additive function. -/
def okL : Int → Int := fun n =>
  if n = 8 then 3 else if n = 4 then 2 else if n = 2 then 1 else 0

/-- The joints are real products: `j₀ = r₀ · E` (`4 = 2·2`). -/
theorem okL_joint0 : (4 : Int) = 2 * 2 := by decide

/-- The joints are real products: `j₁ = r₁ · E` (`8 = 4·2`). -/
theorem okL_joint1 : (8 : Int) = 4 * 2 := by decide

/-- The tangent bound holds at the first point for `okL`. -/
theorem okL_tangent0 : (4 : Int) - 2 ≤ 4 * (okL 4 - okL 2) := by decide

/-- The tangent bound holds at the second point for `okL`. -/
theorem okL_tangent1 : (2 : Int) - 4 ≤ 2 * (okL 2 - okL 4) := by decide

/-- Genuine log-additivity of the joint: `okL (r₀·E) = okL r₀ + okL E`. -/
theorem okL_log0 : okL (2 * 2) = okL 2 + okL 2 := by decide

/-- Genuine log-additivity of the joint: `okL (r₁·E) = okL r₁ + okL E`. -/
theorem okL_log1 : okL (4 * 2) = okL 4 + okL 2 := by decide

/-- The general Gibbs theorem fires on the witness. -/
theorem okL_gibbs_holds : 0 ≤ relEntropy okL 4 2 2 4 :=
  relEntropy_nonneg okL 4 2 2 4 okL_tangent0 okL_tangent1 (by decide)

/-- The generative-model bound fires on the witness. -/
theorem okL_bound_holds :
    (4 + 2) * surprise okL 2 ≤ freeEnergy okL 4 2 (2 * 2) (4 * 2) :=
  freeEnergy_ge_surprise_of_model okL 4 2 2 4 2
    okL_tangent0 okL_tangent1 okL_log0 okL_log1 (by decide)

/-- The witness numbers are exactly as claimed. -/
theorem okL_bound_is_strict :
    (4 + 2) * surprise okL 2 = -6 ∧ freeEnergy okL 4 2 (2 * 2) (4 * 2) = -4 := by
  constructor <;> decide

end ActiveInferenceFormalℤ
