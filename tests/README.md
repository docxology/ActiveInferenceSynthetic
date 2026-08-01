# Tests

The suite covers every scientific module, figure builders, script wrappers,
project paths, and the Lean formal layer.

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
```

Tests use real arrays, generated PNGs, temporary directories, and real Lean
commands. See [AGENTS.md](AGENTS.md) for the module map and
[PATTERNS.md](PATTERNS.md) for test conventions.
