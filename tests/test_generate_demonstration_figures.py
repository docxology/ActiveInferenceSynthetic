"""Smoke tests for individual figure-generator scripts."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts import (
    generate_belief_update_figure,
    generate_synthetic_agent_figure,
    generate_hierarchy_figure,
    generate_efe_figure,
    generate_markov_blanket_figure,
    generate_policy_planning_figure,
    generate_steady_state_figure,
    generate_trajectory_figure,
)
from src import project_paths

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@pytest.mark.parametrize(
    ("module", "figure_name"),
    [
        (generate_belief_update_figure, "belief_update.png"),
        (generate_trajectory_figure, "worked_trajectories.png"),
        (generate_efe_figure, "expected_free_energy.png"),
        (generate_markov_blanket_figure, "markov_blanket.png"),
        (generate_policy_planning_figure, "policy_planning.png"),
        (generate_steady_state_figure, "steady_state_current.png"),
        (generate_synthetic_agent_figure, "synthetic_agent.png"),
        (generate_hierarchy_figure, "hierarchical_inference.png"),
    ],
)
def test_generator_writes_non_empty_png(
    module,
    figure_name: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(project_paths, "_DEFAULT_ROOT", tmp_path)
    out_path = module.main()
    expected = tmp_path / "output" / "figures" / figure_name
    assert out_path == expected
    assert out_path.read_bytes()[:8] == _PNG_SIGNATURE
