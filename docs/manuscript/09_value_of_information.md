# When Information Improves a Decision {#sec:decision-value}

Information gain and instrumental value answer different questions. Mutual
information measures expected belief change in nats. Instrumental value asks
whether an observation improves a subsequent choice under a specified utility.
The open-loop bet in [@sec:planning] does not use hidden context. The closed-loop
agent in [@sec:synthetic-agent] does. We can isolate this difference with exact
finite Bayesian decision analysis, without asserting that utility is EFE or
thermodynamic free energy.

Let the static hidden state have prior $q(x)$, the cue channel be $A(o\mid x)$,
and the available commitments have finite utilities $u(a,x)$. With no cue,
the best expected utility is $V_0$. With a cue, a feedback policy can choose a
different commitment for each reachable observation:

$$
V_0=\max_a\sum_x q(x)u(a,x),\qquad
V_{\mathrm{obs}}=\sum_o\max_a\sum_x q(x)A(o\mid x)u(a,x).
$$ {#eq:decision-values}

The joint-mass expression avoids defining a posterior on an impossible outcome.
On reachable outcomes it equals expected optimal posterior utility. The policy
that ignores the observation and always selects a prior-optimal action is among
the admissible feedback policies. Therefore $V_{\mathrm{obs}}\ge V_0$: for each
outcome the maximum is at least the value of that constant action, and summing
over outcomes recovers $V_0$ by channel normalization. This elementary finite
argument is an exposition here, not a newly imported Lean theorem.

For a fixed acquisition cost $c$ in the same utility units, define

$$
\operatorname{VOI}=V_{\mathrm{obs}}-V_0,\qquad
\operatorname{VOI}_{\mathrm{net}}=V_{\mathrm{obs}}-V_0-c.
$$ {#eq:decision-voi}

The gross value is nonnegative under these assumptions; the net value can be
negative. An optional acquisition is worthwhile under this utility objective
only when its net value is positive. Unlike EFE's explicit epistemic reward,
this calculation rewards information solely through its later consequences.
Utility units, log-preference scores, and nats must not be silently substituted
for one another. If utility is rescaled, its acquisition cost must be rescaled
consistently.

The worked channel has known accuracy {{VOI_ACCURACY}} and a uniform prior.
Correct commitment receives unit utility and incorrect commitment receives
zero. Exact enumeration gives baseline utility {{VOI_BASELINE}}, informed
utility {{VOI_INFORMED}}, and gross value {{VOI_GROSS}}. With cost {{VOI_COST}},
net value is {{VOI_NET}}. The same cue carries {{VOI_INFORMATION}} nats of
information when the utility matrix is replaced by state-independent outcomes,
yet its gross instrumental value then vanishes. An independent cue gives both
zero information and zero gross value.

![**Decision value and information have distinct units.** The left panel sweeps known cue accuracy for an observation-contingent commitment, its acquisition cost, and a state-independent utility counterexample. The right panel shows the same channel's mutual information. Positive information does not imply positive instrumental value; a beneficial cue can also be too costly. Both panels use exact finite computation, not sampled performance estimates.](../output/figures/value_of_information.png){#fig:decision-value width=100%}

`src/value_of_information.py` enumerates every reachable observation; tests
independently enumerate every deterministic feedback policy. Unreachable
outcomes have no invented posterior or action. Ties choose the lowest action
index. The sweep holds the prior and utilities fixed and treats the channel as
known. Miscalibrated models, changing hidden states, action-dependent sensing
costs, limited computation, and learned preferences require additional models.
This is a controlled bridge from learning to acting, not a claim of general
adaptive intelligence.

Enumeration covers the complete finite policy space, but the Python arithmetic
is floating point. Tests use independently calculated references and explicit
tolerances; nonfinite inputs and unrepresentable utility results are rejected.
