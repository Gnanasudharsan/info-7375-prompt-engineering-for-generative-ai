#!/usr/bin/env python3
"""hf_edit.py — the HyperFrames edit pass: burned captions over the Brutalist master.

Input: the verified master (<slug>.mp4, which already carries @Mayank on every frame from the
toolkit) and mp3/words.json. Output project: hyperframes/_edit/index.html; render it with
  hyperframes render hyperframes/_edit --output <slug>-captioned.mp4 --fps 24 --quality high
Captions sit in the band the scenes keep empty (y > 880), centered, clear of the handle.
"""
import json
import re
import shutil
import sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
OUT = REEL / "hyperframes/_edit"
GSAP = Path.home() / "Desktop/Nate_Herk/herk-edit-kit/node_modules/gsap/dist/gsap.min.js"
MAX_WORDS = 7

sheet = json.loads((REEL / "beat_sheet.json").read_text())
words = json.loads((REEL / "mp3/words.json").read_text())
fps = words["fps"]
master = REEL / (sys.argv[1] if len(sys.argv) > 1 else f"{sheet['metadata']['slug']}.mp4")


def chunks(ws):
    cur = []
    for w in ws:
        cur.append(w)
        if len(cur) >= MAX_WORDS or re.search(r"[.?!:;,]$", w["text"]) and len(cur) >= 3:
            yield cur
            cur = []
    if cur:
        yield cur


caps, t0 = [], 0.0
for b in sheet["beats"]:
    dur = float(b["actual_duration_s"])
    groups = list(chunks(words["beats"][b["beat_id"]]))
    for i, g in enumerate(groups):
        start = t0 + g[0]["startFrame"] / fps
        end = t0 + (groups[i + 1][0]["startFrame"] / fps if i + 1 < len(groups) else min(dur, g[-1]["endFrame"] / fps + 0.6))
        if end - start > 0.2:
            caps.append((round(start, 3), round(end - start, 3), " ".join(w["text"] for w in g)))
    t0 += dur
total = round(t0, 3)

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "assets").mkdir(exist_ok=True)
shutil.copy(GSAP, OUT / "assets/gsap.min.js")
link = OUT / "master.mp4"
if link.exists() or link.is_symlink():
    link.unlink()
shutil.copy(master, link)

cap_html = "\n".join(
    f'<div id="c{i}" class="clip cap" data-start="{s}" data-duration="{d}" data-track-index="3"><span>{t}</span></div>'
    for i, (s, d, t) in enumerate(caps))
js = "\n".join(f"tl.from('#c{i} span',{{opacity:0,y:10,duration:.18,ease:'power2.out'}},{s});" for i, (s, _, _) in enumerate(caps))

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>captions</title>
<script src="assets/gsap.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1920px;height:1080px;overflow:hidden;background:#FAF9F5}}
#root{{position:relative;width:1920px;height:1080px;overflow:hidden}}
#vid{{position:absolute;inset:0;width:1920px;height:1080px}}
.cap{{position:absolute;left:340px;width:1240px;bottom:52px;display:flex;justify-content:center}}
.cap span{{font:600 40px/1.25 Inter,Arial,sans-serif;color:#F3F1EA;background:rgba(43,42,37,.92);padding:12px 26px;border-radius:14px;text-align:center;max-width:1240px}}
</style></head><body>
<div id="root" data-composition-id="captions" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
<video id="vid" class="clip" data-start="0" data-duration="{total}" data-track-index="0" src="master.mp4" muted playsinline></video>
<audio id="aud" class="clip" data-start="0" data-duration="{total}" data-track-index="1" src="master.mp4" data-volume="1"></audio>
{cap_html}
</div>
<script>
const tl=gsap.timeline({{paused:true}});
{js}
window.__timelines=window.__timelines||{{}};window.__timelines['captions']=tl;
</script></body></html>
"""
(OUT / "index.html").write_text(html)
(OUT / "meta.json").write_text(json.dumps({"id": "captions", "name": "captions", "width": 1920, "height": 1080, "fps": fps}) + "\n")
print(f"{len(caps)} captions over {total}s -> {OUT}/index.html")
