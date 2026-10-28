"""
iso_kit.py — the show-tell drawing kit. PASTE this block at the top of a reel's scenes.py;
do not import it (Gate A copies only scenes.py into its sandbox).

Drawn isometric objects in the Claude palette: cardboard boxes (closed, open, taped), dark
MCP blocks with ports, flat skill pages, server stacks with lights, checks, a cursor, pills,
and a WRITING KIT (quill, inkwell, paper, scribble lines, branching outline + the write_lines /
grow_tree animations that make the quill write). A PERSON IS NEVER AN ICON: `professor_bear(ratio, …)`
places a random Professor Bear portrait of the right aspect ratio (PROFESSOR BEAR LAW).
Pacing helpers read the reel's beat_sheet.json so scenes wait for their spoken phrase.

Every rule in ../SKILL.md "DRAWING LAWS" is already obeyed by these primitives; keep it that
way when you add one (label beside, never inside; terracotta never under text; dim greys
with gaps for chart blocks; type floor 32).
"""
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


TYPE_FLOOR = 44   # feedback 2026-10-12: enlarge small text; no label below 44


def T(s, size=44, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=max(size, TYPE_FLOOR), weight="BOLD" if bold else "NORMAL")


def M(s, size=40, color=INK):
    """Monospace for REAL program output, copied verbatim from evidence/ logs."""
    return Text(s, font="Menlo", color=color, font_size=size)


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


# ═════════════════════════════ Seeded Faults pitch — helpers ═════════════════════════════
KRAFT_EDGE = "#9C8462"
_MID_MARGIN = 0.4


def _mid(self):
    return _TARGET.get(type(self).__name__.split("_")[0], 0) / 2.0


def go(self, *anims, rt=0.8, **kw):
    """Play, but never across the clip midpoint (GATE T / Gate V sample there)."""
    mid, t = _mid(self), _elapsed(self)
    if mid and t < mid + _MID_MARGIN and t + rt > mid - _MID_MARGIN:
        self.wait(mid + _MID_MARGIN - t)
    self.play(*anims, run_time=rt, **kw)


def at(self, phrase, *anims, rt=0.8, **kw):
    until(self, phrase)
    go(self, *anims, rt=rt, **kw)


def data_table(iso, x0=0.0, y0=0.0, w=3.2, d=2.2, rows=5):
    """The film's data table: a kraft slab with ghost row lines and one darker header line."""
    slab = iso.box(x0, y0, 0, w, d, 0.35)
    z = 0.35
    lines = VGroup(*[Line(iso.p(x0 + 0.2, y0 + d * (i + 1) / (rows + 1), z), iso.p(x0 + w - 0.2, y0 + d * (i + 1) / (rows + 1), z),
                          color=BOX_IN2, stroke_width=5) for i in range(rows)])
    return VGroup(slab, lines)


def test_stack(iso, x0, y0, n=3):
    return VGroup(*[iso.page(x0, y0, 0.12 * i) for i in range(n)])


