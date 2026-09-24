# Lab 09 — Pro-Forma Build
# Asbury Automotive Group (ABG)
# USD millions

# -----------------------------
# ASSUMPTIONS
# -----------------------------

growth = 0.018
gross_margin = 0.1705

sga_ratios = {
    2026: 0.665,
    2027: 0.655,
    2028: 0.645,
    2029: 0.645,
    2030: 0.645,
}

depreciation_ratio = 82.4 / 3070.4
impairment = 120.0
capex = 250.0
tax_rate = 0.255

inventory_days = 2135.8 / (17999.0 - 3071.7) * 365
floor_plan_ratio = 2027.0 / 2135.8

other_working_capital_rate = 0.008

minimum_cash = 25.0
revolver_limit = 850.0
revolver_rate = 0.06

debt_repayment = 150.0
share_buyback = 150.0

floor_plan_interest_rate = 0.0467
term_debt_interest_rate = 0.0544

cost_of_equity = 0.10
terminal_growth = 0.025
shares_outstanding = 17.951349


# -----------------------------
# OPENING BALANCE SHEET — FY2025
# -----------------------------

revenue = 17999.0
inventory = 2135.8
ppe = 3070.4
other_assets = 6371.6
cash = 40.4

floor_plan = 2027.0
term_debt = 3572.0
other_liabilities = 2127.5
equity = 3891.7
revolver = 0.0


# -----------------------------
# STORAGE
# -----------------------------

results = {}


# -----------------------------
# PROJECT 2026–2030
# -----------------------------

for year in range(2026, 2031):

    opening_revenue = revenue
    opening_inventory = inventory
    opening_ppe = ppe
    opening_other_assets = other_assets
    opening_cash = cash
    opening_floor_plan = floor_plan
    opening_debt = term_debt
    opening_equity = equity
    opening_revolver = revolver

    # Income Statement
    revenue = opening_revenue * (1 + growth)
    gross_profit = revenue * gross_margin
    sga = gross_profit * sga_ratios[year]
    depreciation = opening_ppe * depreciation_ratio

    operating_income = (
        gross_profit
        - sga
        - depreciation
        - impairment
    )

    interest = (
        opening_floor_plan * floor_plan_interest_rate
        + opening_debt * term_debt_interest_rate
        + opening_revolver * revolver_rate
    )

    pretax_income = operating_income - interest
    tax = max(0, pretax_income) * tax_rate
    net_income = pretax_income - tax

    # Balance Sheet except cash
    inventory = (revenue - gross_profit) * inventory_days / 365
    floor_plan = inventory * floor_plan_ratio

    ppe = opening_ppe + capex - depreciation

    change_revenue = revenue - opening_revenue
    change_other_wc = other_working_capital_rate * change_revenue

    other_assets = (
        opening_other_assets
        + change_other_wc
        - impairment
    )

    term_debt = opening_debt - debt_repayment

    other_liabilities = other_liabilities

    equity = (
        opening_equity
        + net_income
        - share_buyback
    )

    # Free Cash Flow to Equity
    change_inventory = inventory - opening_inventory
    change_floor_plan = floor_plan - opening_floor_plan

    fcfe = (
        net_income
        + depreciation
        + impairment
        - capex
        - change_inventory
        - change_other_wc
        + change_floor_plan
        - debt_repayment
    )

    # Cash before revolver activity
    cash_before_revolver = (
        opening_cash
        + fcfe
        - share_buyback
    )

    # Revolver logic
    if cash_before_revolver < minimum_cash:
        draw = minimum_cash - cash_before_revolver

        if opening_revolver + draw > revolver_limit:
            raise ValueError(f"{year}: Revolver limit exceeded")

        revolver = opening_revolver + draw
        cash = minimum_cash

    else:
        available_for_repayment = cash_before_revolver - minimum_cash
        revolver_repayment = min(
            opening_revolver,
            available_for_repayment
        )

        revolver = opening_revolver - revolver_repayment
        cash = cash_before_revolver - revolver_repayment

    # Balance sheet check
    total_assets = (
        cash
        + inventory
        + ppe
        + other_assets
    )

    total_liabilities_and_equity = (
        floor_plan
        + term_debt
        + other_liabilities
        + revolver
        + equity
    )

    balance_gap = (
        total_assets
        - total_liabilities_and_equity
    )

    results[year] = {
        "Revenue": revenue,
        "Gross Profit": gross_profit,
        "SG&A": sga,
        "Depreciation": depreciation,
        "Impairment": impairment,
        "Operating Income": operating_income,
        "Interest": interest,
        "Pretax Income": pretax_income,
        "Tax": tax,
        "Net Income": net_income,
        "Inventory": inventory,
        "PP&E": ppe,
        "Other Assets": other_assets,
        "Cash": cash,
        "Floor Plan": floor_plan,
        "Term Debt": term_debt,
        "Other Liabilities": other_liabilities,
        "Revolver": revolver,
        "Equity": equity,
        "FCFE": fcfe,
        "Balance Gap": balance_gap,
    }


