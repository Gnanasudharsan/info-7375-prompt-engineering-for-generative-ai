# FACTCHECK — Seeded Faults pitch

Status: drafted by Claude Code 2026-10-10 from the submission's FRICTIONAL.md and evidence/ folder; read and signed off by Atharva C, 2026-10-13.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | B00 | Atharva is aiming for a data engineering job | PASS | Atharva's own statement (chat, 2026-10-09) | — |
| 2 | B00, B01, B04–B07, B09 | Everything about Seeded Faults itself (repo, script, dbt project, contract, eval log, README table) | EXEMPT | Future tense throughout; brief lists it under "Will exist" | — |
| 3 | B01 | "None of that exists yet … one small test I ran by hand" | PASS | evidence/2026-10-09-first-planted-fault/ | — |
| 4 | B02 | "AI-written tests make this worse" | EXEMPT | Spoken as "My guess is…", a hypothesis the project will measure | Reworded 2026-10-09 from a statement of fact |
| 5 | B03 | Great Expectations version 1.24; I wrote every check myself | PASS | output/versions.txt (great_expectations 1.24.0); Create an Expectation docs page, read 2026-10-09; no Data Assistant/onboarding code in the installed package | — |
| 6 | B03 | Planted fifty missing values; the check caught all fifty | PASS | output/ge_fault.txt: faulted file unexpected_count=50; output/dbt_faulted.txt: FAIL 50 | — |
| 7 | B03 | dbt did the same with tests written in YAML | PASS | output/dbt_clean.txt PASS=3; output/dbt_faulted.txt not_null FAIL 50; models/schema.yml | — |
| 8 | B03 | dbt-expectations adds test types you still write by hand | PASS | hub.getdbt.com/metaplane/dbt_expectations/latest (v0.10.10), README read 2026-10-09 | — |
| 9 | B03 | "Nothing told me what I'd missed" | PASS | No tool tried reported coverage or missed faults (FRICTIONAL.md 2026-10-09) | Scoped to the tools tried, not all tools |
| 10 | B06 | One public table of New York City taxi trips | PASS | NYC TLC yellow taxi trip records, January 2024, public download | — |
| 11 | B08 | Crime Rate Management System is on GitHub; Oracle; built solo; has its own testing script | PASS | github.com/Arc-211/DMDD_FinalProject is public (GitHub API, 2026-10-09) and contains testing.sql; solo per Atharva | — |
