# Gate reports — Agentic Retrieval Lab (final master, 2026-10-11)

All reports below were produced for the exact `scenes.py` and `beat_sheet.json` that built the final master (sha256 `5dccfe23…24bf5`).

| File | Gate | Result |
|---|---|---|
| `gate-F.md` | F: fact-check content and bookend structure | clean / PASS |
| `gate-A.md` | A: static pre-flight, `scenes.py` alone | 15/15 clean |
| `gate-W.md` | W: WCAG contrast, margins, text overlap | 15/15 clean |
| `gate-L.md` | L: beat-mix lint | clean |
| `gate-B-layout-audit.md` | B: layout audit (`--curve-strict`) at every steady state | 15/15 clean |
| `overlap-every-0.5s.md` + `overlap05.py` | Custom check: the same tests sampled every 0.5 s while anything moves | 15/15 clean |
| `gate-V-REPORT.md` | V: frame-level visual QC on the compiled 4K cut (30 frames) | 0 blockers, 0 majors |
| `gate-T-TYPECHECK.md` | T: type-lock check before `art final` | PASS |

## Changes made to pass gates

No gate was disabled or exempted, and the per-scene exemption list in `type_check.py` was not touched.

**Fixed by moving things:**
- B02: the librarian no longer touches the desk.
- B13: the piles are raised 0.3.
- Many label positions were nudged.

**These could not be fixed by moving, and are not pure moves:**
- **Outline colour.** Some outlines changed from ink to kraft-deep (`#9C8462`), because GATE T reads an ink ring around text as two overlapping labels:
  - B01: the search box.
  - B09: the table highlight.
  - B11: the trays.
  - B13: the dashed "learning" blocks.
- **Shoe size.** Every character's shoes are taller (0.48 of the head unit instead of 0.32), so a dimmed shoe is not read as sub-floor text (37 px < 41 px, GATE T min-size, B03).
- **Dim level.** The B07 vault side dims to 50% instead of 35%, to meet Gate V's contrast floor.

## Toolkit setup note
`./setup --install` exits 1 at its ElevenLabs text guard, because files in the toolkit's own `youtube/` reels contain the matched strings. Every install step still completes.

## Known toolkit issues
- `./art smoke` fails on a fresh clone: its fixture's slug, `_smoke`, breaks the toolkit's own slug rule. It passed on a scratch copy.
- `faster-whisper` 1.2.1 doesn't work with `av` 19. Whisper checks fed it ffmpeg-decoded audio instead.
