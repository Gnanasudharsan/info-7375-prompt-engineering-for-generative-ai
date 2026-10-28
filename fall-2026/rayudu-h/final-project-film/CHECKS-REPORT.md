# CHECKS-REPORT: Electricity Supplier Check (pitch film)

Toolkit: Brutalist `519fcbb`, show-tell format. Master: `exports/landscape/electricity-supplier-check-pitch.mp4`.
- Format: 3840×2160, 24 fps, 217.7 s.
- sha256 `c1dffb5c60fc91ffcdf0ee584b1c2b2d1d936ef6cc4681799e885beb4c3de72c`
- Built 2026-10-14 (third master, 22:40). It follows the narrator's second round of revisions: electricity visuals instead of cardboard boxes, spoken disclaimers removed, B05 and B07 reworded. Earlier masters are in `_superseded/master-1/` and `_superseded/master-2/`.

## Gate results

| Gate | What it checks | Result | Report |
|---|---|---|---|
| F (paperwork) | FACTCHECK.md, SHOTLIST.md, PROMPTS.md exist | PASS | — |
| Fact check (`factcheck_check.py`) | Every claim row resolved; claim-bearing beats covered | PASS: 14 rows, 0 uncovered | `FACTCHECK.md` |
| L (`beat_lint.py`) | No single-sentence text slides; placeholder types | PASS | — |
| SHAPE | Finance chart shapes | SKIP (not a finance reel) | — |
| A (`static_scene_check.py`, scenes.py in isolation) | Scenes run; shapes change per beat; coordinates in frame | PASS, all 12 scenes | — |
| W (`wcag_margin_check.py`) | Contrast, margins, text-on-text | PASS, all 12 scenes | — |
| B (`manim_layout_audit.py --curve-strict`) | Text overlap or out of frame, at every steady state | PASS, all 12 scenes. B03 failed once ("label on a curve") and was fixed. | `layout_audit.md` (last scene audited) |
| V (`final_frame_check.py`) | Edge bleed, canvas fill, contrast on the compiled cut | PASS: 0 BLOCKER, 0 MAJOR. Run 1 failed on B00 underfill; a sparse-by-design waiver with a written reason was declared on B00, as on the drawn beats. Run 4 failed B03 and B05 on low contrast (0.27 and 0.22 against a 0.30 minimum) because of the folder's pale fill; the body was changed to the near-white card colour and re-run clean. Edge bleed, empty frame and contrast stay enforced. | `_qc/REPORT.md`, `_qc/contact_sheet.png` |
| T (`type_check.py`) | Type size, safe area, contrast, kerning, wordy cards | PASS, 13/13 beats, 0 FAILs | `TYPECHECK.md` |
| Render integrity (`art final`) | Decodable video and audio; duration matches the timeline; Gate V re-run on the encoded candidate | PASS | `exports/landscape/electricity-supplier-check-pitch.verified.json` |
| MASTER (`master_check.py`) | 3840×2160, 24 fps, yuv420p, h264, audio present, no review-label band | PASS | `MASTERCHECK.md` |
| LOUDNESS (`loudness_check.py`) | −28 to −18 LUFS, true peak ≤ −1 dBTP, no silent beat | PASS: −24.68 LUFS, −2.82 dBTP | `LOUDNESS.md` |
| BOOKEND (`bookend_check.py`, advisory; not wired into run or final) | Composer cold open, verdict, Your Turn, `@NikBearBrown` title outro | FAIL by design: "OUTRO (BOUT): no ClaudeTitleOutro beat". The narrator's rule 1 forbids a channel handle or credit line. The cold open, verdict and Your Turn are declared in `bookend_exempt` with a reason. | this file |
| Visual QC (human-eye pass, `CLAUDE-CODE-VISUAL-QC-CHECK.md`) | Frames at 2 fps, read by eye | Review cut, run 1: all 424 frames read in 11 sheets. Found 3 long holds with no motion, 3 beats opening on empty stage, and assorted crowding and overlap. All were fixed, and the 5 changed beats were re-read in run 2 (`_qc/recheck_B03/B05/B06/B11/B12.png`). After the electricity-cast revision: the whole review cut re-read at 2 fps in five sheets (`_qc/recheck_cast_A`–`E.png`). Found long holds in B03 and B05; fixed and re-read. Third master: 11 sheets generated (`_qc/master-2fps/`); full-resolution frames from B03, B05, B06 and B09 checked. | `_qc/` |

## Teaching arc (`skills/make/nopunt`), honestly

| Item | Status |
|---|---|
| FRAMEWORK beat before examples | ✓ B07 (the pipeline) |
| WORKED EXAMPLE | ✗ No constructed numbers exist in the brief, so none was invented |
| FALSIFIABILITY / failure-mode beat | ✓ B10 |
| SCAFFOLDED viewer task | ✗ Not in the narrator's beat order |
| Four bookends | ✗ Overridden by the narrator's rules 1, 4 and 8; title card only |
| No source, no verdict | ✓ B01 and B02 show their sources with download dates; B06 shows the sites |

Beat classes: 12 SHOW (one drawing each), 1 CARD (B00 title), 0 PUNT.
