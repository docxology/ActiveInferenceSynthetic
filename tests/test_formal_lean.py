"""Source contracts and real native verification of selected fep_formal results."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_FORMAL = Path(__file__).resolve().parent.parent / "formal"
_SOURCES = sorted((_FORMAL / "ActiveInferenceFormal").glob("*.lean"))
_THEOREMS = [
    "finite_path_entropy_nonnegative",
    "finite_path_integral_fluctuation",
    "ℝ_solenoidal_orthogonal",
    "ℝ_flow_work_eq_dissipation",
    "ℝ_freeEnergy_non_increasing",
    "ℝ_detailed_balance_iff",
    "ℝ_entropyProduction_nonneg",
    "ℝ_entropyProduction_eq_zero_iff",
    "ℝ_finiteKL_nonneg",
    "ℝ_finiteKL_self",
    "ℝ_finiteKL_eq_zero_iff",
    "ℝ_entropy_nonneg",
    "ℝ_surprisal_le_VFE",
    "ℝ_VFE_at_posterior",
    "ℝ_negative_VFE_le_logEvidence",
    "ℝ_EFE_decomposition",
    "ℝ_EFE_minimizer_exists",
    "ℝ_epistemicValue_nonneg",
    "negative_dissipation_positive_work",
    "zero_drive_zero_work",
    "disjoint_support_totalized_KL",
    "ℝ_canonical_precision_entries",
    "ℝ_canonical_precision_posDef",
    "ℝ_canonical_gaussian_blanket",
    "ℝ_canonical_conditional_rows",
    "ℝ_coupled_gaussian_not_independent",
    "twoStep_history_predictive_mass",
    "twoStep_history_posterior_mass",
    "ℝ_twoStep_terminal_history_bridge",
    "fair_history_information_zero",
    "fair_terminal_history_value",
    "cumulative_terminal_counterexample",
    "revealing_history_information",
    "revealing_terminal_history_value",
]


def _assert_no_admissions(path: Path) -> None:
    text = re.sub(r"/-.*?-/", " ", path.read_text(), flags=re.DOTALL)
    text = re.sub(r"--[^\n]*", " ", text)
    assert not re.search(r"\b(sorry|admit|axiom)\b", text), path


def _assert_axiom_audit(output: str) -> None:
    assert "sorryAx" not in output, output
    for theorem in _THEOREMS:
        assert re.search(
            rf"ActiveInferenceFormal\.{theorem}' (?:depends on axioms:|does not depend on any axioms)",
            output,
        ), f"Missing axiom audit: {theorem}\n{output}"


def test_selected_formal_sources_and_audit() -> None:
    assert {p.name for p in _SOURCES} == {
        "Geometry.lean",
        "Thermodynamics.lean",
        "Information.lean",
        "Bridge.lean",
        "Witnesses.lean",
        "GaussianBlanket.lean",
        "Planning.lean",
        "Audit.lean",
    }
    corpus = "\n".join(p.read_text() for p in _SOURCES)
    for theorem in _THEOREMS:
        assert f"theorem {theorem}" in corpus
        assert f"#print axioms {theorem}" in corpus
    for path in _SOURCES:
        _assert_no_admissions(path)


def test_admission_check_rejects_real_bad_source(tmp_path: Path) -> None:
    source = tmp_path / "Bad.lean"
    source.write_text("theorem broken : False := by sorry\n")
    with pytest.raises(AssertionError):
        _assert_no_admissions(source)


def test_axiom_audit_rejects_unproved_or_incomplete_output() -> None:
    with pytest.raises(AssertionError):
        _assert_axiom_audit(
            "'ActiveInferenceFormal.ℝ_finiteKL_nonneg' depends on axioms: [sorryAx]"
        )
    with pytest.raises(AssertionError):
        _assert_axiom_audit("Build completed successfully")


def test_upstream_dependency_is_immutable_and_toolchain_aligned() -> None:
    manifest = json.loads((_FORMAL / "lake-manifest.json").read_text())
    dependency = next(p for p in manifest["packages"] if p["name"] == "FepSketches")
    assert dependency["type"] == "git"
    assert (
        dependency["url"]
        == "https://github.com/ActiveInferenceInstitute/fep_formal.git"
    )
    assert re.fullmatch(r"[0-9a-f]{40}", dependency["rev"])
    assert dependency["inputRev"] == dependency["rev"]
    assert dependency["subDir"] == "lean"
    assert dependency["rev"] in (_FORMAL / "lakefile.lean").read_text()
    checkout = _FORMAL / ".lake/packages/FepSketches/lean"
    if checkout.exists():
        assert (_FORMAL / "lean-toolchain").read_text() == (
            checkout / "lean-toolchain"
        ).read_text()


@pytest.mark.skipif(shutil.which("lake") is None, reason="Lean/lake not installed")
def test_lake_build_and_axiom_audit() -> None:
    build = subprocess.run(
        ["lake", "build"],
        cwd=_FORMAL,
        capture_output=True,
        text=True,
        timeout=1800,
        check=False,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    audit = subprocess.run(
        ["lake", "env", "lean", "ActiveInferenceFormal/Audit.lean"],
        cwd=_FORMAL,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert audit.returncode == 0, audit.stdout + audit.stderr
    _assert_axiom_audit(audit.stdout + audit.stderr)


@pytest.mark.skipif(shutil.which("lake") is None, reason="Lean/lake not installed")
@pytest.mark.parametrize(
    "claim",
    [
        "import FepSketches.ness_flow\nexample : (1 : ℝ) ≤ 0 := by norm_num\n",
        "import ActiveInferenceFormal.GaussianBlanket\n"
        "open FEP.Fin4GaussianSemigroup FEP.Fin4GaussianSemigroup.Axis\n"
        "example : K external internal ≠ 0 := by norm_num [K]\n",
        "import ActiveInferenceFormal.Planning\n"
        "open ActiveInferenceFormal FEP.ActiveInference\n"
        "example : terminalHistoryEFE fairBoolLaw fairHistoryChannel fairBoolLaw = 0 := by\n"
        "  rw [fair_terminal_history_value]\n"
        "  norm_num [Real.log_eq_zero]\n",
    ],
    ids=["false-real-inequality", "false-precision-coupling", "missing-terminal-cost"],
)
def test_native_lean_rejects_false_claim(tmp_path: Path, claim: str) -> None:
    source = tmp_path / "FalseClaim.lean"
    source.write_text(claim)
    result = subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=_FORMAL,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode != 0
    output = result.stdout + result.stderr
    assert "error:" in output and "unsolved goals" in output, output
    assert "unknown module" not in output, output
