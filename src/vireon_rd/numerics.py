from __future__ import annotations

import numpy as np

from .specs import ForcingSpec, GrayScottSpec, SQKModelGSpec


def laplacian_periodic(u: np.ndarray, dx: float) -> np.ndarray:
    """
    2D 5-point Laplacian with periodic boundary conditions.
    """
    return (
        np.roll(u, 1, axis=0)
        + np.roll(u, -1, axis=0)
        + np.roll(u, 1, axis=1)
        + np.roll(u, -1, axis=1)
        - 4.0 * u
    ) / (dx * dx)


def forcing_field(
    N: int,
    L: float,
    t: float,
    fs: ForcingSpec,
) -> np.ndarray:
    """
    χ(x,y,t) = -scale * exp(-r^2/(2*sigma_r^2)) * exp(-(t-t0)^2/(2*sigma_t^2))
    Centered at domain center.
    """
    dx = L / N
    x = (np.arange(N) - (N - 1) / 2.0) * dx
    X, Y = np.meshgrid(x, x, indexing="xy")
    r2 = X * X + Y * Y
    spatial = np.exp(-0.5 * r2 / (fs.sigma_r * fs.sigma_r))
    temporal = np.exp(-0.5 * ((t - fs.t0) ** 2) / (fs.sigma_t * fs.sigma_t))
    return -fs.scale * spatial * temporal


def init_sqk(spec: SQKModelGSpec, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Initialize (G, X, Y) near zero with a seeded Gaussian bump into X.
    """
    rng = np.random.default_rng(seed)
    N = spec.grid.N
    L = spec.grid.L
    dx = L / N
    x = (np.arange(N) - (N - 1) / 2.0) * dx
    Xg, Yg = np.meshgrid(x, x, indexing="xy")
    r2 = Xg * Xg + Yg * Yg

    bump = spec.seed_gaussian_amp * np.exp(-0.5 * r2 / (spec.seed_gaussian_sigma**2))

    G = 0.01 * rng.normal(size=(N, N))
    X = bump + 0.01 * rng.normal(size=(N, N))
    Y = 0.01 * rng.normal(size=(N, N))
    return G.astype(float), X.astype(float), Y.astype(float)


def init_grayscott(spec: GrayScottSpec, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Initialize (u, v) with central perturbation and small noise.
    """
    rng = np.random.default_rng(seed)
    N = spec.grid.N
    u = np.ones((N, N), dtype=float)
    v = np.zeros((N, N), dtype=float)

    s = max(1, int(spec.seed_square_frac * N))
    a = N // 2 - s // 2
    b = a + s

    u[a:b, a:b] = spec.seed_u
    v[a:b, a:b] = spec.seed_v

    u += spec.noise * rng.normal(size=(N, N))
    v += spec.noise * rng.normal(size=(N, N))
    return u, v
