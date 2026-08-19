"""Multi-step policy planning — planning as EFE minimization (no mocks)."""

from __future__ import annotations

from itertools import product

import numpy as np
import pytest

from src.demos import (
    ACTIONS,
    BELIEF,
    PLANNING_HORIZON,
    PLANNING_PREFERENCES,
)
from src.policy_planning import (
    MultiStepSelection,
    enumerate_policies,
    evaluate_policy,
    select_multistep_policy,
)


# ---------------------------------------------------------------------------
# enumerate_policies
# ---------------------------------------------------------------------------


def test_enumerate_policies_counts_and_content():
    policies = enumerate_policies(2, 3)
    assert len(policies) == 8
    assert set(policies) == set(product(range(2), repeat=3))


@pytest.mark.parametrize("n_actions,horizon", [(0, 2), (2, 0), (-1, 2), (2, -1)])
def test_enumerate_policies_rejects_invalid(n_actions, horizon):
    with pytest.raises(ValueError):
        enumerate_policies(n_actions, horizon)


# ---------------------------------------------------------------------------
# evaluate_policy — analytic reference cross-checks
# ---------------------------------------------------------------------------


def test_horizon_one_matches_one_step_efe():
    """A length-1 policy must equal the one-step expected_free_energy."""
    from src.expected_free_energy import expected_free_energy

    cue = ACTIONS[0]
    ev = evaluate_policy(ACTIONS, BELIEF, PLANNING_PREFERENCES, (0,))
    assert ev.pragmatic + ev.epistemic == pytest.approx(
        expected_free_energy(cue, BELIEF, PLANNING_PREFERENCES) * -1.0
    )
    assert ev.efe == pytest.approx(
        expected_free_energy(cue, BELIEF, PLANNING_PREFERENCES)
    )


