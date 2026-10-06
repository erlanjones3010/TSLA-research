"""Tesla FCFF DCF valuation driven by proforma.py (USD millions, except per-share data)."""

from copy import deepcopy

from proforma import DRIVERS, SCENARIO_DRIVERS, YEARS, run_forecast
from tesla_inputs import ANALYST_DECISIONS, HISTORY


VALUATION_DATE = "2026-09-01"
TERMINAL_GROWTH = 0.03


def wacc_input(value, source, as_of, basis):
    """Store a WACC input with its source, date, and calculation basis."""
    return {"value": value, "source": source, "as_of": as_of, "basis": basis}


FY2025 = HISTORY["FY2025"]
BALANCE_SHEET = FY2025["balance_sheet"]
EXPENSES = FY2025["expenses_and_cash_flow"]
TAX_RATE = DRIVERS["tax_rate"]["values"][2026]
DILUTED_SHARES = FY2025["shares"]["diluted_weighted_average"]["value"]
DEBT = ANALYST_DECISIONS["FY2025_debt_used_in_equity_bridge"]["decision"]["value"]

# Independently verified market observations used for the specified valuation date.
WACC_INPUTS = {
    "risk_free_rate": wacc_input(
        0.0479,
        "U.S. Department of the Treasury, Daily Treasury Par Yield Curve Rates (10-year), https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve",
        VALUATION_DATE,
        "10-year U.S. Treasury par yield on September 1, 2026.",
    ),
    "beta": wacc_input(
        1.83,
        "Yahoo Finance, Tesla (TSLA) quote/statistics page, https://finance.yahoo.com/quote/TSLA/",
        VALUATION_DATE,
        "Yahoo Finance Beta (5Y Monthly), using five years of monthly observations.",
    ),
    "equity_risk_premium": wacc_input(
        0.0414,
        "Aswath Damodaran, Implied Equity Risk Premium, https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm",
        "2026-09-01",
        "U.S. implied ERP, trailing 12-month adjusted-payout method; September 2026 published value.",
    ),
    "share_price": wacc_input(
        356.09,
        "Yahoo Finance, TSLA historical prices, https://finance.yahoo.com/quote/TSLA/history/",
        VALUATION_DATE,
        "September 1, 2026 NASDAQ regular-session closing price, USD per share.",
    ),
    "diluted_shares": wacc_input(
        DILUTED_SHARES,
        FY2025["shares"]["diluted_weighted_average"]["source"],
        FY2025["shares"]["diluted_weighted_average"]["as_of"],
        "FY2025 diluted weighted-average shares imported from tesla_inputs.py.",
    ),
    "pre_tax_cost_of_debt": wacc_input(
        EXPENSES["interest_expense"]["value"] / DEBT,
        "Tesla FY2025 Form 10-K; values imported from tesla_inputs.py.",
        "2025-12-31",
        "FY2025 interest expense divided by debt and finance leases used in the equity bridge.",
    ),
    "tax_rate": wacc_input(
        TAX_RATE,
        "Project 1/proforma.py driver: tax_rate.",
        "FY2026E-FY2030E",
        "Normalized tax rate used in the pro forma.",
    ),
}
WACC_INPUTS["cost_of_equity"] = wacc_input(
    WACC_INPUTS["risk_free_rate"]["value"]
    + WACC_INPUTS["beta"]["value"] * WACC_INPUTS["equity_risk_premium"]["value"],
    "Calculated from the risk-free rate, beta, and ERP inputs above.",
    VALUATION_DATE,
    "CAPM: risk-free rate + beta × equity risk premium.",
)
WACC_INPUTS["after_tax_cost_of_debt"] = wacc_input(
    WACC_INPUTS["pre_tax_cost_of_debt"]["value"] * (1 - TAX_RATE),
    "Calculated from the pre-tax cost of debt and pro forma normalized tax rate.",
    "2025-12-31 / FY2026E-FY2030E",
    "Pre-tax cost of debt × (1 − tax rate).",
)
WACC_INPUTS["market_value_of_equity"] = wacc_input(
    WACC_INPUTS["share_price"]["value"] * DILUTED_SHARES,
    "Calculated from Yahoo Finance historical closing price and imported FY2025 diluted shares.",
    VALUATION_DATE,
    "TSLA September 1, 2026 close × FY2025 diluted shares.",
)
WACC_INPUTS["debt"] = wacc_input(
    DEBT,
    ANALYST_DECISIONS["FY2025_debt_used_in_equity_bridge"]["decision"]["source"],
    "2025-12-31",
    "Debt and finance leases used in the equity bridge.",
)
TOTAL_CAPITAL = WACC_INPUTS["market_value_of_equity"]["value"] + DEBT
WACC_INPUTS["equity_weight"] = wacc_input(
    WACC_INPUTS["market_value_of_equity"]["value"] / TOTAL_CAPITAL,
    "Calculated from market value of equity and debt above.",
    VALUATION_DATE,
    "Market value of equity ÷ (market value of equity + debt).",
)
WACC_INPUTS["debt_weight"] = wacc_input(
    DEBT / TOTAL_CAPITAL,
    "Calculated from market value of equity and debt above.",
    VALUATION_DATE,
    "Debt ÷ (market value of equity + debt).",
)
WACC_INPUTS["wacc"] = wacc_input(
    WACC_INPUTS["equity_weight"]["value"] * WACC_INPUTS["cost_of_equity"]["value"]
    + WACC_INPUTS["debt_weight"]["value"] * WACC_INPUTS["after_tax_cost_of_debt"]["value"],
    "Calculated from CAPM cost of equity, after-tax cost of debt, and market-value weights above.",
    VALUATION_DATE,
    "E/(D+E) × cost of equity + D/(D+E) × after-tax cost of debt.",
)


