# Final Project Pitch Film — *A Blank Is Not a No*

## Executive summary

This folder is my pitch for my INFO 7375 final project: a 3:45 film and its written brief. The project is `is-funded-sponsor-triage`, a job-search triage tool for international students. It refuses to read a missing sponsorship record as "no". The film says honestly what exists today (a recipe, a Python prototype, eleven tests, a dated run and a TA review) and what I will build next.

| | |
|---|---|
| **Name** | Yudan (Anica) Zhou · GitHub `@yudanzhou` |
| **Working title** | *A Blank Is Not a No* — `is-funded-sponsor-triage` |
| **Target role** | Data Analyst |
| **Runtime** | 3:45 (225.5 s), 1920×1080, H.264 + AAC |
| **Film** | `is-funded-sponsor-triage-pitch.mp4` |
| **Narration** | Synthetic voice (Kokoro `af_heart`, local) reading my own first-person script |

## What is in this folder

| File | What |
|---|---|
| `is-funded-sponsor-triage-pitch.mp4` | The rendered film |
| `PROJECT-BRIEF.md` | The seven answers, ending with *exists today* / *will exist* |
| `beat_sheet.json` | Narration and visual plan for all 14 beats (with the measured audio durations) |
| `BUILD-PROMPT.md` | The prompts, settings and commands that rebuild the film |
| `SOURCES.md` | What I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | Dated log of what broke and what I decided |
| `gate-reports/` | Toolkit quality gates: Gate V (0 BLOCKER / 0 MAJOR), Gate T (PASS), layout audit (CLEAN), bookend check (PASS), fact-check table, run logs, master verification |
| `build/` | The scene source (`scene_body.py`), my outro component (`StudentTitleOutro.tsx` + `Root.tsx.diff`), and the Windows `npx` wrapper |
| `evidence/` | My own h1bdata.info screenshots, 2026-10-13 (drawn in the film as CONSTRUCTED, not shown) |
| `drafts/` | The first beat draft, kept for the record |

## How to rebuild

Follow `BUILD-PROMPT.md`. In short:
1. Clone brutalist.art at `519fcbb`, then install the Python and Remotion dependencies.
2. Add `build/StudentTitleOutro.tsx` and apply `build/Root.tsx.diff`.
3. Create the reel folder from `beat_sheet.json` plus `scenes.py` (the kit's `iso_kit.py` followed by `build/scene_body.py`).
4. Run `generate_audio_kokoro.py`, then the Remotion bookends, then `./art run … --height 1080` and `./art final …`.

On Windows, set `PYTHONUTF8=1` and `ART_NO_DRAWTEXT=1`.
