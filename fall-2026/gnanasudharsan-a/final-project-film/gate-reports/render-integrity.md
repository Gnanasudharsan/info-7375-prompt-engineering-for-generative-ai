# Render integrity — final master decisiontrace-pitch.mp4 (`./art final`, 2026-10-10)

Run: `./art final ~/info7375-films/decisiontrace-pitch --out <working>/final` — strict (no ART_STRICT=0,
no ART_* overrides). Result: exit 0, build-state "ready", decisiontrace-pitch.verified.json written.

`./art final` re-runs its preflight (GATE F paperwork, beat-mix lint, shape gate), refuses if any beat
is a slate, runs compile.py `verify_output`, then GATE V (final_frame_check.py) on the candidate.
It does not re-render scenes, so the Manim gates (A static, W contrast/margins, B layout) are not
part of this run; they passed when each scene was rendered (latest: B01, B06, B08 in the draft-7 build).

Independent re-check of the master:

| Test | Result |
|---|---|
| Video + audio streams | PASS — h264 3840×2160 @24 fps + AAC |
| Duration vs timeline (sum of frame-rounded render_duration_s) | PASS — 191.500 s vs 191.500 s (Δ 0.000 s) |
| Full decode `ffmpeg -v error -xerror -f null` | PASS — exit 0 |
| Audible | PASS — mean −25.4 dB, max −3.6 dB |
| SHA-256 matches verified.json | PASS — 07526250c8e4e0dcc5a7ad520bc8d4d69e3d18f01d262fbdfaf384aaa58e08b7 |
| Review corner tags absent | PASS — bottom-left 1200×140 px at each beat's midpoint: review cut 50–65k non-background px per beat (the tag); final 0 on 12 beats, 1,276 on B03 = the screenshot's own frame border |

GATE V on the final candidate: 26 frames, 0 BLOCKER, 0 MAJOR (gate-V-REPORT.md, gate-V-contact_sheet.png).
Size 12,633,193 bytes (12.6 MB). Runtime 3:11.5.
