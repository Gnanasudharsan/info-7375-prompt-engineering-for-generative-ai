# Gate index: CueGate pitch film

Every gate the Brutalist toolkit (brutalist.art @ 519fcbb) provides for this film, the command that ran it, its result on the submitted master, and where its report is. All runs 2026-10-14. The paths in the Command column are relative to the build folder: `brutalist.art/` is the pinned toolkit checkout and `youtube/cuegate-pitch/` is the reel. rebuild.sh runs the same commands.

**Render integrity.** The toolkit has no gate named "render-integrity". The check that matches the assignment's meaning ("Fix a film that fails its render-integrity check") is `compile.py verify_output`, which `art final` runs on every master. It requires decodable video and audio streams, a duration that matches the beat timeline (within max(0.15 s, 2 frames)), a full `ffmpeg -xerror` decode with no errors, and audible audio. When it passes, `art final` writes `<master>.verified.json` (status "ready", with the master's sha256). That file is here: **gates/cuegate-pitch.verified.json** (status ready; sha256 2cde81921594d3e21229facb84a084942a0c6ad5accf6cc282893e18fb7f9316 = cuegate-pitch.mp4; duration 220.917 s).

| Gate | Command | Result | Report |
| --- | --- | --- | --- |
| Gate F (paperwork exists) | inside `art run` / `art final` (FACTCHECK.md, SHOTLIST.md, PROMPTS.md present and non-empty) | PASS | build-logs/art-final-2.log |
| Gate F content (factcheck) | `python3 brutalist.art/runtime/qc/factcheck_check.py youtube/cuegate-pitch` | PASS: 30 rows, 0 unresolved, 16 beats covered | factcheck.log |
| Gate L (beat lint) | `python3 brutalist.art/runtime/qc/beat_lint.py youtube/cuegate-pitch/beat_sheet.json` (also inside `art run`) | PASS: clean | beat_lint.log |
| Gate SHAPE | inside `art run` (finance reels only) | not applicable: no finance beats | build-logs/art-run-4.log |
| Gate A (static pre-flight) | inside `art run` (static_scene_check.py on each pending scene) | PASS: 14/14 scenes | build-logs/art-run-1.log to art-run-4.log |
| Gate W (WCAG, margins, overlap) | inside `art run` (wcag_margin_check.py) | PASS: 14/14 scenes | build-logs/art-run-1.log to art-run-4.log |
| Gate B (pixel layout audit, strict) | inside `art run` (manim_layout_audit.py --png --curve-strict per rendered scene) | PASS on all 14 scenes. Failed once: B05 label outside the safe area (art run #1), fixed. | layout_audit.md (last scene audited); build-logs/art-run-1.log (the failure), art-run-2.log, art-run-3.log, art-run-4.log |
| Gate V (frame-level visual QC) | inside `art run` and `art final` (final_frame_check.py) | PASS: 32 frames, 0 BLOCKER, 0 MAJOR. Failed once: B08 low contrast (art run #2), fixed. | GATE-V-REPORT.md, GATE-V-contact_sheet.png; build-logs/art-run-2.log (the failure) |
| GATE T (type-lock) | inside `art final` (type_check.py; also run alone) | PASS: 16 beats, 0 FAILs. Failed once: B11 terracotta tape read as accent text (art final #1), fixed. | TYPECHECK.md; build-logs/art-final-1.log (the failure), art-final-2.log |
| Render integrity (compile.py verify_output) | inside `./brutalist.art/art final youtube/cuegate-pitch --height 2160 --out youtube/cuegate-pitch/exports/landscape` | PASS: verified master written | cuegate-pitch.verified.json, build-state.json, build-logs/art-final-2.log |
| GATE BOOKEND | `python3 brutalist.art/runtime/scripts/bookend_check.py youtube/cuegate-pitch` | PASS: "four bookends correct" (cold open, verdict and Your Turn exempt with reasons; outro checked, handle "Deepak Kumaran T S") | bookend.log |
| GATE MASTER | `python3 brutalist.art/runtime/scripts/master_check.py youtube/cuegate-pitch --mp4 <master>` | PASS: 3840x2160, 24 fps, yuv420p, h264, 220.9 s | MASTERCHECK.md, master.log |
| GATE LOUDNESS | `python3 brutalist.art/runtime/scripts/loudness_check.py youtube/cuegate-pitch --mp4 <master>` | PASS: -24.46 LUFS, true peak -2.90 dBTP | LOUDNESS.md, loudness.log |
| GATE SHARPNESS | `python3 brutalist.art/runtime/scripts/sharpness_check.py youtube/cuegate-pitch` | PASS: 16 beats, median Laplacian variance 204.2. It samples the review cut (cuegate-pitch-slate.mp4), the first file it looks for; the master's frames come from the same clips. | SHARPNESS.md, sharpness.log |
| GATE SRT (captions) | `python3 brutalist.art/runtime/scripts/srt_check.py youtube/cuegate-pitch --srt youtube/cuegate-pitch/cuegate-pitch.srt` | PASS: 68 cues, 0 errors | SRTCHECK.md, srt.log |
| Pacing (duration-planner, advisory) | `python3 brutalist.art/skills/make/duration-planner/scripts/pace_check.py youtube/cuegate-pitch` | ADVISORY (exit 1): B04 (19.2 s) and B11 (27.6 s) are over its 18 s "consider splitting" ceiling. The skill calls this advisory: it never edits the sheet and is not a pass/fail gate. Kept as Deepak's narration. | pace.log |
| Visual QC (manual, CLAUDE-CODE-VISUAL-QC-CHECK.md) | 48 frames from the master (15/50/85% of each beat), looked at | PASS: 0 BLOCKER, 0 MAJOR, 2 MINOR | visual-qc-REPORT.md, visual-qc/contact_sheet_master.png, visual-qc/frames/ |
| Review-cut contact sheet | written by `art run` | for reference | qc-sheet.png |
| Rebuild test (R3) | `./rebuild.sh` run from a fresh copy of this folder in a new temporary directory | PASS: exit 0; the rebuilt master passed verify_output and is byte-identical to cuegate-pitch.mp4 (same sha256); the captions are identical; every gate exit is the same as above | recorded in BUILD-PROMPT.md and the build log |

## Captions

`stage_publish.py` (the toolkit's caption writer) keeps only the first three 42-character lines of each beat (`textwrap.wrap(text, 42)[:3]`), so long beats lose most of their words; its output is in stage_publish.log. The submitted captions come from the film's own reel/make_captions.py instead: every word of the narration, at most two 42-character lines per cue, timed inside each beat's measured window. The SRT gate above checked those captions.

## Advisories not counted as failures

- `art run` printed "SKIN LINT: B00: palette=claude but the cold open is 'un-annotated' — COLD OPEN LAW wants ClaudeComposerAsk". B00 is Deepak's real screenshot by decision (no Claude UI mock-up), and the bookend gate's cold-open exemption records why.
