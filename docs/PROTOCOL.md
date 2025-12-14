# GroundTruth Protocol (Certification Rules)

This repo is an evaluation + falsification engine for reaction–diffusion (RD) models.

## What counts as evidence here
A run is evidence only if it is:
1) **reproducible** across seeds,
2) **numerically stable** under refinement (N, dt),
3) **baseline-separable** (vs Gray–Scott controls),
4) **falsifiable** (explicit pass/fail gates).

Patterns alone are not evidence.

## Gates (must pass)
- LocalizationGate: localization_index ≥ threshold
- SpectralGate: tail_snr ≥ threshold
- LambdaFiniteGate: λ* finite and > 0
- TRPGate: TRP ≥ threshold
- NonBlankGate: label not blank/unknown

## Suite-level requirements
A suite should include:
- baseline configuration
- ablations (e.g., remove forcing / remove nonlinearity)
- at least one baseline model (Gray–Scott)
- ΔE_store table across suite

## Reproducibility artifacts
A claim must ship:
- `meta.json`
- `metrics.json`
- `falsifiers.json`
- `report.md`
