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
to better than ${{RK4_MATCH_ATOL}}$.

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
figure's $\approx {{TRAJECTORY_TURNS}}$ turns over the demonstration window $T={{TRAJECTORY_HORIZON}}$ — is not an
intrinsic property of the NESS; it grows with $T$ and would diverge as
$T \to \infty$. The intrinsic, initial-condition-free quantity is the
**rotation rate**. For this isotropic-Gaussian flow the angular velocity is
analytically constant, $\dot\theta = -\omega\,\Pi$ radians per unit time (with
$\Pi$ the precision), so the rate is $\approx {{TRAJECTORY_RATE}}$ turns per unit time
($-\omega\,\Pi/(2\pi)$ at $\omega={{NESS_OMEGA}}$, $\Pi={{PRECISION}}$) for *any* starting point off
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
solenoidal term spirals inward at a constant rate $\approx {{TRAJECTORY_RATE}}$ turns/time
($\approx {{TRAJECTORY_TURNS}}$ turns over the window $T={{TRAJECTORY_HORIZON}}$) while free energy still decreases
monotonically. The nonzero rotation rate witnesses the broken detailed balance
that generates the steady-state probability current — the marker distinguishing
far-from-equilibrium life from equilibrium rest. Rendered deterministically by
`scripts/generate_trajectory_figure.py` over the tested cores in
`src/trajectories.py` and `src/free_energy_flow.py`.](../output/figures/worked_trajectories.png){#fig:trajectories width=94%}