def require_verified_market_inputs():
    """Fail rather than silently use an unverified required market input."""
    missing = [name for name in ("risk_free_rate", "beta", "share_price")
               if WACC_INPUTS[name]["value"] is None]
    if missing:
        raise ValueError("Cannot run valuation: unverified market input(s): " + ", ".join(missing))


def dcf_value(fcff_by_year, wacc, terminal_growth):
    """DCF at each fiscal year-end, measured from December 31, 2025."""
    if wacc <= terminal_growth:
        raise ValueError("WACC must be greater than terminal growth.")
    present_values = {}
    for period, year in enumerate(YEARS, start=1):
        present_values[year] = fcff_by_year[year] / (1 + wacc) ** period
    terminal_value = fcff_by_year[2030] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / (1 + wacc) ** len(YEARS)
    enterprise_value = sum(present_values.values()) + pv_terminal_value
    return {
        "pv_fcff": present_values,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "terminal_value_percent_of_ev": pv_terminal_value / enterprise_value if enterprise_value else None,
    }


def enterprise_to_equity_bridge(enterprise_value):
    """Bridge enterprise value to common-equity value with imported FY2025 balances."""
    bridge = {
        "Enterprise value": enterprise_value,
        "Cash and cash equivalents": BALANCE_SHEET["cash_and_cash_equivalents"]["value"],
        "Short-term investments": BALANCE_SHEET["short_term_investments"]["value"],
        "Digital assets (non-operating)": BALANCE_SHEET["digital_assets"]["value"],
        "Debt and finance leases": -DEBT,
        "Noncontrolling interests": -BALANCE_SHEET["noncontrolling_interests"]["value"],
        "Redeemable noncontrolling interests": -BALANCE_SHEET["redeemable_noncontrolling_interests"]["value"],
    }
    equity_value = sum(bridge.values())
    bridge["Equity value"] = equity_value
    bridge["Diluted shares"] = DILUTED_SHARES
    bridge["Value per share"] = equity_value / DILUTED_SHARES
    return bridge


