# Decision Memo — Riverside Community Foundation Scholarship Endowment

**AI use:** I used Claude (Anthropic, Opus) and Codex (OpenAI) to help write the code and draft documents. I also used Codex (OpenAI) to help write my earlier Lab 14–17 code that this project builds on, and to review the code, explain how it works and fix errors when running the app. The analysis and the decision below are my own.

**Education, not investment advice.** The client is fictional.

**To:** Investment Committee  **From:** *[your name]*  **As of:** 2026-09-30 data (10-yr yield known: 5.26%)

## The question
*[One sentence: what the committee must decide.]*

## What the app shows
| Portfolio | SPY | VCIT | SGOV | Return/yr | Max DD | Verdict |
|---|---|---|---|---|---|---|
| Equal weight | 25% | 25% | 25% (TLT 25%) | 5.7% | 3.1% | FAIL — SPY below 30% |
| 60/40 benchmark | 60% | 40% | 0% | 13.3% | 3.9% | FAIL — SGOV below 5%; volatility cap broken at one decision |
| Constrained | 70% | 25% | 5% | 14.5% | 4.7% | PASS |

Stress run: 6 of 8 scenarios pass; the 12-month window and the 8% volatility cap both break the 25% turnover limit, so the **stop condition is triggered (STOP)**. Backtest 2023-12-29 to 2026-09-30.

## My decision
*[Write without AI: action, allocation range, condition, what you monitor, what would reverse it. Address the STOP.]*

## Allocation range
*[Model-supported range: SPY 50–70%, VCIT 25–45%, SGOV 5%, TLT 0%. State yours.]*

## Monitoring triggers
*[Pick from the app's list and add your own.]*

## Claim most likely to reverse this decision
*[Write without AI.]*

## Committee ask
*[What you want them to approve.]*
