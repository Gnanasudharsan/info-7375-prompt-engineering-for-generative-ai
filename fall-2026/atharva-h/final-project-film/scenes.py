"""scenes.py — Manim scenes for atharva-sponsorsql-pitch (INFO 7375 final project pitch).

A pitch, not a build: every drawing shows something that WILL exist, except the
two real things (the project brief and the DOL data page). Mock-ups and invented
examples carry a CONSTRUCTED label on screen. No numbers are invented: the only
figures are the planned "10 questions" and the constructed 1-vs-3 count in B08,
which is labelled CONSTRUCTED.

Column names in B02 and B08 are copied from the header row of
LCA_Disclosure_Data_FY2026_Q3.xlsx (U.S. DOL OFLC, downloaded 2026-10-24).

Pacing: each scene reads its measured narration length and text from
beat_sheet.json and lands events on spoken phrases (share of characters x
duration). If the sheet is unreadable (Gate A runs on an isolated copy), it
falls back to the durations measured on 2026-10-14.

No LaTeX. Palette: cream ground, warm ink, one terracotta accent per scene.
"""
import json
import os

import numpy as np
from manim import *

# ── Palette ──────────────────────────────────────────────────────────────────
BG    = ManimColor("#FAF9F5")
INK   = ManimColor("#3D3929")
ACC   = ManimColor("#D97757")
SOFT  = ManimColor("#6B6858")
GHOST = ManimColor("#C9C4B4")
CARD  = ManimColor("#FFFFFF")
KRAFT = ManimColor("#F3E9D8")

# ── Pacing from the beat sheet ───────────────────────────────────────────────
_SHEET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "beat_sheet.json")
_FALLBACK = {"B02": 17.47, "B03": 15.00, "B04": 19.26, "B05": 14.42, "B06": 16.11,
             "B07": 17.43, "B08": 18.15, "B09": 17.64, "B10": 15.81, "B12": 7.74}


def _beat(bid):
    try:
        with open(_SHEET) as f:
            for b in json.load(f)["beats"]:
                if b["beat_id"] == bid:
                    return b
    except Exception:
        pass
    return None


class Pacer:
    """Tracks elapsed time; waits until a spoken phrase, then pads to the audio length."""

    def __init__(self, scene, bid):
        scene.camera.background_color = BG
        self.s, self.bid = scene, bid
        b = _beat(bid)
        self.D = float((b or {}).get("actual_duration_s") or _FALLBACK[bid])
        self.text = (b or {}).get("narration_text", "")
        self.t = 0.0

    def until(self, phrase, fallback):
        i = self.text.find(phrase) if self.text else -1
        f = i / len(self.text) if i >= 0 else fallback
        target = min(f * self.D, self.D - 0.5)
        if target > self.t + 0.05:
            self.s.wait(target - self.t)
            self.t = target

    def play(self, *anims, run_time=0.8):
        self.s.play(*anims, run_time=run_time)
        self.t += run_time

    def finish(self):
        rest = self.D - self.t
        if rest > 0.05:
            self.s.wait(rest)
            self.t = self.D


# ── Drawing helpers ──────────────────────────────────────────────────────────
def T(text, size=32, color=None, weight=None):
    kw = {"font_size": size, "color": color or INK}
    if weight:
        kw["weight"] = weight
    return Text(text, **kw)


def M(text, size=24, color=None):
    return Text(text, font_size=size, color=color or INK, font="Menlo")


def keep_in(mob, xr=6.0, yr=3.15):
    """Shift a mobject so its whole box sits inside the safe area."""
    dx = min(0, xr - mob.get_right()[0]) + max(0, -xr - mob.get_left()[0])
    dy = min(0, yr - mob.get_top()[1]) + max(0, -yr - mob.get_bottom()[1])
    mob.shift(RIGHT * dx + UP * dy)
    return mob


def fit(mob, w):
    if mob.width > w:
        mob.scale_to_fit_width(w)
    return mob


def box(w, h, label=None, size=32, fill=CARD):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.14, color=INK,
                         stroke_width=4, fill_color=fill, fill_opacity=1)
    if label is None:
        return VGroup(r)
    return VGroup(r, fit(T(label, size), w - 0.3).move_to(r))


