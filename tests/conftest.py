"""Pytest configuration for the ActiveInferenceSynthetic project tests."""

import os
import sys
from pathlib import Path

# Force headless backend for matplotlib in tests
os.environ.setdefault("MPLBACKEND", "Agg")

# Add src/ AND the repo root to path so the documented per-project pytest command
# works from a clean environment. The project pyproject's `pythonpath` is
# project-relative and omits the repo root, so without this the suite cannot
# import `infrastructure` (tests collect-error).
ROOT = Path(__file__).absolute().parent.parent
SRC = ROOT / "src"


def _find_repo_root(start: Path) -> Path:
    """Walk ancestors until one contains ``infrastructure/``.

    Checks both the literal path and its resolved target so the suite works
    when the project lives in the private sidecar but is executed through the
    template ``projects/working/`` symlink.
    """
    seen: set[Path] = set()
    queue: list[Path] = [
        start,
        *start.parents,
        start.resolve(),
        *start.resolve().parents,
    ]
    for parent in queue:
        if parent in seen:
            continue
        seen.add(parent)
        if (parent / "infrastructure").is_dir():
            return parent
    for parent in start.resolve().parents:
        sibling_template = parent / "template"
        if (sibling_template / "infrastructure").is_dir():
            return sibling_template
    raise RuntimeError(
        "Could not locate the repository root: no ancestor of "
        f"{start} contains an 'infrastructure/' directory."
    )


REPO_ROOT = _find_repo_root(ROOT)

for _path in (str(REPO_ROOT), str(ROOT), str(SRC)):
    if _path not in sys.path:
        sys.path.insert(0, _path)
