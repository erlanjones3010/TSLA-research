# Validation and AI Use

**AI use:** I used Claude (Anthropic, Opus) and Codex (OpenAI) to help write the code and draft documents. I also used Codex (OpenAI) to help write my earlier Lab 14–17 code that this project builds on, and to review the code, explain how it works and fix errors when running the app. The analysis and decision are my own.

**Education, not investment advice.**

## Sources and as-of dates
| Data | Source | Coverage | As-of rule |
|---|---|---|---|
| Monthly ETF prices (SGOV, TLT, VCIT, SPY) | `data/prices.csv` from my Lab 14–15 work; Yahoo Finance historical data (finance.yahoo.com/quote/&lt;ticker&gt;/history), file saved 2026-10-22 | 2021-10-29 to 2026-09-30 | Month-end prices; a decision on date t uses returns through t only |
| 10-year Treasury yield (DGS10) | ALFRED, Federal Reserve Bank of St. Louis | 20 quarter-ends, 2021-12-31 to 2026-09-30 (the model uses the year-ends for rebalancing and 2026-09-30 for the trigger check) | Vintage on the decision date; latest observation strictly before it; stale if > 7 days |

## Definitions and transformations
- **Prices:** Yahoo Finance month-end *adjusted* closes (dividends reinvested), so SGOV's price rises as it pays interest. Yahoo revises past adjusted closes when new dividends are paid; this rescales the price history but leaves monthly returns essentially unchanged.
- **Returns:** simple monthly returns, price(t) / price(t−1) − 1. No rows were dropped, filled or cleaned; the loader stops if a price is missing, zero or out of date order.
- **Risk:** sample covariance (n − 1) of the trailing 24 monthly returns, annualized × 12; volatility is its square root.
- **Expected returns:** TLT = 10-yr yield; VCIT = yield + 1.0%; SPY = yield + 4.0%; SGOV = its trailing 12-month return (a realized rate, used as the cash yield).
- **Signal timing:** for each decision date the ALFRED vintage of that date is used and the latest observation strictly before it is kept, so later revisions cannot leak in (`build_signal_data.py` rebuilds the file).
- **Licensing and privacy:** FRED/ALFRED data is public; Yahoo Finance data is used for coursework only. No personal data or credentials are stored.

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
| test_reserve_minimum_matches_lab13_checker | Known answer: reserve minimum = 3.0%, the same value my Lab 13 `mandate.py` printed | PASS |
| test_portfolio_volatility_known_answer | Known answer: 50/50 of uncorrelated 10% and 20% volatility assets = 11.18% | PASS |
| test_no_look_ahead_in_decisions | Changing every price after a decision date does not change that decision | PASS |
| test_spy_weight_falls_as_equity_premium_rises | Monotonicity: as the equity premium rises (3%→6%), the SPY weight never rises | PASS |

Stress run result: 7 of 8 scenarios pass. With a 2% equity premium, no mix inside the limits reaches 6.5% (MISS). Stop condition = GO (it stops at 2). Trigger check: the 10-year yield on 2026-09-30 (5.26%) is above the review band set at the last rebalance (3.39%–4.89%), so the yield trigger has fired.

## Equity premium sweep (load-bearing assumption)
| Equity premium | SGOV / TLT / VCIT / SPY at last rebalance | Expected return | Backtest return/yr | Vol/yr | Verdict |
|---|---|---|---|---|---|
| 2% | 5 / 0 / 0 / 95 | 6.05% | 19.4% | 11.2% | MISS (6.5% not reachable) |
| 3% | 15 / 0 / 10 / 75 | 6.51% | 16.1% | 9.0% | PASS |
| **4% (base)** | **40 / 0 / 0 / 60** | **6.58%** | **12.5%** | **6.4%** | **PASS** |
| 5% | 45 / 0 / 10 / 45 | 6.54% | 10.2% | 4.8% | PASS |
| 6% | 60 / 0 / 0 / 40 | 6.60% | 9.3% | 4.0% | PASS |

The SPY weight moves 95% → 40% across this range, so the premium is the input that matters most. Below about 3%, the 6.5% objective cannot be reached inside the limits.

**Why 4% is the base:** A 4% equity premium is reasonable because the sweep shows that 3% is the lowest tested premium that still meets the 6.5% return objective. Using 4% provides some cushion without relying on an overly optimistic return assumption.

