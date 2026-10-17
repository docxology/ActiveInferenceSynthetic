module
public import ActiveInferenceFormal.Geometry
public import ActiveInferenceFormal.Information

@[expose] public section

/-! Concrete controls expose the assumptions needed by the paper's exposition.
They complement upstream witnesses and do not claim to verify Python code. -/
namespace ActiveInferenceFormal

open FEP FEP.NessFlow FEP.FiniteInformation

/-- Negative dissipation breaks the non-increasing-work conclusion. -/
theorem negative_dissipation_positive_work :
    dot (flow (-1) 0 (fun i => if i = 0 then 1 else 0))
      (fun i => if i = 0 then 1 else 0) = 1 := by
  norm_num [flow, solenoidal, dissipative, dot, normSq]

/-- A nonzero gradient with zero drive has zero work at zero dissipation. -/
theorem zero_drive_zero_work :
    dot (flow 0 0 (fun i => if i = 0 then 1 else 0))
      (fun i => if i = 0 then 1 else 0) = 0 := by
  norm_num [flow, solenoidal, dissipative, dot, normSq]

/-- Outside positive reference support, totalized finite KL is not extended KL. -/
theorem disjoint_support_totalized_KL :
    finiteKL (FiniteLaw.pointMass true) (FiniteLaw.pointMass false) = 1 :=
  finiteKL_disjoint_pointMass_totalized

end ActiveInferenceFormal
