# Active Inference — A Synthetic Overview

An executable introduction to Active Inference and synthetic intelligences across
equilibrium and non-equilibrium thermodynamic and informational settings.
Daniel Ari Friedman and Alexandra Mikhailova, Active Inference Institute.

## Read, watch, reproduce

| Deliverable | Repository copy | Download |
| --- | --- | --- |
| Revised paper | [28-page PDF](ActiveInferenceSynthetic_Revised.pdf) | [Release PDF](https://github.com/docxology/ActiveInferenceSynthetic/releases/download/synthetic-public-v0.6.1/ActiveInferenceSynthetic_Revised.pdf) |
| Daniel lecture | [Twenty-minute MP4](ActiveInferenceSynthetic_20min.mp4) | [Release video](https://github.com/docxology/ActiveInferenceSynthetic/releases/download/synthetic-public-v0.6.1/ActiveInferenceSynthetic_20min.mp4) |
| Linked slides | [Slide PDF](media/synthetic/slides.pdf) | Included in the release |
| Captions | [SRT](media/synthetic/captions.srt), [WebVTT](media/synthetic/captions.vtt) | Included in the release |
| Narration | [Transcript](media/synthetic/transcript.txt), [speaker notes](media/synthetic/speaker_notes.md) | Included in the source archive |
| Replay inputs | [Lecture guide](docs/lecture.md) | [Frozen replay bundle](https://github.com/docxology/ActiveInferenceSynthetic/releases/download/synthetic-public-v0.6.1/ActiveInferenceSynthetic_Reproducibility.zip) |

The [public release](https://github.com/docxology/ActiveInferenceSynthetic/releases/tag/synthetic-public-v0.6.1)
packages the revised paper, five-animation lecture, source snapshot and documentation.
The [current Zenodo archive](https://zenodo.org/records/23396307) contains this
distribution. The [Zenodo version history](https://doi.org/10.5281/zenodo.23321280) retains each
archival edition, including the [original paper](https://zenodo.org/records/23321281).
[Publication details](docs/publication.md) distinguish the distribution version
**0.6.1**, scientific package/manuscript **0.5.0**, and frozen lecture **edition_v15**.

The PDF and MP4 are ordinary files at the repository root. Their exact byte
identities appear in [publication.json](publication.json) and
[SHA256SUMS.txt](SHA256SUMS.txt). GitHub may require downloading the video for
playback. Verify a checkout with `uv run python scripts/verify_publication.py`.

## Purpose and relationship to fep_formal

Synthetic makes a selected mathematical story concrete: how a model updates
beliefs, selects actions, plans, and represents a statistical boundary; how
relaxation differs from persistent stationary probability current; and how
these examples connect to the Free Energy Principle and Bayesian mechanics.
Its contribution is the teaching sequence, minimal numerical models, tested
examples, figures, and authored paper.

Start with the [methods and experiment guide](docs/methods.md) and the
[resource pathways](docs/resources.md). They distinguish numerical calculations,
formal reuse, vocabulary, model specifications, curricula and transcripts.

[**fep_formal**](https://github.com/ActiveInferenceInstitute/fep_formal) supplies
the broader mathematical reference and reusable formal library. Its interfaces
are `fep_lean` (Python), `fep-lean` (CLI), and `FepSketches` (Lean). Synthetic
selects and explains results from that library; substantive generic proofs
belong upstream. The optional
[GNN model-specification pathway](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation)
is introduced in that guide; the current demonstrations do not require or
execute GNN. See the [positioning and methods map](docs/positioning.md) for
section-level links and the protocol for advancing the upstream pin.

“Synthetic intelligences” is the intended application and teaching perspective.
The current examples are controlled mathematical demonstrations, not empirical
validation of an intelligent organism or a deployed autonomous agent. Persistent
NESS current alone does not establish life or intelligence. Variational free
energy, expected free energy, and thermodynamic free energy require their own
models and units; sharing a name does not establish a physical equivalence.

## The teaching sequence

- **Perception:** a discrete model, Bayesian posterior, and VFE bound.
- **Mechanics:** one Gaussian landscape with relaxation and circulating
  flow; RK4 drift trajectories are checked against an analytic solution.
- **Action:** pragmatic and epistemic contributions to one-step EFE.
- **Boundary:** Gaussian marginal dependence and blanket-conditioned independence.
- **Steady state:** matched-noise OU covariance, current, and entropy production.
- **Formal reference:** selected real-valued upstream results and explicit assumptions.
- **Planning:** action sequences with a static hidden state and conditional
  observation updates; this is distinct from general closed-loop control.
- **Synthetic agent:** informative observations change the next commitment,
  with a state-independent cue as the matched control.
- **Hierarchy:** context predicts state; one observation updates both hidden levels.
- **Decision value:** feedback utility gain, acquisition cost, and informative-but-irrelevant evidence separate learning from useful control.
- **Interpretation:** informational and thermodynamic units, assumptions, and limits.

Parameters and live manuscript values come from the numerical cores, not hand
edits to figures or rendered prose. Scientific scope and proof-transfer limits
are explicit in the [manuscript](docs/manuscript/README.md).

## Python package and imports

```bash
uv sync --locked --extra dev
```

The installed distribution provides the import namespace
`active_inference_synthetic`:

```python
from active_inference_synthetic import posterior
from active_inference_synthetic.synthetic_agent import synthetic_agent_demo
from active_inference_synthetic.hierarchical_model import hierarchical_demo

episode = synthetic_agent_demo(observation=1)
assert episode.commitment.choice == 1
hierarchy = hierarchical_demo()
```

Scripts run from this checkout retain local `src` imports. Lean dependencies
are acquired separately through Lake; there is no implicit Python import of
`fep_lean` or `gnn`. Numerical imports do not run upstream pipelines or load
provider credentials. Installed figure builders accept an explicit
`project_root` for output; manuscript hydration requires the source checkout.

## Run independently

```bash
uv sync --locked --extra dev
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/generate_all_figures.py
```

The numerical package, test collection, figures, and manuscript hydration need
no template or upstream Python package. When Lake is installed, the full suite
also builds the external formal dependency; missing formal prerequisites are
failures, not numerical verification.

For the real-valued formal layer, install the declared Lean toolchain and run:

```bash
(cd formal && lake build)
```

The committed Lake manifest pins a revision observed on upstream `main`, along
with its Lean/Mathlib dependencies. See [formal setup](formal/README.md) for
first-run acquisition and axiom auditing. Do not substitute a moving branch or
a local donor cache for the committed dependency.

PDF/HTML rendering currently uses the research template. From that template root:

```bash
uv run python scripts/pipeline/stage_03_render.py --project working/ActiveInferenceSynthetic
```

See [STANDALONE.md](STANDALONE.md) for execution boundaries and
[docs/README.md](docs/README.md) for operational guides. Outputs are generated
under `output/`; authored sources live under `docs/manuscript/`.

## Development

`src/` owns numerical cores and figure builders; `scripts/` are thin
orchestrators; `tests/` use real computation; `formal/` selects upstream theorems
and supplies paper-specific controls. [AGENTS.md](AGENTS.md) states the layer
contract. [ISA.md](ISA.md) defines purpose and acceptance;
[TODO.md](TODO.md) records implemented teaching extensions and their scope.
