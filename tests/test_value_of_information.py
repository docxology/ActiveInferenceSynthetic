from itertools import product

import numpy as np
import pytest

from src.value_of_information import value_of_information


def test_feedback_matches_all_deterministic_policy_trees():
    prior = np.array([0.3, 0.7])
    channel = np.array([[0.8, 0.1], [0.2, 0.9], [0.0, 0.0]])
    utilities = np.array([[2.0, -1.0], [-2.0, 3.0], [0.5, 0.5]])
    joint = channel * prior
    alternatives = [
        sum(joint[o] @ utilities[choice] for o, choice in enumerate(policy))
        for policy in product(range(3), repeat=3)
    ]
    result = value_of_information(channel, prior, utilities, cost=0.2)
    assert result.informed_utility == pytest.approx(max(alternatives))
    assert result.baseline_utility == pytest.approx(1.5)
    assert result.feedback_actions == (0, 1, None)
    assert result.net_value == pytest.approx(max(alternatives) - 1.5 - 0.2)


def test_binary_accuracy_oracle_cost_and_counterexamples():
    prior = np.array([0.5, 0.5])
    cue = np.array([[0.9, 0.1], [0.1, 0.9]])
    result = value_of_information(cue, prior, np.eye(2), cost=0.15)
    assert result.baseline_action == 0
    assert result.feedback_actions == (0, 1)
    assert result.informed_utility == pytest.approx(0.9)
    assert result.gross_value == pytest.approx(0.4)
    assert result.net_value == pytest.approx(0.25)
    assert result.information_nats == pytest.approx(
        0.9 * np.log(1.8) + 0.1 * np.log(0.2)
    )
    no_information = value_of_information(np.full((2, 2), 0.5), prior, np.eye(2))
    assert no_information.gross_value == pytest.approx(0)
    assert no_information.information_nats == pytest.approx(0)
    irrelevant = value_of_information(cue, prior, np.array([[0.8, 0.8], [0.2, 0.2]]))
    assert irrelevant.information_nats > 0
    assert irrelevant.gross_value == pytest.approx(0)
    costly = value_of_information(cue, prior, np.eye(2), cost=0.5)
    assert costly.net_value < 0


def test_prior_certainty_and_state_only_utility_offset():
    channel = np.eye(2)
    certain = value_of_information(channel, np.array([1., 0.]), np.eye(2))
    assert certain.feedback_actions == (0, None)
    assert certain.gross_value == pytest.approx(0)
    assert certain.information_nats == pytest.approx(0)
    prior = np.array([0.3, 0.7])
    first = value_of_information(channel, prior, np.eye(2))
    shifted = value_of_information(channel, prior, np.eye(2) + np.array([3., -2.]))
    assert first.gross_value == pytest.approx(shifted.gross_value)
    assert first.feedback_actions == shifted.feedback_actions


@pytest.mark.parametrize("cost", [-1., np.nan, np.inf, True, None])
def test_invalid_cost(cost):
    with pytest.raises(ValueError, match="cost"):
        value_of_information(np.eye(2), np.array([0.5, 0.5]), np.eye(2), cost=cost)


@pytest.mark.parametrize("utility", [np.zeros((0, 2)), np.ones(2), np.ones((2, 3)),
                                    np.array([[np.inf, 0.]])])
def test_invalid_utilities(utility):
    with pytest.raises(ValueError, match="utilities"):
        value_of_information(np.eye(2), np.array([0.5, 0.5]), utility)


def test_invalid_channels_and_prior():
    with pytest.raises(ValueError, match="hidden-state"):
        value_of_information(np.eye(3), np.array([0.5, 0.5]), np.eye(2))
    with pytest.raises(ValueError, match="sum to 1"):
        value_of_information(np.zeros((2, 2)), np.array([0.5, 0.5]), np.eye(2))
    with pytest.raises(ValueError, match="prior"):
        value_of_information(np.eye(2), np.array([0.5, np.nan]), np.eye(2))


def test_finite_input_with_unrepresentable_gain_is_rejected():
    utilities = np.full((20, 20), -1e308)
    np.fill_diagonal(utilities, 1e308)
    with pytest.raises(ValueError, match="floating-point range"):
        value_of_information(np.eye(20), np.full(20, 0.05), utilities)
