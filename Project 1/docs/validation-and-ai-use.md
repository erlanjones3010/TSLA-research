# Validation and AI-Use Record — Project 1 (Tesla, TSLA)

**Analyst:** Erlan Jones · FIN 43900 · Valuation date September 1, 2026
**Repository:** https://github.com/erlanjones3010/TSLA-research (folder `Project 1`)
**Named AI tools used:** Codex (OpenAI), Claude (Anthropic). Speech-to-text: faster-whisper.

This is the single working validation and AI-use record for Project 1. It combines `locked_prediction.md`, the test output in `results.txt`, `cold_run_log.md`, `assumption_challenges.md`, and `ai_use_log.md` without changing their content. The submitted `Validation-and-AI-Use.pdf` matches this file.

## Contents

1. Validation summary
2. Locked Changed-Input Record
3. Known-answer test
4. Failure tests (highest-risk claim)
5. Cold run
6. Assumption challenges
7. AI-use log

## 1. Validation summary

| Check | What I did | Result |
|---|---|---|
| Known-answer test | Course training case run through the same DCF code | 18/18 PASS ($27.50) |
| Statement checks | Balance sheet balances and cash ties out, every year, all 3 scenarios | All PASS |
| Locked Changed-Input Record | AI-off prediction committed (`677e401`) before raising terminal growth 3% → 5% | Direction right, size wrong; decision unchanged |
| Failure tests | Negative FY2030 FCFF (highest-risk claim), g = WACC, unbalanced balance sheet, zero shares | Model stopped every time (5/5 PASS) |
| Cold run | Fresh GitHub download, every file run on video | All files ran, all checks PASS |
| AI-output checks | Every material AI output logged with my decision and evidence | 13 entries; errors caught in Entries 1, 2, 4, 8 |

**Highest-risk claim:** the BASE value of $16.54 depends on the terminal value, which is only valid if FY2030 free cash flow is positive. The DOWNSIDE case is only about $1.0B in FY2030, so the model must refuse to value a negative final year. The failure test confirms it does.

**Known limitations:** one qualified peer (GM, automotive-only scope vs. Tesla consolidated); beta viewed Oct 6, 2026 rather than Sep 1; FY2025 balance-sheet values in the bridge against a Sep 1, 2026 price, with no stub-period adjustment; the Locked Changed-Input Record and first cold run were run on the earlier BASE model ($14.93), before the energy-margin revision moved BASE to $16.54.

## 2. Locked Changed-Input Record

### Locked Changed-Input Record — Project 1 (Tesla)

#### Part 1 — Prediction

_Written by me, with AI off for the answers, before running the change. Guiding questions came from Claude; the answers are my own, copied word for word. Committed to GitHub in `677e401` before the run._

| Field | Entry |
|---|---|
| Date / time written | October 6, 2026, 6:30 PM |
| Input changed | Terminal growth rate (g), BASE scenario, `valuation.py` |
| Old value (with units) | 3.0% per year |
| New value (with units) | 5.0% per year |
| File and line where it is changed | `Project 1/valuation.py`, terminal growth input |
| My predicted direction for value per share (up / down / no change) | If Tesla's cash flows keep growing, the company would be worth more but it depends on inflation in the economy. |
| My predicted size (rough) | It would not move a lot because it is all focused on future earnings and as time keeps going the value per share would move a lot more than what it is today. |
| Why I expect this (my own reasoning) | Terminal growth is the rate at which a company's free cash flows grows forever after it becomes mature. |
| Would this change the committee decision? (my prediction) | Yes it does close the gap to the $356 per share. This is because the way Tesla is growing especially in other areas that aren't automobiles such as energy generation and storage. |

#### Part 2 — Result (After Running)

_Factual lines (values, direction, commit) filled in by Claude from the run output; the assessment and diagnosis are my own words. This run used the earlier BASE model ($14.93); see README version notes._


### I ran this on October 6th

