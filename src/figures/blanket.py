"""Markov-blanket figure."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..demos import (
    BLANKET_ETA_IDX,
    BLANKET_GIVEN_IDX,
    BLANKET_MU_IDX,
    BLANKET_PRECISION,
)
from ..markov_blanket import (
    correlation_matrix,
    covariance_from_precision,
    partial_correlation,
)
from . import palette
from .save import save_figure

LABELS = [
    (r"$\eta$" "\nexternal"),
    ("$s$\nsensory"),
    ("$a$\nactive"),
    (r"$\mu$" "\ninternal"),
]


def _draw_matrix(ax: plt.Axes, mat: np.ndarray, title: str, cmap: str) -> None:
    vlim = float(np.abs(mat).max())
    ax.imshow(mat, cmap=cmap, vmin=-vlim, vmax=vlim)
    n = mat.shape[0]
    for i in range(n):
        for j in range(n):
            ax.text(
                j,
                i,
                f"{mat[i, j]:.2f}",
                ha="center",
                va="center",
                fontsize=9,
                color=palette.INK,
            )
    for pair in ((BLANKET_ETA_IDX, BLANKET_MU_IDX), (BLANKET_MU_IDX, BLANKET_ETA_IDX)):
        i, j = pair
        ax.add_patch(
            plt.Rectangle(
                (j - 0.5, i - 0.5),
                1,
                1,
                fill=False,
                edgecolor=palette.VERMILLION,
                linewidth=2.5,
                zorder=5,
            )
        )
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(LABELS, fontsize=8)
    ax.set_yticklabels(LABELS, fontsize=8)
    ax.set_title(title, fontsize=11, fontweight="bold", color=palette.INK, pad=8)


def build_figure() -> plt.Figure:
    cov = covariance_from_precision(BLANKET_PRECISION)
    corr = correlation_matrix(cov)
    pcorr_full = partial_correlation(
        cov, BLANKET_ETA_IDX, BLANKET_MU_IDX, BLANKET_GIVEN_IDX
    )

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(10.2, 5.0))
    _draw_matrix(ax_l, corr, "(a) marginal correlation", "coolwarm")
    _draw_matrix(
        ax_r, BLANKET_PRECISION, "(b) precision (inverse covariance)", "coolwarm"
    )

    ax_l.text(
        0.5,
        -0.16,
        r"$\eta$ and $\mu$ are correlated: "
        f"corr $= {corr[BLANKET_ETA_IDX, BLANKET_MU_IDX]:+.2f}$",
        transform=ax_l.transAxes,
        ha="center",
        va="top",
        fontsize=9,
        color=palette.VERMILLION,
    )
    ax_r.text(
        0.5,
        -0.16,
        r"but $\Pi_{\eta\mu} = 0$  $\Rightarrow$  "
        r"$\eta \perp \mu \mid \{s,a\}$"
        f"\n(partial corr given blanket $= {pcorr_full:+.2f}$)",
        transform=ax_r.transAxes,
        ha="center",
        va="top",
        fontsize=9,
        color=palette.VERMILLION,
    )
    fig.suptitle(
        "The Markov blanket: internal and external states, screened by (s, a)",
        fontsize=12.5,
        fontweight="bold",
        color=palette.INK,
        y=1.00,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    return fig


def render(project_root: Path | None = None) -> Path:
    return save_figure(build_figure(), "markov_blanket.png", project_root)
