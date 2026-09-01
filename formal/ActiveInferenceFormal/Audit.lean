/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/
import ActiveInferenceFormal.Geometry
import ActiveInferenceFormal.Information
import ActiveInferenceFormalℤ.GeometryZ
import ActiveInferenceFormalℤ.InformationZ
import ActiveInferenceFormalℤ.Sanity

/-!
# Axiom audit — ℝ-valued (fep_lean) and ℤ-valued (legacy)

## ℝ-valued theorems (fep_lean imports)
These use mathlib (which depends on the axiom of choice), so they print
`Choice` and `Quot` axioms — the standard mathlib footprint.

## ℤ-valued theorems (legacy)
A clean build emits only Lean's standard trusted axioms
(`propext`, `Classical.choice`, `Quot.sound`) — and never `sorryAx`.
That is the machine-checked guarantee that these results are
proved, not assumed, and depend on no external (mathlib) axioms.
-/

namespace ActiveInferenceFormal

-- ℝ Geometry (exposition from fep_lean)
#print axioms ℝ_solenoidal_orthogonal
#print axioms ℝ_flow_work_eq_dissipation
#print axioms ℝ_detailed_balance_iff
#print axioms ℝ_entropyProduction_nonneg
#print axioms ℝ_entropyProduction_eq_zero_iff

-- ℝ Information (exposition from fep_lean)
#print axioms ℝ_finiteKL_nonneg
#print axioms ℝ_finiteKL_eq_zero_iff
#print axioms ℝ_entropy_nonneg
#print axioms ℝ_surprisal_le_VFE
#print axioms ℝ_EFE_decomposition

end ActiveInferenceFormal

namespace ActiveInferenceFormalℤ

-- ℤ Geometry
#print axioms Vec2.solenoidal_orthogonal
#print axioms Vec2.flow_work_eq_dissipation
#print axioms Vec2.detailed_balance_iff
#print axioms Vec2.entropyProduction_nonneg
#print axioms Vec2.entropyProduction_zero_iff

-- ℤ Information
#print axioms relEntropy_nonneg
#print axioms freeEnergy_eq_surprise_add_relEntropy
#print axioms freeEnergy_ge_surprise
#print axioms freeEnergy_ge_surprise_of_model
#print axioms freeEnergy_eq_surprise_at_posterior

-- ℤ Non-vacuity witnesses
#print axioms relEntropy_can_be_negative
#print axioms okL_gibbs_holds
#print axioms okL_bound_holds
#print axioms okL_bound_is_strict

end ActiveInferenceFormalℤ
