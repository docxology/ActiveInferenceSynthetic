"""A finite, deterministic perception-action loop with state-dependent reward.

The initial stage allows cue/left/right; the final stage requires a left/right
commitment. Hidden context is fixed throughout. An observation is supplied
explicitly, so every possible branch can be reproduced without sampling. This
is a two-stage educational agent, not a learned or autonomous general agent.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .expected_free_energy import PolicySelection, select_policy
from .generative_model import evidence, posterior


@dataclass(frozen=True)
class SyntheticEnvironment:
    """Shared outcomes and hidden states for initial and commitment action models."""

    prior: NDArray[np.float64]
    preferences: NDArray[np.float64]
    initial_models: tuple[NDArray[np.float64], ...]
    commitment_models: tuple[NDArray[np.float64], ...]


@dataclass(frozen=True)
class AgentEpisode:
    """Two EFE decisions separated by one actual Bayesian observation update."""

    initial: PolicySelection
    observation: int
    observation_probability: float
    posterior: NDArray[np.float64]
    baseline_commitment: PolicySelection
    commitment: PolicySelection


def run_agent(environment: SyntheticEnvironment, observation: int) -> AgentEpisode:
    """Select an initial action, condition on its observation, then commit.

    Commitment indices refer to ``commitment_models``. The baseline commitment
    uses the unchanged prior, making observation-dependent decisions explicit.
    All actions must share the same outcome and hidden-state spaces.
    """
    initial = select_policy(list(environment.initial_models), environment.prior, environment.preferences)
    baseline = select_policy(
        list(environment.commitment_models), environment.prior, environment.preferences
    )
    if isinstance(observation, (bool, np.bool_)) or not isinstance(observation, (int, np.integer)):
        raise ValueError("observation must be an integer index")
    selected = environment.initial_models[initial.choice]
    updated = posterior(selected, environment.prior, observation)
    probability = evidence(selected, environment.prior, observation)
    commitment = select_policy(list(environment.commitment_models), updated, environment.preferences)
    return AgentEpisode(initial, int(observation), probability, updated, baseline, commitment)


def synthetic_environment(*, informative: bool = True) -> SyntheticEnvironment:
    """Cue/left/right model with outcomes (cue-left, cue-right, reward, loss).

    Contexts are (reward-left, reward-right). The informative cue reveals context
    exactly; the counterexample cue is an independent fair coin. Left/right
    deliver reward exactly in the matching context. EFE breaks ties by index.
    """
    if not isinstance(informative, bool):
        raise ValueError("informative must be a boolean")
    cue = np.zeros((4, 2), dtype=np.float64)
    cue[:2] = np.eye(2) if informative else np.full((2, 2), 0.5)
    left = np.array([[0., 0.], [0., 0.], [1., 0.], [0., 1.]])
    right = np.array([[0., 0.], [0., 0.], [0., 1.], [1., 0.]])
    return SyntheticEnvironment(
        prior=np.array([0.5, 0.5]),
        preferences=np.array([0.2, 0.2, 0.59, 0.01]),
        initial_models=(cue, left, right),
        commitment_models=(left, right),
    )


def synthetic_agent_demo(observation: int = 1, *, informative: bool = True) -> AgentEpisode:
    """Reproduce one branch; default cue-right changes commitment from left to right."""
    return run_agent(synthetic_environment(informative=informative), observation)
