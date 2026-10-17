module
public import FepSketches.gaussian_precision_conditioning

@[expose] public section

/-! Exact adapter for the second, canonical Gaussian demonstration. The first
paper precision with diagonal 2.5 is a different model and is not covered.
Coordinates are external, sensory, active, internal (indices 0, 1, 2, 3).
The centered law is native multivariate Gaussian; no finite-law substitution. -/
namespace ActiveInferenceFormal
open FEP.Fin4GaussianSemigroup FEP.Fin4GaussianSemigroup.Axis
open FEP.GaussianPrecisionConditioning
open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory

/-- Exact four-by-four Python fixture, transported by the upstream axis equivalence. -/
theorem ℝ_canonical_precision_entries :
    (fun i j : Fin 4 => K (axisFin.symm i) (axisFin.symm j)) =
      !![4, -1, -1, 0; -1, 4, 0, -1; -1, 0, 4, -1; 0, -1, -1, 4] := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

/-- Positive definiteness is proved upstream for this actual precision. -/
theorem ℝ_canonical_precision_posDef : K.PosDef := K_posDef

/-- Zero endpoint precision, nonzero marginal covariance and conditional
independence coexist for the canonical stationary Gaussian, at every center. -/
theorem ℝ_canonical_gaussian_blanket (center : StandardizedState) :
    K external internal = 0 ∧
      cov[fun state : StandardizedState => state external,
        fun state => state internal; stationaryLaw center] = 1 / 24 ∧
      cov[fun state : StandardizedState => state external,
        fun state => state internal; stationaryLaw center] ≠ 0 ∧
      ((fun state : StandardizedState => state external) ⟂ᵢ[
        blanketCoordinates, measurable_blanketCoordinates; stationaryLaw center]
        (fun state => state internal)) :=
  precisionZero_covarianceNonzero_condIndep center

/-- Native conditional rows are a product; each endpoint has variance 1/4
and the explicitly blanket-dependent mean, including at a nonzero center. -/
theorem ℝ_canonical_conditional_rows (center : StandardizedState)
    (blanket : Blanket) :
    endpointConditionalKernel center blanket =
      (gaussianReal (externalConditionalMean center blanket) (1 / 4)).prod
        (gaussianReal (internalConditionalMean center blanket) (1 / 4)) :=
  endpointConditionalKernel_apply center blanket

/-- A coupled bivariate Gaussian is a real negative control; it is not the
canonical four-axis law with a renamed coordinate. -/
theorem ℝ_coupled_gaussian_not_independent :
    ¬ IndepFun perturbedExternal perturbedInternal perturbedEndpointLaw :=
  perturbedEndpoint_external_not_indep_internal
end ActiveInferenceFormal
