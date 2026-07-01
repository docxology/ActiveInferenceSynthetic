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
    """Walk parent directories until one contains ``infrastructure/``.

    A fixed ``../../..`` hop assumes the canonical ``projects/templates/<name>/``
    nesting depth and breaks once this project is reached through its
    ``projects/working/<name>`` symlink into the private sidecar repo. Searching
    upward for the ``infrastructure/`` marker makes root resolution independent
    of nesting depth. ``absolute()`` (not ``resolve()``) is deliberate: the
    ``infrastructure/`` tree lives on the symlink side of the path, so the
    symlinked ancestors must be preserved.
    """
    for parent in (start, *start.parents):
        if (parent / "infrastructure").is_dir():
            return parent
    raise RuntimeError(
        "Could not locate the repository root: no ancestor of "
        f"{start} contains an 'infrastructure/' directory."
    )


REPO_ROOT = _find_repo_root(ROOT)

for _path in (str(REPO_ROOT), str(SRC)):
    if _path not in sys.path:
        sys.path.insert(0, _path)
