# SOURCES

## Executive summary

This page lists what the film uses, what I made, what the AI assistant (Claude Code) contributed, and the licence of every third-party piece. No third-party image, footage or music appears in the film; every picture is drawn in code and the voice is a local open-source model reading my script.

## What I used

| Item | What it is | Licence / terms |
|---|---|---|
| brutalist.art toolkit (commit `519fcbb`) | Show-tell skill, iso drawing kit, Remotion bookends (`BrutalistHesitantWriter`, `ClaudeDefinitions`), quality gates | Course toolkit by the instructor, used as the assignment directs |
| Manim Community 0.20.1 | Draws the 11 body scenes | MIT |
| Remotion | Renders the three bookends | Remotion licence (free for individuals) |
| Kokoro-82M via kokoro-onnx, voice `af_heart` | Synthetic narration voice reading my script | Apache-2.0 |
| EB Garamond | Typeface | SIL Open Font License |
| ffmpeg | Audio padding, assembly | LGPL/GPL |
| Data and run outputs | `nikbearbrown/the-reallocation-engine` fork `yudanzhou`, PR #13 (commit `5ae7747`), run of 2026-10-02 — shipped 80-Days CSV, Form D samples | Course repository |
| h1bdata.info | Two searches I made on 2026-10-13 (Moloco, 123 See); screenshots in `evidence/`. Shown in the film only as a drawing labelled CONSTRUCTED | Public website; screenshots are my own record, not reused in the film |
| TA feedback | Quote "you never turn a blank into a no", received 2026-10-12 | Feedback on my own submission |

## What I made

- The project, the target role, the seven answers in `PROJECT-BRIEF.md`, and approval of every narration sentence in `beat_sheet.json`.
- The two h1bdata.info searches and their screenshots.
- Decisions: the five cuts, keeping "204 records" off screen without evidence, replacing the stock outro.

## What Claude (AI assistant) contributed

- Suggested the project direction, reviewed my brief against my repository (caught four mismatches), and drafted narration I then edited and approved.
- Wrote the 11 Manim scenes (`scene_body.py`), the `StudentTitleOutro` component, the reel QC files (`FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`), and drafts of this file, `BUILD-PROMPT.md`, `FRICTIONAL.md` and `README.md`.
- Ran the toolkit and diagnosed the Windows failures (see `FRICTIONAL.md`).
- No Claude response is shown in the film.
