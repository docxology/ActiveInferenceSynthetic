# Manuscript syntax

- Citations use Pandoc keys: `[@friston2010fep]` — the key must exist in
  `docs/manuscript/references.bib`.
- Figure references use registry labels: `[@fig:overview]`.
- Inline mathematics uses `$...$`; display equations use `$$...$$`.
- Code paths and symbols use backticks.
- Every registered figure needs a PNG path, caption, and alt text in
  `docs/manuscript/figure_registry.yaml`.

Current labels:

| Label | Figure |
| --- | --- |
| `fig:graphical-abstract` | cover graphical abstract; see YAML for exact cover handling |
| `fig:agent` | closed-loop cue and commitment |
| `fig:hierarchy` | exact two-level inference |
| `fig:decision-value` | information, utility and cost |
| `fig:overview` | equilibrium and NESS flow |
| `fig:belief` | belief and VFE descent |
| `fig:trajectories` | integrated trajectories |
| `fig:efe` | policy EFE decomposition |
| `fig:planning` | multi-step policy planning (look, then leap) |
| `fig:blanket` | Gaussian Markov blanket |
| `fig:steady` | stationary probability current |
