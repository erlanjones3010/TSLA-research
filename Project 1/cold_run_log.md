# Cold-Run Log — Project 1 (Tesla, TSLA)

| Field | Entry |
|---|---|
| Date | October 6, 2026 |
| Fresh environment | New copy downloaded from GitHub (TSLA-research → Code → Download ZIP), unzipped to `~/Downloads/TSLA-research-main`. Not my working folder. |
| Python | Python 3.9.6 (`python3`) on my MacBook Air, run from the VS Code terminal |
| Recording | `cold_run_recording.mp4` in this folder (about 2 minutes, VS Code window only; compressed copy of `Screen Recording 2026-10-06 at 7.51.58 PM.mov`) |

## Commands run, one at a time (in `~/Downloads/TSLA-research-main/Project 1`)

```
python3 tesla_inputs.py
python3 proforma.py
python3 valuation.py
python3 comps.py
python3 known_answer_test.py
python3 failure_tests.py
```

## Results

| File | Result |
|---|---|
| `tesla_inputs.py` | All checks PASS (10-K totals; revenue lines sum to total; assets = liabilities + redeemable NCI + equity, FY2023–FY2025). Normalized FY2025 operating income 4,849. |
| `proforma.py` | All checks PASS (base year; balance sheet balances; cash flow ties to cash; BASE, DOWNSIDE, UPSIDE × FY2026–FY2030) |
| `valuation.py` | All checks PASS (WACC > g; value falls as WACC rises and rises with g; bridge; per-share × shares). BASE $14.93, DOWNSIDE $6.84, UPSIDE $37.49 vs. $356.09 share price. |
| `comps.py` | All checks PASS (one with a documented scope exception). P/E (GM) $28.28; EV/adjusted EBITDA (GM) $24.89. |
| `known_answer_test.py` | 18 of 18 PASS against the course training case ($27.50 per share; full sensitivity grid) |
| `failure_tests.py` | 5 of 5 PASS (negative FY2030 FCFF, g = WACC, unbalanced balance sheet, zero shares all stop with errors; normal model unchanged) |

**Outcome:** Clean end-to-end run. No errors, no missing files, no edits needed.

**Note:** The downloaded copy also contained a `__pycache__` folder uploaded by mistake. Python rebuilds these automatically, so it did not affect the run; it should be removed from the repository.
