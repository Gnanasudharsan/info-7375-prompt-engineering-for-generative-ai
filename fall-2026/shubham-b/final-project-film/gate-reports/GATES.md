# Gate reports — Marino Desk Assistant: A Pitch

All gates are brutalist.art's own (commit `519fcbb`), run on 2026-10-13. Local paths in these files are masked as `<reel>`, `<toolkit>`, `<home>`.

## Final state (the submitted master)

`Bagwe_Shubham_INFO7375_FinalProjectFilm.mp4` = `final/marino-desk-assistant-pitch.mp4`, sha256 `ea18ed8b5f405bda07ee334e1704ec26729b1ab62d56bf98ce0f46bf389cab99`, 237.4 s, 16 beats. This is the second master; the first (`be93a1dd…`, 234.8 s) was replaced after the fresh-context review changed B01, B02, B05, B09, B12, B13 and B14.

| Gate / check | Result | Report |
|---|---|---|
| Gate F: paperwork (FACTCHECK, SHOTLIST, PROMPTS) | PASS | `art-run-5.log` |
| `factcheck_check.py`: claims table | PASS: 27 rows, 16 beats covered, 0 uncovered | `factcheck_check.txt` |
| Gate L: beat-mix lint | PASS | `beat_lint.txt` |
| Gate A: static pre-flight (all 16 scenes) | PASS | `art-run-*.log` |
| Gate W: WCAG + margins + overlap pre-flight | PASS | `art-run-*.log` |
| Gate B: Manim layout audit, strict (per scene) | PASS. The pre-audit caught the outro title at x = 6.35, so it was shrunk before the build | `gate-B-preaudit-all-scenes.txt`, `gate-B-layout_audit-last.md` |
| Gate V: frame QC on the compiled cut (32 frames) | **PASS: 0 BLOCKER, 0 MAJOR** on every run that reached it (`art-run-4` stopped at Gate B first) | `gate-V-REPORT.md`, `gate-V-contact_sheet.png` |
| Gate T: type-lock (`art final`) | **PASS: 16/16 beats, 0 FAILs** (after two fixes, below) | `gate-T-TYPECHECK.md`, `art-final-4.log` |
| Final-cut verification (`art final`) | `status: ready`, sha256 recorded | `marino-desk-assistant-pitch.verified.json` |
| `master_check.py`: render integrity of the master | **PASS: 3840×2160, 24 fps, yuv420p, h264, 237.4 s, 0 failures.** One sub-check was skipped: `MASTERCHECK.md` says the duration clock check couldn't import `runtime/scripts/clock_check.py`, which isn't in the toolkit at `519fcbb`. The duration was checked separately: `art final` verified it against the beat timeline | `master_check.txt`, `MASTERCHECK.md` |
| `loudness_check.py` | PASS: −24.00 LUFS, true peak −5.10 dBTP | `loudness_check.txt`, `LOUDNESS.md` |
| `sharpness_check.py` | PASS: 16 beats, median LV 252.2 (measured on the review cut, which has the same frames) | `sharpness_check.txt`, `SHARPNESS.md` |
| `lane_check.py`, `content_check.py`, `banned_card_check.py`, `placeholder_check.py` | PASS | `*.txt` |
| `bookend_check.py` | **1 deliberate FAIL**: "OUTRO handle 'github.com/bagwe-shubham1727/marino-rag' != expected '@NikBearBrown'" | `bookend_check.txt` |

**Why the bookend failure stays.**
- `bookend_check.py` accepts an outro handle only through `metadata.channel_title`, and otherwise requires `@NikBearBrown`.
- But `compile.py` stamps `metadata.channel_title` at the bottom of the first beat, below the title-safe line, and Gate V blocks the film for that.
- The assignment forbids the instructor's credit line, and Gate V is the gate a film must not be submitted over. So `channel_title` is unset, and my outro draws my repo link itself.
- `bookend_check.py` is not wired into `art run` or `art final`; I ran it by hand.
- Every other assertion it makes passes: the outro exists and is last, its title matches `metadata.title`, and its subline is empty.

Advisory, expected: the "SKIN LINT" lines in the run logs (the cold open isn't `ClaudeComposerAsk`; the outro isn't `ClaudeTitleOutro`). Both follow from the `bookend_exempt` choices explained in `beat_sheet.json`.

## The failed checks (not submitted over)

1. **`art-final-1.log`: Gate T FAILED on 3 beats** (`gate-T-TYPECHECK-fail1.md`):
   - B04: bbox overlap. The ink "typed" squiggle sat inside the ink-outlined search pill.
   - B13: bbox overlap. An ink squiggle sat inside the contract slip.
   - B07: min-size. A 40 px "text run" against the 41 px floor; these were the small ink squiggles.

   Fix: those decorative squiggles are now drawn in grey (DIM), which Gate T doesn't treat as text. B04, B07 and B13 were re-rendered (`art-run-2.log`).
2. **`gate-T-TYPECHECK-fail2.md`: B07 still FAILED min-size**, because the five page cards' ink squiggles were showing at the midpoint. They're now grey too, and B07 was re-rendered (`art-run-3.log`).
3. **`art-final-2.log`:** Gate T PASS (16/16), and the first master was written.
4. **Fresh-context review revision.** B01, B05, B09 and B14 were re-voiced, and B02, B12 and B13 were relabelled.
   - `art-run-4.log`: Gate B FAILED on B13. The "today's date" label, moved down to clear the corner tag, touched the calendar. Fix: the label went back up and the calendar moved down.
   - `art-run-5.log`: all gates pass.
   - `art-final-4.log`: Gate T PASS, and the submitted master was written. `art-final-3.log` refused because B13 and B14 weren't yet slotted.
