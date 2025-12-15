# Support

This repository is built to be self-verifying via:
- CI (`.github/workflows/ci.yml`)
- Contract tests (`CONTRACT.md`, tests/)
- Reproduction recipe (`REPRODUCE.md`)
- Evidence Pack output (`results/EVIDENCE_PACK.md`)

## If something breaks
Please open a GitHub Issue and include:

1) Your command(s):
- `vireon-rd run ...` or `vireon-rd suite ...`

2) Your environment:
- Python version
- OS

3) The files from your run directory:
- `meta.json`
- `metrics.json`
- `falsifiers.json`
- `report.md`

If you ran a suite, include:
- `suite.json`

## What we will NOT debug
- silent “screenshots” without the JSON artifacts
- claims without `EVIDENCE_PACK.md` or the underlying run folders
