#!/usr/bin/env python3
"""Pre-flight check for manuscript rendering prerequisites."""

from __future__ import annotations

import sys
from pathlib import Path


def _find_repo_root(start: Path) -> Path | None:
    """Walk parent directories until one contains ``infrastructure/``.

    A fixed ``parents[N]`` index breaks when this project is reached through
    its ``projects/working/<name>`` symlink into the private sidecar repo,
    because the canonical ``projects/templates/<name>/`` nesting depth no
    longer holds. Searching upward for the ``infrastructure/`` marker makes
    root resolution independent of nesting depth. ``absolute()`` (not
    ``resolve()``) is deliberate: the ``infrastructure/`` tree lives on the
    symlink side of the path, so the symlinked ancestors must be preserved.

    Returns ``None`` (instead of raising) when no ancestor carries the marker —
    the script is being run standalone, outside a template checkout.
    """
    for parent in (start, *start.parents):
        if (parent / "infrastructure").is_dir():
            return parent
    return None


def main() -> int:
    # Resolve the template repo root lazily (in ``main``) so importing this
    # module standalone does not crash: the template ``infrastructure/`` tree is
    # only present when running through the template checkout.
    repo_root = _find_repo_root(Path(__file__).absolute())
    if repo_root is None:
        sys.stderr.write(
            "00_preflight: no ancestor of this file contains an "
            "'infrastructure/' directory — the manuscript preflight requires "
            "the template checkout.\n"
            "Run this script from the template checkout, e.g.\n"
            "  uv run python projects/working/ActiveInferenceSynthetic/scripts/00_preflight.py\n"
        )
        return 2

    sys.path.insert(0, str(repo_root))
    try:
        from infrastructure.rendering.preflight import run_manuscript_preflight
    except ImportError as exc:  # pragma: no cover - defensive, infra is present here
        sys.stderr.write(
            f"00_preflight: could not import the preflight helper: {exc}\n"
        )
        return 2

    manuscript_dir = Path(__file__).resolve().parent.parent / "manuscript"
    ok, message = run_manuscript_preflight(manuscript_dir)
    if ok:
        return 0
    sys.stderr.write(message)
    return 1


if __name__ == "__main__":
    sys.exit(main())
