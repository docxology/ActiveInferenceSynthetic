# Workflow edit contract

Preserve the configured source coverage floor and real negative controls.
Show test skips in output and keep native Lean verification distinct from the
hosted Python job. Changing job labels must preserve this scope.

Pin actions to full commit hashes and document their human-readable release
versions. Use `uv sync --locked` and `uv run --frozen --no-sync` so checks do not
silently rewrite dependency resolution. Include package construction and an
isolated wheel import/behavior check after packaging changes.

Run affected commands locally and observe the hosted run at the exact pushed
commit. Retain failed runs and fix the cause; changing a gate to hide a failure
does not establish correctness.
