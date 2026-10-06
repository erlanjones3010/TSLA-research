"""Tesla FY2026–FY2030 three-statement forecast (USD millions, except operating data)."""

from copy import deepcopy

from tesla_inputs import ANALYST_DECISIONS, HISTORY


YEARS = (2026, 2027, 2028, 2029, 2030)
STATUS = "DRAFT – suggested by Claude, Erlan to confirm"


def driver(values, basis, challenge, evidence_that_would_change_it):
    return {
        "values": values,
        "basis": basis,
        "challenge": challenge,
        "evidence_that_would_change_it": evidence_that_would_change_it,
        "status": STATUS,
    }


# Historical inputs are read only from tesla_inputs.py; no historical values are retyped here.
BASE = HISTORY["FY2025"]
BASE_REVENUE = BASE["revenue"]
BASE_COSTS = BASE["cost_of_revenue"]
BASE_EXPENSES = BASE["expenses_and_cash_flow"]
BASE_BALANCE_SHEET = BASE["balance_sheet"]
BASE_DELIVERIES = BASE["operating_data"]["vehicle_deliveries"]["value"]
BASE_ENERGY_GWH = BASE["operating_data"]["energy_storage_deployed"]["value"]
BASE_CASH_AND_INVESTMENTS = (
    BASE_BALANCE_SHEET["cash_and_cash_equivalents"]["value"]
    + BASE_BALANCE_SHEET["short_term_investments"]["value"]
)
BASE_AUTOMOTIVE_EX_CREDITS = (
    BASE_REVENUE["automotive_sales"]["value"]
    + BASE_REVENUE["automotive_leasing"]["value"]
)
BASE_COST_OF_REVENUE = sum(line["value"] for line in BASE_COSTS.values())
BASE_DEPRECIATION = BASE_EXPENSES["depreciation_amortization_and_impairment"]["value"]
BASE_OTHER_ASSETS = (
    BASE_BALANCE_SHEET["total_assets"]["value"]
    - BASE_CASH_AND_INVESTMENTS
    - BASE_BALANCE_SHEET["accounts_receivable"]["value"]
    - BASE_BALANCE_SHEET["inventory"]["value"]
    - BASE_BALANCE_SHEET["property_plant_and_equipment_net"]["value"]
)
BASE_OTHER_LIABILITIES = (
    BASE_BALANCE_SHEET["total_liabilities"]["value"]
    - BASE_BALANCE_SHEET["accounts_payable"]["value"]
    - BASE_BALANCE_SHEET["total_debt_and_finance_leases"]["value"]
)


