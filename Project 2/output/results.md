# Results — Riverside Community Foundation — Scholarship Endowment (fictional)

Run: 2026-11-17 03:40  |  Decision date (as of): 2026-09-30  |  10-yr yield known then: 5.26% (ok)

## Portfolios

| Portfolio | SGOV | TLT | VCIT | SPY | Return/yr | Vol/yr | Max DD | Turnover/yr | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| Equal weight (25% each) | 25.0% | 25.0% | 25.0% | 25.0% | 5.7% | 5.7% | 3.1% | 5.9% | FAIL: SPY between 30% and 70% |
| 60/40 benchmark (SPY/VCIT) | 0.0% | 0.0% | 40.0% | 60.0% | 13.3% | 8.1% | 3.9% | 5.6% | FAIL: SGOV at least 5%; Ex-ante volatility at most 12% (worst decision) |
| Constrained portfolio (signal + limits) | 5.0% | 0.0% | 25.0% | 70.0% | 14.5% | 8.3% | 4.7% | 16.5% | PASS |

Backtest: 2023-12-29 to 2026-09-30, quarterly rebalance, 10 bps one-way cost.

## Stress run (constrained portfolio)

| Scenario | SPY | VCIT | SGOV | Return/yr | Max DD | Turnover/yr | Verdict |
|---|---|---|---|---|---|---|---|
| Base case | 70.0% | 25.0% | 5.0% | 14.5% | 4.7% | 16.5% | PASS |
| Estimates: equity premium 2% (not 4%) | 70.0% | 25.0% | 5.0% | 14.5% | 4.7% | 16.5% | PASS |
| Estimates: credit spread 0.5% (not 1%) | 70.0% | 25.0% | 5.0% | 14.2% | 5.1% | 15.9% | PASS |
| Window: 12 months (not 24) | 70.0% | 25.0% | 5.0% | 16.0% | 4.9% | 34.2% | FAIL: Turnover at most 25% a year |
| Window: 36 months (not 24) | 70.0% | 25.0% | 5.0% | 12.6% | 4.6% | 17.1% | PASS |
| Costs: 50 bps (not 10) | 70.0% | 25.0% | 5.0% | 14.3% | 4.7% | 16.5% | PASS |
| Constraint: SPY at most 50% (not 70%) | 50.0% | 45.0% | 5.0% | 12.0% | 3.3% | 21.9% | PASS |
| Constraint: volatility at most 8% (not 12%) | 55.0% | 40.0% | 5.0% | 11.4% | 4.1% | 37.6% | FAIL: Turnover at most 25% a year |

## Stop condition: STOP

- 2 stress scenarios break a hard limit (stop at 2)

## Allocation range (passing scenarios)

- SGOV: 5.0% to 5.0%
- TLT: 0.0% to 0.0%
- VCIT: 25.0% to 45.0%
- SPY: 50.0% to 70.0%
