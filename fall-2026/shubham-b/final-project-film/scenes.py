"""
iso_kit.py — the show-tell drawing kit. PASTE this block at the top of a reel's scenes.py;
do not import it (Gate A copies only scenes.py into its sandbox).

Drawn isometric objects in the Claude palette: cardboard boxes (closed, open, taped), dark
MCP blocks with ports, flat skill pages, server stacks with lights, checks, a cursor, pills,
and a WRITING KIT (quill, inkwell, paper, scribble lines, branching outline + the write_lines /
grow_tree animations that make the quill write). (The portrait helper is not included in this film's copy.)
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


# ═════════════════════════════ FILM HELPERS (Marino Desk Assistant pitch — mine) ═════════════════════════════
# Everything above this line is the toolkit's show-tell iso_kit.py, pasted (Gate A copies only
# scenes.py). The Professor Bear portrait section is left out: this film shows no people.

KRAFT_DEEP = "#9C8462"          # connectors / small outlines (GATE T: not ink)


def tag(text):
    """The status tag in the top-left corner of every beat: what the picture is (real output,
    constructed/planned, or an illustration). Ink, never terracotta."""
    t = T(text, 38)
    t.to_corner(UL, buff=0.9)
    return t


def G(self, *anims, run_time=1.0, **kw):
    """play() with two guards: (1) never animate across the clip midpoint (GATE T and Gate V sample it),
    (2) never run past the beat's measured audio (compile.py centre-cuts a long clip)."""
    bid = type(self).__name__.split("_")[0]
    target = _TARGET.get(bid, 0)
    if target:
        mid, now = target / 2.0, _elapsed(self)
        if now < mid + 0.25 and now + run_time > mid - 0.25:
            self.wait(mid + 0.25 - now)
            now = mid + 0.25
        run_time = max(0.25, min(run_time, target - 0.45 - now))
    self.play(*anims, run_time=run_time, **kw)


def crate(cx, by, s=1.0, w=0.9, d=0.9, h=0.75):
    """A job crate: a kraft box whose lowest corner sits at (cx, by). `.iso` is its projection,
    `.top` the centre of its top face."""
    iso = Iso(cx, by, s)
    g = iso.box(0, 0, 0, w, d, h)
    g.iso = iso
    g.top = iso.p(w / 2, d / 2, h)
    return g


def spark(pt, r=0.09):
    return Dot(np.array(pt, dtype=float), radius=r, color=TERRA)


def ghost_crate(cx, by, s=1.0, w=0.9, d=0.9, h=0.75, color=DIM):
    """A dashed outline of a crate: something that will exist but doesn't yet."""
    iso = Iso(cx, by, s)
    sil = Polygon(iso.p(0, d, 0), iso.p(0, 0, 0), iso.p(w, 0, 0), iso.p(w, 0, h), iso.p(w, d, h), iso.p(0, d, h))
    inner = VMobject().set_points_as_corners([iso.p(0, d, h), iso.p(0, 0, h), iso.p(w, 0, h)])
    edge = Line(iso.p(0, 0, 0), iso.p(0, 0, h))
    parts = [DashedVMobject(m.set_stroke(color, 5).set_fill(opacity=0), num_dashes=n)
             for m, n in ((sil, 28), (inner, 10), (edge, 5))]
    g = VGroup(*parts)
    g.top = iso.p(w / 2, d / 2, h)
    return g





def drop_in(m, dy=1.0):
    """Start `m` dy above its place (call before play; animate with m.animate.shift(DOWN*dy))."""
    m.shift(UP * dy)
    return m




