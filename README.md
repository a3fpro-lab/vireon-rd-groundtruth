# VIREON × TRP Reaction–Diffusion GroundTruth Engine

This is a **simulation + evaluation + falsification** engine for reaction–diffusion systems.

The point is not “pretty patterns.” The point is **certified behavior**:
- reproducible across seeds
- stable under numerical refinement
- separable from baselines
- gated by explicit falsifiers

---

## Core contracts (math)

- TRP:
  \[
  \mathrm{TRP}=\frac{R\,P}{T+\varepsilon}
  \]
- Energy proxy:
  \[
  E_{\text{current}}=\frac{T+\varepsilon}{RP}=1/\mathrm{TRP}
  \]
- Suite slack:
  \[
  \Delta E_{\text{store}}=E_{\text{current}}-E_{\text{global\_min}}\ge 0
  \]
- KL:
  \[
  D_{\mathrm{KL}}(p\|q)=\sum_i p_i\log\frac{p_i}{q_i}
  \]

---

## What this repo certifies (and does NOT certify)

**Certifies**: whether an RD model’s observed pattern class is **robust** under perturbations and **passes gates**.

**Does not certify**: any fundamental-physics claim from pattern appearance alone.

---

## Commands

Skeleton smoke:
```bash
python -m vireon_rd smoke
