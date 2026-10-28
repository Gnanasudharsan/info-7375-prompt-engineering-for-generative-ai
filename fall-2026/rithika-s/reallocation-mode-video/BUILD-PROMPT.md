# BUILD-PROMPT — A Mode for the Reallocation Engine (mode video)

**Author:** Rithika Sankar Rajeswari. Claude Code drafted this file.

This file holds Rithika's prompt and the commands that rebuild the film from source. **Inputs:**
- `make_sheet.py` → `beat_sheet.json` (her script, verbatim);
- `voice_sentences.py` (per-sentence narration);
- `whisper_words.py` → `word_times.json`;
- `scenes.py` (eight Manim scenes);
- `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `SOURCES.md`.

---

## 1. Rebuild the film from source (free pipeline: no keys, no paid services)

```bash
# 1. toolkit — the working checkout is ~/brutalist-v2 (NOT ~/Downloads/brutalist, the old broken one)
git clone https://github.com/nikbearbrown/brutalist.art ~/brutalist-v2
cd ~/brutalist-v2 && git checkout b21f625
/opt/homebrew/bin/python3.12 -m venv .venv && source .venv/bin/activate
./setup --install                      # pip deps, Remotion node deps, fonts, Kokoro model
export ART_HOME=~/brutalist-v2

# 2. reel folder (the course repo's youtube/ folder; renders and caches stay here, untracked)
R=~/info-7375-prompt-engineering-for-generative-ai/youtube/rithika-reallocation-mode-video

# 3. beat sheet: Rithika's 8 beats verbatim (script_text) + audio-only respellings (narration_text)
python3 $R/make_sheet.py

# 4. narration, voiced PER SENTENCE (see §2), then the measured durations are written back
python3 $R/voice_sentences.py --speed 0.962 --sentence-pause 1.35

# 5. word timestamps + pronunciation check (faster-whisper base, ffmpeg-decoded audio)
cd $R && python3 whisper_words.py && cd $ART_HOME

# 6. review cut (Gates F, L, A, W, B, V) and the clean master (GATE T, then compile)
./art run   $R --height 2160
./art final $R --height 2160 --out $R/exports/landscape

