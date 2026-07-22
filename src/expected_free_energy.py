r"""Expected free energy — action selection, and the explore/exploit balance.

:mod:`generative_model` shows *perception*: minimizing **variational** free
energy over beliefs about the present. This module shows *action*: minimizing
**expected** free energy over policies about the future. They are the two
directions of the one currency the overview is built around — inference tidies
beliefs to fit sensations; action chooses what to do so that future sensations
fit beliefs (and preferences).

Variational free energy $F$ scores a belief against a sensation *already had*.
Expected free energy $G$ scores a candidate action against the sensations it
*would* produce. For an action $a$, a current belief $q(s)$ over hidden states,
an outcome model $p(o \mid s, a)$, and preferences $p_{\text{pref}}(o)$ (a
distribution over outcomes the agent wants to encounter):

* the **predicted outcomes** are $q(o \mid a) = \sum_s p(o \mid s, a)\,q(s)$;
* the **predicted posteriors** are $q(s \mid o, a) \propto p(o \mid s, a)\,q(s)$.

$G$ decomposes into two values the agent seeks to *maximize* (so it minimizes
their negatives):

* **Pragmatic value** — $\mathbb{E}_{q(o\mid a)}[\ln p_{\text{pref}}(o)]$. How
  well the action's expected outcomes match what the agent prefers. This is
  extrinsic, goal-directed value: exploitation.
* **Epistemic value** — $\mathbb{E}_{q(o\mid a)}\!\big[\mathrm{KL}[q(s\mid o,a)
  \,\Vert\, q(s)]\big]$. The expected information the outcomes carry about the
  hidden state — equivalently the mutual information $I(s; o \mid a)$. This is
  intrinsic, curiosity value: exploration. It is always $\ge 0$.

$$
G(a) \;=\; -\underbrace{\mathbb{E}_{q(o\mid a)}[\ln p_{\text{pref}}(o)]}_{\text{pragmatic}}
\;-\; \underbrace{I(s; o \mid a)}_{\text{epistemic}}.
$$

The chosen policy is $\arg\min_a G(a)$. Because $G$ carries *both* terms, the
same rule that chases reward also chases information: when preferences are flat
the epistemic term dominates and the agent explores; when preferences are sharp
the pragmatic term dominates and it exploits. The explore/exploit trade-off is
not bolted on — it falls out of one quantity.

This is the *extrinsic-value + epistemic-value* form of expected free energy
(Parr, Pezzulo & Friston). It is algebraically equivalent to the dual *risk +
ambiguity* decomposition; this module uses the former throughout and does not
mix the two. The epistemic term equals the mutual information $I(s; o \mid a)$
*because* ``predicted_posteriors`` computes $q(s\mid o,a)$ by Bayes inversion of
the same generative model — a fact the tests cross-check against an
independently computed $I(s;o\mid a)$.

Everything is analytic and deterministic — no RNG, no fitting.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

__all__ = [
    "predicted_outcomes",
    "predicted_posteriors",
    "pragmatic_value",
    "epistemic_value",
    "expected_free_energy",
    "select_policy",
]

_TOL = 1e-9


def _as_vector(p: NDArray[np.float64] | list[float], name: str) -> NDArray[np.float64]:
    arr = np.asarray(p, dtype=np.float64)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be 1-D, got shape {arr.shape}")
    return arr


def _check_distribution(p: NDArray[np.float64], name: str) -> NDArray[np.float64]:
    if not np.all(np.isfinite(p)):
        raise ValueError(f"{name} must be finite (no NaN/inf), got {p}")
    if np.any(p < -_TOL):
        raise ValueError(f"{name} must be non-negative, got {p}")
    total = float(p.sum())
    if abs(total - 1.0) > 1e-8:
        raise ValueError(f"{name} must sum to 1, got {total}")
    return np.clip(p, 0.0, None)


def _check_outcome_model(a: NDArray[np.float64]) -> NDArray[np.float64]:
    """Validate an ``O × K`` outcome model ``p(o | s, a)`` (columns sum to 1)."""
    arr = np.asarray(a, dtype=np.float64)
    if arr.ndim != 2:
        raise ValueError(f"outcome_model must be 2-D (O x K), got shape {arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError("outcome_model must be finite (no NaN/inf)")
    if np.any(arr < -_TOL):
        raise ValueError("outcome_model must be non-negative")
    col_sums = arr.sum(axis=0)
    if not np.allclose(col_sums, 1.0, atol=1e-8):
        raise ValueError(
            f"each outcome_model column p(o|s,a) must sum to 1, got {col_sums}"
        )
    return np.clip(arr, 0.0, None)


def _prepare(
    outcome_model: NDArray[np.float64],
    belief: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    a = _check_outcome_model(outcome_model)
    q = _check_distribution(_as_vector(belief, "belief"), "belief")
    if a.shape[1] != q.shape[0]:
        raise ValueError(
            f"outcome_model has {a.shape[1]} states but belief has {q.shape[0]}"
        )
    return a, q


def predicted_outcomes(
    outcome_model: NDArray[np.float64],
    belief: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Predictive outcome distribution ``q(o | a) = Σ_s p(o | s, a) q(s)``."""
    a, q = _prepare(outcome_model, belief)
    return a @ q


