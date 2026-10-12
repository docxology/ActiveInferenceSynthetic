# Action: Variational vs Expected Free Energy {#sec:expected-free-energy}

[@sec:generative-model] showed perception: minimizing **variational** free
energy $F$ over beliefs about what is happening *now*. But a thing that only
perceived would be a spectator. Active Inference closes the loop by minimizing
the *same* currency in the other direction — over **actions**, scored by the
free energy they are *expected* to produce. That forward-looking quantity is
**expected free energy** $G$, and it is what turns inference into behavior. The
core is `src/expected_free_energy.py`; every value below is checked against a
hand-worked reference.

The two free energies differ only in tense. $F[q]$ grades a belief against a
sensation already in hand — it is retrospective, and its minimum is the
posterior. $G(a)$ grades a *candidate action* against the sensations it *would*
generate, averaged over what the agent currently believes. For an action $a$,
belief $q(s)$, outcome model $p(o \mid s, a)$, and preferences
$p_{\text{pref}}(o)$ — a distribution over the outcomes the agent wants to
encounter — $G$ splits into two terms the agent seeks to make large (so it
minimizes their negatives):

$$
G(a) \;=\; -\underbrace{\mathbb{E}_{q(o\mid a)}\big[\ln p_{\text{pref}}(o)\big]}_{\text{pragmatic value}}
\;-\; \underbrace{\mathbb{E}_{q(o\mid a)}\!\big[\mathrm{KL}[\,q(s\mid o,a)\,\Vert\,q(s)\,]\big]}_{\text{epistemic value}}.
$$ {#eq:efe}

**Pragmatic value** is expected utility: how well an action's likely outcomes
match what the agent prefers. **Epistemic value** is expected information gain —
how much the action's outcomes would sharpen the belief about the hidden state,
which is exactly the mutual information $I(s; o \mid a)$ and is always
non-negative. One is the drive to *get what you want*; the other is the drive to
*find out*. Both live inside a single number.

[@fig:efe] shows why that unification matters. An agent is unsure which of two
contexts holds ($q(s) = ({{BELIEF_S0}}, {{BELIEF_S1}})$) and can take one of two actions:
a **cue** that would reveal the context (highly informative, epistemic value
$+{{EFE_CUE_EPISTEMIC}}$ nats, but preference-neutral) or a **bet** that pays off regardless of
context (uninformative, epistemic value $0$, but potentially rewarding). The
*only* thing that changes between the two panels is the preferences. Under
**flat** preferences (panel a) the agent has nothing to chase, so the epistemic
term decides: it takes the cue and **explores** ($G = {{EFE_FLAT_CUE}}$ vs {{EFE_FLAT_BET}}). Under
**sharp** preferences (panel b) the pull of the reward dominates, and the same
minimization takes the bet and **exploits** ($G = {{EFE_SHARP_BET}}$ vs {{EFE_SHARP_CUE}}). This is a
deliberately constructed two-action example, chosen to isolate the mechanism;
what it demonstrates is structural, not incidental to these numbers. The
explore/exploit trade-off is not a separate rule bolted onto the agent — there
is one rule, $\arg\min_a G$. Because $G$ carries both a pragmatic and an
epistemic term, exploration and exploitation are the two limits of a single
balance, and which one wins is decided by the preferences alone.

This is the whole architecture in miniature. Perception ($F$) and action ($G$)
are one imperative — minimize free energy — read in two tenses. Inference makes
beliefs fit the world; action makes the world fit beliefs *and* preferences,
gathering information where it is uncertain and reward where it is confident.

![**One rule yields explore and exploit.** An agent uncertain between two
contexts ($q(s)=({{BELIEF_S0}},{{BELIEF_S1}})$) chooses between an informative "cue" (epistemic
value $+{{EFE_CUE_EPISTEMIC}}$, preference-neutral) and a rewarding but uninformative "bet"
(epistemic value $0$). Bars are expected free energy $G$ per action (lower is
chosen); each is annotated with its pragmatic/epistemic split. **(a) Flat
preferences:** the epistemic term dominates, so the agent explores (cue,
$G={{EFE_FLAT_CUE}}$). **(b) Sharp preferences:** the pragmatic term dominates, so the same
$\arg\min G$ rule exploits (bet, $G={{EFE_SHARP_BET}}$). A single rule; the balance of $G$'s
two terms — not a hand-coded switch — is what turns over between the panels.
Rendered deterministically by
`scripts/generate_efe_figure.py` over the tested core in
`src/expected_free_energy.py`.](../output/figures/expected_free_energy.png){#fig:efe width=92%}
