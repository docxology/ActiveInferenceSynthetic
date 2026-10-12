"""Analytic and invalid-input checks for the finite hierarchy."""

import numpy as np
import pytest

from src.hierarchical_model import hierarchical_demo, infer_hierarchy


@pytest.mark.parametrize("observation", [0, 1])
def test_hierarchy_matches_enumerated_joint(observation):
    result = hierarchical_demo(observation)
    reference = np.empty((2, 2, 2))
    for o in range(2):
        for s in range(2):
            for c in range(2):
                reference[o, s, c] = (
                    [0.6, 0.4][c] * [[0.8, 0.2], [0.2, 0.8]][s][c]
                    * [[0.9, 0.3], [0.1, 0.7]][o][s]
                )
    np.testing.assert_allclose(result.joint, reference)
    np.testing.assert_allclose(result.predicted_states, [0.56, 0.44])
    np.testing.assert_allclose(result.predicted_observations, [0.636, 0.364])
    assert result.joint.sum() == pytest.approx(1)
    assert result.evidence == pytest.approx(reference[observation].sum())
    expected = reference[observation] / reference[observation].sum()
    np.testing.assert_allclose(result.posterior_joint, expected)
    np.testing.assert_allclose(result.posterior_contexts, expected.sum(axis=0))
    np.testing.assert_allclose(result.posterior_states, expected.sum(axis=1))


def test_uninformative_observation_cannot_update_context_or_state():
    result = infer_hierarchy(np.array([0.6, 0.4]), np.eye(2), np.full((2, 2), 0.5), 0)
    np.testing.assert_allclose(result.posterior_contexts, [0.6, 0.4])
    np.testing.assert_allclose(result.posterior_states, result.predicted_states)


@pytest.mark.parametrize("observation", [-1, 2, True, np.bool_(False), 0.5])
def test_invalid_observation(observation):
    with pytest.raises(ValueError, match="observation"):
        hierarchical_demo(observation)


def test_numpy_integer_observation():
    assert hierarchical_demo(np.int64(0)).evidence == pytest.approx(0.636)


@pytest.mark.parametrize(
    "prior,states,likelihood,message",
    [
        ([0.5, 0.5], [[1]], [[1]], "context count"),
        ([1], [[1]], np.eye(2), "state count"),
        ([1], [[1]], [[0], [1]], "zero evidence"),
        ([float('nan')], [[1]], [[1]], "finite"),
        ([1], [[0.5]], [[1]], "sum to 1"),
        ([1], [[1]], [[-0.1], [1.1]], "non-negative"),
        ([[1]], [[1]], [[1]], "1-D"),
        ([1], [1], [[1]], "2-D"),
    ],
)
def test_invalid_hierarchy(prior, states, likelihood, message):
    with pytest.raises(ValueError, match=message):
        infer_hierarchy(np.array(prior), np.array(states), np.array(likelihood), 0)
