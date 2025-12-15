# Changelog

All notable changes to this project are documented here.

This project follows a simple rule:
- If the output contract changes, it is a breaking change and requires a version bump.

---

## v0.1.0-groundtruth — 2025-12-14

Initial GroundTruth release.

### Added
- Falsification-first RD evaluation engine (SQK-like 3-field + Gray–Scott baseline).
- Objective metrics: spectral peak wavelength, anisotropy, localization, KL drift over time.
- TRP scoring layer and suite-level ΔE_store aggregation.
- Hard contract: meta.json / metrics.json / falsifiers.json / report.md per run.
- Numerical health surfaced in meta/report: status ∈ {ok, blowup}, stop_step, stop_time.
- Evidence Pack generator producing results/EVIDENCE_PACK.md.
- Bench workflow that runs suites and uploads a complete results artifact.
- REPRODUCE.md (exact reproduction steps).
- CITATION.cff (GitHub citation support).
