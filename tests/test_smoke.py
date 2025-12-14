from vireon_rd.engine import main


def test_cli_smoke_runs(capsys):
    main(["smoke"])
    out = capsys.readouterr().out
    assert "skeleton is live" in out
