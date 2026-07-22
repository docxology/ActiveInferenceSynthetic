#!/usr/bin/env python3
"""Render the expected-free-energy figure — the explore/exploit balance.

Thin orchestrator: all numerics come from ``src.expected_free_energy``; this
script only lays out the panels and draws. Deterministic — no RNG.

Two panels over the *same* two actions and belief, differing only in
preferences:

* **(a) Flat preferences** — the agent has no goal, so epistemic value (the
  informative "cue" action) dominates: it **explores**.
* **(b) Sharp preferences** — the agent strongly wants the reward, so pragmatic
  value (the rewarding "bet" action) dominates: it **exploits**.

The bars are the expected free energy $G$ per action (lower is chosen); the
annotation on each bar shows the pragmatic/epistemic split that produced it. The
same rule — minimize $G$ — yields both behaviours; nothing about explore/exploit
is hand-tuned.

Output: ``output/figures/expected_free_energy.png``.
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

from src.expected_free_energy import select_policy  # noqa: E402

# Colourblind-safe accents (Okabe–Ito), consistent with the other figures.
_BLUE = "#0072B2"
_VERMILLION = "#D55E00"
_GREY = "#BBBBBB"
_INK = "#222222"

# The decision (parameters of the demo). Belief: uncertain which context holds.
BELIEF = np.array([0.5, 0.5])
# "cue" reveals the state (informative); "bet" is uninformative but rewarding.
CUE = np.array([[0.9, 0.1], [0.1, 0.9]])
BET = np.array([[0.85, 0.85], [0.15, 0.15]])
ACTIONS = [CUE, BET]
ACTION_LABELS = ["explore\n(cue)", "exploit\n(bet)"]

FLAT = np.array([0.5, 0.5])  # no preference
SHARP = np.array([0.9, 0.1])  # strongly prefer outcome o0


def _draw_decision_panel(ax: plt.Axes, preferences: np.ndarray, title: str) -> None:
    """One panel: EFE per action with its pragmatic/epistemic split, winner lit."""
    result = select_policy(ACTIONS, BELIEF, preferences)
    efe = result["efe"]
    prag = result["pragmatic"]
    epi = result["epistemic"]
    choice = result["choice"]

    idx = np.arange(len(ACTIONS))
    colors = [_GREY, _GREY]
    colors[choice] = _BLUE if choice == 0 else _VERMILLION
    ax.bar(idx, efe, color=colors, width=0.55, zorder=3)

    for i in idx:
        ax.annotate(
            f"pragmatic {prag[i]:+.2f}\nepistemic {epi[i]:+.2f}",
            xy=(i, efe[i]),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            color=_INK,
        )
    ax.annotate(
        "chosen (min $G$)",
        xy=(choice, efe[choice]),
        xytext=(choice, efe[choice] - 0.12),
        ha="center",
        va="top",
        fontsize=8.5,
        fontweight="bold",
        color=colors[choice],
    )

    ax.set_xticks(idx)
    ax.set_xticklabels(ACTION_LABELS)
    ax.set_ylabel("expected free energy $G$  (lower chosen)")
    ax.set_title(title, fontsize=11, fontweight="bold", color=_INK, pad=8)
    ax.axhline(0.0, color=_INK, linewidth=0.6)
    ax.set_ylim(min(efe.min(), 0.0) - 0.35, efe.max() + 0.5)
    ax.spines[["top", "right"]].set_visible(False)


def build_figure() -> plt.Figure:
    """Assemble the two-panel explore/exploit figure and return it."""
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 4.6), sharey=True)
    _draw_decision_panel(ax_l, FLAT, "(a) flat preferences → explore")
    _draw_decision_panel(ax_r, SHARP, "(b) sharp preferences → exploit")
    fig.suptitle(
        "Action as expected-free-energy minimization: one rule, explore and exploit",
        fontsize=12.5, fontweight="bold", color=_INK, y=1.00,
    )
    fig.tight_layout(rect=(0, 0.02, 1, 0.94))
    return fig


def main() -> Path:
    """Render the figure to ``output/figures`` and print its path."""
    out_dir = PROJECT_ROOT / "output" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "expected_free_energy.png"

    fig = build_figure()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(str(out_path))
    return out_path


if __name__ == "__main__":
    main()
