"""Isotropic 2-D Ornstein–Uhlenbeck / Bayesian-mechanics model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

_ROT = np.array([[0.0, 1.0], [-1.0, 0.0]])


@dataclass(frozen=True)
class IsotropicOU:
    """Isotropic Gaussian free energy with dissipative and solenoidal terms.

    Parameters:
        precision: Inverse-variance of the belief (``> 0``).
        gamma: Dissipative strength. ``>= 0`` for deterministic flow;
            ``> 0`` required for steady-state / diffusion quantities.
        omega: Solenoidal strength. Zero means detailed balance.
    """

    precision: float = 1.0
    gamma: float = 1.0
    omega: float = 0.0

    def __post_init__(self) -> None:
        if not (
            np.isfinite(self.precision)
            and np.isfinite(self.gamma)
            and np.isfinite(self.omega)
        ):
            raise ValueError(
                "precision, gamma, omega must be finite; "
                f"got {self.precision}, {self.gamma}, {self.omega}"
            )
        if self.precision <= 0.0:
            raise ValueError(f"precision must be > 0, got {self.precision}")
        if self.gamma < 0.0:
            raise ValueError(f"gamma must be >= 0, got {self.gamma}")

    def require_positive_gamma(self) -> None:
        """Raise if ``gamma <= 0`` (steady-state / diffusion path)."""
        if self.gamma <= 0.0:
            raise ValueError(f"gamma must be > 0, got {self.gamma}")

    @property
    def P(self) -> NDArray[np.float64]:
        return self.precision * np.eye(2)

    @property
    def Gamma(self) -> NDArray[np.float64]:
        return self.gamma * np.eye(2)

    @property
    def Q(self) -> NDArray[np.float64]:
        return self.omega * _ROT

    def drift_M(self) -> NDArray[np.float64]:
        """Drift matrix ``M = (Γ − Q) P``."""
        return (self.Gamma - self.Q) @ self.P

    def free_energy(
        self,
        x: NDArray[np.float64],
        y: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        xa = np.asarray(x, dtype=np.float64)
        ya = np.asarray(y, dtype=np.float64)
        return 0.5 * self.precision * (xa**2 + ya**2)

    def grad_free_energy(
        self,
        x: NDArray[np.float64],
        y: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        xa = np.asarray(x, dtype=np.float64)
        ya = np.asarray(y, dtype=np.float64)
        return self.precision * xa, self.precision * ya

    def flow_field(
        self,
        x: NDArray[np.float64],
        y: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Bayesian-mechanics flow ``f = (Q − Γ) @ grad F``."""
        dfdx, dfdy = self.grad_free_energy(x, y)
        fx = -self.gamma * dfdx + self.omega * dfdy
        fy = -self.gamma * dfdy - self.omega * dfdx
        return fx, fy

    def velocity(self, state: NDArray[np.float64]) -> NDArray[np.float64]:
        """Flow at a single ``(x, y)`` state as a 2-vector."""
        fx, fy = self.flow_field(
            np.asarray(state[0]),
            np.asarray(state[1]),
        )
        return np.array([float(fx), float(fy)], dtype=np.float64)
