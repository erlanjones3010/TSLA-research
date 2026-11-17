"""Riverside Community Foundation mandate and model settings (editable inputs).

The client is fictional. Change a number here and every result in the app,
run_analysis.py and the tests is recomputed from it.
"""

CLIENT = "Riverside Community Foundation — Scholarship Endowment (fictional)"
RESERVE_SIZE_MILLIONS = 25.0
ANNUAL_PAYOUT = 0.04              # 4% a year, paid quarterly, for scholarships

# Objective: CPI + 3.5% a year, net of costs, over rolling five-year periods.
ASSUMED_CPI = 0.025               # assumption, not a forecast
REAL_RETURN_TARGET = 0.035
OBJECTIVE_RETURN = ASSUMED_CPI + REAL_RETURN_TARGET   # 6.0% nominal

# Universe (ETFs with monthly prices in data/prices.csv)
ASSETS = ["SGOV", "TLT", "VCIT", "SPY"]
ASSET_NAMES = {
    "SGOV": "0-3 month Treasury bills (cash reserve)",
    "TLT": "20+ year Treasury bonds",
    "VCIT": "Intermediate investment-grade corporate bonds",
    "SPY": "U.S. large-cap stocks (S&P 500)",
}
EQUITY = "SPY"
RESERVE = "SGOV"

# Benchmark (also the second transparent baseline)
BENCHMARK = {"SGOV": 0.0, "TLT": 0.0, "VCIT": 0.40, "SPY": 0.60}

# Hard limits
LIMITS = {
    "equity_min": 0.30,           # SPY at least 30%
    "equity_max": 0.70,           # SPY at most 70%
    "reserve_min": 0.05,          # SGOV at least 5% (more than six months of payouts)
    "vol_max": 0.12,              # ex-ante annual volatility at most 12%
    "drawdown_max": 0.20,         # backtest maximum drawdown at most 20%
    "turnover_max": 0.25,         # turnover at most 25% a year
}

# Risk measure and process settings
ESTIMATION_WINDOW_MONTHS = 24     # trailing months used for volatility and correlation
REBALANCE_MONTHS = (3, 6, 9, 12)  # quarterly, at quarter-end
GRID_STEP = 0.05                  # optimizer searches weights in 5% steps
COST_BPS = 10                     # one-way trading cost, basis points of amount traded

# Signal: point-in-time 10-year Treasury yield (ALFRED DGS10), building-block expected returns
CREDIT_SPREAD = 0.010             # VCIT expected return = 10-yr yield + 1.0%
EQUITY_RISK_PREMIUM = 0.040       # SPY expected return = 10-yr yield + 4.0%
SIGNAL_MAX_AGE_DAYS = 7           # stop if the latest known yield is older than this

# Stop condition: the process stops if any of these is true
#  1. the constrained portfolio breaks a hard limit in the base backtest
#  2. the signal is missing or older than SIGNAL_MAX_AGE_DAYS at a decision date
#  3. no portfolio satisfies the limits at a decision date
#  4. the constrained portfolio breaks a hard limit in 2 or more stress scenarios
STRESS_FAIL_STOP = 2
