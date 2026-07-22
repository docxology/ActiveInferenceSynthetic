"""Tests for src.expected_free_energy — action selection and explore/exploit.

No mocks: every assertion is a real numerical computation against a hand-worked
reference (closed-form predicted outcomes, expected log preferences, and
expected KL / mutual information), not self-consistency.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from src.expected_free_energy import (
    epistemic_value,
    expected_free_energy,
    pragmatic_value,
    predicted_outcomes,
    predicted_posteriors,
    select_policy,
)

# Two hidden states, uniform belief (maximally uncertain about the context).
_BELIEF = np.array([0.5, 0.5])

# "cue" — an informative action: the outcome reveals the state (high epistemic),
# but its outcomes are preference-neutral in expectation.
_CUE = np.array([[0.9, 0.1], [0.1, 0.9]])

# "bet" — an uninformative but rewarding action: outcome o0 ("reward") is likely
# regardless of state (zero epistemic), so its value is purely pragmatic.
_BET = np.array([[0.85, 0.85], [0.15, 0.15]])

_FLAT = np.array([0.5, 0.5])  # indifferent preferences
_SHARP = np.array([0.9, 0.1])  # strongly prefer outcome o0 ("reward")


def test_predicted_outcomes_hand_value() -> None:
    # q(o|cue) = [[0.9,0.1],[0.1,0.9]] @ [0.5,0.5] = [0.5, 0.5]
    assert np.allclose(predicted_outcomes(_CUE, _BELIEF), [0.5, 0.5])
    # q(o|bet) = [0.85, 0.15]
    assert np.allclose(predicted_outcomes(_BET, _BELIEF), [0.85, 0.15])


def test_predicted_posteriors_are_bayes() -> None:
    post = predicted_posteriors(_CUE, _BELIEF)
    # q(s|o0,cue) = [0.9*0.5, 0.1*0.5] / 0.5 = [0.9, 0.1]
    assert np.allclose(post[0], [0.9, 0.1])
    assert np.allclose(post[1], [0.1, 0.9])


def test_pragmatic_value_hand_value() -> None:
    # bet under sharp prefs: 0.85 ln0.9 + 0.15 ln0.1
    expected = 0.85 * math.log(0.9) + 0.15 * math.log(0.1)
    assert pragmatic_value(_BET, _BELIEF, _SHARP) == pytest.approx(expected, abs=1e-12)


def test_epistemic_value_hand_value() -> None:
    # cue: 0.5*KL([0.9,0.1]||[0.5,0.5]) + 0.5*KL([0.1,0.9]||[0.5,0.5]); symmetric.
    kl = 0.9 * math.log(0.9 / 0.5) + 0.1 * math.log(0.1 / 0.5)
    assert epistemic_value(_CUE, _BELIEF) == pytest.approx(kl, abs=1e-12)


def test_epistemic_value_equals_mutual_information() -> None:
    # Independent cross-check: the expected posterior-KL must equal the mutual
    # information I(s; o | a) computed straight from the joint p(o, s) — a
    # different formula, so this is not a roundtrip. I = Σ p(o,s) ln[p(o,s)/(p(o)p(s))].
    a, q = _CUE, _BELIEF
    joint = a * q  # p(o, s) = p(o|s) q(s), shape O x K
    p_o = joint.sum(axis=1)  # p(o)
    mi = 0.0
    for o in range(a.shape[0]):
        for s in range(a.shape[1]):
            if joint[o, s] > 0.0:
                mi += joint[o, s] * math.log(joint[o, s] / (p_o[o] * q[s]))
    assert epistemic_value(_CUE, _BELIEF) == pytest.approx(mi, abs=1e-12)


def test_epistemic_value_is_nonnegative() -> None:
    assert epistemic_value(_CUE, _BELIEF) > 0.0
    assert epistemic_value(_BET, _BELIEF) >= 0.0


def test_uninformative_action_has_zero_epistemic_value() -> None:
    # Positive control: an outcome model independent of the state carries no
    # information, so expected information gain is exactly 0.
    assert epistemic_value(_BET, _BELIEF) == pytest.approx(0.0, abs=1e-12)


def test_expected_free_energy_decomposition_identity() -> None:
    g = expected_free_energy(_CUE, _BELIEF, _SHARP)
    parts = -(
        pragmatic_value(_CUE, _BELIEF, _SHARP) + epistemic_value(_CUE, _BELIEF)
    )
    assert g == pytest.approx(parts, abs=1e-12)


def test_flat_preferences_select_the_informative_action() -> None:
    # With nothing to prefer, epistemic value dominates: explore (cue) wins.
    result = select_policy([_CUE, _BET], _BELIEF, _FLAT)
    assert result["choice"] == 0  # cue
    assert result["efe"][0] < result["efe"][1]


def test_sharp_preferences_select_the_rewarding_action() -> None:
    # With a strong goal, pragmatic value dominates: exploit (bet) wins.
    result = select_policy([_CUE, _BET], _BELIEF, _SHARP)
    assert result["choice"] == 1  # bet
    assert result["efe"][1] < result["efe"][0]


def test_select_policy_reports_decomposition() -> None:
    result = select_policy([_CUE, _BET], _BELIEF, _SHARP)
    assert result["epistemic"][0] > 0.0  # cue is informative
    assert result["epistemic"][1] == pytest.approx(0.0, abs=1e-12)  # bet is not
    assert result["pragmatic"][1] > result["pragmatic"][0]  # bet is more preferred


# --- input validation ---


def test_outcome_model_columns_must_sum_to_one() -> None:
    bad = np.array([[0.9, 0.1], [0.2, 0.9]])  # column 0 sums to 1.1
    with pytest.raises(ValueError, match="sum to 1"):
        predicted_outcomes(bad, _BELIEF)


def test_belief_must_match_state_count() -> None:
    with pytest.raises(ValueError, match="states"):
        predicted_outcomes(_CUE, np.array([0.3, 0.3, 0.4]))


def test_belief_must_sum_to_one() -> None:
    with pytest.raises(ValueError, match="sum to 1"):
        predicted_outcomes(_CUE, np.array([0.6, 0.6]))


def test_belief_must_be_nonnegative() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        predicted_outcomes(_CUE, np.array([1.5, -0.5]))


def test_belief_must_be_1d() -> None:
    with pytest.raises(ValueError, match="1-D"):
        predicted_outcomes(_CUE, np.array([[0.5], [0.5]]))


def test_outcome_model_must_be_nonnegative() -> None:
    bad = np.array([[1.2, 0.1], [-0.2, 0.9]])  # columns sum to 1 but has a negative
    with pytest.raises(ValueError, match="non-negative"):
        predicted_outcomes(bad, _BELIEF)


def test_outcome_model_must_be_2d() -> None:
    with pytest.raises(ValueError, match="2-D"):
        predicted_outcomes(np.array([0.5, 0.5]), _BELIEF)


def test_preferences_must_match_outcome_count() -> None:
    with pytest.raises(ValueError, match="preferences length"):
        pragmatic_value(_CUE, _BELIEF, np.array([0.3, 0.3, 0.4]))


def test_preferences_must_be_strictly_positive() -> None:
    with pytest.raises(ValueError, match="strictly positive"):
        pragmatic_value(_CUE, _BELIEF, np.array([1.0, 0.0]))


def test_select_policy_rejects_empty_policy_set() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        select_policy([], _BELIEF, _FLAT)


def test_epistemic_value_handles_impossible_outcome() -> None:
    # An outcome with zero predictive probability contributes nothing (no nan).
    model = np.array([[1.0, 1.0], [0.0, 0.0]])  # o1 never occurs
    assert np.isfinite(epistemic_value(model, _BELIEF))


def test_epistemic_value_never_negative_from_roundoff() -> None:
    # A near-uninformative action can produce a tiny negative from FP roundoff;
    # mutual information is provably >= 0, so the result must be clamped to >= 0.
    belief = np.array([0.01, 0.99])
    model = np.array([[0.07, 0.07], [0.93, 0.93]])
    assert epistemic_value(model, belief) >= 0.0


def test_nan_belief_is_rejected() -> None:
    with pytest.raises(ValueError, match="finite"):
        predicted_outcomes(_CUE, np.array([np.nan, np.nan]))


def test_nan_outcome_model_is_rejected() -> None:
    with pytest.raises(ValueError, match="finite"):
        predicted_outcomes(np.array([[np.nan, 0.1], [np.nan, 0.9]]), _BELIEF)
