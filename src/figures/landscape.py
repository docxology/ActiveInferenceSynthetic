"""Shared free-energy landscape drawing."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from ..ou_model import IsotropicOU
from . import palette


def draw_landscape(ax: plt.Axes, model: IsotropicOU) -> None:
    """Grey free-energy contours on ``ax``."""
    grid = np.linspace(-3.0, 3.0, 400)
    xx, yy = np.meshgrid(grid, grid)
    fe = model.free_energy(xx, yy)
    ax.contourf(xx, yy, fe, levels=12, cmap="Greys", alpha=0.55)
    ax.contour(xx, yy, fe, levels=6, colors="white", linewidths=0.6, alpha=0.7)


def style_spatial_panel(ax: plt.Axes) -> None:
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def draw_mode_marker(ax: plt.Axes) -> None:
    ax.plot(0, 0, marker="o", markersize=9, color=palette.INK, zorder=6)
    ax.annotate(
        "mode\n(min F)",
        xy=(0, 0),
        xytext=(0.6, 0.7),
        fontsize=8,
        color=palette.INK,
        ha="left",
        zorder=6,
    )
