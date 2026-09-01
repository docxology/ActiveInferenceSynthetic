"""Tests for src.steady_state — NESS current, entropy production, circulation.

No mocks: the Lyapunov solution, entropy-production rate, and circulation are
each asserted against an independent closed form, and the probability current is
checked to be divergence-free by finite differences on a real grid.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.steady_state import (
    current_circulation,
    drift_matrix,
    entropy_production_rate,
    probability_current,
    stationary_covariance,
)


def test_stationary_covariance_equals_inverse_precision() -> None:
    # With D = Gamma (fluctuation-dissipation), the stationary covariance is P^-1.
    p = 1.3
    sigma = stationary_covariance(precision=p, gamma=0.9, omega=2.1)
    assert np.allclose(sigma, (1.0 / p) * np.eye(2), atol=1e-12)


def test_stationary_covariance_solves_lyapunov() -> None:
    p, g, w = 1.3, 0.9, 2.1
    m = drift_matrix(precision=p, gamma=g, omega=w)
    sigma = stationary_covariance(precision=p, gamma=g, omega=w)
    d = g * np.eye(2)
    residual = m @ sigma + sigma @ m.T - 2.0 * d
    assert np.allclose(residual, 0.0, atol=1e-10)


def test_entropy_production_matches_closed_form() -> None:
    p, g, w = 1.3, 0.9, 2.1
    assert entropy_production_rate(precision=p, gamma=g, omega=w) == pytest.approx(
        2.0 * w**2 * p / g, abs=1e-9
    )


def test_entropy_production_matches_current_field_integral() -> None:
    # Independent, non-analytic cross-check: compute sigma operationally by
    # numerically integrating the current-field definition sigma = int j^T D^-1 j / rho,
    # which routes through the probability_current field on a grid rather than the
    # trace/Lyapunov algebra. Guards against a shared-derivation sign slip.
    p, g, w = 1.0, 1.0, 2.4
    length, n = 7.0, 1200
    grid = np.linspace(-length, length, n)
    xx, yy = np.meshgrid(grid, grid)
    d_area = (2 * length / (n - 1)) ** 2
    jx, jy = probability_current(xx, yy, precision=p, gamma=g, omega=w)
    rho = (p / (2 * np.pi)) * np.exp(-0.5 * p * (xx**2 + yy**2))
    numer = (jx**2 + jy**2) / g
    integrand = np.divide(numer, rho, out=np.zeros_like(numer), where=rho > 1e-300)
    sigma_grid = float(np.sum(integrand) * d_area)
    assert sigma_grid == pytest.approx(entropy_production_rate(p, g, w), rel=1e-3)
    assert sigma_grid == pytest.approx(2.0 * w**2 * p / g, rel=1e-3)


def test_entropy_production_zero_at_equilibrium() -> None:
    # Positive control: exactly zero iff detailed balance (omega = 0).
    assert entropy_production_rate(
        precision=1.3, gamma=0.9, omega=0.0
    ) == pytest.approx(0.0, abs=1e-12)


def test_entropy_production_is_nonnegative_and_grows_with_omega() -> None:
    s1 = entropy_production_rate(omega=1.0)
    s2 = entropy_production_rate(omega=2.0)
    assert s1 >= 0.0
    assert s2 > s1  # more irreversibility for a stronger solenoidal drive


def test_current_circulation_matches_closed_form() -> None:
    # Mean angular momentum of the current = -2 omega (independent of p, gamma).
    for p, g, w in [(1.0, 1.0, 1.5), (2.0, 0.7, -0.8)]:
        assert current_circulation(precision=p, gamma=g, omega=w) == pytest.approx(
            -2.0 * w, abs=1e-9
        )


def test_current_circulation_zero_at_equilibrium() -> None:
    assert current_circulation(precision=1.0, gamma=1.0, omega=0.0) == pytest.approx(
        0.0, abs=1e-12
    )


def test_probability_current_vanishes_at_equilibrium() -> None:
    # omega = 0 -> no current anywhere.
    grid = np.linspace(-2, 2, 11)
    xx, yy = np.meshgrid(grid, grid)
    jx, jy = probability_current(xx, yy, precision=1.0, gamma=1.0, omega=0.0)
    assert np.allclose(jx, 0.0)
    assert np.allclose(jy, 0.0)


def test_probability_current_nonzero_out_of_equilibrium() -> None:
    jx, jy = probability_current(
        np.array(1.0), np.array(0.5), precision=1.0, gamma=1.0, omega=2.0
    )
    assert abs(float(jx)) + abs(float(jy)) > 1e-6


def test_probability_current_pointwise_orientation() -> None:
    # Positive control on the ORIENTATION: j = (QPx)rho with QPx = omega*(y, -x)
    # at unit precision. A sign-flipped current would fail this even though it
    # would still be divergence-free and orthogonal to grad F.
    x, y, p, w = 1.0, 0.5, 1.0, 2.0
    jx, jy = probability_current(
        np.array(x), np.array(y), precision=p, gamma=1.0, omega=w
    )
    rho = (p / (2.0 * np.pi)) * np.exp(-0.5 * p * (x**2 + y**2))
    assert float(jx) == pytest.approx(rho * w * y)
    assert float(jy) == pytest.approx(rho * (-w * x))


def test_probability_current_vanishes_at_the_mode() -> None:
    # The current velocity v = QPx is zero at the origin.
    jx, jy = probability_current(
        np.array(0.0), np.array(0.0), precision=1.0, gamma=1.0, omega=2.0
    )
    assert float(jx) == pytest.approx(0.0)
    assert float(jy) == pytest.approx(0.0)


def test_probability_current_is_divergence_free() -> None:
    # In steady state div j = 0. Check by central finite differences on a grid.
    h = 1e-4
    p, g, w = 1.0, 1.0, 2.0

    def jx_at(x: float, y: float) -> float:
        return float(probability_current(np.array(x), np.array(y), p, g, w)[0])

    def jy_at(x: float, y: float) -> float:
        return float(probability_current(np.array(x), np.array(y), p, g, w)[1])

    for x0, y0 in [(0.7, -0.4), (1.1, 0.9), (-0.6, 0.3)]:
        djx_dx = (jx_at(x0 + h, y0) - jx_at(x0 - h, y0)) / (2 * h)
        djy_dy = (jy_at(x0, y0 + h) - jy_at(x0, y0 - h)) / (2 * h)
        assert abs(djx_dx + djy_dy) < 1e-6


def test_probability_current_is_orthogonal_to_gradient() -> None:
    # The current velocity QPx is orthogonal to grad F = P x (it runs along the
    # level sets of F), so it does no work against free energy.
    x, y = np.array(1.3), np.array(-0.8)
    jx, jy = probability_current(x, y, precision=1.0, gamma=1.0, omega=2.0)
    # grad F direction is (x, y) for isotropic P; j should be perpendicular.
    dot = float(jx) * float(x) + float(jy) * float(y)
    assert abs(dot) < 1e-12


# --- input validation ---


def test_rejects_nonpositive_precision() -> None:
    with pytest.raises(ValueError, match="precision must be > 0"):
        stationary_covariance(precision=0.0)


def test_rejects_nonpositive_gamma() -> None:
    with pytest.raises(ValueError, match="gamma must be > 0"):
        entropy_production_rate(gamma=0.0)


def test_rejects_non_finite_parameters() -> None:
    with pytest.raises(ValueError, match="finite"):
        entropy_production_rate(precision=np.nan)
    with pytest.raises(ValueError, match="finite"):
        stationary_covariance(omega=np.inf)


def test_stationary_covariance_closed_form_at_extreme_omega() -> None:
    # Large |omega| * precision used to make a Kronecker Lyapunov solve lose
    # precision. The implementation now returns the exact Sigma = P^{-1}.
    p, g, w = 1e6, 1.0, 1e12
    sigma = stationary_covariance(precision=p, gamma=g, omega=w)
    assert np.allclose(sigma, (1.0 / p) * np.eye(2), rtol=1e-12, atol=1e-18)
    # ... and the downstream entropy production still matches its closed form.
    assert entropy_production_rate(precision=p, gamma=g, omega=w) == pytest.approx(
        2.0 * w**2 * p / g, rel=1e-9
    )


def test_stationary_covariance_raises_on_overflow_parameters() -> None:
    # With parameters so extreme that BOTH the direct solve and the analytic
    # P^{-1} overflow to infinity, the guard still rejects rather than return a
    # silently-wrong matrix.
    with (
        np.errstate(over="ignore", invalid="ignore", divide="ignore"),
        pytest.raises(ValueError, match="unreliable|residual"),
    ):
        stationary_covariance(precision=1e200, gamma=1.0, omega=1e200)
