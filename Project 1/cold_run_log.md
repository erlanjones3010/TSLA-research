# Cold-Run Log — Project 1 (Tesla, TSLA)

## Final cold run (current model)

| Field | Entry |
|---|---|
| Date | October 6, 2026, about 9:08 PM |
| Fresh environment | New copy downloaded from GitHub (TSLA-research → Code → Download ZIP), unzipped to `~/Downloads/TSLA-research-main`. `pwd` at the start of the recording shows `/Users/erlanjones/Downloads/TSLA-research-main/Project 1`. |
| Python | Python 3.9.6 (`python3`) on my MacBook Air, run by me in the VS Code terminal (not by an AI agent) |
| Recording | `cold_run_recording.mp4` in this folder (about 80 seconds, VS Code window only; compressed copy of `Screen Recording 2026-10-06 at 9.08.24 PM.mov`) |

### Commands run, one at a time

```
pwd
python3 tesla_inputs.py
python3 proforma.py
python3 valuation.py
python3 comps.py
python3 known_answer_test.py
python3 failure_tests.py
```

### Results

| File | Result |
|---|---|
| `tesla_inputs.py` | All checks PASS (10-K totals; revenue lines sum to total; assets = liabilities + redeemable NCI + equity, FY2023–FY2025) |
| `proforma.py` | All checks PASS (base year; balance sheet balances; cash flow ties to cash; BASE, DOWNSIDE, UPSIDE × FY2026–FY2030) |
| `valuation.py` | All checks PASS. BASE **$16.54**, DOWNSIDE **$6.84**, UPSIDE **$39.10** vs. $356.09 share price |
| `comps.py` | All checks PASS (one with a documented scope exception). P/E (GM) $28.28; EV/adjusted EBITDA (GM) $24.89 |
| `known_answer_test.py` | 18 of 18 PASS against the course training case ($27.50 per share; full sensitivity grid) |
| `failure_tests.py` | 5 of 5 PASS (negative FY2030 FCFF, g = WACC, unbalanced balance sheet, zero shares all stop; normal model = BASE $16.54, DOWNSIDE $6.84, UPSIDE $39.10) |

**Outcome:** Clean end-to-end run of the final model from a fresh download. No errors, no missing files, no edits needed.

## Earlier cold run (superseded)

On October 6, 2026 at about 7:52 PM I did a first cold run on the earlier model (BASE $14.93, UPSIDE $37.49), before I raised the BASE energy margin. All checks passed. That recording was replaced in this folder by the final one above.
