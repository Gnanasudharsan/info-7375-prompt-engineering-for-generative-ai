# BUILD-PROMPT — how to rebuild the Cite-the-Line pitch film

## Prompts

- **Generation prompts:** none. No image, video, music, or voice generation service was used. Drawings are hand-written Manim code; narration is local Kokoro text-to-speech of the text in `beat_sheet.json`.
- **Claude's role:** I built this film in a working conversation with Claude, which explained the assignment, proposed project options, drafted text and code from my decisions, and helped debug the install. The asks were, in order: explain the assignment and keep me in the loop at each decision; help choose a project for a backend engineer; draft the seven answers; write the narration, `make_sheet.py`, the gate paperwork, and the Manim scenes; fix each install error and gate failure as it came up. The full transcript is private and not included, per the assignment. What Claude contributed is itemised in `SOURCES.md`.

## Environment (macOS, Apple Silicon)

```bash
# Python 3.12 env (Manim 0.18 needs Python < 3.13)
conda create -n brutalist python=3.12 -y
conda activate brutalist

# System libraries for ManimPango / pycairo, and ffmpeg for audio and video
brew install cairo pango pkg-config ffmpeg

# Toolkit
git clone https://github.com/nikbearbrown/brutalist.art brutalist-final
cd brutalist-final
git checkout b21f6253a336098f3f55847a9525ae6868ccbdb7   # the toolkit commit this film was built with
./setup --install        # Python deps, Remotion node deps, fonts, Kokoro voice model
```

## Patch the toolkit's outro

`ClaudeTitleOutro.tsx` hard-codes the instructor's handle and a mascot, but the toolkit's bookend gate requires that component. The patch adds two optional props (`handle`, `hideMascot`); unset, the component behaves as before.

```bash
cd brutalist-final
git apply /path/to/src/outro-handle.patch       # or: python3 /path/to/src/patch_outro.py
```

## Build the film

Put the files from `src/`, plus `SOURCES.md`, into a reel folder `<book>/youtube/cite-the-line-pitch/` (show-tell's Gate F needs SOURCES, FACTCHECK, SHOTLIST and PROMPTS beside the sheet), then:

```bash
TK=/path/to/brutalist-final
cd <book>/youtube/cite-the-line-pitch

python3 make_sheet.py                                   # → beat_sheet.json (20 beats)

cd ..                                                   # audio: run from the youtube folder
python3 $TK/runtime/scripts/generate_audio_kokoro.py cite-the-line-pitch
cd cite-the-line-pitch

# outro: 1.0 s silent tail (once only), then write measured lengths into the sheet
ffmpeg -v error -i mp3/beat-BOUT.mp3 -af "apad=pad_dur=1.0" mp3/beat-BOUT.tmp.mp3 && mv mp3/beat-BOUT.tmp.mp3 mp3/beat-BOUT.mp3
python3 sync_durations.py

python3 whisper_check.py                                # optional: pronunciation check

bash check.sh                                           # builds scenes.py = iso_kit.py + scenes_body.py,
                                                        # renders stills, Gate A pre-audit, layout audit

cd ..
$TK/art run   cite-the-line-pitch --height 2160         # Gates A, B, V + review cut
$TK/art final cite-the-line-pitch --height 2160 --out cite-the-line-pitch/exports/landscape   # GATE T + master
```

Output: `cite-the-line-pitch/exports/landscape/cite-the-line-pitch.mp4`.

Notes: `art run` only renders clips that are missing, so after editing a scene move its old `manim/<BID>.mp4` and the reel's `media/videos` cache aside before re-running. Run `check.sh` with bash, not zsh.