def predicted_posteriors(
    outcome_model: NDArray[np.float64],
    belief: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Bayesian posteriors ``q(s | o, a)`` for each possible outcome.

    Returns an ``O × K`` array whose row ``o`` is the belief over states the
    agent *would* hold if it observed outcome ``o`` after taking the action. A
    row for an outcome that cannot occur (``q(o | a) = 0``) is returned as the
    prior belief (it carries zero weight in every expectation).
    """
    a, q = _prepare(outcome_model, belief)
    joint = a * q  # O x K, joint p(o, s | a)
    q_o = joint.sum(axis=1, keepdims=True)  # O x 1
    posteriors = np.where(q_o > 0.0, joint / np.where(q_o > 0.0, q_o, 1.0), q)
    return posteriors


def pragmatic_value(
    outcome_model: NDArray[np.float64],
    belief: NDArray[np.float64],
    preferences: NDArray[np.float64],
) -> float:
    """Expected log preference ``E_{q(o|a)}[ln p_pref(o)]`` (extrinsic value).

    Higher means the action's expected outcomes better match what the agent
    prefers. ``preferences`` must be a strictly positive distribution over
    outcomes (a zero-preference outcome would give ``-inf`` cost).
    """
    a, q = _prepare(outcome_model, belief)
    c = _check_distribution(_as_vector(preferences, "preferences"), "preferences")
    if c.shape[0] != a.shape[0]:
        raise ValueError(f"preferences length {c.shape[0]} != outcomes {a.shape[0]}")
    if np.any(c <= 0.0):
        raise ValueError("preferences must be strictly positive (finite log)")
    q_o = a @ q
    return float(np.sum(q_o * np.log(c)))


def epistemic_value(
    outcome_model: NDArray[np.float64],
    belief: NDArray[np.float64],
) -> float:
    """Expected information gain ``E_{q(o|a)}[KL[q(s|o,a) ‖ q(s)]]`` (intrinsic).

    Equivalently the mutual information ``I(s; o | a)`` between hidden states
    and outcomes under the action — the expected reduction in uncertainty about
    the state. Always ``>= 0``; exactly ``0`` when outcomes are independent of
    the state (an uninformative action).
    """
    a, q = _prepare(outcome_model, belief)
    joint = a * q  # p(o, s | a)
    q_o = joint.sum(axis=1)  # p(o | a)
    info = 0.0
    for o in range(a.shape[0]):
        if q_o[o] <= 0.0:
            continue
        post = joint[o] / q_o[o]  # q(s | o, a)
        mask = post > 0.0
        info += float(q_o[o] * np.sum(post[mask] * (np.log(post[mask]) - np.log(q[mask]))))
    # Mutual information is provably >= 0; a tiny negative here is pure
    # floating-point roundoff (e.g. a near-uninformative action), so clamp it.
    # A grossly negative value would indicate a real bug and is left to surface.
    if -1e-9 < info < 0.0:
        info = 0.0
    return info


def expected_free_energy(
    outcome_model: NDArray[np.float64],
    belief: NDArray[np.float64],
    preferences: NDArray[np.float64],
) -> float:
    """Expected free energy ``G(a) = −(pragmatic + epistemic)``.

    The policy the agent selects is the one that minimizes this. Lower ``G``
    means outcomes that are both preferred (pragmatic) and informative
    (epistemic).
    """
    return -(
        pragmatic_value(outcome_model, belief, preferences)
        + epistemic_value(outcome_model, belief)
    )


def select_policy(
    outcome_models: list[NDArray[np.float64]],
    belief: NDArray[np.float64],
    preferences: NDArray[np.float64],
) -> dict[str, object]:
    """Choose the expected-free-energy-minimizing policy from a list of actions.

    Args:
        outcome_models: One ``O × K`` outcome model ``p(o | s, a)`` per action.
        belief: Current belief ``q(s)`` over hidden states.
        preferences: Strictly-positive preference distribution over outcomes.

    Returns:
        A dict with ``"choice"`` (index of the argmin-EFE action), ``"efe"``
        (per-action ``G``), ``"pragmatic"`` and ``"epistemic"`` (the per-action
        decomposition). Lower ``efe`` is better; ``choice`` is ``argmin(efe)``.

    Raises:
        ValueError: If ``outcome_models`` is empty or its members disagree on
            the outcome/state dimensions.
    """
    if len(outcome_models) == 0:
        raise ValueError("outcome_models must be non-empty")
    pragmatic = np.array(
        [pragmatic_value(m, belief, preferences) for m in outcome_models]
    )
    epistemic = np.array([epistemic_value(m, belief) for m in outcome_models])
    efe = -(pragmatic + epistemic)
    return {
        "choice": int(np.argmin(efe)),
        "efe": efe,
        "pragmatic": pragmatic,
        "epistemic": epistemic,
    }
