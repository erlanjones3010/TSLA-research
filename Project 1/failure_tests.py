"""Failure tests for the Tesla DCF model; all deliberate changes stay in memory."""

from contextlib import redirect_stdout
from io import StringIO
import re

import proforma
import valuation


def report(test_name, broken, action, expected_message):
    """Run one deliberately broken model path and print a compact test result."""
    try:
        with redirect_stdout(StringIO()):
            action()
    except ValueError as error:
        actual = f"{type(error).__name__}: {error}"
        passed = expected_message in str(error)
    except Exception as error:  # A different exception is not an acceptable model stop.
        actual = f"{type(error).__name__}: {error}"
        passed = False
    else:
        actual = "model did not stop"
        passed = False
    print(
        f"{test_name} | {broken} | expected: stop with error | "
        f"actual: {actual} | {'PASS' if passed else 'FAIL'}"
    )
    return passed


def downside_fcff_with_negative_terminal_year():
    forecast = proforma.run_forecast("DOWNSIDE")
    forecast[2030]["FCFF"] = -500.0
    fcff = {year: forecast[year]["FCFF"] for year in proforma.YEARS}
    valuation.dcf_value(fcff, valuation.WACC_INPUTS["wacc"]["value"], valuation.TERMINAL_GROWTH)


def terminal_growth_equal_to_wacc():
    forecast = proforma.run_forecast("BASE")
    fcff = {year: forecast[year]["FCFF"] for year in proforma.YEARS}
    wacc = valuation.WACC_INPUTS["wacc"]["value"]
    valuation.dcf_value(fcff, wacc, wacc)


def unbalanced_balance_sheet():
    forecast = proforma.run_forecast("BASE")
    forecast[2027]["Cash + Investments"] += 1_000.0
    proforma.assert_checks(forecast, "BASE")


def zero_diluted_shares():
    forecast = proforma.run_forecast("BASE")
    fcff = {year: forecast[year]["FCFF"] for year in proforma.YEARS}
    valuation.value_per_share(
        fcff,
        valuation.WACC_INPUTS["wacc"]["value"],
        valuation.TERMINAL_GROWTH,
        {"diluted_shares": 0},
    )


def normal_model_is_unchanged():
    """Run valuation.main() and confirm the requested scenario values from its summary."""
    normal_output = StringIO()
    with redirect_stdout(normal_output):
        valuation.main()
    values = dict(re.findall(
        r"^(BASE|DOWNSIDE|UPSIDE)\s+.*?\s+(-?\d+\.\d{2})\s+\d+\.\d{2}$",
        normal_output.getvalue(),
        re.MULTILINE,
    ))
    expected = {"BASE": "14.93", "DOWNSIDE": "6.84", "UPSIDE": "37.49"}
    passed = values == expected
    actual = ", ".join(f"{scenario} ${values.get(scenario, 'missing')}" for scenario in expected)
    print(
        "normal model | no changes | expected: BASE $14.93, DOWNSIDE $6.84, UPSIDE $37.49 | "
        f"actual: {actual} | {'PASS' if passed else 'FAIL'}"
    )
    return passed


def main():
    results = [
        report(
            "negative final-year FCFF",
            "DOWNSIDE FY2030 FCFF set to -500 in memory",
            downside_fcff_with_negative_terminal_year,
            "FY2030 FCFF must be positive before a terminal value is calculated.",
        ),
        report(
            "terminal growth equals WACC",
            "terminal growth set equal to WACC in memory",
            terminal_growth_equal_to_wacc,
            "WACC must be greater than terminal growth.",
        ),
        report(
            "unbalanced balance sheet",
            "FY2027 cash increased by 1,000 with no matching entry in memory",
            unbalanced_balance_sheet,
            "FY2027E balance sheet balances",
        ),
        report(
            "zero diluted shares",
            "diluted shares set to 0 in memory",
            zero_diluted_shares,
            "Diluted shares must be positive.",
        ),
        normal_model_is_unchanged(),
    ]
    if not all(results):
        raise SystemExit("One or more failure tests failed.")


if __name__ == "__main__":
    main()
