from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


def _json_default(o: Any):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return {"__ndarray__": True, "shape": o.shape, "dtype": str(o.dtype)}
    return str(o)


def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_json(path: Path, obj: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(obj, indent=2, default=_json_default) + "\n", encoding="utf-8")


def run_meta(engine_version: str, spec_name: str, seed: int, extra: dict[str, Any]) -> dict[str, Any]:
    meta = {
        "engine_version": engine_version,
        "spec": spec_name,
        "seed": int(seed),
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
    }
    meta.update(extra)
    return meta


def write_report_md(path: Path, meta: dict[str, Any], metrics: dict[str, Any], gates: dict[str, bool]) -> None:
    lines: list[str] = []
    lines.append(f"# Report: {meta.get('spec')} seed={meta.get('seed')}")
    lines.append("")
    lines.append("## Meta")
    lines.append("```json")
    lines.append(json.dumps(meta, indent=2, default=_json_default))
    lines.append("```")
    lines.append("")
    lines.append("## Metrics")
    lines.append("```json")
    lines.append(json.dumps(metrics, indent=2, default=_json_default))
    lines.append("```")
    lines.append("")
    lines.append("## Falsifiers")
    lines.append("")
    for k, v in gates.items():
        lines.append(f"- **{k}**: {'PASS' if v else 'FAIL'}")
    lines.append("")
    ensure_dir(path.parent)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def to_float_dict(d: dict[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    for k, v in d.items():
        try:
            out[k] = float(v)
        except Exception:
            continue
    return out


def asdict_safe(obj: Any) -> dict[str, Any]:
    try:
        return asdict(obj)
    except Exception:
        return {"repr": repr(obj)}
