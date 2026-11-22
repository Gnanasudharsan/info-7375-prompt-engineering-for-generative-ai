"""still_clips.py — fill the two screenshot beats from the pitch film's frames.

The frames are reused unchanged from the pitch film (../build/frames/, made by
its tools/compose_frames.py: real screenshots, scaled only, plus a label and
highlight boxes drawn on the canvas):

  B07 (NotebookLM) = media/B07.mp4: B03b.png (run-2 Q1 answer, "uses DynamoDB as its
      primary datastore") from 0 s, then B03a.png (auto-summary, "successfully deploy
      the new NoSQL infrastructure") from the start of "But it described the migration"
      (measured from beat-B07.mp3 with ffmpeg silencedetect).
  B08 (ChatGPT)    = media/B08.png: B04.png unchanged (cropped Q1 answer, "June 15, 2026").

Usage: python3 tools/still_clips.py <reel_dir> <frames_dir>
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

SEQUENCES = {"B07": [("B03b.png", 0.0), ("B03a.png", 4.74)]}   # 4.74 s = "But it described"
STILLS = {"B08": "B04.png"}


def main():
    reel, frames = Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).expanduser()
    (reel / "media").mkdir(exist_ok=True)
    sheet = json.loads((reel / "beat_sheet.json").read_text(encoding="utf-8"))
    dur = {b["beat_id"]: float(b["actual_duration_s"]) for b in sheet["beats"]}

    for bid, src in STILLS.items():
        shutil.copyfile(frames / src, reel / "media" / f"{bid}.png")
        print(f"{bid}: {src} -> media/{bid}.png (unchanged copy)")

    for bid, parts in SEQUENCES.items():
        total = dur[bid]
        starts = [t for _, t in parts] + [total]
        cmd, filt = ["ffmpeg", "-y", "-v", "error"], []
        for i, (src, start) in enumerate(parts):
            cmd += ["-loop", "1", "-t", f"{starts[i + 1] - start:.3f}", "-i", str(frames / src)]
            filt.append(f"[{i}:v]fps=24,format=yuv420p[v{i}]")
        filt.append("".join(f"[v{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[out]")
        out = reel / "media" / f"{bid}.mp4"
        cmd += ["-filter_complex", ";".join(filt), "-map", "[out]", "-c:v", "libx264", "-crf", "16",
                "-preset", "slow", "-pix_fmt", "yuv420p", "-t", f"{total:.3f}", str(out)]
        subprocess.run(cmd, check=True)
        print(f"{bid}: {' + '.join(f'{s}@{t:.2f}s' for s, t in parts)} -> media/{bid}.mp4 ({total:.2f}s)")


if __name__ == "__main__":
    main()
