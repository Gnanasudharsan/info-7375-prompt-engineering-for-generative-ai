# Gate summary — Remnix Agent pitch film

Final master: `../remnix-agent-pitch.mp4` (built at `build/exports/landscape/`) · 3840×2160 · 24 fps · h264 · 231.2 s (3:51) · 18 beats
SHA-256: `55d9b16616854ac8b552918c868cfaefd7177de9b1c8e79cf81f84ded87e2f86`
**Resubmission, 2026-10-25.** All gates re-run in full on the resubmitted film (13 beats re-voiced and re-rendered,
3 new drawings: BPLAIN, B03, B04; terms card and B01 removed), then once more after a new opening line. Results below are from that final run. The first
submission's results (2026-10-14) were the same, except Gate V's first-run failure noted in the table.

| Gate | What it checks | Result | Report |
|---|---|---|---|
| F | Paperwork exists before render (FACTCHECK, SHOTLIST, PROMPTS) | PASS | — |
| L | Beat mix (no text-slide beats) | PASS | run log |
| A | Each scene adds a new shape after frame 1 (static pre-flight) | PASS, 17/17 scenes | run log |
| W | WCAG contrast, margins, text-on-text | PASS, 17/17 scenes | run log |
| B | Layout audit on rendered scenes | PASS | `layout_audit.md` (last scene audited only; the tool overwrites this file per scene) |
| V | Frame-level visual QC on the compiled cut | 2026-10-14 first run **FAILED** (B00 underfill 55%, B07 right-edge bleed) → fixed → PASS. 2026-10-25 resubmission: PASS (36 frames, 0 blocker, 0 major) | `gate-v-REPORT.md`, `gate-v-contact_sheet.png`, `qc-sheet.png` |
| T | Type lock: text size, wordy cards, contrast | PASS, 17 beats (0 FAILs); B00 SKIP (real screenshot, `shot.type: STILL`, so the screenshot's own small text is not judged as film typography) | `TYPECHECK.md` |
| Render integrity | `compile.py` verify_output + atomic promotion of the master | PASS (status `ready`, master SHA-256 recorded) | build's `build-state.json` (not included: it lists local file paths) |
| Master | Resolution, fps, codec, audio stream | PASS. Note: its duration sub-check was skipped because `runtime/scripts/clock_check.py` is missing from the toolkit checkout. Duration checked by hand: master 231.2 s vs measured narration 230.8 s; silent tail −91 dB over the last 0.9 s; every clip within 0.05 s of its audio | `MASTERCHECK.md` |
| Loudness | Integrated loudness, true peak, per-beat silence | PASS, −21.0 LUFS, true peak −3.3 dBTP | `LOUDNESS.md` |
| Sharpness | Blur per beat | PASS, 18 beats, median LV 259.4 | `SHARPNESS.md` |
| Fact-check | Every claim row resolved, every claim beat covered | PASS (23 rows) | `../build/FACTCHECK.md` |
| Bookend | House bookends (composer cold open, verdict, Your Turn, ClaudeTitleOutro) | **FAIL, 2 items, intentional**: the toolkit's `ClaudeTitleOutro` hard-codes the instructor's handle, which this assignment forbids, so the film ends on the student's own Manim card. Cold open, verdict and Your Turn are declared exempt in `metadata.bookend_exempt`. | output quoted below |

Bookend output (verbatim):

```
[bookend] BLOCKED — 2 failure(s) in remnix-agent-pitch:
  ✗ OUTRO handle is empty — must be 'Revan C'
  ✗ OUTRO title is missing or is the sentinel placeholder — set title='Remnix Agent' in the outro beat props
```

Advisory lint lines (not gates): `SKIN LINT: BIDEA … COLD OPEN LAW wants ClaudeComposerAsk` (the show-tell skill says this is expected under `bookend_exempt`) and `SKIN LINT: BOUT … OUTRO LAW wants ClaudeTitleOutro` (same reason as the bookend item).

Frames were also inspected by eye: the review contact sheets, the stills before 4K, and one frame every 8 s of the master.

One edit to the copied reports: in `MASTERCHECK.md`, the local folder path in the clock_check note was replaced with `<toolkit>`.
