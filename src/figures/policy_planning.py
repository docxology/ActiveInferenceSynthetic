"""Multi-step planning figure — look before leaping as EFE minimization."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..demos import ACTIONS, BELIEF, PLANNING_HORIZON, PLANNING_PREFERENCES
from ..policy_planning import select_multistep_policy
from . import palette
from .save import save_figure

POLICY_LABELS: dict[tuple[int, ...], str] = {
    (0, 0): "cue → cue",
    (0, 1): "cue → bet\n(look, then leap)",
    (1, 0): "bet → cue",
    (1, 1): "bet → bet\n(exploit first)",
}


def _policy_label(policy: tuple[int, ...]) -> str:
    return POLICY_LABELS.get(
        policy, " → ".join("cue" if a == 0 else "bet" for a in policy)
    )


def build_figure() -> plt.Figure:
    sel = select_multistep_policy(
        ACTIONS, BELIEF, PLANNING_PREFERENCES, PLANNING_HORIZON
    )
    idx = np.arange(len(sel.policies))
    colors = [palette.GREY] * len(sel.policies)
    colors[sel.choice] = palette.BLUE

    fig, ax = plt.subplots(figsize=(9.6, 4.8))
    ax.bar(idx, sel.efe, color=colors, width=0.55, zorder=3)

    for i in idx:
        x = float(i)
        ax.annotate(
            f"pragmatic {sel.pragmatic[i]:+.2f}\\nepistemic {sel.epistemic[i]:+.2f}",
            xy=(x, float(sel.efe[i])),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            color=palette.INK,
        )
    ax.annotate(
        "chosen (min $G$)",
        xy=(sel.choice, float(sel.efe[sel.choice])),
        xytext=(sel.choice, float(sel.efe[sel.choice]) - 0.12),
        ha="center",
        va="top",
        fontsize=8.5,
        fontweight="bold",
        color=palette.BLUE,
    )
    ax.set_xticks(idx)
    ax.set_xticklabels([_policy_label(p) for p in sel.policies], fontsize=9)
    ax.set_ylabel("expected free energy $G(\\pi)$  (lower chosen)")
    ax.set_title(
        "Planning as EFE minimization over action sequences — look before leaping",
        fontsize=12.5,
        fontweight="bold",
        color=palette.INK,
        pad=10,
    )
    ax.axhline(0.0, color=palette.INK, linewidth=0.6)
    ax.set_ylim(sel.efe.min() - 0.35, sel.efe.max() + 0.5)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


def render(project_root: Path | None = None) -> Path:
    return save_figure(build_figure(), "policy_planning.png", project_root)
