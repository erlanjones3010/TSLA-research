# Lab 11 — Tesla (TSLA) Sensitivity

## V — Check the result

### Check table

| Check | Expected | Actual | Pass/Fail |
|---|---|---|---|
| Base before vs. after the analysis | Same inputs and outputs, within rounding | FY2030 operating income 16,686.4; FCFE 11,728.5; value per share $31.14; `Restored base matches first base run: YES` | Pass |
| Lower/higher runs | Only the selected driver changed; linked items recalculated | Revenue growth paths were 12.0%/12.0%/9.0%/7.0%/5.0% and 18.0%/18.0%/15.0%/13.0%/11.0%; R&D paths were 6.0%/6.0%/5.5%/5.0%/5.0% and 8.0%/8.0%/7.5%/7.0%/7.0%; all runs were valid | Pass |
| Accounting checks | Assets − Liabilities − Equity = 0 on every usable run | 0.0 on every reported usable-run check, except -0.0 for FY2026E in the lower R&D run | Pass |
| Change from base | Changed output minus base output | 15,017.7 − 16,686.4 = −1,668.7 | Pass |

### Sensitivity table

Revenue growth (inputs: % growth; outputs: USD millions except per share)

| Scenario | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 | FY2030 operating income | Change from base | FY2030 FCFE | Change from base | Value per share | Change from base | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Lower | 12.0% | 12.0% | 9.0% | 7.0% | 5.0% | 14566.9 | -2119.5 | 10433.4 | -1295.1 | 27.32 | -3.81 | valid |
| Base | 15.0% | 15.0% | 12.0% | 10.0% | 8.0% | 16686.4 | +0.0 | 11728.5 | +0.0 | 31.14 | +0.00 | valid |
| Higher | 18.0% | 18.0% | 15.0% | 13.0% | 11.0% | 19045.6 | +2359.2 | 13137.4 | +1409.0 | 35.27 | +4.14 | valid |

Span (maximum - minimum across valid lower/base/higher runs): Operating income = 4478.7; FCFE = 2704.0; Value per share = 7.95

R&D % of revenue (inputs: % of revenue; outputs: USD millions except per share)

| Scenario | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 | FY2030 operating income | Change from base | FY2030 FCFE | Change from base | Value per share | Change from base | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Lower | 6.0% | 6.0% | 5.5% | 5.0% | 5.0% | 18355.0 | +1668.6 | 13098.0 | +1369.5 | 35.84 | +4.70 | valid |
| Base | 7.0% | 7.0% | 6.5% | 6.0% | 6.0% | 16686.4 | +0.0 | 11728.5 | +0.0 | 31.14 | +0.00 | valid |
| Higher | 8.0% | 8.0% | 7.5% | 7.0% | 7.0% | 15017.7 | -1668.6 | 10359.0 | -1369.5 | 26.44 | -4.70 | valid |

Span (maximum - minimum across valid lower/base/higher runs): Operating income = 3337.3; FCFE = 2739.0; Value per share = 9.40

### Locked prediction vs. actual

- My locked prediction (written before running): [I WILL FILL IN]
- Actual result: (fill in the actual number for the input I predicted on)
- Why I was off (if I was): [I WILL FILL IN]
- Does this change my valuation view or research priority? Why: [I WILL FILL IN]

### Partner exchange 2 — check each other's evidence

- Result I showed my partner: The R&D higher run (R&D % of revenue +1 percentage point every year). FY2030 operating income fell from 16,686.4 to 15,017.7 (−1,668.7), and value per share fell from $31.14 to $26.44 (−$4.70).
- What my partner checked: My partner recomputed the change from base (15,017.7 − 16,686.4 = −1,668.7), confirmed that revenue growth, gross margin, SG&A, and capex stayed at base, and had me trace the result: higher R&D expense → lower operating income → lower net income → lower FCFE → lower value per share.
- Check I did on my partner's model: I recomputed one of my partner's Walmart changes from base (changed output minus base output = [partner's number]) and confirmed that only their selected driver changed while their other inputs stayed at base.
- Question or correction: My partner asked why FY2030 operating income fell by about 1,669 when R&D rose by only 1 point. I explained that 1% of Tesla's FY2030 revenue (about 166,864) is about 1,669, so the drop matches the R&D increase dollar for dollar.

## E — Find the driver

### Span comparison

| Output | Revenue growth span | R&D % span | Larger span (over these ranges) |
|---|---:|---:|---|
| FY2030 operating income | 4478.7 | 3337.3 | Revenue growth |
| FY2030 FCFE | 2704.0 | 2739.0 | R&D % of revenue |
| Value per share | 7.95 | 9.40 | R&D % of revenue |

State the ranges tested: revenue growth ±3 percentage points each year; R&D % of revenue ±1 percentage point each year.

### My explanation

- Main driver over these ranges: R&D % of revenue was the main driver for FY2030 FCFE and value per share. Revenue growth moved FY2030 operating income more. Over these ranges, R&D had the bigger effect on what Tesla is worth.
- How it flows through the statements: Raising R&D by 1 percentage point raises R&D expense on the income statement every year. That lowers operating income, which lowers net income after tax. Lower net income means lower FCFE, less cash on the balance sheet, and lower equity. Since FCFE drops in every year, the value per share drops too. Revenue growth works differently. Faster growth raises operating income, but it also means Tesla has to carry more inventory, which ties up cash. So part of the extra profit never turns into FCFE, and growth moves value less than it moves operating income.
- Could the ranking come from the ranges I chose? Yes. I moved revenue growth by ±3 points and R&D by only ±1 point, so the two ranges are not the same size. If I had moved R&D by ±0.5 points, revenue growth would probably have been the bigger driver. The FCFE spans are also very close, so that ranking could flip with a small change in range. The ranking holds only over these ranges.

### Partner exchange 3 — explain and compare

- Question I got: Could R&D look like the bigger driver just because of the ranges you chose?
- My answer: Partly, yes. My ranges were different sizes (±3 points for growth, ±1 point for R&D), and the FCFE spans were very close. R&D still moved value per share more ($9.40 span vs. $7.95), so over these ranges it is the bigger driver of value, but a different range could change that.
- Why Tesla's and my partner's company (Walmart) may have different main drivers: Tesla spends heavily on R&D for self-driving, AI, and new products, so R&D is a big cost that moves its value. Walmart is a retailer with very thin margins and little R&D, so small changes in its margin or sales growth likely matter most. We should not compare the two by raw dollar changes, because the companies are very different sizes and businesses.

## AI Partner Validation

I used Codex and Claude as two independent AI partners while building and validating the pro-forma sensitivity analysis. They helped with coding, debugging, planning the lab steps, and drafting parts of the markdown file, but I independently reviewed the work and confirmed the final results.
