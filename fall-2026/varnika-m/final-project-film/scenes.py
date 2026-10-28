"""scenes.py — Terraform Docs, Quoted (Varnika M, INFO 7375 final project pitch).

Show-tell style: one drawn picture per beat, few labels, the narration explains.
The kit block below is pasted from brutalist.art skills/make/show-tell/templates/iso_kit.py
(b21f625), trimmed to the parts this film uses; Gate A copies only this file.
"""
from manim import *
import numpy as np
import json as _json, os as _os

# ═════════════════════════════ ISO KIT (show-tell, trimmed) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"
KRAFT_DEEP = "#9C8462"
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=40, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


class Iso:
    def __init__(self, ox=0.0, oy=0.0, s=1.0):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return np.array([self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s + z * self.s, 0.0])

    def quad(self, pts, fill, stroke=INK, sw=4):
        return Polygon(*[self.p(*q) for q in pts], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)

    def box(self, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, stroke=INK, sw=4):
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, stroke, sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, stroke, sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, stroke, sw))

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


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


def cursor(x, y, s=0.45):
    return Polygon([x, y, 0], [x, y - s, 0], [x + s * 0.28, y - s * 0.72, 0], [x + s * 0.62, y - s * 0.66, 0],
                   fill_color=INK, fill_opacity=1, stroke_color=CARD, stroke_width=2)


# ═════════════════════════════ pacing (narration is the clock) ═════════════════════════════
try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json")))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
    _NARR = {b["beat_id"]: b["narration_text"] for b in _SHEET["beats"]}
except Exception:
    _TARGET, _NARR = {}, {}


def _bid(self):
    return type(self).__name__.split("_")[0]


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def until(self, phrase, lead=0.25):
    n, target = _NARR.get(_bid(self), ""), _TARGET.get(_bid(self), 0)
    if not n or not target or phrase not in n:
        return
    gap = target * n.index(phrase) / len(n) - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def finish(self):
    target = _TARGET.get(_bid(self), 0)
    if not target:
        self.wait(2.0)
        return
    rem = target - _elapsed(self) - 0.1     # stay under the audio: compile.py centre-cuts long clips
    if rem > 0.05:
        self.wait(rem)


def G(self, *anims, rt=0.7):
    """Play, but never across the clip midpoint (GATE T and Gate V sample there)."""
    mid = _TARGET.get(_bid(self), 10) / 2
    now = _elapsed(self)
    if now < mid + 0.3 and now + rt > mid - 0.3:
        self.wait(max(0.01, mid + 0.32 - now))
    self.play(*anims, run_time=rt)


# ═════════════════════════════ this film's cast ═════════════════════════════
def ctag():
    """On-screen honesty label for drawings of things that do not exist yet."""
    return T("planned · constructed", 32).move_to([4.25, -3.05, 0])


def flat_page(x, y, w=3.0, h=3.8, n=6, inset=0.4):
    """The docs page: white sheet, ink outline, kraft shadow, ghost text lines. `.ly` holds line heights."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.14, y - 0.14, 0])
    sheet = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    top, bot = y + h / 2 - 0.55, y - h / 2 + 0.5
    ly = [top - i * (top - bot) / max(1, n - 1) for i in range(n)]
    lines = VGroup(*[Line([x - w / 2 + inset, yy, 0], [x + w / 2 - inset - (0.5 if i % 3 == 2 else 0), yy, 0],
                          color=GHOST, stroke_width=10) for i, yy in enumerate(ly)])
    g = VGroup(shadow, sheet, lines)
    g.ly, g.x0, g.x1 = ly, x - w / 2 + inset, x + w / 2 - inset
    return g


def hl(page, i):
    """Highlight line i of a flat_page: an ink line over it and a terracotta dot at its start."""
    yy = page.ly[i]
    return (Line([page.x0, yy, 0], [page.x1, yy, 0], color=INK, stroke_width=10),
            Dot([page.x0 - 0.22, yy, 0], radius=0.09, color=TERRA))


def qcard(x, y, w=1.3, h=1.0):
    """The question card: a kraft card with two ghost lines."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_R, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
    card = Rectangle(width=w, height=h, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    l1 = Line([x - w / 2 + 0.22, y + 0.15, 0], [x + w / 2 - 0.22, y + 0.15, 0], color=KRAFT_DEEP, stroke_width=8)
    l2 = Line([x - w / 2 + 0.22, y - 0.15, 0], [x + 0.05, y - 0.15, 0], color=KRAFT_DEEP, stroke_width=8)
    return VGroup(shadow, card, l1, l2)


def kcard(x, y, w=1.2, h=1.5, fill=BOX_TOP, stroke=INK):
    shadow = Rectangle(width=w, height=h, fill_color=BOX_R, fill_opacity=1, stroke_width=0).move_to([x + 0.1, y - 0.1, 0])
    card = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=4).move_to([x, y, 0])
    return VGroup(shadow, card)


