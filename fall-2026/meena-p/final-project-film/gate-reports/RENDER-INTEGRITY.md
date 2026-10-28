# RENDER-INTEGRITY — FINAL render

No toolkit gate is named render-integrity. This report repeats, by hand, the checks in brutalist.art/runtime/scripts/compile.py verify_output (line 436), which compile.py also ran automatically on this final before promoting it.

File: film/cite-and-seek-pitch.mp4  ·  sha256 b08dbb34a8ef1cabbd871916be7f71512ab36180aa80fc10abe641697f5938a2  ·  checked 2026-10-12 20:43

| Check | Result |
|---|---|
| Decodable video and audio streams | PASS |
| Duration matches timeline | timeline 239.333 s, file 239.333 s, difference 0.000 s, tolerance 0.150 s -> PASS |
| Full decode, ffmpeg -xerror | PASS (no decode errors) |
| Audio audible (max volume above -80 dB) | PASS (max -3.9 dB, mean -27.1 dB) |
| sha256 matches the toolkit's receipt (cite-and-seek-pitch.verified.json) | PASS |

Streams:

```
stream|codec_name=h264|codec_type=video|width=3840|height=2160|r_frame_rate=24/1
stream|codec_name=aac|codec_type=audio|sample_rate=48000|channels=2|r_frame_rate=0/0
```