# The original margin path is retained intact as the downside case.
DOWNSIDE_DRIVERS = {
    "vehicle_deliveries_growth": driver(
        {2026: 0.03, 2027: 0.06, 2028: 0.07, 2029: 0.06, 2030: 0.05},
        "Deliveries fell in 2025; assumes a slow recovery, not a return to fast growth.",
        "Can Tesla add volume without further price concessions?",
        "Quarterly delivery reports and new-model launches.",
    ),
    "automotive_sales_revenue_per_vehicle_growth": driver(
        {2026: -0.01, 2027: 0.00, 2028: 0.00, 2029: 0.00, 2030: 0.00},
        "2025 prices fell on mix and incentives; assumes pricing stabilizes.",
        "Does mix shift to lower-priced vehicles or do incentives remain elevated?",
        "Average selling-price commentary in 10-Qs and price cuts.",
    ),
    "regulatory_credits": driver(
        {2026: 1200.0, 2027: 800.0, 2028: 500.0, 2029: 300.0, 2030: 200.0},
        "Credit demand from other automakers is expected to shrink as rules loosen and competitors sell more EVs. Tesla's FY2025 10-K says governmental actions including the OBBBA restricted certain credit programs and that revenue also depends on other automakers' demand.",
        "Could regulation tighten or competitors remain short of compliance credits?",
        "Regulatory-credit revenue in 10-Qs.",
    ),
    "automotive_leasing_revenue_growth": driver(
        {year: -0.05 for year in YEARS},
        "Leasing has been shrinking as a share of automotive revenue.",
        "Could leasing grow again as affordability becomes more important?",
        "Quarterly leasing revenue and leasing-program disclosures.",
    ),
    "energy_gwh_growth": driver(
        {2026: 0.25, 2027: 0.20, 2028: 0.18, 2029: 0.15, 2030: 0.12},
        "Strong 2025 growth fades as the business scales.",
        "Can manufacturing capacity and grid demand support this deployment path?",
        "Quarterly deployment numbers and Megapack-factory ramp disclosures.",
    ),
    "energy_revenue_per_gwh_growth": driver(
        {year: -0.03 for year in YEARS},
        "Prices fall with competition as the energy business scales.",
        "Could product mix or storage scarcity support higher revenue per GWh?",
        "Quarterly deployment numbers, revenue disclosure, and Megapack-factory ramp.",
    ),
    "services_and_other_revenue_growth": driver(
        {year: 0.10 for year in YEARS},
        "Grows with the fleet through Supercharging, service, insurance, and used cars.",
        "Can service capacity and monetization keep pace with the installed fleet?",
        "Quarterly services revenue and fleet data.",
    ),
    "automotive_gross_margin_excluding_credits": driver(
        {2026: 0.155, 2027: 0.160, 2028: 0.165, 2029: 0.170, 2030: 0.170},
        "Slow improvement from cost cuts and utilization; no return to 2022-level margins.",
        "Will tariffs, price cuts, or underutilization outweigh cost reductions?",
        "Automotive gross margin in 10-Qs, tariff costs, and price cuts.",
    ),
    "energy_gross_margin": driver(
        {2026: 0.29, 2027: 0.28, 2028: 0.28, 2029: 0.27, 2030: 0.27},
        "Tariffs and competition pressure margins slightly.",
        "Can scale, software, and manufacturing improvements offset pricing pressure?",
        "Energy gross margin, tariffs, and competitor pricing.",
    ),
    "services_and_other_gross_margin": driver(
        {year: 0.075 for year in YEARS},
        "Held at the FY2025 actual level.",
        "Will service utilization and insurance economics improve or deteriorate?",
        "Quarterly services gross-profit disclosure.",
    ),
    "rd_percent_revenue": driver(
        {2026: 0.070, 2027: 0.070, 2028: 0.065, 2029: 0.060, 2030: 0.060},
        "Lab 11 operating-cost assumption, kept as is.",
        "Could AI, robotaxi, and Optimus spending remain structurally higher?",
        "R&D expense in 10-Qs and management spending commentary.",
    ),
    "sga_percent_revenue": driver(
        {2026: 0.060, 2027: 0.058, 2028: 0.056, 2029: 0.055, 2030: 0.055},
        "Lab 11 operating-cost assumption, kept as is.",
        "Are overhead savings achievable while the business adds new products and services?",
        "SG&A expense in 10-Qs and headcount commentary.",
    ),
    "capex": driver(
        {2026: 20500.0, 2027: 18000.0, 2028: 15000.0, 2029: 13000.0, 2030: 12000.0},
        "Lab 11 capex assumption, kept as is.",
        "Could AI infrastructure, factories, and new products require more investment?",
        "Capex guidance, factory plans, and cash-flow statements.",
    ),
    "depreciation_percent_opening_ppe": driver(
        {"rate": BASE_DEPRECIATION
         / BASE_BALANCE_SHEET["property_plant_and_equipment_net"]["value"]},
        "FY2025 D&A divided by FY2025 PP&E, per the Lab 11 method.",
        "Does the asset mix change useful lives or cause impairments?",
        "D&A, impairments, and PP&E disclosures in 10-Qs and 10-Ks.",
    ),
    "incremental_depreciation_from_new_capex": driver(
        {"fy2025_depreciation_embedded_in_segment_margins": BASE_DEPRECIATION},
        "New factories, AI compute, and fleet assets add depreciation that FY2025 margins do not include.",
        "Will newly deployed assets generate enough volume and gross profit to absorb their depreciation?",
        "D&A, capex, asset-utilization, and segment-margin disclosures in 10-Qs and 10-Ks.",
    ),
    "tax_rate": driver(
        {year: 0.25 for year in YEARS},
        "Normalized tax-rate assumption.",
        "Will jurisdictional mix, tax credits, or valuation allowances change the rate?",
        "Effective tax rate and tax-footnote updates.",
    ),
    "working_capital": driver(
        {
            "inventory_days": 58.19,
            "receivable_days": BASE_BALANCE_SHEET["accounts_receivable"]["value"] / BASE_REVENUE["total"]["value"] * 365,
            "payable_days": BASE_BALANCE_SHEET["accounts_payable"]["value"] / BASE_COST_OF_REVENUE * 365,
            "other_assets": "flat at FY2025", "other_liabilities": "flat at FY2025",
        },
        "Inventory is held at 58.19 days of cost of revenue; receivables and payables use FY2025 days; other assets and liabilities are flat.",
        "Will faster growth consume more working capital or improve supplier terms?",
        "Quarterly balance sheets, inventory turns, and supplier-payment trends.",
    ),
    "liquidity_and_debt": driver(
        {"minimum_cash_and_investments": 10000.0, "revolver_limit": 6430.0, "revolver_rate": 0.06, "debt": BASE_BALANCE_SHEET["total_debt_and_finance_leases"]["value"]},
        "Minimum cash, revolver terms, and flat debt are the Lab 11 assumptions; debt follows the FY2025 analyst decision.",
        "Will capex or losses require funding beyond the revolver?",
        "Debt issuance/repayment, liquidity disclosures, and cash-flow results.",
    ),
    "diluted_shares": driver(
        {year: BASE["shares"]["diluted_weighted_average"]["value"] for year in YEARS},
        "FY2025 diluted shares held constant.",
        "Will compensation, option exercises, or repurchases change dilution?",
        "Diluted-share counts in 10-Qs and equity-compensation disclosures.",
    ),
}

