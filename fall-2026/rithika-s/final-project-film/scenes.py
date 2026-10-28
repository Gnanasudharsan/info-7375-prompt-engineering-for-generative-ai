"""
scenes.py — rithika-final-project-pitch ("Agentic Retrieval Lab"), show-tell.

One drawn isometric Manim scene per beat, paced by the measured Bella narration in
beat_sheet.json (until() / done()). The show-tell drawing kit (iso_kit.py) is pasted
below, as the skill requires (Gate A copies only this file). Its instructor-portrait
helper is deliberately left out: this film carries no instructor identity. Its people are generic
cartoon figures (see CARTOON CAST), which Rithika authorised on 2026-10-11.
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
# Added 2026-10-07 from the toolkit author's two reference drawings: a quill drawing a branching outline on a
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


# ═════════════════════════════ FILM CAST (Agentic Retrieval Lab) — redesign v2 ═════════════════════════════
# One cast for the whole film (show-tell law 4):
#   the LIBRARY (bookcases) · KEYWORD LIBRARIAN = BM25 (cart + magnifying glass)
#   MEANING LIBRARIAN = embedding (cart + lightbulb) · the ROBOT (the AI agent)
#   the ANSWER KEY (clipboard) · DECOY BOOKS (grey) · THE PILE (top 100)
#   the RIGHT BOOK is always white with one terracotta dot.
# v2 rules (Rithika, 2026-10-11): real words only (no squiggles), phone-readable ink labels
# (key terms larger), drawings fill title-safe, key terms pop in on the whisper word timestamps
# (word_times.json), every icon labelled, CONSTRUCTED on invented examples, source tags on real data.
# Cartoon people (Rithika's authorisation, 2026-10-11): see CARTOON CAST below.
import random as _rnd

SPINES = [BOX_TOP, PAGE_TOP, BOX_L, GHOST, BOX_R, PAGE_L]
DECOY_TOP, DECOY_L, DECOY_R = "#C9C6C0", "#A9A6A0", "#8F8C86"
KRAFT_DEEP = "#9C8462"
KEY, SEC, TAG = 50, 40, 32          # key-term labels, secondary labels, source tags (type floor is 32)

try:
    _WT = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "word_times.json")))["words"]
except Exception:
    _WT = {}


def bid_of(self):
    return type(self).__name__.split("_")[0]


def _norm(w):
    return "".join(ch for ch in str(w).lower() if ch.isalnum() or ch == "%")


def word_t(bid, phrase, nth=1):
    """Start time (s) of `phrase` in the beat's whisper word timestamps, or None."""
    toks = [t for t in (_norm(x) for x in phrase.split()) if t]
    ws = _WT.get(bid, [])
    seq = [_norm(w[0]) for w in ws]
    hits = 0
    for i in range(len(seq) - len(toks) + 1):
        if seq[i:i + len(toks)] == toks:
            hits += 1
            if hits == nth:
                return float(ws[i][1])
    return None


def at(self, phrase, lead=0.12, nth=1):
    """Wait until `phrase` is spoken (whisper word time). Falls back to until() — the Gate A
    sandbox has only scenes.py, so word_times.json is absent there."""
    t = word_t(bid_of(self), phrase, nth)
    if t is None:
        until(self, phrase)
        return
    gap = t - lead - _elapsed(self)
    if gap > 0.04:
        self.wait(gap)


def P(self, *anims, rt=0.5, **kw):
    """play() with the MIDPOINT GUARD: nothing moves within ±0.25 s of the clip midpoint (GATE T and
    Gate V sample there). An animation that would cross it waits; the delay is logged as [guard]."""
    tgt = _TARGET.get(bid_of(self), 0)
    s = _elapsed(self)
    if tgt:
        m = tgt / 2
        if s < m + 0.25 and s + rt > m - 0.25:
            print(f"[guard] {bid_of(self)} cue at {s:.2f}s held {m + 0.25 - s:.2f}s past the midpoint")
            self.wait(m + 0.25 - s)
    self.play(*anims, run_time=rt, rate_func=kw.pop("rate_func", smooth), **kw)


def pop(self, *mobs, rt=0.45):
    """KEYWORD POP-IN: a gentle scale-in (same easing everywhere)."""
    P(self, *[FadeIn(m, scale=0.7) for m in mobs], rt=rt)


def _fam(mob):
    return list(mob.get_family())


def fade_to(mob, a):
    """Animate a whole group's opacity to `a` × its original (1 = restore). Keeps zero-fill strokes at zero fill."""
    try:
        orig = getattr(mob, "_op0", None)
        if orig is None:
            orig = [(m, float(m.get_fill_opacity()), float(m.get_stroke_opacity())) for m in _fam(mob)]
            mob._op0 = orig
        cur = [(float(m.get_fill_opacity()), float(m.get_stroke_opacity())) for m, _, _ in orig]

        def upd(_, t):
            for (m, f0, s0), (fc, sc) in zip(orig, cur):
                m.set_fill(opacity=fc + (f0 * a - fc) * t, family=False)
                m.set_stroke(opacity=sc + (s0 * a - sc) * t, family=False)
        return UpdateFromAlphaFunc(mob, upd)
    except Exception:                       # Gate A's stub has no opacity model
        return mob.animate.set_opacity(a)


def dim(mob):
    return fade_to(mob, 0.35)


def undim(mob):
    return fade_to(mob, 1.0)


def slide_in(mob, side=LEFT, d=1.0):
    """Characters and big props enter by sliding (never popping)."""
    return FadeIn(mob, shift=-side * d)


def slide_out(mob, side=LEFT, d=1.0):
    return FadeOut(mob, shift=side * d)


def done(self):
    """Hold to the end of the beat's audio, never past it."""
    tgt = _TARGET.get(bid_of(self), 0)
    rem = tgt - _elapsed(self) - 0.06
    if not tgt:
        self.wait(1.0)
    elif rem > 0.05:
        self.wait(rem)


def key(s, x, y, size=KEY):
    return T(s, size, INK, bold=True).move_to([x, y, 0])


def lab(s, x, y, size=SEC, bold=False):
    return T(s, size, INK, bold=bold).move_to([x, y, 0])


TAG_INK = "#5E594E"     # source tags: a lighter ink that still clears 4.5:1 contrast on the stage


def tag(s, x, y, color=TAG_INK):
    return T(s, TAG, color).move_to([x, y, 0])


ROBOT_S = 1.1           # the robot is the same size in every beat


def tag_constructed(x=4.9, y=3.15):
    return T("CONSTRUCTED", TAG, bold=True).move_to([x, y, 0])


def chip(s, x, y, size=44, bold=True):
    """A title chip: ink words on a white pill with a kraft edge."""
    t = T(s, size, INK, bold=bold)
    r = RoundedRectangle(width=t.width + 0.55, height=t.height + 0.36, corner_radius=0.2, fill_color=PAGE_TOP, fill_opacity=1,
                         stroke_color=KRAFT_DEEP, stroke_width=3)
    g = VGroup(r, t).move_to([x, y, 0])
    return g


def card(s, x, y, size=36, w=None, bold=False):
    """A paper card carrying real words."""
    t = T(s, size, INK, bold=bold)
    r = RoundedRectangle(width=(w or t.width + 0.5), height=t.height + 0.34, corner_radius=0.1, fill_color=PAGE_TOP, fill_opacity=1,
                         stroke_color=BAR1, stroke_width=3)
    return VGroup(r, t).move_to([x, y, 0])


