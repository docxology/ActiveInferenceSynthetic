# Project positioning and reuse of fep_formal

**ActiveInferenceSynthetic is a standalone paper and demonstration repository.**
Its purpose is a compact, executable introduction to Active Inference and
synthetic intelligences across equilibrium and non-equilibrium thermodynamic
and informational settings. Its contribution is a teaching synthesis: perception,
action, planning, Markov blankets, and equilibrium versus non-equilibrium flow
are worked through in numerical examples, figures, and an authored manuscript.
It owns the narrative, demonstration models, figure builders, numerical tests,
and paper metadata. The broader Free Energy Principle and Bayesian mechanics
provide the conceptual reference; selected upstream theorems make the hypotheses
inspectable. Synthetic intelligence is an application perspective, not a result
established merely by a low free-energy value or persistent probability current.
Variational/expected free energy and physical thermodynamic free energy have
different definitions and units; transfers require a model-specific argument.

[**fep_formal**](https://github.com/ActiveInferenceInstitute/fep_formal) is the
broader formal-methods repository. Its Python package and CLI are named
`fep_lean` and `fep-lean`; its Lean package is `FepSketches`. These are names for
different interfaces of the same upstream project, not three dependencies.
Upstream owns reusable mathematical carriers, theorem implementations,
assumption reviews, catalogue relations, and their verification workflows.

The relationship is **a focused scientific exposition building on a general
formal library**. This paper can develop on its own publication schedule while
attributing reused results to upstream. Running its Python demonstrations needs
neither the upstream Python package nor Lean. Its real-valued Lean exposition
has an external dependency; PDF/HTML production currently uses the research
template. [STANDALONE.md](../STANDALONE.md) separates these execution surfaces.

## Where to start upstream

The following guides are revision-bound to the formal dependency used here.
The repository landing page provides the evolving current documentation:

- [Documentation map](https://github.com/ActiveInferenceInstitute/fep_formal/blob/99276926da1df4287a2e13e9aa7f6d1822cfdca3/docs/README.md): navigation across methods, formalization, validation, and research programs.
- [Mathematical methods](https://github.com/ActiveInferenceInstitute/fep_formal/blob/99276926da1df4287a2e13e9aa7f6d1822cfdca3/docs/mathematical-methods.md): portable `fep_lean.methods` inspection, exact theorem statements, boundary probes, and transfer rules.
- [Formal-kernel methods](https://github.com/ActiveInferenceInstitute/fep_formal/blob/99276926da1df4287a2e13e9aa7f6d1822cfdca3/docs/formal-kernel-methods.md): normalized carriers, support conditions, foundation versus composition ownership, and validation tiers.
- [Lean workspace](https://github.com/ActiveInferenceInstitute/fep_formal/blob/99276926da1df4287a2e13e9aa7f6d1822cfdca3/docs/lean4.md): pinned Lean/Mathlib setup and canonical-source projection.
- [Theorem maturity audit](https://github.com/ActiveInferenceInstitute/fep_formal/blob/99276926da1df4287a2e13e9aa7f6d1822cfdca3/docs/theorem-maturity-audit.md): semantic scope beyond a successful compilation.
- [Getting started](https://github.com/ActiveInferenceInstitute/fep_formal/blob/99276926da1df4287a2e13e9aa7f6d1822cfdca3/docs/getting-started.md): separate offline inspection, native verification, and full workflows.

These guide links are pinned to the dependency used by the paper. The repository
landing page follows upstream development. A reused result must record its exact
source revision and qualified declaration; a moving documentation link is not
a proof receipt.

## Section-to-method map

The local wrappers are [Geometry.lean](../formal/ActiveInferenceFormal/Geometry.lean)
and [Information.lean](../formal/ActiveInferenceFormal/Information.lean), with
[GaussianBlanket.lean](../formal/ActiveInferenceFormal/GaussianBlanket.lean) and
[Planning.lean](../formal/ActiveInferenceFormal/Planning.lean) as qualified
paper-specific carrier adapters.
Upstream canonical Lean sources live under `src/fep_lean/formal/`; their
`lean/FepSketches/` counterparts are generated build inputs.

- **Perception (authored source section):** `src/generative_model.py` demonstrates posterior updating
  and VFE. Existing wrappers select `FEP.FiniteInformation` and
  `FEP.ActiveInference` results from `finite_probability.lean`,
  `finite_information.lean`, and `active_inference.lean`. Preserve normalization,
  positive evidence, and support hypotheses when matching the Python model.
- **Flow and steady state (authored source section):** `src/free_energy_flow.py`,
  `src/trajectories.py`, and `src/steady_state.py` demonstrate the isotropic OU
  case. Existing wrappers select `FEP.NessFlow` results in `ness_flow.lean`.
  The zero-current equivalence needs a nonzero gradient; the zero-entropy-production
  equivalence needs strictly positive precision and dissipation. RK4 output is
  numerical evidence, not a proof of exact trajectories.
- **Action (authored source section):** `src/expected_free_energy.py` illustrates pragmatic and
  epistemic value. Existing wrappers select the EFE decomposition, finite-policy
  minimizer, and epistemic nonnegativity from `active_inference.lean`. A finite
  minimizer theorem does not prove the correctness of the local softmax code.
- **Markov blanket (authored source section):** the original precision fixture remains numerical.
  A second canonical fixture matches the pinned upstream four-axis native
  Gaussian model; the adapter transports the exact precision and reuses native
  conditional independence, covariance, product conditional rows, and a coupled
  endpoint non-independence witness. It does not certify every precision zero.
- **Planning (authored source section):** the local objective uses terminal preferences and history
  mutual information. Its two-step Boolean history channel matches upstream
  one-step EFE after an explicit constant normalization offset. Controls show
  why summing stage EFE or repeatedly counting perfect information is different.
  General feedback-tree optimization is not claimed for the local sequence code.
- **Closed-loop agent (authored source section):** a separate finite environment supplies cue and
  commitment channels; real informative versus uninformative observations
  distinguish an observation-sensitive decision from a fixed tie rule.
- **Hierarchy (authored source section):** exact context-state-observation inference demonstrates
  downward prediction and upward joint conditioning, independently tested here.
- **Interpretation (authored source section):** physical and informational units, diffusion
  assumptions, and the conditions needed for a mathematical transfer.

In particular, Python's `src/_prob.py` rejects zero reference mass on positive
belief support. Upstream finite KL has an explicitly real-valued totalization
with different behavior outside that support domain. A shared name does not
justify transferring zero-support claims between them.

## Orchestrating methods for this paper

Keep mathematical discovery and proof verification separate. In a prepared
upstream checkout, the following read-only inspection commands expose the
selected live contracts:

```bash
# cwd: fep_formal checkout; use its own locked validator environment
uv run --locked fep-lean --project-root . methods inspect --topic fep-001
uv run --locked fep-lean --project-root . methods analyze fep-001
uv run --locked fep-lean --project-root . methods probe
```

`fep-001` is an inspection starting point, not a blanket citation for every
section. Select the exact topic and qualified theorem for each claim using the
methods guide. Inspection and numerical boundary probes do not compile a proof.
The standalone paper does not require Hermes, OpenGauss, provider credentials,
or the upstream full pipeline for its numerical demonstrations.

For each proposed reuse:

1. Record the paper section, local model/function, upstream commit, canonical
   module, qualified declaration, carrier, and required hypotheses in a reviewable
   claim binding. Identify which local example satisfies each hypothesis.
2. Use the methods interface to inspect the contract and scope. Compare codomains,
   support conventions, matrix orientation, and policy semantics explicitly.
3. Keep generic proofs upstream and manuscript exposition in this repository.
   Add a local adapter only for the chosen model; qualify a new mathematical
   transfer with a theorem rather than treating an import as a bridge.
4. Run a real example and a counterexample to a necessary hypothesis. Then build
   the local wrappers against the selected upstream revision and inspect their
   axiom audit. Retain failures alongside the passing evidence.
5. Generate figures and hydrate manuscript values here; render through the
   template. Record Python, Lean, and rendered-paper evidence separately.

## Pinned alignment with upstream main

The formal dependency selects upstream main revision
`99276926da1df4287a2e13e9aa7f6d1822cfdca3` through a portable Git dependency
in [lakefile.lean](../formal/lakefile.lean). The
[manifest](../formal/lake-manifest.json) locks its transitive dependencies, and
[lean-toolchain](../formal/lean-toolchain) selects `v4.34.1`, matching that
revision's Lean/Mathlib workspace. This project's `.lake/` is isolated from
neighboring worktrees. Python test collection also runs without the template.

The formal layer contains one real-valued exposition target with two qualified
carrier adapters. Local concrete
witnesses retain positive-work and support-boundary controls; generic mathematical
proofs and broader non-vacuity evidence remain upstream. It does not maintain a
second carrier or a copy of the generic library.

To advance the alignment:

1. Resolve upstream `main` to an immutable commit. Inspect its canonical module
   signatures, semantic review, and Lean/Mathlib pins; do not consume uncommitted
   work from a neighboring checkout.
2. Update the dependency revision and local toolchain together. Run `lake update`
   as an intentional maintenance step and review the resulting manifest.
3. Acquire the matching Mathlib cache in this project's workspace, run the real
   build and complete axiom audit, and retain boundary controls.
4. Run the Python suite with its coverage gate, generate figures and hydrated
   manuscript values, and review any changed scientific correspondence.
5. Regenerate and inspect the rendered paper separately before publication.

[Formal setup](../formal/README.md) documents reproduction from the committed
manifest. Main-branch alignment is a pinned snapshot with evidence; it is not
permission to follow upstream changes automatically.


## Interfaces and optional GNN specification

| Project | What Synthetic uses | Reader entry point |
| --- | --- | --- |
| Synthetic | Numerical teaching models and standalone paper | Installed `active_inference_synthetic`; local checkout scripts use `src` |
| [fep_formal](https://github.com/ActiveInferenceInstitute/fep_formal) | Direct Lean dependency on pinned `FepSketches` modules | [Pinned citation metadata](https://github.com/ActiveInferenceInstitute/fep_formal/blob/99276926da1df4287a2e13e9aa7f6d1822cfdca3/CITATION.cff); upstream Python `fep_lean` and CLI `fep-lean` are optional inspection interfaces |
| [Generalized Notation Notation](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation) | Optional upstream parser validates authored specifications against Synthetic parameters; no GNN backend execution | [Reviewed README](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation/blob/9255e19f951d4c9c1461514464d420bd3fc8b912/README.md) and [citation metadata](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation/blob/9255e19f951d4c9c1461514464d420bd3fc8b912/CITATION.cff) |
| [docxology/template](https://github.com/docxology/template) | Manuscript hydration, PDF/HTML rendering, and validation | [Local reproduction steps](rendering_pipeline.md) |

GNN describes models in a structured text format. The optional parser bridge
now checks the authored OU and cue/bet specifications against exact demo values
and selected dimensions, with real failing controls. It records the parser
revision and hashes separately from the cited software archive. Backend execution
still requires an explicit semantic adapter and comparisons to analytic references.
See [GNN specifications](gnn_specifications.md); installing GNN is unnecessary
for the ordinary numerical demonstrations.

## Citation identities

The manuscript bibliography cites both software repositories and their scholarly
references. FEP_Formal uses Daniel Ari Friedman's software metadata and preferred
article citation from the exact imported revision. Its software DOI is
`10.5281/zenodo.23196891`; its preferred article DOI is
`10.5281/zenodo.23220027`. These identify different scholarly objects.
GNN's founding article is by Jakub Smékal and Daniel Ari Friedman (2023),
`10.5281/zenodo.7803328`; the software concept DOI is
`10.5281/zenodo.7803313`. The reviewed GNN source is commit
`9255e19f951d4c9c1461514464d420bd3fc8b912` with version metadata 4.1.0. Its
concept DOI is not presented as a version-specific archive. Source inspection
for these links and citation fields was performed on 2026-10-11.


## Actual Lean import examples

The local formal wrappers import the following case-sensitive upstream modules:

```lean
import FepSketches.ness_flow
import FepSketches.finite_probability
import FepSketches.finite_information
import FepSketches.active_inference
import FepSketches.gaussian_precision_conditioning
```

Lake resolves these modules from the immutable Git revision in
`formal/lakefile.lean`; they are not Python imports. The Gaussian and planning
adapters select model-specific results from these modules. Reproduce them
with `lake build` from `formal/` and inspect `ActiveInferenceFormal.Audit`.
GNN's installed Python namespace is `gnn`, as documented by its own repository;
there is no corresponding `import gnn` in Synthetic's numerical cores.
