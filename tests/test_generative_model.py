"""Tests for src.generative_model — perception as free-energy minimization.

No mocks: every assertion is a real numerical computation against a closed-form
Bayesian reference (hand-checked posteriors, the exact surprise bound, the
complexity−accuracy identity), not self-consistency.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from src.generative_model import (
    evidence,
    joint,
    minimize_free_energy,
    posterior,
    surprise,
    variational_free_energy,
    vfe_components,
)

# A small, fully hand-checkable model: 2 hidden states, 2 observations.
#   prior      p(x)   = [0.6, 0.4]
#   likelihood p(s|x) = [[0.9, 0.2],   # p(s=0|x=0)=0.9, p(s=0|x=1)=0.2
#                        [0.1, 0.8]]   # p(s=1|x=0)=0.1, p(s=1|x=1)=0.8
_PRIOR = np.array([0.6, 0.4])
_LIKELIHOOD = np.array([[0.9, 0.2], [0.1, 0.8]])


def _uniform(k: int) -> np.ndarray:
    return np.full(k, 1.0 / k)


def test_joint_matches_hand_computation() -> None:
    # p(s=0, x) = [0.9*0.6, 0.2*0.4] = [0.54, 0.08]
    assert np.allclose(joint(_LIKELIHOOD, _PRIOR, 0), [0.54, 0.08])


def test_evidence_is_marginal_likelihood() -> None:
    # p(s=0) = 0.54 + 0.08 = 0.62
    assert evidence(_LIKELIHOOD, _PRIOR, 0) == pytest.approx(0.62)
    # p(s=1) = 0.06 + 0.32 = 0.38; both observations partition the mass.
    assert evidence(_LIKELIHOOD, _PRIOR, 1) == pytest.approx(0.38)
    assert evidence(_LIKELIHOOD, _PRIOR, 0) + evidence(
        _LIKELIHOOD, _PRIOR, 1
    ) == pytest.approx(1.0)


def test_posterior_matches_exact_bayes() -> None:
    # p(x|s=0) = [0.54, 0.08] / 0.62
    expected = np.array([0.54, 0.08]) / 0.62
    assert np.allclose(posterior(_LIKELIHOOD, _PRIOR, 0), expected)
    assert posterior(_LIKELIHOOD, _PRIOR, 0).sum() == pytest.approx(1.0)


def test_surprise_equals_neg_log_evidence() -> None:
    assert surprise(_LIKELIHOOD, _PRIOR, 0) == pytest.approx(-np.log(0.62))


def test_vfe_at_posterior_equals_surprise() -> None:
    # The bound is TIGHT at the posterior: F[p(x|s)] = -ln p(s).
    post = posterior(_LIKELIHOOD, _PRIOR, 0)
    f_post = variational_free_energy(post, _LIKELIHOOD, _PRIOR, 0)
    assert f_post == pytest.approx(surprise(_LIKELIHOOD, _PRIOR, 0), abs=1e-12)


@pytest.mark.parametrize(
    "q",
    [
        np.array([0.5, 0.5]),
        np.array([0.1, 0.9]),
        np.array([0.99, 0.01]),
    ],
)
def test_vfe_bounds_surprise_from_above(q: np.ndarray) -> None:
    # For any non-posterior belief, F[q] > -ln p(s) strictly.
    f_q = variational_free_energy(q, _LIKELIHOOD, _PRIOR, 0)
    assert f_q > surprise(_LIKELIHOOD, _PRIOR, 0)


def test_vfe_gap_is_kl_to_posterior() -> None:
    # F[q] - surprise == KL[q || posterior], the exact variational gap.
    q = np.array([0.3, 0.7])
    post = posterior(_LIKELIHOOD, _PRIOR, 0)
    gap = variational_free_energy(q, _LIKELIHOOD, _PRIOR, 0) - surprise(
        _LIKELIHOOD, _PRIOR, 0
    )
    kl = float(np.sum(q * (np.log(q) - np.log(post))))
    assert gap == pytest.approx(kl, abs=1e-12)


def test_vfe_matches_independent_hand_reference() -> None:
    # Fully independent reference: F = Σ q ln(q / p(s,x)) with the joint
    # p(s=0, x) = [0.54, 0.08] computed by hand, NOT via any src function.
    q = np.array([0.3, 0.7])
    hand = 0.3 * math.log(0.3 / 0.54) + 0.7 * math.log(0.7 / 0.08)
    assert variational_free_energy(q, _LIKELIHOOD, _PRIOR, 0) == pytest.approx(
        hand, abs=1e-12
    )


def test_vfe_complexity_minus_accuracy_identity() -> None:
    q = np.array([0.3, 0.7])
    complexity, accuracy = vfe_components(q, _LIKELIHOOD, _PRIOR, 0)
    direct = variational_free_energy(q, _LIKELIHOOD, _PRIOR, 0)
    assert complexity - accuracy == pytest.approx(direct, abs=1e-12)


def test_prior_belief_has_zero_complexity() -> None:
    # KL[prior || prior] == 0: believing the prior pays no complexity cost.
    complexity, _ = vfe_components(_PRIOR, _LIKELIHOOD, _PRIOR, 0)
    assert complexity == pytest.approx(0.0, abs=1e-12)


def test_minimize_free_energy_converges_to_posterior() -> None:
    result = minimize_free_energy(_LIKELIHOOD, _PRIOR, 0, learning_rate=0.3, steps=500)
    final_belief = result.beliefs[-1]
    assert np.allclose(final_belief, posterior(_LIKELIHOOD, _PRIOR, 0), atol=1e-6)


def test_minimize_free_energy_is_monotonic() -> None:
    # Perception lowers free energy: F is non-increasing every step.
    result = minimize_free_energy(_LIKELIHOOD, _PRIOR, 0, learning_rate=0.3, steps=500)
    fe = result.free_energy
    diffs = np.diff(fe)
    assert np.all(diffs <= 1e-12)


def test_minimize_free_energy_reaches_surprise() -> None:
    # The minimized free energy equals the surprise it bounds.
    result = minimize_free_energy(_LIKELIHOOD, _PRIOR, 0, learning_rate=0.3, steps=500)
    assert result.free_energy[-1] == pytest.approx(
        surprise(_LIKELIHOOD, _PRIOR, 0), abs=1e-6
    )


def test_minimize_free_energy_records_full_trajectory() -> None:
    result = minimize_free_energy(_LIKELIHOOD, _PRIOR, 0, steps=10)
    assert result.beliefs.shape == (11, 2)
    assert result.free_energy.shape == (11,)
    # Step 0 is the uniform starting belief.
    assert np.allclose(result.beliefs[0], _uniform(2))


def test_minimize_free_energy_accepts_custom_init() -> None:
    q0 = np.array([0.8, 0.2])
    result = minimize_free_energy(_LIKELIHOOD, _PRIOR, 0, q_init=q0, steps=5)
    assert np.allclose(result.beliefs[0], q0)


# --- input validation (no-mocks: real bad inputs, real exceptions) ---


def test_likelihood_columns_must_sum_to_one() -> None:
    bad = np.array([[0.9, 0.2], [0.2, 0.8]])  # column 0 sums to 1.1
    with pytest.raises(ValueError, match="sum to 1"):
        posterior(bad, _PRIOR, 0)


def test_prior_must_sum_to_one() -> None:
    with pytest.raises(ValueError, match="sum to 1"):
        posterior(_LIKELIHOOD, np.array([0.6, 0.6]), 0)


def test_prior_must_be_nonnegative() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        posterior(_LIKELIHOOD, np.array([1.4, -0.4]), 0)


def test_likelihood_must_be_nonnegative() -> None:
    # A negative likelihood entry (columns still sum to 1) is rejected.
    bad = np.array([[1.2, 0.2], [-0.2, 0.8]])
    with pytest.raises(ValueError, match="non-negative"):
        posterior(bad, _PRIOR, 0)


def test_prior_must_be_finite() -> None:
    with pytest.raises(ValueError, match="finite"):
        posterior(_LIKELIHOOD, np.array([np.nan, np.nan]), 0)


def test_likelihood_must_be_finite() -> None:
    with pytest.raises(ValueError, match="finite"):
        posterior(np.array([[np.nan, 0.1], [np.nan, 0.9]]), _PRIOR, 0)


def test_prior_length_must_match_states() -> None:
    with pytest.raises(ValueError, match="length"):
        posterior(_LIKELIHOOD, np.array([0.3, 0.3, 0.4]), 0)


def test_likelihood_must_be_2d() -> None:
    with pytest.raises(ValueError, match="2-D"):
        posterior(np.array([0.5, 0.5]), _PRIOR, 0)


def test_prior_must_be_1d() -> None:
    with pytest.raises(ValueError, match="1-D"):
        posterior(_LIKELIHOOD, np.array([[0.6], [0.4]]), 0)


def test_obs_out_of_range_raises() -> None:
    with pytest.raises(ValueError, match="obs must be an integer"):
        posterior(_LIKELIHOOD, _PRIOR, 5)


def test_q_length_must_match_states() -> None:
    with pytest.raises(ValueError, match="q length"):
        variational_free_energy(np.array([0.3, 0.3, 0.4]), _LIKELIHOOD, _PRIOR, 0)


def test_vfe_components_q_length_must_match_states() -> None:
    with pytest.raises(ValueError, match="q length"):
        vfe_components(np.array([0.3, 0.3, 0.4]), _LIKELIHOOD, _PRIOR, 0)


def test_minimize_rejects_nonpositive_learning_rate() -> None:
    with pytest.raises(ValueError, match="learning_rate must be > 0"):
        minimize_free_energy(_LIKELIHOOD, _PRIOR, 0, learning_rate=0.0)


def test_minimize_rejects_nonpositive_steps() -> None:
    with pytest.raises(ValueError, match="steps must be >= 1"):
        minimize_free_energy(_LIKELIHOOD, _PRIOR, 0, steps=0)


def test_impossible_observation_raises() -> None:
    # An observation with zero evidence under the model: p(s=1)=0.
    certain = np.array([[1.0, 1.0], [0.0, 0.0]])
    with pytest.raises(ValueError, match="impossible"):
        surprise(certain, _PRIOR, 1)
    with pytest.raises(ValueError, match="impossible"):
        posterior(certain, _PRIOR, 1)


def test_vfe_handles_zero_belief_component() -> None:
    # A belief with a zero entry: 0*ln0 -> 0, no NaN.
    f = variational_free_energy(np.array([1.0, 0.0]), _LIKELIHOOD, _PRIOR, 0)
    assert np.isfinite(f)


def test_vfe_components_no_nan_on_zero_support_likelihood() -> None:
    # State x1 makes the observed s=0 impossible (a_row=[0.9, 0.0]); a belief
    # that has abandoned x1 (q=[1,0]) must give finite, NaN-free components.
    zero_support = np.array([[0.9, 0.0], [0.1, 1.0]])
    complexity, accuracy = vfe_components(np.array([1.0, 0.0]), zero_support, _PRIOR, 0)
    assert np.isfinite(complexity)
    assert np.isfinite(accuracy)


def test_minimize_rejects_zero_support_joint() -> None:
    # A state under which the observation is impossible makes the log-joint
    # infinite; softmax always keeps q>0 there, so this is rejected up front.
    zero_support = np.array([[0.9, 0.0], [0.1, 1.0]])
    with pytest.raises(ValueError, match="strictly positive joint"):
        minimize_free_energy(zero_support, _PRIOR, 0)


def test_minimize_rejects_zero_prior_state() -> None:
    # A state with zero prior mass also gives a zero joint entry.
    with pytest.raises(ValueError, match="strictly positive joint"):
        minimize_free_energy(_LIKELIHOOD, np.array([1.0, 0.0]), 0)
