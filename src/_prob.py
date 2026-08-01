"""Shared probability-vector validation and KL helpers."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

_TOL = 1e-9


def as_prob_vector(
    p: NDArray[np.float64] | list[float], name: str
) -> NDArray[np.float64]:
    """Coerce ``p`` to a 1-D float64 vector."""
    arr = np.asarray(p, dtype=np.float64)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be 1-D, got shape {arr.shape}")
    return arr


def as_distribution(p: NDArray[np.float64], name: str) -> NDArray[np.float64]:
    """Validate that ``p`` is a proper probability vector (>=0, sums to 1)."""
    if not np.all(np.isfinite(p)):
        raise ValueError(f"{name} must be finite (no NaN/inf), got {p}")
    if np.any(p < -_TOL):
        raise ValueError(f"{name} must be non-negative, got {p}")
    total = float(p.sum())
    if abs(total - 1.0) > 1e-8:
        raise ValueError(f"{name} must sum to 1, got {total}")
    return np.clip(p, 0.0, None)


def as_column_stochastic(
    a: NDArray[np.float64], name: str = "matrix"
) -> NDArray[np.float64]:
    """Validate an ``O × K`` matrix: non-negative, each column sums to 1."""
    arr = np.asarray(a, dtype=np.float64)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be 2-D (O x K), got shape {arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must be finite (no NaN/inf)")
    if np.any(arr < -_TOL):
        raise ValueError(f"{name} must be non-negative")
    col_sums = arr.sum(axis=0)
    if not np.allclose(col_sums, 1.0, atol=1e-8):
        raise ValueError(
            f"each column of {name} must sum to 1, got column sums {col_sums}"
        )
    return np.clip(arr, 0.0, None)


def kl_divergence(
    q: NDArray[np.float64],
    p: NDArray[np.float64],
) -> float:
    """KL divergence ``Σ q (ln q − ln p)`` over entries where ``q > 0``.

    For parity with the module's validation strictness, ``p`` must be strictly
    positive wherever ``q > 0`` (a zero reference entry there would make the
    log infinite); entries ``q == 0`` are ignored and may have arbitrary ``p``.

    Raises:
        ValueError: If ``p`` is not strictly positive where ``q`` is positive.
    """
    mask = q > 0.0
    if np.any(p[mask] <= 0.0):
        raise ValueError(
            "kl_divergence: reference distribution p must be strictly positive "
            "where q > 0 (finite log), got a zero/negative entry"
        )
    return float(np.sum(q[mask] * (np.log(q[mask]) - np.log(p[mask]))))
