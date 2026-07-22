---
project: ActiveInferenceSynthetic
task: Complete the roadmap — add expected-free-energy (action) and Markov-blanket demonstrations
effort: E5
phase: complete
progress: 80/80
mode: algorithm
started: 2026-07-22
updated: 2026-07-22
---

# ISA — Active Inference: A Synthetic Overview

## Problem

The manuscript is titled *Active Inference* and its guiding principle is
**show, not tell** — every claim backed by a runnable, tested demonstration.
Yet `v0.1.0` ships exactly one demonstration: the Bayesian-mechanics *flow*
(`f = (Q-Γ)∇F`), which is the thermodynamic / steady-state half of the story.
There is **no inference demonstration at all** — no generative model, no
belief updating, no showing that variational free energy is a computable upper
bound on surprise. The single most central concept of Active Inference
("perception is approximate Bayesian inference by free-energy minimization")
is asserted in prose (`01_extended_abstract.md`) but never *shown*. The
roadmap (`TODO.md`) names four missing demonstrations; none are built.

## Vision

A reader scrolls the overview and *sees* the two pillars of Active Inference,
not just reads them: (1) perception as inference — a belief distribution
visibly sharpening toward the truth as evidence arrives, with a number
(variational free energy) provably falling to the surprise it bounds; and
(2) the equilibrium↔NESS distinction as *trajectories* — one path relaxing to
rest, one circulating forever — with the probability current quantified, not
adjectival. Each new claim is anchored to tested, deterministic code. The
euphoric surprise: the abstract's one-currency-two-directions thesis becomes
literally visible as two falling free-energy curves from two different
mechanisms (inference vs. dissipation) over the *same* quantity.

## Out of Scope

Not building: interactive/animated figures; stochastic simulation (SDE
integration with noise) — everything stays analytic/deterministic per the
project's no-RNG principle; POMDP/`pymdp`-scale agent loops; the Markov-blanket
conditional-independence demo (roadmap #3, deferred — it needs a multivariate
Gaussian partition that is a section of its own); new external dependencies
beyond numpy/matplotlib; changing Layer-1 infrastructure; a full PDF render
gate as an acceptance criterion (pandoc/LaTeX availability is environmental).

## Principles

- **Show, not tell.** Every new manuscript claim traces to tested `src/` code.
- **Determinism.** No RNG; fixed parameters; reproducible renders.
- **Analytic reference.** Tests assert against closed-form truth (exact
  posteriors, finite-difference gradients, conserved quantities), not
  self-consistency.
- **Thin orchestrators.** Numerics in `src/`; scripts only lay out and draw.
- **No mocks.** Real numerical computation in every test.

## Constraints

- `src/` coverage gate ≥ 90% (project standard); target 100% as current.
- Manuscript sections are digit-prefixed `NN_*.md`, lexicographic order,
  `99_*` always last (verified in `infrastructure/rendering/manuscript_discovery.py:255`).
- Figures auto-discovered from `output/figures/*.png` sorted
  (`manuscript_discovery.py:59`).
- Baseline at OBSERVE: 16 tests pass, 100% src coverage (generator ran this
  session via `uv run pytest … --cov-fail-under=90`).
- New numeric constants surfaced in a manuscript figure must be registered in
  `data/claim_ledger.yaml`.
- Colourblind-safe palette (Okabe–Ito) consistent with the existing figure.

## Goal

Add two fully-tested, deterministic demonstrations — (1) a discrete generative
model showing perception as variational-free-energy minimization and the
surprise bound `F ≥ -ln p(s)`, and (2) worked equilibrium-vs-NESS trajectories
quantifying the persistent probability current — each with a figure and a
manuscript section, while reviewing and refining the existing code, docs, and
metadata so the whole project is internally consistent. Done = new suites green
at 100% src coverage, both figures regenerate deterministically, sections slot
into render order, and roadmap/ledger/README reflect reality.

## Criteria

### Generative model demonstration (perception as inference)
- [x] ISC-1: `src/generative_model.py` exists exposing a discrete categorical
  generative model (prior, likelihood, joint, evidence, exact posterior).
- [x] ISC-2: `posterior()` equals the analytic Bayes result on a hand-checked
  2-state / 2-observation example (asserted to machine precision).
