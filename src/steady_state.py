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

__all__ = [
    "drift_matrix",
    "stationary_covariance",
    "probability_current",
    "entropy_production_rate",
    "current_circulation",
]

_ROT = np.array([[0.0, 1.0], [-1.0, 0.0]])  # antisymmetric generator J


def _matrices(
    precision: float, gamma: float, omega: float
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Return ``(P, Gamma, Q)`` for the isotropic 2-D model; validate inputs."""
    if not (np.isfinite(precision) and np.isfinite(gamma) and np.isfinite(omega)):
        raise ValueError(
            f"precision, gamma, omega must be finite; got {precision}, {gamma}, {omega}"
        )
    if precision <= 0.0:
        raise ValueError(f"precision must be > 0, got {precision}")
    if gamma <= 0.0:
        raise ValueError(f"gamma must be > 0, got {gamma}")
    p = precision * np.eye(2)
    g = gamma * np.eye(2)
    q = omega * _ROT
    return p, g, q


def drift_matrix(
    precision: float = 1.0, gamma: float = 1.0, omega: float = 0.0
) -> NDArray[np.float64]:
    """Drift matrix ``M = (Γ − Q) P`` of the linear diffusion ``dx = −M x dt + …``."""
    p, g, q = _matrices(precision, gamma, omega)
    return (g - q) @ p


def stationary_covariance(
    precision: float = 1.0, gamma: float = 1.0, omega: float = 0.0
) -> NDArray[np.float64]:
    """Steady-state covariance ``Σ`` solving the Lyapunov equation ``MΣ + ΣMᵀ = 2D``.

    Solved generally (via the Kronecker vectorization
    ``(I⊗M + M⊗I) vec(Σ) = vec(2D)``) rather than assuming the answer, so the
    tests can confirm it equals the analytic ``P^{-1}`` independently.

    Args:
        precision: Belief precision (``> 0``).
        gamma: Dissipative strength (``> 0``); also the diffusion ``D = γI``.
        omega: Solenoidal strength.

    Returns:
        The ``2 × 2`` symmetric positive-definite stationary covariance.
    """
    p, g, q = _matrices(precision, gamma, omega)
    m = (g - q) @ p
    d = g  # fluctuation–dissipation: diffusion equals dissipation
    eye = np.eye(2)
    lhs = np.kron(eye, m) + np.kron(m, eye)
    sigma = np.linalg.solve(lhs, (2.0 * d).reshape(-1)).reshape(2, 2)
    sigma = 0.5 * (sigma + sigma.T)
    # Guard: the symmetrization can hide a bad solve, so verify the recovered
    # matrix actually satisfies the Lyapunov equation before returning it.
    residual = m @ sigma + sigma @ m.T - 2.0 * d
    scale = max(1.0, float(np.abs(2.0 * d).max()))
    if not np.all(np.isfinite(sigma)) or float(np.abs(residual).max()) > 1e-6 * scale:
        raise ValueError(
            "Lyapunov solve is unreliable for these parameters "
            f"(|omega|/gamma too large): max residual {float(np.abs(residual).max())}"
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
    p, _, q = _matrices(precision, gamma, omega)
    xa = np.asarray(x, dtype=np.float64)
    ya = np.asarray(y, dtype=np.float64)
    qp = q @ p  # velocity operator: v(x) = QP x
    vx = qp[0, 0] * xa + qp[0, 1] * ya
    vy = qp[1, 0] * xa + qp[1, 1] * ya
    # Stationary density rho ∝ exp(-F) = N(0, P^{-1}); F = 0.5*precision*(x^2+y^2).
    norm = precision / (2.0 * np.pi)  # 1/sqrt((2π)^2 det(P^{-1})) = precision/2π
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
    p, g, q = _matrices(precision, gamma, omega)
    sigma = stationary_covariance(precision, gamma, omega)
    d_inv = np.linalg.inv(g)
    value = float(np.trace(d_inv @ q @ p @ sigma @ p.T @ q.T))
    # σ = tr(D⁻¹ (QP) Σ (QP)ᵀ) with D⁻¹ positive-definite and Σ, (QP)Σ(QP)ᵀ
    # positive-semidefinite, so it is provably >= 0. Inputs are validated finite
    # upstream, so the only way `value` is negative here is floating-point
    # roundoff near zero — clamp that to 0.
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
    p, _, q = _matrices(precision, gamma, omega)
    sigma = stationary_covariance(precision, gamma, omega)
    # E_rho[ x × v ] with v = QP x. The z-cross-product x×v = xᵀ R v with
    # R = [[0,1],[-1,0]], so E[xᵀ R QP x] = tr(R QP Σ).
    return float(np.trace(_ROT @ q @ p @ sigma))
