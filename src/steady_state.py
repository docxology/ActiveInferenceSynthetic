r"""The non-equilibrium steady state, quantified — current and entropy production.

:mod:`trajectories` was careful to say that a *deterministic* spiral is only the
**drift** of a non-equilibrium steady state, not the state itself, and that the
probability current proper is a property of a *stochastic* stationary density.
This module supplies exactly that missing object — analytically, with no RNG —
closing the gap the trajectory demonstration honestly left open.

Take the linear (Ornstein–Uhlenbeck) diffusion whose drift is the
Bayesian-mechanics flow and whose noise satisfies the fluctuation–dissipation
relation:

    dx = -M x dt + \sqrt{2D}\, dW,   M = (\Gamma - Q)\,P,   D = \Gamma,

for an isotropic Gaussian free energy ``F = ½ x^T P x`` with ``P = precision·I``,
symmetric dissipation ``\Gamma = \gamma·I`` and antisymmetric solenoidal
``Q = \omega·[[0,1],[-1,0]]``. Three exact facts, each verified in the tests
against a closed form:

1. **Stationary density.** The steady-state covariance ``\Sigma`` solves the
   Lyapunov equation ``M\Sigma + \Sigma M^T = 2D``, and with ``D = \Gamma`` it
   is exactly ``\Sigma = P^{-1}`` — the system's stationary belief covariance.
   So the density the noise settles into is precisely ``\rho \propto e^{-F}``.

2. **Probability current.** The steady-state current is
   ``j(x) = b(x)\rho - D\nabla\rho = (Q P x)\,\rho(x)``. It is **zero everywhere
   when ``Q = 0``** (detailed balance / equilibrium) and a divergence-free
   rotational field when ``Q \neq 0`` (a genuine, sustained probability
   current). This is the current the deterministic spiral only *hinted* at.

3. **Entropy production.** The steady-state entropy-production rate
   ``\sigma = \mathrm{tr}(D^{-1} Q P\,\Sigma\,P^T Q^T)`` measures irreversibility.
   For the isotropic model it is exactly
   ``\sigma = 2\,\omega^2\,\mathrm{precision}/\gamma``: strictly positive out of
   equilibrium and **exactly zero iff ``\omega = 0``**. Entropy production is the
   thermodynamic cost of maintaining the current — the quantitative signature of
   a nonequilibrium (rather than an equilibrium) steady state.

Two conventions, stated so nothing is hidden:

* **Units (``k_B T \equiv 1``).** ``D = \Gamma`` is the Einstein / fluctuation–
  dissipation relation with Boltzmann's constant and temperature absorbed, so
  ``\sigma`` here is a pure *rate* (dimensionally ``1/\mathrm{time}``). There is
  no missing factor — only this implicit one: the dimensional entropy-production
  rate is ``k_B\,\sigma``, and the dissipated *power* (heat rate) is
  ``k_B T\,\sigma``.
* **What certifies the NESS.** The stationary density ``\rho \propto e^{-F}`` is
  Gaussian and, on its own, looks equilibrium-like. The non-equilibrium
  character is certified **not** by the density but by the *current* and
  ``\sigma``: a nonzero divergence-free ``j`` and ``\sigma > 0`` are equivalent
  to broken detailed balance (``\omega \neq 0``).

Everything is closed-form and deterministic — no RNG, no fitting.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .ou_model import IsotropicOU

__all__ = [
    "current_circulation",
    "drift_matrix",
    "entropy_production_rate",
    "probability_current",
    "stationary_covariance",
]


def _model(
    precision: float = 1.0, gamma: float = 1.0, omega: float = 0.0
) -> IsotropicOU:
    model = IsotropicOU(precision=precision, gamma=gamma, omega=omega)
    model.require_positive_gamma()
    return model


def drift_matrix(
    precision: float = 1.0, gamma: float = 1.0, omega: float = 0.0
) -> NDArray[np.float64]:
    """Drift matrix ``M = (Γ − Q) P`` of the linear diffusion ``dx = −M x dt + …``."""
    return _model(precision, gamma, omega).drift_M()


def stationary_covariance(
    precision: float = 1.0, gamma: float = 1.0, omega: float = 0.0
) -> NDArray[np.float64]:
    """Steady-state covariance ``Σ`` of the isotropic matched-noise OU.

    For this class ``D = Γ`` the Lyapunov equation is satisfied identically by
    the closed form ``Σ = P^{-1}``. The implementation returns that form and
    checks the residual; tests still verify the equation independently.

    Args:
        precision: Belief precision (``> 0``).
        gamma: Dissipative strength (``> 0``); also the diffusion ``D = γI``.
        omega: Solenoidal strength.

    Returns:
        The ``2 × 2`` symmetric positive-definite stationary covariance.
    """
    model = _model(precision, gamma, omega)
    m = model.drift_M()
    d = model.Gamma
    sigma = np.linalg.inv(model.P)
    sigma = 0.5 * (sigma + sigma.T)
    residual = m @ sigma + sigma @ m.T - 2.0 * d
    scale = max(1.0, float(np.abs(2.0 * d).max()))
    resid_max = float(np.abs(residual).max())
    if (
        not np.all(np.isfinite(sigma))
        or not np.isfinite(resid_max)
        or resid_max > 1e-6 * scale
    ):
        raise ValueError(
            "Lyapunov identity failed for these parameters "
            f"(|omega|/gamma too large): max residual {resid_max}"
        )
    return sigma


def probability_current(
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    precision: float = 1.0,
    gamma: float = 1.0,
    omega: float = 0.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Steady-state probability current ``j(x) = (Q P x) ρ(x)``.

    Zero everywhere at equilibrium (``omega = 0``); a divergence-free rotational
    field out of equilibrium. ``ρ`` is the stationary Gaussian ``N(0, P^{-1})``.

    Args:
        x: X coordinates (broadcastable array).
        y: Y coordinates.
        precision: Belief precision (``> 0``).
        gamma: Dissipative strength (``> 0``).
        omega: Solenoidal strength.

    Returns:
        A ``(j_x, j_y)`` tuple of the current-density components at each point.
    """
    model = _model(precision, gamma, omega)
    xa = np.asarray(x, dtype=np.float64)
    ya = np.asarray(y, dtype=np.float64)
    qp = model.Q @ model.P
    vx = qp[0, 0] * xa + qp[0, 1] * ya
    vy = qp[1, 0] * xa + qp[1, 1] * ya
    norm = precision / (2.0 * np.pi)
    rho = norm * np.exp(-0.5 * precision * (xa**2 + ya**2))
    return vx * rho, vy * rho


