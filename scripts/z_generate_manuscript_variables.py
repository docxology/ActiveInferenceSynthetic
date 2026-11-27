#!/usr/bin/env python3
"""Thin orchestrator: generate and inject manuscript variables.

Writes ``output/data/manuscript_variables.json`` and hydrates
``output/manuscript/``. Computation lives in ``src.manuscript_variables``.
The project hydrator resolves paths from canonical docs/manuscript sources.
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))


def main() -> int:
    from src.manuscript_variables import (
        generate_variables,
        hydrate_manuscript,
        save_variables,
    )
    from src.project_paths import project_output_dirs

    variables = generate_variables(_PROJECT_ROOT)
    out_path = project_output_dirs(_PROJECT_ROOT)["data"] / "manuscript_variables.json"
    save_variables(variables, out_path)

    hydrate_manuscript(_PROJECT_ROOT, variables)
    print(str(out_path))
    print(str(project_output_dirs(_PROJECT_ROOT)["output"] / "manuscript"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
