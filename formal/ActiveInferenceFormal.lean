/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/
import ActiveInferenceFormal.Geometry
import ActiveInferenceFormal.Information
import ActiveInferenceFormal.Sanity
import ActiveInferenceFormal.Audit

/-!
# Active Inference — Formal Core

A self-contained (mathlib-free) Lean 4 formalization of the mathematical claims
that the manuscript demonstrates numerically in `src/`. See the two modules:

* `ActiveInferenceFormal.Geometry` — the Bayesian-mechanics flow: the solenoidal
  (antisymmetric) operator does no work against the free-energy gradient, so it
  is conservative; detailed balance holds iff the solenoidal strength is zero;
  and the steady-state entropy production is nonnegative, vanishing exactly at
  detailed balance.
* `ActiveInferenceFormal.Information` — perception as inference: the variational
  free energy decomposes as surprise plus a relative entropy, and that relative
  entropy is nonnegative (Gibbs' inequality), so free energy is an upper bound
  on surprise that is tight exactly at the Bayesian posterior.

Every theorem is proved from Lean core; run `#print axioms` on any result to see
that it rests only on Lean's own axioms (no `sorry`, no mathlib).
-/
