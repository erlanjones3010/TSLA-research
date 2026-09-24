"""Tesla, Inc. five-year pro forma (FY2026E–FY2030E).

USD millions, except per-share data. Cash and investments are calculated last.
"""

# Values, labels, and reasons supplied in the Part 1 assumption table.
ASSUMPTION_NOTES = [
    ("Revenue growth: 15%, 15%, 12%, 10%, 8% (FY2026E–FY2030E)", "Judgment", "FY2025 revenue fell 2.9%, so this is not a continuation of recent consolidated growth. It assumes new vehicles, energy storage, and software recover growth, then deliberately fades as the revenue base expands."),
    ("Gross margin: 18.0%, 19.0%, 20.0%, 21.0%, 21.5%", "Judgment", "The historical total margin remained near 18%, while FY2025 energy generation and storage margin was higher than automotive/services. The gradual improvement assumes favorable mix and efficiency, but does not assume an immediate return to earlier Tesla margins."),
    ("SG&A as % of revenue: 6.0%, 5.8%, 5.6%, 5.5%, 5.5%", "Judgment", "FY2025 SG&A was 6.15% of revenue. Modest scale efficiency is plausible, but the assumption keeps SG&A near its recent revenue share while Tesla expands service, charging, and AI operations."),
    ("R&D as % of revenue: 7.0%, 7.0%, 6.5%, 6.0%, 6.0%", "Judgment", "FY2025 R&D was 6.76% of revenue. The first two years retain an elevated level because Tesla is investing in AI, autonomy, robotics, battery technology, and new products; modest later leverage is a modeling choice."),
    ("D&A and impairment / ending PP&E: 15.13%", "History", "FY2025 reported D&A and impairment of $6,148 divided by ending PP&E of $40,643. It is used as a transparent proxy, with the limitation stated above."),
    ("Inventory days: 58.19 days", "History", "FY2025 is the most recent result and lies between FY2023’s 62.87 and FY2024’s 54.66 days."),
    ("Tax rate: 25%", "Judgment", "The three reported rates are distorted by a FY2023 valuation-allowance release and vary from 20.43% in FY2024 to 26.96% in FY2025. A 25% normalized rate avoids treating the FY2023 tax benefit as recurring."),
    ("FY2026 capex: $20,500", "Guidance", "Tesla said 2026 capex is expected to be in excess of $20 billion, driven by AI compute/data centers, manufacturing and R&D facilities, AI-enabled fleet assets, and retail/service/charging expansion. $20.5B is a conservative numerical implementation of “in excess of.”"),
    ("FY2027–FY2030 capex: $18,000; $15,000; $13,000; $12,000", "Judgment", "The path remains well above FY2025’s $8.53B initially, then declines as major build-outs mature. Tesla cautions that capex is difficult to project beyond the short term, so these are plainly judgments, not management guidance."),
    ("Floor-plan financing: none", "None", "Tesla sells directly and the three 10-Ks do not report dealer floor-plan financing. The model should not add a dealership-financing line that the company does not have."),
    ("Minimum cash and investments: $10,000", "Judgment", "Tesla ended FY2025 with $44.06B in cash and investments, but its planned investment program is large. A $10B floor preserves liquidity in the model without treating the whole current balance as required operating cash."),
    ("Revolver limit: $6,430", "History", "FY2025 disclosed unused committed credit amounts of $6.43B. This is financing capacity, not operating cash or earnings."),
    ("Cost of equity: 10.0%; terminal growth: 3.0%", "Judgment", "Tesla’s auto, regulatory, technology, execution, and capital-spending risks support a high discount rate. A 3% perpetual-growth rate is a conservative long-run nominal assumption and should not embed a separate perpetual Robotaxi/Optimus windfall."),
    ("Diluted shares: 3,528", "History", "FY2025 weighted-average diluted shares reported in the 10-K. Any forecast dilution beyond this base must be separately modeled because the 2025 CEO performance award makes dilution materially uncertain."),
]

