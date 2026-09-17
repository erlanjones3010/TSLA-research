# Lab 08 — Deal Evidence and Valuation Triangulation: Tesla, Inc. (TSLA)

**Valuation date:** September 1, 2026. Prices below are the regular-session closing prices on that date. This lab uses reported GAAP annual diluted EPS, not adjusted EPS.

**Problem / decision:** On September 1, 2026, I am valuing Tesla (TSLA) to decide whether the available evidence supports initiating, watching, or deferring. I set the valuation date and the reported-GAAP-EPS peer policy before selecting candidates, so the comparison does not change to fit a preferred multiple.

## 1. Define / discover

Tesla earns most of its revenue from selling and leasing vehicles, plus automotive regulatory credits. It also sells energy-storage and solar products and related services; its Form 10-K describes automotive and energy generation/storage as its two reportable segments. Tesla reported positive FY2025 diluted EPS of **$1.08** ($3.794 billion of income used in EPS divided by 3.528 billion diluted weighted-average shares). [Tesla FY2025 Form 10-K, filed January 29, 2026, Note 2—Net Income per Share, pp. 61–62](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm).

The closest economic categories are vehicle manufacturers that design, manufacture, market, and support their own vehicles, especially those investing in EVs, software, charging, or energy systems. I still need to research whether Tesla's software/autonomy and energy-storage earnings can be separated reliably enough to support a sum-of-the-parts valuation. I also need a larger set of positive-EPS, directly comparable listed manufacturers; this two-company screen does not establish one.

## 2. Peer policy

I will admit a company only when it is a listed operating company with: (1) material revenue and earnings from designing/manufacturing and selling vehicles; (2) consolidated, positive **reported GAAP annual diluted EPS** available by September 1, 2026; and (3) a U.S.-dollar listed share price that can be paired directly with the reported per-share EPS. EV exposure, direct sales, recurring software/service revenue, and energy products improve the match but are not required.

I will qualify rather than fully use a company when its core vehicle economics match but its product mix, distribution, captive-finance exposure, geography, or technology/energy mix differs materially. I will exclude companies with negative/zero GAAP diluted EPS because P/E is not meaningful, and will exclude companies whose reported EPS cannot be paired with the quoted share price without an unverified ADR or currency conversion. I will not replace GAAP EPS with adjusted EPS just to create a multiple.

## 3. Candidate peers (maximum two)

