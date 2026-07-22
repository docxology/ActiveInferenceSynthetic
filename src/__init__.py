"""Active Inference -- A Synthetic Overview: project source.

This package holds the small, fully-tested numerical core behind the
overview's figures and demonstrations. Two complementary cores make the
overview's thesis — *one currency, two directions* — concrete:

* :mod:`src.free_energy_flow` encodes the Helmholtz decomposition of
  steady-state flow used in Bayesian mechanics — the basis of the equilibrium
  vs far-from-equilibrium figure in the extended abstract.
* :mod:`src.generative_model` encodes perception as variational-free-energy
  minimization over a discrete generative model — showing that the belief
  minimizing free energy *is* the Bayesian posterior, and that free energy is
  a tight upper bound on surprise.
* :mod:`src.trajectories` integrates the Bayesian-mechanics flow into worked
  equilibrium and non-equilibrium trajectories, quantifying the persistent
  probability current that distinguishes living systems.
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
    obeys_detailed_balance,
    solenoidal_is_conservative,
)
from .generative_model import (
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
    # free_energy_flow
    "free_energy",
    "grad_free_energy",
    "flow_field",
    "solenoidal_is_conservative",
    "obeys_detailed_balance",
    # generative_model
    "joint",
    "evidence",
    "surprise",
    "posterior",
    "variational_free_energy",
    "vfe_components",
    "minimize_free_energy",
    # trajectories
    "integrate_trajectory",
    "free_energy_along",
    "net_rotation",
    # expected_free_energy
    "predicted_outcomes",
    "predicted_posteriors",
    "pragmatic_value",
    "epistemic_value",
    "expected_free_energy",
    "select_policy",
    # markov_blanket
    "conditional_covariance",
    "partial_correlation",
    "correlation_matrix",
    "covariance_from_precision",
    "is_markov_blanket",
    # steady_state
    "drift_matrix",
    "stationary_covariance",
    "probability_current",
    "entropy_production_rate",
    "current_circulation",
]