def bell(cx, by, s=1.0):
    """The film's hero object: a front-desk bell. Dark base, kraft dome, ink knob. (cx, by) = base centre."""
    base = RoundedRectangle(width=2.0 * s, height=0.26 * s, corner_radius=0.06 * s, fill_color=DARK_TOP,
                            fill_opacity=1, stroke_width=0).move_to([cx, by, 0])
    top = by + 0.13 * s
    pts = [[cx + 0.78 * s * np.cos(a), top + 0.62 * s * np.sin(a), 0] for a in np.linspace(0, PI, 24)]
    dome = Polygon(*pts, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4)
    stem = Line([cx, top + 0.62 * s, 0], [cx, top + 0.8 * s, 0], color=INK, stroke_width=7)
    knob = Circle(radius=0.13 * s, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([cx, top + 0.88 * s, 0])
    g = VGroup(base, dome, stem, knob)
    g.top = np.array([cx, top + 0.88 * s, 0.0])
    return g


def rings(cx, cy, s=1.0):
    """Two ink arcs either side of the knob: the bell rings."""
    return VGroup(*[Arc(radius=r * s, start_angle=a, angle=0.9, color=INK, stroke_width=6).move_arc_center_to([cx, cy, 0])
                    for r in (0.45, 0.7) for a in (0.35, PI - 1.25)])


def window(cx, cy, w, h, bar=0.45):
    """A browser/app window: pale body with a grey outline, a dark title bar, three ghost dots."""
    body = Rectangle(width=w, height=h, fill_color=CARD, fill_opacity=1, stroke_color=DIM, stroke_width=4).move_to([cx, cy, 0])
    tb = Rectangle(width=w, height=bar, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([cx, cy + h / 2 + bar / 2, 0])
    dots = VGroup(*[Dot([cx - w / 2 + 0.3 + i * 0.28, cy + h / 2 + bar / 2, 0], radius=0.065, color=GHOST) for i in range(3)])
    return VGroup(body, tb, dots)


def bubble(cx, cy, w, h, fill=PAGE_TOP):
    return RoundedRectangle(width=w, height=h, corner_radius=0.22, fill_color=fill, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([cx, cy, 0])


def slip_with_slots(cx, cy, w=7.0, h=1.4, xs=(-3.3, -1.5, 0.3, 2.1)):
    """The prompt-contract slip: a paper with four empty grey slots (answer, quote, link, date)."""
    slip = paper(cx, cy, w=w, h=h)
    slots = [RoundedRectangle(width=1.5, height=0.55, corner_radius=0.1, fill_color=BAR3, fill_opacity=1,
                              stroke_width=0).move_to([x, cy, 0]) for x in xs]
    return slip, slots


# ═════════════════════════════ SCENES ═════════════════════════════

class B01_Desk(Scene):
    def construct(self):
        tg = tag("synthetic voice · script written with Claude")
        G(self, FadeIn(tg), run_time=0.4)
        counter = Iso(-3.6, -1.8, 1.0).box(-1.6, -0.6, 0, 3.2, 1.2, 0.8)
        b = bell(-3.6, -0.95)
        G(self, FadeIn(counter, shift=UP * 0.3), run_time=0.6)
        G(self, FadeIn(b, shift=DOWN * 0.4), run_time=0.5)
        until(self, "answer front-desk questions")
        G(self, Create(rings(b.top[0], b.top[1])), run_time=0.5)
        until(self, "Marino Desk Assistant")
        win = window(2.3, -0.5, 5.0, 3.1)
        name = T("Desk Assistant", 56).move_to([2.3, 1.95, 0])
        G(self, FadeIn(win, shift=LEFT * 0.4), FadeIn(name), run_time=0.7)
        until(self, "from the public recreation website")
        bub = bubble(2.1, 0.15, 3.9, 1.0)
        line = scribble(0.5, 0.15, 2.6)
        G(self, FadeIn(bub), run_time=0.4)
        G(self, Create(line), run_time=0.8)
        until(self, "quote the page it used")
        link = RoundedRectangle(width=1.6, height=0.45, corner_radius=0.2, fill_color=BAR3, fill_opacity=1,
                                stroke_width=0).move_to([1.2, -0.95, 0])
        G(self, FadeIn(link), GrowFromCenter(spark([0.65, -0.95, 0], 0.1)), run_time=0.5)
        finish(self)


class B02_Repo(Scene):
    def construct(self):
        tg = tag("planned repo · real: 60 tests pass")
        G(self, FadeIn(tg), run_time=0.4)
        until(self, "public GitHub repository")
        iso = Iso(-2.0, -2.9, 1.15)
        back, front = iso.open_box(0, 0, 0, 2.3, 1.9, 0.55)
        lbl = T("GitHub repo", 56).move_to([-1.8, 1.0, 0])
        G(self, FadeIn(back), FadeIn(front), FadeIn(lbl), run_time=0.7)
        until(self, "a Python and FastAPI backend")
        api = iso.box(0.25, 0.25, 0, 0.8, 0.7, 0.45, DARK_TOP, DARK_L, DARK_R)
        ui = iso.page(1.3, 0.2, 0, w=0.8, d=0.7)
        model = iso.box(0.25, 1.05, 0, 0.8, 0.7, 0.3)
        report = iso.page(1.3, 1.05, 0, w=0.8, d=0.7)
        parts = [api, ui, model, report]
        for p in parts:
            p.set_z_index(1)
            drop_in(p, 1.1)
        G(self, LaggedStart(*[p.animate.shift(DOWN * 1.1) for p in parts], lag_ratio=0.3), run_time=1.8, rate_func=ease_in)
        until(self, "A first version already exists")
        siso = Iso(3.3, -1.6, 0.9)
        stack, lights = siso.server(-0.7, -0.7, 0, w=1.4, d=1.4, slab=0.42, n=3)
        first = T("first version", 46).move_to([3.3, 0.95, 0])
        G(self, FadeIn(stack, shift=UP * 0.3), FadeIn(lights), FadeIn(first), run_time=0.8)
        until(self, "sixty tests passed today")
        ok = T("60 tests pass", 46).move_to([3.3, -2.75, 0])
        G(self, *[l.animate.set_color(TERRA) for l in lights], FadeIn(ok), run_time=0.5)
        finish(self)


class B03_Scroll(Scene):
    def construct(self):
        tg = tag("illustration")
        G(self, FadeIn(tg), run_time=0.4)
        b = bell(-4.4, -1.6, 0.9)
        G(self, FadeIn(b, shift=DOWN * 0.3), run_time=0.5)
        until(self, "asks what an alumni membership costs")
        G(self, Create(rings(b.top[0], b.top[1], 0.9)), run_time=0.5)
        win = window(1.4, -0.15, 5.2, 4.0)
        ys = [1.25 - i * 0.48 for i in range(7)]
        lines = VGroup(*[scribble(-0.9, y, 3.6 if i % 3 else 2.4) for i, y in enumerate(ys)])
        track = Line([3.75, 1.65, 0], [3.75, -1.95, 0], color=GHOST, stroke_width=12)
        thumb = RoundedRectangle(width=0.2, height=0.75, corner_radius=0.08, fill_color=INK, fill_opacity=1,
                                 stroke_width=0).move_to([3.75, 1.2, 0])
        until(self, "The answer is on the website")
        G(self, FadeIn(win), Create(track), run_time=0.6)
        G(self, LaggedStart(*[Create(l) for l in lines], lag_ratio=0.1), FadeIn(thumb), run_time=1.0)
        until(self, "about eight hundred words")
        words = T("~800 words", 52).move_to([1.4, -2.75, 0])
        G(self, FadeIn(words), run_time=0.4)
        until(self, "while the member waits")
        G(self, thumb.animate.shift(DOWN * 2.3), lines.animate.shift(UP * 0.15), run_time=1.6, rate_func=linear)
        finish(self)


class B04_Search(Scene):
    def construct(self):
        tg = tag("real search · 2026-10-13")
        G(self, FadeIn(tg), run_time=0.4)
        pill = RoundedRectangle(width=5.4, height=0.8, corner_radius=0.4, fill_color=PAGE_TOP, fill_opacity=1,
                                stroke_color=INK, stroke_width=4).move_to([0.5, 1.75, 0])
        lens = VGroup(Circle(radius=0.17, stroke_color=INK, stroke_width=5).move_to([-1.85, 1.8, 0]),
                      Line([-1.72, 1.67, 0], [-1.55, 1.5, 0], color=INK, stroke_width=6))
        until(self, "The site's own search")
        q = T("guest pass", 48).move_to([4.6, 1.75, 0])
        G(self, FadeIn(pill), Create(lens), run_time=0.6)
        typed = scribble(-1.25, 1.75, 2.4, color=DIM)
        G(self, Create(typed), FadeIn(q), run_time=0.7)
        until(self, "returned five pages")
        ys = (0.8, 0.15, -0.5, -1.15, -1.8)
        cards = [VGroup(Rectangle(width=5.4, height=0.5, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK,
                                  stroke_width=3).move_to([0.5, y, 0]),
                        Line([-1.9, y, 0], [-0.2 + 0.4 * (i % 3), y, 0], color=GHOST, stroke_width=7)) for i, y in enumerate(ys)]
        five = T("5 pages", 52).move_to([-3.7, -0.5, 0])
        G(self, LaggedStart(*[FadeIn(c, shift=DOWN * 0.25) for c in cards], lag_ratio=0.15), FadeIn(five), run_time=1.2)
        until(self, "with the home page first")
        home = T("Home", 48).move_to([4.15, 0.8, 0])
        G(self, FadeIn(home), Indicate(cards[0], color=BAR3, scale_factor=1.02), run_time=0.6)
        until(self, "Manual lookup")
        cur = cursor(3.7, 0.5)
        G(self, FadeIn(cur), run_time=0.3)
        G(self, cur.animate.shift(DOWN * 2.3), run_time=1.2, rate_func=linear)
        finish(self)


class B05_Answer(Scene):
    def construct(self):
        tg = tag("constructed · planned answer")
        G(self, FadeIn(tg), run_time=0.4)
        until(self, "It will give one answer")
        b1 = bubble(-0.6, 0.65, 6.4, 2.0)
        ans = scribble(-3.4, 1.15, 4.4)
        G(self, FadeIn(b1, shift=UP * 0.3), run_time=0.5)
        G(self, Create(ans), run_time=0.6)
        until(self, "quote the exact line")
        brk = VGroup(Line([-3.45, 0.75, 0], [-3.45, 0.25, 0], color=INK, stroke_width=7),
                     Line([-3.45, 0.75, 0], [-3.3, 0.75, 0], color=INK, stroke_width=7),
                     Line([-3.45, 0.25, 0], [-3.3, 0.25, 0], color=INK, stroke_width=7))
        quote = scribble(-3.05, 0.5, 3.4)
        ql = T("quote + link", 48).move_to([4.35, 0.65, 0])
        G(self, Create(brk), Create(quote), FadeIn(ql), run_time=0.8)
        until(self, "link to it")
        link = RoundedRectangle(width=1.7, height=0.4, corner_radius=0.18, fill_color=BAR3, fill_opacity=1,
                                stroke_width=0).move_to([-2.5, 0.0, 0])
        G(self, FadeIn(link), GrowFromCenter(spark([-3.15, 0.0, 0], 0.1)), run_time=0.5)
        until(self, "when the website doesn't say")
        b2 = bubble(-2.1, -1.75, 3.4, 0.85, fill=BOX_TOP)
        dk = T("I don't know", 52).move_to([1.6, -1.75, 0])
        G(self, FadeIn(b2, shift=UP * 0.3), run_time=0.5)
        G(self, Create(scribble(-3.4, -1.75, 2.4)), FadeIn(dk), run_time=0.6)
        finish(self)


class B06_Reader(Scene):
    def construct(self):
        tg = tag("constructed · planned repo")
        G(self, FadeIn(tg), run_time=0.4)
        until(self, "My target role")
        win = window(-2.4, -0.35, 6.0, 3.8)
        G(self, FadeIn(win), run_time=0.7)
        until(self, "my reader is")
        hm = T("hiring manager", 52).move_to([2.9, 2.2, 0])
        G(self, FadeIn(hm), run_time=0.4)
        until(self, "see the evaluation table")
        ys = (1.0, 0.45, -0.1, -0.65, -1.2)
        rows = VGroup(*[VGroup(Line([-5.0, y, 0], [-3.2, y, 0], color=BAR2, stroke_width=8),
                               Rectangle(width=0.9, height=0.28, fill_color=BAR1 if i % 2 else BAR2, fill_opacity=1,
                                         stroke_width=0).move_to([-2.4, y, 0]),
                               Line([-1.6, y, 0], [0.0, y, 0], color=GHOST, stroke_width=8)) for i, y in enumerate(ys)])
        G(self, LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=0.9)
        until(self, "run one command")
        hero = T("60 s", 120).move_to([3.0, 0.55, 0])
        G(self, FadeIn(hero), run_time=0.4)
        until(self, "ask a fee question")
        card = bubble(3.0, -1.55, 3.4, 0.9)
        G(self, FadeIn(card, shift=LEFT * 0.4), run_time=0.5)
        G(self, Create(scribble(1.65, -1.55, 2.3)), run_time=0.5)
        until(self, "refuse an off-topic one")
        G(self, GrowFromCenter(spark([4.45, -1.55, 0], 0.1)), run_time=0.3)
        finish(self)


class B07_Contract(Scene):
    def construct(self):
        tg = tag("exists: 5 → 3 · planned: contract")
        G(self, FadeIn(tg), run_time=0.4)
        until(self, "Source grounding")
        xs = (-4.8, -3.3, -1.8, -0.3, 1.2)
        pages = [paper(x, 1.15, w=1.15, h=1.45) for x in xs]
        lines = [scribbles_on(p, n=3, inset=0.22, gap=0.32, color=DIM) for p in pages]
        G(self, LaggedStart(*[FadeIn(VGroup(p, l)) for p, l in zip(pages, lines)], lag_ratio=0.12), run_time=1.0)
        until(self, "reranks them to three")
        lbl = T("5 → 3", 64).move_to([3.9, 1.15, 0])
        drop = [VGroup(pages[i], lines[i]) for i in (1, 3)]
        keep = [VGroup(pages[i], lines[i]) for i in (0, 2, 4)]
        G(self, *[d.animate.shift(DOWN * 0.6).set_opacity(0.15) for d in drop], FadeIn(lbl), run_time=0.7)
        G(self, keep[1].animate.shift(LEFT * 1.5 + RIGHT * 0.0), keep[2].animate.shift(LEFT * 3.0), run_time=0.6)
        until(self, "a prompt contract")
        slip, slots = slip_with_slots(-0.6, -1.9)
        ct = T("contract", 52).move_to([4.3, -1.9, 0])
        G(self, FadeIn(slip, shift=UP * 0.3), *[FadeIn(s) for s in slots], FadeIn(ct), run_time=0.7)
        until(self, "the answer, the quoted line")
        fills = [scribble(x - 0.55, -1.9, 1.1, color=DIM) for x in (-3.3, -1.5, 0.3, 2.1)]
        G(self, LaggedStart(*[Create(f) for f in fills], lag_ratio=0.25), run_time=1.0)
        until(self, "isn't in the page fails")
        x = VGroup(Line([-1.95, -1.6, 0], [-1.05, -2.2, 0], color=INK, stroke_width=8),
                   Line([-1.95, -2.2, 0], [-1.05, -1.6, 0], color=INK, stroke_width=8))
        G(self, Create(x), run_time=0.4)
        finish(self)


class B08_Eval(Scene):
    def construct(self):
        tg = tag("constructed · planned")
        G(self, FadeIn(tg), run_time=0.4)
        pages = []
        for r in range(5):
            for c in range(10):
                pages.append(Rectangle(width=0.4, height=0.5, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK,
                                       stroke_width=2.5).move_to([-5.6 + c * 0.5, 1.6 - r * 0.68, 0]))
        book = Iso(3.9, -2.4, 1.0).box(-0.8, -0.6, 0, 1.6, 1.2, 0.5, DARK_TOP, DARK_L, DARK_R)
        n = T("50 questions", 52).move_to([-3.35, -1.95, 0])
        G(self, LaggedStart(*[FadeIn(p) for p in pages], lag_ratio=0.01), FadeIn(n), run_time=1.2)
        G(self, FadeIn(book, shift=UP * 0.3), run_time=0.5)
        until(self, "scored three ways")
        bars = [Rectangle(width=w, height=0.42, fill_color=c, fill_opacity=1, stroke_width=0).move_to([0.6 + w / 2, y, 0])
                for w, y, c in ((2.6, 1.2, BAR1), (2.1, 0.55, BAR2), (2.9, -0.1, BAR1))]
        sc = T("3 scores", 52).move_to([2.0, 1.95, 0])
        G(self, LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.3), FadeIn(sc), run_time=1.2)
        until(self, "Every miss goes in the report")
        miss = (7, 18, 26, 43)
        sp = {i: spark(np.array(pages[i].get_center(), dtype=float), 0.1) for i in miss}
        G(self, *[GrowFromCenter(s) for s in sp.values()], run_time=0.4)
        fly = [VGroup(pages[i], sp[i]) for i in miss]
        G(self, *[f.animate.scale(0.6).move_to([3.5 + 0.25 * k, -1.55, 0]) for k, f in enumerate(fly)], run_time=0.8)
        finish(self)


class B09_Fair(Scene):
    def construct(self):
        tg = tag("illustration")
        G(self, FadeIn(tg), run_time=0.4)
        win = window(-3.2, -0.2, 3.6, 2.6)
        bars = [Rectangle(width=0.55, height=h, fill_color=c, fill_opacity=1, stroke_width=0).move_to([x, -1.2 + h / 2, 0])
                for x, h, c in ((-4.2, 1.2, BAR2), (-3.3, 1.8, BAR1), (-2.4, 0.9, BAR2))]
        G(self, FadeIn(win), run_time=0.5)
        until(self, "could fairly conclude")
        fair = T("fair", 56).move_to([-3.2, -2.35, 0])
        G(self, LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(fair), run_time=0.8)
        G(self, Create(check(-0.8, 0.6, 0.3, INK, 10)), run_time=0.4)
        until(self, "Not that it's")
        badge = DashedVMobject(Circle(radius=1.15, stroke_color=DIM, stroke_width=6).move_to([3.2, -0.2, 0]), num_dashes=28)
        strike = Line([2.2, -1.1, 0], [4.2, 0.7, 0], color=INK, stroke_width=8)
        nc = T("not claimed", 56).move_to([3.2, -2.35, 0])
        G(self, Create(badge), FadeIn(nc), run_time=0.8)
        G(self, Create(strike), run_time=0.4)
        finish(self)


class B10_Scope(Scene):
    def construct(self):
        tg = tag("illustration")
        G(self, FadeIn(tg), run_time=0.4)
        until(self, "the public recreation pages")
        stack = VGroup(*[window(-3.6 + 0.45 * i, -0.55 - 0.45 * i, 3.0, 2.0, bar=0.35) for i in range(3)])
        ps = T("public site", 56).move_to([-3.0, 1.55, 0])
        G(self, LaggedStart(*[FadeIn(w, shift=UP * 0.2) for w in stack], lag_ratio=0.25), FadeIn(ps), run_time=1.0)
        until(self, "Deliberately out")
        fence = Line([1.0, -2.8, 0], [1.0, 2.2, 0], color=DIM, stroke_width=9)
        G(self, Create(fence), run_time=0.5)
        until(self, "internal staff documents")
        box = Iso(3.4, -2.6, 1.0).box(-0.75, -0.75, 0, 1.5, 1.5, 1.1, DARK_TOP, DARK_L, DARK_R)
        lock = VGroup(Arc(radius=0.24, start_angle=0, angle=PI, color=INK, stroke_width=7).move_arc_center_to([4.05, -2.05, 0]),
                      RoundedRectangle(width=0.7, height=0.55, corner_radius=0.08, fill_color=BOX_TOP, fill_opacity=1,
                                       stroke_color=INK, stroke_width=4).move_to([4.05, -2.3, 0]))
        sd = T("staff docs", 56).move_to([3.6, 0.95, 0])
        G(self, FadeIn(box, shift=LEFT * 0.3), FadeIn(lock), FadeIn(sd), run_time=0.7)
        until(self, "never indexes them")
        G(self, VGroup(box, lock).animate.shift(RIGHT * 0.6 + DOWN * 0.1), run_time=0.7)
        finish(self)


class B11_First(Scene):
    def construct(self):
        tg = tag("constructed · planned")
        G(self, FadeIn(tg), run_time=0.4)
        until(self, "a public-only index")
        iso = Iso(-3.3, -2.9, 1.05)
        back, front = iso.open_box(0, 0, 0, 2.2, 2.0, 0.6)
        G(self, FadeIn(back), FadeIn(front), run_time=0.6)
        pages = [paper(x, 1.5, w=0.9, h=1.1) for x in (-4.6, -3.3, -2.0)]
        G(self, LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in pages], lag_ratio=0.2), run_time=0.8)
        for p in pages:
            p.set_z_index(1)
        G(self, *[p.animate.scale(0.5).move_to([-3.3 + 0.35 * (k - 1), -1.6, 0]) for k, p in enumerate(pages)], run_time=0.8)
        until(self, "the right page in the top three")
        t3 = T("top 3", 56).move_to([-3.3, 1.75, 0])
        G(self, FadeIn(t3), run_time=0.4)
        until(self, "that report is in the repo")
        rep = paper(2.7, -0.35, w=3.0, h=3.6)
        rows = VGroup(*[scribble(1.6, y, 1.4) for y in (0.75, 0.15, -0.45, -1.05, -1.65)])
        marks = VGroup(*[check(3.75, y + 0.05, 0.14, INK, 6) for y in (0.75, 0.15, -1.05, -1.65)])
        rp = T("report.md", 52).move_to([2.7, 2.05, 0])
        G(self, FadeIn(rep, shift=UP * 0.3), FadeIn(rp), run_time=0.6)
        G(self, LaggedStart(*[Create(r) for r in rows], lag_ratio=0.1), run_time=0.8)
        G(self, LaggedStart(*[Create(m) for m in marks], lag_ratio=0.1), run_time=0.5)
        until(self, "with the crawl date")
        stamp = VGroup(Circle(radius=0.42, stroke_color=INK, stroke_width=5).move_to([4.75, 1.15, 0]),
                       Dot([4.75, 1.15, 0], radius=0.1, color=TERRA))
        G(self, GrowFromCenter(stamp), run_time=0.4)
        finish(self)


