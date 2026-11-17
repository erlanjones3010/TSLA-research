# Decision Memo — Meridian Endowment (Lab 13 mandate)

**AI use:** I used Claude (Anthropic, Opus) and Codex (OpenAI) to help write the code and draft documents. I also used Codex (OpenAI) to help write my earlier Lab 14–17 code that this project builds on, and to review the code, explain how it works and fix errors when running the app. The analysis and the decision below are my own.

**Education, not investment advice.** Meridian is the course client from Lab 13.

**To:** Investment Committee  **Mandate:** Lab 13 (CPI + 4% = 6.5%, 7-year horizon, annual rebalancing)  **As of:** last rebalance 2025-12-31 (10-yr yield 4.14%); trigger check on 2026-09-30 data (10-yr yield 5.26%)

## My decision
**Rebalance.** I recommend waiting until the scheduled December rebalance rather than immediately changing the portfolio. The fired trigger should be reviewed, but I would not make a major adjustment without confirming the signal. I recommend waiting until the December rebalance to confirm the fired yield trigger. If the 10-year Treasury yield remains above 4.89%, I would review the portfolio and consider rebalancing.

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
- SPY: 40–65%
- VCIT: 0–25%
- SGOV: 30–40%
- TLT: 0%

These ranges cover both the current portfolio and the model's proposed rebalance while maintaining flexibility for future adjustments.

## Material assumptions and sensitivities
- Objective CPI + 4% (Lab 13 S2) uses an assumed CPI of 2.5% (6.5% nominal).
- Expected returns: TLT = 10-yr yield; VCIT = yield + 1.0% credit spread; SPY = yield + 4.0% equity premium; SGOV = trailing 12-month return.
- Risk is estimated from the trailing 24 months of returns; trading cost is 10 bps one way; SPY stands in for global equity in the benchmark.
- Equity premium sweep (validation doc): SPY at the last rebalance is 95% at a 2% premium (6.5% unreachable), 75% at 3%, 60% at 4% (base), 45% at 5% and 40% at 6%.
- Sensitivity (stress run): a 2% equity premium makes 6.5% unreachable inside the limits; a 12-month window moves the mix to SPY 55% / VCIT 15% / SGOV 30% and uses the full 25% turnover; a 36-month window lowers the backtest return to 10.5%; 50 bps costs, a 15% reserve minimum or a 5% loss limit leave the mix unchanged.

## Monitoring triggers
- A 12-month portfolio loss reaches 7.5%.
- Expected annual return falls below 6.5%.
- A rebalance requires more than 20% turnover.

## Claim most likely to reverse this decision
My recommendation assumes the equity premium will remain high enough to meet the 6.5% return objective. If the equity premium falls to 2%, the model shows that the 6.5% target becomes unreachable, which would cause me to reconsider my recommendation.

## Committee ask
I am asking the committee to approve the proposed allocation ranges, continue monitoring the portfolio's risk and return, and allow a rebalance in December unless a major risk trigger requires earlier action.

## AI use and checks
The named AI tools, what they were used for, the checks I ran and the Locked Changed-Input Record are in `docs/validation-and-ai-use.md`.
