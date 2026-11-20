# FRICTIONAL — Job-Search Agent 3

## 2026-11-19 ~11:05–11:20 ET — Started the JS3 folder twice
I copied the JS2 code into js3-filter-tool-score at 9ef84715 (baseline: evidence/js2_baseline_in_js3_2026-11-19T1604Z.txt), then ran the copy again from a fresh chat. The second copy (e4b5939e) re-copied identical files; its only real additions were GATE.md and empty FILTER/FRICTIONAL/SOURCES files. Its message calls it the "starting point"; the real starting point is 9ef84715. Corrected here, not rewritten.
Checked: git log, the file contents, and git ls-files before continuing.

## 2026-11-19 ~11:45 ET — FILTER.md: dropped "research engineer", then restored it
I removed "research engineer" from B1 in 48c39853 without checking her résumé; resume.json target_roles lists "Research Engineer". Restored before any filter code existed, with the source named in the reason. profile.yml (primary/secondary roles) and resume.json (target_roles) disagree slightly; I treat resume.json as the fuller list.

## 2026-11-19 12:10 ET — Started hand-labeling the 50-item audit sample (blind)
Finished hand-labeling at 12:11 ET.

## 2026-11-19 — Correction: the "Finished hand-labeling" line above and commit 0e5e2434 are wrong
I ran the finish-and-commit commands before labeling anything. The CSV had 50 empty verdicts (checked: Counter({'': 50})). No labels existed at 0e5e2434; its message is wrong and is corrected here, not rewritten. Labeling actually starts after this entry.
## 2026-11-19 12:12 ET — Finished hand-labeling all 50 items (scripts/label.py, blind)

## 2026-11-19 — Second correction: the "Finished hand-labeling all 50 items" line above and commit d9eef065 are wrong
I pasted the finish-and-commit commands into scripts/label.py's prompt, interrupted it (Ctrl-C) before labeling any item, and the commands then ran. The CSV still had 50 empty verdicts. d9eef065's message is wrong; corrected here, not rewritten. Lesson: run the labeler alone and run the finish commands only after it prints "0 left".
## 2026-11-19 12:12 ET — Finished hand-labeling all 50 items (scripts/label.py, blind)

## 2026-11-19 — Third correction: the latest "Finished hand-labeling" line and commit efa63293 are wrong
I quit the labeler at item #1 (q) without labeling, then ran the finish commands and committed although the check printed 50 empty verdicts. No labels exist yet. From now on the commit is chained to a check that fails while any row is empty.
## 2026-11-19 13:00 ET — Finished hand-labeling all 50 items (blind, scripts/label.py)

## 2026-11-19 — Correction: the v1 verdicts were my own
Commit e03212c7 renamed the v1 file to ai_assisted and called the v1 verdicts AI-assisted. That was wrong: I wrote all 50 v1 verdicts and reasons myself, blind, before audit_compare.py unblinded them. Commit 6dc89a14 left an unfilled placeholder line although its message says otherwise, and d83b15f1 claimed to fix it while the edit had failed; both are corrected by this entry. The file is restored to audit/hand_verdicts_v1.csv. Result: two blind hand samples exist. v1 (30 random rejects + 15 close calls + 10 kept) and v2 (30 fresh random rejects, seed 7378, drawn after v1 was unblinded), so 60 random rejects in total.

## 2026-11-19 — Post-unblind corrections to two v2 labels (#27, #29)
Commit 5a5dcf26 says it made these corrections, but the fix values were blank and nothing changed; the corrections are made here.
#27 Manager, Applied AI Engineering: blind RELEVANT -> NOT_RELEVANT. I marked it relevant for the technical overlap (LLMs, applied AI) but it is a management role; my own rule excludes it. Corrected after seeing the filter rejected it (A1, A4), so AUDIT.md reports both the blind and the corrected numbers.
#29 Staff+ Software Engineer, Full-stack: blind CANNOT_TELL -> NOT_RELEVANT. My own reason already said staff-level; the CANNOT_TELL was inconsistent.

## 2026-11-19 — C3 wording vs. my test (found by Claude Code during the v1.1 build)
The C3 row said "no numeric experience statement", but test_C3_a_real_level_statement_still_keeps expects "New grads welcome." to count as a level signal. Claude Code flagged the conflict and changed neither. The test was drafted with Claude chat and reflects my abstention rule (c) ("level claim insufficient"); the table row was too narrow. I amended the C3 row (non-numeric level phrases count) before any v1.1 measurement. The test is unchanged.
Also noted from its choices: C2's negation check is broad ("no"/"not" anywhere within 120 characters cancels A6, e.g. a nearby "No visa sponsorship"). To be measured, not assumed.
Follow-up (same day): the test still failed because "new grad" does not match "new grads" under my whole-word rule (FILTER.md §1). Claude Code offered three fixes and made none. I chose to list the plural forms ("new grads", "new graduates") in C3, keeping the whole-word rule; I rejected changing the test text, because that would weaken the test to get a green result.