class B12_Prices(Scene):
    def construct(self):
        tg = tag("real prices · wrong pick illustrated")
        G(self, FadeIn(tg), run_time=0.4)
        until(self, "Prices that depend on the date")
        axis = Line([-5.4, -2.35, 0], [2.0, -2.35, 0], color=INK, stroke_width=6)
        G(self, Create(axis), run_time=0.6)
        until(self, "five yearly prices")
        xs = (-4.6, -3.2, -1.8, -0.4, 1.0)
        prices = (480, 360, 240, 220, 120)
        bars = [Rectangle(width=0.9, height=3.0 * p / 480, fill_color=BAR1, fill_opacity=1, stroke_width=0)
                .move_to([x, -2.35 + 1.5 * p / 480 + 0.04, 0]) for x, p in zip(xs, prices)]
        G(self, LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=1.2)
        until(self, "four hundred eighty dollars")
        hi = T("$480", 56).move_to([-4.6, 1.15, 0])
        G(self, FadeIn(hi), run_time=0.4)
        until(self, "one hundred twenty")
        lo = T("$120", 56).move_to([1.0, -0.65, 0])
        months = T("Sep → Jun", 48).move_to([-1.8, -2.95, 0])
        G(self, FadeIn(lo), FadeIn(months), run_time=0.5)
        until(self, "doesn't know today's date")
        mark = Triangle(fill_color=TERRA, fill_opacity=1, stroke_width=0).scale(0.16).rotate(PI).move_to([-4.6, 1.7 + 0.0, 0])
        mark.move_to([3.3, 0.6, 0])
        q = T("?", 72).move_to([3.3, 1.35, 0])
        G(self, FadeIn(mark), FadeIn(q), run_time=0.4)
        G(self, VGroup(mark, q).animate.shift(np.array([-3.2, 0.25, 0]) - np.array([3.3, 0.6, 0])), run_time=0.9)
        finish(self)


