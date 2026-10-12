# Discussion: Informational and Thermodynamic Interpretation {#sec:interpretation}

The demonstrations connect several mathematical settings without identifying
their free energies merely by name. Variational free energy is a functional of
a recognition distribution and a generative model; with natural logarithms it
is measured in nats. Expected free energy scores predicted outcomes and states
under a policy, with pragmatic and epistemic terms in the same informational
units. Thermodynamic free energy is an energy quantity, measured in joules.
A relation between these objects requires a stated physical model and scaling.

## Equilibrium and stationary circulation

The OU example fixes a Gaussian stationary density and a matched-noise
fluctuation-dissipation convention. Zero solenoidal drive gives detailed
balance. Nonzero drive gives a divergence-free stationary probability current
and positive entropy production for positive precision and dissipation.
The deterministic drift trajectory still relaxes; it is not a perpetual orbit.
Equilibrium's zero probability current also does not imply zero microscopic
stochastic motion [@dacosta2021bayesian; @friston2023bayesian].

The Gaussian landscape used in the drift is dimensionless. Under an explicit
Gibbs model it can be related to an energy landscape through
$F(x)=U(x)/(k_{\mathrm B}T)+\mathrm{constant}$, with temperature in kelvin.
For an isothermal physical interpretation using the corresponding local
thermodynamic assumptions, an informational entropy-production rate $\sigma$
can be scaled to $k_{\mathrm B}\sigma$ and dissipated power to
$k_{\mathrm B}T\sigma$. The code does not estimate temperature, friction,
physical work, or metabolic expenditure from data. The conversion is conditional
on a physical interpretation, not an empirical result of the numerical figure.

## Statistical boundaries and synthetic agents

A Gaussian precision zero is a conditional-independence statement under the
Gaussian law. It does not by itself specify causal channels, action effects,
model learning, or agency. The finite closed-loop example supplies a separate
explicit perception-action carrier, while the hierarchy supplies a separate
multi-level inference carrier. A shared vocabulary is a guide to comparison;
transporting a theorem requires compatible carriers and hypotheses.

Bayesian mechanics provides a framework for relating probabilistic dynamics,
statistical boundaries, and belief interpretation [@ramstead2023bayesian].
The Free Energy Principle supplies the broader organizing perspective
[@friston2010fep]. These worked examples introduce that perspective while
keeping its assumptions visible. They do not establish that every persistent
current is intelligent, every conditional-independence partition is an agent,
or every informational objective is a measured physical free energy.

The intended next use is reproducible exploration: change a channel, a preference,
a precision entry, or a drive parameter; rerun the tests and figures; and inspect
which conclusion survives. For deeper mathematics, the pinned `fep_formal`
methods and formal-kernel documentation provide the declarations, support
conventions, and scope reviews used by this paper's exposition.


## Reading and reusing the Institute repositories

Synthetic supplies the worked teaching models and paper. The Institute's
[fep_formal](https://github.com/ActiveInferenceInstitute/fep_formal) provides
the pinned mathematical reference used in [@sec:formal]
[@fepformal2026software; @friedman2026formalization].
Its `FepSketches` Lean interface is the actual formal dependency; `fep_lean`
and `fep-lean` are upstream Python and command-line interfaces for readers
who want to inspect the broader catalogue.

[Generalized Notation Notation (GNN)](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation)
is a complementary language and toolchain for specifying generative models
[@smekal2023gnn; @gnn2026software]. It is relevant when moving these explicit
priors, likelihoods, preferences, and state variables into a shareable model
specification. The software citation identifies the reviewed
[GNN source snapshot](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation/tree/9255e19f951d4c9c1461514464d420bd3fc8b912).
Synthetic constructs its runtime arrays directly. The optional specification
bridge now parses two authored GNN files with the upstream parser and checks
their parameters and dimensions against those arrays and the OU model
([@sec:thermodynamic-transfer]). It does not execute a GNN simulation backend.
Execution would require further mapping of channel orientation, observations,
preferences, time stepping and control assumptions, with output equivalence
and boundary tests. A GNN representation does not itself certify an upstream
Lean theorem or a thermodynamic interpretation.

The numerical distribution installs as `active_inference_synthetic`;
checkout scripts retain their local `src` imports. Readers can reproduce
the finite models independently of either upstream Python package.
The repository's positioning guide separates mathematical reuse, model
specification, and template-based manuscript rendering, with revision-bound
links and citation metadata for each upstream project.