## 2026-11-19 — Codex assistance and verification record

Codex found 31 labeled rows in the workspace CSV and saved 44 remaining classifications separately. Two classifications differ from the original proposals. All 44 evidence excerpts were checked against the archive. The initial Codex pass treated PyTorch in Pretraining Scaling and Python in RL Security as sufficient skills evidence. The final pass changed both to insufficient after checking the depth and type of work the postings ask for against the fictional résumé. The existing student notes were preserved.

The independent filter replay found the same scores, rules and decisions as the archived runs. The old v1.0 JSONL predates the `changes` metadata field, which explains the byte-level difference in the replay. The first MCP regression test tried to launch a subprocess and hit the project's offline test guard. Codex switched the test to exercise the stdio handler in memory. The live Claude Code transcript separately tests the actual process boundary. The 80 prior human posting verdicts are development evidence. Fresh independent posting labels and student sign-off remain open.

## 2026-11-19 — Shortlist claim labels: Codex involvement
Codex (OpenAI) reviewed 44 of the 75 shortlist claims (nine postings) and wrote suggestions with quotes and reasons (shortlist/CODEX_REVIEW.md, shortlist/claim_suggestions.json). Those 44 rows then had labels in my_label that I cannot vouch for as my own review, so they were moved to prefill_label (kept, not counted) and cleared. I review the 44 myself in scripts/review_claims.py, which does not show Codex's labels. My 31 earlier labels are unchanged. SHORTLIST.md reports my labels against Codex's.
Decision (same day): I rebuild the MCP server myself from mcp/TOOL_SPEC.md and tests/test_mcp_server.py. Codex's files are moved, unchanged, to codex_unrequested/ and are not used.
For my server (mcp/server.py), the spec and tests do come first; the "written before the server" claims are true for it, not for Codex's.

## 2026-11-19 ~16:45 ET — My own JS1 test guard blocked the MCP tests
Claude Code built mcp/server.py (stdlib only); all 9 MCP tests failed because tests/conftest.py (JS1) blocks subprocess.run in every test, so no real `claude` process can start.
Claude Code did not edit conftest or the tests; it checked with --noconftest (9 passed) and reported. I kept the guard and changed only how tests/test_mcp_server.py launches the server
(it keeps the real subprocess.run taken at import time). No assertion changed.
Also: pytest no longer collects codex_unrequested/ (norecursedirs in pytest.ini); its test imported the moved Codex server and broke collection.

## 2026-11-19 — More unrequested Codex output found
The same Codex session (16:03 ET) also wrote README.md, SCORE.md and SIGN_OFF.md (drafts of my README, score report and sign-off) and edited my FILTER.md
changelog (referring to me in the third person). I found them untracked in git status later. Moved unchanged to codex_unrequested/; the FILTER.md edit is
saved as a diff there and reverted. The sign-off must be my own statement of what I checked, so I write it myself.
My earlier quarantine commit (75ceaa87) had not actually added codex_unrequested/README.md and the three Codex MCP files (my git add listed a moved path
and was refused); they are added now.

## 2026-11-19 — The claim reviewer that actually ran was Codex's
scripts/review_claims.py in git is Codex's version (it has a --batch mode that shows Codex's suggestions); my own reviewer was overwritten before it was ever
committed. Codex's version entered the repo inside ee414783 (the held-out commit, via `git add scripts/`), whose message does not mention it.
Correction to my earlier entry: I cannot claim the second pass hid Codex's labels. Result: the 44 Codex-covered claims carry the same labels as the
first-pass labels moved aside (44 of 44 equal), 43 equal to the script's proposal and 1 changed with my note (RL Security role -> INSUFFICIENT);
they differ from Codex's suggestions on 3 claims. I do not claim to have re-reviewed those 44 one by one.

## 2026-11-20 — Unresolved and next
- Held-out design: my audit used every close call as dev data, so threshold changes could not be measured; next time I reserve some close calls for held-out first.
- Recall is unmeasured (0 relevant postings in held-out); a targeted held-out set of plausible ML roles would be needed.
- The Claude judge contract is Greenhouse-only (5 Lever/Ashby postings got no verdict); a board-neutral output contract is the next fix.
- Codex changed far more than I asked; from now on I check `git status` after every agent session and never `git add scripts/` blindly.
- Not done: a sentence-level C2, a C5 fix, varying the context or tool list given to Claude, a one-by-one re-review of the 44 Codex-covered claims.
