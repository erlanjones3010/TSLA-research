# Assumption-Challenge Record — Project 1 (Tesla, TSLA)

Each load-bearing driver: **value · basis · challenge · evidence that would change it**.
Values are the BASE scenario unless noted (USD millions unless noted). Source of every driver: `proforma.py` and `valuation.py`.
Result with these drivers: BASE **$16.54**, DOWNSIDE **$6.84**, UPSIDE **$39.10** per share vs. **$356.09** share price (Sep 1, 2026).

## 1. Load-bearing drivers

| # | Driver | Value (2026 → 2030) | Basis | Challenge | Evidence that would change it | Status |
|---|---|---|---|---|---|---|
| 1 | Vehicle deliveries growth | 3%, 6%, 7%, 6%, 5% (1.64M in FY2025 → 2.13M) | Deliveries fell in 2025; assumes a slow recovery, not a return to fast growth | Sales could keep falling as in 2025, or rise faster if cheaper models sell well | Quarterly delivery reports; new model launches | Accepted by Erlan |
| 2 | Automotive revenue per vehicle | −1% in 2026, then flat (~$39,700) | 2025 prices fell on mix and incentives; assumes pricing stabilizes | More price cuts or a cheaper model would lower it | Average selling price commentary in 10-Qs; price cuts | Accepted by Erlan |
| 3 | Regulatory credits | 1,200; 800; 500; 300; 200 (FY2025: 1,993) | FY2025 10-K: government actions, including the OBBBA, restricted some credit programs; other automakers need fewer credits | Credits are almost pure profit, so faster loss hurts margins more; rules could also last longer | Regulatory-credit revenue in 10-Qs; policy changes | Accepted by Erlan |
| 4 | Energy storage GWh growth | 25%, 20%, 18%, 15%, 12% (46.7 GWh in FY2025) | Strong 2025 growth (+27% revenue), fading as the business scales | Deployment timing is lumpy; tariffs could slow growth | Quarterly deployment numbers; Megapack factory ramp | Accepted by Erlan |
| 5 | Energy revenue per GWh | −3% per year | Prices fall with competition | Prices could fall faster | Megapack pricing; competitor pricing | Accepted by Erlan |
| 6 | Automotive gross margin ex credits | 16.0%, 17.5%, 19.0%, 20.0%, 20.0% (FY2025: 15.4%) | Partial recovery from cost cuts, cheaper models, and better factory utilization; not a return to 2022 levels | Tariffs, price cuts, or underutilization could keep it near 15% (DOWNSIDE case) | Automotive gross margin in 10-Qs; price cuts; tariff costs | Accepted by Erlan |
| 7 | Energy gross margin | 30%, 31%, 32%, 33%, 34% (FY2024: 26.2%; FY2025: 29.8%) | Margin rose from 26.2% to 29.8%; I expect it to keep rising as Megapack production scales | Tariffs on battery cells and price competition could stop the rise | Energy segment gross margin in 10-Qs; tariff costs; Megapack pricing | Revised by Erlan (was 30% flat) |
| 8 | R&D % of revenue | 6.8%, 6.5%, 6.2%, 5.8%, 5.5% (FY2025: 6.8%) | R&D grows in dollars but more slowly than revenue | AI, Robotaxi, and Optimus spending could stay structurally higher | R&D expense in 10-Qs; management commentary | Accepted by Erlan |
| 9 | SG&A % of revenue | 6.0%, 5.7%, 5.4%, 5.2%, 5.0% (FY2025: 6.2%) | Scale benefits as revenue grows | New services and products may add overhead | SG&A in 10-Qs; headcount commentary | Accepted by Erlan |
| 10 | Capex | 20,500; 18,000; 15,000; 13,000; 12,000 (FY2025: 8,527) | Tesla guided 2026 capex "in excess of $20 billion"; later years are my judgment as build-outs mature | Tesla says capex is hard to project beyond the short term; AI compute could keep it higher | Capex in 10-Qs; updated guidance | Erlan – from Lab 11 |
| 11 | Depreciation from new capex | Charged below gross profit (D&A above FY2025's 6,148) | New factories, AI compute, and fleet assets add depreciation that FY2025 margins do not include | If efficiency offsets it, margins would be higher | D&A and segment margins in 10-Qs | Erlan – chosen option (a) |
| 12 | Tax rate | 25% normalized | FY2023–FY2025 reported rates are distorted by valuation-allowance changes | Actual rate could be closer to 21% | Effective tax rate in 10-Qs/10-K | Erlan – from Lab 11 |
| 13 | WACC | 12.30% (risk-free 4.79%, beta 1.83, ERP 4.14%) | CAPM with market inputs verified on Sep 1, 2026 | Beta is current, not as of Sep 1; a lower beta raises value | Treasury yield; Tesla beta; Damodaran ERP | Accepted by Erlan (inputs verified) |
| 14 | Terminal growth | 3.0% | Long-run nominal growth; no permanent Robotaxi/Optimus windfall | At 5%, BASE rose only ~$2 (Locked Changed-Input Record) | Long-run GDP/inflation outlook | Erlan – from Lab 11 |
| 15 | Robotaxi/FSD revenue (UPSIDE only) | 0; 2,000; 8,000; 20,000; 40,000 at 50% margin | Assumes paid Robotaxi/FSD scales from 2027 with regulatory approval | No large paid driverless service exists yet; share price implies ~$605B of 2030 autonomy revenue | Robotaxi launches and approvals; paid FSD subscribers; 10-Q disclosures | Accepted by Erlan (deliberately optimistic) |

## 2. Partner fresh-eyes challenges (Weeks 5–6 labs)

| # | Challenger | Challenge | My answer | Effect on model |
|---|---|---|---|---|
| P1 | Lab partner — **Oliana Ozbaki** (Tesla Part 1, pro-forma assumptions) | "Why does the FY2026 gross-margin judgment start at 18.0% when the model also assumes 15% revenue growth and more than $20 billion of capital spending, and what evidence would make that number too high or too low?" | The starting point is anchored to the recent margin rather than assuming growth restores earlier profitability; it rises only if pricing/mix and energy margin improve while utilization absorbs the investment. | Project 1 replaced the single margin with segment margins (drivers 6–7) and added the depreciation charge (driver 11). |
| P2 | Lab partner — **Cara Riney** (Lab 11, partner exchange 2) | Why did FY2030 operating income fall by about 1,669 when R&D rose by only 1 point? | 1% of FY2030 revenue (about 166,864 in Lab 11) is about 1,669, so the drop matches dollar for dollar. | Confirms R&D % (driver 8) passes straight through to EBIT. |
| P3 | Lab partner — **Cara Riney** (Lab 11, partner exchange 3) | Could R&D look like the bigger driver just because of the ranges you chose? | Partly yes — ranges differed (±3 pts growth vs. ±1 pt R&D); R&D still moved value more over those ranges. | Ranges matter when comparing drivers; scenarios in Project 1 change drivers with stated causes. |

## 3. Which drivers matter most

- **Most of the value is in the terminal value** (BASE terminal value > 100% of EV because 2026–2028 FCFF is negative), so WACC, terminal growth, and 2030 margins carry the valuation.
- **No single driver closes the gap to $356.09.** Even the UPSIDE case (Robotaxi at $40B revenue) reaches only $39.10; the reverse DCF needs about $183B of 2030 FCFF.
