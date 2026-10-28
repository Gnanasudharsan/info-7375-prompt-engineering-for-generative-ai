"""
scenes.py — rithika-reallocation-mode-video ("A Mode for the Reallocation Engine"), show-tell.

One drawn Manim scene per beat, paced by the measured Bella narration in beat_sheet.json and the
whisper word times in word_times.json (at() / done()). The drawing kit and pacing helpers are
copied verbatim from Rithika's final-project film (fall-2026/rithika-s/final-project-film/scenes.py,
itself the show-tell iso_kit.py), pasted here because Gate A copies only scenes.py. The film's
cast helpers (books, carts, robot, people) are left out; this film's cast is below (FILM CAST).
On screen: no screenshots, no personal information, no home-folder paths.
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



# ═════════════════════════════ FILM CAST (Reallocation Engine mode) ═════════════════════════════
# One cast for the whole film (show-tell law 4):
#   SASHA's identity card (fictional persona) · the GATE row (G1 → G2 → Level → G3 → G4) and its
#   three EXITS (HELD / CLOSED / OVER-LEVEL) · TERMINAL cards that carry real output verbatim
#   (dark card, cream type) · STAMPS for decisions (terracotta edge) · the agreement BARS.
# Real text only. Glyphs missing from EB Garamond (✓ ✗ ✅) are drawn with check()/xmark().
CREAM = "#F2F0E9"


def ink_rule(x0, x1, y, color=TERRA, w=6):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w)


def left_text(s, x0, y, size=SEC, color=INK, bold=False):
    t = T(s, size, color, bold=bold)
    return t.move_to([x0 + t.width / 2, y, 0])


def term_card(x0, y0, w, h):
    """A terminal card: dark rounded panel; real output goes on it in cream."""
    return RoundedRectangle(width=w, height=h, corner_radius=0.18, fill_color=DARK_TOP, fill_opacity=1,
                            stroke_color=DARK_R, stroke_width=3).move_to([x0 + w / 2, y0 - h / 2, 0])


def tline(s, x0, y, size=34, bold=False):
    return left_text(s, x0, y, size, CREAM, bold)


def active_badge(x, y, s=0.42, word="active", size=40, on_dark=False):
    """The checker's '✅ active', drawn: a terracotta square with a white check, then the word."""
    sq = RoundedRectangle(width=2 * s, height=2 * s, corner_radius=0.08, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    ck = check(x, y + 0.02, s=s * 0.55, color=PAGE_TOP, w=7)
    t = T(word, size, CREAM if on_dark else INK, bold=True)
    t.move_to([x + s + 0.22 + t.width / 2, y, 0])
    return VGroup(sq, ck, t)


def warn_badge(x, y, s=0.42, word="uncertain", size=40):
    tri = Triangle(fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).scale(s).move_to([x, y, 0])
    bang = T("!", int(size * 0.9), INK, bold=True).move_to([x, y - 0.06, 0])
    t = T(word, size, INK, bold=True)
    t.move_to([x + s + 0.25 + t.width / 2, y, 0])
    return VGroup(tri, bang, t)


def eye(x, y, s=0.42, off=True):
    """An open eye (sees) or, with off=True, a closed eye: lid arc and lashes, one shape (no slash crossing it)."""
    if off:
        lid = Arc(radius=1.1 * s, start_angle=PI + 0.45, angle=PI - 0.9, stroke_color=INK, stroke_width=6).move_to([x, y + 0.12 * s, 0])
        lashes = VGroup(*[Line(lid.point_from_proportion(t), lid.point_from_proportion(t) + np.array([dx, -0.32 * s, 0]),
                               color=INK, stroke_width=5) for t, dx in ((0.2, -0.12 * s), (0.5, 0.0), (0.8, 0.12 * s))])
        return VGroup(lid, lashes)
    lid = Ellipse(width=2.2 * s, height=1.2 * s, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    pupil = Circle(radius=0.32 * s, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    return VGroup(lid, pupil)


def gate_post(x, y, w=1.15, h=1.5):
    """One gate: two kraft posts and a beam. Returns (gate, beam) so the beam can light up."""
    pl = Rectangle(width=0.2, height=h, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x - w / 2, y, 0])
    pr = pl.copy().move_to([x + w / 2, y, 0])
    beam = Rectangle(width=w + 0.4, height=0.24, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y + h / 2 + 0.05, 0])
    return VGroup(pl, pr, beam), beam


def stamp(s, x, y, size=44, color=KRAFT_DEEP, angle=0.0):
    t = T(s, size, INK, bold=True)
    r = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.36, corner_radius=0.12, fill_color=PAGE_TOP, fill_opacity=1,
                         stroke_color=color, stroke_width=7)
    return VGroup(r, t).move_to([x, y, 0]).rotate(angle)


