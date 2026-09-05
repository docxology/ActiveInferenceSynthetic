# Scripts

Thin command-line entry points over `src/`. All numerics live in `src/`; nothing
here computes or draws.

## Quick start

Run from the project root:

```bash
uv run python scripts/generate_all_figures.py
uv run python scripts/z_generate_manuscript_variables.py
uv run python scripts/generate_overview_figure.py
```

## What each does

- `generate_all_figures.py` — renders all seven figures, prints their paths,
  then writes `output/data/manuscript_variables.json` and hydrates
  `output/manuscript/`.
- `generate_*_figure.py` — one figure each, delegating to the matching
  `src.figures` module and printing the path.
- `z_generate_manuscript_variables.py` — variables and manuscript hydration
  only; prefers the template injector when importable, falls back to the
  standalone hydrator.
- `00_preflight.py` — manuscript preflight; needs the template checkout and
  exits `2` without it.

## More information

See [AGENTS.md](AGENTS.md) for the file inventory, the import bootstrap, and how
to add a figure; [CONVENTIONS.md](CONVENTIONS.md) for the rules every script
follows.
