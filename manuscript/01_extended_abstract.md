# Extended Abstract {#sec:extended}

A thing that persists must, in effect, hold a model of the world that keeps
it intact. **Active Inference** turns that observation into mechanics: a
system maintains itself by minimizing *variational free energy*, a single
quantity that scores how badly its internal expectations fit incoming
sensations [@friston2010fep; @parr2022active]. Perception lowers free
energy by updating beliefs; action lowers it by changing the world so the
beliefs come true. One currency, two directions — inference and control —
which is why the same template reappears from single cells to brains to
institutions.

The bound is what makes this *applicable* rather than metaphorical.
Variational free energy is an upper bound on **surprise**, the negative log
evidence $-\ln p(s)$ a system assigns to its own sensory states. Because the
bound is computable from a system's own beliefs, minimizing it *is*
approximate Bayesian inference carried out by the physical dynamics of the
thing itself. The accounting is organized by a **Markov blanket**: a
statistical boundary splitting *external* states $\eta$ from *internal*
states $\mu$, coupled only through *sensory* and *active* blanket states.
Internal states come to parameterize beliefs about the external world they
can never touch directly — the core claim of **Bayesian mechanics**, a
physics written in terms of, and by, those beliefs
[@dacosta2021bayesian; @ramstead2023bayesian].

[@fig:overview] shows the move that this overview is built around, without a
single equation of derivation. Both panels live on *the same* free-energy
landscape — a Gaussian bowl whose floor is the system's expected state. At
**equilibrium** (panel a) the flow is pure descent, $f=-\nabla F$: every
trajectory falls straight to the mode and stops. Detailed balance holds,
there is no net current, and — taken literally — nothing further happens. A
rock is at equilibrium; so, eventually, is a system that has stopped doing
anything. Living systems occupy panel (b). There the flow gains a
*solenoidal* term, $f=(Q-\Gamma)\nabla F$, that runs along the contours of
$F$ rather than down them. Free energy is still minimized — the system still
tracks its niche — yet probability mass **circulates** indefinitely in a
**non-equilibrium steady state**. That persistent current is the signature
of things that stay far from equilibrium: heartbeats, foraging, perception
that never settles. The gradient part is the Free Energy Principle's
"climbing down surprise"; the solenoidal part is what keeps the system
alive while doing so [@friston2023bayesian].

Read the two panels together and the headline of Active Inference is
visible at a glance: the *same* imperative — minimize free energy — produces
inert relaxation in one regime and open-ended, self-sustaining behavior in
the other. The rest of this overview unpacks that picture in the spirit of
*show, not tell*: each subsequent section adds one runnable, minimal
demonstration rather than another layer of formalism.

![**One landscape, two regimes.** Both panels place the system on the same Gaussian free-energy bowl (grey contours; the black dot marks the mode, where free energy is least). **(a) Equilibrium:** the flow is pure gradient descent on free energy, $f=-\nabla F$ (blue arrows). Detailed balance holds, so trajectories fall to the mode and come to rest with no net probability current. **(b) Far-from-equilibrium (NESS):** an antisymmetric *solenoidal* operator $Q$ adds a conservative current, $f=(Q-\Gamma)\nabla F$ (orange streamlines), that flows along the level sets of $F$. Free energy is still minimized, but probability mass circulates without end — the hallmark of living, self-organizing systems. The Free Energy Principle is the descent term; Bayesian mechanics adds the circulation. Internal states $\mu$ infer external states $\eta$ across a Markov blanket (sensory $s$, active $a$). Figure rendered deterministically by `scripts/generate_overview_figure.py` over the tested flow in `src/free_energy_flow.py`.](../output/figures/active_inference_overview.png){#fig:overview width=94%}
