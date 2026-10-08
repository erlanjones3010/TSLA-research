# AI-Use Log — Project 1 (Tesla, TSLA)

Each entry records one AI output, what I decided, and the independent evidence I used.
**Decision options:** Accepted · Corrected · Qualified · Rejected

## Summary

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

---

## Entry 1 — Check that could never fail

- **What I asked:** Build `tesla_inputs.py` with FY2023–FY2025 10-K numbers (source, page, date for each) and PASS/FAIL checks.
- **What the AI produced:** A check that compared FY2025 total revenue, net income, and total assets to the same numbers typed a second time. It would print PASS even if a number were wrong.
- **Decision:** Corrected
- **Fix:** Added checks that can fail:
  - Revenue lines add up to total revenue (FY2023–FY2025)
  - Total assets = total liabilities + redeemable NCI + total equity (FY2023–FY2025)
- **Evidence:** All checks print PASS after the fix. Hand check of FY2025 revenue: 65,821 + 1,993 + 1,712 + 12,771 + 12,530 = 94,827.

## Entry 2 — Redeemable noncontrolling interests counted as liabilities

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

## Entry 3 — Draft forecast drivers suggested by AI

- **What I asked:** Fill in starting assumptions for the 2026–2030 segment drivers (deliveries, revenue per vehicle, regulatory credits, leasing, energy GWh and price, services, segment margins).
- **What the AI produced:** A full draft set, each marked "DRAFT – suggested by Claude, Erlan to confirm" in `proforma.py`. R&D, SG&A, capex, tax rate, and working capital came from my own Lab 11 assumptions, not the AI.
- **Decision:** Qualified — used as a starting point, not accepted as final.
- **Effect after the depreciation fix (Entry 4):** EBIT falls to about $2.7–3.2B in 2027–2030 (about 2.4% of revenue vs. about 5% in FY2025), and FCFF is negative through 2029 and $1.0B in 2030. The draft margins combined with the depreciation charge make the base case strongly bearish, so the margin drivers (auto ex credits, energy, R&D, SG&A) are the ones to challenge first.
- **Evidence:** Each driver is anchored to FY2025 10-K actuals (1.64M deliveries, 46.7 GWh deployed, 15.4% auto margin ex credits, 29.8% energy margin, 7.4% services margin). Regulatory-credit decline basis checked against the FY2025 10-K, which says government actions (including the OBBBA) restricted some credit programs.

## Entry 4 — Depreciation not charged against margins

- **What I asked:** Build `proforma.py`, a five-year three-statement forecast with FCFF and PASS/FAIL checks.
- **What the AI produced:** A working model where all checks pass. It assumed depreciation was already inside fixed gross margins, while depreciation rose from $6.1B (2026) to $10.9B (2030) because of the capex program. The higher depreciation was added back as cash but never charged as a cost, which overstated 2029–2030 EBIT and FCFF.
- **Decision:** Corrected — chose option (a): charge depreciation above the FY2025 level as a separate cost so higher capex lowers operating income.
- **Evidence:** `proforma.py` output: D&A 6,148 → 8,319 → 9,783 → 10,573 → 10,940 while segment margins stayed at the draft values. Other AI-added assumptions noted for review: no interest income on cash; no share issuance or buybacks; other assets/liabilities flat.

## Entry 5 — DCF market inputs

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

## Entry 6 — BASE and DOWNSIDE scenarios

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

## Entry 7 — UPSIDE scenario and market-implied autonomy

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

## Entry 8 — Comparable companies

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

## Entry 9 — Known-answer reconciliation

- **What I asked:** Run the course's official training case ("The Training-Case DCF, Worked End to End") through the same DCF, bridge, and sensitivity functions `valuation.py` uses for Tesla, and compare every result to the published answers.
- **What the AI produced:** `known_answer_test.py`, which imports its functions from `valuation.py` (no separate copy of the math). All 18 lines PASS: PV of FCFF 448.44, TV 1,894.65, PV of TV 1,176.43, EV 1,624.87, TV share 72.4%, equity 1,374.87, value per share $27.50, WACC 11% → $23.41, all 9 sensitivity-grid cells, and the reverse-DCF solver returns a 0.00 shift at the base price.
- **Decision:** Accepted.
- **Evidence:** Expected values come from the course training-case page, not from the AI. Tesla BASE value per share is unchanged at $14.93 after the run.

