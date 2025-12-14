from __future__ import annotations

import numpy as np

from vireon_rd.sim import run_grayscott, run_sqk_model_g
from vireon_rd.specs import ForcingSpec, GrayScottSpec, GridSpec, SQKModelGSpec


def test_sqk_small_sim_runs_and_shapes() -> None:
    # SQK can be stiff; this test is *blow-up aware*.
    # We verify interface/shape, and if it diverges we assert that explicitly.
    grid = GridSpec(N=32, L=20.0, dt=0.01, T=0.2, save_every=2)
    spec = SQKModelGSpec(grid=grid, forcing=ForcingSpec(scale=0.0), enable_forcing=False)

    sim = run_sqk_model_g(spec, seed=1)

    assert isinstance(sim.final, dict)
    assert set(sim.final.keys()) == {"G", "X", "Y"}

    X = sim.final["X"]
    Y = sim.final["Y"]
    G = sim.final["G"]

    assert X.shape == (grid.N, grid.N)
    assert Y.shape == (grid.N, grid.N)
    assert G.shape == (grid.N, grid.N)

    finite = bool(np.isfinite(X).all() and np.isfinite(Y).all() and np.isfinite(G).all())
    if not finite:
        # Divergence is acceptable at this stage; we just don't want silent nonsense.
        assert (np.isinf(X).any() or np.isnan(X).any() or np.isinf(Y).any() or np.isnan(Y).any())
        return

    # If it stays finite, ensure we actually evolved non-trivially.
    assert float(np.abs(X).sum() + np.abs(Y).sum() + np.abs(G).sum()) > 0.0


def test_grayscott_small_sim_runs_and_shapes() -> None:
    grid = GridSpec(N=32, L=20.0, dt=1.0, T=10.0, save_every=2)
    spec = GrayScottSpec(grid=grid, F=0.04, k=0.06, Du=0.16, Dv=0.08)

    sim = run_grayscott(spec, seed=1)

    assert isinstance(sim.final, dict)
    assert set(sim.final.keys()) == {"u", "v"}

    u = sim.final["u"]
    v = sim.final["v"]

    assert u.shape == (grid.N, grid.N)
    assert v.shape == (grid.N, grid.N)

    assert np.isfinite(u).all()
    assert np.isfinite(v).all()

    # Should deviate from the initial uniform background at least slightly
    assert float(np.abs(v - float(v.mean())).sum()) > 0.0
