/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/
import ActiveInferenceFormal.Geometry
import ActiveInferenceFormal.Information
import ActiveInferenceFormal.Sanity

/-!
# Axiom audit

`#print axioms` on each headline theorem. A clean build emits, for every one, only
Lean's standard trusted axioms (`propext`, `Classical.choice`, `Quot.sound`) — and
never `sorryAx`. That is the machine-checked guarantee that these results are
proved, not assumed, and depend on no external (mathlib) axioms.
-/

namespace ActiveInferenceFormal

-- Geometry
#print axioms Vec2.solenoidal_orthogonal
#print axioms Vec2.flow_work_eq_dissipation
#print axioms Vec2.detailed_balance_iff
#print axioms Vec2.entropyProduction_nonneg
#print axioms Vec2.entropyProduction_zero_iff

-- Information
#print axioms relEntropy_nonneg
#print axioms freeEnergy_eq_surprise_add_relEntropy
#print axioms freeEnergy_ge_surprise
#print axioms freeEnergy_ge_surprise_of_model
#print axioms freeEnergy_eq_surprise_at_posterior

-- Non-vacuity witnesses (Sanity): both the negative control and the positive
-- control are themselves proved with clean axioms.
#print axioms relEntropy_can_be_negative
#print axioms okL_gibbs_holds
#print axioms okL_bound_holds
#print axioms okL_bound_is_strict

end ActiveInferenceFormal
