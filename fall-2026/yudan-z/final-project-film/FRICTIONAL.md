# FRICTIONAL — Final Project Pitch Film

## Executive summary

This is my dated log of building the pitch film: what I tried, what broke, what I or the AI assistant (Claude Code) did about it, and what I decided. Each entry names who did the work. The biggest frictions were Windows-specific toolkit failures, a stock outro that hardcoded the instructor's handle, and statements in my own drafts that did not match my files.

---

## 2026-10-12

| # | Attempt | What happened | Response | Who |
|---|---|---|---|---|
| 1 | Read the assignment; looked for the GitHub repo to post into | The assignment gives a folder path (`fall-2026/<name>/final-project-film/`) but my Reallocation Engine repo has no such folder | Decided the folder goes in the instructor's repo, uploaded through the web | Me |
| 2 | Chose a project | I had no idea at first. The AI suggested continuing my Reallocation Engine recipe (`is-funded-sponsor-triage`) because "exists today" would be real; I chose Data Analyst as the target role | Accepted the direction; target role is mine | Me, from an AI suggestion |
| 3 | Checked the local Brutalist checkout | My old clone was 46 commits behind and had uncommitted local edits | Made a fresh clone (`brutalist-film`) instead of pulling over my edits | AI |

## 2026-10-13

| # | Attempt | What happened | Response | Who |
|---|---|---|---|---|
| 4 | First PROJECT-BRIEF draft | An AI review against my repository found 4 statements that did not match my files: it said the tool scores blank companies (it holds them out), credited a Linux run I never did, misdated the submission (10-12 instead of 10-02), and called a 564-approval record "the strongest" in a set with an 8,810-approval one | Corrected all four; added the episode to §6 as an instance of my project's own risk | AI caught, I corrected |
| 5 | Target role | My first brief said Data Scientist / ML Engineer; I had said Data Analyst | Changed to Data Analyst — the project shows data-cleaning and evidence skills, not ML | Me |
| 6 | Alternatives (question 2) | I had written what h1bdata.info "returns" before opening it | Searched h1bdata.info myself on 2026-10-13 22:40 for "Moloco" (long table of filings) and "123 See" (no table, no count, no not-found message); saved screenshots in `evidence/` | Me |
| 7 | "204 records" for Moloco | The number is not visible in any of my four screenshots | Kept it out of the narration and off the screen; the beat says only what the screenshots show | AI flagged, I agreed |
| 8 | Installed Manim | Worried it would not run on Python 3.14; Manim 0.20.1 (the toolkit's pin) installed and a test scene rendered | No switch to Remotion cards needed | AI |
| 9 | Stock outro `ClaudeTitleOutro` | Its source hardcodes `const HANDLE = '@NikBearBrown'` plus the channel mascot, ignoring any `handle` prop. The assignment forbids the instructor's name or credit line | Had the AI assistant write my own component, `StudentTitleOutro` (handle from props, mascot removed), and register it. `bookend_check.py` then passed honestly — I did not edit the shared component or silence the check | My decision; AI wrote the code |
| 10 | My earlier expectation about the check | I (via the AI) first predicted `bookend_check` would report "missing ClaudeTitleOutro". Reading the code showed it only checks the BOUT beat's handle/title/subline | Corrected the plan before building | AI, corrected by reading the code |
| 11 | Narration length | Measured with the real voice: 3:58 — too close to the 4:00 limit | Approved five cuts that each repeated something said elsewhere; final 3:45.5. Moved the run date onto a B02 label so it is still shown | Me (approved cuts), AI (measured) |
| 12 | Generated narration | `generate_audio_kokoro.py` crashed: `UnicodeDecodeError: 'charmap' codec` (Windows default encoding) | Ran with `PYTHONUTF8=1`; no toolkit code changed | AI |
| 13 | `art run` | `manim: command not found` — pip installed it in my user Scripts folder, not on PATH | Added that folder to PATH for the run | AI |
| 14 | Remotion bookends | `[WinError 2]` — the toolkit calls `npx` without a shell, and Windows only has `npx.cmd` | Ran the toolkit's own `remotion_scenes.py` through a small wrapper that resolves `npx` to its full path; no toolkit file changed | AI |
| 15 | Review cut | ffmpeg `drawtext` could not parse the Windows font path `C:\...` (review-cut timecode burn-in) | Used the toolkit's built-in `ART_NO_DRAWTEXT=1` switch; the final master never burns in a timecode | AI |
| 16 | Gate V | 9 MAJOR `underfill` defects. Eight were show-tell's deliberate single-object frames (35–52% fill); B06's midpoint was 6% — nearly empty | Declared the skill's documented `sparse_by_design` waiver (with a reason) on B01, B03, B05, B06, B08, B11; fixed B06's content instead of hiding it (the shortlist sheet is now on stage from the start) | AI proposed, per the skill's rule |

| 17 | `art final` (Gate T) | FAIL on B10: "text-run bbox overlap 46%". The labels did not overlap; the eight record cards were stacked edge to edge, so their grey lines read as stacked text, and the beam crossed the stack | Redrew B10: pivot raised, five cards with gaps, longer pan strings; retired the old clip to `_superseded/` and re-rendered | AI |

**What I learned:** a fluent first draft is the failure my project is about — and it happened to my own pitch before it happened to my tool. Checking each sentence against a file I already had caught every error.

**Still unresolved:** whether the AI voice counts as "narrate as yourself" — the script is mine and in first person, and the film says on screen that the voice is synthetic.