# DOWNSIDE retains the original values; this documents the common case rationale.
for _driver_name in (
    "automotive_gross_margin_excluding_credits",
    "energy_gross_margin",
    "rd_percent_revenue",
    "sga_percent_revenue",
):
    DOWNSIDE_DRIVERS[_driver_name]["basis"] = (
        "Margins stay near FY2025 levels; cost cuts and scale do not offset price pressure, tariffs, and AI spending."
    )

# BASE changes only the four requested margin/operating-cost driver paths.
BASE_DRIVERS = deepcopy(DOWNSIDE_DRIVERS)
BASE_DRIVERS.update({
    "automotive_gross_margin_excluding_credits": driver(
        {2026: 0.160, 2027: 0.175, 2028: 0.190, 2029: 0.200, 2030: 0.200},
        "Partial recovery toward Tesla's 2022–2023 levels from cost cuts, cheaper models, and better factory utilization.",
        "Can cost reductions and utilization overcome competitive pricing and tariffs?",
        "Automotive gross margin in 10-Qs, further price cuts, and tariff costs.",
    ),
    "energy_gross_margin": driver(
        {year: 0.30 for year in YEARS},
        "FY2025 was 29.8%; assumes Megapack scale offsets price competition.",
        "Will price competition or cell tariffs exceed scale benefits?",
        "Energy segment margin in 10-Qs and tariff impact on battery cells.",
    ),
    "rd_percent_revenue": driver(
        {2026: 0.068, 2027: 0.065, 2028: 0.062, 2029: 0.058, 2030: 0.055},
        "R&D grows in dollars but more slowly than revenue.",
        "Could AI, robotaxi, and Optimus spending remain structurally higher?",
        "R&D expense in 10-Qs and management spending commentary.",
    ),
    "sga_percent_revenue": driver(
        {2026: 0.060, 2027: 0.057, 2028: 0.054, 2029: 0.052, 2030: 0.050},
        "Scale benefits as revenue grows.",
        "Are overhead savings achievable while the business adds new products and services?",
        "SG&A expense in 10-Qs and headcount commentary.",
    ),
})

