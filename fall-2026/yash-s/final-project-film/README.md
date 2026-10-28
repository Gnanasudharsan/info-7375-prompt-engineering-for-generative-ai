# Final Project Pitch Film — Actions Docs Q&A

**Yash Saraf** · INFO 7375 · Fall 2026

- **Working title:** actions-docs-qa — a source-grounded Q&A tool for the GitHub Actions docs
- **Target role:** AI Developer / DevOps / Cloud Engineer
- **Runtime:** 2 min 59.5 s (179.5 s), 1920×1080, 24 fps
- **Film:** `actions-docs-qa-pitch.mp4` · SHA-256 `7e9c5ba698d4ba83eaf69a0d9f2bb32e7f3a040ad6a5fe1d97172a79de6a65fe`
  (the course repo's `.gitignore` keeps MP4 and MP3 files out of Git, so the film and the narration
  audio are in the Canvas zip; the hash shows the two copies match)

This is a pitch, not a build: nothing in the project exists yet. Every drawn beat carries an
on-screen "constructed" tag; the two beats about the alternatives (B04, B05) are drawn from my
dated screenshots in `evidence/` (2026-10-11).

## What is in this folder

| File | What it is |
|---|---|
| `actions-docs-qa-pitch.mp4` | the rendered film |
| `PROJECT-BRIEF.md` | the seven answers, with "Exists today" and "Will exist" lists |
| `beat_sheet.json` | narration and visual plan, one entry per beat |
| `BUILD-PROMPT.md` | the prompts and commands that rebuild the film |
| `SOURCES.md` | what I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | my dated log, written as I worked |
| `gate-reports/` | the Brutalist quality-gate reports |
| `evidence/` | six dated screenshots of the alternatives I tried |
| `youtube/actions-docs-qa-pitch/` | the build folder: `make_sheet.py`, `scenes.py`, audio, paperwork |

## How to rebuild the film

See `BUILD-PROMPT.md` for every command. In short, from the folder holding both this folder and a
`brutalist.art` checkout, with a Python that has `manim` and `kokoro-onnx` first on `PATH`:

```bash
python3 final-project-film/youtube/actions-docs-qa-pitch/make_sheet.py
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py final-project-film/youtube/actions-docs-qa-pitch
./brutalist.art/art run   final-project-film/youtube/actions-docs-qa-pitch --height 1080
./brutalist.art/art final final-project-film/youtube/actions-docs-qa-pitch --height 1080 --out final-project-film
```

Free pipeline only: local Kokoro voice, Manim and Remotion. No API key, no paid service, no upload.

## Gate results

Every Brutalist gate passed before the master was cut: F, L, A, W, B, V, GATE T and the bookend
check. GATE T and the bookend check failed on their first run and were fixed. The details, and
two advisory notes that remain on purpose, are in `gate-reports/README.md`.
