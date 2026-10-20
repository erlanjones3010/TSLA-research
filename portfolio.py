"""Lab 14: calculate and compare simple portfolio baselines."""

# Editable inputs: expected annual returns and annual volatilities (decimals).
ASSETS = [
    "Treasury bills",
    "Treasury 10-year note",
    "Investment-grade bond fund",
    "Global equity index fund",
]
EXPECTED_RETURNS = [0.035, 0.043, 0.050, 0.080]
VOLATILITIES = [0.005, 0.070, 0.060, 0.160]

# Rows and columns follow the order in ASSETS.
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]

# Estimated CPI of 2.5% plus 4%.
OBJECTIVE_RETURN = 0.065


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


def print_portfolio(name, weights, covariance_matrix):
    """Calculate and display all required metrics for one portfolio."""
    portfolio_return = calculate_expected_return(weights, EXPECTED_RETURNS)
    volatility = calculate_portfolio_volatility(weights, covariance_matrix)
    reserve_eligible = calculate_reserve_eligible_percentage(weights)
    objective_status = "Yes" if meets_return_objective(
        portfolio_return, OBJECTIVE_RETURN
    ) else "No"

    print(name)
    print("  Weights (Bills / 10-year / IG / Equity): " + " / ".join(
        f"{weight:.1%}" for weight in weights
    ))
    print(f"  Expected annual return: {portfolio_return:.2%}")
    print(f"  Portfolio volatility:   {volatility:.2%}")
    print(f"  Reserve-eligible:       {reserve_eligible:.1%}")
    print(f"  Meets 6.5% objective:   {objective_status}")


def main():
    """Validate inputs, build covariance data, and report three baselines."""
    validate_correlation_matrix(CORRELATIONS)
    covariance_matrix = build_covariance_matrix(CORRELATIONS, VOLATILITIES)

    portfolios = [
        ("Benchmark", [0.0, 0.0, 0.40, 0.60]),
        ("Equal weight", equal_weight_portfolio(len(ASSETS))),
        ("Inverse volatility", inverse_volatility_portfolio(VOLATILITIES)),
    ]
    for index, (name, weights) in enumerate(portfolios):
        if index:
            print()
        print_portfolio(name, weights, covariance_matrix)


if __name__ == "__main__":
    main()
