"""Live manuscript tokens computed from the demonstration cores.

Every numeric claim in ``manuscript/*.md`` is a ``{{TOKEN}}``. Values come from
``src.demos`` and the same functions the figures and tests call — never from
hand-copied literals. The thin orchestrator
``scripts/z_generate_manuscript_variables.py`` writes
``output/data/manuscript_variables.json`` and hydrates ``output/manuscript/``.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

from .demos import (
    ACTIONS,
    BELIEF,
    BELIEF_OBS,
    BLANKET_ETA_IDX,
    BLANKET_MU_IDX,
    BLANKET_PRECISION,
    FLOW,
    FLAT_PREFERENCES,
    LIKELIHOOD,
    OMEGA_NESS,
    PLANNING_HORIZON,
    PLANNING_PREFERENCES,
    PRIOR,
    SHARP_PREFERENCES,
    TRAJECTORY_DT,
    TRAJECTORY_OMEGA_NESS,
    TRAJECTORY_START,
    TRAJECTORY_STEPS,
)
from .expected_free_energy import epistemic_value, expected_free_energy
from .policy_planning import select_multistep_policy
from .generative_model import evidence, joint, posterior
from .markov_blanket import correlation_matrix, covariance_from_precision
from .project_paths import project_output_dirs
from .steady_state import entropy_production_rate
from .trajectories import integrate_trajectory, net_rotation

_DOC_ONLY = frozenset({"AGENTS.md", "README.md", "SYNTAX.md"})
_TOKEN_RE = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")


def _approx(value: float, digits: int = 2) -> str:
    """Fixed-point display used in prose (matches the manuscript's rounding)."""
    return f"{value:.{digits}f}"


def _intish(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return _approx(value)


def compute_claims() -> dict[str, float]:
    """Numeric claims derived from the live demonstration, as floats."""
    j0 = joint(LIKELIHOOD, PRIOR, BELIEF_OBS)
    ev0 = evidence(LIKELIHOOD, PRIOR, BELIEF_OBS)
    post = posterior(LIKELIHOOD, PRIOR, BELIEF_OBS)
    horizon = float(TRAJECTORY_DT * TRAJECTORY_STEPS)
    path = integrate_trajectory(
        TRAJECTORY_START,
        precision=FLOW.precision,
        gamma=FLOW.gamma,
        omega=TRAJECTORY_OMEGA_NESS,
        dt=TRAJECTORY_DT,
        steps=TRAJECTORY_STEPS,
    )
    turns = net_rotation(path) / (2.0 * math.pi)
    rate = turns / horizon
    cov = covariance_from_precision(BLANKET_PRECISION)
    corr = float(correlation_matrix(cov)[BLANKET_ETA_IDX, BLANKET_MU_IDX])
    cue, bet = ACTIONS
    plan = select_multistep_policy(
        ACTIONS, BELIEF, PLANNING_PREFERENCES, PLANNING_HORIZON
    )
    look_then_leap = plan.policies.index((0, 1))
    exploit_first = plan.policies.index((1, 1))
    return {
        "prior_x0": float(PRIOR[0]),
        "prior_x1": float(PRIOR[1]),
        "joint_s0_x0": float(j0[0]),
        "joint_s0_x1": float(j0[1]),
        "evidence_s0": float(ev0),
        "posterior_x0": float(post[0]),
        "precision": float(FLOW.precision),
        "gamma": float(FLOW.gamma),
        "ness_omega": float(OMEGA_NESS),
        "trajectory_omega": float(TRAJECTORY_OMEGA_NESS),
        "trajectory_horizon": horizon,
        "trajectory_turns": float(turns),
        "trajectory_rate": float(rate),
        "belief_s0": float(BELIEF[0]),
        "belief_s1": float(BELIEF[1]),
        "efe_cue_epistemic": float(epistemic_value(cue, BELIEF)),
        "efe_flat_cue": float(expected_free_energy(cue, BELIEF, FLAT_PREFERENCES)),
        "efe_flat_bet": float(expected_free_energy(bet, BELIEF, FLAT_PREFERENCES)),
        "efe_sharp_cue": float(expected_free_energy(cue, BELIEF, SHARP_PREFERENCES)),
        "efe_sharp_bet": float(expected_free_energy(bet, BELIEF, SHARP_PREFERENCES)),
        "planning_horizon": float(PLANNING_HORIZON),
        "planning_efe_look_then_leap": float(plan.efe[look_then_leap]),
        "planning_efe_exploit_first": float(plan.efe[exploit_first]),
        "planning_epistemic_look_then_leap": float(plan.epistemic[look_then_leap]),
        "planning_pragmatic_look_then_leap": float(plan.pragmatic[look_then_leap]),
        "blanket_corr": corr,
        "ness_sigma": float(
            entropy_production_rate(
                precision=FLOW.precision, gamma=FLOW.gamma, omega=OMEGA_NESS
            )
        ),
        "figure_dpi": 300.0,
        "rk4_match_atol": 1e-6,
        "partial_corr_atol": 1e-10,
    }


def generate_variables(project_root: Path | None = None) -> dict[str, str]:
    """Return the ``{{TOKEN}}`` substitution map (uppercase keys, string values)."""
    claims = compute_claims()
    root = project_root or Path(__file__).resolve().parent.parent
    config_path = root / "manuscript" / "config.yaml"
    paper_text = config_path.read_text() if config_path.is_file() else ""

    def _quoted(key: str) -> str:
        match = re.search(rf'(?m)^\s*{key}:\s*"([^"]*)"', paper_text)
        return match.group(1) if match else ""

    j0 = claims["joint_s0_x0"]
    ev0 = claims["evidence_s0"]
    variables = {
        "PRIOR_X0": _approx(claims["prior_x0"]),
        "PRIOR_X1": _approx(claims["prior_x1"]),
        "JOINT_S0_X0": _approx(j0),
        "JOINT_S0_X1": _approx(claims["joint_s0_x1"]),
        "EVIDENCE_S0": _approx(ev0),
        "POSTERIOR_X0_FRAC": f"{_approx(j0)}/{_approx(ev0)}",
        "POSTERIOR_X0": _approx(claims["posterior_x0"]),
        "PRECISION": _intish(claims["precision"]),
        "GAMMA": _intish(claims["gamma"]),
        "NESS_OMEGA": _approx(claims["ness_omega"], 1),
        "TRAJECTORY_HORIZON": f"{claims['trajectory_horizon']:g}",
        "TRAJECTORY_TURNS": _approx(claims["trajectory_turns"]),
        "TRAJECTORY_RATE": _approx(claims["trajectory_rate"]),
        "BELIEF_S0": _approx(claims["belief_s0"]),
        "BELIEF_S1": _approx(claims["belief_s1"]),
        "EFE_CUE_EPISTEMIC": _approx(claims["efe_cue_epistemic"]),
        "EFE_FLAT_CUE": _approx(claims["efe_flat_cue"]),
        "EFE_FLAT_BET": _approx(claims["efe_flat_bet"]),
        "EFE_SHARP_CUE": _approx(claims["efe_sharp_cue"]),
        "EFE_SHARP_BET": _approx(claims["efe_sharp_bet"]),
        "PLANNING_HORIZON": str(int(claims["planning_horizon"])),
        "PLANNING_EFE_LOOK_THEN_LEAP": _approx(claims["planning_efe_look_then_leap"]),
        "PLANNING_EFE_EXPLOIT_FIRST": _approx(claims["planning_efe_exploit_first"]),
        "PLANNING_EPISTEMIC_LOOK_THEN_LEAP": _approx(
            claims["planning_epistemic_look_then_leap"]
        ),
        "PLANNING_PRAGMATIC_LOOK_THEN_LEAP": _approx(
            claims["planning_pragmatic_look_then_leap"]
        ),
        "BLANKET_CORR": _approx(claims["blanket_corr"]),
        "NESS_SIGMA": _approx(claims["ness_sigma"]),
        "NESS_SIGMA_APPROX": _approx(claims["ness_sigma"], 1),
        "FIGURE_DPI": f"{int(claims['figure_dpi'])}",
        "RK4_MATCH_ATOL": "10^{-6}",
        "PARTIAL_CORR_ATOL": "10^{-10}",
        "PAPER_VERSION": _quoted("version"),
        "PAPER_TITLE": _quoted("title"),
    }
    return variables


def save_variables(variables: dict[str, str], path: Path) -> Path:
    """Write the token map as sorted-key JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(variables, indent=2, sort_keys=True) + "\n")
    return path


def manuscript_tokens(manuscript_dir: Path) -> set[str]:
    """Every ``{{TOKEN}}`` used in authored numbered manuscript sections."""
    found: set[str] = set()
    for path in sorted(manuscript_dir.glob("*.md")):
        if path.name in _DOC_ONLY:
            continue
        found.update(_TOKEN_RE.findall(path.read_text()))
    return found


def hydrate_manuscript(
    project_root: Path, variables: dict[str, str]
) -> dict[str, Path]:
    """Substitute tokens into ``output/manuscript/`` (standalone, no Layer 1)."""
    src = project_root / "manuscript"
    dest = project_output_dirs(project_root)["output"] / "manuscript"
    dest.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for path in sorted(src.iterdir()):
        if not path.is_file():
            continue
        text = path.read_text()
        if path.suffix == ".md" and path.name not in _DOC_ONLY:
            for key, value in variables.items():
                text = text.replace("{{" + key + "}}", value)
        out = dest / path.name
        out.write_text(text)
        written[path.name] = out
    return written


def leftover_tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text)
