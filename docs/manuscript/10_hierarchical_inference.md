# A Two-Level Generative Hierarchy {#sec:hierarchy}

A hierarchy gives the model another hidden level without changing the logic of
conditioning. Let context $c$ generate state $x$, which generates observation
$o$. The factorization is

$$p(c,x,o)=p(c)\,p(x\mid c)\,p(o\mid x).$$ {#eq:hierarchy}

Top-down prediction marginalizes the context law through the state channel.
Bottom-up inference conditions the joint on the observed outcome, then
marginalizes the posterior to each hidden level. This preserves the joint
rather than updating the levels independently. The exact categorical core is
`src/hierarchical_model.py`; matrix columns are conditional distributions.

For the worked observation, predictive state-zero mass is
{{HIERARCHY_PREDICTED_STATE0}} and observation evidence is {{HIERARCHY_EVIDENCE}}.
The posterior state-zero mass becomes {{HIERARCHY_STATE0}} and the posterior
context-zero mass becomes {{HIERARCHY_CONTEXT0}}. The observation therefore
updates both levels while their posterior dependence remains represented in
the joint. [@fig:hierarchy] shows the downward prediction and upward update.

A real control makes the observation channel independent of state. Conditioning
then leaves both hidden marginals unchanged. An impossible observation raises
an error instead of manufacturing a posterior. Tests compare the full joint
and each posterior with independently enumerated products, and reject malformed
channels and out-of-range observations.

This is exact inference in a finite Bayesian hierarchy, not a neural network,
a variational message-passing algorithm, or a learned deep model. Its purpose
is to show how a higher-level model supplies a lower-level prior and how
observations update that higher level through the shared generative structure
[@parr2022active].

![**Prediction downward, inference upward.** The context law induces a state
prediction and an observation prediction. Conditioning on one observation
updates both context and state using the same posterior joint, without discarding
their dependence.](../output/figures/hierarchical_inference.png){#fig:hierarchy width=94%}
