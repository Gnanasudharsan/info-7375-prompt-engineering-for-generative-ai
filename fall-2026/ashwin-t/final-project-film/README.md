# Final Project Pitch Film: TraceCase

**Ashwin Thankachan** · INFO 7375 Prompt Engineering for Generative AI · Northeastern · Fall 2026

**Working title:** TraceCase: An Agent That Finds Out Why

**One sentence:** TraceCase will investigate failures in a small Spring Boot service from its logs, traces and
deploy history, and propose one fix that a person must approve before it runs.

**Target role:** software development engineer, backend (new grad).

**Runtime:** 3:53 (232.9 s) · 16:9 · 3840×2160 · H.264 + AAC · narration: a synthetic Kokoro voice (`am_michael`, 0.95 speed) reading my own first-person script. I recorded my voice for the intro and outro, then chose the synthetic voice; see FRICTIONAL.md

**What exists today:** this pitch (brief, beat sheet, film). No TraceCase code exists yet. Every picture of the
product in the film is tagged "constructed" on screen.

**Changed project:** my first pitch, built 2026-10-11, was ProvenDocs. I replaced it on 2026-10-13, before
submitting. [FRICTIONAL.md](FRICTIONAL.md) explains why.

**Video:** `tracecase-pitch.mp4`, in the Canvas zip only. The course repo ignores `.mp4` files.
SHA-256 `6735005146483a17002b25bdf255109923144654642fe7ecbc0913961fb2b4fd`.

## What's in this folder

| File | What it is |
|---|---|
| [PROJECT-BRIEF.md](PROJECT-BRIEF.md) | the seven answers, ending with *exists today* and *will exist* |
| [beat_sheet.json](beat_sheet.json) | narration and visual plan, 18 beats with measured durations |
| [BUILD-PROMPT.md](BUILD-PROMPT.md) | the prompts and commands that rebuild the film |
| [SOURCES.md](SOURCES.md) | what I made, what Claude and Codex contributed, tools, licences, facts read |
| [FRICTIONAL.md](FRICTIONAL.md) | dated log |
| `gate-reports/` | the toolkit's quality-gate reports, fact check, shot list, prompts, and the master's verification record |
| `build/` | the reel sources: `make_sheet.py`, `scene_body.py` (16 Manim drawings), `build_scenes.py`, `finish_audio.py`, `whisper_check.py`, `record_beat.sh` (records your own voice for a beat; not used in the final cut), the pronunciation fix `ashwin.json`, and the toolkit patch in `build/patches/` |

## Quality gates

All from the Brutalist toolkit, run 2026-10-13 on the final version.

| Gate | Result |
|---|---|
| F: fact check (`factcheck_check.py`) | clean, 15 rows resolved, 18/18 beats covered ([report](gate-reports/FACTCHECK.md), [output](gate-reports/FACTCHECK-BOOKEND-CHECKS.md)) |
| Bookends (`bookend_check.py`) | PASS, four bookends correct |
| L: beat-mix lint | clean |
| A: static pre-flight | 16/16 scenes clean ([report](gate-reports/LAYOUT-A-W.md)) |
| W: WCAG contrast, margins, text overlap | 16/16 clean |
| B: layout audit | 16/16 scenes, 0 errors, 0 warnings (after fixes; see FRICTIONAL.md) |
| V: frame-level visual QC | 36 frames, 0 BLOCKER, 0 MAJOR ([report](gate-reports/QC-GATE-V.md)) |
| T: typography | PASS, after fixes to B08 and B07 ([report](gate-reports/QC-GATE-T.md)) |
| Master | `status: ready`; the SHA-256 above matches [the verification record](gate-reports/tracecase-pitch.verified.json) |

One non-blocking toolkit note: its skin lint says the Claude palette prefers a different cold-open card than the
hesitant writer. I kept the hesitant writer because the typed correction ("is it down?" to "why is it down?") is the
idea of the film.

Checks the gates don't do:
- Claude Code reviewed frames sampled every 6 seconds and found the intro correction wasn't firing (fixed).
- A faster-whisper transcript of every beat matched the script.
- I watched the full film myself before submitting.

## Rebuild

See [BUILD-PROMPT.md](BUILD-PROMPT.md). In short: Brutalist at `b21f625` with Python 3.12, apply the patch in
`build/patches/`, copy `build/` outside the course repo, then run `make_sheet.py`, Kokoro audio, `finish_audio.py`,
`align.py`, `build_scenes.py`, `./art run … --height 2160`, and
`./art final … --height 2160`.