def page(w=1.3, h=1.6, lines=4, fill=CARD):
    r = Rectangle(width=w, height=h, color=INK, stroke_width=4, fill_color=fill, fill_opacity=1)
    ls = VGroup(*[Line(LEFT * (w / 2 - 0.2), RIGHT * (w / 2 - 0.2 - (0.25 if i % 2 else 0)),
                       color=GHOST, stroke_width=5).shift(UP * (h / 2 - 0.35 - i * 0.3))
                  for i in range(lines)])
    ls.move_to(r).align_to(r, UP).shift(DOWN * 0.3)
    return VGroup(r, ls)


def check_mark(c, s=0.35, color=ACC):
    return VMobject(color=color, stroke_width=9).set_points_as_corners(
        [c + np.array([-s, 0, 0]), c + np.array([-s * 0.3, -s * 0.7, 0]), c + np.array([s, s * 0.8, 0])])


def tag(text, size=28):
    t = T(text, size, weight="BOLD")
    p = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.35, corner_radius=0.2,
                         color=INK, stroke_width=3, fill_color=KRAFT, fill_opacity=1)
    return VGroup(p, t.move_to(p))


def constructed(text="CONSTRUCTED", note="mock-up · nothing here is real data"):
    g = VGroup(T(text, 26, SOFT, weight="BOLD"), T(note, 22, SOFT)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    return keep_in(g.to_corner(DL, buff=1.0))


def pipeline():
    """The recurring cast: question → SQL → answer → check. Used by B03 and B06."""
    xs = [-4.8, -1.6, 1.6, 4.8]
    names = ["question", "SQL", "answer", "check"]
    boxes = [box(2.6, 1.6, n, 38).move_to([x, 0.7, 0]) for n, x in zip(names, xs)]
    arrows = [Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.08, color=INK,
                    stroke_width=5, max_tip_length_to_length_ratio=0.25) for i in range(3)]
    return boxes, arrows


# ═════════════════════════════════════════════════════════════════════════════
class B02_TheSpreadsheet(Scene):
    def construct(self):
        p = Pacer(self, "B02")
        title = T("LCA disclosure file · FY2026 Q3", 40, weight="BOLD").to_edge(UP, buff=0.75).to_edge(LEFT, buff=1.0)
        src = T("Source: U.S. Department of Labor, OFLC · column names from the FY2026 Q3 file",
                22, SOFT).to_edge(DOWN, buff=0.7)
        fit(src, 11.0)
        p.play(FadeIn(title), FadeIn(src), run_time=0.8)

        widths = [2.4, 2.0, 2.4, 3.4]
        x0, top = -5.9, 1.9
        fields = ["EMPLOYER_NAME", "JOB_TITLE", "WORKSITE_CITY", "WAGE_RATE_OF_PAY_FROM"]
        header = VGroup()
        x = x0
        for w, f in zip(widths, fields):
            cell = Rectangle(width=w, height=0.6, color=INK, stroke_width=3, fill_color=KRAFT, fill_opacity=1)
            cell.move_to([x + w / 2, top, 0])
            header.add(VGroup(cell, fit(M(f, 22), w - 0.2).move_to(cell)))
            x += w
        p.until("the employer", 0.3)
        p.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in header], lag_ratio=0.25), run_time=1.6)

        def row(i):
            y = top - 0.6 - i * 0.42
            g, x = VGroup(), x0
            for w in widths:
                c = Rectangle(width=w, height=0.42, color=INK, stroke_width=1.5, fill_color=CARD, fill_opacity=1)
                c.move_to([x + w / 2, y, 0])
                bar = Rectangle(width=w * 0.55, height=0.1, stroke_width=0, fill_color=SOFT, fill_opacity=1)
                bar.move_to(c).align_to(c, LEFT).shift(RIGHT * 0.15)
                g.add(c, bar)
                x += w
            return g

        p.until("international", 0.62)
        rows = [row(i) for i in range(8)]
        p.play(LaggedStart(*[FadeIn(r) for r in rows[:4]], lag_ratio=0.4), run_time=1.6)
        p.play(LaggedStart(*[FadeIn(r) for r in rows[4:]], lag_ratio=0.2), run_time=0.8)

        p.until("But it's", 0.84)
        more = VGroup(*[Line([x0, top - 0.6 - 8 * 0.42 - 0.12 - k * 0.12, 0],
                             [x0 + sum(widths), top - 0.6 - 8 * 0.42 - 0.12 - k * 0.12, 0],
                             color=INK, stroke_width=2) for k in range(4)])
        q = T("?", 120, ACC, weight="BOLD").move_to([5.3, 0.2, 0])
        p.play(Create(more), FadeIn(q, scale=0.6), run_time=1.0)
        p.finish()


