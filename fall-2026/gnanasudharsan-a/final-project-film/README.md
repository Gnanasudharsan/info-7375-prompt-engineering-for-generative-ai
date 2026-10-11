# DecisionTrace — Final Project Pitch Film

- **Name:** Gnanasudharsan Ashokumar
- **Course:** INFO 7375 Prompt Engineering for Generative AI, Fall 2026
- **Working title:** DecisionTrace
- **Target role:** AI Engineer
- **Runtime:** 3:11 (191.5 s)
- **Film:** `decisiontrace-pitch.mp4` (3840×2160, H.264 + AAC, 12.6 MB)

## What this is

This is a 3-minute pitch for a project that doesn't exist yet.

DecisionTrace will answer "why did we decide X, and where does that
decision stand now?" over a team's documents. It will check each claim
against the source it cites.

Nothing in the project is built. Everything that does exist is listed in
`PROJECT-BRIEF.md` under "Exists today".

## Folder contents

**The film and its paperwork**

| Path | What it is |
|---|---|
| `README.md` | This file. |
| `decisiontrace-pitch.mp4` | The film, the final master from `./art final`. |
| `PROJECT-BRIEF.md` | The seven answers, ending with "Exists today" and "Will exist". |
| `beat_sheet.json` | The film's plan: 13 beats, each with its narration, scene and measured audio length. It includes the build records the toolkit wrote. |
| `BUILD-PROMPT.md` | How to rebuild the film: environment, commands in order, the name pronunciation, and the prompts I used. |
| `SOURCES.md` | What I made, what Claude contributed, third-party material with licences, data and voice. |
| `FRICTIONAL.md` | A dated log of problems and decisions while I worked. |
| `FACTCHECK.md` | Every factual claim in the narration, with its source or marked PLAN. |
| `SHOTLIST.md` | How each beat was made, and its audio source. |
| `PROMPTS.md` | Confirms no AI-generated images or video were requested or used. |
| `.gitignore` | Excludes caches, env files and temporary render folders. It lets `decisiontrace-pitch.mp4` through, because the course repo's root `.gitignore` excludes every `*.mp4`. |

**`gate-reports/`: reports from the final `./art final` run**

| File | What it is |
|---|---|
| `gate-V-REPORT.md` | The visual QC report: 26 frames, 0 BLOCKER, 0 MAJOR. |
| `gate-V-contact_sheet.png` | The frames that check looked at. |
| `render-integrity.md` | Streams, duration against the timeline, a full decode check and loudness, plus a check that the review-cut labels are gone. |
| `persona-grep.md` | A search showing no instructor name or persona strings. |
| `decisiontrace-pitch.verified.json` | The toolkit's verification record: the master's SHA-256, its duration, and a hash for every input. |
| `build-state.json` | The toolkit's build status: `ready`. |
| `final-run.log` | Output of the `./art final` run. |

**`build/`: my own build files (none of these are part of the toolkit)**

| Path | What it is |
|---|---|
| `build/scenes.py` | Manim scenes for every beat except B03 and B04. |
| `build/tools/compose_frames.py` | Builds the labelled screenshot frames for B03 and B04 and the two-part B03 clip. |
| `build/tools/phoneme_name.py` | Kokoro narration for B00 and B12, with my name spoken from hand-set IPA. |
| `build/frames/B03a.png`, `B03b.png`, `B04.png` | The composed screenshot frames used in the film. |

**`evidence/alternatives-test/`: the test of NotebookLM and ChatGPT shown in the film**

| Path | What it is |
|---|---|
| `README.md` | Describes the test. |
| `alt-notes.md` | Answer key and grades. |
| `test-pack/` | Six synthetic documents and `questions.txt`. |
| `screenshots/` | Nine unedited screenshots, captured 2026-10-10. |

## How to rebuild the film

1. Clone the Brutalist toolkit, check out commit `ba2d0e0`, run `./setup --install`, and activate its `.venv`.
2. Make a working folder outside the toolkit. Copy in `beat_sheet.json`, `build/scenes.py`,
   `build/tools/`, `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` and three of the screenshots.
3. Generate the narration. B01–B11 use `generate_audio_kokoro.py --only`. B00 and B12 use
   `tools/phoneme_name.py beats --variant E`.
4. Run `tools/compose_frames.py` to make the B03 and B04 frames.
5. Run `./art run <folder>` for a strict review build with every gate, then
   `./art final <folder> --out <folder>/final` for the clean master.

`BUILD-PROMPT.md` has the exact commands, the folder layout, and the versions used.
