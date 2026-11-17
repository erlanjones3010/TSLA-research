# Decision Memo — Riverside Community Foundation Scholarship Endowment

**AI use:** I used Claude (Anthropic, Opus) and Codex (OpenAI) to help write the code and draft documents. I also used Codex (OpenAI) to help write my earlier Lab 14–17 code that this project builds on, and to review the code, explain how it works and fix errors when running the app. The analysis and the decision below are my own.

**Education, not investment advice.** The client is fictional.

**To:** Investment Committee  **As of:** 2026-09-30 data (10-yr yield known: 5.26%)

## The question
The investment committee needs to decide whether to approve the portfolio recommended by our model and whether it meets the investment rules.

## What the app shows
| Portfolio | SPY | VCIT | SGOV | Return/yr | Max DD | Verdict |
|---|---|---|---|---|---|---|
| Equal weight | 25% | 25% | 25% (TLT 25%) | 5.7% | 3.1% | FAIL — SPY below 30% |
| 60/40 benchmark | 60% | 40% | 0% | 13.3% | 3.9% | FAIL — SGOV below 5%; volatility cap broken at one decision |
| Constrained | 70% | 25% | 5% | 14.5% | 4.7% | PASS |

Stress run: 6 of 8 scenarios pass; the 12-month window and the 8% volatility cap both break the 25% turnover limit, so the **stop condition is triggered (STOP)**. Backtest 2023-12-29 to 2026-09-30.

## My decision
I recommend keeping the current portfolio allocation but not approving any new trades until the STOP condition is resolved. My testing showed that changing the equity risk premium did not change the portfolio weights because the model's limits still applied.

## Allocation range
I recommend staying within these portfolio ranges:

- SPY: 50–70%
- VCIT: 25–45%
- SGOV: 5%
- TLT: 0%

These ranges allow us to invest in stocks and bonds while following the portfolio's rules.

## Monitoring triggers
I would monitor the 10-year Treasury yield and the portfolio's reduction. If the yield drops below 4.51% or rises above 6.01%, I would review the portfolio. I would also review it if the reduction reaches 15%, since that would mean the portfolio has lost a significant amount of value.

## Claim most likely to reverse this decision
My decision is based on the idea that the portfolio can stay within its limits while managing risk. If the portfolio reaches a 15% reduction, I would reconsider my recommendation because it would show that the portfolio is taking on more risk than I am comfortable with.

## Committee ask
I am asking the committee to approve these allocation ranges as a conditional recommendation. I would also like approval to continue monitoring the portfolio and to hold off on new trades until the STOP condition is cleared.