- [x] ISC-3: `variational_free_energy(q, ...)` computes `E_q[ln q - ln p(s,x)]`.
- [x] ISC-4: VFE at the exact posterior equals surprise `-ln p(s)` (bound is
  tight at the minimizer) — asserted to ~1e-12.
- [x] ISC-5: VFE at any non-posterior `q` is strictly greater than `-ln p(s)`
  (bound holds) — asserted on ≥3 perturbed beliefs.
- [x] ISC-6: VFE decomposes as complexity − accuracy
  (`KL[q‖prior] − E_q[ln p(s|x)]`) matching the direct value to ~1e-12.
- [x] ISC-7: A gradient-free coordinate/analytic belief-update path shows VFE
  monotonically non-increasing to the posterior minimum.
- [x] ISC-8: All generative-model inputs validated (distributions sum to 1,
  nonnegative, shape-compatible) with `ValueError` on violation.
- [x] ISC-9: `scripts/generate_belief_update_figure.py` renders
  `output/figures/belief_update.png` deterministically, thin-orchestrator only.
- [x] ISC-10: `manuscript/02_generative_model.md` exists, cites the new figure
  `{#fig:belief}`, and explains perception-as-inference in show-not-tell prose.

### Worked trajectories demonstration (equilibrium vs NESS)
- [x] ISC-11: `src/trajectories.py` integrates the existing `flow_field` with a
  deterministic fixed-step RK4 integrator (reuses tested `free_energy_flow`).
- [x] ISC-12: Equilibrium trajectory (`omega=0`) has free energy monotonically
  non-increasing along the path (asserted step-wise).
- [x] ISC-13: Equilibrium trajectory radius → mode: final radius < 1% of
  initial (asserted).
- [x] ISC-14: NESS trajectory (`omega≠0`) accumulates net angular displacement
  |Δθ| well above 2π over the horizon (persistent current) — asserted.
- [x] ISC-15: NESS trajectory free energy still non-increasing (descent
  preserved despite circulation) — asserted.
- [x] ISC-16: `probability_current`/`net_rotation` helper quantifies the
  equilibrium(≈0) vs NESS(>0) circulation difference — asserted both regimes.
- [x] ISC-17: RK4 integrator matches a known linear-ODE closed form (pure
  dissipation `ẋ=-γx` decays as `x0·e^{-γt}`) within tight tol — analytic check.
- [x] ISC-18: Integrator input validation (positive dt, positive steps,
  2-vector state) raises `ValueError`.
- [x] ISC-19: `scripts/generate_trajectory_figure.py` renders
  `output/figures/worked_trajectories.png` deterministically, orchestrator-only.
- [x] ISC-20: `manuscript/03_worked_regimes.md` exists, cites
  `{#fig:trajectories}`, quantifies the current in prose from real output.

### Tests & coverage
- [x] ISC-21: `tests/test_generative_model.py` — no-mocks, analytic references.
- [x] ISC-22: `tests/test_trajectories.py` — no-mocks, analytic references.
- [x] ISC-23: Figure smoke tests for both new scripts (render → PNG exists,
  non-empty), matching the existing `test_generate_overview_figure.py` pattern.
- [x] ISC-24: Full project suite green: `uv run pytest … --cov-fail-under=90`.
- [x] ISC-25: `src/` coverage remains 100% (no new uncovered lines).

### Expected free energy — action selection (roadmap #2, added 2026-07-22 E5)
- [x] ISC-35: `src/expected_free_energy.py` builds on the generative model:
  predicted outcomes, pragmatic value, epistemic value, EFE, policy selection.
- [x] ISC-36: `predicted_outcomes(a)` = `Σ_s p(o|s,a) q(s)` matches a hand-checked
  value (machine precision).
- [x] ISC-37: `pragmatic_value` = `E_{q(o|a)}[ln p_pref(o)]` — expected log
  preference; asserted against a hand computation.
- [x] ISC-38: `epistemic_value` = `E_{q(o|a)}[ D_KL[q(s|o,a) ‖ q(s)] ]` — expected
  information gain; asserted ≥0 and against a hand computation.
- [x] ISC-39: `expected_free_energy(a)` = `−(pragmatic + epistemic)`; matches the
  sum of its parts to ~1e-12 (decomposition identity).
- [x] ISC-40: Epistemic value is exactly 0 for a fully uninformative action
  (outcome independent of state) — positive control on the info-gain term.
