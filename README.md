File: README.md
Paste this (replace entire file):

![CI](../../actions/workflows/ci.yml/badge.svg)
![Bench](../../actions/workflows/bench.yml/badge.svg)

# VIREON × TRP Reaction–Diffusion GroundTruth Engine

This repo is a **falsification-first** evaluation engine for reaction–diffusion (RD) models.

It is not “a cool sim.” It is a reproducible harness that:
- runs RD systems (currently **SQK-like 3-field** + **Gray–Scott baseline**),
- extracts objective pattern statistics (spectral peak, anisotropy, localization),
- measures stability/drift (KL divergence of spectra over time),
- scores via **TRP** and suite-level **ΔE_store**.

If a model is fragile, resolution-dependent, or seed-dependent, the engine catches it.

---

## Quickstart (local)

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
vireon-rd smoke

Run one:

vireon-rd run --spec sqk --seed 1 --out results/run_sqk_seed1
vireon-rd run --spec gs  --seed 1 --out results/run_gs_seed1

Run a suite:

vireon-rd suite --spec sqk --seeds 1,2,3,4,5 --out results/sqk_suite
vireon-rd suite --spec gs  --seeds 1,2,3,4,5 --out results/gs_suite


⸻

Generate the Evidence Pack (the proof bundle)

After you run both suites above:

python scripts/evidence_pack.py --root results --sqk sqk_suite --gs gs_suite --out results/EVIDENCE_PACK.md

Output:
	•	results/EVIDENCE_PACK.md (single markdown “evidence” file)
	•	plus suite artifacts under results/sqk_suite/ and results/gs_suite/

This is the file you can paste anywhere to show: metrics, falsifiers, TRP, ΔE_store, and numerical health.

⸻

GitHub Actions Bench workflow
	•	Go to Actions → Bench → Run workflow
	•	Optionally set seeds (default: 1,2,3,4,5)
	•	The workflow uploads a vireon-rd-results artifact containing:
	•	results/*
	•	results/EVIDENCE_PACK.md

⸻

Core math (TRP + ΔE_store)

TRP (control signal)

The engine uses a single score:
[
\mathrm{TRP} = \frac{R \cdot P}{T + \varepsilon},
]
where:
	•	(R) = result quality term (pattern signal vs blank/degenerate),
	•	(P) = product/robustness term (penalizes drift/fragility),
	•	(T) = time/compute proxy (simulation horizon),
	•	(\varepsilon>0) avoids division by zero.

The engine also supports “rotation” identities (solve for (R), (P), or (T) given the others).

Suite-level ΔE_store (robustness slack)

Across a suite of perturbed runs:
[
\Delta E_{\text{store}} = E_{\text{current}} - E_{\text{global_min}} \ge 0
]
where:
	•	(E_{\text{current}}) is computed per-run from TRP-layer quantities,
	•	(E_{\text{global_min}}) is the minimum over the suite.

The suite output reports:
	•	(E_{\text{global_min}})
	•	mean (\Delta E_{\text{store}}) across seeds

⸻

GroundTruth rules (non-negotiable)

Numerical health is surfaced

Every run emits meta.json with:
	•	status ∈ {ok, blowup}
	•	stop_step, stop_time (when blowup occurs)

No silent NaNs. No hiding instability.

Contract is enforced by CI

See CONTRACT.md for the required schema and keys.
CI tests enforce:
	•	engine CLI smoke
	•	stable artifacts
	•	meta status fields
	•	ruff formatting/lint

⸻

Output layout

Single run directory:
	•	meta.json
	•	metrics.json
	•	falsifiers.json
	•	report.md

Suite directory:
	•	seed_<N>/ (one run each)
	•	suite.json

⸻

License

MIT — authored by Inkwon Song Jr. 