# ═════════════════════════════════════════════════════════════════════════════
class B03_ThePipeline(Scene):
    def construct(self):
        p = Pacer(self, "B03")
        boxes, arrows = pipeline()
        proposed = keep_in(tag("PROPOSED · not built").move_to([-4.6, -2.7, 0]))
        slots = VGroup(*[DashedVMobject(RoundedRectangle(width=2.6, height=1.6, corner_radius=0.14,
                                                         color=GHOST, stroke_width=4), num_dashes=30)
                         .move_to(bx) for bx in boxes[1:]])
        p.play(FadeIn(proposed), FadeIn(slots), FadeIn(boxes[0], shift=UP * 0.2), run_time=0.8)

        p.until("Claude writes", 0.2)
        p.play(GrowArrow(arrows[0]), FadeIn(boxes[1], shift=UP * 0.2), run_time=0.8)
        p.until("written contract", 0.3)
        contract = page(0.9, 1.1, 3).move_to(boxes[1].get_corner(UR) + np.array([0.1, 0.55, 0]))
        clabel = T("contract", 28).next_to(contract, UP, buff=0.15)
        p.play(FadeIn(contract, shift=DOWN * 0.3), FadeIn(clabel), run_time=0.8)

        p.until("The query runs", 0.55)
        p.play(GrowArrow(arrows[1]), FadeIn(boxes[2], shift=UP * 0.2), run_time=0.8)

        p.until("compared", 0.75)
        key = box(2.6, 1.0, "answer key", 30, fill=KRAFT).move_to([4.8, -1.75, 0])
        mine = T("worked out by hand", 24, SOFT).next_to(key, DOWN, buff=0.15)
        up = Arrow(key.get_top(), boxes[3].get_bottom(), buff=0.08, color=INK, stroke_width=5)
        p.play(GrowArrow(arrows[2]), FadeIn(boxes[3], shift=UP * 0.2), run_time=0.7)
        p.play(FadeIn(key, shift=UP * 0.3), FadeIn(mine), GrowArrow(up), run_time=0.8)

        p.until("myself", 0.86)
        cm = check_mark(np.array([4.8, 2.25, 0]), 0.4)
        p.play(Create(cm), run_time=0.6)
        p.finish()


# ═════════════════════════════════════════════════════════════════════════════
class B04_Alternatives(Scene):
    def construct(self):
        p = Pacer(self, "B04")
        xs = [-4.3, 0.0, 4.3]
        heads = [box(3.2, 1.0, n, 34).move_to([x, 2.3, 0])
                 for x, n in zip(xs, ["ChatGPT", "Vanna.ai", "SponsorSQL"])]
        note = keep_in(T("ChatGPT test: GPT-6 (high), one question, FY2026 Q3 record layout attached, 2026-10-24",
                         22, SOFT).to_edge(DOWN, buff=0.7))
        fit(note, 11.5)

        def lane(i, dashed=False):
            if dashed:
                pg = DashedVMobject(Rectangle(width=1.9, height=1.6, color=SOFT, stroke_width=4), num_dashes=28)
            else:
                pg = page(1.9, 1.6, 4)
            pg.move_to([xs[i], 0.35, 0])
            arr = Arrow(heads[i].get_bottom(), pg.get_top(), buff=0.08, color=INK, stroke_width=5)
            return pg, arr

        pg0, a0 = lane(0)
        p.play(FadeIn(heads[0]), GrowArrow(a0), FadeIn(pg0, shift=DOWN * 0.2), FadeIn(note), run_time=0.9)
        p.until("listed fifteen", 0.3)
        chip15 = tag("15 assumptions", 26).next_to(pg0, DOWN, buff=0.3)
        p.play(FadeIn(chip15, shift=UP * 0.2), run_time=0.6)
        p.until("first worksite", 0.4)
        fw = M("first worksite only", 22).next_to(chip15, DOWN, buff=0.2)
        p.play(FadeIn(fw), run_time=0.5)
        p.until("reported forty", 0.55)
        q = T("40", 64, INK, weight="BOLD").next_to(pg0, RIGHT, buff=0.35).shift(UP * 0.3)
        nc = VGroup(T("its own run", 24), T("unchecked", 24, weight="BOLD")).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        nc.next_to(q, DOWN, buff=0.15).align_to(q, LEFT)
        p.play(FadeIn(q, scale=0.6), FadeIn(nc), run_time=0.6)

        p.until("Vanna", 0.75)
        pg1, a1 = lane(1, dashed=True)
        nt = T("not tested yet", 26).next_to(pg1, DOWN, buff=0.3)
        p.play(FadeIn(heads[1]), GrowArrow(a1), Create(pg1), FadeIn(nt), run_time=0.9)

        p.until("Sponsor S Q L will", 0.85)
        pg2, a2 = lane(2)
        prop = T("(proposed)", 24, SOFT).next_to(heads[2], DOWN, buff=0.12).shift(RIGHT * 1.0)
        p.play(FadeIn(heads[2]), GrowArrow(a2), FadeIn(pg2, shift=DOWN * 0.2), FadeIn(prop), run_time=0.8)
        cm = check_mark(pg2.get_right() + np.array([0.55, 0.35, 0]), 0.28)
        log = page(1.0, 1.2, 3, fill=KRAFT).next_to(pg2, DOWN, buff=0.25).shift(RIGHT * 0.9)
        loglbl = T("failure log", 26).next_to(log, LEFT, buff=0.2)
        p.play(Create(cm), FadeIn(log, shift=RIGHT * 0.4), FadeIn(loglbl), run_time=0.9)
        p.finish()


