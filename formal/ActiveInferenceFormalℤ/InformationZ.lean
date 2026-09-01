/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/

/-!
# Perception as inference — the variational free-energy bound

Formal counterpart to `src/generative_model.py`. The manuscript's central claim
is that **variational free energy is an upper bound on surprise, tight at the
Bayesian posterior**, so minimizing it *is* inference. This module proves exactly
that, for a two-state model, from Lean core alone.

## Honesty of the formalization — point hypotheses, not a vacuous universal

Free energy and relative entropy involve the logarithm, whose analytic
properties (additivity, and the tangent-line inequality `ln x ≤ x - 1`) are the
real content of Gibbs' inequality. A tempting shortcut — assume an abstract
`L : ℤ → ℤ` satisfying those properties *for all* integers — is a **trap**: no
integer function satisfies the cleared tangent bound `b - a ≤ b·(L b - L a)` for
all positive `a, b` (integer rounding kills it on the pair `{2,3}`), so such a
universal antecedent is unsatisfiable and every theorem under it would be
*vacuously* true. `Sanity.lean` records this.

Instead, each theorem takes the log's properties **only at the exact points its
proof consumes**, as ordinary hypotheses:

* `htangent i` — the cleared tangent bound `qᵢ - rᵢ ≤ qᵢ·(L qᵢ - L rᵢ)`, which
  the real `ln` satisfies at every point;
* `hlog i` — additivity `L jᵢ = L rᵢ + L E` at the joint/posterior/evidence
  triple (i.e. `ln jᵢ = ln rᵢ + ln E`, the log of `jᵢ = rᵢ·E`).

These are satisfiable — `Sanity.lean` exhibits a concrete `L` and distribution
where they hold and the bound is non-trivial — so the theorems are genuine, not
vacuous.

## Counts, not normalized reals

A probability vector cannot be encoded as two *positive integers summing to 1*.
So `q` and `r` are integer **counts** sharing a total mass; surprise scales by
that total. Over `ℤ` the faithful, non-vacuous statement is
`freeEnergy = relEntropy + total · surprise` and `total · surprise ≤ freeEnergy`.
The normalized real statement `F ≥ surprise` is recovered by dividing through by
the total — which is legitimate only for a **positive** total, over `ℝ`, where it
equals `1` — and that real-valued instance lives on the Python side; it is *not*
what this `ℤ` development proves.

## Main results

* `relEntropy_nonneg` — Gibbs' inequality: relative entropy is `≥ 0`.
* `relEntropy_self_zero` — it is `0` when the belief equals the reference.
* `freeEnergy_eq_surprise_add_relEntropy` — the exact decomposition.
* `freeEnergy_ge_surprise` — the (total-scaled) bound `total·surprise ≤ F`.
* `freeEnergy_ge_surprise_of_model` — the bound for a genuine model `jᵢ = rᵢ·E`.
* `freeEnergy_eq_surprise_at_posterior` — the bound is attained at the posterior.
-/

namespace ActiveInferenceFormalℤ

/-- Relative entropy `D(q‖r) = Σ qᵢ (L qᵢ − L rᵢ)` of a two-state belief `q`
against a reference `r`. -/
def relEntropy (L : Int → Int) (q0 q1 r0 r1 : Int) : Int :=
  q0 * (L q0 - L r0) + q1 * (L q1 - L r1)

/-- Variational free energy `F[q] = Σ qᵢ (L qᵢ − L jᵢ)` for a belief `q` against
the joint `j` (likelihood × prior) at the observed outcome. -/
def freeEnergy (L : Int → Int) (q0 q1 j0 j1 : Int) : Int :=
  q0 * (L q0 - L j0) + q1 * (L q1 - L j1)

/-- Surprise `−L(evidence)` — the negative log evidence the free energy bounds. -/
def surprise (L : Int → Int) (evidence : Int) : Int := - L evidence

/-- **Gibbs' inequality.** If the cleared tangent-line bound holds at each of the
two points (`htangent0`, `htangent1` — which the real `ln` always satisfies), and
belief and reference share a total mass (`hsum : q0 + q1 = r0 + r1`), then
relative entropy is nonnegative. This is the mathematical core of "free energy is
an upper bound on surprise": the slack between them is exactly this quantity. -/
theorem relEntropy_nonneg (L : Int → Int) (q0 q1 r0 r1 : Int)
    (htangent0 : q0 - r0 ≤ q0 * (L q0 - L r0))
    (htangent1 : q1 - r1 ≤ q1 * (L q1 - L r1))
    (hsum : q0 + q1 = r0 + r1) :
    0 ≤ relEntropy L q0 q1 r0 r1 := by
  simp only [relEntropy]
  omega

/-- The bound is **tight when the belief equals the reference**: `D(q‖q) = 0`.
Applied with the reference equal to the posterior, this is the statement that the
free-energy minimizer is the exact Bayesian posterior. -/
theorem relEntropy_self_zero (L : Int → Int) (q0 q1 : Int) :
    relEntropy L q0 q1 q0 q1 = 0 := by
  simp only [relEntropy, Int.sub_self, Int.mul_zero, Int.add_zero]

