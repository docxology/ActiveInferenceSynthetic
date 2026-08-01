"""The Markov blanket — conditional independence of internal and external states.

The extended abstract organizes Active Inference around a **Markov blanket**: a
statistical boundary that splits *external* states $\\eta$ from *internal* states
$\\mu$, which couple only through *sensory* $s$ and *active* $a$ blanket states.
The blanket's defining property is a **conditional independence**: internal and
external states are dependent in general, but become independent *once the
blanket is known* —

$$
p(\\eta, \\mu \\mid b) = p(\\eta \\mid b)\\, p(\\mu \\mid b), \\qquad b = (s, a).
$$

This module makes that property computable for the tractable case where the
joint over $(\\eta, s, a, \\mu)$ is a multivariate Gaussian. Two facts from
Gaussian graphical models do the work, and both are asserted against analytic
references in the tests:

1. **Conditioning is a Schur complement.** For a jointly-Gaussian partition,
   the covariance of a target block given another block is
   $\\Sigma_{T\\mid G} = \\Sigma_{TT} - \\Sigma_{TG}\\,\\Sigma_{GG}^{-1}\\,\\Sigma_{GT}$.
   Off-diagonal entries of $\\Sigma_{T\\mid G}$ are the residual couplings that
   survive conditioning.
2. **Zeros of the precision matrix are conditional independences.** In a
   Gaussian, variables $i$ and $j$ are independent given *all* the others iff
   the precision (inverse-covariance) entry $\\Pi_{ij} = 0$. So a blanket $b$
   renders $\\eta \\perp \\mu \\mid b$ exactly when the $\\eta$–$\\mu$ block of
   $\\Pi$ vanishes.

The demonstration builds a joint whose precision has a zero $\\eta$–$\\mu$ block
(so the blanket structure holds by construction) and then shows the payoff that
is *not* obvious from that construction: $\\eta$ and $\\mu$ are **marginally
correlated** (they talk, through the blanket), yet their **partial correlation
given $b$ is zero** — the blanket screens them off.

Everything is analytic and deterministic — no RNG, no fitting.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

__all__ = [
    "covariance_from_precision",
    "conditional_covariance",
    "partial_correlation",
    "correlation_matrix",
    "is_markov_blanket",
]

_TOL = 1e-9


def _check_spd(matrix: NDArray[np.float64], name: str) -> NDArray[np.float64]:
    """Validate a symmetric positive-definite (finite) matrix."""
    arr = np.asarray(matrix, dtype=np.float64)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError(f"{name} must be square 2-D, got shape {arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must be finite (no NaN/inf)")
    if not np.allclose(arr, arr.T, atol=1e-10):
        raise ValueError(f"{name} must be symmetric")
    if float(np.linalg.eigvalsh(arr).min()) <= 0.0:
        raise ValueError(f"{name} must be positive-definite")
    return arr


def covariance_from_precision(precision: NDArray[np.float64]) -> NDArray[np.float64]:
    """Invert a precision (inverse-covariance) matrix to a covariance matrix.

    Args:
        precision: A symmetric positive-definite precision matrix ``Π``.

    Returns:
        The covariance ``Σ = Π^{-1}`` (symmetrized to remove numerical asymmetry).

    Raises:
        ValueError: If ``precision`` is not square, not finite, not symmetric,
            not positive-definite, or too ill-conditioned to invert stably.
    """
    arr = _check_spd(precision, "precision")
    cov = np.linalg.inv(arr)
    if not np.all(np.isfinite(cov)):
        raise ValueError(
            "precision is too ill-conditioned to invert stably (non-finite covariance)"
        )
    return 0.5 * (cov + cov.T)


def _check_indices(idx: NDArray[np.int_] | list[int], n: int, name: str) -> list[int]:
    out = [int(i) for i in idx]
    if len(out) == 0:
        raise ValueError(f"{name} must be non-empty")
    if len(set(out)) != len(out):
        raise ValueError(f"{name} must not repeat indices, got {out}")
    if any(not 0 <= i < n for i in out):
        raise ValueError(f"{name} indices out of range [0, {n}): {out}")
    return out


def conditional_covariance(
    cov: NDArray[np.float64],
    target_idx: list[int],
    given_idx: list[int],
) -> NDArray[np.float64]:
    """Covariance of the target block given the conditioning block (Schur complement).

    ``Σ_{T|G} = Σ_TT − Σ_TG Σ_GG^{-1} Σ_GT``.

    Args:
        cov: Symmetric positive-definite joint covariance.
        target_idx: Indices of the variables whose conditional covariance is
            wanted.
        given_idx: Indices of the conditioning (observed) variables. Must be
            disjoint from ``target_idx``.

    Returns:
        The ``len(target) × len(target)`` conditional covariance matrix.

    Raises:
        ValueError: If ``cov`` is not SPD, indices are out of range, or target
            and given overlap.
    """
    arr = _check_spd(cov, "covariance")
    n = arr.shape[0]
    t = _check_indices(target_idx, n, "target_idx")
    g = _check_indices(given_idx, n, "given_idx")
    if set(t) & set(g):
        raise ValueError(
            f"target and given must be disjoint; overlap {set(t) & set(g)}"
        )
    s_tt = arr[np.ix_(t, t)]
    s_tg = arr[np.ix_(t, g)]
    s_gg = arr[np.ix_(g, g)]
    return s_tt - s_tg @ np.linalg.solve(s_gg, s_tg.T)


def partial_correlation(
    cov: NDArray[np.float64],
    i: int,
    j: int,
    given_idx: list[int],
) -> float:
    """Partial correlation between variables ``i`` and ``j`` given a set.

    Zero partial correlation means ``i`` and ``j`` are conditionally
    uncorrelated (and, for a Gaussian, conditionally independent) given the
    conditioning set.

    Args:
        cov: Symmetric positive-definite joint covariance.
        i: First variable index.
        j: Second variable index (``!= i``, and not in ``given_idx``).
        given_idx: Indices of the conditioning variables.

    Returns:
        The partial correlation ``ρ(i, j | given) ∈ [-1, 1]``.
    """
    if i == j:
        raise ValueError("i and j must differ")
    # cov is validated SPD inside conditional_covariance, so its Schur
    # complement is positive-definite and both conditional variances are > 0.
    cond = conditional_covariance(cov, [i, j], given_idx)
    return float(cond[0, 1] / np.sqrt(cond[0, 0] * cond[1, 1]))


def correlation_matrix(cov: NDArray[np.float64]) -> NDArray[np.float64]:
    """Convert a covariance matrix to its correlation matrix (unit diagonal)."""
    arr = _check_spd(cov, "covariance")
    d = np.sqrt(np.diag(arr))
    return arr / np.outer(d, d)


def is_markov_blanket(
    precision: NDArray[np.float64],
    internal_idx: list[int],
    external_idx: list[int],
    tol: float = 1e-9,
) -> bool:
    """Return ``True`` iff the internal–external block of the precision is ~0.

    In a Gaussian, ``Π_{ij} = 0`` means variables ``i`` and ``j`` are
    conditionally independent given all the others. So the remaining variables
    (the blanket) screen the internal states from the external states exactly
    when every internal–external precision entry vanishes.

    Args:
        precision: The inverse-covariance (precision) matrix.
        internal_idx: Indices of the internal states ``μ``.
        external_idx: Indices of the external states ``η``.
        tol: Magnitude below which a precision entry counts as zero
            (must be finite and non-negative).

    Returns:
        ``True`` if ``|Π[μ, η]| <= tol`` for every internal/external pair.

    Raises:
        ValueError: If ``precision`` is not a valid (finite, symmetric,
            positive-definite) precision matrix, ``tol`` is negative, or the
            index sets overlap or are out of range.
    """
    if not np.isfinite(tol) or tol < 0.0:
        raise ValueError(f"tol must be finite and non-negative, got {tol}")
    arr = _check_spd(precision, "precision")
    n = arr.shape[0]
    internal = _check_indices(internal_idx, n, "internal_idx")
    external = _check_indices(external_idx, n, "external_idx")
    if set(internal) & set(external):
        raise ValueError("internal and external index sets must be disjoint")
    block = arr[np.ix_(internal, external)]
    return bool(np.all(np.abs(block) <= tol))
