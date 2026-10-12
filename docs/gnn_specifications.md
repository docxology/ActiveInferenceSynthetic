# GNN specifications and thermodynamic transfer

The versioned [OU specification](../data/gnn/ou_regimes.md) declares the
equilibrium and driven alternatives over the same stationary Gaussian density.
The [finite-agent specification](../data/gnn/finite_agent.md) declares cue/bet
channels, prior and preferences. These are authored GNN model inputs.

Validate them through the real upstream parser from a GNN-enabled environment:

```bash
uv run --project "$GNN_ROOT" --frozen python scripts/validate_gnn_specifications.py \
  --gnn-root "$GNN_ROOT" --negative-controls
```

`GNN_ROOT` is the user's local GNN checkout. The script compares parsed values
and dimensions to Synthetic's tested demo arrays, records the upstream revision
and parser-file hashes in `output/data/gnn_specifications.json`, and confirms
that wrong dissipation or state dimension fails. The checked parser revision
on 2026-10-12 was `d20b76a5486592b1e7ee8a36029cea0f14c4f052`; this provenance
does not replace the cited older GNN software snapshot.

`Q_ou` is antisymmetric drive, not process-noise covariance. `C_probs` contains
normalized probabilities, not the log-preferences accepted by some backends.
The explicit conversions and orientation matter. Parsing is not backend
simulation, proof certification or physical calibration.

The new Lean `Thermodynamics.lean` imports finite path KL nonnegativity and
a supported integral fluctuation identity from the existing pinned FEP_Formal.
Its normalized finite path carrier is distinct from continuous OU path measures.
The manuscript's equilibrium-concepts and thermodynamic-transfer sections
explain stationarity, current, parity, support and physical interpretation.
