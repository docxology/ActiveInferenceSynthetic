# The Steady State, Quantified {#sec:steady-state}

[@sec:worked-regimes] was deliberately careful about one thing. The
deterministic spiral it drew is the *drift* of a non-equilibrium steady state,
not the state itself — a single trajectory relaxes to the mode and stops, while
a genuine steady state is a property of a whole *stochastic* ensemble, with a
current that never dies. This closing section supplies that missing object,
still analytically and with no randomness, in `src/steady_state.py`. It is where
non-equilibrium is characterized by two model quantities: a
**probability current** and an **entropy-production rate**.

Give the Bayesian-mechanics flow a matched noise term — the Ornstein–Uhlenbeck
diffusion $dx = -Mx\,dt + \sqrt{2D}\,dW$ with drift $M = (\Gamma - Q)P$ and, by
the fluctuation–dissipation relation, diffusion $D = \Gamma$. Three exact
results follow, each checked against a closed form in the tests.

First, the ensemble settles into a **stationary density**. Its covariance solves
the Lyapunov equation $M\Sigma + \Sigma M^{\mathsf T} = 2D$, and with $D=\Gamma$
the solution is exactly $\Sigma = P^{-1}$, the stationary ensemble covariance.
The density is $\rho \propto e^{-\Phi}$, where $\Phi$ is the Gaussian potential
called `free_energy` by the code. A stationary ensemble has nonzero variance;
it is not the point reached by a deterministic path or automatically an
agent's recognition distribution.

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
Under even-coordinate time reversal this rate measures path irreversibility;
with an isothermal physical model and local thermodynamic assumptions it can
represent the cost of maintaining the current. It distinguishes the
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
(a) the current field is identically zero and $\sigma=0$: there is no net
stationary circulation or entropy production, although stochastic fluctuations
and energy exchange remain. In the NESS (b) the current curls steadily around the
mode and $\sigma>0$: the same density, now maintained by a perpetual,
entropy-producing flow. Read against the whole overview, this is the final turn
of the one thesis — and the point at which the mathematics reconnects to the
motivation. A system that minimizes free energy need not merely come to rest at
its expected states; a *nonequilibrium* steady state holds those states while
circulating through them, at a strictly positive entropy cost. The model makes the sustained current and its irreversible cost precise
and measurable under the stated diffusion assumptions. This motivates connections
to living and synthetic systems without proving biological adequacy or intelligence.

![**Probability current and entropy production.** Both panels place the same
stationary Gaussian density (grey contours) under the Bayesian-mechanics
diffusion. **(a) Equilibrium** ($Q=0$): the steady-state probability current is
zero everywhere and the entropy-production rate is $\sigma=0$ — detailed balance.
**(b) NESS** ($Q\neq0$): a divergence-free current $j=(QPx)\rho$ circulates
around the mode (orange arrows), sustained at an entropy-production rate
$\sigma=2\omega^2\Pi/\gamma>0$ (here $\sigma\approx{{NESS_SIGMA_APPROX}}$ nats/time). The current
vanishes at the mode (where $QPx=0$) and in the tails (where $\rho\to0$), peaking
on an annulus between. Rendered deterministically by
`scripts/generate_steady_state_figure.py` over the tested core in
`src/steady_state.py`.](../output/figures/steady_state_current.png){#fig:steady width=94%}