def say(left_x, y, s, size=36):
    """A speech bubble with real words, left edge at left_x, tail pointing left (to the speaker)."""
    t = T(s, size, INK)
    w, h = t.width + 0.6, t.height + 0.42
    body = RoundedRectangle(width=w, height=h, corner_radius=0.22, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4)
    body.move_to([left_x + w / 2, y, 0])
    t.move_to(body.get_center())
    tail = Polygon([left_x + 0.06, y + 0.14, 0], [left_x + 0.06, y - 0.14, 0], [left_x - 0.32, y - 0.06, 0],
                   fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(tail, body, t)


def xmark(x, y, s=0.28, w=9):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


def bookcase(iso, x0, y0, w=2.6, d=0.8, h=2.7, shelves=3, seed=0, glow=None):
    r = _rnd.Random(seed)
    case = iso.box(x0, y0, 0, w, d, h)
    planks, books = VGroup(), VGroup()
    g = VGroup(case, planks, books)
    g.glow = None
    step = (h - 0.25) / shelves
    for k in range(shelves):
        z0 = 0.12 + k * step
        planks.add(Line(iso.p(x0, y0, z0), iso.p(x0 + w, y0, z0), color=INK, stroke_width=3))
        a, slot = x0 + 0.14, 0
        while a < x0 + w - 0.3:
            bw = r.uniform(0.16, 0.26)
            bh = r.uniform(0.62, 0.92) * (step - 0.12)
            is_glow = glow is not None and glow == (k, slot)
            fill = PAGE_TOP if is_glow else r.choice(SPINES)
            bk = iso.quad([(a, y0, z0), (a + bw, y0, z0), (a + bw, y0, z0 + bh), (a, y0, z0 + bh)], fill, sw=2)
            books.add(bk)
            if is_glow:
                dot = Dot(iso.p(a + bw / 2, y0, z0 + bh * 0.78), radius=0.07, color=TERRA)
                books.add(dot)
                g.glow = VGroup(bk, dot)
            a += bw + 0.07
            slot += 1
    return g


def library(ox, oy, s=0.6, n=3, seed=1, glow=None, gap=1.5):
    iso = Iso(ox, oy, s)
    cases = [bookcase(iso, 0, i * gap, seed=seed + i, glow=glow if i == 0 else None) for i in range(n)]
    g = VGroup(*reversed(cases))
    g.cases = cases
    g.glow = cases[0].glow
    return g


def cart(ox, oy, s=1.0, tool=None, books=True):
    """A LIBRARIAN: kraft book cart on dark wheels; tool = 'glass' (BM25) or 'bulb' (embedding)."""
    iso = Iso(ox, oy, s)
    wheels = VGroup(*[Circle(radius=0.17 * s, fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3)
                      .move_to(iso.p(fx, 0, 0.17)) for fx in (0.35, 1.45)])
    body = iso.box(0, 0, 0.3, 1.8, 1.0, 0.75)
    g = VGroup(wheels, body)
    if books:
        for i, (fill, hgt) in enumerate([(BOX_TOP, 0.55), (PAGE_TOP, 0.48), (BOX_TOP, 0.42)]):
            g.add(iso.box(0.18 + i * 0.4, 0.3, 1.05, 0.26, 0.5, hgt, fill, PAGE_L if fill == PAGE_TOP else BOX_L, BOX_R, sw=2))
    base = iso.p(1.6, 0.55, 1.05)
    tip = base + UP * 1.25 * s
    g.tool = None
    if tool:
        g.add(Line(base, tip, color=INK, stroke_width=5))
    if tool == "glass":
        lens = Circle(radius=0.36 * s, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=7).move_to(tip + UP * 0.34 * s)
        g.tool = VGroup(lens)
        g.add(g.tool)
    elif tool == "bulb":
        sock = Rectangle(width=0.3 * s, height=0.2 * s, fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(tip + UP * 0.1 * s)
        glass = Circle(radius=0.34 * s, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to(tip + UP * 0.5 * s)
        g.tool = VGroup(sock, glass)
        g.add(g.tool)
    g.tool_center = tip + UP * (0.34 if tool == "glass" else 0.5) * s
    g.top = iso.p(0.9, 0.5, 1.6)
    return g


def light_bulb(c, s=1.0):
    return VGroup(Circle(radius=0.62 * s, stroke_color=GHOST, stroke_width=12).move_to(c), Dot(c, radius=0.09 * s, color=TERRA))


def robot(x, y, s=1.0):
    """The ROBOT (the AI agent)."""
    iso = Iso(x, y, s)
    wheels = VGroup(*[Circle(radius=0.15 * s, fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3)
                      .move_to(iso.p(fx, -0.4, 0.15)) for fx in (-0.3, 0.35)])
    body = iso.box(-0.5, -0.4, 0.25, 1.0, 0.8, 0.85)
    head = iso.box(-0.42, -0.32, 1.15, 0.84, 0.64, 0.55, DARK_TOP, DARK_L, DARK_R)
    eyes = VGroup(Dot(iso.p(-0.15, -0.32, 1.45), radius=0.07 * s, color=TERRA), Dot(iso.p(0.22, -0.32, 1.45), radius=0.07 * s, color=TERRA))
    ant = VGroup(Line(iso.p(0, 0, 1.7), iso.p(0, 0, 2.05), color=INK, stroke_width=4), Dot(iso.p(0, 0, 2.08), radius=0.07 * s, color=INK))
    g = VGroup(wheels, body, head, eyes, ant)
    g.hand = iso.p(0.5, -0.4, 0.75)
    return g


def pile(iso, x0, y0, z0, n=8):
    cols = [(BOX_TOP, BOX_L, BOX_R), (PAGE_TOP, PAGE_L, PAGE_R), (DECOY_TOP, DECOY_L, DECOY_R), (BOX_TOP, BOX_L, BOX_R)]
    return VGroup(*[iso.box(x0 + ((i % 3) - 1) * 0.07, y0 + (i % 2) * 0.06, z0 + i * 0.17, 1.3, 0.85, 0.15, *cols[i % 4], sw=2)
                    for i in range(n)])


def flat_book(x, y, w=0.55, h=0.75, right=False, decoy=False):
    """A 2-D book face: white (right book has a terracotta dot), kraft, or grey decoy."""
    fill = DECOY_L if decoy else (PAGE_TOP if right else BOX_TOP)
    body = RoundedRectangle(width=w, height=h, corner_radius=0.05, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    spine = Line([x - w / 2 + 0.1, y - h / 2 + 0.04, 0], [x - w / 2 + 0.1, y + h / 2 - 0.04, 0], color=INK, stroke_width=3)
    g = VGroup(body, spine)
    if right:
        g.add(Dot([x + 0.05, y + h / 2 - 0.16, 0], radius=0.07, color=TERRA))
    return g


def file_icon(x, y, w=1.0, h=1.25):
    body = Polygon([x - w / 2, y - h / 2, 0], [x + w / 2, y - h / 2, 0], [x + w / 2, y + h / 2 - 0.3, 0], [x + w / 2 - 0.3, y + h / 2, 0], [x - w / 2, y + h / 2, 0],
                   fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
    fold = Polygon([x + w / 2 - 0.3, y + h / 2, 0], [x + w / 2 - 0.3, y + h / 2 - 0.3, 0], [x + w / 2, y + h / 2 - 0.3, 0],
                   fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=3)
    braces = T("{ }", 40, INK, bold=True).move_to([x, y - 0.1, 0])
    return VGroup(body, fold, braces)


def folder(x, y, w=2.2, h=1.5):
    tab = RoundedRectangle(width=w * 0.42, height=0.4, corner_radius=0.08, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x - w * 0.27, y + h / 2 + 0.1, 0])
    body = RoundedRectangle(width=w, height=h, corner_radius=0.1, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(tab, body, Dot([x + w / 2 - 0.3, y + h / 2 - 0.28, 0], radius=0.08, color=TERRA))


def laptop(x, y, s=1.0):
    iso = Iso(x, y, s)
    base = iso.box(-1.3, -0.9, 0, 2.6, 1.8, 0.12)
    screen = iso.quad([(-1.3, 0.9, 0.12), (1.3, 0.9, 0.12), (1.3, 0.9, 1.9), (-1.3, 0.9, 1.9)], DARK_L)
    pane = iso.quad([(-1.15, 0.9, 0.27), (1.15, 0.9, 0.27), (1.15, 0.9, 1.75), (-1.15, 0.9, 1.75)], CARD, sw=2)
    g = VGroup(base, screen, pane)
    g.iso = iso
    return g


def bm25_chart():
    """B06A's finished chart (B06B opens on it, so the '?' can land on the 42% bar)."""
    vals = [(64, "human"), (60, "main rewrite"), (42, "support")]
    xs = [-4.0, -0.2, 3.6]
    floor = RoundedRectangle(width=11.6, height=0.32, corner_radius=0.06, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-0.2, -1.45, 0])
    bars, nums, caps = [], [], []
    for (v, nm), x in zip(vals, xs):
        iso = Iso(x, -1.35, 1.25)
        h = v / 100 * 3.0
        bars.append(iso.box(-0.45, -0.45, 0, 0.9, 0.9, h, BAR3, BAR2, BAR1))
        nums.append(T(f"{v}%", 60, INK, bold=True).move_to([x, -1.35 + 0.56 + 1.25 * h + 0.6, 0]))
        caps.append(lab(nm, x, -2.35, size=44))
    title = key("BM25: right passage in top 100", 0, -3.1, size=42)
    src = tag("source: results/foundation/2026-10-08_bm25/pool_stats.json", 0, 3.05)
    return floor, bars, nums, caps, title, src




# ═════════════════════════════ CARTOON CAST (Rithika, 2026-10-11) ═════════════════════════════
# Rithika authorised generic cartoon people for this film; the toolkit's portrait house rule does not
# apply and no instructor portrait, likeness or name is used. Flat figures from Manim shapes, 4 px ink
# outlines, palette colours only (skin = kraft BOX_L for everyone). Each character is one builder, so it
# looks identical in every beat. Builders return a VGroup with .hand_r / .hand_l / .head_c and, for the
# librarians, .tool and .tool_center (the magnifier or bulb, animatable on its own).
SKIN = BOX_L


def _arm(shoulder, length, w, deg, fill):
    a = np.radians(deg)
    d = np.array([np.sin(a), -np.cos(a), 0.0])
    arm = RoundedRectangle(width=w, height=length, corner_radius=w / 2, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4)
    arm.move_to(np.array(shoulder) + d * length / 2).rotate(a, about_point=np.array(shoulder) + d * length / 2)
    hand = np.array(shoulder) + d * length
    return arm, hand


def _cap(c, r, color, a0=10, a1=170, brow=0.3):
    pts = [np.array(c) + r * 1.04 * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) for a in np.linspace(a0, a1, 14)]
    pts += [np.array(c) + np.array([-r * 0.92, r * brow, 0]), np.array(c) + np.array([r * 0.92, r * brow, 0])]
    return Polygon(*pts, fill_color=color, fill_opacity=1, stroke_color=INK, stroke_width=4)


def person(x, y0, h, top, bottom, hair="short", hair_color=DARK_L, wf=1.0, arm_r=0, arm_l=0, eyes="open",
           glasses=False, bowtie=False, beard=False, buttons=False, mouth=True):
    u = h / 6.0
    g = VGroup()
    for sx in (-1, 1):                                                         # legs + shoes
        g.add(RoundedRectangle(width=0.55 * u, height=2.2 * u, corner_radius=0.12 * u, fill_color=bottom, fill_opacity=1,
                               stroke_color=INK, stroke_width=4).move_to([x + sx * 0.33 * u * wf, y0 + 1.15 * u, 0]))
        g.add(RoundedRectangle(width=0.78 * u, height=0.48 * u, corner_radius=0.16 * u, fill_color=DARK_L, fill_opacity=1,
                               stroke_color=INK, stroke_width=3).move_to([x + sx * 0.4 * u * wf, y0 + 0.24 * u, 0]))   # tall enough that GATE T never reads a (dimmed) shoe as sub-floor text
    head_c = np.array([x, y0 + 5.1 * u, 0])
    r = 0.72 * u
    if hair == "long":                                                         # long hair falls behind the shoulders
        g.add(RoundedRectangle(width=3.0 * r, height=4.2 * r, corner_radius=1.0 * r, fill_color=hair_color, fill_opacity=1,
                               stroke_color=INK, stroke_width=4).move_to(head_c + DOWN * 1.15 * r))
    torso = RoundedRectangle(width=1.7 * u * wf, height=2.4 * u, corner_radius=0.35 * u, fill_color=top, fill_opacity=1,
                             stroke_color=INK, stroke_width=4).move_to([x, y0 + 3.3 * u, 0])
    sh_r = np.array([x + 0.72 * u * wf, y0 + 4.2 * u, 0])
    sh_l = np.array([x - 0.72 * u * wf, y0 + 4.2 * u, 0])
    ar, hand_r = _arm(sh_r, 2.0 * u, 0.48 * u, arm_r, top)
    al, hand_l = _arm(sh_l, 2.0 * u, 0.48 * u, -arm_l, top)
    g.add(al, torso, ar)
    if buttons:
        g.add(Line([x, y0 + 4.4 * u, 0], [x, y0 + 2.2 * u, 0], color=INK, stroke_width=3),
              *[Dot([x + 0.18 * u, y0 + (3.9 - k * 0.6) * u, 0], radius=0.06 * u + 0.01, color=INK) for k in range(3)])
    g.add(*[Circle(radius=0.2 * u, fill_color=SKIN, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(p) for p in (hand_r, hand_l)])
    g.add(Rectangle(width=0.4 * u, height=0.3 * u, fill_color=SKIN, fill_opacity=1, stroke_width=0).move_to([x, y0 + 4.5 * u, 0]))  # neck
    if hair == "long":                                                         # front locks fall over the shoulders
        g.add(*[RoundedRectangle(width=0.5 * r, height=2.3 * r, corner_radius=0.24 * r, fill_color=hair_color, fill_opacity=1,
                                 stroke_color=INK, stroke_width=4).move_to(head_c + np.array([sx * 0.88 * r, -1.0 * r, 0])) for sx in (-1, 1)])
    g.add(Circle(radius=r, fill_color=SKIN, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(head_c))
    if hair in ("long", "short"):
        g.add(_cap(head_c, r, hair_color, brow=0.35 if hair == "long" else 0.45))
    elif hair == "sides":                                                      # bald on top, grey tufts at the sides
        g.add(*[Ellipse(width=0.42 * r, height=0.7 * r, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=3)
                .move_to(head_c + np.array([sx * 0.98 * r, 0.15 * r, 0])) for sx in (-1, 1)])
    elif hair == "white":
        g.add(_cap(head_c, r, PAGE_TOP, brow=0.5))
    elif hair == "messy":
        pts = [head_c + r * 1.05 * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) * (1.18 if i % 2 else 1.0) for i, a in enumerate(np.linspace(5, 175, 11))]
        pts += [head_c + np.array([-r * 0.95, r * 0.35, 0]), head_c + np.array([r * 0.95, r * 0.35, 0])]
        g.add(Polygon(*pts, fill_color=hair_color, fill_opacity=1, stroke_color=INK, stroke_width=4))
    ey = head_c[1] + 0.02 * r
    for sx in (-1, 1):
        ex = head_c[0] + sx * 0.36 * r
        if eyes == "sleepy":
            g.add(Line([ex - 0.16 * r, ey, 0], [ex + 0.16 * r, ey, 0], color=INK, stroke_width=4))
        else:
            g.add(Dot([ex, ey, 0], radius=0.09 * r + 0.012, color=INK))
        if glasses:
            g.add(Circle(radius=0.24 * r, stroke_color=INK, stroke_width=3).move_to([ex, ey, 0]))
    if glasses:
        g.add(Line([head_c[0] - 0.12 * r, ey, 0], [head_c[0] + 0.12 * r, ey, 0], color=INK, stroke_width=3))
    if beard:
        bp = [head_c + r * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) for a in np.linspace(195, 345, 10)]
        bp += [head_c + np.array([0.45 * r, -1.35 * r, 0]), head_c + np.array([0, -1.6 * r, 0]), head_c + np.array([-0.45 * r, -1.35 * r, 0])]
        g.add(Polygon(*bp, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4))
    elif mouth:
        g.add(Arc(radius=0.3 * r, start_angle=PI * 1.2, angle=PI * 0.6, color=INK, stroke_width=4).move_to(head_c + DOWN * 0.42 * r))
    if bowtie:
        bc = np.array([x, y0 + 4.42 * u, 0])
        g.add(Polygon(bc, bc + np.array([-0.32 * u, 0.15 * u, 0]), bc + np.array([-0.32 * u, -0.15 * u, 0]), fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3),
              Polygon(bc, bc + np.array([0.32 * u, 0.15 * u, 0]), bc + np.array([0.32 * u, -0.15 * u, 0]), fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3))
    g.hand_r, g.hand_l, g.head_c, g.u = hand_r, hand_l, head_c, u
    return g


def me(x, y0, h=2.7):
    """ME (Rithika): long dark hair, waving."""
    return person(x, y0, h, top=PAGE_TOP, bottom=DARK_L, hair="long", hair_color=DARK_TOP, wf=0.95, arm_r=150, arm_l=10)


def keyword_librarian(x, y0, h=3.0):
    """KEYWORD LIBRARIAN (BM25): tall thin old man, round glasses, bow tie, magnifying glass."""
    g = person(x, y0, h, top=BAR1, bottom=DARK_L, hair="sides", wf=0.78, arm_r=110, arm_l=8, glasses=True, bowtie=True)
    c = g.hand_r + np.array([0.25, 0.42, 0]) * (h / 3.0)
    lens = VGroup(Line(g.hand_r, c + np.array([-0.17, -0.2, 0]) * (h / 3.0), color=INK, stroke_width=7),
                  Circle(radius=0.32 * h / 3.0, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=7).move_to(c))
    g.tool, g.tool_center = lens, c
    g.add(lens)
    return g


def meaning_librarian(x, y0, h=2.6):
    """MEANING LIBRARIAN (embedding): shorter old man, white beard, cardigan, lightbulb held up."""
    g = person(x, y0, h, top=BOX_R, bottom=BAR1, hair="white", wf=1.15, arm_r=125, arm_l=10, beard=True, buttons=True)
    k = h / 2.6
    sock = Rectangle(width=0.26 * k, height=0.2 * k, fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(g.hand_r + UP * 0.2 * k)
    glass = Circle(radius=0.3 * k, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to(g.hand_r + UP * 0.58 * k)
    g.tool, g.tool_center = VGroup(sock, glass), g.hand_r + UP * 0.58 * k
    g.add(g.tool)
    return g


def lazy_librarian(x, y0, h=2.6):
    """LAZY LIBRARIAN: sleepy young assistant, half-closed eyes, arm out for thin books."""
    return person(x, y0, h, top=BAR2, bottom=BOX_R, hair="messy", hair_color=DARK_L, arm_r=55, arm_l=12, eyes="sleepy")


def searcher(x, y0, h=2.6):
    """SEARCHER: generic person typing on a phone."""
    g = person(x, y0, h, top=BOX_L, bottom=DARK_L, hair="short", hair_color=DARK_L, arm_r=-42, arm_l=-42)
    k = h / 2.6
    c = (g.hand_r + g.hand_l) / 2 + UP * 0.22 * k
    ph = VGroup(RoundedRectangle(width=0.42 * k, height=0.66 * k, corner_radius=0.06 * k, fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(c),
                RoundedRectangle(width=0.3 * k, height=0.46 * k, corner_radius=0.03 * k, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to(c + UP * 0.03 * k))
    g.add(ph)
    g.phone = ph
    g.phone_top = c + UP * 0.33 * k
    return g


def reviewer(x, y0, h=2.2):
    """REVIEWER: generic person holding a coffee cup."""
    g = person(x, y0, h, top=BAR2, bottom=DARK_L, hair="short", hair_color=BOX_R, arm_r=-25, arm_l=10)
    k = h / 2.2
    cup = VGroup(Arc(radius=0.1 * k, start_angle=-PI / 2, angle=PI, color=INK, stroke_width=4).move_to(g.hand_r + np.array([0.2 * k, 0.12 * k, 0])),
                 RoundedRectangle(width=0.3 * k, height=0.36 * k, corner_radius=0.05, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(g.hand_r + UP * 0.12 * k))
    g.add(cup)
    return g


def say_down(cx, y, s, size=40):
    """A speech bubble centred at (cx, y) with its tail pointing down-left (to a speaker below)."""
    t = T(s, size, INK)
    w, h = t.width + 0.6, t.height + 0.42
    body = RoundedRectangle(width=w, height=h, corner_radius=0.22, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([cx, y, 0])
    t.move_to(body.get_center())
    bx = cx - w * 0.2
    tail = Polygon([bx - 0.16, y - h / 2 + 0.06, 0], [bx + 0.16, y - h / 2 + 0.06, 0], [bx - 0.3, y - h / 2 - 0.36, 0],
                   fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(tail, body, t)


def say_r(right_x, y, s, size=36):
    """A speech bubble with real words, right edge at right_x, tail pointing right (to the speaker)."""
    t = T(s, size, INK)
    w, h = t.width + 0.6, t.height + 0.42
    body = RoundedRectangle(width=w, height=h, corner_radius=0.22, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4)
    body.move_to([right_x - w / 2, y, 0])
    t.move_to(body.get_center())
    tail = Polygon([right_x - 0.06, y + 0.14, 0], [right_x - 0.06, y - 0.14, 0], [right_x + 0.32, y - 0.06, 0],
                   fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(tail, body, t)


# ═════════════════════════════ SCENES (v4 choreography, 2026-10-11) ═════════════════════════════
# Staging rules (Rithika): enter on the word (word_times.json), exit or dim when the narration moves on,
# one focus at a time, the same easing (smooth) and 0.4–0.6 s entrances everywhere, characters slide in
# and out (keyword librarian LEFT, meaning librarian RIGHT), the robot is ROBOT_S everywhere, and every
# beat's final state holds >= 1 s. Cues the midpoint guard had to hold are printed as [guard] lines.

class B01_Hook(Scene):
    def construct(self):
        box = RoundedRectangle(width=7.0, height=0.95, corner_radius=0.47, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=KRAFT_DEEP, stroke_width=5).move_to([-2.7, 2.85, 0])
        lens = VGroup(Circle(radius=0.2, stroke_color=INK, stroke_width=5).move_to([0.25, 2.9, 0]), Line([0.39, 2.76, 0], [0.57, 2.58, 0], color=INK, stroke_width=5))
        q = T("when is ski season over", 44, INK)
        q.move_to([-2.9, 2.85, 0]).align_to(box, LEFT).shift(RIGHT * 0.45)
        yours = key("your question", 3.6, 2.85, size=44)
        src = tag("real example · MS MARCO dev · rewritten by Claude Haiku, Oct 8, 2026", 0, 2.12)
        src.align_to(box, LEFT)
        who = searcher(-4.6, -3.4, h=3.9)
        self.add(box, lens, who)
        typing = VGroup(*[Dot(who.phone_top + np.array([-0.2 + k * 0.2, 0.25, 0]), radius=0.06, color=INK) for k in range(3)])
        P(self, Write(q), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in typing], lag_ratio=0.3), rt=1.2)
        P(self, FadeIn(yours, scale=0.7), FadeIn(src), FadeOut(typing), rt=0.5)
        at(self, "an ai assistant")
        P(self, slide_out(who, LEFT, 1.2), rt=0.45)
        bot = robot(-4.5, -2.6, s=ROBOT_S)
        P(self, slide_in(bot, RIGHT, 1.2), rt=0.5)
        rewrites = ["when does ski season end", "ski season closing dates by region",
                    "last day of skiing spring conditions", "ski resort operating schedule winter spring"]
        ys = [1.15, 0.25, -0.65, -1.55]
        bubs = [say(-2.9, y, r, 34) for r, y in zip(rewrites, ys)]
        at(self, "several searches")
        P(self, LaggedStart(*[FadeIn(b, shift=RIGHT * 0.5) for b in bubs], lag_ratio=0.45), rt=1.3)
        pop(self, key("agent's 4 searches", 1.5, -2.5, size=44))
        at(self, "the right answer")
        ring = SurroundingRectangle(VGroup(*bubs), buff=0.18, color=KRAFT_DEEP, stroke_width=4, corner_radius=0.15)
        P(self, Create(ring), rt=0.5)
        done(self)


class B02_Pile(Scene):
    def construct(self):
        lib = library(-3.7, -3.2, s=0.72, n=3, seed=5, glow=(1, 3))
        dsk = Iso(1.0, -3.1, 0.9)
        desk = dsk.box(0, 0, 0, 3.0, 1.6, 1.0)
        bot = robot(5.2, -2.25, s=ROBOT_S)
        self.add(desk, bot)                                          # the robot waits at the desk the whole time
        at(self, "among millions")
        P(self, FadeIn(lib, shift=UP * 0.3), FadeIn(key("8.8 million passages", -3.4, 2.75)), FadeIn(tag("MS MARCO passage collection", -3.4, 2.05)), rt=0.5)
        at(self, "librarian")
        kc = keyword_librarian(-1.85, -3.4, h=2.4)
        P(self, slide_in(kc, LEFT, 1.2), rt=0.55)
        at(self, "a hundred books")
        stack = pile(dsk, 0.8, 0.3, 1.0, n=9)
        top = key("top 100", 1.6, 1.95)
        P(self, LaggedStart(*[FadeIn(sl, shift=DOWN * 0.3) for sl in stack], lag_ratio=0.08), FadeIn(top, scale=0.7), rt=0.45)
        at(self, "right book")
        right = lab("right answer", -0.7, 0.55, size=42, bold=True)
        lead = Line(right.get_left() + LEFT * 0.15 + DOWN * 0.05, lib.glow.get_center() + np.array([0.3, 0.1, 0]), color=INK, stroke_width=4)
        ring = Circle(radius=0.45, stroke_color=TERRA, stroke_width=6).move_to(lib.glow.get_center())
        P(self, FadeIn(right, scale=0.7), Create(lead), Create(ring), dim(kc), dim(stack), dim(top), rt=0.45)
        at(self, "isnt in that pile")
        gap = DashedLine(lib.glow.get_center() + RIGHT * 0.45, np.array([0.9, -0.3, 0]), dash_length=0.15, color=KRAFT_DEEP, stroke_width=5)
        P(self, Create(gap), FadeIn(xmark(0.35, -0.05), scale=0.7), FadeIn(key("missed = AI never sees it", 3.0, 2.95, size=42), scale=0.7), rt=0.5)
        done(self)


class B03_Librarians(Scene):
    def construct(self):
        kc = keyword_librarian(-3.5, -3.4, h=3.0)
        mc = meaning_librarian(3.2, -3.4, h=2.6)
        kc.tool._qc_intentional = True     # the magnifier reading the book's words IS the claim
        self.add(tag_constructed(0, -3.1))
        at(self, "two kinds")
        P(self, slide_in(kc, LEFT, 1.2), slide_in(mc, RIGHT, 1.2), rt=0.55)
        qcard = card("query: car repair cost", 0, 2.95, size=40, bold=True)
        ba = card("car repair cost", -3.4, 1.9, size=38)
        sw = lab("same words", -3.4, 1.1, size=42, bold=True)
        ck1 = check(-1.0, 1.95, s=0.22, color=TERRA)
        chip_l = chip("BM25: keyword search", -3.4, 0.3, size=38)
        at(self, "exact words")
        P(self, FadeIn(qcard, scale=0.9), FadeIn(ba, shift=DOWN * 0.3), FadeIn(chip_l, scale=0.7), dim(mc), rt=0.5)
        lens0 = kc.tool.get_center()
        P(self, kc.tool.animate.move_to(ba.get_center() + DOWN * 0.05), rt=0.5)
        P(self, FadeIn(sw, scale=0.7), Create(ck1), rt=0.45)
        at(self, "its called")
        P(self, kc.tool.animate.move_to(lens0), rt=0.45)
        left = VGroup(kc, ba, sw, ck1, chip_l)
        bb = card("fixing an automobile price", 3.4, 1.9, size=36)
        sm = lab("same meaning", 3.4, 1.1, size=42, bold=True)
        chip_r = chip("Embedding: meaning search", 3.2, 0.3, size=36)
        at(self, "meaning")
        P(self, dim(left), undim(mc), FadeIn(bb, shift=DOWN * 0.3), FadeIn(chip_r, scale=0.7), rt=0.5)
        P(self, FadeIn(light_bulb(mc.tool_center, s=0.85)), FadeIn(sm, scale=0.7), rt=0.45)
        at(self, "an ai model")
        P(self, undim(left), rt=0.45)
        done(self)


class B04_Repo(Scene):
    def construct(self):
        rith = me(0.0, -3.3, h=3.7)
        hi = say_down(1.15, 1.25, "hi!", size=44)
        at(self, "rithika")
        P(self, slide_in(rith, LEFT, 1.0), rt=0.45)
        pop(self, hi, rt=0.4)
        at(self, "agentic retrieval lab")
        P(self, slide_out(rith, RIGHT, 1.2), FadeOut(hi), FadeIn(key("Agentic Retrieval Lab", 0, 2.95, size=60), scale=0.7), rt=0.5)
        iso = Iso(-3.3, -2.9, 0.95)
        plinth = iso.box(-0.2, -0.2, -0.3, 3.0, 2.4, 0.3, DARK_TOP, DARK_L, DARK_R)
        cab = iso.box(0, 0, 0, 2.6, 2.0, 3.0, BOX_L, BOX_R, "#B39A72")
        fronts = []
        for i in range(3):
            z = 0.2 + i * 0.95
            fr = iso.quad([(0.3, 0, z), (2.3, 0, z), (2.3, 0, z + 0.75), (0.3, 0, z + 0.75)], BOX_TOP)
            fronts.append(VGroup(fr, Dot(iso.p(1.3, 0, z + 0.38), radius=0.08, color=INK)))
        at(self, "github repository")
        P(self, FadeIn(VGroup(plinth, cab, *fronts), shift=UP * 0.3), rt=0.5)
        names = {2: "pipeline", 1: "tests", 0: "results"}
        for i, cue in [(2, "python pipeline"), (1, "tests"), (0, "dated result files")]:
            at(self, cue)
            z = 0.2 + i * 0.95
            tray_back, tray_front = iso.open_box(0.3, -1.0, z, 2.0, 1.0, 0.75)
            inside = VGroup()
            if i == 2:
                inside.add(*[iso.box(0.5 + k * 0.55, -0.8, z, 0.35, 0.5, 0.35, DARK_TOP, DARK_L, DARK_R) for k in range(3)])
            elif i == 1:
                inside.add(*[check(*iso.p(0.7 + k * 0.5, -0.5, z + 0.4)[:2], s=0.12, color=INK, w=5) for k in range(3)])
            else:
                inside.add(*[iso.box(0.5 + k * 0.5, -0.85, z, 0.32, 0.65, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5) for k in range(3)])
            drawer = VGroup(tray_back, inside, tray_front)
            nm = lab(names[i], 0, 0, size=46, bold=True).move_to(iso.p(2.3, -1.0, z + 0.4) + RIGHT * 1.15)
            P(self, FadeOut(fronts[i]), FadeIn(drawer, shift=iso.v(0, -0.5, 0)), FadeIn(nm, scale=0.7), rt=0.4)
        at(self, "write up")
        P(self, FadeIn(file_icon(5.2, 1.75, w=1.2, h=1.5), shift=LEFT * 0.3), FadeIn(lab("write-up", 5.2, 0.7, size=40, bold=True), scale=0.7), rt=0.45)
        at(self, "agentic here means")
        bot = robot(5.35, -1.75, s=ROBOT_S)
        P(self, slide_in(bot, RIGHT, 0.35), rt=0.5)          # short slide: the robot starts near the right safe edge
        at(self, "agent written queries")
        pop(self, chip("agentic = agent-written queries", 2.0, -3.0, size=36))
        at(self, "not building")
        P(self, dim(bot), rt=0.45)
        done(self)


class B05_Built(Scene):
    def construct(self):
        xs = [-4.8, -1.6, 1.6, 4.8]
        nums = ["300", "1,200", "8.8M", "103"]
        words = ["questions", "rewrites", "passages", "tests"]
        cues = ["300", "rewrite each", "8 8 million", "103"]
        tops = [(BOX_TOP, BOX_L, BOX_R), (PAGE_TOP, PAGE_L, PAGE_R), (BOX_TOP, BOX_L, BOX_R), (PAGE_TOP, PAGE_L, PAGE_R)]
        plinths = VGroup(*[Iso(x, -1.55, 1.0).box(-0.82, -0.82, -0.25, 1.64, 1.64, 0.25, DARK_TOP, DARK_L, DARK_R) for x in xs])
        self.add(plinths)
        at(self, "this week")
        P(self, FadeIn(tag("built Oct 5–9, 2026 · source: results/foundation/", 0, 3.2)), rt=0.45)
        cols = []
        for k in range(4):
            at(self, cues[k])
            iso = Iso(xs[k], -1.55, 1.0)
            blk = iso.box(-0.65, -0.65, 0, 1.3, 1.3, 1.25, *tops[k])
            col = VGroup(blk, key(nums[k], xs[k], 1.35, size=72), lab(words[k], xs[k] - (0.25 if k == 3 else 0), -2.95, size=44))
            anims = [FadeIn(blk, shift=DOWN * 0.6), FadeIn(col[1], scale=0.7), FadeIn(col[2], scale=0.7)]
            if k == 3:
                anims += [Create(check(xs[3] + 0.95, -2.9, s=0.24, color=TERRA, w=9))] + [undim(c) for c in cols]
            elif cols:
                anims += [dim(cols[-1])]
            P(self, *anims, rt=0.45)
            cols.append(col)
        done(self)


class B06A_Bars(Scene):
    def construct(self):
        floor, bars, nums, caps, title, src = bm25_chart()
        self.add(floor, src, *caps)
        at(self, "top 100")
        pop(self, title)
        for k, cue in enumerate(["64", "60", "42"]):
            at(self, cue)
            anims = [GrowFromEdge(bars[k], DOWN), FadeIn(nums[k], scale=0.7)]
            if k:
                anims += [dim(VGroup(bars[k - 1], nums[k - 1]))]
            P(self, *anims, rt=0.5)
        done(self)


class B06B_AnswerKey(Scene):
    def construct(self):
        floor, bars, nums, caps, title, src = bm25_chart()
        chart = VGroup(floor, *bars, *nums, *caps, title, src)
        self.add(chart)
        for k in (0, 1):                                            # B06A ended with 64 and 60 dimmed
            VGroup(bars[k], nums[k]).set_opacity(0.35)
        qm = T("?", 90, INK, bold=True).next_to(nums[2], RIGHT, buff=0.25)
        at(self, "dont trust")
        pop(self, qm, rt=0.4)
        board = RoundedRectangle(width=4.2, height=4.9, corner_radius=0.15, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-3.6, -0.55, 0])
        paper_ = Rectangle(width=3.7, height=4.2, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=2).move_to([-3.6, -0.7, 0])
        clip = RoundedRectangle(width=1.1, height=0.36, corner_radius=0.08, fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([-3.6, 1.88, 0])
        key_ = VGroup(board, paper_, clip, key("answer key: 1 per question", -3.25, 2.75, size=40))
        at(self, "the answer key", lead=0.1)
        P(self, FadeOut(VGroup(chart, qm), shift=LEFT * 1.0), rt=0.4)          # chart leaves first, then the key slides in
        P(self, FadeIn(key_, shift=LEFT * 1.0), rt=0.45)
        rows = VGroup()
        for i in range(4):
            y = 1.0 - i * 0.95
            rows.add(VGroup(lab(f"Q{i + 1}", -4.9, y, size=40, bold=True), flat_book(-3.6, y, w=0.5, h=0.65, right=True), check(-2.5, y, s=0.2, color=INK, w=6)))
        at(self, "just one")
        P(self, LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), rt=0.6)
        self.add(tag_constructed(4.5, 3.15))
        at(self, "support search")
        bot = robot(4.4, -2.55, s=ROBOT_S)
        P(self, slide_in(bot, RIGHT, 1.0), rt=0.45)
        good = VGroup(flat_book(3.2, -0.4, w=0.6, h=0.8, right=True), lab("good match", 3.2, 0.35, size=36, bold=True))
        at(self, "find a good book")
        P(self, FadeIn(good, shift=UP * 0.3), rt=0.4)
        P(self, good.animate.move_to([0.2, 0.35, 0]), rt=0.45)
        at(self, "still be marked")
        P(self, FadeIn(xmark(1.45, -0.05), scale=0.7), FadeIn(lab("not on the key", 1.65, -0.8, size=36, bold=True), scale=0.7),
          FadeIn(key("good book, marked wrong", 2.4, 1.95, size=44), scale=0.7), rt=0.35)
        done(self)


class B07_Alternatives(Scene):
    def construct(self):
        iso = Iso(-4.2, -3.1, 0.85)
        vault = iso.box(0, 0, 0, 2.4, 2.0, 2.4, BAR3, BAR2, BAR1)
        door = Circle(radius=0.62, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to(iso.p(1.2, 0, 1.2)).stretch(0.8, 0)
        hub = Circle(radius=0.18, fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(door.get_center())
        bar_open = iso.box(2.6, -0.25, 1.05, 1.1, 0.25, 0.28, BOX_TOP, BOX_L, BOX_R)
        q2d = key("Q2D-Web", -3.4, 2.95, size=54)
        at(self, "q2d web")
        P(self, FadeIn(VGroup(vault, door, hub, bar_open), shift=UP * 0.3), FadeIn(q2d, scale=0.7), rt=0.5)
        m190 = lab("190M documents", -3.4, 2.15, size=42, bold=True)
        at(self, "190 million")
        pop(self, m190)
        at(self, "data is private")
        priv = chip("private data", -3.4, 1.35, size=40)
        lockdot = Dot(iso.p(1.2, -0.25, 1.6), radius=0.1, color=TERRA)
        P(self, bar_open.animate.shift(iso.v(-1.3, 0, 0)), FadeIn(priv, scale=0.7), FadeIn(lockdot), rt=0.4)
        board = VGroup(RoundedRectangle(width=1.3, height=1.0, corner_radius=0.1, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.0, -1.9, 0]))
        for k, hh in enumerate([0.6, 0.45, 0.3]):
            board.add(Rectangle(width=0.24, height=hh, fill_color=[BAR1, BAR2, BAR1][k], fill_opacity=1, stroke_width=0).move_to([-1.35 + k * 0.35, -2.3 + hh / 2, 0]))
        lb = lab("public leaderboard only", -1.2, -3.0, size=34, bold=True)
        at(self, "leaderboard")
        P(self, FadeIn(board, scale=0.7), FadeIn(lb, scale=0.7), rt=0.45)
        jso = Iso(2.3, -3.1, 0.85)
        back, front = jso.open_box(0, 0, 0, 2.4, 1.4, 0.9)
        slips = VGroup(*[card(q, 0, 0, size=32) for q in ["when is ski season over", "weather in warwick"]])
        for k, sl in enumerate(slips):
            sl.move_to([3.15, -0.45 + k * 0.72, 0])
        slips.set_z_index(1)
        front.set_z_index(2)
        at(self, "ms marko")
        P(self, fade_to(VGroup(vault, door, hub, bar_open, lockdot, q2d, m190, priv, board, lb), 0.5),   # 50%, not 35%: Gate V contrast floor
          FadeIn(VGroup(back, front), shift=UP * 0.3), LaggedStart(*[FadeIn(s_, shift=UP * 0.4) for s_ in slips], lag_ratio=0.3),
          FadeIn(key("MS MARCO", 3.4, 2.95, size=54), scale=0.7), rt=0.6)
        at(self, "is public")
        pop(self, chip("public", 3.4, 2.15, size=38))
        at(self, "written by humans")
        pop(self, lab("human-written", 1.9, 1.4, size=34, bold=True))
        at(self, "about one answer")
        pop(self, lab("~1 answer each", 4.85, 1.4, size=32, bold=True), rt=0.35)
        done(self)


class B08_Team(Scene):
    def construct(self):
        kc = keyword_librarian(-4.95, -3.4, h=2.9)
        mc = meaning_librarian(-2.05, -3.4, h=2.5)
        kl = lab("BM25", -4.7, 0.3, size=38, bold=True)
        ml = lab("embedding", -1.75, 0.3, size=38, bold=True)
        at(self, "keyword librarian")
        P(self, slide_in(kc, LEFT, 1.2), FadeIn(kl, scale=0.7), rt=0.55)
        at(self, "the most books")
        uniq = VGroup(*[flat_book(-5.9 + k * 0.55, 1.2, w=0.45, h=0.6, right=True) for k in range(3)])
        P(self, LaggedStart(*[FadeIn(u, shift=DOWN * 0.4) for u in uniq], lag_ratio=0.3), FadeIn(chip("paper: BM25 finds unique books", -2.6, 2.95, size=36), scale=0.7), rt=0.55)
        at(self, "the two")
        P(self, slide_in(mc, RIGHT, 1.2), FadeIn(ml, scale=0.7), rt=0.55)
        at(self, "as a team")
        P(self, kc.animate.shift(RIGHT * 0.5), mc.animate.shift(LEFT * 0.4), rt=0.5)
        link = Line(np.array(kc.tool_center) + RIGHT * 0.5, np.array(mc.tool_center) + LEFT * 0.3, color=KRAFT_DEEP, stroke_width=7)
        pop(self, link, key("team-up test", -2.5, 1.95, size=46))
        at(self, "small scale")
        pop(self, lab("small scale · public data", 2.4, 0.95, size=36, bold=True))
        at(self, "one laptop")
        lap = laptop(3.1, -2.25, s=0.85)
        num = T("64%", 48, INK, bold=True).move_to(lap.iso.p(0, 0.9, 1.0))
        P(self, FadeIn(lap, shift=UP * 0.3), FadeIn(num), dim(VGroup(kc, mc, kl, ml, uniq, link)), rt=0.5)
        at(self, "every number")
        f = file_icon(5.6, 1.6, w=0.95, h=1.2)
        arr = Arrow(num.get_right() + RIGHT * 0.05, np.array([5.55, 0.95, 0]), buff=0.05, color=INK, stroke_width=6)
        P(self, GrowArrow(arr), FadeIn(f, scale=0.7), FadeIn(lab("results/…json", 4.95, 2.6, size=36, bold=True), scale=0.7), rt=0.45)
        done(self)


class B09_Reader(Scene):
    def construct(self):
        win = RoundedRectangle(width=8.2, height=5.5, corner_radius=0.15, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-2.05, -0.35, 0])
        bar = Rectangle(width=8.2, height=0.55, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-2.05, 2.15, 0])
        fname = T("README.md", 34, CARD, bold=True).move_to([-2.05, 2.15, 0])
        res = lab("Results", -4.75, 1.4, size=44, bold=True)
        cols, rws = [-1.95, 0.6], [0.55, -0.35, -1.25]
        grid = VGroup(*[Line([-5.7, y - 0.45, 0], [1.75, y - 0.45, 0], color=BAR1, stroke_width=4) for y in rws[:-1]] +
                      [Line([x, 0.95, 0], [x, -1.7, 0], color=BAR1, stroke_width=4) for x in (-3.2, -0.65)])
        cells = VGroup(lab("human", cols[0], rws[0], size=38, bold=True), lab("agent", cols[1], rws[0], size=38, bold=True),
                       lab("BM25", -4.45, rws[1], size=38, bold=True), lab("embedding", -4.45, rws[2], size=38, bold=True))
        dashes = VGroup(*[lab("—", x, y, size=40) for x in cols for y in rws[1:]])
        cmd = RoundedRectangle(width=7.3, height=0.6, corner_radius=0.08, fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([-2.05, -2.45, 0])
        ctext = T("$ uv run pytest -q", 34, CARD).move_to([-3.6, -2.45, 0])
        readme = VGroup(win, bar, fname, res, grid, cells, dashes, cmd, ctext)
        rev = reviewer(3.75, -3.4, h=2.9)
        at(self, "hiring manager")
        P(self, FadeIn(readme, shift=UP * 0.3), slide_in(rev, RIGHT, 1.0), FadeIn(tag_constructed(-4.6, 3.0)), rt=0.55)
        c0 = np.array([3.05, 2.55, 0])
        clock = VGroup(Circle(radius=0.62, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to(c0),
                       Rectangle(width=0.3, height=0.2, fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([3.05, 3.28, 0]))
        hand = Line(c0, c0 + UP * 0.45, color=INK, stroke_width=7)
        hub = Dot(c0, radius=0.08, color=TERRA)
        at(self, "first minute")
        P(self, FadeIn(VGroup(clock, hand, hub), scale=0.7), FadeIn(lab("60 seconds", 5.0, 2.55, size=40, bold=True), scale=0.7), rt=0.45)
        steps = [("1 read table", 1.35, "read the results table"), ("2 click a number", 0.6, "click one number"), ("3 rerun tests", -0.15, "one command")]
        marks = [SurroundingRectangle(VGroup(grid, dashes), buff=0.15, color=KRAFT_DEEP, stroke_width=6),
                 Dot([cols[0], rws[1], 0], radius=0.12, color=TERRA),
                 check(1.25, -2.45, s=0.18, color=TERRA, w=7)]
        for k, (s_, y, cue) in enumerate(steps):
            at(self, cue)
            anims = [Rotate(hand, angle=-2 * PI / 3, about_point=c0), FadeIn(key(s_, 4.35, y, size=40), scale=0.7), (Create(marks[k]) if k == 0 else FadeIn(marks[k], scale=0.7))]
            if k:
                anims.append(FadeOut(marks[k - 1]))
            P(self, *anims, rt=0.45)
        at(self, "today that table")
        hl = VGroup(*[Rectangle(width=2.3, height=0.72, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([x, y, 0]) for x in cols for y in rws[1:]])
        hl.set_z_index(1)
        dashes.set_z_index(2)
        self.add(hl)
        hl.set_opacity(0)
        P(self, hl.animate.set_opacity(1), FadeOut(marks[2]), rt=0.45)
        done(self)


class B10_Badges(Scene):
    def construct(self):
        xs = [-4.3, 0, 4.3]
        names = ["fair test", "sourced numbers", "tested code"]
        cues = ["fair test", "ground every number", "check a pipeline"]

        def badge(x, y, k, r=1.25):
            ring = Circle(radius=r, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
            inner = Circle(radius=r * 0.76, fill_color=BOX_TOP, fill_opacity=1, stroke_color=BOX_R, stroke_width=7).move_to([x, y, 0])
            if k == 0:
                icon = VGroup(Line([x - 0.55, y + 0.25, 0], [x + 0.55, y + 0.25, 0], color=INK, stroke_width=7), Line([x, y + 0.25, 0], [x, y - 0.4, 0], color=INK, stroke_width=7),
                              Line([x - 0.3, y - 0.4, 0], [x + 0.3, y - 0.4, 0], color=INK, stroke_width=7))
            elif k == 1:
                icon = file_icon(x, y, w=0.75, h=0.95)
            elif k == 2:
                icon = check(x + 0.05, y + 0.02, s=0.36, color=INK, w=10)
            else:
                sv = Iso(x - 0.2, y - 0.4, 0.32)
                icon = VGroup(*[sv.box(0, 0, i * 0.5, 1.0, 1.0, 0.42, DARK_TOP, DARK_L, DARK_R, sw=2) for i in range(3)])
            return VGroup(ring, inner, icon)

        got = []
        for k, cue in enumerate(cues):
            at(self, cue)
            g = VGroup(badge(xs[k], 1.0, k), key(names[k], xs[k], -0.75, size=48))
            anims = [FadeIn(g, scale=0.7)] + ([dim(got[-1])] if got else [])
            P(self, *anims, rt=0.45)
            got.append(g)
        at(self, "not that")
        b4 = badge(-2.2, -2.3, 3, r=0.85)
        l4 = key("production RAG", 1.3, -2.3, size=48)
        P(self, FadeIn(b4, scale=0.7), FadeIn(l4, scale=0.7), *[undim(g) for g in got], rt=0.4)
        at(self, "shipped")
        strike = Line(l4.get_left() + LEFT * 0.15, l4.get_right() + RIGHT * 0.15, color=INK, stroke_width=8)
        strike._qc_intentional = True     # the strike-through IS the claim ("not a production system")
        cross = xmark(-2.2, -2.3, s=0.6, w=8)
        cross._qc_intentional = True
        P(self, Create(strike), Create(cross), rt=0.4)
        done(self)


class B11_Scope(Scene):
    def construct(self):
        tray_in = RoundedRectangle(width=5.6, height=3.3, corner_radius=0.15, fill_color=BOX_TOP, fill_opacity=1, stroke_color=KRAFT_DEEP, stroke_width=5).move_to([-3.35, 1.17, 0])
        tray_out = RoundedRectangle(width=4.4, height=2.0, corner_radius=0.15, fill_color=BOX_TOP, fill_opacity=1, stroke_color=KRAFT_DEEP, stroke_width=5).move_to([3.55, 1.78, 0])   # kraft rim: GATE T reads an ink ring round text as overlapping labels
        lin, lout = key("in", -5.75, 3.15, size=50), key("out", 1.75, 3.15, size=50)
        at(self, "in scope")
        P(self, FadeIn(tray_in, shift=UP * 0.2), FadeIn(lin, scale=0.7), rt=0.45)
        cards = VGroup()
        for k, (s_, cue) in enumerate([("embedding vs BM25", "meaning models"), ("human vs agent", "human versus agent"), ("team-up test", "team up test"), ("failure notes", "failure analysis")]):
            at(self, cue)
            c = card(s_, -3.35, 2.25 - k * 0.76, size=36, w=5.0, bold=True)
            pop(self, c, rt=0.4)
            cards.add(c)
        at(self, "out")
        outs = VGroup(*[card(s_, 3.55, 2.25 - k * 0.82, size=38, w=3.8, bold=True) for k, s_ in enumerate(["chatbot", "answer writing"])])
        P(self, FadeIn(tray_out, shift=UP * 0.2), FadeIn(lout, scale=0.7), LaggedStart(*[FadeIn(o, scale=0.7) for o in outs], lag_ratio=0.4), rt=0.55)
        track = RoundedRectangle(width=8.6, height=1.6, corner_radius=0.22, fill_color="#E6E1D5", fill_opacity=1, stroke_color=KRAFT_DEEP, stroke_width=4).move_to([-1.85, -2.65, 0])
        lane = DashedLine([-5.9, -2.65, 0], [2.2, -2.65, 0], dash_length=0.3, color=GHOST, stroke_width=6)
        finish = Line([2.0, -3.35, 0], [2.0, -1.95, 0], color=INK, stroke_width=6)
        kc = keyword_librarian(-5.25, -3.4, h=2.25)
        mc = meaning_librarian(-4.35, -3.25, h=2.05)
        at(self, "race one meaning")
        P(self, FadeIn(VGroup(track, lane, finish), shift=UP * 0.2), slide_in(kc, LEFT, 1.0), slide_in(mc, RIGHT, 1.0),
          dim(VGroup(tray_in, lin, cards, tray_out, lout, outs)), rt=0.55)
        first = key("1 embedding vs BM25", 0.85, -0.95, size=38)
        arr = Arrow(first.get_left() + LEFT * 0.1, np.array(mc.tool_center) + RIGHT * 0.35, buff=0.05, color=INK, stroke_width=6)
        pop(self, arr, first)
        at(self, "against the keyword")
        P(self, mc.animate.shift(RIGHT * 1.8), kc.animate.shift(RIGHT * 1.4), FadeOut(arr), rt=1.2)
        at(self, "dated results folder")
        pop(self, folder(4.55, -1.55, w=2.0, h=1.3), lab("new results/ folder", 4.45, -2.75, size=36, bold=True))
        at(self, "score matches")
        P(self, Create(check(5.85, -2.05, s=0.22, color=TERRA, w=9)), rt=0.35)
        done(self)


class B12_Decoys(Scene):
    def construct(self):
        piv = np.array([-2.2, 0.75, 0])
        post = Line([-2.2, -2.55, 0], piv, color=INK, stroke_width=9)
        base = RoundedRectangle(width=2.0, height=0.35, corner_radius=0.08, fill_color=DARK_L, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([-2.2, -2.7, 0])
        beam = Line(piv + LEFT * 2.0, piv + RIGHT * 2.0, color=INK, stroke_width=9)
        hub = Dot(piv, radius=0.13, color=TERRA)

        def pan(x):
            strings = VGroup(Line([x, 0.75, 0], [x - 0.75, -0.6, 0], color=KRAFT_DEEP, stroke_width=4), Line([x, 0.75, 0], [x + 0.75, -0.6, 0], color=KRAFT_DEEP, stroke_width=4))
            dish = Polygon([x - 0.95, -0.6, 0], [x + 0.95, -0.6, 0], [x + 0.7, -0.85, 0], [x - 0.7, -0.85, 0], fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
            return VGroup(strings, dish)

        lp, rp = pan(-4.2), pan(-0.2)
        scale_ = VGroup(base, post, beam, hub, lp, rp)
        at(self, "test set")
        P(self, FadeIn(scale_, shift=UP * 0.3), FadeIn(tag("source: corpus_stats.json (200k test set)", -2.6, 3.05)), rt=0.5)
        dec = flat_book(-4.2, 0.0, w=1.0, h=1.15, decoy=True)
        good = flat_book(-0.2, -0.12, w=0.42, h=0.9, right=True)
        l65 = VGroup(lab("decoys (BM25-picked)", -4.35, -1.35, size=32, bold=True), lab("65 words", -4.2, -1.95, size=44, bold=True))
        l54 = VGroup(lab("correct", -0.2, -1.35, size=34, bold=True), lab("54 words", -0.2, -1.95, size=44, bold=True))
        at(self, "65 words")
        P(self, FadeIn(dec, shift=DOWN * 0.6), FadeIn(l65, scale=0.7), rt=0.45)
        at(self, "54")
        P(self, FadeIn(good, shift=DOWN * 0.6), FadeIn(l54, scale=0.7), rt=0.45)
        left, right = VGroup(lp, dec, l65), VGroup(rp, good, l54)
        P(self, Rotate(beam, angle=0.1, about_point=piv), left.animate.shift(DOWN * 0.2), right.animate.shift(UP * 0.2), rt=0.55)
        lazy = lazy_librarian(2.55, -2.7, h=2.6)
        hx, hy = lazy.hand_r[0], lazy.hand_r[1]
        thin = VGroup(*[flat_book(hx + 0.15 + k * 0.2, hy + 0.35, w=0.16, h=0.6) for k in range(3)])
        gl = lab("grabs short books", 2.95, -3.05, size=36, bold=True)
        tc = tag_constructed(4.6, 3.05)
        at(self, "grabs short books")
        P(self, slide_in(VGroup(lazy, thin), RIGHT, 1.0), FadeIn(gl, scale=0.7), FadeIn(tc), dim(VGroup(scale_, dec, good, l65, l54)), rt=0.5)
        sb = Iso(5.3, -2.9, 0.9)
        score = sb.box(-0.4, -0.4, 0, 0.8, 0.8, 3.4, BAR3, BAR2, BAR1)
        at(self, "smarter than")
        P(self, GrowFromEdge(score, DOWN), FadeIn(lab("looks good?", 4.85, 1.1, size=40, bold=True), scale=0.7), rt=0.55)
        at(self, "so first")
        stamp = VGroup(Circle(radius=0.62, stroke_color=INK, stroke_width=7).move_to([1.3, 2.25, 0]), check(1.32, 2.25, s=0.28, color=TERRA, w=9))
        pop(self, stamp, key("test first", 3.35, 2.25, size=48))
        at(self, "fix the test set")
        P(self, slide_out(VGroup(lazy, thin), RIGHT, 1.0), FadeOut(gl), rt=0.5)
        done(self)


class B13_Learning(Scene):
    def construct(self):
        c1 = chip("AI/ML engineering · data science", 0, 3.0, size=36)
        c2 = chip("RAG: retrieval · generation · evaluation", 0, 2.2, size=36)
        at(self, "roles")
        pop(self, c1)
        at(self, "rag systems")
        pop(self, c2)
        li = Iso(-4.5, -2.3, 1.0)
        plinth_l = li.box(-0.2, -0.2, -0.3, 2.4, 1.8, 0.3, DARK_TOP, DARK_L, DARK_R)
        have = VGroup(*[li.box(0, 0, k * 0.62, 2.0, 1.4, 0.55, BOX_TOP, BOX_L, BOX_R) for k in range(1)])
        ri = Iso(0.6, -2.3, 1.0)
        plinth_r = ri.box(-0.2, -0.2, -0.3, 2.4, 1.8, 0.3, DARK_TOP, DARK_L, DARK_R)
        learn = [VGroup(*[DashedVMobject(p, num_dashes=7) for p in ri.box(0, 0, k * 0.78, 2.0, 1.4, 0.6, STAGE, STAGE, STAGE)]).set_stroke(KRAFT_DEEP, 5) for k in range(3)]
        track = RoundedRectangle(width=9.0, height=0.36, corner_radius=0.18, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([0, -3.3, 0])
        fill = Rectangle(width=0.01, height=0.26, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-4.45, -3.3, 0], aligned_edge=LEFT)
        at(self, "mostly learning")
        P(self, dim(VGroup(c1, c2)), FadeIn(VGroup(plinth_l, have, plinth_r, *learn, track, fill), shift=UP * 0.3),
          FadeIn(key("already have", -3.9, 1.55, size=48), scale=0.7), FadeIn(key("learning", 4.4, 0.85, size=48), scale=0.7), rt=0.55)
        at(self, "already use")
        top = li.box(0, 0, 0.62, 2.0, 1.4, 0.55, BOX_TOP, BOX_L, BOX_R)
        P(self, FadeIn(top, shift=RIGHT * 0.5), FadeIn(lab("data pipelines", -3.9, 0.95, size=42, bold=True), scale=0.7), rt=0.45)
        names = ["retrieval metrics", "embeddings", "LLM judges"]
        for k, cue in enumerate(["retrieval metrics", "embedding models", "llm"]):
            at(self, cue)
            solid = ri.box(0, 0, k * 0.78, 2.0, 1.4, 0.6, PAGE_TOP, PAGE_L, PAGE_R)
            newfill = Rectangle(width=2.9 * (k + 1), height=0.26, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-4.45, -3.3, 0], aligned_edge=LEFT)
            y = ri.p(1.0, -0.2, k * 0.78 + 0.3)[1]
            P(self, Transform(learn[k], solid), Transform(fill, newfill), FadeIn(lab(names[k], 4.4, y, size=38, bold=True), scale=0.7), rt=0.4)
        done(self)


class BOUT_Close(Scene):
    def construct(self):
        exists = ["repo + tests", "200k test set", "BM25 baseline"]
        will = ["embedding runs", "team-up test", "failure analysis"]
        self.add(key("exists", -3.7, 3.05, size=52))
        rows = []
        for k in range(3):
            y = 2.15 - k * 0.92
            sq = RoundedRectangle(width=0.72, height=0.72, corner_radius=0.1, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([-5.7, y, 0])
            rows.append(VGroup(sq, check(-5.69, y + 0.02, s=0.18, color=INK, w=7), lab(exists[k], 0, y, size=42, bold=True).align_to(np.array([-5.1, 0, 0]), LEFT)))
        at(self, "past tense")
        P(self, LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.5), rt=1.4)
        dashes = VGroup(*[DashedVMobject(RoundedRectangle(width=0.72, height=0.72, corner_radius=0.1).move_to([0.6, 2.15 - k * 0.92, 0]).set_stroke(INK, 5), num_dashes=16) for k in range(3)])
        lw = VGroup(*[lab(will[k], 0, 2.15 - k * 0.92, size=42, bold=True).align_to(np.array([1.2, 0, 0]), LEFT) for k in range(3)])
        at(self, "a plan")
        P(self, FadeIn(key("will", 2.6, 3.05, size=52), scale=0.7), LaggedStart(*[FadeIn(VGroup(d, l), shift=RIGHT * 0.3) for d, l in zip(dashes, lw)], lag_ratio=0.4), rt=0.6)
        at(self, "log every change")
        title = key("Agentic Retrieval Lab", 0, -1.45, size=66)
        rule = Line([-1.4, -2.15, 0], [1.4, -2.15, 0], color=INK, stroke_width=4)
        name = lab("Rithika Sankar Rajeswari · github.com/rithika-sr", 0.35, -2.75, size=40)
        P(self, FadeIn(title, scale=0.8), FadeIn(rule), FadeIn(name), slide_in(me(-5.85, -3.4, h=1.3), LEFT, 0.8), rt=0.55)
        done(self)
