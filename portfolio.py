"""Lab 14: calculate and compare simple portfolio baselines."""

import csv
import io
import math

# Editable inputs: expected annual returns and annual volatilities (decimals).
ASSETS = [
    "Treasury bills",
    "Treasury 10-year note",
    "Investment-grade bond fund",
    "Global equity index fund",
]
EXPECTED_RETURNS = [0.035, 0.043, 0.050, 0.080]
VOLATILITIES = [0.005, 0.070, 0.060, 0.160]

# Rows and columns follow the order in ASSETS. Lab 14 retains its original
# training matrix, and the active Lab 15 matrix uses the restored assumptions.
LAB14_CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]

CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]

# Estimated CPI of 2.5% plus 4%.
OBJECTIVE_RETURN = 0.065
MINIMUM_RESERVE_ELIGIBLE = 0.03
MERIDIAN_RESERVE_ELIGIBLE = [True, True, False, False]


def validate_correlation_matrix(correlations):
    """Raise ValueError unless correlations are square, bounded, and symmetric."""
    size = len(correlations)
    if any(len(row) != size for row in correlations):
        raise ValueError("Correlation matrix must be square.")

    for row_index, row in enumerate(correlations):
        for column_index, value in enumerate(row):
            if not -1.0 <= value <= 1.0:
                raise ValueError(
                    "Correlation at row "
                    f"{row_index + 1}, column {column_index + 1} must be between -1 and +1."
                )
            if value != correlations[column_index][row_index]:
                raise ValueError("Correlation matrix must be symmetric.")


def build_covariance_matrix(correlations, volatilities):
    """Convert correlations and volatilities into a covariance matrix."""
    return [
        [correlations[i][j] * volatilities[i] * volatilities[j]
         for j in range(len(volatilities))]
        for i in range(len(volatilities))
    ]


def calculate_expected_return(weights, expected_returns):
    """Return the weighted expected annual return."""
    return sum(weight * expected_return
               for weight, expected_return in zip(weights, expected_returns))


def calculate_portfolio_volatility(weights, covariance_matrix):
    """Return portfolio volatility from the complete covariance matrix."""
    variance = sum(
        weights[i] * covariance_matrix[i][j] * weights[j]
        for i in range(len(weights))
        for j in range(len(weights))
    )
    return variance ** 0.5


def calculate_reserve_eligible_percentage(weights):
    """Return the share invested in Treasury bills and the 10-year note."""
    return weights[0] + weights[1]


def meets_return_objective(portfolio_return, objective_return):
    """Return whether a portfolio reaches its stated return objective."""
    return portfolio_return >= objective_return


def equal_weight_portfolio(asset_count):
    """Return equal weights for the requested number of assets."""
    return [1 / asset_count] * asset_count


def inverse_volatility_portfolio(volatilities):
    """Return weights proportional to inverse volatility and normalized to 100%."""
    inverse_volatilities = [1 / volatility for volatility in volatilities]
    total = sum(inverse_volatilities)
    return [inverse_volatility / total for inverse_volatility in inverse_volatilities]


def find_lowest_volatility_mix(expected_returns, covariance_matrix, objective_return,
                               minimum_reserve_eligible, reserve_eligible, step=0.05):
    """Search fixed-step, long-only allocations and return the least risky match."""
    asset_count = len(expected_returns)
    if asset_count == 0 or len(reserve_eligible) != asset_count:
        raise ValueError("Expected returns and reserve flags must cover each asset.")
    if len(covariance_matrix) != asset_count or any(
        len(row) != asset_count for row in covariance_matrix
    ):
        raise ValueError("Covariance matrix dimensions must match the assets.")

    steps = round(1 / step)
    if step <= 0 or not math.isclose(steps * step, 1.0, abs_tol=1e-9):
        raise ValueError("Step must divide 100% exactly.")

    best_mix = None

    def search(asset_index, steps_remaining, weights):
        nonlocal best_mix
        if asset_index == asset_count - 1:
            candidate_weights = weights + [steps_remaining * step]
            portfolio_return = calculate_expected_return(candidate_weights, expected_returns)
            reserve_weight = sum(
                weight for weight, eligible in zip(candidate_weights, reserve_eligible)
                if eligible
            )
            if (portfolio_return >= objective_return
                    and reserve_weight >= minimum_reserve_eligible):
                volatility = calculate_portfolio_volatility(
                    candidate_weights, covariance_matrix
                )
                if best_mix is None or volatility < best_mix["volatility"]:
                    best_mix = {
                        "weights": candidate_weights,
                        "expected_return": portfolio_return,
                        "volatility": volatility,
                        "reserve_eligible": reserve_weight,
                    }
            return

        for weight_steps in range(steps_remaining + 1):
            search(
                asset_index + 1,
                steps_remaining - weight_steps,
                weights + [weight_steps * step],
            )

    search(0, steps, [])
    return best_mix


