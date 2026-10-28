# DayThread 15-second preview — check results (2026-10-14)

File: `preview/exports/daythread-preview.mp4`
SHA-256: `37f9d008407f48c2c537a63aada4cd342dec376200989d1034fe90659db2c1fc`

Built with the toolkit's normal commands and settings: `./brutalist.art/art run <preview> --height 2160`,
then `./brutalist.art/art final <preview> --height 2160 --out <preview>/exports`. Manim ran at `-qk --fps 24
-r 3840,2160` (run.sh defaults). No resolution or frame-rate setting was changed, and there is no separate
low-resolution pipeline. The low-res renders in Claude's scratchpad were the skill's own "stills first" look
(step 4) and are not part of the preview.

## Measured (raw output in `probe.txt`)
| Check | Result | How |
|---|---|---|
| Duration | **15.04 s** (video 15.042 s, audio 15.042 s) | ffprobe |
| Resolution / frame rate | **3840×2160, 24 fps**, H.264, yuv420p | ffprobe |
| Sound | AAC, 48 kHz stereo. Mean −26.6 dB, max −3.0 dB, integrated −22.0 LUFS | ffmpeg volumedetect, ebur128 |
| Decode | full decode, no errors | `ffmpeg -xerror -f null` |
| Narration words | Machine transcript matches the script: "A check-in mentions a tumble." / "The summary misses it. Day Threads proposed check reads the original words." / "It brings them to a coordinator before anything is sent." | faster-whisper base.en (`whisper-master.txt`). This is a machine transcript. It is not a human listen, and Claude cannot listen. |
| Speech vs. silence | Speech is 10.69 s. The rest (4.3 s) is silent holds that `pad_audio.py` added on purpose, so the preview reaches ~15 s. Measured gaps between lines: 0.35 s (start), 2.13 s, 2.29 s, 1.66 s (end). | ffmpeg silencedetect at −40 dB |
| Per-beat clip vs. audio | B01 3.917/3.932 s · B02 6.125/6.144 s · B03 4.875/4.912 s. Every clip is shorter than its audio, so nothing was centre-cut. | ffprobe |

## Toolkit gates (final run)
| Gate | Result |
|---|---|
| A — static pre-flight | 3/3 scenes clean, 0 warn, 0 error |
| W — WCAG contrast, margins, overlap | passed (strict mode; the run exited 0) |
| B — layout audit (`--curve-strict`) | B01 5, B02 13, B03 11 snapshots → CLEAN |
| V — frame QC on the compiled cut | 6 frames, 0 BLOCKER, 0 MAJOR (`../_qc/REPORT.md`) |
| T — type check | PASS. Smallest text runs: 50 / 47 / 48 px, floor 41 px (`../TYPECHECK.md`) |
| Compiler verification | `daythread-preview.verified.json`, status "ready", same SHA-256 as above |
| `bookend_check.py` (run by hand) | FAILS as expected: "no ClaudeTitleOutro beat". The preview has no outro by Aditya's instruction. `art run` and `art final` don't run this check (`bookend_check.txt`). |

## Layout, checked by looking (`contact-sheet.png`, `frames/`)
12 frames, from t = 0.2 s to 14.9 s, plus two full-resolution crops of the captions.
- "Constructed — proposed workflow" (bottom) and "Synthesized voice reading Aditya's script" (top left) are on
  every one of the 12 frames. At t = 0.2 s, the page and its heading are still fading in, but both captions
  are already at full strength. At 4K the caption letters are sharp (`frames/crop-*.png`).
- No text crosses the frame edge. Labels sit beside objects, not inside outlines.
- What the frames show: the page with "a little tumble" (B01); the summary with a dashed empty row and
  "missed", then the terracotta scan line stopping on the tumble line of the ORIGINAL page (B02); the
  evidence slip on the coordinator's desk, and the envelope at the gate with "nothing sent" (B03).

## Observations for Aditya's review (not gate failures)
1. The 2.1–2.3 s pauses between lines may feel slow. They come from the holds added to reach 15 s.
2. The top-left disclosure sits close to the "check-in" heading.
3. The gate's barrier doesn't clearly read as *closed*. "nothing sent" carries that meaning.
4. "nothing sent" appears only in the last ~2.3 s (from about 12.7 s).

## Not checked
- No human has listened to the audio yet. Pronunciation of "DayThread's" is known only from the machine
  transcript ("Day Threads").
- Playback in a real player (QuickTime, browser) was not tested.
- No other machine or display.

## Fixes made during the build (both re-rendered at 4K through the same toolkit commands)
1. Run 1: GATE T failed B02 (smallest text run 40 px < 41 px). Claude first raised the disclosure caption
   from size 32 to 36. Run 2 still failed at 40 px, so the caption was not the cause.
2. Claude measured the blobs with the toolkit's own `type_check` functions. The 40 px "text run" was the
   summary page's short **handwriting scribble**. GATE T counts scribbles as text. Raising the scribble
   amplitude from 0.07 to 0.085 fixed it, and run 3 passed. The superseded clips and logs are in
   `../_superseded/`.
