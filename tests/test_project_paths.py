"""Tests for src.project_paths — output-directory resolution helpers."""

from __future__ import annotations

import sys
import types
from pathlib import Path

from src.project_paths import project_output_dirs, resolve_project_root


def test_project_output_dirs_explicit_root(tmp_path: Path) -> None:
    dirs = project_output_dirs(tmp_path)
    assert dirs["output"] == tmp_path / "output"
    assert dirs["figures"] == tmp_path / "output" / "figures"
    assert dirs["data"] == tmp_path / "output" / "data"
    assert dirs["reports"] == tmp_path / "output" / "reports"
    assert dirs["web"] == tmp_path / "output" / "web"


def test_project_output_dirs_default_root() -> None:
    dirs = project_output_dirs()
    # Default root is the project directory (parent of src/).
    assert dirs["figures"].name == "figures"
    assert dirs["figures"].parent.name == "output"


def test_resolve_project_root_reads_module_attribute(tmp_path: Path) -> None:
    mod = types.ModuleType("fake_pkg_for_root")
    mod.project_root = str(tmp_path)  # type: ignore[attr-defined]
    sys.modules["fake_pkg_for_root"] = mod
    try:
        assert resolve_project_root("fake_pkg_for_root") == tmp_path
    finally:
        del sys.modules["fake_pkg_for_root"]


def test_resolve_project_root_falls_back_to_default() -> None:
    root = resolve_project_root("definitely_not_a_real_module_name")
    # Falls back to the package default (the project directory).
    assert (root / "src").is_dir()
