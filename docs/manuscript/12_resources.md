# A Reader's Route Beyond Synthetic {#sec:resources}

Reproduce a worked model first, then choose the resource that answers the next
question. Mathematical proof, shared vocabulary, model specification, software
implementation, and educational discussion are different forms of support.
Links below are navigation resources; they do not add runtime dependencies or
extend the formal guarantees of the selected Synthetic carriers.

| Question | Resource | How to use it |
| --- | --- | --- |
| Which mathematical hypotheses are required? | [FEP_Formal](https://github.com/ActiveInferenceInstitute/fep_formal) | Inspect exact declarations and assumption reviews; Synthetic uses its pinned `FepSketches` Lean interface. |
| How can a model be written as a shareable specification? | [Generalized Notation Notation](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation) | Compare state dimensions, channel orientation, preferences and control assumptions before implementing a mapping. |
| What does a term mean in the shared vocabulary? | [Active Inference Ontology](https://github.com/ActiveInferenceInstitute/Active_Inference_Ontology) | Read definitions and typed relations; a vocabulary entry is not a theorem or empirical validation. |
| Where can I study the foundations systematically? | [fundamentals](https://github.com/ActiveInferenceInstitute/fundamentals) and [courses](https://github.com/ActiveInferenceInstitute/courses) | Use reading-group companion materials and structured curricula; the fundamentals repository describes itself as unofficial textbook support. |
| Where can I explore a broader executable agent implementation? | [cognitive](https://github.com/ActiveInferenceInstitute/cognitive) | Inspect the discrete/continuous model interfaces and their validation commands; compare conventions before reusing code. |
| Where can I find talks and their transcripts? | [ActiveInferenceJournal](https://github.com/ActiveInferenceInstitute/ActiveInferenceJournal) | Navigate the structured video/transcript archive and check the original recording and cited papers. |

The bibliography distinguishes FEP_Formal and GNN software snapshots from their
scholarly papers [@fepformal2026software; @friedman2026formalization;
@gnn2026software; @smekal2023gnn]. The additional learning resources are maintained
independently. Repository availability or a passing software test is not evidence
that a particular explanation is scientifically correct.

For a constructive next experiment, change one cue channel, utility, preference,
precision entry or drive parameter. Predict the result before computing it,
include a control that should falsify the intended conclusion, and compare the
new result with the analytical reference. If the modification crosses into a
different mathematical carrier, document the transfer assumptions before citing
an upstream theorem. The repository's resource and methods guides provide
direct links, runnable examples, and the limits of each execution surface.

The ontology and transcript archive have their own software/dataset citation
records [@ontology2023software; @journalarchive]. Their citation metadata is
independent of the mathematical and scholarly sources used for the worked models.
