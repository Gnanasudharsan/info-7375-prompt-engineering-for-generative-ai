# FACTCHECK — DryRun pitch film (v5, resubmission)

Verdicts: PASS (checked), CORRECTED (changed after checking), EXEMPT (a plan, stated as "will" or "planned", not a fact).

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B00 | My name, aiming for backend and platform engineering roles | PASS | Me | v3: degree, university and graduation date removed from the opening |
| 2 | B01 | AI assistants suggest terminal commands and coding agents run them | PASS | Claude Code runs shell commands through its Bash tool; B02 is a real suggested command | — |
| 3 | B01 | One wrong character can delete files | PASS | General shell behaviour (e.g. a stray space before `*` in `rm -rf build/ *`) | Kept general |
| 4 | B02 | Claude replied `find logs -type f -name "*.log" -mtime +7 -delete` | PASS | Real reply, claude.ai, 2026-10-11 (`evidence/claude-reply-2026-10-11.png`) | v5: shown as the real screenshot, cropped, not retyped |
| 5 | B02 | It advised previewing first, without `-delete` | PASS | Same reply: "To preview what will be deleted first, run the same command without -delete." | v5: the reply's own words are on screen in the screenshot, so the paraphrase label is gone |
| 6 | B03 | On my Mac, the preview did not match a 7.5-day-old file | PASS | `evidence/mtime-test.md` (run 2026-10-11 by Claude Code; re-run by me 2026-10-13, same output; macOS find) | v5: on screen are my own Terminal lines from 13 Oct, copied exactly (the v4 chip said 11 Oct, Claude Code's run). Mac/Linux difference not claimed, because it wasn't tested |
| 7 | B05 | The AI's predicted changes | EXEMPT | Constructed; Claude gave no prediction | Labelled CONSTRUCTED EXAMPLE |
| 8 | B06 | The 8.5-day log is deleted on the copy | EXEMPT | Simulated from the preview test (1 file matched); nothing was deleted | CORRECTED: labelled CONSTRUCTED SIMULATION, not "actual change" |
| 9 | B07, B09 | WARN decision and report | EXEMPT | DryRun doesn't exist | Labelled CONSTRUCTED EXAMPLE / MOCK-UP |
| 10 | B00, B04–B08, B10, B11, B13–B17, B20 | Everything DryRun will do | EXEMPT | PROJECT-BRIEF.md | CORRECTED (v3): every planned feature in future tense, in narration and on screen ("will run", "will check", "will compare"); "Design goal", "Planned", "Version 1 will target" |
| 11 | B12 | `try` previews a command's file changes, Linux only | PASS | github.com/binpash/try README (overlayfs, Linux 5.11+) | — |
| 12 | B12 | Research benchmarks score AI shell commands offline | PASS | InterCode (arXiv 2306.14898); NL2SH (arXiv 2502.06858) | — |
| 13 | B17 | Same command can behave differently on Mac and Linux, e.g. `sed -i` | PASS | macOS ships BSD sed, where `-i` needs a suffix argument; GNU sed does not | — |
| 14 | B19 | I already know Python and testing, from my internship and my Reallocation Engine pull request (32 passing tests); I've used Docker in a cloud project at Northeastern | PASS | PR #33, github.com/nikbearbrown/the-reallocation-engine/pull/33 ("Ran 32 tests", checked 2026-10-13; re-run at commit `c0a7693` on 2026-10-23: "Ran 32 tests in 0.775s … OK", `evidence/pr33-tests-2026-10-23.md`); internship and cloud project: me, PROJECT-BRIEF.md question 7 | v4: evidence named instead of "my projects and my internship"; v5: the real test output is on screen, labelled REAL OUTPUT · PR #33 · 23 Oct 2026 |
| 16 | B14 | A reviewer could fairly conclude I can check and measure an AI's work, not that DryRun makes commands safe | EXEMPT | PROJECT-BRIEF.md, question 4 | v4: added; the second half is labelled NOT CLAIMED |
| 17 | B15 | You'll know the first piece ran when its self-test finds exactly the changes it planted | EXEMPT | PROJECT-BRIEF.md, question 5 (a plan, "will") | v4: added |
| 15 | B20 | No DryRun code exists yet | PASS | This folder | — |
