# Architecture

```mermaid
flowchart LR
    Demos[src/demos.py] --> Cores[Scientific cores]
    OU[src/ou_model.py] --> Cores
    Prob[src/_prob.py] --> Cores
    Cores --> Figures[src/figures]
    Figures --> Scripts[scripts/generate_*]
    Scripts --> Output[output/figures]
    Manuscript[docs/manuscript/*.md] --> Renderer[Template renderer]
    Output --> Renderer
    LeanR[formal/ActiveInferenceFormal] --> Proofs[Machine-checked claims]
    LeanZ["formal/ActiveInferenceFormalℤ"] --> Proofs
```

## Boundaries

- `src/_prob.py`: probability validation and KL only.
- `src/ou_model.py`: canonical isotropic OU/Bayesian-mechanics parameter model.
- Scientific cores: generative model, one-step EFE, multi-step policy planning,
  flow, trajectories, blanket, NESS.
- `src/figures/`: importable presentation logic and output manifest.
- `scripts/`: thin CLI-compatible wrappers.
- `formal/`: independent Lean 4 side-spec for load-bearing theorems, on two
  surfaces — `ActiveInferenceFormal/` (ℝ, via fep_lean) and
  `ActiveInferenceFormalℤ/` (ℤ, Lean core only).
- `tests/`: real numerical references, rendering smoke tests, Lean build checks.

`gamma == 0` is valid for deterministic Hamiltonian flow. Stationary diffusion
quantities require `gamma > 0`, enforced by `IsotropicOU.require_positive_gamma`.