# UPSIDE is BASE plus the potential commercialization of Robotaxi and paid FSD.
UPSIDE_DRIVERS = deepcopy(BASE_DRIVERS)
UPSIDE_DRIVERS.update({
    "autonomy_and_software_revenue": driver(
        {2026: 0.0, 2027: 2000.0, 2028: 8000.0, 2029: 20000.0, 2030: 40000.0},
        "Assumes Robotaxi and paid FSD scale commercially starting in 2027 across multiple cities, with regulatory approval.",
        "No large-scale paid driverless service exists yet; timing and regulation are uncertain.",
        "Robotaxi launches and city approvals, paid FSD subscriber numbers, safety and regulatory decisions, and Tesla 10-Q disclosures.",
    ),
    "autonomy_and_software_gross_margin": driver(
        {year: 0.50 for year in YEARS},
        "Software-like economics, but fleet, insurance, cleaning, and compute costs keep it below pure software margins.",
        "Can the service achieve software-like economics after fleet operations and compute costs?",
        "Robotaxi operating metrics, insurance and fleet costs, compute spending, and Tesla 10-Q disclosures.",
    ),
})
SCENARIO_DRIVERS = {
    "BASE": BASE_DRIVERS,
    "DOWNSIDE": DOWNSIDE_DRIVERS,
    "UPSIDE": UPSIDE_DRIVERS,
}
# BASE is the default scenario for imports and direct execution.
DRIVERS = SCENARIO_DRIVERS["BASE"]


def base_reported_operating_income():
    """Derive reported FY2025 EBIT from imported revenue, cost, and expense lines."""
    return (
        BASE_REVENUE["total"]["value"] - BASE_COST_OF_REVENUE
        - BASE_EXPENSES["research_and_development"]["value"]
        - BASE_EXPENSES["selling_general_and_administrative"]["value"]
        - BASE_EXPENSES["restructuring_and_other"]["value"]
    )


def assert_checks(results, scenario="BASE"):
    """Print PASS/FAIL checks and stop immediately if any required check fails."""
    expected_revenue = sum(BASE_REVENUE[line]["value"] for line in (
        "automotive_sales", "regulatory_credits", "automotive_leasing",
        "energy_generation_and_storage", "services_and_other",
    ))
    base_normalized_ebit = base_reported_operating_income() + BASE_EXPENSES["restructuring_and_other"]["value"]
    expected_normalized_ebit = ANALYST_DECISIONS["FY2025_normalized_operating_income"]["decision"]["value"]
    checks = [
        ("Base FY2025 revenue by segment equals imported total revenue", expected_revenue == BASE_REVENUE["total"]["value"]),
        ("Base FY2025 normalized operating income equals ANALYST_DECISIONS", abs(base_normalized_ebit - expected_normalized_ebit) < 0.000001),
    ]
    for year in YEARS:
        balance_sheet_difference = (
            results[year]["Cash + Investments"] + results[year]["Receivables"]
            + results[year]["Inventory"] + results[year]["PP&E"] + results[year]["Other Assets"]
            - results[year]["Payables"] - results[year]["Debt"] - results[year]["Revolver"]
            - results[year]["Other Liabilities"] - results[year]["Redeemable NCI"]
            - results[year]["Equity"]
        )
        checks.append((f"FY{year}E balance sheet balances", abs(balance_sheet_difference) < 0.000001))
        checks.append((f"FY{year}E CFS ending cash equals balance-sheet cash", abs(results[year]["Cash Check"]) < 0.000001))
    for label, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} — {scenario}: {label}")
    failures = [label for label, passed in checks if not passed]
    if failures:
        raise ValueError("Forecast checks failed: " + "; ".join(failures))