# ═════════════════════════════════════════════════════════════════════════════
class B05_FirstMinute(Scene):
    def construct(self):
        p = Pacer(self, "B05")
        sheet = Rectangle(width=7.2, height=5.2, color=INK, stroke_width=4, fill_color=CARD, fill_opacity=1)
        sheet.move_to([-1.6, 0.1, 0])
        head = M("README.md", 30).move_to(sheet.get_top() + DOWN * 0.5).align_to(sheet, LEFT).shift(RIGHT * 0.4)
        rule = Line(sheet.get_left() + RIGHT * 0.3, sheet.get_right() + LEFT * 0.3, color=GHOST,
                    stroke_width=3).move_to(head).shift(DOWN * 0.45).set_x(sheet.get_x())
        who = VGroup(T("hiring manager", 32, weight="BOLD"), T("first minute", 28, SOFT)).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT).move_to([4.4, 1.4, 0])
        keep_in(who)
        p.play(FadeIn(sheet, shift=RIGHT * 0.4), FadeIn(head), Create(rule), FadeIn(who), run_time=1.0)

        rows_txt = [("questions", "10"), ("passed", "—"), ("failed", "—")]
        rows = VGroup()
        for i, (k, v) in enumerate(rows_txt):
            y = sheet.get_top()[1] - 1.55 - i * 0.75
            cell = Rectangle(width=5.6, height=0.7, color=INK, stroke_width=2.5).move_to([sheet.get_x(), y, 0])
            kt = T(k, 30).move_to(cell).align_to(cell, LEFT).shift(RIGHT * 0.3)
            vt = T(v, 30, weight="BOLD").move_to(cell).align_to(cell, RIGHT).shift(LEFT * 0.4)
            rows.add(VGroup(cell, kt, vt))
        p.until("evaluation table", 0.25)
        p.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.15) for r in rows], lag_ratio=0.35), run_time=1.4)

        p.until("every failure", 0.5)
        link = T("failure log  →", 30).next_to(rows, DOWN, buff=0.35).align_to(rows, LEFT).shift(RIGHT * 0.3)
        p.play(FadeIn(link, shift=RIGHT * 0.2), run_time=0.6)

        p.until("mock-up", 0.8)
        stamp = keep_in(constructed("CONSTRUCTED", "mock-up · no results exist yet").move_to([4.2, -1.2, 0]))
        dot = Dot(radius=0.11, color=ACC).next_to(stamp[0], RIGHT, buff=0.25)
        p.play(FadeIn(stamp), FadeIn(dot, scale=0.4), run_time=0.7)
        p.finish()