- [x] ISC-41: Pragmatic value is maximal for the action whose outcomes best
  match preferences when both actions are equally (un)informative.
- [x] ISC-42: `select_policy` returns the argmin-EFE action; on a constructed
  explore/exploit trade-off the informative action wins when preferences are
  flat and the rewarding action wins when preferences are sharp (both asserted).
- [x] ISC-43: EFE inputs validated (outcome model columns sum to 1, preferences
  normalised or handled, shapes compatible) with `ValueError`.
- [x] ISC-44: `scripts/generate_efe_figure.py` renders
  `output/figures/expected_free_energy.png` deterministically, orchestrator-only.
- [x] ISC-45: `manuscript/04_expected_free_energy.md` exists, cites
  `{#fig:efe}`, explains VFE-vs-EFE and the pragmatic/epistemic split.
- [x] ISC-46: `tests/test_expected_free_energy.py` — no-mocks, analytic refs.

### Markov blanket — conditional independence (roadmap #3, added 2026-07-22 E5)
- [x] ISC-47: `src/markov_blanket.py` provides Gaussian conditioning (Schur
  complement), partial correlation, and a blanket-independence predicate.
- [x] ISC-48: `conditional_covariance` equals the analytic Schur complement on a
  hand-checked small matrix (machine precision).
- [x] ISC-49: Constructed joint where internal μ and external η couple only
  through the blanket b=(s,a): marginal cov(η,μ) ≠ 0 (they are dependent).
- [x] ISC-50: Conditional cov(η,μ | b) ≈ 0 — internal ⊥ external given the
  blanket (the defining Markov-blanket property), asserted to ~1e-10.
- [x] ISC-51: `partial_correlation(η,μ | b)` ≈ 0 for the blanket structure and
  ≠ 0 for a non-blanket conditioning set — positive + negative control.
- [x] ISC-52: `is_markov_blanket(precision, partition)` returns True iff the
  η–μ block of the precision matrix is ~0; tested True and False cases.
- [x] ISC-53: Conditioning input validation (PSD covariance, disjoint index
  partition, index bounds) raises `ValueError`.
- [x] ISC-54: `scripts/generate_markov_blanket_figure.py` renders
  `output/figures/markov_blanket.png` deterministically, orchestrator-only.
- [x] ISC-55: `manuscript/05_markov_blanket.md` exists, cites `{#fig:blanket}`,
  explains conditional independence of internal/external given the blanket.
- [x] ISC-56: `tests/test_markov_blanket.py` — no-mocks, analytic references.

### Extension gates
- [x] ISC-57: Full suite green + 100% src coverage after both additions
  (`uv run pytest … --cov-fail-under=90`).
- [x] ISC-58: Anti: no RNG / mocks introduced in the new modules/tests; new
  scripts hold no business math (all numerics from `src/`).

### Steady state — NESS current + entropy production (capstone, 2026-07-22 E5)
- [x] ISC-59: `src/steady_state.py` gives the analytic NESS: Lyapunov stationary
  covariance, probability current, entropy-production rate, circulation.
- [x] ISC-60: `stationary_covariance` solves `MΣ+ΣMᵀ=2D` (Kronecker) and equals
  `P⁻¹`; residual guard rejects ill-conditioned regimes — asserted.
- [x] ISC-61: `probability_current` = `(QPx)ρ`: zero iff `omega=0`,
  divergence-free (finite-diff), orthogonal to `∇F`, correct pointwise
  orientation (sign-flip positive control) — all asserted.
- [x] ISC-62: `entropy_production_rate` = `2ω²·precision/γ` (closed form) AND
  matches an independent grid-quadrature of `∫ jᵀD⁻¹j/ρ` — non-analytic
  cross-check; zero iff `omega=0`; strictly grows with `omega`.
- [x] ISC-63: `current_circulation` = `−2ω` closed form; zero at equilibrium.
- [x] ISC-64: All-analytic, no RNG; inputs validated finite + positive
  (`ValueError` on NaN/inf/nonpositive).
- [x] ISC-65: `scripts/generate_steady_state_figure.py` renders
  `output/figures/steady_state_current.png` deterministically, orchestrator-only.
- [x] ISC-66: `manuscript/06_steady_state.md` exists, cites `{#fig:steady}`,
  states the k_BT≡1 convention and NESS-certified-by-current point.
