# Agentic Retrieval Lab — final project pitch film

**Author:** Rithika Sankar Rajeswari (github.com/rithika-sr)
**Course:** INFO 7375, Prompt Engineering for Generative AI. Final-project pitch film.
**Working title:** *Agentic Retrieval Lab*
**Target role:** ML/AI engineering and data science, with a focus on retrieval and RAG.

## The film
- **Final master:** `rithika-final-project-pitch.mp4`. It runs 235.33 s (3:55.3) at 3840×2160, 24 fps, with AAC audio, and is 29.28 MB. sha256: `5dccfe2315b2c59d932ab076d65a65371cd17ea5b2c945feeb22010c5ed24bf5`.
- **The MP4 is committed.** The course repo ignores `*.mp4`, so it was force-added (`git add -f`), because the assignment requires the film in this folder.
- **How it was made:** a show-tell explainer with 15 beats drawn in Manim on the brutalist.art toolkit, using the free pipeline only.
- Narration: Kokoro af_bella synthetic voice, first person; script by Rithika. (Speed 1.04.)
- **Honesty labels:** drawings of things that don't exist yet, and invented examples, carry a CONSTRUCTED label. Real data carries a source tag.

## Contents
| Path | What it is |
|---|---|
| `rithika-final-project-pitch.mp4` | Final 4K master (force-added past the repo's `*.mp4` ignore rule) |
| `PROJECT-BRIEF.md` | Project brief |
| `FRICTIONAL.md` | Rithika's process log (copied as-is) |
| `evidence/beat1_example_951820.json` | The verbatim MS MARCO question and its 4 Claude Haiku rewrites shown in beat 1 |
| `beat_sheet.json` | The exact beat sheet: script, spoken text, pronunciation, measured durations, build stamps |
| `FACTCHECK.md` | Every on-screen and spoken claim, with its evidence (39 rows) |
| `SOURCES.md` | Sources, the synthetic-voice disclosure, contributions and the local toolkit patch note |
| `SHOTLIST.md` | Beat-by-beat pictures, on-screen text and honesty labels |
| `PROMPTS.md` | Generation prompts (none: everything is drawn) |
| `toolkit-local-patch.diff` | Local, uncommitted toolkit edit that moves the beat-1 name stamp inside title-safe |
| `gate-reports/` | Gate F, A, W, L, B (layout audit), V and T, plus the every-0.5 s overlap check |
| `BUILD-PROMPT.md` | Rithika's prompts, verbatim, and the rebuild commands |
| `scenes.py` | Every beat's Manim scene: the show-tell kit, the cartoon cast and the choreography |
| `make_sheet.py` | Generator for `beat_sheet.json` (script, pronunciation, metadata) |
| `word_times.json` | Whisper word timestamps of the narration, used to time the pop-ins |

## How to rebuild
`BUILD-PROMPT.md` §1 has the full commands. In short:
1. Clone brutalist.art at `b21f625`.
2. Create a Python 3.12 venv and run `./setup --install`.
3. Apply `toolkit-local-patch.diff`.
4. Run `./art run <reel> --height 2160`, then `./art final <reel> --height 2160`.

**This folder is self-contained** for rebuilding the visuals: `scenes.py`, `beat_sheet.json` (with the measured durations) and `word_times.json` are all here. Copy them into a reel folder in a course book's `youtube/` folder and run the commands above. The narration MP3s are generated there by `generate_audio_kokoro.py --speed 1.04`; pad `beat-BOUT.mp3` with a 1.0 s silent tail afterwards. Re-running `make_sheet.py` rebuilds the sheet but drops the measured durations, so only run it before re-voicing.

## Disclosure
- **Who did what:** see the contributions in `SOURCES.md`.
- **This README and `BUILD-PROMPT.md`** were drafted by Claude Code.
