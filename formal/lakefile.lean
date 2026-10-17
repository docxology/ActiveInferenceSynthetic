import Lake
open Lake DSL

/-! Paper-specific exposition over a pinned revision of fep_formal main.
Generic theorem implementations remain upstream in FepSketches. -/
package «active-inference-formal» where
  leanOptions := #[⟨`autoImplicit, false⟩, ⟨`relaxedAutoImplicit, false⟩]

require FepSketches from git
  "https://github.com/ActiveInferenceInstitute/fep_formal.git" @
  "8ac7761635d20d87790d6018495051fe5f9ad6a8" / "lean"

@[default_target]
lean_lib «ActiveInferenceFormal» where
  roots := #[`ActiveInferenceFormal]
