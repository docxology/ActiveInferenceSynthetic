#!/usr/bin/env python3
"""Render the Markov-blanket figure — conditional independence made visible.

Thin orchestrator: all numerics come from ``src.markov_blanket``; this script
only lays out the panels and draws. Deterministic — no RNG.

A joint Gaussian over external ``eta``, sensory ``s``, active ``a``, internal
``mu`` is built with a zero ``eta``-``mu`` precision block, so the blanket
``b = (s, a)`` renders internal and external states conditionally independent.
Two panels show the payoff:

* **(a) Marginal correlation** — ``eta`` and ``mu`` are correlated: they *do*
  influence each other (through the blanket). The off-diagonal ``eta``-``mu``
  cell is clearly nonzero.
* **(b) Precision (inverse covariance)** — the ``eta``-``mu`` entry is exactly
  zero. In a Gaussian, a zero precision entry *is* conditional independence
  given the other variables, so the blanket screens internal from external.

Output: ``output/figures/markov_blanket.png``.
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

from src.markov_blanket import (  # noqa: E402
    correlation_matrix,
    covariance_from_precision,
    partial_correlation,
)

_INK = "#222222"

# Precision (inverse covariance) over (eta, s, a, mu). The zero eta-mu block
# (corners) encodes eta ⊥ mu | {s, a}. eta and mu each couple to BOTH blanket
# states, so no strict subset of the blanket screens them.
PRECISION = np.array(
    [
        [2.5, -0.8, -0.4, 0.0],
        [-0.8, 2.5, -0.5, -0.7],
        [-0.4, -0.5, 2.5, -0.6],
        [0.0, -0.7, -0.6, 2.5],
    ]
)
COV = covariance_from_precision(PRECISION)
LABELS = [r"$\eta$" "\nexternal", "$s$\nsensory", "$a$\nactive", r"$\mu$" "\ninternal"]
_ETA, _MU = 0, 3


def _draw_matrix(ax: plt.Axes, mat: np.ndarray, title: str, cmap: str) -> None:
    """Heatmap of a 4x4 matrix with per-cell numeric annotations."""
    vlim = float(np.abs(mat).max())
    im = ax.imshow(mat, cmap=cmap, vmin=-vlim, vmax=vlim)
    n = mat.shape[0]
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center",
                    fontsize=9, color=_INK)
    # Ring the eta-mu cells (both off-diagonal corners).
    for (i, j) in [(_ETA, _MU), (_MU, _ETA)]:
        ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                                   edgecolor="#D55E00", linewidth=2.5, zorder=5))
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(LABELS, fontsize=8)
    ax.set_yticklabels(LABELS, fontsize=8)
    ax.set_title(title, fontsize=11, fontweight="bold", color=_INK, pad=8)
    return im


def build_figure() -> plt.Figure:
    """Assemble the two-panel Markov-blanket figure and return it."""
    corr = correlation_matrix(COV)
    pcorr_full = partial_correlation(COV, _ETA, _MU, [1, 2])

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(10.2, 5.0))
    _draw_matrix(ax_l, corr, "(a) marginal correlation", "coolwarm")
    _draw_matrix(ax_r, PRECISION, "(b) precision (inverse covariance)", "coolwarm")

    ax_l.text(0.5, -0.16,
              r"$\eta$ and $\mu$ are correlated: "
              f"corr $= {corr[_ETA, _MU]:+.2f}$",
              transform=ax_l.transAxes, ha="center", va="top", fontsize=9,
              color="#D55E00")
    ax_r.text(0.5, -0.16,
              r"but $\Pi_{\eta\mu} = 0$  $\Rightarrow$  "
              r"$\eta \perp \mu \mid \{s,a\}$"
              f"\n(partial corr given blanket $= {pcorr_full:+.2f}$)",
              transform=ax_r.transAxes, ha="center", va="top", fontsize=9,
              color="#D55E00")

    fig.suptitle(
        "The Markov blanket: internal and external states, screened by (s, a)",
        fontsize=12.5, fontweight="bold", color=_INK, y=1.00,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    return fig


def main() -> Path:
    """Render the figure to ``output/figures`` and print its path."""
    out_dir = PROJECT_ROOT / "output" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "markov_blanket.png"

    fig = build_figure()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(str(out_path))
    return out_path


if __name__ == "__main__":
    main()