- [x] ISC-67: `tests/test_steady_state.py` — no-mocks, analytic + operational refs.
- [x] ISC-68: Anti: §6 prose does not overclaim biology (nonequilibrium, not
  "alive"); dimensional entropy rate stated correctly (k_B·σ, not k_BT·σ).

### Formal verification — Lean 4 (§7, 2026-07-22 E5)
- [x] ISC-69: `formal/` is a self-contained Lean 4 Lake project (no mathlib,
  no external `require`) that `lake build`s cleanly.
- [x] ISC-70: `Geometry.lean` proves `solenoidal_orthogonal` ((Qg)·g=0).
- [x] ISC-71: `Geometry.lean` proves `flow_work_eq_dissipation` (f·g=-γ‖g‖²).
- [x] ISC-72: `Geometry.lean` proves `detailed_balance_iff` and
  `entropyProduction_nonneg` / `entropyProduction_zero_iff`.
- [x] ISC-73: `Information.lean` proves `relEntropy_nonneg` (Gibbs) via point
  tangent hypotheses (NOT a universal ∀ — that would be vacuous over ℤ).
- [x] ISC-74: `Information.lean` proves `freeEnergy_eq_surprise_add_relEntropy`,
  `freeEnergy_ge_surprise`, `freeEnergy_ge_surprise_of_model` (genuine j=r·E),
  `freeEnergy_eq_surprise_at_posterior` (attained-at, not iff).
- [x] ISC-75: Anti (vacuity): `Sanity.lean` proves a NEGATIVE control
  (`relEntropy_can_be_negative` = -20 → tangent hyp necessary).
- [x] ISC-76: Anti (vacuity): `Sanity.lean` proves a POSITIVE control on a
  genuine model (`okL` = 2-adic valuation, j=r·E real products) where all
  hypotheses hold and the bound fires with a non-trivial gap (-6 ≤ -4).
- [x] ISC-77: `Audit.lean` `#print axioms` on every headline theorem + witness
  reports only `[propext, Quot.sound]`; no `sorryAx`.
- [x] ISC-78: `tests/test_formal_lean.py` — no-mocks: greps for sorry/mathlib,
  checks witnesses present, runs real `lake build` + axiom-cleanliness.
- [x] ISC-79: `manuscript/07_formal_verification.md` cites the theorems, states
  the ℤ-vacuity trap honestly, and describes both controls.
- [x] ISC-80: Anti: no overclaim — "machine-checked" scoped to what's proved
  (total-scaled bound, attained-at posterior); vacuity trap disclosed.

### Refinements & consistency
- [x] ISC-26: `README.md` Layout + Roadmap updated to reflect the two new
  demonstrations and section files; build commands correct.
- [x] ISC-27: `TODO.md` current-state + roadmap checklist reflect what shipped
  (items 1 and 4 done; 2 and 3 remaining, honestly marked).
- [x] ISC-28: `data/claim_ledger.yaml` gains claims for the new figures' load-
  bearing constants (each with source + artifact_path).
- [x] ISC-29: `experiment_plan.yaml` extended with the new conditions/figures.
- [x] ISC-30: `manuscript/00_abstract.md` / `01_extended_abstract.md` reviewed;
  forward-reference to the demonstrations added without breaking length intent.
- [x] ISC-31: Anti: no RNG / `random`/`np.random` introduced anywhere in new
  `src/` or `scripts/` (grep returns nothing) — determinism preserved.
- [x] ISC-32: Anti: no mock framework (`unittest.mock`, `MagicMock`,
  `mocker.patch`) in new tests — grep returns nothing.
- [x] ISC-33: Anti: no business logic in `scripts/` — new scripts import all
  numerics from `src/` (grep new scripts for numpy math beyond layout).
- [x] ISC-34: Antecedent: baseline suite green BEFORE additions (captured at
  OBSERVE) so regressions are attributable.

## Test Strategy

