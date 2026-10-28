# SOURCES — SponsorScout (INFO 7375 Final Project Pitch Film)

Akshit Verma · 2026-10-14

## 1. What the film's claims rest on

Every number on screen or in the narration comes from my Assignment 1 repository,
[`the-reallocation-engine`](https://github.com/AkshitVerma-AV/the-reallocation-engine) at commit
`a1d321f` (PR [#44](https://github.com/nikbearbrown/the-reallocation-engine/pull/44), open, not merged).
Claim-by-claim sources are in `FACTCHECK.md`.

| Source | Used for | When I got it |
|---|---|---|
| `course/2026fa/submissions/AkshitVerma-AV/runs/run-2/network-targets.md` | 123 candidates → 2 / 1 / 107 / 13 (B06); 16 boards (B11) | run 2026-10-03 |
| `runs/run-1/` + `WORKED-RUN.md` | the Zoox false positive (B07); 16 boards fetched live | run 2026-10-03 |
| `runs/engine-baseline/role-scores.md` | the engine's scorer gives a sponsor with no live posting 0.000 → Skip (B03) | run 2026-10-03 |
| Assignment 1 `FRICTIONAL.md`, `SUBMISSION.md` | who did what (Claude wrote most code; I set the rules; I signed G1 and G3) | written 2026-10-03/04 |
| Test re-run, this project | "All twenty-five tests passed again on October twelfth" | 2026-10-12 |
| [myvisajobs.com](https://www.myvisajobs.com/) | B04's comparison. **I looked at it on 2026-10-07.** No content, logo or screenshot from the site is used | 2026-10-07 |

Data behind those runs (all public; the job seeker "Jack Spencer" is fictional, `@example.com`):
the 80 Days to Stay sponsorship CSV and the SEC Form D samples shipped in the Reallocation Engine
repository, and the public Greenhouse / Lever / Ashby job-board APIs. No private data, résumé,
contacts, tracker or conversation transcript is in the film or this folder.

## 2. What I used (tools and assets)

| Thing | Version | Licence | Use |
|---|---|---|---|
| [brutalist.art](https://github.com/nikbearbrown/brutalist.art) toolkit (Nik Bear Brown) | `6a8380a` + my changes (`toolkit-changes/`) | no LICENSE file in the repository | the pipeline: audio, word clock, render, gates, compile |
| show-tell drawing kit `iso_kit.py` (same toolkit, upstream `4115560`) | read with `git show`, not cloned | same as above | pasted into `scenes.py` as the skill says (minus the writing kit and the instructor-portrait helper) |
| Kokoro-82M TTS model + `voices-v1.0.bin`, voice **`am_michael`** | v1.0 | Apache-2.0 (per the model's release) | **the narration is a synthetic voice**, not my recorded voice |
| `kokoro-onnx` | 0.6.1 | MIT (per its repository) | runs Kokoro locally |
| Manim Community | 0.18.1 | MIT | all drawings |
| Remotion | 4.0.486 | Remotion License (free for individuals) | the outro card |
| ffmpeg (gyan.dev full build) | 9.0.2 | GPL | encode, caption burn-in |
| faster-whisper (`small` model) | 1.2.1 | MIT | word timing (`align.py`) and the blind listening check |
| EB Garamond | — | SIL OFL 1.1 (`runtime/fonts/EB_Garamond/OFL.txt`) | drawing labels |
| Lato | — | SIL OFL 1.1 | captions, outro |

Cost: $0.00. Free and local: no paid generation, no API keys, no media account, no upload.

## 3. What I made, what Claude contributed

Claude Code (Claude Opus 5.5) did most of the building, in this session, under my direction.

| Part | Me (Akshit) | Claude Code |
|---|---|---|
| Project choice | chose to build on my Assignment 1 recipe | proposed four options, recommended this one |
| Name | chose **SponsorScout** from Claude's list (rejected "Warmlist") | proposed and pronunciation-checked the options |
| PROJECT-BRIEF.md | my reason for the project (§7), the MyVisaJobs check (§2), review | drafted everything else from my Assignment 1 files |
| Narration | approved it; supplied my reason; asked for the intro/outro changes | wrote the script; tightened my reason at my request; fixed misheard and overclaimed lines |
| Visuals | six review notes after watching v1 (screenshots of the defects) | all drawings (`scenes.py`), the outro (`pitch.tsx`), both revisions |
| Voice | chose Kokoro `am_michael` | ran it, measured it |
| Gates, captions | — | ran every gate; fixed every failure; frame-read the film; captions from `words.json` |
| Docs | review | drafted FACTCHECK, SHOTLIST, BUILD-PROMPT, README, this file, and organised FRICTIONAL |
| Sign-off | approved the final film, 2026-10-14 | — |

From my own earlier work, reused: `tools/make_captions.py` (my Week 01 film, built with Claude).

**No Claude response is shown in the film.** The film contains no screenshots: every picture is a
constructed drawing, and each one is tagged on screen as constructed, with "ran <date>" or
"proposed".

## 4. Not in this folder (on purpose)

`_reference/` (copies of the toolkit's skill files, not mine to redistribute), the first version's passing gate reports and listening check (they carry the earlier working title; the failing reports from both versions are kept in `_superseded/`), render caches
(`media/`, `manim/`, `clips/`), the uncaptioned and review cuts, and anything private.
