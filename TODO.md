# Active Inference -- A Synthetic Overview: TODO

Forward roadmap for the educational overview. The guiding principle is
**show, not tell**: each addition is a runnable, minimal, deterministic
demonstration backed by tested code in `src/`, not more formalism.

## Current state (`v0.1.0`)

- **Numerical core:** `src/free_energy_flow.py` — the analytic Bayesian-mechanics
  flow `f = (Q - Gamma) grad F` on an isotropic Gaussian free-energy landscape
  (free energy, gradient, flow field, solenoidal-orthogonality check, detailed-
  balance predicate). Deterministic; no RNG.
- **Figure orchestrator:** `scripts/generate_overview_figure.py` — thin wrapper
  that renders the sole manuscript anchor, `output/figures/active_inference_overview.png`
  (one landscape, two regimes: equilibrium vs NESS).
- **Manuscript:** `manuscript/00_abstract.md`, `manuscript/01_extended_abstract.md`
  (built around `[@fig:overview]`), and `manuscript/99_references.md` + `references.bib`.
- **Tests:** `tests/test_free_energy_flow.py`, `tests/test_project_paths.py`, and a
  figure smoke test — no mocks, 100% coverage of `src/` (gate: >=90%).

## Validation evidence

- Project tests + coverage:
  `uv run pytest projects/working/ActiveInferenceSynthetic/tests/ --cov=projects/working/ActiveInferenceSynthetic/src --cov-fail-under=90`
- Regenerate the figure (deterministic):
  `uv run python projects/working/ActiveInferenceSynthetic/scripts/generate_overview_figure.py`
- Render the manuscript:
  `uv run python scripts/03_render_pdf.py --project working/ActiveInferenceSynthetic`

## Roadmap — one demonstration per section

1. **Generative model.** Add a minimal tested generative model (states, observations,
   likelihood `p(s|x)` and prior `p(x)`) in `src/`, with a figure showing beliefs
   updating under new evidence. Perception as free-energy minimization.
2. **Variational vs expected free energy.** Contrast VFE (perception/inference on
   past-and-present sensations) with EFE (action selection over expected future
   observations, balancing pragmatic and epistemic value). One worked, deterministic
   example each; make the pragmatic/epistemic split visible.
3. **Markov blanket.** A small, tested demonstration of the statistical boundary —
   external `eta`, sensory `s`, active `a`, internal `mu` — showing conditional
   independence of internal and external states given the blanket.
4. **Worked equilibrium / non-equilibrium examples.** Extend the current flow demo
   into concrete trajectories: an equilibrium system relaxing to the mode vs a
   NESS system sustaining a persistent current, quantifying the entropy-production
   / probability-current difference.

## Working agreements

- Keep business logic in `src/` (tested); keep `scripts/` as thin orchestrators
  that only handle I/O, layout, and rendering.
- Every new section ships with no-mocks tests and holds the `src/` coverage gate.
- Keep figures deterministic (fixed parameters, no RNG) so renders are reproducible.
- Keep `data/claim_ledger.yaml` and `experiment_plan.yaml` describing only what the
  project's real code produces — no carryover from the upstream template.
