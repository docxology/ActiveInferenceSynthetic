# Active Inference -- A Synthetic Overview

> An applicable introduction to Active Inference, with a focus on equilibrium
> vs far-from-equilibrium systems, Bayesian Mechanics, and the Free Energy
> Principle. Concise, educational, **show not tell**.

**Authors:** Daniel Ari Friedman, Alexandra Mikhailova — Active Inference Institute.

## Status

Fifth iteration (`v0.5.0`). The manuscript currently contains:

- **`docs/manuscript/00_abstract.md`** — a ~200-character abstract.
- **`docs/manuscript/01_extended_abstract.md`** — a single-page extended abstract
  built around the overview figure ([@fig:overview]).
- **`docs/manuscript/02_generative_model.md`** — *perception as inference*: a
  discrete generative model showing that minimizing variational free energy
  **is** Bayesian updating, and that free energy is a tight upper bound on
  surprise ([@fig:belief]).
- **`docs/manuscript/03_worked_regimes.md`** — *worked equilibrium vs NESS
  trajectories*: the flow integrated into paths, with the persistent
  probability current quantified as net rotation ([@fig:trajectories]).
- **`docs/manuscript/04_expected_free_energy.md`** — *action*: variational vs
  **expected** free energy, whose pragmatic and epistemic terms produce the
  explore/exploit balance from one rule ([@fig:efe]).
- **`docs/manuscript/08_planning.md`** — *planning*: policies as action
  sequences; EFE minimization over sequences makes "look, then leap"
  emerge (`src/policy_planning.py`, `[@fig:planning]`).
- **`docs/manuscript/05_markov_blanket.md`** — *the boundary*: internal and external
  states are marginally dependent but conditionally independent given the
  sensory/active blanket ([@fig:blanket]).
- **`docs/manuscript/06_steady_state.md`** — *the steady state, quantified*: the
  analytic NESS probability current and entropy-production rate ($\sigma=0$ at
  equilibrium, $>0$ far from it), closing the deterministic-drift gap of §3
  ([@fig:steady]).
- **`docs/manuscript/07_formal_verification.md`** — *formal verification*: the
  load-bearing theorems (Gibbs' inequality, the free-energy bound, solenoidal
  orthogonality, entropy-production sign) are **machine-checked in Lean 4**
  (`formal/`) across two surfaces — ℝ theorems re-exported from the companion
  fep_lean library, and a legacy Lean-core-only ℤ surface — with no `sorry`.
- **`docs/manuscript/99_references.md`** + `references.bib` — the canonical FEP /
  Active Inference / Bayesian-mechanics references.

The overview figure is the conceptual anchor: *one free-energy landscape, two
regimes*. At equilibrium the flow is pure gradient descent on free energy
($f=-\nabla F$) and comes to rest; far from equilibrium an antisymmetric
solenoidal term adds a persistent probability current ($f=(Q-\Gamma)\nabla F$) —
the signature of living systems. This is the Free Energy Principle (the descent)
plus Bayesian mechanics (the circulation). The demonstration sections then
show each pillar: §2 perception (inference), §3 the mechanics (equilibrium vs
non-equilibrium trajectories), §4 action (expected free energy / explore-exploit),
§5 the Markov blanket (the boundary that makes inference well-posed).

## Layout

```
docs/manuscript/   abstract through formal verification + references
src/          tested numerical cores + figures/ builders
scripts/      thin orchestrators (generate_all_figures.py + per-figure aliases)
tests/        no-mocks tests; ≥90% coverage of src/ (+ Lean build verification)
formal/       Lean 4 formalization — ℝ (fep_lean) + legacy ℤ (Lean core only)
output/       disposable rendered artifacts (PDF/HTML/figures)
```

The project uses the template repository's build, validation, and rendering
infrastructure while keeping its scientific code self-contained under `src/`.

## Build

```bash
# Generate figures and hydrate {{TOKEN}} manuscript values:
uv run python scripts/generate_all_figures.py
uv run python scripts/z_generate_manuscript_variables.py

# Render PDF from the template checkout:
uv run python scripts/pipeline/stage_03_render.py --project working/ActiveInferenceSynthetic

# Tests (≥90% src coverage, no mocks):
uv run pytest tests/ --cov=src --cov-fail-under=90

# Formal proofs (machine-checked; ℝ via fep_lean + legacy ℤ core-only):
cd formal && lake update && lake build   # prints axiom sets; no `sorry`
```

Output PDF: `output/pdf/ActiveInferenceSynthetic_combined.pdf`.

## Roadmap

All four planned demonstrations ship — the generative model (§2), worked
trajectories (§3), expected free energy / action (§4), the Markov blanket (§5) —
plus a §6 capstone quantifying the non-equilibrium steady state and a §7 that
**machine-checks the mathematics in Lean 4** (`formal/`, via the fep_lean ℝ
surface and a legacy Lean-core ℤ surface). Each numeric section is
runnable, tested, and deterministic; the formal layer proves the theorems those
sections rely on. See [`TODO.md`](TODO.md) for remaining candidate directions
(multi-step policies, a hierarchical model, tightening the ℤ/ℝ formal-layer coupling).
