"""scenes.py — actions-docs-qa-pitch. The show-tell iso_kit is pasted below (Gate A copies only this file),
then the film's own cast and one Scene per beat."""
from manim import *
import numpy as np
import json as _json, os as _os

# ═════════════════════════════ ISO KIT (show-tell) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"          # kraft cardboard: top, left face, right face (deep enough for Gate V contrast)
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"     # inside walls + floor
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"        # MCP / server blocks
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"         # skill pages
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"                # chart segments, dim to ghost
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=36, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


class Iso:
    """Isometric projection: x runs right-up, y runs left-up, z runs up. (ox, oy) is where (0,0,0) lands."""
    def __init__(self, ox=0.0, oy=0.0, s=1.0):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return np.array([self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s + z * self.s, 0.0])

    def v(self, dx, dy, dz=0.0):
        return self.p(dx, dy, dz) - self.p(0, 0, 0)

    def quad(self, pts, fill, stroke=INK, sw=4):
        return Polygon(*[self.p(*q) for q in pts], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)

    def box(self, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, sw=4):
        """Closed box: the two front faces (x = x0 and y = y0) plus the top."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, sw=sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, sw=sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, sw=sw))

    def open_box(self, x0, y0, z0, w, d, h):
        """(back, front): floor + inner back walls, then the front walls. Put contents between them."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        back = VGroup(
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], BOX_FLOOR),
            self.quad([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], BOX_IN1),
            self.quad([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], BOX_IN2))
        front = VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], BOX_L),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], BOX_R))
        back.set_z_index(0); front.set_z_index(2)
        return back, front

    def tape(self, x0, y0, z1, w, d, drop=0.35, t=0.22):
        """Terracotta tape across the top (along x) and down the left front face."""
        ym = y0 + d / 2
        return VGroup(
            self.quad([(x0, ym - t, z1), (x0 + w, ym - t, z1), (x0 + w, ym + t, z1), (x0, ym + t, z1)], TERRA, sw=0),
            self.quad([(x0, ym - t, z1), (x0, ym + t, z1), (x0, ym + t, z1 - drop), (x0, ym - t, z1 - drop)], TERRA, sw=0))

    def mcp(self, x0, y0, z0, w=1.3, d=1.3, h=0.7):
        """Dark MCP block with two light ports on its right front face."""
        body = self.box(x0, y0, z0, w, d, h, DARK_TOP, DARK_L, DARK_R)
        ports = VGroup(*[self.box(x0 + w * f, y0 - 0.18, z0 + h * 0.3, w * 0.16, 0.18, h * 0.3, GHOST, BOX_IN1, BOX_IN2, sw=1)
                         for f in (0.22, 0.58)])
        return VGroup(body, ports)

    def page(self, x0, y0, z0, w=1.1, d=1.4):
        """A skill page lying flat: white slab, three ghost text lines, one terracotta dot."""
        slab = self.box(x0, y0, z0, w, d, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
        zt = z0 + 0.06
        lines = VGroup(*[Line(self.p(x0 + 0.2, y0 + d * f, zt), self.p(x0 + w - 0.2, y0 + d * f, zt), color=GHOST, stroke_width=4)
                         for f in (0.3, 0.5, 0.7)])
        dot = Dot(self.p(x0 + 0.2, y0 + d * 0.86, zt), radius=0.06, color=TERRA)
        return VGroup(slab, lines, dot)

    def server(self, x0, y0, z0, w=1.4, d=1.4, slab=0.42, n=3):
        """A stack of dark server slabs; returns (stack, lights) — lights start ghost, turn terracotta."""
        stack = VGroup(*[self.box(x0, y0, z0 + i * (slab + 0.04), w, d, slab, DARK_TOP, DARK_L, DARK_R) for i in range(n)])
        lights = VGroup(*[Dot(self.p(x0 + 0.25, y0, z0 + i * (slab + 0.04) + slab / 2), radius=0.06, color=GHOST) for i in range(n)])
        return stack, lights


def ease_in(t):
    """Quadratic ease-in (things dropping into a box). Local: Gate A's stub has no ease_in_quad."""
    return t * t


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


def cursor(x, y, s=0.45):
    return Polygon([x, y, 0], [x, y - s, 0], [x + s * 0.28, y - s * 0.72, 0], [x + s * 0.62, y - s * 0.66, 0],
                   fill_color=INK, fill_opacity=1, stroke_color=CARD, stroke_width=2)


def pill(x, y, w, h=0.62, fill="#FFFFFF"):
    return RoundedRectangle(width=w, height=h, corner_radius=h / 2, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


# ═════════════════════════════ WRITING KIT (quill, ink, paper, scribble) ═════════════════════════════
# Added 2026-10-07 from Bear's two reference drawings: a quill drawing a branching outline on a
# scroll, and three scattered pages of scribbled handwriting with a quill. Use when a beat is
# about writing, drafting, authorship, notes, a manuscript, a log, a letter, a signature.
# Terracotta here is only the ink drop and the outline's nodes (dots) — never the lines.


def quill(x, y, s=1.0, angle=0.0, color=INK, fill=BOX_TOP):
    """A drawn quill with its NIB at (x, y); the feather points up-right. `g.nib` is the nib point.
    Kraft-filled feather, ink outline, a shaft line and one barb. Rotate with `angle` (radians)."""
    o = np.array([x, y, 0.0])
    def P(u, v):  # icon units (0..1) → scene, nib at origin, tip at (1, 1.1)·s
        return o + np.array([u * s, v * s, 0.0])
    body = VMobject(fill_color=fill, fill_opacity=1, stroke_color=color, stroke_width=4)
    body.set_points_smoothly([P(0.00, 0.00), P(0.12, 0.62), P(0.55, 1.02), P(1.00, 1.10),
                              P(0.95, 0.68), P(0.62, 0.22), P(0.00, 0.00)])
    shaft = Line(P(0.02, 0.02), P(0.98, 1.06), color=color, stroke_width=3)
    barb = Line(P(0.46, 0.50), P(0.40, 0.72), color=color, stroke_width=2.5)
    g = VGroup(body, shaft, barb)
    if angle:
        g.rotate(angle, about_point=o)
    g.nib = o.copy()
    return g


def inkwell(iso, x0=0.0, y0=0.0, z0=0.0, s=0.7):
    """A dark ink bottle (iso box + narrow neck) with one terracotta ink dot on the lid."""
    body = iso.box(x0, y0, z0, s, s, s * 0.9, DARK_TOP, DARK_L, DARK_R)
    neck = iso.box(x0 + s * 0.3, y0 + s * 0.3, z0 + s * 0.9, s * 0.4, s * 0.4, s * 0.25, DARK_TOP, DARK_L, DARK_R)
    drop = Dot(iso.p(x0 + s * 0.5, y0 + s * 0.5, z0 + s * 1.15), radius=0.07, color=TERRA)
    return VGroup(body, neck, drop)


def paper(x, y, w=2.4, h=3.0, tilt=0.0, fill=PAGE_TOP):
    """A flat 2-D sheet (the scattered-pages drawing): white page, ink outline, kraft drop shadow.
    `tilt` in radians. Returns a VGroup; `.sheet` is the page rectangle for placing lines on it."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    sheet = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    g = VGroup(shadow, sheet)
    if tilt:
        g.rotate(tilt, about_point=[x, y, 0])
    g.sheet = sheet
    g.cx, g.cy, g.w, g.h, g.tilt = float(x), float(y), float(w), float(h), float(tilt)   # read these; never ask the stub for vertices
    return g


def scribble(x, y, w, amp=0.07, waves=None, color=INK, sw=4):
    """One wavy handwriting line from (x, y) rightwards for `w` units. Reads as script, never as type."""
    n = waves or max(3, int(round(w * 3)))
    pts = []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        pts.append([x + w * t, y + amp * np.sin(t * n * 2 * np.pi) * (0.6 + 0.4 * np.cos(t * 5.3)), 0])
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_smoothly(pts)
    return m


def scribble_block(x, y, w, n=3, gap=0.34, last=0.62, color=INK, sw=4):
    """`n` scribble lines stacked downward from (x, y); the last one is `last`× as long (a paragraph end)."""
    return VGroup(*[scribble(x, y - i * gap, w * (last if i == n - 1 else 1.0), color=color, sw=sw) for i in range(n)])


def scribbles_on(page, n=3, inset=0.3, gap=0.34, color=INK, sw=4):
    """Scribble lines laid on a `paper()` group, following its tilt (uses the page's stored geometry)."""
    w = page.w - 2 * inset
    g = scribble_block(page.cx - w / 2, page.cy + page.h / 2 - inset - 0.1, w, n=n, gap=gap, color=color, sw=sw)
    if abs(page.tilt) > 1e-3:
        g.rotate(page.tilt, about_point=[page.cx, page.cy, 0])
    return g


def outline_tree(x, y, h=1.6, levels=2, spread=0.55, color=INK, node=TERRA):
    """A branching outline (the scroll drawing): a trunk rising from (x, y), forking `levels` times,
    a terracotta dot at every tip. Returns VGroup(lines, dots) — draw lines first, dots last."""
    lines, dots = VGroup(), VGroup()
    def grow(px, py, length, lvl, dx):
        qx, qy = px + dx, py + length
        lines.add(Line([px, py, 0], [qx, qy, 0], color=color, stroke_width=4))
        if lvl == 0:
            dots.add(Dot([qx, qy, 0], radius=0.075, color=node))
            return
        for d in (-spread, spread):
            grow(qx, qy, length * 0.62, lvl - 1, d * (0.75 ** (levels - lvl)))
    grow(x, y, h * 0.42, levels, 0.0)
    g = VGroup(lines, dots)
    g.lines, g.dots = lines, dots
    return g


def write_lines(self, q, lines, speed=1.6, hop=0.22, dip=0.06):
    """Animate the quill `q` WRITING each line in `lines`: the nib hops to the line's start, then the
    line draws while the nib rides its tip (the writing motion). `speed` is scene units per second.
    Call between `until()` phrases so each line lands on its words. Works with the midpoint guard."""
    for ln in lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=hop, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib
        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        try:
            length = float(ln.get_arc_length())
        except Exception:          # Gate A's stub has no arc length; any positive number keeps the check moving
            length = 2.0
        rt = max(0.35, length / speed)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=rt, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
        # the small lift between lines keeps the quill from fusing with the ink at GATE T's midpoint
        q.shift([0, dip, 0]); q.nib = q.nib + np.array([0, dip, 0])


def grow_tree(self, q, tree, per=0.45):
    """Animate the quill drawing an `outline_tree`: each segment draws as the nib rides it; dots land last."""
    for ln in tree.lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=0.18, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib
        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=per, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
    self.play(LaggedStart(*[GrowFromCenter(d) for d in tree.dots], lag_ratio=0.15), run_time=0.6)


# ═════════════════════════════ PROFESSOR BEAR (a person is never an icon) ═════════════════════════════
# PROFESSOR BEAR LAW (Bear, 2026-10-07): when a beat needs an icon of a person, or Professor Bear himself,
# do not draw a person token and do not pull a person icon. Show one of the Professor Bear portraits in
# brutalist.art/professor-bear/, chosen at random among those of the right aspect ratio (1x1 · 2x3 · 16x9).
# `./art bear <ratio> --seed <beat>` picks the same way from the shell.
def _pb_dir():
    env = _os.environ.get("ART_HOME")
    cands = [env and _os.path.join(env, "professor-bear")]
    here = _os.path.dirname(_os.path.abspath(__file__))
    for _ in range(8):
        cands.append(_os.path.join(here, "brutalist.art", "professor-bear"))
        cands.append(_os.path.join(here, "professor-bear"))
        here = _os.path.dirname(here)
    cands.append("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/professor-bear")
    for c in cands:
        if c and _os.path.isdir(c):
            return c
    return cands[-1]


_PB_RATIOS = {"1x1": (1.0, 229), "2x3": (2 / 3, 28), "16x9": (16 / 9, 13)}


def _pb_circle(path):
    """A circular cut (alpha outside the circle), cached beside the set in _crops/. Cropping is fine (Bear, 2026-10-07)."""
    from PIL import Image as _Im, ImageDraw as _Dr
    out_dir = _os.path.join(_os.path.dirname(path), "_crops"); _os.makedirs(out_dir, exist_ok=True)
    out = _os.path.join(out_dir, _os.path.splitext(_os.path.basename(path))[0] + "-circle.png")
    if not _os.path.exists(out):
        im = _Im.open(path).convert("RGBA"); w, h = im.size; s = min(w, h); top = max(0, (h - s) // 3)
        im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s))
        mask = _Im.new("L", (s, s), 0); _Dr.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
        im.putalpha(mask); im.save(out)
    return out


def professor_bear(ratio="2x3", height=3.0, seed=None, x=0.0, y=0.0, frame=True, shape="rect"):
    """A Professor Bear portrait (random within `ratio`; `seed` = the beat id for a stable pick across re-renders).
    Returns a Group: kraft drop shadow, the photo, an ink frame. Place with `x, y`; size with `height`.
    `shape="circle"` gives a round cut (use a 1x1 portrait). Cropping is fine: circle, rounded square, tight head shot."""
    import random as _random
    ar, n = _PB_RATIOS[ratio]
    k = _random.Random(str(seed) if seed is not None else None).randint(1, n)
    path = _os.path.join(_pb_dir(), f"professor-bear-{ratio}-{k:02d}.png")
    circle = shape == "circle"
    if circle:
        ar = 1.0
    w = height * ar
    if circle:
        shadow = Circle(radius=height / 2, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Circle(radius=height / 2, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    else:
        shadow = Rectangle(width=w, height=height, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Rectangle(width=w, height=height, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    try:
        img = ImageMobject(_pb_circle(path) if circle else path)
        img.height = height
        img.move_to([x, y, 0])
    except Exception:
        img = Rectangle(width=w, height=height, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    g = Group(shadow, img, border) if frame else Group(img)
    g.path = path
    return g


# ═════════════════════════════ pacing (narration is the clock) ═════════════════════════════
try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json")))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
    _NARR = {b["beat_id"]: b["narration_text"] for b in _SHEET["beats"]}
except Exception:
    _TARGET, _NARR = {}, {}


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def until(self, phrase, lead=0.25):
    """Wait until `phrase` is spoken (its character share of the narration × the measured audio)."""
    bid = type(self).__name__.split("_")[0]
    n, target = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    if not n or not target or phrase not in n:
        return
    gap = target * n.index(phrase) / len(n) - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def finish(self):
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    self.wait(max(0.3, target - _elapsed(self)) if target else 2.0)


# ═════════════════════════════ actions-docs-qa-pitch: shared cast ═════════════════════════════
# The cast, kept for the whole film: the Actions docs (white pages on a kraft plinth), question
# cards (kraft, handwriting scribbles), the local model (a dark block), answer slips and quote
# strips (white), checks and crosses in ink, terracotta only for dots, sparks and the scan line.
# Every body beat carries an on-screen "constructed" tag (honesty rule: nothing is built yet).

SKETCH = "constructed sketch · not built yet"
SHOTS = "constructed from my 2026-10-11 screenshots"
REPOS = "constructed sketch · the repos are real"


def _tgt(self):
    return _TARGET.get(type(self).__name__.split("_")[0], 0)


def P(self, *anims, rt=0.6, rf=smooth, add=()):
    """self.play, held off the clip midpoint (GATE T and Gate V sample there).
    `add`: objects to put on stage only after any guard wait, so a drop never hangs in view."""
    tgt = _tgt(self)
    if tgt:
        a, b = tgt / 2 - 0.3, tgt / 2 + 0.3
        now = _elapsed(self)
        if now < b and now + rt > a:
            self.wait(b - now + 0.02)
    if add:
        self.add(*add)
    self.play(*anims, run_time=rt, rate_func=rf)


def tag(text):
    t = T(text, 32)
    t.move_to([-6.1 + t.width / 2, -3.05, 0])
    return t


def L(text, x, y, size=40):
    return T(text, size).move_to([x, y, 0])


def docs(iso, n=3, w=2.0, d=2.4):
    """The Actions docs: n white pages on a kraft plinth."""
    plinth = iso.box(-0.2, -0.2, -0.42, w + 0.4, d + 0.4, 0.42)
    pages = VGroup(*[iso.page(0, 0, i * 0.14, w=w, d=d) for i in range(n)])
    return VGroup(plinth, pages)


def qcard(x, y, w=1.8, h=1.1, tilt=0.0):
    """A question card: kraft paper with two handwriting lines. Grey edge, not ink: an ink-outlined
    small card around ink scribbles reads as two stacked labels under GATE T §8.6b."""
    pg = paper(x, y, w, h, tilt, fill=BOX_TOP)
    pg.sheet.set_stroke(color=DIM, width=4)
    return VGroup(pg, scribbles_on(pg, n=2, inset=0.28, gap=0.34))


def slip(x, y, w=1.9, h=1.1, n=2, dot=True):
    """An answer slip: white paper, handwriting lines, a terracotta quote dot."""
    pg = paper(x, y, w, h)
    g = VGroup(pg, scribbles_on(pg, n=n, inset=0.32, gap=0.34))
    if dot:
        g.add(Dot([x - w / 2 + 0.2, y + h / 2 - 0.2, 0], radius=0.07, color=TERRA))
    return g


def cross(x, y, s=0.3, w=8, color=INK):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def window(x, y, w, h):
    """A pale app window: card face, ink outline, grey title band (never dark inside an ink card)."""
    shadow = RoundedRectangle(width=w, height=h, corner_radius=0.14, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    body = RoundedRectangle(width=w, height=h, corner_radius=0.14, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    band = Rectangle(width=w - 0.1, height=0.42, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x, y + h / 2 - 0.27, 0])
    return VGroup(shadow, body, band)


def row(x, y, w, h=0.34, fill=BAR3):
    return Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def outline_box(iso, x0, y0, z0, w, d, h):
    """An outline-only box: planned, not built (stage fill, grey edges)."""
    x1, y1, z1 = x0 + w, y0 + d, z0 + h
    return VGroup(
        iso.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], STAGE, stroke=DIM, sw=4),
        iso.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], STAGE, stroke=DIM, sw=4),
        iso.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], STAGE, stroke=DIM, sw=4))


def repo_box(iso):
    """One of my public repos: a small sealed kraft box with terracotta tape."""
    return VGroup(iso.box(0, 0, 0, 1.5, 1.5, 1.0), iso.tape(0, 0, 1.0, 1.5, 1.5, drop=0.25, t=0.16))


DOCS_L = Iso(-3.0, -1.5, 0.78)     # the docs, left of stage (B00, B01)


# ═════════════════════════════ scenes ═════════════════════════════

class B00_Docs(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        d = docs(DOCS_L); d.shift(UP * 4.4); self.add(d)
        P(self, d.animate.shift(DOWN * 4.4), rt=0.9, rf=ease_in)
        P(self, FadeIn(L("Actions docs", -3.15, -2.55)), rt=0.4)
        until(self, "a command-line tool")
        q = qcard(3.4, 0.9, 2.4, 1.5, tilt=-0.06); q.shift(RIGHT * 5.5); self.add(q)
        P(self, q.animate.shift(LEFT * 5.5), rt=0.8)
        P(self, FadeIn(L("question", 3.4, -0.45)), rt=0.35)
        until(self, "own documentation")
        arc = ArcBetweenPoints([2.0, 0.75, 0], [-1.25, 0.35, 0], angle=0.7, color=INK, stroke_width=5)
        P(self, Create(arc), rt=0.6)
        P(self, GrowFromCenter(Dot([-1.25, 0.35, 0], radius=0.1, color=TERRA)), rt=0.3)
        finish(self)


class B01_Search(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        d = docs(DOCS_L)
        self.add(d, L("Actions docs", -3.15, -2.55))
        until(self, "search the docs")
        scan = Line([-5.2, 1.0, 0], [-1.1, 1.0, 0], color=TERRA, stroke_width=6)
        P(self, Create(scan), rt=0.2)
        P(self, scan.animate.shift(DOWN * 2.6), rt=0.5)
        P(self, FadeOut(scan), FadeIn(L("search", -0.55, 1.75)), rt=0.3)
        until(self, "the passage that holds")
        top = d[1][2]
        P(self, top.animate.shift(UP * 1.0 + RIGHT * 0.35), rt=0.5)
        P(self, Indicate(top, color=None, scale_factor=1.06), rt=0.5)
        until(self, "Then a small model")
        M = Iso(2.3, -1.45, 0.8)
        blk = M.mcp(0, 0, 0, w=1.8, d=1.8, h=1.0); blk.shift(UP * 3.6)
        P(self, blk.animate.shift(DOWN * 3.6), rt=0.5, rf=ease_in, add=[blk])
        P(self, FadeIn(L("local model", 2.3, -2.25)), rt=0.3)
        until(self, "write a short answer")
        s = slip(4.55, 1.85, 2.2, 1.25, dot=False)
        P(self, FadeIn(s, shift=UP * 0.8), rt=0.7)
        until(self, "and quote it")
        P(self, GrowFromCenter(Dot([4.55 - 1.1 + 0.2, 1.85 + 0.625 - 0.2, 0], radius=0.08, color=TERRA)), rt=0.35)
        finish(self)


class B02_QuoteCheck(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        pg = paper(-2.6, 0.12, 4.4, 3.4)
        ys = [1.1, 0.45, -0.2, -0.85]
        lines = VGroup(*[scribble(-4.4, y, 3.4) for y in ys])
        self.add(pg, lines)
        # strip A: a copy of line 2, i.e. the exact quote; strip B: a reworded one
        ra = Rectangle(width=3.8, height=0.5, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=DIM, stroke_width=2).move_to([-2.7, 0.45, 0])
        a = VGroup(ra, lines[1].copy()); a.shift([5.6, 0.75, 0]); a.set_z_index(3)
        rb = Rectangle(width=3.8, height=0.5, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=DIM, stroke_width=2).move_to([2.9, -1.0, 0])
        b = VGroup(rb, scribble(1.2, -1.0, 3.4, amp=0.11, waves=6)); b.set_z_index(3)
        self.add(a, b)
        until(self, "word for word")
        P(self, MoveAlongPath(a, ArcBetweenPoints([2.9, 1.2, 0], [-2.7, 0.45, 0], angle=0.5)), rt=1.0)
        until(self, "If it matches")
        P(self, Create(check(0.15, 0.5, s=0.24, w=8)), rt=0.45)
        P(self, FadeIn(T("match", 40).move_to([0.95 + 0.55, 0.45, 0])), rt=0.3)
        until(self, "If it doesn't")
        P(self, b.animate.move_to([0.4, -0.55, 0]), rt=0.6)
        P(self, b.animate.move_to([2.9, -1.0, 0]), rt=0.5)
        P(self, Create(cross(5.3, -1.0, s=0.26)), rt=0.35)
        P(self, FadeIn(L("no match", 2.9, -1.75)), rt=0.3)
        P(self, Indicate(VGroup(pg, lines, a), color=None, scale_factor=1.04), rt=0.6)
        until(self, "No quote, no answer")
        P(self, b.animate.set_opacity(0.35), rt=0.4)
        finish(self)


class B03_Repo(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        until(self, "public GitHub repository")
        plank = VGroup(Rectangle(width=10.6, height=0.32, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0, -1.62, 0]),
                       Rectangle(width=10.6, height=0.16, fill_color=BOX_IN2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0, -1.86, 0]))
        P(self, GrowFromEdge(plank, LEFT), rt=0.6)
        P(self, FadeIn(L("GitHub repo", -3.9, -2.4)), rt=0.3)
        until(self, "the tool")
        tool = Iso(-3.9, -1.45, 0.62).mcp(0, 0, 0, w=1.6, d=1.6, h=0.9); tool.shift(UP * 4)
        P(self, tool.animate.shift(DOWN * 4), rt=0.5, rf=ease_in, add=[tool])
        until(self, "one pinned version")
        dk = docs(Iso(-1.2, -1.2, 0.46)); dk.shift(UP * 4)
        P(self, dk.animate.shift(DOWN * 4), rt=0.5, rf=ease_in, add=[dk])
        until(self, "fifty test questions")
        cards = VGroup(*[qcard(0.75 + i * 0.75, -0.95, 0.62, 0.95) for i in range(3)])
        P(self, LaggedStart(*[FadeIn(c, shift=DOWN * 0.6) for c in cards], lag_ratio=0.25), rt=0.6)
        P(self, FadeIn(L("test set", 1.5, -2.4)), rt=0.3)
        until(self, "a scored report")
        rep = paper(4.1, -0.62, 1.5, 1.7)
        bars = VGroup(row(3.7, -1.05, 0.28, 0.5, BAR1), row(4.1, -0.9, 0.28, 0.8, BAR2), row(4.5, -0.75, 0.28, 1.1, BAR3))
        rg = VGroup(rep, bars); rg.shift(UP * 4)
        P(self, rg.animate.shift(DOWN * 4), rt=0.5, rf=ease_in, add=[rg])
        finish(self)


class B04_KeywordSearch(Scene):
    def construct(self):
        self.add(tag(SHOTS))
        win = window(1.6, 0.15, 6.2, 4.0)
        self.add(win, L("docs search", 1.6, 2.65))
        until(self, "three questions")
        ys = [1.5, 0.0, -1.5]
        cards = VGroup(*[qcard(-4.65, y, 1.9, 1.05) for y in ys])
        P(self, LaggedStart(*[FadeIn(c, shift=RIGHT * 0.8) for c in cards], lag_ratio=0.3), rt=0.8)
        until(self, "keyword search")
        rys = [1.15, 0.45, -0.25, -0.95]
        hits = [False, False, True]
        res = None
        for i, hit in enumerate(hits):
            new = VGroup(*[row(1.6, ry, 4.8, 0.36, BAR1 if (hit and k == 0) else BAR3) for k, ry in enumerate(rys)])
            if hit:
                new.add(Dot([-1.0, rys[0], 0], radius=0.09, color=TERRA))
            P(self, FadeOut(res) if res is not None else Wait(0.01), FadeIn(new), rt=0.35)
            res = new
            mark = check(-3.25, ys[i] + 0.05, s=0.22, w=8) if hit else cross(-3.25, ys[i], s=0.24)
            P(self, Create(mark), rt=0.35)
        until(self, "just one of the three")
        P(self, FadeIn(T("1 of 3", 64).move_to([3.9, -2.55, 0])), rt=0.4)
        finish(self)


class B05_AIAnswers(Scene):
    def construct(self):
        self.add(tag(SHOTS))
        xs = [-3.05, 3.05]
        wins = VGroup(*[window(x, -0.05, 5.6, 4.1) for x in xs])
        self.add(wins, L("Copilot", xs[0], 2.6), L("Claude", xs[1], 2.6))
        ry = [0.95, -0.05, -1.05]

        def slips(cx):
            return VGroup(*[VGroup(Rectangle(width=3.4, height=0.62, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=DIM, stroke_width=2).move_to([cx - 0.55, y, 0]),
                                   row(cx - 0.35, y, 2.4, 0.18, BAR2)) for y in ry])
        left, right = slips(xs[0]), slips(xs[1])
        P(self, LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in left], lag_ratio=0.25), rt=0.6)
        until(self, "the Claude desktop app")
        P(self, LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in right], lag_ratio=0.25), rt=0.6)
        until(self, "matched the docs on all three")
        ticks = VGroup(*[check(x + 1.75, y + 0.04, s=0.18, w=7) for x in xs for y in ry])
        P(self, LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.1), rt=0.5)
        until(self, "sources for only one")
        P(self, GrowFromCenter(Dot([xs[0] - 2.05, ry[0], 0], radius=0.1, color=TERRA)), rt=0.4)
        until(self, "Claude cited none")
        P(self, Indicate(VGroup(wins[1], right), color=None, scale_factor=1.03), rt=0.6)
        finish(self)


