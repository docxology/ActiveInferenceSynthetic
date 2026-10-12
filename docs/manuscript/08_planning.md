# Planning: Policies as Action Sequences {#sec:planning}

The one-step EFE example can be extended to a finite sequence of actions on a
static hidden state. The local algorithm enumerates every observation branch,
updates beliefs along that branch, and scores a declared terminal-preference
objective. It does not optimize a general feedback policy. With
$\pi=(a_1,\ldots,a_T)$, its branch law is

$$q(o_{1:T}\mid\pi)=\sum_x q(x)\prod_t p(o_t\mid x,a_t).$$ {#eq:predictive-history}

The score implemented in `src/policy_planning.py` is

$$G_{\mathrm{terminal}}(\pi)=-\mathbb E[\ln C(o_T)]-I(x;o_{1:T}\mid\pi).$$ {#eq:terminal-efe}

The score in [@eq:terminal-efe] uses the predictive history in [@eq:predictive-history].
Terminal pragmatic value is collected only at the last step. Epistemic value
is the expected sequential posterior KL gain, checked independently against
mutual information of the complete observation history. The two-step result
selects cue-then-bet at {{PLANNING_EFE_LOOK_THEN_LEAP}}, compared with
{{PLANNING_EFE_EXPLOIT_FIRST}} for bet-then-bet. Its information contribution is
{{PLANNING_EPISTEMIC_LOOK_THEN_LEAP}}.

The bet channel here is state-independent. Observing the cue does not improve
that fixed bet's reward distribution. Cue-then-bet wins through the objective's
information term while retaining the preferred terminal outcome law. Genuine
observation-adaptive commitment is demonstrated separately in [@sec:synthetic-agent]. Reading this
open-loop score as an instrumental advantage or a closed-loop control theorem
would exceed what the example computes.

## An explicit upstream carrier bridge

For Boolean observations, define one history outcome $(o_1,o_2)$ with product
likelihood and normalized preference $C_H(o_1,o_2)=C(o_2)/2$. Upstream one-step
EFE on that finite history carrier equals the local terminal/history objective
plus the constant $\ln 2$. The computed normalization offset is
{{HISTORY_NORMALIZATION_OFFSET}}, and the cue-then-bet history-channel score is
{{HISTORY_CHANNEL_EFE}}. The offset does not change the ranking of the same
policy set. `src/planning_bridge.py` tests the correspondence numerically;
`formal/ActiveInferenceFormal/Planning.lean` proves the exact finite-carrier
identity and predictive mass law.

This differs from repeatedly summing one-step EFE at every stage. A fair
uninformative two-step model has terminal preference cost $\ln 2$ but cumulative
preference cost $2\ln 2$. A repeated perfect observation resolves the static
state only once: history mutual information is $\ln 2$, not twice that value.
The native controls preserve these distinctions. The Lean identity is about its
explicit normalized carrier; it does not certify the floating-point branch
implementation or general policy-tree optimization.

![**Finite sequence scoring.** The four two-step sequences share a static hidden
state. Cue-then-bet minimizes the declared terminal-preference minus history-information
objective. The bet remains state-independent; the advantage is information
scoring, not an observation-conditioned improvement in its payout.](../output/figures/policy_planning.png){#fig:planning width=94%}