def _read_price_rows(csv_source):
    """Read CSV text, a path, or an uploaded file and return its rows."""
    if hasattr(csv_source, "read"):
        contents = csv_source.read()
        if isinstance(contents, bytes):
            contents = contents.decode("utf-8-sig")
        return list(csv.reader(io.StringIO(contents)))
    if isinstance(csv_source, str) and "\n" in csv_source:
        return list(csv.reader(io.StringIO(csv_source)))
    with open(csv_source, newline="", encoding="utf-8-sig") as price_file:
        return list(csv.reader(price_file))


def estimate_from_price_csv(csv_source, last_36_months=False):
    """Estimate annual returns, volatility, and correlations from monthly prices."""
    rows = _read_price_rows(csv_source)
    if len(rows) < 3 or len(rows[0]) < 2:
        raise ValueError("CSV needs a date column, ticker columns, and two prices.")

    tickers = rows[0][1:]
    if not all(tickers) or len(set(tickers)) != len(tickers):
        raise ValueError("Ticker column names must be present and unique.")
    prices = []
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(tickers) + 1:
            raise ValueError(f"Row {row_number} does not match the header.")
        try:
            prices.append([float(value) for value in row[1:]])
        except ValueError as error:
            raise ValueError(f"Row {row_number} contains a non-numeric price.") from error
    if any(price <= 0 for row in prices for price in row):
        raise ValueError("Prices must be positive.")

    monthly_returns = [
        [current[i] / previous[i] - 1 for i in range(len(tickers))]
        for previous, current in zip(prices, prices[1:])
    ]
    if last_36_months:
        monthly_returns = monthly_returns[-36:]
    if len(monthly_returns) < 2:
        raise ValueError("At least two monthly returns are required.")

    observations = len(monthly_returns)
    means = [sum(row[i] for row in monthly_returns) / observations
             for i in range(len(tickers))]
    monthly_volatilities = [
        math.sqrt(sum((row[i] - means[i]) ** 2 for row in monthly_returns)
                  / (observations - 1))
        for i in range(len(tickers))
    ]
    correlations = []
    for i in range(len(tickers)):
        correlation_row = []
        for j in range(len(tickers)):
            if i == j:
                correlation_row.append(1.0)
            elif monthly_volatilities[i] == 0 or monthly_volatilities[j] == 0:
                correlation_row.append(0.0)
            else:
                covariance = sum(
                    (row[i] - means[i]) * (row[j] - means[j])
                    for row in monthly_returns
                ) / (observations - 1)
                correlation_row.append(
                    covariance / (monthly_volatilities[i] * monthly_volatilities[j])
                )
        correlations.append(correlation_row)

    return {
        "tickers": tickers,
        "expected_returns": [mean * 12 for mean in means],
        "volatilities": [volatility * math.sqrt(12) for volatility in monthly_volatilities],
        "correlations": correlations,
        "months_used": observations,
    }


search_long_only_mix = find_lowest_volatility_mix
estimate_from_csv = estimate_from_price_csv


def evaluate_portfolio(weights, covariance_matrix):
    """Return the Lab 14 metrics for a set of asset weights."""
    if len(weights) != len(ASSETS):
        raise ValueError(f"Expected {len(ASSETS)} asset weights.")

    portfolio_return = calculate_expected_return(weights, EXPECTED_RETURNS)
    return {
        "expected_return": portfolio_return,
        "volatility": calculate_portfolio_volatility(weights, covariance_matrix),
        "reserve_eligible": calculate_reserve_eligible_percentage(weights),
        "meets_return_objective": meets_return_objective(
            portfolio_return, OBJECTIVE_RETURN
        ),
    }


def baseline_portfolios():
    """Return the three Lab 14 baseline allocations in display order."""
    return [
        ("Benchmark", [0.0, 0.0, 0.40, 0.60]),
        ("Equal weight", equal_weight_portfolio(len(ASSETS))),
        ("Inverse volatility", inverse_volatility_portfolio(VOLATILITIES)),
    ]


def print_portfolio(name, weights, covariance_matrix):
    """Calculate and display all required metrics for one portfolio."""
    metrics = evaluate_portfolio(weights, covariance_matrix)
    objective_status = "Yes" if metrics["meets_return_objective"] else "No"

    print(name)
    print("  Weights (Bills / 10-year / IG / Equity): " + " / ".join(
        f"{weight:.1%}" for weight in weights
    ))
    print(f"  Expected annual return: {metrics['expected_return']:.2%}")
    print(f"  Portfolio volatility:   {metrics['volatility']:.2%}")
    print(f"  Reserve-eligible:       {metrics['reserve_eligible']:.1%}")
    print(f"  Meets 6.5% objective:   {objective_status}")


def main():
    """Validate inputs, build covariance data, and report three baselines."""
    validate_correlation_matrix(LAB14_CORRELATIONS)
    covariance_matrix = build_covariance_matrix(LAB14_CORRELATIONS, VOLATILITIES)

    for index, (name, weights) in enumerate(baseline_portfolios()):
        if index:
            print()
        print_portfolio(name, weights, covariance_matrix)


if __name__ == "__main__":
    main()
