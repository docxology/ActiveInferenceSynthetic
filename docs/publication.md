# Public distribution and archival publication

## Current release

[GitHub public distribution 0.6.1](https://github.com/docxology/ActiveInferenceSynthetic/releases/tag/synthetic-public-v0.6.1)
and [Zenodo record 23396307](https://zenodo.org/records/23396307)
distribute the revised paper, twenty-minute Daniel lecture, linked slides,
captions, frozen lecture replay inputs, complete repository source snapshot,
checksums, and verification report.

Version DOI: [10.5281/zenodo.23396307](https://doi.org/10.5281/zenodo.23396307).
Concept DOI: [10.5281/zenodo.23321280](https://doi.org/10.5281/zenodo.23321280).
The [original paper archive](https://zenodo.org/records/23321281) remains available.

| Identity | Meaning |
| --- | --- |
| Public distribution `0.6.1` | Root deliverables, corrected documentation and a complete source snapshot |
| Scientific package/manuscript `0.5.0` | Version in `pyproject.toml` and manuscript render metadata |
| Teaching release `0.6.0`, lecture `edition_v15` | Frozen PDF, video, slides, captions and replay inputs reused byte-for-byte |

This distribution adds no scientific result and changes no numerical model or
Lean proposition. The development extra now locks its verification tools for
standalone use. The revised PDF and video are the verified teaching-edition
bytes, copied to the repository root. Their embedded earlier links remain
part of that edition. The scientific manuscript config continues to describe
that PDF; citation metadata points readers to the current distribution.

## Files and provenance

`publication.json` binds maintained root/media copies to hashes, sizes and
their original source release. `SHA256SUMS.txt` provides the same local asset
checks in shell format. The GitHub and Zenodo payloads additionally contain:

- `ActiveInferenceSynthetic_Source_v0.6.1.zip`: every committed repository
  file, with archive prefix `ActiveInferenceSynthetic-0.6.1/`; no ignored
  credentials, environments, production caches, or local evidence directories.
- `ActiveInferenceSynthetic_Reproducibility.zip`: the unchanged frozen
  lecture inputs and scoped LectureCreate runtime, rather than the current
  scientific repository tree.
- `RELEASE_IDENTITY.json`: the exact source commit, tag, DOI, file sizes and
  SHA-256 values of the deliverables.
- `VERIFICATION.json`: measured checks for this publication cut.
- `SHA256SUMS.txt`: checksums for distribution payload files.

The source archive is produced from the exact Git commit, using `git archive`.
Its PDF/MP4 match the root copies. The replay ZIP has a different purpose and
preserves the original media inputs even when repository documentation advances.

## Verify a checkout

From the repository root:

```bash
uv run python scripts/verify_publication.py
shasum -a 256 -c SHA256SUMS.txt
uv run pytest tests/ --cov=src --cov-fail-under=90
```

The publication verifier checks asset sizes and hashes, local Markdown links,
and paired README/AGENTS guides in every maintained folder. Numbered manuscript
figure paths deliberately resolve in the hydrated rendering tree; they must
match a declared renderer. External URLs and renderer-specific anchors require
their own checks. Formal verification requires the pinned Lean prerequisites.

## Publish a successor

1. Verify mounted storage, checkout identity, owners, dirty files and runtime.
   Keep unrelated local edits and earlier evidence intact.
2. Use the template Zenodo API client and production credential loaded from the
   template's local environment. Create or resume one unpublished successor
   version of this record; persist its id and reserved DOI before upload.
3. Update distribution and citation metadata. Preserve the previous published
   record and any frozen media edition reused without byte changes.
4. Run scientific checks, publication positive/negative controls, PDF/media
   inspection and the independent acceptance checks required by the task.
5. Commit the reviewed files, freeze the full commit identity, create the source
   archive, and verify the payload inventory against its hashes.
6. Push the commit and a new tag, create its GitHub release, then upload the
   identical payload to the successor Zenodo draft and publish it.
7. Download every asset anonymously from both hosts and compare hashes.
   Verify DOI resolution, record access, repository visibility and the tag's commit.

Rendering a changed paper uses the separate template workflow in
[the rendering guide](rendering_pipeline.md). A changed paper or narration
requires fresh artifact verification; this distribution reuses the frozen bytes.

## Scientific references

Synthetic is a standalone educational synthesis selecting formal results from
FEP_Formal under explicit hypotheses. See [positioning](positioning.md),
[methods](methods.md) and [resources](resources.md).

The [FEP_Formal paper](https://zenodo.org/records/23220027) and
[GNN paper](https://zenodo.org/records/7803328) have distinct
[formal software](https://zenodo.org/records/23196891) and
[GNN software](https://zenodo.org/records/7803313) identifiers.
The imported proof source is controlled by the immutable revision in
`formal/lakefile.lean`, independently of bibliographic and distribution versions.
