"""Project 2 engine: data, point-in-time signal, portfolios, mandate checks,
backtest and stress run. Standard library only; app.py and run_analysis.py use it."""

import csv
import math
from datetime import date
from itertools import product
from pathlib import Path

import config as C

HERE = Path(__file__).parent


# ---------------------------------------------------------------- data
def load_prices(path=HERE / "data" / "prices.csv"):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for i, row in enumerate(rows):
        for a in C.ASSETS:
            if float(row[a]) <= 0:
                raise ValueError(f"Non-positive price for {a} on row {i + 2}.")
    dates = [r["Date"] for r in rows]
    if dates != sorted(dates) or len(set(dates)) != len(dates):
        raise ValueError("Price dates must be unique and in order.")
    return dates, {a: [float(r[a]) for r in rows] for a in C.ASSETS}


def monthly_returns(prices):
    return {a: [p[i] / p[i - 1] - 1 for i in range(1, len(p))] for a, p in prices.items()}


def load_signal(path=HERE / "data" / "dgs10_asof.csv"):
    with open(path, newline="") as f:
        return {r["decision_date"]: r for r in csv.DictReader(f)}


def signal_on(decision_date, signal_table):
    """The 10-yr yield known on the decision date, with a staleness check."""
    row = signal_table.get(decision_date)
    if row is None:
        return None, "missing"
    if row["observation_date"] >= decision_date:
        raise ValueError(f"Look-ahead: observation {row['observation_date']} is not before {decision_date}.")
    age = (date.fromisoformat(decision_date) - date.fromisoformat(row["observation_date"])).days
    status = "ok" if age <= C.SIGNAL_MAX_AGE_DAYS else f"stale ({age} days)"
    return float(row["dgs10_percent"]) / 100, status


# ---------------------------------------------------------------- estimates
def mean(xs):
    return sum(xs) / len(xs)


def covariance_matrix(rets, end, window):
    """Annualized covariance from the `window` monthly returns ending at index `end` (exclusive)."""
    cols = {a: rets[a][end - window:end] for a in C.ASSETS}
    mu = {a: mean(cols[a]) for a in C.ASSETS}
    cov = {}
    for a in C.ASSETS:
        for b in C.ASSETS:
            s = sum((x - mu[a]) * (y - mu[b]) for x, y in zip(cols[a], cols[b]))
            cov[a, b] = s / (window - 1) * 12
    return cov


def expected_returns(dgs10, rets, end, s=None):
    s = s or {}
    erp = s.get("erp", C.EQUITY_RISK_PREMIUM)
    spread = s.get("spread", C.CREDIT_SPREAD)
    sgov_12m = math.prod(1 + r for r in rets["SGOV"][end - 12:end]) - 1
    return {"SGOV": sgov_12m, "TLT": dgs10, "VCIT": dgs10 + spread, "SPY": dgs10 + erp}


def port_return(w, mu):
    return sum(w[a] * mu[a] for a in C.ASSETS)


def port_vol(w, cov):
    v = sum(w[a] * w[b] * cov[a, b] for a in C.ASSETS for b in C.ASSETS)
    return math.sqrt(max(v, 0.0))


# ---------------------------------------------------------------- portfolios
def equal_weight():
    return {a: 1 / len(C.ASSETS) for a in C.ASSETS}


def benchmark():
    return dict(C.BENCHMARK)


def grid(step=C.GRID_STEP):
    n = round(1 / step)
    for combo in product(range(n + 1), repeat=len(C.ASSETS) - 1):
        last = n - sum(combo)
        if last >= 0:
            yield {a: k / n for a, k in zip(C.ASSETS, (*combo, last))}


def static_ok(w, lim):
    return (w[C.EQUITY] >= lim["equity_min"] - 1e-9 and w[C.EQUITY] <= lim["equity_max"] + 1e-9
            and w[C.RESERVE] >= lim["reserve_min"] - 1e-9 and min(w.values()) >= -1e-9)


def constrained(mu, cov, lim):
    """Highest expected return that meets every limit checkable at the decision date;
    ties go to lower volatility. Returns None when nothing qualifies."""
    best = None
    for w in grid():
        if not static_ok(w, lim):
            continue
        vol = port_vol(w, cov)
        if vol > lim["vol_max"] + 1e-12:
            continue
        key = (round(port_return(w, mu), 12), -vol)
        if best is None or key > best[0]:
            best = (key, w)
    return None if best is None else best[1]


