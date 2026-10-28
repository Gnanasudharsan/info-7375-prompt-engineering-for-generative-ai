"""
scenes.py — BiteCheck pitch film v2 (Omkar Salian, INFO 7375 Fall 2026, final project pitch; revised 2026-10-21).

Show-tell format: one drawn picture per beat, minimal labels, the narration explains.
The drawing kit below is pasted from brutalist.art skills/make/show-tell/templates/iso_kit.py
(the Professor Bear portrait helpers are removed: the assignment forbids the instructor's persona).
Every beat carries a corner honesty tag: REAL (exists / ran / was read on 2026-10-12) or
PROPOSED (a constructed drawing of something not built yet).
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


# ═════════════════════════════ BiteCheck pitch: helpers ═════════════════════════════
# Honesty tag in the top-left corner of every beat: REAL (it exists and ran / was read on the
# stated date) or PROPOSED (a constructed drawing of something that does not exist yet).
GUARD = 0.34      # keep every animation this far off the clip midpoint (GATE T / Gate V sample there)


def _bid(self):
    return type(self).__name__.split("_")[0]


def P(self, *anims, rt=0.8, **kw):
    """self.play, but never across the clip midpoint."""
    d = _TARGET.get(_bid(self), 0)
    if d:
        t = _elapsed(self); m = d / 2
        if t < m + GUARD and t + rt > m - GUARD:
            self.wait(m + GUARD - t)
    anims = [FadeIn(a) if isinstance(a, Mobject) else a for a in anims]   # a bare mobject means "fade it in"
    self.play(*anims, run_time=rt, **kw)


def tag(self, kind):
    s = {"REAL": "REAL · ran 2026-10-12",
         "READ": "REAL · read 2026-10-12",
         "STATUS": "STATUS · 2026-10-22",
         "MIXED": "REAL · docs read 10-12 · Stryker ran 10-13",
         "SELF": "SELF-REPORT · PR #37 is public",
         "PROPOSED": "PROPOSED · constructed drawing",
         "WHO": "WHO · the person building it",
         "ANALOGY": "ANALOGY · constructed drawing",
         "CIRAN": "REAL · CI ran 2026-10-22"}[kind]
    t = T(s, 32)
    t.move_to(np.array([-6.1 + t.width / 2, 3.0, 0]))
    self.add(t)
    return t


def lab(s, x, y, size=34):
    return T(s, size).move_to(np.array([x, y, 0]))


def tpage(x, y, w=1.3, h=1.6, n=3, amp=0.07):
    """A test page: flat paper with scribble lines (amp > 0.07 keeps small pages' lines over GATE T's floor)."""
    pg = paper(x, y, w, h)
    iw = w - 0.44
    lines = VGroup(*[scribble(x - iw / 2, y + h / 2 - 0.32 - i * 0.3, iw * (0.62 if i == n - 1 else 1.0), amp=amp)
                     for i in range(n)])
    return VGroup(pg, lines)


def xmark(x, y, s=0.28, color=INK, w=8):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def lock(x, y, s=0.5):
    body = RoundedRectangle(width=s * 1.3, height=s, corner_radius=0.08, fill_color=BOX_R, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    shackle = Arc(radius=s * 0.42, start_angle=0, angle=PI, color=INK, stroke_width=6).move_to([x, y + s * 0.62, 0])
    hole = Dot([x, y, 0], radius=0.07, color=INK)
    return VGroup(shackle, body, hole)


# ═════════════════════════════ scenes, one per beat (v2) ═════════════════════════════

def alarm(x, y, r=0.7):
    """A ceiling smoke alarm: kraft disc, ink ring, inner ring and an indicator light (returned separately)."""
    disc = Circle(radius=r, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    inner = Circle(radius=r * 0.55, fill_opacity=0, stroke_color="#9C8462", stroke_width=4).move_to([x, y, 0])
    light = Dot([x, y, 0], radius=0.1, color=GHOST)
    return VGroup(disc, inner), light


def puff(x, y, s=1.0):
    return VGroup(*[Circle(radius=r * s, fill_color=GHOST, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([x + dx * s, y + dy * s, 0])
                    for r, dx, dy in ((0.32, 0, 0), (0.24, 0.34, 0.1), (0.22, -0.3, 0.12), (0.2, 0.08, 0.3))])


def beeps(x, y, r0=0.95, n=3):
    return VGroup(*[Arc(radius=r0 + i * 0.3, start_angle=-PI / 4, angle=PI / 2, color=INK, stroke_width=6).move_arc_center_to([x, y, 0])
                    for i in range(n)])


class B00_Who(Scene):
    def construct(self):
        tag(self, "WHO")
        card = paper(-2.4, 0.3, 6.2, 3.0)
        name = T("Omkar Salian", 64, bold=True).move_to([-2.4, 0.9, 0])
        line = lab("MS Software Engineering", -2.4, -0.05, 36)
        uni = lab("Northeastern University", -2.4, -0.7, 36)
        P(self, FadeIn(card, shift=UP * 0.3), FadeIn(name), FadeIn(line), FadeIn(uni), rt=1.0)
        until(self, "This is my final project")
        proj = lab("final project: BiteCheck", -2.4, -2.05, 38)
        P(self, FadeIn(proj), rt=0.5)
        until(self, "I'm building it myself")
        iso = Iso(4.0, -0.6, 0.8)
        base = iso.box(-1.0, -0.7, 0, 2.0, 1.4, 0.18, DARK_TOP, DARK_L, DARK_R)
        screen = Polygon(iso.p(-1.0, 0.7, 0.18), iso.p(1.0, 0.7, 0.18), iso.p(1.0, 0.7, 1.6), iso.p(-1.0, 0.7, 1.6),
                         fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4)
        cur = Dot(iso.p(0, 0.7, 0.9), radius=0.09, color=TERRA)
        who = lab("me + Claude Code", 4.0, -1.75, 36)
        P(self, FadeIn(base), FadeIn(screen), FadeIn(who), rt=0.7)
        P(self, GrowFromCenter(cur), rt=0.3)
        finish(self)


class B01_SmokeAlarm(Scene):
    def construct(self):
        tag(self, "ANALOGY")
        ceil = Line([-6.0, 2.2, 0], [6.0, 2.2, 0], color="#9C8462", stroke_width=6)
        a1, l1 = alarm(-3.0, 1.5); a2, l2 = alarm(3.0, 1.5)
        n1, n2 = lab("smoke alarm", -3.0, 0.2, 34), lab("smoke alarm", 3.0, 0.2, 34)
        P(self, Create(ceil), FadeIn(a1), FadeIn(l1), FadeIn(a2), FadeIn(l2), FadeIn(n1), FadeIn(n2), rt=0.9)
        until(self, "blow a little smoke")
        p1, p2 = puff(-3.0, -2.2), puff(3.0, -2.2)
        P(self, FadeIn(p1), FadeIn(p2), rt=0.4)
        P(self, p1.animate.move_to([-3.0, -0.75, 0]), p2.animate.move_to([3.0, -0.75, 0]), rt=1.0)
        until(self, "If it beeps")
        b = beeps(-3.0, 1.5, 0.85, 2)
        P(self, Create(b), l1.animate.set_color(TERRA), rt=0.6)
        P(self, Create(check(-0.6, 1.5, 0.3)), FadeIn(lab("works", -0.6, 0.75, 36)), rt=0.5)
        until(self, "If it stays quiet")
        P(self, Create(xmark(5.2, 1.5, 0.3, w=9)), FadeIn(lab("broken", 5.2, 0.75, 36)), rt=0.6)
        finish(self)


class B02_TestsAreAlarms(Scene):
    def construct(self):
        tag(self, "ANALOGY")
        xs = [-4.6, -2.5, -0.4, 1.7]
        pages = VGroup(*[tpage(x, 0.6, 1.3, 1.6) for x in xs])
        lights = [Dot([x - 0.35, 1.75, 0], radius=0.11, color=GHOST) for x in xs]
        tl = lab("tests", -1.45, -0.9, 38)
        P(self, FadeIn(pages), *[FadeIn(l) for l in lights], FadeIn(tl), rt=1.0)
        until(self, "they can all pass")
        checks = [check(x + 0.4, 1.75, 0.16) for x in xs]
        P(self, *[Create(c) for c in checks], rt=0.6)
        until(self, "BiteCheck is the smoke")
        bug = VGroup(Square(0.9, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4),
                     Dot([0, 0, 0], radius=0.12, color=TERRA)).move_to([5.6, -1.2, 0])
        bl = lab("one bug, on purpose", 4.2, -2.95, 34)
        P(self, FadeIn(bug), rt=0.3)
        P(self, bug.animate.move_to([4.2, -2.0, 0]), FadeIn(bl), rt=0.8)
        until(self, "checks which tests go off")
        P(self, Create(beeps(xs[0] - 0.35, 1.75, 0.28, 1).rotate(PI, about_point=[xs[0] - 0.35, 1.75, 0])),
          Create(beeps(xs[2] - 0.35, 1.75, 0.28, 1).rotate(PI, about_point=[xs[2] - 0.35, 1.75, 0])),
          lights[0].animate.set_color(TERRA), lights[2].animate.set_color(TERRA),
          FadeOut(checks[0]), FadeOut(checks[2]), rt=0.6)
        P(self, Create(xmark(xs[0] + 0.4, 1.75, 0.16)), Create(xmark(xs[2] + 0.4, 1.75, 0.16)), rt=0.4)
        P(self, FadeIn(lab("2 caught it, 2 missed it", -1.45, -1.65, 34)), rt=0.4)
        finish(self)


class B03_Repo(Scene):
    def construct(self):
        tag(self, "PROPOSED")
        iso = Iso(0, -2.3, 0.6)
        back, front = iso.open_box(-1.4, -1.4, 0, 2.8, 2.8, 1.4)
        lbl = lab("GitHub repo", 3.3, -2.0, 38)
        P(self, FadeIn(back, shift=DOWN * 0.5), FadeIn(front, shift=DOWN * 0.5), lbl, rt=1.0)
        xs = [-4.8, -1.6, 1.6, 4.8]
        y0 = 1.75
        prompt = tpage(xs[0], y0, 1.2, 1.4, n=2, amp=0.09)
        bug = VGroup(Iso(xs[1], y0 - 0.5, 0.8).box(-0.6, -0.6, 0, 1.2, 1.2, 0.7, DARK_TOP, DARK_L, DARK_R),
                     Dot(Iso(xs[1], y0 - 0.5, 0.8).p(0, 0, 0.7), radius=0.09, color=TERRA))
        st, lights = Iso(xs[2], y0 - 0.35, 0.6).server(-0.7, -0.7, 0, n=3)
        runner = VGroup(st, lights)
        rep = VGroup(paper(xs[3], y0, 1.3, 1.5),
                     *[Rectangle(width=0.22, height=hh, fill_color=c, fill_opacity=1, stroke_width=0)
                       .move_to([xs[3] - 0.35 + i * 0.35, y0 - 0.5 + hh / 2, 0])
                       for i, (hh, c) in enumerate([(0.9, BAR1), (0.6, BAR2), (0.3, BAR1)])])
        names = ["prompt", "bugs", "runner", "report"]
        parts = [prompt, bug, runner, rep]
        labels = [lab(n, x, 0.45, 40) for n, x in zip(names, xs)]
        until(self, "a prompt that tells")
        P(self, FadeIn(parts[0], shift=UP * 0.5), FadeIn(labels[0]), rt=0.7)
        until(self, "a list of planted bugs")
        P(self, FadeIn(parts[1], shift=UP * 0.5), FadeIn(labels[1]), rt=0.7)
        until(self, "a runner")
        P(self, FadeIn(parts[2], shift=UP * 0.5), FadeIn(labels[2]), rt=0.6)
        self.play(lights.animate.set_color(TERRA), run_time=0.3)
        until(self, "one page report")
        P(self, FadeIn(parts[3], shift=UP * 0.5), FadeIn(labels[3]), rt=0.7)
        finish(self)


class B04_LoanRun(Scene):
    def construct(self):
        tag(self, "REAL")
        iso = Iso(3.8, -1.6, 0.85)
        st, lights = iso.server(-0.8, -0.8, 0, 1.6, 1.6, 0.5, 3)
        name = lab("loan API", 3.8, -2.8)
        ys = [1.5, 0.0, -1.5]
        cards = VGroup(*[paper(-4.6, y, 1.5, 1.0) for y in ys])
        texts = [lab("₹14,999", -2.4, ys[0]), lab("₹15,000", -2.4, ys[1]), lab("pay out early", -2.0, ys[2])]
        P(self, FadeIn(st), FadeIn(lights), name, FadeIn(cards), *[FadeIn(t) for t in texts], rt=1.0)
        self.play(lights.animate.set_color(TERRA), run_time=0.3)
        arrows = [Arrow([-0.6, y, 0], [1.6, y * 0.4 + 0.2, 0], color=DIM, stroke_width=5, buff=0) for y in ys]
        until(self, "was rejected")
        P(self, Create(arrows[0]), rt=0.5)
        P(self, Create(xmark(-4.6, ys[0], 0.25)), rt=0.4)
        until(self, "got an offer")
        P(self, Create(arrows[1]), rt=0.5)
        P(self, Create(check(-4.65, ys[1] + 0.05, 0.22)), rt=0.4)
        until(self, "was refused")
        P(self, Create(arrows[2]), rt=0.5)
        bar = Rectangle(width=0.9, height=0.18, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([-4.6, ys[2], 0])
        code = lab("409", -4.6, ys[2] - 0.75, 32)
        P(self, FadeIn(bar), FadeIn(code), rt=0.4)
        stack = lab("TypeScript · Express", 3.8, 1.7, 34)
        P(self, FadeIn(stack), rt=0.4)
        finish(self)


class B05_PipelineA(Scene):
    def construct(self):
        tag(self, "PROPOSED")
        s1 = lab("1. rules + mutants", -3.6, 2.25, 38)
        rules = tpage(-4.6, 0.3, 1.6, 2.0)
        rl = lab("rules R1, R2", -4.6, -1.05, 34)
        P(self, FadeIn(s1), FadeIn(rules), FadeIn(rl), rt=0.8)
        until(self, "A mutant is a copy")
        mut = VGroup(Square(1.1, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4),
                     Dot([0, 0, 0], radius=0.12, color=TERRA)).move_to([-1.6, 0.3, 0])
        ml = lab("mutant: 15,000 → 1,500", -1.6, -1.7, 34)
        P(self, FadeIn(mut, shift=DOWN * 0.3), FadeIn(ml), rt=0.6)
        until(self, "Step two")
        s2 = lab("2. Claude writes tests", 3.4, 2.25, 38)
        tests = [tpage(x, 0.3, 1.2, 1.5) for x in (2.2, 3.7, 5.2)]
        P(self, FadeIn(s2), *[FadeIn(t) for t in tests], rt=0.7)
        until(self, "must name the rule")
        cab = CubicBezier(np.array([1.5, 1.0, 0]), np.array([0.2, 1.9, 0]), np.array([-2.6, 1.9, 0]), np.array([-3.7, 1.0, 0]),
                          color="#9C8462", stroke_width=6)
        end = Dot([-3.7, 1.0, 0], radius=0.1, color=TERRA)
        tag2 = lab("each test names a rule", 3.7, -1.05, 34)
        P(self, Create(cab), FadeIn(tag2), rt=0.8)
        P(self, GrowFromCenter(end), rt=0.3)
        finish(self)


class B06_PipelineB(Scene):
    def construct(self):
        tag(self, "PROPOSED")
        s3 = lab("3. run on both", 0, 2.25, 38)
        st1, li1 = Iso(-3.6, -0.4, 0.75).server(-0.7, -0.7, 0, 1.4, 1.4, 0.45, 3)
        st2, li2 = Iso(3.0, -0.4, 0.75).server(-0.7, -0.7, 0, 1.4, 1.4, 0.45, 3)
        l1, l2 = lab("real API", -3.6, -1.25, 34), lab("mutant", 3.0, -1.25, 34)
        spark = Dot(Iso(3.0, -0.4, 0.75).p(0, 0, 1.4), radius=0.12, color=TERRA)
        P(self, FadeIn(s3), FadeIn(st1), FadeIn(li1), FadeIn(st2), FadeIn(li2), FadeIn(l1), FadeIn(l2), rt=0.9)
        P(self, GrowFromCenter(spark), rt=0.3)
        until(self, "where they must all pass")
        P(self, *[Create(check(-5.2 + i * 0.55, 1.75, 0.15)) for i in range(4)], FadeIn(lab("all pass", -4.4, 2.3, 32)), rt=0.6)
        until(self, "where at least one should fail")
        P(self, Create(xmark(1.4, 1.75, 0.2)), *[Create(check(1.95 + i * 0.55, 1.75, 0.15)) for i in range(3)],
          FadeIn(lab("one fails = caught", 4.3, 2.3, 32)), rt=0.6)
        until(self, "A mutant nobody catches")
        gap = lab("nobody fails = a gap", -3.0, -2.2, 34)
        P(self, FadeIn(gap), rt=0.4)
        until(self, "goes into a dated log")
        log = paper(3.3, -2.35, 2.4, 0.9)
        ll = lab("Claude's mistakes → log", 3.3, -3.05, 32)
        P(self, FadeIn(log), FadeIn(ll), rt=0.5)
        P(self, Create(scribble(2.4, -2.35, 1.8)), rt=0.4)
        finish(self)


class B07_Alternatives(Scene):
    def construct(self):
        tag(self, "MIXED")
        docs = []
        for x, n in zip((-5.1, -2.5), ("Postbot", "Schemathesis")):
            docs.append(VGroup(Iso(x, -0.4, 0.7).box(-0.75, -0.75, 0, 1.5, 1.5, 1.1), lab(n, x, -1.55)))
        dl = lab("docs only", -3.8, 1.75)
        until(self, "Postbot generates")
        P(self, FadeIn(docs[0], shift=DOWN * 0.4), FadeIn(dl), rt=0.6)
        until(self, "Schemathesis checks")
        P(self, FadeIn(docs[1], shift=DOWN * 0.4), rt=0.6)
        until(self, "I ran Stryker")
        iso = Iso(0.8, -0.6, 0.75)
        sback, sfront = iso.open_box(-0.8, -0.8, 0, 1.6, 1.6, 1.2)
        sl = lab("Stryker, ran", 0.8, -1.8)
        P(self, FadeIn(sback, shift=DOWN * 0.4), FadeIn(sfront, shift=DOWN * 0.4), FadeIn(sl), rt=0.6)
        until(self, "ninety two mutants")
        hero = T("92", 96, bold=True).move_to([0.8, 1.55, 0])
        P(self, FadeIn(hero, shift=UP * 0.3), rt=0.5)
        until(self, "none changed")
        zero = lab("15,000 changed: 0", 0.8, -2.55)
        P(self, FadeIn(zero), rt=0.4)
        until(self, "BiteCheck adds")
        biso = Iso(4.7, -0.6, 0.75)
        back, front = biso.open_box(-0.8, -0.8, 0, 1.6, 1.6, 1.2)
        bl = lab("BiteCheck", 4.7, -1.8)
        P(self, FadeIn(back, shift=LEFT * 0.6), FadeIn(front, shift=LEFT * 0.6), FadeIn(bl), rt=0.6)
        rp = biso.page(-0.45, -0.5, 0.2, 0.9, 0.9)
        rp.set_z_index(1)
        P(self, FadeIn(rp, shift=DOWN * 0.8), rt=0.5)
        finish(self)


class B08_FirstMinute(Scene):
    def construct(self):
        tag(self, "PROPOSED")
        win = RoundedRectangle(width=7.0, height=2.6, corner_radius=0.12, fill_color=CARD, fill_opacity=1,
                               stroke_color=INK, stroke_width=4).move_to([-2.4, 0.4, 0])
        bar = Rectangle(width=7.0, height=0.45, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([-2.4, 1.5, 0])
        wl = lab("terminal", -2.4, -1.3)
        P(self, FadeIn(win), FadeIn(bar), FadeIn(wl), rt=0.8)
        until(self, "they run one command")
        cmd = Text("$ npm run bitecheck", font="Menlo", font_size=34, color=INK).move_to([-2.4, 0.3, 0])
        P(self, AddTextLetterByLetter(cmd), rt=1.2)
        until(self, "read one page")
        rep = paper(3.8, 0.3, 2.6, 3.2)
        rl = lab("report", 3.8, -1.75)
        P(self, FadeIn(rep, shift=LEFT * 0.8), FadeIn(rl), rt=0.7)
        bars = [Rectangle(width=1.6 * f, height=0.32, fill_color=c, fill_opacity=1, stroke_width=0)
                .move_to([2.9 + 0.8 * f, 1.2 - i * 0.65, 0])
                for i, (f, c) in enumerate([(1.0, BAR1), (0.75, BAR2), (0.4, BAR1), (0.25, BAR2)])]
        for b, phrase in zip(bars, ["what passed", "which bugs were caught", "which slipped through", "where Claude was wrong"]):
            until(self, phrase)
            P(self, GrowFromEdge(b, LEFT), rt=0.4)
        finish(self)


class B09_Proves(Scene):
    def construct(self):
        tag(self, "PROPOSED")
        tests = VGroup(*[tpage(-4.6 + i * 0.25, 0.7 - i * 0.2, 1.3, 1.6) for i in range(3)])
        tl = lab("tests", -4.3, -1.0)
        st, lights = Iso(3.6, -1.0, 0.8).server(-0.8, -0.8, 0, 1.6, 1.6, 0.5, 3)
        al = lab("API", 3.6, -2.4)
        P(self, FadeIn(tests), tl, FadeIn(st), FadeIn(lights), al, rt=1.0)
        until(self, "an agent loop")
        a1 = CurvedArrow(np.array([-3.2, 1.8, 0]), np.array([1.6, 1.8, 0]), angle=-PI / 3, color=DIM, stroke_width=5)
        a2 = CurvedArrow(np.array([1.6, -0.2, 0]), np.array([-3.2, -0.2, 0]), angle=-PI / 3, color=DIM, stroke_width=5)
        P(self, Create(a1), Create(a2), rt=1.0)
        until(self, "never the API")
        lk = lock(3.6, 1.9, 0.6)
        P(self, FadeIn(lk, shift=DOWN * 0.4), rt=0.5)
        until(self, "and evaluation")
        track = Rectangle(width=5.0, height=0.36, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([-0.4, -2.6, 0])
        fill = Rectangle(width=3.1, height=0.36, fill_color=BAR1, fill_opacity=1, stroke_width=0)
        fill.move_to([-0.4 - 2.5 + 1.55, -2.6, 0])
        sl = lab("score", -3.8, -2.6)
        P(self, FadeIn(track), FadeIn(sl), rt=0.4)
        P(self, GrowFromEdge(fill, LEFT), rt=0.9)
        finish(self)


class B10_OutAndFirst(Scene):
    def construct(self):
        tag(self, "CIRAN")
        st, lights = Iso(-4.2, -1.5, 0.7).server(-0.7, -0.7, 0, 1.4, 1.4, 0.45, 3)
        handle = Rectangle(width=0.3, height=1.6, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4)
        head = Circle(radius=0.38, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0, 0.95, 0])
        notch = Rectangle(width=0.26, height=0.4, fill_color=STAGE, fill_opacity=1, stroke_width=0).move_to([0, 1.2, 0])
        wrench = VGroup(handle, head, notch).rotate(-PI / 5).move_to([-4.2, 1.6, 0])
        wl = lab("no auto-fix", -4.2, -2.3)
        P(self, FadeIn(st), FadeIn(lights), FadeIn(wrench), wl, rt=0.9)
        until(self, "never fix the app")
        P(self, Create(xmark(-4.2, 1.6, 0.75, w=10)), rt=0.5)
        until(self, "The first piece now runs")
        belt = Rectangle(width=7.0, height=0.7, fill_color="#E6E1D4", fill_opacity=1, stroke_color="#9C8462", stroke_width=4).move_to([2.2, -0.4, 0])
        gates = VGroup(*[VGroup(Rectangle(width=0.16, height=1.5, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to([x, 0.15, 0]))
                         for x in (0.6, 2.2, 3.8)])
        gl = lab("GitHub Actions", 2.2, -1.5)
        bug = VGroup(Square(0.6, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3),
                     Dot([0, 0, 0], radius=0.09, color=TERRA)).move_to([-0.9, 0.2, 0])
        P(self, FadeIn(belt), FadeIn(gates), FadeIn(gl), FadeIn(bug), rt=0.8)
        until(self, "GitHub Actions ran")
        P(self, bug.animate.move_to([5.0, 0.2, 0]), rt=2.0, rate_func=linear)
        until(self, "caught both planted bugs")
        P(self, Create(check(5.6, 1.4, 0.3)), rt=0.5)
        finish(self)


class B11_Risk(Scene):
    def construct(self):
        tag(self, "PROPOSED")
        line = Arrow([-5.6, 0.0, 0], [5.6, 0.0, 0], color=INK, stroke_width=5, buff=0)
        tlab = lab("git history", 4.4, -0.6, 32)
        P(self, Create(line), FadeIn(tlab), rt=0.8)
        until(self, "commit the bug list")
        d1 = Dot([-3.4, 0, 0], radius=0.16, color=TERRA)
        l1 = lab("1. bug list", -3.4, -0.65)
        lk = lock(-3.4, 1.1, 0.55)
        P(self, GrowFromCenter(d1), FadeIn(l1), FadeIn(lk, shift=DOWN * 0.3), rt=0.6)
        until(self, "before Claude writes")
        d2 = Dot([0.6, 0, 0], radius=0.16, color=INK)
        l2 = lab("2. tests", 0.6, -0.65)
        P(self, GrowFromCenter(d2), FadeIn(l2), rt=0.5)
        until(self, "every bug that survived")
        sv = paper(0.6, -2.2, 3.4, 0.9)
        sl = lab("survivors", -2.2, -2.2)
        rows = VGroup(*[scribble(-0.8 + i * 1.0, -2.2, 0.75) for i in range(3)])
        P(self, FadeIn(sv, shift=UP * 0.4), FadeIn(sl), rt=0.6)
        P(self, Create(rows), rt=0.6)
        finish(self)


class B12_WhyMe(Scene):
    def construct(self):
        tag(self, "SELF")
        s1 = Rectangle(width=6.6, height=0.25, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-2.6, -0.6, 0])
        s2 = Rectangle(width=4.2, height=0.25, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.7, -0.6, 0])
        h1, h2 = lab("have", -2.6, 1.9, 38), lab("new to me", 3.7, 1.9, 38)
        P(self, FadeIn(s1), FadeIn(s2), FadeIn(h1), FadeIn(h2), rt=0.8)
        until(self, "I've done API testing")
        hx = [-5.0, -2.6]
        have = [Rectangle(width=1.6, height=1.3, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, 0.18, 0]) for x in hx]
        hl = [lab("API tests", hx[0], -1.2, 32), lab("CI gates", hx[1], -1.2, 32)]
        P(self, *[FadeIn(h, shift=DOWN * 0.3) for h in have], *[FadeIn(l) for l in hl], rt=0.7)
        until(self, "that work is private")
        priv = lab("private", -3.8, -1.95, 34)
        P(self, FadeIn(priv), rt=0.4)
        until(self, "My public Reallocation")
        pr = Rectangle(width=1.6, height=1.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-0.2, 0.18, 0])
        prl, pub = lab("PR #37", -0.2, -1.2, 34), lab("public", -0.2, -1.95, 34)
        P(self, FadeIn(pr, shift=DOWN * 0.3), FadeIn(prl), FadeIn(pub), rt=0.6)
        until(self, "Mutation testing")
        xs = [2.7, 4.7]
        outl = [Rectangle(width=1.5, height=1.3, fill_color=STAGE, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, 0.18, 0]) for x in xs]
        nl = [lab(n, x, -1.2, 32) for n, x in zip(["mutants", "evals"], xs)]
        P(self, *[Create(o) for o in outl], *[FadeIn(l) for l in nl], rt=0.7)
        until(self, "so it's a mix")
        dots = VGroup(*[Dot([x, 0.18, 0], radius=0.12, color=TERRA) for x in xs])
        P(self, LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), rt=0.6)
        finish(self)


class B13_ExistsWill(Scene):
    def construct(self):
        tag(self, "STATUS")
        h1, h2 = lab("exists", -4.4, 2.2, 38), lab("will exist", 2.1, 2.2, 38)
        div = Line([-2.5, 2.4, 0], [-2.5, 0.0, 0], color=GHOST, stroke_width=4)
        P(self, FadeIn(h1), FadeIn(h2), Create(div), rt=0.6)
        until(self, "The loan API exists")
        e = [Rectangle(width=0.7, height=0.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-5.6, y, 0]) for y in (1.3, 0.4)]
        el = [lab("loan API", -4.15, 1.3, 34), lab("Stryker run", -3.95, 0.4, 34)]
        P(self, FadeIn(e[0]), FadeIn(el[0]), rt=0.5)
        until(self, "so did the Stryker check")
        P(self, FadeIn(e[1]), FadeIn(el[1]), rt=0.5)
        until(self, "I chose a second bug")
        e3 = Rectangle(width=0.7, height=0.7, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-5.6, -0.5, 0])
        l3 = lab("tests + 2 bugs + CI", -3.3, -0.5, 34)
        P(self, FadeIn(e3), FadeIn(l3), rt=0.5)
        until(self, "Everything else")
        xs = [-1.4, 0.2, 1.8, 3.4, 5.0]
        names = ["prompt", "all bugs", "API tests", "runner", "report"]
        w = [DashedVMobject(Rectangle(width=1.35, height=0.9, color=INK, stroke_width=4), num_dashes=16).move_to([x, 1.0, 0]) for x in xs]
        wl = [lab(n, x, 0.1, 32) for n, x in zip(names, xs)]
        P(self, *[Create(b) for b in w], *[FadeIn(l) for l in wl], rt=0.8)
        until(self, "this is BiteCheck")
        title = T("BiteCheck", 72, bold=True).move_to([0, -2.0, 0])
        who = lab("Omkar Salian", 0, -2.95, 36)
        ul = Line([-1.9, -2.5, 0], [1.9, -2.5, 0], color=TERRA, stroke_width=6)
        P(self, FadeIn(title), FadeIn(who), Create(ul), rt=0.8)
        finish(self)


