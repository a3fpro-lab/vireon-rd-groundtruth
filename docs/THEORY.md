# Theory Notes (Engine-Level)

## Forced reaction–diffusion (general form)
\[
\partial_t \mathbf{u}=\mathbf{D}\nabla^2\mathbf{u}+\mathbf{f}(\mathbf{u})+\mathbf{s}(\mathbf{x},t).
\]

This repo focuses on *forced* RD because forcing is a clean mathematical way to represent
localized “organizers” or external drives without breaking the RD framework.

## VIREON layers (evaluation decomposition)
- Truth: measurable structure (localization, amplitude)
- Revelation: spectral signatures + drift + KL
- Projection: single scalar TRP + energy proxy

## TRP and suite slack
\[
\mathrm{TRP}=\frac{R\,P}{T+\varepsilon},\quad
E_{\text{current}}=\frac{T+\varepsilon}{RP}=1/\mathrm{TRP},\quad
\Delta E_{\text{store}}=E_{\text{current}}-E_{\text{global\_min}}\ge 0.
\]

## Spectral classifier (structure factor)
Compute
\[
S(\mathbf{k})=|\mathcal{F}\{u-\bar u\}|^2
\]
then use a radial peak and anisotropy index to classify:
- spots (ring-like isotropic peak)
- stripes (anisotropic lobes)
- radial/forced localization (high localization + low anisotropy)

## KL divergence
\[
D_{\mathrm{KL}}(p\|q)=\sum_i p_i\log\frac{p_i}{q_i}
\]
Used as a stability / deviation score across spectral distributions.
