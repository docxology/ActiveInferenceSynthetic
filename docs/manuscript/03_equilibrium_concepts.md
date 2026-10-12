# Equilibrium, Relaxation and Non-Equilibrium Steady States {#sec:equilibrium-concepts}

Three questions organize the dynamical examples: **what distribution is
stationary, which probability currents persist, and what changes under time
reversal?** They distinguish a snapshot of a density, a deterministic drift
path, and a stochastic process. Equilibrium is a property of the process under
specified reversal and boundary conditions, not merely a minimum in a plot.
This treatment follows stationary Bayesian mechanics and stochastic
thermodynamics [@dacosta2021bayesian; @seifert2012stochastic;
@dacosta2023entropy].

## A common density does not imply a common process

Write $\Phi(x)=-\ln\rho_*(x)+\mathrm{constant}$ for the dimensionless stationary
potential. This notation separates a function of physical/model coordinates
from the variational functional $F[q]$ of a recognition distribution. The code
uses `free_energy` for this Gaussian potential; that name does not establish
an identity between the two mathematical objects. For constant positive-definite
diffusion $D$, the Fokker--Planck equation and current are

\begin{equation}
\partial_t\rho_t=-\nabla\!\cdot j_t,
\qquad j_t=b\rho_t-D\nabla\rho_t.
\end{equation}

Stationarity requires $\nabla\!\cdot j_*=0$, not $j_*=0$. In this paper's
overdamped, even-coordinate model, with no boundary flux, detailed balance
means that stationary forward and reversed transitions agree; its current
vanishes. A NESS instead maintains a nonzero divergence-free current. A
nonstationary distribution relaxing toward either regime is a **transient**,
even when its drift has time-independent coefficients.

| Object | Equilibrium stationary process | Non-equilibrium stationary process | Relaxation transient |
| --- | --- | --- | --- |
| Density | Time independent | Time independent | Changes with time |
| Stationary current | Zero in this even-coordinate setting | Nonzero, divergence free | Current need not be divergence free |
| Detailed balance | Holds | Fails for the stated reversal | A stationary criterion cannot be inferred from a transient snapshot |
| A noise-free path | May relax to a fixed point | May also relax to that fixed point | Describes drift only |

For $P=\Pi I$, $\Gamma=\gamma I$ and the antisymmetric $Q$, the two OU regimes
share $\rho_*\propto\exp(-x^{\mathsf T}Px/2)$ because $D=\Gamma$ and
$\gamma,\Pi>0$. Their currents differ by $j_*=QPx\rho_*$. Rotating the drift
does not change this isotropic density. It changes temporal statistics and
forward/reverse path probabilities. The cover graphical abstract therefore
compares **currents over the same contours**, rather than using a different
density as a visual proxy for non-equilibrium.

## Relaxation, circulation and entropy production

Along the deterministic drift, antisymmetry gives
$\dot\Phi=-\nabla\Phi^{\mathsf T}\Gamma\nabla\Phi\le0$.
With stochastic forcing, individual paths fluctuate and need not decrease
$\Phi$ monotonically. At stationarity, fluctuations balance dissipation in the
density while the solenoidal current may remain. Constant $Q,\Gamma$ make this
decomposition particularly transparent; state-dependent coefficients require
additional derivative terms and regularity conditions [@dacosta2023entropy].

For the stated even-coordinate reversal, path irreversibility and the
elliptic stationary current expression agree:

\begin{equation}
\sigma=\lim_{T\to\infty}\frac{1}{T}
D_{\mathrm{KL}}(\mathbb P_{[0,T]}\Vert\mathbb P^{\mathrm R}_{[0,T]})
=\int\frac{j_*^{\mathsf T}D^{-1}j_*}{\rho_*}\,dx.
\end{equation}

Here $\mathbb P^{\mathrm R}$ is the stationary time-reversed path law aligned
to forward coordinates. The OU result is $\sigma=2\omega^2\Pi/\gamma$.
Positive diffusion makes the inverse well defined. Momentum coordinates,
magnetic-field reversal, degenerate diffusion or a different reverse protocol
require a separate analysis; a circulating Hamiltonian phase-space current is
not automatically dissipative. This qualification prevents the word
"solenoidal" from being mistaken for a universal thermodynamic diagnosis
[@dacosta2023entropy; @seifert2012stochastic].

Nonzero $\omega$ establishes non-equilibrium in this model, but does not by
itself establish **far** from equilibrium. The ratio $|\omega|/\gamma$ compares
rotational and dissipative strengths; $\sigma$ depends additionally on
precision and the model time unit. Neither is an empirical measure of a
living system's metabolic cost without a physical calibration. Near-equilibrium
linear response and a strongly driven regime belong to a continuum of parameter
choices, not two different kinds of Gaussian density.

## From stationary physics to inference

Bayesian mechanics relates suitably partitioned stochastic systems to belief
parameterizations under explicit assumptions [@ramstead2023bayesian;
@dacosta2021bayesian]. A stationary density alone supplies neither a generative
model nor an agent's action set. Synthetic therefore adds finite inference,
policy selection and feedback as separate demonstrations. A blanket's
conditional independence, an inference algorithm's VFE descent and an OU
process's stationary current answer different questions. Establishing their
relationship requires a specified parameter map, sensing and control channels,
and hypotheses that survive the transfer; it cannot be inferred from similar
looking gradients [@friston2010fep; @friston2023bayesian].
