"""Overview figure — equilibrium vs NESS flow."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..demos import FLOW, OMEGA_NESS
from ..ou_model import IsotropicOU
from . import palette
from .landscape import draw_landscape, draw_mode_marker, style_spatial_panel
from .save import save_figure


def _draw_panel(
    ax: plt.Axes,
    *,
    model: IsotropicOU,
    title: str,
    subtitle: str,
    stream_color: str,
    style: str,
) -> None:
    draw_landscape(ax, model)
    if style == "quiver":
        qgrid = np.linspace(-2.7, 2.7, 13)
        qx, qy = np.meshgrid(qgrid, qgrid)
        fx, fy = model.flow_field(qx, qy)
        ax.quiver(
            qx,
            qy,
            fx,
            fy,
            color=stream_color,
            angles="xy",
            scale_units="xy",
            scale=4.0,
            width=0.006,
            headwidth=4.0,
            zorder=4,
        )
    else:
        sgrid = np.linspace(-3.0, 3.0, 36)
        sx, sy = np.meshgrid(sgrid, sgrid)
        fx, fy = model.flow_field(sx, sy)
        ax.streamplot(
            sx,
            sy,
            fx,
            fy,
            color=stream_color,
            density=1.1,
            linewidth=1.0,
            arrowsize=1.2,
            broken_streamlines=False,
        )

    draw_mode_marker(ax)
    ax.set_title(title, fontsize=12, fontweight="bold", color=palette.INK, pad=8)
    ax.text(
        0.5,
        -0.13,
        subtitle,
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=9,
        color=stream_color,
    )
    style_spatial_panel(ax)


def build_figure() -> plt.Figure:
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 4.9))
    _draw_panel(
        ax_l,
        model=FLOW,
        title="(a) Equilibrium",
        subtitle=r"$f=-\nabla F$   ·   detailed balance, $Q=0$"
        "\nflow comes to rest — no net current",
        stream_color=palette.BLUE,
        style="quiver",
    )
    ness = IsotropicOU(
        precision=FLOW.precision,
        gamma=FLOW.gamma,
        omega=OMEGA_NESS,
    )
    _draw_panel(
        ax_r,
        model=ness,
        title="(b) Far-from-equilibrium (NESS)",
        subtitle=r"$f=(Q-\Gamma)\,\nabla F$   ·   $Q\neq 0$"
        "\nfree energy still minimised — current persists",
        stream_color=palette.VERMILLION,
        style="stream",
    )
    fig.suptitle(
        "Active Inference: one free-energy landscape, two regimes",
        fontsize=13.5,
        fontweight="bold",
        color=palette.INK,
        y=1.00,
    )
    fig.text(
        0.5,
        0.015,
        r"Free Energy Principle: internal states $\mu$ minimise variational free energy "
        r"$F \geq -\ln p(s)$ across a Markov blanket  external $\eta \mid$ sensory $s$, "
        r"active $a \mid$ internal $\mu$.",
        ha="center",
        va="bottom",
        fontsize=8.5,
        color=palette.INK,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.96))
    return fig


def render(project_root: Path | None = None) -> Path:
    return save_figure(build_figure(), "active_inference_overview.png", project_root)
