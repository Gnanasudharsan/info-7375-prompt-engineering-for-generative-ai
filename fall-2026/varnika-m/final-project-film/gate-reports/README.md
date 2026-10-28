# Gate reports — Terraform Docs, Quoted (final: 2026-10-14)

Produced by the brutalist.art toolkit (revision `b21f625`, unmodified) for the `scenes.py` and
`beat_sheet.json` in this folder, which built `final/varnika-final-project-pitch.mp4`
(sha256 `60c1f4edde7c66b722af0336f55727331d13f8b4e2509420588b43e8336c2296`).

| File | Gate | Result |
|---|---|---|
| `gate-F.md` | F: fact-check rows and bookend structure | clean · PASS |
| `gate-L-A-W.md` | L: beat-mix lint · A: static pre-flight · W: contrast, margins, overlap | clean, all 16 scenes (W skips five class names; checked separately, see the file) |
| `gate-B-layout-audit.md` | B: layout audit at every steady state, `--curve-strict` | 16/16 clean |
| `gate-V-REPORT.md`, `gate-V-contact-sheet.png` | V: frame-level visual QC on the compiled cut, 32 frames | 0 blockers, 0 majors |
| `gate-T-TYPECHECK.md` | T: type check before the final cut | PASS, 16 beats |

## What failed on the way, and the fix

| Run | Gate | Finding | Fix |
|---|---|---|---|
| pre-render | B | B03: strike-through line crossed the "Required?" label | "Required?" fades out; "Optional" takes its place |
| pre-render | B | B07A: page bottom touched its caption | Shorter page |
| 1 | V | B08 low contrast, 0.25 and 0.26 < 0.30 | Darker kraft terminal, dark bases under terminal and tray |
| 2 | T | B02 contrast-local 2.60:1 < 3.0:1: the near-black tool block read as text | Tool block changed to grey |
| 3 | own check | B08 and B13 clips ran 0.06 s and 0.21 s past their audio (the compiler trims long clips) | `finish()` no longer forces a minimum wait; all 16 scenes re-rendered |
| 4 | own check | B13's last animation was still drawing when the beat ended | Starts earlier ("The tool itself"); B13 re-rendered |
| 5 | assignment check | Film did not name the target role; drawings of the planned tool were not labelled "constructed" | B08 re-voiced with the role; "planned · constructed" on B01, B02, B05, B06, B08, B09, B10 and B07B's answer card; those 8 scenes re-rendered |
| 5 | B (warning) | The new tag ran 0.13 past the right safe-area edge | Moved left |
| 6 | own check (frame review) | B01: "docs" label touched the new tag; no gate caught it | "docs" moved above the page; B01 re-rendered |

No gate was disabled, exempted or bypassed. The bookend exemptions (`cold-open`, `bvdt`,
`bhtf`) are declared in `beat_sheet.json` with the reason: those bookends carry the
instructor's identity, which this film may not show.
