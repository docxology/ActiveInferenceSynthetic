#!/usr/bin/env python3
"""Render the multi-step policy-planning figure."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.figures.policy_planning import render


def main():  # noqa: D103
    path = render()
    print(path)
    return path


if __name__ == "__main__":
    main()
