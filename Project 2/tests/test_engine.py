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


def test_constrained_meets_limits_and_objective_every_decision():
    r = E.backtest(DATES, RETS, SIG, "constrained")
    for d in r["log"]:
        assert E.static_ok(d["weights"], C.LIMITS)
        assert d["expected_return"] >= C.OBJECTIVE_RETURN - 1e-9
        assert d["turnover"] <= C.LIMITS["turnover_max"] + 1e-9


def test_benchmark_fails_reserve_rule():
    bm = E.backtest(DATES, RETS, SIG, "benchmark")
    v, fails = E.verdict(bm)
    assert v == "FAIL" and any(f.startswith("S3") for f in fails)


def test_checker_catches_a_short_position():
    r = E.backtest(DATES, RETS, SIG, "equal")
    r["log"][-1]["weights"] = {"SGOV": -0.05, "TLT": 0.25, "VCIT": 0.25, "SPY": 0.55}
    v, fails = E.verdict({**r, "checks": E.mandate_checks(r)})
    assert v == "FAIL" and any("Long-only" in f for f in fails)


def test_unreachable_objective_is_reported():
    r = E.backtest(DATES, RETS, SIG, "constrained", {"objective": 0.20})
    assert r["problems"], "an impossible 20% objective should be flagged"


def test_higher_costs_lower_return():
    lo = E.backtest(DATES, RETS, SIG, "constrained", {"cost_bps": 0})
    hi = E.backtest(DATES, RETS, SIG, "constrained", {"cost_bps": 100})
    assert hi["ann_return"] < lo["ann_return"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