class B13_Dates(Scene):
    def construct(self):
        tg = tag("constructed · planned")
        G(self, FadeIn(tg), run_time=0.4)
        slip, slots = slip_with_slots(-0.6, -1.9)
        G(self, FadeIn(slip), *[FadeIn(s) for s in slots], run_time=0.6)
        until(self, "pass in today's date")
        cal = paper(-4.4, 0.6, w=1.5, h=1.7)
        band = Rectangle(width=1.5, height=0.36, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-4.4, 1.27, 0])
        grid = VGroup(*[Dot([-4.85 + 0.3 * c, 0.75 - 0.3 * r, 0], radius=0.05, color=BAR2) for r in range(3) for c in range(4)])
        td = T("today's date", 52).move_to([-4.4, 2.1, 0])
        G(self, FadeIn(cal), FadeIn(band), FadeIn(grid), FadeIn(td), run_time=0.6)
        calg = VGroup(cal, band, grid)
        G(self, calg.animate.scale(0.45).move_to([2.1, -1.9, 0]), run_time=0.9)
        until(self, "require the quoted row")
        G(self, Create(scribble(-2.05, -1.9, 1.1, color=DIM)), run_time=0.5)
        until(self, "show its crawl date")
        card = bubble(2.3, 0.85, 4.2, 1.3)
        stamp = VGroup(Circle(radius=0.42, stroke_color=INK, stroke_width=5).move_to([5.0, 0.85, 0]),
                       Dot([5.0, 0.85, 0], radius=0.1, color=TERRA))
        cd = T("crawl date", 52).move_to([2.3, 2.05, 0])
        G(self, FadeIn(card), Create(scribble(0.6, 0.85, 2.4)), run_time=0.6)
        G(self, GrowFromCenter(stamp), FadeIn(cd), run_time=0.5)
        finish(self)


