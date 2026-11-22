# DecisionTrace Lite — Project Film

- **Name:** Gnanasudharsan Ashokumar
- **Course:** INFO 7375 Prompt Engineering for Generative AI, Fall 2026
- **Runtime:** 5:01.5 (301.5 s). Executive summary 0:00–0:45, introduction 0:45–1:53, methods
  1:53–3:44, evaluation 3:44–5:01.
- **Film:** `decisiontrace-lite-film.mp4` (3840×2160, H.264 + AAC, 25.0 MB)
- **Status:** rendered 2026-11-22; watched and approved by me 2026-11-22.

## What this is

This is a 5-minute film in the professor's four-part structure: executive summary, introduction,
methods, evaluation. It's for DecisionTrace Lite, a planned tool that answers "why, when or who decided X?"
over synthetic enterprise documents, with a citation for every claim. It's a scoped-down sibling of
my larger Neo4j/LangGraph/FastAPI system, which is a separate project.

DecisionTrace Lite isn't built yet. What exists is the October alternatives test (`../evidence/`)
and these film materials. The pitch film in `../` is separate and unchanged.

## Folder contents

**Planning documents**

| Path | What it is |
|---|---|
| `script.md` | Narration, lines L01–L35 (L10 and L12 cut), section timestamps |
| `slides.md` | Marp slides, one idea each, for a slide-and-voice version |
| `shot-list.md` | Script line → slide or screen recording, for that version |
| `appendix.md` | Build plan, data schemas, metrics and targets, resources (scripted Claude Code use **pending**), references with confidence and VERIFY marks |

**The film and its paperwork**

| Path | What it is |
|---|---|
| `decisiontrace-lite-film.mp4` | The final master from `./art final` |
| `beat_sheet.json` | 20 beats: narration (verbatim from `script.md`), script line IDs, scene, measured audio length, build records |
| `FACTCHECK.md` | Every claim in the narration, with its source or PLAN / AUTHOR'S STATEMENT / CITED / CONSTRUCTED |
| `SHOTLIST.md` | How each beat was made |
| `PROMPTS.md` | No AI-generated images or video |
| `SOURCES.md` | What I made, what Claude contributed, third-party material, data, voice |
| `FRICTIONAL.md` | Dated log of problems and decisions |
| `BUILD-PROMPT.md` | Environment, commands in order, prompts verbatim |
| `.gitignore` | Lets this folder's `.mp4` through the course repo's `*.mp4` exclusion |

**`gate-reports/`: from the final run**

| File | What it is |
|---|---|
| `gate-V-REPORT.md`, `gate-V-contact_sheet.png` | Visual QC on the master: 40 frames, 0 BLOCKER, 0 MAJOR |
| `render-integrity.md` | Streams, duration, full decode, loudness, hash, size, corner tags |
| `persona-grep.md` | No instructor persona strings |
| `decisiontrace-lite-film.verified.json`, `build-state.json` | The toolkit's verification record and build state (`ready`) |
| `final-run.log` | Output of `./art final` |

**`build/`: my build files (not toolkit files)**

| Path | What it is |
|---|---|
| `build/scenes.py` | Manim scenes for 18 beats |
| `build/tools/make_beat_sheet.py` | Builds `beat_sheet.json` from `script.md` |
| `build/tools/still_clips.py` | B07 clip and B08 still from the reused frames |
| `build/tools/phoneme_name.py` | The pitch film's IPA name tool, unchanged |
| `build/frames/` | B03a, B03b, B04, byte-identical to `../build/frames/` |

## How to rebuild

See `BUILD-PROMPT.md` §3–4.
