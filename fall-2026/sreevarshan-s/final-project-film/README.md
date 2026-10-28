# Record Beats AI: A Sponsorship Job Finder That Checks Its Own Answers

**Sreevarshan Sathiyamurthy** · INFO 7375 final project film · target role: **ML / AI engineer**

| | |
|---|---|
| Film | `Sathiyamurthy_Sreevarshan_RecordBeatsAI.mp4` (the 4K master) |
| Runtime | 3:58.6 (238.6 s) |
| Format | 3840×2160, 24 fps, H.264 / AAC, 12.6 MB |
| Voice | **synthetic**: Kokoro TTS, voice `am_michael`, `--speed 1.09`, run locally. Disclosed on screen in the first beat and spoken in the outro. |
| Style | show-tell (one drawn isometric picture per beat), built with the brutalist.art toolkit |

The film pitches a command-line pipeline, built first as my INFO 7375 Assignment 2 prototype (October 2026). It shows an international new graduate on OPT which companies have actually sponsored people at their level, and it refuses to call a job "open" unless a record backs it. Everything said in the past tense is checked against the project repo (see `CLAIMS.md` and `FACTCHECK.md`). Everything not yet built is said with "will".

## What is in this folder

| File | What it is |
|---|---|
| `Sathiyamurthy_Sreevarshan_RecordBeatsAI.mp4` | the film (4K master; passes the toolkit's master check) |
| `PROJECT-BRIEF.md` | my project brief |
| `beat_sheet.json` | the film's beat sheet as built (narration, timings, shots) |
| `make_sheet.py` | generates `beat_sheet.json` |
| `scenes.py` | the Manim drawings, one scene per body beat |
| `finish_audio.py` | pads the bookends and writes measured audio durations back into the sheet |
| `BUILD-PROMPT.md` | the instructions and commands that built the film, in order |
| `SOURCES.md` | sources, authorship (what Claude drafted, what I did), evidence index, third-party licences |
| `CLAIMS.md` | every narration sentence tagged SHOWN / WILL / CONSTRUCTED / EXTERNAL / FRAMING with its proof |
| `FACTCHECK.md` | per-claim verdicts (PASS / CORRECTED / EXEMPT) |
| `SHOTLIST.md` | the picture and labels for each beat |
| `FRICTIONAL.md` | my friction log for this film |
| `evidence/` | repo files and my own screenshots that back the claims (dated) |
| `gate-reports/` | every quality-gate report and the build logs from the final build |

## How to rebuild the film

Needs macOS or Linux with `git`, `ffmpeg`, Node ≥ 20, and Python 3.11. The commands below assume the toolkit and this folder sit side by side; adjust paths as needed.

1. **Clone the toolkit at the exact commit used.**
   ```bash
   git clone https://github.com/nikbearbrown/brutalist.art BrutFilm
   cd BrutFilm && git checkout b21f6253a336098f3f55847a9525ae6868ccbdb7
   ```
2. **Create a fresh Python 3.11 virtual environment and run setup.** Setup installs the Python and Remotion deps, fonts, and downloads the free Kokoro voice model (~340 MB).
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ./setup --install
   ```
   Setup modifies the tracked `runtime/remotion/package-lock.json`. Restore it with `git checkout -- runtime/remotion/package-lock.json`; the installed modules are unaffected.
3. **Make a film folder** (the toolkit builds into `<book>/youtube/<slug>/`, never inside itself) and copy in `make_sheet.py`, `scenes.py`, `finish_audio.py`, `SOURCES.md`, `CLAIMS.md`, `FACTCHECK.md`, `SHOTLIST.md`, and `PROMPTS.md` (from `BUILD-PROMPT.md`). Put `PROJECT-BRIEF.md` two levels up.
   ```bash
   mkdir -p final-project-film/youtube/show-tell-reallocation-recipe-pitch
   ```
4. **Generate the beat sheet.**
   ```bash
   cd final-project-film/youtube/show-tell-reallocation-recipe-pitch
   python3 make_sheet.py
   ```
5. **Generate the narration at speed 1.09**, then pad the bookends and write the measured durations back. The speed is a command-line flag of the audio script; the sheet only records it as `kokoro_speed`.
   ```bash
   python3 ../../../BrutFilm/runtime/scripts/generate_audio_kokoro.py . --speed 1.09
   python3 finish_audio.py
   ```
6. **Build the review cut.** This runs Gates F, L, SHAPE, A, W, B and V. Manim renders at 4K.
   ```bash
   ../../../BrutFilm/art run "$PWD" --height 1080
   ```
7. **Build the 4K master.** This runs Gate T, then exports the verified master.
   ```bash
   ../../../BrutFilm/art final "$PWD" --height 2160 --out "$PWD/exports/landscape-4k"
   ```
8. **Run the remaining gates** on the master; the exact list is in `BUILD-PROMPT.md`.

`make_sheet.py` wipes the measured audio fields and build stamps it writes into the sheet. Re-run `finish_audio.py` after it, and before `art run` or `art final`.

## Quality gates

The assignment asks for a render-integrity check. **The toolkit at this commit has no gate named render-integrity.** Instead, every film-level gate it ships was run on the final build. All of them pass on the 4K master:

- **Pre-render:** Gate F (paperwork), Gate L (beat lint), Gate SHAPE, Gate A (static scene check), Gate W (WCAG contrast and margins).
- **Render and type:** Gate B (Manim layout audit), Gate V (frame-level visual QC), Gate T (type check).
- **Master file:** master check (4K spec), loudness (−23.99 LUFS), sharpness, frame check.
- **Structure and paperwork:** bookend check, fact-check gate, content check, lane check, banned-card check, placeholder check, math-layout check, film audit.
- **Not applicable:** the subtitle check skips because the film has no captions.

The reports are in `gate-reports/`. The two toolkit-wide component checks audit every component in the toolkit, not this film; their outputs are kept separately in `gate-reports/toolkit-wide/`.

## Known toolkit issues at commit `b21f625`

- **`./art doctor` (`./setup`) exits 1** before printing its readiness table. Its ElevenLabs guard flags ten files that ship with the toolkit itself, under `youtube/brutalist/…`. The dependency installs themselves succeed.
- **`./art smoke` fails** with `metadata.slug must be a filename, not a path`. The smoke fixture's own slug `_smoke` starts with an underscore, which `runtime/scripts/build_safety.py` rejects. Running the same smoke steps on a copy with the slug changed renders a real video, so the pipeline works.
- **`ClaudeTitleOutro` hardcodes another channel's handle,** so this film's outro uses a `ShowTellCard` sign-off instead.

No toolkit file was changed to work around any of these.

## Notes

- **The voice is synthetic** (Kokoro `am_michael`), not my own recording. My name is respelled in the narration text only, as `Shreevarshun Saa-thee-ya-moorthy`, so Kokoro pronounces it. Every on-screen use keeps the real spelling.
- **The fictional persona `meera-krishnan`** appears only as a file stamped CONSTRUCTED. No real personal data is used.
- **No chat transcripts are included.** The assignment forbids private conversation transcripts.