# ---------------------------------------------------------------- backtest
def decision_indices(dates, window):
    """Price-row indices that are quarter-ends with enough history before them."""
    out = []
    for i, d in enumerate(dates):
        if int(d[5:7]) in C.REBALANCE_MONTHS and i >= max(window, 12):
            out.append(i)
    return out


def backtest(dates, rets, signal_table, strategy, s=None):
    """strategy: 'equal', 'benchmark' or 'constrained'. Returns a results dict."""
    s = s or {}
    lim = {**C.LIMITS, **s.get("limits", {})}
    window = s.get("window", C.ESTIMATION_WINDOW_MONTHS)
    cost = s.get("cost_bps", C.COST_BPS) / 10000
    decisions = decision_indices(dates, window)
    if not decisions:
        raise ValueError("Not enough price history for this estimation window.")
    value, peak, max_dd = 1.0, 1.0, 0.0
    w_cur, monthly, log, turnover_total = None, [], [], 0.0
    path = []
    problems = []
    first, last = decisions[0], len(dates) - 1
    for i in range(first, last + 1):
        if i in decisions:
            dgs10, status = signal_on(dates[i], signal_table)
            # returns are indexed so rets[a][i-1] is the month ending at dates[i]
            cov = covariance_matrix(rets, i, window)
            if strategy == "constrained":
                if dgs10 is None or status != "ok":
                    problems.append(f"{dates[i]}: signal {status}")
                    target = w_cur or benchmark()
                    mu = None
                else:
                    mu = expected_returns(dgs10, rets, i, s)
                    target = constrained(mu, cov, lim)
                    if target is None:
                        problems.append(f"{dates[i]}: no portfolio meets the limits")
                        target = w_cur or benchmark()
            else:
                target = equal_weight() if strategy == "equal" else benchmark()
                mu = expected_returns(dgs10, rets, i, s) if dgs10 is not None else None
            trade = 0.0 if w_cur is None else sum(abs(target[a] - w_cur[a]) for a in C.ASSETS) / 2
            if w_cur is not None:
                turnover_total += trade
                value *= 1 - 2 * trade * cost
            log.append({"date": dates[i], "dgs10": dgs10, "signal_status": status,
                        "weights": dict(target), "ex_ante_vol": port_vol(target, cov),
                        "expected_return": port_return(target, mu) if mu else None,
                        "turnover": trade})
            w_cur = dict(target)
        if not path:
            path.append((dates[i], value))
        if i == last:
            break
        r = sum(w_cur[a] * rets[a][i] for a in C.ASSETS)   # month ending at dates[i+1]
        value *= 1 + r
        monthly.append(r)
        path.append((dates[i + 1], value))
        grown = {a: w_cur[a] * (1 + rets[a][i]) for a in C.ASSETS}
        tot = sum(grown.values())
        w_cur = {a: grown[a] / tot for a in C.ASSETS}
        peak = max(peak, value)
        max_dd = max(max_dd, 1 - value / peak)
    years = len(monthly) / 12
    ann_ret = value ** (1 / years) - 1 if years > 0 else 0.0
    ann_vol = (math.sqrt(sum((x - mean(monthly)) ** 2 for x in monthly) / (len(monthly) - 1)) * math.sqrt(12)
               if len(monthly) > 1 else 0.0)
    turnover_year = turnover_total / years if years > 0 else 0.0
    res = {"strategy": strategy, "start": dates[first], "end": dates[last], "months": len(monthly),
           "growth_of_1": value, "ann_return": ann_ret, "ann_vol": ann_vol, "max_drawdown": max_dd,
           "turnover_per_year": turnover_year, "log": log, "path": path, "problems": problems, "limits": lim}
    res["checks"] = mandate_checks(res)
    return res


