# SHOTLIST — DryRun pitch film (v5, resubmission)

Every beat is a Manim scene in `scenes.py` (built from `scenes_body.py`). On screen: a course kicker, short phrases (3–10 words) that appear when spoken, honesty chips, and source footers. v5: every beat that was text only now has a picture that carries its idea: real evidence (B02 screenshot, B03 terminal lines, B19 test output) or one of the toolkit's approved props, with the phrases kept as labels. No ShowTellCard beats, no person drawn, no floating decoration. v4: no terracotta anywhere; the props' small orange lights are removed in code (`no_terra`).

| Beat | Phrases and objects | Honesty label | Drawing |
|---|---|---|---|
| B00 | Name · "Target role: backend and platform engineering" · "DryRun will test AI-suggested commands before they touch your files" | — | — |
| B01 | The problem, four phrases (left column) · "your files" · "deleted" | — | agent-workstation hands a command down to an open crate; at "delete files" the files leave the crate |
| B02 | The real screenshot, cropped: my request · Claude's command (outlined when spoken) · its preview advice (underlined when spoken) | REAL SCREENSHOT · claude.ai · 11 Oct 2026; footer "real screenshot, cropped" | the screenshot itself (`evidence/claude-reply-2026-10-11.png`) |
| B03 | Terminal card with my two lines from 13 Oct (`$ find logs -type f -name "*.log" -mtime +7` / `logs/eight-and-a-half-days.log`) · three files by age, 7.5-day row highlighted | MY TERMINAL · 13 Oct 2026; footer "lines copied exactly" | terminal card, file rows |
| B04 | "It will be a GitHub repository" + tests + evaluation report · your folder → "DryRun will make a copy" → throwaway copy inside a dashed boundary · terminal card `find logs … -delete` pointing into the copy · "changes happen only here" · "Design goal: real files are never touched" | — | open context-crate → the same crate, smaller, in a dashed box; terminal card |
| B05 | Example step 1: command card, predicted-changes card | STEP 1 · CONSTRUCTED EXAMPLE | cards |
| B06 | Example step 2: "Planned: locked container · no network" · before/after list · 8.5-day log deleted | STEP 2 · CONSTRUCTED SIMULATION | — |
| B07 | Example step 3: predicted 2 vs simulated 1 · rule · ALLOW / WARN / BLOCK, WARN chosen | STEP 3 · CONSTRUCTED EXAMPLE | permission-gate (orange light removed) |
| B08 | Blocked → back to the AI · retries up to 3 times | LATER PHASE | arrow |
| B09 | Example step 4: report card, "Decision: WARN · 1 file missed" | STEP 4 · REPORT · CONSTRUCTED MOCK-UP | report card |
| B10 | Trap folders, five file chips with captions | — | chips |
| B11 | Evaluation plan, empty counters | PLANNED · NOT MEASURED YET | task-queue (tasks with known answers); the next task moves up |
| B12 | try (previews a command's file changes, Linux only) · research benchmarks (score AI commands offline, InterCode · NL2SH) | WHAT ALREADY EXISTS | checkpoint-scanner (parcel passes) · evidence-binder (cover opens) |
| B13 | "DryRun will go one step further" · the whole planned workflow: your folder (untouched) → throwaway copy (command runs here) → change report vs your request and the AI's prediction → ALLOW / WARN / BLOCK, you decide | PLANNED | open crate → crate in dashed box → report card → three chips |
| B14 | Four course-skill chips; fair conclusion; NOT CLAIMED chip | NOT CLAIMED | review-desk; the evidence is brought onto it at "check an AI's work" |
| B15 | In scope · out of scope · first piece · how you'll know it ran | FIRST PIECE TO RUN, HOW YOU'LL KNOW IT RAN | open crate (files and folders) · experiment-bench; the self-test plants a sample |
| B16 | Hardest part, and the plan | BIGGEST RISK | inspection-lamp lowers onto one task sheet |
| B17 | Mac vs Linux · "Version 1 will target Linux behaviour" | SECOND RISK | comparison-trays labelled Mac / Linux; the Linux sample lifts |
| B18 | Why this project · "my portfolio" | — | version-shelves and a dashed empty slot beside them |
| B19 | Already know (with evidence) vs new to me · terminal card "Ran 32 tests in 0.775s / OK" | REAL OUTPUT · PR #33 · 23 Oct 2026 | terminal card |
| B20 | No DryRun code yet · four phase chips | — | release-parcel, sealed |
| B21 | Title, close, name footer | — | — |
