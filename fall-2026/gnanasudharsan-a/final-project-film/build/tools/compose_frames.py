"""compose_frames.py — build the labelled screenshot frames for B03 and B04.

The screenshot pixels are not edited: each PNG is only scaled (Lanczos) and
placed on a plain 3840x2160 cream canvas. B04 is also CROPPED to one section
(the "current implementation status" list through the "Bottom line" sentence);
the crop box is recorded below and the full original stays in evidence/. The label and the highlight boxes are
drawn on the canvas around/over the placed image; the source file is untouched.

B03 is two real screenshots in sequence: the NotebookLM summary until the narration
reaches "Asked which database" (SPLITS below, measured from beat-B03.mp3 with ffmpeg
silencedetect), then the run-2 Q1 answer. The two composed frames are joined into
media/B03.mp4 at the beat's measured length; each frame is shown unchanged (hold).

Usage: python3 tools/compose_frames.py <reel_dir> <font.ttf>
"""
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 3840, 2160
GROUND, INK, ACCENT = (250, 249, 245), (61, 57, 41), (217, 119, 87)
TOP, BOTTOM_MARGIN, SIDE_MARGIN = 300, 120, 220

FRAMES = {
    # bid: (source, label, highlight boxes in source px, crop box in source px or None)
    "B03a": ("2026-10-10_notebooklm_summary.png",
            "REAL · NotebookLM · captured 2026-10-10",
            # "successfully deploy the new" / "NoSQL infrastructure" — wraps over two lines
            [(488, 502, 699, 524), (38, 524, 208, 547)], None),
    "B03b": ("2026-10-10_notebooklm_run2_q1.png",
            "REAL · NotebookLM · captured 2026-10-10",
            # "uses DynamoDB as its primary datastore"
            [(275, 165, 584, 188)], None),
    "B04": ("2026-10-10_chatgpt_q1.png",
            "REAL · ChatGPT · captured 2026-10-10",
            # "June 15, 2026 (latest supplied records):"
            [(56, 543, 304, 565)],
            # heading "What is the current implementation status?" -> end of "Bottom line"
            (22, 406, 656, 698)),
}


def compose(reel, font_path, bid, src, label, boxes, crop=None):
    shot = Image.open(reel / src).convert("RGB")
    if crop:
        shot = shot.crop(crop)
        boxes = [(l - crop[0], t - crop[1], r - crop[0], b - crop[1]) for (l, t, r, b) in boxes]
    scale = min((H - TOP - BOTTOM_MARGIN) / shot.height, (W - 2 * SIDE_MARGIN) / shot.width)
    placed = shot.resize((round(shot.width * scale), round(shot.height * scale)), Image.LANCZOS)
    x0, y0 = (W - placed.width) // 2, TOP

    canvas = Image.new("RGB", (W, H), GROUND)
    canvas.paste(placed, (x0, y0))
    d = ImageDraw.Draw(canvas)
    d.rectangle([x0 - 4, y0 - 4, x0 + placed.width + 3, y0 + placed.height + 3], outline=INK, width=4)

    font = ImageFont.truetype(str(font_path), 96)
    tw = d.textlength(label, font=font)
    d.text(((W - tw) / 2, 110), label, font=font, fill=INK)

    pad = 7
    for (l, t, r, b) in boxes:
        d.rounded_rectangle([x0 + l * scale - pad, y0 + t * scale - pad,
                             x0 + r * scale + pad, y0 + b * scale + pad],
                            radius=14, outline=ACCENT, width=10)
    folder = "work" if bid in PARTS else "media"   # sequence parts are not slots
    out = reel / folder / f"{bid}.png"
    out.parent.mkdir(exist_ok=True)
    canvas.save(out)
    print(f"{bid}: {src} crop={crop} scaled x{scale:.2f} -> {placed.size}, {len(boxes)} highlight box(es) -> {out}")


# beat -> [(part frame, start second)]; the first part starts at 0
SPLITS = {"B03": [("B03a", 0.0), ("B03b", 8.61)]}   # 8.61 s = start of "Asked which database"
PARTS = {part for seq in SPLITS.values() for part, _ in seq}


def build_sequence(reel, bid, parts, fps=24):
    sheet = json.loads((reel / "beat_sheet.json").read_text(encoding="utf-8"))
    total = next(float(b["actual_duration_s"]) for b in sheet["beats"] if b["beat_id"] == bid)
    starts = [t for _, t in parts] + [total]
    cmd, filt = ["ffmpeg", "-y", "-v", "error"], []
    for i, (part, start) in enumerate(parts):
        cmd += ["-loop", "1", "-t", f"{starts[i + 1] - start:.3f}", "-i", str(reel / "work" / f"{part}.png")]
        filt.append(f"[{i}:v]fps={fps},format=yuv420p[v{i}]")
    filt.append("".join(f"[v{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[out]")
    out = reel / "media" / f"{bid}.mp4"
    cmd += ["-filter_complex", ";".join(filt), "-map", "[out]", "-c:v", "libx264", "-crf", "16",
            "-preset", "slow", "-pix_fmt", "yuv420p", "-t", f"{total:.3f}", str(out)]
    subprocess.run(cmd, check=True)
    print(f"{bid}: {' + '.join(f'{p}@{t:.2f}s' for p, t in parts)} -> {out} ({total:.2f}s)")


if __name__ == "__main__":
    reel, font = Path(sys.argv[1]).expanduser(), Path(sys.argv[2])
    for bid, (src, label, boxes, crop) in FRAMES.items():
        compose(reel, font, bid, src, label, boxes, crop)
    for bid, parts in SPLITS.items():
        build_sequence(reel, bid, parts)
