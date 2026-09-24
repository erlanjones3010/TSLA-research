# Lab 09: Pro-Forma Model

## Model results and validation

The pro-forma model projects the income statement, balance sheet, and FCFE from FY2026E through FY2030E. The results match the provided known answers.

| Metric | FY2026E | FY2030E |
| --- | ---: | ---: |
| Revenue | 18,323.0 | 19,678.3 |
| Operating Income | 844.2 | 971.4 |
| Net Income | 413.6 | 527.5 |
| FCFE | 211.4 | 342.3 |
| Cash | 101.8 | 719.8 |

The valuation output is **$291.75 per share**. Approximately **80%** of the total equity value comes from value after 2030.

## Balance-sheet check

The balance-sheet check, Assets minus Liabilities minus Equity, equals **0.0** in each projected year. This confirms that the completed pro-forma balance sheet balances.

## Break test

I also performed a break test by using an intentionally incorrect cash amount. The model produced a balance gap of **-61.4**, which caused the balance-sheet check to fail as expected. This confirms that the check can identify an imbalance instead of allowing an incorrect balance sheet to pass silently.

The -61.4 gap means that assets are $61.4 million lower than liabilities plus equity. Because cash is an asset, the negative gap indicates that the incorrect cash amount was $61.4 million too low relative to the rest of the balance sheet.

## Reflection

Cash is calculated last because it is the balancing result of the other operating, investing, and financing assumptions. Revenue, expenses, working capital, capital expenditures, debt activity, and equity activity are projected first; the remaining cash flow determines ending cash. Calculating cash last helps the model show whether the separate assumptions fit together in a balanced balance sheet.

## AI Partner Validation

I used Codex and Gemini as two independent AI partners while building and validating the pro-forma model. They helped with coding, debugging, and checking the model against the known answers, but I independently reviewed the work and confirmed the final results.
