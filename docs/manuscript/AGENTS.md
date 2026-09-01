# `docs/manuscript/` technical contract

## Sources

- `config.yaml`: title, authors, version, render policy
- `figure_registry.yaml`: figure paths, labels, captions, alt text
- `references.bib`: citation records
- numbered Markdown files: render order
- `preamble.md`: renderer preamble

## Claim bindings

- Flow and trajectories: `src/free_energy_flow.py`, `src/trajectories.py`
- Perception/VFE: `src/generative_model.py`
- Expected free energy: `src/expected_free_energy.py`
- Blanket: `src/markov_blanket.py`
- NESS current: `src/steady_state.py`
- Formal statements: `formal/ActiveInferenceFormal/`

Numeric claims in numbered sections are `{{TOKEN}}` values from
`src/manuscript_variables.py::generate_variables()`. Never hard-code a demo
number in authored prose. Hydrate with:

```bash
uv run python scripts/z_generate_manuscript_variables.py
```

Regenerate figures and rerun the relevant tests after changing a numerical
claim, caption, or demonstration parameter. Render from the template root with:

```bash
uv run python scripts/pipeline/stage_03_render.py \
  --project working/ActiveInferenceSynthetic
```
