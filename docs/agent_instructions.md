# Agent instructions

1. Keep scientific and rendering logic in `src/`; scripts are entry points.
2. Use `IsotropicOU` for shared `precision`, `gamma`, and `omega` semantics.
3. Keep demonstration constants in `src/demos.py`.
4. Add real numerical tests; do not use mock frameworks.
5. Preserve the distinction between deterministic drift and stationary
   probability current in code, figures, and prose.
6. Keep Python demonstrations and Lean theorem statements aligned.
7. Treat `output/` as generated; regenerate rather than hand-editing it.
8. Use `uv run` for Python commands.

Before completion, run the verification commands in [`AGENTS.md`](AGENTS.md).
