# GNN input contract

Maintain the explicit state dimensions, array orientation, normalization and
parameter meanings in `ou_regimes.md` and `finite_agent.md`. Match shared values
against `src/demos.py`; distinguish antisymmetric drive from diffusion and
probabilities from log-preferences.

After edits, run the real parser bridge with `--negative-controls`, following
[the specification guide](../../docs/gnn_specifications.md). Its receipt must bind
the parser revision and source hashes. README and AGENTS files are documentation,
not additional models. Preserve the distinction between parsing, numerical
verification, formal statements and physical interpretation.
