"""Tests for src.free_energy_flow — the numerical core of the overview figure.

No mocks: every assertion is a real numerical computation against an
analytic reference (closed-form gradients, finite differences, and the
exact orthogonality of the solenoidal term).
"""

from __future__ import annotations

import numpy as np
import pytest

from src.free_energy_flow import (
    flow_field,
    free_energy,
    grad_free_energy,
    solenoidal_is_conservative,
)


def test_free_energy_is_zero_at_mode() -> None:
    assert free_energy(np.array(0.0), np.array(0.0)) == pytest.approx(0.0)


def test_free_energy_quadratic_value() -> None:
    # F = 0.5 * precision * (x^2 + y^2); precision=2 at (1, 1) -> 0.5*2*2 = 2.
    val = free_energy(np.array(1.0), np.array(1.0), precision=2.0)
    assert val == pytest.approx(2.0)


def test_free_energy_rejects_nonpositive_precision() -> None:
    with pytest.raises(ValueError, match="precision must be > 0"):
        free_energy(np.array(1.0), np.array(1.0), precision=0.0)


def test_gradient_matches_finite_difference() -> None:
    x0, y0, prec, h = 0.7, -1.3, 1.7, 1e-6
    gx, gy = grad_free_energy(np.array(x0), np.array(y0), precision=prec)
    fd_x = (
        free_energy(np.array(x0 + h), np.array(y0), prec)
        - free_energy(np.array(x0 - h), np.array(y0), prec)
    ) / (2 * h)
    fd_y = (
        free_energy(np.array(x0), np.array(y0 + h), prec)
        - free_energy(np.array(x0), np.array(y0 - h), prec)
    ) / (2 * h)
    assert float(gx) == pytest.approx(float(fd_x), abs=1e-5)
    assert float(gy) == pytest.approx(float(fd_y), abs=1e-5)


def test_gradient_rejects_nonpositive_precision() -> None:
    with pytest.raises(ValueError, match="precision must be > 0"):
        grad_free_energy(np.array(1.0), np.array(1.0), precision=-1.0)


def test_equilibrium_flow_is_pure_gradient_descent() -> None:
    # omega=0 -> f == -gamma * grad F, pointing straight at the mode.
    x = np.array([1.0, -2.0, 0.5])
    y = np.array([1.0, 0.0, -0.5])
    gx, gy = grad_free_energy(x, y)
    fx, fy = flow_field(x, y, gamma=1.0, omega=0.0)
    assert np.allclose(fx, -gx)
    assert np.allclose(fy, -gy)


def test_equilibrium_flow_points_inward() -> None:
    # Dissipative descent reduces the radius everywhere off the mode.
    x = np.array([2.0, -1.0])
    y = np.array([0.0, 3.0])
    fx, fy = flow_field(x, y, gamma=0.8, omega=0.0)
    # Radial component f . r < 0 (moving toward origin).
    radial = fx * x + fy * y
    assert np.all(radial < 0.0)


def test_solenoidal_term_is_orthogonal_to_gradient() -> None:
    # The Q-current does no work against grad F: inner product ~ 0 everywhere.
    grid = np.linspace(-3.0, 3.0, 9)
    xx, yy = np.meshgrid(grid, grid)
    inner = solenoidal_is_conservative(xx, yy, precision=1.4, omega=2.0)
    assert np.allclose(inner, 0.0, atol=1e-12)


def test_ness_flow_has_rotational_component() -> None:
    # With omega != 0 the flow is no longer parallel to -grad F.
    x, y = np.array(1.0), np.array(0.0)
    gx, gy = grad_free_energy(x, y)
    fx, fy = flow_field(x, y, gamma=1.0, omega=1.5)
    # Cross product of flow with gradient is nonzero -> rotation present.
    cross = float(fx) * float(gy) - float(fy) * float(gx)
    assert abs(cross) > 1e-6


def test_flow_rejects_negative_gamma() -> None:
    with pytest.raises(ValueError, match="gamma must be >= 0"):
        flow_field(np.array(1.0), np.array(1.0), gamma=-0.1)
