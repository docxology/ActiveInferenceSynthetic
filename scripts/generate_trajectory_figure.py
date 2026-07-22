#!/usr/bin/env python3
"""Render the worked-trajectories figure — equilibrium vs NESS paths.

Thin orchestrator: all numerics come from ``src.trajectories`` (which itself
integrates the tested flow in ``src.free_energy_flow``); this script only lays
out the panels and draws. Deterministic — no RNG.

The figure turns the overview's instantaneous flow field into *paths*:

* **(a) Equilibrium** — a trajectory falls straight to the mode and stops. Free
  energy decreases monotonically; net rotation about the mode is ~0.
* **(b) NESS** — the same descent plus a solenoidal current makes the path
  spiral, sweeping many full turns (a persistent probability current) while
  free energy still decreases. The measured net rotation is annotated on each
  panel, so the equilibrium↔NESS distinction is quantitative, not adjectival.

Output: ``output/figures/worked_trajectories.png``.
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
from src.trajectories import integrate_trajectory, net_rotation  # noqa: E402

# Colourblind-safe accents (Okabe–Ito), consistent with the overview figure.
_BLUE = "#0072B2"
_VERMILLION = "#D55E00"
_INK = "#222222"

PRECISION = 1.0
GAMMA = 1.0
OMEGA_NESS = 6.0  # solenoidal strength for the NESS panel
START = (2.6, 0.0)
DT = 0.002
STEPS = 6000


def _draw_landscape(ax: plt.Axes) -> None:
    """Grey free-energy contours shared by both regimes."""
    grid = np.linspace(-3.0, 3.0, 400)
    xx, yy = np.meshgrid(grid, grid)
    fe = free_energy(xx, yy, precision=PRECISION)
    ax.contourf(xx, yy, fe, levels=12, cmap="Greys", alpha=0.5)
    ax.contour(xx, yy, fe, levels=6, colors="white", linewidths=0.6, alpha=0.7)


def _draw_trajectory_panel(
    ax: plt.Axes, *, omega: float, title: str, color: str
) -> float:
    """Draw one integrated trajectory over the landscape; return net rotation."""
    _draw_landscape(ax)
    path = integrate_trajectory(
        START, precision=PRECISION, gamma=GAMMA, omega=omega, dt=DT, steps=STEPS
    )
    ax.plot(path[:, 0], path[:, 1], color=color, linewidth=1.4, zorder=4)
    ax.plot(*START, marker="o", markersize=6, color=color, zorder=6)
    ax.annotate("start", xy=START, xytext=(START[0] - 1.2, START[1] + 0.25),
                fontsize=8, color=color)
    ax.plot(0, 0, marker="o", markersize=8, color=_INK, zorder=6)
    ax.annotate("mode\n(min F)", xy=(0, 0), xytext=(0.35, 0.55), fontsize=8,
                color=_INK)

    # Total winding depends on the integration window T; the intrinsic,
    # IC-independent witness is the rotation *rate* dθ/dt = -ω·precision
    # (exactly 0 at equilibrium), reported here in turns per unit time.
    horizon = DT * STEPS
    turns = net_rotation(path) / (2.0 * np.pi)
    rate = turns / horizon
    ax.text(0.5, -0.09,
            f"rotation rate $\\approx$ {rate:+.2f} turns/time"
            f"\n({turns:+.2f} turns over window $T={horizon:g}$)",
            transform=ax.transAxes, ha="center", va="top", fontsize=8.5, color=color)

    ax.set_title(title, fontsize=11, fontweight="bold", color=_INK, pad=10)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    return net_rotation(path)


def build_figure() -> plt.Figure:
    """Assemble the two-panel worked-trajectories figure and return it."""
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 5.0))
    _draw_trajectory_panel(
        ax_l, omega=0.0,
        title=r"(a) Equilibrium — relaxes to rest", color=_BLUE,
    )
    _draw_trajectory_panel(
        ax_r, omega=OMEGA_NESS,
        title=r"(b) NESS — spirals, current persists", color=_VERMILLION,
    )
    fig.suptitle(
        "Worked trajectories: same landscape, same descent, two fates",
        fontsize=13, fontweight="bold", color=_INK, y=1.00,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    return fig


def main() -> Path:
    """Render the figure to ``output/figures`` and print its path."""
    out_dir = PROJECT_ROOT / "output" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "worked_trajectories.png"

    fig = build_figure()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(str(out_path))
    return out_path


if __name__ == "__main__":
    main()
