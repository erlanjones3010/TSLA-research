# Video 2 Transcript — Code and Validation

**Project:** FIN 43900 Project 1, Tesla (TSLA)
**Video file:** Screen Recording 2026-10-09 at 5.28.11 PM.mov (13:22)
**Question this video answers:** How does the submitted code produce the result, and what high-risk test passed or failed?



---

**[0:00] Intro**

Hi, I'm Erlan Jones. This is Video 2 for my Project 1 Tesla valuation. It answers two questions: how does my submitted code produce the result, and what high-risk test passed or failed? I'll do them in that order.

Before that, the question is whether our fund should buy Tesla stock. This README shows the setup: the decision, the valuation date, the diluted share count, what I left out, and my results. If you want to read more, you can go to the results file. You don't have to run any of the files; you can read the results from there.

**[0:41] Running everything**

When I run my run_all file, it runs all six files in order: the inputs, the five-year forecast, the valuation, the peer comparison, and two test files. I'll wait for it to load.

At the summary, they all say OK. What does OK mean? Each file has checks written into it. A check is a rule that compares two numbers that must agree. For example, in every forecast year, assets minus liabilities minus equity has to equal zero. Another one: when I raise the WACC, the value per share has to go down.

If I go to my pro forma output and search "balance sheet balances," it runs that for each year, and it shows PASS. If a rule holds, the code prints PASS and keeps going. If a rule breaks, the code raises an error and stops right there, so it never prints a value built on a mistake. run_all prints OK only if the file made it all the way to the end. So OK means every check in that file passed, and six OKs, shown here, means every check in the project passed.

I also ran this from a fresh download of my GitHub repo and recorded it, so you can watch that as well under the cold run recording. It worked the same way. So I know the code runs cleanly. Now let's look at how it actually gets to the answer.

**[2:20] Question 1: How does the submitted code produce the result?**

When I go to the Tesla inputs file and go to line 42, it shows 78,509. So, the first question: how does my code produce the result? It starts with the data. This file holds Tesla's real numbers from its 10-K filings for 2023 through 2025. Every number is stored with its source, the page it came from, the date, and whether it's a fact, a normalization, or a forecast.

I didn't just trust these. I opened the 10-K myself and checked the key ones, like total liabilities and redeemable noncontrolling interests on the balance sheet, page 49, and operating income of $4.355 billion. It shows the exact numbers and where I checked them. I double-checked everything, because when VS Code pulls numbers, sometimes there's a mistake, and I have to check that as well.

**[3:14]** If I type in "normalized 4,849," that's the operating income. The file also checks itself. It confirms the revenue lines add up to total revenue, and that assets equal liabilities plus equity, for all three years.

I also made two analyst decisions here. First, I added back $494 million of one-time restructuring, so my clean 2025 operating income is about $4.85 billion. Second, I used $8.4 billion of debt and finance leases in the bridge. I didn't count operating leases as debt, because their cost is already in operating expenses. With the starting numbers set, the next step is the forecast.

**[4:13] Forecast**

When I type in "three-statement," here's the forecast. It builds each part of Tesla separately: car deliveries times price, energy storage gigawatt-hours times price, and services. It builds a full income statement, balance sheet, and cash flow statement for 2026 to 2030, in three scenarios: downside, base, and upside. Every year, the balance sheet has to balance and the cash flow has to tie to the balance sheet, or the file stops and shows an error. The file runs cleanly, so there's no error.

**[4:52]** When I go to the cash flow statement, and to free cash flow: the big factor here is capex. Tesla plans over $20 billion next year, so free cash flow is negative from 2026 to 2028, about minus $10.6 billion in 2026, and only reaches about $5.3 billion by 2030.

**[5:29] WACC**

Next are the WACC inputs. To turn that cash into a value today, I need a discount rate, the WACC. I built it from market data on my valuation date: a 4.79% ten-year Treasury yield, a beta of 1.83 from Yahoo Finance, and a 4.14% equity risk premium from Damodaran. That gives a cost of equity of about 12.4%. Tesla has very little debt, so the WACC is about 12.3%. That's high, because Tesla's stock is much more volatile than the market.

