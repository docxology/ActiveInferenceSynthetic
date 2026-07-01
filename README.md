# Active Inference -- A Synthetic Overview

> An applicable introduction to Active Inference, with a focus on equilibrium
> vs far-from-equilibrium systems, Bayesian Mechanics, and the Free Energy
> Principle. Concise, educational, **show not tell**.

**Authors:** Daniel Ari Friedman, Alexandra Mikhailova — Active Inference Institute.

## Status

First iteration (`v0.1.0`). The manuscript currently contains:

- **`manuscript/00_abstract.md`** — a ~200-character abstract.
- **`manuscript/01_extended_abstract.md`** — a single-page extended abstract
  built around one figure ([@fig:overview]).
- **`manuscript/99_references.md`** + `references.bib` — the canonical FEP /
  Active Inference / Bayesian-mechanics references.

The figure is the conceptual anchor: *one free-energy landscape, two regimes*.
At equilibrium the flow is pure gradient descent on free energy ($f=-\nabla F$)
and comes to rest; far from equilibrium an antisymmetric solenoidal term adds a
persistent probability current ($f=(Q-\Gamma)\nabla F$) — the signature of
living systems. This is the Free Energy Principle (the descent) plus Bayesian
mechanics (the circulation).

## Layout

```
manuscript/   abstract + extended abstract + references
src/          tested numerical core (free_energy_flow.py) behind the figure
scripts/      generate_overview_figure.py — thin orchestrator over src/
tests/        no-mocks tests; 100% coverage of src/
output/       disposable rendered artifacts (PDF/HTML/figures)
```

This project was scaffolded from `projects/templates/template_code_project`;
the optimizer demo content has been pruned and replaced with Active-Inference
material. The build/test/render infrastructure (Layer 1) is unchanged.

## Build

```bash
# Generate the figure (deterministic) and render the manuscript:
uv run python projects/working/ActiveInferenceSynthetic/scripts/generate_overview_figure.py
uv run python scripts/03_render_pdf.py --project working/ActiveInferenceSynthetic

# Tests (100% src coverage, no mocks):
uv run pytest projects/working/ActiveInferenceSynthetic/tests/ \
  --cov=projects/working/ActiveInferenceSynthetic/src --cov-fail-under=90
```

Output PDF: `output/pdf/ActiveInferenceSynthetic_combined.pdf`.

## Roadmap

Each subsequent section will add one runnable, minimal demonstration — the
generative model, variational vs expected free energy, the Markov blanket, and
worked equilibrium / non-equilibrium examples — rather than more formalism.