def value_per_share(fcff_by_year, wacc, terminal_growth):
    dcf = dcf_value(fcff_by_year, wacc, terminal_growth)
    bridge = enterprise_to_equity_bridge(dcf["enterprise_value"])
    return bridge["Value per share"]


def sensitivity_grid(fcff_by_year, base_wacc):
    growth_rates = (0.02, 0.03, 0.04)
    wacc_rates = (base_wacc - 0.01, base_wacc, base_wacc + 0.01)
    return {wacc: {growth: value_per_share(fcff_by_year, wacc, growth)
                   for growth in growth_rates} for wacc in wacc_rates}


def reverse_dcf_fy2030_fcff(fcff_by_year, wacc, terminal_growth, target_share_price):
    """Solve the FY2030 FCFF that gives the target share price under perpetual growth."""
    target_equity_value = target_share_price * DILUTED_SHARES
    nonoperating_assets = (BALANCE_SHEET["cash_and_cash_equivalents"]["value"]
                           + BALANCE_SHEET["short_term_investments"]["value"]
                           + BALANCE_SHEET["digital_assets"]["value"])
    noncommon_claims = (DEBT + BALANCE_SHEET["noncontrolling_interests"]["value"]
                         + BALANCE_SHEET["redeemable_noncontrolling_interests"]["value"])
    target_enterprise_value = target_equity_value - nonoperating_assets + noncommon_claims
    pv_first_four_years = sum(fcff_by_year[year] / (1 + wacc) ** period
                              for period, year in enumerate(YEARS[:4], start=1))
    fy2030_value_factor = (1 + (1 + terminal_growth) / (wacc - terminal_growth)) / (1 + wacc) ** 5
    required_fy2030_fcff = (target_enterprise_value - pv_first_four_years) / fy2030_value_factor
    return required_fy2030_fcff


def assert_checks(fcff_by_year, wacc, dcf, bridge, sensitivity, scenario="BASE"):
    """Print checks and raise an error if any valuation integrity check fails."""
    base_growth = TERMINAL_GROWTH
    lower_wacc, base_wacc, higher_wacc = sorted(sensitivity)
    lower_growth, _, higher_growth = (0.02, base_growth, 0.04)
    bridge_recomputed = sum(value for name, value in bridge.items()
                            if name not in ("Equity value", "Diluted shares", "Value per share"))
    checks = [
        ("WACC is greater than terminal growth", wacc > TERMINAL_GROWTH),
        ("Value per share falls when WACC rises",
         sensitivity[lower_wacc][base_growth] > sensitivity[base_wacc][base_growth] > sensitivity[higher_wacc][base_growth]),
        ("Value per share rises when terminal growth rises",
         sensitivity[base_wacc][lower_growth] < sensitivity[base_wacc][base_growth] < sensitivity[base_wacc][higher_growth]),
        ("Bridge recomputes equity value line by line", abs(bridge_recomputed - bridge["Equity value"]) < 0.000001),
        ("Value per share × diluted shares equals equity value",
         abs(bridge["Value per share"] * bridge["Diluted shares"] - bridge["Equity value"]) < 0.000001),
    ]
    for label, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} — {scenario}: {label}")
    failures = [label for label, passed in checks if not passed]
    if failures:
        raise ValueError("Valuation checks failed: " + "; ".join(failures))


def print_wacc_inputs():
    print("\nWACC INPUTS")
    print(f"{'Input':<25}{'Value':>14}  {'As of':<24}Basis")
    percentage_inputs = {
        "risk_free_rate", "equity_risk_premium", "cost_of_equity", "pre_tax_cost_of_debt",
        "after_tax_cost_of_debt", "tax_rate", "equity_weight", "debt_weight", "wacc",
    }
    for name in ("risk_free_rate", "beta", "equity_risk_premium", "cost_of_equity", "pre_tax_cost_of_debt",
                 "after_tax_cost_of_debt", "market_value_of_equity", "debt", "equity_weight", "debt_weight", "wacc"):
        item = WACC_INPUTS[name]
        value = item["value"]
        if name == "beta":
            value_text = f"{value:.2f}"
        elif name in percentage_inputs:
            value_text = f"{value:.2%}"
        else:
            value_text = f"{value:,.2f}"
        print(f"{name.replace('_', ' '):<25}{value_text:>14}  {item['as_of']:<24}{item['basis']}")
    print("Sources: risk-free rate — U.S. Treasury; beta and share price — Yahoo Finance; "
          "ERP — Aswath Damodaran; debt, interest expense, and shares — imported project inputs.")


