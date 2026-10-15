# Manuscript

Ordered source for **Active Inference — A Synthetic Overview**.

| Section | Demonstration |
| --- | --- |
| `00_abstract.md` | concise abstract |
| `01_extended_abstract.md` | overview |
| `02_generative_model.md` | perception and VFE |
| `02_methods.md` | numerical and formal reproducibility |
| `03_equilibrium_concepts.md` | stationarity, detailed balance, transients and time reversal |
| `03_worked_regimes.md` | equilibrium/NESS trajectories |
| `04_expected_free_energy.md` | action and explore/exploit |
| `05_markov_blanket.md` | conditional independence |
| `06_steady_state.md` | current and entropy production |
| `07_formal_verification.md` | Lean-checked claims |
| `07_thermodynamic_transfer.md` | finite path-theorem imports and validated GNN specifications |
| `08_planning.md` | planning as EFE minimization over action sequences |
| `09_synthetic_agent.md` | closed-loop observation-sensitive commitments |
| `09_value_of_information.md` | feedback utility, acquisition cost and counterexamples |
| `10_hierarchical_inference.md` | two-level exact categorical inference |
| `11_thermodynamic_interpretation.md` | units, model assumptions, and transfer boundaries |
| `12_resources.md` | Institute repository and learning pathways |
| `99_references.md` | bibliography section |

Sections render in filename order; the numeric prefix *is* the order.

## Paper scope

This manuscript is an independently authored educational synthesis with its own
reproducible demonstrations. The broader `fep_formal` repository owns the generic
mathematical library reused by the real-valued formal layer. The
[project positioning guide](../positioning.md) maps the sections to upstream
methods and distinguishes implemented re-exports from prospective bridges.

## Supporting files

| File | Role |
| --- | --- |
| `config.yaml` | Title, authors, version, date, render formats |
| `figure_registry.yaml` | Figure ids, paths, captions, alt text, builders |
| `references.bib` | BibTeX records for `[@key]` citations |
| `preamble.md` | LaTeX preamble injected at render time |
| `MANUSCRIPT_STATUS.md` | Publication-readiness status |
| [`SYNTAX.md`](SYNTAX.md) | Label, citation, and `{{TOKEN}}` syntax |

## Editing rules

Numeric claims are `{{TOKEN}}` values computed by
`src/manuscript_variables.py` — never hard-code a demo number. Hydrate with:

```bash
uv run python scripts/z_generate_manuscript_variables.py   # from the project root
```

Full contract: [AGENTS.md](AGENTS.md).
