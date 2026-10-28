# SponsorSQL — Final Project Pitch Film

**Atharva Hambir** · INFO 7375 · Fall 2026

| | |
|---|---|
| Working title | **SponsorSQL**: plain-English questions, checked answers |
| Target role | Data Analyst |
| Film | `atharva-sponsorsql-pitch.mp4` · 1920×1080 · **3 min 31 s** (210.8 s) · revised 2026-10-24 |
| Status | A pitch. Nothing in SponsorSQL has been built yet. The latest data file is downloaded but not loaded. |
| Stack (planned) | Python, DuckDB, Claude; data: U.S. DOL LCA disclosure file FY2026 Q3 (latest release) |

SponsorSQL will let an international student ask a plain-English question about public H-1B filing data. It will show the SQL Claude wrote, the answer, and whether that answer matched a hand-checked answer key, and it will publish its failure rate and a log of its mistakes.

## What's in this folder

| File | What it is |
|---|---|
| `atharva-sponsorsql-pitch.mp4` | The rendered film |
| `PROJECT-BRIEF.md` | The seven answers, ending with *exists today* and *will exist* |
| `beat_sheet.json` | Narration and visual plan, 13 beats, with the measured audio durations stamped in |
| `scenes.py` | The Manim drawings for B02–B10 and B12 |
| `BUILD-PROMPT.md` | The prompt and commands that rebuild the film |
| `SOURCES.md` | What I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | Dated log of what went wrong and what I did about it |
| `gate-reports/` | The toolkit's gate reports: GATE V (final: 0 BLOCKER, 0 MAJOR), its contact sheet, the GATE B audit, and the log of every build run, including the failed ones |
| `evals/` | The ChatGPT test: the prompt, and the reply word for word (2026-10-24), including the follow-up where it reported 40 |
| `reel-paperwork/` | FACTCHECK, SHOTLIST, PROMPTS (GATE F requires all three before rendering) |

## How to rebuild

See `BUILD-PROMPT.md`. In short, from a `brutalist.art` checkout with its Python 3.12 venv active:

```bash
python3 runtime/scripts/generate_audio_kokoro.py ../youtube/atharva-sponsorsql-pitch
python3 runtime/scripts/remotion_scenes.py ../youtube/atharva-sponsorsql-pitch
./art run ../youtube/atharva-sponsorsql-pitch
./art final ../youtube/atharva-sponsorsql-pitch --height 1080 --out ../youtube/atharva-sponsorsql-pitch
```

Free pipeline only: local Kokoro narration, Manim and Remotion. No API keys, no paid generation, no upload.

## Honesty notes
- Everything about the project is in "will". What exists: the brief, the downloaded FY2026 Q3 file (checksum in the brief) and the ChatGPT test.
- On-screen mock-ups and invented examples are labelled CONSTRUCTED (B00 reply, B05 table, B08 company).
- The only outside AI output shown is my ChatGPT test (B04), quoted from the saved reply. Its 40 is its own run of its own query, and the film says it is unchecked.
- No Claude response is shown in the film.
- The narration is a synthetic voice (Kokoro `am_onyx`). The first-person script was written with Claude and reviewed by me, and the film says both at the start and the end.
