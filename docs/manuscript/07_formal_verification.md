# Formal Reference and Verification {#sec:formal}

This paper supplies worked models and exposition. Its formal layer selects
real-valued results from the Institute's
[fep_formal repository](https://github.com/ActiveInferenceInstitute/fep_formal)
[@fepformal2026software; @friedman2026formalization]. Lake imports its
`FepSketches` Lean modules from the
[pinned revision](https://github.com/ActiveInferenceInstitute/fep_formal/tree/99276926da1df4287a2e13e9aa7f6d1822cfdca3)
in `formal/lakefile.lean`. Generic proofs remain upstream; Synthetic's Python
cores do not import `fep_lean`.

## Selected results and hypotheses

`ActiveInferenceFormal.Geometry` selects the flow and steady-state results;
`ActiveInferenceFormal.Information` selects finite information, VFE, and EFE
results. Their `ℝ_` theorem names correspond to the following claims:

- `ℝ_solenoidal_orthogonal` and `ℝ_flow_work_eq_dissipation`: the antisymmetric
  flow is orthogonal to the gradient, and only dissipation contributes work.
  Non-increasing work requires nonnegative dissipation.
- `ℝ_detailed_balance_iff`: zero solenoidal flow is equivalent to zero drive
  at a nonzero gradient. The gradient condition cannot be dropped.
- `ℝ_entropyProduction_nonneg` and `ℝ_entropyProduction_eq_zero_iff`: the sign
  and zero condition for the selected isotropic OU expression; the equivalence
  requires strictly positive precision and dissipation.
- `ℝ_finiteKL_nonneg`, `ℝ_finiteKL_self`, and `ℝ_finiteKL_eq_zero_iff`: finite
  information laws for the upstream normalized carriers and totalized functional.
- `ℝ_surprisal_le_VFE`, `ℝ_VFE_at_posterior`, and
  `ℝ_negative_VFE_le_logEvidence`: posterior-form VFE bounds and attainment
  for a finite generative model with positive predictive evidence.
- `ℝ_EFE_decomposition`, `ℝ_EFE_minimizer_exists`, and
  `ℝ_epistemicValue_nonneg`: the pragmatic/epistemic identity, finite-policy
  minimum, and information-gain sign for the stated upstream model.

The source signatures, rather than these summaries, own the full hypotheses.
The upstream methods and formal-kernel guides describe the carriers, assumptions,
and reviewed scope. The repository's `docs/positioning.md` provides their
section-level navigation map.

## Numerical and formal evidence

A Lean theorem checks its exact proposition under its hypotheses. A numerical
test checks implementation behavior against its references and tolerances.
Neither replaces the other. In particular, the Python KL helper rejects zero
reference mass on positive belief support, while upstream finite KL has a
real-valued totalization with different boundary behavior. Comparison requires
a common support domain and a justified carrier match.

`Witnesses.lean` retains concrete controls: a permitted zero-work case,
positive work when the nonnegative-dissipation hypothesis is violated, and
the upstream disjoint-support totalized-KL boundary. `Audit.lean` prints the
axiom footprint of every selected result and witness. The Python verification
suite invokes the real build, checks the complete audit for `sorryAx`, and asks
Lean to reject an explicit false real inequality.

## Qualified blanket and planning adapters

`GaussianBlanket.lean` matches an additional canonical four-axis precision to the
upstream native Gaussian carrier. It reuses positive definiteness, marginal
endpoint covariance, conditional product rows, and endpoint conditional independence
at every center. A supplied coupled endpoint perturbation has native non-independence.
This covers the matched canonical example in [@sec:markov-blanket], not the separate original
precision fixture or arbitrary Gaussian models.

`Planning.lean` uses Boolean observation histories as the outcome carrier. Its
normalized terminal-history preference adds the explicit constant $\ln 2$ to
the terminal-preference/history-information score. It proves predictive and
posterior mass identities, a fair-coin terminal/cumulative mismatch, and a
repeated-revealing-observation boundary. The Python implementation is compared
numerically to that mathematical carrier in `src/planning_bridge.py`.
Neither the identity nor the source-name correspondence certifies floating-point
code or general observation-contingent policy-tree optimization.

Together these adapters make the paper's transfer boundaries constructive:
state the carrier, bind an actual example, and test a condition that should
break the conclusion. The closed-loop agent and hierarchical model remain
independently tested numerical demonstrations. The paper does not establish
empirical intelligence or universal formal coverage from these examples.