# ═════════════════════════════════════════════════════════════════════════════
class B06_FourSkills(Scene):
    def construct(self):
        p = Pacer(self, "B06")
        boxes, arrows = pipeline()
        proposed = keep_in(tag("PROPOSED · not built").move_to([-4.6, -2.7, 0]))
        p.play(*[FadeIn(b) for b in boxes], *[FadeIn(a) for a in arrows], FadeIn(proposed), run_time=0.8)

        def attach(target, text, above=True, size=28):
            t = tag(text, size)
            t.next_to(target, UP if above else DOWN, buff=0.35)
            ln = Line(target.get_top() if above else target.get_bottom(),
                      t.get_bottom() if above else t.get_top(), color=INK, stroke_width=3)
            return VGroup(ln, t)

        p.until("A prompt contract", 0.2)
        a = attach(boxes[1], "prompt contract")
        p.play(FadeIn(a, shift=DOWN * 0.2), run_time=0.7)
        p.until("Verification", 0.4)
        b = attach(boxes[3], "verification")
        p.play(FadeIn(b, shift=DOWN * 0.2), run_time=0.7)
        p.until("Evaluation", 0.6)
        c = attach(boxes[3], "evaluation", above=False)
        tally = VGroup(*[Line(UP * 0.25, DOWN * 0.25, color=INK, stroke_width=5).shift(RIGHT * 0.2 * k)
                         for k in range(4)]).next_to(c, DOWN, buff=0.2)
        p.play(FadeIn(c, shift=UP * 0.2), Create(tally), run_time=0.8)
        p.until("source grounding", 0.8)
        d = attach(boxes[2], "source grounding", above=False)
        chip = keep_in(M("FY2026 Q3 · file · query", 24).next_to(d, DOWN, buff=0.2))
        dot = Dot(chip.get_left() + LEFT * 0.25, radius=0.1, color=ACC)
        p.play(FadeIn(d, shift=UP * 0.2), FadeIn(chip), FadeIn(dot, scale=0.4), run_time=0.8)
        p.finish()


# ═════════════════════════════════════════════════════════════════════════════
def tray(x, label):
    w, h, y = 3.4, 2.2, -1.2
    shape = VMobject(color=INK, stroke_width=5).set_points_as_corners(
        [[x - w / 2, y + h / 2, 0], [x - w / 2, y - h / 2, 0], [x + w / 2, y - h / 2, 0], [x + w / 2, y + h / 2, 0]])
    fill = Rectangle(width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    head = T(label, 44, weight="BOLD").move_to([x, 2.6, 0])
    return VGroup(fill, shape), head


def card(text, w=3.0, size=26):
    r = RoundedRectangle(width=w, height=0.75, corner_radius=0.1, color=INK, stroke_width=3,
                         fill_color=CARD, fill_opacity=1)
    return VGroup(r, fit(T(text, size), w - 0.3).move_to(r))


class B07_InOutFirst(Scene):
    def construct(self):
        p = Pacer(self, "B07")
        xs = [-4.3, 0.0, 4.3]
        trays = [tray(x, n) for x, n in zip(xs, ["IN", "OUT", "FIRST"])]
        p.play(*[FadeIn(t[0]) for t in trays], *[FadeIn(t[1]) for t in trays], run_time=0.9)

        def drop(c, x, y):
            c.move_to([x, 2.6, 0])
            self.add(c)
            p.play(c.animate.move_to([x, y, 0]), run_time=0.7)

        p.until("Duck", 0.2)
        drop(card("FY2026 Q3 · DuckDB"), xs[0], -0.65)
        drop(card("contact columns dropped", 3.0, 24), xs[0], -1.6)

        p.until("predict sponsorship", 0.38)
        c1, c2 = card("sponsorship prediction", 2.5, 24), card("legal advice", 2.5, 24)
        drop(c1, xs[1] + 0.35, -0.65)
        drop(c2, xs[1] + 0.35, -1.6)
        crosses = VGroup()
        for cy in (-0.65, -1.6):
            ctr = np.array([xs[1] - 1.25, cy, 0])
            crosses.add(Line(ctr + np.array([-0.17, 0.17, 0]), ctr + np.array([0.17, -0.17, 0]), color=INK, stroke_width=6),
                        Line(ctr + np.array([-0.17, -0.17, 0]), ctr + np.array([0.17, 0.17, 0]), color=INK, stroke_width=6))
        p.play(Create(crosses), run_time=0.5)

        p.until("job offer", 0.55)
        note = keep_in(T("LCA filing ≠ job offer ≠ visa", 28, INK).move_to([xs[1], -2.8, 0]))
        p.play(FadeIn(note), run_time=0.5)

        p.until("ten questions", 0.78)
        f1 = card("10 questions + answer key", 3.1, 24)
        drop(f1, xs[2], -0.65)
        f2 = card("pass / fail table", 3.1, 24)
        drop(f2, xs[2], -1.6)
        dot = Dot([xs[2] + 1.3, 0.2, 0], radius=0.11, color=ACC)
        p.play(FadeIn(dot, scale=0.4), run_time=0.4)
        p.finish()


# ═════════════════════════════════════════════════════════════════════════════
class B08_NameVariants(Scene):
    def construct(self):
        p = Pacer(self, "B08")
        names = ["EXAMPLE DATA LLC", "Example Data, LLC", "EXAMPLE DATA L.L.C."]
        rows = VGroup()
        for i, n in enumerate(names):
            r = Rectangle(width=6.2, height=0.85, color=INK, stroke_width=3, fill_color=CARD, fill_opacity=1)
            r.move_to([-2.4, 1.5 - i * 1.1, 0])
            rows.add(VGroup(r, M(n, 28).move_to(r).align_to(r, LEFT).shift(RIGHT * 0.35)))
        label = constructed("CONSTRUCTED", "invented company · not from the data")
        p.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.3), FadeIn(label), run_time=1.2)

        p.until("trade names", 0.3)
        chip = keep_in(tag("TRADE_NAME_DBA", 26).move_to([3.8, 2.4, 0]))
        chip_note = keep_in(T("a separate field in the file", 24, SOFT).next_to(chip, DOWN, buff=0.15))
        p.play(FadeIn(chip), FadeIn(chip_note), run_time=0.7)

        p.until("undercount", 0.45)
        scan = Line([-5.7, 2.2, 0], [-5.7, -1.1, 0], color=ACC, stroke_width=5)
        p.play(Create(scan), run_time=0.3)
        p.play(scan.animate.shift(RIGHT * 6.6), run_time=1.0)
        hit = SurroundingRectangle(rows[0], color=INK, stroke_width=7, buff=0.06)
        qn = VGroup(T("query", 30), T("1", 60, weight="BOLD")).arrange(RIGHT, buff=0.3).move_to([3.0, 0.4, 0])
        kn = VGroup(T("answer key", 30), T("3", 60, weight="BOLD")).arrange(RIGHT, buff=0.3).move_to([3.3, -0.7, 0])
        p.play(FadeOut(scan), Create(hit), FadeIn(qn), FadeIn(kn), run_time=0.8)

        p.until("show the matching rows", 0.85)
        show = T("show the matching rows", 30, weight="BOLD").move_to([-2.4, -2.0, 0])
        allrows = SurroundingRectangle(rows, color=INK, stroke_width=7, buff=0.12)
        p.play(ReplacementTransform(hit, allrows), FadeIn(show, shift=UP * 0.2), run_time=0.8)
        p.finish()


