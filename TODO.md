# Active Inference -- A Synthetic Overview: TODO

Status: active
Owner: Daniel Ari Friedman
Last reviewed: 2026-08-16

Forward roadmap for the educational overview. The guiding principle is
**show, not tell**: each addition is a runnable, minimal, deterministic
demonstration backed by tested code in `src/`, not more formalism.

## Completed / Closed

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
- **[DONE — §7]** Lean 4 formalization (`formal/`) with no `sorry`, no mathlib;
  `#print axioms` is `[propext, Quot.sound]` (verified `lake build` 2026-08-16).
- **[DONE — 2026-08-16]** Manuscript §3 quoted stale winding
  ($\approx -11.5$ turns, $\approx -0.95$ turns/time) that matched entropy
  production $\sigma=11.52$, not the demo
  (`omega=2.4`, $T=12$ → $\approx -4.58$ turns, $\approx -0.38$ turns/time).
  Fixed `manuscript/03_worked_regimes.md`; regression in
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

## Major

_None open._ Multi-step policies, a hierarchical model, and Lean-over-ℝ remain
candidate expansions (below), not defects in the current contract.

## Medium

_None open from the 2026-08-16 review._ Remaining items are scoped expansions.

## Minor

- **Multi-step policies.** Extend the EFE demo from one-step actions to short
  policies (sequences), showing planning as expected-free-energy minimization
  over trajectories of beliefs.
  Files: `src/expected_free_energy.py`, new section / figure.
  Why: the current demo isolates explore/exploit at one step; planning is the
  next applicable claim.
  Suggested: keep deterministic, no RNG; add no-mocks tests and a figure.

- **Hierarchical / deep model.** A two-level generative model where the top
  level's predictions are the lower level's priors.
  Files: new `src/` module + manuscript section.
  Why: "deep active inference" is the natural next demonstration after one
  discrete level.
  Suggested: smallest two-level discrete model; bind claims to tests.

- **Formal proofs over ℝ.** The Lean development works over ℤ (dependency-free).
  A mathlib-based extension could discharge the `LogAdd`/`Tangent` hypotheses
  from `Real.log`'s actual properties.
  Files: `formal/`.
  Why: the free-energy bound would become an unconditional theorem about the
  real logarithm.
  Suggested: optional extra package, not a replacement of the no-mathlib core.

- **Lyapunov fallback coverage is environment-sensitive.**
  `src/steady_state.py:117-130` falls back to $\Sigma=P^{-1}$ when the
  Kronecker solve residual is large. `test_stationary_covariance_falls_back_to_analytic_closed_form`
  can pass via the *direct* path on some BLAS stacks (line 130 still uncovered
  at 99.76%). Not a correctness bug — the analytic form is exact for this
  isotropic $D=\Gamma$ class.
  Suggested: prefer the closed form and keep Kronecker as a residual check, or
  force the fallback with a residual the current NumPy cannot meet.

## Current state (`v0.5.0`)

- **Numerical cores** (all deterministic, no RNG): `src/free_energy_flow.py`,
  `src/generative_model.py`, `src/trajectories.py`,
  `src/expected_free_energy.py`, `src/markov_blanket.py`,
  `src/steady_state.py`, plus `_prob.py`, `ou_model.py`, `demos.py`,
  `project_paths.py`, `src/figures/`.
- **Formal proofs:** `formal/` — Geometry.lean + Information.lean, audited by
  `tests/test_formal_lean.py` and a real `lake build`.
- **Figure orchestrators:** thin wrappers over `src/figures/` plus
  `generate_all_figures.py` → six PNGs under `output/figures/`.
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