**[6:04] DCF and bridge**

My forecast covers five years, so the terminal value captures everything after 2030 at 3% growth forever. Because the first three years are negative, the terminal value is actually bigger than the whole enterprise value. So most of Tesla's value in my model comes after 2030.

With the enterprise-to-equity bridge: the DCF gives the value of the whole business. To get to shareholders, I add $44 billion of cash and investments plus digital assets, subtract $8.4 billion of debt and the noncontrolling interests, and divide by about 3.5 billion diluted shares, which gives about $16.54 per share.

**[6:48] Scenarios**

In the scenario summary, the downside is $6.84, and the upside, which adds a Robotaxi business, is about $39.10. The stock trades at $356, which is far higher than any case we ran.

The code also runs a reverse DCF that solves for what the price implies. I'll explain what that means for the decision in Video 3. So that's how the code produces the result: it takes Tesla's 10-K numbers, builds a forecast that has to balance every year, discounts the cash flow at 12.3%, and bridges to $16.54 a share. Before I trust that number, I want to check it against how the market values a similar company.

**[8:06] Peer comparison**

If I type in "peer policy": I didn't just look at Tesla alone; I compared it to other carmakers. I wrote my rules for choosing peers first, before picking any, so I couldn't choose companies that gave me the answer I wanted. A peer has to be a listed company that designs, builds, and sells vehicles, with positive earnings, and every company is measured the same way, with lending businesses taken out.

**[8:39]** Ford's EPS and EBITDA are negative, so Ford didn't qualify. Its 2025 earnings and EBITDA were both negative, and a negative multiple doesn't say anything useful about value. GM did qualify, and I checked its earnings, debt, and share price against its 10-K myself. Using GM's multiples gives Tesla about $28 a share on price-to-earnings and about $25 on EV to EBITDA. That's why we didn't go with Ford; we went with GM.

**[9:24]** My checks caught two mismatches. First, GM reports an adjusted profit number, while Tesla's was straight GAAP, so I used Tesla's normalized EBITDA of about $11 billion to compare like with like. Second, GM's numbers leave out its lending business, GM Financial, while Tesla's are company-wide. Tesla doesn't report a separate finance segment, so I couldn't remove that difference, because Tesla has everything in one pile compared to GM. I documented that as an exception instead of hiding it, and any other mismatch would still fail the check.

**[9:59]** In the final table, I didn't average the methods together. Peers come in a bit higher than my DCF because GM is valued as a steady car business, while my forecast has Tesla using up cash for the next few years. Either way, every method lands between about $7 and $39. Each method gives me a number, so the next question depends on the company as well, and the tests show whether it passed or failed.

**[10:38] Question 2: What high-risk test passed or failed?**

So how do we validate this? When we go to "value per share," we come to the second question: what high-risk test passed or failed? First, I checked the math. I ran the class training case through the same DCF code, and all 18 checks match, including $27.50 per share. Then I tried to break it.

**[11:06]** When I move over here, it shows my answer: my highest-risk test passed. If 2030 cash flow turns negative, the terminal value would treat a loss as permanent. My downside is only about $1 billion in 2030, so that's a real risk. When I forced it negative, the model stopped instead of giving a fake number. Growth equal to WACC, an unbalanced balance sheet, and zero shares all stopped it too.

**[11:44] Locked prediction**

In my locked prediction file: before any AI help, I wrote my predictions and locked them for changing growth from 3% to 5%. In Part 2, the results after running it, I got the direction right, but it rose about 16%, a big change compared to what I said, because most of my value is terminal value, which comes in later years. It didn't change my recommendation: about $15 to $17 is not even close to $356.

**[12:21] Cold run and AI use**

Last, I did a cold run from a fresh GitHub download, and everything passed.

With AI assistance, I checked everything, including help with the 10-K filings, as you can see. Nothing failed, and if there was a problem, I double-checked it myself. AI assisted me and helped with brainstorming; it didn't create the whole thing for me. Working with AI was a big help that got me through this, and it assisted with a lot of things, such as creating some tables. I came up with the ideas, and it assisted me.

All right, with that, thank you.