def badge(x, y, r=0.85):
    ring = Circle(radius=r, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    mark = check(x - 0.12, y + 0.05, s=r * 0.42, color=INK, w=10)
    return VGroup(ring, mark)


def crack(x, y, r=0.85):
    pts = [[x - 0.2, y + r, 0], [x + 0.05, y + 0.35, 0], [x - 0.15, y + 0.05, 0], [x + 0.12, y - 0.35, 0], [x - 0.05, y - r, 0]]
    return VMobject(stroke_color=INK, stroke_width=7).set_points_as_corners(pts)


def scoreboard(x, y, w=3.4, rows=4, filled=None):
    """A flat card with rows: grey bar (the fault) + an empty status circle. `filled` = row indices to tick."""
    card = RoundedRectangle(width=w, height=0.55 * rows + 0.5, corner_radius=0.12, fill_color=CARD, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    top = y + (0.55 * rows + 0.5) / 2 - 0.5
    bars = VGroup(*[RoundedRectangle(width=w * 0.55, height=0.2, corner_radius=0.1, fill_color=BAR2, fill_opacity=1,
                                     stroke_width=0).move_to([x - w * 0.12, top - 0.55 * i, 0]) for i in range(rows)])
    dots = VGroup(*[Circle(radius=0.14, stroke_color=BAR1, stroke_width=4).move_to([x + w * 0.32, top - 0.55 * i, 0])
                    for i in range(rows)])
    return VGroup(card, bars, dots)


def arrow(a, b, color=KRAFT_EDGE):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.15, color=color, stroke_width=6, max_tip_length_to_length_ratio=0.18)


def stamp(word, x, y):
    """The honesty label for constructed material: ink type beside a grey rule."""
    t = T(word, 48, INK, bold=True).move_to([x, y, 0])
    rule = Line([x - t.width / 2, y - 0.32, 0], [x + t.width / 2, y - 0.32, 0], color=BAR1, stroke_width=4)
    return VGroup(t, rule)


# ═════════════════════════════ scenes ═════════════════════════════
class B00_TableAndTests(Scene):
    def construct(self):
        iso = Iso(-2.6, -1.4, 1.0)
        table = data_table(iso, 0, 0)
        tl = T("table", 40).move_to([-2.6, -2.75, 0])
        go(self, FadeIn(table, shift=DOWN * 0.3), rt=0.9)
        go(self, FadeIn(tl), rt=0.5)
        iso2 = Iso(2.6, -1.0, 1.0)
        tests = test_stack(iso2, 0, 0, 3)
        tt = T("tests", 40).move_to([2.6, -2.75, 0])
        at(self, "Claude Code writes", LaggedStart(*[FadeIn(p, shift=DOWN * 0.4) for p in tests], lag_ratio=0.3), rt=1.2)
        go(self, FadeIn(tt), rt=0.5)
        q = T("?", 120, INK, bold=True).move_to([2.6, 1.6, 0])
        at(self, "actually catch anything", GrowFromCenter(q), rt=0.6)
        finish(self)


class B01_PlannedRepo(Scene):
    def construct(self):
        iso = Iso(0.0, -2.4, 1.0)
        back, front = iso.open_box(-1.6, -1.6, 0, 3.2, 3.2, 1.4)
        lab = T("planned repo", 40).move_to([-4.6, -1.2, 0])
        st = stamp("CONSTRUCTED", 3.4, 2.8)
        go(self, FadeIn(back), FadeIn(front), rt=0.8)
        go(self, FadeIn(lab), FadeIn(st), rt=0.5)
        parts = [
            ("plants faults", iso.page(-1.3, -1.3, 2.6, 1.0, 1.2)),
            ("dbt project", iso.mcp(0.2, -1.2, 2.6, 1.1, 1.1, 0.6)),
            ("prompt contract", iso.page(-1.3, 0.2, 2.6, 1.0, 1.2)),
            ("evaluation log", iso.page(0.3, 0.3, 2.6, 1.0, 1.2)),
        ]
        for phrase, m in parts:
            m.set_z_index(1)
            at(self, phrase, FadeIn(m, shift=DOWN * 0.5), rt=0.6)
            go(self, m.animate.shift(DOWN * 1.9), rt=0.5, rate_func=ease_in)
        mark = T("one test, by hand", 44).move_to([4.3, -2.6, 0])
        tick = check(4.3, -1.8, s=0.3, color=TERRA, w=9)
        at(self, "one small test", FadeIn(mark), GrowFromCenter(tick), rt=0.6)
        finish(self)


class B02_CrackedPass(Scene):
    def construct(self):
        iso = Iso(-2.8, -1.6, 1.0)
        table = data_table(iso, 0, 0)
        go(self, FadeIn(table), rt=0.6)
        b = badge(2.4, 0.6, 1.0)
        bl = T("all passed", 40).move_to([2.4, -1.0, 0])
        at(self, "They pass on clean data", GrowFromCenter(b), rt=0.7)
        go(self, FadeIn(bl), rt=0.5)
        c = crack(2.4, 0.6, 1.0)
        at(self, "never failed", Create(c), rt=0.8)
        q = T("?", 96, INK, bold=True).move_to([4.6, 1.6, 0])
        at(self, "That's exactly what I want to measure", GrowFromCenter(q), rt=0.5)
        finish(self)


class B03_FiftyCaught(Scene):
    """Real output from evidence/2026-10-09-first-planted-fault/output/ (ge_fault.txt, dbt_clean.txt, dbt_faulted.txt)."""
    def construct(self):
        head = T("real output · 2026-10-09", 48, INK, bold=True).move_to([0, 2.95, 0])
        rule = Line([-6.0, 2.45, 0], [6.0, 2.45, 0], color=BAR1, stroke_width=4)
        go(self, FadeIn(head), Create(rule), rt=0.6)
        def row(y, tool, cond, out):
            g = VGroup()
            if tool:
                g.add(T(tool, 44, bold=True).move_to([0, y, 0]).align_to([-6.0, 0, 0], LEFT))
            g.add(T(cond, 44).move_to([0, y, 0]).align_to([-3.7, 0, 0], LEFT))
            g.add(M(out, 40).move_to([0, y, 0]).align_to([-0.9, 0, 0], LEFT))
            return g
        gx_clean = row(1.65, "GX 1.24", "clean", "unexpected_count=0")
        gx_fault = row(0.85, "", "50 planted", "unexpected_count=50")
        sep = Line([-6.0, 0.25, 0], [6.0, 0.25, 0], color=BAR2, stroke_width=3)
        dbt_clean = row(-0.35, "dbt", "clean", "PASS")
        dbt_fault = row(-1.15, "", "50 planted", "FAIL 50")
        at(self, "In Great Expectations", FadeIn(gx_clean), rt=0.6)
        at(self, "I planted fifty", FadeIn(gx_fault), rt=0.6)
        hit = check(-5.45, 0.9, s=0.28, color=TERRA, w=9)
        at(self, "my check caught all fifty", Create(hit), rt=0.5)
        hit2 = check(-5.45, -1.1, s=0.28, color=TERRA, w=9)
        at(self, "dbt did the same", Create(sep), FadeIn(dbt_clean), FadeIn(dbt_fault), Create(hit2), rt=0.7)
        dx = T("dbt-expectations: still hand-written", 44).move_to([0, -2.25, 0]).align_to([-6.0, 0, 0], LEFT)
        at(self, "dbt-expectations package", FadeIn(dx), rt=0.6)
        ring = Circle(radius=0.28, stroke_color=BAR1, stroke_width=5).move_to([-5.7, -3.0, 0])
        mq = T("what was missed: not reported", 44).move_to([0, -3.0, 0]).align_to([-5.2, 0, 0], LEFT)
        at(self, "Nothing told me", GrowFromCenter(ring), FadeIn(mq), rt=0.6)
        finish(self)


class B04_ReadmeMock(Scene):
    def construct(self):
        panel = RoundedRectangle(width=7.4, height=4.6, corner_radius=0.15, fill_color=CARD, fill_opacity=1,
                                 stroke_color=INK, stroke_width=5).move_to([-0.6, -0.2, 0])
        bar = Rectangle(width=7.4, height=0.5, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-0.6, 1.85, 0])
        lab = T("README", 40).move_to([-0.6, 2.8, 0])
        st = stamp("CONSTRUCTED", 3.4, 2.8)
        go(self, FadeIn(panel), FadeIn(bar), rt=0.6)
        go(self, FadeIn(lab), FadeIn(st), rt=0.5)
        rows = VGroup()
        for i in range(5):
            y = 1.1 - i * 0.62
            rows.add(VGroup(
                RoundedRectangle(width=3.6, height=0.22, corner_radius=0.11, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([-2.0, y, 0]),
                Circle(radius=0.15, stroke_color=BAR1, stroke_width=4).move_to([1.2, y, 0]),
                RoundedRectangle(width=1.2, height=0.22, corner_radius=0.11, fill_color=BAR3, fill_opacity=1, stroke_width=0).move_to([2.3, y, 0])))
        at(self, "see one table", LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), rt=1.0)
        run = pill(4.8, -1.6, 1.6, 0.62, fill=DARK_TOP)
        rl = T("1 command", 34).move_to([4.8, -2.4, 0])
        cur = cursor(5.3, -1.3)
        at(self, "one command reruns", FadeIn(run), FadeIn(rl), rt=0.5)
        go(self, FadeIn(cur), rt=0.4)
        finish(self)


