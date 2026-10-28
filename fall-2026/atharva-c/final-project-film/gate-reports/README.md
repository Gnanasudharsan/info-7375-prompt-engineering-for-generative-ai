# Gate reports — Seeded Faults pitch film

Toolkit: Brutalist (github.com/nikbearbrown/brutalist.art) at commit `b21f625`, free local pipeline only. Final run 2026-10-14 (outro re-rendered to show "Atharva C"; earlier 2026-10-12 re-render after feedback: real output on screen in B03, 44-pt minimum text).

| Gate | What it checks | Result | File |
|---|---|---|---|
| F (paperwork + fact-check) | FACTCHECK/SHOTLIST/PROMPTS exist; every claim resolved | **PASS** (11 rows, 0 unresolved) | `GATE-F-factcheck.txt`, `../film-source/FACTCHECK.md` |
| A (static pre-flight) | every scene adds shapes, stays in the safe area | **PASS** at 4K (11/11 clean) | `art-run-4k.log` |
| W (contrast, margins, overlap) | WCAG contrast and text overlap | **PASS** (all clean) | `art-run-4k.log` |
| B (layout audit) | rendered text inside the safe area, no collisions | **PASS** (CLEAN) | `GATE-B-layout_audit.md` |
| V (frame-level visual QC) | 22 sampled frames | **PASS** (0 BLOCKER, 0 MAJOR) | `GATE-V-REPORT.md`, `GATE-V-contact_sheet.png` |
| T (type lock, before final) | text size, overlap, contrast at each clip midpoint | **PASS** | `GATE-T-TYPECHECK.md` |
| Render integrity (`art final`) | 4K master, hashes of every input | **ready**: 3840×2160, 216.5 s, sha256 `96f04f51…a68e` | `render-integrity.verified.json`, `art-final-4k.log` |
| Bookend check (standalone, not wired into run/final) | toolkit house opening and closing cards | **FAIL — expected and explained below** | `bookend_check.txt` |

## Known, explained non-passes
- **`bookend_check.py`: FAIL.** It expects the toolkit's `ClaudeTitleOutro` card, which hard-codes the instructor's handle "@NikBearBrown" with no override. The assignment forbids the instructor's name, persona or credit line, so the outro is a drawn title scene with my own name. With no ClaudeTitleOutro props on the outro beat, the check reports a missing handle and title (and, since I removed the tiny `channel_title` overlay, it falls back to expecting "@NikBearBrown"). I didn't fake those props to make it pass.
- **SKIN LINT advisories** in `art-run-4k.log` (COLD OPEN LAW / OUTRO LAW) come from the same choice: no persona cold open, no ClaudeTitleOutro. They are advisory and don't block.

Earlier failing runs and their fixes are logged in `../FRICTIONAL.md` (2026-10-10).
