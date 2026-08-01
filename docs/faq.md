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

This is a private working project. Treat `output/` as regeneratable local state.