class B14_Why(Scene):
    def construct(self):
        tg = tag("evidence: robust-data-processor (EventFlow)")
        G(self, FadeIn(tg), run_time=0.4)
        b = bell(0.0, 1.25, 0.6)
        G(self, FadeIn(b, shift=DOWN * 0.3), run_time=0.5)
        left = Iso(-3.3, -1.8, 1.0).box(-1.6, -0.6, 0, 3.2, 1.2, 0.25)
        right = Iso(2.9, -1.8, 1.0).box(-1.6, -0.6, 0, 3.2, 1.2, 0.25)
        until(self, "It's a mix")
        G(self, FadeIn(left), FadeIn(right), run_time=0.8)

        def on_shelf(iso, u):
            q = iso.p(u, 0, 0.25)
            return Iso(q[0], q[1], 1.0).box(-0.45, -0.45, 0, 0.9, 0.9, 0.75)
        liso, riso = Iso(-3.3, -1.8, 1.0), Iso(2.9, -1.8, 1.0)
        until(self, "I wrote the EventFlow Engine")
        ev = on_shelf(liso, 0.0)
        ev_l = T("EventFlow", 48).move_to([-3.3, 0.55, 0])
        drop_in(ev, 0.8)
        G(self, ev.animate.shift(DOWN * 0.8), FadeIn(ev_l), run_time=0.6, rate_func=ease_in)
        G(self, GrowFromCenter(spark(np.array(liso.p(0.0, 0, 0.25)) + np.array([0, 0.75, 0]), 0.1)), run_time=0.3)
        until(self, "New to me")
        q = riso.p(0, 0, 0.25)
        gc = ghost_crate(q[0], q[1] - 0.45, 1.0)
        evl = T("evaluation", 48).move_to([2.9, 0.65, 0])
        G(self, Create(gc), FadeIn(evl), run_time=1.2)
        until(self, "prompt contracts")
        G(self, GrowFromCenter(spark(gc.top, 0.12)), run_time=0.4)
        finish(self)


