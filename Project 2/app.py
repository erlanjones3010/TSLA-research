"""Riverside Community Foundation — investment management app.

    streamlit run app.py

Education, not investment advice. The client is fictional.
"""
import json

import altair as alt
import pandas as pd
import streamlit as st

import config as C
import engine as E

st.set_page_config(page_title="Riverside Endowment App", page_icon="📈", layout="wide")

NAVY, GREEN, RED, AMBER, GREY = "#2F7BBF", "#2E7D4F", "#B23A3A", "#C98A1B", "#6B7685"
ASSET_COLORS = {"SGOV": "#9DB4C8", "TLT": "#5B8DB8", "VCIT": "#2E7D9A", "SPY": "#2B5C8A"}
PORT_COLORS = {"Equal weight": GREY, "60/40 benchmark": AMBER, "Constrained": NAVY}

st.markdown(f"""
<style>
  .block-container {{padding-top: 3.2rem; max-width: 1250px;}}
  .banner {{background: linear-gradient(120deg, #1F5F8B 0%, #163B57 100%); color: #fff;
            padding: 1.4rem 1.8rem; border-radius: 14px; margin-bottom: 1.2rem;}}
  .banner h1 {{color:#fff; font-size: 1.9rem; margin: 0 0 .3rem 0; padding: 0;}}
  .banner p {{color:#D7E3EE; margin: 0; font-size: .95rem;}}
  .card {{background:rgba(127,127,127,.08); border:1px solid rgba(127,127,127,.28); border-radius:12px; padding: .9rem 1.1rem;
          min-height: 118px;}}
  .card .lbl {{opacity:.7; font-size:.72rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; text-transform: uppercase; letter-spacing:.05em;}}
  .card .val {{font-size:1.7rem; font-weight:700; margin-top:.15rem;}}
  .card .sub {{font-size:.82rem; opacity:.7;}}
  .pill {{display:inline-block; padding:.12rem .7rem; border-radius:999px; font-weight:700;
          font-size:1.05rem; color:#fff; margin-top:.35rem;}}
  .stTabs [data-baseweb="tab"] {{font-size: 1rem; font-weight: 600;}}
  .mandate-grid {{display:grid; grid-template-columns: 1fr 1fr; gap: .8rem;}}
  .mandate-grid .card b {{color:{NAVY};}}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="banner">
  <h1>Riverside Community Foundation · Scholarship Endowment</h1>
  <p>Mandate-driven portfolio app — three portfolios, one point-in-time signal, a stress run and a stop rule.
  &nbsp;|&nbsp; <b>Education, not investment advice.</b> Fictional client.</p>
</div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------- sidebar inputs
with st.sidebar:
    st.markdown("### ⚙️ Inputs")
    st.caption("Change a number and the whole app reruns. The mandate of record is config.py.")
    st.markdown("**Estimates**")
    erp = st.slider("Equity risk premium over 10-yr yield", 0.0, 0.08, C.EQUITY_RISK_PREMIUM, 0.005, format="%.3f")
    spread = st.slider("Credit spread over 10-yr yield", 0.0, 0.03, C.CREDIT_SPREAD, 0.0025, format="%.4f")
    window = st.select_slider("Estimation window (months)", [12, 18, 24, 30, 36], C.ESTIMATION_WINDOW_MONTHS)
    cost = st.slider("Trading cost (bps, one way)", 0, 100, C.COST_BPS, 5)
    st.markdown("**Hard limits**")
    eq_min, eq_max = st.slider("SPY range", 0.0, 1.0, (C.LIMITS["equity_min"], C.LIMITS["equity_max"]), 0.05)
    res_min = st.slider("SGOV minimum", 0.0, 0.30, C.LIMITS["reserve_min"], 0.05)
    vol_max = st.slider("Volatility cap", 0.04, 0.20, C.LIMITS["vol_max"], 0.01)

S = {"erp": erp, "spread": spread, "window": window, "cost_bps": cost,
     "limits": {"equity_min": eq_min, "equity_max": eq_max, "reserve_min": res_min, "vol_max": vol_max}}


@st.cache_data
def run(settings_json):
    return E.run_all(json.loads(settings_json))


try:
    out = run(json.dumps(S, sort_keys=True))
except ValueError as e:
    st.error(f"Input error: {e}")
    st.stop()

res = out["results"]
last = res["constrained"]["log"][-1]
LABELS = {"equal": "Equal weight", "benchmark": "60/40 benchmark", "constrained": "Constrained"}
cv = E.verdict(res["constrained"])[0]


def card(col, label, value, sub="", color=None):
    v = f'<span class="pill" style="background:{color}">{value}</span>' if color else f'<div class="val">{value}</div>'
    col.markdown(f'<div class="card"><div class="lbl">{label}</div>{v}<div class="sub">{sub}</div></div>',
                 unsafe_allow_html=True)


def color_verdict(v):
    if v in ("PASS", "GO"):
        return f"background-color:rgba(46,125,79,.22); color:#4CAF73; font-weight:700"
    if v in ("FAIL", "STOP"):
        return f"background-color:rgba(178,58,58,.22); color:#E06666; font-weight:700"
    return ""


def style(df, col="Verdict"):
    sty = df.style
    fn = getattr(sty, "map", None) or sty.applymap
    return fn(color_verdict, subset=[col])


c1, c2, c3, c4, c5 = st.columns(5)
card(c1, "Decision date", last["date"], "latest quarter-end")
card(c2, "10-yr yield", f"{last['dgs10']:.2%}", f"signal {last['signal_status']}")
card(c3, "Return a year", f"{res['constrained']['ann_return']:.1%}",
     f"target {C.OBJECTIVE_RETURN:.1%} nominal")
card(c4, "Constrained verdict", cv, "all hard limits", GREEN if cv == "PASS" else RED)
card(c5, "Stop condition", out["stop"], f"{sum(s['verdict'] == 'FAIL' for s in out['stress'])} of "
     f"{len(out['stress'])} stress fails", GREEN if out["stop"] == "GO" else RED)
st.write("")

tabs = st.tabs(["📋 Mandate", "📡 Signal & data card", "📊 Portfolios", "🧪 Stress & stop",
                "🎯 Recommendation", "💾 Output"])

# ---------------------------------------------------------------- mandate
with tabs[0]:
    lim = C.LIMITS
    st.markdown(f"""
<div class="mandate-grid">
 <div class="card"><b>Client</b><br>{C.CLIENT}. About ${C.RESERVE_SIZE_MILLIONS:.0f} million;
   pays {C.ANNUAL_PAYOUT:.0%} a year for scholarships.</div>
 <div class="card"><b>Objective</b><br>CPI + {C.REAL_RETURN_TARGET:.1%} a year after costs over rolling five-year
   periods (= {C.OBJECTIVE_RETURN:.1%} nominal, assuming CPI of {C.ASSUMED_CPI:.1%}).</div>
 <div class="card"><b>Universe</b><br>{"<br>".join(f"{a} — {C.ASSET_NAMES[a]}" for a in C.ASSETS)}</div>
 <div class="card"><b>Benchmark</b><br>60% SPY / 40% VCIT, rebalanced quarterly.<br><br>
   <b>Risk measure</b><br>Ex-ante annual volatility from the trailing {C.ESTIMATION_WINDOW_MONTHS} months,
   plus backtest maximum drawdown.</div>
 <div class="card"><b>Hard limits</b><br>Long-only, sum to 100% · SPY {lim['equity_min']:.0%}–{lim['equity_max']:.0%}
   · SGOV ≥ {lim['reserve_min']:.0%} · volatility ≤ {lim['vol_max']:.0%} · max drawdown ≤ {lim['drawdown_max']:.0%}
   · turnover ≤ {lim['turnover_max']:.0%} a year</div>
 <div class="card"><b>Process</b><br>Rebalance each quarter-end using only data known on that date.
   Costs of {C.COST_BPS} bps per trade are charged.</div>
</div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------- signal
with tabs[1]:
    left, right = st.columns([3, 2])
    sig = pd.DataFrame(out["signal"].values())
    sig["dgs10_percent"] = sig["dgs10_percent"].astype(float)
    with left:
        st.markdown("#### 10-year Treasury yield, as known on each decision date")
        line = alt.Chart(sig).mark_line(color=NAVY, strokeWidth=2.5, point=alt.OverlayMarkDef(color=NAVY, size=50)).encode(
            x=alt.X("decision_date:T", title=None),
            y=alt.Y("dgs10_percent:Q", title="Yield (%)", scale=alt.Scale(zero=False)),
            tooltip=["decision_date", "observation_date", "dgs10_percent"])
        st.altair_chart(line.properties(height=330), use_container_width=True)
    with right:
        st.markdown("#### Data card")
        st.markdown("""
| | |
|---|---|
| **Series** | DGS10 — 10-yr U.S. Treasury yield, constant maturity, daily, % |
| **Source** | St. Louis Fed, ALFRED (archival FRED) |
| **As-of rule** | Vintage on the decision date; latest observation **before** it |
| **Stale rule** | Stop if older than 7 days |
| **Use** | TLT = yield · VCIT = yield + spread · SPY = yield + equity premium · SGOV = trailing 12-month return |
| **File** | data/dgs10_asof.csv |
| **Limitation** | Spread and premium are assumptions, not estimates |
""")
    with st.expander("Show every point-in-time value"):
        st.dataframe(sig, hide_index=True, use_container_width=True)

# ---------------------------------------------------------------- portfolios
with tabs[2]:
    rows = []
    for k, r in res.items():
        w = r["log"][-1]["weights"]
        v, fails = E.verdict(r)
        rows.append({"Portfolio": LABELS[k], **{a: f"{w[a]:.0%}" for a in C.ASSETS},
                     "Return/yr": f"{r['ann_return']:.1%}", "Vol/yr": f"{r['ann_vol']:.1%}",
                     "Max DD": f"{r['max_drawdown']:.1%}", "Turnover/yr": f"{r['turnover_per_year']:.1%}",
                     "Verdict": v, "Rule failed": "; ".join(fails) or "—"})
    st.markdown("#### Three portfolios, one mandate")
    st.dataframe(style(pd.DataFrame(rows)), hide_index=True, use_container_width=True)
    st.caption(f"Backtest {res['constrained']['start']} to {res['constrained']['end']}, quarterly rebalance, "
               f"{cost} bps cost. Weights are at the latest decision date.")

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("#### Growth of $1")
        growth = pd.DataFrame([{"Date": d, "Value": v, "Portfolio": LABELS[k]}
                               for k, r in res.items() for d, v in r["path"]])
        st.altair_chart(alt.Chart(growth).mark_line(strokeWidth=2.5).encode(
            x=alt.X("Date:T", title=None), y=alt.Y("Value:Q", title="$", scale=alt.Scale(zero=False)),
            color=alt.Color("Portfolio:N", scale=alt.Scale(domain=list(PORT_COLORS), range=list(PORT_COLORS.values())),
                            legend=alt.Legend(orient="bottom")),
            tooltip=["Portfolio", "Date:T", alt.Tooltip("Value:Q", format=".3f")]).properties(height=320),
            use_container_width=True)
    with g2:
        st.markdown("#### Constrained weights at each decision")
        hist = pd.DataFrame([{"Date": d["date"], **d["weights"]} for d in res["constrained"]["log"]])
        st.altair_chart(alt.Chart(hist.melt("Date", var_name="Asset", value_name="Weight")).mark_bar().encode(
            x=alt.X("Date:N", title=None), y=alt.Y("Weight:Q", axis=alt.Axis(format="%")),
            color=alt.Color("Asset:N", scale=alt.Scale(domain=list(ASSET_COLORS), range=list(ASSET_COLORS.values())),
                            legend=alt.Legend(orient="bottom")),
            tooltip=["Date", "Asset", alt.Tooltip("Weight:Q", format=".0%")]).properties(height=320),
            use_container_width=True)

    st.markdown("#### Every mandate check")
    cols = st.columns(3)
    for col, (k, r) in zip(cols, res.items()):
        with col:
            st.markdown(f"**{LABELS[k]}**")
            df = pd.DataFrame([{"Rule": c["rule"], "Value": f"{c['value']:.1f}%",
                                "Verdict": "PASS" if c["pass"] else "FAIL"} for c in r["checks"]])
            st.dataframe(style(df), hide_index=True, use_container_width=True)
    if res["constrained"]["problems"]:
        st.warning("Problems: " + "; ".join(res["constrained"]["problems"]))

# ---------------------------------------------------------------- stress
with tabs[3]:
    st.markdown("#### Stress run on the constrained portfolio")
    sdf = pd.DataFrame([{"Scenario": s["scenario"], **{a: f"{s['latest_weights'][a]:.0%}" for a in C.ASSETS},
                         "Return/yr": f"{s['ann_return']:.1%}", "Max DD": f"{s['max_drawdown']:.1%}",
                         "Turnover/yr": f"{s['turnover_per_year']:.1%}", "Verdict": s["verdict"],
                         "Rule failed": "; ".join(s["failed_rules"]) or "—"} for s in out["stress"]])
    st.dataframe(style(sdf), hide_index=True, use_container_width=True)

    tchart = pd.DataFrame([{"Scenario": s["scenario"], "Turnover": s["turnover_per_year"], "Verdict": s["verdict"]}
                           for s in out["stress"]])
    bars = alt.Chart(tchart).mark_bar(cornerRadiusEnd=4).encode(
        y=alt.Y("Scenario:N", sort=None, title=None, axis=alt.Axis(labelLimit=320)), x=alt.X("Turnover:Q", axis=alt.Axis(format="%"), title="Turnover a year"),
        color=alt.Color("Verdict:N", scale=alt.Scale(domain=["PASS", "FAIL"], range=[GREEN, RED]), legend=None),
        tooltip=["Scenario", alt.Tooltip("Turnover:Q", format=".1%"), "Verdict"])
    rule = alt.Chart(pd.DataFrame({"x": [C.LIMITS["turnover_max"]]})).mark_rule(color=RED, strokeDash=[5, 4]).encode(x="x:Q")
    st.markdown(f"#### Turnover by scenario (dashed line = {C.LIMITS['turnover_max']:.0%} limit)")
    st.altair_chart((bars + rule).properties(height=300), use_container_width=True)

    a, b = st.columns([3, 2])
    with a:
        st.markdown(f"""
**Stop condition** — the process stops if any is true:
1. the constrained portfolio breaks a hard limit in the base backtest;
2. the signal is missing or older than {C.SIGNAL_MAX_AGE_DAYS} days at a decision date;
3. no portfolio meets the limits at a decision date;
4. {C.STRESS_FAIL_STOP} or more stress scenarios break a hard limit.""")
    with b:
        (st.error if out["stop"] == "STOP" else st.success)(
            f"**Stop condition: {out['stop']}**" + ("" if not out["stop_reasons"] else "\n\n" + "; ".join(out["stop_reasons"])))

# ---------------------------------------------------------------- recommendation
with tabs[4]:
    st.markdown("#### What the model supports")
    st.caption("The committee decision itself is in docs/decision-memo.md.")
    left, right = st.columns([3, 2])
    with left:
        rng = pd.DataFrame([{"Asset": a, "Low": lo, "High": hi, "Latest": last["weights"][a]}
                            for a, (lo, hi) in out["range"].items()])
        base = alt.Chart(rng).encode(y=alt.Y("Asset:N", sort=C.ASSETS, title=None))
        band = base.mark_bar(size=22, cornerRadius=4, color="#BCD0E2").encode(
            x=alt.X("Low:Q", axis=alt.Axis(format="%"), title="Weight", scale=alt.Scale(domain=[0, 1])), x2="High:Q")
        dot = base.mark_point(filled=True, size=140, color=NAVY).encode(
            x="Latest:Q", tooltip=["Asset", alt.Tooltip("Low:Q", format=".0%"), alt.Tooltip("High:Q", format=".0%"),
                                   alt.Tooltip("Latest:Q", format=".0%")])
        st.altair_chart((band + dot).properties(height=230), use_container_width=True)
        st.caption("Bar = range across stress scenarios that pass · dot = latest constrained weight")
    with right:
        y = last["dgs10"]
        st.markdown(f"""
**Monitoring triggers** (review at the next quarter-end, or at once if hit)
- 10-yr yield below **{y - 0.0075:.2%}** or above **{y + 0.0075:.2%}**
- Drawdown from peak reaches **15%** (limit 20%)
- Realized 12-month volatility above **{C.LIMITS['vol_max']:.0%}**
- Signal older than **{C.SIGNAL_MAX_AGE_DAYS} days** on a decision date
- Trailing-year turnover above **20%** (limit {C.LIMITS['turnover_max']:.0%})
""")

# ---------------------------------------------------------------- output
with tabs[5]:
    st.markdown("#### Run record")
    record = {"as_of": last["date"], "inputs": S, "signal": {"dgs10": last["dgs10"], "status": last["signal_status"]},
              "verdicts": {k: E.verdict(r) for k, r in res.items()},
              "latest_weights": {k: r["log"][-1]["weights"] for k, r in res.items()},
              "stop": out["stop"], "stop_reasons": out["stop_reasons"], "allocation_range": out["range"]}
    st.download_button("⬇️ Download run record (JSON)", json.dumps(record, indent=2), "run_record.json",
                       "application/json")
    st.json(record, expanded=False)
    st.caption("python run_analysis.py writes the same results to output/results.md and output/results.json.")
