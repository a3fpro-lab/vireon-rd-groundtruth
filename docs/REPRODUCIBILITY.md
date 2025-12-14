# Reproducibility Manifest

## Non-negotiable rule
If it can’t be rerun and falsified, it’s not a claim.

## What must be saved for any result
Every run/suite must emit:
- `meta.json` (engine hash + env snapshot)
- `metrics.json` (numbers)
- `falsifiers.json` (pass/fail)
- `report.md` (human-readable summary)

## Determinism requirements
- All randomized paths must be seedable.
- Suite runs must record the full parameter set.

## CI standard
- ruff check
- ruff format --check
- pytest

CI staying green is part of the claim.
