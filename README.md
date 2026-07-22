# Active Inference -- A Synthetic Overview

> An applicable introduction to Active Inference, with a focus on equilibrium
> vs far-from-equilibrium systems, Bayesian Mechanics, and the Free Energy
> Principle. Concise, educational, **show not tell**.

**Authors:** Daniel Ari Friedman, Alexandra Mikhailova — Active Inference Institute.

## Status

Fifth iteration (`v0.5.0`). The manuscript currently contains:

- **`manuscript/00_abstract.md`** — a ~200-character abstract.
- **`manuscript/01_extended_abstract.md`** — a single-page extended abstract
  built around the overview figure ([@fig:overview]).
- **`manuscript/02_generative_model.md`** — *perception as inference*: a
  discrete generative model showing that minimizing variational free energy
  **is** Bayesian updating, and that free energy is a tight upper bound on
  surprise ([@fig:belief]).
- **`manuscript/03_worked_regimes.md`** — *worked equilibrium vs NESS
  trajectories*: the flow integrated into paths, with the persistent
  probability current quantified as net rotation ([@fig:trajectories]).
- **`manuscript/04_expected_free_energy.md`** — *action*: variational vs
  **expected** free energy, whose pragmatic and epistemic terms produce the
  explore/exploit balance from one rule ([@fig:efe]).
- **`manuscript/05_markov_blanket.md`** — *the boundary*: internal and external
  states are marginally dependent but conditionally independent given the
  sensory/active blanket ([@fig:blanket]).
- **`manuscript/06_steady_state.md`** — *the steady state, quantified*: the
  analytic NESS probability current and entropy-production rate ($\sigma=0$ at
  equilibrium, $>0$ far from it), closing the deterministic-drift gap of §3
  ([@fig:steady]).
- **`manuscript/07_formal_verification.md`** — *formal verification*: the
  load-bearing theorems (Gibbs' inequality, the free-energy bound, solenoidal
  orthogonality, entropy-production sign) are **machine-checked in Lean 4**
  (`formal/`), from core axioms with no `sorry` and no mathlib.
- **`manuscript/99_references.md`** + `references.bib` — the canonical FEP /
  Active Inference / Bayesian-mechanics references.

The overview figure is the conceptual anchor: *one free-energy landscape, two
regimes*. At equilibrium the flow is pure gradient descent on free energy
($f=-\nabla F$) and comes to rest; far from equilibrium an antisymmetric
solenoidal term adds a persistent probability current ($f=(Q-\Gamma)\nabla F$) —
the signature of living systems. This is the Free Energy Principle (the descent)
plus Bayesian mechanics (the circulation). The four demonstration sections then
*show* each pillar: §2 perception (inference), §3 the mechanics (equilibrium vs
non-equilibrium trajectories), §4 action (expected free energy / explore-exploit),
§5 the Markov blanket (the boundary that makes inference well-posed).

## Layout

```
manuscript/   abstract + extended abstract + four demonstration sections + references
src/          tested numerical cores:
                free_energy_flow.py    — Bayesian-mechanics flow (overview figure)
                generative_model.py    — perception as free-energy minimization
                trajectories.py        — RK4 worked equilibrium/NESS trajectories
                expected_free_energy.py — action selection, explore/exploit
                markov_blanket.py      — Gaussian conditional independence
                steady_state.py        — NESS current + entropy production (analytic)
scripts/      thin orchestrators over src/ (one figure generator each)
tests/        no-mocks tests; 100% coverage of src/ (+ Lean build verification)
formal/       Lean 4 formalization — the theorems, machine-checked (no mathlib)
output/       disposable rendered artifacts (PDF/HTML/figures)
```

This project was scaffolded from `projects/templates/template_code_project`;
the optimizer demo content has been pruned and replaced with Active-Inference
material. The build/test/render infrastructure (Layer 1) is unchanged.

## Build

```bash
# Generate the figures (all deterministic) and render the manuscript:
uv run python projects/working/ActiveInferenceSynthetic/scripts/generate_overview_figure.py
uv run python projects/working/ActiveInferenceSynthetic/scripts/generate_belief_update_figure.py
uv run python projects/working/ActiveInferenceSynthetic/scripts/generate_trajectory_figure.py
uv run python projects/working/ActiveInferenceSynthetic/scripts/generate_efe_figure.py
uv run python projects/working/ActiveInferenceSynthetic/scripts/generate_markov_blanket_figure.py
uv run python projects/working/ActiveInferenceSynthetic/scripts/generate_steady_state_figure.py
uv run python scripts/03_render_pdf.py --project working/ActiveInferenceSynthetic

# Tests (100% src coverage, no mocks):
uv run pytest projects/working/ActiveInferenceSynthetic/tests/ \
  --cov=projects/working/ActiveInferenceSynthetic/src --cov-fail-under=90

# Formal proofs (machine-checked, no mathlib, ~1s):
cd formal && lake build   # prints clean axiom sets; no `sorry`
```

Output PDF: `output/pdf/ActiveInferenceSynthetic_combined.pdf`.

## Roadmap

All four planned demonstrations ship — the generative model (§2), worked
trajectories (§3), expected free energy / action (§4), the Markov blanket (§5) —
plus a §6 capstone quantifying the non-equilibrium steady state and a §7 that
**machine-checks the mathematics in Lean 4** (`formal/`). Each numeric section is
runnable, tested, and deterministic; the formal layer proves the theorems those
sections rely on. See [`TODO.md`](TODO.md) for remaining candidate directions
(multi-step policies, a hierarchical model, extending the Lean proofs to ℝ).
