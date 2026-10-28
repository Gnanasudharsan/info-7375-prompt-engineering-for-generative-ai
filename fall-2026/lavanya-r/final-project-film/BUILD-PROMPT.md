# Build Prompt

Rebuild the unpublished `readme-checker-film` reel (README Checker pitch film) from this folder.

Read `beat_sheet.json`, `PROJECT-BRIEF.md`, `SOURCES.md`, `gate-reports/FACTCHECK.md`, and the
current `skills/make/show-tell/SKILL.md` in Brutalist (commit `519fcbb`) first. Preserve every
supplied claim and every line of real terminal output exactly. Use the final beat sheet as the
build contract: show-tell style, Plain register, Claude palette, Kokoro `af_bella`, 20 beats,
about 3 min 29 s. The skill's defaults ("Liam, in for Bear", the `@NikBearBrown` folder label and
the locked `ClaudeTitleOutro` card) are deliberately overridden, because the assignment requires
narrating as myself with no instructor name, persona or credit line.

1. Set up the toolkit with `git clone https://github.com/nikbearbrown/brutalist.art`, then
   `git checkout 519fcbb` and `./setup --install`. At this commit setup exits 1 on its own
   ElevenLabs guard (it flags example films inside the toolkit). The install still completes;
   confirm the voice works with `python3 runtime/scripts/setup_smoke_kokoro.py`.
2. Make an empty working folder named `readme-checker-film`, outside the Brutalist checkout,
   containing `build/make_sheet.py` and `build/scene_body.py`. Run `python3 make_sheet.py` to
   write `beat_sheet.json`. My first name is spelled `Luh-vun-ya` in `narration_text` only, so
   Kokoro says it correctly; on screen it is always "Lavanya". Do not change this spelling.
3. Generate the narration with
   `python3 ~/brutalist.art/runtime/scripts/generate_audio_kokoro.py .`.
   Then pad B14 with a 1.0 s silent tail
   (`ffmpeg -i mp3/beat-B14.mp3 -af "apad=pad_dur=1.0"`) and write its measured duration back
   to `actual_duration_s` and `mp3/timings.json`. Check BHELLO, BIDEA and B14 with a
   faster-whisper transcript before rendering.
4. Build the drawings with
   `cat ~/brutalist.art/skills/make/show-tell/templates/iso_kit.py scene_body.py > scenes.py`.
   Keep the final structure:
   - BHELLO is my own intro.
   - BIDEA is the only Remotion beat: `BrutalistHesitantWriter`, one line, `charMs: 60`,
     `fontSize: 110`, correcting "fix" to "find". Slower settings leave the frame empty and fail
     Gate V.
   - BDEFS is drawn in Manim (`BDEFS_Terms`), not the Remotion `ClaudeDefinitions` card, whose
     fixed text size fails Gate T's 41 px floor.
   - B01T and B02T show only two real terminal lines each, labelled
     `real output · Oct 13, 2026`.
   - B14 is my own outro (box and title only).
   README pages stay as grey lines with ✓ / ⚠ / ✗ marks; do not show README commands on screen.
5. Write the gate paperwork before the first run (`SOURCES.md`, `FACTCHECK.md`, `SHOTLIST.md`,
   `PROMPTS.md`; copies are in `gate-reports/`). Then run
   `~/brutalist.art/art run readme-checker-film --height 2160` from the parent folder. Read
   `_qc/REPORT.md` and fix every BLOCKER and MAJOR defect before continuing. After any voice or
   scene edit, move the stale clip to `_superseded/` and check file timestamps to confirm a
   rebuild really ran.
6. Run
   `~/brutalist.art/art final readme-checker-film --height 2160 --out readme-checker-film/exports/landscape`
   and stop. GATE T must pass. Expect `bookend_check.py` to flag the missing `ClaudeTitleOutro`;
   that is intentional (see FRICTIONAL.md). Never publish or upload.

The report in B05 must remain labelled `CONSTRUCTED MOCK-UP · not built yet`, and the command in
B07 must remain labelled `planned command (constructed)`. Neither may be presented as output of a
tool that exists. Everything about the README Checker is future tense. The only past-tense claims
are the two manual README runs on 2026-10-13 and my public `webapp` repo.
