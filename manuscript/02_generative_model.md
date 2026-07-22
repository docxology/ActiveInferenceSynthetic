# Perception as Inference {#sec:generative-model}

The extended abstract makes a strong claim in one sentence: *minimizing
variational free energy **is** approximate Bayesian inference, carried out by
the physical dynamics of the thing itself*. This section makes that claim
runnable. It is the smallest generative model that still says something true,
and everything below is checked against closed-form Bayes in
`src/generative_model.py`.

A system holds a **generative model** of a hidden cause $x$ and a sensation
$s$: a prior $p(x)$ over states and a likelihood $p(s \mid x)$ saying which
sensations each state tends to produce. Together they fix the joint
$p(s, x) = p(s \mid x)\,p(x)$, the evidence $p(s) = \sum_x p(s, x)$, and — by
Bayes' rule — the posterior $p(x \mid s) = p(s, x) / p(s)$. The system never
sees $x$; it only ever has $s$ and its own model. Inference is the problem of
recovering $p(x \mid s)$ from those.

Active Inference solves it without ever computing $p(s)$ directly, through a
belief $q(x)$ and a single scalar, the **variational free energy**:

$$
F[q] \;=\; \underbrace{\mathrm{KL}\!\left[q(x)\,\Vert\,p(x)\right]}_{\text{complexity}}
\;-\; \underbrace{\mathbb{E}_{q}\!\left[\ln p(s \mid x)\right]}_{\text{accuracy}}.
$$

Two facts, both asserted to machine precision in the tests, make $F$ the whole
game. First, **$F$ is an upper bound on surprise**: $F[q] = -\ln p(s) +
\mathrm{KL}\!\left[q \Vert p(x \mid s)\right] \ge -\ln p(s)$, because a KL
divergence is never negative. Surprise $-\ln p(s)$ is exactly what an organism
"wants" to keep low — the improbability of its own sensory state — but it
cannot compute it. It *can* compute $F$, from quantities it already has.
Second, **the bound is tight at the posterior**: $F$ is least, and equals the
surprise, precisely when $q = p(x \mid s)$. So the belief that minimizes free
energy is the Bayesian posterior, and the minimized value is the surprise it
bounds. Inference falls out of minimization.

[@fig:belief] shows this happening. Take a two-state model with prior
$p(x) = (0.6, 0.4)$ and a likelihood under which state $x_0$ makes the observed
sensation $s$ far more probable than $x_1$ does. Panel (a) starts from a
maximally uncommitted uniform belief and runs gradient descent on $F$ over the
belief simplex; the belief mass migrates toward the exact posterior
$p(x_0 \mid s) = 0.54/0.62 \approx 0.87$. Panel (b) tracks $F$ across the same
descent: it falls **monotonically** to the surprise $-\ln p(s)$ (dashed line),
and the shrinking shaded gap is exactly $\mathrm{KL}\!\left[q_t \Vert p(x \mid
s)\right]$ — the belief's remaining error. Perception, here, is nothing but
this descent: the system lowers free energy by updating beliefs, and in doing
so recovers the posterior it could not compute directly.

The complexity–accuracy split names the trade-off. *Accuracy* rewards beliefs
that explain the sensation; *complexity* penalizes moving away from the prior.
Perception moves beliefs only as far as the evidence warrants — the same
regularized fit that makes the free-energy principle a principle rather than a
slogan. Action, treated in the next demonstrations, minimizes the *same* $F$ in
the other direction: by changing $s$ rather than $q$.

![**Perception as free-energy minimization.** A two-state generative model
(prior $p(x)=(0.6,0.4)$; likelihood favouring $x_0$ for the observed $s$). **(a)**
From a uniform starting belief, gradient descent on variational free energy
drives the belief over hidden states to the exact Bayesian posterior
$p(x\mid s)$ (orange), passing through intermediate beliefs (blue) on the way.
**(b)** Along the same descent the free energy $F[q_t]$ falls monotonically to
the surprise $-\ln p(s)$ (dashed) that it bounds; the shaded gap is exactly
$\mathrm{KL}[q_t\Vert p(x\mid s)]$, the belief's error, which closes as
inference completes. Minimizing free energy is Bayesian updating. Rendered
deterministically by `scripts/generate_belief_update_figure.py` over the tested
core in `src/generative_model.py`.](../output/figures/belief_update.png){#fig:belief width=92%}
