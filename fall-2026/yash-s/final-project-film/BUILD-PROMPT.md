# BUILD-PROMPT — how to rebuild the film

## The prompts I gave Claude Code (2026-10-10 to 10-11, summarised)

1. Read the assignment and tell me what we need to do.
2. Target role: AI Developer / DevOps / Cloud Engineer. Suggest projects like the assignment's examples.
3. I have no Claude API budget and do not want to spend money: change the project to document Q&A.
4. Use the GitHub Actions docs. Check my repos (`iyashsaraf/marketpulse-service`, `CSYE6225CloudSpring2k25`) for evidence of skills I already have.
5. Last week's feedback: no static cards, label every constructed screen, and FRICTIONAL.md must be my own words. Do not repeat those mistakes.
6. I added screenshots of the two alternatives answering my three questions to `evidence/`. Use them.
7. Narrate with the Kokoro voice reading my first-person script. Build the film and run the quality gates.

## One prompt that rebuilds it

> Using the Brutalist toolkit's show-tell skill, build a 2–4 minute pitch film from `PROJECT-BRIEF.md`.
> Narrate in my first person with the local Kokoro `am_onyx` voice, and never use the instructor's
> name, persona or credit line. One moving drawing per beat, a few words of label at most, and an
> on-screen "constructed" tag on every sketch. Draw the alternatives beats only from my dated
> screenshots in `evidence/`. Past tense only for what exists. Run every gate and fix what fails.

## Commands

Requirements: a checkout of `brutalist.art` beside this folder, ffmpeg, Node, and a Python with
`manim` and `kokoro-onnx` (here, `/opt/anaconda3/bin/python3`, put first on `PATH`).

```bash
export PATH="/opt/anaconda3/bin:$PATH"
REEL="final-project-film/youtube/actions-docs-qa-pitch"

# 1. beat sheet: narration + visual plan
python3 $REEL/make_sheet.py

# 2. narration audio (local Kokoro, free); durations are written back into beat_sheet.json
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $REEL

# 3. 1.0 s silent tail on the outro, then record its new length as actual_duration_s
ffmpeg -y -i $REEL/mp3/beat-BOUT.mp3 -af "apad=pad_dur=1.0" /tmp/bout.mp3 && mv /tmp/bout.mp3 $REEL/mp3/beat-BOUT.mp3

# 4. scenes.py = the show-tell iso_kit pasted in, plus this film's scenes (already assembled in the reel)

# 5. render with gates F, L, A, W, B and V, then the review cut
./brutalist.art/art run $REEL --height 1080

# 6. GATE T, then the clean master
./brutalist.art/art final $REEL --height 1080 --out final-project-film

# 7. the bookend report (fails on the outro by design; see README)
python3 brutalist.art/runtime/scripts/bookend_check.py $REEL
```
