# FACTCHECK — SponsorScout

Every claim spoken or shown, checked against a file. `A1/` = Assignment 1 repository
`the-reallocation-engine` at `a1d321f`. `SUB/` = `A1/course/2026fa/submissions/AkshitVerma-AV/`.
Checked by Claude Code on 2026-10-14. Akshit re-checks before submission.

Status: claims checked by Claude Code 2026-10-14; rows 8 and 25 supplied by Akshit Verma 2026-10-14; final film approved by Akshit Verma 2026-10-14: "Go ahead", in reply to Claude's "please watch it … if it looks right, tell me and I'll record your sign-off".

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | "SponsorScout. A final project pitch by Akshit Verma. I'll show what already ran, and what I will build." | PASS | Author of the submission; the narration says "a pitch **by**", so the voice never claims to be Akshit. The synthetic voice (Kokoro `am_michael`) is disclosed in README.md and SOURCES.md (Akshit's choice, 2026-10-14, to drop the spoken disclosure) | Was "Hi, I'm Akshit Verma … in a synthetic voice" |
| 1b | BIDEA | "The question isn't which companies to apply to. It's which ones to network with." | EXEMPT | Framing question, not a claim | — |
| 2 | B00 | "SponsorScout will be a Claude Code workflow that tells … apply, network, check by hand, or skip" | PASS | Proposed (tag `proposed`). The four buckets exist in the prototype: `SUB/runs/run-2/network-targets.md` | Was present tense; "will be" since 2026-10-14 |
| 3 | B01 | "it will be a repository, in Python and Claude Code on public data" | PASS | Proposed. Stack: `A1/scripts/contrib/2026fa/AkshitVerma-AV-preopt-data-network-targets/` (Python stdlib) + `scripts/score/role-scorer.mjs` | — |
| 4 | B02 | Three checks: sponsorship (H-1B records), funding (Form D), entry-level opening on the board today | PASS | `SUB/runs/run-2/network-targets.md` "Data used" line; `A1/.../network_targets.py` | — |
| 5 | B03 | The engine's scorer gives a sponsor with no open job a zero and skips it | PASS | `SUB/runs/engine-baseline/role-scores.md`: "Proven sponsor (ghost posting)", composite 0.000, Skip | — |
| 6 | B03 | "which I had Claude Code run on October third" | CORRECTED | `SUB/WORKED-RUN.md` §0 (2026-10-03); A1 FRICTIONAL records the AI ran commands | Was "which I ran" |
| 7 | B03 | "SponsorScout puts it on a networking list. So a student can stop applying where nothing is open, and keep the sponsors worth contacting" | CORRECTED | run-2: NETWORK 1 (Outset Medical), scorer 0, liveness closed, recent funding. The second sentence is a capability, not a user result | Was "A student stops applying…", which read as a reported outcome; no users exist |
| 8 | B04 | MyVisaJobs lists sponsors and past job counts; doesn't route a sponsor with nothing open to networking | PASS | Akshit looked at myvisajobs.com on 2026-10-07 (reported 2026-10-14). Consistent with Claude's homepage fetch on 2026-10-12 ("Explore H-1B Visa Sponsors", employer job counts; no networking route) | Narrowed 2026-10-14: no longer claims the site lacks current listings |
| 9 | B05 | "I'm targeting data analyst and data engineer roles" | PASS | `A1/course/.../SUBMISSION.md` (O*NET 15-2051.01, 15-1243.01) | — |
| 10 | B05 | "they'll run one offline command" | PASS | Proposed. The offline replay command exists: `SUB/WORKED-RUN.md` line 87/105 (`--snapshot … --as-of 2026-10-03`) | — |
| 11 | B06 | "On October third, the prototype fetched sixteen job boards" | PASS | `SUB/WORKED-RUN.md` line 7 ("fetched 16 human-confirmed ATS boards live"); snapshot `fetched_at 2026-10-03T22:10:42+00:00` | — |
| 12 | B06 | "sorted one hundred twenty-three sponsors: two to apply, one to network, one hundred seven to check by hand, thirteen to skip" | PASS | `SUB/runs/run-2/network-targets.md` executive summary: 123 → NETWORK 1 · APPLY-TAILOR 2 · MANUAL-CHECK 107 · SKIP 13 | "apply" abbreviates APPLY-TAILOR. Was "two apply…", heard as "to apply" by whisper (2026-10-14) |
| 13 | B06 | "The job seeker is fictional" | PASS | Persona Jack Spencer, `jack.spencer@example.com`, `A1/.../fixtures/persona-jack-spencer.json` | — |
| 14 | B07 | "Run one got one wrong: Zoox landed in apply on part-time, contract student-worker postings" | PASS | A1 FRICTIONAL 2026-10-03 ("Wrong [found by AI on first read of run-1]"); `SUB/WORKED-RUN.md` line 11, 79 | — |
| 15 | B07 | "Claude flagged it. I chose the fix, and a test pins it." | PASS | A1 FRICTIONAL: "[ME] decided: exclude contract / student-worker / part-time"; `test_contract_student_worker_posting_does_not_count_as_live` (`SUB/TEST-REPORT.md` line 287) | — |
| 16 | B07 | "All twenty-five tests passed again on October twelfth" | PASS | Re-run 2026-10-12 in this project's session: `Ran 25 tests … OK` (FRICTIONAL Entry 1) | — |
| 17 | B08 | "every number is labelled a record or my own input" | PASS | run-2 report: values tagged `[record]` / `[your-input]`; "[model-judgment] none in this report" | — |
| 18 | B08 | "an unconfirmed board never reaches the scorer, which would treat it as open" | PASS | A1 FRICTIONAL 2026-10-03: `role-scorer.mjs` defaults a missing liveness to 1.0; run-2: "`unresolved` … never reached the scorer" | — |
| 19 | B09 | "Claude Code stops at the human gates for my sign-off" | CORRECTED | Recipe gate table: G1 (entity match + board map) and G3 (outreach sign-off) are human; G2 (liveness) is automatic. `SUBMISSION.md`: "G1 and G3 were signed by me" | Was "at each gate", which overclaimed (G2 is automatic) |
| 20 | B09 | "Evaluation is still to come" | PASS | Proposed; no evaluation set exists | — |
| 21 | B10 | "never apply, email, or contact anyone … won't score résumé fit" | PASS | Scope decision (proposed). The prototype has no send path; fit is not scored ("Fit is **not** scored", run-2) | — |
| 22 | B11 | "Today sixteen of the hundred twenty-three companies have a confirmed board" | PASS | run-2: 16 boards; 123 candidates; 107 MANUAL-CHECK (123 − 16 = 107) | — |
| 23 | B12 | "many of the other hundred and seven may have no public board, and I don't know how many" | CORRECTED | 107 = `no-board-in-map` (run-2). Not evidence they lack a board | Was "many companies use job systems with no public interface" (unsupported) |
| 24 | B13 | "I also don't know if recent funding predicts hiring" | PASS | A1 FRICTIONAL: "'Recent funding → hiring' is my hypothesis (your-input), not a record" | — |
| 25 | B14 | "I picked it because I'm job hunting too, and I wanted a smarter strategy than a hundred-plus applications a day" | PASS | Akshit's own reason, given 2026-10-14 ("…rather than just doing 100-200 applications every day"); Claude tightened the wording at Akshit's request | — |
| 26 | B14 | "Claude Code wrote most of the prototype; I set its rules, like requiring recent funding, and signed its human gates" | CORRECTED | `SUBMISSION.md`: "Claude Code (Opus 5.5) wrote most code"; A1 FRICTIONAL: "[ME] rejected / changed: … I made recent funding a **requirement**"; G1, G3 signed | Was "I can already point to the prototype, its tests" (overclaim) |
| 27 | BOUT | "SponsorScout. A pitch by Akshit Verma." | PASS | Title and author | "Everything marked proposed is still to be built" removed at Akshit's request (2026-10-14); the corner tags still mark ran / proposed on every drawing, and BOPEN shows the legend |
| 28 | all | Corner tags: "constructed drawing" + ran/proposed | EXEMPT | Disclosure labels, not claims; each drawing is constructed by Claude in `scenes.py` | — |
| 29 | B02, B06, B07, B11 | On-screen numbers and labels: "16 boards fetched", "123 sponsors sorted", 2 · 1 · 107 · 13, "25 / 25 tests pass · Oct 12", "16 / 123", "H-1B records", "Form D", "job board" | PASS | Each label repeats a spoken claim checked above (rows 4, 11, 12, 16, 22). No number appears on screen that isn't spoken and sourced | — |
