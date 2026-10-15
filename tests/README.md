# Tests

Real-computation test suite covering every scientific module, the figure
builders, the script wrappers, project paths, and the Lean formal layer.

## Quick start

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90   # from the project root
uv run pytest tests/test_steady_state.py -q          # one file
```

## Key features

- **No mock frameworks.** Every assertion runs real numerics, writes real PNGs,
  or shells out to a real tool.
- **Coverage floor of 90%** on `src/`, enforced by the command above.
- **Isolated output.** Figure tests monkeypatch
  `src.project_paths._DEFAULT_ROOT` to a `tmp_path`, so a run never writes into
  the real `output/` tree.
- **Formal layer included.** `test_formal_lean.py` audits the Lean sources for
  `sorry`/`admit` and runs a real `lake build` when Lake is on PATH. Missing Lake skips native checks; report those skips
  explicitly and prepare the pinned toolchain for full proof verification.

## Layout

| File | Role |
| --- | --- |
| `conftest.py` | Headless matplotlib; adds project root and `src/`, independent of template |
| `test_*.py` | One file per module or script group — see [AGENTS.md](AGENTS.md) |
| [`PATTERNS.md`](PATTERNS.md) | Test conventions |

## More information

See [AGENTS.md](AGENTS.md) for the test-to-module map and the conftest path
resolution, and [`../docs/testing_philosophy.md`](../docs/testing_philosophy.md)
for why the suite is built this way.
