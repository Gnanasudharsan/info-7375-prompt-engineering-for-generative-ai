# DryRun — Final Project Pitch Film

**Name:** Pavithra Prasad
**Course:** INFO 7375, Prompt Engineering for Generative AI (Fall 2026)
**Working title:** DryRun: see what an AI's command will do, before it touches your files
**Target role:** software engineer, backend / platform (new grad, December 2026)
**Film:** `dryrun-pitch.mp4` (resubmission, v5) · **Runtime:** 3:53 (232.9 s) · 3840×2160 · 24 fps
**SHA-256 of the film:** `1b69f5f1a94d246e4314589df811fda315b2959b17c7f11ed1cb003ce7ac92a9`

> **Where the video is:** the course repo's `.gitignore` keeps `.mp4` and `.mp3` files out of Git, so the film is only in the Canvas zip (`Prasad_Pavithra_INFO7375_FinalProjectFilm.zip`). Everything else in the zip matches this folder; the SHA-256 above matches the zip's film.

> **This is a pitch, not a build.** Nothing of DryRun exists yet. Everything the film says DryRun does is what I **will** build. The only real artifacts are a Claude reply (2026-10-11), my test of its preview (re-run 2026-10-13) and the PR #33 test run behind "skills I already have" (2026-10-23), all in `evidence/`.

> **Resubmission (v5).** After the TA feedback (P6 "shown, not asserted" and Frictional), the narration is unchanged word for word and the runtime is the same. On screen, B02 now shows the real Claude screenshot, B03 my own Terminal lines, B19 the real PR #33 test output, and the nine text-only beats (B01, B11, B12, B14–B18, B20) have a picture that carries the idea. `FRICTIONAL.md` was rewritten to the five-row rubric. Every gate was re-run (`reports/`).

## What's in this folder

| File | What it is |
|---|---|
| `dryrun-pitch.mp4` | The film (Canvas zip only, see above) |
| [`PROJECT-BRIEF.md`](PROJECT-BRIEF.md) | The seven answers in text, ending with "exists today" and "will exist" |
| [`beat_sheet.json`](beat_sheet.json) | Narration and picture plan for every beat (from `make_sheet.py`) |
| [`BUILD-PROMPT.md`](BUILD-PROMPT.md) | The prompts and commands that rebuild the film |
| [`SOURCES.md`](SOURCES.md) | What I used, what I made, what Claude contributed |
| [`FRICTIONAL.md`](FRICTIONAL.md) | Dated log of how this was made |
| `scenes_body.py`, `build_scenes.py` | The drawings (one Manim scene per beat) |
| `boost_audio.py` | Raises the narration by 3 dB (about −19 LUFS) before rendering |
| `sharpness_on_final.py` | Runs the toolkit's sharpness gate on the delivered film instead of the review cut |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | The toolkit's required paperwork |
| [`reports/`](reports/) | The toolkit's gate reports: L, A, W, B, V, T, loudness, master check, sharpness. `sharpness.md` names `dryrun-pitch-slate.mp4` because the toolkit's sharpness gate always measures the review cut (the same 22 clips); `sharpness-final-film.md` is the same gate run on the delivered film. `master-check.md` notes a skipped duration sub-check: its file (`clock_check.py`) is missing from the toolkit at `b21f625`. The film's 232.9 s is within 0.5 s of the narration total (232.4 s). |
| [`evidence/`](evidence/) | The real Claude reply (screenshot), the preview test, and the PR #33 test run |

## Rebuild it

Full steps in [`BUILD-PROMPT.md`](BUILD-PROMPT.md). In short, from the Brutalist toolkit (commit `b21f625`) checked out beside this folder, with its venv active:

```bash
python3 ../final-project-film/make_sheet.py && python3 runtime/scripts/generate_audio_kokoro.py ../final-project-film --speed 0.95 && python3 ../final-project-film/boost_audio.py
```

```bash
ART_HOME=$PWD python3 ../final-project-film/build_scenes.py && ./art run ../final-project-film --height 2160
```

```bash
./art final ../final-project-film --height 2160 --out ../final-project-film/exports
```

## Narration and credits

- The narration is a synthetic voice (Kokoro `af_heart`, run locally) reading my script.
- Built with help from Claude Code; see `SOURCES.md`.