| Field | Entry |
|---|---|
| GitHub commit of Part 1 (link or ID) | `677e401` ([commit link](https://github.com/erlanjones3010/TSLA-research/commit/677e40104106439a74cb7c1aa13ddeebb7d8387b)) |
| Old value per share | $14.93 (BASE, g = 3.0%); enterprise value $16,696.7M; terminal value 167.8% of EV |
| New value per share | $17.30 (BASE, g = 5.0%); enterprise value $25,061.9M; terminal value 145.2% of EV |
| Actual direction | Up: +$2.37 per share (+15.9%) |
| Did it match my prediction? | Direction: yes (predicted worth more; value went up). Size: no. My guess was wrong because it went up an extra 15.9% which was way off from what I said "it won't move a lot." Decision: no, I predicted it would change my recommendation, but it did not (see Decision effect). |
| Decision effect | Gap to the $356.09 share price went from −$341.16 to −$338.79. No, it did not change my recommendation (watch / defer) because even though it went up around $2 it still is far too expensive based on the model. |
| If wrong: why (diagnosis). If no change: why | I thought it would not move a lot, but it did because most of Tesla's value in my model comes from the terminal value. It did not change my recommendation because the gap between my value and the $356 price is so large that a $2 change is not worth it. |


## 3. Known-answer test

Output of `python3 known_answer_test.py` (columns: item | expected | actual | result):

```
Sum of PV of FCFF | 448.44 | 448.44 | PASS
Terminal value (Year 5) | 1894.65 | 1894.65 | PASS
PV of terminal value | 1176.43 | 1176.43 | PASS
Enterprise value | 1624.87 | 1624.87 | PASS
Terminal value share of EV | 72.4% | 72.4% | PASS
Equity value | 1374.87 | 1374.87 | PASS
Value per share | 27.50 | 27.50 | PASS
WACC 11% value per share | 23.41 | 23.41 | PASS
Sensitivity WACC 9%, g 2% | 28.60 | 28.60 | PASS
Sensitivity WACC 9%, g 3% | 32.94 | 32.94 | PASS
Sensitivity WACC 9%, g 4% | 39.02 | 39.02 | PASS
Sensitivity WACC 10%, g 2% | 24.36 | 24.36 | PASS
Sensitivity WACC 10%, g 3% | 27.50 | 27.50 | PASS
Sensitivity WACC 10%, g 4% | 31.69 | 31.69 | PASS
Sensitivity WACC 11%, g 2% | 21.06 | 21.06 | PASS
Sensitivity WACC 11%, g 3% | 23.41 | 23.41 | PASS
Sensitivity WACC 11%, g 4% | 26.44 | 26.44 | PASS
Reverse DCF FCFF shift | 0.00 | -0.00 | PASS
```

## 4. Failure tests (highest-risk claim)

Output of `python3 failure_tests.py`:

```
negative final-year FCFF | DOWNSIDE FY2030 FCFF set to -500 in memory | expected: stop with error | actual: ValueError: FY2030 FCFF must be positive before a terminal value is calculated. | PASS
terminal growth equals WACC | terminal growth set equal to WACC in memory | expected: stop with error | actual: ValueError: WACC must be greater than terminal growth. | PASS
unbalanced balance sheet | FY2027 cash increased by 1,000 with no matching entry in memory | expected: stop with error | actual: ValueError: Forecast checks failed: FY2027E balance sheet balances | PASS
zero diluted shares | diluted shares set to 0 in memory | expected: stop with error | actual: ValueError: Diluted shares must be positive. | PASS
normal model | no changes | expected: BASE $16.54, DOWNSIDE $6.84, UPSIDE $39.10 | actual: BASE $16.54, DOWNSIDE $6.84, UPSIDE $39.10 | PASS
```

## 5. Cold run

### Cold-Run Log — Project 1 (Tesla, TSLA)

#### Final cold run (current model)

| Field | Entry |
|---|---|
| Date | October 6, 2026, about 9:08 PM |
| Fresh environment | New copy downloaded from GitHub (TSLA-research → Code → Download ZIP), unzipped to `~/Downloads/TSLA-research-main`. `pwd` at the start of the recording shows `/Users/erlanjones/Downloads/TSLA-research-main/Project 1`. |
| Python | Python 3.9.6 (`python3`) on my MacBook Air, run by me in the VS Code terminal (not by an AI agent) |
| Recording | `cold_run_recording.mp4` in this folder (about 80 seconds, VS Code window only; compressed copy of `Screen Recording 2026-10-06 at 9.08.24 PM.mov`) |

##### Commands run, one at a time

```
pwd
python3 tesla_inputs.py
python3 proforma.py
python3 valuation.py
python3 comps.py
python3 known_answer_test.py
python3 failure_tests.py
```

##### Results

| File | Result |
|---|---|
| `tesla_inputs.py` | All checks PASS (10-K totals; revenue lines sum to total; assets = liabilities + redeemable NCI + equity, FY2023–FY2025) |
| `proforma.py` | All checks PASS (base year; balance sheet balances; cash flow ties to cash; BASE, DOWNSIDE, UPSIDE × FY2026–FY2030) |
| `valuation.py` | All checks PASS. BASE **$16.54**, DOWNSIDE **$6.84**, UPSIDE **$39.10** vs. $356.09 share price |
| `comps.py` | All checks PASS (one with a documented scope exception). P/E (GM) $28.28; EV/adjusted EBITDA (GM) $24.89 |
| `known_answer_test.py` | 18 of 18 PASS against the course training case ($27.50 per share; full sensitivity grid) |
| `failure_tests.py` | 5 of 5 PASS (negative FY2030 FCFF, g = WACC, unbalanced balance sheet, zero shares all stop; normal model = BASE $16.54, DOWNSIDE $6.84, UPSIDE $39.10) |

**Outcome:** Clean end-to-end run of the final model from a fresh download. No errors, no missing files, no edits needed.

#### Earlier cold run (superseded)

On October 6, 2026 at about 7:52 PM I did a first cold run on the earlier model (BASE $14.93, UPSIDE $37.49), before I raised the BASE energy margin. All checks passed. That recording was replaced in this folder by the final one above.


## 6. Assumption challenges

### Assumption-Challenge Record — Project 1 (Tesla, TSLA)

Each load-bearing driver: **value · basis · challenge · evidence that would change it**.
Values are the BASE scenario unless noted (USD millions unless noted). Source of every driver: `proforma.py` and `valuation.py`.
Result with these drivers: BASE **$16.54**, DOWNSIDE **$6.84**, UPSIDE **$39.10** per share vs. **$356.09** share price (Sep 1, 2026).

#### 1. Load-bearing drivers

| # | Driver | Value (2026 → 2030) | Basis | Challenge | Evidence that would change it | Status |
|---|---|---|---|---|---|---|
| 1 | Vehicle deliveries growth | 3%, 6%, 7%, 6%, 5% (1.64M in FY2025 → 2.13M) | Deliveries fell in 2025; assumes a slow recovery, not a return to fast growth | Sales could keep falling as in 2025, or rise faster if cheaper models sell well | Quarterly delivery reports; new model launches | Accepted by Erlan |
| 2 | Automotive revenue per vehicle | −1% in 2026, then flat (~$39,700) | 2025 prices fell on mix and incentives; assumes pricing stabilizes | More price cuts or a cheaper model would lower it | Average selling price commentary in 10-Qs; price cuts | Accepted by Erlan |
| 3 | Regulatory credits | 1,200; 800; 500; 300; 200 (FY2025: 1,993) | FY2025 10-K: government actions, including the OBBBA, restricted some credit programs; other automakers need fewer credits | Credits are almost pure profit, so faster loss hurts margins more; rules could also last longer | Regulatory-credit revenue in 10-Qs; policy changes | Accepted by Erlan |
| 4 | Energy storage GWh growth | 25%, 20%, 18%, 15%, 12% (46.7 GWh in FY2025) | Strong 2025 growth (+27% revenue), fading as the business scales | Deployment timing is lumpy; tariffs could slow growth | Quarterly deployment numbers; Megapack factory ramp | Accepted by Erlan |
| 5 | Energy revenue per GWh | −3% per year | Prices fall with competition | Prices could fall faster | Megapack pricing; competitor pricing | Accepted by Erlan |
| 6 | Automotive gross margin ex credits | 16.0%, 17.5%, 19.0%, 20.0%, 20.0% (FY2025: 15.4%) | Partial recovery from cost cuts, cheaper models, and better factory utilization; not a return to 2022 levels | Tariffs, price cuts, or underutilization could keep it near 15% (DOWNSIDE case) | Automotive gross margin in 10-Qs; price cuts; tariff costs | Accepted by Erlan |
| 7 | Energy gross margin | 30%, 31%, 32%, 33%, 34% (FY2024: 26.2%; FY2025: 29.8%) | Margin rose from 26.2% to 29.8%; I expect it to keep rising as Megapack production scales | Tariffs on battery cells and price competition could stop the rise | Energy segment gross margin in 10-Qs; tariff costs; Megapack pricing | Revised by Erlan (was 30% flat) |
| 8 | R&D % of revenue | 6.8%, 6.5%, 6.2%, 5.8%, 5.5% (FY2025: 6.8%) | R&D grows in dollars but more slowly than revenue | AI, Robotaxi, and Optimus spending could stay structurally higher | R&D expense in 10-Qs; management commentary | Accepted by Erlan |
| 9 | SG&A % of revenue | 6.0%, 5.7%, 5.4%, 5.2%, 5.0% (FY2025: 6.2%) | Scale benefits as revenue grows | New services and products may add overhead | SG&A in 10-Qs; headcount commentary | Accepted by Erlan |
| 10 | Capex | 20,500; 18,000; 15,000; 13,000; 12,000 (FY2025: 8,527) | Tesla guided 2026 capex "in excess of $20 billion"; later years are my judgment as build-outs mature | Tesla says capex is hard to project beyond the short term; AI compute could keep it higher | Capex in 10-Qs; updated guidance | Erlan – from Lab 11 |
| 11 | Depreciation from new capex | Charged below gross profit (D&A above FY2025's 6,148) | New factories, AI compute, and fleet assets add depreciation that FY2025 margins do not include | If efficiency offsets it, margins would be higher | D&A and segment margins in 10-Qs | Erlan – chosen option (a) |
| 12 | Tax rate | 25% normalized | FY2023–FY2025 reported rates are distorted by valuation-allowance changes | Actual rate could be closer to 21% | Effective tax rate in 10-Qs/10-K | Erlan – from Lab 11 |
| 13 | WACC | 12.30% (risk-free 4.79%, beta 1.83, ERP 4.14%) | CAPM with market inputs verified on Sep 1, 2026 | Beta is current, not as of Sep 1; a lower beta raises value | Treasury yield; Tesla beta; Damodaran ERP | Accepted by Erlan (inputs verified) |
| 14 | Terminal growth | 3.0% | Long-run nominal growth; no permanent Robotaxi/Optimus windfall | At 5%, BASE rose only ~$2 (Locked Changed-Input Record) | Long-run GDP/inflation outlook | Erlan – from Lab 11 |
| 15 | Robotaxi/FSD revenue (UPSIDE only) | 0; 2,000; 8,000; 20,000; 40,000 at 50% margin | Assumes paid Robotaxi/FSD scales from 2027 with regulatory approval | No large paid driverless service exists yet; share price implies ~$605B of 2030 autonomy revenue | Robotaxi launches and approvals; paid FSD subscribers; 10-Q disclosures | Accepted by Erlan (deliberately optimistic) |

#### 2. Partner fresh-eyes challenges (Weeks 5–6 labs)

| # | Challenger | Challenge | My answer | Effect on model |
|---|---|---|---|---|
| P1 | Lab partner — **Oliana Ozbaki** (Tesla Part 1, pro-forma assumptions) | "Why does the FY2026 gross-margin judgment start at 18.0% when the model also assumes 15% revenue growth and more than $20 billion of capital spending, and what evidence would make that number too high or too low?" | The starting point is anchored to the recent margin rather than assuming growth restores earlier profitability; it rises only if pricing/mix and energy margin improve while utilization absorbs the investment. | Project 1 replaced the single margin with segment margins (drivers 6–7) and added the depreciation charge (driver 11). |
| P2 | Lab partner — **Cara Riney** (Lab 11, partner exchange 2) | Why did FY2030 operating income fall by about 1,669 when R&D rose by only 1 point? | 1% of FY2030 revenue (about 166,864 in Lab 11) is about 1,669, so the drop matches dollar for dollar. | Confirms R&D % (driver 8) passes straight through to EBIT. |
| P3 | Lab partner — **Cara Riney** (Lab 11, partner exchange 3) | Could R&D look like the bigger driver just because of the ranges you chose? | Partly yes — ranges differed (±3 pts growth vs. ±1 pt R&D); R&D still moved value more over those ranges. | Ranges matter when comparing drivers; scenarios in Project 1 change drivers with stated causes. |

#### 3. Which drivers matter most

- **Most of the value is in the terminal value** (BASE terminal value > 100% of EV because 2026–2028 FCFF is negative), so WACC, terminal growth, and 2030 margins carry the valuation.
- **No single driver closes the gap to $356.09.** Even the UPSIDE case (Robotaxi at $40B revenue) reaches only $39.10; the reverse DCF needs about $183B of 2030 FCFF.


## 7. AI-use log

### AI-Use Log — Project 1 (Tesla, TSLA)

Each entry records one AI output, what I decided, and the independent evidence I used.
**Decision options:** Accepted · Corrected · Qualified · Rejected

#### Summary

| # | Date | Tool | Task | Decision |
|---|---|---|---|---|
| 1 | Oct 6, 2026 | Codex | Build `tesla_inputs.py` | Corrected |
| 2 | Oct 6, 2026 | Codex | Separate redeemable NCI from total liabilities | Corrected |
| 3 | Oct 6, 2026 | Claude | Suggest draft forecast drivers | Accepted after review (energy margin revised) |
| 4 | Oct 6, 2026 | Codex | Build `proforma.py` | Corrected (depreciation) |
| 5 | Oct 6, 2026 | Codex | Build `valuation.py` (WACC, DCF, bridge, sensitivity, reverse DCF) | Accepted (market inputs verified); beta date qualified |
| 6 | Oct 6, 2026 | Claude + Codex | Balanced BASE margins; old margins kept as DOWNSIDE | Accepted after review (energy margin revised) |
| 7 | Oct 6, 2026 | Claude + Codex | UPSIDE scenario (Robotaxi/FSD) + market-implied autonomy | Accepted after review |
| 8 | Oct 6, 2026 | Codex | Build `comps.py` (peer policy, P/E, EV/EBITDA) | Corrected (GM finance arm removed); new definition issue found |
| 9 | Oct 6, 2026 | Codex | Build `known_answer_test.py` (training-case reconciliation) | Accepted |
| 10 | Oct 6, 2026 | Codex | Build `failure_tests.py` (highest-risk failure test) | Accepted |
| 11 | Oct 6, 2026 | Claude | Driver review: relabel drivers; raise BASE energy margin | Revised by me |
| 12 | Oct 6, 2026 | Claude | Rubric fixes: beta date label, disclosure notes, Edition B change table | Accepted after review |
| 13 | Oct 8–12, 2026 | Claude; faster-whisper | Deck tables/charts, video scripts, transcript cleanup | Accepted after review |

---

#### Entry 1 — Check that could never fail

- **What I asked:** Build `tesla_inputs.py` with FY2023–FY2025 10-K numbers (source, page, date for each) and PASS/FAIL checks.
- **What the AI produced:** A check that compared FY2025 total revenue, net income, and total assets to the same numbers typed a second time. It would print PASS even if a number were wrong.
- **Decision:** Corrected
- **Fix:** Added checks that can fail:
  - Revenue lines add up to total revenue (FY2023–FY2025)
  - Total assets = total liabilities + redeemable NCI + total equity (FY2023–FY2025)
- **Evidence:** All checks print PASS after the fix. Hand check of FY2025 revenue: 65,821 + 1,993 + 1,712 + 12,771 + 12,530 = 94,827.

#### Entry 2 — Redeemable noncontrolling interests counted as liabilities

- **What I asked:** Same build as Entry 1.
- **What the AI produced:** `total_liabilities` values that included redeemable noncontrolling interests, so the balance check passed for the wrong reason.
- **Decision:** Corrected
- **Fix:** Used the 10-K "Total liabilities" line only and added redeemable NCI as its own item.

| Fiscal year | AI's original value | 10-K total liabilities | Redeemable NCI | 10-K page |
|---|---:|---:|---:|---:|
| FY2023 | 43,251 | 43,009 | 242 | 49 |
| FY2024 | 48,453 | 48,390 | 63 | 48 |
| FY2025 | 54,999 | 54,941 | 58 | 49 |

- **Evidence:** 10-K Consolidated Balance Sheets (USD millions).
  **Confirmed by me (Oct 6, 2026)** in the FY2025 10-K Consolidated Balance Sheets: total liabilities 54,941 (2025) and 48,390 (2024); redeemable NCI 58 (2025) and 63 (2024). Check: 54,941 + 58 + 82,807 total equity = 137,806 total assets.

#### Entry 3 — Draft forecast drivers suggested by AI

- **What I asked:** Fill in starting assumptions for the 2026–2030 segment drivers (deliveries, revenue per vehicle, regulatory credits, leasing, energy GWh and price, services, segment margins).
- **What the AI produced:** A full draft set, each marked "DRAFT – suggested by Claude, Erlan to confirm" in `proforma.py`. R&D, SG&A, capex, tax rate, and working capital came from my own Lab 11 assumptions, not the AI.
- **Decision:** Qualified — used as a starting point, not accepted as final.
- **Effect after the depreciation fix (Entry 4):** EBIT falls to about $2.7–3.2B in 2027–2030 (about 2.4% of revenue vs. about 5% in FY2025), and FCFF is negative through 2029 and $1.0B in 2030. The draft margins combined with the depreciation charge make the base case strongly bearish, so the margin drivers (auto ex credits, energy, R&D, SG&A) are the ones to challenge first.
- **Evidence:** Each driver is anchored to FY2025 10-K actuals (1.64M deliveries, 46.7 GWh deployed, 15.4% auto margin ex credits, 29.8% energy margin, 7.4% services margin). Regulatory-credit decline basis checked against the FY2025 10-K, which says government actions (including the OBBBA) restricted some credit programs.

#### Entry 4 — Depreciation not charged against margins

- **What I asked:** Build `proforma.py`, a five-year three-statement forecast with FCFF and PASS/FAIL checks.
- **What the AI produced:** A working model where all checks pass. It assumed depreciation was already inside fixed gross margins, while depreciation rose from $6.1B (2026) to $10.9B (2030) because of the capex program. The higher depreciation was added back as cash but never charged as a cost, which overstated 2029–2030 EBIT and FCFF.
- **Decision:** Corrected — chose option (a): charge depreciation above the FY2025 level as a separate cost so higher capex lowers operating income.
- **Evidence:** `proforma.py` output: D&A 6,148 → 8,319 → 9,783 → 10,573 → 10,940 while segment margins stayed at the draft values. Other AI-added assumptions noted for review: no interest income on cash; no share issuance or buybacks; other assets/liabilities flat.

#### Entry 5 — DCF market inputs

- **What I asked:** Build `valuation.py`: WACC from sourced market inputs, FCFF DCF, enterprise-to-equity bridge, sensitivity grid, reverse DCF, and PASS/FAIL checks.
- **What the AI produced:** WACC 12.30%; value per share $6.84 vs. $356.09 share price; all checks PASS. It also added FY2025 digital assets ($1,008M) to `tesla_inputs.py` for the bridge.
- **Decision:** Accepted for the market inputs. Qualified for the beta date: Yahoo shows only the current beta, so it is labeled with the date I looked it up, not September 1, 2026.
- **Evidence (checked myself, Oct 6, 2026):**
  - TSLA close on Sep 1, 2026: $356.09 — Yahoo Finance historical data
  - 10-year Treasury on Sep 1, 2026: 4.79% — U.S. Treasury daily yield curve
  - Beta (5Y monthly): 1.83 — Yahoo Finance statistics, viewed Oct 6, 2026
  - Implied equity risk premium: 4.14% — Damodaran
  - Digital assets $1,008M — FY2025 10-K balance sheet (my screenshot)
- **Issue found:** Enterprise value is negative (−$11.8B), so value per share is mostly net cash. This comes from the draft margins in Entry 3, not from the DCF math.

#### Entry 6 — BASE and DOWNSIDE scenarios

- **What I asked:** Suggest a more balanced base case for the margin drivers (Claude), then add BASE and DOWNSIDE scenarios to `proforma.py` and `valuation.py` (Codex).
- **What the AI produced:** BASE margins (auto ex credits 16% → 20%, energy 30% flat, R&D 6.8% → 5.5%, SG&A 6.0% → 5.0%), marked "DRAFT – suggested by Claude, Erlan to confirm". The prior Entry 3 margins became DOWNSIDE. All checks pass for both scenarios.
- **Decision:** Qualified — I chose the balanced base case over keeping the draft margins, and kept the original drafts as the downside case. Margin values are still AI-suggested; reasons need to be in my own words before submission.
- **Note:** The BASE R&D and SG&A paths replace my own Lab 11 assumptions (R&D 7% → 6%, SG&A 6% → 5.5%).
- **Result (FY2030):**

| Scenario | EBIT ($M) | FCFF ($M) | Enterprise value ($M) | Value/share | Share price (Sep 1, 2026) |
|---|---:|---:|---:|---:|---:|
| BASE | 7,832.2 | 4,521.7 | 16,696.7 | $14.93 | $356.09 |
| DOWNSIDE | 3,186.2 | 1,039.5 | −11,840.1 | $6.84 | $356.09 |

- **Evidence:** BASE result matches my independent rough estimate (about $10–20 per share) made before the run.

#### Entry 7 — UPSIDE scenario and market-implied autonomy

- **What I asked:** Add an UPSIDE scenario = BASE plus an autonomy and software (Robotaxi/FSD) revenue line, and solve for the autonomy revenue the share price implies.
- **What the AI produced:** Autonomy revenue $0 → $2B → $8B → $20B → $40B (2026–2030) at 50% gross margin, marked "DRAFT – suggested by Claude, Erlan to confirm". All checks pass for all three scenarios.
- **Decision:** Qualified — the ramp and margin are illustrative assumptions, not evidence-based forecasts.
- **Result:**

| Scenario | FY2030 EBIT ($M) | FY2030 FCFF ($M) | Enterprise value ($M) | Value/share | Share price (Sep 1, 2026) |
|---|---:|---:|---:|---:|---:|
| BASE | 7,832.2 | 4,521.7 | 16,696.7 | $14.93 | $356.09 |
| DOWNSIDE | 3,186.2 | 1,039.5 | −11,840.1 | $6.84 | $356.09 |
| UPSIDE | 23,632.2 | 15,532.4 | 96,284.8 | $37.49 | $356.09 |

- FY2030 autonomy revenue implied by the share price: **$604.9B**, vs. $40B assumed (about 6x Tesla's total FY2025 revenue of $94.8B).
- **Evidence:** UPSIDE result is close to my rough pre-run estimate ($40–60 per share). Market inputs verified in Entry 5.

#### Entry 8 — Comparable companies

- **What I asked:** Build `comps.py` with my Lab 8 peer policy extended for EV/EBITDA (same EBITDA definition for all companies; captive finance arms excluded from EV), GM and Ford as candidates, and implied Tesla values.
- **What the AI produced:** GM qualified (P/E 26.2x, EV/EBITDA 8.6x). Ford excluded (negative EPS and EBITDA). Tesla trades at 329.7x P/E and 116.2x EV/EBITDA. Implied Tesla value: $28.28/share (P/E) and $35.85/share (EV/EBITDA). All checks PASS.
- **Decision:** Qualified.
- **Issues found:**
  1. Possible definition mismatch for GM: EV excludes GM Financial debt and cash, but GM's consolidated operating income ($2,909M) may still include GM Financial's profit. If so, EBITDA and EV measure different businesses. Check whether the 10-K segment note gives automotive-only operating income.
  2. Only one peer passes the policy, so "peer median" is really GM alone. Present it as a single-peer reference, not a range.
  3. The EV/EBITDA row in the final table is missing its "vs. share price" value.
- **Follow-up (Oct 6, 2026):** GM now uses automotive-only EBIT-adjusted ($10,916M, Note 23, p. 102) and automotive D&A ($7,003M), so GM Financial is out of both EV and EBITDA. GM EV/EBITDA fell from 8.6x to 4.7x; the EV/EBITDA value for Tesla fell from $35.85 to $24.23 per share. The "vs. share price" bug and the "peer median" label are fixed.
- **New issue:** GM's EBIT-adjusted is non-GAAP and excludes one-time charges, while Tesla's EBITDA uses GAAP operating income. The "same definition" check still printed PASS, so the check only compares labels, not the actual definition.
- **Resolution (Oct 6, 2026):** Tesla now uses normalized (adjusted) EBITDA of $10,997M to match GM's adjusted basis; EV/EBITDA value = $24.89/share. The basis check was rewritten to compare actual accounting basis and business scope, and it correctly FAILED on scope (Tesla consolidated vs. GM automotive-only). I accepted this as a documented exception: Tesla has no separate captive-finance segment, so consolidated is the closest match. The check now prints "PASS (with documented exception)" and any other basis difference still fails.

#### Entry 9 — Known-answer reconciliation

- **What I asked:** Run the course's official training case ("The Training-Case DCF, Worked End to End") through the same DCF, bridge, and sensitivity functions `valuation.py` uses for Tesla, and compare every result to the published answers.
- **What the AI produced:** `known_answer_test.py`, which imports its functions from `valuation.py` (no separate copy of the math). All 18 lines PASS: PV of FCFF 448.44, TV 1,894.65, PV of TV 1,176.43, EV 1,624.87, TV share 72.4%, equity 1,374.87, value per share $27.50, WACC 11% → $23.41, all 9 sensitivity-grid cells, and the reverse-DCF solver returns a 0.00 shift at the base price.
- **Decision:** Accepted.
- **Evidence:** Expected values come from the course training-case page, not from the AI. Tesla BASE value per share is unchanged at $14.93 after the run.

#### Entry 10 — Highest-risk failure test

- **What I asked:** Break the model on purpose, one change at a time in memory, and confirm it stops with a clear error.
- **Highest risk chosen:** FY2030 FCFF turning negative. My DOWNSIDE case is only $1.0B in 2030, so a small change could make it negative, and the terminal value would then treat a loss as permanent (the training-case page: "Year 5 must be positive, because the terminal value stands on it").
- **Result:** All 4 tests PASS — the model stops on (1) negative FY2030 FCFF, (2) terminal growth = WACC, (3) an unbalanced FY2027 balance sheet, (4) zero diluted shares. The normal model is unchanged afterward: BASE $14.93, DOWNSIDE $6.84, UPSIDE $37.49.
- **Decision:** Accepted.
- **Evidence:** Error messages printed by the run on Oct 6, 2026; the guard "FY2030 FCFF must be positive before a terminal value is calculated" is in `valuation.py`.

#### Entry 11 — My review of the forecast drivers

- **What I did:** Reviewed the AI-suggested drivers from Entries 3, 6, and 7. I kept deliveries growth, revenue per vehicle, regulatory credits, and the other drivers. I changed one: the BASE energy gross margin.
- **My change:** Energy margin from 30% flat to 30%, 31%, 32%, 33%, 34% (2026–2030), because it rose from 26.2% (FY2024) to 29.8% (FY2025) and I expect it to keep rising as Megapack production scales. DOWNSIDE energy margin is unchanged.
- **Labels in `proforma.py`:** "Accepted by Erlan" for the reviewed drivers; "Revised by Erlan (was 30% flat)" for energy; "Erlan – from Lab 11" for capex, depreciation, tax rate, working capital, liquidity/debt, and DOWNSIDE R&D and SG&A; "Erlan – chosen option (a)" for incremental depreciation. Which drivers came from AI is recorded in Entries 3, 6, and 7.
- **Edits made by:** Claude, directly in `proforma.py` and `failure_tests.py` (updated expected values).
- **Result:** BASE $14.93 → **$16.54**; DOWNSIDE $6.84 (unchanged); UPSIDE $37.49 → **$39.10**. All checks still PASS in all six files.
- **Note:** The Locked Changed-Input Record and the first cold run were done on the earlier model (BASE $14.93). They remain valid records of those runs.

#### Entry 12 — Rubric fixes

- **Beta date label (`valuation.py`):** changed from "2026-09-01" to "2026-10-06 (viewed)", because Yahoo shows only the current beta. Value unchanged (1.83); all checks still PASS. Follows up the "qualified" beta note in Entry 5.
- **Disclosure notes (`locked_prediction.md`):** restored the notes that the guiding questions and the factual result lines came from Claude, while the prediction answers, assessment, and diagnosis are my own words.
- **Edition B:** Claude drafted a "What changed from Edition A" table from my model results and decisions. Edition A was not changed. I write the falsification-question answer myself.
- **GM spot-check (Oct 6, 2026):** I checked GM's FY2025 10-K and Yahoo Finance myself: diluted EPS $3.27 (Note 21), automotive debt $16,247M (Note 14), and the Sep 1, 2026 close of $85.63 all match `comps.py`.
- **Unit fix (Oct 8, 2026):** Claude found FY2023–FY2024 deliveries and production stored in vehicles (e.g., 1,789,000) while FY2025 was in millions (1.64). Converted FY2023–FY2024 to millions in `tesla_inputs.py` so all years match. The model only uses FY2025, so results are unchanged (BASE $16.54, DOWNSIDE $6.84, UPSIDE $39.10); all files still run OK.

#### Entry 13 — Deck, video scripts and transcripts

- **Tool:** Claude (Cowork); speech-to-text: faster-whisper (small.en model).
- **Deck:** Claude designed several of the tables and charts used on the slides (for example the forecast-driver table, the valuation chart, and the "What would change my mind" table) from my model results. I chose the content, the slide order, the recommendation, and the wording, and I fixed the slides myself in PowerPoint.
- **Video scripts:** Claude drafted guide scripts for Videos 1–3 from my files and deck. I presented in my own words and changed what I said where I disagreed.
- **Transcripts:** speech-to-text made the first drafts; Claude fixed misheard words (names, tickers, finance terms) and flagged unclear spots; I listened to each flagged spot and decided the final wording.
- **Decision:** Accepted after review. **Evidence:** each transcript was checked against its recording; every number in the deck traces to `results.txt`.
