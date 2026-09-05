# Manuscript

Ordered source for **Active Inference — A Synthetic Overview**.

| Section | Demonstration |
| --- | --- |
| `00_abstract.md` | concise abstract |
| `01_extended_abstract.md` | overview |
| `02_generative_model.md` | perception and VFE |
| `03_worked_regimes.md` | equilibrium/NESS trajectories |
| `04_expected_free_energy.md` | action and explore/exploit |
| `05_markov_blanket.md` | conditional independence |
| `06_steady_state.md` | current and entropy production |
| `07_formal_verification.md` | Lean-checked claims |
| `08_planning.md` | planning as EFE minimization over action sequences |
| `99_references.md` | bibliography section |

Sections render in filename order; the numeric prefix *is* the order.

## Supporting files

| File | Role |
| --- | --- |
| `config.yaml` | Title, authors, version, date, render formats |
| `config.yaml.example` | Upstream template default, kept for reference |
| `figure_registry.yaml` | Figure ids, paths, captions, alt text, builders |
| `references.bib` | BibTeX records for `[@key]` citations |
| `preamble.md` | LaTeX preamble injected at render time |
| `layer_contract.yaml` | Inherited template contract (no active exemptions here) |
| `MANUSCRIPT_STATUS.md` | Publication-readiness status |
| [`SYNTAX.md`](SYNTAX.md) | Label, citation, and `{{TOKEN}}` syntax |

## Editing rules

Numeric claims are `{{TOKEN}}` values computed by
`src/manuscript_variables.py` — never hard-code a demo number. Hydrate with:

```bash
uv run python scripts/z_generate_manuscript_variables.py   # from the project root
```

Full contract: [AGENTS.md](AGENTS.md).
