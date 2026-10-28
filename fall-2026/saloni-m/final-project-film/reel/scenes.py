"""
iso_kit.py — the show-tell drawing kit. PASTE this block at the top of a reel's scenes.py;
do not import it (Gate A copies only scenes.py into its sandbox).

Drawn isometric objects in the Claude palette: cardboard boxes (closed, open, taped), dark
MCP blocks with ports, flat skill pages, server stacks with lights, checks, a cursor, pills.
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


# ═════════════════════════════ my helpers (OPT Countdown pitch) ═════════════════════════════
# GATE T and Gate V sample each clip at its midpoint, so no animation may be running then.
# P() holds any animation that would cross the midpoint until just after it.
MARGIN = 0.25


def P(self, *anims, rt=1.0):
    bid = type(self).__name__.split("_")[0]
    mid = _TARGET.get(bid, 0) / 2
    t = _elapsed(self)
    if mid and t < mid + MARGIN and t + rt > mid - MARGIN:
        self.wait(mid + MARGIN - t)
    self.play(*anims, run_time=rt)


def end(self):
    """Hold to the end of the narration, a little short so the clip never outruns its audio."""
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    left = target - _elapsed(self) - 0.08
    if left > 0.05:
        self.wait(left)


def L(s, x, y, size=34, align=None, bold=False):
    """A label at (x, y). align=LEFT puts its left edge at x."""
    t = T(s, size=size, bold=bold)
    if align is None:
        t.move_to([x, y, 0])
    else:
        t.move_to([x, y, 0], aligned_edge=align)
    return t


def tag(s):
    """Top-left provenance tag: 'constructed sketch' or the date of a real run."""
    return L(s, -6.0, 3.0, size=32, align=LEFT)


def card(x, y, w=1.6, h=2.0, lines=3):
    """A flat job-posting card: white face, grey outline, ghost text lines."""
    face = RoundedRectangle(width=w, height=h, corner_radius=0.12, fill_color=CARD, fill_opacity=1,
                            stroke_color=DIM, stroke_width=3).move_to([x, y, 0])
    rows = VGroup(*[Line([x - w / 2 + 0.25, y + h / 2 - 0.45 - i * 0.4, 0],
                         [x + w / 2 - 0.25 - (0.3 if i == lines - 1 else 0), y + h / 2 - 0.45 - i * 0.4, 0],
                         color=BAR2, stroke_width=6) for i in range(lines)])
    return VGroup(face, rows)


def person(x, y, s=1.0):
    head = Circle(radius=0.28 * s, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + 0.45 * s, 0])
    body = ArcBetweenPoints([x - 0.5 * s, y - 0.35 * s, 0], [x + 0.5 * s, y - 0.35 * s, 0], angle=-PI * 0.9,
                            color=INK, stroke_width=4)
    body.set_fill(BOX_L, opacity=1)
    return VGroup(body, head)


def cross(x, y, s=0.22, w=7):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


def floor_shadow(x, y, w=3.0):
    return Ellipse(width=w, height=0.35, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


# ═════════════════════════════ scenes ═════════════════════════════

class B00_WhatItIs(Scene):
    def construct(self):
        iso = Iso(-0.2, -1.1, 0.95)
        self.add(tag("constructed sketch"))
        shadow = floor_shadow(-0.2, -1.25, 3.4)
        tool = iso.box(0, 0, 0, 1.8, 1.8, 1.3)
        tape = iso.tape(0, 0, 1.3, 1.8, 1.8)
        name = L("OPT Countdown", -0.2, -2.35, size=40, bold=True)
        P(self, FadeIn(shadow), FadeIn(tool, shift=DOWN * 0.4), FadeIn(tape), rt=0.9)
        P(self, FadeIn(name), rt=0.6)
        until(self, "list of job postings")
        cards = VGroup(*[card(-5.0 + i * 0.18, 0.9 - i * 0.18, 1.3, 1.6) for i in range(4)])
        lab_in = L("postings", -4.75, -0.75, size=34)
        P(self, LaggedStart(*[FadeIn(c, shift=RIGHT * 0.5) for c in cards], lag_ratio=0.2), FadeIn(lab_in), rt=1.2)
        P(self, LaggedStart(*[c.animate.move_to([-0.2, 0.9, 0]).scale(0.3) for c in cards], lag_ratio=0.25), rt=1.4)
        self.remove(*cards)
        until(self, "it says apply")
        outs, labs = VGroup(), VGroup()
        for i, word in enumerate(["apply", "network", "skip", "blocked"]):
            y = 2.0 - i * 1.15
            outs.add(card(3.3, y, 0.8, 0.9, lines=2))
            labs.add(L(word, 4.0, y, size=34, align=LEFT))
        P(self, LaggedStart(*[FadeIn(o, shift=RIGHT * 0.4) for o in outs], lag_ratio=0.3),
          LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.3), rt=1.6)
        until(self, "the evidence")
        dots = VGroup(*[Dot([2.75, 2.0 - i * 1.15 + 0.3, 0], radius=0.07, color=TERRA) for i in range(4)])
        P(self, LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2), rt=0.8)
        end(self)


class B01_ExistsToday(Scene):
    def construct(self):
        self.add(tag("real run · 2026-10-13"))
        hero = L("12 / 12", -3.5, 1.5, size=110, bold=True)
        sub = L("tests pass", -3.5, 0.35, size=38)
        checks = VGroup(*[check(-5.3 + (i % 6) * 0.72, -0.8 - (i // 6) * 0.75, s=0.2) for i in range(12)])
        P(self, FadeIn(sub), rt=0.5)
        until(self, "Twelve of twelve")
        P(self, LaggedStart(*[Create(c) for c in checks], lag_ratio=0.12), FadeIn(hero), rt=1.6)
        until(self, "one apply")
        base = -1.6
        bars, nums, names = VGroup(), VGroup(), VGroup()
        for i, (n, word) in enumerate(zip([1, 2, 3, 2], ["apply", "network", "skip", "blocked"])):
            x = 0.7 + i * 1.5
            bars.add(Rectangle(width=0.9, height=0.7 * n, fill_color=BAR1, fill_opacity=1, stroke_color=INK,
                               stroke_width=3).move_to([x, base + 0.35 * n, 0]))
            nums.add(L(str(n), x, base + 0.7 * n + 0.35, size=38))
            names.add(L(word, x, base - 0.4, size=32))
        cap = L("8 postings · fictional student", 2.95, -2.75, size=34)
        P(self, FadeIn(cap), FadeIn(names), rt=0.6)
        P(self, LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25), rt=1.6)
        P(self, FadeIn(nums), rt=0.5)
        until(self, "Everything after")
        rule = Line([-6.0, 2.55, 0], [6.0, 2.55, 0], color=DIM, stroke_width=3)
        P(self, Create(rule), rt=0.6)
        end(self)


class B02_ByHand(Scene):
    def construct(self):
        post = card(-3.8, 0.5, 2.2, 2.8, lines=4)
        lab = L("one posting", -3.8, -1.35, size=34)
        P(self, FadeIn(post, shift=UP * 0.3), FadeIn(lab), rt=0.8)
        steps = [("Look up", "H-1B record"), ("Open the posting", "still live?"),
                 ("Guess how fast", "hiring speed"), ("Count the days", "count days")]
        for i, (phrase, word) in enumerate(steps):
            until(self, phrase)
            y = 2.0 - i * 1.2
            ring = Circle(radius=0.32, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0.6, y, 0])
            num = L(str(i + 1), 0.6, y, size=36)
            name = L(word, 1.25, y, size=36, align=LEFT)
            P(self, GrowFromCenter(ring), FadeIn(num), FadeIn(name), rt=0.6)
        until(self, "twenty minutes")
        face = Circle(radius=0.5, fill_color=CARD, fill_opacity=1, stroke_color="#917A55", stroke_width=4).move_to([-3.8, -2.45, 0])
        hand = Line([-3.8, -2.45, 0], [-3.8, -2.05, 0], color="#917A55", stroke_width=6)
        est = L("20 min · estimate", -3.05, -2.45, size=34, align=LEFT)
        P(self, FadeIn(face), FadeIn(hand), FadeIn(est), rt=0.6)
        P(self, Rotate(hand, angle=-TAU, about_point=np.array([-3.8, -2.45, 0])), rt=1.5)
        end(self)


class B03_GhostPosting(Scene):
    def construct(self):
        post = card(-3.6, 0.2, 2.2, 2.8, lines=4)
        lab = L("fake job link", -3.6, -1.65, size=34)
        P(self, FadeIn(post, shift=UP * 0.3), FadeIn(lab), rt=0.8)
        until(self, "It said active")
        said = L("checker: active", -4.2, 2.35, size=36, align=None)
        ok = check(-2.2, 2.4, s=0.2)
        P(self, FadeIn(said), Create(ok), rt=0.7)
        scan = Line([-4.8, 1.55, 0], [-2.4, 1.55, 0], color=TERRA, stroke_width=6)
        P(self, FadeIn(scan), rt=0.2)
        P(self, scan.animate.shift(DOWN * 2.7), rt=1.0)
        P(self, FadeOut(scan), rt=0.2)
        until(self, "Greenhouse")
        iso = Iso(3.0, -1.6, 1.0)
        stack, lights = iso.server(0, 0, 0)
        api = L("job API", 3.0, -2.45, size=34)
        P(self, FadeIn(stack, shift=UP * 0.3), FadeIn(lights), FadeIn(api), rt=0.8)
        P(self, lights.animate.set_color(TERRA), rt=0.4)
        code = L("404", 3.0, 1.75, size=90, bold=True)
        P(self, FadeIn(code), rt=0.5)
        until(self, "the API answer wins")
        no = cross(-2.2, 2.4, s=0.22)
        wins = L("API wins", 3.0, 2.75, size=34)
        P(self, FadeOut(ok), rt=0.3)
        P(self, Create(no), FadeIn(wins), rt=0.6)
        end(self)


class B04_Silence(Scene):
    def construct(self):
        x0, y0, cw, rh = -5.6, 1.6, 1.25, 0.62
        cells, fills = VGroup(), VGroup()
        empty = {1: "HubSpot", 3: "DraftKings"}
        for r in range(5):
            for c in range(3):
                cx, cy = x0 + cw / 2 + c * cw, y0 - r * rh
                cells.add(Rectangle(width=cw, height=rh, fill_color=CARD, fill_opacity=1, stroke_color=DIM,
                                    stroke_width=2).move_to([cx, cy, 0]))
                if r not in empty:
                    fills.add(Line([cx - 0.4, cy, 0], [cx + 0.4, cy, 0], color=BAR2, stroke_width=8))
        head = L("H-1B data", -3.7, 2.55, size=36)
        P(self, FadeIn(cells), FadeIn(head), rt=0.8)
        P(self, LaggedStart(*[Create(f) for f in fills], lag_ratio=0.05), rt=1.0)
        until(self, "HubSpot")
        names = VGroup(*[L(n, -1.65, y0 - r * rh, size=32, align=LEFT) for r, n in empty.items()])
        P(self, FadeIn(names), rt=0.6)
        until(self, "skips them")
        no_rec = L("no record ≠ won't sponsor", -3.0, -2.2, size=34)
        P(self, FadeIn(no_rec), rt=0.6)
        until(self, "Mine marks them")
        pile = VGroup(card(3.4, 0.9, 1.2, 1.4, lines=2), card(3.6, 0.7, 1.2, 1.4, lines=2))
        blocked = L("blocked", 3.5, -0.4, size=36)
        who = person(5.3, 0.8, 0.9)
        check_lab = L("a person checks", 4.3, -1.3, size=32)
        P(self, LaggedStart(*[FadeIn(c, shift=RIGHT * 0.8) for c in pile], lag_ratio=0.3), FadeIn(blocked), rt=0.9)
        P(self, FadeIn(who), FadeIn(check_lab), rt=0.6)
        end(self)


class B05_Clock(Scene):
    def construct(self):
        x0, k = -5.4, 0.12          # 0.12 units per day
        def bar(days, y, fill):
            return Rectangle(width=days * k, height=0.55, fill_color=fill, fill_opacity=1, stroke_color=INK,
                             stroke_width=3).move_to([x0 + days * k / 2, y, 0])
        b90 = bar(90, 1.6, BAR2)
        l90 = L("90 days allowed", x0, 2.35, size=34, align=LEFT)
        P(self, GrowFromEdge(b90, LEFT), FadeIn(l90), rt=1.0)
        until(self, "fifty-three days left")
        b53 = bar(53, 0.2, BOX_R)
        l53 = L("53 days left", x0, 0.95, size=34, align=LEFT)
        edge = DashedLine([x0 + 53 * k, 0.7, 0], [x0 + 53 * k, -1.85, 0], color=INK, stroke_width=3)
        P(self, GrowFromEdge(b53, LEFT), FadeIn(l53), rt=0.9)
        P(self, Create(edge), rt=0.4)
        b60 = bar(60, -1.2, BAR1)
        l60 = L("60 days to hire", x0, -2.0, size=34, align=LEFT)
        P(self, GrowFromEdge(b60, LEFT), FadeIn(l60), rt=1.2)
        late = Dot([x0 + 60 * k + 0.25, -1.2, 0], radius=0.1, color=TERRA)
        P(self, GrowFromCenter(late), rt=0.4)
        until(self, "Klaviyo and Toast")
        out = L("Klaviyo, Toast: skip", 3.4, -2.75, size=34)
        P(self, FadeIn(out), rt=0.6)
        end(self)


class B06_WhoOpensIt(Scene):
    def construct(self):
        self.add(tag("constructed sketch"))
        stu = person(-4.9, 0.6, 1.0)
        stu_lab = L("student", -4.9, -0.45, size=34)
        P(self, FadeIn(stu), FadeIn(stu_lab), rt=0.7)
        until(self, "one-page report")
        rep = card(-3.1, 0.6, 1.3, 1.7, lines=3)
        rep_lab = L("report", -3.1, -0.65, size=34)
        P(self, FadeIn(rep, shift=LEFT * 0.4), FadeIn(rep_lab), rt=0.7)
        until(self, "hiring manager")
        win = RoundedRectangle(width=5.4, height=3.9, corner_radius=0.15, fill_color=CARD, fill_opacity=1,
                               stroke_color=DIM, stroke_width=3).move_to([2.9, -0.15, 0])
        bar = Rectangle(width=5.4, height=0.45, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([2.9, 1.58, 0])
        who = L("hiring manager · engineer", 2.9, 2.4, size=34)
        P(self, FadeIn(win), FadeIn(bar), FadeIn(who), rt=0.8)
        rows = ["README", "tests", "eval log"]
        boxes, names = VGroup(), VGroup()
        for i, r in enumerate(rows):
            y = 0.75 - i * 0.95
            boxes.add(Square(side_length=0.42, fill_color=CARD, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([0.95, y, 0]))
            names.add(L(r, 1.45, y, size=36, align=LEFT))
        P(self, FadeIn(boxes), FadeIn(names), rt=0.6)
        ptr = cursor(4.6, -0.6)
        P(self, FadeIn(ptr), rt=0.3)
        for i, phrase in enumerate(["opens the read me", "runs the tests", "evaluation log"]):
            until(self, phrase)
            y = 0.75 - i * 0.95
            P(self, ptr.animate.move_to([1.15, y - 0.2, 0], aligned_edge=UL), rt=0.5)
            P(self, Create(check(0.97, y + 0.02, s=0.16)), rt=0.3)
        until(self, "first minute")
        lab = L("first 60 seconds", 2.9, -2.75, size=34)
        P(self, FadeIn(lab), rt=0.5)
        end(self)


class B07_Proves(Scene):
    def construct(self):
        self.add(tag("constructed sketch"))
        page = RoundedRectangle(width=4.2, height=4.6, corner_radius=0.15, fill_color=CARD, fill_opacity=1,
                                stroke_color=DIM, stroke_width=3).move_to([-2.6, -0.3, 0])
        rows = VGroup(*[Line([-4.3, 1.2 - i * 1.0, 0], [-1.0, 1.2 - i * 1.0, 0], color=BAR1, stroke_width=10) for i in range(4)])
        head = L("report", -2.6, 2.4, size=36)
        top = Rectangle(width=4.2, height=0.45, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([-2.6, 1.78, 0])
        P(self, FadeIn(page), FadeIn(top), FadeIn(head), rt=0.7)
        P(self, LaggedStart(*[Create(r) for r in rows], lag_ratio=0.2), rt=1.0)
        until(self, "Verification")
        tags = ["record", "your input", "model guess"]
        for i, t in enumerate(tags):
            y = 1.2 - i * 1.0
            pl = pill(1.95, y, 2.6, fill=BAR2)
            tx = L(t, 1.95, y, size=34)
            P(self, FadeIn(pl, shift=LEFT * 0.6), FadeIn(tx, shift=LEFT * 0.6), rt=0.5)
        until(self, "Evaluation")
        ev = L("eval: how often wrong", 2.2, 2.4, size=32)
        P(self, FadeIn(ev), rt=0.4)
        until(self, "no record, no answer")
        y = 1.2 - 3 * 1.0
        none = L("no record → blocked", 2.3, y, size=32)
        P(self, FadeIn(none, shift=LEFT * 0.6), rt=0.6)
        until(self, "would not prove")
        not_proven = L("not proven: it gets anyone hired", 0.0, -3.0, size=34)
        P(self, FadeIn(not_proven), rt=0.6)
        end(self)


class B08_Scope(Scene):
    def construct(self):
        out_h = L("out", -3.4, 2.6, size=40, bold=True)
        first_h = L("first", 3.2, 2.6, size=40, bold=True)
        wall = Line([-0.2, 2.6, 0], [-0.2, -2.9, 0], color=GHOST, stroke_width=4)
        iso_a = Iso(-4.3, -1.6, 0.8)
        tool = iso_a.box(0, 0, 0, 1.6, 1.6, 1.1)
        tape_a = iso_a.tape(0, 0, 1.1, 1.6, 1.6)
        P(self, FadeIn(out_h), FadeIn(first_h), Create(wall), FadeIn(tool), FadeIn(tape_a), rt=0.9)
        until(self, "Immigration advice")
        adv = card(-1.6, 0.8, 1.4, 1.7, lines=3)
        adv_lab = L("immigration advice", -2.5, -2.55, size=32)
        P(self, FadeIn(adv), FadeIn(adv_lab), rt=0.5)
        P(self, adv.animate.move_to([-3.0, 0.6, 0]), rt=0.6)
        P(self, adv.animate.move_to([-1.3, 0.8, 0]), rt=0.5)
        no = cross(-1.3, -0.4, s=0.25)
        P(self, Create(no), rt=0.4)
        until(self, "the school's D S O")
        dso = L("ask the DSO", -2.5, 2.0, size=32)
        P(self, FadeIn(dso), rt=0.4)
        until(self, "What comes first")
        iso_b = Iso(3.2, -1.3, 0.8)
        repo = iso_b.box(0, 0, 0, 1.6, 1.6, 1.1, top=PAGE_TOP, left=PAGE_L, right=PAGE_R)
        repo_lab = L("own repo", 3.2, 1.75, size=36)
        P(self, FadeIn(repo, shift=DOWN * 0.3), FadeIn(repo_lab), rt=0.7)
        for i, (phrase, word) in enumerate([("clone it", "clone"), ("run the tests", "test"), ("watch them pass", "pass")]):
            until(self, phrase)
            x = 1.4 + i * 1.75
            P(self, Create(check(x - 0.8, -2.5, s=0.15)), FadeIn(L(word, x + 0.05, -2.5, size=32, align=None)), rt=0.4)
        end(self)


class B09_Risk(Scene):
    def construct(self):
        guess = L("hiring time = my guess", -2.0, 2.55, size=36)
        sx = lambda v: (v - 0.30) * 50          # score → x
        axis = Line([sx(0.20), -0.6, 0], [sx(0.40), -0.6, 0], color=INK, stroke_width=4)
        ends = VGroup(L("0.20", sx(0.20), -1.15, size=32), L("0.40", sx(0.40), -1.15, size=32))
        bar = DashedLine([0, -1.1, 0], [0, 1.4, 0], color=INK, stroke_width=4)
        bar_lab = L("bar 0.30", -1.0, 1.75, size=34)
        P(self, FadeIn(guess), Create(axis), FadeIn(ends), rt=0.8)
        P(self, Create(bar), FadeIn(bar_lab), rt=0.6)
        until(self, "cleared the bar")
        dot = Dot([sx(0.317), 0.9, 0], radius=0.14, color=TERRA)
        val = L("0.317", sx(0.317) + 0.95, 1.75, size=34)
        P(self, FadeIn(dot), FadeIn(val), rt=0.4)
        P(self, dot.animate.move_to([sx(0.317), -0.6, 0]), rt=0.6, )
        gap = L("+0.017", sx(0.317) + 1.0, 0.25, size=32)
        P(self, FadeIn(gap), rt=0.4)
        until(self, "would flip")
        q = L("?", sx(0.317), -2.05, size=80, bold=True)
        arrows = VGroup(Arrow([sx(0.317) - 0.3, -2.0, 0], [sx(0.317) - 1.8, -2.0, 0], color=INK, stroke_width=5, buff=0),
                        Arrow([sx(0.317) + 0.3, -2.0, 0], [sx(0.317) + 1.8, -2.0, 0], color=INK, stroke_width=5, buff=0))
        flip = L("±15 days", sx(0.317), -2.95, size=34)
        P(self, GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(q), FadeIn(flip), rt=0.7)
        end(self)


class B10_WhyThis(Scene):
    def construct(self):
        iso_a = Iso(-3.6, -1.4, 0.85)
        have = iso_a.box(0, 0, 0, 1.6, 1.6, 1.2)
        tape = iso_a.tape(0, 0, 1.2, 1.6, 1.6)
        have_h = L("have", -3.6, 1.6, size=40, bold=True)
        P(self, FadeIn(have, shift=DOWN * 0.3), FadeIn(tape), FadeIn(have_h), rt=0.8)
        until(self, "JavaScript and Node")
        js = L("JavaScript · Node", -3.6, -2.15, size=34)
        P(self, FadeIn(js), rt=0.5)
        until(self, "CodeBuddies")
        cb = L("evidence: CodeBuddies", -3.6, -2.85, size=32)
        ok = check(-1.6, 1.62, s=0.2)
        P(self, FadeIn(cb), Create(ok), rt=0.6)
        until(self, "What's new to me")
        iso_b = Iso(3.2, -1.6, 0.85)
        back, front = iso_b.open_box(0, 0, 0, 1.8, 1.8, 1.1)
        new_h = L("learning", 3.2, 1.6, size=40, bold=True)
        ev = L("evaluation sets", 3.2, -2.15, size=34)
        P(self, FadeIn(back), FadeIn(front), FadeIn(new_h), FadeIn(ev), rt=0.8)
        pages = VGroup(*[iso_b.page(0.35 + 0.1 * i, 0.3, 0.15 + 0.08 * i, 1.0, 1.2) for i in range(3)])
        for pg in pages:
            pg.set_z_index(1)
        P(self, LaggedStart(*[FadeIn(p, shift=DOWN * 0.8) for p in pages], lag_ratio=0.3), rt=1.2)
        until(self, "Claude Code did most")
        cc = L("prototype: mostly typed by Claude Code", 0.0, 2.75, size=32)
        P(self, FadeIn(cc), rt=0.6)
        until(self, "start with thirty")
        thirty = L("start: 30 postings", 3.2, -2.85, size=32)
        P(self, FadeIn(thirty), rt=0.5)
        end(self)


class BOUT_Outro(Scene):
    def construct(self):
        iso = Iso(0, 1.0, 0.7)
        box = iso.box(-0.8, -0.8, 0, 1.6, 1.6, 1.1)
        tape = iso.tape(-0.8, -0.8, 1.1, 1.6, 1.6)
        title = L("OPT Countdown", 0, -0.55, size=84, bold=True)
        sub = L("final project pitch", 0, -1.45, size=44)
        name = L("Saloni Mathure · INFO 7375 · 2026-10-13", 0, -2.35, size=34)
        self.add(box, tape, title, sub, name)
        rule = Line([-3.2, -1.95, 0], [3.2, -1.95, 0], color=DIM, stroke_width=3)
        self.play(Create(rule), run_time=0.8)
        end(self)
