# Visual QC report (manual, per CLAUDE-CODE-VISUAL-QC-CHECK.md)

- Target: the master, youtube/cuegate-pitch/exports/landscape/cuegate-pitch.mp4 (3840x2160, 24 fps, 220.92 s, sha256 2cde81921594d3e21229facb84a084942a0c6ad5accf6cc282893e18fb7f9316)
- Date: 2026-10-14. Done by Claude Code, by looking at the frames.
- Frames: 48, three per beat at 15%, 50% and 85% of each beat's compiled clip (the beat boundaries come from clips/<BID>.mp4 durations). Files: gates/visual-qc/frames/; contact sheet: gates/visual-qc/contact_sheet_master.png. B00, B03 and B08 were also inspected at 1280x720, because their labels sit nearest an edge.

## Defects

| Frame | Time | Beat | Rubric # | Severity | Description | Cause |
| --- | --- | --- | --- | --- | --- | --- |
| B03_85 | 42.717 s | B03 | 4 (overlap) | MINOR | The flag tip comes within a few pixels of the "gap" marker dot; they don't touch and both stay readable. | Flag polygon at x 2.25-2.95 and the dot at x 3.25 in B03_Rules. |
| B07A_85 | 111.035 s | B07A | (plan fit) | MINOR | The grey highlight bars run under the whole source line and the whole reply, not under the exact shifted phrases; the labels "hedged opinion" and "flat refusal" carry the meaning. | Bars sized to the text blocks in B07A_Evidence. |

No BLOCKER or MAJOR defects. Nothing crosses the frame edge or the 5% title-safe inset. No label is hidden behind a shape or overflows its container. Contrast is readable in every sampled frame. The B05 CONSTRUCTED label is visible in all three of its samples (15%, 50%, 85%). No person appears in any frame. No instructor name or handle appears in any frame; the B00 bottom overlay and the outro both read "Deepak Kumaran T S". There are no letterbox bars and the aspect is 16:9.

## Counts

BLOCKER 0 · MAJOR 0 · MINOR 2

## Fixes applied during the build (from the toolkit's gates, not this pass)

- B05: CONSTRUCTED label moved inside the safe area (Gate B strict warning, art run #1).
- B08: tiles set on dark plinths with deeper kraft faces (Gate V low-contrast, art run #2).
- B11: terracotta tape replaced by a grey strap with one terracotta seal (GATE T contrast, art final #1).

Re-check after those fixes: Gate B, Gate V (32 frames) and GATE T all clean; this manual pass found no BLOCKER or MAJOR defect.
