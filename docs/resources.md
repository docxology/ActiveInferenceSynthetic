# Routes beyond Synthetic

These are verified primary-project entry points, reviewed on 2026-10-11. They
are navigation resources, not additional imports or guarantees for this package.

| Your next question | Resource | Start with |
| --- | --- | --- |
| Exact mathematics and assumptions | [FEP_Formal](https://github.com/ActiveInferenceInstitute/fep_formal) | [Pinned methods map](positioning.md); inspect the statement before transporting a theorem |
| Shared generative-model specification | [GNN](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation) | README and model-specification docs; compare dimensions, likelihood orientation and preferences |
| Controlled vocabulary | [Active Inference Ontology](https://github.com/ActiveInferenceInstitute/Active_Inference_Ontology) | `docs/README.md` and structured source; definitions and relations are distinct from mathematical proofs |
| Foundational reading practice | [fundamentals](https://github.com/ActiveInferenceInstitute/fundamentals) | README; unofficial companion material for textbook study |
| Structured educational tracks | [courses](https://github.com/ActiveInferenceInstitute/courses) | README and course registry; select an appropriate level |
| Broader executable models | [cognitive](https://github.com/ActiveInferenceInstitute/cognitive) | README, package interfaces and validation commands; do not assume API equivalence |
| Talks and searchable transcripts | [ActiveInferenceJournal](https://github.com/ActiveInferenceInstitute/ActiveInferenceJournal) | README and dataset schema; verify against original recordings and cited papers |
| Institute project and learning directory | [Institute projects](https://activeinference.institute/projects/) | Distinguish Institute-hosted repositories from independent ecosystem projects |

The actual formal dependency remains `FepSketches` at the revision recorded in
`formal/lake-manifest.json`. The local upstream checkout has advanced since that
pin; the selected canonical information/flow sources were compared with the
new checkout without changing the reproducible dependency. Landing pages evolve,
while scientific reuse stays revision-bound. GNN, Ontology, courses, cognitive
and the Journal are optional reader pathways; Synthetic does not import them.

Ontology citation metadata identifies its v5 release DOI
`10.5281/zenodo.7972289`; its README also names a separate concept DOI. Journal
metadata identifies the transcript dataset DOI `10.5281/zenodo.21074926`.
These identities do not confer mathematical or peer-review status on every
definition or transcript. FEP_Formal and GNN software and scholarly references
remain separated in the paper's bibliography and project citation metadata.

Suggested route: reproduce one [method](methods.md), inspect its assumptions,
look up unfamiliar terminology, read the relevant primary paper, and only then
move into a larger implementation or formalization. Record any mapping between
carriers, including zero-support conventions and utility/information units.
