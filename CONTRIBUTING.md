# Contributing

Start with [the README](README.md), [methods](docs/methods.md), and
[AGENTS.md](AGENTS.md). Before changing a scientific claim, identify its carrier,
assumptions, source function and independent analytical or negative control.

## Set up

Use Python 3.10+ and uv in a Git checkout:

```bash
uv sync --locked --extra dev
uv run ruff check src scripts tests
uv run mypy src
uv run python scripts/verify_publication.py
uv run pytest tests/ --cov=src --cov-fail-under=90
```

Prepare [the pinned Lean environment](formal/README.md) to run native proof
checks. Missing Lake skips those checks; report the skips explicitly.
For GitVault work, follow the runtime/cache/storage bindings in the root agent guide
and preserve unrelated dirty files and evidence.

## Make a focused change

- Put numerical models in `src/`, presentation in `src/figures/`, and entry points
  in `scripts/`. Follow the nearest folder's AGENTS guide.
- Use real numerical references, files and subprocesses in tests; mocking
  frameworks are prohibited. Keep the configured 90% source coverage floor.
- Shared demonstration inputs live in `src/demos.py`; manuscript values derive
  from those sources through token hydration.
- For a new figure, update the renderer map, authored YAML registry, tests and
  figure inventories together. Regenerate the affected outputs.
- Generic mathematical results belong upstream in `fep_formal`. Paper-specific
  adapters must state their carrier and retain complete axiom checks.
- Update documentation alongside behavior. New maintained folders need both
  `README.md` and `AGENTS.md`; the publication verifier checks their presence
  and local link paths.

GitHub displays `.github/README.md` before the root README. Keep their reader
content identical, prefixing local link/image paths with `../` in the `.github`
copy. The publication verifier rejects drift; automation guidance lives in
[the workflow guide](.github/workflows/README.md).

## Validate the affected surface

```bash
uv run python scripts/generate_all_figures.py
uv run python scripts/run_teaching_experiments.py
uv build --out-dir build/distributions
```

Changes to numbered manuscript content, figure inputs or render metadata require
the separate [paper rendering and inspection workflow](docs/rendering_pipeline.md).
Changes to narration, captions or encoded media require a new verified edition;
see [lecture instructions](docs/lecture.md). A prior PDF/video hash is evidence
for its frozen bytes, not for newly edited source.

[Python CI](.github/workflows/README.md) checks supported Python endpoints,
lint, types, asset/documentation consistency, tests and package construction.
It does not install the separate Lean toolchain or render the manuscript/video.

## Report or submit

[Open an issue](https://github.com/docxology/ActiveInferenceSynthetic/issues/new)
with a minimal input, exact command, Python/tool versions, expected behavior and
actual output. Preserve the failure and avoid including credentials.

For a contribution, keep the diff focused, include checks and limitations in
the PR description, and update [CHANGELOG.md](CHANGELOG.md) under Unreleased.
Keep existing published files and tags immutable; follow
[publication instructions](docs/publication.md) for a successor archive.

The existing project license is [CC-BY-4.0](LICENSE). Preserve attribution,
upstream references and the scientific interpretation boundaries.
