# FRICTIONAL — Job-Search Agent 1
Author: Gnanasudharsan Ashokumar

## Entries

Entries for 2026-10-28 were written at the end of the day from commits and terminal history (retrospective).

### 2026-10-28: Board Churn (678 to 680 postings)
- **What happened:** An initial exploration curl fetched 678 postings, while the subsequent baseline run (commit `6baa583`) recorded 680 postings. Because only one watch run has happened so far, nothing about state additions has been tested yet.
- **What I did:** Noted the churn; actual additions testing is deferred to run 2 tomorrow.
- **Commit:** `6baa583`

### 2026-10-28: Greenhouse Data Traps Encountered
- **What happened:** Discovered data anomalies (double HTML escapes, trailing spaces, ambiguous sponsorship phrasing). The exploration commands were supplied by a Claude chat, while all rule and filtering decisions were mine.
- **What I did:** Documented the 10 data traps and encoded corresponding regex/string cleans in the contract and rules.
- **Commit:** `fd949ad`

### 2026-10-28: Seeded-State and Allow-List Adjustments
- **What happened:** Two separate events occurred regarding state handling and host permissions, both written by Claude Code. First, Claude Code’s choice #3 had seeded runs update the real `state/` directory, which I modified to isolate seeded runs in `seeded/` (`806f052`). Second, Claude Code’s interpretation #12 revealed the allow-list omitted `api.anthropic.com`.
- **What I did:** Fixed the allow-list in Amendment 1 (`c841810`), implemented via `ec82533`.
- **Commit:** `806f052`, `c841810`, `ec82533`

### 2026-10-28: Rejected `rm -rf` / Destructive Cleanup Risk
- **What happened:** Claude Code proposed a scratchpad command containing an unguarded `rm -rf $D` on a variable path for the wrong-version check. Its own safety prompt flagged it.
- **What I did:** I chose "No" and explicitly asked for `mktemp -d` with no deletions. Claude Code re-executed the check safely: each wrong version caught its expected failure, and `rule.py`'s shasum remained unchanged.
- **Commit:** `b1f1e45`

### 2026-10-28: 0 of 680 Baseline Finding Leading to Amendment 1
- **What happened:** During its offline sanity check, Claude Code found that the initial strict rule yielded 0 relevant postings out of 680 (leaving the rule code unchanged).
- **What I did:** Evaluated offline variant counts and introduced Amendment 1 (lowering skill threshold to ≥ 2 and adding "research engineer" to target titles), unlocking 7 relevant postings.
- **Expected:** I expected the strict new-grad filtering rule to successfully find at least 50 to 100 relevant postings out of the initial 680 scraped jobs, assuming standard entry-level hiring volumes.
- **Commit:** `c841810`, `ec82533`

### 2026-10-28: Corrected Provenance Header
- **What happened:** The header drafted for me in a Claude chat for `evidence/amendment1_variants.py` stated it "reads only" the raw file. Claude Code flagged that it also reads the persona and imports rule code.
- **What I did:** Accepted Claude Code's corrected header.
- **Commit:** `c841810`

### 2026-10-28: Tie-Breaker Logic Bug
- **What happened:** My first tie-breaker counted only technologies from her shipped list, meaning any posting failing the skills test triggered the skip, rendering the skills test un-failing. Found when a Claude chat reviewed my draft.
- **What I did:** Fixed the tie-breaker wording to specify "of any kind."
- **Commit:** `187b985`

### 2026-10-28: Personal Background Leak in Labeling Rule
- **What happened:** My draft labeling rule's Level line accidentally described my real degree and co-op instead of Ananya's persona values. Found when a Claude chat reviewed my draft.
- **What I did:** Replaced it with Ananya's persona values (MS CS, BU, Lumenwise co-op) before committing.
- **Commit:** `187b985`

