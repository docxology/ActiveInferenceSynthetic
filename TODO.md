# Active Inference -- A Synthetic Overview: TODO

Forward roadmap for the educational overview. The guiding principle is
**show, not tell**: each addition is a runnable, minimal, deterministic
demonstration backed by tested code in `src/`, not more formalism.

## Current state (`v0.3.0`)

- **Numerical cores** (all deterministic, no RNG):
  - `src/free_energy_flow.py` — the analytic Bayesian-mechanics flow
    `f = (Q - Gamma) grad F` on an isotropic Gaussian free-energy landscape.
  - `src/generative_model.py` — a discrete generative model (prior, likelihood,
    joint, evidence, exact posterior), variational free energy with its
    complexity−accuracy decomposition, the surprise bound `F >= -ln p(s)`, and a
    gradient-descent belief updater (perception).
  - `src/trajectories.py` — a fixed-step RK4 integrator over the flow, with
    free-energy-along-path and net-rotation diagnostics, quantifying the
    equilibrium(≈0) vs NESS(persistent-current) distinction (mechanics).
  - `src/expected_free_energy.py` — expected free energy over policies, its
    pragmatic (utility) / epistemic (information-gain) decomposition, and
    argmin-EFE policy selection, yielding the explore/exploit balance (action).
  - `src/markov_blanket.py` — Gaussian conditioning (Schur complement), partial
    correlation, and a precision-zero-block blanket predicate, demonstrating
    conditional independence of internal/external states (the boundary).
  - `src/steady_state.py` — the analytic non-equilibrium steady state: Lyapunov
    stationary covariance, probability-current field `j=(QPx)ρ`, and
    entropy-production rate `σ=2ω²·precision/γ` (zero iff detailed balance),
    closing the deterministic-drift gap of §3 with no RNG.
- **Formal proofs:** `formal/` — a self-contained Lean 4 development (no mathlib)
  machine-checking the load-bearing theorems: solenoidal orthogonality, the
  free-energy-descent rate, detailed-balance equivalence, entropy-production
  sign (Geometry.lean); Gibbs' inequality and the free-energy bound tight at the
  posterior (Information.lean). Every headline theorem's `#print axioms` reports
  only `[propext, Quot.sound]` — no `sorry`, no mathlib. Verified by
  `tests/test_formal_lean.py` (grep + real `lake build`).
- **Figure orchestrators** (thin wrappers over `src/`), one per section:
  overview, belief-update, worked-trajectories, expected-free-energy,
  markov-blanket → the five PNGs under `output/figures/`.
- **Manuscript:** `00_abstract.md`, `01_extended_abstract.md` (`[@fig:overview]`),
  `02_generative_model.md` (`[@fig:belief]`), `03_worked_regimes.md`
  (`[@fig:trajectories]`), `04_expected_free_energy.md` (`[@fig:efe]`),
  `05_markov_blanket.md` (`[@fig:blanket]`), `06_steady_state.md`
  (`[@fig:steady]`), and `99_references.md` + `.bib`.
- **Tests:** one no-mocks suite per core plus figure smoke tests — every
  assertion bound to an analytic reference; 100% coverage of `src/` (gate: >=90%).

## Validation evidence

- Project tests + coverage:
  `uv run pytest projects/working/ActiveInferenceSynthetic/tests/ --cov=projects/working/ActiveInferenceSynthetic/src --cov-fail-under=90`
- Regenerate the figure (deterministic):
  `uv run python projects/working/ActiveInferenceSynthetic/scripts/generate_overview_figure.py`
- Render the manuscript:
  `uv run python scripts/03_render_pdf.py --project working/ActiveInferenceSynthetic`

## Roadmap — one demonstration per section

1. **[DONE — §2, `02_generative_model.md`]** **Generative model.** Minimal tested
   generative model (states, observations, likelihood `p(s|x)`, prior `p(x)`) in
   `src/generative_model.py`, with `[@fig:belief]` showing beliefs updating under
   evidence and free energy falling to the surprise bound. Perception as
   free-energy minimization.
2. **[DONE — §4, `04_expected_free_energy.md`]** **Variational vs expected free
   energy.** `src/expected_free_energy.py` contrasts VFE (perception) with EFE
   (action selection over expected future outcomes), decomposing EFE into
   pragmatic (utility) and epistemic (information-gain) value. `[@fig:efe]`
   shows the explore/exploit flip: flat preferences → explore, sharp
   preferences → exploit, from one `argmin G` rule.
3. **[DONE — §5, `05_markov_blanket.md`]** **Markov blanket.**
   `src/markov_blanket.py` demonstrates the statistical boundary — external
   `eta`, sensory `s`, active `a`, internal `mu` — on a Gaussian with a zero
   `eta`–`mu` precision block: internal and external states are marginally
   dependent but conditionally independent given the blanket (`[@fig:blanket]`),
   via the Schur complement and partial correlation.
4. **[DONE — §3, `03_worked_regimes.md`]** **Worked equilibrium /
   non-equilibrium examples.** `src/trajectories.py` integrates the flow into
   concrete trajectories: an equilibrium system relaxing to the mode vs a NESS
   system sustaining a persistent current, quantifying the difference as the
   intrinsic rotation rate in `[@fig:trajectories]`.

## Candidate future directions (beyond the original roadmap)

- **[DONE — §6, `06_steady_state.md`]** **Stochastic steady state.** Rather than
  an RNG SDE integrator (which would break the no-RNG principle), `src/steady_state.py`
  gives the NESS *analytically*: the Lyapunov stationary density, the closed-form
  probability current `j=(QPx)ρ`, and the entropy-production rate — a genuine,
  measurable current, closing the §3 gap without randomness.
- **Multi-step policies.** Extend the EFE demo from one-step actions to short
  policies (sequences), showing planning as expected-free-energy minimization
  over trajectories of beliefs.
- **Hierarchical / deep model.** A two-level generative model where the top
  level's predictions are the lower level's priors — deep active inference.
- **Formal proofs over ℝ.** The Lean development works over ℤ (dependency-free).
  A mathlib-based extension could discharge the `LogAdd`/`Tangent` hypotheses
  from `Real.log`'s actual properties, turning the free-energy bound into an
  unconditional theorem about the real logarithm.

## Working agreements

- Keep business logic in `src/` (tested); keep `scripts/` as thin orchestrators
  that only handle I/O, layout, and rendering.
- Every new section ships with no-mocks tests and holds the `src/` coverage gate.
- Keep figures deterministic (fixed parameters, no RNG) so renders are reproducible.
- Keep `data/claim_ledger.yaml` and `experiment_plan.yaml` describing only what the
  project's real code produces — no carryover from the upstream template.