def outline_card(x, y, w=1.2, h=1.5):
    """A 'will exist' placeholder: empty outline in deep kraft."""
    return Rectangle(width=w, height=h, stroke_color=KRAFT_DEEP, stroke_width=5, fill_opacity=0).move_to([x, y, 0])


def shelf(x, y, w):
    return Rectangle(width=w, height=0.3, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])


def gate(x, y, h=2.0, w=1.6):
    """A conveyor gate: two kraft posts and a lintel."""
    lp = Rectangle(width=0.28, height=h, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x - w / 2, y + h / 2, 0])
    rp = Rectangle(width=0.28, height=h, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x + w / 2, y + h / 2, 0])
    top = Rectangle(width=w + 0.28, height=0.3, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + h + 0.15, 0])
    return VGroup(lp, rp, top)


def tray(x, y, w=2.6, h=0.9):
    """A flat open tray: kraft base and a front lip."""
    base = Rectangle(width=w, height=h, fill_color=BOX_IN1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    lip = Rectangle(width=w, height=0.35, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y - h / 2 + 0.17, 0])
    base.set_z_index(0); lip.set_z_index(3)
    return base, lip


# ═════════════════════════════ scenes ═════════════════════════════
class B01_Ask(Scene):
    def construct(self):
        page = flat_page(2.2, 0.2, 3.4, 4.4, n=7)
        card = VGroup(qcard(-4.6, 0.6), T("question").move_to([-4.6, -0.45, 0]))
        self.add(page, card, T("docs").move_to([2.2, 2.85, 0]), ctag())
        self.wait(0.3)
        G(self, card.animate.shift(RIGHT * 2.6 + UP * 0.6), rt=0.9)
        until(self, "proves")
        line, dot = hl(page, 2)
        G(self, Create(line), FadeIn(dot), rt=0.6)
        ck = check(4.6, page.ly[2] + 0.05, s=0.26)
        G(self, Create(ck), FadeIn(T("proof").move_to([5.3, page.ly[2] - 0.75, 0])), rt=0.6)
        finish(self)


class B02_Repo(Scene):
    def construct(self):
        iso = Iso(ox=0.3, oy=-1.6, s=1.0)
        back, front = iso.open_box(-1.6, -1.6, 0, 3.2, 3.2, 1.0)
        self.add(back, front, T("GitHub repo").move_to([-4.4, -1.6, 0]), ctag())
        cells = [("Python command-line tool", (0.55, 0.55), ("#C4CAD1", "#A3AAB2", "#868D96")),
                 ("saved copy", (-1.15, 0.55), (PAGE_TOP, PAGE_L, PAGE_R)),
                 ("test suite", (0.55, -1.15), (BOX_TOP, BOX_L, BOX_R)),
                 ("evaluation log", (-1.15, -1.15), (BAR3, BAR2, BAR1))]
        for phrase, (x0, y0), (t, l, r) in cells:
            until(self, phrase)
            part = iso.box(x0, y0, 0, 0.9, 0.9, 0.55, t, l, r, stroke=KRAFT_DEEP, sw=3)
            part.set_z_index(1)
            G(self, FadeIn(part, shift=DOWN * 1.2), rt=0.55)
        finish(self)


class B03_Optional(Scene):
    def construct(self):
        page = flat_page(-2.8, 0.3, 3.6, 4.6, n=7)
        req = T("Required?", 48).move_to([3.0, 1.2, 0])
        self.add(page, req, T("AWS provider v6.68.0 docs · line 54", 32).move_to([0, -2.95, 0]))
        until(self, "required")
        line, dot = hl(page, 3)
        G(self, Create(line), FadeIn(dot), rt=0.6)
        until(self, "optional")
        G(self, FadeOut(req), rt=0.35)
        opt = T("Optional", 52).move_to([3.0, 1.2, 0])
        G(self, FadeIn(opt), Create(check(4.7, 1.25, s=0.24)), rt=0.6)
        finish(self)


