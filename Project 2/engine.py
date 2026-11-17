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


def reserve_weight(w):
    return sum(w[a] for a in C.RESERVE_ELIGIBLE)


def liquid_weight(w):
    return sum(w[a] for a in C.ASSETS if C.REDEEM_DAYS[a] <= C.LIQUIDITY_DAYS)


def largest_issuer(w):
    totals = {}
    for a in C.ASSETS:
        if C.ISSUER[a] not in C.EXEMPT_ISSUERS:
            totals[C.ISSUER[a]] = totals.get(C.ISSUER[a], 0) + w[a]
    return max(totals.values(), default=0.0)


def static_ok(w, lim):
    return (min(w.values()) >= -1e-9 and abs(sum(w.values()) - 1) < 1e-9
            and reserve_weight(w) >= lim["reserve_min"] - 1e-9
            and liquid_weight(w) >= lim["liquidity_min"] - 1e-9
            and largest_issuer(w) <= lim["issuer_max"] + 1e-9)


def trade_size(a_w, b_w):
    return sum(abs(a_w[x] - b_w[x]) for x in C.ASSETS) / 2


def constrained(mu, cov, lim, objective=C.OBJECTIVE_RETURN, current=None):
    """Lab 13 S10 answered as in Lab 14: the lowest ex-ante volatility mix that meets every
    limit checkable at the decision date (S3, S5, S6, S8, and S7 for this trade) and reaches
    the objective return. If no mix inside the limits reaches the objective, return the
    highest-expected-return mix inside the limits and flag it.
    Returns (weights, objective_met) or (None, False) when no mix meets the limits."""
    ok = [w for w in grid() if static_ok(w, lim)
          and (current is None or trade_size(w, current) <= lim["turnover_max"] + 1e-9)]
    if not ok:
        return None, False
    meets = [w for w in ok if port_return(w, mu) >= objective - 1e-12]
    if meets:
        return min(meets, key=lambda w: (port_vol(w, cov), -port_return(w, mu))), True
    return max(ok, key=lambda w: (port_return(w, mu), -port_vol(w, cov))), False


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
    path, yearly = [], {}
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
                    target = w_cur or equal_weight()
                    mu = None
                else:
                    mu = expected_returns(dgs10, rets, i, s)
                    target, met = constrained(mu, cov, lim, s.get("objective", C.OBJECTIVE_RETURN), w_cur)
                    if target is None:
                        problems.append(f"{dates[i]}: no portfolio meets the limits")
                        target = w_cur or equal_weight()
                    elif not met:
                        problems.append(f"{dates[i]}: no portfolio inside the limits reaches the "
                                        f"{s.get('objective', C.OBJECTIVE_RETURN):.1%} objective")
            else:
                target = equal_weight() if strategy == "equal" else benchmark()
                mu = expected_returns(dgs10, rets, i, s) if dgs10 is not None else None
            trade = 0.0 if w_cur is None else trade_size(target, w_cur)
            if w_cur is not None:
                turnover_total += trade
                yearly[dates[i][:4]] = yearly.get(dates[i][:4], 0.0) + trade
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
    vals = [v for _, v in path]
    lag = min(12, len(vals) - 1)
    worst_12m = min((vals[k] / vals[k - lag] - 1 for k in range(lag, len(vals))), default=0.0)
    res = {"strategy": strategy, "start": dates[first], "end": dates[last], "months": len(monthly),
           "growth_of_1": value, "ann_return": ann_ret, "ann_vol": ann_vol, "max_drawdown": max_dd,
           "turnover_per_year": turnover_year, "worst_12m_loss": max(0.0, -worst_12m),
           "max_turnover_year": max(yearly.values(), default=0.0), "final_weights": dict(w_cur), "log": log, "path": path, "problems": problems, "limits": lim}
    res["checks"] = mandate_checks(res)
    return res


