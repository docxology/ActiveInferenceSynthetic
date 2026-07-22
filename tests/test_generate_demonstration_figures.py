"""Smoke tests for the two demonstration-figure generators.

Each new manuscript section is anchored on a figure ([@fig:belief],
[@fig:trajectories]); these tests confirm each generator actually writes a
real, non-empty PNG.

No mocks: ``main()`` runs the real matplotlib render over the real tested cores
(``src.generative_model``, ``src.trajectories``). Only the output *location* is
redirected — via ``pytest``'s ``MonkeyPatch`` on each module's ``PROJECT_ROOT``
attribute, the orchestration-boundary pattern sanctioned in ``tests/PATTERNS.md``
— so the tests write under ``tmp_path`` instead of the repo's ``output/`` tree.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

_SCRIPTS = Path(__file__).absolute().parent.parent / "scripts"

# PNG magic number: the first eight bytes of every well-formed PNG file.
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _load(script_name: str, module_name: str) -> ModuleType:
    """Import a figure generator directly from its file path."""
    spec = importlib.util.spec_from_file_location(module_name, _SCRIPTS / script_name)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("script", "module_name", "figure_name"),
    [
        (
            "generate_belief_update_figure.py",
            "belief_update_generator",
            "belief_update.png",
        ),
        (
            "generate_trajectory_figure.py",
            "trajectory_generator",
            "worked_trajectories.png",
        ),
        (
            "generate_efe_figure.py",
            "efe_generator",
            "expected_free_energy.png",
        ),
        (
            "generate_markov_blanket_figure.py",
            "markov_blanket_generator",
            "markov_blanket.png",
        ),
        (
            "generate_steady_state_figure.py",
            "steady_state_generator",
            "steady_state_current.png",
        ),
    ],
)
def test_generator_writes_non_empty_png(
    script: str,
    module_name: str,
    figure_name: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load(script, module_name)
    monkeypatch.setattr(module, "PROJECT_ROOT", tmp_path)

    out_path = module.main()

    expected = tmp_path / "output" / "figures" / figure_name
    assert out_path == expected
    assert out_path.is_file()
    assert out_path.stat().st_size > 0
    assert out_path.read_bytes()[:8] == _PNG_SIGNATURE
