# SOURCES — A Mode for the Reallocation Engine (mode video)

**Film:** *A Mode for the Reallocation Engine*, an INFO 7375 video by Rithika Sankar Rajeswari about her mode `rithika-sr-ds-h1b-liveness` for the Reallocation Engine. Built 2026-10-21.

## Project evidence (read-only)
- **Repository:** the-reallocation-engine (fork `rithika-sr/the-reallocation-engine`), branch `mode/rithika-sr-ds-h1b-liveness` at `3cadfe1`. Nothing in it was edited for this video.
- **Files read** (`M/` = `course/2026fa/submissions/rithika-sr/mode/`):
  - `M/G4-HUMAN-REVIEW.md`, `M/WORKED-RUN.md`, `M/DOMAIN-JUSTIFICATION.md`;
  - `M/worked-run/EVALUATION.md`, `M/worked-run/candidates.real.json`;
  - `M/worked-run/out*/mode-log.json` (Runs 1–3), `M/worked-run/terminal/D7-airbnb-redirect.txt`, `D7b-airbnb-liveness-rerun.txt`, `R2-D3-network-calls.txt`;
  - `recipes/cases/2026fa/rithika-sr-ds-h1b-liveness.md`;
  - `scripts/contrib/2026fa/rithika-sr-ds-h1b-liveness/` (`aggregators.json`, `ats_record.py`, `level_rules.json`);
  - the persona file `scripts/contrib/2026fa/rithika-sr-ds-newgrad-h1b-15-2051/fixtures/persona.example.json`;
  - the 2026-10-03 worked run, `course/2026fa/submissions/rithika-sr/WORKED-RUN.md`.
- **Every on-screen number and quoted output** is traced to one of these files in `FACTCHECK.md` (41 rows).

## The persona
Sasha Jones is a **fictional persona** (the persona file's own note says "FICTIONAL persona, safe to commit"). The film labels her "fictional persona" on screen.

## Third-party assets and licences

| Asset | Used for | Licence | Where the licence was read |
|---|---|---|---|
| Kokoro TTS runtime, `kokoro-onnx` | Speech synthesis | MIT | as recorded for the final-project film (same toolkit venv): `.venv/…/kokoro_onnx-0.6.1.dist-info/licenses/LICENSE` |
| Kokoro voice model, Kokoro-82M by hexgrad (`kokoro-v1.0.onnx`, `voices-v1.0.bin`, voice `af_bella`) | The narrator voice | Apache-2.0 | https://huggingface.co/hexgrad/Kokoro-82M (as recorded for the final-project film) |
| faster-whisper 1.2.1 | Word timestamps and the pronunciation check (not shown on screen) | MIT | toolkit venv |
| EB Garamond (the only font in the film) | All on-screen text | SIL Open Font License 1.1 | `brutalist-v2/runtime/fonts/EB_Garamond/OFL.txt` |
| Manim Community 0.18.1 | Drawing and animation | MIT | toolkit venv, `manim-0.18.1.dist-info/METADATA` |
| brutalist.art toolkit (github.com/nikbearbrown/brutalist.art, commit `b21f625`, local checkout `brutalist-v2`) | Build pipeline, gates and the show-tell drawing kit | licence not verified: the repository states no licence (checked for the final-project film) | — |

## Toolkit and voice
- **Toolkit:** brutalist.art `show-tell` skill, free local pipeline: no API keys, paid services or uploads. The drawing kit and pacing helpers in `scenes.py` are copied from Rithika's final-project film, which itself pasted the skill's `iso_kit.py`.
- **Narration:** synthetic voice, Kokoro-82M, voice `af_bella`, **speed 0.962**. It reads Rithika's script in the first person and is **not a recording of Rithika**.
  - The narration was voiced one sentence at a time (`voice_sentences.py`, using the toolkit's own Kokoro helpers) and joined with silences, to reach the 3:40–3:55 target without changing a word: 1.35 s after each sentence, 1.4 s on terminal-text beats, and 1.4 s between beats.
  - A few words are respelled for the audio only (listed in `beat_sheet.json` → `metadata.pronunciation`); on-screen text keeps the standard spelling.
- **No external media.** Every picture is drawn in Manim. There are no screenshots, stock images, photos, music, or AI-generated images or video.
- **No instructor identity.** The film carries no name, portrait, voice, handle or mascot from the instructor's brand kit, and no channel-title stamp.
- **No personal information on screen.** No name, handle, email or home-folder path appears in the picture. The only URLs shown are the job hosts and paths quoted from the repo's transcripts.

## Local toolkit patch
- The `brutalist-v2` checkout carries the uncommitted local edit from the final-project film (it moves the channel_title stamp inside title-safe; `toolkit-local-patch.diff`). This film sets no channel title, so the patch has no effect on it.

## Contributions
- **Rithika:** the mode, the runs and the G4 browser review; the script (verbatim, 8 beats); the visual brief for every beat; the runtime decision (sentence pauses).
- **Claude Code:** built the reel (beat sheet, per-sentence voicing, Manim scenes), ran the gates and checks, and drafted this paperwork.

Rithika's script edits: After reading the first script, I asked for a stronger story because it ended at "the checker is wrong"; that led to the Run 2 and Run 3 fix round. I approved the final 8-beat script without word changes.
