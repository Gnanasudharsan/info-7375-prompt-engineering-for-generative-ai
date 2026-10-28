## Executive summary

This is a short video about a screening tool built for a fictional international student, Sasha Jones, who needs an entry-level data scientist job that sponsors a work visa. In under four minutes it shows:
- what she can't see when she looks at a job page;
- how the tool checks postings in a fixed order and refuses to score what it can't confirm;
- the false recommendation it caught;
- the two bugs a person found by opening pages by hand, and the fixes;
- an honest caveat: the fixes were checked on the same postings that person had already reviewed.

Every number on screen is traced to a project file.

# A Mode for the Reallocation Engine — mode video

- **Author:** Rithika Sankar Rajeswari · INFO 7375 · 2026-10-21
- **Final file:** `rithika-reallocation-mode-video.mp4`.
  - **Runtime:** 222.875 s (3:42.9), measured with `ffprobe -show_entries format=duration` on the master, not taken from the beat sheet.
  - **Format:** 3840×2160, 24 fps, H.264 + AAC, 17.9 MB.
  - **sha256:** `95424b95ffcfb3275ab2486fa408b6dd42b4aa33bb110262f8f0563581a4a0ee`.
- **Narration:** Kokoro `af_bella` synthetic voice in the first person, reading my 8-beat script verbatim. It is not a recording of me. It was voiced per sentence at speed 0.962 with 1.35–1.4 s pauses to reach the 3:40–3:55 target (see `BUILD-PROMPT.md` §2).
- **Toolkit:** brutalist.art `show-tell` skill (local checkout `brutalist-v2`, commit `b21f625`), drawn in Manim, free local pipeline.

## Beats

| Beat | Audio s | Scene | What it shows |
|---|---|---|---|
| B01 | 33.07 | `B01_Persona` | Sasha's ID card (fictional persona), her visa timeline, aggregator sites |
| B02 | 25.35 | `B02_CantSee` | Three things she can't see; the 90-day clock |
| B03 | 35.55 | `B03_Gates` | G1 → G2 → Level → G3 → G4, "gates, not votes", exits HELD / CLOSED / OVER-LEVEL |
| B04 | 26.16 | `B04_Removed` | The Built In page removed Jun 11, 2025 vs the checker's "active"; v0.1 Apply ✗ → HELD ✓ |
| B05 | 22.27 | `B05_Bugs` | The real Airbnb redirect chain; Nextdoor's visible Apply button vs "uncertain" |
| B06 | 39.76 | `B06_Fixes` | Run 2 fixes, Airbnb → CLOSED, Nextdoor → live, Senior roles → OVER-LEVEL, agreement 3/5 → 2/5 → 4/5 |
| B07 | 27.09 | `B07_Caveats` | Not a held-out test; three remaining limits |
| BOUT | 13.37 | `BOUT_Status` | Status: DRAFT · ran live 3× · typed TODOs open; Next: held-out test |

## Checks on the final master

- **Gates:**
  - F: clean, 41 rows.
  - L: clean.
  - A: 8/8 clean.
  - W: 7/7 clean.
  - B: `--curve-strict`, 8/8 CLEAN.
  - V: 0 blockers, 0 majors.
  - T: PASS.

  Reports are in `gate-reports/`.
- **Silence** (`silencedetect noise=-35dB:d=0.5`): 44 silences. 15 are slightly over 1.5 s, at 1.50–1.59 s; 7 of those are between beats and 8 inside beats. The full list is in `gate-reports/silencedetect-35dB-0.5s.txt`.
- **Frames:**
  - every 12 s on the master: `gate-reports/frames-every-12s.jpg`;
  - the last frame of each beat: `gate-reports/frames-beat-ends.jpg`.

## Files

| File | What it is |
|---|---|
| `rithika-reallocation-mode-video.mp4` | Final 4K master |
| `beat_sheet.json` | The beat sheet: verbatim script, spoken text, measured durations, build stamps |
| `make_sheet.py` | Generator for `beat_sheet.json` (script, audio-only respellings, metadata) |
| `voice_sentences.py` | Per-sentence narration with the toolkit's own Kokoro helpers |
| `whisper_words.py` / `word_times.json` | Word timestamps (and pronunciation check) used to time every label |
| `scenes.py` | The eight Manim scenes (drawing kit copied from my final-project film) |
| `FACTCHECK.md` | Every spoken claim and on-screen number, with its source file (41 rows) |
| `SHOTLIST.md` / `PROMPTS.md` | What each beat draws · generation prompts (none) |
| `SOURCES.md` | Evidence files, licences, synthetic-voice disclosure, contributions |
| `BUILD-PROMPT.md` | My prompts, the measured runtime trials, and the rebuild commands |
| `FRICTIONAL.md` | What went wrong and what was decided |
| `gate-reports/` | Gates F, L, A, W, B, V, T, silencedetect and frame contact sheets |

## How to rebuild
See `BUILD-PROMPT.md` §1. In short:
1. Clone brutalist.art at `b21f625` into `~/brutalist-v2` and create a Python 3.12 venv.
2. Run `./setup --install`.
3. Copy this folder's sources into a reel folder.
4. Run `make_sheet.py`, then `voice_sentences.py --speed 0.962 --sentence-pause 1.35`, then `whisper_words.py`.
5. Run `./art run <reel> --height 2160`, then `./art final <reel> --height 2160`.

## Disclosure
Claude Code built the reel, ran the checks and drafted this README, `BUILD-PROMPT.md`, `SOURCES.md` and `FRICTIONAL.md`. I wrote the script and the visual brief, and made the runtime decision. Contributions are in `SOURCES.md`.