def print_dcf(dcf, fcff_by_year):
    print("\nDCF (USD millions; fiscal year-end discounting from December 31, 2025)")
    print(f"{'Year':<12}{'FCFF':>16}{'Present Value':>18}")
    for year in YEARS:
        print(f"FY{year}E{fcff_by_year[year]:>16,.1f}{dcf['pv_fcff'][year]:>18,.1f}")
    print(f"{'Terminal value':<12}{dcf['terminal_value']:>16,.1f}")
    print(f"{'PV terminal value':<12}{dcf['pv_terminal_value']:>16,.1f}")
    print(f"{'Enterprise value':<12}{dcf['enterprise_value']:>16,.1f}")
    print(f"{'PV terminal value / EV':<24}{dcf['terminal_value_percent_of_ev']:>8.1%}")
    print("Convention: FCFF is discounted at each December 31 fiscal year-end from December 31, 2025. "
          "The September 1, 2026 market valuation date is not stub-period adjusted, creating an eight-month timing mismatch.")


def print_bridge(bridge):
    print("\nENTERPRISE-TO-EQUITY BRIDGE (FY2025 balance sheet; USD millions except per share)")
    for line in ("Enterprise value", "Cash and cash equivalents", "Short-term investments", "Digital assets (non-operating)",
                 "Debt and finance leases", "Noncontrolling interests", "Redeemable noncontrolling interests", "Equity value",
                 "Diluted shares", "Value per share"):
        print(f"{line:<40}{bridge[line]:>16,.2f}")
    share_price = WACC_INPUTS["share_price"]["value"]
    print(f"{'TSLA share price on valuation date':<40}{share_price:>16,.2f}")
    print(f"{'Value per share less share price':<40}{bridge['Value per share'] - share_price:>16,.2f}")


def print_sensitivity(grid):
    print("\nVALUE PER SHARE SENSITIVITY (USD per share)")
    print("WACC \\ g".ljust(14) + f"{'2.0%':>14}{'3.0%':>14}{'4.0%':>14}")
    for wacc in sorted(grid):
        print(f"{wacc:>12.2%}  " + "".join(f"{grid[wacc][growth]:>14,.2f}" for growth in (0.02, 0.03, 0.04)))


def print_scenario_summary(models):
    """Print the requested comparative valuation summary for both scenarios."""
    print("\nSCENARIO SUMMARY")
    print(f"{'Scenario':<12}{'FY2030 EBIT':>16}{'FY2030 FCFF':>16}{'Enterprise value':>20}{'Value/share':>16}{'Share price':>16}")
    for scenario in ("BASE", "DOWNSIDE", "UPSIDE"):
        model = models[scenario]
        print(f"{scenario:<12}{model['forecast'][2030]['EBIT']:>16,.1f}{model['fcff'][2030]:>16,.1f}"
              f"{model['dcf']['enterprise_value']:>20,.1f}{model['bridge']['Value per share']:>16,.2f}"
              f"{WACC_INPUTS['share_price']['value']:>16,.2f}")


