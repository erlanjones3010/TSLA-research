"""Run with:  python -m pytest -q   (or  python tests/test_engine.py)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C   # noqa: E402
import engine as E   # noqa: E402

DATES, PRICES = E.load_prices()
RETS = E.monthly_returns(PRICES)
SIG = E.load_signal()


def test_signal_is_point_in_time():
    for d, row in SIG.items():
        assert row["observation_date"] < d, f"look-ahead on {d}"


def test_signal_not_stale():
    for d in SIG:
        _, status = E.signal_on(d, SIG)
        assert status == "ok", f"{d}: {status}"


def test_covariance_is_symmetric():
    cov = E.covariance_matrix(RETS, 30, 24)
    for a in C.ASSETS:
        for b in C.ASSETS:
            assert abs(cov[a, b] - cov[b, a]) < 1e-12


def test_constrained_meets_static_limits_every_quarter():
    r = E.backtest(DATES, RETS, SIG, "constrained")
    for d in r["log"]:
        w = d["weights"]
        assert abs(sum(w.values()) - 1) < 1e-9
        assert E.static_ok(w, C.LIMITS)
        assert d["ex_ante_vol"] <= C.LIMITS["vol_max"] + 1e-9


def test_baselines_fail_for_the_named_rule():
    eq = E.backtest(DATES, RETS, SIG, "equal")
    bm = E.backtest(DATES, RETS, SIG, "benchmark")
    assert E.verdict(eq)[0] == "FAIL" and any("SPY" in f for f in E.verdict(eq)[1])
    assert E.verdict(bm)[0] == "FAIL" and any("SGOV" in f for f in E.verdict(bm)[1])


def test_infeasible_limits_are_reported():
    r = E.backtest(DATES, RETS, SIG, "constrained", {"limits": {"vol_max": 0.01}})
    assert r["problems"], "an impossible volatility cap should be flagged"


def test_higher_costs_lower_return():
    lo = E.backtest(DATES, RETS, SIG, "constrained", {"cost_bps": 0})
    hi = E.backtest(DATES, RETS, SIG, "constrained", {"cost_bps": 100})
    assert hi["ann_return"] < lo["ann_return"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
