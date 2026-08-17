"""Bayesian-mechanics flow on a Gaussian free-energy landscape.

This module provides the small, fully-tested numerical core behind the
overview figure. It encodes the *Helmholtz decomposition* of steady-state
flow used in Bayesian mechanics:

    f(x) = (Q - Gamma) @ grad F(x)

where, for a Gaussian (quadratic) free energy ``F``:

* ``Gamma`` is a symmetric positive-semidefinite *dissipative* operator
  (positive-definite when ``gamma > 0``; ``gamma == 0`` is allowed for
  deterministic flow). The
  ``-Gamma @ grad F`` term is pure gradient descent on free energy — the
  Free Energy Principle's claim that a system *climbs down* its own
  surprise. On its own it drives the system to the mode and stops.
* ``Q`` is an antisymmetric *solenoidal* operator. The ``Q @ grad F`` term
  is conservative: it is everywhere orthogonal to ``grad F`` and so leaves
  free energy unchanged while pushing probability mass *around* the mode.

When ``Q = 0`` the flow obeys detailed balance and the system relaxes to a
classical thermodynamic *equilibrium*. When ``Q != 0`` the same landscape
sustains a persistent probability current — a *non-equilibrium steady
state* (NESS), the regime of living, far-from-equilibrium systems.

The free energy here is isotropic, ``F(x, y) = 0.5 * precision * (x^2 + y^2)``,
i.e. the negative log of a zero-mean Gaussian *kernel*, up to an additive
constant independent of ``x`` (the code keeps only the ``x``-dependent part;
the full 2-D normalization ``ln(precision / 2π)`` is dropped), with scalar
precision.
Everything is analytic and deterministic — no RNG, no fitting.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .ou_model import IsotropicOU

__all__ = [
    "free_energy",
    "grad_free_energy",
    "flow_field",
    "solenoidal_is_conservative",
]


def _model(
    precision: float = 1.0,
    gamma: float = 1.0,
    omega: float = 0.0,
) -> IsotropicOU:
    return IsotropicOU(precision=precision, gamma=gamma, omega=omega)


def free_energy(
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    precision: float = 1.0,
) -> NDArray[np.float64]:
    """Gaussian free energy ``F = 0.5 * precision * (x^2 + y^2)``.

    This is the (negative log) surprise of a zero-mean isotropic Gaussian
    belief: low at the mode, rising quadratically away from it.

    Args:
        x: X coordinates (any broadcastable array).
        y: Y coordinates (any broadcastable array).
        precision: Inverse-variance ``precision > 0`` of the belief.

    Returns:
        Free-energy values, same broadcast shape as ``x`` and ``y``.

    Raises:
        ValueError: If ``precision`` is not strictly positive.
    """
    return _model(precision=precision).free_energy(x, y)


def grad_free_energy(
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    precision: float = 1.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Gradient ``grad F = precision * (x, y)`` of :func:`free_energy`.

    Args:
        x: X coordinates.
        y: Y coordinates.
        precision: Inverse-variance of the belief (``> 0``).

    Returns:
        A ``(dF/dx, dF/dy)`` tuple, each the shape of the broadcast inputs.

    Raises:
        ValueError: If ``precision`` is not strictly positive.
    """
    return _model(precision=precision).grad_free_energy(x, y)


def flow_field(
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    precision: float = 1.0,
    gamma: float = 1.0,
    omega: float = 0.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Bayesian-mechanics flow ``f = (Q - Gamma) @ grad F``.

    With ``Gamma = gamma * I`` (dissipative) and the antisymmetric
    ``Q = omega * [[0, 1], [-1, 0]]`` (solenoidal), the flow components are::

        fx = -gamma * dFdx + omega * dFdy
        fy = -gamma * dFdy - omega * dFdx

    ``omega == 0`` gives pure gradient descent on free energy (an
    equilibrium that obeys detailed balance); ``omega != 0`` adds a
    rotational current that never changes ``F`` (a non-equilibrium steady
    state).

    Args:
        x: X coordinates.
        y: Y coordinates.
        precision: Inverse-variance of the belief (``> 0``).
        gamma: Strength of the symmetric dissipative term (``>= 0``).
        omega: Strength of the antisymmetric solenoidal term. Zero means
            detailed balance / equilibrium.

    Returns:
        A ``(fx, fy)`` velocity-field tuple matching the input shapes.

    Raises:
        ValueError: If ``gamma`` is negative (``precision`` is validated by
            :func:`grad_free_energy`).
    """
    return _model(precision=precision, gamma=gamma, omega=omega).flow_field(x, y)


def solenoidal_is_conservative(
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    precision: float = 1.0,
    omega: float = 1.0,
) -> NDArray[np.float64]:
    """Inner product of the solenoidal flow with ``grad F`` (should be ~0).

    The conservative (``Q``) component does no work against the free-energy
    gradient: ``(Q @ grad F) . grad F == 0`` everywhere. Returning the field
    of inner products lets a test assert this to machine precision.

    Args:
        x: X coordinates.
        y: Y coordinates.
        precision: Inverse-variance of the belief (``> 0``).
        omega: Solenoidal strength.

    Returns:
        Pointwise ``(Q grad F) . grad F``; analytically identically zero.
    """
    dfdx, dfdy = grad_free_energy(x, y, precision)
    qx = omega * dfdy
    qy = -omega * dfdx
    return qx * dfdx + qy * dfdy
