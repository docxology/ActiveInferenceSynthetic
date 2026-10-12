"""Normalized history-channel bridge for two-step terminal-preference planning."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from numpy.typing import NDArray

from ._prob import as_column_stochastic, as_distribution, as_prob_vector
from .expected_free_energy import expected_free_energy


@dataclass(frozen=True)
class HistoryEFE:
    """EFE on the history carrier and its explicit normalization correction."""

    history_efe: float
    terminal_history_efe: float
    normalization_offset: float
    likelihood: NDArray[np.float64]
    preferences: NDArray[np.float64]


def two_step_history_efe(
    first: NDArray[np.float64],
    second: NDArray[np.float64],
    belief: NDArray[np.float64],
    terminal_preferences: NDArray[np.float64],
) -> HistoryEFE:
    """Lift two static-state actions to one finite observation-history channel.

    Rows are lexicographic pairs (first outcome, terminal outcome). Conditional
    independence given the static state gives the product likelihood. A normalized
    preference on histories assigns C(o2)/O to every pair. The resulting one-step
    EFE is terminal pragmatic cost minus history mutual information plus log(O).
    For Boolean outcomes this is the carrier used by the local Lean adapter.
    """
    a = as_column_stochastic(first, "first")
    b = as_column_stochastic(second, "second")
    if a.shape != b.shape:
        raise ValueError("first and second must share an outcome/state shape")
    c = as_distribution(
        as_prob_vector(terminal_preferences, "preferences"), "preferences"
    )
    if c.shape[0] != a.shape[0]:
        raise ValueError("preferences must match the outcome dimension")
    if np.any(c <= 0):
        raise ValueError("preferences must be strictly positive")
    channel = (a[:, None, :] * b[None, :, :]).reshape(-1, a.shape[1])
    preference = np.tile(c, a.shape[0]) / a.shape[0]
    efe = expected_free_energy(channel, belief, preference)
    offset = math.log(a.shape[0])
    return HistoryEFE(efe, efe - offset, offset, channel, preference)
