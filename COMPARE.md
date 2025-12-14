# Comparing Models: SQK vs Gray–Scott (VIREON × TRP GroundTruth)

This engine outputs **artifacts**, not vibes.

For each run:
- `meta.json`: spec + grid + dt + sim horizon
- `metrics.json`: measured statistics + TRP + E_current
- `falsifiers.json`: PASS/FAIL gates
- `report.md`: human-readable summary

For a suite:
- `suite.json`: E_global_min and ΔE_store_mean over seeds

---

## What counts as “better”

### 1) Falsifiers first (hard gates)
A model is **non-credible** for claims of robust structure if it fails:
- **LocalizationGate** (structure too weak / diffuse)
- **LambdaFiniteGate** (no stable dominant scale)
- **DriftGate** (pattern not stable in time; spectral KL drift too large)
- **NonBlankGate** (degenerate output)

If it fails gates, TRP does not rescue it.

### 2) TRP (the score)
We use:
\[
\mathrm{TRP}=\frac{R\cdot P}{T+\varepsilon}
\]
- Higher TRP = more result/coherence per time budget.

In `metrics.json`:
- `R` and `P` are derived from measured metrics (localization, anisotropy, drift).
- `TRP` is computed by `vireon_rd.trp`.

### 3) E_current and ΔE_store (suite-level stability)
We also define:
\[
E_{\text{current}}=\frac{T+\varepsilon}{R\cdot P}
\]
Over a suite of perturbations/seeds:
\[
E_{\text{global\_min}}=\min_i E_{\text{current}}^{(i)},\quad
\Delta E_{\text{store}}^{(i)}=E_{\text{current}}^{(i)}-E_{\text{global\_min}}
\]
The suite reports:
- `E_global_min`
- `dE_store_mean`

Interpretation:
- Lower `E_current` is better.
- Lower `dE_store_mean` means the model is **consistently near its best behavior** (robustness).
- High `dE_store_mean` means the model is fragile: sometimes great, usually not.

---

## Minimal “win conditions” (for credible claims)

A model can claim robustness over another if, on the same suite:
1) It passes all falsifier gates on most seeds
2) Its mean TRP is higher (or median TRP is higher)
3) Its `dE_store_mean` is lower (more stable)

SQK “wins” against Gray–Scott only if it wins on these measurable terms.

---

## How to run comparison

Local:
```bash
python scripts/run_bench.py --out results --seeds 1,2,3,4,5