class B05_Proof(Scene):
    def construct(self):
        contract = paper(-4.4, 0.6, 1.8, 2.3)
        lines = scribbles_on(contract, n=4, color=BOX_IN2, sw=6)
        lc = T("contract", 38).move_to([-4.4, -1.1, 0])
        go(self, FadeIn(contract), rt=0.5)
        at(self, "a written prompt contract", Create(lines), FadeIn(lc), rt=0.7)
        lens = VGroup(Circle(radius=0.75, stroke_color=INK, stroke_width=8, fill_color=CARD, fill_opacity=1).move_to([-1.3, 0.8, 0]),
                      Line([-0.78, 0.27, 0], [-0.2, -0.3, 0], color=INK, stroke_width=12))
        lv = T("verify", 38).move_to([-1.3, -1.1, 0])
        at(self, "checking Claude's work", GrowFromCenter(lens), FadeIn(lv), rt=0.6)
        loop = VGroup(Arc(radius=0.75, start_angle=0.4, angle=5.2, color=INK, stroke_width=8).move_to([1.8, 0.7, 0]))
        tip = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(0.18).rotate(-0.4).move_to([2.48, 1.08, 0])
        lr = T("rerun", 38).move_to([1.8, -1.1, 0])
        at(self, "an evaluation anyone can rerun", Create(loop), FadeIn(tip), FadeIn(lr), rt=0.7)
        iso = Iso(4.6, -0.3, 1.0)
        log = test_stack(iso, -0.5, -0.6, 2)
        ll = T("log", 38).move_to([4.6, -1.6, 0])
        arr = arrow((2.8, 0.4), (3.7, 0.4))
        at(self, "the proof will be the log", Create(arr), FadeIn(log, shift=DOWN * 0.3), FadeIn(ll), rt=0.7)
        finish(self)


