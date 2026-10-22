"""Lab 15 Streamlit portfolio optimizer using functions from portfolio.py."""

import hashlib
import io

import streamlit as st

from portfolio import (
    ASSETS,
    CORRELATIONS,
    EXPECTED_RETURNS,
    MERIDIAN_RESERVE_ELIGIBLE,
    MINIMUM_RESERVE_ELIGIBLE,
    OBJECTIVE_RETURN,
    VOLATILITIES,
    build_covariance_matrix,
    estimate_from_price_csv,
    find_lowest_volatility_mix,
    validate_correlation_matrix,
)


def loaded_meridian_inputs():
    """Return the course inputs in the same shape as CSV estimates."""
    validate_correlation_matrix(CORRELATIONS)
    return {
        "tickers": ASSETS,
        "expected_returns": EXPECTED_RETURNS,
        "volatilities": VOLATILITIES,
        "correlations": CORRELATIONS,
    }


def show_mix(title, mix, asset_names):
    """Render an optimizer result without reproducing portfolio calculations."""
    st.subheader(title)
    if mix is None:
        st.info("No mix meets the objective.")
        return
    st.dataframe(
        [{"Asset": asset, "Weight": f"{weight:.1%}"}
         for asset, weight in zip(asset_names, mix["weights"])],
        hide_index=True,
        use_container_width=True,
    )
    first, second, third = st.columns(3)
    first.metric("Expected return", f"{mix['expected_return']:.2%}")
    second.metric("Volatility", f"{mix['volatility']:.2%}")
    third.metric("Reserve-eligible", f"{mix['reserve_eligible']:.2%}")


st.set_page_config(page_title="Portfolio Optimizer", page_icon="📈", layout="wide")
st.title("Portfolio Optimizer")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Optimizer settings")
    objective = st.number_input(
        "Return objective (%)", min_value=-100.0, max_value=100.0,
        value=OBJECTIVE_RETURN * 100, step=0.1,
    ) / 100
    reserve_minimum = st.number_input(
        "Minimum reserve-eligible (%)", min_value=0.0, max_value=100.0,
        value=MINIMUM_RESERVE_ELIGIBLE * 100, step=0.1,
    ) / 100
    uploaded_file = st.file_uploader("Monthly prices CSV", type="csv")
    use_last_36 = st.toggle("Use only the last 36 months", value=False)

if uploaded_file is None:
    loaded_inputs = loaded_meridian_inputs()
    active_inputs = loaded_inputs
    source_id = "meridian"
    st.caption("Using Meridian course inputs. Upload a price CSV to estimate inputs.")
else:
    file_bytes = uploaded_file.getvalue()
    source_id = hashlib.sha256(file_bytes).hexdigest()
    try:
        loaded_inputs = estimate_from_price_csv(io.BytesIO(file_bytes))
        active_inputs = estimate_from_price_csv(
            io.BytesIO(file_bytes), last_36_months=use_last_36
        )
    except ValueError as error:
        st.error(f"Could not use the CSV: {error}")
        st.stop()
    st.caption(
        f"Using {'the last 36 months' if use_last_36 else 'all available months'} "
        f"({active_inputs['months_used']} monthly returns)."
    )

asset_names = active_inputs["tickers"]
st.subheader("Expected annual returns")
st.write("Edit the annual return assumptions used in the active optimization.")
edited_returns = []
for index, (asset, default_return) in enumerate(
    zip(asset_names, active_inputs["expected_returns"])
):
    edited_returns.append(
        st.number_input(
            asset,
            min_value=-100.0,
            max_value=100.0,
            value=float(default_return * 100),
            step=0.1,
            key=f"return_{source_id}_{use_last_36}_{index}",
        ) / 100
    )

st.subheader("Reserve eligibility")
reserve_flags = []
for index, asset in enumerate(asset_names):
    default_flag = (
        MERIDIAN_RESERVE_ELIGIBLE[index]
        if uploaded_file is None and index < len(MERIDIAN_RESERVE_ELIGIBLE)
        else False
    )
    reserve_flags.append(
        st.checkbox(asset, value=default_flag, key=f"reserve_{source_id}_{index}")
    )

active_covariance = build_covariance_matrix(
    active_inputs["correlations"], active_inputs["volatilities"]
)
loaded_covariance = build_covariance_matrix(
    loaded_inputs["correlations"], loaded_inputs["volatilities"]
)
optimized_mix = find_lowest_volatility_mix(
    edited_returns, active_covariance, objective, reserve_minimum, reserve_flags
)
loaded_mix = find_lowest_volatility_mix(
    loaded_inputs["expected_returns"], loaded_covariance, objective,
    reserve_minimum, reserve_flags,
)

optimized_column, loaded_column = st.columns(2)
with optimized_column:
    show_mix("Lowest-risk mix", optimized_mix, asset_names)
with loaded_column:
    show_mix("Inputs as loaded", loaded_mix, loaded_inputs["tickers"])
    if optimized_mix is not None and loaded_mix is not None:
        largest_change = max(
            abs(current - original)
            for current, original in zip(optimized_mix["weights"], loaded_mix["weights"])
        )
        st.metric("Largest weight change", f"{largest_change * 100:.1f} points")
