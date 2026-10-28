# PROJECT-BRIEF.md: Electricity Supplier Check

**Student:** Hemanth Rayudu · **Target role:** AI Engineer (agentic systems), ideally at energy companies · **Stack:** Python 3.11, pytest, Claude Code (it builds the code, and the agent calls Claude through Claude Code in headless mode); no paid API calls

**1. What is it?** I am building a tool that reads a Massachusetts electric bill and tells you exactly how much more, or less, you paid than your utility's basic service rate, with the math shown: a Python repository with the agent, a dated rate table citing its source tariffs, constructed test bills with known answers, and an evaluation report.

**2. Why would anyone care?** The Massachusetts Attorney General found that residential customers on competitive supply paid $738.7 million more than basic service over the last decade, and that suppliers charging 10% to 30% above basic service account for more than half of those losses: markups hard to spot on a bill. Mine will save a household the work of finding the right published rate, matching it to their billing period, and doing the math. Energy Switch Massachusetts (Department of Public Utilities) helps you shop for a supplier but does not read your bill or tell you what you already paid extra; town energy coaches check whether you are on competitive supply but need a person and are not instant. Mine is instant, with every number traced to the bill or a published tariff.

**3. Who opens it?** A Massachusetts household, or an energy coach or legal aid worker checking many families' bills, uploads a bill and within sixty seconds sees "on this bill, you paid $X more than basic service," the formula, and next steps. A hiring manager for AI engineering roles opens the project's GitHub repository: its evaluation report shows, for every test bill, whether each number in Claude's explanation matches a number the Python calculator produced, and they can rerun the tests.

**4. What does it prove about me?** Prompt contracts (an extraction schema checked in code), verification separate from generation, every number grounded in a dated rate table, a bounded agent loop with retries, held out evaluation, and data boundaries for sensitive documents. A reviewer could fairly conclude I can pull exact, auditable numbers from messy documents without the model inventing any. Evidence: tests, constructed bills with planted traps, and traces of rejected drafts.

**5. In, out, and first.** In: National Grid residential bills vs. basic service, prorating across rate changes, rate trends, plain English explanation, next steps. Out: never recommending a supplier or signing anyone up, contacting utilities or suppliers, or storing real bills. First: a rate table snapshot, a prorating calculator, and ten constructed bills in pytest, one crossing August 1, 2026; it ran when tests pass and the prorated amount matches my hand computed answer. For now it is a portfolio demo: whoever runs it needs Claude Code access.

**6. What could sink it?** A wrong dollar amount from the wrong rate period or load zone. So rate rows will store source and retrieval date, prorating will get its own tests, uncertain fields will return "can't verify," and reports will show the formula. I don't know yet whether bills print the load zone; I will check a real bill against the tariff and log it in FRICTIONAL.md.

**7. Why this project?** It happened to me: I overpaid on a competitive supplier and missed it. Already have: Python, backend, and API integration (TCS, Tech Mahindra); evaluation design (Ask Boston). New: retail electricity tariffs, reliable field extraction from bill images, and a verifier that rejects any number not computed by code. A mix of learning and showing off.

**Exists today**

- Nothing yet. This is a pitch.

**Will exist**

- Electricity Supplier Check itself: a Python repository with the agent that reads a bill and shows what you paid versus basic service, with the formula and next steps
- Dated National Grid residential rate table with sources
- Prorating calculator and comparison calculator
- Constructed test bills with hand computed answers
- Claude extraction step with a schema checked in code
- Consistency check and number verifier
- Plain English report with next steps
- Evaluation report
