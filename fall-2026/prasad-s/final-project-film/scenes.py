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


# ═════════════════════════════ GistGap helpers ═════════════════════════════
# Gate V samples each beat at 50% and 85%; GATE T samples at 50%. go() keeps every
# animation off those instants (it finishes before the window or starts after it),
# and hold() fills to the measured audio without running past it.
DEEP_KRAFT = "#9C8462"


def _bid(self):
    return type(self).__name__.split("_")[0]


def go(self, phrase, *anims, rt=0.6, lead=0.25):
    if phrase:
        until(self, phrase, lead)
    total = _TARGET.get(_bid(self), 0)
    if total:
        for frac, pad in ((0.5, 0.4), (0.85, 0.3)):
            t = _elapsed(self)
            lo, hi = total * frac - pad, total * frac + pad
            if t < hi and t + rt > lo:
                if lo - t >= 0.3:
                    rt = lo - t - 0.02        # fits before the window
                else:
                    self.wait(max(0.05, hi - t))  # start after it
        rt = max(0.2, min(rt, total - 0.1 - _elapsed(self)))
    self.play(*anims, run_time=rt)


def at(self, frac):
    """Wait until `frac` of the beat's measured audio (narration-independent timing)."""
    total = _TARGET.get(_bid(self), 0)
    if total:
        gap = total * frac - _elapsed(self)
        if gap > 0.05:
            self.wait(gap)


def hold(self):
    total = _TARGET.get(_bid(self), 0)
    rest = (total - _elapsed(self) - 0.06) if total else 1.5
    if rest > 0.05:
        self.wait(rest)


def tag(s):
    """The provenance label (CONSTRUCTED · …, WILL EXIST · …, REDRAWN …), top left."""
    t = T(s, 32, bold=True)
    t.move_to([-6.0 + t.width / 2, 3.0, 0])
    return t


def lab(s, x, y, size=38):
    return T(s, size).move_to([x, y, 0])


def lab_l(s, x, y, size=38):
    t = T(s, size)
    t.move_to([x + t.width / 2, y, 0])
    return t


def cross(x, y, s=0.35, w=8):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


def arrow(a, b, w=8):
    return Arrow(a, b, buff=0, color=INK, stroke_width=w, max_tip_length_to_length_ratio=0.08,
                 max_stroke_width_to_length_ratio=10)


def on_base(iso, x0, y0, z0, w, d, h, pad=0.2, base_h=0.25):
    """A kraft box on a dark base (the base carries Gate V contrast)."""
    base = iso.box(x0 - pad, y0 - pad, z0, w + 2 * pad, d + 2 * pad, base_h, DARK_TOP, DARK_L, DARK_R)
    box = iso.box(x0, y0, z0 + base_h, w, d, h)
    return base, box


def _manim_field(bid, key, default):
    for b in (_SHEET["beats"] if "_SHEET" in globals() else []):
        if b.get("beat_id") == bid:
            return ((b.get("shot") or {}).get("manim") or {}).get(key, default)
    return default


