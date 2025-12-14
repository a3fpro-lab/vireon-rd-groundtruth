from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .trp import TRPConfig, trp_score


@dataclass(frozen=True)
class FalsifierConfig:
    # gates
    min_trp: float = 1e-6
    min_localization: float = 0.40
    max_kl_drift: float = 1.0
    require_finite_lambda: bool = True
    forbid_blank: bool = True


def compute_RP_from_metrics(metrics: dict[str, float]) -> tuple[float, float]:
    """
    Define R and P from metrics.

    R (Result): strength of structure (localization proxy)
    P (Product): coherence proxy (1 / (1 + anisotropy + KL drift))
    """
    loc = float(metrics.get("localization", 0.0))
    an = float(metrics.get("anisotropy", 0.0))
    kl = float(metrics.get("kl_mean_to_final", 0.0))

    R = max(loc, 0.0)
    P = 1.0 / (1.0 + max(an, 0.0) + max(kl, 0.0))
    return R, P


def falsify_one(
    *,
    metrics: dict[str, float],
    T: float,
    trp_cfg: TRPConfig,
    cfg: FalsifierConfig,
) -> tuple[dict[str, bool], dict[str, float]]:
    """
    Returns (gates, extras) where extras includes TRP and E_current.
    """
    label = str(metrics.get("label", "unknown"))
    loc = float(metrics.get("localization", 0.0))
    kl = float(metrics.get("kl_mean_to_final", 0.0))
    lam = float(metrics.get("lambda_star", float("nan")))

    R, P = compute_RP_from_metrics(metrics)
    TRP = trp_score(R, P, T, trp_cfg)
    E_current = (T + trp_cfg.eps) / max(R * P, 1e-12)

    gates: dict[str, bool] = {}
    gates["TRPGate"] = cfg.min_trp <= TRP
    gates["LocalizationGate"] = cfg.min_localization <= loc
    gates["DriftGate"] = kl <= cfg.max_kl_drift

    if cfg.require_finite_lambda:
        gates["LambdaFiniteGate"] = bool(np.isfinite(lam) and lam > 0.0)
    else:
        gates["LambdaFiniteGate"] = True

    if cfg.forbid_blank:
        gates["NonBlankGate"] = label != "blank"
    else:
        gates["NonBlankGate"] = True

    extras = {"R": float(R), "P": float(P), "TRP": float(TRP), "E_current": float(E_current)}
    return gates, extras


def suite_delta_e_store(E_currents: list[float]) -> tuple[float, float]:
    """
    Given a list of E_current values across a suite, returns (E_global_min, ΔE_store_mean).
    """
    if not E_currents:
        return 0.0, 0.0
    E_min = float(np.min(E_currents))
    dE_mean = float(np.mean([e - E_min for e in E_currents]))
    return E_min, dE_mean
