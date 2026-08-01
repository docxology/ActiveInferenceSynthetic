"""Expected-free-energy figure — explore/exploit."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..demos import ACTIONS, BELIEF, FLAT_PREFERENCES, SHARP_PREFERENCES
from ..expected_free_energy import select_policy
from . import palette
from .save import save_figure

ACTION_LABELS = ["explore\n(cue)", "exploit\n(bet)"]


def _draw_decision_panel(ax: plt.Axes, preferences: np.ndarray, title: str) -> None:
    result = select_policy(ACTIONS, BELIEF, preferences)
    idx = np.arange(len(ACTIONS))
    colors = [palette.GREY, palette.GREY]
    colors[result.choice] = palette.BLUE if result.choice == 0 else palette.VERMILLION
    ax.bar(idx, result.efe, color=colors, width=0.55, zorder=3)

    for index in range(len(ACTIONS)):
        x = float(index)
        ax.annotate(
            f"pragmatic {result.pragmatic[index]:+.2f}\n"
            f"epistemic {result.epistemic[index]:+.2f}",
            xy=(x, float(result.efe[index])),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            color=palette.INK,
        )
    ax.annotate(
        "chosen (min $G$)",
        xy=(result.choice, result.efe[result.choice]),
        xytext=(result.choice, result.efe[result.choice] - 0.12),
        ha="center",
        va="top",
        fontsize=8.5,
        fontweight="bold",
        color=colors[result.choice],
    )
    ax.set_xticks(idx)
    ax.set_xticklabels(ACTION_LABELS)
    ax.set_ylabel("expected free energy $G$  (lower chosen)")
    ax.set_title(title, fontsize=11, fontweight="bold", color=palette.INK, pad=8)
    ax.axhline(0.0, color=palette.INK, linewidth=0.6)
    ax.set_ylim(min(result.efe.min(), 0.0) - 0.35, result.efe.max() + 0.5)
    ax.spines[["top", "right"]].set_visible(False)


def build_figure() -> plt.Figure:
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 4.6), sharey=True)
    _draw_decision_panel(ax_l, FLAT_PREFERENCES, "(a) flat preferences → explore")
    _draw_decision_panel(ax_r, SHARP_PREFERENCES, "(b) sharp preferences → exploit")
    fig.suptitle(
        "Action as expected-free-energy minimization: one rule, explore and exploit",
        fontsize=12.5,
        fontweight="bold",
        color=palette.INK,
        y=1.00,
    )
    fig.tight_layout(rect=(0, 0.02, 1, 0.94))
    return fig


def render(project_root: Path | None = None) -> Path:
    return save_figure(build_figure(), "expected_free_energy.png", project_root)
