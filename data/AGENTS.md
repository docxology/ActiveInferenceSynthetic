# Data Directory — Agent Guide

Versioned project **inputs** only. Pipeline outputs must not be committed here.

## `claim_ledger.yaml`

Evidence-registry for manuscript claims that are intentionally sourced from code, examples, or generated reports rather than `{{VARIABLE}}` injection.

### Schema (preserve when adding rows)

Top-level `claims` holds records with unique `claim_id`, `kind`, `value`,
`source`, `source_tier`, `freshness`, `artifact_path`, and optional `note`.
Measured inventory counts should be queried from the YAML rather than copied
into this guide. Derived values must identify the numerical source and the
behavioral test; artifacts belong in `output/`, not here.

## GNN inputs

Read [gnn/AGENTS.md](gnn/AGENTS.md) before changing model specifications.
Use the upstream parser bridge and its wrong-parameter/dimension controls;
parsing does not establish backend equivalence.

## Edit protocol

1. Edit only when manuscript claims, figure defaults, or source-backed numeric facts change.
2. Re-run evidence validation / pipeline stages that consume the ledger.
3. Do not store generated CSV/JSON/PNG under `data/`.

Quick orientation: [`README.md`](README.md).
