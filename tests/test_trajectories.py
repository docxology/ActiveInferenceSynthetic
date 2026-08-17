"""Tests for src.trajectories — worked equilibrium vs NESS trajectories.

No mocks: the RK4 integrator is validated against the closed-form solution of
the linear ODE it reduces to at equilibrium, and the regime distinctions
(descent, relaxation, persistent current) are asserted on real integrated
paths.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.trajectories import (
    free_energy_along,
    integrate_trajectory,
    net_rotation,
)


def test_rk4_matches_closed_form_decay() -> None:
    # Equilibrium with precision=gamma=1 gives f = -x, so x(t) = x0 e^{-t}.
    start = (2.0, -1.5)
    dt, steps = 0.01, 500
    path = integrate_trajectory(start, gamma=1.0, omega=0.0, dt=dt, steps=steps)
    t_final = dt * steps
    expected = np.array(start) * np.exp(-t_final)
    assert np.allclose(path[-1], expected, atol=1e-6)


def test_equilibrium_free_energy_monotonically_decreases() -> None:
    path = integrate_trajectory((2.5, 1.0), omega=0.0, dt=0.01, steps=1000)
    fe = free_energy_along(path)
    assert np.all(np.diff(fe) <= 1e-9)


def test_equilibrium_relaxes_to_mode() -> None:
    start = (2.8, -2.0)
    path = integrate_trajectory(start, omega=0.0, dt=0.01, steps=2000)
    r0 = float(np.hypot(*start))
    r_final = float(np.hypot(path[-1, 0], path[-1, 1]))
    assert r_final < 0.01 * r0


def test_equilibrium_has_negligible_net_rotation() -> None:
    # Pure descent moves radially: essentially no angle is swept.
    path = integrate_trajectory((2.5, 1.3), omega=0.0, dt=0.01, steps=1500)
    assert abs(net_rotation(path)) < 1e-6


def test_ness_free_energy_still_decreases() -> None:
    # The solenoidal current does no work against F: descent is preserved.
    path = integrate_trajectory((2.5, 0.0), omega=2.4, dt=0.005, steps=2000)
    fe = free_energy_along(path)
    assert np.all(np.diff(fe) <= 1e-9)


def test_ness_accumulates_persistent_current() -> None:
    # A NESS spiral sweeps well past a full turn before relaxing inward.
    path = integrate_trajectory((2.5, 0.0), omega=6.0, dt=0.002, steps=6000)
    assert abs(net_rotation(path)) > 2.0 * np.pi


def test_ness_rotation_rate_is_intrinsic() -> None:
    # The angular velocity of this flow is analytically constant: dθ/dt = -ω·prec,
    # independent of radius and initial condition. So the accumulated angle is
    # exactly -ω·prec·T over horizon T = dt·steps — the intrinsic, window-free
    # witness of broken detailed balance is the RATE, not the window total.
    omega, precision, dt, steps = 5.0, 1.3, 0.002, 4000
    horizon = dt * steps
    for start in [(2.5, 0.0), (0.0, 1.8), (-1.2, 1.2)]:
        path = integrate_trajectory(
            start, precision=precision, gamma=1.0, omega=omega, dt=dt, steps=steps
        )
        expected = -omega * precision * horizon
        assert net_rotation(path) == pytest.approx(expected, rel=1e-3)


def test_ness_rotation_sign_follows_omega() -> None:
    # Flipping omega's sign reverses the circulation direction.
    p_pos = integrate_trajectory((2.0, 0.0), omega=4.0, dt=0.002, steps=4000)
    p_neg = integrate_trajectory((2.0, 0.0), omega=-4.0, dt=0.002, steps=4000)
    assert np.sign(net_rotation(p_pos)) == -np.sign(net_rotation(p_neg))
    assert abs(net_rotation(p_pos)) > 1.0


def test_ness_rotation_exceeds_equilibrium() -> None:
    eq = integrate_trajectory((2.5, 0.0), omega=0.0, dt=0.005, steps=2000)
    ness = integrate_trajectory((2.5, 0.0), omega=4.0, dt=0.005, steps=2000)
    assert abs(net_rotation(ness)) > abs(net_rotation(eq)) + 1.0


def test_trajectory_starts_at_start() -> None:
    path = integrate_trajectory((1.7, -0.3), dt=0.01, steps=10)
    assert np.allclose(path[0], (1.7, -0.3))
    assert path.shape == (11, 2)


# --- input validation ---


def test_integrate_rejects_nonpositive_dt() -> None:
    with pytest.raises(ValueError, match="dt must be > 0"):
        integrate_trajectory((1.0, 1.0), dt=0.0)


def test_integrate_rejects_nonpositive_steps() -> None:
    with pytest.raises(ValueError, match="steps must be >= 1"):
        integrate_trajectory((1.0, 1.0), steps=0)


def test_integrate_rejects_non_2vector_start() -> None:
    with pytest.raises(ValueError, match="2-vector"):
        integrate_trajectory((1.0, 2.0, 3.0))


def test_integrate_propagates_flow_validation() -> None:
    # gamma < 0 is rejected downstream by flow_field.
    with pytest.raises(ValueError, match="gamma must be >= 0"):
        integrate_trajectory((1.0, 1.0), gamma=-0.5)


def test_free_energy_along_rejects_bad_shape() -> None:
    with pytest.raises(ValueError, match=r"\(N, 2\)"):
        free_energy_along(np.zeros((5, 3)))


def test_net_rotation_rejects_bad_shape() -> None:
    with pytest.raises(ValueError, match=r"\(N, 2\)"):
        net_rotation(np.zeros((5,)))


def test_demo_rotation_matches_claim_ledger() -> None:
    """Live NESS winding must match data/claim_ledger.yaml, not sigma=11.52."""
    from src.demos import (
        FLOW,
        TRAJECTORY_DT,
        TRAJECTORY_OMEGA_NESS,
        TRAJECTORY_START,
        TRAJECTORY_STEPS,
    )

    horizon = TRAJECTORY_DT * TRAJECTORY_STEPS
    path = integrate_trajectory(
        TRAJECTORY_START,
        precision=FLOW.precision,
        gamma=FLOW.gamma,
        omega=TRAJECTORY_OMEGA_NESS,
        dt=TRAJECTORY_DT,
        steps=TRAJECTORY_STEPS,
    )
    turns = net_rotation(path) / (2.0 * np.pi)
    rate = turns / horizon
    analytic_rate = -TRAJECTORY_OMEGA_NESS * FLOW.precision / (2.0 * np.pi)
    analytic_turns = analytic_rate * horizon
    assert rate == pytest.approx(analytic_rate, rel=1e-8)
    assert turns == pytest.approx(analytic_turns, rel=1e-8)
    from src.manuscript_variables import compute_claims

    claims = compute_claims()
    assert turns == pytest.approx(claims["trajectory_turns"], rel=1e-8)
    assert rate == pytest.approx(claims["trajectory_rate"], rel=1e-8)
    assert abs(turns) < abs(claims["ness_sigma"])  # sigma is not winding


def test_manuscript_winding_not_confused_with_entropy_production() -> None:
    """§3 must quote the demo winding (~4.58 turns), not sigma (~11.5 nats/time)."""
    from pathlib import Path

    from src.manuscript_variables import generate_variables, leftover_tokens

    authored = (
        Path(__file__).resolve().parent.parent / "manuscript" / "03_worked_regimes.md"
    ).read_text()
    assert "{{TRAJECTORY_TURNS}}" in authored
    assert "{{TRAJECTORY_RATE}}" in authored
    assert "-11.5" not in authored
    assert "-0.95" not in authored
    variables = generate_variables()
    hydrated = authored
    for key, value in variables.items():
        hydrated = hydrated.replace("{{" + key + "}}", value)
    assert leftover_tokens(hydrated) == []
    assert variables["TRAJECTORY_TURNS"] in hydrated
    assert variables["NESS_SIGMA_APPROX"] not in hydrated
