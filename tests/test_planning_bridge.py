"""Compare history-carrier EFE with exact terminal/history enumeration."""

import math
import numpy as np
import pytest

from src.demos import ACTIONS, BELIEF, SHARP_PREFERENCES
from src.planning_bridge import two_step_history_efe
from src.policy_planning import evaluate_policy


@pytest.mark.parametrize("policy", [(0, 0), (0, 1), (1, 0), (1, 1)])
def test_history_carrier_matches_terminal_history_objective(policy):
    result = two_step_history_efe(
        ACTIONS[policy[0]], ACTIONS[policy[1]], BELIEF, SHARP_PREFERENCES
    )
    direct = evaluate_policy(ACTIONS, BELIEF, SHARP_PREFERENCES, policy)
    assert result.terminal_history_efe == pytest.approx(direct.efe)
    assert result.history_efe == pytest.approx(direct.efe + math.log(2))
    np.testing.assert_allclose(result.likelihood.sum(axis=0), [1, 1])
    assert result.preferences.sum() == pytest.approx(1)


def test_impossible_history_rows_are_permitted():
    eye = np.eye(2)
    result = two_step_history_efe(eye, eye, BELIEF, np.array([0.5, 0.5]))
    np.testing.assert_array_equal(result.likelihood[[1, 2]], [[0, 0], [0, 0]])
    assert result.terminal_history_efe == pytest.approx(0, abs=1e-12)


def test_uninformative_repetition_is_not_cumulative_pragmatic_cost():
    coin = np.full((2, 2), 0.5)
    result = two_step_history_efe(coin, coin, BELIEF, np.array([0.5, 0.5]))
    assert result.terminal_history_efe == pytest.approx(math.log(2))
    assert result.history_efe == pytest.approx(2 * math.log(2))


@pytest.mark.parametrize(
    "first,second,pref",
    [
        (np.eye(2), np.eye(3), np.array([0.5, 0.5])),
        (np.eye(2), np.eye(2), np.array([1.0])),
        (np.eye(2), np.eye(2), np.array([1.0, 0.0])),
    ],
)
def test_bridge_rejects_invalid_shapes_and_support(first, second, pref):
    with pytest.raises(ValueError):
        two_step_history_efe(first, second, BELIEF, pref)