def test_epistemic_equals_mutual_information_identity():
    """KL[q(s|o_{1:T}) || q(s)] averaged over branches == I(s; o_{1:T})."""
    models = ACTIONS
    q0 = BELIEF
    n_outcomes = models[0].shape[0]
    horizon = PLANNING_HORIZON
    # brute-force mutual information between state and outcome sequence
    joint = np.zeros((n_outcomes**horizon, len(q0)))
    branch_probs = np.zeros(n_outcomes**horizon)
    k = 0
    for branch in product(range(n_outcomes), repeat=horizon):
        q = q0.copy()
        p_branch = 1.0
        for t, o in enumerate(branch):
            a = models[t % len(models)]  # alternating policies exercise mixing
            q_o = float(a[o] @ q)
            if q_o <= 0.0:
                p_branch = 0.0
                break
            p_branch *= q_o
            q = (a[o] * q) / q_o
        branch_probs[k] = p_branch
        joint[k] = q * p_branch
        k += 1
    # I = sum over branches, states of q(branch, s) ln( q(branch,s) / (q(branch) q(s)) )
    total = 0.0
    for i, p_b in enumerate(branch_probs):
        if p_b <= 0.0:
            continue
        for s in range(len(q0)):
            p_joint = joint[i, s]
            if p_joint <= 0.0:
                continue
            total += p_joint * np.log(p_joint / (p_b * q0[s]))
    # Now find an alternating policy evaluation and compare epistemic term
    ev = evaluate_policy(models, q0, PLANNING_PREFERENCES, (0, 1) * (horizon // 2))
    assert ev.epistemic == pytest.approx(total, abs=1e-12)


def test_repeated_uninformative_action_has_zero_epistemic():
    """A policy of only the uninformative 'bet' resolves no uncertainty."""
    bet_idx = 1
    ev = evaluate_policy(
        ACTIONS, BELIEF, PLANNING_PREFERENCES, (bet_idx,) * PLANNING_HORIZON
    )
    assert ev.epistemic == pytest.approx(0.0, abs=1e-12)


def test_branch_probabilities_sum_to_one():
    ev = evaluate_policy(ACTIONS, BELIEF, PLANNING_PREFERENCES, (0, 1))
    assert ev.branch_probabilities.sum() == pytest.approx(1.0, abs=1e-12)


def test_pragmatic_uses_only_final_outcome():
    """A pure-noise first step cannot change the terminal payoff expectation:
    pragmatic of (noise, a) equals the one-step E_{q(o|a)}[ln c(o)] from the
    prior — only the *final* action enters the payoff."""
    from src.expected_free_energy import pragmatic_value

    noise = np.full((2, 2), 0.5)
    models = [noise, ACTIONS[0]]  # index 0 = noise, index 1 = cue
    ev = evaluate_policy(models, BELIEF, PLANNING_PREFERENCES, (0, 1))
    reference = pragmatic_value(ACTIONS[0], BELIEF, PLANNING_PREFERENCES)
    assert ev.pragmatic == pytest.approx(reference, abs=1e-12)


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------


def test_empty_policy_rejected():
    with pytest.raises(ValueError):
        evaluate_policy(ACTIONS, BELIEF, PLANNING_PREFERENCES, ())


def test_unknown_action_rejected():
    with pytest.raises(ValueError):
        evaluate_policy(ACTIONS, BELIEF, PLANNING_PREFERENCES, (0, 7))


def test_zero_preference_rejected():
    prefs = np.array([1.0, 0.0])
    with pytest.raises(ValueError):
        evaluate_policy(ACTIONS, BELIEF, prefs, (0,))


def test_empty_models_rejected():
    with pytest.raises(ValueError):
        evaluate_policy([], BELIEF, PLANNING_PREFERENCES, (0,))


def test_mismatched_shapes_rejected():
    with pytest.raises(ValueError):
        evaluate_policy(
            [ACTIONS[0], np.ones((3, 2)) / 2.0], BELIEF, PLANNING_PREFERENCES, (0,)
        )


# ---------------------------------------------------------------------------
# select_multistep_policy — the planning demo
# ---------------------------------------------------------------------------


def test_planning_selects_look_then_leap_over_short_horizon():
    """The demo: cue-first then wager beats wager-first; 'look before leaping'
    emerges from EFE minimization over sequences, not as an extra rule."""
    sel = select_multistep_policy(
        ACTIONS, BELIEF, PLANNING_PREFERENCES, PLANNING_HORIZON
    )
    assert isinstance(sel, MultiStepSelection)
    # policies are tuples of action indices
    assert all(isinstance(p, tuple) for p in sel.policies)
    # chosen policy starts with the informative action
    chosen = sel.policies[sel.choice]
    assert chosen[0] == 0  # cue first
    # EFE ordering: chosen is argmin
    assert sel.efe[sel.choice] == pytest.approx(sel.efe.min())
    # and the pure-exploit sequence is strictly worse
    exploit = sel.policies.index((1,) * PLANNING_HORIZON)
    assert sel.efe[sel.choice] < sel.efe[exploit]


def test_select_returns_consistent_decomposition():
    sel = select_multistep_policy(
        ACTIONS, BELIEF, PLANNING_PREFERENCES, PLANNING_HORIZON
    )
    assert sel.efe == pytest.approx(-(sel.pragmatic + sel.epistemic))


def test_horizon_two_equal_policies_to_one_step_when_actions_uninformative():
    """With a completely uninformative action set, longer horizons add no
    epistemic value: G stays at the pragmatic floor."""
    uninformative = [np.array([[0.5, 0.5], [0.5, 0.5]])]
    sel1 = select_multistep_policy(uninformative, BELIEF, PLANNING_PREFERENCES, 1)
    sel2 = select_multistep_policy(uninformative, BELIEF, PLANNING_PREFERENCES, 3)
    assert sel2.epistemic.min() == pytest.approx(0.0, abs=1e-12)
    assert sel2.pragmatic.min() == pytest.approx(sel1.pragmatic.min(), abs=1e-12)


def test_evaluation_dataclass_is_frozen():
    ev = evaluate_policy(ACTIONS, BELIEF, PLANNING_PREFERENCES, (0,))
    with pytest.raises(Exception):
        ev.efe = 1.0  # type: ignore[misc]
