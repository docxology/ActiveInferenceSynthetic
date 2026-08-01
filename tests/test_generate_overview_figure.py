"""Smoke test for scripts/generate_overview_figure.py."""

from __future__ import annotations

from pathlib import Path

import pytest

import src.project_paths as project_paths
from scripts import generate_overview_figure

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def test_main_writes_non_empty_png(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(project_paths, "_DEFAULT_ROOT", tmp_path)
    out_path = generate_overview_figure.main()
    expected = tmp_path / "output" / "figures" / "active_inference_overview.png"
    assert out_path == expected
    assert out_path.read_bytes()[:8] == _PNG_SIGNATURE
