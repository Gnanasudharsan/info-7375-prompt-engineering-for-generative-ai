# OPT Countdown — Final Project Pitch Film

**Name:** Saloni Mathure · INFO 7375, SEC 01, Fall 2026
**Working title:** OPT Countdown
**Target role:** new-grad software engineer / data analyst
**Runtime:** 3:45 (225.25 s), 13 beats, 3840×2160, narrated by me with the local Kokoro voice `af_heart`

## The pitch in one sentence

OPT Countdown will be a command-line tool that takes an international student's OPT dates and a list of job postings, and sorts each posting into apply, network first, skip, or blocked, using the employer's public H-1B record, whether the posting is still live, and whether the employer can hire before the 90-day unemployment limit runs out.

**What exists today:** a prototype recipe in the Reallocation Engine (PR nikbearbrown/the-reallocation-engine#48, commit `81d0161`). It has 12 tests, which I re-ran on 2026-10-13 (12/12 pass), and a worked run on 8 postings for a fictional student. **Everything else is proposed.** The two lists are at the end of `PROJECT-BRIEF.md`.

## Contents

| File | What it is |
|---|---|
| `video.mp4` | the rendered film (12 MB). **Canvas zip only:** the course repo's `.gitignore` excludes all `.mp4`/`.mp3` files, so the GitHub copy rebuilds it from the files below |
| `PROJECT-BRIEF.md` | the seven answers, ending with *exists today* and *will exist* |
| `beat_sheet.json` | narration and visual plan (a copy of `reel/beat_sheet.json`, which the build ran from) |
| `BUILD-PROMPT.md` | the commands and prompts that rebuild the film |
| `SOURCES.md` | what I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | dated log of what broke and what changed |
| `evidence/rerun-2026-10-13.txt` | the real prototype output shown in the film |
| `reel/make_sheet.py` | the narration source; it writes the beat sheet |
| `reel/scenes.py` | the twelve drawn Manim scenes (show-tell kit pasted at the top) |
| `reel/FACTCHECK.md` | every claim in the film, with verdict and source |
| `reel/SHOTLIST.md`, `reel/PROMPTS.md` | work order, and a note that nothing was AI-generated |

## Gate reports (Brutalist `cd4bf20`)

| Gate | Result | Report |
|---|---|---|
| Gate A static pre-flight | 12/12 clean | in the `art run` output |
| Layout audit | clean | `reel/layout_audit.md` |
| Gate V / render integrity (`final_frame_check.py`) | BLOCKER 0, MAJOR 0 (failed once, fixed; see FRICTIONAL) | `reel/_qc/REPORT.md`, `reel/_qc/contact_sheet.png` |
| GATE T type check | PASS, 13/13 | `reel/TYPECHECK.md` |
| Verified master | `ready`, sha256 matches `video.mp4` | `reel/_qc/opt-countdown-pitch.verified.json` |
| `bookend_check.py` (optional) | fails on purpose: my own outro replaces the stock one, which hardcodes the instructor's handle | `reel/bookend_check.txt` |

## How to rebuild

```bash
git clone https://github.com/nikbearbrown/brutalist.art && cd brutalist.art && git checkout cd4bf20
python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
nvm use 20 && ./setup --install
python3 runtime/scripts/generate_audio_kokoro.py <this folder>/reel
# pad BOUT with 1.0 s of silence (BUILD-PROMPT.md step 3), then:
./art run   <this folder>/reel --height 2160
./art final <this folder>/reel --height 2160 --out <this folder>/reel/exports/landscape
```

Full steps, including re-checking the prototype's numbers, are in `BUILD-PROMPT.md`.

## Honesty notes

- Beats that show things that don't exist yet (B00, B06, B07) carry the on-screen tag **constructed sketch**. The beat with real output (B01) carries **real run · 2026-10-13**.
- The student in the prototype run is fictional. No résumé, contacts, tracker or transcript is included. Company names are public employers from the prototype's public data.
- No Claude response appears in the film. Claude Code's contributions are listed in `SOURCES.md`, and the film says aloud that Claude Code did most of the typing on the prototype.
