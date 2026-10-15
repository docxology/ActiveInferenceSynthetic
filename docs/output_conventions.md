# Output conventions

`output/` holds generated working artifacts. Regenerate derived outputs from
sources; preserve failed receipts and existing evidence until a verified
replacement permits retirement.

The root PDF and MP4 are deliberate tracked publication copies. Their hashes
are bound by [publication.json](../publication.json); committed companions live
in [media/synthetic/](../media/synthetic/README.md). Release assets and Zenodo
archives retain the corresponding frozen distribution.

| Path | Producer |
| --- | --- |
| `output/figures/*.png` | `src.figures` via `scripts/generate_*` |
| `output/pdf/*` | template render stage |
| `output/web/*` | template render stage |
| `output/reports/*` | validation and publication stages |

Stable source inputs live in `src/`, `formal/`, `data/`, and `docs/manuscript/`.
Never repair a source defect by editing a generated artifact.
