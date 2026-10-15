# Twenty-minute animated Synthetic lecture

## Watch and read

The current public distribution contains the unchanged, verified `edition_v15`
lecture from teaching release `synthetic-teaching-v0.6.0`.

- [Root MP4](../ActiveInferenceSynthetic_20min.mp4) or [direct release download](https://github.com/docxology/ActiveInferenceSynthetic/releases/download/synthetic-public-v0.6.1/ActiveInferenceSynthetic_20min.mp4)
- [Revised paper](../ActiveInferenceSynthetic_Revised.pdf)
- [Linked slides](../media/synthetic/slides.pdf)
- [SRT captions](../media/synthetic/captions.srt), [WebVTT captions](../media/synthetic/captions.vtt)
- [Transcript](../media/synthetic/transcript.txt), [speaker notes](../media/synthetic/speaker_notes.md)
- [Frozen replay bundle](https://github.com/docxology/ActiveInferenceSynthetic/releases/download/synthetic-public-v0.6.1/ActiveInferenceSynthetic_Reproducibility.zip)
- [Zenodo archive](https://zenodo.org/records/23396307)

The video runs for exactly 1200 seconds at 1920 × 1080, with 26 chapters and
344 English caption cues. Its Daniel narration uses the existing ElevenLabs
Daniel voice. Five animations distinguish inference iteration, deterministic
drift time, transient ensemble relaxation, a stationary drive-parameter sweep
and a cue-accuracy sweep. A parameter sweep is distinct from a time trajectory.

The slides present actual GNN parameters and a Lean finite-path fluctuation
declaration under positive-support hypotheses. Numerical implementation,
finite theorem carriers and physical interpretation retain separate boundaries.
The opening's references identify the earlier archived paper and original
teaching release; those historical links remain correct for this frozen edition.
The new archive republishes the identical media bytes, without revising narration.

## Captions and verification

Known-text Wav2Vec2 CTC alignment supplies measured word times. Independent
small.en transcription covered all recordings; four flagged passages were
regenerated and rechecked in the original production. Captions preserve the
authored script and survived exact embedded subtitle round-trip.
These are machine checks, not a human listening-panel assessment.

The frozen [media manifest](../media/synthetic/release_manifest.json) binds
the original edition. The root [publication manifest](../publication.json)
binds its reuse in public distribution 0.6.1. Local receipts, a renderer exit,
and hosted download verification each establish different facts.

## Reproduce from the replay bundle

Extract the reproducibility ZIP into a fresh directory on the intended storage
volume. It supplies `lecture/`, frozen recordings and alignment data, scientific
inputs, and a scoped `runtime/` LectureCreate project. A plain clone contains
the authored scripts but omits those large replay inputs.

From the extracted bundle root:

```bash
uv run --project runtime --with matplotlib --with numpy --with pypdf==6.20.0 \
  python lecture/render.py --verify-sources
uv run --project runtime --with matplotlib --with numpy --with pypdf==6.20.0 \
  python lecture/render.py --out output/replay
uv run --project runtime python lecture/verify.py --out output/replay
uv run --project runtime python lecture/package_delivery.py \
  --production output/replay --delivery-out output/replay_delivery
```

FFmpeg is required. Use fresh production and delivery directories.
Bind uv, Python, cache and temporary paths to the working storage volume.
Replay uses measured recordings and makes no paid synthesis calls.
Voice preparation and regeneration are separate credentialed operations.

## Earlier development editions

Earlier static and three-animation productions were superseded by edition_v15.
Their local outputs and failed receipts remain development evidence, outside
the current public payload. Historical implementation is available in Git
history and the original teaching release; local `output/video/` paths and
Downloads copies are not portable publication links.
