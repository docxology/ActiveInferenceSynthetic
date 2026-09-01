# Manuscript syntax

- Cite sources with Pandoc citation keys: `[@friston2010]`.
- Refer to figures by registry label: `[@fig:overview]`.
- Use `$...$` for inline mathematics and `$$...$$` for display equations.
- Use backticks for code symbols and paths.
- Keep captions and alt text in `figure_registry.yaml`.
- Keep claims concrete: identify the supporting module, function, test, or Lean
  theorem when the binding is not obvious.
- Demo numbers are `{{TOKEN}}` substitutions. Author tokens; generate values
  with `src/manuscript_variables.py`. Do not paste live floats into `.md`.

Figure labels are listed in [`../docs/syntax_guide.md`](../docs/syntax_guide.md).
