# Abstract {#sec:abstract}

Active Inference casts perception and action as free-energy minimization. This overview shows how Bayesian mechanics carries the Free Energy Principle from equilibrium to far-from-equilibrium life.



```{=latex}
\newpage
```


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
*show, not tell*: each section adds one runnable, minimal demonstration
rather than another layer of formalism. [@sec:generative-model] makes the
*inference* concrete — that minimizing variational free energy over a
generative model **is** Bayesian updating, and that free energy is a tight
upper bound on surprise. [@sec:worked-regimes] makes the *mechanics*
concrete — integrating the flow above into worked equilibrium and
non-equilibrium trajectories and quantifying the persistent current that
separates the living regime from the inert one. [@sec:expected-free-energy]
turns to *action* — minimizing the same currency over policies, whose pragmatic
and epistemic terms produce the explore/exploit balance from one rule. [@sec:markov-blanket] exhibits the *boundary* itself — the Markov blanket that
makes internal states inferring an external world a well-posed idea rather than
a metaphor. [@sec:steady-state] quantifies the far-from-equilibrium
regime outright — the analytic probability current and the entropy-production
rate that is zero exactly at detailed balance and positive out of it. Finally
[@sec:formal] closes the loop on rigour: the load-bearing theorems — Gibbs'
inequality, the free-energy bound, the conservative solenoidal current, the sign
of entropy production — are **machine-checked in Lean 4**, proved from the
kernel's axioms with no `sorry` and no external library.

