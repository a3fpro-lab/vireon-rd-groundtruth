from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GridSpec:
    N: int = 128          # grid size (NxN)
    L: float = 40.0       # domain length (units)
    dt: float = 0.01      # timestep
    T: float = 60.0       # final time
    save_every: int = 10  # save stride (steps)


@dataclass(frozen=True)
class ForcingSpec:
    # χ(x,y,t) = -scale * exp(-r^2/(2*sigma_r^2)) * exp(-(t-t0)^2/(2*sigma_t^2))
    scale: float = 0.20
    sigma_r: float = 2.0
    t0: float = 10.0
    sigma_t: float = 3.0


@dataclass(frozen=True)
class SQKModelGSpec:
    """
    A practical, testable 3-field forced RD system inspired by SQK Model-G "potential-form" motifs:
      - three fields: G, X, Y
      - quadratic coupling: Q = (X + c1)^2 * (Y + c2)
      - optional localized forcing χ into X (organizer-like source)
    This is engineered as an evaluation testbed (not a physics endorsement).
    """
    grid: GridSpec = GridSpec()
    forcing: ForcingSpec = ForcingSpec()

    # diffusion (asymmetric)
    Dg: float = 0.05
    Dx: float = 0.20
    Dy: float = 0.60

    # "potential shift" constants (keep explicit; tuneable)
    c1: float = 140.0 / 9.0
    c2: float = 40.0 / 3.0

    # reaction gains / damping
    alpha_g: float = 0.010
    alpha_x: float = 0.020
    alpha_y: float = 0.015

    beta_g: float = 0.080
    beta_x: float = 0.120
    beta_y: float = 0.090

    # forcing toggle
    enable_forcing: bool = True

    # init
    seed_gaussian_amp: float = 0.40
    seed_gaussian_sigma: float = 2.0


@dataclass(frozen=True)
class GrayScottSpec:
    """
    Standard Gray–Scott baseline (2-field RD):
      u_t = Du ∆u - u v^2 + F(1-u)
      v_t = Dv ∆v + u v^2 - (F+k)v
    """
    grid: GridSpec = GridSpec()

    Du: float = 0.16
    Dv: float = 0.08
    F: float = 0.060
    k: float = 0.062

    # init
    noise: float = 0.02
    seed_square_frac: float = 0.10  # central square size as fraction of N
    seed_v: float = 0.25
    seed_u: float = 0.50


def get_spec(name: str) -> SQKModelGSpec | GrayScottSpec:
    key = name.strip().lower()
    if key in {"sqk", "sqk-g", "model-g", "modelg"}:
        return SQKModelGSpec()
    if key in {"gs", "gray-scott", "grayscott"}:
        return GrayScottSpec()
    raise ValueError(f"Unknown spec: {name!r} (use 'sqk' or 'gs')")
