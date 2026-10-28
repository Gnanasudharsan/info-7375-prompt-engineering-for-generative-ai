# FACTCHECK — bitecheck-pitch (v2, 2026-10-21)

Beat numbers refer to the v2 film. v1 rows were re-mapped: v1 B00→B02, B01→B03, B02/B03→B04, B04→B05, B05→B06, B06→B07, B07→B08, B08→B05, and B09–B13 unchanged.

Status: every row was checked by Claude Code on 2026-10-12 and updated 2026-10-13 against the evidence named. Rows 4, 23 and 24 depended on facts only Omkar could confirm; he confirmed them in chat on 2026-10-13.

Evidence: `evidence/los_smoke_test.txt` (a live run of the local InstaLoan backend, 2026-10-12 11:48 EDT, synthetic applicant). The rule values were read from `LOS/backend/src/constants.ts` (`MIN_MONTHLY_INCOME: 15000`, `STAGE_PRECONDITION`). Tool descriptions come from the vendors' docs and reviews read on 2026-10-12 (URLs in SOURCES.md). Stryker figures come from `evidence/stryker/` (StrykerJS 8.7.1, run 2026-10-13). Pronunciation was checked with Whisper-tiny (`evidence/pronunciation_check.txt`).

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | B02 (v1 only) | Claude can draft a whole suite of API tests that all come back green | EXEMPT | Framing: a possibility, not a measured result. No number is claimed. | Not in v2; B02 now says "Claude can write hundreds of them, and they can all pass" (row 29) |
| 1b | B02 (v1 only) | BiteCheck tells an engineer reviewing AI-written tests which ones would catch a broken business rule | PASS (future) | Design goal, PROJECT-BRIEF §2; tagged PROPOSED | Not in v2 narration; the same idea is in brief §2 |
| 2 | B02 (v1 only) | A green test only means something if it would turn red when the code is wrong | PASS | Definition of mutation testing (StrykerJS docs) | Not in v2 narration; B01–B02 make the point through the analogy |
| 3 | B03 | BiteCheck *will be* a public repo with a prompt, a bug list, a runner and a report | PASS (future) | PROJECT-BRIEF §1, "Will exist" list; tagged PROPOSED on screen | — |
| 4 | B04 | A loan application API "I built earlier with Claude's help" | PASS | `~/Desktop/LOS` exists. Omkar confirmed in chat on 2026-10-13: "Yes" (built with Claude's help). | — |
| 5 | B04 | It uses made-up applicants and mock vendors | PASS | LOS README ("mock adapters"); smoke test used a synthetic applicant | — |
| 6 | B04 | It checks a minimum income and the order of steps | PASS | `constants.ts` RULES.MIN_MONTHLY_INCOME = 15000; STAGE_PRECONDITION map | — |
| 7 | B04 | On 2026-10-12, income ₹14,999 was rejected | PASS | `los_smoke_test.txt`: REJECTED, "Monthly income below minimum ₹15000" | — |
| 7a | B04 | "On October twelfth, I ran it on made-up applicants with Claude Code" | PASS | Claude Code ran the smoke test during the build Omkar asked for (`evidence/los_smoke_test.txt`). | Was "I ran it", which wrongly suggested Omkar ran it himself, so "with Claude Code" was added on 2026-10-14 |
| 8 | B04 | ₹15,000 got an offer | PASS | `los_smoke_test.txt`: status OFFER_GENERATED | — |
| 9 | B04 | Paying out before the earlier steps was refused (409) | PASS | `los_smoke_test.txt`: HTTP 409, "expected 'ESIGN_COMPLETED'" | — |
| 10 | B04 (v1 only) | It has no tests yet | PASS | `find LOS -name '*.test.*' -o -name '*.spec.*'` (excluding node_modules) returned nothing on 2026-10-12 | **Not in v2, and no longer true.** Claude Code added 4 tests on 2026-10-21 (row 33) |
| 11 | B05 | Example mutant: minimum income 15,000 → 1,500 | PASS (future) | Hypothetical example; tagged PROPOSED. No mutant exists yet. | — |
| 12 | B06 | A test failing on correct code means Claude got it wrong; these go into a log | PASS (future) | Design statement, PROJECT-BRIEF §4 | — |
| 13 | B07 | From their docs, Postbot generates test scripts | PASS | Postman Postbot page and reviews (read 2026-10-12) | — |
| 14 | B07 | Schemathesis checks an API against its schema | PASS | Schemathesis docs (read 2026-10-12) | — |
| 15 | B07 | On Oct 13, I ran Stryker on my loan rules with Claude Code | PASS | `evidence/stryker/stryker_run.log`, `stryker_summary.txt`. Claude Code ran it on a scratch copy at Omkar's request. Omkar can re-run it with the command in BUILD-PROMPT §4. | Was "I ran Stryker myself", which was untrue, so it was changed |
| 16 | B07 | It made 92 mutants (on-screen hero "92") | PASS | `stryker_summary.txt`: TOTAL mutants: 92 (bre.ts 90, constants.ts 2) | — |
| 17 | B07 | None changed the 15,000 limit (on screen "15,000 changed: 0") | PASS | `stryker_summary.txt`: numeric-literal mutants 0; no mutant on constants.ts L46 `MIN_MONTHLY_INCOME: 15000` | — |
| 17b | B07 (v1 only) | Its one step-order mutant deletes every guard at once | PASS | `stryker_summary.txt`: the only mutant on STAGE_PRECONDITION is ObjectLiteral → `{}` (constants.ts L33). routes.ts was not in the mutate set, so this is scoped to the rules files. | Not in v2 narration; still true, see stryker_summary.txt |
| 17c | B07 | BiteCheck adds those business-rule bugs, one at a time | PASS (future) | PROJECT-BRIEF §2/§5; tagged on screen | — |
| 18 | B08 | The first-minute flow (one command, one page) | PASS (future) | Design; tagged PROPOSED; `npm run bitecheck` does not exist yet | — |
| 19 | B05, B09 | Prompt contract, source grounding, bounded agent loop, evaluation | PASS (future) | PROJECT-BRIEF §4; course topics | — |
| 20 | B09 | "It won't prove this works on every API" | PASS | Scope limit, PROJECT-BRIEF §4–5 | — |
| 21 | B10 | Out: not a general tool, never fixes app code. First: the income rule in GitHub Actions | PASS (future) | PROJECT-BRIEF §5 | — |
| 22 | B11 | Risk: I write the bugs. Mitigation: commit the bug list first, report survivors | PASS (future) | PROJECT-BRIEF §6 | — |
| 23 | B12 | I've done API testing and CI gates at my last job; that work is private | PASS | Checked against Omkar's résumé (private; not in this folder): automated Postman API test collections and GitHub Actions CI with staged quality gates. Omkar confirmed on 2026-10-13: "i have already worked on api testing". | — |
| 23b | B12 | My public Reallocation Engine pull request, a Claude workflow with a run log | PASS | nikbearbrown/the-reallocation-engine#37 (opened 2026-10-03; includes `logs/runs/2026fa-o7580-1.md`) | — |
| 24 | B12 | Mutation testing and evaluation design are new to me | PASS | Omkar confirmed in chat on 2026-10-13: "Yes". | — |
| 25 | B13 (v1 only) | Exists: the loan API (ran), the brief, the film. Everything else will exist. | PASS | PROJECT-BRIEF "Exists today" / "Will exist" | Superseded by row 33 and the v2 B13 wording |

## New claims in v2 (checked by Claude Code, 2026-10-21)

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 26 | B00 | "I'm Omkar Salian, a software engineering master's student at Northeastern" | PASS | Omkar's résumé (private): MS Computer Software Engineering, Northeastern University, Dec 2026 | — |
| 27 | B00 | "I'm building it myself, with Claude Code as my coding assistant" | PASS | The project is solo; Claude's role is listed in SOURCES.md | — |
| 28 | B01 | Smoke-alarm comparison | EXEMPT | Analogy, tagged ANALOGY · constructed drawing; no factual claim | — |
| 29 | B02 | "Claude can write hundreds of tests, and they can all pass" | EXEMPT | Framing, a possibility rather than a measured result; tagged ANALOGY | — |
| 30 | B05 | Mutant = a copy of the code with one rule broken; example 15,000 → 1,500 | PASS (future) | PROJECT-BRIEF "How it works"; tagged PROPOSED | — |
| 31 | B05 | "Claude Code writes the tests in TypeScript" | PASS (future) | The 2026-10-21 scaffold uses TypeScript with Node's test runner (`LOS/backend/test/income-rule.test.ts`) | Was "Jest + Supertest" in v1's brief; changed to match the code |
| 32 | B06 | Run on the real API (all pass) and each mutant (one fails); survivors are gaps; failures on correct code go into a log | PASS (future) | PROJECT-BRIEF "How it works"; tagged PROPOSED | — |
| 33 | B13 (v2 first cut) | "On October twenty first, Claude Code also wrote the first income rule tests and one mutant, checked locally" | PASS | `LOS/backend/test/income-rule.test.ts` (4 tests), `test/mutants/BROKEN-income-rule.ts` (`<`→`<=`), `test/mutants/ci-run-2026-10-21.txt`. That folder's README says "written by Claude, the coding agent" and "Not run on real GitHub Actions". | — |
| 34 | B10 | "On October twenty second, GitHub Actions ran the income rule tests. They passed on the real rule, and caught both planted bugs" | PASS | Run 39843450055 on O7580/instaloan-los (private), commit 1a9df4c: conclusion success; test:mutants "2 killed · 0 survived" (`evidence/ci/github-actions-run-2026-10-22.txt`) | v1 said "will"; now REAL |
| 35 | B10, B13 | "the one I chose" / "I chose a second bug" | PASS | Omkar chose 15,000 → 1,500 and wrote its comment in chat on 2026-10-22; Claude typed it in (FRICTIONAL.md 2026-10-22) | Says "chose", not "wrote", because Claude typed it |
| 36 | B13 | "Claude Code wrote the first income rule tests" | PASS | Row 33 | — |
| 37 | B10, B13 | Scope: these are unit tests of the income-rule function | PASS | `test/income-rule.test.ts` imports `incomeRuleRejection` directly; it does not call the API. "API tests" stay in "will exist" in B13. | Narration says "income rule tests", not "API tests" |
