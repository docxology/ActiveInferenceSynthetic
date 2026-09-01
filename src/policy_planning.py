r"""Multi-step policies — planning as expected-free-energy minimization.

:mod:`expected_free_energy` scores *one* action against the sensations it
would produce. This module extends the same currency to *policies* — short
sequences of actions — so that the agent can plan: choose now the action whose
value lies in what it makes possible later.

Model
-----
The hidden state is static across the (short) horizon: an unknown context that
does not change while the agent acts. Each action ``a`` has an outcome model
``p(o | s, a)``. A policy ``π = (a_1, …, a_T)`` induces a distribution over
outcome sequences ``q(o_{1:T} | π)``: outcomes are generated independently
given the state, so a branch ``(o_1, …, o_T)`` has probability

$$
q(o_{1:T} \mid \pi) \;=\; \sum_s q(s)\, \prod_{t} p(o_t \mid s, a_t),
$$

and the belief along the branch evolves by exact Bayes rule,
``q_{t+1}(s) ∝ p(o_t | s, a_t) q_t(s)``.

Expected free energy of a policy
--------------------------------
Two terms, mirroring the one-step decomposition:

* **Pragmatic (terminal)** — the expected log preference of the *final*
  outcome only:
  $\mathbb{E}_{q(o_{1:T}|\pi)}[\ln p_{\text{pref}}(o_T)]$.
  Payoffs are collected at the end of the plan, which is what makes
  *sequencing* matter: an informative first action has no immediate payoff but
  sharpens the belief the final action is chosen under — along each branch.

* **Epistemic (cumulative)** — the expected total belief resolution:
  $\mathbb{E}_{q(o_{1:T}|\pi)}\big[\mathrm{KL}[\,q(s \mid o_{1:T})\, \Vert\, q(s)\,]\big]$.
  By the chain rule of relative entropy this equals the mutual information
  $I(s; o_{1:T} \mid \pi)$ — the tests cross-check exactly this identity.

$$
G(\pi) \;=\; -\,\mathbb{E}_{q(o_{1:T}\mid\pi)}\big[\ln p_{\text{pref}}(o_T)\big]
\;-\; I(s; o_{1:T} \mid \pi).
$$

The plan selected is $\arg\min_\pi G(\pi)$.

Because later-step quantities are evaluated *along each branch* and then
averaged, the nonlinearity of Bayes rule is preserved: the value of
information is real. A mixture belief would collapse
$\mathbb{E}[\text{posterior}]$ back to the prior and erase the value of
looking before leaping. Branch enumeration is exact — every branch of
$O^T$ outcomes is summed, no sampling, no RNG.

Everything is analytic and deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np
from numpy.typing import NDArray

from ._prob import as_column_stochastic, as_distribution, as_prob_vector, kl_divergence

__all__ = [
    "MultiStepSelection",
    "PolicyEvaluation",
    "enumerate_policies",
    "evaluate_policy",
    "select_multistep_policy",
]


@dataclass(frozen=True)
class PolicyEvaluation:
    """Decomposition of one action sequence."""

    policy: tuple[int, ...]
    efe: float
    pragmatic: float
    epistemic: float
    #: Probability of each non-impossible outcome branch, in the order those
    #: branches are enumerated (impossible branches are omitted, so the array
    #: can be shorter than ``n_outcomes ** horizon``).
    branch_probabilities: NDArray[np.float64]


@dataclass(frozen=True)
class MultiStepSelection:
    """Argmin-EFE choice over a fixed set of multi-step policies."""

    choice: int
    policies: list[tuple[int, ...]]
    efe: NDArray[np.float64]
    pragmatic: NDArray[np.float64]
    epistemic: NDArray[np.float64]


def enumerate_policies(n_actions: int, horizon: int) -> list[tuple[int, ...]]:
    """All action sequences of length ``horizon`` over ``n_actions`` actions."""
    if n_actions < 1:
        raise ValueError("n_actions must be >= 1")
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    return list(product(range(n_actions), repeat=horizon))


def _prepare_models(
    outcome_models: list[NDArray[np.float64]],
) -> list[NDArray[np.float64]]:
    if len(outcome_models) == 0:
        raise ValueError("outcome_models must be non-empty")
    models = [as_column_stochastic(m, "outcome_model") for m in outcome_models]
    shape = models[0].shape
    for m in models:
        if m.shape != shape:
            raise ValueError("outcome_models must share the same (O, K) shape")
    return models


def evaluate_policy(
    outcome_models: list[NDArray[np.float64]],
    belief: NDArray[np.float64],
    preferences: NDArray[np.float64],
    policy: tuple[int, ...],
) -> PolicyEvaluation:
    """Exact EFE decomposition of one action sequence.

    Args:
        outcome_models: One ``O × K`` column-stochastic model per action.
        belief: Prior belief ``q(s)`` over the static hidden state.
        preferences: Strictly-positive preference distribution over outcomes;
            applied to the *final* outcome of the sequence.
        policy: Sequence of action indices, one per time step.

    Returns:
        A :class:`PolicyEvaluation` with total ``efe = -(pragmatic +
        epistemic)``, the terminal pragmatic value, the cumulative epistemic
        value, and the branch outcome-sequence probabilities.

    Raises:
        ValueError: On empty inputs, shape disagreement, non-distribution
            inputs, zero-probability preferences, or unknown action indices.
    """
    models = _prepare_models(outcome_models)
    q0 = as_distribution(as_prob_vector(belief, "belief"), "belief")
    c = as_distribution(as_prob_vector(preferences, "preferences"), "preferences")
    if c.shape[0] != models[0].shape[0]:
        raise ValueError(
            f"preferences length {c.shape[0]} != outcomes {models[0].shape[0]}"
        )
    if np.any(c <= 0.0):
        raise ValueError("preferences must be strictly positive (finite log)")
    if not policy:
        raise ValueError("policy must be non-empty")
    if any(a < 0 or a >= len(models) for a in policy):
        raise ValueError("policy contains an unknown action index")

    n_outcomes = models[0].shape[0]
    horizon = len(policy)

    pragmatic = 0.0
    epistemic = 0.0
    branch_probs: list[float] = []
    for branch in product(range(n_outcomes), repeat=horizon):
        # Branch probability and posterior under the static-state model.
        q = q0
        log_branch = 0.0
        for t, outcome in enumerate(branch):
            action = models[policy[t]]
            q_o = float(action[outcome] @ q)
            if q_o <= 0.0:
                log_branch = -np.inf
                break
            log_branch += np.log(q_o)
            q = (action[outcome] * q) / q_o
        if log_branch == -np.inf:
            continue
        p_branch = float(np.exp(log_branch))
        branch_probs.append(p_branch)
        pragmatic += p_branch * float(np.log(c[branch[-1]]))
        epistemic += p_branch * kl_divergence(q, q0)

    # Mutual information is mathematically >= 0; snap away float round-off
    # noise so exact-zero-epistemic policies compare cleanly at machine precision.
    if -1e-9 < epistemic < 0.0:
        epistemic = 0.0
    return PolicyEvaluation(
        policy=tuple(policy),
        efe=float(-(pragmatic + epistemic)),
        pragmatic=float(pragmatic),
        epistemic=float(epistemic),
        branch_probabilities=np.array(branch_probs, dtype=np.float64),
    )


def select_multistep_policy(
    outcome_models: list[NDArray[np.float64]],
    belief: NDArray[np.float64],
    preferences: NDArray[np.float64],
    horizon: int,
) -> MultiStepSelection:
    """Choose the EFE-minimizing action sequence of the given horizon.

    Evaluates every policy in :func:`enumerate_policies` and returns the full
    decomposition; ``choice`` indexes ``policies`` and is ``argmin(efe)``.
    """
    models = _prepare_models(outcome_models)
    policies = enumerate_policies(len(models), horizon)
    evaluations = [evaluate_policy(models, belief, preferences, p) for p in policies]
    efe = np.array([e.efe for e in evaluations], dtype=np.float64)
    pragmatic = np.array([e.pragmatic for e in evaluations], dtype=np.float64)
    epistemic = np.array([e.epistemic for e in evaluations], dtype=np.float64)
    return MultiStepSelection(
        choice=int(np.argmin(efe)),
        policies=policies,
        efe=efe,
        pragmatic=pragmatic,
        epistemic=epistemic,
    )
