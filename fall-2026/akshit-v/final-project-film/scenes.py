"""
scenes.py — INFO 7375 Final Project Pitch Film, "SponsorScout" (Akshit Verma).

Show-tell style: one drawing per beat, short labels, the voice explains. Revision of 2026-10-14
(Akshit's notes): depth-correct isometric objects (a crate passes BETWEEN a gate's back and front
posts; trays hold crates between their back and front walls), word-timed reveals (mp3/words.json,
from align.py), an entrance build and an end-of-beat fade on every scene for smooth transitions,
a moving conveyor, and nothing drawn in the caption band (y < -2.5).

The ISO KIT block below is pasted (not imported) from brutalist.art upstream
skills/make/show-tell/templates/iso_kit.py (4115560), as that skill says, because Gate A copies
only scenes.py. Removed from the paste: the writing kit and `professor_bear` (the instructor's
portrait library; this film draws no people).

HONESTY: every body scene carries a corner tag — "constructed drawing" plus "ran <date>" or
"proposed". The only numbers drawn are real ones from Assignment 1's committed run outputs
(FACTCHECK.md).
"""
from manim import *
import numpy as np
import json as _json, os as _os, re as _re

# ── font: EB Garamond ships with the toolkit (runtime/fonts/EB_Garamond, SIL OFL) but is not installed
#    system-wide on this machine; register the file so Pango can find it.
try:
    import manimpango as _mp
    for _base in (_os.environ.get("ART_HOME"), r"C:\Users\Akshit Verma\PromptEngr\brutalist.art"):
        _f = _base and _os.path.join(_base, "runtime", "fonts", "EB_Garamond", "static", "EBGaramond-Regular.ttf")
        if _f and _os.path.isfile(_f):
            _mp.register_font(_f)
            break
except Exception:
    pass

# ═════════════════════════════ ISO KIT (show-tell, pasted) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"
DEEP_KRAFT = "#9C8462"
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=36, color=INK):
    return Text(s, font=SERIF, color=color, font_size=size)


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
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, sw=sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, sw=sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, sw=sw))

    def open_box(self, x0, y0, z0, w, d, h):
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


def ease_in(t):
    return t * t


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))
# ═════════════════════════════ end ISO KIT ═════════════════════════════


# ═════════════════════════════ pacing: the narration's own word clock ═════════════════════════════
_HERE = _os.path.dirname(_os.path.abspath(__file__))
try:
    _SHEET = _json.load(open(_os.path.join(_HERE, "beat_sheet.json"), encoding="utf-8"))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
    _NARR = {b["beat_id"]: b["narration_text"] for b in _SHEET["beats"]}
    _TAG = {b["beat_id"]: b.get("honesty_tag", "") for b in _SHEET["beats"]}
except Exception:
    _TARGET, _NARR, _TAG = {}, {}, {}
try:   # word-level timing written by align.py: {"fps": .., "beats": {BID: [{text, startFrame, endFrame}]}}
    _W = _json.load(open(_os.path.join(_HERE, "mp3", "words.json"), encoding="utf-8"))
    _WORDS = {k: [(_re.sub(r"[^a-z0-9]", "", w["text"].lower()), w["startFrame"] / _W["fps"]) for w in v]
              for k, v in _W["beats"].items()}
except Exception:
    _WORDS = {}

MID_MARGIN = 0.25   # GATE T and Gate V sample the clip midpoint: keep motion off it


def _bid(self):
    return type(self).__name__.split("_")[0]


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def at(self, phrase, lead=0.15):
    """Wait until `phrase` is spoken: its first word's start in words.json (exact), else its share of the text."""
    bid = _bid(self)
    toks = [t for t in (_re.sub(r"[^a-z0-9]", "", x.lower()) for x in phrase.split()) if t]
    words = _WORDS.get(bid)
    t0 = None
    if words and toks:
        texts = [w for w, _ in words]
        for i in range(len(texts) - len(toks) + 1):
            if texts[i:i + len(toks)] == toks:
                t0 = words[i][1]
                break
    if t0 is None:
        n, target = _NARR.get(bid, ""), _TARGET.get(bid, 0)
        if not n or not target or phrase not in n:
            return
        t0 = target * n.index(phrase) / len(n)
    gap = t0 - lead - _elapsed(self)
    if gap > 0.04:
        self.wait(gap)


def gplay(self, *anims, run_time=0.6, **kw):
    """play(), but never across the clip midpoint: wait past it first if the move would straddle it."""
    tgt = _TARGET.get(_bid(self), 0)
    if tgt:
        mid, t = tgt / 2, _elapsed(self)
        if t < mid + MID_MARGIN and t + run_time > mid - MID_MARGIN:
            self.wait(mid + MID_MARGIN - t)
    self.play(*anims, run_time=run_time, **kw)


def enter(self, *mobs, run_time=0.7):
    """The entrance build: everything rises in, staggered."""
    self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.3) for m in mobs], lag_ratio=0.12), run_time=run_time)


def finish(self, fade=0.4):
    """Hold, then fade the whole frame to the stage just before the beat ends: a dip-to-cream transition."""
    target = _TARGET.get(_bid(self), 0)
    if not target:
        self.wait(1.0)
        return
    t = _elapsed(self)
    start = target - fade - 0.12
    if start > t:
        self.wait(start - t)
    mobs = [m for m in self.mobjects]
    if mobs:
        self.play(*[FadeOut(m) for m in mobs], run_time=fade)
    rest = target - _elapsed(self) - 0.04
    if rest > 0.04:
        self.wait(rest)


def honesty_tag(self):
    """The corner tag, top-left inside SAFE, ink, size 32 (type floor). Added with the first frame."""
    s = _TAG.get(_bid(self)) or "constructed drawing"
    t = T(s, 32)
    t.move_to([-6.1 + t.width / 2, 3.25 - t.height / 2, 0])
    self.add(t)
    return t


def label(s, at_xy, size=36):
    t = T(s, size)
    t.move_to(np.array([at_xy[0], at_xy[1], 0], dtype=float))
    return t


def centre(m):
    return np.array(m.get_center(), dtype=float)