def entropy_production_rate(
    precision: float = 1.0, gamma: float = 1.0, omega: float = 0.0
) -> float:
    """Steady-state entropy-production rate ``σ = tr(D⁻¹ Q P Σ Pᵀ Qᵀ)`` (nats/time).

    A measure of irreversibility: strictly positive out of equilibrium, exactly
    zero iff ``omega = 0`` (detailed balance). For the isotropic model it equals
    the closed form ``2 ω² · precision / γ``.

    Args:
        precision: Belief precision (``> 0``).
        gamma: Dissipative strength (``> 0``).
        omega: Solenoidal strength.

    Returns:
        The entropy-production rate ``σ ≥ 0``.
    """
    model = _model(precision, gamma, omega)
    sigma = stationary_covariance(precision, gamma, omega)
    d_inv = np.linalg.inv(model.Gamma)
    value = float(np.trace(d_inv @ model.Q @ model.P @ sigma @ model.P.T @ model.Q.T))
    return max(0.0, value)


def current_circulation(
    precision: float = 1.0, gamma: float = 1.0, omega: float = 0.0
) -> float:
    """Mean angular momentum of the probability current, ``⟨x × v⟩`` under ``ρ``.

    A signed scalar summarizing the sustained circulation: zero at equilibrium,
    sign following ``omega``. For the isotropic model it equals ``−2 ω`` (the
    factor absorbs the stationary variance ``tr(Σ) = 2/precision``).

    Args:
        precision: Belief precision (``> 0``).
        gamma: Dissipative strength (``> 0``).
        omega: Solenoidal strength.

    Returns:
        The mean current angular momentum (radians·variance per unit time).
    """
    model = _model(precision, gamma, omega)
    sigma = stationary_covariance(precision, gamma, omega)
    rot = np.array([[0.0, 1.0], [-1.0, 0.0]])
    return float(np.trace(rot @ model.Q @ model.P @ sigma))
