#!/usr/bin/env python3
"""Render all Active Inference manuscript figures."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.figures.render_all import export_registry, render_all


def main() -> dict[str, Path]:
    manifest = render_all()
    for path in manifest.values():
        print(path)
    print(export_registry(Path(__file__).resolve().parent.parent))
    # The variables + hydration tail belongs to z_generate_manuscript_variables;
    # reuse its main() so both entry points share one code path (including the
    # template-infrastructure injector preference).
    from scripts.z_generate_manuscript_variables import main as generate_variables_tail

    generate_variables_tail()
    return manifest


if __name__ == "__main__":
    main()
