# SOURCES

What I used, what I made, and what Claude contributed to the CueGate pitch film. Rows marked "checked" were confirmed on the date shown. Evidence notes are in evidence/day-one/.

## What I used (third party)

| Item | Use | Licence / terms | Accessed |
| --- | --- | --- | --- |
| Brutalist video toolkit, https://github.com/nikbearbrown/brutalist.art, commit 519fcbb96e9e1898d374c8794117cab494ffc5cb | Film pipeline: Kokoro narration, Manim scenes, Remotion outro, compile and gates | No licence is stated in the repository at that commit: no LICENSE, LICENCE or COPYING file, and the GitHub API reports none (checked 2026-10-14). Used as the course assignment requires. | Cloned 2026-10-14 |
| Brutalist show-tell kit code (skills/make/show-tell/templates/iso_kit.py, lines 16-118, 153-163, 311-338) | Drawing primitives and pacing for the Manim scenes | As above (no licence stated). Not included in this submission: reel/build_scenes.py copies these lines from the pinned checkout at build time, after checking the file's sha256. | 2026-10-14 |
| Kokoro TTS voice am_onyx, model files kokoro-v1.0.onnx and voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx, release model-files-v1.0) | Narration audio, generated locally | Kokoro-82M model: Apache-2.0 (Hugging Face model card for hexgrad/Kokoro-82M, checked 2026-10-14). kokoro-onnx 0.6.1 runtime: MIT (GitHub API, checked 2026-10-14). | 2026-10-14 |
| EB Garamond font (bundled in brutalist.art/runtime/fonts/EB_Garamond/) | All on-screen text: Manim labels, the B00 caption, the outro card | SIL Open Font License 1.1 ("Copyright 2017 The EB Garamond Project Authors", OFL.txt beside the font) | 2026-10-14 |
| Manim Community 0.20.1, Remotion 4, ffmpeg 9.0.1, faster-whisper | Rendering, encoding, a local pronunciation check | Each under its own open-source licence; run locally, nothing redistributed | 2026-10-14 |
| Netflix Partner Help: English (USA) Timed Text Style Guide; Timed Text Style Guide: Subtitle Timing Guidelines, General Requirements, Subtitle Templates | Rule facts in B03, PROJECT-BRIEF §2 and the plan's rule profile | Read only, not reproduced (short quotes in evidence/day-one/netflix.md) | 2026-10-14 |
| Gotham Lab, Netflix subtitle delivery requirements guide (secondary) | Attribution for "delivery guides say the file gets rejected" (B03) | Read only | 2026-10-14 |
| Subtitle Edit documentation, https://subtitleedit.github.io/subtitleedit/ (feature index and AI Assistant page) | Alternative named in B04 | Read only | 2026-10-14, re-checked 2026-10-14 |
| Editsub, https://editsub.com/ | Alternative named in B04 | Read only | 2026-10-14, re-checked 2026-10-14 |
| EZTitles, https://eztitles.com/ (home page, Webhelp editing and reading-speed pages) | Alternative named in B04 | Read only | 2026-10-14, re-checked 2026-10-14 |
| PySceneDetect detector documentation, https://www.scenedetect.com/docs/latest/api/detectors.html | Support for "fades and fast motion can fool cut detectors" (B10) | Read only | 2026-10-14 |
| Tears of Steel (Blender Foundation), https://download.blender.org/demo/movies/ToS/subtitles/TOS-en.srt | Candidate corpus film behind "an open Blender film" (B09); no subtitle text used in the film | Film: Creative Commons Attribution 3.0 (mango.blender.org/about). The subtitle file's own licence is not stated on the pages checked. | 2026-10-14 |

## What I made

- The CueGate plan, the narration and the visual plan (edited by me from Claude's first versions; see below).
- The subtitle line in the cold open ("I really don't think we should go in there tonight, not after what happened."), written by me for this film.
- The screenshot of my Claude exchange shown in B00 (evidence/claude-exchange.png, taken 2026-10-14), shown unaltered and scaled only.
- The Reallocation Engine recipe PR #25 that B11 points to, https://github.com/nikbearbrown/the-reallocation-engine/pull/25 (head commit edbac80, open, not merged), built with Claude Code as co-author.
- No drawings or stock images from anyone else. Every picture in the film is drawn by the film's own Manim code (reel/scenes_film.py) or is my own screenshot.

## What Claude contributed

- 2026-10-14, claude.ai (Claude Opus 5.5): helped choose the project; wrote first versions of the CueGate planning README and PDF, the PROJECT-BRIEF, the narration and the Claude Code build prompt. It also found that a competitor claim in its own earlier version was false. I reviewed and edited all of it. The conversation transcript is private and not included.
- 2026-10-14 16:18, Claude desktop app (Opus 5): the cold-open exchange shown in B00, B01 and B07A, reproduced exactly with its date (evidence/claude-exchange.md and .png).
- 2026-10-14, Claude Code (Claude Opus 5.5): authored beat_sheet.json from my narration and wrote the film's scene code, the B00 still builder, first versions of the GATE P paperwork, the outro-handle patch, the setup-guard patch, build_scenes.py, rebuild.sh and the brief renderer; fetched the day-one sources; ran the Brutalist pipeline and gates; assembled this folder. Every change was shown to me, and my verdicts are recorded in REVIEW.md, which I keep outside this submission. The commands are in BUILD-PROMPT.md.
- Reallocation Engine PR #25: every commit is co-authored by me and Claude Opus 5.5.

## Mock-ups

The report table in B05 is labelled CONSTRUCTED on screen for the whole beat. No other interface is shown: B13's prompt is a drawn card, and the only Claude interface on screen is my real screenshot in B00. No screenshot of CueGate exists, because no CueGate code exists yet.
