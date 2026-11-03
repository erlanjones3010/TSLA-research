"""Streamlit interface for Lab 18: Legend Investor as Skill."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

SKILL_SCRIPT = Path(__file__).parent / ".agents" / "skills" / "buffett-investor" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPT))
from sec_buffett import make_memo, run, validate_memo  # noqa: E402

OUTPUT_DIR = Path(__file__).parent / "lab18_outputs"


def render_value(cell: dict, kind: str) -> str:
    if kind == "ROE":
        return "not known" if cell.get("percent") is None else f"{cell['percent']:.1f}%"
    return "not found" if cell.get("millions") is None else f"${cell['millions']:,.1f} million"


def table_frame(analysis: dict) -> pd.DataFrame:
    table = []
    for row in analysis["rows"]:
        record = {"Fiscal year end": row["fiscal_year_end"]}
        for metric in ["Revenue", "Net income", "Operating cash flow", "Capital spending", "Equity", "Owner earnings", "ROE"]:
            record[metric] = render_value(row[metric], metric)
            record[f"{metric} XBRL tag"] = row[metric]["tag"]
        table.append(record)
    return pd.DataFrame(table)


def load_saved(ticker: str) -> dict | None:
    path = OUTPUT_DIR / f"{ticker.upper()}_analysis.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


st.set_page_config(page_title="Lab 18 Buffett Investor", layout="wide")
st.title("Lab 18: Legend Investor as Skill")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

ticker = st.text_input("Ticker", value="COST").strip().upper()
user_agent = st.text_input("SEC-compliant User-Agent (your name and email)", value=os.getenv("SEC_USER_AGENT", ""), type="password",
                           help="Used only for this request; do not place it in source files.")
col1, col2 = st.columns(2)
with col1:
    download = st.button("Download SEC 10-K data", type="primary")
with col2:
    use_saved = st.button("Load saved analysis")

analysis = st.session_state.get("analysis")
if download:
    try:
        analysis = run(ticker, user_agent, str(OUTPUT_DIR))
        st.session_state["analysis"] = analysis
        st.success(f"Downloaded and saved {ticker} SEC EDGAR analysis.")
    except (ValueError, RuntimeError) as error:
        st.error(str(error))
if use_saved:
    analysis = load_saved(ticker)
    if analysis is None:
        st.warning(f"No saved analysis for {ticker}. Download SEC data first.")
    else:
        st.session_state["analysis"] = analysis

if analysis:
    st.subheader(f"{analysis['company']} ({analysis['ticker']}) — annual 10-K facts")
    st.dataframe(table_frame(analysis), use_container_width=True, hide_index=True)
    chart_rows = []
    for row in analysis["rows"]:
        chart_rows.append({"Fiscal year end": row["fiscal_year_end"], "Owner earnings": row["Owner earnings"]["millions"],
                           "Net income": row["Net income"]["millions"]})
    chart = pd.DataFrame(chart_rows).set_index("Fiscal year end")
    st.subheader("Owner earnings and net income")
    st.line_chart(chart)
    st.subheader("Buffett checks")
    checks = analysis["checks"]
    check_columns = st.columns(3)
    for column, (name, result) in zip(check_columns, checks.items()):
        column.metric(name, result.upper())

    memo_path = OUTPUT_DIR / f"{analysis['ticker']}_buffett_memo.md"
    memo = memo_path.read_text(encoding="utf-8") if memo_path.exists() else make_memo(analysis)
    st.subheader("Saved investment memo")
    st.markdown(memo)
    st.subheader("Memo numerical-claim validator")
    st.caption("Checks percentages and monetary amounts; it intentionally ignores years and ticker names.")
    edited_memo = st.text_area("Memo to validate", memo, height=260)
    issues = validate_memo(edited_memo, analysis)
    if issues:
        st.error("; ".join(issues))
    else:
        st.success("No unsupported percentages or monetary amounts detected.")
