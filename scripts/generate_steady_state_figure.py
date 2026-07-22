#!/usr/bin/env python3
"""Render the steady-state figure — the probability current, made real.

Thin orchestrator: all numerics come from ``src.steady_state``; this script only
lays out the panels and draws. Deterministic — no RNG.

Where the trajectory figure showed a deterministic spiral (the *drift* of a
NESS), this one shows the actual **probability current** ``j(x) = (Q P x)ρ(x)``
of the corresponding stochastic steady state, over the stationary density:

* **(a) Equilibrium** (``omega = 0``): the current is zero everywhere — detailed
  balance, entropy production ``σ = 0``. The density just sits there.
* **(b) NESS** (``omega ≠ 0``): a divergence-free current circulates around the
  density forever; the entropy-production rate ``σ = 2ω²·precision/γ > 0`` is the
  thermodynamic price of that sustained motion.

Output: ``output/figures/steady_state_current.png``.
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

from src.free_energy_flow import free_energy  # noqa: E402
from src.steady_state import (  # noqa: E402
    entropy_production_rate,
    probability_current,
)

_BLUE = "#0072B2"
_VERMILLION = "#D55E00"
_INK = "#222222"

PRECISION = 1.0
GAMMA = 1.0
OMEGA_NESS = 2.4


def _draw_panel(ax: plt.Axes, *, omega: float, title: str, color: str) -> None:
    """Density contours plus the steady-state probability-current field."""
    grid = np.linspace(-3.0, 3.0, 400)
    xx, yy = np.meshgrid(grid, grid)
    # Stationary density ∝ exp(-F): reuse the tested free energy for the contours.
    fe = free_energy(xx, yy, precision=PRECISION)
    ax.contourf(xx, yy, fe, levels=12, cmap="Greys", alpha=0.5)
    ax.contour(xx, yy, fe, levels=6, colors="white", linewidths=0.6, alpha=0.7)

    qgrid = np.linspace(-2.4, 2.4, 15)
    qx, qy = np.meshgrid(qgrid, qgrid)
    jx, jy = probability_current(qx, qy, precision=PRECISION, gamma=GAMMA, omega=omega)
    mag = float(np.hypot(jx, jy).max())
    if mag > 0.0:
        ax.quiver(qx, qy, jx, jy, color=color, angles="xy", scale_units="xy",
                  scale=mag / 1.6, width=0.006, headwidth=4.0, zorder=4)
    else:
        ax.text(0.0, 0.0, "no current\n$j \\equiv 0$", ha="center", va="center",
                fontsize=10, color=color, fontweight="bold", zorder=6)

    ax.plot(0, 0, marker="o", markersize=8, color=_INK, zorder=6)
    sigma = entropy_production_rate(precision=PRECISION, gamma=GAMMA, omega=omega)
    ax.text(0.5, -0.09, f"entropy production $\\sigma = {sigma:.2f}$ nats/time",
            transform=ax.transAxes, ha="center", va="top", fontsize=9, color=color)

    ax.set_title(title, fontsize=11, fontweight="bold", color=_INK, pad=10)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def build_figure() -> plt.Figure:
    """Assemble the two-panel steady-state-current figure and return it."""
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 5.0))
    _draw_panel(ax_l, omega=0.0,
                title=r"(a) Equilibrium — no current, $\sigma=0$", color=_BLUE)
    _draw_panel(ax_r, omega=OMEGA_NESS,
                title=r"(b) NESS — sustained current, $\sigma>0$", color=_VERMILLION)
    fig.suptitle(
        "The steady state, quantified: probability current and entropy production",
        fontsize=12.5, fontweight="bold", color=_INK, y=1.00,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    return fig


def main() -> Path:
    """Render the figure to ``output/figures`` and print its path."""
    out_dir = PROJECT_ROOT / "output" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "steady_state_current.png"

    fig = build_figure()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(str(out_path))
    return out_path


if __name__ == "__main__":
    main()