| isc | type | check | threshold | tool |
|-----|------|-------|-----------|------|
| ISC-2 | analytic | posterior vs hand Bayes | 1e-12 | pytest |
| ISC-4 | analytic | VFE(post)=-ln p(s) | 1e-12 | pytest |
| ISC-5 | property | VFE(q)>-ln p(s) | strict | pytest |
| ISC-6 | analytic | complexity-accuracy id | 1e-12 | pytest |
| ISC-12/15 | property | ΔF ≤ 0 stepwise | ≤1e-9 | pytest |
| ISC-13 | property | r_final/r_0 | <0.01 | pytest |
| ISC-14 | property | \|Δθ\| | >2π | pytest |
| ISC-17 | analytic | RK4 vs e^{-γt} | 1e-6 | pytest |
| ISC-24/25 | gate | suite + coverage | pass, 100% | pytest --cov |
| ISC-9/19/23 | render | PNG exists non-empty | >0 bytes | pytest + Read |
| ISC-31/32/33 | anti | grep forbidden patterns | 0 hits | Grep |

### Governance

- authoritative_baseline: `uv run pytest projects/working/ActiveInferenceSynthetic/tests/ --cov=…/src --cov-fail-under=90` — 16 passed, 100% (OBSERVE)
- environment_probe: uv run under template `.venv`, `UV_CACHE_DIR=$TMPDIR/uvcache`
- production_entrypoint: the two figure scripts + pytest suite
- coactor_isolation: sidecar repo `working/ActiveInferenceSynthetic` on `main`, clean tree at OBSERVE
- owned_paths: ["src/generative_model.py","src/trajectories.py","scripts/generate_belief_update_figure.py","scripts/generate_trajectory_figure.py","tests/test_generative_model.py","tests/test_trajectories.py","manuscript/02_generative_model.md","manuscript/03_worked_regimes.md","README.md","TODO.md","data/claim_ledger.yaml","experiment_plan.yaml","ISA.md","manuscript/00_abstract.md","manuscript/01_extended_abstract.md"]
- visual_verification: Read rendered PNGs after generation
- long_pole_command: full pytest+coverage run
- final_gate_run_count: 1

## Features

| name | satisfies | depends_on | parallelizable |
|------|-----------|------------|----------------|
| generative_model core | ISC-1..8 | — | yes |
| generative_model figure+section | ISC-9,10 | core | no |
| trajectories core | ISC-11..18 | free_energy_flow | yes |
| trajectories figure+section | ISC-19,20 | core | no |
| test suites | ISC-21..25 | cores | no |
| refinements | ISC-26..33 | all | no |

## Decisions

- 2026-07-22: E4 from classifier (deep multi-file review + additions). Kept ISA
  proportionate (34 ISCs) rather than padding to the 128 soft floor — the work
  is two focused, deterministic modules, not a complex app; padding probes
  would be ceremony the doctrine warns against. Show-your-math logged here.
- 2026-07-22: Chose roadmap items #1 (generative model) and #4 (trajectories)
  over #2 (VFE/EFE) and #3 (Markov blanket). #1 closes the glaring "no inference
  demo" gap; #4 reuses the already-tested flow (lowest risk, highest reuse). #2
  and #3 each deserve their own section and are deferred honestly in TODO.
- 2026-07-22: Deterministic RK4 (not scipy) — keeps the no-new-deps + no-RNG
  constraints and stays analytic-testable against a linear-ODE closed form.
- 2026-07-22 (refined:): Advisor + Cato (codex read-only, cross-vendor) both
  confirmed the core science correct and both flagged that the reported total
  winding (−11.46 turns) is integration-window-dependent, not intrinsic. Fixed:
  the figure/prose/tests now report the intrinsic rotation *rate*
  (dθ/dt = −ω·precision, IC-free, exactly 0 at equilibrium), and reword the
  probability current as *generated/witnessed* by the deterministic drift, not
  *measured* by it. Cato additionally caught nan-on-zero-support in
  `vfe_components`/`minimize_free_energy` (masked + guarded), an
  independence gap in the VFE tests (added a hand-coded reference), and
  precision/step-size caveats now stated in docstrings and prose.
- 2026-07-22: Deferred (not a regression this session): `tests/conftest.py`
  root-resolution requires an `infrastructure/` ancestor, so a *standalone*
  sidecar clone cannot collect tests without the template tree. Works in the
  supported in-template checkout (68 tests green). Left untouched to avoid
  risking the green path; noted for a future standalone-harness pass.

## Changelog

