"""Smoke test for scripts/generate_overview_figure.py.

The overview figure is the manuscript's sole anchor ([@fig:overview]), so its
generator gets a direct test that it actually writes a real, non-empty PNG.

No mocks: ``main()`` runs the real matplotlib render over the real tested flow
in ``src.free_energy_flow``. Only the output *location* is redirected — via
``pytest``'s ``MonkeyPatch`` on the module's ``PROJECT_ROOT`` attribute, the
orchestration-boundary pattern sanctioned in ``tests/PATTERNS.md`` — so the
test writes under ``tmp_path`` instead of the repo's ``output/`` tree.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

_SCRIPT_PATH = Path(__file__).absolute().parent.parent / "scripts" / "generate_overview_figure.py"

# PNG magic number: the first eight bytes of every well-formed PNG file.
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _load_generator() -> ModuleType:
    """Import the figure generator directly from its file path.

    Loading by path (rather than ``import scripts.generate_overview_figure``)
    avoids colliding with the repo-level ``scripts`` package that also sits on
    ``sys.path`` during the pipeline.
    """
    spec = importlib.util.spec_from_file_location(
        "active_inference_overview_generator", _SCRIPT_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_main_writes_non_empty_png(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """main() renders a real, non-empty PNG under the redirected output root."""
    module = _load_generator()

    # Redirect the output tree into tmp_path; the render itself is untouched.
    monkeypatch.setattr(module, "PROJECT_ROOT", tmp_path)

    out_path = module.main()

    expected = tmp_path / "output" / "figures" / "active_inference_overview.png"
    assert out_path == expected
    assert out_path.is_file()
    assert out_path.stat().st_size > 0
    # Confirm it is a real PNG, not a zero-byte or truncated placeholder.
    assert out_path.read_bytes()[:8] == _PNG_SIGNATURE
