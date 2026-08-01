# Forking guide

1. Copy the project into the private sidecar under a new qualified name.
2. Replace manuscript metadata and citations.
3. Replace `src/demos.py` constants and scientific cores as required.
4. Keep reusable validation and model boundaries explicit.
5. Replace or extend figures in `src/figures/`; update `render_all.py`.
6. Add real tests before changing manuscript claims.
7. Update the Lean side-spec when formalized claims change.
8. Run tests, type checks, figure generation, and rendering.

Do not publish the private sidecar tree through the public template repository.
