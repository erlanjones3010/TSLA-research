"""Meridian endowment mandate (from Lab 13) and model settings (editable inputs).

Each rule is tagged with the Lab 13 statement it comes from (S1-S10).
Change a number here and every result in the app, run_analysis.py and the tests is recomputed.
"""

CLIENT = "Meridian Endowment (course client from Lab 13)"
RESERVE_SIZE_MILLIONS = 100.0
QUARTERLY_PAYOUT_MILLIONS = 0.75           # S3
REQUIRED_RESERVE_QUARTERS = 4              # S3: twelve months of quarterly payouts
HORIZON_YEARS = 7                          # S1

# S2 objective: CPI + 4% a year after costs over rolling five-year periods
ASSUMED_CPI = 0.025                        # assumption, not a forecast
REAL_RETURN_TARGET = 0.04
OBJECTIVE_RETURN = ASSUMED_CPI + REAL_RETURN_TARGET   # 6.5% nominal (same as Lab 14)

# Universe: liquid ETFs with monthly prices in data/prices.csv
ASSETS = ["SGOV", "TLT", "VCIT", "SPY"]
ASSET_NAMES = {
    "SGOV": "0-3 month Treasury bills",
    "TLT": "20+ year Treasury bonds",
    "VCIT": "Intermediate investment-grade corporate bonds",
    "SPY": "U.S. large-cap stocks (S&P 500)",
}
EQUITY = "SPY"
RESERVE_ELIGIBLE = ["SGOV", "TLT"]         # S3: cash or eligible U.S. government securities
REDEEM_DAYS = {"SGOV": 1, "TLT": 1, "VCIT": 1, "SPY": 1}       # exchange-traded, T+1
ISSUER = {"SGOV": "U.S. Treasury", "TLT": "U.S. Treasury", "VCIT": "diversified fund", "SPY": "diversified fund"}
EXEMPT_ISSUERS = {"cash", "U.S. Treasury", "diversified fund"}  # same exemptions as Lab 13 mandate.py

# S4 benchmark (also the second transparent baseline): 60% global equity / 40% U.S. IG bonds.
# SPY stands in for global equity (the universe has no global equity ETF) and VCIT for U.S. IG bonds.
BENCHMARK = {"SGOV": 0.0, "TLT": 0.0, "VCIT": 0.40, "SPY": 0.60}

# Hard limits
LIMITS = {
    "reserve_min": REQUIRED_RESERVE_QUARTERS * QUARTERLY_PAYOUT_MILLIONS / RESERVE_SIZE_MILLIONS,  # S3: 3%
    "issuer_max": 0.08,                    # S6: any single nonexempt issuer
    "turnover_max": 0.25,                  # S7: a year, without committee approval
    "liquidity_min": 0.90,                 # S8: redeemable within LIQUIDITY_DAYS
    "loss_max": 0.10,                      # S9: made checkable here as the worst rolling 12-month loss
}
LIQUIDITY_DAYS = 5                         # S8
# S5: no borrowing, short selling or derivatives -> long-only weights that sum to 100%

# S10 (missing optimization goal) answered as in Lab 14: lowest risk that still reaches the objective
RISK_MEASURE = "ex-ante annual volatility"
ESTIMATION_WINDOW_MONTHS = 24              # trailing months used for volatility and correlation
REBALANCE_MONTHS = (12,)                   # S1: annual rebalancing, at year-end
GRID_STEP = 0.05                           # optimizer searches weights in 5% steps
COST_BPS = 10                              # one-way trading cost, basis points of amount traded

# Signal: point-in-time 10-year Treasury yield (ALFRED DGS10), building-block expected returns
CREDIT_SPREAD = 0.010                      # VCIT expected return = 10-yr yield + 1.0%
EQUITY_RISK_PREMIUM = 0.040                # SPY expected return = 10-yr yield + 4.0%
SIGNAL_MAX_AGE_DAYS = 7                    # stop if the latest known yield is older than this

# Stop condition: the process stops if any of these is true
#  1. the constrained portfolio breaks a hard limit in the base backtest
#  2. the signal is missing or older than SIGNAL_MAX_AGE_DAYS at a decision date
#  3. no portfolio meets the limits and the 6.5% objective at a decision date
#  4. in 2 or more stress scenarios the constrained portfolio breaks a hard limit or cannot reach the objective
STRESS_FAIL_STOP = 2
