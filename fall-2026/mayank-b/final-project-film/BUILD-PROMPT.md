# BUILD-PROMPT — Source Check for Support AI (pitch film)

## The prompts that drove the build (Claude Code, 2026-10-14)
```
Lets start building 1. [support AI that gives outdated policy answers]. Help me write all the answers;
if you have a problem answering, ask me questions or MCQ, then draft an answer.
```
```
Make a video using brutalist, then we'll refine it, and put it in the Assignment_5 folder.
```
Claude then asked me four multiple-choice questions (target role, stack, existing skills, narration) and
which alternatives I had looked at, and drafted PROJECT-BRIEF.md from my answers.

## Rebuild from this folder (free, local, no keys)
Prereqs: `git clone https://github.com/nikbearbrown/brutalist.art` two levels up (`../../brutalist.art`),
`./setup --install`, `pip install matplotlib`, and the reel-local outro `TcTitleOutro` registered in the
toolkit (see `../../brutalist-changes/toolkit-changes.patch`).

```bash
source ../../brutalist.art/.venv/bin/activate
TK=../../brutalist.art

# 1. beat sheet + scenes
python3 code/make_sheet.py
python3 code/build_scenes.py          # scenes.py = iso_kit + iso_originals_25 + code/scenes_body.py

# 2. audio (the master clock); stdin closed, because the script can hang waiting on it
python3 $TK/runtime/scripts/generate_audio_kokoro.py . < /dev/null
#    pad BIDEA with a 0.8 s lead and BOUT with a 1.0 s tail (ffmpeg -nostdin … concat), then
#    write each ffprobe duration back to actual_duration_s and BDEFS.durationSeconds

# 3. bookends (Remotion)
for b in BIDEA BDEFS BOUT; do python3 $TK/runtime/scripts/remotion_scenes.py . --only $b --force; done

# 4. Gate A pre-audit from a folder holding ONLY scenes.py, then the full run
python3 $TK/runtime/qc/static_scene_check.py scenes.py --class B00_RealCase   # … each class
$TK/art run . --height 1080            # renders scenes, Gates A/B/L/V, review cut
$TK/art final . --height 1080 --out .  # GATE T, then the clean master
```
Never publishes.

## v3 (2026-10-22): the resubmission prompt
```
I want you to go through the following feedbacks and make changes to the video accordingly, the old
submission got me a score of 41/50 [professor's five points, the TA's comments, and the side note:
"In every assignment log what did you do and what did claude do"]
also start using hyperframes for editing videos, it might help
```

## Rebuild v3 (free, local, no keys)
Prereqs as above, plus Node 22+ and HyperFrames (`npm i -D hyperframes@0.7.109`, or point `HYPERFRAMES_BIN` at it), plus the toolkit changes in `../brutalist-changes/`.

```bash
source ../../brutalist.art/.venv/bin/activate; TK=../../brutalist.art
(cd slice && python3 -m pytest -v)                       # the slice: 15 passed
python3 code/make_sheet.py                                # beat sheet v3
python3 $TK/runtime/scripts/generate_audio_kokoro.py . < /dev/null
#   pad BIDEA with 0.8 s lead and BOUT with 1.0 s tail (ffmpeg -nostdin adelay / apad), write durations back
python3 $TK/runtime/scripts/align.py .                    # mp3/words.json: cue and caption timing
python3 code/hf_scenes.py                                 # hyperframes/<BID>/index.html
python3 $TK/runtime/scripts/hyperframes_scenes.py . --force   # -> media/<BID>.mp4 (lint, render, duration check)
for b in BIDEA BOUT; do python3 $TK/runtime/scripts/remotion_scenes.py . --only $b --force; done
$TK/art run . --height 1080                               # review cut + Gate V
$TK/art final . --height 1080 --out .                     # GATE T + verified master, @Mayank on every frame
python3 code/hf_edit.py                                   # caption edit project over the master
hyperframes render hyperframes/_edit --output source-check-pitch-v3.mp4 --fps 24 --quality high
```