def run_forecast(scenario="BASE", drivers=None):
    """Run the segment-driven linked forecast using minimum-cash/revolver mechanics."""
    if drivers is None:
        if scenario not in SCENARIO_DRIVERS:
            raise ValueError(f"Unknown scenario: {scenario}")
        drivers = SCENARIO_DRIVERS[scenario]
    data = deepcopy(drivers)
    opening = {
        "cash": BASE_CASH_AND_INVESTMENTS,
        "receivables": BASE_BALANCE_SHEET["accounts_receivable"]["value"],
        "inventory": BASE_BALANCE_SHEET["inventory"]["value"],
        "ppe": BASE_BALANCE_SHEET["property_plant_and_equipment_net"]["value"],
        "other_assets": BASE_OTHER_ASSETS,
        "payables": BASE_BALANCE_SHEET["accounts_payable"]["value"],
        "debt": ANALYST_DECISIONS["FY2025_debt_used_in_equity_bridge"]["decision"]["value"],
        "revolver": 0.0,
        "other_liabilities": BASE_OTHER_LIABILITIES,
        "redeemable_nci": BASE_BALANCE_SHEET["redeemable_noncontrolling_interests"]["value"],
        "equity": BASE_BALANCE_SHEET["total_equity"]["value"],
        "deliveries": BASE_DELIVERIES,
        "energy_gwh": BASE_ENERGY_GWH,
        "auto_revenue_per_vehicle": BASE_REVENUE["automotive_sales"]["value"] / BASE_DELIVERIES,
        "energy_revenue_per_gwh": BASE_REVENUE["energy_generation_and_storage"]["value"] / BASE_ENERGY_GWH,
        "leasing_revenue": BASE_REVENUE["automotive_leasing"]["value"],
    }
    interest_rate = BASE_EXPENSES["interest_expense"]["value"] / opening["debt"]
    results = {}

    for year in YEARS:
        opening_ppe, opening_inventory = opening["ppe"], opening["inventory"]
        opening_receivables, opening_payables = opening["receivables"], opening["payables"]
        opening_cash, opening_revolver = opening["cash"], opening["revolver"]

        opening["deliveries"] *= 1 + data["vehicle_deliveries_growth"]["values"][year]
        opening["auto_revenue_per_vehicle"] *= 1 + data["automotive_sales_revenue_per_vehicle_growth"]["values"][year]
        automotive_sales = opening["deliveries"] * opening["auto_revenue_per_vehicle"]
        regulatory_credits = data["regulatory_credits"]["values"][year]
        opening["leasing_revenue"] *= 1 + data["automotive_leasing_revenue_growth"]["values"][year]
        automotive_leasing = opening["leasing_revenue"]
        opening["energy_gwh"] *= 1 + data["energy_gwh_growth"]["values"][year]
        opening["energy_revenue_per_gwh"] *= 1 + data["energy_revenue_per_gwh_growth"]["values"][year]
        energy_revenue = opening["energy_gwh"] * opening["energy_revenue_per_gwh"]
        services_revenue = BASE_REVENUE["services_and_other"]["value"] if year == YEARS[0] else results[year - 1]["Services & Other Revenue"]
        services_revenue *= 1 + data["services_and_other_revenue_growth"]["values"][year]
        autonomy_revenue = data.get("autonomy_and_software_revenue", {"values": {year: 0.0}})["values"][year]

        automotive_gp_ex_credits = (automotive_sales + automotive_leasing) * data["automotive_gross_margin_excluding_credits"]["values"][year]
        regulatory_credits_gp = regulatory_credits
        energy_gp = energy_revenue * data["energy_gross_margin"]["values"][year]
        services_gp = services_revenue * data["services_and_other_gross_margin"]["values"][year]
        autonomy_gp = autonomy_revenue * data.get("autonomy_and_software_gross_margin", {"values": {year: 0.0}})["values"][year]
        total_revenue = automotive_sales + regulatory_credits + automotive_leasing + energy_revenue + services_revenue + autonomy_revenue
        total_gross_profit = automotive_gp_ex_credits + regulatory_credits_gp + energy_gp + services_gp + autonomy_gp
        cost_of_revenue = total_revenue - total_gross_profit
        rd = total_revenue * data["rd_percent_revenue"]["values"][year]
        sga = total_revenue * data["sga_percent_revenue"]["values"][year]
        depreciation = opening_ppe * data["depreciation_percent_opening_ppe"]["values"]["rate"]
        incremental_depreciation = depreciation - data["incremental_depreciation_from_new_capex"]["values"]["fy2025_depreciation_embedded_in_segment_margins"]
        old_ebit = total_gross_profit - rd - sga
        ebit = old_ebit - incremental_depreciation
        interest = opening["debt"] * interest_rate + opening_revolver * data["liquidity_and_debt"]["values"]["revolver_rate"]
        pretax_income = ebit - interest
        taxes = max(0.0, pretax_income) * data["tax_rate"]["values"][year]
        net_income = pretax_income - taxes

        wc = data["working_capital"]["values"]
        receivables = total_revenue * wc["receivable_days"] / 365
        inventory = cost_of_revenue * wc["inventory_days"] / 365
        payables = cost_of_revenue * wc["payable_days"] / 365
        ppe = opening_ppe + data["capex"]["values"][year] - depreciation
        increase_in_working_capital = (receivables - opening_receivables) + (inventory - opening_inventory) - (payables - opening_payables)
        cash_before_revolver = opening_cash + net_income + depreciation - increase_in_working_capital - data["capex"]["values"][year]
        minimum_cash = data["liquidity_and_debt"]["values"]["minimum_cash_and_investments"]
        if cash_before_revolver < minimum_cash:
            borrowing_repayment = minimum_cash - cash_before_revolver
            revolver = opening_revolver + borrowing_repayment
            if revolver > data["liquidity_and_debt"]["values"]["revolver_limit"]:
                raise ValueError(f"FY{year}E revolver limit exceeded: {revolver:,.1f}")
            cash = minimum_cash
        else:
            repayment = min(opening_revolver, cash_before_revolver - minimum_cash)
            borrowing_repayment = -repayment
            revolver = opening_revolver - repayment
            cash = cash_before_revolver - repayment
        change_in_cash = cash - opening_cash
        equity = opening["equity"] + net_income
        assets = cash + receivables + inventory + ppe + opening["other_assets"]
        liabilities_and_equity = (
            payables + opening["debt"] + revolver + opening["other_liabilities"]
            + opening["redeemable_nci"] + equity
        )
        old_fcff = old_ebit * (1 - data["tax_rate"]["values"][year]) + depreciation - data["capex"]["values"][year] - increase_in_working_capital
        fcff = ebit * (1 - data["tax_rate"]["values"][year]) + depreciation - data["capex"]["values"][year] - increase_in_working_capital
        results[year] = {
            "Automotive Sales Revenue": automotive_sales, "Regulatory Credits Revenue": regulatory_credits,
            "Automotive Leasing Revenue": automotive_leasing, "Energy Revenue": energy_revenue,
            "Services & Other Revenue": services_revenue, "Autonomy & Software Revenue": autonomy_revenue,
            "Total Revenue": total_revenue,
            "Automotive GP ex Credits": automotive_gp_ex_credits, "Regulatory Credits GP": regulatory_credits_gp,
            "Energy GP": energy_gp, "Services & Other GP": services_gp, "Autonomy & Software GP": autonomy_gp,
            "Total Gross Profit": total_gross_profit,
            "Incremental depreciation from new capex": incremental_depreciation, "R&D": rd, "SG&A": sga,
            "Old EBIT": old_ebit, "EBIT": ebit, "Interest": interest, "Taxes": taxes,
            "Net Income": net_income, "Cash + Investments": cash, "Receivables": receivables,
            "Inventory": inventory, "PP&E": ppe, "Other Assets": opening["other_assets"], "Payables": payables,
            "Debt": opening["debt"], "Revolver": revolver, "Other Liabilities": opening["other_liabilities"],
            "Redeemable NCI": opening["redeemable_nci"], "Equity": equity, "Net Income (CFS)": net_income,
            "D&A": depreciation, "Increase in Working Capital": increase_in_working_capital,
            "Capex": data["capex"]["values"][year], "Borrowing/(Repayment)": borrowing_repayment,
            "Change in Cash": change_in_cash, "Old FCFF": old_fcff, "FCFF": fcff, "Balance Check": assets - liabilities_and_equity,
            "Cash Check": opening_cash + net_income + depreciation - increase_in_working_capital
            - data["capex"]["values"][year] + borrowing_repayment - cash,
        }
        opening.update({"cash": cash, "receivables": receivables, "inventory": inventory, "ppe": ppe,
                        "payables": payables, "revolver": revolver, "equity": equity})
    return results


