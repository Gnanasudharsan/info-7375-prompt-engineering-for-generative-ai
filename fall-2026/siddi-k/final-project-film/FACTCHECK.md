# FACTCHECK — Sponsor Triage pitch film

Every claim spoken or shown. Verdicts: **PASS** (checked against the named source), **CORRECTED** (was wrong in a draft and fixed), **EXEMPT** (a plan or proposal, labelled SKETCH on screen and "will" in narration), **STUDENT** (about me; only I can confirm it).

Checked 2026-10-14 by the Claude Code session against files in `kommurisi/the-reallocation-engine` at commit `0e33800` (branch `contrib/2026fa-kommurisi-data-role-sponsor-match`). Paths below are relative to that repo unless they start with `evidence/`.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | I'm on an F-1 student visa, looking for data jobs. | STUDENT | My answer in the session, 2026-10-14 | confirmed by me |
| 2 | B00 | An agent that will check each posting three ways (data-role sponsorship, liveness, OPT time); a GitHub repo with agent, tests, evaluation, report. | EXEMPT | PROJECT-BRIEF.md §1 (plan) | labelled SKETCH |
| 3 | B01 | The 80 Days CSV is a table in the course repo built from public H-1B data. | PASS | `data/80-days-to-stay/README.md` (Day 08: mapped against DOL LCA Disclosure Data and the USCIS H-1B Employer Data Hub) | none |
| 4 | B01 | Databricks has 1,640 H-1B approvals in the CSV. | PASS | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv:7249`; `evidence/databricks-csv-line-7249.txt` | none |
| 5 | B01 | Its five top sponsored titles are software and solutions roles; none is a data role. | PASS | same line: Software Engineer, Senior Software Engineer, Solutions Architect, Specialist Solutions Architect, Senior Solutions Engineer | none |
| 6 | B02 | On October 3 my recipe gave the repo's page check a Klaviyo job id that does not exist. | PASS | `scripts/contrib/2026fa/kommurisi-data-role-sponsor-match/fixtures/worked-run/liveness.txt` (captured 2026-10-03T19:59:31Z, URL `.../klaviyo/jobs/1000000001`, role id `klaviyo-dead-job-CONSTRUCTED`) | "my recipe": Claude wrote it in my session (see #19) |
| 7 | B02 | The page check said active. | PASS | same file: `✅ active https://job-boards.greenhouse.io/klaviyo/jobs/1000000001` | none |
| 8 | B02 | Greenhouse's API said 404. | PASS | `.../fixtures/worked-run/greenhouse-api.json`: `"klaviyo/1000000001": {"status": 404}` | none |
| 9 | B02 | My recipe already lets the API win. | PASS | `evidence/worked-run-report-2026-10-03.md`: "gate factor 0 (greenhouse-api-404 — the page check DISAGREED; the API 404 wins)" | none |
| 10 | B03 | Readers: students like me; a hiring manager for data engineering roles. One offline command; every decision and number traced to file and line. | EXEMPT | PROJECT-BRIEF.md §3 (the recipe already runs offline with one command and writes `{value, source}`; the final project will keep that) | labelled SKETCH |
| 11 | B04 | Loop: take a posting, pick the missing check, call one tool, record with source; stop on empty queue or budget, not on model say-so. | EXEMPT | PROJECT-BRIEF.md §4–5 (plan) | labelled SKETCH |
| 12 | B05 | Tools fenced in code to the CSV and Greenhouse's API; never applies or messages; won't promise a specific job will be sponsored. | EXEMPT | PROJECT-BRIEF.md §5 (plan) | labelled SKETCH |
| 13 | B06 | Every Apply and Unresolved comes back to me; approve, refuse, or defer. | EXEMPT | PROJECT-BRIEF.md §5 (plan) | labelled SKETCH |
| 14 | B07 | About 40 hand-labelled public postings, some held back, at least five planted failures; Claude vs the recipe's patterns, keep the winner. | EXEMPT | PROJECT-BRIEF.md §4–5 (plan; "I don't know yet" stated aloud) | labelled SKETCH |
| 15 | B08 | The October run had seven postings, two of them made-up tests. | PASS | `evidence/worked-run-report-2026-10-03.md`: 7 roles; "Klaviyo — Data Analyst (CONSTRUCTED…)" and "Northwind Analytics … CONSTRUCTED" | none |
| 16 | B08 | The recipe's decisions: one Apply, two Consider, one Skip, three Unresolved. | PASS | same report: "Apply 1 · Consider 2 · Skip 1 · Unresolved 3" | on-screen tag says the loop itself is a SKETCH |
| 17 | B09 | More than half the sponsoring companies in the CSV list just one title. | CORRECTED | `evidence/csv-title-coverage-2026-10-14.txt`: 862 of 1,552 companies with approvals > 0 (55.5%) | The draft said "the CSV keeps only five titles per company". That was false: 42 sponsoring companies list 6–14. Rewritten 2026-10-14, before the narration was voiced. |
| 18 | B09 | In my run, two real postings came out Unresolved and two only Likely. | PASS | report: DraftKings (no-sponsorship-record) and Absci (ambiguous-company-match) Unresolved; Databricks and Toast tier "Likely" | none |
| 19 | B09 | The Labor Department's disclosure data lists the job title on every application. | PASS | DOL OFLC, LCA Record Layout FY2024 Q1, field `JOB_TITLE` (Form ETA-9035 §B item 1): https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Record_Layout_FY2024_Q1.pdf (read 2026-10-14) | "application" = labor condition application, not an approved petition (noted in PROJECT-BRIEF §6) |
| 20 | B10 | I've built Python data work and an NBA RAG app with a retrieval evaluation. | STUDENT | `github.com/kommurisi/Advances-in-Data-Science---Final-Portfolio-Project---NBA-Rag-App` (commits by kommurisi, 2025-12-14; README lists an evaluation script with Hit@K) | confirmed by me, 2026-10-14: "Yes, I built it" |
| 21 | B10 | Agent loops, permissions and held-out evaluation are new to me. | STUDENT | my answer "Mix", 2026-10-14 | confirmed by me |
| 22 | B11 | In the recipe, Claude wrote the code and I accepted it unchanged. | PASS | `course/2026fa/submissions/kommurisi/SOURCES.md` (recipe): "wrote all prototype code, tests and fixtures"; "I accepted the code, tests … without changes" | none |
| 23 | B11 | The recipe and its twelve passing tests exist today. | PASS | `evidence/recipe-tests-2026-10-14.txt` (12 pass, 0 fail, re-run 2026-10-14) | none |
| 24 | B11 | This time I'll write the contract and tests first and check the rows myself. | EXEMPT | PROJECT-BRIEF.md §7 (a commitment) | none |
| 25 | BOUT | Title "Sponsor Triage", my name, INFO 7375, October 2026. | EXEMPT | metadata | none |
