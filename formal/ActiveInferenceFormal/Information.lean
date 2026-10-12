/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/
import FepSketches.finite_information
import FepSketches.finite_probability
import FepSketches.active_inference

/-!
# Perception as inference — the variational free-energy bound

The central claim of the perception section (§2) is that variational free
energy is an upper bound on surprise, and that minimizing it *is* Bayesian
inference.  This module imports the ℝ-valued proofs from the companion
**fep_lean** library and re-exports them with exposition.

## Evidence boundary

The real-valued propositions are imported from fep_formal's FepSketches library.
Python supplies independently tested numerical examples. The upstream finite
KL convention is totalized over reals; Python rejects zero reference mass on
positive belief support. Agreement requires the appropriate support domain.

## Key theorems imported from fep_lean

| fep_lean theorem | This module | Meaning |
|---|---|---|
| ``finiteKL_nonneg`` | ``ℝ_finiteKL_nonneg`` | KL(Q‖P) ≥ 0 (Gibbs' inequality) |
| ``finiteKL_self`` | ``ℝ_finiteKL_self`` | KL(Q‖Q) = 0 |
| ``finiteKL_eq_zero_iff`` | ``ℝ_finiteKL_eq_zero_iff`` | KL(Q‖P) = 0 iff Q = P |
| ``entropy_nonneg`` | ``ℝ_entropy_nonneg`` | Shannon entropy is nonnegative |
| ``outcomeSurprisal_le_variationalFreeEnergy`` | ``ℝ_surprisal_le_VFE`` | VFE bounds surprise |
| ``expectedFreeEnergy_eq_negPragmaticValuePlusEpistemicValue`` | ``ℝ_EFE_decomposition`` | G(π) = -(E[ln P(o)] + I(s; o)) |
| ``exists_expectedFreeEnergy_minimizer`` | ``ℝ_EFE_minimizer_exists`` | An optimal policy exists |
-/

namespace ActiveInferenceFormal

open FEP.FiniteInformation
open FEP.ActiveInference
open FEP

/-! ## Gibbs' inequality and finite KL divergence (ℝ, from fep_lean) -/

/-- **Gibbs' inequality.** KL divergence is nonnegative over ℝ-valued finite
laws. -/
theorem ℝ_finiteKL_nonneg {α : Type*} [Fintype α] (p q : FiniteLaw α) :
    0 ≤ finiteKL p q :=
  finiteKL_nonneg p q

/-- **KL divergence of a law from itself is zero.** -/
theorem ℝ_finiteKL_self {α : Type*} [Fintype α] (p : FiniteLaw α) :
    finiteKL p p = 0 :=
  finiteKL_self p

/-- **KL divergence vanishes exactly at equality.**  For finite ℝ-valued laws,
``KL(Q‖P) = 0`` iff ``Q = P`` pointwise. -/
theorem ℝ_finiteKL_eq_zero_iff {α : Type*} [Fintype α] (p q : FiniteLaw α) :
    finiteKL p q = 0 ↔ p = q :=
  finiteKL_eq_zero_iff p q

/-- **Shannon entropy is nonnegative** for finite ℝ-valued laws. -/
theorem ℝ_entropy_nonneg {α : Type*} [Fintype α] (p : FiniteLaw α) :
    0 ≤ entropy p :=
  entropy_nonneg p

/-! ## Variational free energy bound (ℝ, from fep_lean) -/

/-- **Variational free energy upper-bounds surprise.**  For any recognition
distribution and a positive-mass outcome, the VFE is at least the negative log
predictive probability. -/
theorem ℝ_surprisal_le_VFE
    {Policy State Outcome : Type*} [Fintype Policy] [Fintype State] [Fintype Outcome]
    (model : GenerativeModel Policy State Outcome) (policy : Policy)
    (outcome : Outcome) (h : 0 < predictedOutcome model policy outcome)
    (recognition : FiniteLaw State) :
    outcomeSurprisal model policy outcome ≤
      variationalFreeEnergy model policy outcome h recognition :=
  outcomeSurprisal_le_variationalFreeEnergy model policy outcome h recognition

/-- **The exact Bayesian posterior attains the bound.**  When the recognition
distribution is the true posterior, VFE equals surprise. -/
theorem ℝ_VFE_at_posterior
    {Policy State Outcome : Type*} [Fintype Policy] [Fintype State] [Fintype Outcome]
    (model : GenerativeModel Policy State Outcome) (policy : Policy)
    (outcome : Outcome) (h : 0 < predictedOutcome model policy outcome) :
    variationalFreeEnergy model policy outcome h
        (posteriorState model policy outcome h) =
      outcomeSurprisal model policy outcome :=
  variationalFreeEnergy_posterior model policy outcome h

/-- **The ELBO form:** the negative VFE is a lower bound on the log evidence. -/
theorem ℝ_negative_VFE_le_logEvidence
    {Policy State Outcome : Type*} [Fintype Policy] [Fintype State] [Fintype Outcome]
    (model : GenerativeModel Policy State Outcome) (policy : Policy)
    (outcome : Outcome) (h : 0 < predictedOutcome model policy outcome)
    (recognition : FiniteLaw State) :
    -variationalFreeEnergy model policy outcome h recognition ≤
      Real.log (predictedOutcome model policy outcome) :=
  negative_variationalFreeEnergy_le_logEvidence model policy outcome h recognition

/-! ## Expected free energy (ℝ, from fep_lean) -/

/-- **EFE decomposition matching ActiveInferenceSynthetic.**  G(π) =
-(E[ln C(o)] + I(s; o|π)), where C is the outcome preference law.  The ``pragmaticValue`` is the expected
log-preference; the ``epistemicValue`` is the mutual information between
latent state and outcome. -/
theorem ℝ_EFE_decomposition
    {Policy State Outcome : Type*} [Fintype Policy] [Fintype State] [Fintype Outcome]
    (model : GenerativeModel Policy State Outcome) (policy : Policy) :
    expectedFreeEnergy model policy =
      -(pragmaticValue model policy + epistemicValue model policy) :=
  expectedFreeEnergy_eq_negPragmaticValuePlusEpistemicValue model policy

/-- **An optimal policy always exists** on the finite policy carrier. -/
theorem ℝ_EFE_minimizer_exists
    {Policy State Outcome : Type*} [Fintype Policy] [Fintype State] [Fintype Outcome]
    (model : GenerativeModel Policy State Outcome) :
    ∃ policy : Policy, ∀ alternative : Policy,
      expectedFreeEnergy model policy ≤ expectedFreeEnergy model alternative :=
  exists_expectedFreeEnergy_minimizer model

/-- **Epistemic value is nonnegative:** the predictive joint has nonnegative
mutual information. -/
theorem ℝ_epistemicValue_nonneg
    {Policy State Outcome : Type*} [Fintype Policy] [Fintype State] [Fintype Outcome]
    (model : GenerativeModel Policy State Outcome) (policy : Policy) :
    0 ≤ epistemicValue model policy :=
  epistemicValue_nonneg model policy

end ActiveInferenceFormal
