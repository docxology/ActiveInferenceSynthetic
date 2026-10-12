# Methods: what each demonstration establishes

Synthetic is an executable teaching paper. Each model has its own carrier,
objective and assumptions. Similar language does not supply a mathematical
transfer between them.

| Model | Computation / units | Independent check | Limit |
| --- | --- | --- | --- |
| Categorical perception | Bayes and VFE, nats | Direct posterior and VFE/surprise identity | Requires positive evidence and compatible support |
| Isotropic OU drift | Deterministic RK4, model time | Linear analytic trajectory | A spiral is not an ensemble steady state |
| Matched-diffusion NESS | Stationary covariance/current/entropy rate | Lyapunov equation and detailed-balance controls | Physical units require thermodynamic conventions |
| Gaussian blanket | Conditional covariance | Precision-zero and coupled-endpoint controls | Statistical screening is not causal direction |
| One-step EFE | Preference cost minus mutual information, nats | Explicit branch enumeration | Supplied preferences and channels |
| Fixed action sequences | Terminal preference plus history information | Normalized history-channel correspondence | Open-loop sequence is not feedback control |
| Closed-loop agent | Observe, condition, choose commitment again | Informative versus independent cue | Fixed, supplied environment; no learned autonomy |
| Decision value | Optimal expected utility, acquisition cost | Every deterministic feedback policy enumerated independently | Static state, known channel/utilities, unchanged action set |
| Hierarchy | Context–state–observation joint | Direct enumeration and posterior marginals | Exact finite inference is not a neural implementation |

## Decision value: an executable next step

```python
import numpy as np
from active_inference_synthetic import value_of_information

cue = np.array([[0.9, 0.1], [0.1, 0.9]])  # rows: observations; columns: states
prior = np.array([0.5, 0.5])
utilities = np.eye(2)                     # rows: commitments; columns: states
result = value_of_information(cue, prior, utilities, cost=0.15)
print(result.feedback_actions, result.gross_value, result.net_value)
```

The feedback policy can choose a different commitment after each observation.
Gross information value compares this policy with the best prior-only action.
Net value subtracts acquisition cost. Utilities are declared task scores, not
measured energy or EFE. The same informative cue can have zero instrumental
value when action consequences do not depend on hidden state.

## Reproducible experiment orchestration

From the checkout:

```bash
uv run python scripts/run_teaching_experiments.py
uv run python scripts/generate_all_figures.py
uv run pytest tests/ --cov=src --cov-fail-under=90
```

The first command emits `output/data/teaching_experiments.json`: exact condition
inputs, expected utility values, information in nats and source hashes. A changed
source changes the receipt; missing source files prevent output. The figure
runner and token hydration use the same parameters and tested cores. This report
does not certify a published paper or validate a physical interpretation.

For extension, predict which conclusion should fail before changing the model.
Try a noisy cue, a skewed prior, a state-independent utility, or a cost that
outweighs information value. Preserve the control and record the assumptions
needed for the new conclusion. See [resources.md](resources.md) for deeper routes.
