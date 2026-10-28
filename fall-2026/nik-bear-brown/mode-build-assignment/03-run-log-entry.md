# RUN_LOG entry

## Executive summary

This is the log entry for the funded-research mode's first real run, in the format the engine's run log uses (it would be appended to the repository's `logs/RUN_LOG.md`). It says what was run, on what, what came out, and what is still open. **Result: the mode is a DRAFT with a completed sample run; six decisions remain a human's.**

## Entry

```markdown
## 2026-10-19, case-part-time-funded-research-lab v0.1.0 (sample run, not a gate clearance)
- Inputs: six Boston-area institutions (NIH spelling), topic "single cell", NIH fiscal year 2026, work start 2027-01-01, minimum 6 months left. No private data.
- Engine commands run on a clean clone (commit 015843d): npm run verify (158 files conform, 3 manifest warnings); npm run doctor; npm run ats:scan -- --dry-run (4 boards, 937 postings, 7 kept); npm run ats:liveness (live posting active; made-up closed posting uncertain, not expired); npm run bls:local-wage (could not run: .venv and data/bls/local-wage/ absent from main).
- New script run: python3 scripts/funding/check-awards.py (17 unit tests pass; live run: 349 awards, 223 research-project awards running 6+ months past the start; NIH counts cross-checked against a second query, all six equal).
- Outputs: runs/awards-2026-10-19.json (agent log), runs/awards-2026-10-19.md (human report). Award numbers redacted; no investigator names in either.
- Deliberate break attempts: typo in an organisation name (caught by the control query); partial name HARVARD (matched 3 organisations, now reported); start date 2031 (ended awards removed); private-file path outside private/ (refused); dead proxy (stopped, no empty result written).
- Broke and fixed: control query paged through every award (hang); NSF capped silently at 25 a page; NSF loose awardee match inflated the headline (588 vs 350); investigator file empty (wrong API key); recipe wrongly said the database needs exact names.
- Gates: G5 human look not cleared. Nothing was posted, drafted or sent.
- Open issues: 6 typed TODOs in the recipe (NSF organisation-name mapping; local-wage input data missing on main; liveness cannot report expired; min-months-left; activity-code lists; report columns). Status stays DRAFT. The engine's doctor sees 324 declared and 324 body TODOs (318 before this recipe).
```
