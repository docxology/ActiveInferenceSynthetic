"""Separate instrumental utility gain from information measured in nats."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..demos import (
    VOI_ACCURACIES, VOI_PRIOR, VOI_UTILITIES, VOI_COST, VOI_IRRELEVANT_UTILITIES,
)
from ..value_of_information import value_of_information
from . import palette
from .save import save_figure


def build_figure() -> plt.Figure:
    """Plot exact feedback value and its information/cost counterexamples."""
    results = [
        value_of_information(
            np.array([[r, 1-r], [1-r, r]]), VOI_PRIOR, VOI_UTILITIES, cost=VOI_COST,
        ) for r in VOI_ACCURACIES
    ]
    irrelevant = [
        value_of_information(
            np.array([[r, 1-r], [1-r, r]]), VOI_PRIOR, VOI_IRRELEVANT_UTILITIES,
        ).gross_value for r in VOI_ACCURACIES
    ]
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.4))
    axes[0].plot(VOI_ACCURACIES, [r.gross_value for r in results],
                 color=palette.BLUE, label="gross feedback value")
    axes[0].plot(VOI_ACCURACIES, [r.net_value for r in results],
                 color=palette.VERMILLION, label=f"net value (cost {VOI_COST:g})")
    axes[0].plot(VOI_ACCURACIES, irrelevant, "--", color=palette.GREY,
                 label="state-independent utility: zero gain")
    axes[0].axhline(0, color=palette.INK, linewidth=0.8)
    axes[0].set_ylabel("expected utility gain")
    axes[0].set_title("Information helps a decision only through its consequences")
    axes[0].legend(frameon=False, fontsize=8)
    axes[1].plot(VOI_ACCURACIES, [r.information_nats for r in results],
                 color=palette.GREEN)
    axes[1].set_ylabel("mutual information (nats)")
    axes[1].set_title("The same cue remains informative under either utility")
    for ax in axes:
        ax.set_xlabel("known cue accuracy")
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


def render(project_root: Path | None = None) -> Path:
    """Write the registered decision-value figure."""
    return save_figure(build_figure(), "value_of_information.png", project_root)
