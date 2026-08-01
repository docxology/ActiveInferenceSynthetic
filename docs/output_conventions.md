# Output conventions

`output/` is generated and disposable.

| Path | Producer |
| --- | --- |
| `output/figures/*.png` | `src.figures` via `scripts/generate_*` |
| `output/pdf/*` | template render stage |
| `output/web/*` | template render stage |
| `output/reports/*` | validation and publication stages |

Stable source inputs live in `src/`, `formal/`, `data/`, and `manuscript/`.
Never repair a source defect by editing a generated artifact.
