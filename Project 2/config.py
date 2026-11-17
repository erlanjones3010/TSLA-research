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

# Monitoring triggers (analyst choices, shown in the app and memo)
YIELD_TRIGGER_BAND = 0.0075                # review if the 10-yr yield moves more than 0.75 points from the last rebalance
LOSS_TRIGGER = 0.075                       # review if the rolling 12-month loss reaches 7.5% (S9 limit 10%)
TURNOVER_TRIGGER = 0.20                    # review if a rebalance needs more than 20% turnover (S7 limit 25%)

# Stop condition: the process stops if any of these is true
#  1. the constrained portfolio breaks a hard limit in the base backtest
#  2. the signal is missing or older than SIGNAL_MAX_AGE_DAYS at a decision date
#  3. no portfolio meets the limits and the 6.5% objective at a decision date
#  4. in 2 or more stress scenarios the constrained portfolio breaks a hard limit or cannot reach the objective
STRESS_FAIL_STOP = 2


# ---------------------------------------------------------------- driver panel
# Exposed drivers: the committee can move these in the app sidebar, inside defended bounds.
# (key, label, base, low, high, step, why the bounds)
EXPOSED_DRIVERS = [
    ("erp", "Equity risk premium over 10-yr yield", EQUITY_RISK_PREMIUM, 0.0, 0.08, 0.005,
     "0% = stocks earn no more than Treasuries; 8% = double the base. Covers a no-premium case through a crisis-level premium."),
    ("spread", "Credit spread over 10-yr yield", CREDIT_SPREAD, 0.0, 0.03, 0.0025,
     "0% = corporate bonds pay the same as Treasuries; 3% = roughly triple the base, a credit-stress level."),
    ("window", "Estimation window (months)", ESTIMATION_WINDOW_MONTHS, 12, 36, 6,
     "Under 12 months is too noisy for a covariance; over 36 is not possible because prices start 2021-10."),
    ("cost_bps", "Trading cost (bps, one way)", COST_BPS, 0, 100, 5,
     "0 = free trading; 100 bps = about 10x the cost of trading these liquid ETFs, a stress level."),
    ("objective", "Objective return (CPI + real target)", OBJECTIVE_RETURN, 0.03, 0.10, 0.0025,
     "3% = CPI + 0.5%; 10% = CPI + 7.5%. Covers a near-cash goal through an aggressive goal."),
    ("reserve_min", "S3 reserve-eligible minimum", LIMITS["reserve_min"], 0.0, 0.30, 0.01,
     "0% removes the reserve rule; 30% = ten years of payouts held in Treasuries."),
    ("turnover_max", "S7 turnover maximum per year", LIMITS["turnover_max"], 0.05, 0.50, 0.05,
     "5% = almost no trading allowed; 50% = double the Lab 13 limit."),
    ("loss_max", "S9 worst 12-month loss maximum", LIMITS["loss_max"], 0.02, 0.30, 0.01,
     "2% = near-cash tolerance; 30% = an equity-like loss tolerance."),
]

# Locked drivers: fixed by the Lab 13 mandate or the data; not adjustable in the app.
LOCKED_DRIVERS = [
    ("Universe", "SGOV, TLT, VCIT, SPY", "Fixed ETF list with price data in data/prices.csv"),
    ("S1 rebalancing", "Annual, at year-end", "Lab 13 S1"),
    ("S4 benchmark", "60% SPY / 40% VCIT", "Lab 13 S4 (SPY stands in for global equity)"),
    ("S5 long-only", "No borrowing, short selling or derivatives", "Lab 13 S5"),
    ("S6 issuer limit", "Any nonexempt issuer at most 8%", "Lab 13 S6"),
    ("S8 liquidity", "At least 90% redeemable within 5 days", "Lab 13 S8"),
    ("Assumed CPI", "2.5%", "Assumption behind the 6.5% objective (move the objective slider instead)"),
    ("Signal", "10-yr Treasury yield (ALFRED DGS10), as known on each date", "Point-in-time data file"),
]

# Equity premium sweep shown in the app (the load-bearing assumption)
ERP_SWEEP = [0.02, 0.03, 0.04, 0.05, 0.06]