- conjectured: an "Active Inference" overview could stand on the thermodynamic
  flow figure alone.
  refuted_by: the title's central concept (perception = inference by
  free-energy minimization) was asserted in prose but never shown; the project
  had zero inference demonstration.
  learned: the inference half (generative model + VFE bound) and the mechanics
  half (worked trajectories) are separable, each a self-contained tested
  demonstration; building both makes the "one currency, two directions" thesis
  literally visible.
  criterion_now: ISC-1..20 require both a generative-model inference demo and a
  worked-trajectory mechanics demo, each figure-anchored and analytically
  tested.
- conjectured: net rotation (accumulated winding) is a good scalar proxy for
  the NESS probability current.
  refuted_by: cross-vendor audit showed total winding scales with the
  integration window T and diverges as T→∞ — it is not intrinsic; and a
  deterministic decaying spiral is the *drift* of a NESS, not the current
  itself.
  learned: the intrinsic, IC-free witness is the rotation *rate*
  (dθ/dt = −ω·precision), exactly 0 at equilibrium; the honest claim is that
  nonzero winding *witnesses/generates* the current, not measures it.
  criterion_now: ISC-16 quantifies via `net_rotation`, and the manuscript +
  figure report the intrinsic rate with the window-total explicitly labelled.

## Changelog (extension)

- conjectured: the roadmap's remaining two demos (EFE action-selection, Markov
  blanket) would each need substantial new machinery.
  refuted_by: EFE reused the generative model's Bayes inversion directly, and the
  blanket reduced to standard Gaussian-graphical-model algebra (Schur complement
  + precision zero-block) — both are small, fully-analytic modules.
  learned: the four demonstrations compose into the full Active Inference arc
  (perception → mechanics → action → boundary) with no new dependencies; the
  "one currency, two directions" thesis becomes VFE(perception) + G(action) over
  the same generative model.
  criterion_now: ISC-35..56 cover EFE and blanket as tested, figure-anchored
  sections; ISC-57 holds the whole suite at 100% coverage.
- conjectured: "the explore/exploit trade-off is not tuned in" and the blanket's
  states "influence each other" are fair descriptions.
  refuted_by: cross-vendor audit — the specific EFE example is constructed (the
  mechanism is intrinsic, the numbers are not incidental), and a static Gaussian
  covariance is statistical coupling, not causal influence.
  learned: separate the intrinsic mechanism claim (honest) from the illustrative
  example (constructed), and never let a covariance imply causation without a
  dynamical/interventional model.
  criterion_now: §4/§5 prose reworded; the honesty holds under the audit.

## Verification

- ISC-1..8, 21: `uv run pytest tests/test_generative_model.py` — 34 tests
  green; posterior/VFE/bound asserted to analytic references (independent
  hand-coded VFE reference `0.3*ln(0.3/0.54)+0.7*ln(0.7/0.08)` matches to
  1e-12; `test_vfe_at_posterior_equals_surprise` abs=1e-12;
  `test_vfe_bounds_surprise_from_above` positive control on 3 off-posterior q).
- ISC-9, 19, 23: figure smoke tests — `test_generate_demonstration_figures.py`
  (2 params) render real non-empty PNGs (PNG signature checked); both figures
  visually confirmed (belief bars → posterior 0.87; NESS spiral, rate −0.95
  turns/time).
- ISC-11..18, 22: `tests/test_trajectories.py` — RK4 vs `x0·e^{-γΠt}` (1e-6);
  `test_ness_rotation_rate_is_intrinsic` binds net rotation to −ω·Π·T across 3
  starts (rel 1e-3); equilibrium net rotation < 1e-6; descent monotone both
  regimes.
- ISC-24, 25: definitive gate `uv run pytest tests/ --cov=…/src
  --cov-fail-under=90` → "68 passed", "Total coverage: 100.00%" (all five src
  modules 100%). final_gate_run_count = 1 at the final tree.
- ISC-26..30: README/TODO/claim_ledger/experiment_plan/config + extended
  abstract updated (Read-confirmed); claim-ledger `trajectory-ness-rotation-rate`
  value −0.9549… matches analytic −ω·Π/(2π).
- ISC-31: `grep random|np.random|rng|seed` new src/scripts → "CLEAN: no RNG".
- ISC-32: `grep unittest.mock|MagicMock|mocker.patch` new tests → "CLEAN".
- ISC-33: new scripts contain no core math (only a drawing function named
  `_draw_free_energy_panel`); all numerics imported from `src/`.
