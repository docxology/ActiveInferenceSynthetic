"""Discrete generative model — perception as free-energy minimization.

This is the *inference* half of Active Inference, the complement to the
Bayesian-mechanics flow in :mod:`free_energy_flow`. Where that module shows the
thermodynamic descent of a system on its own free-energy landscape, this one
shows the epistemic content of that descent: **perception is approximate
Bayesian inference, carried out by minimizing variational free energy.**

The setup is the smallest thing that still says something true. A system holds
a categorical *generative model* of hidden states ``x`` and observations ``s``:

* a **prior** ``p(x)`` — a probability vector over ``K`` hidden states;
* a **likelihood** ``p(s | x)`` — an ``O × K`` matrix whose column ``x`` is the
  distribution over the ``O`` possible observations given state ``x``.

Together they define the joint ``p(s, x) = p(s | x) p(x)`` and the model
**evidence** ``p(s) = Σ_x p(s | x) p(x)``. The exact Bayesian **posterior** is
``p(x | s) = p(s, x) / p(s)``.

The load-bearing quantity is **variational free energy**. For any belief
``q(x)`` about the hidden state, given an observation ``s``:

    F[q] = E_q[ ln q(x) − ln p(s, x) ]
         = KL[ q(x) ‖ p(x) ]  −  E_q[ ln p(s | x) ]
           └── complexity ──┘    └──── accuracy ────┘

Two facts make this *applicable* rather than decorative, and both are asserted
to machine precision in the tests:

1. **F is an upper bound on surprise.** ``F[q] = −ln p(s) + KL[q ‖ p(x|s)] ≥
   −ln p(s)`` for every ``q``. Minimizing F over beliefs therefore minimizes an
   accessible bound on the (inaccessible) surprise ``−ln p(s)``.
2. **The bound is tight at the posterior.** ``F`` is minimized exactly when
   ``q = p(x | s)``, where it *equals* the surprise. So free-energy
   minimization **is** Bayesian inference — the belief that minimizes F is the
   posterior, and the minimized value is the surprise it bounds.

:func:`minimize_free_energy` makes the descent explicit: gradient descent on F
over the belief simplex (softmax parameterization) drives an arbitrary starting
belief *toward* the posterior while F falls monotonically toward the surprise —
a small step and enough iterations close the gap (the default ``steps=200``
lands within ~1e-5 of the posterior; ~500 steps reaches machine precision). That is
"perception lowers free energy by updating beliefs," shown rather than told.

Everything is analytic and deterministic — no RNG, no fitting.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from ._prob import as_column_stochastic, as_distribution, as_prob_vector, kl_divergence

__all__ = [
    "BeliefDescent",
    "evidence",
    "joint",
    "minimize_free_energy",
    "posterior",
    "surprise",
    "variational_free_energy",
    "vfe_components",
]


@dataclass(frozen=True)
class BeliefDescent:
    """Belief trajectory and free-energy values from gradient descent on VFE."""

    beliefs: NDArray[np.float64]
    free_energy: NDArray[np.float64]


def _prepare(
    likelihood: NDArray[np.float64],
    prior: NDArray[np.float64],
    obs: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Validate inputs and return ``(likelihood_row_for_obs, prior)``."""
    a = as_column_stochastic(likelihood, "likelihood")
    p = as_distribution(as_prob_vector(prior, "prior"), "prior")
    n_obs, n_states = a.shape
    if p.shape[0] != n_states:
        raise ValueError(
            f"prior length {p.shape[0]} != likelihood state count {n_states}"
        )
    if not isinstance(obs, (int, np.integer)) or not 0 <= int(obs) < n_obs:
        raise ValueError(f"obs must be an integer in [0, {n_obs}), got {obs!r}")
    return a[int(obs)], p


def joint(
    likelihood: NDArray[np.float64],
    prior: NDArray[np.float64],
    obs: int,
) -> NDArray[np.float64]:
    """Joint ``p(s, x) = p(s | x) p(x)`` for the observed ``s``, over states."""
    a_row, p = _prepare(likelihood, prior, obs)
    return a_row * p


