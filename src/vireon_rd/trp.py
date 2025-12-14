from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class TRPConfig:
    # small ε to avoid division by zero
    eps: float = 1e-9
    # allow time to be penalized as T^power
    time_power: float = 1.0
    # hard floors to prevent collapse to 0
    result_floor: float = 1e-12
    product_floor: float = 1e-12


def trp_score(R: float, P: float, T: float, cfg: TRPConfig) -> float:
    r = max(float(R), cfg.result_floor)
    p = max(float(P), cfg.product_floor)
    t = max(float(T), 0.0)
    return (r * p) / ((t ** cfg.time_power) + cfg.eps)


def trp_rotate(
    TRP: float,
    *,
    R: Optional[float] = None,
    P: Optional[float] = None,
    T: Optional[float] = None,
    eps: float = 1e-9,
) -> Dict[str, float]:
    """
    “Rotation” identities (algebraic solves) when 2 of {R,P,T} are known.

    TRP = (R*P)/(T+eps)
      => R = TRP*(T+eps)/P
      => P = TRP*(T+eps)/R
      => T = (R*P)/TRP - eps
    """
    out: Dict[str, float] = {"TRP": float(TRP)}

    known = {"R": R is not None, "P": P is not None, "T": T is not None}
    if sum(known.values()) < 2:
        # not enough info to solve
        if R is not None:
            out["R"] = float(R)
        if P is not None:
            out["P"] = float(P)
        if T is not None:
            out["T"] = float(T)
        return out

    if R is None and (P is not None) and (T is not None):
        out["R"] = float(TRP) * (float(T) + eps) / float(P)
    if P is None and (R is not None) and (T is not None):
        out["P"] = float(TRP) * (float(T) + eps) / float(R)
    if T is None and (R is not None) and (P is not None):
        out["T"] = (float(R) * float(P)) / float(TRP) - eps

    if R is not None:
        out["R"] = float(R)
    if P is not None:
        out["P"] = float(P)
    if T is not None:
        out["T"] = float(T)

    return out
