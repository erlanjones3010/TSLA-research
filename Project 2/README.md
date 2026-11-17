# Riverside Community Foundation — Investment Management App (FIN 43900 Project 2)

**AI use:** I used Claude (Anthropic, Opus) to help write the Python code, tests and document drafts. *[Add any other AI tool and what you used it for.]* The mandate choices, the analysis, the checks I ran and the committee decision are my own.

**Education, not investment advice.** The client is fictional.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Optional: `python run_analysis.py` (writes `output/results.md` and `output/results.json`) and `python tests/test_engine.py` (runs the tests). No API key is needed; the data files are in `data/`.

## What it does

A $25 million scholarship endowment must earn CPI + 3.5% a year while paying out 4%. The app:

1. States the mandate: objective, universe (SGOV, TLT, VCIT, SPY), 60/40 benchmark, risk measure, hard limits (`config.py`).
2. Builds three portfolios each quarter: **equal weight**, the **60/40 benchmark**, and a **constrained portfolio** that maximizes expected return inside every limit. Each gets a PASS/FAIL verdict and the rule it broke.
3. Uses one point-in-time signal: the **10-year Treasury yield as known on each decision date** (ALFRED vintages, data card in the app).
4. Stress-tests estimates, window, costs and constraints, and applies a **stop condition**.
5. Shows the supported allocation range and monitoring triggers, and saves a run record.

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
| `docs/decision-memo.md` | Committee decision |
| `docs/validation-and-ai-use.md` | Sources, tests, limitations, AI use, Locked Changed-Input Record |
