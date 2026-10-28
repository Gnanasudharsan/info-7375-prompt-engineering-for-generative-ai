#!/usr/bin/env python3
"""make_b00.py: media/B00.png for the CueGate pitch film.

Places Deepak's real screenshot (../../inputs/claude-exchange.png) unaltered on the show-tell cream
stage, scaled only, in an ink frame, with a caption that carries the exchange's date, because the
screenshot itself shows no date. The date is read from ../../inputs/claude-exchange.md. Nothing in
the screenshot is redrawn, retouched or cropped.
"""
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SHOT = ROOT / "inputs" / "claude-exchange.png"
MD = ROOT / "inputs" / "claude-exchange.md"
FONT = ROOT / "brutalist.art" / "runtime" / "fonts" / "EB_Garamond" / "static" / "EBGaramond-Regular.ttf"
OUT = HERE / "media" / "B00.png"

W, H = 3840, 2160
STAGE, INK, KRAFT = (0xF2, 0xF0, 0xE9), (0x3D, 0x39, 0x29), (0xDC, 0xC9, 0xAA)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

date = re.search(r"^- Date:\s*(\d{4})-(\d{2})-(\d{2})\s*$", MD.read_text(), re.M)
if not date:
    raise SystemExit("no '- Date: YYYY-MM-DD' line in claude-exchange.md")
y, m, d = (int(g) for g in date.groups())
caption = f"Claude, asked by me on {d} {MONTHS[m - 1]} {y}"

shot = Image.open(SHOT).convert("RGB")
target_w = 3300
scale = target_w / shot.width
shot = shot.resize((target_w, round(shot.height * scale)), Image.LANCZOS)

canvas = Image.new("RGB", (W, H), STAGE)
draw = ImageDraw.Draw(canvas)
x0 = (W - shot.width) // 2
y0 = (H - shot.height) // 2 + 60
draw.rectangle([x0 + 24, y0 + 24, x0 + shot.width + 24, y0 + shot.height + 24], fill=KRAFT)   # kraft drop shadow
canvas.paste(shot, (x0, y0))
draw.rectangle([x0 - 6, y0 - 6, x0 + shot.width + 5, y0 + shot.height + 5], outline=INK, width=8)

font = ImageFont.truetype(str(FONT), 88)
tw = draw.textlength(caption, font=font)
draw.text(((W - tw) / 2, y0 - 230), caption, font=font, fill=INK)

OUT.parent.mkdir(exist_ok=True)
canvas.save(OUT)
(OUT.with_suffix(".source.txt")).write_text(
    "B00 still: Deepak Kumaran T S's own screenshot of a Claude desktop-app exchange, taken 2026-10-14 "
    "(inputs/claude-exchange.png), placed unaltered (scaled only) by make_b00.py with a date caption read "
    "from inputs/claude-exchange.md. source: own. Not generated. No licence needed (own capture of a reply "
    "Deepak received).\n")
print(OUT, canvas.size, "screenshot scale", round(scale, 3), "caption:", caption)