# ═════════════════════════════════════════════════════════════════════════════
def chip(text, size=28, fill=CARD):
    t = T(text, size)
    r = RoundedRectangle(width=t.width + 0.5, height=0.75, corner_radius=0.18, color=INK,
                         stroke_width=3, fill_color=fill, fill_opacity=1)
    return VGroup(r, t.move_to(r))


class B09_HaveAndNew(Scene):
    def construct(self):
        p = Pacer(self, "B09")
        shelf_l = Line([-6.0, -1.0, 0], [-0.6, -1.0, 0], color=INK, stroke_width=6)
        shelf_r = Line([0.6, -1.0, 0], [6.0, -1.0, 0], color=INK, stroke_width=6)
        h_l = T("already have", 38, weight="BOLD").move_to([-3.3, 2.85, 0])
        h_r = T("new to me", 38, weight="BOLD").move_to([3.3, 2.85, 0])
        p.play(Create(shelf_l), Create(shelf_r), FadeIn(h_l), FadeIn(h_r), run_time=0.9)

        p.until("I already use", 0.2)
        have = VGroup(chip("SQL"), chip("Python · pandas"), chip("BI dashboards")).arrange(DOWN, buff=0.15)
        have.next_to(shelf_l, UP, buff=0.12)
        p.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in have[::-1]], lag_ratio=0.3), run_time=1.2)
        src = T("earlier academic + professional work", 24, SOFT).next_to(shelf_l, DOWN, buff=0.2)
        p.play(FadeIn(src), run_time=0.4)

        p.until("What's new", 0.5)
        new = VGroup(chip("eval harness for AI-written SQL", 26), chip("honest failure reports", 26)).arrange(DOWN, buff=0.15)
        fit(new, 5.2)
        new.next_to(shelf_r, UP, buff=0.12)
        keep_in(new)
        p.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in new[::-1]], lag_ratio=0.3), run_time=1.0)

        p.until("international student", 0.8)
        why = chip("international student", 30, fill=KRAFT).move_to([0, -2.7, 0])
        dot = Dot(why.get_left() + LEFT * 0.3, radius=0.11, color=ACC)
        p.play(FadeIn(why, shift=UP * 0.3), FadeIn(dot, scale=0.4), run_time=0.7)
        p.finish()


