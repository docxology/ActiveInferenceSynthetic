# Formal layer contract

One real-valued exposition target imports the pinned `FepSketches` library from
`ActiveInferenceInstitute/fep_formal`. Generic proofs belong upstream. Read
[README.md](README.md) when setting up or advancing dependencies; read
[../docs/positioning.md](../docs/positioning.md) before claiming a mathematical
transfer to a paper example.

- Keep `lakefile.lean`, `lake-manifest.json`, and `lean-toolchain` aligned.
- Use an immutable revision observed on upstream main; never a machine-specific path.
- Keep paper wrappers and concrete boundary witnesses here. Do not duplicate the
  generic theorem library or introduce an alternative proof carrier.
- Audit every selected declaration and witness in `Audit.lean`; no `sorry`,
  `admit`, new assumed axioms, or `sorryAx` evidence is allowed.
- Changing a statement requires checking its upstream hypotheses and the local
  example's carrier; a numerical test is not a formal transfer theorem.
- For Gaussian or planning changes, read the exact carrier contracts in
  [README.md](README.md): the canonical Gaussian fixture and two-step Boolean
  history adapter have distinct boundaries from the other paper examples.

Verify with `(cd formal && lake build)` and
`uv run pytest tests/test_formal_lean.py` from the project root. Retain failures.
