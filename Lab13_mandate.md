# FIN 43900 Lab 13 — Portfolio Mandate Defense

## 1. Classify S1–S10

| Statement | Classification | Reason |
|---|---|---|
| S1 | Hard constraint | Establishes the seven-year investment horizon and annual rebalancing. |
| S2 | Objective | Establishes the CPI + 4% annual return goal after costs over rolling five-year periods. |
| S3 | Hard constraint | Requires twelve months of quarterly payouts to be held in cash or eligible government securities. |
| S4 | Preference | Establishes the 60% global equity and 40% U.S. investment-grade bond benchmark for comparison. |
| S5 | Hard constraint | Prohibits borrowing, short selling, and derivatives. |
| S6 | Hard constraint | Limits any single nonexempt issuer to 8% of the portfolio. |
| S7 | Hard constraint | Limits annual turnover to 25% without committee approval. |
| S8 | Hard constraint | Requires at least 90% of the portfolio to be redeemable within five business days. |
| S9 | Unverifiable promise | The 10% annual loss limit cannot be tested without clarification about measurement and enforcement. |
| S10 | Missing information | The CIO has not specified what the portfolio should optimize. |

## 2. Question for the CIO

> Should we prioritize maximizing investment returns or minimizing portfolio risk?

If the CIO prioritizes returns, I would allocate more toward equities. If the CIO prioritizes minimizing risk, I would allocate more toward bonds and cash.

## 3. Python Checker Results

The Python checker shows that the minimum reserve requirement is 3.0%.

| Portfolio | Checker result |
|---|---|
| Portfolio A | Passes all five checkable rules. |
| Portfolio B | Fails three rules: reserve, liquidity, and issuer limit. |
| Portfolio C | Fails one rule: reserve. |
| Portfolio D | Passes all five checkable rules. |

Portfolio A is the only original candidate that passes every checkable rule. Portfolio D is an additional candidate designed to test whether passing the checker guarantees suitability. The calendar-year loss requirement still needs CIO clarification.

## 4. Long-Only Test

I changed Portfolio A's cash weight from 2% to -2% and increased its global equity fund weight from 60% to 64%.

The checker reported:

| Check | Result |
|---|---|
| Weights total | 100.0% — pass |
| Long-only | -2.0% — FAIL |
| Reserve | 10.0% — pass |
| Liquidity | 100.0% — pass |
| Largest company | 0.0% — pass |
| Verdict | Fails 1 rule |

This confirmed that the checker could detect a negative weight. I restored Portfolio A's original weights afterward.

## 5. Portfolio D and Explanation

| Holding | Portfolio D |
|---|---|
| Cash | 5% |
| Treasury bills | 5% |
| Treasury 10-year note | 90% |
| Global equity index fund | 0% |
| Investment-grade bond fund | 0% |
| Private real estate fund | 0% |
| Acme Corp bonds | 0% |
| Acme Corp stock | 0% |

| Check | Portfolio D |
|---|---|
| Weights total | 100.0% — pass |
| Long-only | 0.0% — pass |
| Reserve eligible | 100.0% — pass |
| Liquidity | 100.0% — pass |
| Largest company | 0.0% — pass |
| Verdict | Passes every checkable rule |

Portfolio D passes every rule in my Python checker, but the CIO could still reject it because 90% is invested in a 10-year Treasury note, which may not provide enough returns to meet the CPI + 4% objective. This relates to S2 because the portfolio needs to support the client's return objective, not just satisfy the checkable constraints.

## 6. Investment Policy Statement

An Investment Policy Statement (IPS) is a written plan describing a client's investment objectives, constraints, and guidelines. Objectives establish the desired results, while constraints establish the rules that must be followed.

In this IPS, S1 covers the investment horizon and rebalancing. S2 states the return objective. S3 sets the reserve requirement, and S4 provides the benchmark. S5 lists the investment restrictions. S6 sets the issuer concentration limit, S7 sets the turnover restriction, and S8 sets the liquidity requirement. S9 is an unclear annual loss requirement that needs clarification. S10 shows that the portfolio's optimization priority is missing.

## 7. Reflection

A portfolio can pass every checkable rule but still be unsuitable for the client because the rules do not guarantee that it will meet the investment objective. Portfolio D is an example. It passes the Python checks, but 90% of the portfolio is invested in a 10-year Treasury note. This portfolio may not earn enough to achieve the CPI + 4% return objective.

S9 was the most difficult classification for me. At first, it looked like a hard constraint because it established a maximum annual loss of 10%. However, the CIO did not explain how the loss should be measured or how the limit would be enforced. Without that information, it cannot be checked consistently, so I classified it as an unverifiable promise.

### AI Partner Validation

I used Codex and Gemini as two independent AI partners while completing the portfolio mandate analysis. They helped with coding, debugging, testing the portfolio constraints, and drafting parts of the Markdown file, but I independently reviewed the work and confirmed the final results.
