"""Smoke tests for figure generators."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.figures import render_all
from src.figures import (
    belief,
    blanket,
    efe,
    overview,
    steady_state,
    trajectories_figure,
)
import src.project_paths as project_paths

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@pytest.fixture
def tmp_project_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(project_paths, "_DEFAULT_ROOT", tmp_path)
    return tmp_path


def test_render_all_writes_manifest(tmp_project_root: Path) -> None:
    manifest = render_all(tmp_project_root)
    assert len(manifest) == 6
    for path in manifest.values():
        assert path.is_file()
        assert path.stat().st_size > 0
        assert path.read_bytes()[:8] == _PNG_SIGNATURE


@pytest.mark.parametrize(
    ("render_fn", "filename"),
    [
        (overview.render, "active_inference_overview.png"),
        (belief.render, "belief_update.png"),
        (trajectories_figure.render, "worked_trajectories.png"),
        (efe.render, "expected_free_energy.png"),
        (blanket.render, "markov_blanket.png"),
        (steady_state.render, "steady_state_current.png"),
    ],
)
def test_individual_figure_render(
    render_fn,
    filename: str,
    tmp_project_root: Path,
) -> None:
    out_path = render_fn(tmp_project_root)
    expected = tmp_project_root / "output" / "figures" / filename
    assert out_path == expected
    assert out_path.read_bytes()[:8] == _PNG_SIGNATURE