def print_table(results, title, rows):
    print(f"\n{title} (USD millions)")
    print(f"{'Line':<31}" + "".join(f"FY{year}E".rjust(14) for year in YEARS))
    for row in rows:
        print(f"{row:<31}" + "".join(f"{results[year][row]:>14,.1f}" for year in YEARS))


def print_depreciation_impact(results):
    """Print the old fixed-margin treatment against the new depreciation treatment."""
    print("\nDEPRECIATION TREATMENT IMPACT (USD millions)")
    print(f"{'Year':<10}{'Old EBIT':>14}{'New EBIT':>14}{'Old FCFF':>14}{'New FCFF':>14}")
    for year in YEARS:
        print(f"FY{year}E{results[year]['Old EBIT']:>14,.1f}{results[year]['EBIT']:>14,.1f}"
              f"{results[year]['Old FCFF']:>14,.1f}{results[year]['FCFF']:>14,.1f}")


def print_assumptions_added():
    print("\nASSUMPTIONS ADDED (not specified in the task)")
    print("- Interest is modeled only as interest expense: FY2025 interest expense divided by FY2025 debt; no interest income is forecast.")
    print("- Redeemable noncontrolling interests remain at the FY2025 reported balance so the balance sheet reconciles.")
    print("- Equity increases only by forecast net income; no dividends, share issuance, repurchases, or other equity movements are forecast.")
    print("- Working capital is defined as receivables plus inventory less payables; all other assets and other liabilities stay flat as instructed.")
    print("- Segment gross margins include FY2025 D&A only; incremental D&A from new capex is charged below gross profit.")


