import json
import shutil
from pathlib import Path

import pytest

from src.experiment_suite import run_teaching_experiments


def test_real_source_bound_repeatable_suite(tmp_path):
    root = Path(__file__).resolve().parents[1]
    shutil.copytree(root / "src", tmp_path / "src")
    path = run_teaching_experiments(tmp_path)
    original = path.read_bytes()
    result = json.loads(original)
    assert result["conditions"]["informative_feedback"]["net_value"] == pytest.approx(0.25)
    control = result["conditions"]["informative_irrelevant_payoff"]
    assert control["information_nats"] > 0
    assert control["gross_value"] == pytest.approx(0)
    assert run_teaching_experiments(tmp_path).read_bytes() == original
    changed = tmp_path / "src/demos.py"
    changed.write_text(changed.read_text() + "\n")
    updated = json.loads(run_teaching_experiments(tmp_path).read_text())
    assert updated["source_sha256"]["src/demos.py"] != result["source_sha256"]["src/demos.py"]


def test_missing_source_refuses_report(tmp_path):
    with pytest.raises(FileNotFoundError):
        run_teaching_experiments(tmp_path)
    assert not (tmp_path / "output/data/teaching_experiments.json").exists()