# ---------------------------------------------------------------- mandate verdict
def mandate_checks(res):
    lim = res["limits"]
    latest = res["log"][-1]
    w = latest["weights"]
    worst_vol = max(x["ex_ante_vol"] for x in res["log"])
    checks = [
        ("Weights sum to 100%", sum(w.values()) * 100, abs(sum(w.values()) - 1) < 1e-9),
        ("Long-only (lowest weight)", min(w.values()) * 100, min(w.values()) >= -1e-9),
        (f"SPY between {lim['equity_min']:.0%} and {lim['equity_max']:.0%}", w[C.EQUITY] * 100,
         lim["equity_min"] - 1e-9 <= w[C.EQUITY] <= lim["equity_max"] + 1e-9),
        (f"SGOV at least {lim['reserve_min']:.0%}", w[C.RESERVE] * 100, w[C.RESERVE] >= lim["reserve_min"] - 1e-9),
        (f"Ex-ante volatility at most {lim['vol_max']:.0%} (worst decision)", worst_vol * 100,
         worst_vol <= lim["vol_max"] + 1e-9),
        (f"Backtest max drawdown at most {lim['drawdown_max']:.0%}", res["max_drawdown"] * 100,
         res["max_drawdown"] <= lim["drawdown_max"] + 1e-9),
        (f"Turnover at most {lim['turnover_max']:.0%} a year", res["turnover_per_year"] * 100,
         res["turnover_per_year"] <= lim["turnover_max"] + 1e-9),
    ]
    return [{"rule": r, "value": v, "pass": p} for r, v, p in checks]


def verdict(res):
    fails = [c["rule"] for c in res["checks"] if not c["pass"]]
    return ("PASS", []) if not fails else ("FAIL", fails)


# ---------------------------------------------------------------- stress run
STRESS_SCENARIOS = [
    ("Base case", {}),
    ("Estimates: equity premium 2% (not 4%)", {"erp": 0.02}),
    ("Estimates: credit spread 0.5% (not 1%)", {"spread": 0.005}),
    ("Window: 12 months (not 24)", {"window": 12}),
    ("Window: 36 months (not 24)", {"window": 36}),
    ("Costs: 50 bps (not 10)", {"cost_bps": 50}),
    ("Constraint: SPY at most 50% (not 70%)", {"limits": {"equity_max": 0.50}}),
    ("Constraint: volatility at most 8% (not 12%)", {"limits": {"vol_max": 0.08}}),
]


def stress_run(dates, rets, signal_table, base=None):
    base = base or {}
    rows = []
    for name, change in STRESS_SCENARIOS:
        s = {**base, **change}
        if "limits" in base or "limits" in change:
            s["limits"] = {**base.get("limits", {}), **change.get("limits", {})}
        r = backtest(dates, rets, signal_table, "constrained", s)
        v, fails = verdict(r)
        rows.append({"scenario": name, "latest_weights": r["log"][-1]["weights"],
                     "ann_return": r["ann_return"], "max_drawdown": r["max_drawdown"],
                     "ann_vol": r["ann_vol"], "turnover_per_year": r["turnover_per_year"],
                     "verdict": v, "failed_rules": fails, "problems": r["problems"],
                     "start": r["start"]})
    return rows


def stop_condition(base_res, stress_rows):
    reasons = []
    v, fails = verdict(base_res)
    if v == "FAIL":
        reasons.append("Base case breaks: " + "; ".join(fails))
    reasons += base_res["problems"]
    n_fail = sum(1 for r in stress_rows if r["verdict"] == "FAIL")
    if n_fail >= C.STRESS_FAIL_STOP:
        reasons.append(f"{n_fail} stress scenarios break a hard limit (stop at {C.STRESS_FAIL_STOP})")
    return ("STOP" if reasons else "GO"), reasons


def allocation_range(stress_rows):
    """Min-max of each weight at the latest decision across scenarios that pass."""
    ok = [r for r in stress_rows if r["verdict"] == "PASS"] or stress_rows
    return {a: (min(r["latest_weights"][a] for r in ok), max(r["latest_weights"][a] for r in ok))
            for a in C.ASSETS}


def run_all(s=None):
    dates, prices = load_prices()
    rets = monthly_returns(prices)
    sig = load_signal()
    results = {k: backtest(dates, rets, sig, k, s) for k in ("equal", "benchmark", "constrained")}
    stress = stress_run(dates, rets, sig, s)
    status, reasons = stop_condition(results["constrained"], stress)
    return {"dates": dates, "results": results, "stress": stress, "stop": status,
            "stop_reasons": reasons, "range": allocation_range(stress), "signal": sig}
