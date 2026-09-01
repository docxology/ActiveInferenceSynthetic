# Planning: Policies as Action Sequences {#sec:planning}

[@sec:expected-free-energy] scored *one* action: what is the best thing to do
right now? But the value of an action often lies in what it makes possible
*next*. This section extends the same currency to **policies** — short
sequences of actions — and shows that *planning* is not a new rule bolted onto
Active Inference: it is expected free energy minimized over sequences. The
core is `src/policy_planning.py`; every value below is checked against a
hand-worked reference, and [@fig:planning] is generated from the same live
computation.

The agent of [@sec:expected-free-energy] returns, with the same two actions —
a **cue** that reveals the hidden context and a **bet** whose outcome model is
state-independent — and the same **sharp** preferences under which the
*one-step* rule chose to exploit. Now it plans over a horizon of
$T = {{PLANNING_HORIZON}}$ steps. A policy $\pi = (a_1, \dots, a_T)$ induces a
distribution over outcome sequences; along each branch the belief evolves by
exact Bayes rule, and the plan's expected free energy is

$$
G(\pi) \;=\; -\underbrace{\mathbb{E}_{q(o_{1:T}\mid\pi)}\big[\ln p_{\text{pref}}(o_T)\big]}_{\text{pragmatic (terminal)}}
\;-\; \underbrace{I(s;\, o_{1:T} \mid \pi)}_{\text{epistemic (cumulative)}}.
$$

Two changes from the one-step $G(a)$ are load-bearing. The **pragmatic term
is terminal**: payoffs are collected on the *final* outcome only, so an
informative first action earns nothing immediately — its entire value is the
sharper belief the final action is then chosen under. And the **epistemic term
is cumulative**: the expected resolution of uncertainty over the whole
sequence, which by the chain rule of relative entropy is the mutual
information $I(s; o_{1:T} \mid \pi)$ between the context and the *entire*
outcome sequence (a fact the tests verify against an independently computed
mutual information).

The subtlety that makes this genuinely planning rather than bookkeeping is
*when* the expectation is taken. Each branch is followed to its end, the
final action evaluated under that branch's posterior, and only then averaged
over branches. The nonlinearity of Bayes rule is preserved inside the
expectation — which is exactly why information has value. Averaging *first*
(the posterior-mixture shortcut) would collapse every branch's posterior back
to the prior and erase the value of looking before leaping.

![**Planning as expected-free-energy minimization.** The same agent and
preferences as [@sec:expected-free-energy] now plan over two-step policies. All
four plans are scored exactly (branch enumeration, no sampling): bars are
$G(\pi)$, annotated with pragmatic/epistemic splits. **Cue-then-bet wins**
($G = {{PLANNING_EFE_LOOK_THEN_LEAP}}$): the first action collects epistemic
value ($+{{PLANNING_EPISTEMIC_LOOK_THEN_LEAP}}$ nats), and the terminal bet is
then placed under the sharpened belief. Betting first
($G = {{PLANNING_EFE_EXPLOIT_FIRST}}$) pays the same either way and forgoes the
information — under these sharp preferences the *one-step* optimum is not the
*plan* optimum. Exploration is deferred exploitation. Rendered
deterministically by `scripts/generate_policy_planning_figure.py` over the
tested core in `src/policy_planning.py`.](../output/figures/policy_planning.png){#fig:planning width=94%}

[@fig:planning] evaluates all four two-step policies. The winner is **cue
then bet**: look, resolve the uncertainty (epistemic value
$+{{PLANNING_EPISTEMIC_LOOK_THEN_LEAP}}$ nats), and *then* place the wager the
sharpened belief licenses — $G = {{PLANNING_EFE_LOOK_THEN_LEAP}}$. Betting
first — the one-step optimum under these same preferences — costs
$G = {{PLANNING_EFE_EXPLOIT_FIRST}}$: the terminal bet pays the same either
way, but it forgoes the information the plan could have collected first. The
explore/exploit balance of [@sec:expected-free-energy] is revealed as a
*temporal* structure: exploration is what exploitation looks like when it is
allowed to plan. One currency, one minimization, now over sequences — the
agent defers gratification because $\arg\min_\pi G(\pi)$ told it to.

Branch enumeration is exact — every one of $O^T$ outcome sequences is summed,
no sampling, no RNG — so the demonstration is deterministic and reproducible.
The horizon is deliberately short; tree search over longer horizons, and
approximate schemes for intractable ones, are the natural next expansions, and
are recorded as such in the roadmap.
