# `formal/` — AGENTS.md

Lean 4 formalization of load-bearing theorems used by the manuscript. Two
surfaces: ℝ theorems imported from the companion **fep_lean** library
(`FepSketches`, mathlib-backed), and a legacy ℤ surface proved from Lean core
alone — no `sorry` anywhere.

## Layout

| File | Content |
| --- | --- |
| `ActiveInferenceFormal.lean` | Root module |
| `ActiveInferenceFormal/Geometry.lean` | ℝ solenoidal orthogonality, dissipation (fep_lean) |
| `ActiveInferenceFormal/Information.lean` | ℝ Gibbs inequality, free-energy bound, EFE (fep_lean) |
| `ActiveInferenceFormal/Bridge.lean` | Python ℝ ↔ formal ℝ ↔ formal ℤ correspondence |
| `ActiveInferenceFormal/GeometryZ.lean` | ℤ flow identities (Lean core only) |
| `ActiveInferenceFormal/InformationZ.lean` | ℤ VFE bound (Lean core only) |
| `ActiveInferenceFormal/Sanity.lean` | ℤ non-vacuity witnesses (controls) |
| `ActiveInferenceFormal/Audit.lean` | Axiom audit (`#print axioms`) |

## Build

```bash
cd formal && lake update && lake build
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