# ASSUMPTIONS
growth = {2026: 0.15, 2027: 0.15, 2028: 0.12, 2029: 0.10, 2030: 0.08}
gross_margin = {2026: 0.180, 2027: 0.190, 2028: 0.200, 2029: 0.210, 2030: 0.215}
sga_percent_revenue = {2026: 0.060, 2027: 0.058, 2028: 0.056, 2029: 0.055, 2030: 0.055}
rd_percent_revenue = {2026: 0.070, 2027: 0.070, 2028: 0.065, 2029: 0.060, 2030: 0.060}
capex = {2026: 20_500.0, 2027: 18_000.0, 2028: 15_000.0, 2029: 13_000.0, 2030: 12_000.0}
depreciation_ratio = 6_148.0 / 40_643.0
inventory_days = 58.19
tax_rate = 0.25
minimum_cash_and_investments = 10_000.0
revolver_limit = 6_430.0
revolver_rate = 0.06
cost_of_equity = 0.10
terminal_growth = 0.03
shares_outstanding = 3_528.0

# FY2025 reported interest divided by the matching FY2025 balance input.
interest_income_rate = 1_680.0 / 44_059.0
debt_interest_rate = 338.0 / 8_376.0
floor_plan_financing = 0.0

# OPENING BALANCE SHEET — FY2025 Form 10-K
revenue = 94_827.0
cash_and_investments = 44_059.0
inventory = 12_392.0
ppe = 40_643.0
other_assets = 40_712.0
debt_and_finance_leases = 8_376.0
# Total liabilities less debt and finance leases, plus redeemable NCI.
other_liabilities = 46_623.0
# Tesla stockholders' equity plus noncontrolling interests.
equity = 82_807.0
revolver = 0.0

other_assets_percent_revenue = other_assets / revenue
other_liabilities_percent_revenue = other_liabilities / revenue
results = {}


for year in range(2026, 2031):
    opening_revenue = revenue
    opening_cash_and_investments = cash_and_investments
    opening_inventory = inventory
    opening_ppe = ppe
    opening_other_assets = other_assets
    opening_debt_and_finance_leases = debt_and_finance_leases
    opening_other_liabilities = other_liabilities
    opening_equity = equity
    opening_revolver = revolver

    # Income statement
    revenue = opening_revenue * (1.0 + growth[year])
    gross_profit = revenue * gross_margin[year]
    sga = revenue * sga_percent_revenue[year]
    rd = revenue * rd_percent_revenue[year]
    depreciation = opening_ppe * depreciation_ratio
    operating_income = gross_profit - sga - rd - depreciation
    interest_income = opening_cash_and_investments * interest_income_rate
    interest_expense = (
        opening_debt_and_finance_leases * debt_interest_rate
        + opening_revolver * revolver_rate
    )
    pretax_income = operating_income + interest_income - interest_expense
    tax = max(0.0, pretax_income) * tax_rate
    net_income = pretax_income - tax

    # Balance sheet except cash and investments
    cost_of_revenues = revenue - gross_profit
    inventory = cost_of_revenues * inventory_days / 365.0
    ppe = opening_ppe + capex[year] - depreciation
    other_assets = revenue * other_assets_percent_revenue
    other_liabilities = revenue * other_liabilities_percent_revenue
    debt_and_finance_leases = opening_debt_and_finance_leases
    equity = opening_equity + net_income

    # FCFE before revolver activity. Cash and investments are calculated last.
    change_inventory = inventory - opening_inventory
    change_other_assets = other_assets - opening_other_assets
    change_other_liabilities = other_liabilities - opening_other_liabilities
    fcfe = (
        net_income + depreciation - capex[year] - change_inventory
        - change_other_assets + change_other_liabilities
    )
    cash_before_revolver = opening_cash_and_investments + fcfe

    if cash_before_revolver < minimum_cash_and_investments:
        revolver_draw = minimum_cash_and_investments - cash_before_revolver
        if opening_revolver + revolver_draw > revolver_limit:
            raise ValueError(
                f"FY{year}E revolver limit exceeded: draw = {revolver_draw:.1f}"
            )
        revolver = opening_revolver + revolver_draw
        cash_and_investments = minimum_cash_and_investments
    else:
        revolver_repayment = min(
            opening_revolver,
            cash_before_revolver - minimum_cash_and_investments,
        )
        revolver = opening_revolver - revolver_repayment
        cash_and_investments = cash_before_revolver - revolver_repayment

    total_assets = cash_and_investments + inventory + ppe + other_assets
    total_liabilities_and_equity = (
        debt_and_finance_leases + other_liabilities + revolver + equity
    )
    balance_gap = total_assets - total_liabilities_and_equity

    results[year] = {
        "Revenue": revenue, "Gross Profit": gross_profit, "SG&A": sga,
        "R&D": rd, "Depreciation": depreciation,
        "Operating Income": operating_income, "Interest Income": interest_income,
        "Interest Expense": interest_expense, "Pretax Income": pretax_income,
        "Tax": tax, "Net Income": net_income,
        "Cash & Investments": cash_and_investments, "Inventory": inventory,
        "PP&E": ppe, "Other Assets": other_assets,
        "Debt & Finance Leases": debt_and_finance_leases,
        "Floor-Plan Financing": floor_plan_financing,
        "Other Liabilities": other_liabilities, "Revolver": revolver,
        "Equity": equity, "FCFE": fcfe, "Balance Gap": balance_gap,
    }


