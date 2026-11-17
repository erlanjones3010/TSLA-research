# Decision Memo — Meridian Endowment (Lab 13 mandate)

**AI use:** I used Claude (Anthropic, Opus) and Codex (OpenAI) to help write the code and draft documents. I also used Codex (OpenAI) to help write my earlier Lab 14–17 code that this project builds on, and to review the code, explain how it works and fix errors when running the app. The analysis and the decision below are my own.

**Education, not investment advice.** Meridian is the course client from Lab 13.

**To:** Investment Committee  **As of:** last rebalance 2025-12-31 (10-yr yield 4.14%); trigger check on 2026-09-30 data (10-yr yield 5.26%)

## My decision
I recommend keeping the current portfolio allocation but not approving any new trades until the STOP condition is resolved. My testing showed that changing the equity risk premium did not change the portfolio weights because the model's limits still applied.

## The question
The investment committee needs to decide whether to approve the portfolio recommended by our model and whether it meets the investment rules.

## What the app shows
| Portfolio | SPY | VCIT | SGOV | TLT | Expected return | Return/yr | Max DD | Verdict |
|---|---|---|---|---|---|---|---|---|
| Equal weight | 25% | 25% | 25% | 25% | 5.42% (below 6.5%) | 5.8% | 3.1% | PASS (but misses the objective) |
| 60/40 benchmark | 60% | 40% | 0% | 0% | 6.94% | 13.4% | 3.9% | FAIL — S3 reserve below 3% |
| Constrained | 60% | 0% | 40% | 0% | 6.58% | 12.5% | 3.2% | PASS |

Backtest 2023-12-29 to 2026-09-30, annual rebalance. Stress run: 7 of 8 scenarios pass; with a 2% equity premium no mix inside the limits reaches 6.5% (MISS). **Stop condition: GO.**

**Trigger check (2026-09-30):** the 10-year yield is 5.26%, above the 3.39%–4.89% review band set at the last rebalance, so **the yield trigger has fired**. The portfolio has drifted to SPY 62% / SGOV 38% (expected return 7.17%). If rebalanced today, the model would hold SPY 40% / VCIT 25% / SGOV 35% (expected return 6.58%, lower risk), which needs a 25% trade, the full yearly S7 turnover limit.

## Allocation range
I recommend staying within these portfolio ranges:

- SPY: 50–70%
- VCIT: 25–45%
- SGOV: 5%
- TLT: 0%

These ranges allow us to invest in stocks and bonds while following the portfolio's rules.

## Material assumptions and sensitivities
- Objective CPI + 4% (Lab 13 S2) uses an assumed CPI of 2.5% (6.5% nominal).
- Expected returns: TLT = 10-yr yield; VCIT = yield + 1.0% credit spread; SPY = yield + 4.0% equity premium; SGOV = trailing 12-month return.
- Risk is estimated from the trailing 24 months of returns; trading cost is 10 bps one way; SPY stands in for global equity in the benchmark.
- Sensitivity (stress run): a 2% equity premium makes 6.5% unreachable inside the limits; a 12-month window moves the mix to SPY 55% / VCIT 15% / SGOV 30% and uses the full 25% turnover; a 36-month window lowers the backtest return to 10.5%; 50 bps costs, a 15% reserve minimum or a 5% loss limit leave the mix unchanged.

## Monitoring triggers
I would monitor the 10-year Treasury yield and the portfolio's reduction in value from its peak. If the yield drops below 4.51% or rises above 6.01%, I would review the portfolio. I would also review it if the reduction reaches 15%, since that would mean the portfolio has lost a significant amount of value.

## Claim most likely to reverse this decision
My decision is based on the idea that the portfolio can stay within its limits while managing risk. If the portfolio reaches a 15% reduction, I would reconsider my recommendation because it would show that the portfolio is taking on more risk than I am comfortable with.

## Committee ask
I am asking the committee to approve these allocation ranges as a conditional recommendation. I would also like approval to continue monitoring the portfolio and to hold off on new trades until the STOP condition is cleared.

## AI use and checks
The named AI tools, what they were used for, the checks I ran and the Locked Changed-Input Record are in `docs/validation-and-ai-use.md`.
