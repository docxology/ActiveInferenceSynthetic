"""Belief-update figure — perception as free-energy minimization."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..demos import (
    BELIEF_LEARNING_RATE,
    BELIEF_OBS,
    BELIEF_STEPS,
    LIKELIHOOD,
    PRIOR,
)
from ..generative_model import minimize_free_energy, posterior, surprise
from . import palette
from .save import save_figure


def build_figure() -> plt.Figure:
    trajectory = minimize_free_energy(
        LIKELIHOOD,
        PRIOR,
        BELIEF_OBS,
        learning_rate=BELIEF_LEARNING_RATE,
        steps=BELIEF_STEPS,
    )
    post = posterior(LIKELIHOOD, PRIOR, BELIEF_OBS)
    surp = surprise(LIKELIHOOD, PRIOR, BELIEF_OBS)

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(9.6, 4.2))

    labels = ["state $x_0$", "state $x_1$"]
    idx = np.arange(len(labels))
    width = 0.26
    ax_l.bar(
        idx - width,
        trajectory.beliefs[0],
        width,
        label="start (uniform)",
        color=palette.GREY,
    )
    ax_l.bar(
        idx,
        trajectory.beliefs[BELIEF_STEPS // 6],
        width,
        label="mid-descent",
        color=palette.BLUE,
        alpha=0.85,
    )
    ax_l.bar(
        idx + width,
        post,
        width,
        label="posterior $p(x\\,|\\,s)$",
        color=palette.VERMILLION,
    )
    ax_l.set_xticks(idx)
    ax_l.set_xticklabels(labels)
    ax_l.set_ylim(0, 1)
    ax_l.set_ylabel("belief mass $q(x)$")
    ax_l.set_title(
        "(a) beliefs sharpen toward the posterior",
        fontsize=11,
        fontweight="bold",
        color=palette.INK,
        pad=8,
    )
    ax_l.legend(frameon=False, fontsize=8, loc="upper right")
    ax_l.spines[["top", "right"]].set_visible(False)

    it = np.arange(len(trajectory.free_energy))
    ax_r.plot(
        it,
        trajectory.free_energy,
        color=palette.GREEN,
        linewidth=2.0,
        zorder=3,
        label=r"variational free energy $F[q_t]$",
    )
    ax_r.axhline(
        surp,
        color=palette.INK,
        linestyle="--",
        linewidth=1.1,
        zorder=2,
        label=r"surprise $-\ln p(s)$",
    )
    ax_r.fill_between(
        it, trajectory.free_energy, surp, color=palette.GREEN, alpha=0.12, zorder=1
    )
    ax_r.set_xlabel("inference step $t$")
    ax_r.set_ylabel("free energy (nats)")
    ax_r.set_title(
        "(b) free energy falls to the surprise it bounds",
        fontsize=11,
        fontweight="bold",
        color=palette.INK,
        pad=8,
    )
    ax_r.annotate(
        r"gap $= \mathrm{KL}[q_t \Vert p(x|s)]$",
        xy=(len(trajectory.free_energy) * 0.18, (trajectory.free_energy[0] + surp) / 2),
        fontsize=8.5,
        color=palette.GREEN,
    )
    ax_r.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax_r.spines[["top", "right"]].set_visible(False)

    fig.suptitle(
        "Perception as inference: minimizing free energy is Bayesian updating",
        fontsize=13,
        fontweight="bold",
        color=palette.INK,
        y=1.00,
    )
    fig.tight_layout(rect=(0, 0.02, 1, 0.95))
    return fig


def render(project_root: Path | None = None) -> Path:
    return save_figure(build_figure(), "belief_update.png", project_root)
