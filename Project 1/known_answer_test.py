"""Known-answer reconciliation for the course training-case DCF (USD millions)."""

from valuation import (
    dcf_value,
    enterprise_to_equity_bridge,
    reverse_dcf_fy2030_fcff,
    sensitivity_grid,
    value_per_share,
)


FCFF = {
    1: 108.0,
    2: 114.48,
    3: 120.204,
    4: 125.01216,
    5: 128.762525,
}
WACC = 0.10
TERMINAL_GROWTH = 0.03
BRIDGE_INPUTS = {
    "cash": 50.0,
    "short_term_investments": 0.0,
    "digital_assets": 0.0,
    "debt": 300.0,
    "noncontrolling_interests": 0.0,
    "redeemable_noncontrolling_interests": 0.0,
    "diluted_shares": 50.0,
}


def check(item, expected, result, tolerance=0.01, suffix=""):
    """Print one reconciliation line and return whether it is within tolerance."""
    passed = abs(result - expected) <= tolerance
    expected_text = f"{expected:.1%}" if suffix == "%" else f"{expected:.2f}"
    result_text = f"{result:.1%}" if suffix == "%" else f"{result:.2f}"
    print(f"{item} | {expected_text} | {result_text} | {'PASS' if passed else 'FAIL'}")
    return passed


def main():
    dcf = dcf_value(FCFF, WACC, TERMINAL_GROWTH)
    bridge = enterprise_to_equity_bridge(dcf["enterprise_value"], **BRIDGE_INPUTS)
    grid = sensitivity_grid(FCFF, WACC, BRIDGE_INPUTS)
    value_at_11_percent = value_per_share(FCFF, 0.11, TERMINAL_GROWTH, BRIDGE_INPUTS)
    solved_fcff = reverse_dcf_fy2030_fcff(
        FCFF, WACC, TERMINAL_GROWTH, bridge["Value per share"], BRIDGE_INPUTS
    )

    results = [
        check("Sum of PV of FCFF", 448.44, sum(dcf["pv_fcff"].values())),
        check("Terminal value (Year 5)", 1894.65, dcf["terminal_value"]),
        check("PV of terminal value", 1176.43, dcf["pv_terminal_value"]),
        check("Enterprise value", 1624.87, dcf["enterprise_value"]),
        check("Terminal value share of EV", 0.724, dcf["terminal_value_percent_of_ev"], 0.001, "%"),
        check("Equity value", 1374.87, bridge["Equity value"]),
        check("Value per share", 27.50, bridge["Value per share"]),
        check("WACC 11% value per share", 23.41, value_at_11_percent),
    ]
    expected_grid = {
        0.09: {0.02: 28.60, 0.03: 32.94, 0.04: 39.02},
        0.10: {0.02: 24.36, 0.03: 27.50, 0.04: 31.69},
        0.11: {0.02: 21.06, 0.03: 23.41, 0.04: 26.44},
    }
    for wacc, growth_values in expected_grid.items():
        model_wacc = next(rate for rate in grid if abs(rate - wacc) < 1e-12)
        for growth, expected in growth_values.items():
            model_growth = next(rate for rate in grid[model_wacc] if abs(rate - growth) < 1e-12)
            results.append(check(
                f"Sensitivity WACC {wacc:.0%}, g {growth:.0%}", expected,
                grid[model_wacc][model_growth]
            ))
    results.append(check("Reverse DCF FCFF shift", 0.0, solved_fcff - FCFF[5]))

    if not all(results):
        raise AssertionError("Known-answer reconciliation failed.")


if __name__ == "__main__":
    main()
