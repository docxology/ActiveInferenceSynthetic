# Script conventions

- Import a `render()` or orchestration function from `src/`.
- Keep `main()` responsible for invocation, path output, and exit behavior.
- Do not duplicate palettes, numerical constants, or scientific formulas.
- Do not mutate `sys.path`; project execution uses the installed package or
  project-root Python path.
- Print generated paths for pipeline artifact collection.
- Add a real smoke test for each new entry point.
