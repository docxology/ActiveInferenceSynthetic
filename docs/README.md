# Project documentation

Operational guides for **Active Inference — A Synthetic Overview**.

Begin with [project positioning and upstream methods](positioning.md): the
standalone paper's contribution, its relationship to `fep_formal`, and the
section-to-method map with upstream documentation entry points.

| Guide | Purpose |
| --- | --- |
| [Quick start](quickstart.md) | Install, test, generate figures, render |
| [Architecture](architecture.md) | Python, figure, script, and Lean boundaries |
| [Testing](testing_philosophy.md) | Real-computation tests and coverage |
| [Rendering](rendering_pipeline.md) | Figure and manuscript pipeline |
| [Outputs](output_conventions.md) | Disposable artifact layout |
| [Syntax](syntax_guide.md) | Manuscript labels and citations |
| [Style](style_guide.md) | Source and documentation conventions |
| [Troubleshooting](troubleshooting.md) | Common failures and checks |
| [Forking](forking_guide.md) | Adapting the project |
| [FAQ](faq.md) | Short answers |
| [Agent instructions](agent_instructions.md) | Working rules for agents editing this tree |
| [Output inventory](output_inventory.md) | The registered figure and artifact names |
| [Lecture](lecture.md) | Current lecture, captions, and frozen replay workflow |
| [Publication](publication.md) | Synthetic DOI, source archive and published upstream references |
| [GNN specifications](gnn_specifications.md) | Authored models, optional parser checks and thermodynamic transfer |

## Contribute, validate and cite

- [Contributor workflow](../CONTRIBUTING.md): setup, layer ownership, real controls and PR evidence.
- [Change history](../CHANGELOG.md): development work versus immutable archives.
- [Python CI](../.github/workflows/README.md): supported runtimes and verification scope.
- [Citation metadata](../CITATION.cff) and [project license](../LICENSE).

`graphical_abstract.png` is a documentation copy of the generated cover panel,
produced by `src/figures/graphical_abstract.py`. Regenerate from that builder
when its scientific inputs change; do not hand-edit numerical content.

## Manuscript

The [methods guide](methods.md) maps carriers, units, analytical checks and
limitations. The [resource guide](resources.md) gives verified Institute and
ecosystem routes for the next learning or implementation question.

The manuscript sources are a subdirectory here, not a guide:
[`manuscript/`](manuscript/README.md) holds the numbered Markdown sections,
`config.yaml`, `figure_registry.yaml`, `references.bib`, and the render
preamble.

Technical inventory: [AGENTS.md](AGENTS.md).
