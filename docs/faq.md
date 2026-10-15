# FAQ

## Why both deterministic trajectories and probability current?

Trajectories demonstrate the drift. `steady_state.py` computes the stationary
probability current and entropy production that certify broken detailed balance.

## Why can `gamma` be zero in one place but not another?

Pure deterministic flow permits `gamma == 0`. A stationary OU diffusion with
the implemented fluctuation–dissipation relation requires `gamma > 0`.

## Why is Lean separate from Python?

Python supplies executable demonstrations. Lean checks the load-bearing
mathematical statements without becoming a runtime dependency.

## Where do figure parameters live?

`src/demos.py`. Scientific operators live in `src/ou_model.py`.

## Are outputs tracked evidence?

This repository is public. `output/` is generated working state; preserve
existing evidence until replacement checks pass. The root PDF/video and
`media/synthetic/` companions are deliberate tracked release artifacts.
GitHub release assets and Zenodo records provide immutable distribution copies.

## Does the new agent learn a world model?

No. It conditions an explicitly supplied finite model and changes its subsequent
commitment. Informative and uninformative cues distinguish actual information
use from a label-driven decision.

## Are the original Gaussian and canonical native example the same law?

No. The second fixture exactly matches the upstream native carrier; that bridge
does not retroactively certify the original arbitrary precision matrix.

## Is terminal/history EFE the sum of one-step EFE?

No. The history-channel adapter requires normalized history preferences and an
explicit constant offset. The native controls expose the difference between
terminal preference cost, cumulative preference cost, and repeated information.
