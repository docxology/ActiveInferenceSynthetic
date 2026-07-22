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
`src/steady_state.py`.](../output/figures/steady_state_current.png){#fig:steady width=94%}
