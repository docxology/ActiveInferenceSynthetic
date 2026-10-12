# Selected formal results for the Synthetic paper

This is an exposition and verification layer over
[ActiveInferenceInstitute/fep_formal](https://github.com/ActiveInferenceInstitute/fep_formal).
The generic real-valued mathematics lives upstream in `FepSketches`.
[Positioning and methods](../docs/positioning.md) links each paper section to
its upstream carrier and explains where a transfer remains unproved.

The dependency is pinned to upstream main revision
`99276926da1df4287a2e13e9aa7f6d1822cfdca3`, with Lean/Mathlib `v4.34.1`.
`lakefile.lean` and `lake-manifest.json` record the portable Git dependency and
transitive revisions. This package has one real-valued library target.

## First build

With elan/Lake installed, from this directory:

```bash
lake exe cache get
lake build
lake env lean ActiveInferenceFormal/Audit.lean
```

The committed manifest is the dependency authority. `lake update` is a maintenance
operation for intentionally advancing the pin, not a routine reproduction step.
Lean is selected by `lean-toolchain`. Dependencies and compiled objects belong
to this checkout's `.lake/`, never a symlink into another active project.

## Source ownership

- `Geometry.lean`: selected flow orthogonality, dissipation, detailed balance,
  and entropy-production propositions from `FEP.NessFlow`.
- `Information.lean`: selected finite information, VFE, and EFE propositions.
- `Witnesses.lean`: concrete positive/boundary controls, including negative
  dissipation and disjoint-support totalized KL.
- `GaussianBlanket.lean`: canonical four-axis Gaussian fixture, native
  conditional independence, exact conditional rows and a coupled countermodel.
- `Planning.lean`: two-step Boolean history channel, terminal-preference
  normalization correction, static cumulative-objective counterexample and
  uninformative/perfect-observation witnesses.
- `Bridge.lean`: paper-to-library correspondence and its limits.
- `Audit.lean`: axiom output for every selected theorem and witness.

The wrappers retain the `ℝ_` naming convention. Numerical Python tests are
independent implementation evidence; the Lean propositions do not certify
floating-point code, biological adequacy, or a deployed agent.

The Gaussian adapter covers only the canonical precision with diagonal 4,
in the explicit external/sensory/active/internal order. It does not transfer
conditional independence to the original diagonal-2.5 numerical example.
The planning adapter covers two Boolean observations of a static Boolean
state. A history preference `c(last)/2` is normalized, so its upstream EFE is
the paper's terminal-cost/full-history-information objective plus `log 2`.
Strictly positive terminal preferences are required; impossible histories
are allowed. The static cumulative EFE theorem is not that objective:
even two fair uninformative observations give `2 log 2` rather than `log 2`.

In index order `(external, sensory, active, internal)`, the canonical fixture is

```text
K = [[4,-1,-1,0],[-1,4,0,-1],[-1,0,4,-1],[0,-1,-1,4]]
Sigma = (1/24) * [[7,2,2,1],[2,7,1,2],[2,1,7,2],[1,2,2,7]]
```

At any center `m`, conditioning on sensory/active values `(s,a)` gives
independent endpoint Gaussians with means
`m_endpoint + ((s-m_sensory)+(a-m_active))/4` and variance `1/4`.
The marginal external/internal covariance is `1/24`. The separate native
nonindependence witness has endpoint precision `[[4,1],[1,4]]` and covariance
`(1/15)*[[4,-1],[-1,4]]`.

For a fixed two-action sequence, the history likelihood is
`L(h|state)=first(state,h.first)*second(state,h.last)`. Both rows and the prior
are normalized finite laws; the history posterior is defined only when its
predictive mass is positive. The adapter accepts any normalized Boolean-history
channel, and `twoStepHistory` supplies the conditionally independent product
channel used in the paper. Fair uninformative observations yield zero mutual
information and terminal EFE `log 2`; repeated perfect observations yield
mutual information `log 2` and terminal EFE zero. The latter permits impossible
off-diagonal histories. Generic horizon lengths, observation-adaptive trees,
and a formal proof of Python's floating-point posterior-KL summation are outside
this adapter.

## Verification

From the project root, `uv run pytest tests/test_formal_lean.py` checks immutable
dependency metadata, source contracts, the real build, complete axiom output,
and real false propositions that Lean must reject. The current audit has 34
declarations; the explicit inventory in `tests/test_formal_lean.py` is the
maintained authority. `sorryAx`, missing audit
entries, and admission keywords fail the checks. Positive support and other
hypotheses remain visible rather than being inferred from theorem names.

Module instructions: [ActiveInferenceFormal/AGENTS.md](ActiveInferenceFormal/AGENTS.md).