def evidence(
    likelihood: NDArray[np.float64],
    prior: NDArray[np.float64],
    obs: int,
) -> float:
    """Model evidence (marginal likelihood) ``p(s) = Σ_x p(s | x) p(x)``."""
    return float(joint(likelihood, prior, obs).sum())


def surprise(
    likelihood: NDArray[np.float64],
    prior: NDArray[np.float64],
    obs: int,
) -> float:
    """Surprise ``−ln p(s)`` — the quantity variational free energy bounds."""
    p_s = evidence(likelihood, prior, obs)
    if p_s <= 0.0:
        raise ValueError("evidence p(s) is zero; observation impossible under model")
    return -float(np.log(p_s))


def posterior(
    likelihood: NDArray[np.float64],
    prior: NDArray[np.float64],
    obs: int,
) -> NDArray[np.float64]:
    """Exact Bayesian posterior ``p(x | s) = p(s, x) / p(s)``."""
    j = joint(likelihood, prior, obs)
    p_s = float(j.sum())
    if p_s <= 0.0:
        raise ValueError("evidence p(s) is zero; observation impossible under model")
    return j / p_s


def variational_free_energy(
    q: NDArray[np.float64],
    likelihood: NDArray[np.float64],
    prior: NDArray[np.float64],
    obs: int,
) -> float:
    """Variational free energy ``F[q] = E_q[ln q(x) − ln p(s, x)]``.

    Args:
        q: Belief over hidden states — a probability vector of length ``K``.
        likelihood: ``O × K`` likelihood ``p(s | x)``.
        prior: Prior ``p(x)`` of length ``K``.
        obs: Observed index ``s`` in ``[0, O)``.

    Returns:
        The (scalar) variational free energy of belief ``q`` under observation
        ``s``. Always ``>= surprise(...)``, with equality iff ``q`` is the
        posterior.
    """
    a_row, p = _prepare(likelihood, prior, obs)
    qv = as_distribution(as_prob_vector(q, "q"), "q")
    if qv.shape[0] != p.shape[0]:
        raise ValueError(f"q length {qv.shape[0]} != state count {p.shape[0]}")
    joint_x = a_row * p
    mask = qv > 0.0
    if np.any(joint_x[mask] <= 0.0):
        raise ValueError(
            "variational_free_energy: joint p(s, x) must be strictly positive "
            "where q > 0 (finite log)"
        )
    return float(np.sum(qv[mask] * (np.log(qv[mask]) - np.log(joint_x[mask]))))


def vfe_components(
    q: NDArray[np.float64],
    likelihood: NDArray[np.float64],
    prior: NDArray[np.float64],
    obs: int,
) -> tuple[float, float]:
    """Return ``(complexity, accuracy)`` with ``F = complexity − accuracy``.

    * **complexity** = ``KL[q ‖ prior]`` — how far belief moved from the prior.
    * **accuracy**   = ``E_q[ln p(s | x)]`` — how well the belief explains ``s``.

    Perception trades these off: it moves beliefs (paying complexity) only as
    far as the evidence (accuracy) warrants.
    """
    a_row, p = _prepare(likelihood, prior, obs)
    qv = as_distribution(as_prob_vector(q, "q"), "q")
    if qv.shape[0] != p.shape[0]:
        raise ValueError(f"q length {qv.shape[0]} != state count {p.shape[0]}")
    mask = qv > 0.0
    if np.any(a_row[mask] <= 0.0):
        raise ValueError(
            "vfe_components: likelihood p(s | x) must be strictly positive "
            "where q > 0 (finite log)"
        )
    complexity = kl_divergence(qv, p)
    accuracy = float(np.sum(qv[mask] * np.log(a_row[mask])))
    return complexity, accuracy


