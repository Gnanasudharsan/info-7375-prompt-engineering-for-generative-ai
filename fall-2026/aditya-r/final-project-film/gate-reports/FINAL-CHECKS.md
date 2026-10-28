# DayThread pitch film — final-render checks (v4 rebuild, 2026-10-25)

Master: `exports/daythread-pitch-film.mp4`, packaged as `Raj_Aditya_INFO7375_FinalProjectFilm.mp4`
(byte-identical).
SHA-256: `7914fc970d5e2cb931cac61f9681d8cacd3071ccc1267daef7bf0a2696a34f47` · 22,830,610 bytes.

It replaces the 2026-10-14 master (`be9d096c…e8eb`, 198.71 s). Only beats B04 and B15 changed
(`../SCRIPT.md`, "Changes from v3"). The other 16 clips and their audio were reused unchanged; the
audio files are byte-identical to the 2026-10-14 build.

Built with the toolkit's normal commands and settings: `art run … --height 2160`, then `art final …
--height 2160 --out …/exports`, at toolkit revision `519fcbb`, with no toolkit source changes.

## A. Toolkit gates (final passing runs)

| Gate | Result | Evidence |
|---|---|---|
| GATE F (paperwork files present) | passed (it prints nothing when FACTCHECK/SHOTLIST/PROMPTS exist) | run exit 0 |
| GATE L (beat mix) | clean | `run.log` |
| Gate A (static pre-flight) | clean for B15 (first run) and for the final B04 | `revision-attempts/run-1.log`, `run.log` |
| Gate W (WCAG, margins, overlap) | no failure reported; run exit 0 | `run.log` |
| Gate B (layout audit, curve-strict) | CLEAN: B15 36 snapshots, B04 13 snapshots | `revision-attempts/run-1.log`, `run.log` |
| Gate V (frame QC on the compiled cut) | 36 frames, **0 BLOCKER, 0 MAJOR** | `gate-v-REPORT.md`, `gate-v-contact_sheet.png` |
| GATE T (type check) | **PASS on all 18 beats**, after two failing runs on B04 (below) | `TYPECHECK.md` |
| bookend_check.py (run by hand; not called by `art run`/`art final`) | **FAILS by design**: "OUTRO handle is empty — must be '@NikBearBrown'". The outro shows Aditya's identity; the assignment forbids the instructor's credit line. | `bookend_check.txt` |
| SKIN LINT (advisory) | "cold open / outro un-annotated" (expected template exceptions) | `final.log` |

**GATE T failures on the way (kept in `revision-attempts/`):**
1. **B04 §8.6b bbox overlap.** The longer narration moved B04's clip midpoint, where GATE T takes
   its frame, past the moment the Day 1 → Day 2 ink arc is drawn. The arc joined both page outlines
   and the scribbles into one blob that the checker read as text overlapping a scribble. No real
   text overlapped. (`TYPECHECK-FAIL-B04.md`)
2. **B04 §8.3 contrast.** Redrawing the arc in terracotta made the checker read it as low-contrast
   accent text (2.74:1). (`TYPECHECK-FAIL-B04-2.md`)
3. **Fix.** A short ink link in the gap between the pages, touching neither page. GATE T then
   passed. Neither the toolkit nor the timing was changed to get past the gate.

## B. Checks on the master (`final_checks.py`; machines only, not human viewing or listening)

| Check | Result | Evidence |
|---|---|---|
| Duration | **206.17 s (3:26.2)**, inside 2–4 min. Verification JSON 206.167 s | `probe.txt`, `master.verified.json` |
| Format | 3840×2160, 24 fps, H.264 yuv420p, 4,948 frames; AAC 48 kHz stereo | `probe.txt` |
| Loudness | integrated −24.3 LUFS, LRA 5.8 LU | `probe.txt` |
| Audio continuity | no silence ≥ 0.6 s except inter-beat pauses (0.60–0.76 s) and the outro tail (1.54 s, including the planned 1.0 s pad) | `probe.txt` |
| Decode | full decode, exit 0, no errors | `probe.txt` |
| Narration | the small.en transcript of the master matches the v4 script, including the new B04 and B15 lines | `whisper-master.txt`, `whisper-beats.txt` |

## C. Claude's frame inspection (a model looking at frames; still not human viewing)

- 54 frames (every beat at 15 / 50 / 90 %) and 34 frames 0.06 s either side of every cut:
  `frames-contact-sheet-*.png`, `transitions-contact-sheet.png`.
- B15 shows four pages on "today" (the replay page carries the tumble dot), "prediction: wrong",
  five dashed outlines on "to build", and the caption "Replay run 2026-10-25 · synthetic data ·
  fictional client".
- B04 keeps "Constructed — proposed workflow". The new link sits between the pages.
- The cuts behave as in the 2026-10-14 film: a hard cut, then the next scene draws in.
- No text crosses a frame edge. There are no people, no instructor identity and no mascot.

## D. Human viewing

Aditya watched the v4 film and approved it on 2026-10-25: "I watch the video, and I approve of it."
Aditya did not comment separately on individual items, such as the pronunciation points in Claude's
viewing checklist.

## Not changed, by choice

B02 still says "I'll predict that, then trigger it on purpose". Triggering the omission remains an
unmet plan: the replay's first attempt did not produce it. B15 reports that outcome.

## Not checked

Playback in QuickTime, a browser or Canvas; other displays; captions or subtitles (none produced).
