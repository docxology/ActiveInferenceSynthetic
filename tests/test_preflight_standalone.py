"""00_preflight must degrade when run outside the template checkout."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "00_preflight.py"


def test_preflight_exits_2_without_template_infrastructure() -> None:
    result = subprocess.run(
        [sys.executable, str(_SCRIPT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "infrastructure" in result.stderr
