"""Real closed-loop branches and deliberately uninformative negative control."""

from dataclasses import replace

import numpy as np
import pytest

from src.synthetic_agent import run_agent, synthetic_agent_demo, synthetic_environment


@pytest.mark.parametrize("observation", [0, 1])
def test_exact_cue_drives_rewarded_commitment(observation):
    environment = synthetic_environment()
    result = run_agent(environment, observation)
    assert result.initial.choice == 0
    assert result.observation_probability == pytest.approx(0.5)
    np.testing.assert_allclose(result.initial.epistemic, np.full(3, np.log(2)))
    np.testing.assert_allclose(result.initial.efe, [
        -np.log(0.2) - np.log(2),
        -0.5 * np.log(0.59 * 0.01) - np.log(2),
        -0.5 * np.log(0.59 * 0.01) - np.log(2),
    ])
    expected_posterior = np.eye(2)[observation]
    np.testing.assert_array_equal(result.posterior, expected_posterior)
    assert result.baseline_commitment.choice == 0
    assert result.commitment.choice == observation
    selected_law = environment.commitment_models[result.commitment.choice]
    np.testing.assert_array_equal(selected_law @ result.posterior, [0, 0, 1, 0])
    assert result.commitment.efe[observation] == pytest.approx(-np.log(0.59))
    np.testing.assert_allclose(result.commitment.epistemic, [0, 0])


def test_default_demo_changes_downstream_decision():
    result = synthetic_agent_demo()
    assert result.observation == 1
    assert result.baseline_commitment.choice != result.commitment.choice


@pytest.mark.parametrize("observation", [0, 1])
def test_uninformative_counterexample_preserves_prior_and_decision(observation):
    result = synthetic_agent_demo(observation, informative=False)
    assert result.initial.choice == 0
    assert result.initial.epistemic[0] == pytest.approx(0)
    assert result.observation_probability == pytest.approx(0.5)
    np.testing.assert_array_equal(result.posterior, [0.5, 0.5])
    assert result.commitment.choice == result.baseline_commitment.choice == 0
    np.testing.assert_allclose(result.commitment.efe, result.baseline_commitment.efe)


@pytest.mark.parametrize("observation", [-1, 4, True, np.bool_(True), 0.5, 2])
def test_invalid_or_impossible_observation(observation):
    with pytest.raises(ValueError, match="obs|evidence"):
        synthetic_agent_demo(observation)


def test_numpy_integer_observation():
    assert synthetic_agent_demo(np.int64(1)).commitment.choice == 1


@pytest.mark.parametrize("informative", [0, None, 'yes'])
def test_factory_rejects_nonboolean_mode(informative):
    with pytest.raises(ValueError, match="boolean"):
        synthetic_environment(informative=informative)


@pytest.mark.parametrize("field", ['initial_models', 'commitment_models'])
def test_empty_actions_rejected(field):
    with pytest.raises(ValueError, match="non-empty"):
        run_agent(replace(synthetic_environment(), **{field: ()}), 0)


def test_incompatible_commitment_states_rejected():
    environment = synthetic_environment()
    bad = replace(environment, commitment_models=(np.ones((4, 1)) / 4,))
    with pytest.raises(ValueError, match="states"):
        run_agent(bad, 0)


def test_invalid_preferences_rejected():
    bad = replace(synthetic_environment(), preferences=np.array([0., 0., 1., 0.]))
    with pytest.raises(ValueError, match="strictly positive"):
        run_agent(bad, 0)
