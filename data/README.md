# Project data

Project-maintained inputs for the Active Inference overview.

## Quick reference

| File | Role |
| --- | --- |
| `claim_ledger.yaml` | Source-backed numeric, vector, and string claims for evidence validation, grouped by the figure each supports |

[`gnn/`](gnn/README.md) contains the authored optional GNN specifications.
Query the YAML for the current ledger count. Generated analysis outputs belong under `output/`
during pipeline runs, not in `data/`.

Claims are the *code-sourced* counterpart to the manuscript's `{{TOKEN}}`
values: tokens are injected into prose by
[`../src/manuscript_variables.py`](../src/manuscript_variables.py), while ledger
rows register facts that live in code or in a generated artifact.

Schema and edit protocol: [`AGENTS.md`](AGENTS.md).
