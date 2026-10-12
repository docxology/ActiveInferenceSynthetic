"""Closed-loop perception and commitment with an uninformative control."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from ..synthetic_agent import synthetic_agent_demo
from . import palette
from .save import save_figure


def build_figure() -> plt.Figure:
    episodes = [
        synthetic_agent_demo(0),
        synthetic_agent_demo(1),
        synthetic_agent_demo(1, informative=False),
    ]
    labels = ["cue-left", "cue-right", "uninformative cue"]
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.4))
    x = np.arange(2)
    for ax, episode, label in zip(axes, episodes, labels, strict=True):
        ax.bar(x - 0.16, [0.5, 0.5], 0.30, color=palette.GREY, label="prior")
        ax.bar(x + 0.16, episode.posterior, 0.30, color=palette.BLUE, label="posterior")
        ax.set_xticks(x, ["left context", "right context"])
        ax.set_ylim(0, 1.18)
        ax.set_ylabel("belief probability")
        ax.set_title(label, fontsize=11)
        choice = ("left", "right")[episode.commitment.choice]
        ax.text(
            0.5,
            1.07,
            f"commit: {choice}",
            ha="center",
            transform=ax.transAxes,
            color=palette.VERMILLION,
        )
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].legend(frameon=False)
    fig.suptitle(
        "Observe → infer → act: information changes the next decision", fontsize=14
    )
    fig.tight_layout()
    return fig


def render(project_root: Path | None = None) -> Path:
    return save_figure(build_figure(), "synthetic_agent.png", project_root)
