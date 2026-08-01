"""Verify the Lean 4 formalization in `formal/`.

No mocks: this greps the real Lean sources and, when a Lean toolchain is
available, runs the real `lake build` and inspects the real axiom-audit output.
The formalization is the *proof-level* analogue of the manuscript's no-mocks
policy — the mathematical claims the Python demonstrates numerically are here
machine-checked from Lean's core axioms alone (no mathlib, no `sorry`).
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest


def _strip_lean_comments(text: str) -> str:
    """Remove Lean block ``/- … -/`` and line ``--`` comments.

    A comment may legitimately *mention* ``sorry``/``admit`` (e.g. the axiom-audit
    docstring); only their appearance in actual code is a defect.
    """
    text = re.sub(r"/-.*?-/", " ", text, flags=re.DOTALL)
    text = re.sub(r"--[^\n]*", " ", text)
    return text


_FORMAL = Path(__file__).absolute().parent.parent / "formal"
_LEAN_SOURCES = sorted((_FORMAL / "ActiveInferenceFormal").glob("*.lean"))

# Theorems the manuscript relies on; the audit must report axioms for each.
_HEADLINE_THEOREMS = [
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

# Non-vacuity controls: the free-energy hypotheses must be shown both necessary
# (a negative witness) and satisfiable (a positive witness), else the bound is
# vacuously true.
_WITNESS_THEOREMS = [
    "relEntropy_can_be_negative",  # negative control: hypothesis is load-bearing
    "okL_gibbs_holds",  # positive control: hypotheses are satisfiable
    "okL_bound_holds",  # positive control: the bound fires non-vacuously
    "okL_bound_is_strict",  # the fired bound is a real gap, not x ≤ x
]


def test_formal_sources_exist() -> None:
    assert _LEAN_SOURCES, "no Lean sources found under formal/ActiveInferenceFormal/"
    names = {p.name for p in _LEAN_SOURCES}
    assert {"Geometry.lean", "Information.lean", "Audit.lean"} <= names


def test_no_sorry_or_admit_in_lean_sources() -> None:
    # An unproved proof would use `sorry`/`admit`; the formalization forbids both
    # in actual code (comments discussing them are fine).
    for src in _LEAN_SOURCES:
        code = _strip_lean_comments(src.read_text())
        assert "sorry" not in code, f"{src.name} contains `sorry` in code"
        assert not re.search(r"\badmit\b", code), f"{src.name} contains `admit` in code"


def test_every_headline_theorem_is_stated() -> None:
    corpus = "\n".join(p.read_text() for p in _LEAN_SOURCES)
    for name in _HEADLINE_THEOREMS:
        assert f"theorem {name}" in corpus, f"missing theorem {name}"


def test_non_vacuity_witnesses_present() -> None:
    # The formalization must prove its free-energy hypotheses both necessary and
    # satisfiable, so the bound is not vacuously true.
    corpus = "\n".join(p.read_text() for p in _LEAN_SOURCES)
    for name in _WITNESS_THEOREMS:
        assert f"theorem {name}" in corpus, f"missing non-vacuity witness {name}"


def test_no_mathlib_dependency() -> None:
    # The project must build from Lean core alone: no `import Mathlib`, and the
    # lakefile must declare no external require.
    for src in _LEAN_SOURCES:
        assert "import Mathlib" not in src.read_text()
    lakefile = (_FORMAL / "lakefile.lean").read_text()
    assert "require" not in lakefile


@pytest.mark.skipif(shutil.which("lake") is None, reason="Lean/lake not installed")
def test_lake_build_succeeds_with_clean_axioms() -> None:
    """`lake build` succeeds and every headline theorem's axiom set is clean."""
    result = subprocess.run(
        ["lake", "build"],
        cwd=_FORMAL,
        capture_output=True,
        text=True,
        timeout=600,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, f"lake build failed:\n{output}"

    # The Audit module prints `#print axioms` for each headline theorem. Every
    # line must report only Lean's trusted axioms — never `sorryAx`, never a
    # mathlib axiom.
    audit_lines = [ln for ln in output.splitlines() if "depends on axioms" in ln]
    assert len(audit_lines) >= len(_HEADLINE_THEOREMS), (
        f"expected an axiom report per theorem, got {len(audit_lines)}:\n{output}"
    )
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    for line in audit_lines:
        assert "sorryAx" not in line, f"a theorem rests on `sorry`:\n{line}"
        inside = line.split("[", 1)[1].rstrip("]") if "[" in line else ""
        axioms = {a.strip() for a in inside.split(",") if a.strip()}
        assert axioms <= allowed, f"unexpected axiom(s) {axioms - allowed} in:\n{line}"