# ---------------------------------------------------------------- mandate verdict
def mandate_checks(res):
    lim = res["limits"]
    w = res["log"][-1]["weights"]
    worst_reserve = min(reserve_weight(x["weights"]) for x in res["log"])
    checks = [
        ("S5 Weights sum to 100%", sum(w.values()) * 100, abs(sum(w.values()) - 1) < 1e-9),
        ("S5 Long-only, no leverage (lowest weight)", min(w.values()) * 100, min(w.values()) >= -1e-9),
        (f"S3 Reserve-eligible (SGOV+TLT) at least {lim['reserve_min']:.0%} (every decision)", worst_reserve * 100,
         worst_reserve >= lim["reserve_min"] - 1e-9),
        (f"S6 Largest nonexempt issuer at most {lim['issuer_max']:.0%}", largest_issuer(w) * 100,
         largest_issuer(w) <= lim["issuer_max"] + 1e-9),
        (f"S7 Turnover at most {lim['turnover_max']:.0%} in any year", res["max_turnover_year"] * 100,
         res["max_turnover_year"] <= lim["turnover_max"] + 1e-9),
        (f"S8 Redeemable in {C.LIQUIDITY_DAYS} days at least {lim['liquidity_min']:.0%}", liquid_weight(w) * 100,
         liquid_weight(w) >= lim["liquidity_min"] - 1e-9),
        (f"S9 Worst 12-month loss at most {lim['loss_max']:.0%}", res["worst_12m_loss"] * 100,
         res["worst_12m_loss"] <= lim["loss_max"] + 1e-9),
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
    ("Constraint: reserve at least 15% (not 3%)", {"limits": {"reserve_min": 0.15}}),
    ("Constraint: 12-month loss at most 5% (not 10%)", {"limits": {"loss_max": 0.05}}),
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
        if v == "PASS" and r["problems"]:
            v = "MISS"      # inside the limits, but the objective could not be reached
        rows.append({"scenario": name, "latest_weights": r["log"][-1]["weights"],
                     "ann_return": r["ann_return"], "max_drawdown": r["max_drawdown"],
                     "ann_vol": r["ann_vol"], "turnover_per_year": r["turnover_per_year"],
                     "max_turnover_year": r["max_turnover_year"], "worst_12m_loss": r["worst_12m_loss"],
                     "objective_met": not r["problems"],
                     "verdict": v, "failed_rules": fails, "problems": r["problems"],
                     "start": r["start"]})
    return rows


def stop_condition(base_res, stress_rows):
    reasons = []
    v, fails = verdict(base_res)
    if v == "FAIL":
        reasons.append("Base case breaks: " + "; ".join(fails))
    reasons += base_res["problems"]
    n_fail = sum(1 for r in stress_rows if r["verdict"] in ("FAIL", "MISS"))
    if n_fail >= C.STRESS_FAIL_STOP:
        reasons.append(f"{n_fail} stress scenarios break a hard limit or miss the objective "
                       f"(stop at {C.STRESS_FAIL_STOP})")
    return ("STOP" if reasons else "GO"), reasons


def allocation_range(stress_rows):
    """Min-max of each weight at the latest decision across scenarios that pass."""
    ok = [r for r in stress_rows if r["verdict"] == "PASS"] or stress_rows
    return {a: (min(r["latest_weights"][a] for r in ok), max(r["latest_weights"][a] for r in ok))
            for a in C.ASSETS}


def trigger_review(dates, rets, signal_table, res, s=None):
    """Off-cycle check on the latest data: has the yield trigger fired since the last
    rebalance, and what would the model hold if it rebalanced today?"""
    s = s or {}
    lim = {**C.LIMITS, **s.get("limits", {})}
    window = s.get("window", C.ESTIMATION_WINDOW_MONTHS)
    i = len(dates) - 1
    last_dec = res["log"][-1]
    dgs10, status = signal_on(dates[i], signal_table)
    out = {"date": dates[i], "dgs10": dgs10, "status": status, "last_decision": last_dec["date"],
           "last_dgs10": last_dec["dgs10"], "band": (last_dec["dgs10"] - C.YIELD_TRIGGER_BAND, last_dec["dgs10"] + C.YIELD_TRIGGER_BAND),
           "current_weights": res["final_weights"]}
    out["triggered"] = dgs10 is not None and not (out["band"][0] <= dgs10 <= out["band"][1])
    if dgs10 is not None and status == "ok":
        mu = expected_returns(dgs10, rets, i, s)
        cov = covariance_matrix(rets, i, window)
        w, met = constrained(mu, cov, lim, s.get("objective", C.OBJECTIVE_RETURN), res["final_weights"])
        out.update({"review_weights": w, "objective_met": met,
                    "review_expected_return": port_return(w, mu) if w else None,
                    "review_vol": port_vol(w, cov) if w else None,
                    "current_expected_return": port_return(res["final_weights"], mu),
                    "trade": trade_size(w, res["final_weights"]) if w else None})
    return out


def run_all(s=None):
    dates, prices = load_prices()
    rets = monthly_returns(prices)
    sig = load_signal()
    results = {k: backtest(dates, rets, sig, k, s) for k in ("equal", "benchmark", "constrained")}
    stress = stress_run(dates, rets, sig, s)
    status, reasons = stop_condition(results["constrained"], stress)
    review = trigger_review(dates, rets, sig, results["constrained"], s)
    return {"dates": dates, "results": results, "stress": stress, "stop": status, "review": review,
            "stop_reasons": reasons, "range": allocation_range(stress), "signal": sig}