## Driver panel
The app exposes eight drivers inside defended bounds (`config.py`, `EXPOSED_DRIVERS`, each with its reason), lists the locked drivers fixed by the Lab 13 mandate (`LOCKED_DRIVERS`), flags any driver changed from base and has a **Reset to base** button. Checked on 2026-11-17: moving the equity premium to 5% showed "Changed from base"; Reset returned every driver to base.

## Reproducibility (cold run)
- 2026-11-17: downloaded the repository fresh from GitHub, created a new Python environment, ran `pip install -r requirements.txt`, then `python3 tests/test_engine.py` (all tests passed), `python3 run_analysis.py` (output matched `output/results.md`) and loaded the app with no errors. (Run with Claude.)
- Partner cold run: my classmate Oliana Oozbaki ran the app from the README alone, without my help. It ran; no fixes were needed.

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

*Correction: in Video 1 at 2:12 I said "Codex wrote the chart code." It was Claude; the record above is correct.*

## Locked Changed-Input Record 1
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

*The before/after table and diagnosis wording were drafted with Claude after the run; the prediction and the lesson below are my own.*

**What I learned:** Overall, I learned how the app helps make investment decisions by analyzing expected returns, risks, and portfolio constraints. It also showed me that even when an investment looks attractive, the portfolio must still meet the client's requirements, which helps the committee make more informed decisions.

## Locked Changed-Input Record 2
*(Final app. Written with AI off and committed before the run.)*

**Changed input:** Objective return, from 6.5% to 7.0% (everything else at base)

**My prediction** (commit link: https://github.com/erlanjones3010/TSLA-research/commit/ae495c91a8218b6bf89691f3b07075305e130c60, 2026-11-17 21:27 UTC):
- Weights at the last rebalance (now SGOV 40 / TLT 0 / VCIT 0 / SPY 60): SGOV 30 / TLT 0 / VCIT 0 / SPY 70
- Size: SPY increases by about 10 percentage points; expected return at the last rebalance about 6.9% (now 6.58%); backtest return about 13.0% a year (now 12.5%)
- Verdict: FAIL; stop condition: STOP
- Decision threshold: If the portfolio cannot achieve the 7.0% expected return while meeting its constraints, I would change my recommendation to reject the rebalance.
- Why: Increasing the required return should make the model favor stocks, but the portfolio may still fall short of the higher target. This shows how raising return expectations can make it harder to meet the client's requirements.

**Result after the run (objective 7.0%, all else at base; AI closed):**

| | Before (6.5%) | My prediction (7.0%) | After (7.0%) |
|---|---|---|---|
| Weights at last rebalance 2025-12-31 (SGOV / TLT / VCIT / SPY) | 40 / 0 / 0 / 60 | 30 / 0 / 0 / 70 | 25 / 0 / 5 / 70 |
| SPY change | — | about +10 points | +10 points |
| SPY at each rebalance (2023 / 2024 / 2025) | 55 / 40 / 60 | — | 70 / 55 / 70 |
| Expected return at last rebalance | 6.58% | about 6.9% | 7.02% |
| Backtest return a year | 12.5% | about 13.0% | 14.5% |
| Backtest volatility / max drawdown | 6.4% / 3.2% | — | 7.9% / 3.9% |
| Worst-year turnover | 19.2% | — | 18.5% |
| Constrained verdict | PASS | FAIL | PASS |
| Stop condition | GO | STOP | GO (1 of 8 stress scenarios MISS, same as base) |
| Decision threshold hit? | — | yes, if 7.0% not reachable | no: 7.0% is reachable inside every limit |

- Prediction vs result: the direction and size of the SPY move (+10 points to 70%) were right, and the expected and backtest returns rose as predicted (the backtest rose more than predicted). The verdict and stop condition were wrong: the portfolio still passes every hard limit and the process stays GO.
- Diagnosis: a higher return target forces the optimizer to take more risk, so it shifts weight from SGOV to SPY until the expected return reaches 7.0%. That mix still fits every Lab 13 limit: SGOV stays far above the 3% reserve, turnover stays under 25%, and the worst 12-month loss stays far below 10%. A FAIL would need a hard limit to break, and a STOP would need two stress scenarios to break or miss; neither happened. Because 7.0% is reachable, my decision threshold was not triggered, so my recommendation does not change.

*The before/after table and diagnosis wording were drafted with Claude after the run; the prediction and the lesson below are my own.*

**What I learned:** I learned that increasing the objective return makes the model allocate more to stocks, which I predicted correctly. However, I incorrectly assumed the portfolio would FAIL and STOP, when it actually met the higher return target without breaking any constraints, showing me the importance of checking the results before making a decision.

