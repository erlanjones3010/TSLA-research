# Results — Meridian Endowment (course client from Lab 13)

Run: 2026-11-17 15:01  |  Decision date (as of): 2025-12-31  |  10-yr yield known then: 4.14% (ok)

Inputs: objective 6.5% (CPI 2.5% + 4%), equity premium 4.0%, credit spread 1.0%, window 24 months, cost 10 bps, annual rebalance; limits: reserve-eligible >= 3%, issuer <= 8%, turnover <= 25%/yr, liquidity >= 90% in 5 days, 12-month loss <= 10%, long-only

## Portfolios

| Portfolio | SGOV | TLT | VCIT | SPY | Expected return | Return/yr | Vol/yr | Max DD | Worst-year turnover | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| Equal weight (25% each) | 25.0% | 25.0% | 25.0% | 25.0% | 5.42% | 5.8% | 5.7% | 3.1% | 4.4% | PASS |
| 60/40 benchmark (SPY/VCIT, S4) | 0.0% | 0.0% | 40.0% | 60.0% | 6.94% | 13.4% | 8.1% | 3.9% | 4.5% | FAIL: S3 Reserve-eligible (SGOV+TLT) at least 3% (every decision) |
| Constrained portfolio (signal + limits) | 40.0% | 0.0% | 0.0% | 60.0% | 6.58% | 12.5% | 6.4% | 3.2% | 19.2% | PASS |

Backtest: 2023-12-29 to 2026-09-30, annual rebalance, 10 bps one-way cost. Verdict covers the hard limits (S3, S5-S9).

## Stress run (constrained portfolio)

| Scenario | SPY | VCIT | SGOV | Return/yr | Max DD | Worst-year turnover | Verdict |
|---|---|---|---|---|---|---|---|
| Base case | 60.0% | 0.0% | 40.0% | 12.5% | 3.2% | 19.2% | PASS |
| Estimates: equity premium 2% (not 4%) | 95.0% | 0.0% | 5.0% | 19.4% | 7.2% | 0.8% | MISS: objective not reachable |
| Estimates: credit spread 0.5% (not 1%) | 60.0% | 0.0% | 40.0% | 12.5% | 3.2% | 19.2% | PASS |
| Window: 12 months (not 24) | 55.0% | 15.0% | 30.0% | 13.9% | 7.6% | 25.0% | PASS |
| Window: 36 months (not 24) | 60.0% | 0.0% | 40.0% | 10.5% | 3.2% | 17.0% | PASS |
| Costs: 50 bps (not 10) | 60.0% | 0.0% | 40.0% | 12.4% | 3.2% | 19.2% | PASS |
| Constraint: reserve at least 15% (not 3%) | 60.0% | 0.0% | 40.0% | 12.5% | 3.2% | 19.2% | PASS |
| Constraint: 12-month loss at most 5% (not 10%) | 60.0% | 0.0% | 40.0% | 12.5% | 3.2% | 19.2% | PASS |

## Stop condition: GO

- No stop rule triggered.

## Trigger check on the latest data (2026-09-30)

- 10-yr yield 5.26% vs review band 3.39% to 4.89% (last rebalance 2025-12-31 at 4.14%): TRIGGER FIRED
- Current drifted mix: SGOV 37.8%, TLT 0.0%, VCIT 0.0%, SPY 62.2% (expected return 7.17%)
- Model if rebalanced today: SGOV 35.0%, TLT 0.0%, VCIT 25.0%, SPY 40.0% (expected return 6.58%; trade 25.0%)

## Allocation range (passing scenarios)

- SGOV: 30.0% to 40.0%
- TLT: 0.0% to 0.0%
- VCIT: 0.0% to 15.0%
- SPY: 55.0% to 60.0%
