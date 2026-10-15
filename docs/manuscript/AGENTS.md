# `docs/manuscript/` technical contract

## Sources

| File | Role |
| --- | --- |
| `00_`–`99_*.md` | Authored sections; the numeric prefix is the render order |
| `config.yaml` | Title, subtitle, version, date, authors, keywords, render formats, test gates |
| `figure_registry.yaml` | Per-figure `id`, `file`, `section`, `caption`, `alt_text`, `builder`, `script` |
| `references.bib` | BibTeX citation records cited as `[@key]` |
| `preamble.md` | LaTeX preamble injected by `infrastructure/rendering/latex_utils.py` |
| `MANUSCRIPT_STATUS.md` | Publication-readiness status of this directory |
| `SYNTAX.md` | Label, citation, and `{{TOKEN}}` syntax for authors |
| `AGENTS.md` / `README.md` | This contract / the section index |

`config.yaml` is loaded by
`infrastructure/rendering/_pdf_combined_renderer.py` and
`infrastructure.publishing.extract_publication_metadata`. Keep its `version` in
step with `pyproject.toml`.

`figure_registry.yaml` must stay in sync with `src/figures/render_all.py`
(the authoritative renderer map), the `expected_figures` list in
`experiment_plan.yaml`, the `figure_types` / `artifact_expectations` lists in
`domain_profile.yaml`, and the `{#fig:...}` anchors in the numbered sections.

## Figure references resolve at render time

Numbered sections embed their figures using paths such as
`](../output/figures/<name>.png){#fig:<id> width=NN%}`. That path is relative to
the **hydrated** manuscript in `output/manuscript/`, not to this directory — it
is deliberately dead when browsed from `docs/manuscript/`. Do not "fix" it to
`../../output/figures/`.

## Claim bindings

- Flow and trajectories: `src/free_energy_flow.py`, `src/trajectories.py`
- Perception/VFE: `src/generative_model.py`
- Expected free energy: `src/expected_free_energy.py`
- Blanket: `src/markov_blanket.py`
- NESS current: `src/steady_state.py`
- Closed-loop/hierarchy: `src/synthetic_agent.py`, `src/hierarchical_model.py`
- Decision value: `src/value_of_information.py`, `src/experiment_suite.py`
- History planning: `src/policy_planning.py`, `src/planning_bridge.py`
- Finite path thermodynamics: `formal/ActiveInferenceFormal/Thermodynamics.lean`
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
