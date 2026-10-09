# Video 2 Transcript — Code and Validation

**Project:** FIN 43900 Project 1, Tesla (TSLA)
**Video file:** Screen Recording 2026-10-09 at 5.28.11 PM.mov (13:22)
**Question this video answers:** How does the submitted code produce the result, and what high-risk test passed or failed?

_How this transcript was made: word-for-word speech-to-text (faster-whisper, small.en model), with Claude's help fixing only words the software misheard (for example "WOC" → "WACC," "Denver Duran" → "Damodaran," "gap" → "GAAP"). Nothing was cut or reworded. I reviewed it against the recording._

---

[0:00] Hi, I'm Erlan Jones. This is video two for my project one Tesla valuation.
[0:05] So it answers two questions. How does my submitted code produce result?
[0:10] And what high risk test passed or failed? And I'll just do them in that order. So
[0:15] before that, the question is whether our fund should buy Tesla stock. This README shows the
[0:22] setup, the decision, the valuation date, the diluted share count, what I left out and my results.
[0:30] And if you want to read more of that stuff, you can go to results file and you don't have to run
[0:36] any of the files. You can just read them from here. That shows the results.
[0:41] So when I go to our my run_all file, this file runs all six files in order, inputs, the five year
[0:50] forecast, the valuation, the peer comparison and two test files. So wait for this to load real quick.
[1:00] And then at the summary, they all say okay. But what does okay mean? So each file has checks
[1:07] run into it. A check is a rule that compares two numbers that must agree. For example,
[1:11] in every forecast year assets minus liabilities minus equity has to equal zero. Another one
[1:18] is when I raise the WACC, the value per share has to go down. So if I go to my balance sheet,
[1:30] go to my pro forma on balance sheet balances, and it runs all that for each year. And then with that,
[1:43] it will show pass. So if a rule holds the code prints pass and keeps going. If a rule breaks,
[1:48] the code raises an error and stops right there. So it never prints a value built on a mistake.
[1:54] So run_all prints. Okay, if the file made it all the way to the end.
[1:58] So okay means every check in that file pass and six okay, which shows it here means every check
[2:03] in that project passed. I also ran this from a fresh download of my GitHub repo and recorded it.
[2:09] So you can watch that as well, because it worked the same way under cold run recording as well.
[2:15] So with that, I know the code runs cleanly. Now let's look at how it actually gets the
[2:20] answer. So question one, how does the submitted code produce the result? So when I go to the
[2:24] tesla_inputs file, and then go to 42, it shows 78,508. So with that, what is our first question? How
[2:36] does my code produce result? It starts with the data. This file holds Tesla's real numbers from
[2:40] its 10-K filings for 2023 through 2025. Every number is stored with its source. The page it
[2:46] came from the date, whether it's a fact, a normalization or a forecast. I didn't just trust
[2:51] these I opened the 10-K myself and check the key ones like total liabilities and redeemable
[2:55] non controlling interest in the balance sheet, page 49 and operating income of 4.35 billion dollars.
[3:02] So line 49 and just shows just the exact numbers and where I checked it. Just double checked it
[3:08] everything because as and vs code as it pulls, sometimes it's a mistake. And I have to check
[3:14] that as well. So right here, it shows
[3:25] if I type in
[3:33] so with the normalized 4849 is the operating income. With that, so the file also checks itself,
[3:41] it confirms revenue lines add up to total revenue and the assets equal liabilities plus equity for
[3:47] all three years. I also made two analyst decisions here. First I added back 494 million dollars of
[3:55] one-time restructuring. So my clean 2025 operating income is about 4.85 billion dollars. Second,
[4:00] I use 8.4 billion dollars of debt and finance leases in the bridge. I didn't count operating
[4:06] leases as a debt because its cost is already in operating expenses with the strong with the
[4:13] starting number set. The next step is the forecast. So when I type in the three statement here forecast
[4:22] with this the forecast build each part of Tesla separately car deliveries time per times car
[4:28] deliveries times price energy storage gigawatt-hours times price and services. It builds a full income
[4:34] statement balance sheet and cash flow statement for 2026 to 20, to 2030 and three scenarios downside
[4:41] base and upside with that as well. So every year the balance sheet has to balance and the cash
[4:47] flow has to tie to the balance sheet or the file stops and it will say error and the file runs
[4:52] cleanly so there's no error. So when I go to the cash flow statement right here
[5:04] and go to the free cash flow. All right go to free cash flow. The big factor of this is
[5:15] CapEx. So with this Tesla plans over 20 billion dollars next year. So free cash flow is negative
[5:23] from 2026 to 2028 about minus 10.6 billion dollars in 2026 and only reaches about 5.3
[5:29] billion dollars by 2030. So what does that mean? So another reason we can look is the WACC inputs. So
[5:38] to turn that cash in the value today I need to discount rate the WACC. I build it from market
[5:43] data on my valuation date a 4.79 percent 10 year treasury yield a beta of 1.83 from Yahoo Finance
[5:51] and a 4.14 percent equity risk premium from Damodaran that gives a cost of equity of
[5:58] about 12.4 percent. Tesla has very little debts the WACC is about 12.3 percent. That's high because
[6:04] Tesla stock is much more volatile than the market. So when I'm looking at this as well the enterprise
[6:14] equity since my forecast covers five years the terminal value captures everything after 2030
[6:19] at 3 percent growth rate forever. Because the first three years are negative the terminal value
[6:24] is actually bigger than the whole enterprise value. So most of Tesla's value in my model comes
[6:28] after 2030. So with the enterprise to equity the DCF gives the whole value of the business.
[6:37] To get shareholders I add 44 billion dollars of cash and investments plus digital assets subtract
[6:42] 8.4 billion dollars of debt and the non-controlling interest and divided by about 3.5 billion dollars
[6:48] in diluted shares which gives around 16.54 dollars per share. And then with the scenario summary
[7:01] the downside of it is six dollars and 84 cents which adds and the upside which adds like the
[7:10] Robotaxi business is around 39 dollars and 10 cents and however the stock does trade at 356
[7:16] dollars which is way highly expected than when we ran this case. So
[7:39] so with this the code also runs a reverse DCF that solves for what the price implies.
[7:45] I'll explain what that means for the decision in video three. So that's how the code produces
[7:50] result it takes the Tesla's 10-K numbers builds a forecast that has to balance every year
[7:54] discounts the cash flow at 12.3 percent and bridges to 16 dollars and 54 cents a share
[7:59] before I touch that number I want to check it against how the market values a similar company.
[8:06] So if I type in peer policy
[8:08] I didn't just compare it just to Tesla I compared it to other car market other car makers. I wrote
[8:17] my rules for choosing peers first because pick any before picking any so I couldn't choose companies
[8:23] that gave me the answer I wanted. I peer has to be listed has to be a listed company that designs
[8:27] build and sells vehicles with positive earnings and every company is measured the same way
[8:32] with lending business take businesses taken out.
[8:39] So with EPS and EBITDA EBIT are negative. So with that it's Ford didn't qualify its 25 2025 earnings
[8:51] and the EBITDA were both negative and a negative multiple doesn't say anything useful about value
[8:58] GM did qualify and I checked his earnings debt and share price against its 10-K myself using GM's
[9:04] multiple using GM's multiples gives Tesla about $28 a share on the price earnings and about $25
[9:11] on EBITDA as well. So that's why we didn't go with Ford we went with GM.
[9:24] So with this my checks caught two mismatches first GM reports and adjusted profit number
[9:31] while Tesla was straight GAAP so I use Tesla's normalized EBITDA of about $11 billion to
[9:37] compare like with like second GM's numbers leave out its lending business.
[9:42] GM Financial while Tesla's are company-wide Tesla doesn't report a separate finance segment
[9:47] so I couldn't remove that difference because Tesla has everything in one big pile compared to GM.
[9:50] I documented that
[9:56] as an exception instead of hiding it and any other mismatch would still fail the
[9:59] check. So when we go to the final table, I don't with the final table I didn't
[10:08] average the methods together. Peers come in a bit higher than my DCF because GM
[10:12] is valued as a steady car business while my forecast has Tesla using up cash
[10:17] for the next few years. Either way every method lands between about $7 and $39.
[10:22] Each method gives me a number so the next so the so the next question so the next
[10:30] question just depends on the company as well and with that and with that that
[10:38] just shows if it passed or failed too. So how do we validate this as well? So when
[10:51] we go to value per share we have to ask our second question what high-risk test
[10:58] pass or failed first I checked the math I ran the class training case through the
[11:01] same DCF code and all 18 checks match including $27 and 50 cents per share
[11:06] then I tried to break it so when I moved over here it shows my answer my highest
[11:18] risk test pass if 2030 cash flows turns negative the terminal value would treat
[11:22] a loss as permanent my downside is only about one billion dollars in 2030 so
[11:27] that's a real risk so when I went basically when I force a negative the
[11:30] model stopped instead of giving a fake number so with that growth equal to
[11:34] WACC is an unbalanced balance sheet and zero shares all stopped it too as well so
[11:44] when I get go to my locked prediction markdown file so before I had any AI use
[11:53] or any AI help assistance I wrote my predictions and locked my growth
[12:00] prediction from 3% to 5% however when I go to part two its results after running
[12:06] it I got the direction right but it was about 16% so a huge change compared to
[12:12] what I said because most of my terminal because most of my value is terminal
[12:17] value which comes in later years and it changed my recommendation now about
[12:21] 15 to 17 dollars because $356 is not even close to 16% as well last I did a
[12:32] cold run from a fresh GitHub download and everything passed and with AI
[12:37] assistance I helped check everything help with the 10-K filings as you see as
[12:43] well and just check everything so like nothing failed and if there was a
[12:49] problem I went to check it double check myself so AI just assisted me and just
[12:53] helped me with brainstorming not just creating the whole thing for me so just
[12:58] working with AI is a big use and helpful friend that just got me through
[13:04] this and it assisted me in a lot of things such as creating creating like
[13:10] some tables however I came up with the ideas and stuff it just assisted me
[13:16] all right with that thank you
