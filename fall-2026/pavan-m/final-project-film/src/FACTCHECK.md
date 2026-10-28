# FACTCHECK — cite-the-line-pitch

Every factual claim in the narration, checked before audio. Statements of plan ("will") are labelled EXEMPT: they are intentions, not facts, and the film voices them in future tense.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | I am Pavan Majji, a backend software engineer | PASS | Author's own statement | — |
| 2 | BIDEA | A common habit is to paste an error into a chatbot and ask how to fix it | PASS | Author's own observation from development work; phrased as a habit, not a statistic | Avoided any frequency claim |
| 3 | BDEFS | Definitions of root cause, source grounding, prompt contract | PASS | Standard usage; prompt contract and source grounding as taught in INFO7375 | — |
| 4 | B00 | Nothing in the project is built yet | PASS | State of the work as of the date of this sheet; see PROJECT-BRIEF.md "Exists today" | — |
| 5 | B01–B05 | The tool, test service, prompt contract, checker, and 3 runs per incident | EXEMPT | Plan in PROJECT-BRIEF.md; narrated in future tense | — |
| 6 | B04 | Claude Code can be run from a script | PASS | Claude Code headless mode docs (docs.claude.com/en/docs/claude-code/headless) | — |
| 7 | B06 | Datadog's Bits AI SRE proposes root causes | PASS | Datadog Bits AI SRE documentation, "Investigate issues" page (read by author) | — |
| 8 | B06 | It runs inside Datadog's paid platform | PASS | Datadog product pages; Bits AI SRE is a Datadog product feature | — |
| 9 | B06 | Its accuracy/performance is reported by Datadog | PASS | Datadog's product page markets its own results; no independent benchmark found by author | Narration does not repeat Datadog's figures |
| 10 | B06 | I can't re-check its accuracy myself | PASS | Author has no Datadog account or access to its test data | — |
| 11 | B07 | "It's not a competitor" | PASS | Positioning statement; the project claims no market or comparison results | — |
| 12 | B08 | The results numbers don't exist yet | PASS | No runs have happened; table drawn with "?" cells | — |
| 13 | B10 | It will only be tested on incidents I made | EXEMPT | Plan; states the boundary of what the evidence can support | — |
| 14 | B11–B14 | Never acts; first run; risk and plan B | EXEMPT | Plan in PROJECT-BRIEF.md | — |
| 15 | B15 | I already work with FastAPI, Postgres and Docker, from engineering experience and coursework | PASS | Author's own statement; courses: Network Structures & Cloud Computing, Object-Oriented Design, Software Quality, Web Design & User Experience | — |
| 16 | B15 | Fault injection, prompt contracts, and LLM evaluation are new to me | PASS | Author's own statement | — |
| 17 | B16 | What exists today is the plan and my notes | PASS | PROJECT-BRIEF.md "Exists today" list | — |

## Corrections made before the sheet was written

| Claim | Verdict | Fix |
|---|---|---|
| During brainstorming, Claude described log platforms such as Datadog as tools that search logs but do not reason about cause | CORRECTED | Datadog's docs show Bits AI SRE proposes root causes and can mark an investigation inconclusive. The value proposition was narrowed to "open, re-checkable test bench." Logged in FRICTIONAL.md. |
