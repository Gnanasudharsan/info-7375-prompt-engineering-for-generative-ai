# DayThread — Final Project Pitch Film (resubmission)

**Aditya Raj** · INFO 7375 Prompt Engineering and Agentic AI · Fall 2026
**Project:** DayThread, a *proposed* AI check-in assistant that connects details across daily
conversations and brings concerning changes to a home care coordinator for review.
**Target role:** AI Engineer
**Runtime:** 3:26.2 (206.17 s, measured)

## What changed in this resubmission (2026-10-25)

The original film, submitted 2026-10-14, **proposed** a two-day replay as the first thing to make
run. Nothing had run then. For this class-wide resubmission, and following the TA's feedback ("write
the build log for the two-day replay yourself, starting with your prediction of how the summary will
drop the tumble, before you run it"):

1. **Prediction first.** Aditya recorded a prediction before any experimental call
   (`replay/PRE-RUN.md`, and the 13:57 entry in `FRICTIONAL.md`).
2. **A minimal replay was built and run** (`replay/`). It used:
   - one fictional client and a synthetic day-one transcript;
   - a normal and a constrained summary, 5 trials each;
   - two day-two openings per summary (summary only; summary plus the raw transcript);
   - 30 isolated Claude CLI calls, all saved.
3. **Result: Aditya's main prediction was wrong.** The constrained summary was predicted to drop the
   tumble in at least 3 of 5 trials; it dropped it in **0 of 5**.
   - What did go wrong: 9 of 10 summaries turned "I don't want my daughter fussing about it" into a
     disclosure prohibition, and some added unsupported facts.
   - Openings with and without the transcript both followed up in every trial, so these runs don't
     show that the transcript helped.
   - Details and limitations: `replay/RESULTS.md`.
4. **Film corrected minimally** (script v4). Only B04 and B15 changed:
   - B04 no longer calls the replay future work;
   - B15 no longer says "no results", lists the replay as existing, states the prediction and that
     it was wrong, and adds the caption "Replay run 2026-10-25 · synthetic data · fictional client";
   - GATE T then forced one small drawing change in B04.

   Rebuilt and re-gated; see `gate-reports/FINAL-CHECKS.md`.

**Still true:** no DayThread prototype exists. The replay is a small experiment on synthetic data,
not the product.

> **Where the film is.** The film is in the Canvas ZIP `Raj_Aditya_INFO7375_FinalProjectFilm.zip`
> at `final-project-film/Raj_Aditya_INFO7375_FinalProjectFilm.mp4`. It is **not** in the GitHub
> folder, because the course repo's `.gitignore` excludes `*.mp4` and `*.mp3`.

## The film

| | |
|---|---|
| File | `Raj_Aditya_INFO7375_FinalProjectFilm.mp4` (Canvas ZIP only) |
| Version | v4, rebuilt 2026-10-25 (replaces the 2026-10-14 film, SHA-256 `be9d096c…e8eb`, 198.71 s) |
| Measured runtime | **3:26.2 (206.17 s)** (ffprobe) |
| Format | 3840×2160, 24 fps, H.264 + AAC 48 kHz stereo |
| Size | 22,830,610 bytes |
| SHA-256 | `7914fc970d5e2cb931cac61f9681d8cacd3071ccc1267daef7bf0a2696a34f47` |
| Voice | synthesized (Kokoro `am_onyx`, local) reading Aditya's script, disclosed on screen and aloud |

The seven pitch questions are answered in the film (map: `gate-reports/questions-coverage.md`) and
on one page in `PROJECT-BRIEF.md`.

## Contents

| Path | What it is |
|---|---|
| `Raj_Aditya_INFO7375_FinalProjectFilm.mp4` | the film (v4 master from `art final`); **Canvas ZIP only** |
| `PROJECT-BRIEF.md` | one-page answers to the seven questions (original pitch), with *Revision* notes; ends with *exists today* and *will exist* |
| `replay/` | **new:** the two-day replay. Start with `replay/README.md`, then `PRE-RUN.md` (prediction, written first), `RESULTS.md` (final), and `runs/20261025T135900/` (raw outputs, SQLite, review sheet) |
| `SCRIPT.md` | narration source (v4) and the change notes; earlier versions in `source/drafts/` |
| `beat_sheet.json` | the toolkit beat sheet with measured audio durations and build stamps |
| `BUILD-PROMPT.md` | Aditya's prompts for the original film, and the commands run |
| `SOURCES.md` | sources, licences, and who contributed what (original film and resubmission) |
| `FRICTIONAL.md` | dated log: original entries (2026-10-14), then the resubmission entries (2026-10-25) |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | the toolkit's paperwork set, updated for v4 |
| `TOOLKIT-CHANGES.md` | toolkit state; no toolkit source changes for either version |
| `gate-reports/` | gate reports and checks for the **v4** film; `revision-attempts/` holds the two failing GATE T runs; `original-2026-10-14/` holds the reports for the original film |
| `source/` | rebuild source: `make_sheet.py`, `audio_post.py`, `assemble_scenes.py`, `scenes_body.py`, the assembled `scenes.py`, `final_checks.py` (new), narration audio `mp3/` (**Canvas ZIP only**), `mp3/timings.json`, the 2026-10-14 pre-audit reports, script drafts v1–v3 |
| `preview/` | the 15-second preview Aditya approved before the original film (`daythread-preview.mp4`, **Canvas ZIP only**) |

