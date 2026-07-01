#!/usr/bin/env python3
"""Pre-flight check for manuscript rendering prerequisites."""

from __future__ import annotations

import sys
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    """Walk parent directories until one contains ``infrastructure/``.

    A fixed ``parents[N]`` index breaks when this project is reached through
    its ``projects/working/<name>`` symlink into the private sidecar repo,
    because the canonical ``projects/templates/<name>/`` nesting depth no
    longer holds. Searching upward for the ``infrastructure/`` marker makes
    root resolution independent of nesting depth. ``absolute()`` (not
    ``resolve()``) is deliberate: the ``infrastructure/`` tree lives on the
    symlink side of the path, so the symlinked ancestors must be preserved.
    """
    for parent in (start, *start.parents):
        if (parent / "infrastructure").is_dir():
            return parent
    raise RuntimeError(
        "Could not locate the repository root: no ancestor of "
        f"{start} contains an 'infrastructure/' directory."
    )


REPO_ROOT = _find_repo_root(Path(__file__).absolute())
sys.path.insert(0, str(REPO_ROOT))

from infrastructure.rendering.preflight import run_manuscript_preflight  # noqa: E402


def main() -> int:
    manuscript_dir = Path(__file__).resolve().parent.parent / "manuscript"
    ok, message = run_manuscript_preflight(manuscript_dir)
    if ok:
        return 0
    sys.stderr.write(message)
    return 1


if __name__ == "__main__":
    sys.exit(main())
