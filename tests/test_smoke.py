from __future__ import annotations

from vireon_rd.engine import main


def test_cli_smoke_runs(capsys) -> None:
    main(["smoke"])
    out = capsys.readouterr().out
    assert "engine CLI is live" in out
