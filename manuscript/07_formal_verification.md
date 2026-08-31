# Formal Verification {#sec:formal}

Every preceding section pairs a claim with a runnable, tested demonstration —
*show, not tell* at the level of numerics. This section takes the discipline one
level deeper: the load-bearing *mathematical* claims are not only computed and
tested, they are **machine-checked**. A small self-contained Lean 4 development
in `formal/` proves them with no `sorry`. The development has two surfaces: the
manuscript-canonical ℝ theorems are re-exported, with exposition, from the
companion **fep_lean** library (mathlib-backed), while a legacy ℤ surface proves
the same structural statements from Lean's core axioms alone. Where `src/`
guarantees the numbers are right, `formal/` guarantees the theorems are.

The formalization mirrors the two halves of the overview.
`ActiveInferenceFormal.Geometry` and `ActiveInferenceFormal.GeometryZ` carry the
facts behind the flow and the steady state (ℝ and ℤ respectively);
`ActiveInferenceFormal.Information` and `ActiveInferenceFormal.InformationZ`
carry the facts behind perception, and `Bridge.lean` maps the three evidence
surfaces — Python, formal ℝ, formal ℤ — onto one another. The headline results:

| Lean theorem | What it establishes | Section |
|---|---|---|
| `solenoidal_orthogonal` | $(Q\,g)\cdot g = 0$: the antisymmetric current does no work against $\nabla F$ | §1, §3 |
| `flow_work_eq_dissipation` | $f\cdot g = -\gamma\lVert g\rVert^2$: only dissipation changes $F$; the circulation is free | §3 |
| `detailed_balance_iff` | the solenoidal current vanishes $\iff \omega=0$ | §3 |
| `entropyProduction_nonneg` | $\gamma\sigma = 2\omega^2\Pi \ge 0$ | §6 |
| `entropyProduction_zero_iff` | entropy production is zero $\iff \omega=0$ | §6 |
| `relEntropy_nonneg` | Gibbs' inequality: relative entropy $\ge 0$ | §2 |
| `freeEnergy_eq_surprise_add_relEntropy` | $F = \text{surprise} + D(q\Vert\text{posterior})$ | §2 |
| `freeEnergy_ge_surprise` | the (total-scaled) bound $\text{total}\cdot\text{surprise} \le F$ | §2 |
| `freeEnergy_ge_surprise_of_model` | the bound for a genuine model $j_i = r_i E$ | §2 |
| `freeEnergy_eq_surprise_at_posterior` | the bound is attained at the posterior | §2 |

Two design choices keep the development honest and light. First, it works over
the integers $\mathbb{Z}$ rather than the reals: the results above are polynomial
identities and sign facts whose truth does not depend on the real-number
completion, so $\mathbb{Z}$ suffices and the project needs no analysis library
(it builds in about a second and depends on *nothing* but Lean core). The
floating-point instances live on the Python side; the two layers verify the same
statements at different resolutions.

Second — and this is the crux for the free-energy bound — the logarithm's
analytic properties are made **explicit hypotheses** rather than hidden inside a
library. Gibbs' inequality rests on exactly two facts about $\ln$: that it turns
products into sums ($\ln(ab)=\ln a+\ln b$), and the tangent-line bound
$\ln x \le x-1$. But there is a subtlety that a green build alone will not catch,
and the development takes pains to get it right. Stating those two properties as
*universal* hypotheses over $\mathbb{Z}$ — "for **all** positive integers" —
would be a trap: no integer function can satisfy the cleared tangent bound
$b-a \le b(L b - L a)$ at both orientations of the pair $\{2,3\}$ (integer
rounding destroys the real-line tangency), so such an antecedent has no model and
every theorem beneath it would be **vacuously** true. A proof assistant will
happily check a vacuous theorem: no `sorry`, clean axioms, and no content.

The development therefore takes the log's properties only at the **exact points
each proof consumes** — the tangent bound and additivity at the specific
belief/reference/evidence values — which the real $\ln$ satisfies and which are
jointly satisfiable over $\mathbb{Z}$. To *prove* they are satisfiable rather than
merely assert it, `Sanity.lean` carries a matched pair of controls: a negative
one (`relEntropy_can_be_negative` — a concrete function for which relative entropy
is $-20$, so the tangent hypothesis is genuinely necessary) and a **positive
control** on a *genuine generative model*: `okL` is the 2-adic valuation (an
actually log-additive function), with belief $(4,2)$, posterior $(2,4)$, evidence
$2$, and joint $(4,8) = (r_0 E, r_1 E)$ — real products, not hand-picked values.
There every hypothesis provably holds and the bound fires with a *non-trivial*
gap, $-6 \le -4$, equal to the relative entropy $2$. Necessity and satisfiability
together certify the theorems are faithful, not vacuous.

The guarantee is auditable. The `Audit` module runs `#print axioms` on each
headline theorem *and each witness*. Every ℤ theorem reports
`depends on axioms: [propext, Quot.sound]` — Lean's standard trusted core — and
the ℝ theorems report the standard mathlib footprint; no theorem ever depends on
`sorryAx`. The project's test suite runs the real `lake build`, inspects
that output, and checks the non-vacuity witnesses are present, so the "it is
proved, and it is not vacuous" claim is itself tested rather than asserted. In the
spirit of the whole overview: the strongest thing you can say about a
mathematical claim is not that it looks right, or even that it computes right, but
that a machine has checked the proof — and here, that you can re-check the
checker, and that what it checked has content.
