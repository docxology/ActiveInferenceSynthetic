"""Exact two-stage decision value of a finite observation channel.

Utilities use rows for commitment actions and columns for fixed hidden states.
Observation channels use rows for outcomes and columns for hidden states.
Gross value compares optimal feedback commitments with the best prior action;
net value additionally subtracts a declared acquisition cost in utility units.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from ._prob import as_column_stochastic, as_distribution, as_prob_vector
from .expected_free_energy import epistemic_value


@dataclass(frozen=True)
class DecisionValue:
    """Expected utilities, information, and a policy for reachable outcomes."""

    baseline_utility: float
    informed_utility: float
    gross_value: float
    net_value: float
    information_nats: float
    baseline_action: int
    feedback_actions: tuple[int | None, ...]
    outcome_probabilities: NDArray[np.float64]


def value_of_information(
    channel: NDArray[np.float64],
    prior: NDArray[np.float64],
    utilities: NDArray[np.float64],
    *,
    cost: float = 0.0,
) -> DecisionValue:
    """Enumerate reachable observations and optimize the subsequent commitment.

    The hidden state is static, the utility matrix is known, and observation
    acquisition does not itself change the state or available commitments.
    Ties choose the lowest action index. Unreachable outcomes have no posterior
    and receive ``None`` in the feedback policy, rather than fabricated beliefs.
    Probability roundoff admitted by the shared validators is normalized.
    """
    q = as_distribution(as_prob_vector(prior, "prior"), "prior")
    a = as_column_stochastic(channel, "channel")
    u = np.asarray(utilities, dtype=np.float64)
    if a.shape[1] != q.size:
        raise ValueError("channel hidden-state dimension must match prior")
    if u.ndim != 2 or u.shape[0] == 0 or u.shape[1] != q.size:
        raise ValueError("utilities must be nonempty actions by hidden states")
    if not np.all(np.isfinite(u)):
        raise ValueError("utilities must be finite")
    if (
        isinstance(cost, (bool, np.bool_))
        or not isinstance(cost, (int, float, np.integer, np.floating))
        or not np.isfinite(cost)
        or cost < 0
    ):
        raise ValueError("cost must be a finite nonnegative scalar")
    q = q / q.sum()
    a = a / a.sum(axis=0)
    values = u @ q
    baseline_action = int(np.argmax(values))
    baseline = float(values[baseline_action])
    probabilities = a @ q
    choices: list[int | None] = []
    informed = 0.0
    for row, probability in zip(a, probabilities, strict=True):
        if probability == 0:
            choices.append(None)
            continue
        conditional_values = u @ (row * q / probability)
        choice = int(np.argmax(conditional_values))
        choices.append(choice)
        informed += float(probability * conditional_values[choice])
    gain = informed - baseline
    net = gain - float(cost)
    if not np.all(np.isfinite([baseline, informed, gain, net])):
        raise ValueError("utility calculation exceeded finite floating-point range")
    return DecisionValue(
        baseline, informed, gain, net,
        epistemic_value(a, q), baseline_action, tuple(choices), probabilities,
    )
