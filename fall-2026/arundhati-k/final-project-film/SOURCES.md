# SOURCES — Co-op Sponsor Check (pitch film)

Arundhati Kandelkar · INFO 7375 · 2026-10-12

## What I used

| Thing | What it is | Licence / terms |
|---|---|---|
| brutalist.art toolkit, commit `b21f625` (cloned 2026-10-10) | `show-tell` skill, Manim drawing kit, Remotion bookend components, gates | course-provided; no licence file in the checkout |
| Kokoro-82M via `kokoro-onnx` 0.6.1, voice `bf_emma` | local text-to-speech, free, no account | Apache-2.0 (per the model's release) |
| Manim Community 0.18.1, Remotion 4, ffmpeg 9.0.2, faster-whisper 1.2.1 | rendering, encoding, transcript check | open-source |
| EB Garamond (bundled in the toolkit) | typeface | SIL Open Font License (`runtime/fonts/EB_Garamond/OFL.txt`) |
| The Reallocation Engine, my fork `arundhatik26/the-reallocation-engine` | the engine my recipe runs on | MIT (code), CC BY 4.0 (book content) |
| USCIS H-1B Employer Data Hub (uscis.gov), searched 2026-10-12 | the alternative compared in B05/B05A; four names for "Mellon", one for "JPMorgan" | U.S. government public data |
| "80 Days to Stay" sponsorship dataset (`data/80-days-to-stay/`) inside that repo | company sponsorship records; its README describes the SEC-list origin | MIT |

**Synthetic narration.** The voice is Kokoro `bf_emma`, a synthetic text-to-speech voice, not my own voice.
It reads a script I approved. (An earlier cut said this aloud; I removed the spoken line on 2026-10-12 and keep the
disclosure here and in README.md.)

## What I made

- The project idea and the choice of project (option A of three Claude sketched; I chose it).
- The recipe and prototype `coop_sponsor_check.py`, 17 tests, gates G1–G5 (commit `03784b0`, 2026-10-03;
  built with Claude's help, recorded in that submission's own SOURCES.md).
- My voice choice, the decision to keep my name in place of the toolkit persona, the instruction to search the
  USCIS hub, and my answers for B11/B11A and brief §7 (chosen from options Claude offered; the evidence line for
  B11A — my role at Giesecke+Devrient — is from my own résumé, which I chose to cite; the résumé itself is not in
  this folder).

## What Claude (Claude Code, Opus 5.5) contributed

- Sketched three candidate projects; drafted PROJECT-BRIEF.md except §7 (mine).
- Wrote the narration draft, `make_sheet.py`, `scenes.py` (eighteen drawings on the toolkit's kit), FACTCHECK.md,
  SHOTLIST.md, PROMPTS.md, this file, README.md and BUILD-PROMPT.md.
- **Ran the USCIS H-1B Employer Data Hub search on my instruction** (2026-10-12, its built-in browser): read
  the filter list and the FY2026 employer names for "MELLON" and "JPMORGAN"; recorded in
  `evidence/uscis-hub-search-2026-10-12.md`. It drafted B05/B05A and PROJECT-BRIEF §2 from that record. I approved it in chat ("OK..DO IT", 2026-10-12).
- **Ran the first 6 evaluation rows on my instruction** (2026-10-12): wrote `evidence/eval_first_rows.py`, which
  imports my recipe's matcher unchanged, and searched each company in the USCIS hub; table in
  `evidence/eval-first-rows-2026-10-12.md`. The six companies were my choice.
- **2026-10-24/25, on my instruction:** fixed the "AND" defect with a test (fork commit `379252f`); wrote
  `evidence/eval_rows.py`; recorded my predictions *before* the run (`evidence/predictions-2026-10-25.md`, options
  offered by Claude, choice mine); ran rows 7–25 and searched 18 of them in the USCIS hub. **Row 12 (Capital One) I
  searched myself.** It rewrote the opening, B04, B07, B07A, new B07B, B08, B09P; cut the terms card and Your Turn.
- Re-ran my recipe and tests on 2026-10-10 (`evidence/recipe-rerun-2026-10-10.txt`).
- Diagnosed the setup failures, fixed two mispronunciations found by a whisper transcript, and made a
  local edit to the toolkit's outro card so it shows my name instead of the instructor's handle.
- No Claude response is shown in the film. The Your Turn composer shows only a prompt for the viewer.

## Third-party data shown on screen

Company names (JPMorgan Chase, Goldman Sachs, Morgan Stanley, BNY Mellon / The Bank of New York Mellon)
appear as words only, drawn as plain boxes. No logos. No real person, résumé, contact or transcript appears.
The persona in the recipe (Ananya Rao) is fictional and does not appear in the film.
