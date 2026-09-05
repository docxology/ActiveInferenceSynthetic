# Data Directory — Agent Guide

Versioned project **inputs** only. Pipeline outputs must not be committed here.

## `claim_ledger.yaml`

Evidence-registry for manuscript claims that are intentionally sourced from code, examples, or generated reports rather than `{{VARIABLE}}` injection.

### Schema (preserve when adding rows)

Top-level key `claims:` holds a list of records. As of this writing there are
**26**, grouped by comment banner into the figure each belongs to.

| Field | Purpose | Values in use |
| --- | --- | --- |
| `claim_id` | Stable identifier | kebab-case, unique |
| `kind` | Claim category | `number`, `vector`, `string` |
| `value` | Declared numeric or textual value | — |
| `source` | Provenance (module, symbol, call) | `src/…` paths |
| `source_tier` | Trust tier for validation | `project_source` (a literal constant), `derived` (computed by a core) |
| `freshness` | Staleness policy | `active` |
| `artifact_path` | Path to the backing figure | one of the seven `output/figures/*.png`; present on all 26 current rows |
| `note` | Optional prose: caveats and the test that verifies the value | free text; on 10 rows today |

Current distribution: 23 `number`, 2 `string`, 1 `vector`; 14
`project_source` against 12 `derived`; every row `freshness: active`.

`source_tier: derived` rows should name the test that pins the value — 9 of the
12 already do, in `note`.

## Edit protocol

1. Edit only when manuscript claims, figure defaults, or source-backed numeric facts change.
2. Re-run evidence validation / pipeline stages that consume the ledger.
3. Do not store generated CSV/JSON/PNG under `data/`.

Quick orientation: [`README.md`](README.md).
