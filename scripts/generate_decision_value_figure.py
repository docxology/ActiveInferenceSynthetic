"""Render the decision-value figure through its registered builder."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.figures.decision_value import render


def main() -> Path:
    """Delegate to the figure builder."""
    path = render(ROOT)
    print(path)
    return path


if __name__ == "__main__":
    main()
