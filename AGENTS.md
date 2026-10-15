# ActiveInferenceSynthetic

Public educational paper, numerical demonstrations, formal adapters, and narrated
lecture. Read [README.md](README.md) for the reader workflow and
[docs/positioning.md](docs/positioning.md) before changing mathematical scope.

## Ownership and sources

- `src/`: deterministic numerical cores; `src/figures/`: presentation only.
  Core mathematics belongs outside scripts and never imports template infrastructure.
- `scripts/`: figure, hydration, experiment, and optional GNN entry points.
  Publication verification checks files and documentation rather than scientific models.
- `formal/`: paper adapters over pinned upstream `FepSketches`; generic proofs
  belong in `fep_formal`. Preserve carriers, hypotheses, and complete axiom checks.
- `docs/manuscript/`: authored paper sections and render metadata.
- `data/`: claim ledger and authored GNN inputs.
- `media/`: frozen lecture edition and companions. Read its nested guides before editing.
- `output/`: generated working outputs; preserve existing evidence until replacement
  validation succeeds. Root PDF/video are deliberate versioned publication copies.

Each maintained folder has a `README.md` and `AGENTS.md`. Follow the nearest
guide when changing that folder. The figure registry in
`src/figures/render_all.py` and the authored YAML registry must agree.

## Verification

Run from the repository root:

```bash
uv sync --locked --extra dev
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/generate_all_figures.py
uv run python scripts/run_teaching_experiments.py
uv run python scripts/verify_publication.py
```

The full suite includes real Lean builds and false-proposition controls when
Lake is present. Report missing-tool skips explicitly; they do not verify proofs.
Formal setup: [formal/README.md](formal/README.md).
Use real files, numerical references, and subprocesses; mocking frameworks are prohibited.
The locked dev extra supplies lint/type tools and YAML stubs:
`uv run ruff check src scripts tests` and `uv run mypy src`.
Ruff is pinned to the original template's 0.15.21 toolchain; advancing the
linter is an explicit maintenance change rather than a silent default-rule change.

On GitVault, bind the Python environment, interpreter, temporary directory, uv
cache, and matplotlib cache to the mounted SSD. Verify resolved `sys.prefix`
and `sys.base_prefix` before Python source work; retain the existing environment
and dirty files when creating an isolated verification environment.

## Publication

[docs/publication.md](docs/publication.md) owns release/version distinctions and
the upload procedure. `publication.json` binds the root deliverables to their
hashes and archived lecture edition. `SHA256SUMS.txt` is the human-readable copy.
Verify both before upload; download published assets anonymously and compare hashes.
Create a successor Zenodo version while retaining earlier published records.

Scientific package/manuscript version is `0.5.0`. Public distribution version
`0.6.1` refreshes documentation and packages the revised paper and existing
`edition_v15` lecture; it introduces no new scientific result.
