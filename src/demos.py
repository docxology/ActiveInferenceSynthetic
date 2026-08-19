"""Shared demonstration parameters for figures and tests."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .ou_model import IsotropicOU

# Flow / landscape parameters (overview, steady-state, trajectories).
FLOW = IsotropicOU(precision=1.0, gamma=1.0, omega=0.0)
OMEGA_NESS = 2.4
TRAJECTORY_OMEGA_NESS = 2.4
TRAJECTORY_START = (2.6, 0.0)
TRAJECTORY_DT = 0.002
TRAJECTORY_STEPS = 6000

# Discrete generative model (belief-update figure).
PRIOR: NDArray[np.float64] = np.array([0.6, 0.4])
LIKELIHOOD: NDArray[np.float64] = np.array([[0.9, 0.2], [0.1, 0.8]])
BELIEF_OBS = 0
BELIEF_LEARNING_RATE = 0.3
BELIEF_STEPS = 60

# Expected free energy (explore/exploit figure).
BELIEF: NDArray[np.float64] = np.array([0.5, 0.5])
CUE: NDArray[np.float64] = np.array([[0.9, 0.1], [0.1, 0.9]])
BET: NDArray[np.float64] = np.array([[0.85, 0.85], [0.15, 0.15]])
ACTIONS = [CUE, BET]
FLAT_PREFERENCES: NDArray[np.float64] = np.array([0.5, 0.5])
SHARP_PREFERENCES: NDArray[np.float64] = np.array([0.9, 0.1])

# Multi-step planning (policy-sequence EFE figure).
#: Planning horizon: two steps — look, then leap.
PLANNING_HORIZON = 2
#: Terminal preferences for the planning demo (same sharp preferences under
#: which the *one-step* rule exploits — the sequencing is what flips it).
PLANNING_PREFERENCES: NDArray[np.float64] = SHARP_PREFERENCES

# Markov blanket (4-variable Gaussian).
BLANKET_PRECISION: NDArray[np.float64] = np.array(
    [
        [2.5, -0.8, -0.4, 0.0],
        [-0.8, 2.5, -0.5, -0.7],
        [-0.4, -0.5, 2.5, -0.6],
        [0.0, -0.7, -0.6, 2.5],
    ]
)
BLANKET_ETA_IDX = 0
BLANKET_MU_IDX = 3
BLANKET_GIVEN_IDX = [1, 2]
