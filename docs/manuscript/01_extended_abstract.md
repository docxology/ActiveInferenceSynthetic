# Introduction and Extended Abstract {#sec:extended}

This is a worked introduction to Active Inference and synthetic intelligences
across equilibrium and non-equilibrium thermodynamic and informational settings.
The examples connect the Free Energy Principle and Bayesian mechanics to
inference, action, and self-organization. The broader `fep_formal` library
provides the mathematical reference [@fepformal2026software; @friedman2026formalization]; this paper supplies selected executable
models and their exposition. Variational, expected, and thermodynamic free
energy have distinct definitions and units. Persistent stationary current
alone is not evidence of life or intelligence.

**Active Inference** connects inference and action within a specified generative
model [@friston2010fep; @parr2022active]. Updating a candidate belief changes its
variational free energy after an observation. Choosing a future policy instead
requires an objective over predicted outcomes, with explicit preferences and
information terms. Those objectives are related by their model assumptions;
they are not interchangeable quantities. Whether a biological or engineered
system realizes such computations is a further scientific question.

On the admitted support domain, variational free energy bounds **surprise**,
the negative log evidence $-\ln p(s)$. The finite demonstration can compute
both the exact posterior and that evidence independently, so the identity has
a direct numerical check. Relating this inference calculation to physical
dynamics requires additional assumptions. Likewise, a **Markov blanket** states
conditional independence between *external* states $\eta$ and *internal* states
$\mu$ given *sensory* and *active* blanket states. That screening condition
alone does not establish causal direction or a representational mapping.
**Bayesian mechanics** investigates such mappings under specified dynamical
and statistical hypotheses [@dacosta2021bayesian; @ramstead2023bayesian].

[@fig:overview] shows the move that this overview is built around, without a
single equation of derivation. Both panels live on *the same* free-energy
landscape — a Gaussian bowl whose floor is the system's expected state. At
**equilibrium** (panel a) the flow is pure descent, $f=-\nabla F$: every
trajectory falls straight to the mode and stops. Detailed balance holds,
the stationary probability current vanishes. This does not mean that
stochastic microscopic motion ceases.
Panel (b) supplies a contrasting non-equilibrium example. There the flow gains a
*solenoidal* term, $f=(Q-\Gamma)\nabla F$, that runs along the contours of
$F$ rather than down them. The deterministic drift still lowers the quadratic
potential, while stationary probability mass **circulates** indefinitely in a
**non-equilibrium steady state**. That persistent current diagnoses broken
detailed balance in the stated diffusion model. The gradient part illustrates
the Free Energy Principle's descent; the solenoidal part supplies conservative
circulation in this example [@friston2023bayesian].

Read the two panels together and the headline of Active Inference is
visible at a glance: the *same* imperative — minimize free energy — produces
relaxation in one regime and persistent stationary current in the other.
The rest of this overview unpacks that picture in the spirit of
*show, not tell*: each section adds one runnable, minimal demonstration
rather than another layer of formalism. [@sec:generative-model] makes the
*inference* concrete — that minimizing variational free energy over a
generative model **is** Bayesian updating, and that free energy is a tight
upper bound on surprise. [@sec:worked-regimes] makes the *mechanics*
concrete — integrating the flow above into worked equilibrium and
non-equilibrium trajectories and quantifying the persistent current that
separates these two model regimes. [@sec:expected-free-energy]
turns to *action* — evaluating expected free energy over policies, whose pragmatic
and epistemic terms produce the explore/exploit balance from one rule.
[@sec:markov-blanket] exhibits conditional screening in a specified Gaussian
model; a representational interpretation requires further hypotheses.
[@sec:steady-state] quantifies the non-equilibrium
regime outright — the analytic probability current and the entropy-production
rate that is zero exactly at detailed balance and positive out of it. Finally
[@sec:formal] closes the loop on rigour: the load-bearing theorems — Gibbs'
inequality, the free-energy bound, the conservative solenoidal current, the sign
of entropy production — are **machine-checked in Lean 4**, proved from the
kernel's axioms with no `sorry`: the real-valued exposition imports the
`FepSketches` library maintained in `fep_formal`.

![**One landscape, two drift regimes.** Grey contours show the same Gaussian dimensionless potential; the black dot is its mode. **(a)** Zero drive gives radial deterministic relaxation. **(b)** An antisymmetric operator adds tangential motion to the same dissipative drift, producing a relaxing spiral. With matched diffusion, these drifts correspond to equilibrium and a non-equilibrium steady state, respectively; stationary current is computed separately in [@sec:steady-state]. The diagram does not establish a universal identification of FEP with gradient descent, or a belief interpretation from a statistical partition alone. Rendered from the tested numerical flow.](../output/figures/active_inference_overview.png){#fig:overview width=94%}
