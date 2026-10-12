# Manuscript syntax

- Cite sources with Pandoc citation keys: `[@friston2010fep]`. Every key must
  exist in `references.bib`, including the foundational papers and separate software/article entries
  for FEP_Formal and GNN. Repository revision URLs and concept/version DOI
  distinctions are retained in those entries.
- Refer to figures by registry label: `[@fig:overview]`.
- Use `$...$` for inline mathematics. Every display equation must carry a unique
  Pandoc label: `$$...$$ {#eq:meaningful-name}`. Template runs pandoc-crossref
  to assign consecutive numbers automatically in PDF and HTML; refer to an
  equation with `[@eq:meaningful-name]`, never a hand-written number.
- Use backticks for code symbols and paths.
- Keep captions and alt text in `figure_registry.yaml`.
- Keep claims concrete: identify the supporting module, function, test, or Lean
  theorem when the binding is not obvious.
- Demo numbers are `{{TOKEN}}` substitutions. Author tokens; generate values
  with `src/manuscript_variables.py`. Do not paste live floats into `.md`.

Figure labels are listed in [`../syntax_guide.md`](../syntax_guide.md).

Hyperlinks use red in both formats. The PDF preamble specifies red hyperref
colors; a Pandoc HTML-only style block in `00_abstract.md` also covers figure
inspection links. The keyboard skip link uses a lighter red against its dark
background. These styles are authored inputs, not post-render edits.
