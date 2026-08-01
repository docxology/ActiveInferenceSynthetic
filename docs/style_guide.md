# Style guide

- Keep public APIs typed and documented.
- Return named dataclasses for multi-field scientific results.
- Validate arrays at module boundaries; reuse `src/_prob.py`.
- Reuse `IsotropicOU` instead of rebuilding `P`, `Gamma`, `Q`, or `M`.
- Keep figure constants in `src/demos.py` and colors in
  `src/figures/palette.py`.
- Keep scripts short and free of scientific calculations.
- Prefer explicit equations and file/function references over promotional
  adjectives.
- Preserve deterministic behavior and avoid hidden normalization.
- Put imports at module scope.
