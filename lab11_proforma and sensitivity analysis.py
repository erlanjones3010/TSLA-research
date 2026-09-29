"""Lab 11 — Tesla five-year pro forma and one-at-a-time sensitivity analysis.

USD millions, except per-share data.
"""

from copy import deepcopy


YEARS = [2026, 2027, 2028, 2029, 2030]

BASE_INPUTS = {
    "growth": {2026: .15, 2027: .15, 2028: .12, 2029: .10, 2030: .08},
    "gross_margin": {2026: .180, 2027: .190, 2028: .200, 2029: .210, 2030: .215},
    "sga_percent_revenue": {2026: .060, 2027: .058, 2028: .056, 2029: .055, 2030: .055},
    "rd_percent_revenue": {2026: .070, 2027: .070, 2028: .065, 2029: .060, 2030: .060},
    "capex": {2026: 20_500.0, 2027: 18_000.0, 2028: 15_000.0, 2029: 13_000.0, 2030: 12_000.0},
    "depreciation_ratio": 6_148.0 / 40_643.0,
    "inventory_days": 58.19,
    "tax_rate": .25,
    "minimum_cash_and_investments": 10_000.0,
    "revolver_limit": 6_430.0,
    "revolver_rate": .06,
    "cost_of_equity": .10,
    "terminal_growth": .03,
    "shares_outstanding": 3_528.0,
    "interest_income_rate": 1_680.0 / 44_059.0,
    "debt_interest_rate": 338.0 / 8_376.0,
    "floor_plan_financing": 0.0,
    "opening": {
        "revenue": 94_827.0, "cash_and_investments": 44_059.0,
        "inventory": 12_392.0, "ppe": 40_643.0, "other_assets": 40_712.0,
        "debt_and_finance_leases": 8_376.0, "other_liabilities": 46_623.0,
        "equity": 82_807.0, "revolver": 0.0,
    },
}


def assert_balanced(results, minimum_cash):
    """Refuse to value a model with an unbalanced balance sheet."""
    for year in YEARS:
        gap = results[year]["Balance Gap"]
        if abs(gap) > 0.000001:
            raise ValueError(f"FY{year}E balance sheet does not balance. Gap = {gap:.6f}")
        if results[year]["Cash & Investments"] < minimum_cash:
            raise ValueError(f"FY{year}E cash and investments below the minimum.")


def print_table(results, title, rows):
    print(f"\n{title}")
    print(f"{'Line':<25}" + "".join(f"{year:>12}" for year in YEARS))
    for row in rows:
        print(f"{row:<25}" + "".join(f"{results[year][row]:>12.1f}" for year in YEARS))


def print_checks(results):
    print("\nCHECKS")
    for year in YEARS:
        data = results[year]
        print(f"FY{year}E: Assets - Liabilities - Equity = {data['Balance Gap']:.1f}, "
              f"Cash & Investments = {data['Cash & Investments']:.1f}")


def print_valuation(model):
    print("\nVALUATION")
    if model["value_per_share"] is None:
        print("value per share unavailable")
        print(model["valuation_reason"])
    else:
        print(f"Equity value: ${model['equity_value']:.2f} million")
        print(f"Value per diluted share: ${model['value_per_share']:.2f}")


def print_full_model(model):
    results = model["results"]
    print_table(results, "INCOME STATEMENT", [
        "Revenue", "Gross Profit", "SG&A", "R&D", "Operating Income",
        "Interest Income", "Interest Expense", "Pretax Income", "Tax", "Net Income",
    ])
    print_table(results, "BALANCE SHEET", [
        "Cash & Investments", "Inventory", "PP&E", "Other Assets",
        "Debt & Finance Leases", "Floor-Plan Financing", "Other Liabilities",
        "Revolver", "Equity",
    ])
    print_table(results, "CASH FLOW", ["Depreciation", "FCFE"])
    print_checks(results)
    print_valuation(model)