def arrow(a, b, dashed=False, color=INK, sw=5):
    a, b = np.array([a[0], a[1], 0], dtype=float), np.array([b[0], b[1], 0], dtype=float)
    if dashed:
        line = DashedLine(a, b, color=color, stroke_width=sw, dash_length=0.16)
    else:
        line = Line(a, b, color=color, stroke_width=sw)
    d = (b - a) / max(np.linalg.norm(b - a), 1e-6)
    n = np.array([-d[1], d[0], 0])
    head = Polygon(b, b - d * 0.26 + n * 0.13, b - d * 0.26 - n * 0.13, fill_color=color, fill_opacity=1, stroke_width=0)
    return VGroup(line, head)


def cross(x, y, s=0.22, color=INK, w=7):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def sheet(x, y, w=1.4, h=1.8, rows=4, fill=PAGE_TOP, line=GHOST):
    """A flat page facing the viewer: white face, ink edge, kraft offset shadow, ghost text rows."""
    sh = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
    pg = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    gap = h / (rows + 1)
    ln = VGroup(*[Line([x - w / 2 + 0.22, y + h / 2 - gap * (i + 1), 0], [x + w / 2 - 0.22 - (0.3 if i == rows - 1 else 0),
                       y + h / 2 - gap * (i + 1), 0], color=line, stroke_width=6) for i in range(rows)])
    g = VGroup(sh, pg, ln)
    g.rows_y = [y + h / 2 - gap * (i + 1) for i in range(rows)]
    return g