class B04_Deprecated(Scene):
    def construct(self):
        page = flat_page(-3.2, 0.3, 3.6, 4.6, n=7)
        self.add(page, T("AWS provider v6.68.0 docs · line 70", 32).move_to([0, -2.95, 0]))
        self.wait(0.3)
        line, dot = hl(page, 4)
        G(self, Create(line), FadeIn(dot), rt=0.6)
        G(self, FadeIn(T("Deprecated", 48).move_to([0.9, page.ly[4] + 0.75, 0])), rt=0.5)
        until(self, "separate resource")
        small = flat_page(4.4, -0.4, 2.0, 2.4, n=3, inset=0.3)
        arrow = Arrow([0.0, page.ly[4] - 0.3, 0], [3.1, -0.4, 0], color=DIM, stroke_width=6, buff=0.1)
        G(self, Create(arrow), FadeIn(small), rt=0.7)
        until(self, "which docs")
        G(self, FadeIn(T("v6.68.0", 40).move_to([-3.2, 3.05, 0])), rt=0.5)
        finish(self)


class B05_Conveyor(Scene):
    def construct(self):
        belt = RoundedRectangle(width=12.0, height=0.7, corner_radius=0.35, fill_color="#E2DCD0", fill_opacity=1,
                                stroke_color=KRAFT_DEEP, stroke_width=4).move_to([0, -1.2, 0])
        xs = [-3.2, 0.4, 4.0]
        gates = VGroup(*[gate(x, -0.85) for x in xs])
        labels = VGroup(*[T(s).move_to([x, -2.3, 0]) for s, x in zip(("find", "answer", "check"), xs)])
        card = qcard(-5.4, -0.25, w=1.1, h=0.85)
        self.add(belt, gates, labels, card, ctag())
        for phrase, x in (("Find", xs[0]), ("Ask Claude", xs[1])):
            until(self, phrase)
            G(self, card.animate.move_to([x, -0.25, 0]), rt=0.8)
        until(self, "my code checks")
        G(self, card.animate.move_to([xs[2], -0.25, 0]), rt=0.8)
        scan = Line([xs[2] - 0.6, 0.6, 0], [xs[2] + 0.6, 0.6, 0], color=TERRA, stroke_width=6)
        G(self, FadeIn(scan), rt=0.2)
        G(self, scan.animate.move_to([xs[2], -0.75, 0]), rt=0.6)
        G(self, FadeOut(scan), Create(check(xs[2] + 1.35, 1.6, s=0.24)), rt=0.5)
        finish(self)


class B06_NotFound(Scene):
    def construct(self):
        page = flat_page(3.0, 0.5, 3.4, 4.2, n=6)
        base, lip = tray(-3.6, -1.9, w=3.0, h=1.0)
        card = qcard(-3.6, 1.6)
        self.add(page, base, lip, card, T("not in the docs").move_to([-3.6, -3.0, 0]), ctag())
        G(self, card.animate.move_to([0.4, 1.6, 0]), rt=0.7)
        scan = Line([1.5, 2.2, 0], [4.5, 2.2, 0], color=TERRA, stroke_width=6)
        G(self, FadeIn(scan), rt=0.2)
        G(self, scan.animate.move_to([3.0, -1.2, 0]), rt=0.9)
        G(self, FadeOut(scan), rt=0.2)
        until(self, "That counts")
        card.set_z_index(1)
        G(self, card.animate.move_to([-3.6, -1.75, 0]), rt=0.8)
        G(self, Create(check(-1.5, -1.2, s=0.26)), rt=0.5)
        finish(self)