def run_model(inputs):
    """Run the complete linked model from a fresh independent input set."""
    data = deepcopy(inputs)
    opening = data["opening"]
    revenue = opening["revenue"]
    cash = opening["cash_and_investments"]
    inventory = opening["inventory"]
    ppe = opening["ppe"]
    other_assets = opening["other_assets"]
    debt = opening["debt_and_finance_leases"]
    other_liabilities = opening["other_liabilities"]
    equity = opening["equity"]
    revolver = opening["revolver"]
    other_assets_pct = other_assets / revenue
    other_liabilities_pct = other_liabilities / revenue
    results = {}

    for year in YEARS:
        opening_revenue, opening_cash = revenue, cash
        opening_inventory, opening_ppe = inventory, ppe
        opening_other_assets, opening_other_liabilities = other_assets, other_liabilities
        opening_debt, opening_equity, opening_revolver = debt, equity, revolver

        revenue = opening_revenue * (1 + data["growth"][year])
        gross_profit = revenue * data["gross_margin"][year]
        sga = revenue * data["sga_percent_revenue"][year]
        rd = revenue * data["rd_percent_revenue"][year]
        depreciation = opening_ppe * data["depreciation_ratio"]
        # Depreciation is already included in cost of revenues and gross profit.
        operating_income = gross_profit - sga - rd
        interest_income = opening_cash * data["interest_income_rate"]
        interest_expense = opening_debt * data["debt_interest_rate"] + opening_revolver * data["revolver_rate"]
        pretax_income = operating_income + interest_income - interest_expense
        tax = max(0.0, pretax_income) * data["tax_rate"]
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * data["inventory_days"] / 365.0
        ppe = opening_ppe + data["capex"][year] - depreciation
        other_assets = revenue * other_assets_pct
        other_liabilities = revenue * other_liabilities_pct
        debt = opening_debt
        equity = opening_equity + net_income
        change_inventory = inventory - opening_inventory
        change_other_assets = other_assets - opening_other_assets
        change_other_liabilities = other_liabilities - opening_other_liabilities
        fcfe = (net_income + depreciation - data["capex"][year] - change_inventory
                - change_other_assets + change_other_liabilities)

        cash_before_revolver = opening_cash + fcfe
        if cash_before_revolver < data["minimum_cash_and_investments"]:
            draw = data["minimum_cash_and_investments"] - cash_before_revolver
            if opening_revolver + draw > data["revolver_limit"]:
                raise ValueError(f"FY{year}E revolver limit exceeded: draw = {draw:.1f}")
            revolver = opening_revolver + draw
            cash = data["minimum_cash_and_investments"]
        else:
            repayment = min(opening_revolver, cash_before_revolver - data["minimum_cash_and_investments"])
            revolver = opening_revolver - repayment
            cash = cash_before_revolver - repayment

        assets = cash + inventory + ppe + other_assets
        liabilities_and_equity = debt + other_liabilities + revolver + equity
        results[year] = {
            "Revenue": revenue, "Gross Profit": gross_profit, "SG&A": sga, "R&D": rd,
            "Depreciation": depreciation, "Operating Income": operating_income,
            "Interest Income": interest_income, "Interest Expense": interest_expense,
            "Pretax Income": pretax_income, "Tax": tax, "Net Income": net_income,
            "Cash & Investments": cash, "Inventory": inventory, "PP&E": ppe,
            "Other Assets": other_assets, "Debt & Finance Leases": debt,
            "Floor-Plan Financing": data["floor_plan_financing"],
            "Other Liabilities": other_liabilities, "Revolver": revolver, "Equity": equity,
            "FCFE": fcfe, "Balance Gap": assets - liabilities_and_equity,
        }

    assert_balanced(results, data["minimum_cash_and_investments"])
    fcfe_2030 = results[2030]["FCFE"]
    pv_fcfe = sum(results[year]["FCFE"] / (1 + data["cost_of_equity"]) ** period
                  for period, year in enumerate(YEARS, start=1))
    if fcfe_2030 <= 0.0:
        return {"inputs": data, "results": results, "equity_value": None,
                "value_per_share": None,
                "valuation_reason": "FY2030E FCFE is zero or negative; no terminal value is calculated."}
    terminal_value = fcfe_2030 * (1 + data["terminal_growth"]) / (data["cost_of_equity"] - data["terminal_growth"])
    equity_value = pv_fcfe + terminal_value / (1 + data["cost_of_equity"]) ** len(YEARS)
    return {"inputs": data, "results": results, "equity_value": equity_value,
            "value_per_share": equity_value / data["shares_outstanding"], "valuation_reason": None}


def print_case_inputs(driver, unit, inputs):
    print(f"Input values ({unit}): " + ", ".join(
        f"FY{year} {inputs[driver][year]:.1%}" for year in YEARS))


def change(value, base, decimals=1):
    return "n/a" if value is None or base is None else f"{value - base:+.{decimals}f}"


