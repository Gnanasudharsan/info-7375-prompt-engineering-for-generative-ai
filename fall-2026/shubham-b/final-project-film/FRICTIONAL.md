# FRICTIONAL — Marino Desk Assistant pitch film

Dated entries, written on 2026-10-13 and later re-drafted it on 2026-10-21. I worked with Claude Code (Opus 5.5) throughout — drafted it in rough words and improvised it using claude, but every decision below is mine.

**~13:30 — Started.** Pasted the assignment in, had Claude plan and build in a new `Final Project Pitch Film/` folder. Re-cloned the Brutalist toolkit at `519fcbb` since my Week 1 checkout was gone.

**~13:38 — Setup issue.** `./setup --install` failed on a false-positive "ElevenLabs reference found" (it was the toolkit's own example reels, not mine). Had Claude run the readiness checks by hand instead — all passed.

**~13:40–14:45 — First attempt was the wrong project.** Went along with pitching my Reallocation Engine recipe (swe-opt-clock, PR #49) at first. It built and passed every gate, but three reviews (a grader agent, a five-advisor "LLM council," and its peers) kept landing on the same problem: the code was Claude's, so the pitch proved nothing about me. Carried forward from this: never present Claude-written code as my own evidence, say "written with Claude" out loud, use "will" for anything unbuilt, and label who ran each check.

**~15:05 — Rejected the first pitch.** Told Claude the career-ops and Reallocation Engine projects weren't mine, and the assignment wants work that shows I can do the job I want. Had Claude archive that version (`_archive/`, not submitted) and start over from my own repos and project bank.

**~15:10 — Chose again.** Two real candidates came up: EventFlow Engine (`robust-data-processor`), mine, no AI involved; and marino-rag, a Q&A assistant I'd started for the Marino front desk. marino-rag had two problems — it read SharePoint training docs (restricted data under the assignment's rules) and called OpenRouter instead of Claude. Decided to pitch marino-rag rescoped to the public site only, answers moved to Claude, target role new-grad full-stack SWE, and to disclose the Kokoro narration. Told Claude the honest authorship: EventFlow is mine; marino-rag's code is mostly AI-generated under my direction.

**~15:17 — Checked the facts before writing anything.** Re-ran marino-rag's tests (60 passed, `dd3205e`), confirmed the SharePoint exports were gitignored and never committed, ran the site's own search ("guest pass" → 5 pages, Home first), and pulled the Alumni page through marino-rag's own parser (782 words, five annual prices for one membership, $480 down to $120 depending on join date). That last check changed the risk I decided to pitch: the stale 2023–24 prices hidden in the HTML are already dropped by the parser, so the real risk is that the price table is date-dependent at all, not that old prices leak through. All of this is in `evidence/`.

**~15:21–15:30 — Script and look.** First script draft fit the 4:00 cap with no cuts needed (627 words, 234.5 s). Whisper caught a mispronunciation ("EventFlow" heard as "a vent flow"), fixed and re-voiced. Reviewed contact sheets before the 4K render and had Claude fix seven layout issues and one safe-area overflow first.

**15:30–15:43 — First 4K build.** Passed every `art run` gate, but `art final` was blocked by Gate T on three beats — decorative ink squiggles were being misread as overlapping text. Fixed by drawing them in grey; first master ran 234.8 s, sha256 `be93a1dd…`. I looked at every beat's frames in the master myself.

**~15:50 — Fresh-context review.** Confirmed my facts (tests, prices, search results, sha256), then flagged real problems: two beats still spoke planned behavior in the present tense, my portfolio site was cited despite being mostly Claude's commits, the PRD's "Suhas" author name wasn't explained, one beat overclaimed given marino-rag's AI-generated code, and a couple of tags/labels didn't match their pictures.

**~18:05 — Fixed what the review found.** Confirmed I work as a Facility Assistant at Marino and go by "Suhas" there (hence the PRD name). Dropped the portfolio site as evidence and rested existing-skill proof on EventFlow alone. Re-voiced the overclaiming beats to "will," relabeled the mismatched tags, and rebuilt. New master: 237.4 s, sha256 `ea18ed8b…`.

**2026-10-14 — My own pre-submission review.** Watched the full film with sound and was satisfied. Re-opened all four `evidence/` files myself and confirmed they matched the film and brief. Made one docs-only fix (clarified "Marino" means Northeastern's campus gym, for a hiring-manager reader who might not know) and corrected some out-of-order timestamps in this log. Left two things unresolved on purpose: `bookend_check.py`'s one documented failure, and a skipped duration sub-check the toolkit doesn't support at this commit (see `gate-reports/GATES.md`).

**2026-10-21 - What I did after the grading of previous submission:**
- **This file.** Drafted this file in my own words by using reference of original submission and claude memory logs and then further improvised the typing, grammar, spelling using claude.
- **The repo.** Had Claude rebuild marino-rag's index from the public site only (60 pages, `recreation.northeastern.edu`, 2026-10-21), wrote 50 real front-desk questions myself, and had Claude build a retrieval-check script confirming the right page shows up in the top 3 for 48/50 (96%) of them — both misses explained in `eval/report.md`, not hidden. Updated the repo's README and PRD so SharePoint ingestion is marked permanently out of scope instead of just deferred, and committed and pushed all of it. This is exactly the "First" milestone my own `PROJECT-BRIEF.md` already promised.
- **What I didn't change:** the film, `PROJECT-BRIEF.md` and `beat_sheet.json` still say the public-only index and eval report "will exist," because that's what the narration says and I'm not re-recording it. The repo now backs that promise up, a week later than the film claims — I'm not pretending it was already true on 2026-10-13.