- ISC-34: baseline captured at OBSERVE — 16 tests green, 100% coverage before
  additions.
- Advisor: `Inference.ts --mode advisor` invoked — science sound, two label
  tightenings demanded (rate-not-total, generates-not-measures), both applied.
- Cato/cross-vendor: `codex exec --sandbox read-only` invoked — core CONFIRMED
  correct; 7 defects triaged, 6 fixed (VFE test independence, nan guards, lr /
  dt / precision / origin caveats, NESS-vs-stochastic wording), 1 deferred with
  reason (standalone conftest).
- Reflection Ledger v2: entry_id cbec234c-f201-493e-81ea-3e2f37417bd2 @ 2026-07-22T16:09:21.484Z (34/34 passed, 0 failed/open/deferred).
- Reflection Ledger v2 (E5 extension): entry_id 5b7852b7-ddbe-4593-90b7-408149eb66d8 @ 2026-07-22T16:48:41.527Z (24/24 passed, 0 failed/open/deferred).
- Reflection Ledger v2 (§6 capstone): entry_id 711a754a-d767-49c1-bd83-423d4e64ac19 @ 2026-07-22T17:25:16.026Z (10/10 passed, 0 failed/open/deferred).
- Reflection Ledger v2 (§7 formal): entry_id 716335c4-7bde-49ad-bfd7-904ebb9e9fc3 @ 2026-07-22T19:32:36.606Z (12/12 passed, 0 failed/open/deferred).

### Formal-verification verification (§7 Lean, E5, 2026-07-22)

