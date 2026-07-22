#!/usr/bin/env python3
"""Render the belief-updating figure — perception as free-energy minimization.

Thin orchestrator: all numerics come from ``src.generative_model``; this script
only lays out the panels and draws. Deterministic — no RNG.

The figure shows the *inference* half of Active Inference, the complement to the
overview's thermodynamic flow:

* **(a) Beliefs sharpen.** Starting from a maximally-uncommitted uniform belief,
  free-energy descent drives the belief over hidden states toward the exact
  Bayesian posterior — perception as belief updating under evidence.
* **(b) Free energy falls to surprise.** The variational free energy of the
  belief decreases monotonically to ``−ln p(s)``, the surprise it bounds. The
  gap that closes is exactly ``KL[q ‖ posterior]`` — the belief's error.

Output: ``output/figures/belief_update.png``.
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

from src.generative_model import (  # noqa: E402
    minimize_free_energy,
    posterior,
    surprise,
)

# Colourblind-safe accents (Okabe–Ito), consistent with the overview figure.
_BLUE = "#0072B2"
_VERMILLION = "#D55E00"
_GREEN = "#009E73"
_INK = "#222222"

# The demonstration model (parameters of the demo, like the overview's
# PRECISION/GAMMA/OMEGA): 2 hidden states, 2 observations. All inference math
# is done in src.generative_model.
PRIOR = np.array([0.6, 0.4])
LIKELIHOOD = np.array([[0.9, 0.2], [0.1, 0.8]])
OBS = 0  # the observed sensory index s
LEARNING_RATE = 0.3
STEPS = 60


def _draw_belief_panel(ax: plt.Axes, beliefs: np.ndarray, post: np.ndarray) -> None:
    """Belief bars: uniform start, an intermediate step, and the posterior."""
    labels = ["state $x_0$", "state $x_1$"]
    idx = np.arange(len(labels))
    width = 0.26

    ax.bar(idx - width, beliefs[0], width, label="start (uniform)", color="#BBBBBB")
    ax.bar(idx, beliefs[STEPS // 6], width, label="mid-descent", color=_BLUE, alpha=0.85)
    ax.bar(idx + width, post, width, label="posterior $p(x\\,|\\,s)$", color=_VERMILLION)

    ax.set_xticks(idx)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1)
    ax.set_ylabel("belief mass $q(x)$")
    ax.set_title("(a) beliefs sharpen toward the posterior", fontsize=11,
                 fontweight="bold", color=_INK, pad=8)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)


def _draw_free_energy_panel(ax: plt.Axes, fe: np.ndarray, surp: float) -> None:
    """Free-energy descent curve with the surprise asymptote."""
    it = np.arange(len(fe))
    ax.plot(it, fe, color=_GREEN, linewidth=2.0, zorder=3,
            label=r"variational free energy $F[q_t]$")
    ax.axhline(surp, color=_INK, linestyle="--", linewidth=1.1, zorder=2,
               label=r"surprise $-\ln p(s)$")
    ax.fill_between(it, fe, surp, color=_GREEN, alpha=0.12, zorder=1)

    ax.set_xlabel("inference step $t$")
    ax.set_ylabel("free energy (nats)")
    ax.set_title("(b) free energy falls to the surprise it bounds", fontsize=11,
                 fontweight="bold", color=_INK, pad=8)
    ax.annotate(
        r"gap $= \mathrm{KL}[q_t \Vert p(x|s)]$",
        xy=(len(fe) * 0.18, (fe[0] + surp) / 2),
        fontsize=8.5, color=_GREEN,
    )
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)


def build_figure() -> plt.Figure:
    """Assemble the two-panel belief-updating figure and return it."""
    trajectory = minimize_free_energy(
        LIKELIHOOD, PRIOR, OBS, learning_rate=LEARNING_RATE, steps=STEPS
    )
    post = posterior(LIKELIHOOD, PRIOR, OBS)
    surp = surprise(LIKELIHOOD, PRIOR, OBS)

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 4.2))
    _draw_belief_panel(ax_l, trajectory["beliefs"], post)
    _draw_free_energy_panel(ax_r, trajectory["free_energy"], surp)

    fig.suptitle(
        "Perception as inference: minimizing free energy is Bayesian updating",
        fontsize=13, fontweight="bold", color=_INK, y=1.00,
    )
    fig.tight_layout(rect=(0, 0.02, 1, 0.95))
    return fig


def main() -> Path:
    """Render the figure to ``output/figures`` and print its path."""
    out_dir = PROJECT_ROOT / "output" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "belief_update.png"

    fig = build_figure()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(str(out_path))
    return out_path


if __name__ == "__main__":
    main()
