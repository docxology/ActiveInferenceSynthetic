"""Tests for src.markov_blanket — conditional independence given the blanket.

No mocks: the Schur complement is checked against a hand-computed value, and the
blanket property (marginal dependence, conditional independence) is asserted on
a Gaussian built with a zero internal–external precision block.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.markov_blanket import (
    conditional_covariance,
    correlation_matrix,
    covariance_from_precision,
    is_markov_blanket,
    partial_correlation,
)

# Joint over (eta, s, a, mu) = indices (0, 1, 2, 3). The precision has a zero
# eta-mu block (0,3), so the blanket b = {s, a} = {1, 2} renders eta ⊥ mu | b.
# eta couples to BOTH blanket states (s and a); mu couples to both — so no
# strict subset of the blanket screens them.
_PRECISION = np.array(
    [
        [2.5, -0.8, -0.4, 0.0],  # eta — links to s, a; NOT mu
        [-0.8, 2.5, -0.5, -0.7],  # s   — links to eta, a, mu
        [-0.4, -0.5, 2.5, -0.6],  # a   — links to eta, s, mu
        [0.0, -0.7, -0.6, 2.5],  # mu  — links to s, a; NOT eta
    ]
)
_COV = covariance_from_precision(_PRECISION)

_ETA, _S, _A, _MU = 0, 1, 2, 3
_BLANKET = [_S, _A]


def test_covariance_from_precision_inverts() -> None:
    cov = covariance_from_precision(_PRECISION)
    assert np.allclose(cov @ _PRECISION, np.eye(4), atol=1e-10)
    assert np.allclose(cov, cov.T)


def test_covariance_from_precision_rejects_non_pd() -> None:
    with pytest.raises(ValueError, match="positive-definite"):
        covariance_from_precision(np.array([[1.0, 2.0], [2.0, 1.0]]))


def test_covariance_from_precision_rejects_non_square() -> None:
    with pytest.raises(ValueError, match="square"):
        covariance_from_precision(np.zeros((2, 3)))


def test_covariance_from_precision_rejects_asymmetric() -> None:
    with pytest.raises(ValueError, match="symmetric"):
        covariance_from_precision(np.array([[2.0, 0.5], [1.0, 2.0]]))


def test_precision_is_valid_spd_covariance() -> None:
    # Sanity: the constructed joint is a proper Gaussian.
    assert np.allclose(_COV, _COV.T)
    assert np.linalg.eigvalsh(_COV).min() > 0.0


def test_conditional_covariance_matches_hand_schur_complement() -> None:
    # Sigma_{0|1} = Sigma_00 - Sigma_01 Sigma_11^{-1} Sigma_10 on [[2,1],[1,2]].
    cov = np.array([[2.0, 1.0], [1.0, 2.0]])
    cond = conditional_covariance(cov, [0], [1])
    assert cond[0, 0] == pytest.approx(2.0 - 1.0 * (1.0 / 2.0) * 1.0)  # 1.5


def test_internal_and_external_are_marginally_dependent() -> None:
    # eta and mu talk through the blanket: nonzero marginal covariance.
    assert abs(_COV[_ETA, _MU]) > 1e-2
    corr = correlation_matrix(_COV)
    assert abs(corr[_ETA, _MU]) > 1e-2


def test_internal_and_external_independent_given_blanket() -> None:
    # The defining Markov-blanket property: eta ⊥ mu | {s, a}.
    cond = conditional_covariance(_COV, [_ETA, _MU], _BLANKET)
    assert abs(cond[0, 1]) < 1e-10


def test_partial_correlation_zero_given_full_blanket() -> None:
    assert partial_correlation(_COV, _ETA, _MU, _BLANKET) == pytest.approx(
        0.0, abs=1e-10
    )


def test_blanket_marginal_dependent_but_conditionally_independent() -> None:
    # Positive control in one assertion: the SAME pair is strongly dependent
    # marginally yet independent to machine precision given the blanket. A
    # vacuous test would fail the first clause, so this cannot pass trivially.
    marginal = correlation_matrix(_COV)[_ETA, _MU]
    conditional = partial_correlation(_COV, _ETA, _MU, _BLANKET)
    assert abs(marginal) > 0.1  # genuinely dependent without the blanket
    assert abs(conditional) < 1e-10  # independent given the blanket


def test_marginal_correlation_matches_pinned_ledger_value() -> None:
    # Regression-guards the derived pin `blanket-eta-mu-marginal-correlation =
    # 0.19` in data/claim_ledger.yaml and the manuscript/figure caption. If the
    # demonstration joint changes, this exact assertion forces a deliberate,
    # auditable update of the ledger + figure text together.
    corr = correlation_matrix(_COV)[_ETA, _MU]
    assert float(corr) == pytest.approx(0.18938495031558975, rel=1e-9)


def test_partial_correlation_nonzero_given_partial_blanket() -> None:
    # Negative control: conditioning on only s (not a) leaves the eta-a-mu path
    # open, so eta and mu remain conditionally correlated.
    assert abs(partial_correlation(_COV, _ETA, _MU, [_S])) > 1e-3


def test_is_markov_blanket_true_for_zero_block() -> None:
    assert is_markov_blanket(_PRECISION, internal_idx=[_MU], external_idx=[_ETA])


def test_is_markov_blanket_false_when_block_nonzero() -> None:
    # Add a direct eta-mu coupling: the blanket no longer screens them.
    bad = _PRECISION.copy()
    bad[_ETA, _MU] = bad[_MU, _ETA] = -0.3
    assert not is_markov_blanket(bad, internal_idx=[_MU], external_idx=[_ETA])


def test_correlation_matrix_has_unit_diagonal() -> None:
    corr = correlation_matrix(_COV)
    assert np.allclose(np.diag(corr), 1.0)


# --- input validation ---


def test_conditional_covariance_rejects_non_spd() -> None:
    with pytest.raises(ValueError, match="positive-definite"):
        conditional_covariance(np.array([[1.0, 2.0], [2.0, 1.0]]), [0], [1])


def test_conditional_covariance_rejects_asymmetric() -> None:
    with pytest.raises(ValueError, match="symmetric"):
        conditional_covariance(np.array([[2.0, 0.5], [1.0, 2.0]]), [0], [1])


def test_conditional_covariance_rejects_non_finite() -> None:
    with pytest.raises(ValueError, match="finite"):
        conditional_covariance(np.array([[np.nan, 0.0], [0.0, 1.0]]), [0], [1])


def test_is_markov_blanket_rejects_non_finite_precision() -> None:
    bad = _PRECISION.copy()
    bad[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        is_markov_blanket(bad, internal_idx=[_MU], external_idx=[_ETA])


def test_conditional_covariance_rejects_overlap() -> None:
    with pytest.raises(ValueError, match="disjoint"):
        conditional_covariance(_COV, [_ETA, _S], [_S, _A])


def test_conditional_covariance_rejects_out_of_range() -> None:
    with pytest.raises(ValueError, match="out of range"):
        conditional_covariance(_COV, [0], [9])


def test_conditional_covariance_rejects_non_square() -> None:
    with pytest.raises(ValueError, match="square"):
        conditional_covariance(np.zeros((2, 3)), [0], [1])


def test_conditional_covariance_rejects_empty_index_set() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        conditional_covariance(_COV, [], [1])


def test_conditional_covariance_rejects_repeated_indices() -> None:
    with pytest.raises(ValueError, match="not repeat"):
        conditional_covariance(_COV, [0, 0], [1])


def test_partial_correlation_rejects_equal_indices() -> None:
    with pytest.raises(ValueError, match="must differ"):
        partial_correlation(_COV, _ETA, _ETA, _BLANKET)


def test_is_markov_blanket_rejects_overlap() -> None:
    with pytest.raises(ValueError, match="disjoint"):
        is_markov_blanket(_PRECISION, internal_idx=[_MU], external_idx=[_MU, _ETA])


def test_is_markov_blanket_rejects_non_square() -> None:
    with pytest.raises(ValueError, match="square"):
        is_markov_blanket(np.zeros((2, 3)), internal_idx=[0], external_idx=[1])


def test_is_markov_blanket_rejects_non_positive_definite() -> None:
    # A "precision" that is not SPD is not a valid Gaussian precision — the
    # conditional-independence reading of a zero block would be meaningless.
    with pytest.raises(ValueError, match="positive-definite"):
        is_markov_blanket(np.diag([1.0, -1.0]), internal_idx=[0], external_idx=[1])


def test_is_markov_blanket_rejects_asymmetric() -> None:
    with pytest.raises(ValueError, match="symmetric"):
        is_markov_blanket(
            np.array([[2.0, 0.5], [1.0, 2.0]]), internal_idx=[0], external_idx=[1]
        )


def test_is_markov_blanket_rejects_negative_tol() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        is_markov_blanket(_PRECISION, internal_idx=[_MU], external_idx=[_ETA], tol=-1.0)


def test_covariance_from_precision_rejects_ill_conditioned() -> None:
    # A near-singular precision cannot be inverted to a finite covariance.
    with pytest.raises(ValueError, match="positive-definite|ill-conditioned|finite"):
        covariance_from_precision(np.diag([1.0, 1e-320]))
