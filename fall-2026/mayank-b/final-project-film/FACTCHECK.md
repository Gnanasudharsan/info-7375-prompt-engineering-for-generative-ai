# FACTCHECK — Source Check for Support AI (pitch film v3.1, 2026-10-25)

Verdicts: PASS (sourced or true as stated) · RAN (shown output from the slice, saved in `slice/evidence/`) · LABELLED (a plan, said with "will" and chipped "proposed design" on screen) · EXEMPT (definition, opinion or my own reasoning).

| # | Beat | Claim | Verdict | Source | Note |
|---|---|---|---|---|---|
| 1 | BIDEA, BWHO | I'm Mayank Bhadrasen, a master's student in Information Systems at Northeastern | PASS | my enrolment | v3.1 removed "solo project" and the target role |
| 2 | BWHO | Claude Code is my assistant; I decide what to build and what counts as correct | EXEMPT (my account of the split) | SOURCES.md "Who did what", FRICTIONAL.md | Mayank to confirm in his own words |
| 3 | BKID | a robot helper can sound sure and still be wrong | EXEMPT (plain-language framing) | B00 is the real example | |
| 4 | B00 | In 2024, Air Canada's chatbot told a grieving customer he could claim a bereavement fare after his trip; the policy required the request before | PASS | *Moffatt v. Air Canada*, BC Civil Resolution Tribunal (Feb 2024), as reported by CP/Yahoo and Tom's Guide | both on-screen quotes are labelled "paraphrased"; no award amount quoted (reports disagree) |
| 5 | B00 | the tribunal held the airline responsible for what its chatbot said | PASS | same | |
| 6 | B01 | a bot gives the same answer to everyone who asks, so one wrong rule becomes a wrong promise to all of them | EXEMPT (my reasoning) | | no count of customers or cost is claimed |
| 7 | B01 | today's safety net is usually someone reading transcripts later | EXEMPT (hedged: "usually") | B08 manual-review card | |
| 8 | B02–B04, B06, B10, B11 | everything Source Check will do | LABELLED | PROJECT-BRIEF.md | narration says "will" or describes the design; chip says "proposed design" |
| 9 | B05 | Python compares the claim field by field; after vs before is a mismatch; the answer is held and the reason quotes the policy line | RAN | `slice/evidence/demo_2026-10-25.txt` | the table is the checker's real comparison of the `air_canada_shape` case; the airline and policy BRV-2026-03 are fictional |
| 10 | B07 | the Air Canada case is held; within 90 days vs 90 days after is held; a matching answer passes; 21 of 21 tests pass | RAN | `slice/evidence/pytest_2026-10-25.txt` | |
| 11 | B07 | with the check broken on purpose, tests fail | RAN | `slice/evidence/mutation_2026-10-25.txt`: ignore before/after 6 failed, ignore dates 6 failed, allow extra fields 2 failed | |
| 12 | B07 | the claims are written by hand for now | PASS | `slice/data/cases.json` `_note` | |
| 13 | B08 | Intercom Fin is an AI agent trained on a company's policies and procedures; teams test changes in simulations before going live; it hands cases to people | PASS | fin.ai, read 2026-10-25 ("trained on your policies, rules, guidelines and operating procedures"; "testing suite to run simulations"; hands off to human teams) | the page's resolution-rate figures are vendor claims and are not used |
| 14 | B08 | Zendesk's AI agents answer from the help-center articles you connect and escalate to a human when they can't answer | PASS | Zendesk help center: [knowledge sources](https://support.zendesk.com/hc/en-us/articles/8357749301658-Connecting-knowledge-sources-to-power-generative-replies-in-AI-agents), [knowledge reply and escalation](https://support.zendesk.com/hc/en-us/articles/10448933203994-Customizing-the-Knowledge-reply-in-an-AI-agent-with-agentic-AI), read 2026-10-25 | upgraded from the v1 third-party source |
| 15 | B08 | not found on their public pages: a per-answer check against the current policy version before sending | PASS (my search result, not a claim about the products) | v1 research, 2026-10-14 | never stated as "they don't" |
| 16 | B09 | one command shows the Air Canada answer held, with the reason and the policy line; it works today | RAN | `python3 -m source_check.demo`, output in `slice/evidence/demo_2026-10-25.txt` | |
| 17 | B12 | (v3.1: the "why me" sentence was cut) the exists-today list still names my public n8n + Claude repos | PASS | github.com/Mayank-1024/AI-Marketing-Ad-Review, /Madison-Project | |
| 18 | BOUT | "check the answer before the customer sees it" | EXEMPT (tagline) | | |
