# Source conventions

- Scientific functions are deterministic and typed.
- Shared probability validation belongs in `_prob.py`.
- Shared OU/Bayesian-mechanics parameters belong in `ou_model.py`.
- Shared demonstration fixtures belong in `demos.py`.
- Multi-field results use frozen dataclasses.
- Figure builders live in `figures/`; scripts only call `render()`.
- `src/` does not import template `infrastructure`.
- Public names are explicitly re-exported by `src/__init__.py`.
