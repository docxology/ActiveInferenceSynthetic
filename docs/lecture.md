# Lecture: Equilibrium and Non-Equilibrium in Active Inference

A ~20-minute LectureCreate video walkthrough of the equilibrium /
non-equilibrium structure of active inference, produced from the AIS
codebase's live demonstrations.

## What it covers

1. Equilibrium as gradient flow with detailed balance (OU model).
2. Breaking it: the solenoidal term and circulating probability currents.
3. Measuring it: entropy production rate, time-reversal asymmetry.
4. The dial view: omega interpolates smoothly between the regimes.
5. Free energy: perception as dissipative descent on F, action as
   solenoidal circulation driven by expected free energy G.
6. The Markov blanket as the maintained non-equilibrium boundary.

## Numbers and provenance

Every numeric claim in the lecture comes from `src/manuscript_variables.py`
(`compute_claims()` / `generate_variables()`), which computes values from
the same deterministic demo cores the figures and tests call — never
hand-copied literals. Key live values used: NESS omega 2.4, entropy
production 11.52 nats/time, trajectory winding 4.58 turns / 12 time units
(0.38 turns/time), blanket marginal correlation 0.19, belief descent
uniform → 0.87 in 60 steps, look-then-leap EFE 0.07 vs 0.43.

## Figure-to-section mapping

| Asset | Lecture content |
| --- | --- |
| `assets/worked_trajectories.png` | s1 equilibrium decay, s2 NESS spiral |
| `assets/steady_state_current.png` | s3 current fields, s6 recap |
| `assets/belief_update.png` | s4 perception as free-energy descent |
| `assets/expected_free_energy.png` | s4 explore vs exploit |
| `assets/policy_planning.png` | s4 look-then-leap planning |
| `assets/markov_blanket.png` | s5 blanket precision/correlation |

Figures are rendered by `src/figures/` (300 DPI, deterministic) into
`output/figures/`. The `assets/` names above are the copies inside the
LectureCreate workspace — this repository does not contain an `assets/`
directory; the files are mirrored there from `output/figures/`.

## Production recipe (LectureCreate)

LectureCreate is an **external** tool. Neither it nor `lecture.yaml` lives in
this repository, and none of the steps below run in this project's `.venv` or
as part of its gates. Run them from the LectureCreate workspace, with that
tool's own environment on `PATH`:

1. Author `lecture.yaml` (schema v1.0; equations go in the `equation:`
   field with `mathtext: true`).
2. `lecturecreate validate lecture.yaml` — must pass.
3. `lecturecreate lint lecture.yaml` — require 0 findings.
4. Pre-verify every equation renders as matplotlib mathtext
   (`\frac` not `\tfrac`, `\mathrm{}` not `\text{}`; no `\underbrace`).
5. Render.

The only obligation on *this* repository is that the numbers and figures the
lecture cites stay reproducible here — regenerate them with
`uv run python scripts/generate_all_figures.py` from the project root.
