# Tesla, Inc. (TSLA) — Company Research Report

**Decision user:** Investment Committee  
**Valuation date:** September 1, 2026  
**Primary source:** Tesla, Inc. Form 10-K for the fiscal year ended December 31, 2025, filed January 29, 2026, accession `0001628280-26-003952`. [SEC filing](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm)

## Business and investment context

Tesla operates automotive and energy generation and storage segments and is pursuing growth in autonomy, Robotaxi, and robotics. Management’s strategy is to use its vehicle, energy, software, and AI capabilities to build a more service-oriented business. [Source: Tesla FY2025 Form 10-K, Item 1, p. 2; Item 7, p. 31]

The investment case has two opposing forces. The automotive business weakened in 2025, while the energy generation and storage business grew quickly and reported stronger segment economics. The central question is whether the newer growth initiatives can offset pressure in automotive without requiring uneconomic investment. [Source: Tesla FY2025 Form 10-K, Item 7, pp. 31, 37–38]

## Operating performance

FY2025 revenue was **$94.827 billion**, down 3% from $97.690 billion in FY2024. Automotive revenue declined 10% to $69.526 billion; automotive sales revenue declined 9%, which management attributed to lower cash deliveries and lower average selling prices driven by sales mix and customer incentives. [Source: Tesla FY2025 Form 10-K, Item 7, p. 37]

Tesla produced approximately **1.66 million** consumer vehicles and delivered approximately **1.64 million** in 2025. Net income attributable to common stockholders was **$3.794 billion**, down from $7.091 billion in 2024. [Source: Tesla FY2025 Form 10-K, Item 7, p. 31; Note 2, p. 61]

Energy generation and storage was the principal positive operating driver: segment revenue increased 27% to **$12.771 billion**, led by higher Megapack and Powerwall deployments. Segment gross margin increased to **29.8%** from 26.2%, and Tesla deployed **46.7 GWh** of energy-storage products in 2025. [Source: Tesla FY2025 Form 10-K, Item 7, pp. 31, 37–38]

## Financial position and capital needs

Tesla ended 2025 with **$16.513 billion** of cash and cash equivalents and **$27.546 billion** of short-term investments. Aggregate debt principal was **$8.180 billion**, including $1.580 billion due within one year. [Source: Tesla FY2025 Form 10-K, Item 7, p. 41; Note 4, pp. 62–63]

Operating cash flow was **$14.747 billion** in 2025, while capital expenditures were **$8.53 billion**. Management expects capital expenditures to exceed **$20 billion** in 2026, driven by AI compute and data centers, manufacturing and R&D capacity, company-operated AI-enabled assets, and service and charging infrastructure. [Source: Tesla FY2025 Form 10-K, Item 7, pp. 31, 41–42]

Tesla reported **3.528 billion** weighted-average diluted shares in FY2025, including a **303 million** diluted impact from stock-based awards. [Source: Tesla FY2025 Form 10-K, Note 2, p. 61]

## What must be proven

- Energy-storage growth and margin expansion must remain durable despite tariffs, product mix, and deployment timing. *Analyst judgment.*
- Automotive delivery growth, manufacturing utilization, and pricing must support automotive margins while Tesla funds new products and AI programs. *Analyst judgment.*
- Autonomy, robotics, and AI-related investments must earn attractive incremental returns rather than merely increase capital intensity. *Analyst judgment.*
- The appropriate enterprise-to-equity bridge treatment for lease liabilities, noncontrolling interests, and other claims remains **UNSOURCED** because the class convention was not provided.

## Research priorities

Review subsequent Tesla filings for vehicle deliveries, automotive gross margin, average selling price, regulatory-credit revenue, factory utilization, energy-storage unit economics, and capital expenditure. Assess the timing, regulatory feasibility, and economics of autonomy, Robotaxi, and other AI initiatives. *Analyst research plan.*

## Falsification question

**Partner-generated question — answer intentionally omitted:** What evidence would show that Tesla’s expected future growth and profitability are not strong enough to justify its current market valuation?

## Investment call

**watch-defer.** Tesla’s liquidity and energy-storage momentum are constructive, but declining automotive revenue and earnings, together with a planned step-up in AI-related capital spending, require more evidence before initiating. *Analyst judgment, informed by Tesla FY2025 Form 10-K, Item 7, pp. 31, 37, 41–42.*

This call would change to **initiate-buy** if Tesla demonstrates sustained improvement in automotive economics and evidence that energy and AI investments generate attractive returns on incremental capital. *Analyst judgment.*

## What changed from Edition A

| Item | Edition A said | Edition B / final model says | Why it changed | Source |
|---|---|---|---|---|
| Investment call | Watch / defer | **Watch / defer** (unchanged) | The model confirms the caution: every method values TSLA far below the share price | `Project 1/README.md` |
| Valuation | No valuation; numerical bridge left open | **$15–$20 per share** (BASE DCF $16.54); methods span $6.84–$39.10 vs. $356.09 (Sep 1, 2026) | Built a five-year FCFF DCF driven by a segment forecast, plus P/E and EV/EBITDA comparables | `valuation.py`, `comps.py` |
| FY2025 energy revenue | $12,270 million | **$12,771 million** | Edition A figure did not match the 27% growth it cited; corrected from the 10-K | FY2025 10-K, Item 7 |
| Debt in the bridge | $8,180 million principal | **$8,376 million** (debt + finance leases, balance sheet) | Use the balance-sheet amount, including finance leases; operating leases not treated as debt | FY2025 10-K balance sheet, p. 49 |
| Other bridge claims | Leases, NCI, other claims "require the class convention" | **Subtract NCI $670M and redeemable NCI $58M; add cash, short-term investments, and digital assets** | Resolved each open bridge line | FY2025 10-K balance sheet, p. 49 |
| Base year | Not normalized | **Normalized FY2025 operating income $4,849M** (reported $4,355M + $494M restructuring) | Restructuring is a one-time cost | FY2025 10-K income statement |
| Energy storage | Growth and margin must prove durable | **Energy margin 30% → 34%** in the base case; massive Megapack commercialization is a trigger toward initiate | Margin rose from 26.2% (FY2024) to 29.8% (FY2025) | FY2025 10-K, Item 7 |
| AI / Robotaxi | Returns on AI investment unproven | **Excluded from BASE; UPSIDE adds Robotaxi/FSD to $40B revenue → $39.10/share**; the price implies about $602B of 2030 autonomy revenue | Shows how much the share price depends on autonomy | `valuation.py` |
| Falsification question | Answer intentionally omitted | **Answered below** | | |

## Answer to the falsification question

**Question (partner-generated):** What evidence would show that Tesla's expected future growth and profitability are not strong enough to justify its current market valuation?

**Answer:** My valuation would be wrong if Tesla does not grow enough to reach the expectations in the reverse DCF. If Robotaxi revenue stays far below about $602 billion or Tesla cannot get close to $183 billion in FCFF by 2030, it would show that the current stock price is hard to support.
