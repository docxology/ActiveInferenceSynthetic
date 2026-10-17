module
public import FepSketches.path_thermodynamics

@[expose] public section

namespace ActiveInferenceFormal

open FEP.PathThermodynamics
open scoped BigOperators

/-- Finite normalized path KL is nonnegative; this is not a continuum OU theorem. -/
theorem finite_path_entropy_nonnegative {Path : Type*} [Fintype Path]
    (protocol : FinitePathProtocol Path) : 0 ≤ entropyProduction protocol :=
  entropyProduction_nonneg protocol

/-- The finite fluctuation identity requires positive forward and reverse support. -/
theorem finite_path_integral_fluctuation {Path : Type*} [Fintype Path]
    (protocol : FinitePathProtocol Path)
    (hForward : ∀ path, 0 < protocol.forward path)
    (hReverse : ∀ path, 0 < protocol.reverseAligned path) :
    ∑ path, protocol.forward path *
      Real.exp (-pathwiseEntropyProduction protocol path) = 1 :=
  integralFluctuation_eq_one protocol hForward hReverse

end ActiveInferenceFormal
