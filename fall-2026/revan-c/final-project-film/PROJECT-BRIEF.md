# PROJECT-BRIEF — Remnix Agent

**Revan C · INFO 7375 · Final Project Pitch · 2026-10-14, resubmitted 2026-10-25**

**1. What is it?**
Remnix will be an agent that answers USD→Mexico remittance cost questions using Money Map's data, showing the math and the source behind every number, including stablecoin routes. When it is done, it will be a public GitHub repository holding a PostgreSQL database (tables `quotes`, `fx_rates` and `snapshots`, each row stamped with its source and time), a FastAPI endpoint (`POST /ask`), a Claude agent with two tools (`get_quotes` reads prices; `compute_cost` does the math in Python), a 20-question test set with known answers run by pytest, and a log of every wrong answer and how it was caught (`wrong_answers.md`). In plain words: when you send money home to Mexico, part of it disappears in fees and the exchange rate; Remnix will be a calculator that shows its work.

**2. Why would anyone care?**
Someone sending $500 to family in Mexico can already pick filters on Money Map and read a ranked price list. But a sender's question might come in plain words, like "why is Wise cheaper than my bank?" Remnix will answer that kind of question, write out the arithmetic, and name the price source and its timestamp. Alternatives I looked at (checked 2026-10-14): Wise's comparison page and Monito both compare providers, but neither includes stablecoin routes. The World Bank's Remittance Prices Worldwide covers US→Mexico, but it is collected once a quarter for fixed $200 and $500 amounts; the latest US→Mexico data was collected in August 2025, and its provider list has no stablecoin routes. What Remnix will do that they do not: give a sender stablecoin routes next to banks and transfer services, priced from Money Map's live data, with the math and source behind every number it gives.

**3. Who opens it, and what do they do?**
The main reader is a hiring manager or engineer at a fintech or crypto company; the target role is software engineer. Researchers and policymakers who study what it costs to send money abroad are a second audience; for now Remnix covers only the USD→Mexico corridor. In the first sixty seconds they will read the README, run one command that asks Remnix one question, and see an answer whose every number links to a database row and timestamp. Then they will open the evaluation log.

**4. What does it prove about me?**
Source grounding (every number traced to a row), agent tool calling (Claude chooses tools, Python does the math), evaluation (a fixed test set scored the same way each run), verification (a wrong-answer log), and a prompt contract (no number without a source). A reviewer could fairly conclude I can build a small, checked LLM tool on real financial data. The evidence will be the test set results and the wrong-answer log in the repository.

**5. What is in, what is out, what comes first?**
In: one corridor, USD→Mexico. Out: Remnix will not send money or tell anyone which provider to choose; it explains costs only. First: load Money Map's Mexico data (which I am allowed to use) into PostgreSQL and answer one question correctly with sources. Someone will know it ran because the answer prints its source rows and timestamp, and the total matches Money Map for the same snapshot.

**6. What could sink it?**
Money Map's prices are live (on 2026-10-14 the page said "updated 1 h ago"), so a "known answer" written today will be wrong tomorrow, and the test set will fail for the wrong reason. I will freeze a dated snapshot of the data for testing and compute each known answer from that snapshot.

**7. Why this project?**
A mix. I picked it because it builds on Money Map and points at the fintech work I want. I already know remittance cost modelling, frontend dashboard work and GitHub Pages deployment; the evidence is Money Map, which I built as a Software Engineer Co-op at the MIT Digital Currency Initiative and which is live at https://mit-dci.github.io/payments-dashboard/. New to me: RAG and source grounding, agent tool calling, evaluation test sets, PostgreSQL and FastAPI.

**Stack:** Python, PostgreSQL, Claude, FastAPI.

### Exists today
- Money Map, live at https://mit-dci.github.io/payments-dashboard/ (viewed 2026-10-14), comparing USD→Mexico options including a "stablecoin sandwich" route.
- This brief, the beat sheet and the pitch film.

### Will exist
- The PostgreSQL database of Mexico corridor data.
- The Remnix agent (Claude + tools) and its FastAPI service.
- One question answered correctly with sources.
- The 20-question test set with known answers.
- The wrong-answer log.
