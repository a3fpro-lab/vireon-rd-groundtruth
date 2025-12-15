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

One command generates the full proof bundle:

```bash
make install
make evidence

Open:
	•	results/EVIDENCE_PACK.md

If you want to run individual pieces:

# CLI sanity
vireon-rd smoke

# Run one:
vireon-rd run --spec sqk --seed 1 --out results/run_sqk_seed1
vireon-rd run --spec gs  --seed 1 --out results/run_gs_seed1

# Run suites:
vireon-rd suite --spec sqk --seeds 1,2,3,4,5 --out results/sqk_suite
vireon-rd suite --spec gs  --seeds 1,2,3,4,5 --out results/gs_suite

Generate the Evidence Pack (the proof bundle)

After you run both suites above:

python scripts/evidence_pack.py --root results --sqk sqk_suite --gs gs_suite --out results/EVIDENCE_PACK.md

Output:
	•	results/EVIDENCE_PACK.md (single markdown “evidence” file)
	•	plus suite artifacts under results/sqk_suite/ and results/gs_suite/

This is the file you can paste anywhere to show: metrics, falsifiers, TRP, ΔE_store, numerical health.

⸻

GitHub Actions: Bench workflow
	•	Go to Actions → Bench → Run workflow
	•	Optionally set seeds (default: 1,2,3,4,5)
	•	The workflow uploads a vireon-rd-results artifact containing:
	•	results/*
	•	results/EVIDENCE_PACK.md

⸻

Core math (TRP + ΔE_store)

TRP (control signal)

We use a single score:

$$
\mathrm{TRP}=\frac{R\cdot P}{T+\varepsilon}
$$
	•	(R): “Result” term (structure strength)
	•	(P): “Product / robustness” term (penalizes drift + anisotropy)
	•	(T): time/compute proxy (simulation horizon)
	•	(\varepsilon>0): avoids division by zero

Engine-defined (R,P) (current):
	•	(R := \max(\mathrm{localization}, 0))
	•	(P := \frac{1}{1+\max(\mathrm{anisotropy},0)+\max(\mathrm{KL},0)})

Rotation identities (algebraic solves)

Given TRP and two of ({R,P,T}) (with (\varepsilon) known):
	•	(R = \mathrm{TRP}\cdot (T+\varepsilon)/P)
	•	(P = \mathrm{TRP}\cdot (T+\varepsilon)/R)
	•	(T = (R\cdot P)/\mathrm{TRP} - \varepsilon)

Suite-level ΔE_store (robustness slack)

Per run, the engine also computes:

$$
E_{\text{current}} := \frac{T+\varepsilon}{\max(R\cdot P,10^{-12})}
$$

Across a suite of perturbed runs (seeds / settings):

$$
\Delta E_{\text{store}} = E_{\text{current}} - E_{\text{global_min}} \ge 0,
\quad
E_{\text{global_min}}:=\min_{\text{suite}} E_{\text{current}}.
$$

The suite reports:
	•	(E_{\text{global_min}})
	•	mean (\Delta E_{\text{store}}) across the suite

⸻

GroundTruth rules (non-negotiable)

Numerical health is surfaced

Every run emits meta.json with:
	•	status ∈ {ok, blowup}
	•	stop_step, stop_time (when blowup occurs)

No silent NaNs. No hiding instability.

Contract is enforced by CI

CI tests enforce:
	•	engine CLI smoke
	•	stable artifacts
	•	meta status fields
	•	ruff formatting/lint

See CONTRACT.md for the required schema and keys.

⸻

Public claim boundary (anti-strawman)

This repository makes engineering claims, not metaphysical ones.

What we claim
	•	A reproducible, falsification-first harness for RD models
	•	Objective, comparable metrics and gates across seeds/suites
	•	Explicit surfacing of numerical instability (status/stop_*)
	•	Model comparison via TRP + suite-level ΔE_store

What we do NOT claim
	•	We do not claim SQK (or any RD system here) is validated as fundamental physics.
	•	We do not claim particles, gravity, or cosmology are “explained” by these PDEs.
	•	The only “wins” recognized here are robustness + metrics + reproducibility improvements.

What counts as progress (this repo’s definition)

A model improves if it:
	•	passes falsifier gates across suites,
	•	keeps metrics stable under perturbations (seed/resolution/forcing),
	•	improves TRP and reduces ΔE_store_mean vs baselines (or widens separation cleanly),
	•	produces evidence pack outputs consistent across machines/CI runs.

⸻

Output layout

Single run directory:
	•	meta.json
	•	metrics.json
	•	falsifiers.json
	•	report.md

Suite directory:
	•	seed_*/ (one run each)
	•	suite.json

⸻

License

MIT — authored by Inkwon Song Jr.