## Toolchain (as used, macOS arm64)

**Film:**
- **Toolkit:** brutalist.art at `main` `519fcbb96e9e1898d374c8794117cab494ffc5cb`, skill
  `show-tell`. No toolkit source changes.
- **Python env:** conda env `brutalist-daythread`, Python 3.12.14.
- **Packages:** Manim 0.20.1, kokoro-onnx 0.6.1 (Kokoro v1.0), faster-whisper 1.2.1 (checks only),
  Pillow 12.3.0.
- **Other tools:** FFmpeg 9.0.2; MacTeX; EB Garamond.
- **Cost:** $0.00, with no network calls while rendering.

**Replay:**
- **Python:** 3.12.8, standard library + SQLite 3.51.0.
- **Calls:** Claude Code CLI 2.1.241 via Aditya's claude.ai login (no API key), model
  `claude-opus-5`. See `replay/README.md`.

## Rebuild

**Replay** (model output varies, so the text will differ; the setup is identical):
```bash
cd replay
python3 -B replay.py --trials 5 && python3 -B flags.py runs/<run_id> && python3 -B make_review_sheet.py runs/<run_id>
```

**Film.** Put `source/` contents in a reel folder outside the toolkit, e.g.
`~/Desktop/Brutalist/my-videos/youtube/daythread/film/`, with `SCRIPT.md` one level above it.
`make_sheet.py` reads `../SCRIPT.md`. Then:
```bash
eval "$(/usr/libexec/path_helper)" && export PATH="/opt/anaconda3/envs/brutalist-daythread/bin:/opt/homebrew/bin:$PATH"
cd ~/Desktop/Brutalist/brutalist.art && git checkout 519fcbb && ./setup        # expect all features ready
REEL=~/Desktop/Brutalist/my-videos/youtube/daythread/film
cd $REEL
python make_sheet.py              # beat_sheet.json from ../SCRIPT.md (keeps measured audio if unchanged)
# Narration audio is in the Canvas ZIP (source/mp3). From the GitHub folder alone, regenerate it:
#   python ~/Desktop/Brutalist/brutalist.art/runtime/scripts/generate_audio_kokoro.py . && rm -rf mp3/raw && python audio_post.py
python assemble_scenes.py         # scenes.py = toolkit iso_kit.py + 11 props (verbatim) + scenes_body.py
cd ~/Desktop/Brutalist
./brutalist.art/art run   "$REEL" --height 2160                    # Gates F, L, A, W, B, V + review cut
./brutalist.art/art final "$REEL" --height 2160 --out "$REEL/exports"   # GATE T + verified 4K master
cd "$REEL" && python final_checks.py   # probe, transcript, frame sheets, bookend_check -> checks/
```
- `art run` renders only scenes whose `manim/<BID>.mp4` is missing. For v4, only B04 and B15 were
  re-rendered.
- After re-voicing a beat, delete its `mp3/raw/beat-<BID>.mp3` before `audio_post.py`. Otherwise
  the old raw audio is reused.
- This folder's MP4 is a renamed copy of `exports/daythread-pitch-film.mp4`.

## GitHub folder vs Canvas ZIP

The ZIP was built from this folder. The GitHub folder should hold the same files, except the media
that the course repo's `.gitignore` keeps out of Git (`*.mp3`, `*.mp4`). These are in the ZIP only:
- `Raj_Aditya_INFO7375_FinalProjectFilm.mp4`: the v4 film (SHA-256 above);
- `preview/daythread-preview.mp4`: the approved 15-second preview (SHA-256 `37f9d008…c1fc`);
- `source/mp3/beat-*.mp3` (18 files) and `source/mp3/raw/beat-*.mp3` (18 files): the narration.

The ZIP's own checksum can't be written inside the ZIP. It goes in the Canvas submission text.

## Honesty notes

- Every drawn workflow beat is captioned "Constructed — proposed workflow". The one observed
  result in the film (B15) is captioned with its run date and "synthetic data · fictional client".
- The replay's fixture is fictional and was written by Claude. The prediction is Aditya's, recorded
  before the run. Aditya's review judgments are kept apart from Claude's provisional scores
  (`replay/runs/20261025T135900/`).
- Lifeline and DailyCall are described only from their own documentation, read by Aditya on
  2026-10-14. Neither product was tested.
- Aditya watched the v4 rebuild and approved it on 2026-10-25: "I watch the video, and I approve of it."
- **Contributions:** `SOURCES.md` says what Aditya and Claude each contributed.

## Credits

Built with the brutalist.art toolkit (show-tell skill, iso kit and props), Manim Community, and Kokoro
TTS. The replay uses Claude through Claude Code. Licences are in `SOURCES.md`.
