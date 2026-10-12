"""Two-level top-down prediction and bottom-up Bayesian updating."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from ..hierarchical_model import hierarchical_demo
from . import palette
from .save import save_figure


def build_figure() -> plt.Figure:
    update = hierarchical_demo()
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.2))
    panels = [
        ("Context", update.joint.sum(axis=(0, 1)), update.posterior_contexts),
        ("State", update.predicted_states, update.posterior_states),
        ("Predicted observation", update.predicted_observations, None),
    ]
    x = np.arange(2)
    for ax, (title, before, after) in zip(axes, panels, strict=True):
        ax.bar(
            x - 0.15 if after is not None else x,
            before,
            0.3 if after is not None else 0.55,
            color=palette.GREY,
            label="prediction",
        )
        if after is not None:
            ax.bar(x + 0.15, after, 0.3, color=palette.BLUE, label="posterior")
        ax.set_xticks(x, ["0", "1"])
        ax.set_ylim(0, 1.0)
        ax.set_title(title)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("probability")
    axes[0].legend(frameon=False)
    fig.suptitle(
        "A hierarchy: context predicts state; observation updates both levels",
        fontsize=13,
    )
    fig.tight_layout()
    return fig


def render(project_root: Path | None = None) -> Path:
    return save_figure(build_figure(), "hierarchical_inference.png", project_root)
