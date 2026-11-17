# Validation and AI Use

**AI use:** I used Claude (Anthropic, Opus) and Codex (OpenAI) to help write the code and draft documents. I also used Codex (OpenAI) to help write my earlier Lab 14–17 code that this project builds on, and to review the code, explain how it works and fix errors when running the app. The analysis and decision are my own.

**Education, not investment advice.**

## Sources and as-of dates
| Data | Source | Coverage | As-of rule |
|---|---|---|---|
| Monthly ETF prices (SGOV, TLT, VCIT, SPY) | `data/prices.csv` from my Lab 14–15 work; Yahoo Finance historical data (finance.yahoo.com/quote/&lt;ticker&gt;/history), file saved 2026-10-22 | 2021-10-29 to 2026-09-30 | Month-end prices; a decision on date t uses returns through t only |
| 10-year Treasury yield (DGS10) | ALFRED, Federal Reserve Bank of St. Louis | 20 quarter-ends, 2021-12-31 to 2026-09-30 | Vintage on the decision date; latest observation strictly before it; stale if > 7 days |

## Tests (`python tests/test_engine.py`)
| Test | What it checks | Result |
|---|---|---|
| test_signal_is_point_in_time | Every yield observation is dated before its decision date | PASS |
| test_signal_not_stale | No yield is more than 7 days old | PASS |
| test_covariance_is_symmetric | Risk matrix is symmetric (the Lab 14 correlation matrix was not) | PASS |
| test_constrained_meets_static_limits_every_quarter | Weights sum to 100%, SPY/SGOV limits and vol cap met at every decision | PASS |
| test_baselines_fail_for_the_named_rule | Equal weight fails SPY minimum; 60/40 fails SGOV minimum | PASS |
| test_infeasible_limits_are_reported | An impossible 1% vol cap is flagged, not hidden | PASS |
| test_higher_costs_lower_return | Higher trading costs lower the return | PASS |

Stress run result: 6 of 8 scenarios pass; stop condition = STOP (turnover breaks with a 12-month window and with an 8% vol cap).

## Limitations
- Short backtest (11 quarters, 2023-12 to 2026-09) in a strong stock market; it does not include a large drawdown.
- Expected returns are building blocks (yield + assumed premium); a 2% equity premium gave the same weights, so the result is driven more by the limits than by the signal.
- Four ETFs only; no taxes; costs are a flat estimate.
- CPI is assumed at 2.5%, not measured.

## AI tools used
| Tool | Model / version | Date | Used for | How I checked it |
|---|---|---|---|---|
| Claude (Cowork) | claude-opus-5-5 | 2026-11 | Code for app, engine and tests; downloading ALFRED data; document drafts | I checked Claude’s work by running the app and testing it on my Mac. I found an error with the `width` setting, fixed it, and checked the results in the app to make sure everything worked correctly. |
| Codex | OpenAI Codex CLI v0.169.0 | Oct–Nov 2026 | Lab 14–17 code this project builds on; reviewing code; explaining code; fixing errors when running the app | I checked Codex’s work by running the code and comparing the results with the expected answers. I also reviewed the code to make sure the calculations were correct and fixed any errors I found. |

**One AI output I checked:** One AI output I checked was the portfolio allocation from my app. I tested it by changing the equity risk premium to 5% and checking the results. The weights stayed the same, which helped me confirm that the portfolio was still following its investment limits.

## Locked Changed-Input Record
**Changed input:** Equity risk premium, from 4.0% to 5.0% (everything else at default)

**My prediction, written with AI off and committed before the run** (commit link: https://github.com/erlanjones3010/TSLA-research/commit/56d5d72c3b610471488f532be63b1d468a20a88f, 2026-11-17):
- Constrained weights at the latest date: SGOV 5% / TLT 0% / VCIT 15% / SPY 80%
- Return a year: higher
- Constrained verdict: PASS
- Stop condition: GO
- Why: I increased SPY to 80% because I want more exposure to stocks and their potential for higher long-term returns. I took the extra 10% from VCIT because I would rather invest more in stocks than corporate bonds.

**Result after the run (equity premium 5.0%, all else default):**
- Constrained weights at the latest date: SGOV 5% / TLT 0% / VCIT 25% / SPY 70% (unchanged from the 4% base case; all 12 quarterly decisions identical)
- Return a year: 14.5% (unchanged)
- Constrained verdict: PASS
- Stop condition: STOP (2 of 8 stress scenarios break the 25% turnover limit; unrelated to the premium)
- Prediction vs result: weights, return and stop condition were wrong; the verdict was right. SPY stayed at 70% because 70% is the mandate's hard maximum, so an 80% SPY weight would have failed the mandate.

**What I learned:** I learned that even though I predicted SPY would increase to 80%, the portfolio rules only allow 70%. Changing the equity premium did not change the weights, which showed me that the portfolio limits have more control over the results than I originally thought.