- ISC-69..77: `cd formal && lake build` → "Build completed successfully (7
  jobs)"; the Audit module's `#print axioms` on all 9 headline theorems + 4
  witnesses reports only `[propext, Quot.sound]` (two witnesses "does not depend
  on any axioms") — no `sorryAx`, no mathlib.
- ISC-78: `tests/test_formal_lean.py` (6 tests) — grep no-sorry (comment-aware),
  no-mathlib, headline + witness theorems present, and a real `lake build` with
  an axiom-cleanliness assertion; all green in the full suite (152 passed).
- ISC-73..76 (vacuity): the Advisor caught that a UNIVERSAL `Tangent`/`LogAdd`
  over ℤ is unsatisfiable (integer rounding on {2,3}), which would make the
  free-energy theorems vacuously true despite a clean build. Fixed: theorems now
  take point hypotheses; `Sanity.lean` proves a negative control (necessity) AND
  a positive control on a genuine 2-adic-valuation model (satisfiability, gap
  -6 ≤ -4). Verified `okL_bound_holds` instantiates `freeEnergy_ge_surprise_of_model`.
- Definitive gate: full project suite "152 passed", src coverage 100.00%,
  final_gate_run_count = 1.
- Advisor: `Inference.ts --mode advisor` — delivered the pivotal vacuity finding
  (universal-domain hypotheses unsatisfiable ⇒ vacuous); its prescribed fix
  (point hypotheses + positive control) was applied in full.
- Cato/cross-vendor: `codex exec --sandbox read-only` — CONFIRMED the fix (okL is
  a real positive control; cleared tangent inequality and decomposition correct;
  geometry non-trivial); 3 faithfulness refinements applied: genuine model
  (j=r·E via 2-adic valuation) not hand-picked values, positive-total qualifier
  on normalized recovery, and "attained at" (not "precisely/iff at") the posterior.

## Changelog (§7 formal)

- conjectured: a clean `lake build` with no `sorry` and minimal axioms proves the
  formalization is faithful.
  refuted_by: the Advisor showed a universal `Tangent` hypothesis over ℤ is
  unsatisfiable (no integer L clears the tangent bound on both orientations of
  {2,3}), so the free-energy theorems were VACUOUSLY true — green build, clean
  axioms, zero content. A negative-control witness (`badL`) proves a hypothesis
  restrictive but not that it is satisfiable.
  learned: for a conditional formalization, "no sorry + clean axioms" is
  necessary but not sufficient; non-vacuity requires a POSITIVE control — an
  exhibited model where the hypotheses hold and the conclusion is non-trivial.
  Cross-vendor review then demanded the model be genuine (j=r·E, log-additive L),
  not merely locally consistent point values.
  criterion_now: ISC-73..76 require point hypotheses plus both a negative and a
  positive control (the latter on a real 2-adic-valuation generative model), all
  axiom-audited and tested.

### Capstone verification (§6 steady state, E5, 2026-07-22)

- ISC-59..64, 67: `tests/test_steady_state.py` (18 tests) — Σ=P⁻¹ (Lyapunov,
  1e-12) + Lyapunov residual == 0; entropy production == 2ω²Π/γ closed form AND
  == grid-quadrature of ∫jᵀD⁻¹j/ρ (rel 1e-3, operationally independent);
  circulation == −2ω; current div-free (finite-diff <1e-6), ⊥∇F (<1e-12),
  pointwise orientation positive-control; equilibrium controls (σ=0, j≡0);
  finite/positive param validation + ill-conditioned Lyapunov rejection.
- ISC-65: figure smoke test renders real PNG; figure visually confirmed
  (equilibrium σ=0 no current; NESS σ=11.52 circulating field).
- ISC-57 (extended): definitive gate → "146 passed", "Total coverage: 100.00%"
  (all 8 src modules 100%). final_gate_run_count = 1.
- ISC-68: no-RNG grep CLEAN; §6 prose reworded to nonequilibrium (not "alive");
  k_B·σ dimensional statement corrected.
- Advisor: `Inference.ts --mode advisor` — independently re-derived all three
  results (Σ=P⁻¹, j=(QPx)ρ, σ=2ω²Π/γ) as CORRECT; demanded the k_BT≡1 note, the
  current-not-density NESS point, and one non-analytic cross-check — all added.
- Cato/cross-vendor: `codex exec --sandbox read-only` — core CONFIRMED correct
  (Lyapunov, current, σ, circulation, normalization, σ=11.52, grid-check not
  green-by-construction); 7 findings, all fixed: finite-param validation,
  Lyapunov residual guard, pointwise-orientation positive control, divide-by-zero
  in the grid test, a wrong cross-product comment, the k_Bσ dimensional
  correction, and the biology overclaim.

### Extension verification (roadmap #2 + #3, E5, 2026-07-22)

- ISC-35..46 (EFE): `tests/test_expected_free_energy.py` — predicted_outcomes /
  posteriors / pragmatic / epistemic hand-checked; `epistemic == I(s;o|a)`
  cross-checked against an independently computed mutual information
  (`test_epistemic_value_equals_mutual_information`); explore/exploit flip
  asserted both directions (flat→cue G 0.325<0.693; sharp→bet G 0.435<0.836);
  epistemic non-negativity + FP-roundoff clamp regression; NaN inputs rejected.
- ISC-47..56 (blanket): `tests/test_markov_blanket.py` — Schur complement vs
  hand value; marginal-dependent (corr 0.189) AND machine-zero conditional
  (partial corr <1e-10) pinned in one positive-control assertion; partial-blanket
  negative control (0.040 ≠ 0); `is_markov_blanket` True/False + SPD/symmetry/
  finite/tol validation; `covariance_from_precision` ill-conditioned guard.
- ISC-57: definitive gate `uv run pytest tests/ --cov=…/src --cov-fail-under=90`
  → "127 passed", "Total coverage: 100.00%" (all 7 src modules 100%).
  final_gate_run_count = 1 at the final tree.
- ISC-58: `grep random|np.random|MagicMock|mocker.patch` new modules/tests →
  "CLEAN"; new figure scripts hold no core math (markov `inv` moved into
  `src.markov_blanket.covariance_from_precision`).
- Figures: `expected_free_energy.png` (flip: explore G 0.33 / exploit G 0.43)
  and `markov_blanket.png` (corr 0.19 vs precision 0.00) rendered + visually
  confirmed; both smoke-tested to real non-empty PNGs.
- Advisor: `Inference.ts --mode advisor` — both conventions confirmed standard;
  demanded MI cross-check (added) and a combined positive-control blanket test
  (added). Sign-convention note added to the EFE docstring.
- Cato/cross-vendor: `codex exec --sandbox read-only` — core CONFIRMED correct
  (equations, Bayes inversion, flip, Schur complement, numbers match prose); 6
  findings, all fixed: epistemic FP clamp, NaN-input rejection (EFE +
  generative_model via R14 sweep), `is_markov_blanket` SPD validation,
  ill-conditioned inversion guard, "constructed demonstration" wording (§4),
  causal→statistical wording (§5).
