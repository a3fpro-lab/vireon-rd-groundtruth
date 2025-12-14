# VIREON × TRP RD GroundTruth Engine — Contract

This repo is an evaluation engine. Its outputs are a contract.

If any of these fields change, it is a breaking change and requires:
- `ENGINE_VERSION` bump
- `CHANGELOG.md` entry

---

## Output directory contract (single run)

A single run directory MUST contain:

- `meta.json`
- `metrics.json`
- `falsifiers.json`
- `report.md`

---

## `meta.json` contract

`meta.json` MUST include:

### Identity
- `engine_version` (string)
- `spec` (string)
- `seed` (int)
- `utc` (string, ISO)
- `python` (string)
- `platform` (string)

### Simulation
- `model` (string: `"sqk"` or `"gs"`)
- `grid` (object/dict with at least: `N`, `L`, `dt`, `T`, `save_every`)
- `dt` (float)
- `T` (float)

### Numerical health (mandatory)
- `status` (string: `"ok"` or `"blowup"`)
- `stop_step` (int or null)
- `stop_time` (float or null)

If `status != "ok"`, then at least one of `stop_step` or `stop_time` MUST be non-null.

---

## `metrics.json` contract

`metrics.json` MUST include:

- `lambda_star` (float)
- `anisotropy` (float)
- `localization` (float)
- `kl_drift` (float)

TRP-layer fields MUST include:

- `R` (float)
- `P` (float)
- `TRP` (float)
- `E_current` (float)

Notes:
- `E_current = (T+eps)/(R*P)` as implemented by the engine’s TRP module.
- `eps` is internal but must be > 0.

---

## `falsifiers.json` contract

`falsifiers.json` MUST include boolean keys:

- `TRPGate`
- `LocalizationGate`
- `DriftGate`
- `LambdaFiniteGate`
- `NonBlankGate`

---

## `report.md` contract

`report.md` MUST render:
- Meta JSON block
- Metrics JSON block
- Falsifier PASS/FAIL list

If `meta.status != "ok"`, `report.md` MUST clearly display status + stop info near the top.

---

## Suite contract

A suite directory MUST contain:

- one subdir per seed: `seed_<N>/` with the single-run contract
- `suite.json`

`suite.json` MUST include:

- `spec`
- `seeds`
- `E_global_min`
- `dE_store_mean`
- `runs` (list with `{seed, E_current, TRP}`)

---

## Non-negotiable intent

This engine exists to prevent:
- cherry-picked runs
- silent numerical instability
- “looks cool” pattern claims without robustness
- unrepeatable parameter drift

If a model fails, the engine MUST say so.
