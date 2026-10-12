"""Active Inference -- A Synthetic Overview: project source.

Installed imports use ``active_inference_synthetic``; checkout scripts use
``src``. The Python package does not import ``fep_lean`` or ``gnn``. The
independent Lean layer imports pinned ``FepSketches`` modules through Lake.

This package holds the small, fully-tested numerical core behind the
overview's figures and demonstrations. The examples keep their mathematical
objects and interpretation boundaries distinct:

* :mod:`src.free_energy_flow` encodes the Helmholtz decomposition of
  steady-state flow used in Bayesian mechanics — the basis of the equilibrium
  vs far-from-equilibrium figure in the extended abstract.
* :mod:`src.generative_model` encodes perception as variational-free-energy
  minimization over a discrete generative model — showing that the belief
  minimizing free energy *is* the Bayesian posterior, and that free energy is
  a tight upper bound on surprise.
* :mod:`src.trajectories` integrates deterministic drift trajectories;
  ensemble probability current is calculated separately in the diffusion model.
* :mod:`src.expected_free_energy` extends the generative model to *action*:
  choosing policies by minimizing expected free energy, whose pragmatic and
  epistemic terms produce the explore/exploit balance.
* :mod:`src.markov_blanket` demonstrates the statistical boundary itself —
  internal and external states are marginally dependent but conditionally
  independent given the sensory/active blanket.
* :mod:`src.steady_state` quantifies the non-equilibrium steady state
  analytically — the stationary density, its probability current, and the
  entropy-production rate that is zero exactly at detailed balance.
"""

from .expected_free_energy import (
    PolicySelection,
    epistemic_value,
    expected_free_energy,
    pragmatic_value,
    predicted_outcomes,
    predicted_posteriors,
    select_policy,
)
from .free_energy_flow import (
    flow_field,
    free_energy,
    grad_free_energy,
    solenoidal_is_conservative,
)
from .generative_model import (
    BeliefDescent,
    evidence,
    joint,
    minimize_free_energy,
    posterior,
    surprise,
    variational_free_energy,
    vfe_components,
)
from .markov_blanket import (
    conditional_covariance,
    correlation_matrix,
    covariance_from_precision,
    is_markov_blanket,
    partial_correlation,
)
from .ou_model import IsotropicOU
from .value_of_information import DecisionValue, value_of_information
from .steady_state import (
    current_circulation,
    drift_matrix,
    entropy_production_rate,
    probability_current,
    stationary_covariance,
)
from .trajectories import (
    free_energy_along,
    integrate_trajectory,
    net_rotation,
)

__all__ = [
    "DecisionValue",
    "value_of_information",
    "BeliefDescent",
    "IsotropicOU",
    "PolicySelection",
    "conditional_covariance",
    "correlation_matrix",
    "covariance_from_precision",
    "current_circulation",
    "drift_matrix",
    "entropy_production_rate",
    "epistemic_value",
    "evidence",
    "expected_free_energy",
    "flow_field",
    "free_energy",
    "free_energy_along",
    "grad_free_energy",
    "integrate_trajectory",
    "is_markov_blanket",
    "joint",
    "minimize_free_energy",
    "net_rotation",
    "partial_correlation",
    "posterior",
    "pragmatic_value",
    "predicted_outcomes",
    "predicted_posteriors",
    "probability_current",
    "select_policy",
    "solenoidal_is_conservative",
    "stationary_covariance",
    "surprise",
    "variational_free_energy",
    "vfe_components",
]
