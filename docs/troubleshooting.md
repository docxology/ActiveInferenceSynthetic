# Troubleshooting

## uv or the expected Python is missing

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and use Python
3.10 or newer. Run `uv sync --locked --extra dev` from the repository root.
For GitVault work, verify the mounted volume and resolved interpreter prefixes
as described in [AGENTS.md](../AGENTS.md); an external virtualenv can still point
to an internal interpreter.

## Import or lint/type tools are missing

Use `uv run` from the checkout after syncing the dev extra. Numerical users
who omitted `--extra dev` do not have the development tools installed.
Installed imports use `active_inference_synthetic`; checkout scripts use `src`.
Ruff's required version is declared in `pyproject.toml`; use the locked tool.

## Publication verification fails

The command requires the Git checkout's tracked file list. If you downloaded a
ZIP, use [the checkout workflow](quickstart.md) for this command; validate an
archived release with its supplied SHA256SUMS inventory.

A hash/size failure means the root asset differs from the recorded edition.
Compare with the [frozen release](publication.md) before intentionally changing
the manifest. A broken/untracked link or missing folder guide must be fixed in
the source tree and staged/committed before it becomes part of the tracked inventory.
Local-only output files do not make a portable link valid.

## Rendering cannot resolve figures

Regenerate with `uv run python scripts/generate_all_figures.py`, then confirm the
paths in `docs/manuscript/figure_registry.yaml` exist under `output/figures/`.
PDF/HTML rendering requires the separate template checkout and tools:
[rendering guide](rendering_pipeline.md).

## Native Lean checks are skipped or fail

Missing Lake skips native tests. Install the toolchain in `formal/lean-toolchain`
and acquire the committed dependency/cache using [formal setup](../formal/README.md).
From the project root, `(cd formal && lake build)` must succeed.
A present but incomplete Lean environment fails rather than substituting a
Python test for proof verification. Source-level formal checks still run without Lake.

## Lecture scripts cannot find recordings or assets

The clone contains authoring scripts and companions. Full replay requires the
[reproducibility ZIP](lecture.md), including frozen recordings, alignment data,
scientific inputs and the scoped LectureCreate runtime. Extract it to a fresh
directory and follow the bundle-root commands; rendering is distinct from
credentialed voice generation.

## Coverage is below the gate

```bash
uv run pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=90
```

Inspect missing branches and retained failures. Keep the threshold and negative
controls intact; correct the implementation or add an independent real control.

## The development README differs from Zenodo

The [0.6.1 archive](https://zenodo.org/records/23396307) is immutable and binds
commit `65b57d8a579834003f02ada0ff13f902e6cc6aa4`. Later `main`
documentation and tooling are recorded under Unreleased in
[CHANGELOG.md](../CHANGELOG.md). Use the archived source ZIP for exact historical
reproduction.
