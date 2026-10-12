import Lake
open Lake DSL

/-! Paper-specific exposition over a pinned revision of fep_formal main.
Generic theorem implementations remain upstream in FepSketches. -/
package «active-inference-formal» where
  leanOptions := #[⟨`autoImplicit, false⟩, ⟨`relaxedAutoImplicit, false⟩]

require FepSketches from git
  "https://github.com/ActiveInferenceInstitute/fep_formal.git" @
  "99276926da1df4287a2e13e9aa7f6d1822cfdca3" / "lean"

@[default_target]
lean_lib «ActiveInferenceFormal» where
  roots := #[`ActiveInferenceFormal]
