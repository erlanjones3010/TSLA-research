# Lab 14 — Portfolio Baselines

## 1. Lab 14 Question

**What does each simple portfolio earn and risk — and does any of them meet the Meridian mandate?**

This lab compares three simple portfolios using expected return, portfolio volatility, and reserve eligibility. Expected return and volatility show the portfolio's projected reward and risk, while reserve eligibility checks whether enough of the portfolio is held in Treasury bills or Treasury notes to meet the Meridian reserve requirement.

## 2. Portfolio Baseline Results

| Portfolio | Weights (Bills / 10-year / IG / Equity) | Expected Return | Volatility | Reserve Eligible | Meets 6.5% Return Objective? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

These results use the professor's training inputs, not actual market forecasts. The benchmark meets the 6.5% return objective but has no reserve-eligible assets. The other two portfolios have adequate reserve eligibility but do not meet the return objective, so none of the three satisfies both conditions of the Meridian mandate.

## 3. Validation Tests

Three validation tests were completed in `portfolio.py`:

- Changing both investment-grade bond/equity correlations from 0.25 to 0.50 increased benchmark volatility from 10.46% to 11.00%.
- Changing both correlations to 1.30 caused the checker to reject the input because a correlation cannot exceed +1.
- Changing only one correlation to 0.50 caused the checker to reject the matrix because it was not symmetric.

All correlation inputs were restored to their original 0.25 values after testing.

## 4. Portfolio E — Mandate Checker

Portfolio E represents the client's benchmark: 60% in the global equity index fund and 40% in the investment-grade bond fund.

| Check | Result |
|---|---|
| Weights total | 100.0% — pass |
| Long-only | 0.0% — pass |
| Reserve eligible | 0.0% — FAIL |
| Liquidity | 100.0% — pass |
| Largest single company | 0.0% — pass |
| Calendar-year loss | Requires CIO clarification |
| Final verdict | Fails 1 rule |

The benchmark meets the expected return objective, but it violates Meridian's minimum 3% reserve requirement. It would need to be adjusted before it could be accepted under the mandate.

## 5. Diversification

### 1. What is diversification?

Diversification means spreading investments across different assets instead of putting all the money into one investment. A diversified portfolio is less dependent on the performance of a single asset or market.

### 2. How does it work, and why can a correlation below +1 reduce portfolio risk?

Assets do not always rise and fall by the same amount at the same time. Correlation measures how closely two assets move together. If correlation is below +1, the assets are not moving perfectly together. When one asset has a weaker period, the other may fall less or move differently. That offset can reduce the portfolio's overall volatility.

### 3. Benchmark volatility calculation by hand

For the benchmark, the investment-grade bond weight is \(w_{IG}=0.40\), the equity weight is \(w_E=0.60\), bond volatility is \(\sigma_{IG}=0.06\), equity volatility is \(\sigma_E=0.16\), and correlation is \(\rho_{IG,E}=0.25\).

First, calculate the covariance:

\[
\operatorname{Cov}(IG,E) = \rho_{IG,E}\sigma_{IG}\sigma_E
= 0.25(0.06)(0.16) = 0.0024
\]

Then calculate portfolio variance:

\[
\begin{aligned}
\sigma_p^2 &= w_{IG}^2\sigma_{IG}^2 + w_E^2\sigma_E^2
+ 2w_{IG}w_E\operatorname{Cov}(IG,E) \\
&= (0.40)^2(0.06)^2 + (0.60)^2(0.16)^2 + 2(0.40)(0.60)(0.0024) \\
&= 0.000576 + 0.009216 + 0.001152 \\
&= 0.010944
\end{aligned}
\]

Finally, take the square root:

\[
\sigma_p = \sqrt{0.010944} = 0.1046 = 10.46\%
\]

## 6. Reflection

### 1. Why does inverse volatility put so much weight into Treasury bills?

Inverse volatility gives more weight to assets with lower volatility. Treasury bills have a volatility of only 0.5%, which is much lower than the other assets. Because the strategy uses one divided by volatility, Treasury bills receive most of the weight. This makes the portfolio very stable, but it also keeps the expected return low.

### 2. Which baseline would I show the CIO first, and why?

I would show the benchmark first because it meets the 6.5% return objective and is the closest starting point to the client's intended 60% equity and 40% investment-grade bond allocation. However, I would point out that it fails the reserve requirement because it has 0% reserve-eligible assets. It needs to be adjusted before it could be accepted.

## 7. AI Partner Validation

I used Codex and Gemini as independent AI partners to help with coding, debugging, validation, and drafting. I reviewed the calculations, program output, and written results myself before including them in this lab.

## 8. Project 2 Fund Universe

The following are example candidates for research before Thursday. They are **not yet verified or selected**.

| Ticker | Fund | Role |
|---|---|---|
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Fixed income |
| VT | Vanguard Total World Stock ETF | Equity |

Historical data source: pending.  
Download date: pending.  
Verification status: pending. Five years of monthly adjusted closing prices have not yet been downloaded or verified.

## 9. Final Verification

This report includes the Lab 14 question, baseline results, validation tests, Portfolio E mandate results, diversification explanation and calculation, reflection, AI partner validation, and the Project 2 fund universe. The report was saved as `lab14_portfolio_baselines.md` in the FIN43900-Fall2026 folder.
