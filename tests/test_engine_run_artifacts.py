from __future__ import annotations

import json
from pathlib import Path

from vireon_rd import specs as specs_mod
from vireon_rd.engine import run_one
from vireon_rd.specs import ForcingSpec, GridSpec, SQKModelGSpec


def test_engine_run_writes_artifacts(tmp_path: Path, monkeypatch) -> None:
    # Keep it fast: override default SQK spec to tiny grid + short time
    tiny_grid = GridSpec(N=32, L=20.0, dt=0.05, T=0.5, save_every=2)
    tiny_spec = SQKModelGSpec(grid=tiny_grid, forcing=ForcingSpec(scale=0.0), enable_forcing=False)

    def _tiny_get_spec(name: str):
        if name.strip().lower() == "sqk":
            return tiny_spec
        return specs_mod.get_spec(name)

    monkeypatch.setattr(specs_mod, "get_spec", _tiny_get_spec)

    out_dir = tmp_path / "out"
    run_one("sqk", seed=1, out_dir=out_dir)

    assert (out_dir / "meta.json").exists()
    assert (out_dir / "metrics.json").exists()
    assert (out_dir / "falsifiers.json").exists()
    assert (out_dir / "report.md").exists()

    meta = json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))
    metrics = json.loads((out_dir / "metrics.json").read_text(encoding="utf-8"))
    fals = json.loads((out_dir / "falsifiers.json").read_text(encoding="utf-8"))

    assert meta["spec"] == "sqk"
    assert "TRP" in metrics
    assert "E_current" in metrics
    assert "TRPGate" in fals