class B06_Sentence(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        xs = [-3.2, 2.6]
        pages, lines = [], []
        for x in xs:
            pg = paper(x, 0.25, 3.4, 3.7)
            ln = VGroup(*[scribble(x - 1.35, 1.45 - k * 0.55, 2.7) for k in range(5)])
            pages.append(pg); lines.append(ln)
            self.add(pg, ln)
        P(self, FadeIn(L("whole page", xs[0], -2.35)), rt=0.3)
        until(self, "the exact sentence")
        band = Rectangle(width=3.0, height=0.36, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([xs[1], 1.45 - 2 * 0.55, 0])
        band.set_z_index(-0.5); pages[1].set_z_index(-1)
        P(self, GrowFromEdge(band, LEFT), FadeIn(L("one sentence", xs[1], -2.35)), rt=0.5)
        P(self, GrowFromCenter(Dot([xs[1] - 1.55, 1.45 - 2 * 0.55, 0], radius=0.08, color=TERRA)), rt=0.3)
        until(self, "checked in the docs")
        P(self, Create(check(xs[1] + 2.15, 1.45 - 2 * 0.55 + 0.05, s=0.22, w=8)), rt=0.4)
        until(self, "a whole page")
        frame = Rectangle(width=3.9, height=4.2, stroke_color=DIM, stroke_width=7, fill_opacity=0).move_to([xs[0], 0.25, 0])
        P(self, Create(frame), rt=0.5)
        finish(self)


class B07_Local(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        LP = Iso(-3.2, -2.0, 0.62)
        base = LP.box(0, 0, 0, 4.2, 3.0, 0.22)
        screen = LP.quad([(0, 3.0, 0.22), (4.2, 3.0, 0.22), (4.2, 3.0, 2.7), (0, 3.0, 2.7)], BAR1)
        self.add(screen, base, L("my laptop", -2.9, -2.55))
        until(self, "on my own laptop")
        parts = VGroup(LP.page(0.45, 0.45, 0.22, w=1.4, d=1.6), LP.page(0.45, 0.45, 0.36, w=1.4, d=1.6), LP.mcp(2.35, 0.55, 0.22, w=1.3, d=1.3, h=0.7))
        parts.shift(UP * 4)
        P(self, parts.animate.shift(DOWN * 4), rt=0.5, rf=ease_in, add=[parts])
        until(self, "The docs search notes")
        cloud = VGroup(Circle(radius=0.8, fill_color=BAR3, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.3, 1.3, 0]),
                       Circle(radius=0.6, fill_color=BAR3, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([4.3, 1.1, 0]),
                       Circle(radius=0.55, fill_color=BAR3, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([2.45, 1.05, 0]),
                       Rectangle(width=2.6, height=0.7, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([3.35, 0.82, 0]))
        P(self, GrowFromCenter(cloud), rt=0.5)
        P(self, FadeIn(L("docs search", 3.35, -0.2)), rt=0.3)
        until(self, "keeps the questions")
        qs = VGroup(*[qcard(3.35 + (i - 1) * 0.55, 1.0 + i * 0.08, 0.7, 0.45) for i in range(3)])
        P(self, LaggedStart(*[FadeIn(c, shift=UP * 0.6) for c in qs], lag_ratio=0.25), rt=0.6)
        until(self, "send nothing anywhere")
        line = Line([-0.6, 0.3, 0], [2.0, 0.5, 0], color=INK, stroke_width=5)
        P(self, Create(line), rt=0.45)
        P(self, Create(cross(0.7, 0.4, s=0.26)), line.animate.set_color(GHOST), rt=0.35)
        finish(self)


class B08_Reader(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        rd = paper(-3.3, 0.0, 4.0, 4.6)
        summ = VGroup(scribble(-4.9, 1.75, 3.2), scribble(-4.9, 1.3, 2.2))
        self.add(rd, summ, L("README", -3.3, 2.75))
        until(self, "In the first minute")
        track = Circle(radius=0.75, stroke_color=GHOST, stroke_width=9, fill_opacity=0).move_to([4.0, 1.55, 0])
        ring = Arc(radius=0.75, start_angle=PI / 2, angle=-TAU * 0.999, color=INK, stroke_width=9).move_arc_center_to([4.0, 1.55, 0])
        self.add(track)
        P(self, Create(ring), rt=1.1, rf=linear)
        P(self, GrowFromCenter(Dot([4.0, 2.3, 0], radius=0.1, color=TERRA)), FadeIn(L("60 s", 4.0, 0.4)), rt=0.35)
        until(self, "the results table")
        rows = VGroup(*[Rectangle(width=3.2, height=0.5, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([-3.3, y, 0]) for y in (0.35, -0.35, -1.05)])
        P(self, LaggedStart(*[GrowFromEdge(r, LEFT) for r in rows], lag_ratio=0.25), rt=0.6)
        until(self, "open one test question")
        card = paper(2.5, -1.2, 4.4, 2.0, fill=BOX_TOP)
        sl = VGroup(*[VGroup(Rectangle(width=1.8, height=1.1, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=DIM, stroke_width=2).move_to([x, -1.2, 0]),
                             scribble(x - 0.65, -1.2, 1.3)) for x in (1.35, 3.65)])
        P(self, FadeIn(VGroup(card, sl), shift=RIGHT * 0.8), rt=0.7)
        until(self, "compare the expected passage")
        P(self, Create(check(2.5, -2.6, s=0.24, w=8)), rt=0.4)
        until(self, "No install needed")
        P(self, Indicate(VGroup(rd, summ, rows), color=None, scale_factor=1.03), rt=0.6)
        finish(self)


class B09_Proves(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        until(self, "ground answers in a source")
        src = slip(-4.6, 0.35, 2.2, 2.4, n=4)
        P(self, FadeIn(src, shift=UP * 0.5), rt=0.5)
        P(self, FadeIn(L("source", -4.6, -1.75)), rt=0.3)
        until(self, "verify them with a script")
        P(self, Create(check(-1.65, 0.35, s=0.6, w=13)), rt=0.5)
        P(self, FadeIn(L("check", -1.55, -1.75)), rt=0.3)
        until(self, "fixed output shape")
        shape = VGroup(paper(1.55, 0.35, 2.2, 2.4),
                       *[Rectangle(width=1.5, height=0.42, fill_color=BAR3, fill_opacity=1, stroke_color=DIM, stroke_width=2).move_to([1.55, y, 0]) for y in (1.0, 0.35, -0.3)])
        P(self, FadeIn(shape, shift=UP * 0.5), rt=0.5)
        until(self, "evaluate it honestly")
        tray = Rectangle(width=2.9, height=0.42, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([4.6, -0.75, 0])
        cards = VGroup(*[qcard(3.6 + i * 0.5, 0.05, 0.42, 1.0) for i in range(5)])
        P(self, FadeIn(tray), LaggedStart(*[FadeIn(c, shift=DOWN * 0.5) for c in cards], lag_ratio=0.15), rt=0.8)
        P(self, FadeIn(L("test set", 4.6, -1.75)), rt=0.3)
        until(self, "ten of which")
        ghosts = VGroup(*[Rectangle(width=0.42, height=1.0, fill_color=STAGE, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([3.6 + i * 0.5, 0.05, 0]) for i in (3, 4)])
        P(self, FadeOut(VGroup(cards[3], cards[4])), FadeIn(ghosts), rt=0.5)
        finish(self)


class B10_Out(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        self.add(docs(Iso(0.35, -1.4, 0.7)), L("Actions docs", 0.25, -2.45))
        # arrowhead sits on the arc's end, pointing along it (counter-clockwise tangent)
        a_end = 2.65 + TAU * 0.8   # arc ends near the top, between the cross arms
        tip_at = np.array([0.55 * np.cos(a_end), 0.55 * np.sin(a_end), 0.0])
        tang = np.array([-np.sin(a_end), np.cos(a_end), 0.0])
        radial = tip_at / 0.55
        # base straddles the arc's end, point runs on into the gap
        head = Polygon(tip_at + 0.26 * tang, tip_at + 0.15 * radial, tip_at - 0.15 * radial,
                       fill_color=DIM, fill_opacity=1, stroke_width=0)
        loop = VGroup(Arc(radius=0.55, start_angle=2.65, angle=TAU * 0.8, color=DIM, stroke_width=8), head)
        web = VGroup(RoundedRectangle(width=1.9, height=1.25, corner_radius=0.1, stroke_color=DIM, stroke_width=6, fill_opacity=0),
                     Rectangle(width=1.8, height=0.25, fill_color=BAR3, fill_opacity=1, stroke_width=0).shift(UP * 0.45))
        other = VGroup(*[Rectangle(width=1.3, height=1.6, fill_color=STAGE, fill_opacity=1, stroke_color=DIM, stroke_width=5).shift([k * 0.18, k * 0.14, 0]) for k in range(2)])
        mem = VGroup(Circle(radius=0.62, stroke_color=DIM, stroke_width=6, fill_opacity=0),
                     Circle(radius=0.16, stroke_color=DIM, stroke_width=5, fill_opacity=0).shift([-0.75, -0.62, 0]),
                     Circle(radius=0.09, stroke_color=DIM, stroke_width=4, fill_opacity=0).shift([-1.0, -0.9, 0]))
        plan = [("agent loops", loop, [-2.1, 1.5, 0], [-4.7, 1.9, 0]),
                ("a web interface", web, [2.6, 1.5, 0], [4.7, 1.9, 0]),
                ("other docs", other, [-2.2, -0.9, 0], [-4.7, -1.1, 0])]
        for phrase, obj, start, end in plan:
            until(self, phrase)
            obj.shift(start)                       # every object is built around the origin
            P(self, FadeIn(obj), rt=0.25)
            P(self, obj.animate.shift(np.array(end) - np.array(start)), rt=0.35)
            P(self, Create(cross(end[0], end[1], s=0.32)), rt=0.25)
        P(self, FadeIn(L("out", 4.7, 0.4)), rt=0.3)
        until(self, "model's memory")
        mem.shift([2.6, -0.9, 0])                   # the big circle's centre, not the group's
        P(self, FadeIn(mem), rt=0.25)
        P(self, mem.animate.shift([2.1, -0.4, 0]), rt=0.3)
        P(self, Create(cross(4.7, -1.3, s=0.32)), rt=0.22)
        finish(self)


class B11_FirstPiece(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        DK = Iso(-1.0, -1.35, 0.62)
        self.add(docs(DK), L("Actions docs", -1.1, -2.35))
        until(self, "my three questions plus two more")
        cards = VGroup(*[qcard(-5.0, y, 1.45, 0.72) for y in (2.0, 1.0, 0.0, -1.0, -2.0)])
        P(self, LaggedStart(*[FadeIn(c, shift=RIGHT * 0.6) for c in cards], lag_ratio=0.2), rt=0.8)
        until(self, "checking whether", lead=0.45)
        scan = Line([-2.75, 0.6, 0], [0.55, 0.6, 0], color=TERRA, stroke_width=6)
        P(self, Create(scan), rt=0.2)
        P(self, scan.animate.shift(DOWN * 2.2), rt=0.4)
        P(self, FadeOut(scan), rt=0.2)
        until(self, "the top three")
        slots = VGroup(*[RoundedRectangle(width=2.6, height=0.66, corner_radius=0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([2.7, y, 0]) for y in (1.75, 0.95, 0.15)])
        P(self, LaggedStart(*[GrowFromCenter(s) for s in slots], lag_ratio=0.2), rt=0.6)
        P(self, FadeIn(L("top 3", 2.7, 2.55)), rt=0.3)
        until(self, "A dated results file")
        plank = Rectangle(width=3.4, height=0.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([4.3, -2.15, 0])
        P(self, GrowFromEdge(plank, LEFT), rt=0.3)
        res = slip(4.3, -1.45, 1.4, 1.1, n=2)
        res.shift(UP * 4)
        P(self, res.animate.shift(DOWN * 4), rt=0.5, rf=ease_in, add=[res])
        P(self, FadeIn(L("results", 4.3, -2.7)), rt=0.3)
        finish(self)


class B12_Risk(Scene):
    def construct(self):
        self.add(tag(SKETCH))
        q = qcard(-4.85, 0.35, 1.9, 1.15)
        DK = Iso(3.15, -1.55, 0.7)
        d = docs(DK)
        self.add(q, d, L("Actions docs", 3.05, -2.55))
        until(self, "search missing")
        lane1 = Line([-3.5, 0.55, 0], [1.25, 0.45, 0], color="#9C8462", stroke_width=7)   # deep kraft: an ink cable fuses its ends into one text blob
        P(self, Create(lane1), rt=0.6)
        P(self, FadeIn(L("keyword", -1.1, 1.0)), rt=0.3)
        until(self, "missed two of my three")
        wrong = d[1][1]
        P(self, wrong.animate.shift(UP * 1.25 + LEFT * 0.2), rt=0.5)
        P(self, Create(cross(5.2, 1.4, s=0.3)), rt=0.4)
        until(self, "mine starts the same way")
        P(self, Indicate(lane1, color=None, scale_factor=1.04), rt=0.5)
        until(self, "matches by meaning")
        lane2 = ArcBetweenPoints([-3.5, 0.05, 0], [1.45, -1.25, 0], angle=0.45, color=DIM, stroke_width=6)
        P(self, Create(lane2), rt=0.6)
        P(self, FadeIn(L("meaning", -1.1, -1.55)), rt=0.3)
        ghost = Rectangle(width=1.5, height=0.95, fill_color=STAGE, fill_opacity=1, stroke_color=DIM, stroke_width=4).move_to([5.25, -0.55, 0])
        P(self, FadeIn(ghost, shift=UP * 0.4), rt=0.4)
        finish(self)


class B13_Why(Scene):
    def construct(self):
        self.add(tag(REPOS))
        until(self, "C I pipelines")
        boxes = VGroup(*[repo_box(Iso(x, -0.75, 0.48)) for x in (-4.6, -3.1, -1.6)])
        for bx in boxes:
            bx.shift(UP * 4)
        P(self, LaggedStart(*[bx.animate.shift(DOWN * 4) for bx in boxes], lag_ratio=0.25), rt=0.8, rf=ease_in, add=[boxes])
        P(self, FadeIn(L("have", -3.1, -1.75)), rt=0.3)
        until(self, "three public repos")
        P(self, Create(check(-3.1, 1.75, s=0.3, w=9)), rt=0.4)
        NI = Iso(3.55, -0.75, 0.48)
        lens = VGroup(Circle(radius=0.55, stroke_color=DIM, stroke_width=6, fill_opacity=0).move_to([1.9, 0.35, 0]),
                      Line([2.3, -0.05, 0], [2.75, -0.55, 0], color=DIM, stroke_width=8))
        blk = outline_box(NI, 0, 0, 0, 1.5, 1.5, 0.85)
        tray = VGroup(Rectangle(width=1.6, height=0.32, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([5.2, -0.55, 0]),
                      *[Rectangle(width=0.36, height=0.8, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([4.7 + i * 0.5, 0.05, 0]) for i in range(3)])
        until(self, "Building search")
        P(self, Create(lens), rt=0.4)
        until(self, "running a local model")
        P(self, Create(blk), rt=0.4)
        until(self, "measuring answers")
        P(self, Create(tray), rt=0.4)
        P(self, FadeIn(L("new", 3.55, -1.75)), rt=0.3)
        until(self, "It interests me")
        sparks = VGroup(*[Dot(p, radius=0.09, color=TERRA) for p in ([1.9, 0.35, 0], [3.55, 0.75, 0], [5.2, 0.75, 0])])
        P(self, LaggedStart(*[GrowFromCenter(s) for s in sparks], lag_ratio=0.25), rt=0.6)
        until(self, "explore it further")
        P(self, Indicate(VGroup(lens, blk, tray, sparks), color=None, scale_factor=1.05), rt=0.6)
        finish(self)


class B14_Exists(Scene):
    def construct(self):
        self.add(tag(REPOS))
        until(self, "three earlier repos")
        boxes = VGroup(*[repo_box(Iso(x, 0.75, 0.4)) for x in (-4.8, -3.6, -2.4)])
        P(self, FadeIn(boxes, shift=DOWN * 0.4), rt=0.4)
        P(self, FadeIn(L("exists", -3.3, 2.65)), rt=0.3)
        until(self, "six dated screenshots")
        frames = VGroup(*[window(x, y, 0.95, 0.62) for y in (-0.35, -1.15) for x in (-4.7, -3.6, -2.5)])
        P(self, LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.12), rt=0.5)
        until(self, "the brief")
        brief = slip(-1.05, -0.75, 1.1, 1.45, n=3, dot=False)
        P(self, FadeIn(brief, shift=UP * 0.3), rt=0.3)
        until(self, "Everything else")
        WI = Iso(1.55, -0.9, 0.5)
        outs = VGroup(outline_box(WI, 0, 0, 0, 1.4, 1.4, 0.8),
                      outline_box(Iso(3.2, -0.9, 0.5), 0, 0, 0, 1.4, 1.7, 0.18),
                      Rectangle(width=1.0, height=1.3, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([4.75, -0.3, 0]),
                      VGroup(*[Rectangle(width=0.3, height=0.75, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([5.45 + i * 0.0, -0.3, 0]) for i in range(1)]))
        P(self, LaggedStart(*[Create(o) for o in outs], lag_ratio=0.2), rt=0.8)
        P(self, FadeIn(L("will exist", 3.4, 2.65)), rt=0.3)
        finish(self)


class BOUT_Outro(Scene):
    def construct(self):
        d = docs(Iso(0.3, 0.55, 0.42)); d.shift(UP * 3.5); self.add(d)
        P(self, d.animate.shift(DOWN * 3.5), rt=0.7, rf=ease_in)
        P(self, FadeIn(T("Actions Docs Q&A", 72).move_to([0, -0.6, 0])), rt=0.45)
        P(self, FadeIn(T("Final Project Pitch", 44).move_to([0, -1.45, 0])), rt=0.35)
        P(self, FadeIn(T("Yash Saraf", 40).move_to([0, -2.15, 0])), rt=0.35)
        until(self, "by Yash Saraf")
        P(self, GrowFromCenter(Dot([0, -2.8, 0], radius=0.1, color=TERRA)), rt=0.3)
        finish(self)
