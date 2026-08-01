"""Figure save helpers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from ..project_paths import project_output_dirs


def save_figure(
    fig: plt.Figure, filename: str, project_root: Path | None = None
) -> Path:
    """Save ``fig`` under ``output/figures/`` and return the path."""
    figures_dir = project_output_dirs(project_root)["figures"]
    figures_dir.mkdir(parents=True, exist_ok=True)
    out_path = figures_dir / filename
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out_path
