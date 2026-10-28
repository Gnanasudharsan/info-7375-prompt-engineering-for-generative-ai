# Final Project Pitch Film — Seeded Faults

- **Name:** Atharva Chonkar
- **Course:** INFO 7375, Fall 2026
- **Working title:** Seeded Faults — data-quality tests, tested
- **Target role:** Data Engineer / BI Engineer
- **Runtime:** 3:36 (216.5 s)
- **Film:** `seeded-faults-pitch.mp4` (3840×2160, re-rendered 2026-10-14 with Brutalist show-tell, free local pipeline)

## What's in this folder
| File | What it is |
|---|---|
| `PROJECT-BRIEF.md` | The seven answers, plus *exists today* / *will exist* |
| `beat_sheet.json` | Narration and visual plan, one idea per beat |
| `BUILD-PROMPT.md` | Prompts and commands that rebuild the film |
| `SOURCES.md` | What I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | Dated work log |
| `evidence/` | Scripts and logs behind every past-tense claim in the film |
| `gate-reports/` | Brutalist quality-gate reports; summary in `gate-reports/README.md` |
| `film-source/` | `scenes.py`, `make_sheet.py` and the toolkit paperwork that rebuild the film |

## How to rebuild the film
See `BUILD-PROMPT.md` for the exact commands. In short: install Brutalist (free local pipeline, Kokoro narration), copy `film-source/` into a build folder, run `make_sheet.py`, generate audio, then `./art run` and `./art final` at 4K.
