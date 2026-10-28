"""scenes.py — Cite & Seek pitch film: one drawn scene per drawn beat (show-tell style).

Palette and type follow the show-tell kit (brutalist.art/skills/make/show-tell/templates/iso_kit.py),
drawn flat rather than isometric. Written for this film; nothing is imported from the toolkit.

Rules every scene follows:
- Its beat's `shot.screen_tag` ("constructed" or "constructed · planned") is on screen from the first
  frame, top right, full ink, size 32 (the toolkit minimum). BOUT is a title card and has no tag.
- Pacing: durations come from beat_sheet.json (measured audio). All motion lands by 40% of the beat,
  so nothing moves at the 50% midpoint that GATE T and Gate V sample; the scene then holds and ends
  0.06 s before its audio, so compile.py never centre-cuts it. Without the sheet (Gate A's sandbox
  copies only this file) a fallback duration is used.
- Labels: ink, size 32-40, beside objects (never inside an outline), never terracotta. Terracotta only for
  dots. Pipeline stages are labelled boxes joined by arrows; file names and chunk ranges are real. Every coordinate stays inside +-6.2 x +-3.3.
- Every scene adds a new non-text shape after its first frame (Gate A).
"""
import json
import os
from contextlib import contextmanager

import numpy as np
from manim import *

try:  # Gate A's static stub has no register_font; the real manim does (pattern: runtime/manim/seis_graphics.py)
    from manim import register_font as _register_font
except Exception:
    _register_font = None

# ── Palette (show-tell kit) ─────────────────────────────────────────────────────
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
KRAFT = "#DCC9AA"; KRAFT_D = "#C7AE86"; BAR1 = "#8B8F96"; BAR2 = "#B4AFA6"
SERIF = "EB Garamond"
config.background_color = STAGE

# ── Font: this Manim/Pango build does not scan ~/Library/Fonts, so register the file per scene ──
_HERE = os.path.dirname(os.path.abspath(__file__))
_SERIF_TTF = next((p for p in (os.path.join(_HERE, "fonts", "EBGaramond-Regular.ttf"),)
                   if os.path.exists(p)), None)


@contextmanager
def serif_font():
    if _SERIF_TTF and _register_font is not None:
        with _register_font(_SERIF_TTF):
            yield
    else:
        yield


# ── Durations and tags from the beat sheet ──────────────────────────────────────
_DUR, _TAG, _NARR, _HEAD, _SUB = {}, {}, {}, {}, {}
try:
    with open(os.path.join(_HERE, "beat_sheet.json")) as fh:
        for _b in json.load(fh)["beats"]:
            _DUR[_b["beat_id"]] = float(_b.get("actual_duration_s") or _b.get("estimated_duration_s") or 8.0)
            _TAG[_b["beat_id"]] = (_b.get("shot") or {}).get("screen_tag")
            _NARR[_b["beat_id"]] = _b.get("narration_text", "")
            _HEAD[_b["beat_id"]] = (_b.get("shot") or {}).get("heading")
            _SUB[_b["beat_id"]] = (_b.get("shot") or {}).get("subheading")
except (OSError, ValueError, KeyError):
    pass
FALLBACK_S = 8.0
SLACK_S = 0.06
MOTION_SHARE = 0.40


class Pacer:
    """Scale the planned animation time to fit 40% of the beat; then hold to the end."""

    def __init__(self, scene, bid, planned):
        self.sc, self.bid = scene, bid
        self.dur = _DUR.get(bid, FALLBACK_S)
        self.k = min(1.0, MOTION_SHARE * self.dur / planned)
        self.used = 0.0

    def play(self, *anims, rt=0.5):
        t = rt * self.k
        self.sc.play(*anims, run_time=t)
        self.used += t

    def finish(self):
        self.sc.wait(max(0.3, self.dur - self.used - SLACK_S))


# Segment headings, written here so the static gates (A and W, which see only this file) check them.
# They must match make_sheet.py SEGMENTS; begin() raises if beat_sheet.json disagrees.
HEADINGS = {
    "B00": ("What It Is", "Answers with citations, or refuses"),
    "B03": ("What It Is", "A real open-source e-commerce codebase"),
    "B01": ("The Hypothesis", "Help a new engineer understand unfamiliar code"),
    "B02": ("The Hypothesis", "Haven't tested with real engineers yet"),
    "B10": ("Who It's For", "Target reader: hiring manager for an entry-level AI Engineer role"),
    "B04": ("How It Works", "Retrieval"),
    "B05": ("How It Works", "Citation"),
    "B06": ("How It Works", "Abstention"),
    "B07": ("What It Proves", "In course terms: source grounding, prompt contracts, evaluation"),
    "B07B": ("What It Proves", "What a reviewer could fairly conclude"),
    "B08": ("Why It's Different", "Test questions before retrieval code"),
    "B09": ("Why It's Different", "The alternative: reading the code by hand"),
    "B09B": ("Why It's Different", "Cite & Seek points to the exact lines"),
    "B11": ("Scope: In, Out, First", "In scope and out of scope"),
    "B12": ("Scope: In, Out, First", "First: the scoring harness"),
    "B13": ("What Could Sink It", "Sample size"),
    "B16": ("Why This Project", None),
    "B14": ("Built So Far / Will Build", None),
    "B15": ("Built So Far / Will Build", None),
}
HEAD_SIZE, SUB_SIZE = 40, 32
HEAD_DROP = 0.55   # drawings move down this far on beats with a heading, so the heading never overlaps them
_DY = 0.0