### 2026-10-28: Managing Claude Code Choices & Prompts
- **What happened:** Of the 9 watch choices, I accepted 8 and modified #3 (seeded-state isolation). Of the 12 judge interpretations, I accepted 11; #12 (the allow-list gap) led to Amendment 1. Furthermore, Claude Code twice suggested prompts ("Write the two amendment1 tests" and "Commit the evidence files") that I chose not to send, keeping test independence and commit control strictly in my hands.
- **Commit:** `806f052`, `b1f1e45`

### 2026-10-28: Test-Driven Development Milestones
- **What happened:** My rule tests and Amendment 1 tests were written before the code they test (test file drafted with help from a Claude chat; cases from my contract).
- **Commit:** `bbbafdf`, `b1f1e45`, `c841810`, `ec82533`

### 2026-10-28: Corrected Wrong Claim in Amendment 1
- **What happened:** The original wording claiming "No existing test changed" came from a Claude chat suggestion; Claude Code flagged that it was no longer true after it fixed its own two tests.
- **What I did:** Promptly corrected the contract line to reflect reality.
- **Commit:** `ec82533`

### 2026-10-28: Unresolved / Known Limitations & Lessons Learned
- **What happened / Known limits:**
- Remote non-US locations pass the rule without country filtering.
- Anthropic "Research Engineer" roles may require research depth beyond new-grad scope.
- The seeded-run guard is only in the CLI; calling `run_watch()` directly with the project folder as root isn't blocked.
- Python 3.10 runtime remains untested.
- Absolute paths appear in some output records.
- The second-day live run is not completed yet (done 2026-10-29, `b04c897`).
- **Learned:** A rule can pass every unit test and still find nothing on real data; check per-condition pass rates on real data before trusting it.

### 2026-10-29: Backend Transition (No API Key) & Smoke Test
- **What happened:** Lacking an Anthropic API key or budget, I first switched the judge execution to Claude Code's non-interactive print mode (`JOBWATCH_BACKEND=claude_cli`) under my Enterprise login, and wrote Amendment 2 before any live call. The first live smoke test then returned `NOT_RELEVANT` for posting `4613568008` while my human label was `RELEVANT` (num_turns 1, temp cwd).
- **What I did:** Formalized the CLI backend in Amendment 2 with all tools disabled (`--tools ""`) and a fresh empty temporary working directory per call, corrected an overclaim about test coverage, and kept both the label and the prompt unchanged after the smoke test.
- **Commit:** `beb7793`, `14c75ac`, `96de51f`, `fe1df1d`

### 2026-10-29: Second-Day Live Run (Run 2)
- **What happened:** Executed the second calendar day watch run, resulting in 2 new additions and 3 removals (board size shifting 680 to 679). Recomputation matched successfully.
- **What I did:** Verified state behavior; noted that because the state file persists removed IDs, a re-posted job ID would not trigger a new addition report.
- **Commit:** `b04c897`

### 2026-10-29: Sampling Trial Run & Disagreement Analysis
- **What happened:** Ran 5 dev postings across 4 fresh calls each (20 total evaluations), achieving 55% agreement (11/20) and 4/5 unanimous postings. Unanimous disagreements clustered around two distinct rule/model gaps: implicit level signals (pay bands and seniority qualifications) and how experiments are categorized (evaluate vs. research).
- **What I did:** Scored the sampling outputs, generated evidence files, and authored `SAMPLING_REPORT.md` to document the repeatability and divergence patterns.
- **Expected:** I expected Claude's live judgments to achieve at least 80% to 90% agreement with my hand-crafted labels, assuming our definitions of a relevant new-grad ML role were largely aligned.
- **Commit:** `b7e58f7` (sampling run), `1f1f07c` (scorer)

### 2026-10-29: Quoted Text Mismatch in Sampling Report
- **What happened:** My first draft of Section 4 in `SAMPLING_REPORT.md` mistakenly quoted job description text as if it were Claude's generated reasoning. A grep check against the saved run outputs revealed 0 matches for those strings.
- **What I did:** Replaced the incorrect text with Claude's actual reasoning phrases extracted directly from the run logs (`5438044008_r01.json` and `4631822008_r01.json`).
- **Commit:** `e5ce9e5`

