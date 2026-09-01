"""Verify the Lean 4 formalization in `formal/`.

No mocks: this greps the real Lean sources and, when a Lean toolchain is
available, runs the real `lake build` and inspects the real axiom-audit output.

The formalization now has TWO surfaces:
1. R-valued (manuscript-canonical): Geometry.lean, Information.lean
   import from `FepSketches` (the companion fep_lean library, which uses mathlib).
2. Z-valued (legacy, no mathlib): GeometryZ.lean, InformationZ.lean,
   Sanity.lean prove the same statements from Lean core alone.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest


def _strip_lean_comments(text: str) -> str:
    """Remove Lean block ``/- ... -/`` and line ``--`` comments."""
    text = re.sub(r"/-.*?-/\s*", " ", text, flags=re.DOTALL)
    text = re.sub(r"--[^\n]*", " ", text)
    return text


_FORMAL = Path(__file__).absolute().parent.parent / "formal"
_LEAN_SOURCES = sorted((_FORMAL / "ActiveInferenceFormal").glob("*.lean"))

# Z-valued sources (must build from Lean core, no mathlib)
_Z_SOURCES = [s for s in _LEAN_SOURCES if s.stem.endswith("Z") or s.stem == "Sanity"]
# R-valued sources (import fep_lean/mathlib)
_R_EXCLUDE = {"Sanity", "Audit", "Bridge"}
_R_SOURCES = [
    s for s in _LEAN_SOURCES if not s.stem.endswith("Z") and s.stem not in _R_EXCLUDE
]

_HEADLINE_THEOREMS_R = [
    "solenoidal_orthogonal",
    "flow_work_eq_dissipation",
    "detailed_balance_iff",
    "entropyProduction_nonneg",
    "entropyProduction_eq_zero_iff",
]
_HEADLINE_THEOREMS_Z = [
    "solenoidal_orthogonal",
    "flow_work_eq_dissipation",
    "detailed_balance_iff",
    "entropyProduction_nonneg",
    "entropyProduction_zero_iff",
    "relEntropy_nonneg",
    "freeEnergy_eq_surprise_add_relEntropy",
    "freeEnergy_ge_surprise",
    "freeEnergy_ge_surprise_of_model",
    "freeEnergy_eq_surprise_at_posterior",
]

_WITNESS_THEOREMS = [
    "relEntropy_can_be_negative",
    "okL_gibbs_holds",
    "okL_bound_holds",
    "okL_bound_is_strict",
]


def test_formal_sources_exist() -> None:
    assert _LEAN_SOURCES, "no Lean sources under formal/ActiveInferenceFormal/"
    names = {p.name for p in _LEAN_SOURCES}
    expected = {
        "Geometry.lean",
        "Information.lean",
        "Bridge.lean",
        "GeometryZ.lean",
        "InformationZ.lean",
        "Sanity.lean",
        "Audit.lean",
    }
    assert expected <= names, f"missing: {expected - names}"


def test_no_sorry_or_admit_in_lean_sources() -> None:
    for src in _LEAN_SOURCES:
        code = _strip_lean_comments(src.read_text())
        assert "sorry" not in code, f"{src.name} contains `sorry`"
        assert not re.search(r"\badmit\b", code), f"{src.name} contains `admit`"


def test_every_headline_theorem_is_stated() -> None:
    corpus = "\n".join(p.read_text() for p in _LEAN_SOURCES)
    for name in _HEADLINE_THEOREMS_R:
        prefix = "theorem " + chr(8477) + "_"
        assert prefix + name in corpus, f"missing R theorem {name}"
    for name in _HEADLINE_THEOREMS_Z:
        assert f"theorem {name}" in corpus, f"missing Z theorem {name}"


def test_non_vacuity_witnesses_present() -> None:
    corpus = "\n".join(p.read_text() for p in _LEAN_SOURCES)
    for name in _WITNESS_THEOREMS:
        assert f"theorem {name}" in corpus, f"missing witness {name}"


def test_Z_surface_no_mathlib() -> None:
    """Z surface must build from Lean core alone: no `import Mathlib`."""
    for src in _Z_SOURCES:
        assert "import Mathlib" not in src.read_text(), (
            f"{src.name} imports Mathlib (violates Z contract)"
        )


def test_R_surface_imports_fep_lean() -> None:
    """R surface imports FepSketches (which uses Mathlib); that's expected."""
    for src in _R_SOURCES:
        text = src.read_text()
        ok = "import FepSketches" in text or "import ActiveInferenceFormal" in text
        assert ok, f"{src.name} neither imports FepSketches nor its own surface"


@pytest.mark.skipif(shutil.which("lake") is None, reason="Lean/lake not installed")
def test_lake_manifest_present() -> None:
    manifest = _FORMAL / "lake-manifest.json"
    if not manifest.is_file():
        pytest.skip("lake-manifest.json not found; run `lake update` first")


@pytest.mark.skipif(shutil.which("lake") is None, reason="Lean/lake not installed")
def test_lake_build_succeeds() -> None:
    manifest = _FORMAL / "lake-manifest.json"
    if not manifest.is_file():
        pytest.skip("no manifest")
    # Under fleet load a cold mathlib build can take far longer than a warm
    # incremental build; 1800 s keeps this opt-in test from flaking on load
    # while still bounding the subprocess.
    result = subprocess.run(
        ["lake", "build"],
        cwd=_FORMAL,
        capture_output=True,
        text=True,
        timeout=1800,
        check=False,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, f"lake build failed:\n{output}"
