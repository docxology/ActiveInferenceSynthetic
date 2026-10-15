# Forking guide

1. Fork the public repository under a new qualified name and clone it once
   into the appropriate local visibility folder. Use worktrees for parallel work.
2. Replace manuscript metadata and citations.
3. Replace `src/demos.py` constants and scientific cores as required.
4. Keep reusable validation and model boundaries explicit.
5. Replace or extend figures in `src/figures/`; update `render_all.py`.
6. Add real tests before changing manuscript claims.
7. Update the Lean side-spec when formalized claims change.
8. Run tests, type checks, figure generation, and rendering.

Give the fork its own repository, citation metadata, release identity, and
artifact hashes. Template links are optional rendering inputs; private projects
require their own explicit publication authorization.
