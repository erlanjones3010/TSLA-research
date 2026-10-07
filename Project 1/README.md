# Project 1 — Tesla, Inc. (TSLA): Should the fund initiate a position?

**Results without running anything:** see [`results.txt`](results.txt) (full output of every file) and the summary below.

## Decision setup

| Item | Value |
|---|---|
| Investment user | Investment Committee of a buy-side fund with no current TSLA position |
| Decision | Initiate / watch-defer / do not initiate |
| Decision horizon | 3–5 years, reviewed every quarter as Tesla reports results |
| Target / security | Tesla, Inc. common stock (NASDAQ: TSLA) |
| Valuation date | September 1, 2026 (share price $356.09, Sep 1, 2026 close) |
| Currency / units | U.S. dollars, millions unless noted |
| Share basis | Diluted: 3,528 million FY2025 weighted-average diluted shares (FY2025 10-K) |
| Primary filing | Tesla FY2025 Form 10-K, filed Jan 29, 2026, accession 0001628280-26-003952 |
| Exclusions | Robotaxi and FSD excluded from BASE (modeled only in UPSIDE); no share buybacks or new issuance; operating leases not treated as debt; Optimus robotics not modeled in any scenario; extra dilution from future stock awards (including the CEO award) not modeled beyond FY2025 diluted shares; transaction evidence not used, because no comparable takeover of a company Tesla's size exists, so a control price could not be defended |

## Headline result (value per diluted share)

| Method | Value per share | vs. $356.09 share price |
|---|---:|---:|
| DCF — DOWNSIDE (margins stay near FY2025) | $6.84 | −$349.25 |
| DCF — BASE | **$16.54** | −$339.55 |
| EV/adjusted EBITDA (GM, single qualified peer) | $24.89 | −$331.20 |
| P/E (GM) | $28.28 | −$327.81 |
| DCF — UPSIDE (BASE + Robotaxi/FSD to $40B revenue by 2030) | $39.10 | −$316.99 |

- **Market-implied expectations:** the share price needs about **$183B of FY2030 FCFF** (model BASE: $5.3B), or about **$602B of FY2030 autonomy revenue** in the UPSIDE case (model: $40B).
- **WACC** 12.30%; **terminal growth** 3.0%; terminal value is 145.8% of BASE enterprise value because FY2026–FY2028 FCFF is negative (heavy capex).
## Committee recommendation

- **Action: Watch / defer.**
- **Valuation range: $15–$20 per share** (BASE DCF $16.54), vs. a **$356.09** share price (Sep 1, 2026). Full spread across methods: $6.84 (DOWNSIDE) to $39.10 (UPSIDE).
- **Conditions to initiate:** the price moves toward the range, or Robotaxi/FSD shows paid revenue at scale while energy storage and automotive margins keep improving.
- **Triggers to move to do not initiate:** Robotaxi/FSD delays or regulatory bans; severe free-cash-flow drain from capex.
- **Trigger to move toward initiate:** massive Megapack commercialization — energy storage deployments and energy margins growing well above my forecast (25% → 12% GWh growth; 30% → 34% margin), shown in Tesla's quarterly deployment numbers and 10-Q energy segment results.

## How to run

Requires Python 3 (tested on Python 3.9.6). No extra packages. From inside the `Project 1` folder:

```
python3 tesla_inputs.py        # FY2023–FY2025 10-K inputs and checks
python3 proforma.py            # five-year three-statement forecast (BASE, DOWNSIDE, UPSIDE)
python3 valuation.py           # WACC, FCFF DCF, bridge, sensitivity, reverse DCF, scenarios
python3 comps.py               # peer policy, P/E and EV/EBITDA
python3 known_answer_test.py   # course training-case reconciliation
python3 failure_tests.py       # highest-risk failure tests
```

Every file prints PASS/FAIL checks and stops with an error if a check fails.

## Files

| File | What it is |
|---|---|
| `tesla_inputs.py` | Sourced FY2023–FY2025 numbers (value, unit, source, page, date, type), normalization candidates, and my analyst decisions (debt 8,376; restructuring 494 added back) |
| `proforma.py` | Segment-driven forecast FY2026–FY2030 with income statement, balance sheet, cash flow, FCFF, and articulation checks; each driver has value · basis · challenge · evidence |
| `valuation.py` | WACC from sourced market inputs, FCFF DCF, enterprise-to-equity bridge, WACC × growth grid, reverse DCF, scenarios, market-implied autonomy |
| `comps.py` | Peer policy (written before peers), GM qualified, Ford excluded, P/E and EV/adjusted EBITDA with definition-consistency checks |
| `known_answer_test.py` | Runs the course training case through the same functions: 18/18 PASS ($27.50) |
| `failure_tests.py` | Breaks the model on purpose (negative FY2030 FCFF, g = WACC, unbalanced balance sheet, zero shares) and confirms it stops |
| `results.txt` | Saved output of all six files |
| `assumption_challenges.md` | Assumption-challenge record, including partner challenges (credited) |
| `locked_prediction.md` | Locked Changed-Input Record (prediction committed in `677e401` before the run) |
| `ai_use_log.md` | AI-use log: every material AI output and whether I accepted, corrected, qualified, or rejected it |
| `cold_run_log.md`, `cold_run_recording.mp4` | Clean run from a fresh GitHub download |

## Version notes

- The Locked Changed-Input Record and the first cold run were done on the earlier BASE model ($14.93 per share). I later raised the BASE energy margin (30% flat → 30%–34%), which moved BASE to $16.54. Those records stay as written; `valuation.py` now prints the same g = 3% → 5% test on the current BASE model.
