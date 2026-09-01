/-
Copyright (c) 2026 Daniel Ari Friedman, Alexandra Mikhailova.
Released under the CC-BY-4.0 license (matching the manuscript).
-/
import ActiveInferenceFormal.Geometry
import ActiveInferenceFormal.Information
import ActiveInferenceFormal.Bridge
import ActiveInferenceFormalℤ.GeometryZ
import ActiveInferenceFormalℤ.InformationZ
import ActiveInferenceFormalℤ.Sanity
import ActiveInferenceFormal.Audit

/-!
# Active Inference — Formal Core

This package exposes formal proofs for the mathematical claims of
``Active Inference — A Synthetic Overview``.  The theorems live in two
canonical surfaces:

## ℝ-valued surface (manuscript-canonical, fep_lean-backed)

``Geometry`` — the Bayesian-mechanics NESS flow, imported from
  ``FepSketches.ness_flow``.
``Information`` — the variational free-energy bound, expected free energy,
  and policy selection, imported from ``FepSketches.finite_information`` and
  ``FepSketches.active_inference``.
``Bridge`` — documentation connecting the ℝ and ℤ surfaces to the
  Python demos.

## ℤ-valued legacy surface (no mathlib, Lean core only)

``GeometryZ`` — the same flow identities over ℤ (algebraic only).
``InformationZ`` — the same VFE bound over ℤ (combinatorial only).
``Sanity`` — concrete witnesses proving every ℤ theorem is non-vacuous.

Every ℤ theorem depends only on Lean'''s built-in axioms (\`[propext, Quot.sound]\`)
and never \`sorryAx\`.  See ``Audit`` for the full axiom footprint on every result.
-/
