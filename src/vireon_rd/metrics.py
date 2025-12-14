from __future__ import annotations

import math

import numpy as np


def safe_log(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    return np.log(np.maximum(x, eps))


def kl_divergence(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
    """
    D_KL(p||q) for discrete distributions (nonnegative, not necessarily normalized).
    """
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    p = np.maximum(p, 0.0)
    q = np.maximum(q, 0.0)
    sp = float(p.sum())
    sq = float(q.sum())
    if sp <= eps or sq <= eps:
        return 0.0
    p = p / sp
    q = q / sq
    return float((p * (safe_log(p, eps) - safe_log(q, eps))).sum())


def structure_factor_2d(u: np.ndarray) -> np.ndarray:
    """
    S(kx,ky) = |FFT(u - mean(u))|^2
    """
    x = np.asarray(u, dtype=float)
    x = x - float(x.mean())
    F = np.fft.fft2(x)
    S = np.abs(F) ** 2
    return np.fft.fftshift(S)


def radial_average(S: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Radial average of a 2D array around its center.
    Returns (r, profile) with integer radii bins.
    """
    S = np.asarray(S, dtype=float)
    ny, nx = S.shape
    cy = (ny - 1) / 2.0
    cx = (nx - 1) / 2.0
    y, x = np.indices((ny, nx))
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    r_int = r.astype(int)
    r_max = int(r_int.max())
    prof = np.zeros(r_max + 1, dtype=float)
    cnt = np.zeros(r_max + 1, dtype=float)
    np.add.at(prof, r_int, S)
    np.add.at(cnt, r_int, 1.0)
    prof = prof / np.maximum(cnt, 1.0)
    return np.arange(r_max + 1, dtype=float), prof


def peak_wavelength_from_profile(r: np.ndarray, prof: np.ndarray) -> float:
    """
    Estimate dominant wavelength λ* from peak radius in the radial spectrum.

    Uses k_index ~= r_peak, so λ* ~ 2π / k_peak in index-units.
    If peak is at 0 or too flat, returns NaN.
    """
    r = np.asarray(r, dtype=float)
    prof = np.asarray(prof, dtype=float)
    if prof.size < 5:
        return float("nan")

    # ignore DC region (first few bins)
    start = min(3, prof.size - 1)
    idx = int(np.argmax(prof[start:]) + start)
    k = float(r[idx])
    if k <= 0.0:
        return float("nan")
    return float(2.0 * math.pi / k)


def anisotropy_index(S: np.ndarray, eps: float = 1e-12) -> float:
    """
    Simple anisotropy proxy from second moments around center in Fourier domain.
    0 ~ isotropic; larger => more directional.
    """
    S = np.asarray(S, dtype=float)
    ny, nx = S.shape
    cy = (ny - 1) / 2.0
    cx = (nx - 1) / 2.0
    y, x = np.indices((ny, nx))
    w = np.maximum(S, 0.0)
    Z = float(w.sum())
    if Z <= eps:
        return 0.0
    dx = x - cx
    dy = y - cy
    mxx = float((w * dx * dx).sum()) / Z
    myy = float((w * dy * dy).sum()) / Z
    # normalized difference
    return float(abs(mxx - myy) / (mxx + myy + eps))


def localization_index(u: np.ndarray, q: float = 0.95, eps: float = 1e-12) -> float:
    """
    How concentrated is the field energy?
    Returns fraction of L2 energy contained in top-q pixels (by |u|).
    """
    x = np.asarray(u, dtype=float)
    e = x * x
    total = float(e.sum())
    if total <= eps:
        return 0.0
    flat = np.sort(e.ravel())
    k = int(max(1, round((1.0 - q) * flat.size)))
    # top-q => drop lowest (1-q)
    top = float(flat[k:].sum())
    return float(top / total)
