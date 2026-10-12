# Thermodynamic Proof Imports and GNN Specifications {#sec:thermodynamic-transfer}

## What is actually imported from FEP_Formal

The immutable `FepSketches` dependency remains revision `99276926` of
`ActiveInferenceInstitute/fep_formal`. `Geometry.lean` imports `ness_flow`:
solenoidal orthogonality, the dissipative work identity, a pointwise
zero-drive equivalence away from a zero gradient, and the isotropic entropy-rate
algebra. These are real-valued propositions. They do not constitute a proof of
an SDE's invariant measure, a general detailed-balance theorem or a measured
physical heat rate [@fepformal2026software; @friedman2026formalization].

This revision also imports `FepSketches.path_thermodynamics` in
`Thermodynamics.lean`. Its carrier is a pair of **normalized finite path laws**
with an involutive reversal and a reverse law aligned to forward coordinates.
Synthetic re-exports nonnegative path KL and, with strictly positive forward
and reverse support, the integral fluctuation identity

\begin{equation}
\Sigma(\tau)=\ln\frac{P(\tau)}{P^{\mathrm R}(\tau)},
\qquad \mathbb E_P[\exp(-\Sigma)]=1.
\end{equation}

This identity follows from normalization and the supported likelihood ratio.
Interpreting $\Sigma$ as physical entropy production additionally requires the
correct physical reverse protocol and local thermodynamic assumptions
[@seifert2012stochastic]. The finite theorem is not asserted to be the continuum
OU rate theorem: the path carrier, measure, support and time limit differ.
Lean's totalized real logarithm at zero is not an infinite entropy production;
the full-support hypotheses must remain visible. Upstream documentation and
the paper's positioning guide distinguish these contracts.

## A concrete GNN representation of both settings

Two versioned model inputs now accompany the paper:
`data/gnn/ou_regimes.md` describes the matched-density continuous process, and
`data/gnn/finite_agent.md` describes the finite cue/bet observation channels
[@smekal2023gnn; @gnn2026software]. The continuous file declares dimension,
precision, dissipation, the zero/driven alternatives, diffusion, density,
current, time convention and equations. `Q_ou` denotes the antisymmetric
drive; it must not be confused with the process-noise covariance called `Q`
by some continuous-model interfaces. The finite file declares outcome-by-state
likelihoods, prior, normalized preferences and their logarithmic conversion.
It keeps the state static and does not introduce an adaptive payout.

| GNN declaration | Synthetic carrier | Required interpretation |
| --- | --- | --- |
| `x[2]`, `P_ou`, `Gamma_ou`, `Q_ou`, `D_ou` | `IsotropicOU` and stationary-current functions | Continuous even coordinates; $D=\Gamma$; $\gamma,\Pi>0$ for diffusion |
| `A_cue`, `A_bet`, `D` | Action likelihood arrays and belief | Outcome rows, state columns; normalized columns and prior |
| `C_probs`, `C_log` | Preference law and expected log-preference | Positive normalized preference law; natural logs in nats |
| `Equations`, `Time` | Authored semantic specification | Syntax does not implement an SDE solver or an EFE backend |

The optional `scripts/validate_gnn_specifications.py` invokes the upstream
Markdown GNN parser, verifies exact demo parameters and selected dimensions,
records parser source hashes and revision, and rejects altered dissipation or
state dimension as real negative controls. The parser provenance is separate
from the older cited GNN software snapshot. Run it in an environment with the
GNN parser available, passing `--gnn-root` explicitly. The normal Synthetic
Python package remains independent of that optional environment.

Parsing a specification, evaluating its declared equations, executing a target
backend and establishing a theorem correspondence are four separate checks.
This bridge establishes the first and its parameter/dimension correspondence
to the tested examples. It does not claim that a generic GNN backend executes
the OU diffusion or shares Synthetic's policy-scoring convention. A future
execution bridge must compare matrices, time discretization, state parity,
support, reversal and outputs before inheriting any conclusion.
