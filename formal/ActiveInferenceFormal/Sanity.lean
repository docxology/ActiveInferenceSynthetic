/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/
import ActiveInferenceFormal.Information

/-!
# Non-vacuity witnesses — the hypotheses are load-bearing *and* satisfiable

A conditional theorem is only meaningful if its hypotheses do real work: if they
were contradictory the result would be vacuous, and if the conclusion held
without them the hypotheses would be idle. This module pins both directions for
the information-theoretic results — the formal analogue of a known-bad probe
*and* a positive control.

* **Load-bearing (negative control).** `relEntropy_can_be_negative` exhibits a
  function and distribution for which relative entropy is `-20 < 0`; so
  `relEntropy_nonneg` genuinely needs its tangent hypotheses.
* **Satisfiable, by a genuine model (positive control).** `okL` is the 2-adic
  valuation on `{1,2,4,8}` — an *actually* log-additive function — and the
  witness is a real generative model: posterior `r = (2,4)`, evidence `E = 2`,
  and joint `j = (4,8) = (r₀·E, r₁·E)` (not hand-picked values). At it every
  hypothesis provably holds (`by decide`) and the free-energy bound fires with a
  **non-trivial** gap (`-6 ≤ -4`, the slack being the relative entropy `2`). So
  the theorems have a genuine model and are not vacuously true.
-/

namespace ActiveInferenceFormal

/-! ## Negative control — the tangent hypothesis is necessary -/

/-- A concrete "anti-log", increasing the wrong way, so it breaks the tangent
bound. -/
def badL : Int → Int := fun n => if n = 1 then 10 else 0

/-- With `q = (3,1)`, `r = (1,3)` (equal totals) and `badL`, relative entropy is
`-20 < 0`. So `relEntropy_nonneg`'s conclusion fails for a function that violates
the tangent bound — the hypothesis is necessary, not decoration. -/
theorem relEntropy_can_be_negative : relEntropy badL 3 1 1 3 = -20 := by decide

/-! ## Positive control — a genuine generative model satisfies the hypotheses

`okL` is the 2-adic valuation restricted to the points the witness uses
(`okL 1 = 0`, `okL 2 = 1`, `okL 4 = 2`, `okL 8 = 3`); it is genuinely
log-additive there (`okL (a·b) = okL a + okL b`). The model: belief `q = (4,2)`,
posterior `r = (2,4)`, evidence `E = 2`, joint `j = (r₀·E, r₁·E) = (4,8)`. -/

/-- The 2-adic valuation on `{1,2,4,8}` — a genuinely log-additive information
function. -/
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

/-- Genuine log-additivity of the joint: `okL (r₀·E) = okL r₀ + okL E`
(`okL 4 = okL 2 + okL 2`, i.e. `2 = 1 + 1`). -/
theorem okL_log0 : okL (2 * 2) = okL 2 + okL 2 := by decide

/-- Genuine log-additivity of the joint: `okL (r₁·E) = okL r₁ + okL E`
(`okL 8 = okL 4 + okL 2`, i.e. `3 = 2 + 1`). -/
theorem okL_log1 : okL (4 * 2) = okL 4 + okL 2 := by decide

/-- **Non-trivial positive control.** At `okL` the relative entropy is `2`,
strictly positive — the bound is not the degenerate `0 ≤ 0`. -/
theorem okL_relEntropy_positive : relEntropy okL 4 2 2 4 = 2 := by decide

/-- **The general Gibbs theorem fires on the witness**, discharging its
hypotheses with the concrete facts above — so `relEntropy_nonneg` is inhabited,
not vacuous. -/
theorem okL_gibbs_holds : 0 ≤ relEntropy okL 4 2 2 4 :=
  relEntropy_nonneg okL 4 2 2 4 okL_tangent0 okL_tangent1 (by decide)

/-- **The generative-model bound fires on the witness.** Instantiating
`freeEnergy_ge_surprise_of_model` with `okL` and a real model (`j = r·E`,
log-additive `L`) yields a genuine, non-vacuous inequality
(`(q0+q1)·surprise = -6 ≤ freeEnergy = -4`, the gap being the relative entropy
`2`). -/
theorem okL_bound_holds :
    (4 + 2) * surprise okL 2 ≤ freeEnergy okL 4 2 (2 * 2) (4 * 2) :=
  freeEnergy_ge_surprise_of_model okL 4 2 2 4 2
    okL_tangent0 okL_tangent1 okL_log0 okL_log1 (by decide)

/-- The witness numbers are exactly as claimed: the bound is `-6 ≤ -4`, a genuine
(strict, gap `= 2`) inequality — not `x ≤ x`. -/
theorem okL_bound_is_strict :
    (4 + 2) * surprise okL 2 = -6 ∧ freeEnergy okL 4 2 (2 * 2) (4 * 2) = -4 := by
  constructor <;> decide

end ActiveInferenceFormal
