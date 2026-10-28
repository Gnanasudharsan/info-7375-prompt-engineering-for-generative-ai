# FRICTIONAL — Job-Search Agent 1
Author: Gnanasudharsan Ashokumar

## Entries

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
  - The second-day live run is not completed yet.
- **Learned:** A rule can pass every unit test and still find nothing on real data; check per-condition pass rates on real data before trusting it.