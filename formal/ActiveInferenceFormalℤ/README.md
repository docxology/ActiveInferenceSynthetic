# `ActiveInferenceFormalℤ` — the legacy ℤ surface

The same structural theorems as the ℝ surface, proved over the integers from
Lean core alone — no mathlib, no external dependency, no `sorry`.

## Quick start

```bash
cd formal && lake build ActiveInferenceFormalℤ   # from the project root
```

Builds in seconds; needs nothing but the toolchain pinned in
[`../lean-toolchain`](../lean-toolchain).

## Files

| File | Role |
| --- | --- |
| `GeometryZ.lean` | Flow identities: solenoidal orthogonality, dissipation, detailed balance, entropy production |
| `InformationZ.lean` | Gibbs' inequality and the variational free-energy bound |
| `Sanity.lean` | Positive and negative controls proving the bound is non-vacuous |

## Key facts

- Namespace `ActiveInferenceFormalℤ` throughout.
- The logarithm's properties are hypotheses taken **at the points consumed**,
  never universally — a universal version over ℤ is unsatisfiable and would make
  the theorems vacuous. `Sanity.lean` proves both that the hypotheses are
  necessary and that they are satisfiable.
- Audited by `../ActiveInferenceFormal/Audit.lean` and `tests/test_formal_lean.py`.

## More information

See [AGENTS.md](AGENTS.md) for the theorem inventory and editing rules, and
[`../README.md`](../README.md) for why this surface exists alongside the ℝ one.
