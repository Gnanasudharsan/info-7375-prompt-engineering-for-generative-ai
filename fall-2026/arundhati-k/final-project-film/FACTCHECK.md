# FACTCHECK — Co-op Sponsor Check (pitch film)

Status: checked 2026-10-12, updated 2026-10-25 by Claude against the files named below; Arundhati Kandelkar to confirm on review.
Rule: past tense only for what exists and is shown in evidence; everything else is "will". Every frame audited, bookends included.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 3 | B00 | Pushed a recipe to my fork on October third; tag "commit 03784b0" | PASS | `git log -1 03784b0` → Sat Oct 3 16:55 2026, branch `contrib/2026fa-arundhatik26-coop-sponsor-swe-15-1252` | — |
| 4 | B01 | It checks three things: software-title record, co-op before graduation, posting live | PASS | CHANGE-BRIEF gates G2–G4; run output shows `matched`/`liveness=`/`DEPENDS ON GRADUATION DATE` (evidence/recipe-rerun-2026-10-10.txt) | — |
| 5 | B02 | A missing company is not treated as zero; it says unknown and tells you to ask a person | PASS | `test_F1_not_in_dataset_is_unknown_not_zero`; jpmc row → "NETWORK: … ask an alum or recruiter directly" | worded "does not treat that as zero", not "never prints zero" |
| 6 | B03 | JPMorgan Chase, Goldman Sachs, Morgan Stanley not in the dataset | PASS | CHANGE-BRIEF F1: searched 2026-10-02, none found; jpmc → `not-in-dataset` in re-run | — |
| 7 | B03 | Dataset built from a list of funded startups taken from SEC filings | PASS | `data/80-days-to-stay/README.md`: "mapped our SEC startup list against … DOL LCA … USCIS H-1B Employer Data Hub" | spoken as "would explain", not as a proven cause |
| 10 | B06 | A second public data source | EXEMPT | proposal, spoken as "will exist"; tag PLANNED on screen | — |
| 13 | B09 | Will not give immigration advice; every answer labelled record / judgment / your input | PASS | labels exist today: `test_every_scorer_term_is_labeled`; scope statement is a plan (PLANNED tag) | — |
| 14 | B10 | Reader runs one command, sees unknown rows and a right/wrong table | EXEMPT | proposal; drawing tagged "CONSTRUCTED · not built yet"; ticks/crosses illustrative, no counts | — |
| 17 | BOUT | Title and my name; no instructor handle | PASS | ClaudeTitleOutro `handle` = "Arundhati Kandelkar" (local toolkit edit, BUILD-LOG.md) | — |
| 18 | B05 | USCIS H-1B Employer Data Hub, searched October twelfth, lists JPMorgan Chase | PASS | evidence/uscis-hub-search-2026-10-12.md: FY2026 name list shows "JPMORGAN CHASE AND CO" | search run by Claude in its browser on my instruction; SOURCES.md says so |
| 19 | B05 | Searched one employer at a time, by name, place or industry, not by job title | PASS | same file: filters are Fiscal Year, Employer Name, NAICS, City, State, Zip — no job-title filter | the hub's CSV download is acknowledged in PROJECT-BRIEF §2 |
| 20 | B05A | "Mellon" returned four employers: three BNY companies and Carnegie Mellon University | PASS | same file, FY2026 list for `MELLON` | names shown in title case for legibility; the hub lists them in capitals |
| 21 | B05A | My tool already has a test that refuses a match on part of a name | PASS | `test_substring_does_not_match` ("MELLON", "ACME"), TEST-REPORT §4 | — |
| 22 | B05A | My tool will check a whole list for software titles and co-op dates | PASS | list input + title match + timeline exist today (rows 4, 9); "will" covers the hub-backed version | — |
| 23 | B11 | I'm an international student; this is the question I face choosing a co-op | PASS | my own statement, chosen 2026-10-12 from options Claude offered (SOURCES.md) | — |
| 24 | B11A | I already build Java and Spring Boot services; three years as a software developer at G+D; this project doesn't show that | PASS | my résumé (not committed — private): Software Developer, Giesecke+Devrient, Pune, Aug 2021–Sep 2024 (updated résumé, 2026-10-12; an earlier copy said Sep 2022), Java 8 / Spring Boot / REST; "three years" = 37 months | narration says "G plus D" (Kokoro misread the full name); only Java + Spring Boot claimed, since that is what the role shows |
| 25 | B11A | New for me: joining a second public data source into a small Python tool | PASS | my own statement; matches "Will exist" in PROJECT-BRIEF | — |
| 30 | B09P | Every answer is labelled as a record, a judgment, or your input | PASS | `test_every_scorer_term_is_labeled` passes (evidence/recipe-rerun-2026-10-10.txt); labels `record` / `model-judgment` / `your-input` in run-log.json | — |
| 32 | B09P | Every sponsor record in the run log cites its CSV line | PASS | runs/sample/run-log.json in the fork at 03784b0: 48 `csv_line` fields, one per record-sourced value (checked 2026-10-12) | — |
| 8 | B04 | Eighteen tests pass today, incl. a new test for a bug the evaluation found | PASS | fork branch `final/arundhatik26-and-fix` @ `379252f`: "Ran 18 tests … OK"; new test failed before the fix | — |
| 11 | B07 | Tested on 25 companies; every company looked up in the official hub was there; tool found a record for 2 | PASS | evidence/eval-25-rows-2026-10-25.md: 24/24 searched by Claude found; Capital One is my own search; 2 matched (Stripe, Chime) | worded "every company I looked up", not "all 25", until my Capital One search is recorded |
| 26 | B07 | It never guessed no | PASS | 23/23 unmatched rows are `not-in-dataset` / `no-sponsorship-record` → "unknown"; no zero | — |
| 27 | B07A | Matcher turned "Goldman Sachs and Co LLC" into "Goldman Sachs and"; fixed, test failed before and passes after | PASS | commit `379252f` on `final/arundhatik26-and-fix`; before: 1 failure of 18; after: 18 OK | — |
| 33 | B07B | Typing Robinhood found nothing, but my data holds Robinhood Markets with 824 approvals; Chime and SoFi failed the same way | PASS | eval-rows-dataset-2026-10-25.json (Robinhood not-in-dataset); CSV line 22735 ROBINHOOD MARKETS INC, Total Approvals 824; Chime → CHIME INC (2) not CHIME FINANCIAL INC line 5469 (580); SoFi → not-in-dataset, SOCIAL FINANCE INC line 24681 (182) | narration "So Fi" for pronunciation |
| 12 | B08 | Names are the risk, and the test proved it; the tool will show likely legal names to a person | PASS | eval-25-rows: 2 name defects; showing candidates is a plan (PLANNED tag); gate G2 exists | — |
| 31 | B09P | Twenty-five answers were checked against the official hub | PASS | evidence/eval-25-rows-2026-10-25.md (24 by Claude on my instruction, Capital One by me) | — |
| 1 | BNAME | "I'm Arundhati Kandelkar, a master's student at Northeastern"; on screen: name + "MSIS, Northeastern University" | PASS | my name and programme; synthetic voice Kokoro `bf_emma`, disclosed in README.md and SOURCES.md | — |
| 34 | BBUILD | "I'm building Co-op Sponsor Check: a tool that tells international students whether a company has ever sponsored someone for a software job" | PASS | the project as it exists (recipe `03784b0`, fix `379252f`) and as planned (PROJECT-BRIEF §1); "building" = in progress | on-screen text matches the spoken sentence |
| 35 | BIDEA | A missing record looks like a no today; my tool says "I don't know" instead of guessing no | PASS | `test_F1_not_in_dataset_is_unknown_not_zero`; 23/23 unmatched rows reported unknown (eval-25-rows) | "looks like a no" is my framing of the problem, not a measured claim |
| 1 | BNAME | "I'm Arundhati Kandelkar, a master's student at Northeastern"; on screen: name + "MSIS, Northeastern University" | PASS | my name and programme; synthetic voice Kokoro `bf_emma`, disclosed in README.md and SOURCES.md | — |
| 34 | BBUILD | "I'm building Co-op Sponsor Check: a tool that tells international students whether a company has ever sponsored someone for a software job" | PASS | the project as it exists (recipe `03784b0`, fix `379252f`) and as planned (PROJECT-BRIEF §1) | on-screen text matches the spoken sentence |
| 35 | BIDEA | A missing record looks like a no today; my tool says "I don't know" instead of guessing no | PASS | `test_F1_not_in_dataset_is_unknown_not_zero`; 23/23 unmatched rows reported unknown (eval-25-rows) | "looks like a no" is my framing of the problem |
| 29 | BWHAT | When done: a public GitHub repository — the tool, a 25-company evaluation set, a failure log | EXEMPT | "will be"; tag "PLANNED · finished form" | — |