def terminal(x, y, w=1.9, h=1.3):
    """A dark terminal card: no glyphs, ghost command lines and a terracotta cursor block."""
    body = RoundedRectangle(width=w, height=h, corner_radius=0.12, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK,
                            stroke_width=4).move_to([x, y, 0])
    bar = Rectangle(width=w - 0.04, height=0.2, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x, y + h / 2 - 0.12, 0])
    l1 = Line([x - w / 2 + 0.25, y + 0.1, 0], [x + 0.3, y + 0.1, 0], color=BAR2, stroke_width=7)
    l2 = Line([x - w / 2 + 0.25, y - 0.22, 0], [x - 0.15, y - 0.22, 0], color=BAR2, stroke_width=7)
    cur = Rectangle(width=0.16, height=0.24, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([x + 0.02, y - 0.22, 0])
    return VGroup(body, bar, l1, l2, cur)


# ── the film's cast, depth-correct ──
def crate(iso, x, y, z=0.0, w=1.2, d=1.2, h=0.9):
    """The film's company: a kraft crate, grey strap, one terracotta seal. z-index 1: between a tray's back (0)
    and front (2), and between a gate's back post (0) and front post (3)."""
    body = iso.box(x, y, z, w, d, h)
    ym = y + d / 2
    strap = iso.quad([(x, ym - 0.12, z + h), (x + w, ym - 0.12, z + h), (x + w, ym + 0.12, z + h), (x, ym + 0.12, z + h)],
                     BAR2, stroke=DEEP_KRAFT, sw=2)
    seal = Dot(iso.p(x + w / 2, ym, z + h), radius=0.08, color=TERRA)
    g = VGroup(body, strap, seal)
    g.set_z_index(1)
    return g


def iso_at(cx, cy, w, d, h, s=1.0):
    """An Iso whose box(0, 0, 0, w, d, h) is centred on screen point (cx, cy)."""
    return Iso(cx - (w - d) / 2 * C30 * s, cy - (w + d) / 2 * 0.5 * s - h / 2 * s, s)


def crate_at(cx, cy, w=1.2, h=0.9, s=1.0):
    return crate(iso_at(cx, cy, w, w, h, s), 0, 0, 0, w, w, h)


def tray_at(cx, cy, w=1.8, h=0.5, s=1.0):
    back, front = iso_at(cx, cy, w, w, h, s).open_box(0, 0, 0, w, w, h)
    return VGroup(back, front)


def dark_block(cx, cy, w=1.5, h=1.0, s=1.0):
    """A dark machine block (scorer / workflow / resolver) with one terracotta lamp."""
    iso = iso_at(cx, cy, w, w, h, s)
    g = iso.box(0, 0, 0, w, w, h, DARK_TOP, DARK_L, DARK_R)
    lamp = Dot(iso.p(w * 0.5, 0, h * 0.55), radius=0.09, color=TERRA)
    return VGroup(g, lamp)


def plinth(iso, x, y, w, d, t=0.28):
    """A dark slab under a pale object (Gate V contrast: a lone kraft object read 0.28 < 0.30)."""
    p = iso.box(x - 0.25, y - 0.25, -t, w + 0.5, d + 0.5, t, DARK_TOP, DARK_L, DARK_R)
    p.set_z_index(-1)
    return p


def gate(iso, x, y, h=1.8, span=1.75, pw=0.22):
    """A check gate across the belt, in depth order: back post z0 < (crate z1) < front post + bar z3 < lamp z4."""
    back = iso.box(x, y + span, 0, pw, pw, h, DARK_TOP, DARK_L, DARK_R); back.set_z_index(0)
    front = iso.box(x, y, 0, pw, pw, h, DARK_TOP, DARK_L, DARK_R); front.set_z_index(3)
    bar = iso.box(x, y, h, pw, span + pw, 0.2, DARK_TOP, DARK_L, DARK_R); bar.set_z_index(3)
    lamp = Circle(radius=0.15, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(
        iso.p(x + pw / 2, y + span / 2 + pw / 2, h + 0.5))
    lamp.set_z_index(4)
    return VGroup(back, front, bar), lamp


def belt(iso, x0, y0, length, width=1.95):
    """A flat conveyor along +x: within 28 of the stage, deep-kraft edges, ghost centre dashes (which move)."""
    body = iso.quad([(x0, y0, 0), (x0 + length, y0, 0), (x0 + length, y0 + width, 0), (x0, y0 + width, 0)],
                    "#E6E1D5", stroke=DEEP_KRAFT, sw=3)
    body.set_z_index(-2)
    dashes = VGroup(*[Line(iso.p(x0 + i, y0 + width / 2, 0), iso.p(x0 + i + 0.5, y0 + width / 2, 0), color=GHOST, stroke_width=5)
                      for i in np.arange(0.3, length - 1.4, 1.0)])
    dashes.set_z_index(-1)
    return body, dashes


def ride(self, iso, crate_m, dashes, dx, run_time=0.8):
    """The crate rides the belt by dx while the belt's dashes run with it (then reset by one period, unseen)."""
    period = iso.v(1.0, 0, 0)
    gplay(self, crate_m.animate.shift(iso.v(dx, 0, 0)), dashes.animate.shift(period), run_time=run_time, rate_func=smooth)
    dashes.shift(-period)


def pulse(self, lamp, color=TERRA):
    ring = Circle(radius=0.2, stroke_color=color, stroke_width=5).move_to(centre(lamp))
    ring.set_z_index(5)
    gplay(self, lamp.animate.set_fill(color), Create(ring), run_time=0.3)
    self.play(ring.animate.scale(1.8).set_stroke(opacity=0), run_time=0.3)
    self.remove(ring)


def under(m, s, size=32, buff=0.22):
    """A label just below an object's lowest point (never overlapping it)."""
    return T(s, size).next_to(m, DOWN, buff=buff)


def beside(m, s, size=32, buff=0.25, side=RIGHT):
    return T(s, size).next_to(m, side, buff=buff)


def at_left(t, x):
    """Place a label so its left edge sits at x (keeps long labels inside SAFE)."""
    t.shift(RIGHT * (x - t.get_left()[0]))
    return t


# ═════════════════════════════ BOPEN — the name ═════════════════════════════
class BOPEN_Title(Scene):
    def construct(self):
        title = T("SponsorScout", 112).move_to([1.35, 0.95, 0])
        rule = Line([-1.6, 0.05, 0], [4.3, 0.05, 0], color=TERRA, stroke_width=6)
        # the mark: a crate under a scout's lens
        c = crate_at(-5.0, 0.45, 1.05, 0.8, 1.0)
        lens = VGroup(Circle(radius=0.55, stroke_color=INK, stroke_width=8, fill_color=CARD, fill_opacity=0.35),
                      Line([0.39, -0.39, 0], [0.9, -0.9, 0], color=INK, stroke_width=12)).move_to([-4.35, 1.4, 0])
        glint = Dot([-4.6, 1.65, 0], radius=0.07, color=TERRA)
        self.play(FadeIn(c, shift=UP * 0.3), Write(title), run_time=1.0)
        self.play(FadeIn(lens, shift=DOWN * 0.3 + LEFT * 0.2), Create(rule), run_time=0.5)
        self.add(glint)
        at(self, "A final project pitch")
        by = T("a final project pitch by Akshit Verma", 44).move_to([1.35, -0.6, 0])
        gplay(self, FadeIn(by, shift=UP * 0.2), run_time=0.45)
        at(self, "I'll show")
        ran_dot = Dot([-1.2, -1.75, 0], radius=0.13, color=INK)
        ran_t = beside(ran_dot, "ran", 36, buff=0.2)
        prop_ring = DashedVMobject(Circle(radius=0.14, stroke_color=INK, stroke_width=4), num_dashes=8).move_to([1.6, -1.75, 0])
        prop_t = beside(prop_ring, "proposed", 36, buff=0.2)
        gplay(self, FadeIn(ran_dot), FadeIn(ran_t), run_time=0.3)
        at(self, "and what")
        gplay(self, Create(prop_ring), FadeIn(prop_t), run_time=0.3)
        finish(self)


# ═════════════════════════════ BIDEA — the question, corrected ═════════════════════════════
class BIDEA_Question(Scene):
    def construct(self):
        card = RoundedRectangle(width=12.0, height=3.0, corner_radius=0.25, fill_color=CARD, fill_opacity=1,
                                stroke_width=0).move_to([0, 0.35, 0])
        bar = Rectangle(width=0.16, height=2.2, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([-5.7, 0.35, 0])
        l1 = T("Which companies should I", 60).move_to([0.2, 0.95, 0])
        old = T("apply to?", 60).move_to([0.2, -0.15, 0])
        self.add(card)
        self.play(FadeIn(bar), Write(l1), run_time=0.7)
        self.play(Write(old), run_time=0.45)
        at(self, "It's which ones")
        # greyed + a cross beside it (a line THROUGH the words reads as "label on a line" to Gate B)
        x_mark = cross(old.get_left()[0] - 0.55, old.get_center()[1], 0.2)
        gplay(self, old.animate.set_color(BAR2), Create(x_mark), run_time=0.3)
        at(self, "network with", lead=0.35)
        new = T("network with?", 60).move_to([0.2, -0.15, 0])
        dot = Dot([new.get_right()[0] + 0.3, -0.3, 0], radius=0.09, color=TERRA)
        gplay(self, FadeOut(VGroup(old, x_mark), shift=UP * 0.45), FadeIn(new, shift=DOWN * 0.45), run_time=0.4)
        self.add(dot)
        finish(self, fade=0.3)


# ═════════════════════════════ B00 — what it is ═════════════════════════════
class B00_Company(Scene):
    def construct(self):
        honesty_tag(self)
        ciso = iso_at(-4.75, 0.6, 1.0, 1.0, 0.8, 1.0)   # left edge of the plinth must clear SAFE x=-6.2 (Gate V)
        comp = VGroup(plinth(ciso, 0, 0, 1.0, 1.0), crate(ciso, 0, 0, 0, 1.0, 1.0, 0.8))
        enter(self, comp, under(comp, "a company"))
        at(self, "a Claude Code workflow")
        flow = dark_block(-1.85, 0.6, 1.2, 0.85, 1.0)
        gplay(self, FadeIn(flow, shift=UP * 0.3), FadeIn(under(flow, "SponsorScout")), Create(arrow([-3.6, 0.6], [-2.95, 0.6])),
              run_time=0.6)
        # the four verdicts: one column, a clean fan of arrows, each landing on its spoken word
        cells = [("apply", 1.95, "whether to apply"), ("network", 0.8, "network"),
                 ("check by hand", -0.35, "check by hand"), ("skip", -1.5, "or skip")]
        trays = {}
        for name, y, cue in cells:
            at(self, cue)
            tr = tray_at(1.35, y, 1.0, 0.4, 0.8)
            trays[name] = tr
            gplay(self, FadeIn(tr, shift=LEFT * 0.2), FadeIn(beside(tr, name, 32, buff=0.25)),
                  Create(arrow([-0.7, 0.6], [0.45, y], sw=4)), run_time=0.35)
        at(self, "with the record")
        net = trays["network"]
        pick = crate_at(1.35, 0.98, 0.55, 0.4, 0.8)
        rec = sheet(5.0, 0.8, 0.7, 0.85, rows=2)
        gplay(self, FadeIn(pick, shift=DOWN * 0.4), FadeIn(rec, shift=LEFT * 0.3),
              Create(arrow([3.55, 0.8], [4.55, 0.8], sw=4)), run_time=0.5)
        gplay(self, FadeIn(T("record", 32).next_to(rec, UP, buff=0.15)), run_time=0.3)   # above: below it hit "check by hand"
        finish(self)


# ═════════════════════════════ B01 — the artifact ═════════════════════════════
class B01_Repository(Scene):
    def construct(self):
        honesty_tag(self)
        biso = iso_at(-4.3, 0.55, 1.5, 1.5, 1.0, 1.0)   # plinth clears SAFE x=-6.2 (Gate V)
        back, front = biso.open_box(0, 0, 0, 1.5, 1.5, 1.0)
        repo = VGroup(plinth(biso, 0, 0, 1.5, 1.5), back, front)
        enter(self, repo)
        at(self, "a repository")
        lab_r = under(repo, "repository", 36, buff=0.15)
        gplay(self, FadeIn(lab_r), run_time=0.35)
        at(self, "in Python")
        stack = at_left(under(lab_r, "Python · Claude Code · public data", 28, buff=0.12), -6.05)
        gplay(self, FadeIn(stack), run_time=0.4)
        xs = [-2.15, -0.35, 1.45, 3.25, 5.05]
        y = 0.6
        items = [
            ("recipe", sheet(xs[0], y, 1.1, 1.45, rows=3), "a recipe"),
            ("prototype", terminal(xs[1], y, 1.4, 1.05), "a prototype"),
            ("tests", VGroup(RoundedRectangle(width=1.3, height=0.6, corner_radius=0.3, fill_color=PAGE_TOP, fill_opacity=1,
                                              stroke_color=INK, stroke_width=4).move_to([xs[2], y, 0]),
                             check(xs[2] - 0.05, y, 0.16)), "tests"),
            ("eval log", VGroup(Rectangle(width=1.05, height=1.4, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4),
                                Rectangle(width=0.16, height=1.4, fill_color=DARK_L, fill_opacity=1, stroke_width=0).shift(LEFT * 0.45)
                                ).move_to([xs[3], y, 0]), "an evaluation log"),
            ("report", sheet(xs[4], y, 1.1, 1.45, rows=4), "and a report"),
        ]
        start = biso.p(0.75, 0.75, 1.1)
        for name, m, cue in items:
            at(self, cue)
            lb = T(name, 32).move_to([m.get_center()[0], y - 1.15, 0])
            gplay(self, FadeIn(m, target_position=start, scale=0.6), FadeIn(lb), run_time=0.45)
        at(self, "row by row")
        rep = items[4][1]
        ring = RoundedRectangle(width=1.0, height=0.3, corner_radius=0.1, stroke_color=TERRA, stroke_width=5).move_to(
            [xs[4], rep.rows_y[1], 0])
        gplay(self, Create(ring), run_time=0.35)
        gplay(self, ring.animate.move_to([xs[4], rep.rows_y[2], 0]), run_time=0.35)
        finish(self)


# ═════════════════════════════ B02 — three checks (exists) ═════════════════════════════
class B02_ThreeGates(Scene):
    def construct(self):
        honesty_tag(self)
        iso = Iso(-3.0, -2.35, 0.78)
        GX = (1.6, 4.0, 6.4)
        body, dashes = belt(iso, 0, 0, 8.4)
        gates = [gate(iso, x, -0.05) for x in GX]
        c = crate(iso, 0.15, 0.35, 0.02, 1.15, 1.15, 0.85)
        enter(self, VGroup(body, dashes), *[VGroup(g, l) for g, l in gates], c)
        names = ["sponsored? (H-1B records)", "funded? (Form D)", "open today? (job board)"]
        cues = ["Has it sponsored", "Has it raised", "Is an entry-level"]
        x_now = 0.15
        for gx, (g, lamp), name, cue in zip(GX, gates, names, cues):
            at(self, cue)
            x_to = gx - 0.05 - 0.45
            ride(self, iso, c, dashes, x_to - x_now, run_time=0.75)
            x_now = x_to
            pulse(self, lamp)
            # one line, below-right of this gate's front post: clear of the belt edge and of the next gate
            post = iso.p(gx + 0.1, -0.05, 0)
            lb = at_left(T(name, 32).move_to([0, post[1] - 0.45, 0]), post[0] + 0.25)
            gplay(self, FadeIn(lb, shift=UP * 0.15), run_time=0.3)
        at(self, "today", lead=0.0)
        ride(self, iso, c, dashes, 1.3, run_time=0.6)
        finish(self)


# ═════════════════════════════ B03 — the difference (exists) ═════════════════════════════
class B03_Route(Scene):
    def construct(self):
        honesty_tag(self)
        c = crate_at(-5.0, 0.1, 1.05, 0.8, 1.0)
        lamp = Circle(radius=0.15, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([-5.0, 1.15, 0])
        sponsor = VGroup(c, lamp)
        enter(self, sponsor, under(c, "no open job", 32))
        # top path: the engine's scorer (grey, dashed)
        at(self, "The engine's own scorer")
        eng = dark_block(-1.6, 1.45, 1.0, 0.7, 0.9)
        gplay(self, FadeIn(eng, shift=UP * 0.2), FadeIn(under(eng, "engine scorer", 30, buff=0.12)),
              Create(arrow([-4.25, 0.6], [-2.55, 1.35], dashed=True, color=BAR1)), run_time=0.5)
        at(self, "a zero")
        zero = T("0", 72).move_to([0.25, 1.55, 0])
        gplay(self, FadeIn(zero, scale=1.4), run_time=0.35)
        at(self, "skips it")
        skip = tray_at(3.5, 1.5, 1.3, 0.4, 0.9)
        gplay(self, Create(arrow([0.75, 1.5], [2.4, 1.5], dashed=True, color=BAR1)), FadeIn(skip, shift=LEFT * 0.2),
              FadeIn(beside(skip, "skip", 36)), run_time=0.45)
        # bottom path: SponsorScout (solid)
        at(self, "SponsorScout puts it")
        ss = dark_block(-1.6, -0.75, 1.0, 0.7, 0.9)
        net = tray_at(3.5, -0.75, 1.5, 0.45, 0.95)
        gplay(self, FadeIn(ss, shift=UP * 0.2), FadeIn(under(ss, "SponsorScout", 30, buff=0.12)),
              Create(arrow([-4.25, -0.25], [-2.55, -0.7])), run_time=0.45)
        gplay(self, Create(arrow([-0.65, -0.75], [2.25, -0.75])), FadeIn(net, shift=LEFT * 0.2),
              FadeIn(under(net, "network list", 32, buff=0.12)), run_time=0.45)
        gplay(self, sponsor.animate.scale(0.7).move_to([3.5, -0.3, 0]), run_time=0.8)
        at(self, "keep the sponsors")
        gplay(self, Create(check(5.4, -0.6, 0.24)), run_time=0.35)
        finish(self)


# ═════════════════════════════ B04 — MyVisaJobs ═════════════════════════════
class B04_Compare(Scene):
    def construct(self):
        honesty_tag(self)
        panel = RoundedRectangle(width=4.4, height=3.2, corner_radius=0.18, fill_color=CARD, fill_opacity=1,
                                 stroke_color=INK, stroke_width=4).move_to([-3.5, 0.0, 0])
        head = Rectangle(width=4.36, height=0.4, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-3.5, 1.38, 0])
        enter(self, panel, head, T("MyVisaJobs", 38).next_to(panel, UP, buff=0.2))
        at(self, "It lists sponsors")
        rows = VGroup()
        for i, wv in enumerate((2.4, 1.6, 2.9, 1.1, 2.0)):
            yy = 0.85 - i * 0.5
            rows.add(VGroup(Line([-5.35, yy, 0], [-4.45, yy, 0], color=BAR2, stroke_width=8),
                            Rectangle(width=wv * 0.55, height=0.24, fill_color=BAR1, fill_opacity=1, stroke_width=0)
                            .move_to([-4.15 + wv * 0.275, yy, 0])))
        gplay(self, LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.15), run_time=0.6)
        at(self, "past job counts")
        gplay(self, FadeIn(under(panel, "sponsors · past job counts", 32)), run_time=0.35)
        at(self, "It doesn't take")
        c = crate_at(1.1, 0.25, 1.0, 0.75, 0.95)
        lamp = Circle(radius=0.14, fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([1.1, 1.3, 0])
        net = tray_at(4.6, 0.15, 1.5, 0.45, 0.95)
        gplay(self, FadeIn(VGroup(c, lamp), shift=UP * 0.2), FadeIn(net, shift=UP * 0.2), FadeIn(under(net, "network", 34)),
              run_time=0.45)
        at(self, "with nothing open")
        gplay(self, Create(arrow([2.0, 0.15], [3.45, 0.15], dashed=True, color=BAR1)), run_time=0.4)
        at(self, "tell you")
        gplay(self, Create(cross(2.72, 0.15, 0.22)), FadeIn(T("no network step", 32).move_to([2.3, -1.6, 0])), run_time=0.35)
        finish(self)


# ═════════════════════════════ B05 — the reader's sixty seconds ═════════════════════════════
class B05_Trace(Scene):
    def construct(self):
        honesty_tag(self)
        # the reader: a briefcase (no person drawn)
        handle = Arc(radius=0.32, start_angle=0, angle=PI, stroke_color=INK, stroke_width=9).move_to([-4.6, 1.75, 0])
        body = RoundedRectangle(width=1.6, height=1.05, corner_radius=0.12, fill_color=DARK_TOP, fill_opacity=1,
                                stroke_color=INK, stroke_width=4).move_to([-4.6, 1.05, 0])
        strap = Rectangle(width=1.56, height=0.12, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-4.6, 1.1, 0])
        clasp = Rectangle(width=0.22, height=0.2, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([-4.6, 1.1, 0])
        case = VGroup(handle, body, strap, clasp)
        enter(self, case)
        at(self, "data analyst")
        l1 = under(case, "data analyst", 30, buff=0.2)
        gplay(self, FadeIn(l1), run_time=0.3)
        at(self, "data engineer")
        l2 = under(l1, "data engineer", 30, buff=0.1)
        gplay(self, FadeIn(l2), run_time=0.3)
        at(self, "hiring manager")
        gplay(self, FadeIn(under(l2, "hiring manager", 36, buff=0.18)), run_time=0.35)
        # the clock
        at(self, "In sixty seconds")
        face = Circle(radius=0.5, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([1.6, 2.15, 0])
        hand = Line([1.6, 2.15, 0], [1.6, 2.55, 0], color=TERRA, stroke_width=6)
        knob = Dot([1.6, 2.15, 0], radius=0.07, color=INK)
        gplay(self, FadeIn(face), FadeIn(hand), FadeIn(knob), FadeIn(beside(face, "60 s", 40)), run_time=0.35)
        # the three steps
        at(self, "run one offline command")
        term = terminal(-1.35, 0.0, 1.8, 1.25)
        gplay(self, FadeIn(term, shift=UP * 0.2), FadeIn(under(term, "one command", 32)),
              Rotate(hand, -PI * 2 / 3, about_point=[1.6, 2.15, 0]), run_time=0.45)
        at(self, "open the report")
        rep = sheet(1.6, 0.0, 1.45, 1.8, rows=4)
        gplay(self, Create(arrow([-0.35, 0.0], [0.75, 0.0], sw=4)), FadeIn(rep, shift=UP * 0.2),
              FadeIn(under(rep, "report", 32)), Rotate(hand, -PI * 2 / 3, about_point=[1.6, 2.15, 0]), run_time=0.45)
        at(self, "trace a networking row")
        ring = RoundedRectangle(width=1.3, height=0.3, corner_radius=0.1, stroke_color=TERRA, stroke_width=5).move_to(
            [1.6, rep.rows_y[1], 0])
        src = sheet(4.7, 0.0, 1.35, 1.65, rows=3)
        gplay(self, Create(ring), FadeIn(src, shift=UP * 0.2), run_time=0.4)
        gplay(self, Create(arrow([2.35, rep.rows_y[1]], [3.95, src.rows_y[0]], sw=4)), FadeIn(under(src, "source record", 32)),
              Rotate(hand, -PI * 2 / 3, about_point=[1.6, 2.15, 0]), run_time=0.5)
        finish(self)


# ═════════════════════════════ B06 — run-2, the real counts ═════════════════════════════
class B06_RunTwo(Scene):
    """Real numbers only: course/2026fa/submissions/AkshitVerma-AV/runs/run-2/network-targets.md (2026-10-03)."""
    def construct(self):
        honesty_tag(self)
        XS = (-4.6, -1.55, 1.55, 4.6)
        trays = [tray_at(x, -0.3, 1.55, 0.5, 0.92) for x in XS]
        enter(self, *trays, T("job seeker: fictional", 30).move_to([0, -2.2, 0]))
        at(self, "sixteen job boards")
        gplay(self, FadeIn(T("16 boards fetched", 36).move_to([-3.4, 2.35, 0])), run_time=0.35)
        at(self, "one hundred twenty-three")
        gplay(self, FadeIn(T("123 sponsors sorted", 36).move_to([2.7, 2.35, 0])), run_time=0.35)
        counts = [("apply", "2", "two to apply"), ("network", "1", "one to network"),
                  ("check by hand", "107", "one hundred seven"), ("skip", "13", "thirteen to skip")]
        for tr, x, (w, n, cue) in zip(trays, XS, counts):
            at(self, cue)
            anims = [FadeIn(T(n, 72).move_to([x, 1.15, 0]), shift=UP * 0.25), FadeIn(under(tr, w, 34, buff=0.12))]
            if w == "network":
                anims.append(Create(Ellipse(width=2.6, height=1.75, stroke_color=TERRA, stroke_width=5).move_to([x, -0.3, 0])))
            gplay(self, *anims, run_time=0.35)
        finish(self)


# ═════════════════════════════ B07 — the caught false positive ═════════════════════════════
class B07_Caught(Scene):
    def construct(self):
        honesty_tag(self)
        apply_t = tray_at(-1.0, -0.4, 1.6, 0.5, 0.95)
        c = crate_at(-4.8, 0.3, 1.0, 0.75, 0.95)
        lab_z = under(c, "Zoox · run 1", 32)
        enter(self, apply_t, under(apply_t, "apply", 34, buff=0.12), c, lab_z)
        at(self, "landed in apply")
        gplay(self, FadeOut(lab_z), c.animate.move_to([-1.0, -0.15, 0]), run_time=0.7)
        at(self, "part-time")
        gplay(self, FadeIn(T("part-time contract postings", 32).move_to([-1.0, 1.3, 0])), run_time=0.35)
        at(self, "Claude flagged it")
        scan = Line([-2.3, 0.65, 0], [0.3, 0.65, 0], color=TERRA, stroke_width=7)
        gplay(self, Create(scan), run_time=0.3)
        gplay(self, scan.animate.shift(DOWN * 0.9), run_time=0.35)
        self.remove(scan)
        flag = VGroup(Line([0.6, -0.1, 0], [0.6, 0.8, 0], color=INK, stroke_width=5),
                      Polygon([0.6, 0.8, 0], [1.15, 0.63, 0], [0.6, 0.46, 0], fill_color=TERRA, fill_opacity=1, stroke_width=0))
        gplay(self, FadeIn(flag, shift=UP * 0.2), FadeIn(beside(flag, "flagged", 32, buff=0.15)), run_time=0.3)
        at(self, "I chose the fix")
        out = tray_at(3.6, -0.4, 1.5, 0.45, 0.95)
        gplay(self, FadeIn(out, shift=LEFT * 0.2), FadeIn(under(out, "excluded", 34, buff=0.12)), run_time=0.35)
        gplay(self, c.animate.move_to([3.6, -0.18, 0]), run_time=0.65)
        at(self, "a test pins it")
        pill = RoundedRectangle(width=1.5, height=0.6, corner_radius=0.3, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK,
                                stroke_width=4).move_to([3.4, 1.55, 0])
        gplay(self, FadeIn(pill, shift=DOWN * 0.2), Create(check(3.1, 1.55, 0.16)), FadeIn(beside(pill, "test", 32)), run_time=0.35)
        at(self, "All twenty-five")
        gplay(self, FadeIn(T("25 / 25 tests pass · Oct 12", 30).move_to([3.4, 2.3, 0])), run_time=0.35)
        finish(self)


# ═════════════════════════════ B08 — grounding + gates ═════════════════════════════
class B08_Binder(Scene):
    def construct(self):
        honesty_tag(self)
        panel = RoundedRectangle(width=4.6, height=3.0, corner_radius=0.18, fill_color=CARD, fill_opacity=1, stroke_color=INK,
                                 stroke_width=4).move_to([-3.5, 0.15, 0])
        enter(self, panel)
        at(self, "Source grounding")
        gplay(self, FadeIn(T("every number, labelled", 34).next_to(panel, UP, buff=0.2)), run_time=0.35)
        rows = VGroup()
        for i, (wv, src) in enumerate(((2.2, "rec"), (1.4, "you"), (2.6, "rec"), (1.8, "rec"))):
            yy = 1.05 - i * 0.6
            bar = Rectangle(width=wv, height=0.26, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.45 + wv / 2, yy, 0])
            mark = (Dot([-1.75, yy, 0], radius=0.13, color=INK) if src == "rec" else
                    Circle(radius=0.13, stroke_color=INK, stroke_width=4).move_to([-1.75, yy, 0]))
            rows.add(VGroup(bar, mark))
        gplay(self, LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.15), run_time=0.6)
        at(self, "a record")
        d1 = Dot([-5.4, -1.75, 0], radius=0.13, color=INK)
        gplay(self, FadeIn(d1), FadeIn(beside(d1, "record", 32, buff=0.18)), run_time=0.3)
        at(self, "my own input")
        d2 = Circle(radius=0.13, stroke_color=INK, stroke_width=4).move_to([-3.2, -1.75, 0])
        gplay(self, FadeIn(d2), FadeIn(beside(d2, "my input", 32, buff=0.18)), run_time=0.3)
        at(self, "Verification")
        wall = Rectangle(width=0.3, height=3.0, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([2.5, 0.15, 0])
        scorer = dark_block(4.75, 0.25, 1.1, 0.75, 0.9)
        gplay(self, FadeIn(wall, shift=UP * 0.2), FadeIn(scorer), FadeIn(under(scorer, "scorer", 32, buff=0.12)), run_time=0.45)
        at(self, "an unconfirmed board")
        c = crate_at(0.55, 0.0, 0.95, 0.7, 0.9)
        gplay(self, FadeIn(c, shift=RIGHT * 0.6), FadeIn(under(c, "unconfirmed", 32)), run_time=0.45)
        gplay(self, Create(cross(1.85, 0.75, 0.2)), run_time=0.3)
        at(self, "treat it as open")
        gplay(self, FadeIn(T("would read it as open", 30).next_to(scorer, UP, buff=0.25).set_x(4.3)), run_time=0.35)
        finish(self)


# ═════════════════════════════ B09 — agent loop + the eval log to come ═════════════════════════════
class B09_SignOff(Scene):
    def construct(self):
        honesty_tag(self)
        loop = Ellipse(width=5.6, height=2.8, stroke_color=INK, stroke_width=5).move_to([-2.2, 0.0, 0])
        head = Polygon([-5.0, 0.3, 0], [-5.22, -0.1, 0], [-4.78, -0.1, 0], fill_color=INK, fill_opacity=1, stroke_width=0)
        enter(self, loop, head, at_left(T("Claude Code runs the recipe", 34).move_to([0, 2.4, 0]), -5.0))
        at(self, "the human gates")
        g1 = Square(side_length=0.5, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(loop.point_from_proportion(0.25))
        g2 = Square(side_length=0.5, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(loop.point_from_proportion(0.75))
        gplay(self, FadeIn(g1, scale=0.6), FadeIn(g2, scale=0.6), FadeIn(under(g2, "human gates", 32, buff=0.2)), run_time=0.4)
        token = Dot(loop.point_from_proportion(0.0), radius=0.16, color=TERRA)
        self.add(token)
        # the work token travels the loop and stops JUST SHORT of the first human gate (on top of it, GATE T reads
        # the two as overlapping labels)
        gplay(self, MoveAlongPath(token, loop), run_time=0.9, rate_func=lambda t: 0.205 * smooth(t))
        at(self, "for my sign-off")
        tick = check(*(np.array(g1.get_center(), dtype=float)[:2] + np.array([0.8, 0.55])), s=0.2)   # clear of the loop line
        gplay(self, Create(tick), FadeIn(beside(tick, "my sign-off", 32, buff=0.2)), run_time=0.35)
        at(self, "Evaluation is still")
        ghost = DashedVMobject(Rectangle(width=1.7, height=2.1, stroke_color=INK, stroke_width=4), num_dashes=30).move_to([4.6, 0.0, 0])
        lab = under(ghost, "eval log", 34)
        gplay(self, Create(ghost), FadeIn(lab), run_time=0.5)
        at(self, "with the wrong ones")
        gplay(self, FadeIn(under(lab, "(proposed)", 30, buff=0.1)), run_time=0.3)
        finish(self)


# ═════════════════════════════ B10 — what it will never do ═════════════════════════════
class B10_Never(Scene):
    def construct(self):
        honesty_tag(self)
        wall = Rectangle(width=0.3, height=4.0, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([0.0, 0.25, 0])
        enter(self, wall)
        icons = [
            ("apply", sheet(-3.0, 1.45, 0.75, 0.95, rows=2), "never apply"),
            ("email", VGroup(Rectangle(width=1.0, height=0.66, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4),
                             Line([-0.5, 0.33, 0], [0, -0.05, 0], color=INK, stroke_width=4),
                             Line([0, -0.05, 0], [0.5, 0.33, 0], color=INK, stroke_width=4)).move_to([-3.0, 0.25, 0]), "email"),
            ("contact", VGroup(RoundedRectangle(width=1.0, height=0.66, corner_radius=0.2, fill_color=PAGE_TOP, fill_opacity=1,
                                                stroke_color=INK, stroke_width=4),
                               Polygon([-0.25, -0.33, 0], [-0.05, -0.33, 0], [-0.35, -0.55, 0], fill_color=INK, fill_opacity=1,
                                       stroke_width=0)).move_to([-3.0, -0.95, 0]), "or contact anyone"),
        ]
        for name, m, cue in icons:
            at(self, cue)
            y = centre(m)[1]
            gplay(self, FadeIn(m, shift=RIGHT * 1.0), FadeIn(T(name, 32).move_to([-5.2, y, 0])), run_time=0.4)
            gplay(self, Create(cross(-1.0, y, 0.18)), run_time=0.2)
        at(self, "The person decides")
        lst = sheet(3.4, 0.9, 1.4, 1.8, rows=4)
        gplay(self, FadeIn(lst, shift=LEFT * 0.4), FadeIn(under(lst, "you decide", 34)), run_time=0.45)
        at(self, "won't score")
        cv = sheet(3.4, -1.55, 0.8, 0.85, rows=2)
        gplay(self, FadeIn(cv), FadeIn(beside(cv, "no résumé", 32)), run_time=0.35)
        gplay(self, Create(cross(3.4, -1.55, 0.3)), run_time=0.25)
        finish(self)


# ═════════════════════════════ B11 — the first piece: coverage 16 / 123 ═════════════════════════════
class B11_Coverage(Scene):
    """16 confirmed boards of 123 candidates: run-2 (2026-10-03). The bar never fills: no invented progress."""
    def construct(self):
        honesty_tag(self)
        base = Rectangle(width=10.0, height=0.55, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([0.4, -1.15, 0])
        enter(self, base)
        at(self, "board resolver")
        res = dark_block(-4.3, 1.25, 1.3, 0.85, 1.0)
        gplay(self, FadeIn(res, shift=UP * 0.3), FadeIn(under(res, "board resolver", 34, buff=0.15)), run_time=0.45)
        at(self, "Today sixteen")
        num = T("16 / 123", 104).move_to([1.4, 1.2, 0])
        filled = Rectangle(width=10.0 * 16 / 123, height=0.55, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0)
        filled.move_to([-4.6 + 10.0 * 16 / 123 / 2, -1.15, 0])
        gplay(self, FadeIn(num, scale=0.85), run_time=0.45)
        gplay(self, GrowFromEdge(filled, LEFT), FadeIn(under(base, "boards confirmed today", 32)), run_time=0.5)
        at(self, "that number rises")
        gplay(self, Create(arrow([4.5, 0.55], [4.5, 1.9], dashed=True, color=BAR1)), run_time=0.45)
        at(self, "raw response")
        gplay(self, FadeIn(under(num, "+ raw response + a test, per board", 30, buff=0.2)), run_time=0.35)
        finish(self)


# ═════════════════════════════ B12 — the risk ═════════════════════════════
class B12_Locked(Scene):
    def construct(self):
        honesty_tag(self)
        viso = iso_at(-4.4, 0.45, 1.6, 1.6, 1.6, 0.92)
        vault = viso.box(0, 0, 0, 1.6, 1.6, 1.6, DARK_TOP, DARK_L, DARK_R)
        lock = Circle(radius=0.2, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(viso.p(0.8, 0, 0.8))
        v = VGroup(vault, lock)
        enter(self, v)
        at(self, "may have no public board")
        gplay(self, FadeIn(under(v, "no public board?", 34, buff=0.15)), run_time=0.35)
        c = crate_at(-1.6, 0.55, 0.95, 0.7, 0.9)
        gplay(self, FadeIn(c, shift=LEFT * 0.5), run_time=0.4)
        gplay(self, Create(cross(-2.7, 0.75, 0.18)), run_time=0.25)
        at(self, "I don't know how many")
        hand = tray_at(-0.6, -1.15, 1.4, 0.45, 0.9)
        gplay(self, FadeIn(hand), FadeIn(beside(hand, "check by hand", 32)), run_time=0.35)
        gplay(self, c.animate.move_to([-0.6, -0.95, 0]), run_time=0.6)
        for nm, x in (("Greenhouse", 1.6), ("Lever", 3.2), ("Ashby", 4.8)):
            at(self, nm)
            pg = sheet(x, 1.75, 1.15, 1.3, rows=3)
            gplay(self, FadeIn(pg, shift=DOWN * 0.2), FadeIn(under(pg, nm, 30, buff=0.12)), run_time=0.3)
        at(self, "never scrape")
        gplay(self, FadeIn(T("public boards only · no scraping", 30).move_to([3.2, 0.2, 0])), run_time=0.35)
        at(self, "report coverage")
        gplay(self, FadeIn(T("coverage, reported as a number", 30).move_to([3.3, -0.45, 0])), run_time=0.35)
        finish(self)


# ═════════════════════════════ B13 — what I don't know yet ═════════════════════════════
class B13_Experiment(Scene):
    def construct(self):
        honesty_tag(self)
        ciso = iso_at(-4.6, 0.5, 1.05, 1.05, 0.8, 1.0)
        comp = VGroup(plinth(ciso, 0, 0, 1.05, 1.05), crate(ciso, 0, 0, 0, 1.05, 1.05, 0.8))
        enter(self, comp)
        at(self, "recent funding")
        gplay(self, FadeIn(under(comp, "recent funding", 34)), run_time=0.35)
        at(self, "predicts hiring")
        gplay(self, FadeIn(T("→ hiring?", 44).move_to([-1.85, 0.45, 0]), shift=RIGHT * 0.2), run_time=0.35)
        at(self, "after fourteen days")
        days = VGroup(*[Square(side_length=0.42, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3)
                        for _ in range(14)]).arrange_in_grid(rows=2, cols=7, buff=0.12).move_to([1.7, 0.45, 0])
        gplay(self, FadeIn(days), FadeIn(under(days, "14 days", 34)), run_time=0.35)
        gplay(self, LaggedStart(*[d.animate.set_fill(BAR2) for d in days], lag_ratio=0.12), run_time=1.2)
        at(self, "logging whether")
        res = DashedVMobject(Square(side_length=1.3, stroke_color=INK, stroke_width=5), num_dashes=20).move_to([4.75, 0.45, 0])
        gplay(self, Create(res), FadeIn(T("?", 64).move_to([4.75, 0.45, 0])), FadeIn(under(res, "posting appeared?", 30).set_x(4.55)),
              run_time=0.45)
        finish(self)


# ═════════════════════════════ B14 — why this project ═════════════════════════════
class B14_Stack(Scene):
    def construct(self):
        honesty_tag(self)
        pile = VGroup(*[sheet(-4.4 + 0.12 * i, 0.55 - 0.08 * i, 1.3, 1.6, rows=3) for i in range(8)])
        enter(self, pile)
        at(self, "a hundred-plus")
        lab_p = under(pile, "100+ applications a day", 32)
        gplay(self, FadeIn(lab_p), run_time=0.3)
        at(self, "It's a mix")
        smart = sheet(-4.0, 0.55, 1.3, 1.6, rows=3)
        gplay(self, FadeOut(pile, shift=DOWN * 0.3), FadeOut(lab_p), FadeIn(smart), FadeIn(under(smart, "a short list", 32)),
              run_time=0.5)
        # Claude Code's part (grey), mine (kraft), new to me (dashed); every label right of its own layer
        biso = Iso(-0.9, -2.0, 1.0)
        x_lab = 1.25

        def lab_for(m, s):
            return at_left(T(s, 30).move_to([0, centre(m)[1], 0]), x_lab)
        b_code = biso.box(0, 0, 0, 2.0, 2.0, 0.5, BAR3, BAR2, BAR1)
        at(self, "Claude Code wrote")
        gplay(self, FadeIn(b_code, shift=UP * 0.2), FadeIn(lab_for(b_code, "prototype code: Claude Code")), run_time=0.4)
        at(self, "I set its rules")
        b_rules = biso.box(0, 0, 0.56, 2.0, 2.0, 0.5)
        gplay(self, FadeIn(b_rules, shift=DOWN * 0.3), FadeIn(lab_for(b_rules, "the rules: mine")), run_time=0.4)
        at(self, "signed its human gates")
        b_gates = biso.box(0, 0, 1.12, 2.0, 2.0, 0.5)
        gplay(self, FadeIn(b_gates, shift=DOWN * 0.3), FadeIn(lab_for(b_gates, "gate sign-offs: mine")), run_time=0.4)
        at(self, "New for me")
        news = [DashedVMobject(biso.quad([(0, 0, z), (2.0, 0, z), (2.0, 2.0, z), (0, 2.0, z)], STAGE, stroke=INK, sw=4),
                               num_dashes=24) for z in (2.05, 2.65)]
        gplay(self, FadeIn(VGroup(*news), shift=DOWN * 0.5), run_time=0.45)
        at(self, "evaluation")
        gplay(self, FadeIn(lab_for(news[0], "new: evaluation")), run_time=0.3)
        at(self, "and resolving")
        gplay(self, FadeIn(lab_for(news[1], "new: resolving boards")), run_time=0.3)
        finish(self)
