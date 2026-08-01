"""Tests for src.ou_model.IsotropicOU."""

from __future__ import annotations

import numpy as np
import pytest

from src.ou_model import IsotropicOU


def test_flow_matches_free_energy_flow() -> None:
    # IsotropicOU.flow_field (used by demos.py) must agree with the independent
    # src.free_energy_flow.flow_field and with the analytic form
    # f = (Q - Gamma) grad F -> fx = -gamma*p*x + omega*p*y;
    #                          fy = -gamma*p*y - omega*p*x.
    from src.free_energy_flow import flow_field as reference_flow

    precision, gamma, omega = 1.4, 0.8, 2.0
    model = IsotropicOU(precision=precision, gamma=gamma, omega=omega)
    x = np.array([1.0, -2.0])
    y = np.array([0.0, 3.0])
    fx, fy = model.flow_field(x, y)

    ref_fx, ref_fy = reference_flow(x, y, precision=precision, gamma=gamma, omega=omega)
    assert np.allclose(fx, ref_fx)
    assert np.allclose(fy, ref_fy)

    p, g, w = precision, gamma, omega
    assert np.allclose(fx, -g * p * x + w * p * y)
    assert np.allclose(fy, -g * p * y - w * p * x)


def test_require_positive_gamma_for_steady_state_path() -> None:
    model = IsotropicOU(gamma=0.0)
    with pytest.raises(ValueError, match="gamma must be > 0"):
        model.require_positive_gamma()
