# Meridian Endowment — Investment Management App (FIN 43900 Project 2)

**AI use:** I used Claude (Anthropic, Opus) and Codex (OpenAI) to help write the code and draft documents. I also used Codex (OpenAI) to help write my earlier Lab 14–17 code that this project builds on, and to review the code, explain how it works and fix errors when running the app. The analysis and the decision below are my own.

**Education, not investment advice.** Meridian is the course client from Lab 13.

## Finance decision and intended user

**Intended user:** the investment committee of the Meridian endowment (the Lab 13 client), advised by a portfolio analyst.

**Decision:** adopt, allocate to, rebalance, pilot or reject the proposed constrained allocation across SGOV, TLT, VCIT and SPY under the Lab 13 mandate in `config.py` (7-year horizon, annual rebalancing). The recommendation is in `docs/decision-memo.md`.

## Run it

The app is in the `Project 2` folder of this repo. Clone or download the repo, then:

```bash
cd "Project 2"
pip install -r requirements.txt
streamlit run app.py
```

Optional: `python3 run_analysis.py` (writes `output/results.md` and `output/results.json`) and `python3 tests/test_engine.py` (runs the 12 tests). No API key or credentials are needed; the data files are in `data/`. Tested with Python 3.9 and 3.10.

## What it does

The Meridian endowment ($100 million, $0.75 million paid out each quarter) must earn CPI + 4% a year (6.5% nominal) under the mandate from Lab 13. The app:

1. States the mandate, with each rule tagged to its Lab 13 statement (S1–S10): objective, universe (SGOV, TLT, VCIT, SPY), 60/40 benchmark, risk measure (ex-ante volatility) and hard limits: reserve-eligible ≥ 3%, long-only, issuer ≤ 8%, turnover ≤ 25% a year, ≥ 90% redeemable in 5 days, 12-month loss ≤ 10% (`config.py`).
2. Builds three portfolios at each annual rebalance: **equal weight**, the **60/40 benchmark**, and a **constrained portfolio**, which is the lowest-volatility mix that meets every limit and still reaches 6.5% (Lab 13's open question S10, answered as in Lab 14). Each gets a PASS/FAIL verdict and the rule it broke.
3. Uses one point-in-time signal: the **10-year Treasury yield as known on each decision date** (ALFRED vintages, data card in the app).
4. Stress-tests estimates, window, costs and constraints, and applies a **stop condition**.
5. Shows the supported allocation range and monitoring triggers, checks whether a trigger has fired on the latest data, and saves a run record.
6. Gives the committee a **driver panel**: eight exposed drivers (estimates, objective and three hard limits) that move only inside defended bounds (hover ⓘ for the reason), a list of locked drivers fixed by the Lab 13 mandate, a "Changed from base" flag and a **Reset to base** button. The bounds and reasons live in `config.py`.
7. Sweeps the load-bearing assumption, the equity premium (2% to 6%), and shows how the portfolio moves.

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit app |
| `engine.py` | Data, signal, portfolios, mandate checks, backtest, stress run |
| `config.py` | Mandate and settings |
| `run_analysis.py` | Same analysis without the app; writes `output/` |
| `build_signal_data.py` | Rebuilds `data/dgs10_asof.csv` from ALFRED (needs internet) |
| `data/` | `prices.csv` (monthly ETF prices), `dgs10_asof.csv` (point-in-time yield) |
| `tests/test_engine.py` | Tests |
| `output/` | Executed results: `results.md` (readable) and `results.json` (every number) |
| `docs/decision-memo.md` | Committee decision |
| `docs/validation-and-ai-use.md` | Sources, tests, limitations, AI use, Locked Changed-Input Record |

## Data sources

| Data | Source | As of |
|---|---|---|
| Monthly prices for SGOV, TLT, VCIT, SPY (`data/prices.csv`) | Yahoo Finance historical data | 2021-10-29 to 2026-09-30 (file saved 2026-10-22) |
| 10-year Treasury yield, point in time (`data/dgs10_asof.csv`) | ALFRED (St. Louis Fed), series DGS10 | Vintage on each quarter-end, 2021-12-31 to 2026-09-30; the model uses the year-ends for rebalancing and 2026-09-30 for the trigger check |

Each decision uses only data known on that date. Full details: `docs/validation-and-ai-use.md`.

## Executed output

`output/results.md` and `output/results.json` show the inputs, the last rebalance date (2025-12-31), all three portfolios with verdicts, the stress run, the stop condition and the trigger check on the latest data (2026-09-30). The app's Output tab shows the same run record.

## Known limitations

- Short backtest: 2023-12 to 2026-09 with three annual rebalances, in a strong stock market with no large loss, so the 10% loss limit was never tested.
- SPY stands in for global equity in the benchmark; the universe has no global equity ETF.
- Expected returns are building blocks (yield plus an assumed premium or spread), not estimates; with a 2% equity premium no mix inside the limits reaches 6.5%.
- Four ETFs only; no taxes; trading costs are a flat estimate; CPI is assumed at 2.5%.
- S9's loss limit is measured as the worst rolling 12-month loss; Lab 13 flagged that the CIO never defined it.
