# Lab 18 — Buffett Investor Skill

## What the skill does

`.agents/skills/buffett-investor/` is a repository-local Codex skill. Its Python script accepts a ticker, uses the official SEC ticker-to-CIK and companyfacts endpoints (no API key), and reads USD facts reported in 10-K or 10-K/A filings only. It creates five fiscal-year-end rows, preserving the latest filing when a fiscal period appears more than once.

The script follows these source priorities:

- Revenue: `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues`
- Net income: `NetIncomeLoss`
- Operating cash flow: `NetCashProvidedByUsedInOperatingActivities`
- Capital spending: `PaymentsToAcquirePropertyPlantAndEquipment`, then `PaymentsToAcquireProductiveAssets`
- Equity: `StockholdersEquity`

## What Python computes versus what AI judges

Python deterministically selects filing facts, displays tags and values in millions, computes ROE as net income divided by year-end equity, computes owner earnings as operating cash flow less capital spending, and determines the three checks. It does not estimate missing values. Zero or negative equity produces `not known` for ROE.

The memo uses Buffett-inspired business questions—business quality, economic moats, consistent profitability, financial strength, and owner earnings—to frame a qualitative judgment. It may use only numbers printed by Python, distinguishes those verified results from judgment, and does not discuss stock price or targets.

## Annual-row conversion

`annual_candidates()` filters USD companyfacts to 10-K / 10-K/A facts. For flows it retains only approximately one-year durations (330–370 days); for every fiscal-year-end date it retains the latest `filed` observation. It applies a fallback XBRL tag only where the higher-priority tag has no fact for that date. `build_analysis()` combines the five latest fiscal-year ends into display rows.

## Costco verification

Live SEC EDGAR run completed for COST on 2026-11-03. The selected tags were `RevenueFromContractWithCustomerExcludingAssessedTax`, `NetIncomeLoss`, `NetCashProvidedByUsedInOperatingActivities`, `PaymentsToAcquirePropertyPlantAndEquipment`, and `StockholdersEquity`.

| Fiscal year end | Revenue ($m) | Net income ($m) | OCF ($m) | Capex ($m) | Equity ($m) | ROE | Owner earnings ($m) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2022-08-28 | 226,954.0 | 5,844.0 | 7,392.0 | 3,891.0 | 20,642.0 | 28.3% | 3,501.0 |
| 2023-09-03 | 242,290.0 | 6,292.0 | 11,068.0 | 4,323.0 | 25,058.0 | 25.1% | 6,745.0 |
| 2024-09-01 | 254,453.0 | 7,367.0 | 11,339.0 | 4,710.0 | 23,622.0 | 31.2% | 6,629.0 |
| 2025-08-31 | 275,235.0 | 8,099.0 | 13,335.0 | 5,498.0 | 29,164.0 | 27.8% | 7,837.0 |
| 2026-08-30 | 303,154.0 | 9,226.0 | 15,817.0 | 6,435.0 | 35,803.0 | 25.8% | 9,382.0 |

All three checks passed: ROE was at least 15% in each year; owner earnings were positive in each year; and owner earnings increased from $3,501.0 million to $9,382.0 million.

## My Decision

I conditionally trust the Buffett verdict on Costco because the company passed all three financial checks using verified SEC data. However, the results alone do not establish whether Costco has a durable competitive advantage or whether its stock is reasonably priced.

## Code Explanation for My Partner

In my script, `sec_get()` downloads the SEC ticker-to-CIK list and the matching companyfacts data from SEC EDGAR. The function that turns those facts into annual financial rows is `build_analysis()` in `sec_buffett.py`. It identifies the company's fiscal years from the ending dates in annual 10-K facts and keeps the newest five.

For each year, I use the required XBRL tags in priority order—for example, the preferred revenue tag before its fallback. `annual_candidates()` chooses the latest filed 10-K when the same fiscal period appears more than once. Python calculates ROE as net income divided by year-end equity and owner earnings as operating cash flow minus capital spending. `metric_cell()` returns `not found` when a source fact is missing, and the script never estimates it because an estimate could create an unsupported financial conclusion.

Python computes the filing facts, financial values, and three Buffett checks. AI interprets those verified outputs and judges business quality, such as the possible strength of a moat; it does not make up the calculations.

## Fresh-Chat Comparison

Question: “Is Costco a Buffett business? Give its ROE for the last five years.”

My verified COST ROE results are:

- FY2022: 28.3%
- FY2023: 25.1%
- FY2024: 31.2%
- FY2025: 27.8%
- FY2026: 25.8%

An AI without this skill may provide numbers without a reproducible calculation or a clearly identified source. My skill uses Python to calculate financial metrics directly from SEC EDGAR data, with the selected XBRL tags and fiscal-year-end dates retained in the output.

My fresh-chat observations: I asked, “Is Costco a Buffett business? Give its ROE for the last five years.” The fresh chat gave the same verified ROE values: FY2022 28.3%, FY2023 25.1%, FY2024 31.2%, FY2025 27.8%, and FY2026 25.8%. It described Costco as a strong Buffett-style business because of its membership model, customer loyalty, economies of scale, competitive prices, and consistent profitability. It also correctly noted that a stock-investment decision would require separate valuation analysis.

My Buffett skill is more reproducible because Python applies the same ROE calculation and SEC EDGAR source rules every time. An AI without the skill may not follow the same calculation rules or identify the exact source tags. I trust verified, reproducible calculations more than unsupported AI-generated numbers because I can trace and check how each value was produced.

## JPMorgan missing-data probe

Live SEC EDGAR run completed for JPM on 2026-11-03. No selected capital-spending tag was found in any of the five annual rows. Capital spending and owner earnings display `not found`; both owner-earnings checks are `not known`. The generated JPM memo explicitly says owner earnings cannot be evaluated. The ROE check was `fail`; it does not change the missing-data result.

## Unsupported-number validation probe

The saved test copy `lab18_outputs/COST_buffett_memo_invalid_test.md` inserts `40.0%`. The validator flags `Unsupported percentage: 40.0%`. Its tests also confirm that an annual year such as `2026` and a supported amount such as `$10.0 million` are not false positives.

## What I learned

An AI skill packages repeatable instructions plus deterministic supporting code. The model is useful for bounded qualitative explanation, but code must calculate and validate financial claims. Missing data should stay missing: substituting, extrapolating, or estimating a capital-spending number would create a false owner-earnings conclusion.

## Reflection

My Buffett skill makes the financial calculations and the three Buffett checks consistent across companies. Python computes the financial values, while AI interprets the results and judges business quality. Reporting `not found` is better than estimating because it prevents unsupported financial conclusions. Costco's results support a positive business-quality assessment, but this analysis does not establish whether the stock is reasonably priced.

## AI Partner Validation

Codex assisted with the skill structure, SEC extraction code, Streamlit interface, memo template, and tests. ChatGPT assisted as the AI writing partner for the Buffett-style framing. I independently verified the live COST and JPM outputs, the selected XBRL tags, the three Costco check outcomes, and the deliberate unsupported-40.0%-claim validator probe.
