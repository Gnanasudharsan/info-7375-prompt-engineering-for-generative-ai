#!/usr/bin/env python3
"""patch_outro.py — local patch to the Brutalist toolkit's ClaudeTitleOutro.

Why: the component hard-codes '@NikBearBrown' and always draws a mascot, but
bookend_check.py requires this component on every outro. The INFO7375 assignment
forbids the instructor's name, persona, or credit line. This patch adds two OPTIONAL
props; when they are not set, the component behaves exactly as before.
  handle      — text shown under the title (default stays '@NikBearBrown')
  hideMascot  — true skips the mascot

Run once from the toolkit root:   python3 /path/to/patch_outro.py
Safe to re-run: it detects an already-patched file. Afterwards:  git diff > outro-handle.patch
"""
from pathlib import Path

f = Path("runtime/remotion/src/scenes/ClaudeTitleOutro.tsx")
s = f.read_text()
if "hideMascot" in s:
    print("already patched"); raise SystemExit(0)

edits = [
    (" * Other channels (HAI, Medhavy, Musinique) use their own outro components — never this one.\n */",
     " * Other channels (HAI, Medhavy, Musinique) use their own outro components — never this one.\n *\n"
     " * LOCAL PATCH (INFO7375 final-project film, Pavan Majji): optional `handle` and `hideMascot`\n"
     " * props, so a student film can show its author instead of the instructor's credit line.\n"
     " * Unset, both keep the original locked behaviour.\n */"),
    ("  lectureLayout: z.boolean().optional(),\n});",
     "  lectureLayout: z.boolean().optional(),\n  handle: z.string().optional(),\n  hideMascot: z.boolean().optional(),\n});"),
    ("({ title, slug, mascotAnimation, lectureLayout }) => {",
     "({ title, slug, mascotAnimation, lectureLayout, handle, hideMascot }) => {"),
    ("        {HANDLE}\n", "        {handle || HANDLE}\n"),
    ("      {/* Mascot — slug-seeded, small, under the handle */}\n      <div style={{",
     "      {/* Mascot — slug-seeded, small, under the handle (LOCAL PATCH: hideMascot skips it) */}\n      {!hideMascot && <div style={{"),
    ("        <MascotSVG s={mascotState} scale={1} />\n      </div>",
     "        <MascotSVG s={mascotState} scale={1} />\n      </div>}"),
]
for old, new in edits:
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"patch FAILED: expected 1 match, found {n}:\n{old[:80]}")
    s = s.replace(old, new)
f.write_text(s)
print("patched", f)
