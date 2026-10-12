"""Reproduce finite decision experiments and bind outputs to their source files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from .demos import (
    VOI_CHANNEL, VOI_PRIOR, VOI_UTILITIES, VOI_IRRELEVANT_UTILITIES, VOI_COST,
)
from .value_of_information import value_of_information


def run_teaching_experiments(project_root: Path) -> Path:
    """Write exact condition results, inputs and hashes; never certify publication."""
    conditions = {
        "informative_feedback": (VOI_CHANNEL, VOI_UTILITIES, VOI_COST),
        "uninformative_feedback": (np.full_like(VOI_CHANNEL, 0.5), VOI_UTILITIES, 0.),
        "informative_irrelevant_payoff": (VOI_CHANNEL, VOI_IRRELEVANT_UTILITIES, 0.),
    }
    rows = {}
    for name, (channel, utilities, cost) in conditions.items():
        result = value_of_information(channel, VOI_PRIOR, utilities, cost=cost)
        rows[name] = {
            "channel": channel.tolist(), "prior": VOI_PRIOR.tolist(),
            "utilities": utilities.tolist(), "cost": cost,
            "baseline_utility": result.baseline_utility,
            "informed_utility": result.informed_utility,
            "gross_value": result.gross_value, "net_value": result.net_value,
            "information_nats": result.information_nats,
            "feedback_actions": result.feedback_actions,
        }
    sources = [
        "src/value_of_information.py", "src/expected_free_energy.py", "src/_prob.py",
        "src/demos.py", "src/experiment_suite.py",
    ]
    bindings = {
        name: hashlib.sha256((project_root / name).read_bytes()).hexdigest()
        for name in sources
    }
    target = project_root / "output/data/teaching_experiments.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({
        "schema_version": "synthetic-teaching-experiments-v1",
        "method": "exact finite enumeration; no RNG or fitting",
        "units": {"value": "declared utility", "information": "nats"},
        "conditions": rows, "source_sha256": bindings,
    }, indent=2, sort_keys=True, allow_nan=False) + "\n")
    return target
