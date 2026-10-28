# Sponsor Triage — Final Project Pitch Film

**Siddi Kommuri** · INFO 7375 Prompt Engineering for Generative AI, Fall 2026 · built 2026-10-14

| | |
|---|---|
| **Working title** | Sponsor Triage |
| **What it is** | An agent that will check each job posting three ways for an F-1 student looking for data roles: has this company sponsored a *data* role, is the posting live, and is there time left on my OPT. It hands every Apply and every Unresolved back to me at a human gate. |
| **Target role** | Data engineer / analytics engineer (early career). Readers: a hiring manager or engineer on a data team, and the end user (an F-1 student like me). |
| **Film** | `Kommuri_Siddi_INFO7375_FinalProjectFilm.mp4`: **3:29.9** (209.875 s), 3840×2160, 24 fps, H.264 + AAC, 14 MB |
| **SHA-256** | `8a5165529f31a96fe262200bcfc5caea73ef4fa07a3780d4d901be333167ae45` (matches `reports/sponsor-triage-pitch.verified.json`) |
| **Narration** | **Synthetic voice:** Kokoro-82M `af_heart`, free and local, reading my first-person script. It is not my voice, and not the instructor's Liam voice. A TA confirmed on 2026-10-14 that a Brutalist voice is fine. |
| **Toolkit** | Brutalist (`nikbearbrown/brutalist.art` @ `519fcbb`), show-tell skill, free local pipeline only (Manim 0.20.1, Remotion, ffmpeg, Kokoro, faster-whisper). No API keys, no paid generation, no upload. |

## What exists vs. what is proposed

The film tags every body beat bottom-left:
- **RECORD** shows a real file or observation, with its date.
- **SKETCH · proposed** shows something that does not exist yet. In the narration, those things are always "will".

- **Exists today:** my Reallocation Engine recipe `data-role-sponsor-match` (DRAFT; Claude wrote its code, which the film says aloud). Its 12 tests passed again on 2026-10-14, and its worked run is from 2026-10-03.
- **Will exist:** the agent loop, the permission policy, the human gate, the evaluation set and everything else. The full lists end PROJECT-BRIEF.md.

## Folder

| File | What |
|---|---|
| `Kommuri_Siddi_INFO7375_FinalProjectFilm.mp4` | the film. **In the Canvas zip only:** the course repo's `.gitignore` keeps audio and video out of Git, so the GitHub copy omits the MP4 and `mp3/*.mp3`. Check the Canvas file against the SHA-256 above. |
| `PROJECT-BRIEF.md` | the seven answers in text; ends with **Exists today** / **Will exist** |
| `beat_sheet.json` | narration and visual plan for all 14 beats, with measured durations and honesty tags |
| `BUILD-PROMPT.md` | the prompts I gave Claude Code, and the exact rebuild commands |
| `SOURCES.md` | what I used, what I made, what Claude contributed, licences |
| `FRICTIONAL.md` | dated log: Part A build log (Claude's work), Part B my entries |
| `FACTCHECK.md` | every spoken or shown claim → its source; one claim corrected before voicing |
| `SHOTLIST.md`, `PROMPTS.md` | the toolkit's required paperwork (Gate F) |
| `evidence/` | dated evidence behind the RECORD beats, the CSV measurement script, and my local Windows patch to the toolkit |
| `reports/` | the gate reports (below), the build logs, and the pronunciation check |
| `make_sheet.py`, `scene_body.py`, `assemble_scenes.py`, `scenes.py`, `voice.py`, `pronunciation.json`, `finish_audio.py`, `word_clock.py`, `pronunciation_check.py`, `fonts/`, `mp3/` | the source that rebuilds the film |

## Quality gates (the toolkit's own, run 2026-10-14)

| Gate | Tool | Result | Report |
|---|---|---|---|
| F: paperwork | `run.sh` / `compile.py` | PASS | FACTCHECK, SHOTLIST, PROMPTS |
| L: beat mix, SHAPE | `beat_lint.py`, `gate_shape.py` | PASS | `reports/art-run-4k*.log` |
| A: static pre-flight | `static_scene_check.py` | 13/13 PASS | `reports/art-run-4k*.log` |
| W: WCAG contrast, margins, overlap | `wcag_margin_check.py` | 13/13 PASS | `reports/art-run-4k*.log` |
| B: layout audit on rendered frames (strict) | `manim_layout_audit.py --png --curve-strict` | 13/13 CLEAN | `reports/GATE-B-summary.txt` |
| V: frame-level visual QC | `final_frame_check.py` | 28 frames, 0 BLOCKER, 0 MAJOR | `reports/GATE-V-REPORT.md`, `reports/gate-v-contact-sheet.png` |
| T: typography | `type_check.py` | PASS, 14/14 beats | `reports/TYPECHECK.md` |
| Render integrity | `compile.py verify_output` + receipt | PASS | `reports/RENDER-INTEGRITY.md`, `reports/sponsor-triage-pitch.verified.json` |
| Master | `master_check.py` | PASS | `reports/MASTERCHECK.md` |
| Loudness | `loudness_check.py` | PASS (−20.3 LUFS, true peak −5.0 dBTP) | `reports/LOUDNESS.md` |
| Sharpness | `sharpness_check.py` | PASS | `reports/SHARPNESS.md` |

These gates failed during the build and were fixed, not waived: Gate A on B08, layout on B04/B05, and Gate T min-size on B09. Gate V edge-bleed was traced to the Windows-only review timecode. Each fix is in FRICTIONAL.md Part A. The film was built on Windows 11 with two small local patches to the toolkit's `compile.py` and one to `remotion_scenes.py` (`evidence/brutalist-local-windows-patches-2026-10-14.patch`). No gate code was changed.

## Rebuild

```bash
# toolkit next to this folder, at 519fcbb, with its README's setup; on Windows apply evidence/brutalist-local-windows-patches-2026-10-14.patch
export ART_HOME=/path/to/brutalist.art
python make_sheet.py
python voice.py --speed 0.95
python finish_audio.py --src mp3 --prefix beat-
python word_clock.py
python assemble_scenes.py
ART_NO_TIMECODE=1 $ART_HOME/art run . --height 2160
$ART_HOME/art final . --height 2160 --out exports
```

Every step, with what it does, is in BUILD-PROMPT.md. In the Canvas zip, `mp3/` already holds the exact narration used, so step 2 can be skipped. In the GitHub copy the MP3s are git-ignored, so step 2 regenerates them; the word timings and durations are committed in `mp3/words.json` and `mp3/timings.json`.

Privacy: in the logs, reports and receipt posted here, absolute paths under my home folder are shown as `~` (`make_submission.sh` does this when staging; the local originals are unchanged). No credentials, private data or conversation transcripts are included.
