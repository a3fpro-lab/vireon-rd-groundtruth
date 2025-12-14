from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _read_json(p: Path) -> dict[str, Any]:
    return json.loads(p.read_text(encoding="utf-8"))


def _fmt(x: Any) -> str:
    try:
        if x is None:
            return "-"
        if isinstance(x, bool):
            return "PASS" if x else "FAIL"
        if isinstance(x, (int, float)):
            return f"{float(x):.6g}"
    except Exception:
        pass
    return str(x)


def _row(spec: str, suite: dict[str, Any]) -> str:
    return (
        f"| {spec} | {_fmt(suite.get('E_global_min'))} | {_fmt(suite.get('dE_store_mean'))} "
        f"| {_fmt(len(suite.get('runs', [])))} |"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate VIREON-RD Evidence Pack markdown from results/")
    ap.add_argument("--root", default="results", help="root results directory")
    ap.add_argument("--sqk", default="sqk_suite", help="sqk suite folder name under root")
    ap.add_argument("--gs", default="gs_suite", help="gs suite folder name under root")
    ap.add_argument("--out", default="results/EVIDENCE_PACK.md", help="markdown output path")
    args = ap.parse_args()

    root = Path(args.root)
    sqk_suite = _read_json(root / args.sqk / "suite.json")
    gs_suite = _read_json(root / args.gs / "suite.json")

    # include one representative run report links (seed_1)
    sqk_meta = _read_json(root / args.sqk / "seed_1" / "meta.json")
    sqk_metrics = _read_json(root / args.sqk / "seed_1" / "metrics.json")
    sqk_gates = _read_json(root / args.sqk / "seed_1" / "falsifiers.json")

    gs_meta = _read_json(root / args.gs / "seed_1" / "meta.json")
    gs_metrics = _read_json(root / args.gs / "seed_1" / "metrics.json")
    gs_gates = _read_json(root / args.gs / "seed_1" / "falsifiers.json")

    lines: list[str] = []
    lines.append("# VIREON × TRP RD GroundTruth — Evidence Pack")
    lines.append("")
    lines.append("This file is generated from reproducible suite runs. It summarizes:")
    lines.append("- suite-level ΔE_store (robustness slack)")
    lines.append("- TRP-derived metrics")
    lines.append("- falsifier gates")
    lines.append("")

    lines.append("## Suite summary")
    lines.append("")
    lines.append("| Spec | E_global_min | dE_store_mean | Runs |")
    lines.append("|---|---:|---:|---:|")
    lines.append(_row("sqk", sqk_suite))
    lines.append(_row("gs", gs_suite))
    lines.append("")

    def block(title: str, meta: dict[str, Any], metrics: dict[str, Any], gates: dict[str, Any]) -> None:
        lines.append(f"## Representative run: `{title}` (seed=1)")
        lines.append("")
        lines.append("### Meta (numerical health included)")
        lines.append("```json")
        lines.append(json.dumps(meta, indent=2))
        lines.append("```")
        lines.append("")
        lines.append("### Metrics")
        lines.append("```json")
        lines.append(json.dumps(metrics, indent=2))
        lines.append("```")
        lines.append("")
        lines.append("### Falsifiers")
        for k in sorted(gates.keys()):
            lines.append(f"- **{k}**: {'PASS' if gates[k] else 'FAIL'}")
        lines.append("")

    block("sqk", sqk_meta, sqk_metrics, sqk_gates)
    block("gs", gs_meta, gs_metrics, gs_gates)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: wrote {out_path}")


if __name__ == "__main__":
    main()
