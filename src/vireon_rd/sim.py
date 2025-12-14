from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .numerics import forcing_field, init_grayscott, init_sqk, laplacian_periodic
from .specs import GrayScottSpec, SQKModelGSpec


@dataclass
class SimResult:
    model: str
    dt: float
    T: float
    save_every: int
    times: list[float] = field(default_factory=list)
    snapshots: list[dict[str, np.ndarray]] = field(default_factory=list)
    final: dict[str, np.ndarray] = field(default_factory=dict)


def run_sqk_model_g(spec: SQKModelGSpec, seed: int) -> SimResult:
    """
    Explicit-Euler integrator for the 3-field forced RD testbed.
    Periodic BC, 5-point Laplacian.
    """
    N = spec.grid.N
    L = spec.grid.L
    dt = spec.grid.dt
    T = spec.grid.T
    save_every = spec.grid.save_every
    dx = L / N

    G, X, Y = init_sqk(spec, seed=seed)
    steps = int(np.ceil(T / dt))

    out = SimResult(model="sqk", dt=dt, T=T, save_every=save_every)

    zero = np.zeros((N, N), dtype=float)

    for n in range(steps + 1):
        t = n * dt

        if n % save_every == 0:
            out.times.append(float(t))
            out.snapshots.append(
                {
                    "G": G.copy(),
                    "X": X.copy(),
                    "Y": Y.copy(),
                }
            )

        # build forcing χ (only into X channel by design)
        chi = forcing_field(N, L, t, spec.forcing) if spec.enable_forcing else zero

        # quadratic coupling
        Q = (X + spec.c1) ** 2 * (Y + spec.c2)

        # diffusion
        LG = laplacian_periodic(G, dx)
        LX = laplacian_periodic(X, dx)
        LY = laplacian_periodic(Y, dx)

        # reactions (engine-grade: explicit, tunable, not “claimed physics”)
        dG = spec.Dg * LG + spec.alpha_g * Q - spec.beta_g * G
        dX = spec.Dx * LX + spec.alpha_x * Q - spec.beta_x * X + chi
        dY = spec.Dy * LY + spec.alpha_y * Q - spec.beta_y * Y

        # explicit Euler
        G = G + dt * dG
        X = X + dt * dX
        Y = Y + dt * dY

    out.final = {"G": G, "X": X, "Y": Y}
    return out


def run_grayscott(spec: GrayScottSpec, seed: int) -> SimResult:
    """
    Explicit-Euler Gray–Scott baseline.
    """
    N = spec.grid.N
    L = spec.grid.L
    dt = spec.grid.dt
    T = spec.grid.T
    save_every = spec.grid.save_every
    dx = L / N

    u, v = init_grayscott(spec, seed=seed)
    steps = int(np.ceil(T / dt))

    out = SimResult(model="gs", dt=dt, T=T, save_every=save_every)

    for n in range(steps + 1):
        t = n * dt

        if n % save_every == 0:
            out.times.append(float(t))
            out.snapshots.append({"u": u.copy(), "v": v.copy()})

        Lu = laplacian_periodic(u, dx)
        Lv = laplacian_periodic(v, dx)

        uv2 = u * v * v
        du = spec.Du * Lu - uv2 + spec.F * (1.0 - u)
        dv = spec.Dv * Lv + uv2 - (spec.F + spec.k) * v

        u = u + dt * du
        v = v + dt * dv

    out.final = {"u": u, "v": v}
    return out