def sensitivity(driver, title, unit, shift, first_base):
    print(f"\n{'=' * 100}\nSENSITIVITY: {title}")
    cases = []
    for name, adjustment in (("Lower", -shift), ("Base", 0.0), ("Higher", shift)):
        inputs = deepcopy(BASE_INPUTS)
        for year in YEARS:
            inputs[driver][year] = BASE_INPUTS[driver][year] + adjustment
        print(f"\n{name} run")
        print_case_inputs(driver, unit, inputs)
        try:
            model = run_model(inputs)
            output = model["results"][2030]
            print(f"FY2030 Operating income = {output['Operating Income']:.1f}")
            print(f"FY2030 FCFE = {output['FCFE']:.1f}")
            if model["value_per_share"] is None:
                print("value per share unavailable")
                print(model["valuation_reason"])
            else:
                print(f"Value per share = {model['value_per_share']:.2f}")
            print_checks(model["results"])
            cases.append((name, model, None))
        except ValueError as error:
            print(f"INVALID RUN: {error}")
            cases.append((name, None, str(error)))

    base_2030 = first_base["results"][2030]
    base_value = first_base["value_per_share"]
    print(f"\n{title.upper()} SUMMARY (inputs: {unit}; outputs: USD millions except per share)")
    print(f"{'Scenario':<10}{'FY2026':>9}{'FY2027':>9}{'FY2028':>9}{'FY2029':>9}{'FY2030':>9}"
          f"{'Op Income':>13}{'Change':>10}{'FCFE':>13}{'Change':>10}{'Value/share':>14}{'Change':>10}  Status")
    valid_models = []
    for name, model, error in cases:
        inputs = BASE_INPUTS if name == "Base" else next(c[1]["inputs"] for c in cases if c[0] == name and c[1] is not None) if model else deepcopy(BASE_INPUTS)
        # The input path is stored in valid models; invalid cases retain their only changed driver path below.
        if model is None:
            adjusted = {year: BASE_INPUTS[driver][year] + ({"Lower": -shift, "Base": 0, "Higher": shift}[name]) for year in YEARS}
            path = "".join(f"{adjusted[year]:>8.1%}" for year in YEARS)
            print(f"{name:<10}{path}{'n/a':>13}{'n/a':>10}{'n/a':>13}{'n/a':>10}{'n/a':>14}{'n/a':>10}  INVALID: {error}")
            continue
        output = model["results"][2030]
        path = "".join(f"{model['inputs'][driver][year]:>8.1%}" for year in YEARS)
        value = model["value_per_share"]
        value_text = "unavailable" if value is None else f"{value:.2f}"
        status = "valid" if value is not None else f"unavailable: {model['valuation_reason']}"
        print(f"{name:<10}{path}{output['Operating Income']:>13.1f}{change(output['Operating Income'], base_2030['Operating Income']):>10}"
              f"{output['FCFE']:>13.1f}{change(output['FCFE'], base_2030['FCFE']):>10}"
              f"{value_text:>14}{change(value, base_value, 2):>10}  {status}")
        valid_models.append(model)
    if valid_models:
        operating_income_span = max(m["results"][2030]["Operating Income"] for m in valid_models) - min(m["results"][2030]["Operating Income"] for m in valid_models)
        fcfe_span = max(m["results"][2030]["FCFE"] for m in valid_models) - min(m["results"][2030]["FCFE"] for m in valid_models)
        valid_values = [m["value_per_share"] for m in valid_models if m["value_per_share"] is not None]
        value_span = "unavailable" if not valid_values else f"{max(valid_values) - min(valid_values):.2f}"
        print("Span (maximum - minimum across valid lower/base/higher runs): "
              f"Operating income = {operating_income_span:.1f}; FCFE = {fcfe_span:.1f}; Value per share = {value_span}")
    else:
        print("Span unavailable: no valid runs.")


if __name__ == "__main__":
    print("BASE RUN (corrected depreciation treatment)")
    first_base_run = run_model(deepcopy(BASE_INPUTS))
    print_full_model(first_base_run)
    sensitivity("growth", "Revenue growth", "% growth", .03, first_base_run)
    sensitivity("rd_percent_revenue", "R&D % of revenue", "% of revenue", .01, first_base_run)
    print(f"\n{'=' * 100}\nRESTORED BASE RUN")
    restored_base_run = run_model(deepcopy(BASE_INPUTS))
    print_full_model(restored_base_run)
    matches = (first_base_run["results"] == restored_base_run["results"] and
               first_base_run["value_per_share"] == restored_base_run["value_per_share"])
    print(f"\nRestored base matches first base run: {'YES' if matches else 'NO'}")
