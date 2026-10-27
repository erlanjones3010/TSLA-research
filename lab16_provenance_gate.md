# FIN43900 Lab 16 — Provenance Gate

## 1. Objective

A month identifies the period a number measures, while a publication date identifies when that number became available. For example, a value for February may not be published until March or later. In a backtest or trading decision, using a value before its publication date would use information that was not known at the time. Keeping these dates separate prevents look-ahead bias.

## 2. Four Filtering Rules

1. **Quarantine missing tickers.** Rows without a ticker cannot be assigned to a company, so they are excluded from the investable panel.
2. **Remove exact duplicates.** Identical records add no information and could double-count an observation.
3. **Remove rows published after the decision date.** A decision may use only information that was available on or before that date.
4. **Keep the latest available publication for each ticker and month.** When several revisions exist for the same company and measurement month, use the newest version that was available by the decision date.

## 3. Known-Answer Verification

Decision date: **March 31, 2026**.

- Missing ticker: row 11
- Duplicate: row 7
- Published too late: rows 3, 8, and 10
- Older revision: row 2
- Remaining rows: 1, 4, 5, 6, 9, and 12

| Ticker | As-of signal | Naive signal |
| --- | --- | --- |
| AAA | +1.98% February | +5.83% March |
| BBB | -1.02% February | -5.15% March |
| CCC | +0.91% February | +1.82% February |

## 4. Code Explanation

Rule 4 groups records using the pair `(ticker, month)`. Within each group, it keeps the record with the latest `published` date, after the publication-date filter has already limited records to those available by the decision date. For AAA's February value, the later available revision changes the index from 104 to 103, so the 103 publication is retained and the earlier 104 record is treated as an older revision.

## 5. Partner Test

Changing the decision date to **April 15, 2026** produced these as-of signals:

- AAA: +5.83% March
- BBB: -5.15% March
- CCC: +1.82% February

These match the original naive signals because the later publications had become available by April 15. In this test, Rule 4 removed older revisions from rows 2 and 12. The decision date was then restored to March 31, 2026.

## 6. Learning and Reflection

This lab showed that a data value's measurement month is not enough to establish whether it could have informed a historical decision. I need to check publication timing, remove invalid or duplicate records, and choose the correct available revision before calculating signals. Otherwise, results can look stronger or materially different because they rely on information that was not yet public.

## AI Partner Validation

I used Codex and ChatGPT as two AI partners while building and validating the point-in-time filter for Lab 16. They helped with coding, debugging, applying the publication-date and revision rules, and drafting parts of the markdown file. I independently reviewed the work, confirmed the as-of and naive signals against the known answers, and tested a later decision date to verify that the filter correctly prevented look-ahead bias.
