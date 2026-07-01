"""Active Inference -- A Synthetic Overview: project source.

This package holds the small, fully-tested numerical core behind the
overview's figures and demonstrations. The first such core is
:mod:`src.free_energy_flow`, which encodes the Helmholtz decomposition of
steady-state flow used in Bayesian mechanics — the basis of the equilibrium
vs far-from-equilibrium figure in the extended abstract.
"""

from .free_energy_flow import (
    flow_field,
    free_energy,
    grad_free_energy,
    obeys_detailed_balance,
    solenoidal_is_conservative,
)

__all__ = [
    "free_energy",
    "grad_free_energy",
    "flow_field",
    "solenoidal_is_conservative",
    "obeys_detailed_balance",
]