## Entry 10 — Highest-risk failure test

- **What I asked:** Break the model on purpose, one change at a time in memory, and confirm it stops with a clear error.
- **Highest risk chosen:** FY2030 FCFF turning negative. My DOWNSIDE case is only $1.0B in 2030, so a small change could make it negative, and the terminal value would then treat a loss as permanent (the training-case page: "Year 5 must be positive, because the terminal value stands on it").
- **Result:** All 4 tests PASS — the model stops on (1) negative FY2030 FCFF, (2) terminal growth = WACC, (3) an unbalanced FY2027 balance sheet, (4) zero diluted shares. The normal model is unchanged afterward: BASE $14.93, DOWNSIDE $6.84, UPSIDE $37.49.
- **Decision:** Accepted.
- **Evidence:** Error messages printed by the run on Oct 6, 2026; the guard "FY2030 FCFF must be positive before a terminal value is calculated" is in `valuation.py`.

## Entry 11 — My review of the forecast drivers

- **What I did:** Reviewed the AI-suggested drivers from Entries 3, 6, and 7. I kept deliveries growth, revenue per vehicle, regulatory credits, and the other drivers. I changed one: the BASE energy gross margin.
- **My change:** Energy margin from 30% flat to 30%, 31%, 32%, 33%, 34% (2026–2030), because it rose from 26.2% (FY2024) to 29.8% (FY2025) and I expect it to keep rising as Megapack production scales. DOWNSIDE energy margin is unchanged.
- **Labels in `proforma.py`:** "Accepted by Erlan" for the reviewed drivers; "Revised by Erlan (was 30% flat)" for energy; "Erlan – from Lab 11" for capex, depreciation, tax rate, working capital, liquidity/debt, and DOWNSIDE R&D and SG&A; "Erlan – chosen option (a)" for incremental depreciation. Which drivers came from AI is recorded in Entries 3, 6, and 7.
- **Edits made by:** Claude, directly in `proforma.py` and `failure_tests.py` (updated expected values).
- **Result:** BASE $14.93 → **$16.54**; DOWNSIDE $6.84 (unchanged); UPSIDE $37.49 → **$39.10**. All checks still PASS in all six files.
- **Note:** The Locked Changed-Input Record and the first cold run were done on the earlier model (BASE $14.93). They remain valid records of those runs.

## Entry 12 — Rubric fixes

- **Beta date label (`valuation.py`):** changed from "2026-09-01" to "2026-10-06 (viewed)", because Yahoo shows only the current beta. Value unchanged (1.83); all checks still PASS. Follows up the "qualified" beta note in Entry 5.
- **Disclosure notes (`locked_prediction.md`):** restored the notes that the guiding questions and the factual result lines came from Claude, while the prediction answers, assessment, and diagnosis are my own words.
- **Edition B:** Claude drafted a "What changed from Edition A" table from my model results and decisions. Edition A was not changed. I write the falsification-question answer myself.
- **GM spot-check (Oct 6, 2026):** I checked GM's FY2025 10-K and Yahoo Finance myself: diluted EPS $3.27 (Note 21), automotive debt $16,247M (Note 14), and the Sep 1, 2026 close of $85.63 all match `comps.py`.
- **Unit fix (Oct 8, 2026):** Claude found FY2023–FY2024 deliveries and production stored in vehicles (e.g., 1,789,000) while FY2025 was in millions (1.64). Converted FY2023–FY2024 to millions in `tesla_inputs.py` so all years match. The model only uses FY2025, so results are unchanged (BASE $16.54, DOWNSIDE $6.84, UPSIDE $39.10); all files still run OK.
