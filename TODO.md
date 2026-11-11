# Completed Synthetic improvement scope

Owner: Daniel Ari Friedman. This revision implements the bounded development
scope described in [ISA.md](ISA.md), with scientific evidence kept separate from
publication or biological adequacy claims.

- **Closed-loop agent:** an informative cue changes the next commitment;
  a matched uninformative cue leaves the posterior and tie rule unchanged.
- **Hierarchy:** exact context-state-observation prediction and joint conditioning,
  with both hidden marginals and real malformed/impossible-evidence controls.
- **Thermodynamic/informational teaching:** a dedicated interpretation section
  distinguishes VFE, EFE, physical units, drift, density, current, and assumptions.
- **Gaussian bridge:** an additional matched native four-axis carrier reuses the
  upstream Gaussian conditional-independence theorem and a coupled endpoint control.
  The original numerical precision fixture remains separately qualified.
- **Planning bridge:** a normalized two-step Boolean history channel proves the
  terminal objective's constant offset and exposes cumulative-scoring differences.
- **Paper and lecture:** the revised paper and measured twenty-minute lecture
  are distributed at the repository root and through the
  [public release](https://github.com/docxology/ActiveInferenceSynthetic/releases/tag/synthetic-public-v0.6.1).
  [Publication](docs/publication.md) and [lecture](docs/lecture.md) guides record
  the archival boundary and frozen replay inputs.

The selected additions are implemented. General learned models, arbitrary feedback
control, empirical intelligence, or a universal physical equivalence are outside
this paper's claims, rather than implied by its demonstrations. A future expansion
must name its own model and acceptance tests.

## Workflowz review — 2026-11-10

- [ ] **AIS-01 · P1 — Make probability and symmetry validation tolerances absolute.**
  - **Evidence:** `src/_prob.py:44-48` calls `np.allclose(col_sums, 1.0, atol=1e-8)` without `rtol=0`, so NumPy's default relative tolerance admits column sums roughly `1e-5` away from one despite the stated absolute tolerance. `src/markov_blanket.py:56-65` similarly checks symmetry with `atol=1e-10` but the default relative tolerance, allowing large absolute asymmetry in high-scale SPD matrices. Existing malformed-input tests use only gross errors (`tests/test_prob.py:20-24`, `tests/test_markov_blanket.py:55-57,141-143`).
  - **Outcome:** `as_column_stochastic` and `_check_spd` enforce their documented absolute tolerances, with regressions that reject a column sum of `1.00002` and a high-scale matrix whose asymmetry exceeds `1e-10`; ordinary valid fixtures and accepted floating-point roundoff remain supported.
  - **Probe:** From the repository root, run `uv run pytest tests/test_prob.py tests/test_markov_blanket.py tests/test_generative_model.py tests/test_expected_free_energy.py -q`; the new near-tolerance negative controls and all existing analytic references pass.
  - **Dependencies/constraints:** Set `rtol=0.0` at these validation gates rather than tightening the declared absolute tolerances or changing downstream formulas. Preserve the existing finite/nonnegative/SPD checks and intentional clipping semantics.

- [ ] **AIS-02 · P1 — Rebind live formal documentation and citations to the actual Lean dependency.**
  - **Evidence:** The executable dependency is `FepSketches` revision `8ac7761635d20d87790d6018495051fe5f9ad6a8` with `leanprover/lean4:v4.35.0` (`formal/lakefile.lean:7-11`, `formal/lake-manifest.json:4-13`, `formal/lean-toolchain:1`), while `formal/README.md:9-12`, `docs/positioning.md:33-45,131-139,170`, `docs/manuscript/07_formal_verification.md:7-10`, `docs/manuscript/07_thermodynamic_transfer.md:5-14`, `docs/manuscript/references.bib:92-95`, and `CITATION.cff:39-46` still name revision `99276926da1df4287a2e13e9aa7f6d1822cfdca3` and, where stated, Lean/Mathlib `v4.34.1`. `tests/test_formal_lean.py:97-117` checks Lake/manifest alignment but not these reader-facing claims.
  - **Outcome:** All live dependency links, setup prose, authored manuscript statements, and software citation metadata identify the same imported revision/toolchain; a source-contract test derives the revision from the manifest and rejects stale live references.
  - **Probe:** Run `uv run pytest tests/test_formal_lean.py tests/test_publication.py -q -rs`; new revision/documentation consistency checks and existing source/publication contracts pass. Any Lake skips remain explicit and are not counted as native proof verification.
  - **Dependencies/constraints:** Read upstream `CITATION.cff` at `8ac7761635d20d87790d6018495051fe5f9ad6a8` before changing its version, DOI, or access-date metadata; do not blindly carry forward `1.6.0`. Render and inspect changed manuscript source through the documented template pipeline. Do not overwrite the frozen root PDF/publication hashes without the successor-release procedure.

- [ ] **AIS-03 · P1 — Align Python support, lint target, and CI inventory with executable metadata.**
  - **Evidence:** `pyproject.toml:25` and `uv.lock:3` require Python `>=3.11`, and `src/value_of_information.py:73` uses Python 3.10's `zip(..., strict=True)`, but `README.md:46`, `.github/README.md:46`, `docs/quickstart.md:7`, and `docs/troubleshooting.md:5-6` still advertise 3.10. The actual CI matrix is 3.14/3.15 and setup-uv is v10.3.3 (`.github/workflows/checks.yml:19-20,27-33`), whereas `.github/workflows/README.md:7-10` and `docs/testing_philosophy.md:25-27` report 3.10/3.14 and v10.3.2. `pyproject.toml:86-88` also leaves Ruff at `target-version = "py310"` despite the 3.11 package floor; `CHANGELOG.md:13-16` repeats stale Unreleased runtime claims.
  - **Outcome:** The package floor is consistently documented as Python 3.11+, Ruff targets `py311`, the workflow guide and testing guide name the real matrix/action versions, and a metadata test prevents reader/CI drift. The GitHub homepage remains an exact rebased copy of the root README.
  - **Probe:** Run `uv run pytest tests/test_runtime_metadata.py tests/test_publication.py -q && uv run ruff check src scripts tests`; new assertions compare `requires-python`, Ruff's target, the parsed CI matrix/action version and their documentation, and all existing README-drift/link checks and lint pass.
  - **Dependencies/constraints:** Do not lower `requires-python` to 3.10 or rewrite archived release history. Update only the current Unreleased notes and live guides. Coordinate with AIS-04 if the exact 3.15 CI pin lands afterward.

- [ ] **AIS-04 · P2 — Pin the default and latest CI interpreter to Python 3.15.2.**
  - **Evidence:** `.python-version:1` currently selects floating `3.15`, and the latest CI entry is also `3.15` (`.github/workflows/checks.yml:19-20`), so otherwise identical locked runs can use different patch interpreters. The project already targets 3.15 and `uv.lock:3-6` has a distinct `>=3.15` resolution; no source/deployment constraint requiring an earlier 3.15 patch was found.
  - **Outcome:** The checkout default and latest CI entry select exactly CPython `3.15.2`, while the 3.14 compatibility job and package's `>=3.11` supported range remain intact; current runtime documentation names the exact entry.
  - **Probe:** Run `uv sync --locked --extra dev --python 3.15.2 && uv run --frozen --no-sync python -c "import sys; assert sys.version_info[:3] == (3, 15, 2); print(sys.version)" && uv run --frozen --no-sync pytest tests/test_runtime_metadata.py -q`; synchronization preserves the lock, the interpreter assertion prints 3.15.2, and metadata checks pass.
  - **Dependencies/constraints:** Land after AIS-03 to avoid conflicting documentation edits. This is an interpreter reproducibility pin, not a dependency upgrade: do not regenerate `uv.lock` or raise the package minimum solely for this change.

- [ ] **AIS-05 · P2 — Reject Boolean observation indices in the generative-model core.**
  - **Evidence:** `src/generative_model.py:82-92` accepts `bool`/`np.bool_` because they satisfy the integer check, silently interpreting `True` as observation 1 and `False` as observation 0. The sibling public entry points explicitly reject these values (`src/hierarchical_model.py:48-51`, `src/synthetic_agent.py:53-54`), and their tests include Boolean controls (`tests/test_hierarchical_model.py:37`, `tests/test_synthetic_agent.py:50`), but `tests/test_generative_model.py:205-207` covers only an out-of-range integer.
  - **Outcome:** `joint`, `evidence`, `surprise`, `posterior`, VFE, and descent consistently raise the documented `ValueError` for Python and NumPy Boolean observations while retaining valid Python/NumPy integer indices.
  - **Probe:** Run `uv run pytest tests/test_generative_model.py tests/test_hierarchical_model.py tests/test_synthetic_agent.py -q`; parametrized `True`, `False`, `np.bool_(True)`, and `np.bool_(False)` rejection tests pass alongside all existing posterior and agent controls.
  - **Dependencies/constraints:** Change only `_prepare` index validation and its shared tests; do not alter numeric observation results, bounds, or the sibling implementations.
