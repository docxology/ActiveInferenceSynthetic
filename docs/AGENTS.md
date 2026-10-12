# `docs/` technical index

These guides describe the live ActiveInferenceSynthetic tree. Keep commands
valid from the project root unless a guide explicitly says “template root.”

## Contents

| Path | Purpose |
| --- | --- |
| [`positioning.md`](positioning.md) | Paper purpose, upstream methods, pin advancement and transfer boundaries |
| [`quickstart.md`](quickstart.md) | Install, test, generate figures, render |
| [`architecture.md`](architecture.md) | Python / figure / script / Lean layer boundaries |
| [`testing_philosophy.md`](testing_philosophy.md) | Real-computation tests and the coverage floor |
| [`rendering_pipeline.md`](rendering_pipeline.md) | Figure and manuscript render stages |
| [`output_conventions.md`](output_conventions.md) | Disposable artifact layout under `output/` |
| [`output_inventory.md`](output_inventory.md) | The registered figure and artifact names |
| [`syntax_guide.md`](syntax_guide.md) | Manuscript labels, citations, `{{TOKEN}}` values |
| [`style_guide.md`](style_guide.md) | Source and documentation conventions |
| [`troubleshooting.md`](troubleshooting.md) | Common failures and the checks for them |
| [`forking_guide.md`](forking_guide.md) | Adapting the project to a new topic |
| [`faq.md`](faq.md) | Short answers |
| [`agent_instructions.md`](agent_instructions.md) | Working rules for agents editing this tree |
| [`lecture.md`](lecture.md) | Outline of the video walkthrough built from the codebase |
| [`manuscript/`](manuscript/AGENTS.md) | Manuscript sources, config, figure registry, bibliography |

## Sources of truth

- Public Python API: [`../src/__init__.py`](../src/__init__.py)
- Figure registry: [`../src/figures/render_all.py`](../src/figures/render_all.py)
- Manuscript order: [`../docs/manuscript/`](../docs/manuscript/)
- Package version: [`../pyproject.toml`](../pyproject.toml)
- Render metadata: [`../docs/manuscript/config.yaml`](../docs/manuscript/config.yaml)
- Formal modules: [`../formal/ActiveInferenceFormal/`](../formal/ActiveInferenceFormal/)

Do not copy measured test counts into long-lived prose. State the configured
coverage floor (90%) and measure current results with the documented command.

## Verification

From the project root:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/generate_all_figures.py
(cd formal && lake build)
```

`ruff` and `mypy` are configured for this project (`[tool.ruff]` in
[`../pyproject.toml`](../pyproject.toml)) but are supplied by the template's dev
dependency group, not by this project's own dependencies — run them where that
group is installed:

```bash
uv run ruff check src scripts tests
uv run mypy src
```