def assert_balanced():
    """Refuse to value the company unless every projected balance sheet balances."""
    for year, data in results.items():
        if abs(data["Balance Gap"]) > 0.1:
            raise ValueError(
                f"FY{year}E balance sheet does not balance. "
                f"Gap = {data['Balance Gap']:.1f}"
            )
        if data["Cash & Investments"] < minimum_cash_and_investments:
            raise ValueError(f"FY{year}E cash and investments below the minimum.")


def print_table(title, rows):
    years = list(results)
    print(f"\n{title}")
    print(f"{'Line':<25}" + "".join(f"{year:>12}" for year in years))
    for row in rows:
        print(
            f"{row:<25}"
            + "".join(f"{results[year][row]:>12.1f}" for year in years)
        )


years = list(results)
print_table(
    "INCOME STATEMENT",
    [
        "Revenue", "Gross Profit", "SG&A", "R&D", "Depreciation",
        "Operating Income", "Interest Income", "Interest Expense",
        "Pretax Income", "Tax", "Net Income",
    ],
)
print_table(
    "BALANCE SHEET",
    [
        "Cash & Investments", "Inventory", "PP&E", "Other Assets",
        "Debt & Finance Leases", "Floor-Plan Financing", "Other Liabilities",
        "Revolver", "Equity",
    ],
)
print_table("CASH FLOW", ["FCFE"])

print("\nCHECKS")
for year in years:
    print(
        f"FY{year}E: Assets - Liabilities - Equity = "
        f"{results[year]['Balance Gap']:.1f}, "
        f"Cash & Investments = {results[year]['Cash & Investments']:.1f}"
    )

# Do not value Tesla unless the completed pro forma balances.
assert_balanced()

# VALUATION — FCFE discounted at cost of equity
pv_fcfe = sum(
    results[year]["FCFE"] / ((1.0 + cost_of_equity) ** period)
    for period, year in enumerate(years, start=1)
)
fcfe_2030 = results[2030]["FCFE"]
if fcfe_2030 <= 0.0:
    raise ValueError("FY2030E FCFE must be positive for a Gordon-growth terminal value.")

terminal_value = (
    fcfe_2030 * (1.0 + terminal_growth) / (cost_of_equity - terminal_growth)
)
pv_terminal = terminal_value / ((1.0 + cost_of_equity) ** len(years))
equity_value = pv_fcfe + pv_terminal
value_per_share = equity_value / shares_outstanding

print("\nVALUATION")
print(f"Equity value: ${equity_value:.2f} million")
print(f"Value per diluted share: ${value_per_share:.2f}")
