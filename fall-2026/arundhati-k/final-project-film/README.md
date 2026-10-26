# Co-op Sponsor Check — Final Project Pitch Film

- **Name:** Arundhati Kandelkar
- **Working title:** Co-op Sponsor Check
- **Target role:** software developer / full-stack developer
- **Runtime:** 3:37 (216.9 s) · 3840×2160 · 24 fps · 22 beats · master SHA-256 `ff39c0ebb8ddf1989da3f109cfaa776cc9c0638daef0b484cb5be275a195a6d1` · revised 2026-10-25
- **Narration:** synthetic voice (Kokoro `bf_emma`, local, free) reading my script — not my recorded voice.
- **Status:** pitch, not a build. What exists and what will exist are listed at the end of [PROJECT-BRIEF.md](PROJECT-BRIEF.md).

## What is in this folder

| File | What it is |
|---|---|
| `coop-sponsor-check-pitch.mp4` | the rendered film |
| `PROJECT-BRIEF.md` | the seven answers in text, ending with *exists today* and *will exist* |
| `beat_sheet.json` | narration and visual plan, with measured audio durations |
| `BUILD-PROMPT.md` | the prompts and commands that rebuild the film |
| `SOURCES.md` | what I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | my own dated entries, in my own words |
| `BUILD-LOG.md` | Claude's technical log of the build (commands, errors, fixes) — was FRICTIONAL.md until 2026-10-21 |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | the toolkit's required records |
| `reports/` | gate reports: GATE T `TYPECHECK.md` (PASS), Gate V (0 blocker / 0 major), layout audit, verified.json |
| `evidence/` | the 2026-10-10 recipe re-run, USCIS hub searches, my predictions (`predictions-2026-10-25.md`), and the **25-row evaluation** (`eval-25-rows-2026-10-25.md`, script + raw output) |
| `source/` | `make_sheet.py` and `scenes.py`, copied from the reel folder `youtube/coop-sponsor-check-pitch/` |
| `SCRIPT-DRAFT.md` | the narration draft before it became the beat sheet |

## How to rebuild

See [BUILD-PROMPT.md](BUILD-PROMPT.md). Short version, from a folder holding both repos:

```bash
cd brutalist-final && export PATH="$PWD/.venv/bin:$PATH"
python3 runtime/scripts/generate_audio_kokoro.py ../info-7375-prompt-engineering-for-generative-ai/youtube/coop-sponsor-check-pitch
./art run   ../info-7375-prompt-engineering-for-generative-ai/youtube/coop-sponsor-check-pitch --height 2160
./art final ../info-7375-prompt-engineering-for-generative-ai/youtube/coop-sponsor-check-pitch --height 2160
```