class B15_Ledger(Scene):
    def construct(self):
        tg = tag("summary · tests re-run 2026-10-13")
        G(self, FadeIn(tg), run_time=0.4)
        div = Line([-0.25, -2.7, 0], [-0.25, 1.9, 0], color=DIM, stroke_width=6)
        G(self, Create(div), run_time=0.4)
        until(self, "Exists today")
        ex = T("exists today", 56).move_to([-3.4, 1.5, 0])
        have = [crate(x, -1.6, 0.95) for x in (-5.0, -3.4, -1.8)]
        G(self, FadeIn(ex), LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in have], lag_ratio=0.25), run_time=1.0)
        G(self, *[Create(check(x + 0.05, 0.55, 0.2, INK, 8)) for x in (-5.0, -3.4, -1.8)], run_time=0.5)
        until(self, "sixty passing tests")
        real = Text("60 passed", font="PT Mono", color=INK, font_size=44).move_to([-3.4, -2.35, 0])
        G(self, FadeIn(real), run_time=0.4)
        until(self, "Will exist")
        wl = T("will exist", 56).move_to([3.2, 1.5, 0])
        will = [ghost_crate(x, -1.5, 0.9) for x in (1.5, 3.2, 4.9)]
        G(self, FadeIn(wl), run_time=0.4)
        G(self, LaggedStart(*[Create(g) for g in will], lag_ratio=0.35), run_time=1.8)
        finish(self)


class BOUT_Close(Scene):
    def construct(self):
        b = bell(0.0, 0.9, 0.9)
        G(self, FadeIn(b, shift=DOWN * 0.3), run_time=0.5)
        title = T("Marino Desk Assistant: A Pitch", 68).move_to([0, -0.55, 0])
        handle = T("github.com/bagwe-shubham1727/marino-rag", 44).move_to([0, -1.85, 0])
        G(self, FadeIn(title), run_time=0.4)
        G(self, FadeIn(handle), run_time=0.4)
        G(self, Create(rings(b.top[0], b.top[1], 0.9)), run_time=0.5)
        finish(self)
