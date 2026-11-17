# Validation and AI Use

**AI use:** I used Claude (Anthropic, Opus) and Codex (OpenAI) to help write the code and draft documents. I also used Codex (OpenAI) to help write my earlier Lab 14–17 code that this project builds on, and to review the code, explain how it works and fix errors when running the app. The analysis and decision are my own.

**Education, not investment advice.**

## Sources and as-of dates
| Data | Source | Coverage | As-of rule |
|---|---|---|---|
| Monthly ETF prices (SGOV, TLT, VCIT, SPY) | `data/prices.csv` from my Lab 14–15 work; Yahoo Finance historical data (finance.yahoo.com/quote/&lt;ticker&gt;/history), file saved 2026-10-22 | 2021-10-29 to 2026-09-30 | Month-end prices; a decision on date t uses returns through t only |
| 10-year Treasury yield (DGS10) | ALFRED, Federal Reserve Bank of St. Louis | 20 quarter-ends, 2021-12-31 to 2026-09-30 (the model uses the year-ends for rebalancing and 2026-09-30 for the trigger check) | Vintage on the decision date; latest observation strictly before it; stale if > 7 days |

## Mandate source
The mandate is the Meridian mandate from Lab 13 (statements S1–S10). Each rule in `config.py` and the app is tagged with its statement. S10 (no optimization goal) is answered as in Lab 14: the lowest-volatility mix that meets every limit and still reaches the 6.5% objective. S9 (the 10% loss limit Lab 13 flagged as unverifiable) is measured here as the worst rolling 12-month loss.

## Tests (`python tests/test_engine.py`)
| Test | What it checks | Result |
|---|---|---|
| test_signal_is_point_in_time | Every yield observation is dated before its decision date | PASS |
| test_signal_not_stale | No yield is more than 7 days old | PASS |
| test_covariance_is_symmetric | Risk matrix is symmetric (the Lab 14 correlation matrix was not) | PASS |
| test_constrained_meets_limits_and_objective_every_decision | At every rebalance: reserve, long-only, issuer and liquidity limits met, turnover ≤ 25%, expected return ≥ 6.5% | PASS |
| test_benchmark_fails_reserve_rule | The 60/40 benchmark holds no SGOV or TLT and fails S3 | PASS |
| test_checker_catches_a_short_position | A −5% SGOV weight is caught by the S5 long-only rule | PASS |
| test_unreachable_objective_is_reported | An impossible 20% objective is flagged, not hidden | PASS |
| test_higher_costs_lower_return | Higher trading costs lower the return | PASS |

Stress run result: 7 of 8 scenarios pass. With a 2% equity premium, no mix inside the limits reaches 6.5% (MISS). Stop condition = GO (it stops at 2). Trigger check: the 10-year yield on 2026-09-30 (5.26%) is above the review band set at the last rebalance (3.39%–4.89%), so the yield trigger has fired.

## Limitations
- Short backtest: 2023-12 to 2026-09 with three annual rebalances, in a strong stock market; the 10% loss limit was never tested.
- SPY stands in for global equity in the benchmark.
- Expected returns are building blocks (yield + assumed premium or spread), not estimates.
- Four ETFs only; no taxes; costs are a flat estimate; CPI is assumed at 2.5%, not measured.

## AI tools used
| Tool | Model / version | Date | Used for | How I checked it |
|---|---|---|---|---|
| Claude (Cowork) | claude-opus-5-5 | 2026-11 | Code for app, engine and tests; downloading ALFRED data; document drafts | I checked Claude’s work by running the app and testing it on my Mac. I found an error with the `width` setting, fixed it, and checked the results in the app to make sure everything worked correctly. |
| Codex | OpenAI Codex CLI v0.169.0 | Oct–Nov 2026 | Lab 14–17 code this project builds on; reviewing code; explaining code; fixing errors when running the app | I checked Codex’s work by running the code and comparing the results with the expected answers. I also reviewed the code to make sure the calculations were correct and fixed any errors I found. |

**One AI output I checked:** Claude wrote the app's chart code using a `width="stretch"` setting. When I ran the app on my Mac, it crashed with `TypeError: altair_chart() got an unexpected keyword argument 'width'`, because my installed Streamlit version does not support that setting. **Corrected:** the code was changed back to `use_container_width=True`, which works in both older and newer Streamlit versions, and I restarted the app and confirmed every tab loaded without errors. I did not accept the AI code until it ran on my own machine.

## Locked Changed-Input Record
*(For the final Lab 13 version of the app. Written with AI off and committed before the run.)*

**Changed input:** Equity risk premium, from 4.0% to 5.0% (everything else at default)

**Reason for the test:** To test how a higher expected equity return affects portfolio allocation and whether the portfolio increases its stock exposure.

**My prediction** (commit link: https://github.com/erlanjones3010/TSLA-research/commit/d4e172f8d846ecbb2decb271a9f3da2716b5c1db, 2026-11-17 15:12 UTC):
- Constrained weights at the last rebalance: SGOV 30% / TLT 0% / VCIT 0% / SPY 70%
- Return a year: higher
- Constrained verdict: PASS
- Stop condition: GO
- Why: Increasing the equity premium to 5% should make stocks more attractive, causing the portfolio to increase its SPY allocation. I predict a higher expected return while remaining within the portfolio constraints.

**Result after the run (equity premium 5.0%, all else default; AI closed):**

| | Before (4%) | After (5%) |
|---|---|---|
| Weights at last rebalance 2025-12-31 (SGOV / TLT / VCIT / SPY) | 40 / 0 / 0 / 60 | 45 / 0 / 10 / 45 |
| SPY at each rebalance (2023 / 2024 / 2025) | 55 / 40 / 60 | 40 / 30 / 45 |
| Expected return at last rebalance | 6.58% | 6.54% |
| Backtest return a year | 12.5% | 10.2% |
| Backtest volatility / max drawdown | 6.4% / 3.2% | 4.9% / 2.4% |
| Constrained verdict | PASS | PASS |
| Stop condition | GO | GO |

- Prediction vs result: verdict (PASS) and stop condition (GO) were right; the weights and return were wrong in direction. SPY fell from 60% to 45% instead of rising to 70%, and the backtest return fell instead of rising.
- Diagnosis: the optimizer takes the lowest-volatility mix that still reaches the 6.5% objective (Lab 13 S10, answered as in Lab 14). A higher equity premium raises SPY's expected return, so less SPY is needed to reach 6.5%, and the model shifts weight to lower-risk SGOV and VCIT. The backtest return fell because SPY was the best performer over 2023–2026 and the portfolio held less of it.

**What I learned:** Overall, I learned how the app helps make investment decisions by analyzing expected returns, risks, and portfolio constraints. It also showed me that even when an investment looks attractive, the portfolio must still meet the client's requirements, which helps the committee make more informed decisions.

### Earlier record (superseded)
This record was made on an earlier version of the app that used my own Riverside mandate instead of the Lab 13 mandate. I kept it as history; the record above is the one for the final app.

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
