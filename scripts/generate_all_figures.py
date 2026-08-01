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
    return manifest


if __name__ == "__main__":
    main()
