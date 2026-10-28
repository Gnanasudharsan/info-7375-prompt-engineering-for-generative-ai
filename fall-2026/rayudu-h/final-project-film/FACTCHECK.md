# Fact check: Electricity Supplier Check (pitch film)

Status: checked by Claude (Claude Code), 2026-10-14, against the source files and pages named below. The narration was approved by Hemanth Rayudu on 2026-10-14. Hemanth has not yet signed off this fact check.

Verdicts:
- **PASS:** matches the source.
- **CORRECTED:** the brief was changed to match the source.
- **EXEMPT:** a statement about a plan, or the narrator's own first-hand account. There is no external source to check it against; it is labelled as such in the film.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | B02 | Residential customers on competitive supply paid $738.7 million more than basic service over the last decade | CORRECTED | AG 2026 competitive supply report (`03.30.2026_CES Report.pdf`), p. 2, Executive Summary: "paid $738.7 million more than if they stayed on basic service"; Table ES-1 "Ten-Year Total Net Loss", July 2015–June 2025 | Brief said "over $738.7 million"; "over" removed 2026-10-14 (narrator approved) |
| 2 | B02 | Suppliers charging 10–30% above basic service account for more than half of those losses | PASS | Same report, p. 4: "suppliers charging between 10 and 30 percent above the basic service rate account for 51.45 percent of customer losses" | — |
| 3 | B02 | On-screen caption: source, pages, download date 2026-10-14 | PASS | File in project folder; download date per narrator (filesystem time is a copy time) | — |
| 4 | B01 | Residential basic service rate: fixed $0.17185 per kWh; August $0.16074 per kWh | PASS | `meco_basic_service.pdf`, M.D.P.U. No. 1-26-H, "Total Billed Basic Service Rate", Residential (R-1, R-2); "Effective: August 1, 2026" | Added at the narrator's request 2026-10-14; printed on the constructed bill (narrator's choice); not in PROJECT-BRIEF.md |
| 5 | B01 | I was on a competitive supplier and overpaid compared to basic service | EXEMPT | Narrator's own account (brief §7). The bill shown is a labelled constructed drawing, not his bill | — |
| 6 | B06 | Energy Switch Massachusetts is the DPU's site for shopping for a new electric supplier | PASS | energyswitchma.gov, fetched 2026-10-14: page title "The Massachusetts Department Of Public Utilities' Shopping for Electric Supply website" | — |
| 7 | B06 | Energy Switch Massachusetts doesn't read your current bill or tell you what you've already paid extra | EXEMPT | Narrator's own review of the alternative (brief §2). The fetched page is JavaScript-rendered; only its title was readable, and it shows no bill-reading feature | Framed as what I looked at, not as an audit of the site |
| 8 | B06 | Some towns' energy coaches check whether you're on competitive supply; that needs a person and isn't instant | PASS | greennewton.org Newton Power Choice article, fetched 2026-10-14: "Reach out to energycoach@newtonma.gov if you need help determining whether you're on Newton Power Choice or competitive supply." Help is by email to a person | One town given as the example (brief Sources) |
| 9 | B09 | A test bill crossing August 1, 2026 | PASS | Tariff 1-26-H takes effect August 1, 2026, so a bill spanning that date crosses a rate change | — |
| 10 | B10 | On-screen date "Aug 1, 2026" as the rate-change line | PASS | Same tariff, "Effective: August 1, 2026" | — |
| 11 | B03, B04, B07, B08, B09, B10, B12 | Everything the tool will do or contain (repository, rate table, test bills, eval report, extraction, verifier, scope, first piece, risk fixes) | EXEMPT | Plans from PROJECT-BRIEF.md §1, §3–§6 and the "Will exist" list; always spoken with "will" and tagged PROPOSED or CONSTRUCTED where drawn | — |
| 12 | B05 | Target role: AI engineer for agentic systems, ideally at an energy company | EXEMPT | Narrator's stated goal (brief header) | — |
| 15 | B05 | The hiring manager opens the project's GitHub repository; its evaluation report will show, for every test bill, whether each number in Claude's explanation matches a calculator number; they can rerun the tests | EXEMPT | Plan, brief §3 (added 2026-10-14 at the narrator's request) | — |
| 16 | B07 | Claude Code builds it, and the agent will call Claude through Claude Code (headless), with no paid API calls | EXEMPT | Plan, brief Stack header (clarified 2026-10-14 at the narrator's request) | — |
| 13 | B11 | Prior experience: Python, backend and API work at TCS and Tech Mahindra; evaluation design from the Ask Boston project | EXEMPT | Narrator's own record (brief §7) | — |
| 14 | B00, B12 | Nothing is built yet; today nothing exists | PASS | Brief "Exists today: Nothing yet. This is a pitch." | — |
