# Script conventions

- Import a `render()` or orchestration function from `src/`.
- Keep `main()` responsible for invocation, path output, and exit behavior.
- Do not duplicate palettes, numerical constants, or scientific formulas.
- Use the standard project-root bootstrap and nothing else:
  `sys.path.insert(0, str(Path(__file__).resolve().parent.parent))` before the
  `src` import, so a script runs directly whether or not the package is
  installed. Every `generate_*_figure.py` and `generate_all_figures.py` uses
  exactly this line; `z_generate_manuscript_variables.py` binds the same path to
  `_PROJECT_ROOT` and inserts that, because it reuses the value. Do not invent
  other `sys.path` manipulation. (`00_preflight.py` is not a `src` consumer — it
  locates and inserts the template repo root instead.)
- Print generated paths for pipeline artifact collection.
- Add a real smoke test for each new scientific entry point.
- `validate_gnn_specifications.py` and `verify_publication.py` are operational
  validators: external parser checks and publication file checks belong here;
  numerical models remain in `src/`.
