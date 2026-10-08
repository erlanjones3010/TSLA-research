"""Tesla, Inc. (TSLA) Project 1 historical inputs.

Valuation date: 2026-09-01.  Monetary amounts are USD millions unless a
different unit is stated.  Share figures are diluted share counts in millions.
No forecasts or normalizations have been applied to the reported history.
"""

VALUATION_DATE = "2026-09-01"
COMPANY = "Tesla, Inc. (TSLA)"

FY2023_10K = (
    "Tesla Form 10-K for FY2023, filed 2024-01-29, "
    "accession 0001628280-24-002390"
)
FY2024_10K = (
    "Tesla Form 10-K for FY2024, filed 2025-01-30, "
    "accession 0001628280-25-003063"
)
FY2025_10K = (
    "Tesla Form 10-K for FY2025, filed 2026-01-29, "
    "accession 0001628280-26-003952"
)


def item(value, unit, source, location, as_of, item_type="fact"):
    """Return the required, source-traceable representation for one input."""
    return {
        "value": value,
        "unit": unit,
        "source": source,
        "location": location,
        "as_of": as_of,
        "type": item_type,
    }


# Income-statement and cash-flow history.  Parentheses in the filings are
# represented as negative values; expense lines are stored as positive outflows.
HISTORY = {
    "FY2023": {
        "revenue": {
            "automotive_sales": item(78509, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "2023-12-31"),
            "regulatory_credits": item(1790, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "2023-12-31"),
            "automotive_leasing": item(2120, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "2023-12-31"),
            "energy_generation_and_storage": item(6035, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "2023-12-31"),
            "services_and_other": item(8319, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "2023-12-31"),
            "total": item(96773, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "2023-12-31"),
        },
        "cost_of_revenue": {
            "automotive": item(66389, "USD millions", FY2023_10K, "Consolidated Statements of Operations, total automotive cost of revenues, p. 50", "2023-12-31"),
            "energy_generation_and_storage": item(4894, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "2023-12-31"),
            "services_and_other": item(7830, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "2023-12-31"),
        },
        "expenses_and_cash_flow": {
            "research_and_development": item(3969, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "FY2023"),
            "selling_general_and_administrative": item(4800, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "FY2023"),
            "restructuring_and_other": item(0, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50 (reported as dash)", "FY2023"),
            "depreciation_amortization_and_impairment": item(4667, "USD millions", FY2023_10K, "Consolidated Statements of Cash Flows, p. 53; combined reported line", "FY2023"),
            "stock_based_compensation": item(1812, "USD millions", FY2023_10K, "Consolidated Statements of Cash Flows, p. 53", "FY2023"),
            "interest_expense": item(156, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50 (reported as $(156))", "FY2023"),
            "income_tax": item(-5001, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50 (benefit)", "FY2023"),
            "operating_cash_flow": item(13256, "USD millions", FY2023_10K, "Consolidated Statements of Cash Flows, p. 53", "FY2023"),
            "capex": item(8898, "USD millions", FY2023_10K, "Consolidated Statements of Cash Flows, purchases of property and equipment excluding finance leases, net of sales, p. 53", "FY2023"),
        },
        "net_income": item(14974, "USD millions", FY2023_10K, "Consolidated Statements of Operations, p. 50", "FY2023"),
        "balance_sheet": {
            "cash_and_cash_equivalents": item(16398, "USD millions", FY2023_10K, "Consolidated Balance Sheets, p. 49", "2023-12-31"),
            "short_term_investments": item(12696, "USD millions", FY2023_10K, "Consolidated Balance Sheets, p. 49", "2023-12-31"),
            "accounts_receivable": item(3508, "USD millions", FY2023_10K, "Consolidated Balance Sheets, p. 49", "2023-12-31"),
            "inventory": item(13626, "USD millions", FY2023_10K, "Consolidated Balance Sheets, p. 49", "2023-12-31"),
            "property_plant_and_equipment_net": item(29725, "USD millions", FY2023_10K, "Consolidated Balance Sheets, p. 49", "2023-12-31"),
            "accounts_payable": item(14431, "USD millions", FY2023_10K, "Consolidated Balance Sheets, p. 49", "2023-12-31"),
            "total_debt_and_finance_leases": item(5230, "USD millions", FY2023_10K, "Consolidated Balance Sheets: current portion plus non-current debt and finance leases, p. 49", "2023-12-31"),
            "finance_lease_liabilities": item(573, "USD millions", FY2023_10K, "Note 14, Leases, total finance lease liabilities, p. 77", "2023-12-31"),
            "operating_lease_liabilities": item(4343, "USD millions", FY2023_10K, "Note 14, Leases, total operating lease liabilities, p. 77", "2023-12-31"),
            "noncontrolling_interests": item(733, "USD millions", FY2023_10K, "Consolidated Balance Sheets, p. 49", "2023-12-31"),
            "total_liabilities": item(43009, "USD millions", FY2023_10K, "Consolidated Balance Sheets, total liabilities, p. 49", "2023-12-31"),
            "redeemable_noncontrolling_interests": item(242, "USD millions", FY2023_10K, "Consolidated Balance Sheets, redeemable noncontrolling interests in subsidiaries, p. 49", "2023-12-31"),
            "total_equity": item(63367, "USD millions", FY2023_10K, "Consolidated Statements of Redeemable Noncontrolling Interests and Equity, total equity, p. 52", "2023-12-31"),
            "total_assets": item(106618, "USD millions", FY2023_10K, "Consolidated Balance Sheets, p. 49", "2023-12-31"),
        },
        "shares": {
            "diluted_weighted_average": item(3485, "millions of shares", FY2023_10K, "Consolidated Statements of Operations, p. 50", "FY2023"),
            "period_end_shares_outstanding": item(3185, "millions of shares", FY2023_10K, "Consolidated Balance Sheets, common stock outstanding, p. 49", "2023-12-31"),
        },
        "operating_data": {
            "vehicle_deliveries": item(1.808581, "millions of vehicles", FY2023_10K, "MD&A, Overview and 2023 Highlights, p. 33", "FY2023"),
            "vehicle_production": item(1.845985, "millions of vehicles", FY2023_10K, "MD&A, Overview and 2023 Highlights, p. 33", "FY2023"),
            "energy_storage_deployed": item(14.72, "GWh", FY2023_10K, "MD&A, Overview and 2023 Highlights, p. 33", "FY2023"),
        },
    },
    "FY2024": {
        "revenue": {
            "automotive_sales": item(72480, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "2024-12-31"),
            "regulatory_credits": item(2763, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "2024-12-31"),
            "automotive_leasing": item(1827, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "2024-12-31"),
            "energy_generation_and_storage": item(10086, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "2024-12-31"),
            "services_and_other": item(10534, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "2024-12-31"),
            "total": item(97690, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "2024-12-31"),
        },
        "cost_of_revenue": {
            "automotive": item(62873, "USD millions", FY2024_10K, "Consolidated Statements of Operations, total automotive cost of revenues, p. 49", "2024-12-31"),
            "energy_generation_and_storage": item(7446, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "2024-12-31"),
            "services_and_other": item(9921, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "2024-12-31"),
        },
        "expenses_and_cash_flow": {
            "research_and_development": item(4540, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "FY2024"),
            "selling_general_and_administrative": item(5150, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "FY2024"),
            "restructuring_and_other": item(684, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "FY2024"),
            "depreciation_amortization_and_impairment": item(5368, "USD millions", FY2024_10K, "Consolidated Statements of Cash Flows, p. 52; combined reported line", "FY2024"),
            "stock_based_compensation": item(1999, "USD millions", FY2024_10K, "Consolidated Statements of Cash Flows, p. 52", "FY2024"),
            "interest_expense": item(350, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49 (reported as $(350))", "FY2024"),
            "income_tax": item(1837, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "FY2024"),
            "operating_cash_flow": item(14923, "USD millions", FY2024_10K, "Consolidated Statements of Cash Flows, p. 52", "FY2024"),
            "capex": item(11339, "USD millions", FY2024_10K, "Consolidated Statements of Cash Flows, purchases of property and equipment excluding finance leases, net of sales, p. 52", "FY2024"),
        },
        "net_income": item(7153, "USD millions", FY2024_10K, "Consolidated Statements of Operations, p. 49", "FY2024"),
        "balance_sheet": {
            "cash_and_cash_equivalents": item(16139, "USD millions", FY2024_10K, "Consolidated Balance Sheets, p. 48", "2024-12-31"),
            "short_term_investments": item(20424, "USD millions", FY2024_10K, "Consolidated Balance Sheets, p. 48", "2024-12-31"),
            "accounts_receivable": item(4418, "USD millions", FY2024_10K, "Consolidated Balance Sheets, p. 48", "2024-12-31"),
            "inventory": item(12017, "USD millions", FY2024_10K, "Consolidated Balance Sheets, p. 48", "2024-12-31"),
            "property_plant_and_equipment_net": item(35836, "USD millions", FY2024_10K, "Consolidated Balance Sheets, p. 48", "2024-12-31"),
            "accounts_payable": item(12474, "USD millions", FY2024_10K, "Consolidated Balance Sheets, p. 48", "2024-12-31"),
            "total_debt_and_finance_leases": item(8213, "USD millions", FY2024_10K, "Consolidated Balance Sheets: current portion plus non-current debt and finance leases, p. 48", "2024-12-31"),
            "finance_lease_liabilities": item(335, "USD millions", FY2024_10K, "Note 13, Leases, total finance lease liabilities, p. 76", "2024-12-31"),
            "operating_lease_liabilities": item(5410, "USD millions", FY2024_10K, "Note 13, Leases, total operating lease liabilities, p. 76", "2024-12-31"),
            "noncontrolling_interests": item(704, "USD millions", FY2024_10K, "Consolidated Balance Sheets, p. 48", "2024-12-31"),
            "total_liabilities": item(48390, "USD millions", FY2024_10K, "Consolidated Balance Sheets, total liabilities, p. 48", "2024-12-31"),
            "redeemable_noncontrolling_interests": item(63, "USD millions", FY2024_10K, "Consolidated Balance Sheets, redeemable noncontrolling interests in subsidiaries, p. 48", "2024-12-31"),
            "total_equity": item(73617, "USD millions", FY2024_10K, "Consolidated Statements of Redeemable Noncontrolling Interests and Equity, total equity, p. 51", "2024-12-31"),
            "total_assets": item(122070, "USD millions", FY2024_10K, "Consolidated Balance Sheets, p. 48", "2024-12-31"),
        },
        "shares": {
            "diluted_weighted_average": item(3498, "millions of shares", FY2024_10K, "Consolidated Statements of Operations, p. 49", "FY2024"),
            "period_end_shares_outstanding": item(3216, "millions of shares", FY2024_10K, "Consolidated Balance Sheets, common stock outstanding, p. 48", "2024-12-31"),
        },
        "operating_data": {
            "vehicle_deliveries": item(1.789, "millions of vehicles (approximately)", FY2024_10K, "MD&A, Overview and 2024 Highlights, p. 32", "FY2024"),
            "vehicle_production": item(1.773, "millions of vehicles (approximately)", FY2024_10K, "MD&A, Overview and 2024 Highlights, p. 32", "FY2024"),
            "energy_storage_deployed": item(31.4, "GWh", FY2024_10K, "MD&A, Overview and 2024 Highlights, p. 32", "FY2024"),
        },
    },
    "FY2025": {
        "revenue": {
            "automotive_sales": item(65821, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "2025-12-31"),
            "regulatory_credits": item(1993, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "2025-12-31"),
            "automotive_leasing": item(1712, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "2025-12-31"),
            "energy_generation_and_storage": item(12771, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "2025-12-31"),
            "services_and_other": item(12530, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "2025-12-31"),
            "total": item(94827, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "2025-12-31"),
        },
        "cost_of_revenue": {
            "automotive": item(57165, "USD millions", FY2025_10K, "Consolidated Statements of Operations, total automotive cost of revenues, p. 50", "2025-12-31"),
            "energy_generation_and_storage": item(8969, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "2025-12-31"),
            "services_and_other": item(11599, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "2025-12-31"),
        },
        "expenses_and_cash_flow": {
            "research_and_development": item(6411, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "FY2025"),
            "selling_general_and_administrative": item(5834, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "FY2025"),
            "restructuring_and_other": item(494, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "FY2025"),
            "depreciation_amortization_and_impairment": item(6148, "USD millions", FY2025_10K, "Consolidated Statements of Cash Flows, p. 53; combined reported line", "FY2025"),
            "stock_based_compensation": item(2825, "USD millions", FY2025_10K, "Consolidated Statements of Cash Flows, p. 53", "FY2025"),
            "interest_expense": item(338, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50 (reported as $(338))", "FY2025"),
            "income_tax": item(1423, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "FY2025"),
            "operating_cash_flow": item(14747, "USD millions", FY2025_10K, "Consolidated Statements of Cash Flows, p. 53", "FY2025"),
            "capex": item(8527, "USD millions", FY2025_10K, "Consolidated Statements of Cash Flows, purchases of property and equipment excluding finance leases, net of sales, p. 53", "FY2025"),
        },
        "net_income": item(3855, "USD millions", FY2025_10K, "Consolidated Statements of Operations, p. 50", "FY2025"),
        "balance_sheet": {
            "cash_and_cash_equivalents": item(16513, "USD millions", FY2025_10K, "Consolidated Balance Sheets, p. 49", "2025-12-31"),
            "short_term_investments": item(27546, "USD millions", FY2025_10K, "Consolidated Balance Sheets, p. 49", "2025-12-31"),
            "accounts_receivable": item(4576, "USD millions", FY2025_10K, "Consolidated Balance Sheets, p. 49", "2025-12-31"),
            "inventory": item(12392, "USD millions", FY2025_10K, "Consolidated Balance Sheets, p. 49", "2025-12-31"),
            "property_plant_and_equipment_net": item(40643, "USD millions", FY2025_10K, "Consolidated Balance Sheets, p. 49", "2025-12-31"),
            "digital_assets": item(1008, "USD millions", FY2025_10K, "Consolidated Balance Sheets, p. 49", "2025-12-31"),
            "accounts_payable": item(13371, "USD millions", FY2025_10K, "Consolidated Balance Sheets, p. 49", "2025-12-31"),
            "total_debt_and_finance_leases": item(8376, "USD millions", FY2025_10K, "Consolidated Balance Sheets: current portion plus non-current debt and finance leases, p. 49", "2025-12-31"),
            "finance_lease_liabilities": item(223, "USD millions", FY2025_10K, "Note 13, Leases, total finance lease liabilities, p. 76", "2025-12-31"),
            "operating_lease_liabilities": item(6343, "USD millions", FY2025_10K, "Note 13, Leases, total operating lease liabilities, p. 76", "2025-12-31"),
            "noncontrolling_interests": item(670, "USD millions", FY2025_10K, "Consolidated Balance Sheets, p. 49", "2025-12-31"),
            "total_liabilities": item(54941, "USD millions", FY2025_10K, "Consolidated Balance Sheets, total liabilities, p. 49", "2025-12-31"),
            "redeemable_noncontrolling_interests": item(58, "USD millions", FY2025_10K, "Consolidated Balance Sheets, redeemable noncontrolling interests in subsidiaries, p. 49", "2025-12-31"),
            "total_equity": item(82807, "USD millions", FY2025_10K, "Consolidated Statements of Redeemable Noncontrolling Interests and Equity, total equity, p. 52", "2025-12-31"),
            "total_assets": item(137806, "USD millions", FY2025_10K, "Consolidated Balance Sheets, p. 49", "2025-12-31"),
        },
        "shares": {
            "diluted_weighted_average": item(3528, "millions of shares", FY2025_10K, "Consolidated Statements of Operations, p. 50", "FY2025"),
            "period_end_shares_outstanding": item(3751, "millions of shares", FY2025_10K, "Consolidated Balance Sheets, common stock outstanding, p. 49", "2025-12-31"),
        },
        "operating_data": {
            "vehicle_deliveries": item(1.64, "millions of vehicles (approximately)", FY2025_10K, "MD&A, Overview and 2025 Highlights, p. 31", "FY2025"),
            "vehicle_production": item(1.66, "millions of vehicles (approximately)", FY2025_10K, "MD&A, Overview and 2025 Highlights, p. 31", "FY2025"),
            "energy_storage_deployed": item(46.7, "GWh", FY2025_10K, "MD&A, Overview and 2025 Highlights, p. 31", "FY2025"),
        },
    },
}

# Candidates only: these remain in HISTORY and are not adjusted out.
NORMALIZATION_CANDIDATES = {
    "FY2025_restructuring_and_other": item(494, "USD millions", FY2025_10K, "Consolidated Statements of Operations, restructuring and other, p. 50", "FY2025", "normalization"),
    "FY2025_impairment_within_combined_cash_flow_line": item(None, "USD millions", FY2025_10K, "Consolidated Statements of Cash Flows, depreciation, amortization and impairment is a combined $6,148M line, p. 53; stand-alone impairment amount NOT FOUND", "FY2025", "normalization"),
    "FY2025_digital_assets_loss_net": item(68, "USD millions", FY2025_10K, "Consolidated Statements of Cash Flows, digital assets loss (gain), net, p. 53; Note 3, p. 69", "FY2025", "normalization"),
    "FY2025_foreign_currency_transaction_unrealized_loss": item(452, "USD millions", FY2025_10K, "Consolidated Statements of Cash Flows, foreign currency transaction net unrealized loss, p. 53", "FY2025", "normalization"),
    "FY2025_change_in_valuation_allowances": item(389, "USD millions", FY2025_10K, "Note 12, income-tax reconciliation, p. 84", "FY2025", "normalization"),
    "FY2025_other_tax_adjustments": item(139, "USD millions", FY2025_10K, "Note 12, income-tax reconciliation, p. 84", "FY2025", "normalization"),
    "FY2025_goodwill_impairment": item(0, "USD millions", FY2025_10K, "Note 2, Goodwill: no impairment recognized, p. 65", "FY2025", "normalization"),
}

# Analyst-selected valuation treatments. These do not alter reported history.
ANALYST_DECISIONS = {
    "FY2025_debt_used_in_equity_bridge": {
        "decision": item(8376, "USD millions", FY2025_10K, "Consolidated Balance Sheets, current portion of debt and finance leases ($1,640M) plus non-current debt and finance leases ($6,736M), p. 49", "2025-12-31", "normalization"),
        "reason": "Finance leases are a form of borrowing. Operating leases are NOT treated as debt because their cost is already in operating expenses.",
    },
    "FY2025_normalized_operating_income": {
        "decision": item(4849, "USD millions", FY2025_10K, "Calculated as FY2025 reported operating income ($4,355M) plus restructuring and other charge ($494M); Consolidated Statements of Operations, p. 50", "FY2025", "normalization"),
        "reason": "Restructuring is a one-time cost, not part of Tesla's normal operations.",
        "note": "Tesla also reported restructuring in FY2024, so this could recur.",
    },
}

NOTES = [
    "The historical assumptions file agrees with the 10-K history for revenue, net income, inventory, PP&E, and stockholders' equity.",
    "Its capex values are rounded MD&A figures; this file uses the exact cash-flow-statement amounts. This is a rounding/presentation difference, not a silent replacement.",
    "Tesla reports depreciation, amortization, and impairment as one combined cash-flow line; a stand-alone depreciation-and-amortization amount was NOT FOUND.",
    "Total debt is labeled total_debt_and_finance_leases because that is the balance-sheet presentation. Finance lease liabilities are separately supplied and therefore overlap that total.",
    "FY2024 and FY2025 vehicle production and deliveries are only stated approximately in the respective 10-Ks; the reported precision is retained.",
]

# Independent FY2025 10-K total-line controls used by the runnable check below.
REPORTED_FY2025_TOTALS = {
    "total_revenue": item(94827, "USD millions", FY2025_10K, "Consolidated Statements of Operations, total revenues, p. 50", "FY2025"),
    "net_income": item(3855, "USD millions", FY2025_10K, "Consolidated Statements of Operations, net income, p. 50", "FY2025"),
    "total_assets": item(137806, "USD millions", FY2025_10K, "Consolidated Balance Sheets, total assets, p. 49", "2025-12-31"),
}


def check_fy2025_reported_totals():
    """Print PASS/FAIL checks against the FY2025 10-K reported totals."""
    fy = HISTORY["FY2025"]
    checks = {
        "total revenue": (fy["revenue"]["total"]["value"], REPORTED_FY2025_TOTALS["total_revenue"]["value"]),
        "net income": (fy["net_income"]["value"], REPORTED_FY2025_TOTALS["net_income"]["value"]),
        "total assets": (fy["balance_sheet"]["total_assets"]["value"], REPORTED_FY2025_TOTALS["total_assets"]["value"]),
    }
    for label, (actual, reported) in checks.items():
        print(f"FY2025 {label}: {'PASS' if actual == reported else 'FAIL'}")


def check_reconciliations():
    """Print revenue and balance-sheet PASS/FAIL reconciliations by year."""
    revenue_lines = (
        "automotive_sales",
        "regulatory_credits",
        "automotive_leasing",
        "energy_generation_and_storage",
        "services_and_other",
    )
    for fiscal_year in ("FY2023", "FY2024", "FY2025"):
        fy = HISTORY[fiscal_year]
        revenue = fy["revenue"]
        balance_sheet = fy["balance_sheet"]
        revenue_total = sum(revenue[line]["value"] for line in revenue_lines)
        liabilities_redeemable_interests_and_equity = (
            balance_sheet["total_liabilities"]["value"]
            + balance_sheet["redeemable_noncontrolling_interests"]["value"]
            + balance_sheet["total_equity"]["value"]
        )
        print(
            f"{fiscal_year} revenue lines equal total revenue: "
            f"{'PASS' if revenue_total == revenue['total']['value'] else 'FAIL'}"
        )
        print(
            f"{fiscal_year} total assets equal total liabilities plus redeemable noncontrolling interests plus total equity: "
            f"{'PASS' if balance_sheet['total_assets']['value'] == liabilities_redeemable_interests_and_equity else 'FAIL'}"
        )


def print_fy2025_normalized_operating_income():
    """Print FY2025 reported and analyst-normalized operating income."""
    fy = HISTORY["FY2025"]
    reported_operating_income = (
        fy["revenue"]["total"]["value"]
        - sum(fy["cost_of_revenue"][line]["value"] for line in fy["cost_of_revenue"])
        - fy["expenses_and_cash_flow"]["research_and_development"]["value"]
        - fy["expenses_and_cash_flow"]["selling_general_and_administrative"]["value"]
        - fy["expenses_and_cash_flow"]["restructuring_and_other"]["value"]
    )
    normalized_operating_income = (
        reported_operating_income
        + fy["expenses_and_cash_flow"]["restructuring_and_other"]["value"]
    )
    print(
        "FY2025 operating income (USD millions): "
        f"reported {reported_operating_income:,} | normalized {normalized_operating_income:,}"
    )


if __name__ == "__main__":
    check_fy2025_reported_totals()
    check_reconciliations()
    print_fy2025_normalized_operating_income()
