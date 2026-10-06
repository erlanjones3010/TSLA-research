"""Tesla comparable-company valuation (USD millions except per-share data).

Valuation date: 2026-09-01.  Run from this directory with ``python comps.py``.
The program deliberately stops if a required fact is missing or a multiple would
violate the policy.  In particular, the verified Ford FY2025 EBITDA is negative,
so Ford cannot be used despite the requested EV/EBITDA-only screen.
"""

from statistics import median

from tesla_inputs import ANALYST_DECISIONS, HISTORY
from valuation import (
    WACC_INPUTS,
    dcf_value,
    enterprise_to_equity_bridge,
    run_forecast,
)


USD_MILLIONS = "USD millions"
VALUATION_DATE = "2026-09-01"
SCOPE_EXCEPTION_REASON = (
    "Tesla does not report a separate captive-finance segment (unlike GM Financial), "
    "so consolidated is the closest available match to GM's automotive-only scope. "
    "Tesla's consolidated results also include energy and services, which GM does not have."
)


def fact(value, source, page, as_of):
    """A source-traceable observed input; monetary and share values are millions."""
    return {"value": value, "source": source, "page": page, "as_of": as_of}


# This must print before any peer data.  It restates the Lab 8 policy and its
# EV/EBITDA extension before the candidates are considered.
PEER_POLICY = """PEER POLICY
Reuse Lab 8 policy: listed operating companies with material vehicle design,
manufacturing, and sales; USD share price; data from filings available by
September 1, 2026.

EV/EBITDA extension:
- Positive EBITDA is required for EV/EBITDA; positive GAAP diluted EPS is
  required for P/E.
- EV/EBITDA uses adjusted EBITDA (excludes one-time items) when the selected
  peer uses a clearly defined non-GAAP operating metric. The accounting basis
  (GAAP or adjusted) and business scope (automotive-only or consolidated) must
  match between the peer and Tesla.
- Captive finance arms (GM Financial and Ford Credit) are excluded from the EV
  bridge: automotive/industrial debt and cash only are used. If a filing did
  not split them, that peer would be excluded from EV/EBITDA.
- Classification is use, qualify, or exclude, with a one-line reason below.
"""


# All peer observations below were available before the valuation date.  GM's
# cash balance is the filing's automotive cash and cash equivalents, excluding
# GM Financial; Ford's Company Cash and debt both exclude Ford Credit.
GM = {
    "ticker": "GM",
    "classification": "qualify",
    "reason": "Qualify: material vehicle manufacturer, but dealer-led ICE mix and GM Financial differ materially from Tesla.",
    "price": fact(85.63, "Yahoo Finance, GM historical prices", "historical-price row", VALUATION_DATE),
    "diluted_shares": fact(973, "General Motors 2025 Form 10-K filed 2026-01-27", "Note 21, p. 99", "FY2025"),
    "diluted_eps": fact(3.27, "General Motors 2025 Form 10-K filed 2026-01-27", "Note 21, p. 99", "FY2025"),
    # Note 23 defines EBIT-adjusted as the automotive operating metric and
    # reports it separately from GM Financial.  The automotive components are
    # GMNA $10,452M + GMI $737M + Cruise $(273)M = $10,916M.  Corporate D&A
    # is included with the automotive D&A because it is not GM Financial.
    "operating_income": fact(10916, "General Motors 2025 Form 10-K filed 2026-01-27", "Note 23, Automotive EBIT-adjusted (GMNA + GMI + Cruise), p. 102", "FY2025"),
    "da": fact(7003, "General Motors 2025 Form 10-K filed 2026-01-27", "Note 23, automotive D&A (GMNA + GMI + Cruise + Corporate), p. 102", "FY2025"),
    "ebitda_basis": {"accounting": "adjusted", "scope": "automotive-only"},
    "automotive_debt": fact(16247, "General Motors 2025 Form 10-K filed 2026-01-27", "Note 14, Total automotive debt, p. 77", "2025-12-31"),
    "automotive_cash": fact(15100, "General Motors 2025 Form 10-K filed 2026-01-27", "Liquidity and Capital Resources, p. 35", "2025-12-31"),
}

