# BUILD-PROMPT — how to rebuild the film

## Executive summary

This file lists the exact commands, settings and local toolkit changes that turned `beat_sheet.json` into `is-funded-sponsor-triage-pitch.mp4`. It also records the prompts I gave the AI assistant. Everything runs locally and free: Brutalist (show-tell skill), Manim, Remotion, and the Kokoro voice. No generation service, API key or upload was used.

## Environment (as built, 2026-10-13)

- Windows 11, Git Bash, Python 3.14.2, Node 24.11.1, ffmpeg 9.0.2.
- Brutalist: fresh clone of `https://github.com/nikbearbrown/brutalist.art` at commit `519fcbb`, in `C:\Users\zyud0\brutalist-film`.
- Python deps: `python3 -m pip install --user -r requirements.txt` (Manim 0.20.1, ManimPango 0.6.1, kokoro-onnx 0.4.7).
- Remotion deps: `cd runtime/remotion && npm install`.
- Kokoro model files copied into `runtime/models/kokoro/` from an earlier checkout (same release files the setup script downloads).

## Windows settings used for every command

```bash
export PYTHONUTF8=1                       # toolkit reads JSON with the default codec otherwise (UnicodeDecodeError)
export ART_NO_DRAWTEXT=1                  # ffmpeg drawtext cannot parse a C:\ font path (review-cut timecode only)
export PATH="$APPDATA/Python/Python314/Scripts:$PATH"   # where pip --user put manim.exe
```

## Local toolkit change (one new component, nothing edited in shared logic)

- Added `runtime/remotion/src/scenes/StudentTitleOutro.tsx`: a copy of `ClaudeTitleOutro.tsx` with `handle` read from props (default `@yudanzhou`) and the mascot block removed. The stock component hardcodes `const HANDLE = '@NikBearBrown'`, which the assignment forbids.
- Registered it in `runtime/remotion/src/Root.tsx` with one import line and one `<Composition id="StudentTitleOutro" …/>` block beside `ClaudeTitleOutro`.

## Reel folder

`brutalist-film/youtube/is-funded-sponsor-triage-pitch/` holds `beat_sheet.json`, `scenes.py` (= `skills/make/show-tell/templates/iso_kit.py` + `scene_body.py`), `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` and `SOURCES.md`.

## Commands, in order

```bash
cd brutalist-film
R=youtube/is-funded-sponsor-triage-pitch

# 1. narration (Kokoro af_heart, local)
python3 runtime/scripts/generate_audio_kokoro.py $R
#    pad the outro with a 1.0 s silent tail and write the duration back
ffmpeg -y -i $R/mp3/beat-BOUT.mp3 -af "apad=pad_dur=1.0" -c:a libmp3lame -q:a 2 $R/mp3/beat-BOUT.pad.mp3 && mv $R/mp3/beat-BOUT.pad.mp3 $R/mp3/beat-BOUT.mp3

# 2. stills first (low-res last frame of each scene) for a contact-sheet check
python3 -m manim -ql -s --disable_caching $R/scenes.py B01_Trays     # …repeat per scene

# 3. Remotion bookends (BIDEA, BDEFS, BOUT). On Windows the toolkit's subprocess call to
#    `npx` needs npx.cmd, so the unchanged toolkit script is run through a 10-line wrapper
#    that resolves `npx` with shutil.which before calling subprocess.run:
PYTHONPATH=runtime/scripts python3 npx_shim_run.py runtime/scripts/remotion_scenes.py $R

# 4. Gates A, W, B, layout audit, Gate V and the review cut
./art run $R --height 1080

# 5. Gate T and the clean master
./art final $R --height 1080 --out $R/exports/landscape
```

## Prompts I gave the AI assistant (Claude Code), summarized

- "指导我做一下这个作业，一步一步来" — then my answers: deadline 14th, no project idea, target role DA, AI voice.
- Approved the five narration cuts; asked for the run date as a B02 label; asked to replace the instructor-handle outro with our own Remotion component so `bookend_check` passes honestly; "Don't change any narration text beyond the five approved cuts."
- The AI wrote `scene_body.py` (11 Manim scenes), `StudentTitleOutro.tsx`, the reel's QC files and drafts of these documents; I approved every narration sentence.
