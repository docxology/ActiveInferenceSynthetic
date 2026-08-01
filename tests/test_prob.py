"""Tests for src._prob shared validators."""

from __future__ import annotations

import numpy as np
import pytest

from src._prob import (
    as_column_stochastic,
    as_distribution,
    as_prob_vector,
    kl_divergence,
)


def test_as_distribution_rejects_bad_sum() -> None:
    with pytest.raises(ValueError, match="sum to 1"):
        as_distribution(np.array([0.6, 0.6]), "p")


def test_as_column_stochastic_validates_columns() -> None:
    good = np.array([[0.9, 0.2], [0.1, 0.8]])
    out = as_column_stochastic(good, "likelihood")
    assert np.allclose(out.sum(axis=0), 1.0)


def test_kl_divergence_hand_value() -> None:
    q = np.array([0.9, 0.1])
    p = np.array([0.5, 0.5])
    expected = 0.9 * np.log(0.9 / 0.5) + 0.1 * np.log(0.1 / 0.5)
    assert kl_divergence(q, p) == pytest.approx(expected)


def test_kl_divergence_rejects_zero_reference_where_q_positive() -> None:
    # A zero reference entry under a positively-weighted mass makes ln p = -inf;
    # the helper must reject it rather than silently return inf.
    q = np.array([0.5, 0.5])
    p = np.array([1.0, 0.0])
    with pytest.raises(ValueError, match="strictly positive"):
        kl_divergence(q, p)


def test_kl_divergence_ignores_zero_q_with_zero_p() -> None:
    # Where the belief q has zero mass the reference may be zero too; only the
    # positively-weighted entries participate (mask semantics).
    q = np.array([1.0, 0.0])
    p = np.array([0.5, 0.0])
    assert kl_divergence(q, p) == pytest.approx(1.0 * np.log(1.0 / 0.5))


def test_as_prob_vector_rejects_2d() -> None:
    with pytest.raises(ValueError, match="1-D"):
        as_prob_vector(np.array([[0.5, 0.5]]), "p")
