# `formal/` — AGENTS.md

Lean 4 formalization of load-bearing theorems used by the manuscript. Two
surfaces: ℝ theorems imported from the companion **fep_lean** library
(`FepSketches`, mathlib-backed), and a legacy ℤ surface proved from Lean core
alone — no `sorry` anywhere.

## Layout

Two `lean_lib` targets are declared in `lakefile.lean`, one per surface, each
with its own directory.

| File | Content |
| --- | --- |
| `lakefile.lean` | Both targets; `require FepSketches` for the ℝ surface |
| `lean-toolchain` | `leanprover/lean4:v4.33.1` (matches fep_lean) |
| `lake-manifest.json` | Resolved dependency manifest written by `lake update` |
| `ActiveInferenceFormal.lean` | Root module — imports every module of both surfaces |
| [`ActiveInferenceFormal/`](ActiveInferenceFormal/AGENTS.md) | **ℝ surface** target (below) |
| `ActiveInferenceFormal/Geometry.lean` | ℝ solenoidal orthogonality, dissipation (fep_lean) |
| `ActiveInferenceFormal/Information.lean` | ℝ Gibbs inequality, free-energy bound, EFE (fep_lean) |
| `ActiveInferenceFormal/Bridge.lean` | Python ℝ ↔ formal ℝ ↔ formal ℤ correspondence |
| `ActiveInferenceFormal/Audit.lean` | Axiom audit (`#print axioms`) over both surfaces |
| [`ActiveInferenceFormalℤ/`](ActiveInferenceFormalℤ/AGENTS.md) | **ℤ surface** target (below) |
| `ActiveInferenceFormalℤ/GeometryZ.lean` | ℤ flow identities (Lean core only) |
| `ActiveInferenceFormalℤ/InformationZ.lean` | ℤ VFE bound (Lean core only) |
| `ActiveInferenceFormalℤ/Sanity.lean` | ℤ non-vacuity witnesses (controls) |

## Build

```bash
cd formal && lake update && lake build          # both surfaces
cd formal && lake build ActiveInferenceFormalℤ  # ℤ surface alone, no dependencies
```

The ℝ surface requires the fep_lean checkout at the relative path declared in
`lakefile.lean` (`../../../ongoing/instituteos/repos/fep_lean/lean` from this
directory). The ℤ surface builds from Lean core with no dependencies.

Verified by `tests/test_formal_lean.py` when Lean is installed.

## Contract

Python cores in `src/` are the runnable demonstrations; the ℝ surface
(fep_lean) is the manuscript-canonical machine-checked spec; the ℤ surface
proves the same structural statements are algebraic. Keep all three aligned
when changing theorem statements.

## See Also

- [`ActiveInferenceFormal/AGENTS.md`](ActiveInferenceFormal/AGENTS.md) — ℝ theorem inventory
- [`ActiveInferenceFormalℤ/AGENTS.md`](ActiveInferenceFormalℤ/AGENTS.md) — ℤ theorem inventory and the non-vacuity controls
- [`README.md`](README.md) — the two-surface design and what is proved
- [`../docs/manuscript/07_formal_verification.md`](../docs/manuscript/07_formal_verification.md) — the manuscript section this backs
- [`../tests/AGENTS.md`](../tests/AGENTS.md) — `test_formal_lean.py`
