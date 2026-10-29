"""Lab 17: compare today's FRED rates with an ALFRED point-in-time vintage."""

from datetime import date
from io import StringIO

import pandas as pd
import requests
import streamlit as st


FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
ALFRED_CSV = (
    "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}"
    "&vintage_date={vintage_date}"
)
DEFAULT_SERIES = ["BAA", "FEDFUNDS", "DGS10", "MORTGAGE30US"]
SERIES_LABELS = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Effective federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year fixed mortgage rate",
}


def _read_fred_csv(url, series_id):
    """Fetch one FRED/ALFRED CSV and return its date and value columns."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    frame = pd.read_csv(StringIO(response.text), na_values=".")
    date_column = next(
        (column for column in ("DATE", "observation_date") if column in frame.columns),
        None,
    )
    if date_column is None or len(frame.columns) < 2:
        raise ValueError("The server did not return a FRED data series.")

    value_column = series_id if series_id in frame.columns else frame.columns[-1]
    frame = frame[[date_column, value_column]].rename(
        columns={date_column: "date", value_column: "value"}
    )
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    return frame.dropna(subset=["date", "value"]).sort_values("date")


@st.cache_data(show_spinner=False)
def download_current(series_id):
    """Download the current (latest-revised) FRED series once per ID."""
    return _read_fred_csv(FRED_CSV.format(series_id=series_id), series_id)


@st.cache_data(show_spinner=False)
def download_as_known_on(series_id, vintage_date):
    """Download the ALFRED vintage available on the requested date once per ID/date."""
    url = ALFRED_CSV.format(series_id=series_id, vintage_date=vintage_date)
    return _read_fred_csv(url, series_id)


def last_observation(frame):
    """Return the last row, or None when a valid response has no observations."""
    return None if frame.empty else frame.iloc[-1]


def fred_page(series_id):
    return f"https://fred.stlouisfed.org/series/{series_id}"


def format_observation(observation):
    if observation is None:
        return "No observations"
    return f"{observation['date'].date():%Y-%m-%d}: {observation['value']:.3f}"


st.set_page_config(page_title="Point-in-Time Interest-Rate Audit", page_icon="📊", layout="wide")
st.title("Point-in-Time Interest-Rate Audit")
st.caption(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded "
    "today; built with AI help, a learning demonstration, not investment advice."
)

with st.sidebar:
    st.header("Audit settings")
    selected_series = st.multiselect(
        "Interest-rate series",
        options=DEFAULT_SERIES,
        default=DEFAULT_SERIES,
        format_func=lambda series_id: f"{series_id} — {SERIES_LABELS[series_id]}",
    )
    extra_series = st.text_input("Add another FRED series ID").strip().upper()
    start_date = st.date_input("Start date", value=date(2020, 1, 1))
    as_known_on = st.date_input("As known on", value=date.today())

if extra_series and extra_series not in selected_series:
    selected_series.append(extra_series)

if not selected_series:
    st.info("Choose at least one FRED series in the sidebar.")
    st.stop()

comparison_rows = []
for series_id in selected_series:
    try:
        # Exactly one request per series for each source; cache keys include all inputs.
        current = download_current(series_id)
        historical = download_as_known_on(series_id, as_known_on.isoformat())
    except (requests.RequestException, ValueError, pd.errors.ParserError) as error:
        st.error(f"{series_id}: could not download this FRED series ({error}).")
        continue

    historical = historical[historical["date"].dt.date <= as_known_on]
    current_last = last_observation(current)
    historical_last = last_observation(historical)
    chart_data = current[current["date"].dt.date >= start_date].set_index("date")

    st.subheader(f"{series_id} — {SERIES_LABELS.get(series_id, 'FRED series')}")
    if chart_data.empty:
        st.info(f"No current observations for {series_id} on or after {start_date:%Y-%m-%d}.")
    else:
        st.line_chart(chart_data[["value"]], y_label="Rate")
    st.caption(
        f"Last observation known on {as_known_on:%Y-%m-%d}: "
        f"{format_observation(historical_last)}"
    )

    if historical_last is None:
        observations_added = len(current)
        revisions = 0
    else:
        observations_added = int((current["date"] > historical_last["date"]).sum())
        overlapping = historical.merge(current, on="date", how="inner", suffixes=("_then", "_now"))
        revisions = int((overlapping["value_then"] != overlapping["value_now"]).sum())

    comparison_rows.append(
        {
            "Series ID": series_id,
            "Historical last observation": format_observation(historical_last),
            "Current last observation": format_observation(current_last),
            "Observations added": observations_added,
            "Overlapping observations revised": revisions,
        }
    )

st.subheader("Point-in-time comparison")
if comparison_rows:
    # Markdown preserves a direct link on the Series ID itself, as requested.
    headers = list(comparison_rows[0])
    markdown_rows = ["| " + " | ".join(headers) + " |"]
    markdown_rows.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in comparison_rows:
        values = []
        for header in headers:
            value = row[header]
            if header == "Series ID":
                value = f"[{value}]({fred_page(value)})"
            values.append(str(value))
        markdown_rows.append("| " + " | ".join(values) + " |")
    st.markdown("\n".join(markdown_rows))
else:
    st.warning("None of the selected series could be downloaded. Check the IDs and try again.")
