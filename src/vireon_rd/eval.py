from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from .metrics import (
    anisotropy_index,
    kl_divergence,
    localization_index,
    peak_wavelength_from_profile,
    radial_average,
    structure_factor_2d,
)


Label = Literal["spots", "stripes", "radial", "blank", "unknown"]


@dataclass(frozen=True)
class EvalConfig:
    # localization fraction top-q
    loc_q: float = 0.95
    # classification thresholds
    anisotropy_stripe: float = 0.25
    localization_radial: float = 0.65
    blank_std: float = 1e-6


def classify_pattern(S: np.ndarray, u: np.ndarray, cfg: EvalConfig) -> Label:
    """
    Minimal classifier:
      - blank if field is near-constant
      - stripes if anisotropy > threshold
      - radial if highly localized
      - else spots
    """
    if float(np.std(u)) <= cfg.blank_std:
        return "blank"

    a = anisotropy_index(S)
    if a >= cfg.anisotropy_stripe:
        return "stripes"

    loc = localization_index(u, q=cfg.loc_q)
    if loc >= cfg.localization_radial:
        return "radial"

    return "spots"


def eval_field(u: np.ndarray, cfg: EvalConfig) -> dict[str, float]:
    """
    Compute metrics for a single 2D field.
    """
    S = structure_factor_2d(u)
    r, prof = radial_average(S)
    lam = peak_wavelength_from_profile(r, prof)
    a = anisotropy_index(S)
    loc = localization_index(u, q=cfg.loc_q)

    label = classify_pattern(S, u, cfg)

    return {
        "lambda_star": float(lam) if np.isfinite(lam) else float("nan"),
        "anisotropy": float(a),
        "localization": float(loc),
        "label": str(label),
    }


def eval_time_drift(
    fields_over_time: list[np.ndarray],
    cfg: EvalConfig,
) -> dict[str, float]:
    """
    Compute spectral drift over time using KL divergence between
    the last snapshot spectrum and earlier spectra (averaged).
    """
    if len(fields_over_time) < 2:
        return {"kl_mean_to_final": 0.0}

    S_final = structure_factor_2d(fields_over_time[-1])
    # normalize to distribution
    Sf = np.maximum(S_final, 0.0)
    Sf = Sf / max(float(Sf.sum()), 1e-12)

    kls: list[float] = []
    for u in fields_over_time[:-1]:
        S = structure_factor_2d(u)
        S = np.maximum(S, 0.0)
        S = S / max(float(S.sum()), 1e-12)
        kls.append(kl_divergence(S, Sf))
    return {"kl_mean_to_final": float(np.mean(kls)) if kls else 0.0}
