#!/usr/bin/env python3
"""Render all Active Inference manuscript figures."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.figures.render_all import render_all


def main() -> dict[str, Path]:
    manifest = render_all()
    for path in manifest.values():
        print(path)
    from src.manuscript_variables import (
        generate_variables,
        hydrate_manuscript,
        save_variables,
    )
    from src.project_paths import project_output_dirs

    root = Path(__file__).resolve().parent.parent
    variables = generate_variables(root)
    save_variables(
        variables, project_output_dirs(root)["data"] / "manuscript_variables.json"
    )
    hydrate_manuscript(root, variables)
    return manifest


if __name__ == "__main__":
    main()