# ═════════════════════════════ GistGap scenes ═════════════════════════════
class B01_Agent(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · drawn to explain"))
        R = Iso(-3.9, -1.9, 1.0)
        base = R.box(-0.3, -0.3, 0, 2.6, 1.9, 0.3, DARK_TOP, DARK_L, DARK_R)
        body = R.box(0, 0, 0.3, 1.3, 1.0, 1.4)
        head = R.box(0.15, 0.1, 1.8, 1.0, 0.8, 0.8)
        eyes = VGroup(Dot(R.p(0.4, 0.1, 2.25), radius=0.1, color=TERRA), Dot(R.p(0.85, 0.1, 2.25), radius=0.1, color=TERRA))
        antenna = VGroup(Line(R.p(0.65, 0.5, 2.6), R.p(0.65, 0.5, 3.0), color=INK, stroke_width=6),
                         Dot(R.p(0.65, 0.5, 3.0), radius=0.1, color=INK))
        bag_back, bag_front = R.open_box(1.45, 0.1, 0.3, 0.8, 0.7, 0.75)
        handle = VGroup(Line(R.p(1.6, 0.45, 1.05), R.p(1.75, 0.45, 1.45), color=INK, stroke_width=5),
                        Line(R.p(1.75, 0.45, 1.45), R.p(2.1, 0.45, 1.45), color=INK, stroke_width=5),
                        Line(R.p(2.1, 0.45, 1.45), R.p(2.25, 0.45, 1.05), color=INK, stroke_width=5))
        arm = Line(R.p(1.3, 0.5, 1.2), R.p(1.75, 0.45, 1.45), color=INK, stroke_width=6)
        robot = VGroup(base, body, head, eyes, antenna, bag_back, bag_front, handle, arm)

        phone = RoundedRectangle(width=2.3, height=4.3, corner_radius=0.3, fill_color=DIM, fill_opacity=1,
                                 stroke_color=DIM, stroke_width=4).move_to([3.4, -0.15, 0])
        screen = RoundedRectangle(width=1.9, height=3.6, corner_radius=0.15, fill_color=CARD, fill_opacity=1,
                                  stroke_width=0).move_to([3.4, -0.05, 0])
        button = pill(3.4, -1.2, 1.75, 0.66, fill=BAR3)
        approve = T("Approve", 34).move_to([3.4, -1.2, 0])
        handset = VGroup(phone, screen, button, approve)
        tap = cursor(4.0, -1.5, 0.5)
        q = T("?", 110).move_to([0.6, 1.3, 0])

        go(self, None, FadeIn(robot, shift=UP * 0.3), rt=0.7)
        go(self, "spend your money", FadeIn(handset), rt=0.5)
        go(self, "You tap Approve", FadeIn(tap, shift=LEFT * 0.4), rt=0.4)
        go(self, "what, exactly", FadeIn(q), rt=0.4)
        hold(self)


class B02_ShownSigned(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · drawn to explain"))
        A, S = Iso(-3.6, -1.3, 1.0), Iso(3.6, -1.3, 1.0)
        base_a, box_a = on_base(A, 0, 0, 0, 1.7, 1.7, 1.5)
        base_s, box_s = on_base(S, 0, 0, 0, 1.7, 1.7, 1.5)
        tape = S.tape(0, 0, 1.75, 1.7, 1.7, drop=0.35)
        shown, signed = lab("SHOWN", -3.6, -2.0, 40), lab("SIGNED", 3.6, -2.0, 40)
        q = T("?", 110).move_to([0, 0.4, 0])
        self.add(base_a, base_s)
        go(self, "What you're shown", FadeIn(box_a, shift=DOWN * 0.3), FadeIn(shown), rt=0.6)
        go(self, "what you sign", FadeIn(VGroup(box_s, tape), shift=DOWN * 0.3), FadeIn(signed), rt=0.6)
        go(self, "They should match", FadeIn(q), rt=0.4)
        hold(self)


class B03_Contract(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · invented example"))
        L, Rt = Iso(-3.4, -0.9, 1.0), Iso(2.8, -0.9, 1.0)
        plinth_l = L.box(-0.25, -0.25, -0.3, 2.5, 3.0, 0.3, DARK_TOP, DARK_L, DARK_R)
        sheets = VGroup(*[L.box(0, 0, 0.08 * i, 2.0, 2.5, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5) for i in range(3)])
        cover = L.page(0, 0, 0.32, 2.0, 2.5)
        cover.set_z_index(3)                           # the cover stays the top sheet
        plinth_r = Rt.box(-0.25, -0.25, -0.3, 2.5, 3.0, 0.3, DARK_TOP, DARK_L, DARK_R)
        page12 = L.page(0, 0, 0.24, 2.0, 2.5)          # page 12 starts just under the cover
        page12.set_z_index(2)                          # stays above the right-hand base when it lands
        start = np.array(L.p(1.0, 1.25, 0.24))
        end = np.array(Rt.p(1.0, 1.25, 0.0))
        path = ArcBetweenPoints(start, end, angle=-PI / 4)
        cover_lab = lab("cover: $50", -3.4, -2.0, 40)
        p12_lab = lab("page 12: $500 / month", 2.8, -2.0, 40)
        scan = Line([0.7, -1.05, 0], [0.7, 1.5, 0], color=TERRA, stroke_width=6)
        scan.set_z_index(3)
        curve = ArcBetweenPoints([-3.0, 1.9, 0], [2.9, 1.9, 0], angle=-PI / 4, color=INK, stroke_width=6)
        spark = Dot([2.9, 1.9, 0], radius=0.1, color=TERRA)

        go(self, None, FadeIn(VGroup(plinth_l, sheets, cover, page12, plinth_r)), rt=0.5)
        go(self, "fifty dollars", FadeIn(cover_lab), rt=0.4)
        go(self, "page twelve", MoveAlongPath(page12, path), rt=0.8)
        go(self, None, FadeIn(scan), rt=0.15)
        go(self, None, scan.animate.shift(RIGHT * 3.8), rt=0.6)
        go(self, None, FadeOut(scan), FadeIn(p12_lab), rt=0.3)
        go(self, "That's the gap", Create(curve), rt=0.8)
        go(self, None, FadeIn(spark), rt=0.3)
        hold(self)


class B04_Browser(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · mock-up, not built"))
        ys = (1.1, 0.5, -0.1, -0.7, -1.3)
        fields = ("amount", "merchant", "cap", "expiry", "recurring")
        lx, rx, cx = -1.6, 3.6, 1.0                    # left panel, right panel, check column
        win = RoundedRectangle(width=10.0, height=5.0, corner_radius=0.2, fill_color=CARD, fill_opacity=1,
                               stroke_color=INK, stroke_width=4).move_to([1.0, 0.05, 0])
        bar = Rectangle(width=9.7, height=0.45, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([1.0, 2.25, 0])
        lights = VGroup(*[Circle(radius=0.08, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([x, 2.25, 0])
                          for x in (-3.4, -3.1, -2.8)])
        panels, rows = VGroup(), VGroup()
        for px, widths in ((lx, (2.6, 2.0, 2.4, 1.8, 2.2)), (rx, (2.6, 2.0, 0.9, 1.8, 2.2))):   # cap row short on the text side
            panels.add(Rectangle(width=3.6, height=3.6, fill_color="#FFFFFF", fill_opacity=1,
                                 stroke_color=BAR1, stroke_width=3).move_to([px, -0.1, 0]))
            for wd, y in zip(widths, ys):
                r = Rectangle(width=wd, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0)
                r.move_to([px - 1.5 + wd / 2, y, 0])
                rows.add(r)
        names = VGroup(*[lab_l(f, -6.0, y, 32) for f, y in zip(fields, ys)])      # field names outside the window
        heads = VGroup(lab("mandate", lx, -2.9, 38), lab("text", rx, -2.9, 38))
        lens = Rectangle(width=8.9, height=0.5, stroke_color=BAR1, stroke_width=4, fill_opacity=0).move_to([1.0, ys[0], 0])
        tick = lambda y: check(cx - 0.05, y, s=0.2, color=INK, w=7)
        flag = Dot([rx - 1.5 + 0.9 + 0.35, ys[2], 0], radius=0.12, color=TERRA)

        go(self, None, FadeIn(VGroup(win, bar, lights, panels, rows)), FadeIn(names), FadeIn(heads), rt=0.6)
        at(self, 0.12); go(self, None, FadeIn(lens), rt=0.15)
        at(self, 0.15); go(self, None, Create(tick(ys[0])), rt=0.3)
        at(self, 0.22); go(self, None, lens.animate.move_to([1.0, ys[1], 0]), rt=0.15)
        at(self, 0.25); go(self, None, Create(tick(ys[1])), rt=0.3)
        at(self, 0.30); go(self, None, lens.animate.move_to([1.0, ys[2], 0]), rt=0.15)
        at(self, 0.33); go(self, None, Create(cross(cx, ys[2], s=0.18, w=7)), FadeIn(flag, scale=0.5), rt=0.4)
        at(self, 0.57); go(self, None, lens.animate.move_to([1.0, ys[3], 0]), rt=0.15)
        at(self, 0.60); go(self, None, Create(tick(ys[3])), rt=0.3)
        at(self, 0.67); go(self, None, lens.animate.move_to([1.0, ys[4], 0]), rt=0.15)
        at(self, 0.70); go(self, None, Create(tick(ys[4])), rt=0.3)
        at(self, 0.72); go(self, None, lens.animate.move_to([1.0, ys[2], 0]), rt=0.2)   # rest on the mismatch
        hold(self)


class B05_Checklist(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · drawn to explain"))
        ys = (1.4, 0.0, -1.4)
        boxes = VGroup(*[Square(side_length=0.7, fill_color=CARD, fill_opacity=1, stroke_color=INK,
                                stroke_width=5).move_to([-4.0, y, 0]) for y in ys])
        bars = VGroup()
        for wd, y in ((3.6, ys[0]), (2.8, ys[1])):
            r = Rectangle(width=wd, height=0.26, fill_color=BAR1, fill_opacity=1, stroke_width=0)
            r.move_to([-3.2 + wd / 2, y, 0])
            bars.add(r)
        question = lab_l("approval text tested?", -3.2, ys[2], 40)
        ticks = VGroup(check(-4.05, ys[0], s=0.22, color=INK, w=8), check(-4.05, ys[1], s=0.22, color=INK, w=8))
        mark = Dot([1.45, ys[2], 0], radius=0.14, color=TERRA)

        go(self, None, FadeIn(VGroup(boxes, bars)), FadeIn(question), rt=0.6)
        go(self, "Before launch", LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.4), rt=0.8)
        go(self, "drops or changes", FadeIn(mark, scale=0.5), rt=0.4)
        hold(self)


class B06_Landscape(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · drawn to explain"))
        A, Rp, G = Iso(-4.6, 1.1, 0.6), Iso(-4.6, -2.0, 0.6), Iso(3.4, -1.3, 1.1)
        ap2 = VGroup(*on_base(A, 0, 0, 0, 1.1, 1.1, 1.0, pad=0.15, base_h=0.2))
        repo = VGroup(*on_base(Rp, 0, 0, 0, 1.1, 1.1, 1.0, pad=0.15, base_h=0.2))
        g_base, g_box = on_base(G, 0, 0, 0, 1.6, 1.6, 1.4)
        gist = VGroup(g_base, g_box, G.tape(0, 0, 1.65, 1.6, 1.6, drop=0.35))
        ap2_lab = VGroup(lab_l("Google AP2", -6.0, 0.5, 38), lab_l("Agent Payments Protocol", -6.0, -0.1, 32))
        repo_lab = VGroup(lab_l("Razorpay buildathon repo", -6.0, -2.55, 38), lab_l("Mandate Mirror", -6.0, -3.1, 32))
        gist_lab = lab("GistGap", 3.4, -2.0, 40)
        links = VGroup(arrow([-3.65, 1.85, 0], [1.45, 0.85, 0]), arrow([-3.65, -1.25, 0], [1.45, -0.15, 0]))

        go(self, "Google's AP2", FadeIn(ap2, shift=DOWN * 0.3), FadeIn(ap2_lab), rt=0.6)
        go(self, "a buildathon repo", FadeIn(repo, shift=DOWN * 0.3), FadeIn(repo_lab), rt=0.6)
        go(self, "neither tests the text", FadeIn(gist, shift=DOWN * 0.3), FadeIn(gist_lab), rt=0.6)
        go(self, "GistGap will", *[GrowArrow(a) for a in links], rt=0.6)
        hold(self)


class B07_Examples(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · mock-up, not built"))
        xs = (-4.1, 0.0, 4.1)
        cards, lines = VGroup(), VGroup()
        for x in xs:
            cards.add(RoundedRectangle(width=2.9, height=3.2, corner_radius=0.15, fill_color=CARD, fill_opacity=1,
                                       stroke_color=INK, stroke_width=4).move_to([x, 0.35, 0]))
            for wd, y in ((2.0, 1.4), (1.4, 1.0)):
                r = Rectangle(width=wd, height=0.2, fill_color=BAR1, fill_opacity=1, stroke_width=0)
                r.move_to([x - 1.1 + wd / 2, y, 0])
                lines.add(r)
        names = VGroup(lab("clean", xs[0], -1.75), lab("hidden cap", xs[1], -1.75), lab("changed amount", xs[2], -1.75))
        marks = VGroup(check(xs[0] - 0.3, -0.2, s=0.42, color=INK, w=10),
                       cross(xs[1], -0.2, s=0.42, w=10), cross(xs[2], -0.2, s=0.42, w=10))
        tap = cursor(0.55, -0.45, 0.5)

        go(self, None, FadeIn(VGroup(cards, lines)), FadeIn(names), rt=0.6)
        go(self, "they will click", FadeIn(tap, shift=LEFT * 0.4), rt=0.4)
        go(self, "three constructed examples", LaggedStart(*[Create(m) for m in marks], lag_ratio=0.35), rt=1.0)
        hold(self)


class B08_Skills(Scene):
    def construct(self):
        self.add(tag("WILL EXIST · not built yet"))
        P = Iso(-4.85, 0.75, 0.85)
        contract = VGroup(P.box(-0.15, -0.15, -0.25, 1.4, 1.7, 0.25, DARK_TOP, DARK_L, DARK_R), P.page(0, 0, 0, 1.1, 1.4))
        frame = Square(side_length=1.3, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([1.5, 1.2, 0])
        verify = VGroup(frame, check(1.45, 1.2, s=0.32, color=INK, w=9))
        evaluate = VGroup(*[Rectangle(width=0.36, height=h, fill_color=c, fill_opacity=1, stroke_width=0)
                            .move_to([x, -2.0 + h / 2, 0])
                            for x, h, c in ((-5.35, 0.8, BAR1), (-4.87, 1.3, BAR1), (-4.39, 1.0, BAR2))])
        src = Rectangle(width=0.9, height=1.1, fill_color="#FFFFFF", fill_opacity=1, stroke_color=INK,
                        stroke_width=4).move_to([0.35, -1.4, 0])
        field = Square(side_length=0.55, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([1.45, -1.4, 0])
        link = Line([0.9, -1.4, 0], [1.08, -1.4, 0], color=DEEP_KRAFT, stroke_width=7)
        ground = VGroup(src, link, field)
        names = (lab_l("prompt contracts", -3.55, 1.2, 40), lab_l("verification", 2.6, 1.2, 40),
                 lab_l("evaluation", -3.55, -1.4, 40), lab_l("source grounding", 2.05, -1.4, 40))

        go(self, "prompt contracts", FadeIn(contract), FadeIn(names[0]), rt=0.4)
        go(self, "verification", FadeIn(verify), FadeIn(names[1]), rt=0.4)
        go(self, "evaluation", LaggedStart(*[GrowFromEdge(b, DOWN) for b in evaluate], lag_ratio=0.2), FadeIn(names[2]), rt=0.5)
        go(self, "source grounding", FadeIn(ground), FadeIn(names[3]), rt=0.4)
        hold(self)


class B09_Fields(Scene):
    def construct(self):
        self.add(tag("WILL EXIST · not built yet"))
        xs = (-4.8, -2.4, 0.0, 2.4, 4.8)
        words = ("amount", "merchant", "cap", "expiry", "recurring")
        cues = ("Amount", "merchant", "spending cap", "expiry date", "recurring")
        bases, boxes = VGroup(), []
        for x in xs:
            I = Iso(x, -0.9, 0.7)
            base, box = on_base(I, 0, 0, 0, 1.2, 1.2, 1.1, pad=0.15, base_h=0.22)
            bases.add(base)
            boxes.append(box)
        self.add(bases)
        for x, word, cue, box in zip(xs, words, cues, boxes):
            go(self, cue, FadeIn(box, shift=DOWN * 0.8), FadeIn(lab(word, x, -1.5, 36)), rt=0.4)
        hold(self)


class B10_ScopeTest(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · planned test, no results yet"))
        items = ("real signing", "real payments", "protocol compliance", "original request")
        ys = (1.5, 0.5, -0.5, -1.5)
        texts = VGroup(*[lab_l(s, -5.1, y, 36) for s, y in zip(items, ys)])
        xs_marks = VGroup(*[cross(-5.6, y, s=0.18, w=7) for y in ys])
        pos = [(0.9 + i * 1.1, y) for y in (0.75, -0.75) for i in range(5)]
        dots = VGroup(*[Dot([x, y, 0], radius=0.3, color=INK) for x, y in pos])
        planted = (1, 5, 8)
        reds = VGroup(*[Dot([pos[i][0], pos[i][1], 0], radius=0.3, color=TERRA) for i in planted])
        rings = VGroup(*[Circle(radius=0.46, color=INK, stroke_width=6).move_to([pos[i][0], pos[i][1], 0]) for i in planted])
        count = lab("ten mandates", 3.1, -1.8, 36)

        go(self, None, FadeIn(texts), rt=0.5)
        go(self, None, LaggedStart(*[Create(m) for m in xs_marks], lag_ratio=0.25), rt=0.8)
        go(self, "ten constructed mandates", FadeIn(dots), FadeIn(count), rt=0.5)
        go(self, "three with planted errors", FadeIn(reds), rt=0.4)
        go(self, "flags exactly those three", LaggedStart(*[Create(r) for r in rings], lag_ratio=0.3), rt=0.8)
        hold(self)


class B11_Shrink(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · drawn to explain"))
        S = Iso(-2.0, -2.05, 1.0)
        base, box = on_base(S, 0, 0, 0, 2.2, 2.2, 2.0)
        z0, z1 = 0.25, 2.25
        outline = Polygon(S.p(0, 0, z0), S.p(2.2, 0, z0), S.p(2.2, 0, z1), S.p(2.2, 2.2, z1), S.p(0, 2.2, z1), S.p(0, 2.2, z0),
                          stroke_color=DIM, stroke_width=4, fill_opacity=0)
        question = lab("smaller problem?", 3.6, 0.6, 44)

        go(self, None, FadeIn(VGroup(base, box)), rt=0.5)
        go(self, "smaller than I think", FadeIn(outline), VGroup(base, box).animate.scale(0.55, about_point=S.p(0, 0, z0)), rt=1.0)
        go(self, None, FadeIn(question), rt=0.4)
        hold(self)


class B12_GitLog(Scene):
    def construct(self):
        self.add(tag("REDRAWN from my git log, Oct 9"))
        # Oldest to newest, left to right; names paraphrase the commit subjects.
        nodes = ((-4.5, "1 · environment", "fe9c16c"), (-1.5, "2 · evidence", "2a1f40f"),
                 (1.5, "3 · video built", "2eb73eb"), (4.5, "close-out", "1a6aa5b"))
        y = 0.0
        line = Line([-4.5, y, 0], [4.5, y, 0], color=INK, stroke_width=5)
        stops = [(Dot([x, y, 0], radius=0.18, color=TERRA), lab(name, x, y + 0.75, 36), lab(sha, x, y - 0.65, 32))
                 for x, name, sha in nodes]

        go(self, None, Create(line), rt=0.8)
        go(self, "the commit trail", *[FadeIn(m) for m in stops[0]], rt=0.4)
        for stop in stops[1:]:
            self.wait(0.25)
            go(self, None, *[FadeIn(m) for m in stop], rt=0.4)
        hold(self)


class B13_Columns(Scene):
    def construct(self):
        heads = VGroup(T("EXISTS TODAY", 42, bold=True).move_to([-3.2, 2.3, 0]),
                       T("WILL EXIST", 42, bold=True).move_to([3.2, 2.3, 0]))
        now = (("the brief", "the brief"), ("the beat sheet", "the beat sheet"), ("this film", "this film"))
        later = (("the generator", "the generator"), ("the checker", "the checker"), ("the test set", "the test set"),
                 ("the demo page", "the demo page"), ("the results table", "the results table"))
        ys = (1.3, 0.45, -0.4, -1.25, -2.1)

        go(self, None, FadeIn(heads), rt=0.5)
        for (text, cue), y in zip(now, ys):
            dot = Square(side_length=0.26, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([-5.2, y, 0])
            go(self, cue, FadeIn(dot), FadeIn(lab_l(text, -4.8, y, 38)), rt=0.3)
        for (text, cue), y in zip(later, ys):
            box = Square(side_length=0.26, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([1.0, y, 0])
            go(self, cue, FadeIn(box), FadeIn(lab_l(text, 1.4, y, 38)), rt=0.3)
        hold(self)


class B14_Title(Scene):
    def construct(self):
        # A drawn title (replaces the masked ShowTellCard, whose clip left the "p" descender hollow).
        # Unlabelled, like the card it replaces. All motion ends by ~0.70 s, before the 50% sample.
        title = T("GistGap", 170, bold=True).move_to([0, 0.9, 0])
        rule = Line([-3.5, -0.6, 0], [3.5, -0.6, 0], color=INK, stroke_width=5)
        spark = Dot([3.5, -0.6, 0], radius=0.1, color=TERRA)
        tagline = T("What you see is what you sign", 48).move_to([0, -1.4, 0])

        go(self, None, FadeIn(title, shift=UP * 0.2), rt=0.35)
        go(self, None, Create(rule), FadeIn(spark), FadeIn(tagline), rt=0.35)
        hold(self)
