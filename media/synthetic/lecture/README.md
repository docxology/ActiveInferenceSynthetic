# Frozen lecture authoring sources

These scripts and `lecture.json` describe the released `edition_v15` lecture.
They depend on LectureCreate and frozen `sources/` and `assets/` directories,
which are supplied in the release replay ZIP rather than ordinary Git history.

| Files | Responsibility |
| --- | --- |
| `author.py`, `lecture.json`, `narration_draft.md` | Authored teaching sequence and narration |
| `freeze_science.py` | Scientific source inventory for a new edition |
| `visual_design.py`, `model_animation.py`, `slide_links.py`, `publication.json` | Slide design, model-driven animations, and original edition links |
| `prepare_voice.py`, `revise_audio.py` | Initial or replacement voice preparation; may require synthesis credentials |
| `align_audio.py`, `local_speech_review.py`, `aligned_captions.py` | Transcription, measured word alignment, and captions |
| `render.py`, `package_delivery.py` | Frozen-audio production and delivery packaging |
| `verify.py`, `check_animation.py`, `qa_encoded_animations.py` | Source, audio, timeline, and encoded-animation checks |

Use the [replay instructions](../../../docs/lecture.md) from an extracted release
bundle. A plain repository clone intentionally lacks the measured recordings and
scoped LectureCreate runtime. [AGENTS.md](AGENTS.md) defines edition boundaries.
