"""Exact-rational reference for the upstream canonical Gaussian carrier."""

import numpy as np
import pytest

from src.demos import NATIVE_BLANKET_PRECISION, NATIVE_BLANKET_COVARIANCE
from src.markov_blanket import (
    covariance_from_precision,
    conditional_covariance,
    partial_correlation,
)


def test_canonical_precision_and_covariance_match_exact_rational_inverse():
    np.testing.assert_allclose(
        NATIVE_BLANKET_PRECISION @ NATIVE_BLANKET_COVARIANCE, np.eye(4), atol=1e-15
    )
    np.testing.assert_allclose(
        covariance_from_precision(NATIVE_BLANKET_PRECISION), NATIVE_BLANKET_COVARIANCE
    )
    assert NATIVE_BLANKET_COVARIANCE[0, 3] == pytest.approx(1 / 24)


def test_canonical_conditioning_recovers_native_variance_and_mean_coefficients():
    cov = covariance_from_precision(NATIVE_BLANKET_PRECISION)
    np.testing.assert_allclose(
        conditional_covariance(cov, [0, 3], [1, 2]), np.eye(2) / 4, atol=1e-15
    )
    coefficient = cov[np.ix_([0, 3], [1, 2])] @ np.linalg.inv(
        cov[np.ix_([1, 2], [1, 2])]
    )
    np.testing.assert_allclose(coefficient, np.full((2, 2), 1 / 4))
    assert partial_correlation(cov, 0, 3, [1, 2]) == pytest.approx(0, abs=1e-15)


def test_nonzero_endpoint_precision_breaks_blanket_independence():
    perturbed = NATIVE_BLANKET_PRECISION.copy()
    perturbed[0, 3] = perturbed[3, 0] = 1.0
    conditional = conditional_covariance(
        covariance_from_precision(perturbed), [0, 3], [1, 2]
    )
    np.testing.assert_allclose(conditional, np.array([[4.0, -1.0], [-1.0, 4.0]]) / 15)
    assert conditional[0, 1] == pytest.approx(-1 / 15)
