# DayThread pitch film — final-render checks (2026-10-14)

Master: `exports/daythread-pitch-film.mp4` (packaged as `Raj_Aditya_INFO7375_FinalProjectFilm.mp4`, byte-identical)
SHA-256: `be9d096cca7525d938707551a6652d9434a7a1d13de467c81a89e4cd57a5e8eb` · 22,087,344 bytes

Built with the toolkit's normal commands and settings: `art run … --height 2160`, then `art final … --height 2160 --out …/exports`.
Manim ran at `-qk --fps 24 -r 3840,2160` (run.sh defaults). No rendering configuration was changed.

## A. Automated checks (machines only — not human viewing or listening)

| Check | Result | Evidence |
|---|---|---|
| Duration | **198.71 s (3:18.7)** — inside 2–4 min. Video 198.667 s / audio 198.708 s; the compiler's verification passed | `probe.txt`, `master.verified.json` |
| Resolution / frame rate | **3840×2160, 24 fps**, H.264 yuv420p, 4,768 frames | `probe.txt` |
| Audio | AAC 48 kHz stereo; mean −26.9 dB, peak −2.9 dB, integrated −24.2 LUFS, LRA 5.6 LU | `probe.txt` |
| Audio continuity | No silence ≥ 0.6 s except natural inter-beat pauses (0.63–0.81 s) and the outro tail (1.58 s, incl. the 1.0 s planned pad). No dropouts | silencedetect in `probe.txt` |
| Decode | full decode, no errors | `probe.txt` |
| Narration content | small.en transcript of the master matches the script start to end | `whisper-master.txt` |
| Pronunciation (machine) | Two problems found and fixed before the final (B09 "AI engineer", BOUT name). Open: the master transcript hears "**full** detection" (B07, ~1:18–1:30) while per-beat and isolated tests hear "fall"; BOUT name transcribed "addediraj" by small.en per-beat, "Aditya Raj" on the master | `whisper-beats.txt`, `whisper-master.txt`, FRICTIONAL |
| Clip vs audio | All 18 clips shorter than their audio by 0.06–0.10 s (no centre-cut) | FRICTIONAL; `run.log` |
| GATE F (paperwork) | passed | `run.log` |
| GATE L (beat mix) | passed | `run.log` |
| Gate A (static pre-flight) | 18/18 clean in the first full run; the 4 re-rendered scenes clean again in the final run | `run.log`, `../source/preaudit/` |
| Gate W (WCAG, margins, overlap) | passed (strict mode; run exit 0) | `run.log` |
| Gate B (layout audit, curve-strict) | CLEAN for every rendered scene (18 + the 4 re-renders) | `run.log`, `../source/preaudit/` |
| Gate V (frame QC on compiled cut) | 36 frames, **0 BLOCKER, 0 MAJOR** | `gate-v-REPORT.md`, `gate-v-contact_sheet.png` |
| GATE T (type check, final) | **PASS** on all 18 beats — after one failing run (B03 overlap, B08 and B13 36 px), fixed and re-rendered | `TYPECHECK.md`, FRICTIONAL |
| bookend_check.py (run by hand; not called by art run/final) | **FAILS by design**: "OUTRO handle is empty — must be '@NikBearBrown'" and outro title prop missing. The drawn outro shows DayThread · Aditya Raj · github.com/aditya-raj-sde per Aditya's identity instruction | `bookend_check.txt`, SCRIPT.md exceptions |
| SKIN LINT (advisory) | "cold open un-annotated" / "outro un-annotated" — expected for the template exceptions | `final.log` |

## B. Claude's frame inspection (a model looking at frames — still not human viewing)

- 54 frames (every beat at 15 / 50 / 90 %) and 34 transition frames (0.06 s each side of every cut): `frames-contact-sheet-*.png`, `transitions-contact-sheet.png`.
- Top-band caption "Synthesized voice reading Aditya's script" on every inspected frame; bottom-band "Constructed — proposed workflow" on every [C] beat frame; B07 carries the documentation caption. Captions are italic, in their own bands, apart from the scene headings.
- The gate (B05, B06, B08) is drawn closed with a lit stop light; it opens only after the approve check in B05.
- No text crosses the frame edge; no people, no instructor identity, no channel handle, no mascot.
- Observations (not failures): every non-continuation beat hard-cuts to a near-empty frame and draws in; B07, B09, B10 and B14 are sparse for their first 1–2 s; the outro name appears only in the last ~1.3 s plus the 1.0 s tail.

## C. Human viewing and listening

When these checks were run, no human had viewed the finished film; Aditya had approved only the 15-second preview. **Later on 2026-10-14, Aditya watched the finished film:** "Yes, i have watched the film and approve of what Claude created." Aditya did not comment separately on the items flagged for listening: the name in the opening and outro, and "fall detection" (~1:18–1:30).

## Not checked
Playback in QuickTime / a browser / Canvas; other displays; captions/subtitles for accessibility (none produced — the narration is not captioned as a transcript).