# -----------------------------
# BALANCE CHECK
# -----------------------------

def assert_balanced():
    for year, data in results.items():

        gap = data["Balance Gap"]

        if abs(gap) > 0.1:
            raise ValueError(
                f"FY{year}E balance sheet does not balance. "
                f"Gap = {gap:.1f}"
            )

        if data["Cash"] < minimum_cash:
            raise ValueError(
                f"FY{year}E cash below minimum."
            )


# -----------------------------
# PRINT TABLES
# -----------------------------

years = list(results.keys())


def print_table(title, rows):
    print("\n" + title)

    print(
        f"{'Line':<25}"
        + "".join(f"{year:>12}" for year in years)
    )

    for row in rows:
        print(
            f"{row:<25}"
            + "".join(
                f"{results[year][row]:>12.1f}"
                for year in years
            )
        )


print_table(
    "INCOME STATEMENT",
    [
        "Revenue",
        "Gross Profit",
        "SG&A",
        "Depreciation",
        "Impairment",
        "Operating Income",
        "Interest",
        "Pretax Income",
        "Tax",
        "Net Income",
    ],
)

print_table(
    "BALANCE SHEET",
    [
        "Cash",
        "Inventory",
        "PP&E",
        "Other Assets",
        "Floor Plan",
        "Term Debt",
        "Other Liabilities",
        "Revolver",
        "Equity",
    ],
)

print_table(
    "CASH FLOW",
    [
        "FCFE",
    ],
)

print("\nCHECKS")

for year in years:
    print(
        f"FY{year}E: "
        f"Assets - Liabilities - Equity = "
        f"{results[year]['Balance Gap']:.1f}, "
        f"Cash = {results[year]['Cash']:.1f}"
    )


# Check model before valuation
assert_balanced()


# -----------------------------
# VALUATION
# -----------------------------

pv_fcfe = 0.0

for i, year in enumerate(years, start=1):
    pv_fcfe += (
        results[year]["FCFE"]
        / ((1 + cost_of_equity) ** i)
    )

fcfe_2030 = results[2030]["FCFE"]

terminal_value = (
    (fcfe_2030 + debt_repayment)
    * (1 + terminal_growth)
    / (cost_of_equity - terminal_growth)
)

pv_terminal = (
    terminal_value
    / ((1 + cost_of_equity) ** 5)
)

equity_value = pv_fcfe + pv_terminal

share_after_2030 = (
    pv_terminal / equity_value
)

value_per_share = (
    equity_value / shares_outstanding
)


print("\nVALUATION")
print(f"Equity value: ${equity_value:.2f} million")
print(
    f"Share of value after 2030: "
    f"{share_after_2030:.1%}"
)
print(
    f"Value per share: "
    f"${value_per_share:.2f}"
)