# 7. the real runtime — measured on the render, never from the beat sheet
ffprobe -v error -show_entries format=duration -of csv=p=0 $R/exports/landscape/<slug>.mp4
```

Gate B can be run on its own before the slow 4K render:

```bash
python3 runtime/qc/manim_layout_audit.py $R/scenes.py --class <Scene> --curve-strict
python3 runtime/qc/static_scene_check.py $R/scenes.py --class <Scene>      # Gate A
```

## 2. Per-sentence voicing (a documented deviation from the toolkit's audio step)

The toolkit voices each beat in one call (`generate_audio_kokoro.py`). This film does not, and here is why.

**Measured, not estimated:**

| Setting | Narration length |
|---|---|
| One call per beat at speed 1.04 | 170.48 s (2:50.5) |
| Per sentence, speed 1.0, 1.0 s pauses | 210.84 s (3:30.8) |
| Per sentence, speed 0.962, 1.2 s pauses | 218.58 s (3:38.6) |
| Per sentence, speed 0.962, 1.35 s pauses (**used**) | 222.70 s (3:42.7) |

**Rithika's decision (2026-10-21):** sentence pauses rather than long silences between beats:
- about 1.0 s after each sentence;
- up to 1.5 s on the terminal-text beats (4, 5, 6) so the text is readable;
- about 1.5 s between beats;
- a target of 3:40–3:55, hard limit under 4:00;
- a voice speed change of at most 1.04×.

To reach the 3:40 floor without changing a word, the sentence pause went to 1.35 s and the speed to 0.962 (a 1.0395× slow-down, inside the limit). Every pause stays under 1.5 s, so no silence between words exceeds the 1.5 s gap check.

`voice_sentences.py` imports the toolkit's own helpers (`load_engine`, `normalize_for_tts`, `lang_for`, `write_mp3`, `measure` from `runtime/scripts/generate_audio_kokoro.py`). For each sentence it:
1. voices the sentence with Kokoro `af_bella`;
2. trims its edge silence to 0.04 s, so each pause is exactly the planned length;
3. joins the sentences with silence;
4. adds a beat tail of 1.4 s (1.0 s on the outro).

It then writes `mp3/beat-<ID>.mp3`, `mp3/timings.json`, and `actual_duration_s` plus `audio_file` in `beat_sheet.json`, from one measurement of each file. `mp3/sentences.json` records every sentence's speech length.

**Pronunciation.** Whisper heard "Risica", "in-stack art", "airbim", "repose" and "to DOS". The audio-only respellings in `make_sheet.py` fixed most of these. "repo's" still transcribes as "repose", because Whisper cannot hear the stress difference. Listen to beat 4.

## 3. What the build produced (2026-10-21)

- **Master:** `exports/landscape/rithika-reallocation-mode-video.mp4`, 3840×2160, 24 fps, H.264 + AAC, 17.9 MB, sha256 `95424b95ffcfb3275ab2486fa408b6dd42b4aa33bb110262f8f0563581a4a0ee`.
- **Runtime (ffprobe on the master):** 222.875 s = 3:42.9.
- **Gates:**
  - Gate F: clean, 41 rows.
  - Gate L: clean.
  - Gate A: 8/8 clean.
  - Gate W: 7/7 clean (it skips the outro).
  - Gate B (`--curve-strict`): 8/8 CLEAN, 221 snapshots.
  - Gate V: 0 blockers, 0 majors.
  - Gate T: PASS.

  Reports are in `gate-reports/`.
- **Changes Gate T forced:**
  - outlines around text changed from terracotta to kraft-deep;
  - the crossed-out eye replaced by a closed eye;
  - lit gate beams changed from terracotta to dark ink.

  `./art run` skips beats whose `manim/<B>.mp4` already exists, so stale clips were moved into `_scratch/` before each re-render.

## 4. The prompts, verbatim

### Video step (2026-10-21)

> Video step. Do not touch the reallocation-engine repo except to READ transcripts and outputs.
>
> Setup:
> - Find my working Brutalist toolkit checkout (brutalist-v2, NOT the old broken one) and follow its documented workflow and my past conventions: beat_sheet.json, BUILD-PROMPT.md, README.md, SOURCES.md, FRICTIONAL.md in the video folder.
> - Find my local clone of the course repo (nikbearbrown/info-7375-prompt-engineering-for-generative-ai) and my existing Week 1 video folder in it. Create a sibling folder for this video using the same naming convention, e.g. .../rithika-s/reallocation-mode-video/. If either can't be found, stop and ask.
>
> Narration = the 8 beats below, VERBATIM.
>
> Visuals per beat (on-screen text only, no screenshots, no personal info, no home-folder paths): […eight beat briefs — see SHOTLIST.md for what was drawn…]
>
> Checks:
> - HARD LIMIT: measured runtime < 4:00, target 3:45–3:55. Use natural pauses between beats to reach the target; speed change max 1.04x. Verify with ffprobe on the actual render, never from the beat sheet.
> - silencedetect (noise=-35dB:d=0.5): report any gap > 1.5s.
> - Extract frames at fps=1/12 and check each beat's visuals actually appear and text is readable, not placeholder.
> - Every number on screen must match EVALUATION.md / the transcripts; list each on-screen number with its source file.
> - Do not commit or push yet. Report runtime, silence gaps, frame check, number-source list, and file paths.
>
> SCRIPT (verbatim): […the eight beats, as in `beat_sheet.json` → `script_text`…]

### Runtime decision (2026-10-21, answer to "how should I place the silence?")

> Go with Sentence pauses: speed 1.0, ~1.0 s after each sentence, ~1.5 s between beats, target ~3:40–3:55, hard limit under 4:00. Where a beat shows terminal text (beats 4, 5, 6), you may extend that pause up to 1.5 s so it's readable. Document the per-sentence voicing in BUILD-PROMPT.md.
