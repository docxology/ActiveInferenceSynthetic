"""Render all manuscript figures."""

from __future__ import annotations

from pathlib import Path
import json

import yaml

from . import (
    belief,
    synthetic_agent,
    hierarchy,
    blanket,
    efe,
    overview,
    policy_planning,
    steady_state,
    trajectories_figure,
    decision_value,
    graphical_abstract,
)

FIGURE_RENDERERS = {
    "graphical_abstract.png": graphical_abstract.render,
    "active_inference_overview.png": overview.render,
    "belief_update.png": belief.render,
    "worked_trajectories.png": trajectories_figure.render,
    "expected_free_energy.png": efe.render,
    "policy_planning.png": policy_planning.render,
    "markov_blanket.png": blanket.render,
    "steady_state_current.png": steady_state.render,
    "synthetic_agent.png": synthetic_agent.render,
    "hierarchical_inference.png": hierarchy.render,
    "value_of_information.png": decision_value.render,
}


def render_all(project_root: Path | None = None) -> dict[str, Path]:
    """Build every figure once and return a filename → path manifest."""
    return {name: render(project_root) for name, render in FIGURE_RENDERERS.items()}


def export_registry(project_root: Path) -> Path:
    """Bind authored figure metadata to the complete generated PNG collection."""
    source = project_root / "docs" / "manuscript" / "figure_registry.yaml"
    payload = yaml.safe_load(source.read_text())
    if not isinstance(payload, dict) or not isinstance(payload.get("figures"), list):
        raise ValueError("Figure registry must contain a figures list")
    entries = payload["figures"]
    labels: set[str] = set()
    names: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Figure registry entries must be mappings")
        label = entry.get("id")
        filename = entry.get("file")
        if (
            not isinstance(label, str)
            or not label.startswith("fig:")
            or label in labels
        ):
            raise ValueError("Figure labels must be unique fig: identifiers")
        if (
            not isinstance(filename, str)
            or filename != f"output/figures/{Path(filename).name}"
        ):
            raise ValueError("Figure files must be direct output/figures paths")
        if filename in names:
            raise ValueError("Figure files must be unique")
        if not isinstance(entry.get("alt_text"), str) or not entry["alt_text"].strip():
            raise ValueError("Figure alt text must be nonempty")
        if (project_root / filename).read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Invalid PNG: {filename}")
        labels.add(label)
        names.add(filename)
    if names != {f"output/figures/{name}" for name in FIGURE_RENDERERS}:
        raise ValueError("Figure registry must match every figure renderer")
    target = project_root / "output" / "figures" / "figure_registry.json"
    target.write_text(
        json.dumps(
            {
                "figures": [
                    dict(entry, label=entry["id"], filename=Path(entry["file"]).name)
                    for entry in entries
                ]
            },
            indent=2,
        )
        + "\n"
    )
    return target
