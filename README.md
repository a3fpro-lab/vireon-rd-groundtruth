![CI](../../actions/workflows/ci.yml/badge.svg)
![Bench](../../actions/workflows/bench.yml/badge.svg)

# VIREON × TRP Reaction–Diffusion GroundTruth Engine

This repo is a *falsification-first* evaluation engine for reaction–diffusion (RD) models.

It is not “a cool sim.” It is a reproducible harness that:
- runs RD systems (currently SQK-like 3-field + Gray–Scott baseline),
- extracts objective pattern statistics (spectral peak, anisotropy, localization),
- measures stability/drift (KL divergence of spectra over time),
- scores via **TRP** and **ΔE_store** across perturbation suites.

If a model is fragile, resolution-dependent, or seed-dependent, the engine catches it.

---

## Core math (TRP + ΔE_store)

We treat each run as producing measurable outcomes:

- **R** (Result): structure strength proxy (localization index)
- **P** (Product): coherence proxy (penalizes anisotropy + drift)
- **T** (Time): wall-clock proxy; here we use simulation horizon `T`

### TRP score
We use:
\[
\mathrm{TRP}=\frac{R\cdot P}{T+\varepsilon}.
\]

### Rotations (algebraic identities)
Given TRP and any 2 of {R,P,T}, solve the third:
- \(R=\mathrm{TRP}\frac{T+\varepsilon}{P}\)
- \(P=\mathrm{TRP}\frac{T+\varepsilon}{R}\)
- \(T=\frac{R P}{\mathrm{TRP}}-\varepsilon\)

### Energy proxy and stored slack
Define:
\[
E_{\text{current}}=\frac{T+\varepsilon}{R\cdot P}.
\]
For a suite of runs (multiple seeds / perturbations):
\[
E_{\text{global\_min}}=\min_i E_{\text{current}}^{(i)},\quad
\Delta E_{\text{store}}^{(i)}=E_{\text{current}}^{(i)}-E_{\text{global\_min}}.
\]
We report suite mean \(\langle \Delta E_{\text{store}}\rangle\).

Interpretation: how much “slack” remains between typical behavior and the best-achieved behavior under the same spec.

---

## What it measures

From a 2D field `u(x,y)`:
- **Structure factor** \(S(\mathbf{k}) = |\mathcal{F}\{u-\bar u\}|^2\)
- **Dominant wavelength** \(\lambda^\* = 2\pi/k_{\max}\) (from radial-averaged spectrum)
- **Anisotropy index** (stripe-ness)
- **Localization index** (how concentrated the top-q energy is)
- **Drift**: KL divergence between spectra over time

Then it applies falsifiers (gates):
- TRP gate
- localization gate
- drift gate
- finite-wavelength gate
- non-blank gate

---

## Quickstart (CLI)

Install (editable):
```bash
python -m pip install -r requirements.txt
python -m pip install -e .
