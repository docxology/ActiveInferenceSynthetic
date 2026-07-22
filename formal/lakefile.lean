import Lake
open Lake DSL

/-!
Self-contained Lean 4 formalization of the mathematical core of
"Active Inference -- A Synthetic Overview".

Deliberately depends on NO external packages (no mathlib): every theorem is
proved from Lean core alone, so the project builds in seconds and its axiom
footprint is exactly Lean's. This mirrors the manuscript's no-mocks / analytic
principle at the level of *proof* rather than *test*.
-/

package «active-inference-formal» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

@[default_target]
lean_lib «ActiveInferenceFormal» where
  roots := #[`ActiveInferenceFormal]
