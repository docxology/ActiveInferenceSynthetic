"""Render all manuscript figures."""

from __future__ import annotations

from pathlib import Path

from . import (
    belief,
    blanket,
    efe,
    overview,
    policy_planning,
    steady_state,
    trajectories_figure,
)

FIGURE_RENDERERS = {
    "active_inference_overview.png": overview.render,
    "belief_update.png": belief.render,
    "worked_trajectories.png": trajectories_figure.render,
    "expected_free_energy.png": efe.render,
    "policy_planning.png": policy_planning.render,
    "markov_blanket.png": blanket.render,
    "steady_state_current.png": steady_state.render,
}


def render_all(project_root: Path | None = None) -> dict[str, Path]:
    """Build every figure once and return a filename → path manifest."""
    return {name: render(project_root) for name, render in FIGURE_RENDERERS.items()}