def begin(scene, bid, planned, tagged=True):
    """Put the segment heading, subheading and screen tag on stage (static, whole beat); return the pacer."""
    global _DY
    head, sub = HEADINGS.get(bid, (None, None))
    if _DUR and (_HEAD.get(bid), _SUB.get(bid)) != (head, sub):
        raise ValueError(f"{bid}: heading in scenes.py {(head, sub)} != beat_sheet.json {(_HEAD.get(bid), _SUB.get(bid))}")
    _DY = HEAD_DROP if head else 0.0
    if head:
        h = Text(head, font=SERIF, color=INK, font_size=HEAD_SIZE).to_corner(UL, buff=1.0)
        scene.add(h)
        if sub:
            scene.add(Text(sub, font=SERIF, color=INK, font_size=SUB_SIZE)
                      .next_to(h, DOWN, buff=0.18, aligned_edge=LEFT))
    if tagged:
        tag = Text(_TAG.get(bid) or "constructed", font=SERIF, color=INK, font_size=32)
        tag.to_corner(UR, buff=1.0)
        scene.add(tag)
    return Pacer(scene, bid, planned)


# ── Drawing primitives ──────────────────────────────────────────────────────────
def P3(x, y):
    return np.array([x, y - _DY, 0.0])


def lab(s, size=40):
    return Text(s, font=SERIF, color=INK, font_size=size)


def block(w, h, x, y, color=INK):
    return Rectangle(width=w, height=h, fill_color=color, fill_opacity=1,
                     stroke_color=color, stroke_width=4).move_to(P3(x, y))


def page(w, h, x, y, fill=CARD):
    return Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1,
                     stroke_color=INK, stroke_width=4).move_to(P3(x, y))


def slab(w, h, x, y):
    return Rectangle(width=w, height=h, fill_color=KRAFT_D, fill_opacity=1,
                     stroke_color=INK, stroke_width=4).move_to(P3(x, y))


def tick(x, y, s=0.32, color=INK):
    a, b, c = P3(x - s, y), P3(x - s * 0.35, y - s * 0.7), P3(x + s, y + s * 0.8)
    return VGroup(Line(a, b), Line(b, c)).set_stroke(color, width=9)


def spark(x, y, r=0.13):
    return Dot(point=P3(x, y), radius=r, color=TERRA)


def magnifier(x, y):
    ring = Circle(radius=0.42, color=INK, stroke_width=8).move_to(P3(x, y))
    handle = Line(P3(x + 0.30, y - 0.30), P3(x + 0.75, y - 0.75)).set_stroke(INK, width=12)
    return VGroup(ring, handle)


def gauge(x, y, r=1.2):
    arc = Arc(radius=r, start_angle=0, angle=PI, arc_center=P3(x, y)).set_stroke(INK, width=8)
    base = Dot(point=P3(x, y), radius=0.12, color=INK)
    return VGroup(arc, base)


def needle(x, y, angle, r=1.0):
    tip = P3(x + r * np.cos(angle), y + r * np.sin(angle))
    return Line(P3(x, y), tip).set_stroke(INK, width=10)


def row_xs(n, x0, w=0.62, gap=0.32):
    return [x0 + i * (w + gap) for i in range(n)]


def pages_row(n, x0, y, w=0.62, h=0.82, gap=0.32, fill=CARD):
    return [page(w, h, x, y, fill) for x in row_xs(n, x0, w, gap)]


def arrow(x1, y1, x2, y2):
    return Arrow(P3(x1, y1), P3(x2, y2), buff=0, color=INK, stroke_width=6,
                 max_tip_length_to_length_ratio=0.22)


def laptop(x, y):
    screen = block(1.9, 1.15, x, y + 0.45)
    base = slab(2.5, 0.2, x, y - 0.25)
    return VGroup(screen, base)


CITE = "[app/api/orders.py:52-84]"   # a real chunk boundary from the baseline's chunker


