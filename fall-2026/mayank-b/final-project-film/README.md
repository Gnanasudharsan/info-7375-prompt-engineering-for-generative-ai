# Final Project Pitch Film, v3.1 (resubmission) — Source Check for Support AI

**Author:** Mayank Bhadrasen · INFO 7375, Fall 2026
**Working title:** Source Check for Support AI
**Target role:** AI automation engineer
**Runtime:** 4 min 6 s (245.6 s) · 17 beats · 1920×1080 · captions burned in · @Mayank on every frame
**Stack (planned):** n8n · Python · Claude. **Built so far:** the Python checker and its tests, in [`slice/`](slice/README.md).

> **Still a pitch, with one real piece.** v1 (2026-10-14, 41/50) had nothing built. Following the TA's next step,
> v3 adds the deterministic checker with the Air Canada-shaped test and two condition-flip tests. v3.1 (2026-10-25) also
> rejects claims with extra fields and ignores policies not yet in effect: 21/21 tests pass, and each of three deliberate
> breaks makes tests fail. Every beat carries a chip saying what it shows: `real case`, `real output` or
> `proposed design`. The seven answers are in [PROJECT-BRIEF.md](PROJECT-BRIEF.md).

## What changed from v1, point by point
| Feedback | Where v3 answers it |
|---|---|
| Prof: display @Mayank at all times | the toolkit stamps `@Mayank` bottom-right on every frame (`compile.py`, `~/.config/brutalist/profile.json`) |
| Prof: make it more detailed | B03 five-step architecture, B04 the JSON contract, B05 the field-by-field check, B06 the human gate |
| Prof: why is it a problem | B00 the Air Canada case drawn as words vs policy; B01 one wrong rule repeated to every customer |
| Prof: tell Claude to update Brutalist to add my name to all videos | done in the toolkit, not just this film: see `../brutalist-changes/` |
| Prof: what are you doing and why is it important | B02 (catch it before the customer sees it) |
| Prof side note: log what I did and what Claude did | SOURCES.md "who did what", FRICTIONAL.md |
| TA: who is doing it | BIDEA + BWHO |
| TA: explain it to a five-year-old | BKID (robot helper, checker at the door, rule book) |
| TA: P6 shown, not asserted | real artifacts instead of generic props; B00/B05 put the bot's words beside the policy line with the conflicting word marked |
| TA: Frictional in my own words | FRICTIONAL.md 2026-10-22, "In my own words" |
| TA: next step (Air Canada fixture + two condition flips) | built: `slice/` and B07/B09 show its real output |

## What changed since the pitch
- **Feedback (41/50):** the professor asked for @Mayank on screen at all times, more detail, why this is a problem, and what I am doing and why it matters. The TA asked for who is doing it, an explanation a non-technical viewer can follow, pictures that show the idea instead of labels, Frictional entries in my own words, and, as the next step, the Air Canada fixture plus two condition-flip tests.
- **Built:** that next step, in `slice/` (above).
- **Film v3:** rebuilt around those points. See `CHANGELOG.md`.
- **Project unchanged:** still Source Check for Support AI. The Final Project now requires an agentic loop, tools, a stop condition and a human gate. The HOLD queue is the gate. How the loop and the stop condition fit is a question for Update 1 (Nov 5).

## Run the slice
```bash
cd slice && python3 -m pytest -v && python3 -m source_check.demo
```

## Rebuild the film
Kokoro narration, HyperFrames body scenes, Remotion bookends, Brutalist gates. Full steps: [BUILD-PROMPT.md](BUILD-PROMPT.md).

## Files
- `source-check-pitch-v3.mp4` (the film): Canvas only, not on GitHub
- `PROJECT-BRIEF.md` · `beat_sheet.json` · `BUILD-PROMPT.md` · `SOURCES.md` · `FRICTIONAL.md` · `CHANGELOG.md`
- `FACTCHECK.md` · `SHOTLIST.md` · `PROMPTS.md`: the toolkit's required paperwork
- `slice/`: the checker, cases, tests and saved evidence
- `code/make_sheet.py` (beat sheet), `code/hf_scenes.py` (scenes), `code/hf_edit.py` (captions) · `hyperframes/`: the generated compositions and DESIGN.md
- `_qc/`: gate reports and frame checks · `_v1/`: the v1 sheet, scenes and renders

Note: the instructor asked us not to publish videos on GitHub, so the mp4 is submitted on Canvas only.