# ═════════════════════════════════════════════════════════════════════════════
class B10_TodayAndWill(Scene):
    def construct(self):
        p = Pacer(self, "B10")
        div = DashedLine([-0.9, 2.9, 0], [-0.9, -2.9, 0], color=GHOST, stroke_width=3)
        h_t = T("exists today", 38, weight="BOLD").move_to([-3.6, 2.6, 0])
        h_w = T("will exist", 38, weight="BOLD").move_to([2.6, 2.6, 0])
        p.play(FadeIn(h_t), FadeIn(h_w), Create(div), run_time=0.8)

        def item(y, text):
            ic = page(0.75, 0.95, 3).move_to([-5.4, y, 0])
            lb = fit(T(text, 30), 3.6).next_to(ic, RIGHT, buff=0.3)
            return VGroup(ic, lb)

        p.until("my project brief", 0.2)
        i1 = item(1.35, "project brief")
        p.play(FadeIn(i1, shift=DOWN * 0.2), run_time=0.6)
        p.until("latest data file", 0.3)
        i2 = item(0.1, "data file · FY2026 Q3")
        p.play(FadeIn(i2, shift=DOWN * 0.2), run_time=0.6)
        p.until("test", 0.45)
        i3 = item(-1.15, "ChatGPT test · 2026-10-24")
        p.play(FadeIn(i3, shift=DOWN * 0.2), run_time=0.6)

        p.until("Nothing is loaded", 0.55)
        dot = Dot([-5.4, -2.45, 0], radius=0.11, color=ACC)
        built = fit(T("nothing loaded or built yet", 26, SOFT), 3.6).next_to(dot, RIGHT, buff=0.3)
        p.play(FadeIn(dot, scale=0.4), FadeIn(built), run_time=0.6)

        p.until("The database", 0.7)
        names = ["database", "contract", "test set", "run logs", "failure log"]
        ghosts = VGroup()
        for k, n in enumerate(names):
            col, rw = k % 3, k // 3
            x, y = 0.4 + col * 2.0, 0.9 - rw * 2.4
            outline = DashedVMobject(Rectangle(width=1.4, height=1.5, color=SOFT, stroke_width=4), num_dashes=24)
            outline.move_to([x, y, 0])
            ghosts.add(VGroup(outline, T(n, 26, SOFT).next_to(outline, DOWN, buff=0.12)))
        p.play(LaggedStart(*[Create(g[0]) for g in ghosts], lag_ratio=0.2),
               LaggedStart(*[FadeIn(g[1]) for g in ghosts], lag_ratio=0.2), run_time=1.6)
        p.finish()


# ═════════════════════════════════════════════════════════════════════════════
class B12_Outro(Scene):
    def construct(self):
        p = Pacer(self, "B12")
        name = T("SponsorSQL", 132, weight="BOLD")
        dot = Dot(radius=0.17, color=ACC).next_to(name, RIGHT, buff=0.1).align_to(name, DOWN).shift(UP * 0.07)
        title = VGroup(name, dot).move_to([0, 1.7, 0])
        sub = T("Plain-English questions, checked answers", 48).next_to(title, DOWN, buff=0.45)
        fit(sub, 11.5)
        p.play(FadeIn(name, shift=UP * 0.2), run_time=0.7)
        p.play(FadeIn(dot, scale=0.3), FadeIn(sub), run_time=0.5)

        rule = Line(LEFT * 5.6, RIGHT * 5.6, color=INK, stroke_width=3).next_to(sub, DOWN, buff=0.55)
        cred = VGroup(
            T("Atharva Hambir · INFO 7375 · a pitch, nothing built yet", 34),
            T("Script written with Claude, reviewed by me · narration: Kokoro synthetic voice", 30, SOFT),
        ).arrange(DOWN, buff=0.25).next_to(rule, DOWN, buff=0.45)
        fit(cred, 11.5)
        p.until("checked answers", 0.25)
        p.play(Create(rule), FadeIn(cred), run_time=0.7)
        p.finish()