# ═════════════════════════════════ Introduction (title card) ════════════════════
class BIDEA_Intro(Scene):
    """'Introduction' large; the course name types out as it is spoken; then 'Final Project'. No tag.

    Timing: typing starts when the course name is spoken (its character share of the narration after the
    0.8 s lead), but finishes before the 45-55% window GATE T and Gate V sample; 'Final Project' lands after it.
    """

    def construct(self):
        with serif_font():
            global _DY
            _DY = 0.0
            dur = _DUR.get("BIDEA", 11.5)
            narr = _NARR.get("BIDEA", "")
            lead = 0.8
            share = narr.find("INFO") / len(narr) if "INFO" in narr else 0.3
            spoken = lead + share * (dur - lead)
            guard_start, guard_end = 0.45 * dur - 0.22, 0.55 * dur + 0.22
            t = 0.0
            head = Text("Introduction", font=SERIF, color=INK, font_size=96).to_corner(UL, buff=1.0)
            self.play(FadeIn(head), run_time=0.5); t += 0.5
            # The underline spans the heading's measured width (it was two fixed 2.2-unit halves, 4.4 units,
            # shorter than the word). It is still drawn in two halves: Gate A needs two distinct shape states.
            half = head.width / 2
            left = Rectangle(width=half, height=0.07, fill_color=INK, fill_opacity=1, stroke_color=INK,
                             stroke_width=2).next_to(head, DOWN, buff=0.25, aligned_edge=LEFT)
            right = Rectangle(width=half, height=0.07, fill_color=INK, fill_opacity=1, stroke_color=INK,
                              stroke_width=2).next_to(left, RIGHT, buff=0)
            self.play(GrowFromEdge(left, LEFT), run_time=0.3); t += 0.3
            self.play(GrowFromEdge(right, LEFT), run_time=0.3); t += 0.3
            # Course name as two lines, each left-aligned with the heading (a single two-line Text centres
            # its second line), typed one after the other.
            line1 = Text("INFO 7375: Prompt Engineering", font=SERIF, color=INK, font_size=60)
            line1.move_to(P3(0, 0.55)).align_to(head, LEFT)
            line2 = Text("for Generative AI", font=SERIF, color=INK, font_size=60)
            line2.move_to(P3(0, -0.35)).align_to(head, LEFT)
            type_s = 1.0
            start = max(t, min(spoken, guard_start - type_s))
            if start > t:
                self.wait(start - t); t = start
            self.play(AddTextLetterByLetter(line1), run_time=0.62 * type_s); t += 0.62 * type_s
            self.play(AddTextLetterByLetter(line2), run_time=0.38 * type_s); t += 0.38 * type_s
            if guard_end > t:
                self.wait(guard_end - t); t = guard_end
            final = Text("Final Project", font=SERIF, color=INK, font_size=64)
            final.move_to(P3(0, -1.9)).align_to(head, LEFT)
            self.play(FadeIn(final), run_time=0.5); t += 0.5
            self.wait(max(0.3, dur - t - SLACK_S))


