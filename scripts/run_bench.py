from __future__ import annotations

import argparse
from pathlib import Path

from vireon_rd.engine import run_one, run_suite


def main() -> None:
    ap = argparse.ArgumentParser(description="Run benchmark suites and write results/")
    ap.add_argument("--out", default="results", help="base output directory")
    ap.add_argument("--seeds", default="1,2,3,4,5", help="comma-separated seeds")
    args = ap.parse_args()

    out = Path(args.out)
    seeds = [int(x.strip()) for x in args.seeds.split(",") if x.strip()]

    # SQK: suite + one canonical run
    run_one("sqk", seed=seeds[0], out_dir=out / "sqk" / f"seed_{seeds[0]}")
    run_suite("sqk", seeds=seeds, out_dir=out / "sqk_suite")

    # Gray–Scott: suite + one canonical run
    run_one("gs", seed=seeds[0], out_dir=out / "gs" / f"seed_{seeds[0]}")
    run_suite("gs", seeds=seeds, out_dir=out / "gs_suite")

    print("OK: wrote benchmark artifacts to", out)


if __name__ == "__main__":
    main()