class B07A_Registry(Scene):
    def construct(self):
        page = flat_page(-0.6, 0.35, 4.0, 5.0, n=9)
        menu = VGroup(*[Rectangle(width=1.4, height=0.28, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                        .move_to([-4.6, 2.0 - i * 0.62, 0]) for i in range(6)])
        find = RoundedRectangle(width=2.6, height=0.8, corner_radius=0.2, fill_color=CARD, fill_opacity=1,
                                stroke_color=KRAFT_DEEP, stroke_width=4).move_to([4.3, 2.2, 0])
        self.add(page, menu, find, T("bucket", 40).move_to([4.0, 2.2, 0]),
                 T("redrawn from my screenshot · 2026-10-11", 32).move_to([0, -3.05, 0]))
        until(self, "page menu")
        bar = Rectangle(width=1.4, height=0.28, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(menu[3].get_center())
        G(self, FadeIn(bar), Create(check(-3.5, 0.2, s=0.2)), rt=0.6)
        until(self, "searching")
        mark = Dot([1.75, page.ly[0], 0], radius=0.1, color=TERRA)
        G(self, FadeIn(mark), rt=0.3)
        for i in (2, 4, 6):
            G(self, mark.animate.move_to([1.75, page.ly[i], 0]), rt=0.35)
        until(self, "two hundred")
        G(self, FadeIn(T("70 / 220", 48).move_to([4.3, 1.1, 0])), rt=0.5)
        until(self, "number seventy")
        line, _ = hl(page, 7)
        G(self, mark.animate.move_to([1.75, page.ly[7], 0]), Create(line), rt=0.6)
        finish(self)


class B07B_Chat(Scene):
    def construct(self):
        reply = Rectangle(width=4.6, height=3.6, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-3.0, 0.4, 0])
        ys = [1.55, 0.75, -0.05, -0.85]
        rl = VGroup(*[Line([-4.9, yy, 0], [-1.1 - (0.6 if i == 3 else 0), yy, 0], color=GHOST, stroke_width=10) for i, yy in enumerate(ys)])
        self.add(reply, rl, T("Claude reply").move_to([-3.0, -1.95, 0]),
                 T("redrawn from my screenshot · claude.ai, Sonnet 5.5 · 2026-10-11", 32).move_to([0, -3.05, 0]))
        until(self, "optional")
        G(self, Create(Line([-4.9, ys[0], 0], [-1.1, ys[0], 0], color=INK, stroke_width=10)),
          Create(check(-0.55, ys[0], s=0.2)), rt=0.6)
        until(self, "added two details")
        G(self, FadeIn(T("not on page", 40).move_to([1.05, 0.35, 0])),
          FadeIn(Line([-0.75, ys[1], 0], [-0.75, ys[2], 0], color=DIM, stroke_width=6)), rt=0.6)
        until(self, "My tool")
        ans = flat_page(4.2, 0.9, 2.8, 2.6, n=3, inset=0.35)
        G(self, FadeIn(ans, shift=LEFT * 1.5), rt=0.7)
        line, dot = hl(ans, 1)
        G(self, Create(line), FadeIn(dot), FadeIn(T("planned · constructed", 32).move_to([4.2, -0.75, 0])), rt=0.6)
        finish(self)


class B08_FirstMinute(Scene):
    def construct(self):
        term = Rectangle(width=4.4, height=2.6, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-3.1, 0.6, 0])
        plinths = VGroup(Rectangle(width=4.8, height=0.32, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([-3.1, -0.86, 0]),
                         Rectangle(width=3.6, height=0.32, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([2.0, -1.06, 0]))
        prompt = T(">", 48).move_to([-4.9, 1.35, 0])
        base, lip = tray(2.0, -0.4, w=3.2, h=1.0)
        cells = VGroup(*[Rectangle(width=0.6, height=0.6, fill_color=BOX_TOP, fill_opacity=1, stroke_color=KRAFT_DEEP,
                                   stroke_width=3).move_to([1.0 + i * 1.0, -0.25, 0]) for i in range(3)])
        cells.set_z_index(1)
        dial = Circle(radius=0.75, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([5.0, 2.0, 0])
        hand = Line([5.0, 2.0, 0], [5.0, 2.6, 0], color=INK, stroke_width=6)
        self.add(plinths, term, prompt, base, lip, cells, dial, hand,
                 T("one command").move_to([-3.1, -1.55, 0]), T("tests").move_to([2.0, -1.75, 0]),
                 ctag())
        self.wait(0.3)
        G(self, Rotate(hand, angle=-PI / 2, about_point=np.array([5.0, 2.0, 0])), rt=1.2)
        until(self, "run one command")
        out = Line([-4.5, 0.45, 0], [-1.6, 0.45, 0], color=INK, stroke_width=10)
        G(self, Create(out), rt=0.6)
        until(self, "quoted line")
        G(self, FadeIn(Dot([-4.75, 0.45, 0], radius=0.09, color=TERRA)), rt=0.3)
        until(self, "run the tests")
        G(self, *[Create(check(1.0 + i * 1.0, -0.2, s=0.16)) for i in range(3)],
          Rotate(hand, angle=-PI, about_point=np.array([5.0, 2.0, 0])), rt=0.8)
        finish(self)


class B09_Proves(Scene):
    def construct(self):
        sh = shelf(0, -1.0, 10.2)
        self.add(sh, ctag())
        xs = [-3.9, -1.3, 1.3, 3.9]
        cues = [("prompt contract", "contract"), ("source grounding", "grounding"),
                ("verification", "verify"), ("evaluation", "evaluate")]
        for x, (phrase, word) in zip(xs, cues):
            until(self, phrase)
            b = kcard(x, 0.0, w=1.2, h=1.7)
            spine = Dot([x, 0.55, 0], radius=0.09, color=TERRA)
            grp = VGroup(b, spine)
            G(self, FadeIn(grp, shift=DOWN * 1.0), FadeIn(T(word).move_to([x, -1.75, 0])), rt=0.6)
        until(self, "It won't prove")
        fence = Rectangle(width=10.8, height=2.75, stroke_color=KRAFT_DEEP, stroke_width=5,
                          fill_opacity=0).move_to([0, 0.05, 0])
        G(self, Create(fence), rt=0.9)
        G(self, FadeIn(T("tested questions only", 40).move_to([0, 2.1, 0])), rt=0.5)
        finish(self)


class B10_Scope(Scene):
    def construct(self):
        fence = Rectangle(width=3.4, height=4.2, stroke_color=KRAFT_DEEP, stroke_width=5, fill_opacity=0).move_to([-4.3, 0.2, 0])
        run = RoundedRectangle(width=1.9, height=1.0, corner_radius=0.3, fill_color=BAR2, fill_opacity=1,
                               stroke_color=INK, stroke_width=4).move_to([0.0, 0.6, 0])
        tri = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(0.22).rotate(-PI / 2).move_to([0.0, 0.6, 0])
        self.add(fence, run, tri, T("in").move_to([-4.3, 2.75, 0]), T("out").move_to([0.0, 2.0, 0]), ctag())
        until(self, "ten AWS")
        pages = VGroup(*[Rectangle(width=2.4, height=0.18, fill_color=PAGE_TOP if i % 2 else PAGE_L, fill_opacity=1,
                                   stroke_color=KRAFT_DEEP, stroke_width=2).move_to([-4.3, -1.4 + i * 0.26, 0]) for i in range(10)])
        G(self, LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in pages], lag_ratio=0.12), rt=1.2)
        until(self, "will not write")
        cross = VGroup(Line([-1.1, -0.1, 0], [1.1, 1.3, 0], color=INK, stroke_width=7),
                       Line([-1.1, 1.3, 0], [1.1, -0.1, 0], color=INK, stroke_width=7))
        G(self, Create(cross), rt=0.5)
        until(self, "The first piece")
        chk = kcard(4.0, 1.1, w=1.8, h=1.3)
        G(self, FadeIn(chk), FadeIn(T("first").move_to([4.0, 2.3, 0])), rt=0.6)
        G(self, FadeIn(Dot([4.5, 1.35, 0], radius=0.1, color=TERRA)), rt=0.3)
        until(self, "made-up quote")
        base, lip = tray(4.0, -1.9, w=2.4, h=0.9)
        G(self, FadeIn(base), FadeIn(lip), rt=0.4)
        fake = qcard(2.3, -0.4, w=1.0, h=0.75)
        fake.set_z_index(1)
        G(self, FadeIn(fake), rt=0.3)
        G(self, fake.animate.move_to([4.0, -1.75, 0]), rt=0.6)
        finish(self)


class B11_Risk(Scene):
    def construct(self):
        page = flat_page(0.6, 0.15, 3.8, 5.6, n=9)
        self.add(page, T("AWS provider v6.68.0 docs · lines 54 and 221", 32).move_to([0, -3.05, 0]))
        until(self, "optional at the top")
        a, da = hl(page, 1)
        G(self, Create(a), FadeIn(da), FadeIn(T("line 54 · Optional", 40).move_to([-4.0, page.ly[1], 0])), rt=0.6)
        until(self, "required inside")
        b, db = hl(page, 7)
        G(self, Create(b), FadeIn(db), FadeIn(T("line 221 · Required", 40).move_to([-4.0, page.ly[7], 0])), rt=0.6)
        until(self, "could pick")
        cur = cursor(3.4, 2.0)
        G(self, FadeIn(cur), rt=0.3)
        G(self, cur.animate.move_to([3.5, page.ly[7] - 0.15, 0]), rt=0.8)
        until(self, "track which section")
        div = Line([-1.6, (page.ly[3] + page.ly[4]) / 2, 0], [2.8, (page.ly[3] + page.ly[4]) / 2, 0], color=BAR1, stroke_width=14)
        G(self, Create(div), rt=0.6)
        until(self, "this exact case")
        G(self, FadeIn(kcard(4.9, -1.2, w=1.1, h=1.2)), rt=0.4)
        G(self, Create(check(4.9, -1.2, s=0.2)), rt=0.4)
        finish(self)


class B12A_Have(Scene):
    def construct(self):
        sh = shelf(0, -1.0, 10.6)
        self.add(sh, T("already have", 44).move_to([0, 2.7, 0]))
        until(self, "Python and Terraform")
        c1 = kcard(-3.6, 0.0, w=1.5, h=1.6, fill=BAR2, stroke=INK)
        c2 = flat_page(0.0, 0.0, 1.5, 1.6, n=3, inset=0.25)
        G(self, FadeIn(c1, shift=DOWN * 0.9), FadeIn(c2, shift=DOWN * 0.9),
          FadeIn(T("Python").move_to([-3.6, -1.75, 0])), FadeIn(T("Terraform").move_to([0.0, -1.75, 0])), rt=0.6)
        until(self, "small, tested")
        c3 = kcard(3.6, 0.0, w=1.8, h=1.6)
        G(self, FadeIn(c3), rt=0.4)
        G(self, *[Create(check(3.1 + i * 0.5, 0.0, s=0.13, w=5)) for i in range(3)], rt=0.5)
        until(self, "twenty-two")
        G(self, FadeIn(T("PR #21 · 22 tests").move_to([3.6, -1.75, 0])), rt=0.5)
        finish(self)


class B12B_New(Scene):
    def construct(self):
        sh = shelf(0, -1.4, 9.0)
        self.add(sh, T("new to me", 44).move_to([0, 2.7, 0]))
        page = flat_page(-2.2, 0.35, 2.0, 3.2, n=6, inset=0.3)
        G(self, FadeIn(page), rt=0.5)
        line, dot = hl(page, 3)
        G(self, Create(line), FadeIn(dot), rt=0.5)
        until(self, "building a test set")
        sheet = kcard(2.2, 0.0, w=2.0, h=2.4, fill=CARD)
        G(self, FadeIn(sheet), rt=0.4)
        G(self, *[Create(check(1.9, 0.7 - i * 0.6, s=0.14, w=5)) for i in range(3)], rt=0.5)
        finish(self)


class B13_Ledger(Scene):
    def construct(self):
        s1, s2 = shelf(-3.4, -1.2, 5.6), shelf(3.4, -1.2, 5.6)
        self.add(s1, s2, T("today").move_to([-3.4, -1.95, 0]), T("will exist").move_to([3.4, -1.95, 0]))
        until(self, "licence check")
        G(self, FadeIn(kcard(-5.2, -0.45, w=0.9, h=1.2)), rt=0.4)
        until(self, "one saved docs page")
        G(self, FadeIn(flat_page(-3.9, -0.1, 1.2, 1.9, n=3, inset=0.2)), rt=0.4)
        until(self, "my two tests")
        G(self, FadeIn(kcard(-2.4, -0.45, w=0.9, h=1.2, fill=CARD)), FadeIn(kcard(-1.3, -0.45, w=0.9, h=1.2, fill=CARD)), rt=0.5)
        until(self, "The tool itself")
        outs = VGroup(*[outline_card(x, -0.3, w=1.0, h=1.5) for x in (1.6, 2.8, 4.0, 5.2)])
        G(self, LaggedStart(*[Create(o) for o in outs], lag_ratio=0.2), rt=0.8)
        finish(self)


class BOUT_Title(Scene):
    def construct(self):
        page = flat_page(-4.9, 0.1, 1.6, 2.1, n=3, inset=0.25)
        self.add(page, T("Terraform Docs, Quoted", 72).move_to([0.9, 0.55, 0]), T("Varnika M", 48).move_to([0.9, -0.6, 0]))
        self.wait(0.3)
        G(self, Create(check(-4.0, -1.35, s=0.24)), rt=0.5)
        finish(self)