# ═════════════════════════════════ Q1 ═══════════════════════════════════════════
class B00_WhatItIs(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B00", planned=3.6)
            q = page(1.2, 0.8, -5.0, 1.2)
            ql = lab("question", 36).next_to(q, DOWN, buff=0.3)
            p.play(FadeIn(q), FadeIn(ql), rt=0.5)
            tool = block(2.0, 1.4, -1.9, 1.2)
            tl = lab("Cite & Seek", 36).next_to(tool, DOWN, buff=0.3)
            p.play(FadeIn(tool), FadeIn(tl), Create(arrow(-4.3, 1.2, -2.95, 1.2)), rt=0.6)
            ans = page(1.3, 0.85, 1.7, 1.2)
            p.play(Create(arrow(-0.85, 1.2, 0.95, 1.2)), FadeIn(ans), rt=0.5)
            ct = lab(CITE, 32).move_to(P3(2.3, 0.2))
            p.play(GrowFromCenter(spark(2.05, 1.2)), FadeIn(ct), rt=0.5)
            p.play(Create(arrow(-1.9, -0.35, -1.9, -1.35)), rt=0.4)
            slip = page(1.6, 0.55, -1.9, -1.75)
            sl = lab("ABSTAIN", 36).next_to(slip, RIGHT, buff=0.4)
            p.play(FadeIn(slip), FadeIn(sl), rt=0.5)
            p.finish()


# ═════════════════════════════════ Q2: impact (hypothesis) ══════════════════════
class B01_Hypothesis(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B01", planned=2.4)
            new, senior = laptop(-4.0, -0.7), laptop(3.9, -0.7)
            nl = lab("new engineer", 34).next_to(new, DOWN, buff=0.3)
            sl = lab("senior engineer", 34).next_to(senior, DOWN, buff=0.3)
            p.play(FadeIn(new), FadeIn(senior), FadeIn(nl), FadeIn(sl), rt=0.6)
            # The box sits level with the laptops; question and answer are two horizontal arrows, 0.6 apart,
            # so their bounding boxes never overlap (crossing diagonals read as stacked text in GATE T §8.6b).
            tool = block(1.8, 1.0, 0.0, -0.25)
            tl = lab("Cite & Seek", 34).next_to(tool, UP, buff=0.3)
            p.play(FadeIn(tool), FadeIn(tl), rt=0.5)
            p.play(Create(arrow(-2.9, 0.05, -1.05, 0.05)), rt=0.4)
            p.play(Create(arrow(-1.05, -0.55, -2.9, -0.55)), rt=0.4)
            p.play(GrowFromCenter(spark(3.9, -0.25, r=0.16)), rt=0.3)
            p.finish()


class B02_Checkable(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B02", planned=1.6)
            src = page(2.4, 3.0, -1.4, -0.4)
            fl = lab("app/api/orders.py", 34).next_to(src, UP, buff=0.3)
            bars = [Rectangle(width=1.8, height=0.22, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                    .move_to(P3(-1.4, 0.7 - i * 0.5)) for i in range(5)]
            p.play(FadeIn(src), FadeIn(fl), *[FadeIn(b) for b in bars], rt=0.5)
            hi = [Rectangle(width=1.8, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0)
                  .move_to(P3(-1.4, 0.7 - i * 0.5)) for i in (2, 3)]
            p.play(*[FadeIn(h) for h in hi], rt=0.4)
            mag = magnifier(0.75, 0.55)
            ll = lab("lines 52-84", 36).move_to(P3(2.9, -0.15))
            p.play(FadeIn(mag), FadeIn(ll), rt=0.5)
            p.finish()


# ═════════════════════════════════ Q5: the data ═════════════════════════════════
class B03_Data(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B03", planned=2.8)
            crate = slab(3.2, 1.1, -3.9, -1.1)
            p.play(FadeIn(crate), rt=0.4)
            files = [page(0.75, 0.95, x, -0.05) for x in (-4.85, -3.9, -2.95)]
            p.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.3) for f in files], lag_ratio=0.25), rt=0.7)
            rl = lab("e-commerce API", 36).move_to(P3(-3.9, 0.85))
            gl = lab("GitHub · MIT", 34).next_to(crate, DOWN, buff=0.3)
            p.play(FadeIn(rl), FadeIn(gl), rt=0.4)
            binder = block(1.2, 1.6, 0.5, -0.5)
            bl = lab("53 questions", 34).next_to(binder, DOWN, buff=0.3)
            p.play(FadeIn(binder), FadeIn(bl), rt=0.5)
            folder = Rectangle(width=1.8, height=1.25, fill_color=KRAFT_D, fill_opacity=1,
                               stroke_color=INK, stroke_width=4).move_to(P3(4.2, -0.6))
            tab = Rectangle(width=0.7, height=0.25, fill_color=KRAFT_D, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to(P3(3.65, 0.15))
            il = lab("10 synthetic incidents", 32).next_to(folder, DOWN, buff=0.3)
            p.play(FadeIn(folder), FadeIn(tab), FadeIn(il), rt=0.6)
            p.finish()


# ═════════════════════════════════ Q5: the pipeline today ═══════════════════════
class B04_Retrieve(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B04", planned=3.4)
            q = page(1.1, 0.75, -5.0, 1.4)
            ql = lab("question", 34).next_to(q, DOWN, buff=0.3)
            p.play(FadeIn(q), FadeIn(ql), rt=0.4)
            p.play(Create(arrow(-4.35, 1.4, -3.35, 1.4)), rt=0.3)
            emb = block(1.8, 0.9, -2.4, 1.4)
            el = lab("MiniLM embed", 34).next_to(emb, DOWN, buff=0.3)
            p.play(FadeIn(emb), FadeIn(el), rt=0.4)
            p.play(Create(arrow(-1.4, 1.4, 0.55, 1.4)), rt=0.3)
            srch = block(1.8, 0.9, 1.5, 1.4)
            sl = lab("search all chunks", 32).next_to(srch, DOWN, buff=0.3)
            p.play(FadeIn(srch), FadeIn(sl), rt=0.4)
            names = ("orders.py 52-84", "cart.py 27-46", "payments.py 1-24")
            strips = [page(2.0, 0.42, 1.2, -0.65 - i * 0.7) for i in range(3)]
            p.play(LaggedStart(*[FadeIn(s) for s in strips], lag_ratio=0.25), rt=0.7)
            nls = [lab(n, 32).next_to(s, RIGHT, buff=0.35) for n, s in zip(names, strips)]
            tl = lab("≤ 200 tokens", 34).move_to(P3(-1.9, -1.35))
            p.play(*[FadeIn(n) for n in nls], FadeIn(tl), rt=0.5)
            p.finish()


class B05_Answer(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B05", planned=3.5)
            srch = block(1.4, 0.8, -5.0, 1.3)
            sl = lab("search", 34).next_to(srch, DOWN, buff=0.3)
            p.play(FadeIn(srch), FadeIn(sl), rt=0.3)
            p.play(Create(arrow(-4.25, 1.3, -3.45, 1.3)), rt=0.25)
            top5 = [Rectangle(width=1.1, height=0.14, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                    .move_to(P3(-2.8, 1.7 - i * 0.2)) for i in range(5)]
            tl = lab("top 5", 34).move_to(P3(-2.8, 0.45))
            p.play(LaggedStart(*[FadeIn(t) for t in top5], lag_ratio=0.2), FadeIn(tl), rt=0.5)
            p.play(Create(arrow(-2.15, 1.3, -1.25, 1.3)), rt=0.25)
            hk = block(2.2, 0.9, 0.0, 1.3)
            hl = lab("Claude Haiku 4.5", 32).next_to(hk, DOWN, buff=0.3)
            p.play(FadeIn(hk), FadeIn(hl), rt=0.4)
            p.play(Create(arrow(1.15, 1.3, 2.2, 1.3)), rt=0.25)
            ans = page(1.4, 0.95, 3.05, 1.3)
            al = lab("answer", 34).next_to(ans, DOWN, buff=0.3)
            p.play(FadeIn(ans), FadeIn(al), rt=0.4)
            ct = lab(CITE, 32).move_to(P3(2.55, -0.45))
            p.play(GrowFromCenter(spark(3.45, 1.3)), FadeIn(ct), rt=0.4)
            rule = page(0.9, 1.1, -4.9, -1.75)
            rl = lab("only these chunks · cite every claim", 32).next_to(rule, RIGHT, buff=0.4)
            p.play(FadeIn(rule), FadeIn(rl), rt=0.5)
            p.finish()


class B06_Abstain(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B06", planned=2.8)
            hk = block(2.0, 0.9, -4.0, 0.3)
            hl = lab("Claude Haiku 4.5", 32).next_to(hk, DOWN, buff=0.3)
            p.play(FadeIn(hk), FadeIn(hl), rt=0.4)
            p.play(Create(arrow(-2.9, 0.6, -0.9, 1.45)), rt=0.3)
            part = page(1.6, 1.0, 0.1, 1.6)
            lines = [Rectangle(width=1.1, height=0.14, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                     .move_to(P3(-0.05, 1.85 - i * 0.3)) for i in range(2)]
            p.play(FadeIn(part), *[FadeIn(l) for l in lines], rt=0.4)
            pl = lab("no partial answers", 34).next_to(part, RIGHT, buff=0.4)
            p.play(part.animate.set_fill(GHOST), FadeIn(pl), rt=0.5)
            p.play(Create(arrow(-2.9, 0.0, -0.9, -1.3)), rt=0.3)
            slip = page(1.6, 0.55, 0.1, -1.5)
            al = lab("ABSTAIN: what's missing", 32).next_to(slip, RIGHT, buff=0.4)
            p.play(FadeIn(slip), FadeIn(al), rt=0.5)
            p.finish()


# ═════════════════════════════════ Q4: what it proves ═══════════════════════════
class B07_Skills(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B07", planned=3.2)
            xs = (-4.5, -1.5, 1.5, 4.5)
            names = ("Retrieval", "Citation", "Abstention", "Evaluation")
            solid = [block(1.7, 1.1, x, 0.1) for x in xs[:3]]
            p.play(LaggedStart(*[FadeIn(s) for s in solid], lag_ratio=0.25), rt=0.9)
            nls = [lab(n, 36).move_to(P3(x, -0.85)) for n, x in zip(names, xs)]
            p.play(*[FadeIn(n) for n in nls[:3]], rt=0.4)
            bracket = Line(P3(-5.35, 0.95), P3(2.35, 0.95)).set_stroke(INK, width=5)
            bl = lab("built", 36).move_to(P3(-1.5, 1.6))
            p.play(Create(bracket), FadeIn(bl), rt=0.5)
            ev = Rectangle(width=1.7, height=1.1, stroke_color=INK, stroke_width=6).move_to(P3(4.5, 0.1))
            wl = lab("will build", 36).move_to(P3(4.5, 1.6))
            p.play(Create(ev), FadeIn(nls[3]), FadeIn(wl), rt=0.6)
            p.finish()


class B07B_Conclude(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B07B", planned=2.4)
            binder = block(1.2, 1.6, -3.8, -0.1)
            bl = lab("53 questions", 34).next_to(binder, DOWN, buff=0.3)
            p.play(FadeIn(binder), FadeIn(bl), rt=0.4)
            p.play(Create(arrow(-2.95, -0.1, -1.35, -0.1)), rt=0.4)
            system = Rectangle(width=2.8, height=1.3, stroke_color=INK, stroke_width=5).move_to(P3(0.3, -0.1))
            sl = lab("system", 34).next_to(system, DOWN, buff=0.3)
            p.play(Create(system), FadeIn(sl), rt=0.5)
            t = tick(-3.9, -2.35, s=0.26)
            cl = lab("test before the system", 36).move_to(P3(-1.4, -2.35))
            p.play(Create(t), FadeIn(cl), rt=0.5)
            p.finish()


# ═════════════════════════════════ Q2: why it is different ══════════════════════
class B08_Order(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B08", planned=3.2)
            binder = block(1.2, 1.6, -4.6, 0.7)
            bl = lab("53 questions", 34).next_to(binder, DOWN, buff=0.3)
            p.play(FadeIn(binder), FadeIn(bl), rt=0.5)
            body = Rectangle(width=0.6, height=0.5, fill_color=KRAFT_D, fill_opacity=1,
                             stroke_color=INK, stroke_width=4).move_to(P3(-3.45, 0.55))
            shackle = Arc(radius=0.2, start_angle=0, angle=PI, arc_center=P3(-3.45, 0.8)).set_stroke(INK, width=7)
            p.play(FadeIn(VGroup(shackle, body), shift=DOWN * 0.2), rt=0.4)
            fl = lab("first", 36).move_to(P3(-1.95, 1.3))
            p.play(Create(arrow(-2.95, 0.7, -1.05, 0.7)), FadeIn(fl), rt=0.5)
            code = Rectangle(width=3.0, height=1.4, stroke_color=INK, stroke_width=5).move_to(P3(0.6, 0.7))
            cl = lab("retrieval code", 34).next_to(code, DOWN, buff=0.3)
            p.play(Create(code), FadeIn(cl), rt=0.5)
            row = [page(0.5, 0.65, -5.0 + i * 0.75, -1.9) for i in range(8)]
            p.play(LaggedStart(*[FadeIn(pg, shift=RIGHT * 0.3) for pg in row], lag_ratio=0.12), rt=0.9)
            ul = lab("8 unanswerable", 34).move_to(P3(2.7, -1.9))
            p.play(FadeIn(ul), rt=0.3)
            p.finish()


class B09_Alternative(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B09", planned=3.6)
            xs = (-4.4, -2.2, 0.0, 2.2, 4.4)
            names = ("orders.py", "cart.py", "auth.py", "payments.py", "models.py")
            row = [page(1.0, 1.3, x, -0.2, fill=GHOST) for x in xs]
            nls = [lab(n, 32).move_to(P3(x, -1.25)) for n, x in zip(names, xs)]
            self.add(*row, *nls)
            mag = magnifier(xs[0] + 0.17, 1.25)
            p.play(FadeIn(mag), rt=0.4)   # "by hand" is now the subheading
            for i, x in enumerate(xs):
                if i > 0:
                    p.play(mag.animate.move_to(P3(x + 0.17, 1.25)), rt=0.35)
                if i != 2:
                    p.play(row[i].animate.set_fill(CARD), Create(tick(x, -0.2, s=0.24)), rt=0.3)
            ml = lab("missed file?", 36).move_to(P3(xs[2], -1.95))
            p.play(FadeIn(ml), rt=0.4)
            p.finish()


class B09B_Instead(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B09B", planned=2.6)
            src = page(2.2, 2.6, -3.0, -0.4)
            fl = lab("app/api/orders.py", 34).next_to(src, UP, buff=0.3)
            bars = [Rectangle(width=1.6, height=0.2, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                    .move_to(P3(-3.0, 0.5 - i * 0.45)) for i in range(5)]
            p.play(FadeIn(src), FadeIn(fl), *[FadeIn(b) for b in bars], rt=0.5)
            hi = [Rectangle(width=1.6, height=0.2, fill_color=BAR1, fill_opacity=1, stroke_width=0)
                  .move_to(P3(-3.0, 0.5 - i * 0.45)) for i in (2, 3)]
            p.play(*[FadeIn(h) for h in hi], GrowFromCenter(spark(-1.95, -0.2)), rt=0.5)
            ct = lab(CITE, 32).move_to(P3(2.2, 0.55))
            p.play(FadeIn(ct), rt=0.4)
            g = gauge(1.0, -2.0, r=0.8)
            gl = lab("misses: will measure", 32).move_to(P3(3.95, -1.75))
            p.play(Create(g[0]), FadeIn(g[1]), FadeIn(gl), rt=0.6)
            p.finish()


# ═════════════════════════════════ Q3: who opens it ═════════════════════════════
class B10_Reader(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B10", planned=2.9)
            readme = page(3.0, 2.8, 0.3, -0.3)
            band = Rectangle(width=2.6, height=0.32, fill_color=BAR1, fill_opacity=1,
                             stroke_width=0).move_to(P3(0.3, 0.8))
            p.play(FadeIn(readme), FadeIn(band), rt=0.5)
            rl = lab("README", 36).next_to(readme, UP, buff=0.3)
            p.play(FadeIn(rl), rt=0.3)
            rows = [Rectangle(width=2.6, height=0.3, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                    .move_to(P3(0.3, 0.2 - i * 0.6)) for i in range(3)]
            p.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25), rt=0.6)
            b1 = lab("baseline", 34).move_to(P3(-2.55, 0.2))
            b2 = lab("experiment 1", 34).move_to(P3(-2.85, -0.4))
            p.play(FadeIn(b1), FadeIn(b2), rt=0.4)
            p.play(GrowFromCenter(spark(1.3, 0.2)), FadeIn(magnifier(2.8, 0.75)), rt=0.5)
            al = lab("entry-level AI engineer", 34).move_to(P3(3.2, -2.3))
            p.play(FadeIn(al), rt=0.4)
            p.finish()


# ═════════════════════════════════ Q5: scope and first ══════════════════════════
class B11_Scope(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B11", planned=3.0)
            crate = slab(2.8, 1.1, -4.0, -1.2)
            files = [page(0.65, 0.85, x, -0.2) for x in (-4.85, -4.0, -3.15)]
            p.play(FadeIn(crate), *[FadeIn(f) for f in files], rt=0.6)
            il = lab("in scope", 36).move_to(P3(-4.0, 0.7))
            cl = lab("37 files", 36).next_to(crate, DOWN, buff=0.3)
            p.play(FadeIn(il), FadeIn(cl), rt=0.4)
            gate = block(0.3, 2.8, 0.4, -0.3)
            ol = lab("out of scope", 34).move_to(P3(0.4, 1.6))
            p.play(FadeIn(gate), FadeIn(ol), rt=0.5)
            specs = (("agents", 1.9, 0.5), ("fine-tuning", 3.4, -1.1), ("frameworks", 4.9, 0.5))
            outs = []
            for name, x, ly in specs:
                outs.append(VGroup(block(0.8, 0.8, x, -0.3), lab(name, 32).move_to(P3(x, ly))))
            p.play(*[FadeIn(o) for o in outs], rt=0.4)
            p.play(*[o.animate.shift(LEFT * 0.9) for o in outs], rt=0.6)
            p.play(*[o.animate.shift(RIGHT * 0.9) for o in outs], rt=0.5)
            p.finish()


class B12_First(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B12", planned=3.3)
            term = block(2.6, 1.4, -4.2, 1.1)
            tl = lab("one command", 34).next_to(term, DOWN, buff=0.3)
            p.play(FadeIn(term), FadeIn(tl), rt=0.4)
            line = Rectangle(width=1.8, height=0.14, fill_color=GHOST, fill_opacity=1,
                             stroke_width=0).move_to(P3(-4.3, 1.3))
            p.play(GrowFromEdge(line, LEFT), rt=0.4)
            p.play(Create(arrow(-2.8, 1.1, -1.65, 1.1)), rt=0.25)
            hn = block(1.9, 1.0, -0.6, 1.1)
            hl = lab("harness", 34).next_to(hn, DOWN, buff=0.3)
            p.play(FadeIn(hn), FadeIn(hl), rt=0.4)
            p.play(Create(arrow(0.45, 1.1, 1.65, 1.1)), rt=0.25)
            res = page(1.2, 1.4, 2.4, 1.1)
            rl = lab("results", 34).next_to(res, DOWN, buff=0.3)
            p.play(FadeIn(res), FadeIn(rl), rt=0.4)
            mx = (-2.0, -1.0, 0.0, 1.0)
            jl = lab("judge", 34).move_to(P3(-4.2, -1.5))
            p.play(FadeIn(jl), *[FadeIn(block(0.32, 0.32, x, -1.5)) for x in mx], rt=0.6)
            ml = lab("my labels", 34).move_to(P3(-4.2, -2.4))
            p.play(FadeIn(ml), *[GrowFromCenter(spark(x, -2.4, r=0.16)) for x in mx], rt=0.6)
            p.finish()


# ═════════════════════════════════ Q6: risk ═════════════════════════════════════
GAUGE_X, GAUGE_Y = 0.0, -2.1


class B13_Risk(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B13", planned=3.9)
            xs = row_xs(8, -3.3, w=0.6, gap=0.32)
            row = [page(0.6, 0.8, x, 1.4) for x in xs]
            p.play(LaggedStart(*[FadeIn(pg) for pg in row], lag_ratio=0.1), rt=0.7)
            p.play(*[pg.animate.shift(LEFT * 0.9) for pg in row[:6]],
                   *[pg.animate.shift(RIGHT * 0.9) for pg in row[6:]], rt=0.6)
            al = lab("about 6", 34).move_to(P3((xs[0] + xs[5]) / 2 - 0.9, 0.6))
            hl = lab("held out", 34).move_to(P3((xs[6] + xs[7]) / 2 + 0.9, 0.6))
            p.play(FadeIn(al), FadeIn(hl), rt=0.4)
            g = gauge(GAUGE_X, GAUGE_Y, r=1.1)
            nd = needle(GAUGE_X, GAUGE_Y, PI * 0.8, r=0.9)
            p.play(Create(g[0]), FadeIn(g[1]), FadeIn(nd), rt=0.5)
            p.play(nd.animate.rotate(-PI * 0.55, about_point=P3(GAUGE_X, GAUGE_Y)), rt=0.6)
            ol = lab("one refusal", 34).move_to(P3(2.9, -1.6))
            p.play(FadeIn(ol), rt=0.3)
            band = AnnularSector(inner_radius=1.25, outer_radius=1.6, angle=PI * 0.3, start_angle=PI * 0.1,
                                 arc_center=P3(GAUGE_X, GAUGE_Y), fill_color=BAR2, fill_opacity=1, stroke_width=0)
            cl = lab("raw counts", 34).move_to(P3(-3.0, -1.6))
            p.play(FadeIn(band), FadeIn(cl), rt=0.5)
            p.finish()


# ═════════════════════════════════ Built so far / will build ════════════════════
BUILT = ("53-question test set", "retrieval (run)", "prompt: cite or ABSTAIN")
WILL = ("scoring harness", "experiments", "write-up", "public GitHub repository")
ROW_Y = (0.9, -0.1, -1.1, -2.1)


def built_column():
    head = lab("Built so far", 40).move_to(P3(-3.6, 2.0))
    items = []
    for text, y in zip(BUILT, ROW_Y):
        m = block(0.42, 0.42, -5.6, y)
        items.append((m, lab(text, 34).next_to(m, RIGHT, buff=0.35)))
    return head, items


class B14_Built(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B14", planned=1.9)
            head, items = built_column()
            p.play(FadeIn(head), rt=0.4)
            for m, t in items:
                p.play(GrowFromCenter(m), FadeIn(t), rt=0.5)
            p.finish()


class B15_WillBuild(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B15", planned=1.9)
            head, items = built_column()
            self.add(head, *[x for pair in items for x in pair])
            wh = lab("Will build", 40).move_to(P3(2.5, 2.0))
            p.play(FadeIn(wh), rt=0.3)
            for text, y in zip(WILL, ROW_Y):
                m = Rectangle(width=0.42, height=0.42, stroke_color=INK, stroke_width=5).move_to(P3(0.8, y))
                p.play(Create(m), FadeIn(lab(text, 34).next_to(m, RIGHT, buff=0.35)), rt=0.4)
            p.finish()


# ═════════════════════════════════ Q7: why this project ═════════════════════════
class B16_Why(Scene):
    def construct(self):
        with serif_font():
            p = begin(self, "B16", planned=3.2)
            have = slab(2.4, 0.45, -4.7, -1.2)
            hl = lab("have", 36).next_to(have, DOWN, buff=0.3)
            p.play(FadeIn(have), FadeIn(hl), rt=0.4)
            ev = block(1.2, 0.9, -4.7, -0.5)
            p.play(FadeIn(ev, shift=DOWN * 0.8), rt=0.5)
            p.play(FadeIn(lab("evaluation", 34).next_to(ev, UP, buff=0.3)), rt=0.3)
            new = slab(6.4, 0.45, 2.3, -1.2)
            nl = lab("new", 36).next_to(new, DOWN, buff=0.3)
            p.play(FadeIn(new), FadeIn(nl), rt=0.4)
            names = ("retrieval", "embeddings", "LLM judge")
            blocks = [block(0.75, 0.75, x, -0.6) for x in (-0.2, 2.3, 4.8)]
            for b in blocks:
                p.play(FadeIn(b, shift=DOWN * 0.8), rt=0.4)
            p.play(*[FadeIn(lab(n, 32).next_to(b, UP, buff=0.3)) for n, b in zip(names, blocks)], rt=0.4)
            p.finish()


# ═════════════════════════════════ Outro ════════════════════════════════════════
class BOUT_Close(Scene):
    """Title card: exactly the title and the handle (matches BOUT's bookend props). No screen tag."""

    def construct(self):
        with serif_font():
            p = begin(self, "BOUT", planned=1.6, tagged=False)
            title = Text("Cite & Seek", font=SERIF, color=INK, font_size=110).move_to(P3(0, 0.55))
            p.play(FadeIn(title), rt=0.6)
            # One underline drawn in two halves: Gate A needs two distinct shape states.
            left = Rectangle(width=1.6, height=0.06, fill_color=INK, fill_opacity=1,
                             stroke_color=INK, stroke_width=2).move_to(P3(-0.8, -0.35))
            right = Rectangle(width=1.6, height=0.06, fill_color=INK, fill_opacity=1,
                              stroke_color=INK, stroke_width=2).move_to(P3(0.8, -0.35))
            p.play(GrowFromEdge(left, RIGHT), rt=0.25)
            p.play(GrowFromEdge(right, LEFT), rt=0.25)
            handle = Text("@meenuviji", font=SERIF, color=INK, font_size=52).move_to(P3(0, -1.05))
            p.play(FadeIn(handle), rt=0.5)
            p.finish()
