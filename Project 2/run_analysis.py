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
LABELS = {"equal": "Equal weight (25% each)", "benchmark": "60/40 benchmark (SPY/VCIT)",
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
             "## Portfolios", "",
             "| Portfolio | SGOV | TLT | VCIT | SPY | Return/yr | Vol/yr | Max DD | Turnover/yr | Verdict |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for k, r in res.items():
        w = r["log"][-1]["weights"]
        v, fails = E.verdict(r)
        lines.append(f"| {LABELS[k]} | " + " | ".join(pct(w[a]) for a in C.ASSETS) +
                     f" | {pct(r['ann_return'])} | {pct(r['ann_vol'])} | {pct(r['max_drawdown'])} | "
                     f"{pct(r['turnover_per_year'])} | {v}{': ' + '; '.join(fails) if fails else ''} |")
    lines += ["", f"Backtest: {res['constrained']['start']} to {res['constrained']['end']}, quarterly rebalance, "
              f"{C.COST_BPS} bps one-way cost.", "", "## Stress run (constrained portfolio)", "",
              "| Scenario | SPY | VCIT | SGOV | Return/yr | Max DD | Turnover/yr | Verdict |", "|---|---|---|---|---|---|---|---|"]
    for s in out["stress"]:
        w = s["latest_weights"]
        lines.append(f"| {s['scenario']} | {pct(w['SPY'])} | {pct(w['VCIT'])} | {pct(w['SGOV'])} | "
                     f"{pct(s['ann_return'])} | {pct(s['max_drawdown'])} | {pct(s['turnover_per_year'])} | "
                     f"{s['verdict']}{': ' + '; '.join(s['failed_rules']) if s['failed_rules'] else ''} |")
    lines += ["", f"## Stop condition: {out['stop']}", ""]
    lines += [f"- {r}" for r in out["stop_reasons"]] or ["- No stop rule triggered."]
    lines += ["", "## Allocation range (passing scenarios)", ""]
    lines += [f"- {a}: {pct(lo)} to {pct(hi)}" for a, (lo, hi) in out["range"].items()]
    (OUT / "results.md").write_text("\n".join(lines) + "\n")
    slim = {"as_of": last["date"], "signal": {"dgs10": last["dgs10"], "status": last["signal_status"]},
            "portfolios": {k: {x: r[x] for x in ("start", "end", "ann_return", "ann_vol", "max_drawdown",
                                                  "turnover_per_year", "checks", "problems")} |
                           {"latest_weights": r["log"][-1]["weights"], "verdict": E.verdict(r)[0],
                            "decisions": r["log"]} for k, r in res.items()},
            "stress": out["stress"], "stop": out["stop"], "stop_reasons": out["stop_reasons"],
            "allocation_range": out["range"]}
    (OUT / "results.json").write_text(json.dumps(slim, indent=2))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
