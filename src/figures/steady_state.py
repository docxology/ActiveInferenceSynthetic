"""Steady-state probability-current figure."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..demos import FLOW, OMEGA_NESS
from ..ou_model import IsotropicOU
from ..steady_state import entropy_production_rate, probability_current
from . import palette
from .landscape import draw_landscape, style_spatial_panel
from .save import save_figure


def _draw_panel(ax: plt.Axes, *, model: IsotropicOU, title: str, color: str) -> None:
    draw_landscape(ax, model)
    qgrid = np.linspace(-2.4, 2.4, 15)
    qx, qy = np.meshgrid(qgrid, qgrid)
    jx, jy = probability_current(
        qx,
        qy,
        precision=model.precision,
        gamma=model.gamma,
        omega=model.omega,
    )
    mag = float(np.hypot(jx, jy).max())
    if mag > 0.0:
        ax.quiver(
            qx,
            qy,
            jx,
            jy,
            color=color,
            angles="xy",
            scale_units="xy",
            scale=mag / 1.6,
            width=0.006,
            headwidth=4.0,
            zorder=4,
        )
    else:
        ax.text(
            0.0,
            0.0,
            "no current\n$j \\equiv 0$",
            ha="center",
            va="center",
            fontsize=10,
            color=color,
            fontweight="bold",
            zorder=6,
        )

    ax.plot(0, 0, marker="o", markersize=8, color=palette.INK, zorder=6)
    sigma = entropy_production_rate(
        precision=model.precision,
        gamma=model.gamma,
        omega=model.omega,
    )
    ax.text(
        0.5,
        -0.09,
        f"entropy production $\\sigma = {sigma:.2f}$ nats/time",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=9,
        color=color,
    )
    ax.set_title(title, fontsize=11, fontweight="bold", color=palette.INK, pad=10)
    style_spatial_panel(ax)


def build_figure() -> plt.Figure:
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 5.0))
    _draw_panel(
        ax_l,
        model=FLOW,
        title=r"(a) Equilibrium — no current, $\sigma=0$",
        color=palette.BLUE,
    )
    ness = IsotropicOU(
        precision=FLOW.precision,
        gamma=FLOW.gamma,
        omega=OMEGA_NESS,
    )
    _draw_panel(
        ax_r,
        model=ness,
        title=r"(b) NESS — sustained current, $\sigma>0$",
        color=palette.VERMILLION,
    )
    fig.suptitle(
        "The steady state, quantified: probability current and entropy production",
        fontsize=12.5,
        fontweight="bold",
        color=palette.INK,
        y=1.00,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    return fig


def render(project_root: Path | None = None) -> Path:
    return save_figure(build_figure(), "steady_state_current.png", project_root)
