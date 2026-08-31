# Scripts

Thin command-line entry points over `src/`.

```bash
uv run python scripts/generate_all_figures.py
uv run python scripts/z_generate_manuscript_variables.py
uv run python scripts/generate_overview_figure.py
```

`generate_all_figures.py` prints the seven generated paths. Per-figure wrappers
delegate to the corresponding `src.figures` module. `00_preflight.py` invokes
the template manuscript preflight.

See [AGENTS.md](AGENTS.md) and [CONVENTIONS.md](CONVENTIONS.md).
