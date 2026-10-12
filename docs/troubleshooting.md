# Troubleshooting

## Formal dependency is unavailable

The full suite runs native checks when Lake is installed. Acquire the committed
Git dependency and Mathlib cache using [formal setup](../formal/README.md).
Numerical test collection requires no template infrastructure.

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
