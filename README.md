[![CI](https://github.com/a3fpro-lab/vireon-rd-groundtruth/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/a3fpro-lab/vireon-rd-groundtruth/actions/workflows/ci.yml)
[![Bench](https://github.com/a3fpro-lab/vireon-rd-groundtruth/actions/workflows/bench.yml/badge.svg?branch=main)](https://github.com/a3fpro-lab/vireon-rd-groundtruth/actions/workflows/bench.yml)

# VIREON × TRP Reaction–Diffusion GroundTruth Engine

**Proof bundle:** generate `results/EVIDENCE_PACK.md` locally, or run the **Bench** workflow and download it from the `vireon-rd-results` artifact.

This repo is a **falsification-first** evaluation engine for reaction–diffusion (RD) models.

It is not “a cool sim.” It is a reproducible harness that:
- runs RD systems (currently **SQK-like 3-field** + **Gray–Scott baseline**),
- extracts objective pattern statistics (**spectral peak**, **anisotropy**, **localization**),
- measures stability/drift (KL divergence of spectra over time),
- scores via **TRP** and suite-level **ΔE_store**.

If a model is fragile, resolution-dependent, or seed-dependent, the engine catches it.

---

## Quickstart (local)

```bash
python -m pip install -r requirements.txt
python -m pip install -e .

vireon-rd smoke

# Run one:
vireon-rd run --spec sqk --seed 1 --out results/run_sqk_seed1
vireon-rd run --spec gs  --seed 1 --out results/run_gs_seed1

# Run a suite:
vireon-rd suite --spec sqk --seeds 1,2,3,4,5 --out results/sqk_suite
vireon-rd suite --spec gs  --seeds 1,2,3,4,5 --out results/gs_suite