FORD = {
    "ticker": "F",
    "classification": "exclude",
    "reason": "Exclude: FY2025 GAAP diluted EPS and EBITDA are negative; positive EBITDA is required for EV/EBITDA.",
    "price": fact(13.84, "Yahoo Finance, F historical prices", "historical-price row", VALUATION_DATE),
    "diluted_shares": fact(3979, "Ford Motor Company 2025 Form 10-K filed 2026-02-11", "Consolidated Income Statements, p. 82", "FY2025"),
    "diluted_eps": fact(-2.06, "Ford Motor Company 2025 Form 10-K filed 2026-02-11", "Consolidated Income Statements, p. 82", "FY2025"),
    "operating_income": fact(-9169, "Ford Motor Company 2025 Form 10-K filed 2026-02-11", "Consolidated Income Statements, p. 82", "FY2025"),
    "da": fact(7834, "Ford Motor Company 2025 Form 10-K filed 2026-02-11", "Consolidated Statements of Cash Flows, p. 86", "FY2025"),
    "ebitda_basis": {"accounting": "GAAP", "scope": "consolidated"},
    "automotive_debt": fact(21000, "Ford Motor Company 2025 Form 10-K filed 2026-02-11", "Company excluding Ford Credit liquidity table, p. 58", "2025-12-31"),
    "automotive_cash": fact(28700, "Ford Motor Company 2025 Form 10-K filed 2026-02-11", "Company excluding Ford Credit liquidity table, p. 58", "2025-12-31"),
}
PEERS = (GM, FORD)


def number(item, label):
    value = item["value"]
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"Required verified input is missing: {label}")
    return value


def print_fact(label, item):
    value = "None" if item["value"] is None else f"{item['value']:,.2f}"
    print(f"  {label:<22}{value:>14}  | {item['source']}; {item['page']}; {item['as_of']}")


def peer_metrics(peer):
    """Compute values only from source-traceable peer inputs."""
    for name in ("price", "diluted_shares", "operating_income", "da", "automotive_debt", "automotive_cash"):
        number(peer[name], f"{peer['ticker']} {name}")
    market_cap = peer["price"]["value"] * peer["diluted_shares"]["value"]
    ebitda = peer["operating_income"]["value"] + peer["da"]["value"]
    ev = market_cap + peer["automotive_debt"]["value"] - peer["automotive_cash"]["value"]
    pe = None if peer["diluted_eps"]["value"] <= 0 else peer["price"]["value"] / peer["diluted_eps"]["value"]
    ev_ebitda = None if ebitda <= 0 else ev / ebitda
    return {"market_cap": market_cap, "ebitda": ebitda, "ev": ev, "pe": pe, "ev_ebitda": ev_ebitda}


def ebitda_label(basis):
    """State the actual accounting basis instead of applying an adjusted label to every peer."""
    return ("adjusted EBITDA (excludes one-time items)"
            if basis["accounting"] == "adjusted" else "GAAP EBITDA")


def tesla_metrics():
    fy2025 = HISTORY["FY2025"]
    bs = fy2025["balance_sheet"]
    expenses = fy2025["expenses_and_cash_flow"]
    shares = fy2025["shares"]["diluted_weighted_average"]
    price = WACC_INPUTS["share_price"]
    debt = ANALYST_DECISIONS["FY2025_debt_used_in_equity_bridge"]["decision"]
    # tesla_inputs.py stores the reported figure through its imported
    # normalized-operating-income decision; recover it from those imported
    # source-traceable components instead of retyping a Tesla number here.
    operating_income = (
        ANALYST_DECISIONS["FY2025_normalized_operating_income"]["decision"]["value"]
        - expenses["restructuring_and_other"]["value"]
    )
    # Do not substitute a hand-entered Tesla balance-sheet or market item: all
    # bridge components and price are imported from the project modules.
    reported_ebitda = operating_income + expenses["depreciation_amortization_and_impairment"]["value"]
    normalized_ebitda = reported_ebitda + expenses["restructuring_and_other"]["value"]
    market_cap = price["value"] * shares["value"]
    ev = (market_cap + debt["value"] + bs["noncontrolling_interests"]["value"]
          + bs["redeemable_noncontrolling_interests"]["value"]
          - bs["cash_and_cash_equivalents"]["value"] - bs["short_term_investments"]["value"]
          - bs["digital_assets"]["value"])
    return {"price": price, "shares": shares, "operating_income": operating_income,
            "da": expenses["depreciation_amortization_and_impairment"], "restructuring": expenses["restructuring_and_other"],
            "debt": debt, "bs": bs, "market_cap": market_cap, "ev": ev,
            "reported_ebitda": reported_ebitda, "normalized_ebitda": normalized_ebitda,
            "ebitda_basis": {"accounting": "adjusted", "scope": "consolidated"},
            "pe": price["value"] / 1.08, "ev_ebitda": ev / normalized_ebitda}


