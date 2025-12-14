# Engine Contract (Stability Promise)

This repo is meant to be cited and replicated. So we define what is stable.

## 1) Artifact contract (run outputs)
`vireon-rd run ...` MUST always emit:
- `meta.json`
- `metrics.json`
- `falsifiers.json`
- `report.md`

`vireon-rd suite ...` MUST always emit:
- `suite.json`

## 2) Metric keys (minimum set)
`metrics.json` MUST include:
- `label`
- `lambda_star`
- `anisotropy`
- `localization`
- `kl_mean_to_final`
- `TRP`
- `E_current`

## 3) Falsifier keys (minimum set)
`falsifiers.json` MUST include:
- `TRPGate`
- `LocalizationGate`
- `DriftGate`
- `LambdaFiniteGate`
- `NonBlankGate`

## 4) Backward compatibility
- New metrics may be added.
- Existing keys should not be removed in 0.x unless a major mistake is proven.
- If a rename is unavoidable, we support both keys for at least one minor version.

## 5) Reproducibility
- Specs must be explicit (grid, dt, T, forcing parameters).
- Seeds must be recorded in meta.
- Evaluation must be deterministic given the seed and spec.

This is how we keep it “undeniable.”
