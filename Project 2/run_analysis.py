"""Run the full analysis without the app and save the results.

    python run_analysis.py

Writes output/results.md (readable) and output/results.json (every number).
"""
import json
from datetime import datetime
from pathlib import Path

import config as C
import engine as E

OUT = Path(__file__).parent / "output"
LABELS = {"equal": "Equal weight (25% each)", "benchmark": "60/40 benchmark (SPY/VCIT, S4)",
          "constrained": "Constrained portfolio (signal + limits)"}


def pct(x):
    return f"{x:.1%}"


def main():
    out = E.run_all()
    OUT.mkdir(exist_ok=True)
    res, last = out["results"], out["results"]["constrained"]["log"][-1]
    lines = [f"# Results — {C.CLIENT}", "",
             f"Run: {datetime.now():%Y-%m-%d %H:%M}  |  Decision date (as of): {last['date']}  |  "
             f"10-yr yield known then: {last['dgs10']:.2%} ({last['signal_status']})", "",
             f"Inputs: objective {C.OBJECTIVE_RETURN:.1%} (CPI {C.ASSUMED_CPI:.1%} + {C.REAL_RETURN_TARGET:.0%}), "
             f"equity premium {C.EQUITY_RISK_PREMIUM:.1%}, credit spread {C.CREDIT_SPREAD:.1%}, "
             f"window {C.ESTIMATION_WINDOW_MONTHS} months, cost {C.COST_BPS} bps, annual rebalance; limits: "
             f"reserve-eligible >= {C.LIMITS['reserve_min']:.0%}, issuer <= {C.LIMITS['issuer_max']:.0%}, "
             f"turnover <= {C.LIMITS['turnover_max']:.0%}/yr, liquidity >= {C.LIMITS['liquidity_min']:.0%} in "
             f"{C.LIQUIDITY_DAYS} days, 12-month loss <= {C.LIMITS['loss_max']:.0%}, long-only", "",
             "## Portfolios", "",
             "| Portfolio | SGOV | TLT | VCIT | SPY | Expected return | Return/yr | Vol/yr | Max DD | Worst-year turnover | Verdict |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, r in res.items():
        w = r["log"][-1]["weights"]
        v, fails = E.verdict(r)
        er = r["log"][-1]["expected_return"]
        lines.append(f"| {LABELS[k]} | " + " | ".join(pct(w[a]) for a in C.ASSETS) +
                     f" | {'%.2f%%' % (er * 100) if er is not None else '-'} | {pct(r['ann_return'])} | "
                     f"{pct(r['ann_vol'])} | {pct(r['max_drawdown'])} | {pct(r['max_turnover_year'])} | {v}{': ' + '; '.join(fails) if fails else ''} |")
    lines += ["", f"Backtest: {res['constrained']['start']} to {res['constrained']['end']}, annual rebalance, "
              f"{C.COST_BPS} bps one-way cost. Verdict covers the hard limits (S3, S5-S9).", "", "## Stress run (constrained portfolio)", "",
              "| Scenario | SPY | VCIT | SGOV | Return/yr | Max DD | Worst-year turnover | Verdict |", "|---|---|---|---|---|---|---|---|"]
    for s in out["stress"]:
        w = s["latest_weights"]
        lines.append(f"| {s['scenario']} | {pct(w['SPY'])} | {pct(w['VCIT'])} | {pct(w['SGOV'])} | "
                     f"{pct(s['ann_return'])} | {pct(s['max_drawdown'])} | {pct(s['max_turnover_year'])} | "
                     f"{s['verdict']}{': ' + '; '.join(s['failed_rules']) if s['failed_rules'] else (': objective not reachable' if s['verdict'] == 'MISS' else '')} |")
    lines += ["", f"## Stop condition: {out['stop']}", ""]
    lines += [f"- {r}" for r in out["stop_reasons"]] or ["- No stop rule triggered."]
    rv = out["review"]
    lines += ["", f"## Trigger check on the latest data ({rv['date']})", "",
              f"- 10-yr yield {rv['dgs10']:.2%} vs review band {rv['band'][0]:.2%} to {rv['band'][1]:.2%} "
              f"(last rebalance {rv['last_decision']} at {rv['last_dgs10']:.2%}): "
              f"{'TRIGGER FIRED' if rv['triggered'] else 'not hit'}",
              "- Current drifted mix: " + ", ".join(f"{a} {pct(rv['current_weights'][a])}" for a in C.ASSETS) +
              f" (expected return {rv['current_expected_return']:.2%})",
              "- Model if rebalanced today: " + ", ".join(f"{a} {pct(rv['review_weights'][a])}" for a in C.ASSETS) +
              f" (expected return {rv['review_expected_return']:.2%}; trade {pct(rv['trade'])})"]
    lines += ["", "## Allocation range (passing scenarios)", ""]
    lines += [f"- {a}: {pct(lo)} to {pct(hi)}" for a, (lo, hi) in out["range"].items()]
    (OUT / "results.md").write_text("\n".join(lines) + "\n")
    slim = {"as_of": last["date"], "signal": {"dgs10": last["dgs10"], "status": last["signal_status"]},
            "portfolios": {k: {x: r[x] for x in ("start", "end", "ann_return", "ann_vol", "max_drawdown",
                                                  "turnover_per_year", "max_turnover_year", "worst_12m_loss", "checks", "problems")} |
                           {"latest_weights": r["log"][-1]["weights"], "verdict": E.verdict(r)[0],
                            "decisions": r["log"]} for k, r in res.items()},
            "stress": out["stress"], "stop": out["stop"], "stop_reasons": out["stop_reasons"],
            "allocation_range": out["range"], "trigger_review": out["review"]}
    (OUT / "results.json").write_text(json.dumps(slim, indent=2))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
