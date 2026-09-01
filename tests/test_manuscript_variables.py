"""Live {{TOKEN}} map: every authored claim is generated, none leftover."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from src.demos import TRAJECTORY_DT
from src.manuscript_variables import (
    compute_claims,
    generate_variables,
    hydrate_manuscript,
    leftover_tokens,
    manuscript_tokens,
    save_variables,
)

_ROOT = Path(__file__).resolve().parent.parent
_MANUSCRIPT = _ROOT / "docs" / "manuscript"
_Z_SCRIPT = _ROOT / "scripts" / "z_generate_manuscript_variables.py"

# Drift-prone demonstration literals that must live in tokens, not prose.
_FORBIDDEN = re.compile(
    r"(?<![\d.])(?:"
    r"0\.19|0\.37|0\.33|0\.69|0\.43|0\.84|0\.87|"
    r"0\.54|0\.62|0\.38|4\.58|11\.52|11\.5|"
    r"2\.4|0\.6|0\.4"
    r")(?![\d.])"
)


def test_generate_variables_keys_are_uppercase() -> None:
    variables = generate_variables(_ROOT)
    assert variables
    assert all(key == key.upper() and key.isidentifier() for key in variables)
    assert all(isinstance(value, str) and value != "" for value in variables.values())


def test_all_manuscript_tokens_are_generated() -> None:
    variables = generate_variables(_ROOT)
    used = manuscript_tokens(_MANUSCRIPT)
    missing = used - set(variables)
    assert not missing, (
        f"manuscript tokens missing from generate_variables: {sorted(missing)}"
    )


def test_authored_sections_do_not_hardcode_demo_values() -> None:
    offenders: list[str] = []
    for path in sorted(_MANUSCRIPT.glob("0*.md")):
        if _FORBIDDEN.search(path.read_text()):
            offenders.append(path.name)
    assert not offenders, f"hard-coded demo numbers in {offenders}; use {{{{TOKEN}}}}"


def test_hydrate_resolves_every_token(tmp_path: Path) -> None:
    src = tmp_path / "docs" / "manuscript"
    src.mkdir(parents=True)
    for path in _MANUSCRIPT.iterdir():
        if path.is_file():
            (src / path.name).write_text(path.read_text())
    variables = generate_variables(_ROOT)
    written = hydrate_manuscript(tmp_path, variables)
    leftovers: list[str] = []
    for name, dest in written.items():
        if name.endswith(".md") and name[0].isdigit():
            leftovers.extend(
                f"{name}:{tok}" for tok in leftover_tokens(dest.read_text())
            )
    assert leftovers == []


def test_hydrated_values_match_live_rounding() -> None:
    variables = generate_variables(_ROOT)
    claims = compute_claims()
    assert variables["TRAJECTORY_HORIZON"] == f"{claims['trajectory_horizon']:g}"
    assert variables["TRAJECTORY_TURNS"] == f"{claims['trajectory_turns']:.2f}"
    assert variables["TRAJECTORY_RATE"] == f"{claims['trajectory_rate']:.2f}"
    assert variables["NESS_SIGMA"] == f"{claims['ness_sigma']:.2f}"
    assert variables["BLANKET_CORR"] == f"{claims['blanket_corr']:.2f}"
    assert variables["POSTERIOR_X0"] == f"{claims['posterior_x0']:.2f}"
    assert variables["NESS_OMEGA"] == f"{claims['ness_omega']:.1f}"
    assert variables["PAPER_VERSION"]


def test_claim_ledger_matches_live_claims() -> None:
    claims = compute_claims()
    ledger = yaml.safe_load((_ROOT / "data" / "claim_ledger.yaml").read_text())
    by_id = {row["claim_id"]: row["value"] for row in ledger["claims"]}
    assert by_id["belief-model-prior"][0] == pytest.approx(claims["prior_x0"])
    assert by_id["belief-model-prior"][1] == pytest.approx(claims["prior_x1"])
    assert by_id["belief-posterior-x0"] == pytest.approx(claims["posterior_x0"])
    assert by_id["solenoidal-strength-omega-ness"] == pytest.approx(
        claims["ness_omega"]
    )
    assert by_id["trajectory-integrator-dt"] == pytest.approx(float(TRAJECTORY_DT))
    assert by_id["trajectory-ness-net-rotation-turns"] == pytest.approx(
        claims["trajectory_turns"], rel=1e-8
    )
    assert by_id["trajectory-ness-rotation-rate"] == pytest.approx(
        claims["trajectory_rate"], rel=1e-8
    )
    assert by_id["efe-cue-epistemic-value"] == pytest.approx(
        claims["efe_cue_epistemic"], rel=1e-8
    )
    assert by_id["planning-horizon-two"] == pytest.approx(claims["planning_horizon"])
    assert by_id["planning-look-then-leap-efe"] == pytest.approx(
        claims["planning_efe_look_then_leap"], abs=0.005
    )
    assert by_id["planning-exploit-first-efe"] == pytest.approx(
        claims["planning_efe_exploit_first"], abs=0.005
    )
    assert by_id["planning-look-then-leap-epistemic"] == pytest.approx(
        claims["planning_epistemic_look_then_leap"], abs=0.005
    )
    assert by_id["steady-state-entropy-production-ness"] == pytest.approx(
        claims["ness_sigma"]
    )
    assert by_id["blanket-eta-mu-marginal-correlation"] == pytest.approx(
        claims["blanket_corr"], abs=0.01
    )


def test_save_variables_roundtrip(tmp_path: Path) -> None:
    variables = generate_variables(_ROOT)
    path = save_variables(variables, tmp_path / "manuscript_variables.json")
    loaded = json.loads(path.read_text())
    assert loaded == variables


def test_z_generate_script_writes_json_and_hydrates() -> None:
    result = subprocess.run(
        [sys.executable, str(_Z_SCRIPT)],
        cwd=_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    json_path = _ROOT / "output" / "data" / "manuscript_variables.json"
    assert json_path.is_file()
    variables = json.loads(json_path.read_text())
    hydrated = _ROOT / "output" / "manuscript" / "03_worked_regimes.md"
    assert hydrated.is_file()
    text = hydrated.read_text()
    assert leftover_tokens(text) == []
    assert variables["TRAJECTORY_TURNS"] in text
    assert "-11.5" not in text


def test_intish_formats_non_integers() -> None:
    from src.manuscript_variables import _intish

    assert _intish(1.0) == "1"
    assert _intish(2.4) == "2.40"


def test_hydrate_skips_nested_directories(tmp_path: Path) -> None:
    src = tmp_path / "docs" / "manuscript"
    src.mkdir(parents=True)
    (src / "nested").mkdir()
    (src / "02_generative_model.md").write_text("p={{PRIOR_X0}}")
    written = hydrate_manuscript(tmp_path, generate_variables(_ROOT))
    assert "nested" not in written
    assert leftover_tokens(written["02_generative_model.md"].read_text()) == []
