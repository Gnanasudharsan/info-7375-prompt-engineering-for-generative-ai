# Gate reports — actions-docs-qa-pitch

Brutalist's own quality gates, run 2026-10-11 on the free local pipeline. The final master
(`../actions-docs-qa-pitch.mp4`) was cut only after every gate passed.

| Gate | What it checks | Result | Report |
|---|---|---|---|
| F | paperwork exists before rendering (FACTCHECK, SHOTLIST, PROMPTS) | PASS | `art-run-*.log` |
| L | beat mix: no single-sentence text slides | PASS (clean) | `art-run-*.log` |
| A | static pre-flight on every scene (shapes change, no crashes) | PASS, 16/16 | `art-run-*.log` |
| W | contrast, margins, text-on-text, before render | PASS, 16/16 | `art-run-*.log` |
| B | layout audit of every rendered scene | PASS, every scene CLEAN | `art-run-*.log`, `GATE-B-layout-audit-last-scene.md` |
| V | frame-level visual QC of the compiled film | PASS: 34 frames, 0 blocker, 0 major | `GATE-V-REPORT.md`, `GATE-V-contact-sheet.png` |
| T | type lock: size, contrast, overlap, kerning | **FAIL on the first try, then PASS** (again PASS after the B08 re-voice, 2026-10-13) | `art-final-1-BLOCKED.log`, `art-final-3-PASS.log`, `GATE-T-TYPECHECK.md` |
| Bookend | opening and closing structure | **FAIL on the first try, then PASS** | `BOOKEND-CHECK.txt` |

## What failed and how it was fixed

**GATE T, first run (BLOCKED, no master cut).** Four beats (B00, B04, B11, B12) failed §8.6b
bbox-overlap: each small question card had an ink outline around ink handwriting lines, which
the checker read as two labels printed on top of each other. In B12 the ink line from the card
to the docs also fused into one wide "text" blob. Fix: question cards got a grey edge, the B12
line became deep kraft with a gap at each end, and the eight scenes using the card were
re-rendered (old clips kept in `../youtube/actions-docs-qa-pitch/_superseded/`). Second run: PASS.

**Bookend check, first run.** It found the film's own outro beat but no title or name recorded
for it. The outro does show both, so they were added to the beat sheet where the check reads
them. Second run: PASS.

## Advisory lines that remain, on purpose

`art final` prints two SKIN LINT notes: the opening is the hesitant writer rather than the
Claude.ai composer, and the outro is not the house `ClaudeTitleOutro` card. Both are deliberate.
The assignment says to narrate as myself and never use the instructor's name, persona or credit
line, and the house outro card has the instructor's handle hard-coded.
