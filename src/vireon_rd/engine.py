from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from .eval import EvalConfig, eval_field, eval_time_drift
from .falsify import FalsifierConfig, falsify_one, suite_delta_e_store
from .io import asdict_safe, run_meta, write_json, write_report_md
from .sim import run_grayscott, run_sqk_model_g
from .specs import GrayScottSpec, SQKModelGSpec, get_spec
from .trp import TRPConfig

ENGINE_VERSION = "0.1.0"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="vireon-rd",
        description="VIREON × TRP RD GroundTruth Engine",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    runp = sub.add_parser("run", help="run one model + evaluate + falsify")
    runp.add_argument("--spec", default="sqk", choices=["sqk", "gs"])
    runp.add_argument("--seed", type=int, default=1)
    runp.add_argument("--out", default="results/run", help="output directory")

    suite = sub.add_parser("suite", help="run multiple seeds and compute ΔE_store over suite")
    suite.add_argument("--spec", default="sqk", choices=["sqk", "gs"])
    suite.add_argument("--seeds", default="1,2,3,4,5", help="comma-separated seeds")
    suite.add_argument("--out", default="results/suite", help="output directory")

    sub.add_parser("smoke", help="minimal smoke command")
    return p


def _pick_primary_field(model: str, final: dict[str, np.ndarray]) -> np.ndarray:
    if model == "sqk":
        return final["X"]
    if model == "gs":
        return final["v"]
    raise ValueError(model)


def run_one(spec_name: str, seed: int, out_dir: Path) -> None:
    spec = get_spec(spec_name)

    if isinstance(spec, SQKModelGSpec):
        sim = run_sqk_model_g(spec, seed=seed)
        model = "sqk"
        T = spec.grid.T
        primary_series = [snap["X"] for snap in sim.snapshots]
    elif isinstance(spec, GrayScottSpec):
        sim = run_grayscott(spec, seed=seed)
        model = "gs"
        T = spec.grid.T
        primary_series = [snap["v"] for snap in sim.snapshots]
    else:
        raise TypeError("Unknown spec type")

    primary_final = _pick_primary_field(model, sim.final)

    eval_cfg = EvalConfig()
    m = eval_field(primary_final, eval_cfg)
    m.update(eval_time_drift(primary_series))

    trp_cfg = TRPConfig()
    fals_cfg = FalsifierConfig()
    gates, extras = falsify_one(metrics=m, T=T, trp_cfg=trp_cfg, cfg=fals_cfg)
    metrics = dict(m)
    metrics.update(extras)

    meta = run_meta(
        engine_version=ENGINE_VERSION,
        spec_name=spec_name,
        seed=seed,
        extra={
            "model": model,
            "grid": asdict_safe(spec.grid),
            "dt": float(sim.dt),
            "T": float(sim.T),
        },
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "meta.json", meta)
    write_json(out_dir / "metrics.json", metrics)
    write_json(out_dir / "falsifiers.json", gates)
    write_report_md(out_dir / "report.md", meta, metrics, gates)


def run_suite(spec_name: str, seeds: list[int], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    E_list: list[float] = []
    runs: list[dict[str, float]] = []

    for s in seeds:
        run_dir = out_dir / f"seed_{s}"
        run_one(spec_name, s, run_dir)

        mj = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
        e = float(mj.get("E_current", 0.0))
        trp = float(mj.get("TRP", 0.0))
        E_list.append(e)
        runs.append({"seed": float(s), "E_current": e, "TRP": trp})

    E_min, dE_mean = suite_delta_e_store(E_list)
    suite_summary = {
        "spec": spec_name,
        "seeds": seeds,
        "E_global_min": E_min,
        "dE_store_mean": dE_mean,
        "runs": runs,
    }
    write_json(out_dir / "suite.json", suite_summary)


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)

    if args.cmd == "smoke":
        print("OK: vireon-rd engine CLI is live.")
        return

    if args.cmd == "run":
        run_one(args.spec, int(args.seed), Path(args.out))
        print(f"OK: wrote {args.out}")
        return

    if args.cmd == "suite":
        seeds = [int(x.strip()) for x in str(args.seeds).split(",") if x.strip()]
        run_suite(args.spec, seeds, Path(args.out))
        print(f"OK: wrote {args.out}")
        return

    raise SystemExit(2)
