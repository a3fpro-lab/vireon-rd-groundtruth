from __future__ import annotations

import json
from pathlib import Path

from vireon_rd.engine import run_one


def test_meta_includes_status_fields(tmp_path: Path) -> None:
    out_dir = tmp_path / "run"
    run_one("sqk", seed=1, out_dir=out_dir)

    meta = json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))

    assert "status" in meta
    assert "stop_step" in meta
    assert "stop_time" in meta

    assert meta["status"] in {"ok", "blowup"}

    if meta["status"] != "ok":
        assert meta["stop_step"] is not None or meta["stop_time"] is not None
