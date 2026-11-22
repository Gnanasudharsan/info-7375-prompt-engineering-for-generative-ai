# Render integrity — decisiontrace-lite-film.mp4

Checked 2026-11-22 on the final master from `./art final`, copied here byte-identical
(`cmp` against `final/decisiontrace-lite-film.mp4` in the working folder).

| Check | Command | Result |
|---|---|---|
| Streams | `ffprobe -show_entries stream=codec_type,codec_name,width,height` | video h264 3840×2160; audio aac |
| Duration | `ffprobe -show_entries format=duration` | 301.541667 s (5:01.5). Narration sum 301.13 s; the rest is frame rounding per beat |
| Full decode | `ffmpeg -v error -xerror -i … -f null -` | no errors |
| Loudness | `ffmpeg -af volumedetect` | mean −25.3 dB, max −2.9 dB (pitch: mean ≈ −25.4 dB) |
| SHA-256 | `shasum -a 256` | `882a80a11b0c18bace0f13f71f5b3109edf46f7354dcd812372156d7109add57` (matches `decisiontrace-lite-film.verified.json`) |
| Size | `stat` | 25003984 bytes (under GitHub's 100 MB limit) |
| Review-cut corner tags | one frame per beat at 80% of its length, viewed by eye | absent in all 20 frames |
| GATE V on the master | `./art final` | 40 frames, 0 BLOCKER, 0 MAJOR (`gate-V-REPORT.md`) |
