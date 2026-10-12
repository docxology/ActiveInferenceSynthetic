"""Worked-trajectories figure."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from ..demos import (
    FLOW,
    TRAJECTORY_DT,
    TRAJECTORY_OMEGA_NESS,
    TRAJECTORY_START,
    TRAJECTORY_STEPS,
)
from ..ou_model import IsotropicOU
from ..trajectories import integrate_trajectory, net_rotation
from . import palette
from .landscape import draw_landscape, style_spatial_panel
from .save import save_figure


def _draw_trajectory_panel(
    ax: plt.Axes, *, model: IsotropicOU, title: str, color: str
) -> None:
    draw_landscape(ax, model)
    path = integrate_trajectory(
        TRAJECTORY_START,
        precision=model.precision,
        gamma=model.gamma,
        omega=model.omega,
        dt=TRAJECTORY_DT,
        steps=TRAJECTORY_STEPS,
    )
    ax.plot(path[:, 0], path[:, 1], color=color, linewidth=1.4, zorder=4)
    ax.plot(*TRAJECTORY_START, marker="o", markersize=6, color=color, zorder=6)
    ax.annotate(
        "start",
        xy=TRAJECTORY_START,
        xytext=(TRAJECTORY_START[0] - 1.2, TRAJECTORY_START[1] + 0.25),
        fontsize=8,
        color=color,
    )
    ax.plot(0, 0, marker="o", markersize=8, color=palette.INK, zorder=6)
    ax.annotate(
        "mode\n(min F)",
        xy=(0, 0),
        xytext=(0.35, 0.55),
        fontsize=8,
        color=palette.INK,
    )

    horizon = TRAJECTORY_DT * TRAJECTORY_STEPS
    turns = net_rotation(path) / (2.0 * 3.141592653589793)
    rate = turns / horizon
    ax.text(
        0.5,
        -0.09,
        f"rotation rate $\\approx$ {rate:+.2f} turns/time"
        f"\n({turns:+.2f} turns over window $T={horizon:g}$)",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=8.5,
        color=color,
    )
    ax.set_title(title, fontsize=11, fontweight="bold", color=palette.INK, pad=10)
    style_spatial_panel(ax)


def build_figure() -> plt.Figure:
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 5.0))
    _draw_trajectory_panel(
        ax_l,
        model=FLOW,
        title=r"(a) Equilibrium — relaxes to rest",
        color=palette.BLUE,
    )
    ness = IsotropicOU(
        precision=FLOW.precision,
        gamma=FLOW.gamma,
        omega=TRAJECTORY_OMEGA_NESS,
    )
    _draw_trajectory_panel(
        ax_r,
        model=ness,
        title=r"(b) Rotating drift — spirals and relaxes",
        color=palette.VERMILLION,
    )
    fig.suptitle(
        "Worked trajectories: same landscape, same descent, two fates",
        fontsize=13,
        fontweight="bold",
        color=palette.INK,
        y=1.00,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    return fig


def render(project_root: Path | None = None) -> Path:
    return save_figure(build_figure(), "worked_trajectories.png", project_root)
