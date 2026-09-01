import Lake
open Lake DSL

/-!
Self-contained Lean 4 formalization of the mathematical core of
"Active Inference -- A Synthetic Overview".

The heavy theorem proving lives in the companion **fep_lean** repository
(ActiveInferenceInstitute/fep_lean, package ``FepSketches``).  This package
imports the ℝ/mathlib theorems from there and provides a thin expositional
layer that introduces each result and connects it to the Python
demonstrations in ``src/``.

A legacy ℤ-only surface (`ActiveInferenceFormal.Geometry`` and
``ActiveInferenceFormal.Information``) proves the same structural statements
from Lean core alone (no mathlib), preserved as a curiosity: the
information-theoretic bounds and the Bayesian-mechanics flow identities are
algebraic facts that do not require ℝ analysis.
-/

package «active-inference-formal» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

require FepSketches from "../../../ongoing/instituteos/repos/fep_lean/lean"

@[default_target]
lean_lib «ActiveInferenceFormal» where
  roots := #[`ActiveInferenceFormal]

@[default_target]
lean_lib «ActiveInferenceFormalℤ» where
  roots := #[`ActiveInferenceFormalℤ.GeometryZ, `ActiveInferenceFormalℤ.InformationZ, `ActiveInferenceFormalℤ.Sanity]