![**One landscape, two regimes.** Both panels place the system on the same Gaussian free-energy bowl (grey contours; the black dot marks the mode, where free energy is least). **(a) Equilibrium:** the flow is pure gradient descent on free energy, $f=-\nabla F$ (blue arrows). Detailed balance holds, so trajectories fall to the mode and come to rest with no net probability current. **(b) Far-from-equilibrium (NESS):** an antisymmetric *solenoidal* operator $Q$ adds a conservative current, $f=(Q-\Gamma)\nabla F$ (orange streamlines), that flows along the level sets of $F$. Free energy is still minimized, but probability mass circulates without end — the hallmark of living, self-organizing systems. The Free Energy Principle is the descent term; Bayesian mechanics adds the circulation. Internal states $\mu$ infer external states $\eta$ across a Markov blanket (sensory $s$, active $a$). Figure rendered deterministically by `scripts/generate_overview_figure.py` over the tested flow in `src/free_energy_flow.py`.](../figures/active_inference_overview.png){#fig:overview width=94%}



```{=latex}
\newpage
```


# Perception as Inference {#sec:generative-model}

The extended abstract makes a strong claim in one sentence: *minimizing
variational free energy **is** approximate Bayesian inference, carried out by
the physical dynamics of the thing itself*. This section makes that claim
runnable. It is the smallest generative model that still says something true,
and everything below is checked against closed-form Bayes in
`src/generative_model.py`.

A system holds a **generative model** of a hidden cause $x$ and a sensation
$s$: a prior $p(x)$ over states and a likelihood $p(s \mid x)$ saying which
sensations each state tends to produce. Together they fix the joint
$p(s, x) = p(s \mid x)\,p(x)$, the evidence $p(s) = \sum_x p(s, x)$, and — by
Bayes' rule — the posterior $p(x \mid s) = p(s, x) / p(s)$. The system never
sees $x$; it only ever has $s$ and its own model. Inference is the problem of
recovering $p(x \mid s)$ from those.

Active Inference solves it without ever computing $p(s)$ directly, through a
belief $q(x)$ and a single scalar, the **variational free energy**:

$$
F[q] \;=\; \underbrace{\mathrm{KL}\!\left[q(x)\,\Vert\,p(x)\right]}_{\text{complexity}}
\;-\; \underbrace{\mathbb{E}_{q}\!\left[\ln p(s \mid x)\right]}_{\text{accuracy}}.
$$

Two facts, both asserted to machine precision in the tests, make $F$ the whole
game. First, **$F$ is an upper bound on surprise**: $F[q] = -\ln p(s) +
\mathrm{KL}\!\left[q \Vert p(x \mid s)\right] \ge -\ln p(s)$, because a KL
divergence is never negative. Surprise $-\ln p(s)$ is exactly what an organism
"wants" to keep low — the improbability of its own sensory state — but it
cannot compute it. It *can* compute $F$, from quantities it already has.
Second, **the bound is tight at the posterior**: $F$ is least, and equals the
surprise, precisely when $q = p(x \mid s)$. So the belief that minimizes free
energy is the Bayesian posterior, and the minimized value is the surprise it
bounds. Inference falls out of minimization.

[@fig:belief] shows this happening. Take a two-state model with prior
$p(x) = (0.60, 0.40)$ and a likelihood under which state $x_0$ makes the observed
sensation $s$ far more probable than $x_1$ does. Panel (a) starts from a
maximally uncommitted uniform belief and runs gradient descent on $F$ over the
belief simplex; the belief mass migrates toward the exact posterior
$p(x_0 \mid s) = 0.54/0.62 \approx 0.87$. Panel (b) tracks $F$ across the same
descent: it falls **monotonically** to the surprise $-\ln p(s)$ (dashed line),
and the shrinking shaded gap is exactly $\mathrm{KL}\!\left[q_t \Vert p(x \mid
s)\right]$ — the belief's remaining error. Perception, here, is nothing but
this descent: the system lowers free energy by updating beliefs, and in doing
so recovers the posterior it could not compute directly.

The complexity–accuracy split names the trade-off. *Accuracy* rewards beliefs
that explain the sensation; *complexity* penalizes moving away from the prior.
Perception moves beliefs only as far as the evidence warrants — the same
regularized fit that makes the free-energy principle a principle rather than a
slogan. Action, treated in the next demonstrations, minimizes the *same* $F$ in
the other direction: by changing $s$ rather than $q$.

![**Perception as free-energy minimization.** A two-state generative model
(prior $p(x)=(0.60,0.40)$; likelihood favouring $x_0$ for the observed $s$). **(a)**
From a uniform starting belief, gradient descent on variational free energy
drives the belief over hidden states to the exact Bayesian posterior
$p(x\mid s)$ (orange), passing through intermediate beliefs (blue) on the way.
**(b)** Along the same descent the free energy $F[q_t]$ falls monotonically to
the surprise $-\ln p(s)$ (dashed) that it bounds; the shaded gap is exactly
$\mathrm{KL}[q_t\Vert p(x\mid s)]$, the belief's error, which closes as
inference completes. Minimizing free energy is Bayesian updating. Rendered
deterministically by `scripts/generate_belief_update_figure.py` over the tested
core in `src/generative_model.py`.](../figures/belief_update.png){#fig:belief width=92%}



```{=latex}
\newpage
```


# Worked Regimes: Equilibrium and Non-Equilibrium {#sec:worked-regimes}

The overview figure ([@fig:overview]) contrasts two *flows* — one that comes to
rest, one that circulates — as arrow fields. A flow field says where a system
would go next; it does not, on its own, show where a system *ends up*. This
section integrates the flow into actual **trajectories**, so the
equilibrium↔non-equilibrium distinction becomes a path you can watch, and the
"persistent current" of living systems becomes a number rather than an
adjective. The integrator and its diagnostics live in `src/trajectories.py`,
built directly on the tested flow of `src/free_energy_flow.py`.

Both regimes obey the Bayesian-mechanics flow $f = (Q - \Gamma)\nabla F$ on the
*same* isotropic Gaussian free-energy landscape. The only difference is the
antisymmetric solenoidal operator $Q$: zero at equilibrium, nonzero in a
non-equilibrium steady state (NESS). A fixed-step fourth-order Runge–Kutta
scheme (no adaptive stepping, no randomness) advances a starting point under
this flow. That the integrator can be trusted is not assumed: at equilibrium
the flow reduces to the linear system $\dot{x} = -\gamma\,\Pi\,x$ (with $\Pi$
the precision), and the tests confirm the RK4 path matches the closed form
$x(t) = x_0\,e^{-\gamma\,\Pi\,t}$ — i.e. $x_0 e^{-\gamma t}$ at unit precision —
to better than $10^{-6}$.

[@fig:trajectories] shows the two fates. In panel (a), the **equilibrium**
trajectory ($Q = 0$) falls straight down the free-energy gradient to the mode
and stops. Free energy decreases monotonically along the path, the radius
collapses to under 1% of its starting value, and the net angle swept about the
mode is zero to numerical precision — detailed balance, no current. This is a
rock settling, a battery draining, a belief that has finished inferring.

Panel (b) is the **NESS** ($Q \neq 0$). The dissipative term still pulls the
system down $F$ — free energy again decreases monotonically, so the system is
*still* minimizing surprise — yet the solenoidal term drives it *around* the
level sets of $F$ at the same time. The result is a spiral that sweeps many
full turns before relaxing inward.

How much it winds is worth stating carefully. The *total* net rotation — the
figure's $\approx -4.58$ turns over the demonstration window $T=12$ — is not an
intrinsic property of the NESS; it grows with $T$ and would diverge as
$T \to \infty$. The intrinsic, initial-condition-free quantity is the
**rotation rate**. For this isotropic-Gaussian flow the angular velocity is
analytically constant, $\dot\theta = -\omega\,\Pi$ radians per unit time (with
$\Pi$ the precision), so the rate is $\approx -0.38$ turns per unit time
($-\omega\,\Pi/(2\pi)$ at $\omega=2.4$, $\Pi=1$) for *any* starting point off
the mode — and it is exactly $0$ at equilibrium for every window. That
zero-versus-nonzero rate is the honest, quantitative witness that detailed
balance is broken. The tests pin it directly: net rotation equals
$-\omega\,\Pi\,T$ across several starting points to a tenth of a percent.

One more distinction keeps the claim precise. Taken on its own, the
deterministic trajectory here *relaxes* — it spirals into the mode and would sit
there. A genuine non-equilibrium steady state is a property of the *stochastic*
system: a stationary density $\rho \propto e^{-F}$ carrying a divergence-free
probability current $j = Q\nabla F\,\rho$ that never dies. What the figure shows
is that system's **deterministic drift**, and the spiral is the mechanistic
*origin* of that current, not a measurement of it. So the honest reading of
"NESS" here is precise: the nonzero winding **witnesses** the solenoidal
$Q \neq 0$ that breaks detailed balance and thereby renders the corresponding
stochastic stationary state a non-equilibrium one. Reverse the sign of $Q$ and
the circulation reverses with it, as the tests confirm.
([@sec:steady-state] supplies the measurement this section withholds — the
actual probability current and its entropy-production rate.)

Read the two panels against the abstract's thesis. Descent — the Free Energy
Principle's "climbing down surprise" — is common to both; it is present in the
falling free energy of *each* trajectory. What separates the living regime from
the inert one is not whether free energy is minimized but whether a conservative
current runs *alongside* the descent, keeping the system in perpetual, ordered
motion while it stays close to its expected states. Equilibrium is where things
stop; the non-equilibrium steady state is where things stay alive.

![**Worked trajectories over one landscape.** Both panels integrate the
Bayesian-mechanics flow $f=(Q-\Gamma)\nabla F$ from the same starting point
(coloured dot) over the same Gaussian free-energy bowl (grey contours; black
dot marks the mode). **(a) Equilibrium** ($Q=0$): pure descent falls radially
to the mode and rests — free energy monotonically decreasing, rotation rate
$\approx 0$ turns/time. **(b) NESS** ($Q\neq 0$): the same descent plus a
solenoidal term spirals inward at a constant rate $\approx -0.38$ turns/time
($\approx -4.58$ turns over the window $T=12$) while free energy still decreases
monotonically. The nonzero rotation rate witnesses the broken detailed balance
that generates the steady-state probability current — the marker distinguishing
far-from-equilibrium life from equilibrium rest. Rendered deterministically by
`scripts/generate_trajectory_figure.py` over the tested cores in
`src/trajectories.py` and `src/free_energy_flow.py`.](../figures/worked_trajectories.png){#fig:trajectories width=94%}



```{=latex}
\newpage
```


# Action: Variational vs Expected Free Energy {#sec:expected-free-energy}

[@sec:generative-model] showed perception: minimizing **variational** free
energy $F$ over beliefs about what is happening *now*. But a thing that only
perceived would be a spectator. Active Inference closes the loop by minimizing
the *same* currency in the other direction — over **actions**, scored by the
free energy they are *expected* to produce. That forward-looking quantity is
**expected free energy** $G$, and it is what turns inference into behavior. The
core is `src/expected_free_energy.py`; every value below is checked against a
hand-worked reference.

The two free energies differ only in tense. $F[q]$ grades a belief against a
sensation already in hand — it is retrospective, and its minimum is the
posterior. $G(a)$ grades a *candidate action* against the sensations it *would*
generate, averaged over what the agent currently believes. For an action $a$,
belief $q(s)$, outcome model $p(o \mid s, a)$, and preferences
$p_{\text{pref}}(o)$ — a distribution over the outcomes the agent wants to
encounter — $G$ splits into two terms the agent seeks to make large (so it
minimizes their negatives):

$$
G(a) \;=\; -\underbrace{\mathbb{E}_{q(o\mid a)}\big[\ln p_{\text{pref}}(o)\big]}_{\text{pragmatic value}}
\;-\; \underbrace{\mathbb{E}_{q(o\mid a)}\!\big[\mathrm{KL}[\,q(s\mid o,a)\,\Vert\,q(s)\,]\big]}_{\text{epistemic value}}.
$$

**Pragmatic value** is expected utility: how well an action's likely outcomes
match what the agent prefers. **Epistemic value** is expected information gain —
how much the action's outcomes would sharpen the belief about the hidden state,
which is exactly the mutual information $I(s; o \mid a)$ and is always
non-negative. One is the drive to *get what you want*; the other is the drive to
*find out*. Both live inside a single number.

[@fig:efe] shows why that unification matters. An agent is unsure which of two
contexts holds ($q(s) = (0.50, 0.50)$) and can take one of two actions:
a **cue** that would reveal the context (highly informative, epistemic value
$+0.37$ nats, but preference-neutral) or a **bet** that pays off regardless of
context (uninformative, epistemic value $0$, but potentially rewarding). The
*only* thing that changes between the two panels is the preferences. Under
**flat** preferences (panel a) the agent has nothing to chase, so the epistemic
term decides: it takes the cue and **explores** ($G = 0.33$ vs 0.69). Under
**sharp** preferences (panel b) the pull of the reward dominates, and the same
minimization takes the bet and **exploits** ($G = 0.43$ vs 0.84). This is a
deliberately constructed two-action example, chosen to isolate the mechanism;
what it demonstrates is structural, not incidental to these numbers. The
explore/exploit trade-off is not a separate rule bolted onto the agent — there
is one rule, $\arg\min_a G$. Because $G$ carries both a pragmatic and an
epistemic term, exploration and exploitation are the two limits of a single
balance, and which one wins is decided by the preferences alone.

This is the whole architecture in miniature. Perception ($F$) and action ($G$)
are one imperative — minimize free energy — read in two tenses. Inference makes
beliefs fit the world; action makes the world fit beliefs *and* preferences,
gathering information where it is uncertain and reward where it is confident.

![**One rule yields explore and exploit.** An agent uncertain between two
contexts ($q(s)=(0.50,0.50)$) chooses between an informative "cue" (epistemic
value $+0.37$, preference-neutral) and a rewarding but uninformative "bet"
(epistemic value $0$). Bars are expected free energy $G$ per action (lower is
chosen); each is annotated with its pragmatic/epistemic split. **(a) Flat
preferences:** the epistemic term dominates, so the agent explores (cue,
$G=0.33$). **(b) Sharp preferences:** the pragmatic term dominates, so the same
$\arg\min G$ rule exploits (bet, $G=0.43$). A single rule; the balance of $G$'s
two terms — not a hand-coded switch — is what turns over between the panels.
Rendered deterministically by
`scripts/generate_efe_figure.py` over the tested core in
`src/expected_free_energy.py`.](../figures/expected_free_energy.png){#fig:efe width=92%}



```{=latex}
\newpage
```


# The Markov Blanket {#sec:markov-blanket}

Everything so far assumed a clean split between a system and its world — a
belief $q(s)$ about *hidden* states, sensations $o$ that are not those states,
actions that reach *out*. That split is not a modeling convenience; it is a
structural claim, and it has a name: the **Markov blanket**. This section shows
what the blanket actually asserts, using the one case where it is exactly
computable — a jointly Gaussian world. The core is `src/markov_blanket.py`.

Partition the variables of a system-plus-environment into four roles:
*external* states $\eta$ (the world), *internal* states $\mu$ (the system's own
states, which parameterize its beliefs), and the *blanket* that lies between
them — *sensory* states $s$ (world $\to$ system) and *active* states $a$ (system
$\to$ world). The blanket's defining property is a **conditional independence**:

$$
p(\eta, \mu \mid s, a) \;=\; p(\eta \mid s, a)\; p(\mu \mid s, a).
$$

Internal and external states are *not* independent — they are statistically
coupled, that is the entire point of a mind modeling a world. But that coupling
is **screened by** the blanket. Fix the blanket, and they become conditionally
independent: nothing about $\eta$ tells you anything more about $\mu$ once you
know $s$ and $a$. (This is a statement about statistical dependence in the joint
distribution, not about causal direction or intervention — a causal reading
would need a dynamical or interventional model on top of this one.) That
conditional independence is what licenses treating internal states as
*inferring* external ones they never share a variable with: conditioned on the
blanket, the internal states' sufficient statistics for the external world are
exactly their beliefs given the blanket.

[@fig:blanket] makes both halves of the claim visible on a Gaussian built so
that the $\eta$–$\mu$ block of its **precision matrix** (the inverse covariance)
is exactly zero. Panel (a) is the ordinary correlation matrix: $\eta$ and $\mu$
are plainly correlated ($\mathrm{corr} = 0.19$): they are statistically coupled
through the blanket. Panel (b) is the precision matrix, and the payoff is
the highlighted cell: $\Pi_{\eta\mu} = 0$. In a Gaussian a zero precision entry
is *exactly* a conditional independence given the remaining variables — so the
zero at $(\eta,\mu)$ says $\eta \perp \mu \mid \{s,a\}$. Conditioning on the
blanket collapses the partial correlation between internal and external states
to zero (the tests confirm it vanishes to $10^{-10}$ via the Schur complement),
even though conditioning on only *part* of the blanket does not — both the
sensory and active states are needed to close the channel.

That is the geometry underneath the whole overview. A free-energy-minimizing
system is one whose internal states, across its blanket, come to encode a
posterior over the external states it is coupled to but cannot see. Perception
([@sec:generative-model]) updates that encoding; action
([@sec:expected-free-energy]) acts through the blanket to keep the world within
the range the encoding expects; and the flow and trajectories
([@sec:extended;@sec:worked-regimes]) are what that coupling looks like as
dynamics. The blanket is the boundary that makes "a thing that models its world"
a well-posed idea rather than a metaphor.

![**Marginal dependence, conditional independence.** A jointly Gaussian world
over external $\eta$, sensory $s$, active $a$, internal $\mu$, built with a zero
$\eta$–$\mu$ precision block. **(a) Marginal correlation:** $\eta$ and $\mu$ are
correlated ($0.19$, highlighted) — they are statistically coupled through the
blanket. **(b) Precision (inverse covariance):** the $\eta$–$\mu$ entry is
exactly $0$, which in a Gaussian *is* conditional independence given the other
variables — so $\eta \perp \mu \mid \{s,a\}$ and the partial correlation given
the blanket is $0$. The sensory and active states screen the internal states
from the external world. Rendered deterministically by
`scripts/generate_markov_blanket_figure.py` over the tested core in
`src/markov_blanket.py`.](../figures/markov_blanket.png){#fig:blanket width=94%}



```{=latex}
\newpage
```


# The Steady State, Quantified {#sec:steady-state}

[@sec:worked-regimes] was deliberately careful about one thing. The
deterministic spiral it drew is the *drift* of a non-equilibrium steady state,
not the state itself — a single trajectory relaxes to the mode and stops, while
a genuine steady state is a property of a whole *stochastic* ensemble, with a
current that never dies. This closing section supplies that missing object,
still analytically and with no randomness, in `src/steady_state.py`. It is where
"far from equilibrium" stops being a picture and becomes two numbers: a
**probability current** and an **entropy-production rate**.

Give the Bayesian-mechanics flow a matched noise term — the Ornstein–Uhlenbeck
diffusion $dx = -Mx\,dt + \sqrt{2D}\,dW$ with drift $M = (\Gamma - Q)P$ and, by
the fluctuation–dissipation relation, diffusion $D = \Gamma$. Three exact
results follow, each checked against a closed form in the tests.

First, the ensemble settles into a **stationary density**. Its covariance solves
the Lyapunov equation $M\Sigma + \Sigma M^{\mathsf T} = 2D$, and with $D=\Gamma$
the solution is exactly $\Sigma = P^{-1}$ — the system's own belief covariance.
The distribution the noisy system lives in is precisely $\rho \propto e^{-F}$:
free-energy minimization and the steady state are the same fixed point.

Second, that density carries a **probability current**
$j(x) = b(x)\rho - D\nabla\rho = (QPx)\,\rho(x)$. When $Q=0$ the current is zero
*everywhere* (detailed balance — the density just sits), and when $Q\neq0$ it is
a divergence-free field that circulates around the mode without end. This is the
sustained current the deterministic trajectory could only gesture at; here it is
an explicit vector field, orthogonal to $\nabla F$ (the tests confirm both
$\nabla\!\cdot j = 0$ and $j\perp\nabla F$ to machine precision).

Third, the current has a price. The **entropy-production rate**
$\sigma = \operatorname{tr}\!\big(D^{-1} Q P\,\Sigma\,P^{\mathsf T}Q^{\mathsf T}\big)$
measures the system's irreversibility, and for the isotropic model it is exactly
$\sigma = 2\,\omega^2\,\Pi/\gamma$ (with $\Pi$ the precision). It is strictly
positive out of equilibrium and **exactly zero if and only if $\omega=0$**.
Entropy production is the thermodynamic cost of staying far from equilibrium — of
keeping the current running — and it is the sharpest available statement of the
difference between the two regimes: not the shape of a path, but a
non-negative number that vanishes precisely at detailed balance. (Two
conventions, stated plainly: the choice $D=\Gamma$ is the fluctuation–
dissipation relation with $k_{\mathrm B}T\equiv1$ absorbed, so $\sigma$ is a pure
rate — the dimensional entropy-production rate is $k_{\mathrm B}\sigma$ and the
dissipated power is $k_{\mathrm B}T\sigma$; and crucially the nonequilibrium
character is certified by the *current* and $\sigma$, **not** by the density —
the Gaussian $\rho$ on its own looks equilibrium-like, so it is the circulation,
not the shape of the steady state, that marks the regime as nonequilibrium.)

[@fig:steady] shows both panels over the same stationary density. At equilibrium
(a) the current field is identically zero and $\sigma=0$: nothing circulates and
nothing is dissipated. In the NESS (b) the current curls steadily around the
mode and $\sigma>0$: the same density, now maintained by a perpetual,
entropy-producing flow. Read against the whole overview, this is the final turn
of the one thesis — and the point at which the mathematics reconnects to the
motivation. A system that minimizes free energy need not merely come to rest at
its expected states; a *nonequilibrium* steady state holds those states while
circulating through them, at a strictly positive entropy cost. The overview
opened by claiming that living systems occupy exactly this regime; the model
here does not prove that of any organism, but it makes the regime itself — the
sustained current and its irreversible price — precise and measurable.

![**Probability current and entropy production.** Both panels place the same
stationary Gaussian density (grey contours) under the Bayesian-mechanics
diffusion. **(a) Equilibrium** ($Q=0$): the steady-state probability current is
zero everywhere and the entropy-production rate is $\sigma=0$ — detailed balance.
**(b) NESS** ($Q\neq0$): a divergence-free current $j=(QPx)\rho$ circulates
around the mode (orange arrows), sustained at an entropy-production rate
$\sigma=2\omega^2\Pi/\gamma>0$ (here $\sigma\approx11.5$ nats/time). The current
vanishes at the mode (where $QPx=0$) and in the tails (where $\rho\to0$), peaking
on an annulus between. Rendered deterministically by
`scripts/generate_steady_state_figure.py` over the tested core in
`src/steady_state.py`.](../figures/steady_state_current.png){#fig:steady width=94%}



```{=latex}
\newpage
```


# Formal Verification {#sec:formal}

Every preceding section pairs a claim with a runnable, tested demonstration —
*show, not tell* at the level of numerics. This section takes the discipline one
level deeper: the load-bearing *mathematical* claims are not only computed and
tested, they are **machine-checked**. A small self-contained Lean 4 development
in `formal/` proves them with no `sorry`. The development has two surfaces: the
manuscript-canonical ℝ theorems are re-exported, with exposition, from the
companion **fep_lean** library (mathlib-backed), while a legacy ℤ surface proves
the same structural statements from Lean's core axioms alone. Where `src/`
guarantees the numbers are right, `formal/` guarantees the theorems are.

The formalization mirrors the two halves of the overview.
`ActiveInferenceFormal.Geometry` and `ActiveInferenceFormal.GeometryZ` carry the
facts behind the flow and the steady state (ℝ and ℤ respectively);
`ActiveInferenceFormal.Information` and `ActiveInferenceFormal.InformationZ`
carry the facts behind perception, and `Bridge.lean` maps the three evidence
surfaces — Python, formal ℝ, formal ℤ — onto one another. The headline results:

| Lean theorem | What it establishes | Section |
|---|---|---|
| `solenoidal_orthogonal` | $(Q\,g)\cdot g = 0$: the antisymmetric current does no work against $\nabla F$ | §1, §3 |
| `flow_work_eq_dissipation` | $f\cdot g = -\gamma\lVert g\rVert^2$: only dissipation changes $F$; the circulation is free | §3 |
| `detailed_balance_iff` | the solenoidal current vanishes $\iff \omega=0$ | §3 |
| `entropyProduction_nonneg` | $\gamma\sigma = 2\omega^2\Pi \ge 0$ | §6 |
| `entropyProduction_zero_iff` | entropy production is zero $\iff \omega=0$ | §6 |
| `relEntropy_nonneg` | Gibbs' inequality: relative entropy $\ge 0$ | §2 |
| `freeEnergy_eq_surprise_add_relEntropy` | $F = \text{surprise} + D(q\Vert\text{posterior})$ | §2 |
| `freeEnergy_ge_surprise` | the (total-scaled) bound $\text{total}\cdot\text{surprise} \le F$ | §2 |
| `freeEnergy_ge_surprise_of_model` | the bound for a genuine model $j_i = r_i E$ | §2 |
| `freeEnergy_eq_surprise_at_posterior` | the bound is attained at the posterior | §2 |

Two design choices keep the development honest and light. First, it works over
the integers $\mathbb{Z}$ rather than the reals: the results above are polynomial
identities and sign facts whose truth does not depend on the real-number
completion, so $\mathbb{Z}$ suffices and the project needs no analysis library
(it builds in about a second and depends on *nothing* but Lean core). The
floating-point instances live on the Python side; the two layers verify the same
statements at different resolutions.

Second — and this is the crux for the free-energy bound — the logarithm's
analytic properties are made **explicit hypotheses** rather than hidden inside a
library. Gibbs' inequality rests on exactly two facts about $\ln$: that it turns
products into sums ($\ln(ab)=\ln a+\ln b$), and the tangent-line bound
$\ln x \le x-1$. But there is a subtlety that a green build alone will not catch,
and the development takes pains to get it right. Stating those two properties as
*universal* hypotheses over $\mathbb{Z}$ — "for **all** positive integers" —
would be a trap: no integer function can satisfy the cleared tangent bound
$b-a \le b(L b - L a)$ at both orientations of the pair $\{2,3\}$ (integer
rounding destroys the real-line tangency), so such an antecedent has no model and
every theorem beneath it would be **vacuously** true. A proof assistant will
happily check a vacuous theorem: no `sorry`, clean axioms, and no content.

The development therefore takes the log's properties only at the **exact points
each proof consumes** — the tangent bound and additivity at the specific
belief/reference/evidence values — which the real $\ln$ satisfies and which are
jointly satisfiable over $\mathbb{Z}$. To *prove* they are satisfiable rather than
merely assert it, `Sanity.lean` carries a matched pair of controls: a negative
one (`relEntropy_can_be_negative` — a concrete function for which relative entropy
is $-20$, so the tangent hypothesis is genuinely necessary) and a **positive
control** on a *genuine generative model*: `okL` is the 2-adic valuation (an
actually log-additive function), with belief $(4,2)$, posterior $(2,4)$, evidence
$2$, and joint $(4,8) = (r_0 E, r_1 E)$ — real products, not hand-picked values.
There every hypothesis provably holds and the bound fires with a *non-trivial*
gap, $-6 \le -4$, equal to the relative entropy $2$. Necessity and satisfiability
together certify the theorems are faithful, not vacuous.

The guarantee is auditable. The `Audit` module runs `#print axioms` on each
headline theorem *and each witness*. Every ℤ theorem reports
`depends on axioms: [propext, Quot.sound]` — Lean's standard trusted core — and
the ℝ theorems report the standard mathlib footprint; no theorem ever depends on
`sorryAx`. The project's test suite runs the real `lake build`, inspects
that output, and checks the non-vacuity witnesses are present, so the "it is
proved, and it is not vacuous" claim is itself tested rather than asserted. In the
spirit of the whole overview: the strongest thing you can say about a
mathematical claim is not that it looks right, or even that it computes right, but
that a machine has checked the proof — and here, that you can re-check the
checker, and that what it checked has content.



```{=latex}
\newpage
```


# Planning: Policies as Action Sequences {#sec:planning}

[@sec:expected-free-energy] scored *one* action: what is the best thing to do
right now? But the value of an action often lies in what it makes possible
*next*. This section extends the same currency to **policies** — short
sequences of actions — and shows that *planning* is not a new rule bolted onto
Active Inference: it is expected free energy minimized over sequences. The
core is `src/policy_planning.py`; every value below is checked against a
hand-worked reference, and [@fig:planning] is generated from the same live
computation.

The agent of [@sec:expected-free-energy] returns, with the same two actions —
a **cue** that reveals the hidden context and a **bet** whose outcome model is
state-independent — and the same **sharp** preferences under which the
*one-step* rule chose to exploit. Now it plans over a horizon of
$T = 2$ steps. A policy $\pi = (a_1, \dots, a_T)$ induces a
distribution over outcome sequences; along each branch the belief evolves by
exact Bayes rule, and the plan's expected free energy is

$$
G(\pi) \;=\; -\underbrace{\mathbb{E}_{q(o_{1:T}\mid\pi)}\big[\ln p_{\text{pref}}(o_T)\big]}_{\text{pragmatic (terminal)}}
\;-\; \underbrace{I(s;\, o_{1:T} \mid \pi)}_{\text{epistemic (cumulative)}}.
$$

Two changes from the one-step $G(a)$ are load-bearing. The **pragmatic term
is terminal**: payoffs are collected on the *final* outcome only, so an
informative first action earns nothing immediately — its entire value is the
sharper belief the final action is then chosen under. And the **epistemic term
is cumulative**: the expected resolution of uncertainty over the whole
sequence, which by the chain rule of relative entropy is the mutual
information $I(s; o_{1:T} \mid \pi)$ between the context and the *entire*
outcome sequence (a fact the tests verify against an independently computed
mutual information).

The subtlety that makes this genuinely planning rather than bookkeeping is
*when* the expectation is taken. Each branch is followed to its end, the
final action evaluated under that branch's posterior, and only then averaged
over branches. The nonlinearity of Bayes rule is preserved inside the
expectation — which is exactly why information has value. Averaging *first*
(the posterior-mixture shortcut) would collapse every branch's posterior back
to the prior and erase the value of looking before leaping.

![**Planning as expected-free-energy minimization.** The same agent and
preferences as [@sec:expected-free-energy] now plan over two-step policies. All
four plans are scored exactly (branch enumeration, no sampling): bars are
$G(\pi)$, annotated with pragmatic/epistemic splits. **Cue-then-bet wins**
($G = 0.07$): the first action collects epistemic
value ($+0.37$ nats), and the terminal bet is
then placed under the sharpened belief. Betting first
($G = 0.43$) pays the same either way and forgoes the
information — under these sharp preferences the *one-step* optimum is not the
*plan* optimum. Exploration is deferred exploitation. Rendered
deterministically by `scripts/generate_policy_planning_figure.py` over the
tested core in `src/policy_planning.py`.](../figures/policy_planning.png){#fig:planning width=94%}

[@fig:planning] evaluates all four two-step policies. The winner is **cue
then bet**: look, resolve the uncertainty (epistemic value
$+0.37$ nats), and *then* place the wager the
sharpened belief licenses — $G = 0.07$. Betting
first — the one-step optimum under these same preferences — costs
$G = 0.43$: the terminal bet pays the same either
way, but it forgoes the information the plan could have collected first. The
explore/exploit balance of [@sec:expected-free-energy] is revealed as a
*temporal* structure: exploration is what exploitation looks like when it is
allowed to plan. One currency, one minimization, now over sequences — the
agent defers gratification because $\arg\min_\pi G(\pi)$ told it to.

Branch enumeration is exact — every one of $O^T$ outcome sequences is summed,
no sampling, no RNG — so the demonstration is deterministic and reproducible.
The horizon is deliberately short; tree search over longer horizons, and
approximate schemes for intractable ones, are the natural next expansions, and
are recorded as such in the roadmap.



```{=latex}
\newpage
```


# References {#sec:references}

Bibliography lives in [`docs/manuscript/references.bib`](references.bib) and is read by Pandoc during PDF render. The build pipeline invokes Pandoc with `--natbib`, so every `[@key]` citation in the manuscript is rewritten to the appropriate `\cite{}`/`\citep{}`/`\citet{}` LaTeX command and resolved against the bib file.

To validate that `references.bib` is syntactically clean and contains the required fields per entry type:

```bash
uv run python -m infrastructure.reference.citation.cli validate \
    projects/working/ActiveInferenceSynthetic/docs/manuscript/references.bib --strict
```
