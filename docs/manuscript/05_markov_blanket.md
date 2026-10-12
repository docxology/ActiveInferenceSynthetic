# The Markov Blanket {#sec:markov-blanket}

Everything so far assumed a clean split between a system and its world — a
belief $q(s)$ about *hidden* states, sensations $o$ that are not those states,
actions that reach *out*. That split is not a modeling convenience; it is a
structural claim, and it has a name: the **Markov blanket**. This section shows
what the blanket actually asserts, using the one case where it is exactly
computable — a jointly Gaussian world. The core is `src/markov_blanket.py`.

Partition the variables of a system-plus-environment into four roles:
*external* states $\eta$ (the world), *internal* states $\mu$ (the system's own
states, which parameterize its beliefs), and the *blanket* that lies between
them — *sensory* states $s$ (world $\to$ system) and *active* states $a$ (system
$\to$ world). The blanket's defining property is a **conditional independence**:

$$
p(\eta, \mu \mid s, a) \;=\; p(\eta \mid s, a)\; p(\mu \mid s, a).
$$ {#eq:blanket-factorization}

In this example the endpoints are marginally dependent, but their coupling is
screened by the blanket. Given sensory and active coordinates, knowing the
external coordinate supplies no additional information about the internal
coordinate under the stated Gaussian law. A causal interpretation would need
a dynamical or interventional model. Conditional independence alone does not
establish a posterior encoding or a cognitive interpretation.

[@fig:blanket] makes both halves of the claim visible on a Gaussian built so
that the $\eta$–$\mu$ block of its **precision matrix** (the inverse covariance)
is exactly zero. Panel (a) is the ordinary correlation matrix: $\eta$ and $\mu$
are plainly correlated ($\mathrm{corr} = {{BLANKET_CORR}}$): they are statistically coupled
through the blanket. Panel (b) is the precision matrix, and the payoff is
the highlighted cell: $\Pi_{\eta\mu} = 0$. In a Gaussian a zero precision entry
is *exactly* a conditional independence given the remaining variables — so the
zero at $(\eta,\mu)$ says $\eta \perp \mu \mid \{s,a\}$. Conditioning on the
blanket collapses the partial correlation between internal and external states
to zero (the tests confirm it vanishes to ${{PARTIAL_CORR_ATOL}}$ via the Schur complement),
even though conditioning on only *part* of the blanket does not — both the
sensory and active states are needed to close the channel.

## A matched native Gaussian example

A second fixture matches the pinned upstream canonical four-axis Gaussian
carrier. Its ordered variables are external, sensory, active, and internal.
The exact precision and covariance arrays live in `src/demos.py`; tests verify
their rational inverse relation. External and internal marginal covariance is
{{NATIVE_BLANKET_COVARIANCE}}, while conditioning on sensory and active yields
a diagonal endpoint covariance. The native Lean adapter binds the canonical
precision to a positive-definite Gaussian law and uses upstream conditional
independence for every supplied center, including its almost-everywhere
conditional-kernel interpretation.

The corresponding perturbed endpoint precision supplies a genuine boundary:
adding a nonzero external-internal coupling produces conditional covariance
$-1/15$ and native non-independence. The original numerical fixture and this
canonical native fixture are distinct examples. Formal coverage is claimed for
the matched canonical carrier, not inferred for arbitrary precision matrices
from the appearance of a zero cell.

Conditional independence alone does not imply that internal states encode a
posterior, that the partition is causal, or that an organism is intelligent.
Those interpretations require a generative or dynamical model and additional
assumptions. The finite perception-action example makes such a model explicit
rather than inferring it from the Gaussian partition.

![**Marginal dependence, conditional independence.** A jointly Gaussian world
over external $\eta$, sensory $s$, active $a$, internal $\mu$, built with a zero
$\eta$–$\mu$ precision block. **(a) Marginal correlation:** $\eta$ and $\mu$ are
correlated (${{BLANKET_CORR}}$, highlighted) — they are statistically coupled through the
blanket. **(b) Precision (inverse covariance):** the $\eta$–$\mu$ entry is
exactly $0$, which in a Gaussian *is* conditional independence given the other
variables — so $\eta \perp \mu \mid \{s,a\}$ and the partial correlation given
the blanket is $0$. **(c)** The matched upstream canonical fixture has a
diagonal conditioned endpoint covariance despite nonzero marginal coupling.
The sensory and active states screen the internal states
from the external world. Rendered deterministically by
`scripts/generate_markov_blanket_figure.py` over the tested core in
`src/markov_blanket.py`.](../output/figures/markov_blanket.png){#fig:blanket width=94%}
