# Formal verification (Lean 4)

Machine-checked formalization of the mathematical core of *Active Inference —
A Synthetic Overview*. The development has **two surfaces**:

1. **ℝ surface (manuscript-canonical).** `Geometry.lean` and `Information.lean`
   import and re-export the ℝ-valued theorems from the companion **fep_lean**
   library (`FepSketches`, mathlib-backed). `Bridge.lean` documents how the
   three evidence surfaces — Python `src/` (floats), formal ℝ, and formal ℤ —
   map onto one another.
2. **ℤ legacy surface (Lean core only).** `GeometryZ.lean`, `InformationZ.lean`,
   and `Sanity.lean` prove the same structural statements over ℤ from Lean's
   core axioms alone — no mathlib, no `sorry` — showing the identities are
   algebraic, not analytic.

## Build

```bash
cd formal
lake update   # first time, or when the fep_lean path changes
lake build
```

The `require FepSketches from "../../../ongoing/instituteos/repos/fep_lean/lean"`
is a relative path into the private projects repository's `ongoing/` tree; the
ℝ surface needs that checkout present. The ℤ surface alone builds from Lean core
with no dependencies.

The build prints, via the `Audit` module, the axiom set of each headline
theorem: ℝ theorems carry the standard mathlib footprint (including
`Classical.choice`); every ℤ theorem reports only Lean's trusted core — never
`sorryAx`.

## Layout

```
lakefile.lean                        requires FepSketches (fep_lean) + exposes both surfaces
lean-toolchain                       leanprover/lean4:v4.33.1 (matches fep_lean)
ActiveInferenceFormal.lean           library root (imports all modules)
ActiveInferenceFormal/
  Geometry.lean                      ℝ flow / steady-state facts (from fep_lean)
  Information.lean                   ℝ perception / free-energy bound, EFE (from fep_lean)
  Bridge.lean                        documentation bridging Python ℝ, formal ℝ, formal ℤ
  GeometryZ.lean                     ℤ flow identities (Lean core only)
  InformationZ.lean                  ℤ VFE bound (Lean core only)
  Sanity.lean                        non-vacuity witnesses for the ℤ surface
  Audit.lean                         `#print axioms` on every headline theorem
```

## What is proved

**Geometry / NESS flow** (§1, §3, §6) — on both surfaces:

- `solenoidal_orthogonal` — the antisymmetric current `Q g` is orthogonal to the
  gradient `g` (it does no work against free energy).
- `flow_work_eq_dissipation` — the work of the full flow is exactly `-γ‖g‖²`;
  the solenoidal part is free, so free energy is non-increasing.
- `detailed_balance_iff` — the current vanishes iff `ω = 0`.
- `entropyProduction_nonneg` / zero-iff — entropy production is `≥ 0` and `= 0`
  exactly at `ω = 0`.

**Information / perception** (§2) — ℤ surface plus ℝ counterparts from fep_lean:

- `relEntropy_nonneg` — Gibbs' inequality (relative entropy `≥ 0`).
- `freeEnergy_eq_surprise_add_relEntropy` — the decomposition `F = surprise +
  D(q‖posterior)`.
- `freeEnergy_ge_surprise` — variational free energy is an upper bound on
  surprise (ℤ: total-scaled; ℝ: for a genuine generative model).
- `freeEnergy_eq_surprise_at_posterior` — the bound is tight at the posterior.

## Design notes

- **Why ℤ at all.** The structural claims are polynomial identities and sign
  facts; the integers suffice and keep the legacy surface dependency-free. The
  real-valued instances live on the Python side and in the fep_lean-backed ℝ
  surface.
- **The logarithm's properties are explicit hypotheses — and non-vacuity is
  proved.** The ℤ free-energy bound needs two facts about `ln`: additivity and
  the tangent bound (`ln x ≤ x-1`). Stated *universally* over ℤ these are
  unsatisfiable, which would make the theorems vacuously true. The development
  takes them only at the exact points each proof consumes, and `Sanity.lean`
  proves both a **negative control** (`relEntropy_can_be_negative`: the tangent
  hypothesis is necessary) and a **positive control** (`okL*`: the hypotheses
  are satisfiable on a genuine generative model and the bound fires with a real
  gap). So the ℤ results are faithful, not vacuous.

The Python suite verifies all of this via `tests/test_formal_lean.py`: source
audits (`sorry`/`admit` absence, theorem and witness presence, surface import
contracts) plus a real `lake build` with axiom-audit inspection when a Lean
toolchain is installed.
