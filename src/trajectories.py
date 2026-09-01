"""Worked equilibrium vs. non-equilibrium trajectories.

:mod:`free_energy_flow` defines the *instantaneous* Bayesian-mechanics flow
``f = (Q − Γ)∇F`` as a velocity field. This module integrates that field into
*trajectories* — the concrete paths a system traces — so the equilibrium↔NESS
distinction becomes something you watch happen rather than read about.

Two regimes over the *same* isotropic Gaussian free-energy landscape:

* **Equilibrium** (``omega = 0``): pure gradient descent. A trajectory falls
  straight to the mode and comes to rest. Free energy decreases monotonically;
  there is no net rotation — the flow obeys detailed balance.
* **Non-equilibrium steady state** (``omega ≠ 0``): the same descent plus a
  solenoidal current. Free energy *still* decreases monotonically, yet the path
  spirals — because the conservative ``Q``-term circulates probability mass
  along the level sets of ``F`` without ever changing it. That persistent
  circulation is the signature of living systems.

For this isotropic-Gaussian flow the angular velocity is analytically
*constant*, ``dθ/dt = −ω · precision`` radians per unit time — independent of
radius, and the same for every initial condition *off the origin* (the origin
is the fixed point, where the angle is undefined). So the *total* winding over
a horizon ``T`` is exactly ``−ω · precision · T`` radians (window-dependent),
while the intrinsic, IC-free witness of broken detailed balance is the **rate**:
``−ω · precision`` rad/time, or ``−ω · precision / (2π)`` turns/time, which is
exactly zero at equilibrium. A deterministic winding is the mechanistic
*origin* of the steady-state probability current, not a direct measurement of
it — the current proper is a property of the stochastic stationary density
``ρ ∝ e^{−F}`` whose deterministic drift this flow is. Nonzero winding
witnesses the solenoidal ``Q ≠ 0`` that makes that stationary state a
non-equilibrium (detailed-balance-breaking) one.

Integration is a fixed-step **RK4** scheme written out explicitly: no SciPy, no
adaptive stepping, no RNG. It is validated in the tests against the closed-form
solution of the linear ODE it reduces to at equilibrium — with ``Γ = γ·I`` and
``∇F = precision · x`` the descent is ``ẋ = −γ · precision · x``, so
``x(t) = x₀ e^{−γ · precision · t}`` (which is ``x₀ e^{−γ t}`` at unit
precision). Monotone free-energy descent along a trajectory is a property of
the *continuous* flow; RK4 reproduces it at the small step sizes used here, but
(like any explicit scheme) an overly large ``dt`` can overshoot — the
demonstrations use ``dt`` well inside the stable range.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .free_energy_flow import free_energy
from .ou_model import IsotropicOU

__all__ = [
    "free_energy_along",
    "integrate_trajectory",
    "net_rotation",
]


def integrate_trajectory(
    start: NDArray[np.float64] | tuple[float, float],
    *,
    precision: float = 1.0,
    gamma: float = 1.0,
    omega: float = 0.0,
    dt: float = 0.01,
    steps: int = 2000,
) -> NDArray[np.float64]:
    """Integrate the Bayesian-mechanics flow with fixed-step RK4.

    Args:
        start: Initial ``(x, y)`` position.
        precision: Belief precision of the Gaussian free energy (``> 0``).
        gamma: Dissipative (descent) strength (``>= 0``).
        omega: Solenoidal (rotational) strength. ``0`` gives the equilibrium
            regime; nonzero gives a non-equilibrium steady state.
        dt: Positive fixed time step.
        steps: Positive number of integration steps.

    Returns:
        An ``(steps + 1, 2)`` array of states; row 0 is ``start``.

    Raises:
        ValueError: If ``dt <= 0``, ``steps < 1``, or ``start`` is not a
            2-vector. (``precision``/``gamma`` are validated by
            :class:`~src.ou_model.IsotropicOU`.)
    """
    if dt <= 0.0:
        raise ValueError(f"dt must be > 0, got {dt}")
    if steps < 1:
        raise ValueError(f"steps must be >= 1, got {steps}")
    state = np.asarray(start, dtype=np.float64)
    if state.shape != (2,):
        raise ValueError(f"start must be a 2-vector (x, y), got shape {state.shape}")

    model = IsotropicOU(precision=precision, gamma=gamma, omega=omega)
    path = np.empty((steps + 1, 2), dtype=np.float64)
    path[0] = state

    for i in range(steps):
        s = path[i]

        def f(point: NDArray[np.float64]) -> NDArray[np.float64]:
            return model.velocity(point)

        k1 = f(s)
        k2 = f(s + 0.5 * dt * k1)
        k3 = f(s + 0.5 * dt * k2)
        k4 = f(s + dt * k3)
        path[i + 1] = s + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    return path


def free_energy_along(
    path: NDArray[np.float64],
    precision: float = 1.0,
) -> NDArray[np.float64]:
    """Free energy evaluated at every point of a trajectory.

    Args:
        path: An ``(N, 2)`` trajectory as returned by
            :func:`integrate_trajectory`.
        precision: Belief precision of the Gaussian free energy.

    Returns:
        A length-``N`` array ``F(x_i, y_i)`` along the path. For both regimes
        this sequence is non-increasing (descent is preserved even when the
        NESS current circulates).
    """
    arr = np.asarray(path, dtype=np.float64)
    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValueError(f"path must be (N, 2), got shape {arr.shape}")
    return free_energy(arr[:, 0], arr[:, 1], precision=precision)


def net_rotation(path: NDArray[np.float64]) -> float:
    """Total signed angle (radians) swept about the origin along a trajectory.

    Computed by summing the exterior angle between successive position vectors
    via ``atan2`` cross/dot, so it accumulates past ``±π`` rather than wrapping.
    Near-zero for the equilibrium regime (a straight fall to the mode); large in
    magnitude for a NESS spiral, which is exactly the persistent probability
    current made quantitative.

    Args:
        path: An ``(N, 2)`` trajectory.

    Returns:
        The accumulated signed angle in radians (``> 0`` counter-clockwise).
    """
    arr = np.asarray(path, dtype=np.float64)
    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValueError(f"path must be (N, 2), got shape {arr.shape}")
    total = 0.0
    for i in range(arr.shape[0] - 1):
        x0, y0 = arr[i]
        x1, y1 = arr[i + 1]
        cross = x0 * y1 - y0 * x1
        dot = x0 * x1 + y0 * y1
        total += float(np.arctan2(cross, dot))
    return total
