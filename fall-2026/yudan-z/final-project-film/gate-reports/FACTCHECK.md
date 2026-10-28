# FACTCHECK — is-funded-sponsor-triage-pitch

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | Narrator is Yudan Zhou, an IS master's student; the voice is synthetic | EXEMPT | Self-description; voice = Kokoro `af_heart` | — |
| 2 | BDEFS | A blank record = the dataset matched no filing, not a refusal | CORRECTED | CSV: 28,812 blank vs 5 explicit-zero `Total Approvals` | Was "nobody has a filing on file" (asserted no filing exists) |
| 3 | B01 | Tool sorts postings into apply/consider/skip from public funding + sponsorship records; says "no record" instead of no | PASS | the-reallocation-engine `scripts/contrib/2026fa/yudanzhou-is-funded-sponsor-triage/triage.py` (statuses, NEXT_ACTION) | — |
| 4 | B02 | 27,874 funded · 1,532 with any H-1B approval · 131 of those funded in last 24 months | PASS | `course/2026fa/submissions/yudanzhou/runs/triage/triage-report.md`, run 2026-10-02 | Date shown on screen |
| 5 | B03 | 28,812 blank approval rows; 5 explicit zeros | PASS | `course/2026fa/submissions/yudanzhou/CHANGE-BRIEF.md` §2 (count over the shipped CSV) | — |
| 6 | B04 | 2026-10-13: h1bdata.info "Moloco" returned a long table of filings; "123 See" returned no table, no count, no "not found" message | PASS | `evidence/2026-10-13_h1bdata_*.png` (student's own screenshots) | Removed "204 records" and "median salary": not visible in the screenshots |
| 7 | B05 | Blank → kept out of ranking, moved to networking list with a question | PASS | `triage.py`: status `no-h1b-record` → held out; NEXT_ACTION "Networking list…" | — |
| 8 | B06 | One command; every scored number tagged record / your-input | PASS | contrib `README.md`; `roles.json` sources | — |
| 9 | B07 | Eleven tests exist; one checks the tags | PASS | `test_triage.py` (11 tests; `test_every_scored_value_is_labeled`) | — |
| 10 | B07 | 2026-10-12 TA review: "you never turn a blank into a no" | PASS | TA feedback text received 2026-10-12 (quoted verbatim, partial) | — |
| 11 | B08 | Exists today: recipe, Python prototype, eleven tests | PASS | PR nikbearbrown/the-reallocation-engine#13, commit 5ae7747 | — |
| 12 | B08 | Still to come: corrected status, written reasons, sensitivity check, test set, failure analysis | EXEMPT | Future work ("will"), PROJECT-BRIEF.md | — |
| 13 | B09 | Only explicit-zero companies (five) get a negative | PASS | `triage.py` `sponsorship_for`: approvals == 0 → tier None | — |
| 14 | B10 | A company with 564 approvals scored zero because of one hand-entered demo value | PASS | `runs/triage/role-scores.md` (TREDENCE INC, liveness 0 [your-input], Skip 0.000) | "I typed" → "hand-entered demo value" (fixture written by AI) |
| 15 | B10 | The pitch's first draft had four statements that did not match the files; an AI review caught them | PASS | PROJECT-BRIEF.md §6; review 2026-10-13 | — |
| 16 | B11 | The code was written with an AI assistant under the student's direction | PASS | `course/2026fa/submissions/yudanzhou/SOURCES.md` (previous assignment) | — |
