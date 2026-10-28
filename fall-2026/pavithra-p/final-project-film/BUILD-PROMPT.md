# BUILD-PROMPT — how to rebuild the DryRun pitch film

Everything is free and local: Kokoro for the voice, Manim for the drawings, ffmpeg for the cut. No API keys, no accounts, no uploads.

## 1. What you need

- macOS (or Linux) with Python 3.12, `ffmpeg`, and `cairo`, `pkg-config` and `pango` (Manim needs the last three)
- The Brutalist toolkit checked out **beside** this folder, at the commit used for this film:

```bash
git clone https://github.com/nikbearbrown/brutalist.art
```

```bash
git -C brutalist.art checkout b21f625
```

```bash
cd brutalist.art && python3.12 -m venv .venv && . .venv/bin/activate && ./setup --install
```

`./setup --install` installs the Python packages and fetches the Kokoro model into `runtime/models/kokoro/`.

## 2. Rebuild, in order

Run from `brutalist.art/` with the venv active. `REEL` is this folder.

```bash
REEL=../final-project-film
```

**a. Beat sheet** (narration + picture plan) from `make_sheet.py`:

```bash
python3 $REEL/make_sheet.py
```

**b. Narration, the master clock.** Kokoro voice `af_heart`, speed 0.95. This writes `mp3/beat-B*.mp3` and stamps the measured durations into `beat_sheet.json`.

```bash
python3 runtime/scripts/generate_audio_kokoro.py $REEL --speed 0.95
```

**b2. Loudness (v4).** Raises every narration mp3 by 3 dB with a peak limiter, to about −19 LUFS (the toolkit's window is −28 to −18). Durations don't change. Safe to run twice.

```bash
python3 $REEL/boost_audio.py
```

**c. Drawings.** Paste the toolkit's drawing kit and props into `scenes.py`, with `scenes_body.py` after them:

```bash
ART_HOME=$PWD python3 $REEL/build_scenes.py
```

**d. Gates and review cut.** Runs Gates F, L, A, W, B and V, renders every scene at 4K into `manim/`, and compiles a review cut:

```bash
./art run $REEL --height 2160
```

**e. Clean master.** Runs GATE T, then writes the master:

```bash
./art final $REEL --height 2160 --out $REEL/exports
```

**f. Sharpness on the delivered film** (v5). The toolkit's sharpness gate measures the review cut; this runs the same gate, unchanged, on `exports/dryrun-pitch.mp4`:

```bash
python3 $REEL/sharpness_on_final.py runtime/scripts/sharpness_check.py $REEL
```

## 3. The prompts behind it

The film was planned and built in Claude Code sessions from 2026-10-10 to 2026-10-13, and revised for the resubmission on 2026-10-23. These are the main prompts, quoted short:

- "give more unique ideas … score them … which is perfect n all and follows the course guidelines"
- "okay go start now, create one new folder called final project pitch … give an intro of me and then start talking about the project"
- "can u make it more soft the voice" → five local samples → "go with 3" (`af_heart`)
- "first check whether all these changes are really needed or these are … just nitpicks" (GPT's review, checked point by point)
- v4, 2026-10-13: "score it properly" → three rubric gaps; ChatGPT's film review checked against the file; "can you try to remove that [small orange circle]" and "make it a bit more clear about how the throwaway copy is being used" (with a reference image)
- v5, 2026-10-23 (resubmission): "I'm resubmitting the DryRun pitch film (currently 47/50, need 49+, no best-of-two) … Follow the plan in §5 and the rules in §2. Ask before any commit or push." Narration unchanged; B02, B03 and B19 show real evidence, and nine text-only beats get a prop. Then: "add a picture to B14 and B15 the same safe way" (B11 too).

**The real Claude reply in B02** came from a fresh claude.ai chat on 2026-10-11, with the prompt:

> Give me one terminal command to delete all .log files older than 7 days in a folder called logs on Linux.

## 4. What drives what

| File | Role |
|---|---|
| `make_sheet.py` → `beat_sheet.json` | Narration and picture plan for every beat |
| `mp3/` | Measured narration; the durations set every scene's length |
| `scenes_body.py` → `scenes.py` | One Manim scene per beat (B00–B21) |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | Gate F paperwork, required before any render |
| `evidence/` | The real Claude reply (B02 shows the screenshot itself), its test (B03) and the PR #33 test run (B19) |
