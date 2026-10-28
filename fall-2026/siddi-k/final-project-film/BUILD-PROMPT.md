# BUILD-PROMPT — how this film was made, and how to rebuild it

## The prompts (Claude Code, Claude Opus 5.5, 2026-10-14)

1. I pasted the full Canvas description of *Final Project Pitch Film — Show What You Will Build* into Claude Code, with no other instruction.
2. Claude asked four questions before building. My answers:
   - **Project:** "Sponsor-match agent": grow my `data-role-sponsor-match` recipe into an agent loop.
   - **Voice:** "I record my own voice."
   - **Why this project:** "Mix" of new learning and existing skill.
   - **Personal:** "Yes, say I'm on F-1."
3. Same day, after Claude had prepared a recording script: *"I just spoke to the TA he said that I do not need to record my own voice, he said Brutalist is fine, so do that, and let me know what else I should do."* Claude made four Kokoro voice samples. I chose **`af_heart`**, and chose to disclose the synthetic voice **in the README only**, not in the video.
4. *[Any later instructions I gave: add them here with the date.]*

No prompt asked for invented results. Claude was told by the assignment text to keep past tense for what exists, label constructed material, and not use the instructor's persona.

## Rebuild from scratch (Windows 11 + Git Bash; macOS/Linux the same without the shim)

```bash
# 1. toolkit (free local pipeline; README: ./setup checks deps)
git clone https://github.com/nikbearbrown/brutalist.art && git -C brutalist.art checkout 519fcbb
cd brutalist.art && python -m venv .venv && .venv/Scripts/python -m pip install -r requirements.txt && (cd runtime/remotion && npm install) && cd ..
# Windows only: apply the two local patches (npx path; drawtext path + ART_NO_TIMECODE)
git -C brutalist.art apply ../final-project-film/evidence/brutalist-local-windows-patches-2026-10-14.patch
# Put ffmpeg/ffprobe on PATH and make `python3` resolve to the venv (I use brutalist.art/.shim/env.sh)

# 2. the film (this folder sits next to brutalist.art)
cd final-project-film
python make_sheet.py        # beat_sheet.json (narration, shots, honesty tags); keeps measured audio fields
python voice.py --speed 0.95                    # Kokoro af_heart -> mp3/beat-<BID>.mp3 (+ pronunciation.json)
python finish_audio.py --src mp3 --prefix beat- # -> audio/<BID>.wav: trim, -20 LUFS, pads; writes durations
python pronunciation_check.py                   # whisper transcript vs script -> reports/PRONUNCIATION-CHECK.md
python word_clock.py        # mp3/words.json word timings (faster-whisper via ffmpeg decode)
python assemble_scenes.py   # scenes.py = show-tell kit + 15 original props + scene_body.py

# 3. render + gates (Gate F paperwork, L, SHAPE, A, W, B per scene, V on the review cut)
ART_NO_TIMECODE=1 ../brutalist.art/art run . --height 2160
# 4. Gate T, then the verified master (compile.py checks duration, decode, audio, writes a .verified.json receipt)
../brutalist.art/art final . --height 2160 --out exports
# 5. publish-hardening checks the toolkit runs at staging (run by hand; no upload)
python ../brutalist.art/runtime/scripts/master_check.py .
python ../brutalist.art/runtime/scripts/loudness_check.py .
python ../brutalist.art/runtime/scripts/sharpness_check.py .
```

Exact outputs, durations and the master's SHA-256 are in README.md and `reports/`.
