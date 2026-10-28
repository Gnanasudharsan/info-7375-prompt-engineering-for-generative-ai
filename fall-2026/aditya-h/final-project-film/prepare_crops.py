#!/usr/bin/env python3
"""prepare_crops.py: makes the film's crops of Aditya's real ChatGPT run (2026-10-25).

Input: the uncropped screenshots in ~/PEAI_Class/baseline-v2-originals/ (kept out of the repo, since the sidebar shows
private chat titles). Output: research/film-crops/*.png, which the B05/B06 scenes load.
Each crop is cut from the original pixels only. Its colours are inverted (ChatGPT's dark mode becomes light) and it is
enlarged so the text clears GATE T's contrast and 41px minimum at 4K. Nothing is retouched; the on-screen tag says
"colours inverted".
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path.home() / "PEAI_Class/baseline-v2-originals"
OUT = Path(__file__).resolve().parent / "research/film-crops"
OUT.mkdir(parents=True, exist_ok=True)

# name: (screenshot, (left, top, right, bottom) in original 2000×1125 pixels, output width in 4K pixels)
CROPS = {
    "prompt":  (1, (1030, 147, 1452, 268), 2700),   # Aditya's prompt bubble (planted Baymard line inside)
    "date":    (1, (1884, 1, 1990, 17), 760),       # menu-bar clock: "Sun Oct 25 6:24 PM"
    "premise": (1, (848, 480, 1452, 550), 3000),    # "1. Challenge the assumption…" + "The premise is incorrect…"
    "chip":    (1, (872, 690, 1392, 710), 3000),    # the one cited line, ending in the "Baymard +2" chip
    "chipzoom": (1, (1255, 690, 1392, 710), 2600),  # close-up: "fixing them." + the "Baymard +2" chip
}

for name, (shot, box, width) in CROPS.items():
    im = Image.open(SRC / f"{shot}.webp").convert("RGB").crop(box)
    im = ImageOps.invert(im)
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(OUT / f"{name}.png")
    print(f"{name:8} {box} -> {im.size}")
