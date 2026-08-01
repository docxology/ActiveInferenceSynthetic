# `formal/` — AGENTS.md

Lean 4 formalization of load-bearing theorems used by the manuscript. No mathlib,
no `sorry`.

## Layout

| File | Content |
| --- | --- |
| `ActiveInferenceFormal.lean` | Root module |
| `ActiveInferenceFormal/Geometry.lean` | Solenoidal orthogonality |
| `ActiveInferenceFormal/Information.lean` | Gibbs inequality, free-energy bound |
| `ActiveInferenceFormal/Audit.lean` | Axiom audit (`#print axioms`) |
| `ActiveInferenceFormal/Sanity.lean` | Smoke theorems |

## Build

```bash
cd formal && lake build
```

Verified by `tests/test_formal_lean.py` when Lean is installed.

## Contract

Python cores in `src/` are the runnable demonstrations; Lean proofs are the
machine-checked side-spec. Keep both aligned when changing theorem statements.
