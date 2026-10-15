# Paper exposition modules

`Geometry.lean`, `Information.lean`, and `Thermodynamics.lean` re-export selected real-valued
`FepSketches` theorems under `ActiveInferenceFormal`. Keep their `ℝ_` names
stable and retain upstream hypotheses. `Witnesses.lean` supplies concrete
boundary cases. `GaussianBlanket.lean` transports the canonical four-axis
precision; `Planning.lean` represents two-step Boolean observation histories
with the terminal-preference normalization correction. Before changing either
adapter, read its qualified declaration map in [README.md](README.md) and the
exact carriers in [../README.md](../README.md). `Bridge.lean` documents numerical
correspondence; `Audit.lean` prints every selected axiom footprint.

Before adding a result, inspect the upstream canonical declaration and reviewed
scope using [the methods guide](../../docs/positioning.md). New generic proofs
belong in `fep_formal`; paper-specific adapters require an explicit justified
carrier match. Include the declaration in the audit and source/native tests.
No admissions or assumed replacement axioms are allowed.

Build and run axiom inspection as documented in [../README.md](../README.md).
The full suite must reject a false Lean proposition and incomplete audit output.
