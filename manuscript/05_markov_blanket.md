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
$$

Internal and external states are *not* independent — they are statistically
coupled, that is the entire point of a mind modeling a world. But that coupling
is **screened by** the blanket. Fix the blanket, and they become conditionally
independent: nothing about $\eta$ tells you anything more about $\mu$ once you
know $s$ and $a$. (This is a statement about statistical dependence in the joint
distribution, not about causal direction or intervention — a causal reading
would need a dynamical or interventional model on top of this one.) That
conditional independence is what licenses treating internal states as
*inferring* external ones they never share a variable with: conditioned on the
blanket, the internal states' sufficient statistics for the external world are
exactly their beliefs given the blanket.

[@fig:blanket] makes both halves of the claim visible on a Gaussian built so
that the $\eta$–$\mu$ block of its **precision matrix** (the inverse covariance)
is exactly zero. Panel (a) is the ordinary correlation matrix: $\eta$ and $\mu$
are plainly correlated ($\mathrm{corr} = 0.19$): they are statistically coupled
through the blanket. Panel (b) is the precision matrix, and the payoff is
the highlighted cell: $\Pi_{\eta\mu} = 0$. In a Gaussian a zero precision entry
is *exactly* a conditional independence given the remaining variables — so the
zero at $(\eta,\mu)$ says $\eta \perp \mu \mid \{s,a\}$. Conditioning on the
blanket collapses the partial correlation between internal and external states
to zero (the tests confirm it vanishes to $10^{-10}$ via the Schur complement),
even though conditioning on only *part* of the blanket does not — both the
sensory and active states are needed to close the channel.

That is the geometry underneath the whole overview. A free-energy-minimizing
system is one whose internal states, across its blanket, come to encode a
posterior over the external states it is coupled to but cannot see. Perception
([@sec:generative-model]) updates that encoding; action
([@sec:expected-free-energy]) acts through the blanket to keep the world within
the range the encoding expects; and the flow and trajectories
([@sec:extended;@sec:worked-regimes]) are what that coupling looks like as
dynamics. The blanket is the boundary that makes "a thing that models its world"
a well-posed idea rather than a metaphor.

![**Marginal dependence, conditional independence.** A jointly Gaussian world
over external $\eta$, sensory $s$, active $a$, internal $\mu$, built with a zero
$\eta$–$\mu$ precision block. **(a) Marginal correlation:** $\eta$ and $\mu$ are
correlated ($0.19$, highlighted) — they are statistically coupled through the
blanket. **(b) Precision (inverse covariance):** the $\eta$–$\mu$ entry is
exactly $0$, which in a Gaussian *is* conditional independence given the other
variables — so $\eta \perp \mu \mid \{s,a\}$ and the partial correlation given
the blanket is $0$. The sensory and active states screen the internal states
from the external world. Rendered deterministically by
`scripts/generate_markov_blanket_figure.py` over the tested core in
`src/markov_blanket.py`.](../output/figures/markov_blanket.png){#fig:blanket width=94%}
