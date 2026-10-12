# Methods and Reproducibility {#sec:methods}

The examples are deliberately small models with declared inputs, rather than
empirical estimates of biological or artificial-system performance. Numerical
parameters are shared between figure builders and tests in `src/demos.py`.
Manuscript tokens are computed by the same numerical cores and hydrated before
the template renders the paper. Each figure caption identifies the corresponding
model or script; the figure registry binds labels, filenames and builders.

Finite probability channels store outcomes in rows and hidden states in
columns. Their columns are normalized; beliefs are probability vectors.
Conditioning enumerates reachable observations or observation histories.
The decision-value calculation compares the best prior commitment with optimal
observation-contingent commitments under the same state, actions, utilities and
acquisition cost. Impossible outcomes do not acquire invented posteriors.
These finite enumerations cover their specified branch spaces, while their
Python arithmetic remains floating point with explicit validation and test
tolerances. They do not establish an optimum outside the declared model class.

Independent references are chosen for each model: direct Bayes conditioning for
belief updates, alternative free-energy decompositions, exhaustive deterministic
feedback policies for decision value, the linear closed form for RK4 paths,
and Gaussian covariance and precision identities for blanket screening. The
OU stationary calculations additionally require matched diffusion and positive
dissipation. A deterministic path is not substituted for stationary current.
Information is reported in nats; utility and observation cost share declared
utility units; physical thermodynamic interpretations require extra scaling.

Counterexamples exercise interpretation boundaries. Independent cues provide
no context information. Informative cues with state-independent utilities give
no instrumental gain. Excessive observation cost can make net gain negative.
Partial blanket conditioning and altered precision couplings need not preserve
screening. Invalid probabilities, support mismatches and nonfinite quantities
are rejected. The formal tests also check that false Lean statements fail,
rather than relying only on successful proof builds.

The package's installed namespace is `active_inference_synthetic`. Reproduction
from the standalone project uses:

```bash
uv sync --locked --extra dev
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/generate_all_figures.py
uv run python scripts/run_teaching_experiments.py
```

The last command records
inputs, computed decision values and source hashes for the informative,
uninformative and irrelevant-payoff conditions. A changed or missing source
changes or blocks that receipt. Such a receipt establishes the inputs of a
particular execution; it is not certification of a scientific interpretation.

The independent formal layer builds with `lake build` from `formal/` and pins
FEP_Formal through Lake. The publication renderer belongs to the template
repository. Python execution, Lean checking, rendered-document inspection and
publication-file integrity are separate verification steps. The accompanying
source archive supplies the authored numerical, test, formal and manuscript
files; it excludes local environments, credentials and intermediate runtime
state. The resource guide identifies further mathematical and educational
materials [@sec:resources].