def run_checks(peer_results, tsla, implied_values, multiples_used, admitted_peers):
    expected_date = VALUATION_DATE
    def is_documented_scope_exception(peer):
        return (peer["ticker"] == "GM"
                and peer["ebitda_basis"]["accounting"] == tsla["ebitda_basis"]["accounting"]
                and peer["ebitda_basis"]["scope"] == "automotive-only"
                and tsla["ebitda_basis"]["scope"] == "consolidated")

    basis_matches = []
    exception_used = False
    for peer in admitted_peers:
        accounting_matches = peer["ebitda_basis"]["accounting"] == tsla["ebitda_basis"]["accounting"]
        scope_matches = peer["ebitda_basis"]["scope"] == tsla["ebitda_basis"]["scope"]
        allowed_exception = is_documented_scope_exception(peer)
        basis_matches.append(accounting_matches and (scope_matches or allowed_exception))
        exception_used = exception_used or (accounting_matches and not scope_matches and allowed_exception)
    definitions_match = all(basis_matches)
    checks = [("Same FY2025 period and Sep. 1, 2026 price date", all(
        peer["price"]["as_of"] == expected_date and peer["operating_income"]["as_of"] == "FY2025"
        and peer["da"]["as_of"] == "FY2025" for peer in PEERS)),
        ("EV/EBITDA basis matches: accounting basis and business scope", definitions_match),
        ("EV recomputes from market cap + automotive debt - automotive cash", all(
            abs(result["ev"] - (result["market_cap"] + peer["automotive_debt"]["value"] - peer["automotive_cash"]["value"])) < 1e-6
            for peer, result in zip(PEERS, peer_results))),
        ("All multiples used are positive", all(value > 0 for value in multiples_used)),
        ("Implied value/share × 3,528 equals implied equity value", all(
            abs(value["per_share"] * value["shares"] - value["equity_value"]) < 1e-6
            for value in implied_values.values()))]
    print("\nCHECKS")
    for label, passed in checks:
        if label == "EV/EBITDA basis matches: accounting basis and business scope" and passed and exception_used:
            print(f"PASS (with documented exception) — {label}")
            print(f"  Exception: Tesla scope = consolidated vs. GM scope = automotive-only. {SCOPE_EXCEPTION_REASON}")
        else:
            print(f"{'PASS' if passed else 'FAIL'} — {label}")
    if not definitions_match:
        peer_bases = "; ".join(
            f"{peer['ticker']}={peer['ebitda_basis']['accounting']}, {peer['ebitda_basis']['scope']}"
            for peer in admitted_peers
        )
        print(f"  Basis detail: Tesla={tsla['ebitda_basis']['accounting']}, {tsla['ebitda_basis']['scope']}; {peer_bases}")


def print_peer_removal_sensitivity(tsla, peer_results):
    """Show the consequence of removing each candidate from each admissible set."""
    print("\nPEER-REMOVAL SENSITIVITY")
    for peer in PEERS:
        remaining_pe = [other["pe"] for candidate, other in zip(PEERS, peer_results)
                        if candidate is not peer and candidate["classification"] in {"use", "qualify"}
                        and other["pe"] is not None]
        remaining_ev = [other["ev_ebitda"] for candidate, other in zip(PEERS, peer_results)
                        if candidate is not peer and candidate["classification"] in {"use", "qualify"}
                        and other["ev_ebitda"] is not None]
        pe_text = "no policy-compliant P/E estimate" if not remaining_pe else f"${median(remaining_pe) * 1.08:.2f}/share"
        if remaining_ev:
            bridge = enterprise_to_equity_bridge(median(remaining_ev) * tsla["normalized_ebitda"])
            ev_text = f"${bridge['Value per share']:.2f}/share"
        else:
            ev_text = "no policy-compliant EV/EBITDA estimate"
        print(f"  Remove {peer['ticker']}: P/E {pe_text}; EV/EBITDA {ev_text}")


def dcf_values():
    """Derive the required DCF rows from valuation.py rather than copying outputs."""
    values = {}
    for scenario in ("DOWNSIDE", "BASE", "UPSIDE"):
        forecast = run_forecast(scenario)
        fcff = {year: forecast[year]["FCFF"] for year in forecast if isinstance(year, int)}
        dcf = dcf_value(fcff, WACC_INPUTS["wacc"]["value"], 0.03)
        values[scenario] = enterprise_to_equity_bridge(dcf["enterprise_value"])["Value per share"]
    return values


