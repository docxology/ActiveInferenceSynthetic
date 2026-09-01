# Troubleshooting

## Tests cannot locate `infrastructure/`

Run from the template symlink or keep the sibling `template/` checkout beside
the private projects repository. `tests/conftest.py` supports both layouts.

## A figure command fails to import `src`

Run from the project root with `uv run`:

```bash
uv run python scripts/generate_all_figures.py
```

## Rendering cannot resolve figures

Regenerate figures, then confirm all paths declared in
`docs/manuscript/figure_registry.yaml` exist under `output/figures/`.

## Lean checks are unavailable

Install the toolchain declared by `formal/lean-toolchain`, then run:

```bash
(cd formal && lake build)
```

## Coverage is below the gate

Use the terminal-missing report:

```bash
uv run pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=90
```
