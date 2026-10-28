#!/usr/bin/env python3
"""make_shotlist.py — write SHOTLIST.md (Gate F's typed work order) from beat_sheet.json + scenes.py."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
s = json.loads((HERE / "beat_sheet.json").read_text())
src = (HERE / "scenes.py").read_text()
L = ["# SHOTLIST — Marino Desk Assistant: A Pitch", "",
     "Typed work order. Every beat is one drawn Manim scene in `scenes.py` (show-tell style). No cards, no stock,",
     "no generated media, no screenshots. The corner tag on each beat says what the picture is: real output",
     "(re-run 2026-10-13), constructed/planned (a drawing of work that doesn't exist yet), or an illustration.", "",
     "| Beat | Question | Status | Dur (s) | Class | Picture (one per beat) | Tag on screen |", "|---|---|---|---|---|---|---|"]
for b in s["beats"]:
    cls = b["shot"]["manim"]["class"]
    body = src.split(f"class {cls}(Scene):", 1)[1].split("\nclass ", 1)[0]
    m = re.search(r'tag\("([^"]*)"\)', body)
    L.append(f"| {b['beat_id']} | {b['assignment_question']} | {b['claim_status']} | {b['actual_duration_s']:.2f} | "
             f"`{cls}` | {b['shot']['visual_intent']} | {m.group(1) if m else '— (outro: title + handle)'} |")
L += ["", "Why no `ShowTellCard`: no beat passes the card test (SKILL.md). Each idea is a thing or a flow the drawn cast",
      "(desk bell, browser window, pages, answer cards, crates, contract slip) shows directly.", "",
      f"Total measured narration: {sum(b['actual_duration_s'] for b in s['beats']):.2f} s across {len(s['beats'])} beats."]
(HERE / "SHOTLIST.md").write_text("\n".join(L) + "\n")
print("SHOTLIST.md:", len(s["beats"]), "beats")
