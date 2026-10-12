# A Closed-Loop Synthetic Agent {#sec:synthetic-agent}

The previous examples separate inference and policy scoring. Here one finite
agent connects them: predict observations, select an action by one-step EFE,
receive a cue, update its belief by Bayes' rule, and choose a subsequent
commitment. The hidden context is left or right and remains fixed during the
episode. The outcome alphabet distinguishes cue-left, cue-right, reward, and
loss. Action-conditioned likelihoods and positive outcome preferences are
explicit in `src/synthetic_agent.py`.

The initial action set is cue, left, and right. The cue minimizes the initial
EFE, with value {{AGENT_CUE_EFE}}. A cue-right observation has predictive
probability {{AGENT_CUE_PROBABILITY}} and gives posterior right-context mass
{{AGENT_POSTERIOR_RIGHT}}. The second-stage action set is explicitly restricted
to left and right: information gathering has finished, and the agent must
commit. Its right-action EFE is {{AGENT_COMMIT_RIGHT_EFE}}, compared with
{{AGENT_COMMIT_LEFT_EFE}} for left. Cue-left gives the opposite decision.
These are observation-contingent commitments, not a fixed action sequence.

The matched counterexample replaces the cue with a context-independent coin.
An observed cue-right label then leaves right-context mass at
{{AGENT_CONTROL_RIGHT}}. The commitment scores tie, and the declared deterministic
first-index tie rule selects left for either cue label. The label alone does
not convey information: its state-dependent likelihood does. The tests check
both real informative branches, the uninformative branch, impossible evidence,
invalid indices, and normalization.

This is a deliberately small synthetic agent, with a supplied observation
whose likelihood is checked against its environment model. The episode includes
inference and an observation-sensitive next action. It does not learn its
likelihood, discover its preferences, solve an arbitrary partially observed
control problem, or establish empirical intelligence. EFE and policy support
still depend on the stated model [@parr2022active].

![**Observation changes the next decision.** Informative cue-left and cue-right
produce different posterior beliefs and opposite commitments. Replacing the cue
with a state-independent coin leaves the prior unchanged and fails to produce
an observation-sensitive commitment. Every panel comes from the same exact
finite inference and action-selection core.](../output/figures/synthetic_agent.png){#fig:agent width=94%}
