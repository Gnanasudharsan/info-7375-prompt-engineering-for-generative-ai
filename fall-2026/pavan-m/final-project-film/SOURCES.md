# SOURCES — cite-the-line-pitch

## What I used
- **Brutalist toolkit**, cloned from https://github.com/nikbearbrown/brutalist.art into `~/Desktop/Prompt2/brutalist-final`. Used the `show-tell` skill, its isometric drawing kit, Remotion bookend components, and its quality gates. Licence: no LICENSE file found in the checkout (checked 2026-10-11); used for INFO7375 coursework as the assignment directs.
- **Kokoro TTS**, run locally through `kokoro-onnx` with the `am_onyx` voice. The narration is a **synthetic voice reading a script I wrote in my own first person**; it is not a recording of me. Licence: the Kokoro-82M model weights are Apache 2.0 (hexgrad/Kokoro-82M model card); the `kokoro-onnx` package's licence field is empty in its pip metadata (checked 2026-10-11).
- **Manim Community 0.18.1** (drawings) and **Remotion** (bookend cards), installed by the toolkit's setup.
- **Fonts** bundled by the toolkit (EB Garamond, Inter, Lato, Montserrat, PT Mono, and others). Licence: SIL Open Font License; OFL.txt files ship with each family under `runtime/fonts/` and `runtime/manim/fonts/`.
- **Datadog Bits AI SRE documentation**, read by me to describe the alternative named in B06 (read 2026-10-09). No Datadog logos or screenshots are used.
- **Claude Code headless mode documentation**, for the claim in B04 that Claude Code can be run from a script.

## What I made
- The project idea and its choice among alternatives, the target role, and all project decisions recorded in PROJECT-BRIEF.md and FRICTIONAL.md.
- The motivation (B00/BIDEA): my own observation from development work.
- Edits to every draft below, and approval of the final narration.

## What Claude contributed
- Explained the assignment and proposed three candidate project ideas; I chose and shaped one.
- Drafted the seven answers in PROJECT-BRIEF.md from my answers and decisions; I corrected my skills list and evidence wording.
- Drafted the narration script, `make_sheet.py` (adapted from the toolkit's `example-make_sheet.py`), FACTCHECK.md, SHOTLIST.md, PROMPTS.md, README.md, BUILD-PROMPT.md, and this file.
- Wrote the 17 Manim scenes (`scenes_body.py`) and the helper scripts (`check.sh`, `sync_durations.py`, `whisper_check.py`, `patch_outro.py`), and revised them after each gate report. I ran every render and gate, reviewed every contact sheet, and watched the review cut and the master.
- Diagnosed that the toolkit's outro hard-codes the instructor's handle, and wrote the patch; I decided to patch it and to remove the mascot.
- Helped debug the toolkit install (Python version, Pango/Cairo libraries).
- Made one incorrect competitor claim during brainstorming (that log platforms like Datadog don't reason about cause). It was caught against Datadog's documentation and corrected before the script; see FRICTIONAL.md.
- No Claude response is shown on screen in the film.

## Changes to the toolkit
- One local patch to `runtime/remotion/src/scenes/ClaudeTitleOutro.tsx` (`src/outro-handle.patch`): optional `handle` and `hideMascot` props, so the outro shows my name instead of the hard-coded instructor handle. Unset, the component behaves as before.

## Third-party assets
- None beyond the toolkit's own bundled drawing kit, components, and fonts listed above. No stock images, music, or footage.
