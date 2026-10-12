# Twenty-minute animated Synthetic lecture

## Current teaching release

[Download the complete teaching release](https://github.com/docxology/ActiveInferenceSynthetic/releases/tag/synthetic-teaching-v0.6.0).
The release video uses the revised graphical-abstract cover, 26 chapters and
the existing ElevenLabs Daniel voice. Five animations distinguish inference
iteration, deterministic drift time, transient ensemble relaxation, a stationary
drive-parameter sweep and a cue-accuracy sweep. Parameter sweeps are explicitly
identified as different from time trajectories.

The source-bound slides show actual GNN parameters and the Lean fluctuation
declaration with positive-support hypotheses. The numerical implementation,
finite theorem carrier and physical interpretation retain separate boundaries.
The earlier Zenodo publication is linked as an archived edition; this revised
paper and lecture are distributed through the teaching release.

All measured recordings were transcribed independently with local small.en ASR
and aligned against the authored narration with Wav2Vec2 CTC. Four flagged
passages were regenerated and rechecked. Final captions use measured word
times, preserve the entire script and undergo exact embedded round-trip checks.
ASR and alignment are machine checks, not a claim of a human listening panel.

Reproducibility sources and measured recordings are supplied in the release ZIP.
From its extracted directory, use the bundled LectureCreate runtime:

```bash
uv run --project runtime --with matplotlib --with numpy --with pypdf==6.20.0 \
  python lecture/render.py --out output/replay
uv run --project runtime python lecture/package_delivery.py \
  --production output/replay --delivery-out output/replay_delivery
```

Replay uses frozen recordings and alignment results, making no paid synthesis
calls. FFmpeg is required. Version 0.6.0 identifies the teaching release;
the scientific package and manuscript metadata remain version 0.5.0.
The final development edition is `edition_v15` in LectureCreate; earlier
attempts and their failures remain preserved outside the release.

## Publication edition

Edition v11 opens with a screenshot of the Synthetic paper cover, its own
[Zenodo record](https://zenodo.org/records/23321281), and the published
[FEP_Formal reference](https://zenodo.org/records/23220027). Clearer reading prompts,
larger resource labels and quieter layouts accompany the three model animations.
The 26-page slide PDF contains 35 clickable links, including the
[GNN publication](https://zenodo.org/records/7803328).

The current delivery is `output/video/synthetic_publication_daniel_20261012/`.
[Watch the publication lecture](../output/video/synthetic_publication_daniel_20261012/ActiveInferenceSynthetic_Publication_20min.mp4)
or [open the linked slides](../output/video/synthetic_publication_daniel_20261012/ActiveInferenceSynthetic_Publication_Slides.pdf).
Downloads receives `ActiveInferenceSynthetic_Publication_20min.mp4`,
`ActiveInferenceSynthetic_Publication_Slides.pdf`, and the published paper PDF.
The video retains the measured twenty-minute Daniel narration, 26 chapters and
307 selectable English captions. It reuses the frozen recordings; publication
and layout changes require no new synthesis calls.

From the neighboring LectureCreate root, replay to a fresh output directory:

```bash
uv run --with pypdf==6.20.0 python examples/active_inference_synthetic/edition_v11/render.py --verify-sources
uv run --with pypdf==6.20.0 python examples/active_inference_synthetic/edition_v11/render.py --out output/my_publication_lecture
uv run python examples/active_inference_synthetic/edition_v11/verify.py --out output/my_publication_lecture
uv run python examples/active_inference_synthetic/edition_v11/package_delivery.py \
  --production output/my_publication_lecture --delivery-out output/my_publication_delivery
```

Its production directory is
`output/active_inference_synthetic_20min_20261012/production_v11_publication_daniel/`.
The frozen source bundle includes the exact cover PDF and slide link metadata.
Caption timing remains character-proportional within measured speech; the
receipts document encoded animation, full decode and audio checks separately.

## Preserved animated edition

The preserved LectureCreate example is `examples/active_inference_synthetic/edition_v10/`
in the neighboring repository. Its production is
`output/active_inference_synthetic_20min_20261011/production_v10_animated_daniel/`.
The project delivery is `output/video/synthetic_animated_daniel_20261011/`, with a
copy at `~/Downloads/ActiveInferenceSynthetic_Daniel_Animated_20min.mp4`.

[Watch the animated lecture](../output/video/synthetic_animated_daniel_20261011/ActiveInferenceSynthetic_Daniel_Animated_20min.mp4)

The 2,764-word, 26-chapter edition adds a finite decision-value example, its
cost and irrelevant-payoff controls, and a reader's map of FEP_Formal, GNN,
Active Inference Ontology, fundamentals, courses, cognitive and
ActiveInferenceJournal. See the [methods](methods.md) and [resources](resources.md)
guides for definitions, assumptions and direct repository links.

Three animations show computed categorical belief descent, radial/rotating
deterministic trajectories, and a cue-accuracy sweep. Their clocks are explicitly
algorithm iteration, model time, and known parameter value. Independent analytic
oracles check the data; encoded frame comparisons check the presented panels.
Stationary current is an ensemble property, distinct from a relaxing trajectory.
Decision utility and cost are distinct from information in nats.

The existing ElevenLabs Daniel profile supplies the voice. Unchanged chapters
reuse raw recordings only on exact narration-text agreement; the two revised
chapters were synthesized anew. Measured pitch-preserving pacing fits the exact
twenty-minute timeline with reading pauses. Ten scientific figures, guided
plates, chapters, selectable captions, slides, transcript and a source ledger
accompany the video. Caption timing is character-proportional within measured
speech, not forced alignment or a human listening-panel assessment.

From the LectureCreate root, use a fresh output directory:

```bash
uv run python examples/active_inference_synthetic/edition_v10/render.py --verify-sources
uv run python examples/active_inference_synthetic/edition_v10/render.py --out output/my_lecture
uv run python examples/active_inference_synthetic/edition_v10/verify.py --out output/my_lecture
uv run python examples/active_inference_synthetic/edition_v10/package_delivery.py \
  --production output/my_lecture --delivery-out output/my_delivery
uv run python examples/active_inference_synthetic/edition_v10/qa_encoded_animations.py \
  --production output/my_lecture \
  --video output/my_delivery/ActiveInferenceSynthetic_20min_captioned.mp4
```

Replay uses frozen recordings and makes no paid synthesis calls. FFmpeg is
required. The frozen source inventory binds the numerical cores, hydrated paper,
figures, references, formal sources, experiment report, resource guides and audio.
The Python namespace is `active_inference_synthetic`; the independent Lean layer
imports pinned FepSketches, and GNN remains an optional specification pathway.

Earlier productions remain preserved. Edition v8 retains its receipt-generation
failure, and v9 retains the drift-axis clipping caught by visual QA. Edition v10
corrects that layout. Paper and media receipts are separate local validations.

## Preserved earlier Daniel edition

The material below records the earlier static v7 production, not the current
animated delivery.

The completed LectureCreate example lives in the neighboring
`LectureCreate/examples/active_inference_synthetic/edition_v7/` project. Its
source-bound production is `LectureCreate/output/active_inference_synthetic_20min_20261011/production_v7_daniel/`.
A byte-verified delivery copy lives in this repository at
`output/video/synthetic_daniel_20min_20261011/`. The final video is also copied to
`~/Downloads/ActiveInferenceSynthetic_Daniel_20min.mp4` and hash-verified there.

[Watch the narrated lecture](../output/video/synthetic_daniel_20min_20261011/ActiveInferenceSynthetic_Daniel_20min.mp4)

The lecture covers inference and VFE, equilibrium and NESS, probability current
and entropy production, Gaussian blankets and the qualified native model,
preferences and EFE, history-channel planning, closed-loop commitments,
hierarchical inference, thermodynamic units, proof-transfer boundaries, and
reproduction. It uses the nine generated scientific figures and conceptual
cards, with the ElevenLabs Daniel voice and an exact measured twenty-minute
timeline. Chapters, selectable English subtitles, a slide PDF, transcript,
speaker notes, source ledger, and frozen input snapshots accompany the video.
The final edition also explains the installed Synthetic Python namespace,
its actual pinned FepSketches Lean dependency, and GNN's optional role.

The revised opening poses concrete questions; figure-reading prompts and the
closing recap connect them to the demonstrations. Repeated explanations were
tightened while retaining scientific assumptions and limits. The 2,739-word
script has about 19 minutes 10 seconds of measured speech, leaving 50 seconds
for reading pauses and transitions. All 26 chapters and nine figures remain.

## Reproduce using LectureCreate

From the LectureCreate root:

```bash
uv run python examples/active_inference_synthetic/edition_v7/render.py --verify-sources
uv run python examples/active_inference_synthetic/edition_v7/render.py \
  --out output/my_synthetic_lecture
uv run python examples/active_inference_synthetic/edition_v7/verify.py \
  --out output/my_synthetic_lecture
uv run python examples/active_inference_synthetic/edition_v7/package_delivery.py \
  --production output/my_synthetic_lecture \
  --delivery-out output/my_synthetic_delivery
```

Use a fresh output directory. Replay requires ffmpeg and the frozen Daniel
recordings included in this edition; it makes no new paid synthesis calls.
First-generation speech was produced through the existing ElevenLabs backend
in `edition_v5`, using voice ID `f1fdYDHzR22JxAxrWWgE` from `voices/daf/profile.yaml`
and model `eleven_multilingual_v2`. The raw 21-minute narration is preserved.
A measured 1.10002× tempo adjustment retains pitch and all sentences, with
original/paced audio hashes and the processing receipt in the frozen bundle.
Measured speech determines the budget; no sentence is trimmed
to force duration. The delivery packaging helper and its separate hash-bound
receipt supply corrected captions and a lossless selectable-subtitle derivative.

## Evidence boundaries

Caption cues are character-proportional within measured speech spans, not forced
alignment. Postproduction checks require positive monotonic cue durations,
complete narration-text equality, bounded speech intervals, exact embedded-cue
round-trip, and full video decoding. The original invalid boundary and initial
productions are retained as failure/custody evidence.

The final video binds its own immutable current scientific snapshot, including
the updated manuscript, positioning guide, package metadata and citations.
Its 302 English caption cues survive exact embedded round-trip. All 26 audio
clips are non-silent and have no clipped PCM samples. Every encoded chapter
midpoint was visually inspected. Visual evidence uses actual encoded frame
captures in the delivered `media_qa/` folder. The new design uses focused
scientific panels, large results, three-step reading guides and explicit model
roles. All nine scientific figures remain represented.

Earlier editions, source freezes and timing comparisons remain preserved.
The media verification receipts are separate from the paper's template-rendering
receipt and do not claim a new publication or a human listening-panel review.
