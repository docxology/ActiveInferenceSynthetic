# `ActiveInferenceFormal` — the ℝ surface

Manuscript-canonical Lean 4 statements, re-exported from the companion
**fep_lean** library (`FepSketches`, mathlib-backed), plus the cross-surface
bridge and the axiom audit.

## Quick start

```bash
cd formal && lake update && lake build   # from the project root
```

Requires the fep_lean checkout at the relative path in
[`../lakefile.lean`](../lakefile.lean). The ℤ target builds without it.

## Files

| File | Role |
| --- | --- |
| `Geometry.lean` | ℝ flow geometry — solenoidal orthogonality, dissipation, detailed balance, entropy production |
| `Information.lean` | ℝ Gibbs inequality, VFE bound and tightness, EFE decomposition |
| `Bridge.lean` | Maps Python ℝ ↔ formal ℤ ↔ formal ℝ; documentation only |
| `Audit.lean` | `#print axioms` on every headline theorem, both surfaces |

## Key facts

- Every theorem here is prefixed `ℝ_` and lives in namespace `ActiveInferenceFormal`.
- No proofs originate in this package — it re-exports fep_lean with exposition.
- No `sorry`; verified by `tests/test_formal_lean.py`.

## More information

See [AGENTS.md](AGENTS.md) for the full theorem inventory and editing rules,
and [`../README.md`](../README.md) for the two-surface design.