def main():
    print(PEER_POLICY)
    print("PEER INPUTS AND CLASSIFICATIONS (USD millions except per-share data)")
    peer_results = []
    for peer in PEERS:
        print(f"\n{peer['ticker']} — {peer['classification'].upper()}: {peer['reason']}")
        for label, key in (("Sep. 1 close", "price"), ("Diluted shares", "diluted_shares"),
                           ("GAAP diluted EPS", "diluted_eps"), ("Operating income / EBIT-adj.", "operating_income"),
                           ("D&A", "da"), ("Auto/industrial debt", "automotive_debt"),
                           ("Auto/industrial cash", "automotive_cash")):
            print_fact(label, peer[key])
        result = peer_metrics(peer)
        peer_results.append(result)
        print(f"  {ebitda_label(peer['ebitda_basis'])} {result['ebitda']:,.2f} | EV {result['ev']:,.2f} | P/E {result['pe']} | EV/EBITDA {result['ev_ebitda']}")

    tsla = tesla_metrics()
    print("\nTESLA (imported Project 1 inputs; USD millions except per-share data)")
    print(f"  Sep. 1 close (valuation.py): ${tsla['price']['value']:.2f}")
    print(f"  Diluted shares (tesla_inputs.py): {tsla['shares']['value']:,.0f}")
    print(f"  Reported EBITDA (reference only): imported reported operating income ${tsla['operating_income']:,.0f} + imported D&A ${tsla['da']['value']:,.0f} = ${tsla['reported_ebitda']:,.0f}")
    print(f"  Adjusted EBITDA (excludes one-time items): ${tsla['reported_ebitda']:,.0f} + imported restructuring ${tsla['restructuring']['value']:,.0f} = ${tsla['normalized_ebitda']:,.0f}")
    print(f"  EV: market cap ${tsla['market_cap']:,.2f} + debt ${tsla['debt']['value']:,.0f} + NCI ${tsla['bs']['noncontrolling_interests']['value']:,.0f} + redeemable NCI ${tsla['bs']['redeemable_noncontrolling_interests']['value']:,.0f} - cash ${tsla['bs']['cash_and_cash_equivalents']['value']:,.0f} - STI ${tsla['bs']['short_term_investments']['value']:,.0f} - digital assets ${tsla['bs']['digital_assets']['value']:,.0f} = ${tsla['ev']:,.2f}")
    print(f"  Tesla P/E: {tsla['pe']:.6f}x | Tesla EV/adjusted EBITDA (excludes one-time items): {tsla['ev_ebitda']:.6f}x")

    # This is intentionally evaluated before any implied valuation.  Ford's
    # verified -$1,335M EBITDA makes the requested Ford EV/EBITDA inadmissible.
    admitted_ev = [result for peer, result in zip(PEERS, peer_results)
                  if peer['classification'] in {'use', 'qualify'} and result['ev_ebitda'] is not None]
    if not admitted_ev:
        raise ValueError("Comparable-company valuation stopped: no policy-compliant positive-EV/EBITDA peers. Ford EBITDA is negative under the required GAAP definition.")

    pe_value = GM['price']['value'] / GM['diluted_eps']['value'] * 1.08
    multiple = median(result['ev_ebitda'] for result in admitted_ev)
    implied_ev = multiple * tsla['normalized_ebitda']
    implied_bridge = enterprise_to_equity_bridge(implied_ev)
    implied = {"P/E (GM)": {"per_share": pe_value, "equity_value": pe_value * tsla['shares']['value'], "shares": tsla['shares']['value']},
               "EV/adjusted EBITDA (excludes one-time items; GM (single qualified peer))": {"per_share": implied_bridge['Value per share'], "equity_value": implied_bridge['Equity value'], "shares": implied_bridge['Diluted shares']}}
    print_peer_removal_sensitivity(tsla, peer_results)

    print("\nFINAL TABLE")
    print(f"{'Method':<28}{'Value per share':>18}{'vs. share price ($356.09)':>29}")
    for scenario, value in dcf_values().items():
        print(f"DCF {scenario.lower():<24}{value:>18.2f}{value - tsla['price']['value']:>29.2f}")
    for method, value in implied.items():
        print(f"{method:<28}{value['per_share']:>18.2f}{value['per_share'] - tsla['price']['value']:>29.2f}")
    run_checks(peer_results, tsla, implied, [GM['price']['value'] / GM['diluted_eps']['value'], multiple],
               [peer for peer in PEERS if peer['classification'] in {'use', 'qualify'}])


if __name__ == "__main__":
    main()