/-- **The variational free energy decomposes as surprise plus relative entropy.**
Given the log-additivity of the joint at each point (`hlog0 : L j0 = L r0 + L
evidence`, i.e. `ln j0 = ln r0 + ln E` from `j0 = r0·E`), the free energy against
the joint equals the total-scaled surprise plus the relative entropy against the
reference `r` (the posterior). No normalization is assumed; the total mass
`q0 + q1` appears explicitly. -/
theorem freeEnergy_eq_surprise_add_relEntropy (L : Int → Int)
    (q0 q1 r0 r1 j0 j1 evidence : Int)
    (hlog0 : L j0 = L r0 + L evidence)
    (hlog1 : L j1 = L r1 + L evidence) :
    freeEnergy L q0 q1 j0 j1
      = relEntropy L q0 q1 r0 r1 + (q0 + q1) * surprise L evidence := by
  simp only [freeEnergy, surprise, relEntropy, hlog0, hlog1]
  -- Distribute every qᵢ over the L-sums/differences into atomic products.
  simp only [Int.mul_sub, Int.mul_add, Int.mul_neg]
  -- The one nonlinear fact omega needs: q0·Le + q1·Le = (q0+q1)·Le.
  have hsplit : q0 * L evidence + q1 * L evidence = (q0 + q1) * L evidence := by
    rw [Int.add_mul]
  omega

/-- **The free-energy bound.** With the tangent bound at each point, the
log-additivity of the joint at each point, and belief/reference sharing a total,
the total-scaled surprise is a lower bound on variational free energy. Minimizing
`F` therefore minimizes an accessible bound on the inaccessible surprise — the
quantitative heart of the Free Energy Principle. -/
theorem freeEnergy_ge_surprise (L : Int → Int)
    (q0 q1 r0 r1 j0 j1 evidence : Int)
    (htangent0 : q0 - r0 ≤ q0 * (L q0 - L r0))
    (htangent1 : q1 - r1 ≤ q1 * (L q1 - L r1))
    (hlog0 : L j0 = L r0 + L evidence)
    (hlog1 : L j1 = L r1 + L evidence)
    (hsum : q0 + q1 = r0 + r1) :
    (q0 + q1) * surprise L evidence ≤ freeEnergy L q0 q1 j0 j1 := by
  have hdecomp := freeEnergy_eq_surprise_add_relEntropy L q0 q1 r0 r1 j0 j1 evidence
    hlog0 hlog1
  have hgibbs : 0 ≤ relEntropy L q0 q1 r0 r1 :=
    relEntropy_nonneg L q0 q1 r0 r1 htangent0 htangent1 hsum
  rw [hdecomp]; omega

/-- **The bound for an actual generative model.** Here the joint is the genuine
product `jᵢ = rᵢ · evidence` (likelihood × prior = the posterior times the
evidence), and log-additivity is required *of that product* — `L (rᵢ · evidence)
= L rᵢ + L evidence` — which the real `ln`, and the 2-adic valuation used in the
positive-control witness, actually satisfy. This makes the free-energy bound a
statement about a real model, not just about abstract point values. -/
theorem freeEnergy_ge_surprise_of_model (L : Int → Int)
    (q0 q1 r0 r1 evidence : Int)
    (htangent0 : q0 - r0 ≤ q0 * (L q0 - L r0))
    (htangent1 : q1 - r1 ≤ q1 * (L q1 - L r1))
    (hmul0 : L (r0 * evidence) = L r0 + L evidence)
    (hmul1 : L (r1 * evidence) = L r1 + L evidence)
    (hsum : q0 + q1 = r0 + r1) :
    (q0 + q1) * surprise L evidence
      ≤ freeEnergy L q0 q1 (r0 * evidence) (r1 * evidence) :=
  freeEnergy_ge_surprise L q0 q1 r0 r1 (r0 * evidence) (r1 * evidence) evidence
    htangent0 htangent1 hmul0 hmul1 hsum

/-- **The bound is tight *at* the posterior.** When the belief equals the
reference (`q = r`, so the relative entropy vanishes), the free energy equals the
total-scaled surprise: the lower bound is attained at the inference problem's
solution. (This is the "attained at the posterior" direction; the converse —
that equality forces `q = r` — is not claimed, and can fail for weak point
hypotheses over `ℤ`.) -/
theorem freeEnergy_eq_surprise_at_posterior (L : Int → Int)
    (q0 q1 j0 j1 evidence : Int)
    (hlog0 : L j0 = L q0 + L evidence)
    (hlog1 : L j1 = L q1 + L evidence) :
    freeEnergy L q0 q1 j0 j1 = (q0 + q1) * surprise L evidence := by
  have hdecomp := freeEnergy_eq_surprise_add_relEntropy L q0 q1 q0 q1 j0 j1 evidence
    hlog0 hlog1
  rw [hdecomp, relEntropy_self_zero, Int.zero_add]

end ActiveInferenceFormalℤ
