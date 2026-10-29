# FIN43900 Lab 17 — Point-in-Time Audit

## 1. Objective

My main question is: was each number in my series knowable on the day I would have traded, and may Project 2 use it? I use point-in-time information so that each backtest decision relies only on data available at that time. This prevents look-ahead bias, which occurs when a backtest improperly uses later observations or later-revised values that an investor could not have known.

## 2. Application Overview

My `asof_app.py` Streamlit application downloads current data from [FRED](https://fred.stlouisfed.org/) and historical data vintages from [ALFRED](https://alfred.stlouisfed.org/). It displays interest-rate charts, compares historical observations with current observations, and counts observations added and overlapping observations revised. The user can select a historical “As known on” decision date to audit what information was available then.

## 3. Known-Answer Verification

I tested October 5, 2026, and matched all four professor-provided known answers. These values were calculated from downloaded data; they were not hardcoded.

| Series | Last observation known | Value |
| --- | --- | --- |
| BAA | September 2026 | 6.47% |
| FEDFUNDS | September 2026 | 3.75% |
| DGS10 | October 2, 2026 | 5.28% |
| MORTGAGE30US | October 1, 2026 | 7.28% |

## 4. PAYEMS Revision Test

For my January 15, 2025 test of `PAYEMS`, the latest observation known was December 2024, with a historical value of 159,536 thousand jobs. Since that vintage, 21 observations were added and 381 overlapping observations were revised. The large revision count demonstrates why current data cannot automatically substitute for historical vintages.

The current last observation of 159,044 refers to September 2026, not December 2024. I separately checked the current FRED download for December 2024: it reports 158,316 thousand jobs, which is below 159,536. This confirms that the current December 2024 value is lower than the January 15, 2025 vintage value; it does not make the current value appropriate for a January 2025 backtest.

## 5. DGS10 Data Card

| Field | Documentation |
| --- | --- |
| Series | `DGS10` — 10-year Treasury constant maturity yield |
| Source | Federal Reserve Bank of St. Louis, [FRED](https://fred.stlouisfed.org/series/DGS10) and [ALFRED](https://alfred.stlouisfed.org/) |
| Measure | 10-year Treasury constant maturity yield |
| Units | Percent per annum |
| Frequency | Daily, on available business days |
| Publication lag | Short, generally around the observation date. I have not stated an exact lag because it requires verification from the source’s release information. |
| Revisions | Zero overlapping observations revised in my September 30 versus October 29 comparison |
| Download date | October 29, 2026 |
| Relevance | Treasury yields affect bond valuations and are particularly relevant to TLT and VCIT in my Project 2 ETF universe. |

My verified application comparison was:

| Vintage | Last available observation | Yield | Observations added afterward | Overlapping observations revised |
| --- | --- | --- | ---: | ---: |
| As known on September 30, 2026 | September 29, 2026 | 5.26% | 19 | 0 |
| As known on October 29, 2026 | October 27, 2026 | 4.99% | 0 | 0 |

I manually checked these three DGS10 observations against the FRED data:

| Manual-check date | FRED value |
| --- | --- |
| September 29, 2026 | 5.26% |
| October 2, 2026 | 5.28% |
| October 27, 2026 | 4.99% |

## 6. Code Explanation

### Partner Code Walkthrough: ALFRED Historical Download

In `asof_app.py`, `download_as_known_on(series_id, vintage_date)` constructs an ALFRED CSV URL from `ALFRED_CSV` by calling `ALFRED_CSV.format(series_id=series_id, vintage_date=vintage_date)`. It then passes that URL and the series ID to `_read_fred_csv`. `_read_fred_csv` requests the CSV with `requests.get`, reads the response with `pd.read_csv`, identifies either `DATE` or `observation_date` as the date column, selects the requested series column when it exists (otherwise the last column), renames the selected columns to `date` and `value`, converts them to usable types, removes missing records, and sorts by date.

For each selected series, the app calls `download_current(series_id)` for the latest FRED series and `download_as_known_on(series_id, as_known_on.isoformat())` for the requested vintage. It limits the historical data to dates on or before `as_known_on`, then compares it with current data to count later observations and changed overlapping values. Therefore, the decision-date result uses the publication vintage rather than today’s values to determine what information was available.

## 7. Partner Attack

My partner asked: “How can we be sure DGS10's historical values are reliable if the data might be revised later?”

My response: “My app compared DGS10 values from September 30, 2026, with today's data and found zero revisions among overlapping observations. This suggests the historical values are stable over the tested period, although future revisions are still possible.”

## 8. Project 2 Decision

**Decision: ADMIT DGS10 CONDITIONALLY.**

DGS10 is useful for monitoring interest-rate changes affecting my bond ETFs. My condition is that Project 2 must use only observations actually available on or before each investment decision date; it cannot use later observations even if they appear in today’s FRED data. If publication timing or historical revisions cannot be verified for a particular backtest date, I will quarantine the affected observations until they can be verified.

## 9. Learning and Reflection

A data card is a concise record of a dataset’s source, definition, units, frequency, timing, revisions, and intended use. Simply cleaning data is insufficient because clean values can still be unavailable at the time of a historical decision.

Publication dates and revisions create look-ahead bias when a backtest uses values published after the decision date or values later revised from what was originally available. My September 30 comparison showed that the September 29 DGS10 observation was the last available one at that decision date, so a later observation should not have been used. A backtest using today’s data could incorrectly claim that it knew later rate movements or revised values when the trade was made.

## 10. AI Partner Validation

I used Codex and ChatGPT as two AI partners while building and validating my point-in-time interest-rate audit. They helped with coding, debugging, and interpreting FRED and ALFRED data, but I independently reviewed the work and verified the known-answer results. I also tested historical vintages, examined revisions, and evaluated whether DGS10 could be used in Project 2 without introducing look-ahead bias.

## 11. Conclusion

Point-in-time data matters because a credible backtest can use only information an investor could have known at the decision date. DGS10 is conditionally admitted for Project 2 because it is relevant to my bond ETFs and showed no overlapping revisions in my tested comparison, provided every backtest observation is verified as available at the relevant decision date.
