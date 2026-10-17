module
/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/
public import FepSketches.ness_flow

@[expose] public section

/-!
# Bayesian-mechanics flow geometry — equilibrium vs non-equilibrium

The central dynamical claim of Bayesian Mechanics is that the flow of
beliefs and states decomposes into a dissipative (gradient-descent) part
and a solenoidal (circulating) part:

`f = (Q - Γ)∇F`

where `Γ = γ·I` is symmetric and `Q = ω·[[0,1],[-1,0]]` is antisymmetric.

At equilibrium (ω = 0) the flow is pure gradient descent and comes to rest.
Far from equilibrium (ω ≠ 0) a persistent probability current circulates
along the level sets of free energy in the stated stochastic model.

## Source of theorems

Every theorem in this module is proved in the companion **fep_lean** library
(``FepSketches.ness_flow``) over ℝ using mathlib.  We import and re-export
them here with exposition linking to the Python demonstrations.

## Connection to Python

| Lean theorem | Python file | Demo figure |
|---|---|---|
| ``solenoidal_orthogonal`` | ``src/free_energy_flow.py`` | [@fig:overview] — flow field |
| ``flow_work_eq_dissipation`` | ``src/trajectories.py`` | [@fig:trajectories] — RK4 paths |
| ``detailed_balance_iff`` | ``src/free_energy_flow.py`` | [@fig:overview] — equilibrium vs NESS |
| ``entropyProduction_nonneg`` | ``src/steady_state.py`` | [@fig:steady] — entropy rate |
-/

namespace ActiveInferenceFormal

open FEP.NessFlow

/-! ## The ℝ Bayesian-mechanics flow (from fep_lean) -/

/-- Antisymmetric drive is orthogonal to the gradient. This geometric identity
does not imply zero physical work or zero stochastic entropy production. -/
theorem ℝ_solenoidal_orthogonal (ω : ℝ) (g : Fin 2 → ℝ) :
    dot (solenoidal ω g) g = 0 :=
  solenoidal_orthogonal ω g

/-- **Free-energy descent rate.** (ℝ version from fep_lean.)
``f·g = -γ·‖g‖²`` — the flow's work against the gradient is purely
dissipative.  Since ``‖g‖² ≥ 0``, free energy is non-increasing for ``γ ≥ 0``.
-/
theorem ℝ_flow_work_eq_dissipation (γ ω : ℝ) (g : Fin 2 → ℝ) :
    dot (flow γ ω g) g = -γ * normSq g :=
  flow_work_eq_dissipation γ ω g

/-- **Free energy is non-increasing along the flow.** (ℝ version from fep_lean.)
This is a work inequality for the stated flow under nonnegative dissipation. -/
theorem ℝ_freeEnergy_non_increasing (γ : ℝ) (hγ : 0 ≤ γ) (ω : ℝ) (g : Fin 2 → ℝ) :
    dot (flow γ ω g) g ≤ 0 :=
  freeEnergy_non_increasing γ hγ g

/-- At a nonzero gradient, the algebraic solenoidal vector vanishes iff drive
is zero. Relating this to stochastic detailed balance requires a diffusion model. -/
theorem ℝ_detailed_balance_iff (ω : ℝ) (g : Fin 2 → ℝ) (hg : g 0 ≠ 0 ∨ g 1 ≠ 0) :
    solenoidal ω g = 0 ↔ ω = 0 :=
  detailed_balance_iff ω g hg

/-- **Entropy production is nonnegative.** (ℝ version from fep_lean.)
``σ = 2·ω²·precision/γ ≥ 0`` for nonnegative ``γ`` and ``precision``.
A positive entropy-production rate is the measurable signature of a NESS. -/
theorem ℝ_entropyProduction_nonneg (precision ω γ : ℝ)
    (hp : 0 ≤ precision) (hg : 0 ≤ γ) : 0 ≤ entropyProduction precision ω γ :=
  entropyProduction_nonneg precision ω γ hp hg

/-- **Entropy production vanishes at detailed balance.** (ℝ version from fep_lean.)
For strictly positive ``γ`` and ``precision``, ``σ = 0 ↔ ω = 0``. -/
theorem ℝ_entropyProduction_eq_zero_iff (precision ω γ : ℝ)
    (hp : 0 < precision) (hg : 0 < γ) :
    entropyProduction precision ω γ = 0 ↔ ω = 0 :=
  entropyProduction_eq_zero_iff precision ω γ hp hg


end ActiveInferenceFormal
