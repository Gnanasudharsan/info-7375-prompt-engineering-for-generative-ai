# RENDER-INTEGRITY — final master

No toolkit gate is literally named "render integrity". This repeats by hand the checks that `brutalist.art/runtime/scripts/compile.py` `verify_output()` ran automatically before it promoted the master and wrote its receipt.

File: `exports/sponsor-triage-pitch.mp4` (submitted as `Kommuri_Siddi_INFO7375_FinalProjectFilm.mp4`, a byte-identical copy). Checked 2026-10-14T22:03Z.

| Check | Result |
|---|---|
| Decodable video and audio streams | PASS |
| Duration matches timeline | timeline 209.875 s (each beat's measured audio rounded up to whole frames at 24 fps, as compile.py `prepare_timeline` does; raw audio sum 209.656 s), file 209.875 s, difference 0.000 s, tolerance max(0.15 s, 2 frames): PASS |
| Full decode, `ffmpeg -xerror` | PASS (no decode errors) |
| Audio audible (max volume above -80 dB) | PASS (mean_volume: -23.6 dB · max_volume: -5.0 dB) |
| SHA-256 matches the toolkit's receipt (`reports/sponsor-triage-pitch.verified.json`, status `ready`) | file `8a5165529f31a96fe262200bcfc5caea73ef4fa07a3780d4d901be333167ae45`, receipt `8a5165529f31a96fe262200bcfc5caea73ef4fa07a3780d4d901be333167ae45`: PASS |

Streams:

```
stream|codec_name=h264|codec_type=video|width=3840|height=2160|r_frame_rate=24/1
stream|codec_name=aac|codec_type=audio|sample_rate=48000|channels=2|r_frame_rate=0/0
```

History: a first master (`8b02d2fb39442906f1436bbef4fcdfdb83a816f87db5160900c033b4e97efb66`) also passed these checks, but was superseded after B09's honesty tag was corrected (FRICTIONAL.md Part A).
