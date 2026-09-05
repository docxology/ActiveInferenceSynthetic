# Manuscript syntax

- Cite sources with Pandoc citation keys: `[@friston2010fep]`. Every key must
  exist in `references.bib`, which currently holds `friston2010fep`,
  `parr2022active`, `friston2023bayesian`, `ramstead2023bayesian`, and
  `dacosta2021bayesian`.
- Refer to figures by registry label: `[@fig:overview]`.
- Use `$...$` for inline mathematics and `$$...$$` for display equations.
- Use backticks for code symbols and paths.
- Keep captions and alt text in `figure_registry.yaml`.
- Keep claims concrete: identify the supporting module, function, test, or Lean
  theorem when the binding is not obvious.
- Demo numbers are `{{TOKEN}}` substitutions. Author tokens; generate values
  with `src/manuscript_variables.py`. Do not paste live floats into `.md`.

Figure labels are listed in [`../syntax_guide.md`](../syntax_guide.md).