def minimize_free_energy(
    likelihood: NDArray[np.float64],
    prior: NDArray[np.float64],
    obs: int,
    *,
    learning_rate: float = 0.2,
    steps: int = 200,
    q_init: NDArray[np.float64] | None = None,
) -> BeliefDescent:
    """Descend variational free energy to the posterior — perception as optimization.

    Runs deterministic gradient descent on ``F`` over the belief simplex using a
    softmax parameterization ``q = softmax(z)``. The gradient has the closed
    form ``∂F/∂z_j = q_j (c_j − F)`` where ``c_x = ln q_x − ln p(s, x)`` is the
    pointwise free-energy density and ``E_q[c] = F``. The unique fixed point is
    the exact posterior, where every ``c_x`` equals the surprise and the
    gradient vanishes.

    Because ``F`` is convex in ``q`` (a KL divergence is convex), a
    *sufficiently small* step size gives monotone descent that converges to the
    unique posterior minimizer. The default ``learning_rate`` is small enough
    for the small models this overview uses; an overly large step can overshoot
    and is not guaranteed monotone (as for any explicit gradient scheme). This
    routine also requires the observed likelihood column ``p(s | x)`` to have
    full support (every state assigns nonzero probability to ``s``), so the
    log-joint is finite; a state that makes ``s`` impossible would give that
    belief infinite free energy and is rejected up front.

    Args:
        likelihood: ``O × K`` likelihood ``p(s | x)`` with a strictly positive
            observed column.
        prior: Prior ``p(x)``.
        obs: Observed index ``s``.
        learning_rate: Step size (``> 0``). Small values guarantee monotone
            descent; the default is safe for the models this overview uses.
        steps: Number of descent iterations (``>= 1``).
        q_init: Optional starting belief (probability vector). Defaults to the
            uniform belief — maximally uncommitted.

    Returns:
        A :class:`BeliefDescent` with ``beliefs`` (``(steps+1, K)`` array of
        the belief at each iteration) and ``free_energy`` (``(steps+1,)`` array
        of ``F`` at each iteration). ``beliefs[0]`` is ``q_init``;
        ``beliefs[-1]`` is the final learned belief — the posterior as ``steps`` grows
        (the default of 200 is within ~1e-5 of it; ~500 reaches machine precision).

    Raises:
        ValueError: If ``learning_rate <= 0``, ``steps < 1``, or the observed
            likelihood column has a zero entry (a state under which ``s`` is
            impossible).
    """
    if learning_rate <= 0.0:
        raise ValueError(f"learning_rate must be > 0, got {learning_rate}")
    if steps < 1:
        raise ValueError(f"steps must be >= 1, got {steps}")

    a_row, p = _prepare(likelihood, prior, obs)
    joint_x = a_row * p
    if np.any(joint_x <= 0.0):
        raise ValueError(
            "minimize_free_energy requires a strictly positive joint p(s, x) "
            "over all states (finite log-joint) — every state must have nonzero "
            f"prior and assign nonzero probability to obs={obs}; got joint {joint_x}"
        )
    log_joint = np.log(joint_x)
    n_states = p.shape[0]

    if q_init is None:
        q = np.full(n_states, 1.0 / n_states, dtype=np.float64)
    else:
        q = as_distribution(as_prob_vector(q_init, "q_init"), "q_init").copy()

    z = np.log(np.clip(q, 1e-300, None))
    beliefs = np.empty((steps + 1, n_states), dtype=np.float64)
    free_energy = np.empty(steps + 1, dtype=np.float64)

    def _softmax(logits: NDArray[np.float64]) -> NDArray[np.float64]:
        shifted = logits - logits.max()
        exps = np.exp(shifted)
        return exps / exps.sum()

    for t in range(steps + 1):
        q = _softmax(z)
        beliefs[t] = q
        density = np.log(q) - log_joint
        f = float(np.sum(q * density))
        free_energy[t] = f
        if t < steps:
            grad = q * (density - f)
            z = z - learning_rate * grad

    return BeliefDescent(beliefs=beliefs, free_energy=free_energy)
