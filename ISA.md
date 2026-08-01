---
project: ActiveInferenceSynthetic
effort: E5
phase: complete
updated: 2026-07-22
---

# Ideal State — Active Inference: A Synthetic Overview

## Purpose

Provide a compact, executable introduction to Active Inference in which every
load-bearing scientific claim is bound to a deterministic Python
demonstration, an analytic-reference test, a scholarly citation, or a Lean
theorem.

## Ideal-state criteria

- [x] Perception is demonstrated as VFE minimization converging to the Bayesian
  posterior and surprise bound.
- [x] Equilibrium and NESS share one explicit `IsotropicOU` model and sign
  convention.
- [x] Deterministic trajectories are described as drift, not confused with
  stationary probability current.
- [x] The NESS demonstration computes current and entropy production with
  `gamma > 0`.
- [x] EFE policy selection reports typed pragmatic, epistemic, and total values.
- [x] The Gaussian Markov blanket demonstrates marginal dependence and
  conditional independence.
- [x] Shared demo parameters come from `src/demos.py`; figures and evidence do
  not maintain competing constants.
- [x] Figure builders are importable under `src/figures/`; scripts are thin.
- [x] Tests use real computations and enforce at least 90% branch coverage.
- [x] Lean checks the formalized geometric and information-theoretic claims
  without `sorry`.
- [x] Manuscript figure labels, captions, paths, and alt text are registry-backed.
- [x] Package, citation, CodeMeta, Zenodo, manuscript, and domain metadata refer
  to this project and version 0.5.0.
- [x] Documentation commands work from either the project root or the template
  root as explicitly stated.

## Verification

From the project root:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src scripts tests
uv run mypy src
uv run python scripts/generate_all_figures.py
(cd formal && lake build)
```

From the template root:

```bash
uv run python scripts/pipeline/stage_03_render.py \
  --project working/ActiveInferenceSynthetic
```

## Durable decisions

- The deterministic-flow layer permits `gamma == 0`; stochastic steady-state
  quantities require `gamma > 0`.
- Rotation rate is the intrinsic trajectory diagnostic. Total winding depends
  on the integration window and is labelled as such.
- Covariance describes statistical coupling, not causal influence.
- Python and Lean are sibling evidence surfaces: executable demonstrations and
  machine-checked propositions.