def market_implied_autonomy_revenue(wacc, target_share_price):
    """Solve FY2030 autonomy revenue while retaining the UPSIDE 0%/5%/20%/50%/100% ramp."""
    ramp_shape = {2026: 0.00, 2027: 0.05, 2028: 0.20, 2029: 0.50, 2030: 1.00}

    def implied_value_per_share(fy2030_revenue):
        drivers = deepcopy(SCENARIO_DRIVERS["UPSIDE"])
        drivers["autonomy_and_software_revenue"]["values"] = {
            year: fy2030_revenue * ramp_shape[year] for year in YEARS
        }
        forecast = run_forecast("UPSIDE", drivers=drivers)
        fcff_by_year = {year: forecast[year]["FCFF"] for year in YEARS}
        return value_per_share(fcff_by_year, wacc, TERMINAL_GROWTH)

    lower, upper = 0.0, SCENARIO_DRIVERS["UPSIDE"]["autonomy_and_software_revenue"]["values"][2030]
    while implied_value_per_share(upper) < target_share_price:
        upper *= 2
        if upper > 10_000_000:
            raise ValueError("Unable to bracket the market-implied FY2030 autonomy revenue.")
    for _ in range(80):
        midpoint = (lower + upper) / 2
        if implied_value_per_share(midpoint) < target_share_price:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2


def main():
    require_verified_market_inputs()
    wacc = WACC_INPUTS["wacc"]["value"]
    models = {}
    for scenario in ("BASE", "DOWNSIDE", "UPSIDE"):
        forecast = run_forecast(scenario)
        fcff_by_year = {year: forecast[year]["FCFF"] for year in YEARS}
        dcf = dcf_value(fcff_by_year, wacc, TERMINAL_GROWTH)
        bridge = enterprise_to_equity_bridge(dcf["enterprise_value"])
        models[scenario] = {
            "forecast": forecast,
            "fcff": fcff_by_year,
            "dcf": dcf,
            "bridge": bridge,
            "grid": sensitivity_grid(fcff_by_year, wacc),
        }
    base_model = models["BASE"]
    reverse_fcff = reverse_dcf_fy2030_fcff(base_model["fcff"], wacc, TERMINAL_GROWTH, WACC_INPUTS["share_price"]["value"])
    implied_autonomy_revenue = market_implied_autonomy_revenue(wacc, WACC_INPUTS["share_price"]["value"])

    print("TESLA FCFF DCF VALUATION — BASE SCENARIO")
    print_wacc_inputs()
    print_dcf(base_model["dcf"], base_model["fcff"])
    print_bridge(base_model["bridge"])
    print_sensitivity(base_model["grid"])
    print("\nREVERSE DCF (USD millions)")
    print(f"{'FY2030 FCFF in pro forma':<42}{base_model['fcff'][2030]:>16,.1f}")
    print(f"{'FY2030 FCFF required for share price':<42}{reverse_fcff:>16,.1f}")
    print("Assumption: FY2030 FCFF is held at the solved level; terminal-period FCFF grows at 3.0%.")
    print("\nCHECKS")
    for scenario in ("BASE", "DOWNSIDE", "UPSIDE"):
        model = models[scenario]
        assert_checks(model["fcff"], wacc, model["dcf"], model["bridge"], model["grid"], scenario)
    print("\nASSUMPTIONS ADDED")
    print("- The September 1, 2026 valuation date is not stub-period adjusted; cash flows are discounted from December 31, 2025 at fiscal year-end.")
    print("- FY2025 cash, investments, digital assets, debt, and noncontrolling interests are used in the bridge even though market inputs are dated September 1, 2026.")
    print("- No market input used in this valuation is unverified.")
    print_scenario_summary(models)
    print("\nMARKET-IMPLIED AUTONOMY (UPSIDE; USD millions)")
    print(f"{'FY2030 autonomy revenue assumption':<46}{SCENARIO_DRIVERS['UPSIDE']['autonomy_and_software_revenue']['values'][2030]:>16,.1f}")
    print(f"{'FY2030 autonomy revenue implied by share price':<46}{implied_autonomy_revenue:>16,.1f}")
    print("Ramp held at 0% / 5% / 20% / 50% / 100% of FY2030 revenue for FY2026–FY2030; gross margin held at 50%.")


if __name__ == "__main__":
    main()
