# Change history

Repository/tooling changes and archival distributions have separate identities.
The numerical package and manuscript metadata remain version 0.5.0.
A dated archive identifies an exact source snapshot; `main` may contain later work.

## Unreleased

- Enforce absolute tolerances for likelihood column sums and precision matrix symmetry.
- Reorganize the GitHub README around the paper/video, a runnable example,
  scientific questions, execution boundaries, repository navigation and citation.
- Add the existing CC-BY-4.0 license text and explicit package license metadata.
- Add contributor guidance, prerequisite/failure instructions and release history.
- Configure Python checks for 3.14 and 3.15, with separate native Lean
  verification. Document the package minimum, checkout default and
  where to find hosted runs.
- Include package construction and an isolated installed-wheel smoke check.
- Consolidate reader and developer guides under `docs/`. Build the paper from
  `docs/manuscript/` with the pinned Template renderer.
- Use a physical working checkout inside Template for manuscript rendering.
- Document project-owned manuscript hydration and the Template's render and
  validation stages.
- Align live formal documentation and citations with the Lean 4.35.0 dependency.
- Keep GitHub's preferred `.github/README.md` synchronized with the root reader
  guide, with a real drift-rejection test and publication check.
- Update the pinned setup-uv action and uv runtime used by Python checks.

## Public distribution 0.6.1 — 2026-10-15

[GitHub release](https://github.com/docxology/ActiveInferenceSynthetic/releases/tag/synthetic-public-v0.6.1) ·
[Zenodo archive](https://zenodo.org/records/23396307)

- Make the repository public and place the verified paper and video at its root.
- Correct folder guides, private-project wording, figure inventories and portable
  lecture/publication links; add missing README/AGENTS pairs.
- Add root artifact hashes, a publication verifier, real corruption/link controls,
  and locked standalone lint/type tooling.
- Archive exact commit `65b57d8a579834003f02ada0ff13f902e6cc6aa4`
  with paper, lecture, companions, complete repository source and frozen replay inputs.

## Teaching release 0.6.0 — 2026-10-12

[GitHub release](https://github.com/docxology/ActiveInferenceSynthetic/releases/tag/synthetic-teaching-v0.6.0)

- Distribute the revised graphical-abstract paper, twenty-minute Daniel lecture,
  linked slides, aligned captions and frozen LectureCreate replay bundle.
- Preserve the scientific package/manuscript version 0.5.0 and explicit
  equilibrium, transient-relaxation, NESS, formal and physical-interpretation boundaries.

## Original archived paper — 2026-10-12

[Zenodo record 23321281](https://zenodo.org/records/23321281)

Original paper/source archive, followed by the revised teaching-edition PDF.
The [concept DOI](https://doi.org/10.5281/zenodo.23321280) groups archival versions.
