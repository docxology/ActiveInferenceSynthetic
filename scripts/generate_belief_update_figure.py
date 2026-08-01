#!/usr/bin/env python3
"""Render the belief-updating figure."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.figures.belief import render


def main():
    path = render()
    print(path)
    return path


if __name__ == "__main__":
    main()
