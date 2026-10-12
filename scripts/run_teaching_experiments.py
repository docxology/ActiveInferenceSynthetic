"""Run the source-bound exact decision experiment suite from a checkout."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.experiment_suite import run_teaching_experiments


def main() -> Path:
    """Delegate numerical orchestration and print the generated report path."""
    path = run_teaching_experiments(ROOT)
    print(path)
    return path


if __name__ == "__main__":
    main()