| Candidate | Fit and important difference | Latest annual reported diluted EPS available by valuation date | Classification |
| --- | --- | --- | --- |
| General Motors (GM) | GM is a global vehicle manufacturer, so its manufacturing, vehicle demand, pricing, warranty, and dealer/service economics provide a real automotive comparison. The important difference is that GM's dealer-led, ICE-heavy model and GM Financial are much more mature than Tesla's direct-sales, EV, energy-storage, and autonomy strategy. | **$3.27**, FY ended Dec. 31, 2025; published/filed **Jan. 27, 2026**. Primary source: [GM FY2025 Form 10-K, Note 21—Earnings Per Share](https://www.sec.gov/Archives/edgar/data/1467858/000146785826000013/gm-20251231.htm). | **Qualify.** Positive GAAP EPS and USD shares make the arithmetic compatible, but the business-model differences are material. |
| Ford Motor (F) | Ford manufactures and sells vehicles and has Ford Blue, Model e, Ford Pro, and Ford Credit, so it is a relevant operating candidate. Its important difference is the captive-finance business and a different dealer/legacy-vehicle mix. | **$(2.06)**, FY ended Dec. 31, 2025; published/filed **Feb. 11, 2026**. Primary source: [Ford FY2025 Form 10-K, Item 7—Results of Operations and Note 25—Earnings Per Share](https://www.sec.gov/Archives/edgar/data/37996/000003799626000015/f-20251231.htm). | **Exclude.** Reported diluted EPS is negative; the filing's $1.09 adjusted diluted EPS is non-GAAP and is not substituted. |

## 4. P/E valuation

The regular-session closing prices were verified in the historical-prices tables published by [Yahoo Finance for TSLA](https://finance.yahoo.com/quote/TSLA/history/?period1=1788220800&period2=1788393600) and [Yahoo Finance for GM](https://finance.yahoo.com/quote/GM/history/?period1=1788220800&period2=1788393600): on **September 1, 2026**, TSLA closed at **$356.09** and GM closed at **$85.63**. These are the unadjusted `Close` values used below, rather than a price from another trading date or an adjusted-price series.

| Company | Same-date price | FY2025 GAAP diluted EPS | P/E |
| --- | ---: | ---: | ---: |
| Tesla | $356.09 | $1.08 | 329.713x |
| GM (qualified peer) | $85.63 | $3.27 | 26.187x |

Applying GM's qualified-peer P/E to Tesla's reported diluted EPS gives a **reference estimate of $28.28 per TSLA share** (26.186544 × $1.08). It is not a peer range because only one candidate met the policy. The calculator is in `lab08_tesla_pe.py`.

## 5. Validation

Manual check: **$85.63 ÷ $3.27 = 26.186544x**, which matches the calculator's GM P/E (rounding only in display).

Removing GM removes the only admitted peer. The implied value therefore changes from **$28.28** to **no peer-P/E estimate**, not to a different numeric result. This happens because Ford was correctly excluded for negative GAAP EPS; treating Ford's adjusted EPS as usable would violate the stated policy and make the sensitivity look more precise than it is.

## 6. DCF comparison

| Method | Result per TSLA share | Date / inputs | Main assumption or limitation |
| --- | ---: | --- | --- |
| Week 3 DCF | $38.82 | Existing `dcf.py`; FY2025 financial inputs, 10.0% WACC, 3.0% terminal growth, five explicit growth rates of 8%, 6%, 5%, 4%, and 3% | FCFF proxy is operating cash flow less capex; terminal value is 72.4% of enterprise value. The intrinsic-value calculation has no market-price input or formal September 1 as-of date. |
| Qualified-peer P/E | $28.28 reference estimate | Sep. 1, 2026 price; FY2025 reported diluted EPS | One qualified peer only; GM does not match Tesla's energy/software/autonomy economics. |

The DCF is $10.54 higher because it embeds positive FCFF growth and a terminal-value assumption, while the P/E method applies the market's much lower multiple for a mature, dealer-led automaker to Tesla's current earnings. Neither result should be mechanically averaged: they answer different questions and both have important model risk.

The `target_share_price = 367.81` input in `dcf.py` is used only by the reverse-DCF routine, not by `calculate_dcf()` or its $38.82 intrinsic-value result. The verified historical-price table shows that $367.81 is TSLA's **September 9, 2026** close; the code's old September 10 label was incorrect. Thus the P/E market price is September 1, the reverse-DCF target price is September 9, and the $38.82 DCF is an FY2025-input model result rather than a market-price-derived September 1 calculation. I have not changed the DCF intrinsic-value calculation merely to force the dates to match.

## 7. AI criticism

**Skeptical criticism:** The comparison mismatches the valuation object: Tesla's market price may reflect expected autonomy, software, and energy value, but GM's GAAP P/E mostly prices a mature automotive/finance business. Also, the reverse-DCF price input is from September 9, 2026 while this P/E valuation date is September 1, 2026.

**Classification: accept.** Tesla's 10-K identifies separate automotive and energy generation/storage segments, while GM's filing discloses GM Financial and a substantially different business mix. The P/E result is therefore a conservative automotive reference, not a fair-value conclusion for all of Tesla. The source check accepts the date criticism in substance but corrects its date: the $367.81 reverse-DCF input is September 9, not September 10. Its $38.82 intrinsic-value output does not change because it is not calculated from that price; a direct market-price comparison should still use one common as-of date.

## AI Partner Validation

I used Codex and Gemini as two independent AI partners during peer discovery. Both received Tesla (TSLA), the September 1, 2026 valuation date, and my peer-selection policy. Their responses helped identify and evaluate possible peer companies, but I independently checked the evidence and primary sources before making final decisions. Based on the evidence documented above, GM is **Qualify** and Ford is **Exclude**.

## 8. Final reflection

GM is included only as a qualified automotive reference; Ford is excluded because the latest reported GAAP EPS is negative. The P/E comparison adds a market-based warning to the DCF: applying a conventional automaker multiple to Tesla's current earnings produces a much lower value than the DCF. The results differ because the DCF assumes growing cash flow and a continuing value, while GM's multiple reflects different growth, risk, finance, and product economics.

**Call: watch / defer.** I would not initiate from this evidence alone. I would reconsider an initiate call if Tesla shows sustained automotive-margin improvement, profitable growth in energy storage, and verifiable evidence that autonomy/software investment earns returns, while an expanded peer screen produces more than one policy-compliant positive-EPS peer. I would move toward do-not-initiate if automotive earnings/cash flow weaken further or capital spending rises without demonstrated returns.

## Items still unresolved

- A direct DCF-versus-market-price comparison still needs one common as-of date if the instructor requires that comparison; the $38.82 model itself is based on FY2025 inputs and has no market-price date.
- Research additional policy-compliant peers. Do not add foreign/ADR peers until share-ratio and currency conversion are documented.