def main():
    results = run_forecast("BASE")
    downside_results = run_forecast("DOWNSIDE")
    upside_results = run_forecast("UPSIDE")
    print("TESLA FIVE-YEAR THREE-STATEMENT FORECAST — BASE SCENARIO")
    print("Base FY2025 normalized EBIT: "
          f"{ANALYST_DECISIONS['FY2025_normalized_operating_income']['decision']['value']:,.1f} "
          f"(reported {base_reported_operating_income():,.1f} + restructuring {BASE_EXPENSES['restructuring_and_other']['value']:,.1f})")
    print_table(results, "INCOME STATEMENT", [
        "Automotive Sales Revenue", "Regulatory Credits Revenue", "Automotive Leasing Revenue",
        "Energy Revenue", "Services & Other Revenue", "Autonomy & Software Revenue", "Total Revenue", "Automotive GP ex Credits",
        "Regulatory Credits GP", "Energy GP", "Services & Other GP", "Autonomy & Software GP", "Total Gross Profit",
        "Incremental depreciation from new capex", "R&D",
        "SG&A", "EBIT", "Interest", "Taxes", "Net Income",
    ])
    print_table(results, "BALANCE SHEET", [
        "Cash + Investments", "Receivables", "Inventory", "PP&E", "Other Assets", "Payables", "Debt",
        "Revolver", "Other Liabilities", "Redeemable NCI", "Equity",
    ])
    print_table(results, "CASH FLOW STATEMENT", [
        "Net Income (CFS)", "D&A", "Increase in Working Capital", "Capex", "Borrowing/(Repayment)",
        "Change in Cash", "FCFF",
    ])
    print_depreciation_impact(results)
    print("\nCHECKS")
    assert_checks(results, "BASE")
    assert_checks(downside_results, "DOWNSIDE")
    assert_checks(upside_results, "UPSIDE")
    print_assumptions_added()


if __name__ == "__main__":
    main()