def clock(x, y, r=1.25):
    face = Circle(radius=r, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    ticks = VGroup(*[Line([x + 0.86 * r * np.cos(a), y + 0.86 * r * np.sin(a), 0], [x + 0.98 * r * np.cos(a), y + 0.98 * r * np.sin(a), 0],
                          color=INK, stroke_width=4) for a in np.linspace(0, TAU, 12, endpoint=False)])
    hand = Line([x, y, 0], [x, y + 0.75 * r, 0], color=TERRA, stroke_width=9)
    hub = Dot([x, y, 0], radius=0.08, color=INK)
    return VGroup(face, ticks, hand, hub), hand


# ═════════════════════════════ BEATS ═════════════════════════════
SAFE_X, SAFE_Y = 6.28, 3.38          # Gate B layout audit safe area is ±6.3 x / ±3.4 y; keep a hair inside it


def row(*mobs, buff=0.28):
    """Lay a row out from measured widths (never hand-placed x)."""
    return VGroup(*mobs).arrange(RIGHT, buff=buff, center=False, aligned_edge=ORIGIN)


import manim as _manim_mod
_REAL_MANIM = hasattr(_manim_mod, "__version__")   # Gate A runs construct() on a geometry stub with estimated text widths


def lay(ok, msg):
    """A layout assertion that only applies under real Manim (the stub's widths are estimates)."""
    if _REAL_MANIM and not ok:
        raise AssertionError(msg)


def safe(m, name=""):
    """Fail the render if anything leaves the title-safe area (cheap, before Gates B/T/V). Real Manim only."""
    if not _REAL_MANIM:
        return m
    if m.get_left()[0] < -SAFE_X or m.get_right()[0] > SAFE_X or m.get_bottom()[1] < -SAFE_Y or m.get_top()[1] > SAFE_Y:
        raise ValueError(f"{name or m} leaves title-safe: x {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f}, "
                         f"y {m.get_bottom()[1]:.2f}..{m.get_top()[1]:.2f}")
    return m


def boxed(m, pad_x=0.35, pad_y=0.22, stroke=BAR1, fill=PAGE_TOP, w=None):
    r = RoundedRectangle(width=(w or m.width + 2 * pad_x), height=m.height + 2 * pad_y, corner_radius=0.14,
                         fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=3).move_to(m.get_center())
    return VGroup(r, m)


class B01_Persona(Scene):
    def construct(self):
        title = safe(key("A mode for the Reallocation Engine", 0, 2.98, size=50), "title")
        self.add(title)
        cx, cy, cw, ch = -2.45, -0.38, 7.6, 4.0
        body = RoundedRectangle(width=cw, height=ch, corner_radius=0.22, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=KRAFT_DEEP, stroke_width=4).move_to([cx, cy, 0])
        band = Rectangle(width=cw - 0.08, height=0.95, fill_color=BOX_TOP, fill_opacity=1, stroke_width=0).move_to([cx, cy + ch / 2 - 0.52, 0])
        name = left_text("SASHA JONES", cx - cw / 2 + 0.4, cy + ch / 2 - 0.52, size=KEY, bold=True)
        head = Circle(radius=0.55, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([cx - 2.6, cy + 0.45, 0])
        torso_fill = Sector(radius=0.95, angle=PI, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([cx - 2.6, cy - 0.75, 0])
        idcard = safe(VGroup(body, band, name, torso_fill, head), "idcard")
        persona = stamp("fictional persona", 0, 0, size=36)
        persona.move_to([cx + cw / 2 - persona.width / 2, cy + ch / 2 + persona.height / 2 + 0.1, 0])   # above the card's top-right corner
        safe(persona, "persona")
        lay(persona.get_bottom()[1] > body.get_top()[1] and persona.get_top()[1] < title.get_bottom()[1], "persona stamp collides")
        fx = cx - 1.45
        fields = [("F-1 student", "f1"), ("MS Data Science", "data science"), ("grad Dec 2026", "december"),
                  ("OPT Jan 2027", "january"), ("SOC 15-2051", "scientist roles")]
        rows = [safe(VGroup(Dot([fx, cy + 0.72 - i * 0.58, 0], radius=0.07, color=KRAFT_DEEP),
                            left_text(s, fx + 0.25, cy + 0.72 - i * 0.58, size=SEC, bold=(i == 4))), s) for i, (s, _) in enumerate(fields)]
        for r in rows:
            lay(r.get_bottom()[1] > body.get_bottom()[1] + 0.12 and r.get_top()[1] < band.get_bottom()[1] - 0.05, "field leaves the card")
        at(self, "sasha jones")
        P(self, slide_in(idcard, LEFT, 1.0), rt=0.6)
        at(self, "fictional")
        pop(self, persona)
        for (s, cue), r in zip(fields, rows):
            at(self, cue)
            pop(self, r, rt=0.4)
        need = safe(chip("needs H-1B sponsorship", cx, -2.95, size=34), "need")
        lay(need.get_top()[1] < body.get_bottom()[1] - 0.08, "need chip touches the card")
        at(self, "h1b")
        pop(self, need)
        sites = VGroup()
        for i, s in enumerate(["Built In", "LinkedIn", "Indeed"]):
            sites.add(card(s, 4.4, 1.25 - i * 1.05, size=40, w=2.9, bold=True).rotate((i - 1) * -0.06))
        cap = lab("aggregator sites", 4.4, -2.05, size=SEC, bold=True)
        safe(VGroup(sites, cap), "sites")
        at(self, "aggregator")
        P(self, LaggedStart(*[FadeIn(c, shift=LEFT * 0.6) for c in sites], lag_ratio=0.25), FadeIn(cap), rt=0.7)
        done(self)


class B02_CantSee(Scene):
    def construct(self):
        head = safe(key("What Sasha can't see", 0, 2.95, size=54), "head")
        self.add(head)
        items = [("Is the job still open?", "look open"), ("Does it sponsor this role?", "sponsors this"), ("Is it her level?", "her level")]
        cards = []
        for i, (s, _) in enumerate(items):
            y = 1.5 - i * 1.5
            box = RoundedRectangle(width=8.1, height=1.15, corner_radius=0.16, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([-2.15, y, 0])
            cards.append(safe(VGroup(box, eye(-5.5, y, s=0.36), left_text(s, -4.65, y, size=44, bold=True)), s))
        for (s, cue), c in zip(items, cards):
            at(self, cue)
            P(self, FadeIn(c, shift=RIGHT * 0.5), rt=0.45)
        face, hand = clock(4.25, 0.45, r=1.3)
        days = key("90 days", 4.25, -1.45, size=56)
        sub = VGroup(lab("unemployment limit", 4.25, -2.15, size=36), lab("once OPT starts", 4.25, -2.7, size=36))
        safe(VGroup(face, days, sub), "clock")
        at(self, "dead application")
        P(self, FadeIn(face, scale=0.8), rt=0.5)
        at(self, "once opt")
        P(self, Rotate(hand, angle=-TAU * 0.92, about_point=face[0].get_center()), rt=2.0, rate_func=linear)
        at(self, "90 days")
        pop(self, days, sub)
        done(self)


class B03_Gates(Scene):
    def construct(self):
        xs = [-4.8, -2.4, 0.0, 2.4, 4.8]
        names = [("G1", "sponsorship"), ("G2", "liveness"), ("Level", "entry title"), ("G3", "timeline"), ("G4", "human")]
        cues = ["g1", "g2", "level check", "g3", "g4"]
        y = 1.0
        gates, beams, labels = [], [], []
        for x, (a, b) in zip(xs, names):
            g, beam = gate_post(x, y)
            gates.append(g); beams.append(beam)
            labels.append(VGroup(key(a, x, y - 1.2, size=48), lab(b, x, y - 1.8, size=36)))
        row_ = VGroup(*gates)
        head = key("Gates, in order", 0, 2.98, size=50)
        safe(VGroup(row_, *labels, head), "gates")
        self.add(head, row_)
        role = chip("role", xs[0], y - 0.05, size=32)
        role.set_opacity(0)
        agg = tag("an aggregator's \u201cactive\u201d alone is not enough", -2.4, -1.4)
        for i, cue in enumerate(cues):
            at(self, cue)
            P(self, beams[i].animate.set_fill(DARK_TOP), FadeIn(labels[i], scale=0.8), role.animate.move_to([xs[i], y - 0.05, 0]).set_opacity(1), rt=0.5)
            if i == 1:
                at(self, "aggregator saying")
                pop(self, agg, rt=0.4)
        votes = stamp("gates, not votes", 0, 2.55, size=46)
        at(self, "gates not votes")
        P(self, FadeOut(agg), FadeOut(head), rt=0.3)
        pop(self, votes)
        exits = [("HELD", -4.2, "held"), ("CLOSED", 0.0, "closed"), ("OVER-LEVEL", 4.2, "over level")]
        at(self, "fails")
        P(self, role.animate.move_to([0.0, -2.4, 0]).set_opacity(0.0), rt=0.5)
        for s, x, cue in exits:
            arrow = Arrow([x, -1.85, 0], [x, -2.4, 0], buff=0, color=INK, stroke_width=6, max_tip_length_to_length_ratio=0.35)
            box = safe(stamp(s, x, -2.92, size=42, color=INK), s)
            at(self, cue)
            pop(self, arrow, box, rt=0.35)
        done(self)


class B04_Removed(Scene):
    def construct(self):
        top = safe(chip("13 real postings", 0, 2.88, size=42), "top")
        at(self, "13")
        pop(self, top)
        # left: the Built In page (its real banner text, seen by hand in the G4 review)
        px0, py0, pw, ph = -6.2, 2.25, 6.45, 3.7
        page = RoundedRectangle(width=pw, height=ph, corner_radius=0.16, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([px0 + pw / 2, py0 - ph / 2, 0])
        bar = Rectangle(width=pw - 0.06, height=0.66, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([px0 + pw / 2, py0 - 0.37, 0])
        host = left_text("builtin.com", px0 + 0.3, py0 - 0.37, size=34, bold=True)
        job = left_text("Instacart · Data Scientist", px0 + 0.3, py0 - 1.05, size=34)
        banner = VGroup(*[left_text(s, px0 + 0.35, py0 - 1.8 - i * 0.52, size=32) for i, s in enumerate(
            ["Sorry, this job was removed at", "02:28 p.m. (UTC) on Wednesday,", "Jun 11, 2025."])])
        hl = SurroundingRectangle(banner, color=KRAFT_DEEP, stroke_width=7, buff=0.12)
        lay(hl.get_right()[0] < page.get_right()[0] - 0.05, "banner highlight leaves the page card")
        src_l = tag("page text, opened by hand (G4 review)", px0 + pw / 2, py0 - ph - 0.35)
        safe(VGroup(page, banner, hl, src_l), "page")
        at(self, "built in page")
        P(self, FadeIn(VGroup(page, bar, host, job), shift=RIGHT * 0.6), rt=0.5)
        at(self, "removed")
        P(self, FadeIn(banner), Create(hl), FadeIn(src_l), rt=0.6)
        # right: the repo checker's real output line (Run 1 log, raw stdout)
        tx0, tw, th = 0.5, 5.7, 2.9
        term = term_card(tx0, 2.25, tw, th)
        cmd = tline("$ npm run ats:liveness", tx0 + 0.3, 1.75, size=34)
        badge = active_badge(tx0 + 0.65, 1.0, s=0.32, size=40, on_dark=True)
        url = VGroup(tline("https://builtin.com/job/", tx0 + 0.3, 0.25, size=32), tline("data-scientist/3375738", tx0 + 0.3, -0.25, size=32))
        src_r = tag("repo checker output, Run 1 log", tx0 + tw / 2, -1.0)
        safe(VGroup(term, cmd, badge, url, src_r), "term")
        at(self, "checker")
        P(self, FadeIn(VGroup(term, cmd), shift=LEFT * 0.6), rt=0.45)
        at(self, "active")
        pop(self, badge, url, src_r)
        v1 = row(T("v0.1:", 46, INK, bold=True), T("Apply", 46, INK), xmark(0, 0, s=0.22, w=9), buff=0.3)
        arrow = Arrow(ORIGIN, RIGHT * 1.1, buff=0, color=INK, stroke_width=6)
        v2 = row(T("this mode:", 46, INK, bold=True), stamp("HELD", 0, 0, size=42), check(0, 0, s=0.24, color=INK, w=9), buff=0.3)
        strip = row(v1, arrow, v2, buff=0.45).move_to([0, -2.85, 0])
        safe(strip, "strip")
        at(self, "first version")
        pop(self, v1)
        at(self, "held it")
        P(self, GrowArrow(arrow), FadeIn(v2, scale=0.8), rt=0.5)
        done(self)


class B05_Bugs(Scene):
    def construct(self):
        top = safe(chip("G4 · human review", 0, 0, size=40).move_to([-6.2, 2.92, 0], aligned_edge=LEFT), "top")
        at(self, "g4 human")
        pop(self, top)
        # the real Airbnb redirect chain (curl -sIL, transcript D7)
        hops = [("", "boards.greenhouse.io/airbnb/jobs/6768605"),
                ("301 →", "job-boards.greenhouse.io/airbnb/jobs/6768605"),
                ("302 →", "/airbnb?error=true"),
                ("302 →", "careers.airbnb.com/positions/"),
                ("200", "the general job list")]
        rows = []
        for i, (code, url) in enumerate(hops):
            yy = 1.95 - i * 0.66
            c = T(code, 34, INK, bold=True)
            c.move_to([-6.2 + c.width / 2, yy, 0])
            u = T(url, 32, INK, bold=(i == 0))
            u.move_to([-4.65 + u.width / 2, yy, 0])
            lay(c.get_right()[0] < u.get_left()[0] - 0.12 or not code, f"hop {i}: code touches url")
            rows.append(VGroup(c, u))
        err = SurroundingRectangle(rows[2][1], color=KRAFT_DEEP, stroke_width=7, buff=0.1)
        src = tag("Airbnb link · curl -sIL redirect chain", -2.9, -1.2)
        chain = safe(VGroup(*rows, err, src), "chain")
        verdict = row(T("checker:", 38, INK, bold=True), active_badge(0, 0, s=0.3, size=38), T("· scored Apply", 38, INK), buff=0.25)
        verdict.move_to([6.2 - verdict.width / 2, 2.92, 0])
        safe(verdict, "verdict")
        lay(top.get_right()[0] < verdict.get_left()[0] - 0.3, "verdict runs into the G4 chip")
        lay(rows[0].get_top()[1] < min(top.get_bottom()[1], verdict.get_bottom()[1]) - 0.1, "chain runs into the top row")
        at(self, "airbnb link")
        pop(self, rows[0])
        at(self, "scored")
        pop(self, verdict)
        at(self, "redirected")
        P(self, FadeIn(rows[1], shift=DOWN * 0.2), rt=0.4)
        at(self, "error page")
        P(self, FadeIn(rows[2], shift=DOWN * 0.2), Create(err), rt=0.45)
        at(self, "general job list")
        P(self, FadeIn(rows[3], shift=DOWN * 0.2), FadeIn(rows[4], shift=DOWN * 0.2), FadeIn(src), rt=0.45)
        # Nextdoor: the checker missed an Apply button a person could see
        nd1 = row(T("Nextdoor:", 42, INK, bold=True), eye(0, 0, s=0.34, off=False), T("Apply button visible", 42, INK), buff=0.3).move_to([0, -2.15, 0])
        arr = Arrow(ORIGIN, RIGHT * 1.0, buff=0, color=INK, stroke_width=6)
        nd2 = row(arr, T("checker:", 42, INK, bold=True), warn_badge(0, 0, s=0.34, size=42), buff=0.3).move_to([0, -3.0, 0])
        safe(VGroup(nd1, nd2), "nextdoor")
        at(self, "next door")
        P(self, FadeIn(nd1, shift=UP * 0.3), rt=0.45)
        at(self, "missed")
        P(self, GrowArrow(arr), FadeIn(nd2, scale=0.8), rt=0.45)
        done(self)


class B06_Fixes(Scene):
    def construct(self):
        head = safe(chip("Run 2 fixes", 0, 2.92, size=42), "head")
        at(self, "run two")
        pop(self, head)
        fixes = [("job record API", "actual job record"), ("redirect chain", "redirect"), ("trusted-site allowlist", "only trusts")]
        chips = [card(s, 0, 0, size=36, bold=True) for s, _ in fixes]
        safe(row(*chips, buff=0.35).move_to([0, 2.15, 0]), "fix chips")
        for c, (s, cue) in zip(chips, fixes):
            at(self, cue)
            P(self, FadeIn(c, shift=DOWN * 0.4), rt=0.4)
        def flip(name, old, new_stamp, y):
            a = T(name, 46, INK, bold=True); a.move_to([-5.9 + a.width / 2, y, 0])
            b = T(old, 46, INK); b.move_to([-2.2 + b.width / 2, y, 0])
            arr = Arrow([0.4, y, 0], [1.9, y, 0], buff=0, color=INK, stroke_width=6)
            n = new_stamp.move_to([2.4 + new_stamp.width / 2, y, 0])
            return VGroup(a, b), arr, n
        a_row, a_arr, a_new = flip("Airbnb", "Apply", stamp("CLOSED", 0, 0, size=44), 0.55)
        n_row, n_arr, n_new = flip("Nextdoor", "uncertain", stamp("live", 0, 0, size=44, color=INK), -0.75)
        safe(VGroup(a_row, a_arr, a_new, n_row, n_arr, n_new), "flips")
        at(self, "airbnb")
        pop(self, a_row)
        at(self, "closed")
        P(self, GrowArrow(a_arr), FadeIn(a_new, scale=0.8), rt=0.45)
        at(self, "next door")
        pop(self, n_row)
        at(self, "live")
        P(self, GrowArrow(n_arr), FadeIn(n_new, scale=0.8), rt=0.45)
        phase1 = VGroup(a_row, a_new, a_arr, n_row, n_new, n_arr)
        at(self, "new problem")
        P(self, FadeOut(phase1, shift=LEFT * 0.6), *[dim(c) for c in chips], rt=0.45)
        seniors = [("Senior Data Scientist I", "Instacart · Meals", -3.45), ("Senior Data Scientist", "Nextdoor · Search", 3.45)]
        cards_, applies, overs = [], [], []
        for t1, t2, x in seniors:
            box = RoundedRectangle(width=5.2, height=1.7, corner_radius=0.16, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([x, 0.3, 0])
            cards_.append(VGroup(box, lab(t1, x, 0.6, size=40, bold=True), lab(t2, x, -0.05, size=36)))
            applies.append(stamp("Apply", x, -1.3, size=44))
            overs.append(stamp("OVER-LEVEL", x, -1.3, size=44))
        safe(VGroup(*cards_, *overs), "seniors")
        at(self, "two senior")
        P(self, *[FadeIn(c, shift=UP * 0.3) for c in cards_], rt=0.45)
        at(self, "scored")
        P(self, *[FadeIn(a, scale=0.8) for a in applies], rt=0.4)
        g, beam = gate_post(0.0, 0.35, w=0.9, h=1.4)
        glab = lab("Level", 0.0, -0.75, size=40, bold=True)
        at(self, "run three")
        P(self, FadeIn(VGroup(g, glab), shift=DOWN * 0.3), rt=0.4)
        at(self, "level gate")
        P(self, beam.animate.set_fill(DARK_TOP), *[ReplacementTransform(a, o) for a, o in zip(applies, overs)], rt=0.5)
        # agreement with my G4 review on 5 postings: 3/5 → 2/5 → 4/5 (worked-run/EVALUATION.md)
        phase2 = VGroup(*cards_, *overs, g, glab, *chips, head)
        at(self, "against")
        P(self, FadeOut(phase2), rt=0.45)
        ctitle = key("Agreement with my review of 5 postings", 0, 2.98, size=48)
        base_y, unit = -2.25, 0.9
        floor = Line([-4.6, base_y, 0], [4.6, base_y, 0], color=INK, stroke_width=5)
        vals, xs = [3, 2, 4], [-2.8, 0.0, 2.8]
        bars, nums, caps = [], [], []
        for v, x, run in zip(vals, xs, ["Run 1", "Run 2", "Run 3"]):
            bars.append(Rectangle(width=1.6, height=v * unit, fill_color=TERRA if run == "Run 3" else BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, base_y + v * unit / 2, 0]))
            nums.append(key(f"{v}/5", x, base_y + v * unit + 0.45, size=52))
            caps.append(lab(run, x, base_y - 0.45, size=40, bold=True))
        src = tag("source: worked-run/EVALUATION.md", 0, -3.15)
        safe(VGroup(ctitle, floor, *bars, *nums, *caps, src), "chart")
        P(self, FadeIn(ctitle), Create(floor), *[FadeIn(c) for c in caps], FadeIn(src), rt=0.45)
        for k, cue in enumerate(["agreement", "then two", "then four"]):
            at(self, cue)
            P(self, GrowFromEdge(bars[k], DOWN), FadeIn(nums[k], scale=0.7), rt=0.45)
        done(self)


class B07_Caveats(Scene):
    def construct(self):
        head = safe(key("Two honest caveats", 0, 2.98, size=50), "head")
        self.add(head)
        same = safe(lab("rules checked on the same 5 postings I reviewed", 0, 0.8, size=40), "same")
        at(self, "same five")
        pop(self, same)
        big = safe(stamp("Not a held-out test", 0, 1.95, size=60), "big")
        at(self, "held out")
        P(self, FadeIn(big, scale=1.15), rt=0.45)
        sub = lab("what it still can't see", 0, -0.35, size=SEC, bold=True)
        at(self, "still cant")
        pop(self, sub)
        limits = [("title ≠ description", "Figma", -4.15, "figmas"),
                  ("company-wide", "sponsorship data", 0.0, "company wide"),
                  ("Greenhouse only", "record check so far", 4.15, "only greenhouse")]
        for t1, t2, x, cue in limits:
            box = RoundedRectangle(width=3.95, height=1.8, corner_radius=0.16, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([x, -2.0, 0])
            a, b = lab(t1, x, -1.68, size=36, bold=True), lab(t2, x, -2.35, size=32)
            lay(a.width < 3.75 and b.width < 3.75, f"{t1} overflows its card")
            g = safe(VGroup(box, a, b), t1)
            at(self, cue)
            P(self, FadeIn(g, shift=UP * 0.3), rt=0.45)
        done(self)


class BOUT_Status(Scene):
    def construct(self):
        title = safe(VGroup(key("A Mode for the Reallocation Engine", 0, -2.55, size=48), tag("INFO 7375", 0, -3.12)), "title")
        self.add(title)
        texts = [T("Status:", 36, INK, bold=True), stamp("DRAFT", 0, 0, size=34), T("·  ran live 3×", 36, INK), T("·  typed TODOs open", 36, INK)]
        line = row(*texts, buff=0.26).move_to([0, 2.2, 0])
        board = RoundedRectangle(width=line.width + 0.7, height=1.35, corner_radius=0.2, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=KRAFT_DEEP, stroke_width=4).move_to(line.get_center())
        safe(board, "board")
        at(self, "draft")
        P(self, FadeIn(board), FadeIn(texts[0], scale=0.7), FadeIn(texts[1], scale=0.7), rt=0.4)   # the board never shows empty
        at(self, "ran live")
        pop(self, texts[2], rt=0.4)
        at(self, "still open")
        pop(self, texts[3], rt=0.4)
        nxt = key("Next: held-out test", 0, 0.65, size=56)
        at(self, "next step")
        pop(self, nxt)
        s1 = card("1  decide on new postings first", 0, 0, size=34, bold=True)
        arr = Arrow(ORIGIN, RIGHT * 0.8, buff=0, color=INK, stroke_width=6)
        s2 = card("2  then run the mode", 0, 0, size=34, bold=True)
        safe(row(s1, arr, s2, buff=0.3).move_to([0, -0.85, 0]), "steps")
        at(self, "decide")
        P(self, FadeIn(s1, shift=UP * 0.3), rt=0.4)
        at(self, "then run")
        P(self, GrowArrow(arr), FadeIn(s2, shift=UP * 0.3), rt=0.4)
        done(self)