### 2026-10-29: Two Revision Changes Applied by Accident
- **What happened:** While writing `prompts/judge_revision.md`, I ran both candidate edits (experiments-as-evaluate in point 1, explicit-only level in point 2), so the revision briefly had two changes, which would break "one change at a time".
- **What I did:** `diff` against the baseline showed two changed lines before any run. I reset the file to the baseline, applied only change (b), confirmed one changed line, and committed it before the revision's dev run (commit 05:17:08 UTC; order check in `evidence/exp_revision_order_check.txt`).
- **Commit:** `908b8f7`

### 2026-10-29: Hand-Typed Diff in the Experiment Report
- **What happened:** In `EXPERIMENT_REPORT.md` I retyped the prompt diff by hand several times; versions had paraphrased wording, an invented `@@` header, wrong run-folder names, and made-up timestamps that did not match my files.
- **What I did:** Replaced the typed diff with the exact added sentence and a pointer to the machine-generated `evidence/exp_prompt_diff.txt` (`diff -u`), and copied run-folder names from `ls` output. Lesson: only copy evidence from the terminal or files, never retype it.
- **Commit:** `71830f9`, `0ab1c6c`

### 2026-10-29: Prompt Experiment Result — Held-Out at the Ceiling
- **What happened:** Baseline 7/10 on dev; the one-change revision 10/10 on dev; both 10/10 on held-out. Held-out had no research-blended posting with only implicit seniority signals, so it could not separate the prompts.
- **What I did:** Reported generalization as untested instead of claiming the revision is better, and did not change either prompt after seeing held-out.
- **Expected:** I expected the held-out set to show a clear drop for the baseline and a higher score for the revision, confirming that the explicit-level rule generalized successfully across unseen data.
- **Commit:** `71830f9`

### 2026-10-29: Action Surface — Clipboard Overwritten
- **What happened:** For Mode 1, my clipboard was overwritten twice: copying the check commands, and then copying terminal output, replaced the prompt I meant to paste into Claude.ai.
- **What I did:** Wrote the input to `experiment/action_surface/mode1_input.txt` and copied from that file right before pasting, which also records exactly what was pasted.
- **Commit:** `93600bf`

### 2026-10-29: Action Surface — Auto Mode Found in the Session Logs
- **What happened:** In Mode 3, Claude Code never asked me for permission. Extracting the tool calls from the local session logs showed `permissionMode: auto` for both Mode 2 and Mode 3: every step was a raw Bash command approved by the auto-mode classifier, not by me. Mode 3 also wrote files in a scratchpad outside the sandbox folder, stayed on `boards-api.greenhouse.io` only by its own choice, and unescaped the double-escaped content once.
- **What I did:** Recorded only the extracted tool calls (`mode2_tool_summary.txt`, `mode3_tool_log.txt`), not the transcripts, and used the finding in `ACTION_SURFACE.md`: the authority comes from the tool settings, not the task.
- **Commit:** `93600bf`

### 2026-10-29: Unresolved / Not Checked (as of submission)
- Removed postings are not reported, and the state keeps removed ids, so a re-posted id would not be reported as new.
- Remote postings outside the US pass the rule; Research Engineer roles may require research depth the rule does not check.
- The revision prompt's generalization is untested (held-out ceiling); the watch still uses the baseline prompt.
- Modes 2 and 3 were run only in auto mode; default permission mode was not tested. Each tool call appears twice in the session logs, which I did not verify.
- Python 3.10 untested (3.14.0 only); the seeded-run guard is CLI-only; the claude_cli and API backends were not compared.
- **Learned:** Repeatability is not correctness; a held-out set only tests what it contains; and an agent's reach is set by its permissions, not by the task it is given.

_Note: 2026-10-29 entries in this section were organized with help from a Claude chat from my commits and evidence files; the events and decisions are mine._