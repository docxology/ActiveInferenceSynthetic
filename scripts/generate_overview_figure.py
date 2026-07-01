#!/usr/bin/env python3
"""Render the single Active Inference overview figure.

Thin orchestrator: all numerics come from ``src.free_energy_flow``; this
script only lays out the panels and draws. Deterministic — no RNG.

The figure contrasts two regimes over *the same* Gaussian free-energy
landscape:

* **(a) Equilibrium** — pure gradient descent on free energy (the Free
  Energy Principle). Detailed balance holds, the flow spirals to rest at
  the mode, and there is no net probability current.
* **(b) Far-from-equilibrium (NESS)** — the same descent plus a solenoidal
  current (Bayesian mechanics' Helmholtz term). Free energy is still
  minimised, but probability mass circulates indefinitely.

Output: ``output/figures/active_inference_overview.png``.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for _path in (PROJECT_ROOT, PROJECT_ROOT / "src"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from src.free_energy_flow import flow_field, free_energy  # noqa: E402

# Colourblind-safe accents (Okabe–Ito).
_BLUE = "#0072B2"
_VERMILLION = "#D55E00"
_INK = "#222222"

PRECISION = 1.0
GAMMA = 1.0
OMEGA = 2.4  # solenoidal strength for the NESS panel


def _draw_panel(
    ax: plt.Axes,
    *,
    omega: float,
    title: str,
    subtitle: str,
    stream_color: str,
    style: str,
) -> None:
    """Draw free-energy contours plus the flow of the chosen regime.

    ``style='quiver'`` draws clean inward arrows (best for the purely
    dissipative equilibrium); ``style='stream'`` draws integrated
    streamlines (best for showing the persistent NESS circulation).
    """
    grid = np.linspace(-3.0, 3.0, 400)
    xx, yy = np.meshgrid(grid, grid)

    # Free-energy bowl as filled contours (low at the mode).
    fe = free_energy(xx, yy, precision=PRECISION)
    ax.contourf(xx, yy, fe, levels=12, cmap="Greys", alpha=0.55)
    ax.contour(xx, yy, fe, levels=6, colors="white", linewidths=0.6, alpha=0.7)

    if style == "quiver":
        qgrid = np.linspace(-2.7, 2.7, 13)
        qx, qy = np.meshgrid(qgrid, qgrid)
        fx, fy = flow_field(qx, qy, precision=PRECISION, gamma=GAMMA, omega=omega)
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
        fx, fy = flow_field(sx, sy, precision=PRECISION, gamma=GAMMA, omega=omega)
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

    # The mode (target of the free-energy descent).
    ax.plot(0, 0, marker="o", markersize=9, color=_INK, zorder=6)
    ax.annotate(
        "mode\n(min F)",
        xy=(0, 0),
        xytext=(0.6, 0.7),
        fontsize=8,
        color=_INK,
        ha="left",
        zorder=6,
    )

    ax.set_title(title, fontsize=12, fontweight="bold", color=_INK, pad=8)
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
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def build_figure() -> plt.Figure:
    """Assemble the two-panel overview figure and return it."""
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 4.9))

    _draw_panel(
        ax_l,
        omega=0.0,
        title="(a) Equilibrium",
        subtitle=r"$f=-\nabla F$   ·   detailed balance, $Q=0$"
        "\nflow comes to rest — no net current",
        stream_color=_BLUE,
        style="quiver",
    )
    _draw_panel(
        ax_r,
        omega=OMEGA,
        title="(b) Far-from-equilibrium (NESS)",
        subtitle=r"$f=(Q-\Gamma)\,\nabla F$   ·   $Q\neq 0$"
        "\nfree energy still minimised — current persists",
        stream_color=_VERMILLION,
        style="stream",
    )

    fig.suptitle(
        "Active Inference: one free-energy landscape, two regimes",
        fontsize=13.5,
        fontweight="bold",
        color=_INK,
        y=1.00,
    )
    # Bottom strip: the Free Energy Principle one-liner + Markov blanket.
    fig.text(
        0.5,
        0.015,
        r"Free Energy Principle: internal states $\mu$ minimise variational free energy "
        r"$F \geq -\ln p(s)$ across a Markov blanket  external $\eta \mid$ sensory $s$, "
        r"active $a \mid$ internal $\mu$.",
        ha="center",
        va="bottom",
        fontsize=8.5,
        color=_INK,
    )

    fig.tight_layout(rect=(0, 0.06, 1, 0.96))
    return fig


def main() -> Path:
    """Render the figure to ``output/figures`` and print its path."""
    out_dir = PROJECT_ROOT / "output" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "active_inference_overview.png"

    fig = build_figure()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(str(out_path))
    return out_path


if __name__ == "__main__":
    main()
