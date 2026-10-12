"""Cover synthesis of numerical regimes and the separate evidence layers."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..demos import FLOW, OMEGA_NESS
from ..steady_state import probability_current
from . import palette
from .save import save_figure


def build_figure() -> plt.Figure:
    """Compose matched-density current panels and a qualified model-to-proof map."""
    fig = plt.figure(figsize=(10, 8.2), facecolor="white")
    fig.text(0.5, 0.97, "ONE DENSITY, TWO STATIONARY REGIMES", ha="center",
             fontsize=17, weight="bold", color=palette.INK)
    grid = np.linspace(-2.4, 2.4, 19)
    x, y = np.meshgrid(grid, grid)
    landscape = FLOW.free_energy(x, y)
    for left, omega, title, color, note in (
        (0.09, 0.0, "EQUILIBRIUM", palette.BLUE, "$j_*=0$, $\\sigma=0$  |  detailed balance"),
        (0.57, OMEGA_NESS, "NON-EQUILIBRIUM STEADY STATE", palette.VERMILLION,
         "$\\nabla\\cdot j_*=0$, $\\sigma>0$  |  circulation"),
    ):
        ax = fig.add_axes((left, 0.59, 0.34, 0.29))
        ax.contour(x, y, landscape, levels=8, colors=palette.GREY, linewidths=0.6)
        jx, jy = probability_current(x, y, precision=FLOW.precision,
                                     gamma=FLOW.gamma, omega=omega)
        if omega != 0:
            ax.quiver(x[::2, ::2], y[::2, ::2], jx[::2, ::2], jy[::2, ::2], color=color)
        else:
            ax.text(0, 0, "Zero ensemble current\nFluctuations remain", ha="center",
                    va="center", fontsize=11, color=color,
                    bbox={"facecolor": "white", "edgecolor": "none"})
        ax.set(aspect="equal", xticks=[], yticks=[])
        ax.set_title(title, fontsize=12, color=color, pad=12)
        for spine in ax.spines.values():
            spine.set_visible(False)
        fig.text(left + 0.17, 0.55, note, ha="center", fontsize=12, color=palette.INK)
    fig.text(0.5, 0.49, "$\\rho_*\\propto e^{-\\Phi}$   |   $D=\\Gamma>0$   |   both drift paths relax",
             ha="center", fontsize=15, color=palette.INK)
    fig.text(0.5, 0.445, "Even coordinates under time reversal; current concerns a stochastic ensemble.",
             ha="center", fontsize=12, color=palette.INK)
    fig.text(0.5, 0.38, "ACTIVE INFERENCE: A SEPARATE GENERATIVE-MODEL LAYER",
             ha="center", fontsize=14, weight="bold", color=palette.GREEN)
    fig.text(0.5, 0.33, "Observe  →  infer beliefs (VFE)  →  evaluate policies (EFE)  →  act",
             ha="center", fontsize=13, color=palette.INK)
    fig.text(0.5, 0.285, "Blankets: conditional independence  |  agency: explicit sensing and control",
             ha="center", fontsize=12, color=palette.INK)
    for position, title, detail in (
        (0.17, "GNN", "Specify variables,\nparameters and equations"),
        (0.50, "SYNTHETIC", "Compute examples,\ncontrols and figures"),
        (0.83, "FEP_FORMAL", "Import Lean results\nwith stated hypotheses"),
    ):
        fig.text(position, 0.19, title, ha="center", fontsize=14, weight="bold", color=palette.BLUE)
        fig.text(position, 0.13, detail, ha="center", va="center", fontsize=12, color=palette.INK)
    fig.text(0.5, 0.035, "Specification ≠ execution ≠ proof ≠ physical interpretation",
             ha="center", fontsize=13, color=palette.VERMILLION)
    return fig


def render(project_root: Path | None = None) -> Path:
    """Save the reproducible cover graphic through the shared figure boundary."""
    return save_figure(build_figure(), "graphical_abstract.png", project_root)
