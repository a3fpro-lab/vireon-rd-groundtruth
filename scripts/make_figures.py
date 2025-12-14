from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from vireon_rd.metrics import peak_wavelength_from_profile, radial_average, structure_factor_2d
from vireon_rd.sim import run_grayscott, run_sqk_model_g
from vireon_rd.specs import GrayScottSpec, SQKModelGSpec, get_spec


def _pick_field(spec_name: str, final: dict[str, np.ndarray]) -> tuple[str, np.ndarray]:
    if spec_name == "sqk":
        return "X", final["X"]
    if spec_name == "gs":
        return "v", final["v"]
    raise ValueError(spec_name)


def _run_final_field(spec_name: str, seed: int) -> tuple[float, np.ndarray]:
    spec = get_spec(spec_name)

    if isinstance(spec, SQKModelGSpec):
        sim = run_sqk_model_g(spec, seed=seed)
    elif isinstance(spec, GrayScottSpec):
        sim = run_grayscott(spec, seed=seed)
    else:
        raise TypeError("Unknown spec type")

    _, field = _pick_field(spec_name, sim.final)
    dx = spec.grid.L / spec.grid.N
    return dx, field


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate figures for a single run (field + spectrum).")
    ap.add_argument("--spec", default="sqk", choices=["sqk", "gs"])
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--figdir", default="results/figures", help="directory to write figures")
    args = ap.parse_args()

    figdir = Path(args.figdir)
    figdir.mkdir(parents=True, exist_ok=True)

    dx, field = _run_final_field(args.spec, args.seed)

    # --- Figure 1: final field ---
    plt.figure()
    plt.imshow(field, origin="lower")
    plt.title(f"{args.spec} seed={args.seed} final field")
    plt.colorbar()
    out1 = figdir / f"{args.spec}_seed{args.seed}_field.png"
    plt.savefig(out1, dpi=200, bbox_inches="tight")
    plt.close()

    # --- Figure 2: radial-averaged structure factor ---
    S2 = structure_factor_2d(field)
    k, prof = radial_average(S2, dx=dx)
    lam = peak_wavelength_from_profile(k, prof)

    plt.figure()
    plt.plot(k, prof)
    plt.title(f"{args.spec} seed={args.seed} radial spectrum (lambda*={lam:.4g})")
    plt.xlabel("k")
    plt.ylabel("S_radial(k)")
    out2 = figdir / f"{args.spec}_seed{args.seed}_spectrum.png"
    plt.savefig(out2, dpi=200, bbox_inches="tight")
    plt.close()

    # --- Write a tiny figure note ---
    note = figdir / f"{args.spec}_seed{args.seed}_figures.txt"
    note.write_text(
        "\n".join(
            [
                f"spec={args.spec}",
                f"seed={args.seed}",
                f"dx={dx}",
                f"lambda_star={lam}",
                f"field_png={out1.name}",
                f"spectrum_png={out2.name}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"OK: wrote {out1}")
    print(f"OK: wrote {out2}")
    print(f"OK: wrote {note}")


if __name__ == "__main__":
    main()
