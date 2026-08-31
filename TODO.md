# Active Inference -- A Synthetic Overview: TODO

Status: active
Owner: Daniel Ari Friedman
Last reviewed: 2026-08-30

Forward roadmap for the educational overview. The guiding principle is
**show, not tell**: each addition is a runnable, minimal, deterministic
demonstration backed by tested code in `src/`, not more formalism.

## Completed / Closed

- **[DONE — §8 — 2026-08-19]** Multi-step policies: planning as EFE
  minimization over action sequences (`src/policy_planning.py`,
  `[@fig:planning]`, manuscript `08_planning.md`). Two-step demo: with sharp
  terminal preferences the argmin plan is cue-then-bet ("look, then leap";
  G=0.07) over bet-first (G=0.43) — exploration is deferred exploitation.
  Epistemic term equals I(s; o_{1:T}) by the KL chain rule, cross-checked
  against an independent brute-force mutual information in tests.
  19 new no-mocks tests; figure + tokens + claim ledger entries added.
- **[DONE — §2]** Generative model / perception as VFE minimization
  (`src/generative_model.py`, `[@fig:belief]`).
- **[DONE — §3]** Worked equilibrium vs NESS trajectories
  (`src/trajectories.py`, `[@fig:trajectories]`).
- **[DONE — §4]** Expected free energy / explore–exploit
  (`src/expected_free_energy.py`, `[@fig:efe]`).
- **[DONE — §5]** Markov blanket / conditional independence
  (`src/markov_blanket.py`, `[@fig:blanket]`).
- **[DONE — §6]** Analytic NESS current and entropy production
  (`src/steady_state.py`, `[@fig:steady]`).
- **[DONE — §7]** Lean 4 formalization (`formal/`) with no `sorry`; the original
  ℤ-only surface reports `#print axioms` `[propext, Quot.sound]` (verified
  `lake build` 2026-08-16). Since extended: ℝ theorems are now re-exported from
  the companion fep_lean library (see Current state below).
- **[DONE — 2026-08-16]** Manuscript §3 quoted stale winding
  ($\approx -11.5$ turns, $\approx -0.95$ turns/time) that matched entropy
  production $\sigma=11.52$, not the demo
  (`omega=2.4`, $T=12$ → $\approx -4.58$ turns, $\approx -0.38$ turns/time).
  Fixed `docs/manuscript/03_worked_regimes.md`; regression in
  `tests/test_trajectories.py`.
- **[DONE — 2026-08-16]** `variational_free_energy` / `vfe_components` returned
  `±inf` (RuntimeWarning) when $q>0$ on a zero joint/likelihood entry; siblings
  `kl_divergence` and `minimize_free_energy` already raised. Now raise
  `ValueError` (`src/generative_model.py`).
- **[DONE — 2026-08-16]** `figure_registry.yaml` caption called the equilibrium
  path a "spiral"; equilibrium is a radial fall.
- **[DONE — 2026-08-16]** `free_energy_flow` docstring called $\Gamma$ SPD;
  `gamma == 0` is allowed and makes $\Gamma$ only SPSD.
- **[DONE — 2026-08-16]** `CITATION.cff` said `type: dataset` and
  `date-released: 2026-06-28`; aligned to `software` / `2026-07-22` with
  manuscript + CodeMeta.
- **[DONE — 2026-08-16]** All demo numbers in authored manuscript sections
  are `{{TOKEN}}` values from `src/manuscript_variables.py` (live cores +
  `src/demos.py`). Hydrator: `scripts/z_generate_manuscript_variables.py`.
  Guarded by `tests/test_manuscript_variables.py`.
- **[DONE — 2026-08-16]** `stationary_covariance` returns the exact
  `Sigma = P^{-1}` and checks the Lyapunov residual (no Kronecker fallback).

## Major

_None open._ Multi-step policies, a hierarchical model, and Lean-over-ℝ remain
candidate expansions (below), not defects in the current contract.

## Medium

_None open from the 2026-08-16 review._ Remaining items are scoped expansions.

## Minor

- **Hierarchical / deep model.** A two-level generative model where the top
  level's predictions are the lower level's priors.
  Files: new `src/` module + manuscript section.
  Why: "deep active inference" is the natural next demonstration after one
  discrete level.
  Suggested: smallest two-level discrete model; bind claims to tests.

- **Formal proofs over ℝ (in progress).** The ℝ surface is now provided by the
  companion fep_lean library (`Geometry.lean`/`Information.lean` re-export
  mathlib-backed ℝ theorems). Remaining: tighten the coupling so the ℤ
  hypotheses in `Sanity.lean` are discharged from `Real.log` where the two
  surfaces overlap, and keep the ℤ core as a dependency-free regression surface.
  Files: `formal/`, fep_lean.

## Current state (`v0.5.0`)

- **Numerical cores** (all deterministic, no RNG): `src/free_energy_flow.py`,
  `src/generative_model.py`, `src/trajectories.py`,
  `src/expected_free_energy.py`, `src/markov_blanket.py`,
  `src/steady_state.py`, plus `_prob.py`, `ou_model.py`, `demos.py`,
  `project_paths.py`, `src/figures/`.
- **Formal proofs:** `formal/` — two surfaces: ℝ (imported from the companion
  fep_lean library; manuscript-canonical) and a legacy ℤ surface (Lean core
  only), audited by `tests/test_formal_lean.py` and a real `lake build`.
- **Figure orchestrators:** thin wrappers over `src/figures/` plus
  `generate_all_figures.py` → seven PNGs under `output/figures/`.
- **Manuscript:** `00`–`07` + `99_references.md` / `.bib`.
- **Tests:** no-mocks suite; configured `src/` coverage gate ≥90%.

## Validation evidence

- `uv run pytest tests/ --cov=src --cov-fail-under=90`
- `uv run ruff check src scripts tests`
- `uv run mypy src`
- `uv run python scripts/generate_all_figures.py`
- `(cd formal && lake build)`
- Render: from the template checkout,
  `uv run python scripts/pipeline/stage_03_render.py --project working/ActiveInferenceSynthetic`

## Working agreements

- Keep business logic in `src/` (tested); keep `scripts/` as thin orchestrators
  that only handle I/O, layout, and rendering.
- Every new section ships with no-mocks tests and holds the `src/` coverage gate.
- Keep figures deterministic (fixed parameters, no RNG) so renders are reproducible.
- Keep `data/claim_ledger.yaml` and `experiment_plan.yaml` describing only what the
  project's real code produces — no carryover from the upstream template.
- Numeric claims in manuscript prose must match `src/demos.py` and the claim
  ledger. Do not reuse $\sigma$ (nats/time) as a winding (turns).
