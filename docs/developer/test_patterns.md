# Test patterns

- Compare numerical outputs with hand calculations or independent formulas.
- Test invariants: normalization, monotonicity, orthogonality, positive
  semidefiniteness, detailed-balance limits.
- Use `tmp_path` for figure output and verify the PNG signature.
- Test script wrappers by running their real `main()` functions.
- Test validation with malformed real arrays and explicit error messages.
- Build Lean with the declared toolchain; never replace proof checks with mocks.
- Keep environment/path isolation separate from dependency replacement.
