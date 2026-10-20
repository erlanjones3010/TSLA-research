"""FIN 43900 Lab 13 — Portfolio Mandate Defense checker."""

# Holding: (issuer, business days to redeem, reserve eligible)
HOLDINGS = {
    "Cash": ("cash", 0, True),
    "Treasury bills": ("U.S. Treasury", 1, True),
    "Treasury 10-year note": ("U.S. Treasury", 1, True),
    "Global equity index fund": ("diversified fund", 2, False),
    "Investment-grade bond fund": ("diversified fund", 3, False),
    "Private real estate fund": ("diversified fund", 90, False),
    "Acme Corp bonds": ("Acme Corp", 4, False),
    "Acme Corp stock": ("Acme Corp", 1, False),
}

# Portfolio weights in percent
PORTFOLIOS = {
    "A": {
        "Cash": 2,
        "Treasury bills": 2,
        "Treasury 10-year note": 10,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 26,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 55,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 15,
        "Acme Corp bonds": 5,
        "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1,
        "Treasury bills": 1,
        "Treasury 10-year note": 0,
        "Global equity index fund": 70,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 8,
    },
    "D": {
        "Cash": 5,
        "Treasury bills": 5,
        "Treasury 10-year note": 90,
        "Global equity index fund": 0,
        "Investment-grade bond fund": 0,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "E": {
        "Cash": 0,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 40,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
}

# Editable mandate inputs
RESERVE_SIZE_MILLIONS = 100.0
QUARTERLY_PAYOUT_MILLIONS = 0.75
REQUIRED_RESERVE_QUARTERS = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUIDITY_PERCENT = 90.0
MAX_SINGLE_COMPANY_PERCENT = 8.0

EXEMPT_ISSUERS = {"cash", "U.S. Treasury", "diversified fund"}


def minimum_reserve_percent():
    """Calculate the reserve requirement as a percentage of the portfolio."""
    return (
        REQUIRED_RESERVE_QUARTERS * QUARTERLY_PAYOUT_MILLIONS
        / RESERVE_SIZE_MILLIONS
        * 100
    )


def largest_nonexempt_issuer_percent(weights):
    """Combine nonexempt holdings by issuer and return the largest total."""
    issuer_totals = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding][0]
        if issuer not in EXEMPT_ISSUERS:
            issuer_totals[issuer] = issuer_totals.get(issuer, 0) + weight
    return max(issuer_totals.values(), default=0.0)


def portfolio_checks(weights, reserve_minimum):
    """Return each automatically checkable mandate rule and its result."""
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_weight = sum(
        weight for holding, weight in weights.items() if HOLDINGS[holding][2]
    )
    liquid_weight = sum(
        weight
        for holding, weight in weights.items()
        if HOLDINGS[holding][1] <= LIQUIDITY_WINDOW_DAYS
    )
    largest_issuer = largest_nonexempt_issuer_percent(weights)

    return [
        ("Weights sum to 100%", total_weight, abs(total_weight - 100) < 1e-9),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0),
        (
            f"Reserve-eligible >= {reserve_minimum:.1f}%",
            reserve_weight,
            reserve_weight >= reserve_minimum,
        ),
        (
            f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days >= {MINIMUM_LIQUIDITY_PERCENT:.1f}%",
            liquid_weight,
            liquid_weight >= MINIMUM_LIQUIDITY_PERCENT,
        ),
        (
            f"Largest single company <= {MAX_SINGLE_COMPANY_PERCENT:.1f}%",
            largest_issuer,
            largest_issuer <= MAX_SINGLE_COMPANY_PERCENT,
        ),
    ]


def main():
    reserve_minimum = minimum_reserve_percent()
    print(f"Minimum reserve requirement: {reserve_minimum:.1f}%")
    print(
        f"  ({REQUIRED_RESERVE_QUARTERS} quarters x ${QUARTERLY_PAYOUT_MILLIONS:.2f}M "
        f"/ ${RESERVE_SIZE_MILLIONS:.1f}M)"
    )

    for name, weights in PORTFOLIOS.items():
        print(f"\nPortfolio {name}")
        failures = 0
        for rule, value, passed in portfolio_checks(weights, reserve_minimum):
            status = "pass" if passed else "FAIL"
            print(f"  {rule:<38}{value:>6.1f}%  {status}")
            failures += not passed

        print(f"  {'Calendar-year loss <= 10%':<38}requires CIO clarification")
        if failures:
            print(f"  Verdict: fails {failures} rule(s)")
        else:
            print("  Verdict: passes every checkable rule")


if __name__ == "__main__":
    main()