class B06_Scope(Scene):
    def construct(self):
        tray = RoundedRectangle(width=7.0, height=4.6, corner_radius=0.2, fill_color="#ECE8DD", fill_opacity=1,
                                stroke_color=KRAFT_EDGE, stroke_width=5).move_to([-2.4, -0.3, 0])
        li = T("in", 40).move_to([-2.4, 2.65, 0])
        go(self, FadeIn(tray), FadeIn(li), rt=0.6)
        iso = Iso(-4.4, -1.9, 0.75)
        table = data_table(iso, 0, 0, 3.0, 2.0, 4)
        at(self, "New York City taxi trips", FadeIn(table), rt=0.6)
        faults = VGroup(*[Dot([-1.6 + 0.32 * (i % 4), 1.1 - 0.32 * (i // 4), 0], radius=0.09, color=TERRA) for i in range(16)])
        fl = T("faults", 34).move_to([-1.1, 1.75, 0])
        at(self, "fault types", LaggedStart(*[GrowFromCenter(d) for d in faults], lag_ratio=0.05), FadeIn(fl), rt=0.8)
        iso2 = Iso(-0.4, -1.9, 0.8)
        tests = test_stack(iso2, 0, 0, 2)
        at(self, "tests written by Claude", FadeIn(tests, shift=DOWN * 0.3), rt=0.5)
        lo = T("out", 40).move_to([4.6, 2.65, 0])
        iso3 = Iso(4.6, 0.4, 0.8)
        srv, lights = iso3.server(-0.7, -0.7, 0, 1.4, 1.4, 0.4, 3)
        strike = Line([3.5, 2.0, 0], [5.7, -0.4, 0], color=INK, stroke_width=9)
        wl = T("warehouse", 34).move_to([4.6, -1.0, 0])
        at(self, "It won't repair data", FadeIn(lo), FadeIn(srv), FadeIn(wl), rt=0.6)
        go(self, Create(strike), rt=0.4)
        one = VGroup(Circle(radius=0.42, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.1, 0.6, 0]),
                     T("1", 36, INK, bold=True).move_to([0.1, 0.6, 0]))
        at(self, "The first thing I'll build", GrowFromCenter(one[0]), FadeIn(one[1]), rt=0.5)
        sb = scoreboard(4.6, -2.3, 2.6, 2)
        at(self, "what was caught", FadeIn(sb), rt=0.5)
        finish(self)


class B07_Balance(Scene):
    def construct(self):
        post = Line([0, -2.4, 0], [0, 1.2, 0], color=KRAFT_EDGE, stroke_width=12)
        base = Polygon([-1.2, -2.6, 0], [1.2, -2.6, 0], [0.6, -2.2, 0], [-0.6, -2.2, 0],
                       fill_color=DARK_TOP, fill_opacity=1, stroke_width=0)
        beam = Line([-3.4, 1.2, 0], [3.4, 1.2, 0], color=KRAFT_EDGE, stroke_width=12)
        go(self, Create(post), FadeIn(base), Create(beam), rt=0.8)
        def pan(x):
            return VGroup(Line([x, 1.2, 0], [x - 0.9, -0.3, 0], color=KRAFT_EDGE, stroke_width=4),
                          Line([x, 1.2, 0], [x + 0.9, -0.3, 0], color=KRAFT_EDGE, stroke_width=4),
                          Arc(radius=1.0, start_angle=PI, angle=PI, color=KRAFT_EDGE, stroke_width=9).move_to([x, -0.6, 0]))
        lp, rp = pan(-3.4), pan(3.4)
        ml = T("missed", 40).move_to([-3.4, -2.1, 0])
        fa = T("false alarms", 40).move_to([3.4, -2.1, 0])
        at(self, "catch almost nothing", FadeIn(lp), FadeIn(ml), rt=0.6)
        at(self, "flag perfectly clean data", FadeIn(rp), FadeIn(fa), rt=0.6)
        lw = VGroup(*[Dot([-3.7 + 0.3 * i, -0.75, 0], radius=0.12, color=TERRA) for i in range(3)])
        rw = VGroup(*[Dot([3.1 + 0.3 * i, -0.75, 0], radius=0.12, color=BAR1) for i in range(3)])
        at(self, "count false alarms", LaggedStart(*[GrowFromCenter(d) for d in [*lw, *rw]], lag_ratio=0.1), rt=0.7)
        lock_body = RoundedRectangle(width=0.9, height=0.7, corner_radius=0.1, fill_color=DARK_TOP, fill_opacity=1,
                                     stroke_width=0).move_to([5.3, 2.3, 0])
        shackle = Arc(radius=0.3, start_angle=0, angle=PI, color=INK, stroke_width=9).move_to([5.3, 2.8, 0])
        ll = T("fault list locked", 34).move_to([2.6, 2.4, 0])
        at(self, "lock the fault list", FadeIn(lock_body), Create(shackle), FadeIn(ll), rt=0.6)
        finish(self)


class B08_TwoColumns(Scene):
    def construct(self):
        la = T("already do", 42).move_to([-3.4, 2.7, 0])
        lb = T("learning", 42).move_to([3.4, 2.7, 0])
        div = Line([0, 2.6, 0], [0, -2.8, 0], color=BAR1, stroke_width=4)
        go(self, FadeIn(la), Create(div), rt=0.6)
        iso = Iso(-3.4, -0.4, 1.0)
        db = iso.server(-0.7, -0.7, 0, 1.4, 1.4, 0.42, 3)[0]
        repo = T("DMDD_FinalProject", 34).move_to([-3.4, -2.2, 0])
        at(self, "Crime Rate Management System", FadeIn(db, shift=DOWN * 0.3), FadeIn(repo), rt=0.7)
        tick = check(-1.6, 1.4, s=0.3, color=TERRA, w=9)
        at(self, "its own testing script", Create(tick), rt=0.4)
        pages = VGroup(paper(2.1, 0.75, 1.2, 1.5, -0.08), paper(3.4, 0.85, 1.2, 1.5, 0.0), paper(4.7, 0.75, 1.2, 1.5, 0.08))
        names = VGroup(T("prompt contracts", 44).move_to([3.4, -1.15, 0]), T("evaluation", 44).move_to([3.4, -1.85, 0]),
                       T("fault injection", 44).move_to([3.4, -2.55, 0]))
        at(self, "The new part for me", FadeIn(lb), LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in pages], lag_ratio=0.25), rt=0.9)
        go(self, FadeIn(names), rt=0.5)
        finish(self)


class B09_Close(Scene):
    def construct(self):
        b = badge(-3.0, 0.4, 1.1)
        c = crack(-3.0, 0.4, 1.1)
        title = T("Seeded Faults", 56, INK, bold=True).move_to([0, 2.7, 0])
        go(self, FadeIn(b), Create(c), FadeIn(title), rt=0.7)
        sb = scoreboard(2.6, -0.1, 4.0, 5)
        at(self, "It isn't built yet", FadeIn(sb), rt=0.6)
        nl = T("next: fault script", 36).move_to([2.6, -2.5, 0])
        at(self, "Next up", FadeIn(nl), rt=0.5)
        finish(self)


class BOUT_Title(Scene):
    def construct(self):
        title = T("Seeded Faults", 72, INK, bold=True).move_to([0, 0.6, 0])
        rule = Line([-2.6, -0.2, 0], [2.6, -0.2, 0], color=BAR1, stroke_width=5)
        name = T("Atharva C", 44).move_to([0, -0.9, 0])
        dot = Dot([3.0, -0.2, 0], radius=0.09, color=TERRA)
        self.play(FadeIn(title), Create(rule), run_time=0.5)
        self.play(FadeIn(name), GrowFromCenter(dot), run_time=0.4)
        finish(self)
