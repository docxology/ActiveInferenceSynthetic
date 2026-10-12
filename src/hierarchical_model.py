"""Exact two-level categorical inference: context -> state -> observation.

This finite Bayesian hierarchy illustrates top-down prediction and bottom-up
conditioning; it makes no claim of neural implementation or approximate inference.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from ._prob import as_column_stochastic, as_distribution, as_prob_vector


@dataclass(frozen=True)
class HierarchicalUpdate:
    """Joint axes are (observation, state, context); posterior axes (state, context)."""

    joint: NDArray[np.float64]
    predicted_states: NDArray[np.float64]
    predicted_observations: NDArray[np.float64]
    evidence: float
    posterior_joint: NDArray[np.float64]
    posterior_states: NDArray[np.float64]
    posterior_contexts: NDArray[np.float64]


def infer_hierarchy(
    context_prior: NDArray[np.float64],
    state_given_context: NDArray[np.float64],
    observation_given_state: NDArray[np.float64],
    observation: int,
) -> HierarchicalUpdate:
    """Predict downward and condition both hidden levels on one observation.

    Columns of each conditional matrix are distributions. Impossible observed
    outcomes raise an error rather than returning an arbitrary posterior.
    """
    prior = as_distribution(as_prob_vector(context_prior, "context_prior"), "context_prior")
    states = as_column_stochastic(state_given_context, "state_given_context")
    likelihood = as_column_stochastic(observation_given_state, "observation_given_state")
    if states.shape[1] != prior.size:
        raise ValueError("state_given_context context count must match context_prior")
    if likelihood.shape[1] != states.shape[0]:
        raise ValueError("observation_given_state state count must match state_given_context")
    if isinstance(observation, (bool, np.bool_)) or not isinstance(observation, (int, np.integer)):
        raise ValueError("observation must be an integer index")
    if not 0 <= observation < likelihood.shape[0]:
        raise ValueError("observation index out of range")
    joint = likelihood[:, :, None] * states[None, :, :] * prior[None, None, :]
    predicted_states = states @ prior
    predicted_observations = joint.sum(axis=(1, 2))
    evidence = float(predicted_observations[observation])
    if evidence <= 0.0:
        raise ValueError("observation has zero evidence under the hierarchy")
    posterior_joint = joint[observation] / evidence
    return HierarchicalUpdate(
        joint=joint,
        predicted_states=predicted_states,
        predicted_observations=predicted_observations,
        evidence=evidence,
        posterior_joint=posterior_joint,
        posterior_states=posterior_joint.sum(axis=1),
        posterior_contexts=posterior_joint.sum(axis=0),
    )


def hierarchical_demo(observation: int = 0) -> HierarchicalUpdate:
    """Two contexts, two states, and a noisy binary observation; all laws explicit."""
    return infer_hierarchy(
        np.array([0.6, 0.4]),
        np.array([[0.8, 0.2], [0.2, 0.8]]),
        np.array([[0.9, 0.3], [0.1, 0.7]]),
        observation,
    )
