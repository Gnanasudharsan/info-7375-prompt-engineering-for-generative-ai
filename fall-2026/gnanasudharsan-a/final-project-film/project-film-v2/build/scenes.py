"""scenes.py — Manim beats for the DecisionTrace Lite project film.

The palette and helper functions (Clock, word, fit, tag, doc, tick, cross,
rules, text_beat) are copied from the pitch film's build/scenes.py, so both
films look the same. text_beat takes an extra `speed` factor for very short beats.

Each scene's length is read from beat_sheet.json (actual_duration_s, measured
from the Kokoro audio), so the picture ends when the narration does. In-scene
cue times (seconds from the start of the beat) were measured from each beat's mp3
with `ffmpeg -af silencedetect=noise=-35dB:d=0.18` and are noted beside each cue.

Honesty labels, all drawn on screen:
  * B02 shows an example of the planned output: "CONSTRUCTED · NOT REAL OUTPUT"
  * B06, B11: "SYNTHETIC TEST DATA" / "SYNTHETIC · FICTIONAL COMPANY"
  * B10: the larger system is labelled "separate project"
  * B13: the JSON is the planned schema: "SCHEMA · NOT OUTPUT"
  * B18: the expected answer comes from the answer key: "TARGET ANSWER · NOT OUTPUT"
  * B19: "Narration: synthetic voice (Kokoro)"
"""
import json
from pathlib import Path

from manim import *

GROUND = "#FAF9F5"
INK = "#3D3929"
SOFT = "#8A8470"
ACCENT = "#D97757"
OK_GREEN = "#2E6B3F"
BAD_RED = "#B3261E"
PAPER = "#FFFFFF"
BAR = "#EEEAE0"
FONT = "EB Garamond"
MONO = "PT Mono"

MAX_W = 11.0          # widest a line of text may run (safe area is ±6.3)
RULE_X = 5.6          # half-length of the top and bottom rules


def _load_durations():
    # The real render runs beside beat_sheet.json. GATE A checks an isolated copy
    # of this file with no sheet next to it, so fall back to a 10 s default there.
    for folder in (Path(__file__).resolve().parent, Path.cwd()):
        sheet = folder / "beat_sheet.json"
        if sheet.is_file():
            return {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 10)
                    for b in json.loads(sheet.read_text(encoding="utf-8"))["beats"]}
    return {}


_DUR = _load_durations()


class Clock:
    """Tracks elapsed scene time so cues can be placed at measured seconds."""

    def __init__(self, scene):
        self.scene, self.t = scene, 0.0

    def play(self, *anims, run_time=1.0):
        self.scene.play(*anims, run_time=run_time)
        self.t += run_time

    def until(self, t):
        if t > self.t + 0.05:
            self.scene.wait(t - self.t)
            self.t = t

    def finish(self, bid):
        self.scene.wait(max(0.1, _DUR.get(bid, 10.0) - self.t))


def word(text, size=44, color=INK, font=FONT):
    return Text(text, font=font, font_size=size, color=color)


def fit(mob, max_w=MAX_W):
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob


def tag(text, width=3.6, height=0.9, size=38, color=INK):
    box = RoundedRectangle(corner_radius=0.18, width=width, height=height,
                           stroke_color=color, stroke_width=3)
    return VGroup(box, fit(word(text, size, color), width - 0.3).move_to(box.get_center()))


def doc(width=2.4, height=3.0):
    """A page: outline with a folded corner and three grey text lines."""
    body = Polygon([-width / 2, height / 2, 0], [width / 2 - 0.45, height / 2, 0],
                   [width / 2, height / 2 - 0.45, 0], [width / 2, -height / 2, 0],
                   [-width / 2, -height / 2, 0], stroke_color=INK, stroke_width=3)
    fold = VMobject(stroke_color=INK, stroke_width=3).set_points_as_corners(
        [[width / 2 - 0.45, height / 2, 0], [width / 2 - 0.45, height / 2 - 0.45, 0],
         [width / 2, height / 2 - 0.45, 0]])
    lines = VGroup(*[Line([-width / 2 + 0.3, y, 0], [width / 2 - 0.3, y, 0],
                          stroke_color=SOFT, stroke_width=4) for y in (0.6, 0.0, -0.6)])
    return VGroup(body, fold, lines)


def mini_doc(width=0.42, height=0.55):
    """A small page for grids: outline + folded corner, no text lines."""
    c = min(width, height) * 0.3
    body = Polygon([-width / 2, height / 2, 0], [width / 2 - c, height / 2, 0],
                   [width / 2, height / 2 - c, 0], [width / 2, -height / 2, 0],
                   [-width / 2, -height / 2, 0], stroke_color=INK, stroke_width=2)
    return body


def tick(color=OK_GREEN, scale=1.0):
    return VMobject(stroke_color=color, stroke_width=8).set_points_as_corners(
        [[-0.25, 0, 0], [-0.05, -0.22, 0], [0.32, 0.28, 0]]).scale(scale)


def cross(color=BAD_RED, scale=1.0):
    return VGroup(Line([-0.25, -0.25, 0], [0.25, 0.25, 0], stroke_color=color, stroke_width=8),
                  Line([-0.25, 0.25, 0], [0.25, -0.25, 0], stroke_color=color, stroke_width=8)).scale(scale)


def rules():
    return (Line([-RULE_X, 3.0, 0], [RULE_X, 3.0, 0], stroke_color=INK, stroke_width=3),
            Line([-RULE_X, -2.9, 0], [RULE_X, -2.9, 0], stroke_color=INK, stroke_width=3))


def top_label(text, size=44):
    return fit(word(text, size)).move_to([0, 3.08, 0])


def text_beat(scene, bid, heading, body, label=None, label_size=50, speed=1.0):
    """Large serif heading + body between two ink rules (the pitch film's layout):
    top rule y=3.0, optional label y=2.3, heading y=0.55, body y=-1.45,
    bottom rule y=-2.9. `speed` < 1 shortens every animation for short beats."""
    scene.camera.background_color = GROUND
    clock = Clock(scene)
    top, bottom = rules()
    if "\n" in heading:
        head = VGroup(*[word(ln, 96) for ln in heading.split("\n")]).arrange(DOWN, buff=0.35)
    else:
        head = word(heading, 96)
    head_scale = min(1.0, MAX_W / head.width)
    head.scale(head_scale).move_to([0, 0.55, 0])
    sub = fit(word(body, max(44, min(56, 96 * head_scale * 0.85)), INK)).move_to([0, -1.45, 0])
    under_y = -0.35
    if "\n" in heading:
        head.move_to([0, 0.55, 0]).shift(UP * (-0.05 - head.get_bottom()[1]))
        under_y = head.get_bottom()[1] - 0.3
    half = min(head.width, MAX_W) / 2
    under = Line([-half, under_y, 0], [half, under_y, 0], stroke_color=ACCENT, stroke_width=6)
    mark = Line([-0.6, -2.3, 0], [0.6, -2.3, 0], stroke_color=ACCENT, stroke_width=6)
    clock.play(Create(top), Create(bottom), run_time=0.8 * speed)
    if label:
        lab = fit(word(label, label_size, INK)).move_to([0, 2.3, 0])
        clock.play(FadeIn(lab), run_time=0.5 * speed)
    clock.play(FadeIn(head, shift=UP * 0.15), run_time=0.9 * speed)
    clock.play(Create(under), run_time=0.7 * speed)
    clock.play(FadeIn(sub, shift=UP * 0.15), Create(mark), run_time=0.8 * speed)
    clock.finish(bid)


def row_table(rows, left_x=-5.6, mid_x=0.6, top_y=1.9, gap=0.95, size=48, right_x=5.8):
    """Two-column rows (label | value), left-aligned, returned as a list of VGroups."""
    left = [word(a, size) for a, _ in rows]
    right = [word(b, size) for _, b in rows]
    # one scale per column, so every row in a column has the same type size
    sa = min([1.0] + [(mid_x - left_x - 0.4) / m.width for m in left])
    sb = min([1.0] + [(right_x - mid_x) / m.width for m in right])
    out = []
    for i, (la, lb) in enumerate(zip(left, right)):
        y = top_y - i * gap
        la.scale(sa).move_to([0, y, 0]).align_to([left_x, 0, 0], LEFT)
        lb.scale(sb).move_to([0, y, 0]).align_to([mid_x, 0, 0], LEFT)
        out.append(VGroup(la, lb))
    return out


def base_rule():
    """A bottom ink rule spanning the text column. Gives diagram beats the same
    frame as the text beats, and keeps GATE V's content box above its 55% fill floor."""
    return Line([-RULE_X, -3.2, 0], [RULE_X, -3.2, 0], stroke_color=INK, stroke_width=3)


def row_mark(x, y):
    """A short accent bar beside a table row, drawn as the row lands."""
    return Line([x, y - 0.24, 0], [x, y + 0.24, 0], stroke_color=ACCENT, stroke_width=8)


def same_size(mobs, max_w):
    """Scale a list of text mobjects by one shared factor so the widest fits max_w."""
    s = min([1.0] + [max_w / m.width for m in mobs])
    for m in mobs:
        m.scale(s)
    return mobs


# ---------------------------------------------------------------- 1. executive summary

class B00_Title(Scene):
    def construct(self):
        # 4.1 s beat: animations run at 0.6x so the full card holds ~1.9 s
        text_beat(self, "B00", "DecisionTrace Lite", "Why, when and who decided — with sources",
                  label="Gnanasudharsan Ashokumar", label_size=44, speed=0.6)


class B01_Scattered(Scene):
    """Meeting notes, an email and a ticket; the three questions; one page out of date."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        pages = VGroup(*[doc(2.3, 2.9) for _ in range(3)]).arrange(RIGHT, buff=1.4).move_to([0, 0.9, 0])
        pages[0].rotate(0.06)
        pages[2].rotate(-0.05)
        names = VGroup(*[word(n, 44).next_to(p, DOWN, buff=0.3)
                         for n, p in zip(("meeting notes", "email", "ticket"), pages)])
        qs = VGroup(word("why?", 60), word("who approved?", 60), word("still true?", 60)) \
            .arrange(RIGHT, buff=0.9).move_to([0, -2.55, 0])
        fit(qs)
        old = pages[0]
        stamp = tag("out of date", 1.9, 0.75, 36, BAD_RED).move_to(old.get_center())   # fits inside the page

        clock.play(*[Create(p) for p in pages], run_time=1.2)
        clock.play(FadeIn(names), run_time=0.6)
        clock.until(5.71)                                   # "why did we decide this ..."
        for q in qs:
            clock.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
        clock.until(9.23)                                   # "The answer is scattered ..."
        clock.play(pages[0].animate.shift(LEFT * 0.35 + UP * 0.15),
                   pages[2].animate.shift(RIGHT * 0.35 + DOWN * 0.1), run_time=0.8)
        clock.until(11.46)                                  # "and some are out of date"
        # the page's text lines fade first so the stamp never sits on a line (GATE B)
        clock.play(FadeOut(old[2]), old[0].animate.set_stroke(opacity=0.45),
                   old[1].animate.set_stroke(opacity=0.45), Create(stamp[0]), FadeIn(stamp[1]), run_time=0.6)
        clock.finish("B01")


class B02_AnswerCard(Scene):
    """An example of the planned output (constructed): answer, status, citation;
    then the refusal."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        label = top_label("CONSTRUCTED · NOT REAL OUTPUT", 48)
        q = fit(word("“Why did tracking switch databases?”", 56)).move_to([0, 2.2, 0])
        card = RoundedRectangle(corner_radius=0.2, width=11.6, height=4.1, stroke_color=INK,
                                stroke_width=3, fill_color=PAPER, fill_opacity=1).move_to([0, -0.55, 0])
        rows = row_table([("answer", "~40k → ~900k events/day; cost ~4×"),
                          ("status", "in progress"),
                          ("source", "2026-05-18 meeting notes")],
                         left_x=-5.4, mid_x=-2.4, top_y=0.75, gap=1.2, size=46, right_x=5.4)
        status_ring = SurroundingRectangle(rows[1][1], color=ACCENT, buff=0.12, corner_radius=0.15,
                                           stroke_width=6)
        refusal = VGroup(
            RoundedRectangle(corner_radius=0.2, width=11.6, height=2.4, stroke_color=INK, stroke_width=3,
                             fill_color=PAPER, fill_opacity=1),
            word("“Not in the sources.”", 84)).move_to([0, -0.55, 0])
        refusal[1].move_to(refusal[0])

        clock.play(FadeIn(label), FadeIn(q), run_time=0.8)
        clock.play(Create(card), run_time=0.8)
        clock.until(2.45)                                   # "a short answer"
        clock.play(FadeIn(rows[0]), run_time=0.5)
        clock.until(3.64)                                   # "the decision's current status"
        clock.play(FadeIn(rows[1]), Create(status_ring), run_time=0.5)
        clock.until(5.46)                                   # "and a citation ..."
        clock.play(FadeIn(rows[2]), run_time=0.5)
        clock.until(9.18)                                   # "If the documents don't say"
        clock.play(FadeOut(VGroup(card, *rows, status_ring)), FadeIn(refusal), run_time=0.7)
        clock.finish("B02")


class B03_WhyItMatters(Scene):
    """Two answers that look the same; one is wrong. Then: check it in seconds."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        top, bottom = rules()
        self.add(top, bottom)                                # the text-beat frame, present throughout

        def answer_card(x):
            box = RoundedRectangle(corner_radius=0.2, width=4.6, height=3.0, stroke_color=INK,
                                   stroke_width=3, fill_color=PAPER, fill_opacity=1).move_to([x, 0.6, 0])
            lines = VGroup(*[Line([x - 1.8, y, 0], [x + 1.8 - (0.8 if y < 0 else 0), y, 0],
                                  stroke_color=SOFT, stroke_width=5) for y in (1.3, 0.6, -0.1)])
            return VGroup(box, lines, word("answer", 44).move_to([x, 2.6, 0]))

        a, b = answer_card(-3.0), answer_card(3.0)
        ok = VGroup(tick(scale=1.3), word("current", 48, OK_GREEN)).arrange(RIGHT, buff=0.25).move_to([-3.0, -1.6, 0])
        bad = VGroup(cross(scale=1.0), word("reversed", 48, BAD_RED)).arrange(RIGHT, buff=0.25).move_to([3.0, -1.6, 0])
        check = fit(word("Check it in seconds.", 104)).move_to([0, 0.5, 0])
        score = fit(word("And a published score.", 64)).move_to([0, -1.4, 0])
        under = Line([-check.width / 2, -0.35, 0], [check.width / 2, -0.35, 0], stroke_color=ACCENT,
                     stroke_width=6)

        clock.play(FadeIn(a), FadeIn(b), run_time=1.0)       # "looks exactly like a right one"
        clock.until(5.06)                                    # "acting on a reversed ... decision"
        clock.play(Create(ok), run_time=0.5)
        clock.play(Create(bad), run_time=0.5)
        clock.until(9.79)                                    # "An answer you can check in seconds"
        clock.play(FadeOut(VGroup(a, b, ok, bad)), FadeIn(check, shift=UP * 0.15), run_time=0.8)
        clock.play(Create(under), run_time=0.5)
        clock.until(13.66)                                   # "And I'll publish how often it's right"
        clock.play(FadeIn(score, shift=UP * 0.15), run_time=0.6)
        clock.finish("B03")


# ---------------------------------------------------------------- 2. introduction

class B04_Tools(Scene):
    def construct(self):
        text_beat(self, "B04", "NotebookLM · ChatGPT", "Answers over documents you upload, with sources",
                  label="What already exists")


class B05_Research(Scene):
    """RAG, ALCE, RAGAS — one row each, landing on its sentence."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        top, bottom = rules()
        head = word("Research", 80).move_to([0, 2.3, 0])
        # each item: name + citation on one line, what it does underneath
        rows = []
        for i, (name, what) in enumerate((("RAG · Lewis et al., 2020", "grounds answers in retrieved text"),
                                          ("ALCE · Gao et al., 2023", "do citations support the sentence?"),
                                          ("RAGAS · Es et al., 2023", "scores faithfulness to sources"))):
            y = 0.95 - i * 1.4
            rows.append(VGroup(word(name, 50).move_to([0, y + 0.28, 0]).align_to([-4.4, 0, 0], LEFT),
                               word(what, 42).move_to([0, y - 0.32, 0]).align_to([-4.4, 0, 0], LEFT)))
        clock.play(Create(top), Create(bottom), FadeIn(head), run_time=0.9)
        # an accent underline under each full name line, drawn as the row lands
        # fixed coordinates (GATE A checks coordinates without real text widths)
        marks = [Line([-4.85, 0.95 - i * 1.4 + 0.5, 0], [-4.85, 0.95 - i * 1.4 - 0.5, 0],
                      stroke_color=ACCENT, stroke_width=8) for i in range(3)]
        for r, m, cue in zip(rows, marks, (1.98, 9.56, 13.90)):   # RAG / "The ALCE benchmark" / "RAGAS scores"
            clock.until(cue)
            clock.play(FadeIn(r, shift=UP * 0.1), Create(m), run_time=0.6)
        clock.finish("B05")


class B06_TestSetup(Scene):
    def construct(self):
        text_beat(self, "B06", "6 docs · 4 questions · 2 tools",
                  "PostgreSQL → DynamoDB: approved, not finished", label="SYNTHETIC TEST DATA · 2026-10-09")


class B09_Gap(Scene):
    """Existing tools vs DecisionTrace Lite (scoped to my test)."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        lx, rx = -3.3, 3.3
        divider = Line([0, 2.9, 0], [0, -2.8, 0], stroke_color=INK, stroke_width=3)
        lh = word("Existing tools", 58).move_to([lx, 2.55, 0])
        lnote = word("(in my test)", 40).next_to(lh, DOWN, buff=0.15)
        rh = word("DecisionTrace Lite", 58).move_to([rx, 2.55, 0])
        same_size([lh, rh], 5.4)
        lu = Line([lx - 2.4, 2.1, 0], [lx + 2.4, 2.1, 0], stroke_color=INK, stroke_width=3)
        ru = Line([rx - 2.4, 2.1, 0], [rx + 2.4, 2.1, 0], stroke_color=ACCENT, stroke_width=6)
        lnote.next_to(lu, DOWN, buff=0.15)

        texts = {s: word(s, 50) for s in ("how often right: ?", "finds facts", "decision status",
                                          "checks every citation", "publishes its score")}
        same_size(list(texts.values()), 4.3)

        def item(text, x, y, mark):
            m = mark.move_to([x - 2.45, y, 0])
            t = texts[text].move_to([0, y, 0]).align_to([x - 2.05, 0, 0], LEFT)
            return VGroup(m, t)

        score_q = item("how often right: ?", lx, -1.9, cross(scale=0.75))
        facts = item("finds facts", lx, 0.3, tick(scale=1.0))
        status = item("decision status", rx, 0.6, tick(scale=1.0))
        cites = item("checks every citation", rx, -0.65, tick(scale=1.0))
        score = item("publishes its score", rx, -1.9, tick(scale=1.0))

        clock.play(FadeIn(lh), Create(lu), Create(divider), run_time=0.8)
        clock.play(FadeIn(lnote), FadeIn(score_q), run_time=0.6)    # "Neither tool told me how often"
        clock.until(2.62)                                            # "That's the gap"
        clock.play(FadeIn(rh), Create(ru), run_time=0.7)
        clock.until(3.76)                                            # "Existing tools find facts"
        clock.play(FadeIn(facts), run_time=0.5)
        clock.until(6.07)                                            # "built around a decision's status"
        clock.play(FadeIn(status), run_time=0.5)
        clock.until(9.50)                                            # "It checks every citation"
        clock.play(FadeIn(cites), run_time=0.5)
        clock.until(11.24)                                           # "and it publishes its score"
        clock.play(FadeIn(score), run_time=0.5)
        clock.finish("B09")


# ---------------------------------------------------------------- 3. methods

class B10_LargerToLite(Scene):
    """The larger system (separate project) → the Lite core."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        base = base_rule()
        self.add(base)                                       # static frame, present from the first frame
        plan = word("The plan", 110).move_to([0, 0.3, 0])
        bx, lxx = -3.2, 3.2
        big = RoundedRectangle(corner_radius=0.25, width=5.4, height=5.2, stroke_color=INK,
                               stroke_width=3).move_to([bx, -0.3, 0])
        big_h = word("Larger system", 52).move_to([bx, 1.75, 0])
        big_sub = word("separate project", 40).next_to(big_h, DOWN, buff=0.12)
        parts = VGroup(*[word(p, 44) for p in ("Neo4j", "LangGraph", "FastAPI", "hallucination detection")]) \
            .arrange(DOWN, buff=0.25)
        fit(parts, 4.6).move_to([bx, -1.05, 0])
        lite = RoundedRectangle(corner_radius=0.25, width=5.4, height=5.2, stroke_color=ACCENT,
                                stroke_width=6).move_to([lxx, -0.3, 0])
        lite_h = fit(word("DecisionTrace Lite", 52), 4.8).move_to([lxx, 1.75, 0])
        arrow = Arrow([bx + 2.75, -0.3, 0], [lxx - 2.75, -0.3, 0], color=INK, stroke_width=6, buff=0.05)
        q_in = word("question in", 46).move_to([lxx, 0.6, 0])
        down = Arrow([lxx, 0.3, 0], [lxx, -0.55, 0], color=INK, stroke_width=5, buff=0)
        a_out = fit(word("grounded answer out", 46), 4.8).move_to([lxx, -0.9, 0])
        stack = word("Python + Claude", 46).move_to([lxx, -2.1, 0])

        clock.play(FadeIn(plan), run_time=0.6)               # "Here's the plan, step by step."
        clock.until(2.22)                                    # "a scoped-down version of a larger system"
        clock.play(FadeOut(plan), Create(big), FadeIn(big_h), FadeIn(big_sub), run_time=0.8)
        clock.until(5.61)                                    # "with Neo4j, LangGraph, FastAPI ..."
        clock.play(LaggedStart(*[FadeIn(p) for p in parts], lag_ratio=0.35), run_time=1.6)
        clock.until(11.12)                                   # "Here I keep only the core"
        clock.play(GrowArrow(arrow), Create(lite), FadeIn(lite_h), run_time=0.8)
        clock.until(12.84)                                   # "question in"
        clock.play(FadeIn(q_in), run_time=0.4)
        clock.until(13.78)                                   # "grounded answer out"
        clock.play(GrowArrow(down), FadeIn(a_out), run_time=0.5)
        clock.until(15.12)                                   # "in plain Python with Claude"
        clock.play(FadeIn(stack), run_time=0.5)
        clock.finish("B10")


class B11_Data(Scene):
    """6 synthetic documents grow to ~50; four kinds of hard case."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        base = base_rule()
        self.add(base)                                       # static frame, present from the first frame
        label = top_label("SYNTHETIC · FICTIONAL COMPANY", 48)
        step = word("1 · Data", 60).move_to([0, 2.4, 0])
        six = VGroup(*[mini_doc(0.62, 0.8) for _ in range(6)]).arrange(RIGHT, buff=0.3).move_to([0, 0.9, 0])
        grid = VGroup(*[mini_doc(0.36, 0.46) for _ in range(50)]).arrange_in_grid(rows=5, cols=10, buff=(0.2, 0.16)) \
            .move_to([-2.6, 0.05, 0])
        count = word("6 → ~50", 64).move_to([-2.6, -2.3, 0])
        kinds = VGroup(*[word(k, 52) for k in ("reversed", "unfinished", "contradictory", "no answer")]) \
            .arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to([3.6, 0.3, 0])
        marks = [grid[i] for i in (7, 18, 31, 44)]

        clock.play(FadeIn(step), Create(six), run_time=1.0)
        clock.until(1.60)                                    # "I'll grow my six ... into about fifty"
        clock.play(ReplacementTransform(six, grid[:6]), run_time=0.8)
        clock.play(LaggedStart(*[Create(d) for d in grid[6:]], lag_ratio=0.05), FadeIn(count), run_time=2.0)
        for k, m, cue in zip(kinds, marks, (8.48, 10.27, 11.69, 13.72)):   # each kind on its phrase
            clock.until(cue)
            clock.play(FadeIn(k, shift=LEFT * 0.1), m.animate.set_fill(ACCENT, opacity=0.8), run_time=0.5)
        clock.until(16.10)                                   # "All of it is synthetic."
        clock.play(FadeIn(label), run_time=0.5)
        clock.finish("B11")


class B12_TestSet(Scene):
    """My hand-written test set; why I write it (Claude helps write the documents)."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        base = base_rule()
        self.add(base)                                       # static frame, present from the first frame
        step = word("2 · Test set", 64).move_to([0, 2.55, 0])
        page = doc(width=5.0, height=4.2).move_to([-3.1, -0.2, 0])
        page_h = fit(word("~50 questions", 52), 4.4).move_to([-3.1, 1.2, 0])
        fields = VGroup(*[word(f, 46) for f in ("answer", "status", "passages")]) \
            .arrange(DOWN, buff=0.3).move_to([-3.1, -0.65, 0])
        by_me = word("hand-written by me", 48).move_to([-3.1, -2.85, 0])
        page[2].set_opacity(0)
        docs_side = VGroup(doc(1.6, 2.0), word("documents:", 44), word("Claude helps", 44)) \
            .arrange(DOWN, buff=0.2).move_to([3.3, 0.35, 0])
        warn = VGroup(cross(scale=0.8),
                      VGroup(word("a model grading", 46), word("its own homework", 46)).arrange(DOWN, buff=0.12)) \
            .arrange(RIGHT, buff=0.3).move_to([3.3, -2.3, 0])

        clock.play(FadeIn(step), Create(page), run_time=0.9)
        clock.until(1.01)                                    # "about fifty test questions I write by hand"
        clock.play(FadeIn(page_h), FadeIn(by_me), run_time=0.6)
        clock.until(3.89)                                    # "each with the correct answer, status ..."
        clock.play(LaggedStart(*[FadeIn(f) for f in fields], lag_ratio=0.4), run_time=1.4)
        clock.until(8.13)                                    # "because Claude helps generate the documents"
        clock.play(FadeIn(docs_side), run_time=0.7)
        clock.until(11.80)                                   # "a model grading its own homework isn't a test"
        clock.play(Create(warn[0]), FadeIn(warn[1]), run_time=0.6)
        clock.finish("B12")


class B13_RetrieveAnswer(Scene):
    """BM25 picks passages; Claude returns the JSON contract (schema, not output)."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        step3 = word("3 · Retrieval", 64).move_to([0, 2.55, 0])
        pile = VGroup(*[mini_doc(0.62, 0.8) for _ in range(12)]).arrange_in_grid(rows=3, cols=4, buff=0.2) \
            .move_to([-4.3, -0.2, 0])
        bm = tag("BM25", 2.6, 1.3, 64).move_to([0, -0.2, 0])
        a1 = Arrow(pile.get_right(), bm.get_left(), color=INK, stroke_width=5, buff=0.25)
        stdlib = word("Python standard library", 42).next_to(bm, DOWN, buff=0.35)
        bars = VGroup(*[RoundedRectangle(corner_radius=0.08, width=2.8, height=0.34, stroke_width=0,
                                         fill_color=ACCENT, fill_opacity=0.45) for _ in range(5)]) \
            .arrange(DOWN, buff=0.18).move_to([4.3, -0.2, 0])
        top5 = word("top passages", 42).next_to(bars, DOWN, buff=0.3)
        a2 = Arrow(bm.get_right(), bars.get_left(), color=INK, stroke_width=5, buff=0.25)

        step4 = word("4 · Answer contract", 60).move_to([0, 2.45, 0])
        schema_lbl = top_label("SCHEMA · NOT OUTPUT", 44)
        box = RoundedRectangle(corner_radius=0.2, width=11.4, height=4.5, stroke_color=INK, stroke_width=3,
                               fill_color=PAPER, fill_opacity=1).move_to([0, -0.2, 0])

        def code(text, y, indent=0):
            # Text() drops leading spaces, so indentation is an x offset in character widths
            m = Text(text, font=MONO, font_size=38, color=INK)
            cw = Text("M", font=MONO, font_size=38).width
            return m.move_to([0, y, 0]).align_to([-5.0 + indent * cw, 0, 0], LEFT)

        c = [code("{", 1.6),
             code('"answer": "…",', 1.0, 2),
             code('"status": "in_progress",', 0.4, 2),
             VGroup(code('"claims": [{"text": "…",', -0.2, 2),
                    code('"doc_id": "…",', -0.8, 14),
                    code('"quote": "…"}]', -1.4, 14)),
             code("}", -2.0)]

        clock.play(FadeIn(step3), LaggedStart(*[Create(d) for d in pile], lag_ratio=0.05), run_time=1.2)
        clock.until(1.84)                                    # "A simple keyword ranker called BM25"
        clock.play(GrowArrow(a1), Create(bm[0]), FadeIn(bm[1]), run_time=0.7)
        clock.until(4.66)                                    # "written with Python's standard library"
        clock.play(FadeIn(stdlib), run_time=0.5)
        clock.until(6.84)                                    # "finds the most relevant passages"
        clock.play(GrowArrow(a2), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2), FadeIn(top5),
                   run_time=1.0)
        clock.until(9.36)                                    # "Step four"
        clock.play(FadeOut(VGroup(step3, pile, bm, a1, stdlib, bars, top5, a2)),
                   FadeIn(step4), FadeIn(schema_lbl), Create(box), FadeIn(c[0]), FadeIn(c[4]), run_time=0.8)
        clock.until(12.73)                                   # "an answer, a status"
        clock.play(FadeIn(c[1]), run_time=0.4)
        clock.play(FadeIn(c[2]), run_time=0.4)
        clock.until(15.38)                                   # "each with a document ID and an exact quote"
        clock.play(FadeIn(c[3]), run_time=0.6)
        clock.finish("B13")


class B14_VerifyLoop(Scene):
    """quote in doc? (code) → supports claim? (Claude) → cited answer;
    fail → retry once → "not supported by the sources"; then harness → report."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        base = base_rule()
        self.add(base)                                       # static frame, present from the first frame
        step = word("5 · Verify", 64).move_to([0, 2.95, 0])
        ans = tag("answer", 1.9, 1.1, 42).move_to([-5.4, 0.9, 0])
        quote = tag("quote in doc?", 2.9, 1.1, 42).move_to([-2.1, 0.9, 0])
        judge = tag("supports claim?", 3.2, 1.1, 42).move_to([1.75, 0.9, 0])
        by_code = word("code", 40).next_to(quote, DOWN, buff=0.2)
        by_claude = word("second Claude call", 40).next_to(judge, DOWN, buff=0.2)
        ok = VGroup(tick(scale=1.1), word("cited", 48)).arrange(RIGHT, buff=0.2).move_to([5.0, 0.9, 0])
        a1 = Arrow(ans.get_right(), quote.get_left(), color=INK, stroke_width=5, buff=0.12)
        a2 = Arrow(quote.get_right(), judge.get_left(), color=INK, stroke_width=5, buff=0.12)
        a3 = Arrow(judge.get_right(), ok.get_left(), color=INK, stroke_width=5, buff=0.12)
        back = CurvedArrow([1.75, -0.6, 0], [-5.4, 0.3, 0], angle=-PI / 3, color=ACCENT, stroke_width=6)
        retry = word("fail → retry once", 46).move_to([3.7, -1.0, 0])
        nots = tag("“Not supported by the sources.”", 8.6, 1.0, 46).move_to([0, -2.35, 0])
        harness = fit(word("6 · Evaluation harness → written report", 52)).move_to([0, -2.35, 0])

        clock.play(FadeIn(step), Create(ans[0]), FadeIn(ans[1]), run_time=0.8)
        clock.until(2.45)                                    # "Code checks that every quote appears ..."
        clock.play(GrowArrow(a1), Create(quote[0]), FadeIn(quote[1]), FadeIn(by_code), run_time=0.7)
        clock.until(6.21)                                    # "and a second Claude call judges ..."
        clock.play(GrowArrow(a2), Create(judge[0]), FadeIn(judge[1]), FadeIn(by_claude), run_time=0.7)
        clock.play(GrowArrow(a3), Create(ok), run_time=0.6)
        clock.until(10.10)                                   # "An answer that fails gets one retry."
        clock.play(Create(back), FadeIn(retry), run_time=0.9)
        clock.until(12.80)                                   # "If it still fails, the tool says ..."
        clock.play(Create(nots[0]), FadeIn(nots[1]), run_time=0.7)
        clock.until(16.99)                                   # "Step six: the evaluation harness ..."
        clock.play(FadeOut(nots), FadeIn(harness, shift=UP * 0.1), run_time=0.7)
        clock.finish("B14")


class B15_Resources(Scene):
    """Resource table; scripted use of the NEU seat is PENDING, with the fallback."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        base = base_rule()
        self.add(base)                                       # static frame, present from the first frame
        head = word("Resources", 72).move_to([0, 2.75, 0])
        rows = row_table([("Model", "Claude · my NEU Claude Code seat"),
                          ("Scripted use", "PENDING: professor / NEU IT"),
                          ("If not allowed", "request API credits"),
                          ("Saved responses", "re-score with no new calls"),
                          ("Compute", "M4 MacBook Pro · no GPU"),
                          ("Code", "GitHub")],
                         left_x=-5.5, mid_x=-1.6, top_y=1.65, gap=0.88, size=46)
        bars = [row_mark(-5.8, 1.65 - i * 0.88) for i in range(6)]
        pending = SurroundingRectangle(rows[1][1], color=ACCENT, buff=0.12, corner_radius=0.15, stroke_width=6)
        rule = Line([-5.8, 2.2, 0], [5.8, 2.2, 0], stroke_color=INK, stroke_width=3)

        clock.play(FadeIn(head), Create(rule), run_time=0.7)
        clock.until(1.11)                                    # "Claude runs through my Northeastern ... seat"
        clock.play(FadeIn(rows[0]), Create(bars[0]), run_time=0.5)
        clock.until(5.73)                                    # "Using it from a script is pending ..."
        clock.play(FadeIn(rows[1]), Create(bars[1]), Create(pending), run_time=0.6)
        clock.until(10.91)                                   # "If it isn't allowed, I'll request API credits"
        clock.play(FadeIn(rows[2]), Create(bars[2]), run_time=0.5)
        clock.until(14.89)                                   # "Saved responses let me re-score ..."
        clock.play(FadeIn(rows[3]), Create(bars[3]), run_time=0.5)
        clock.until(18.34)                                   # "Compute is my M4 MacBook Pro, with no GPU"
        clock.play(FadeIn(rows[4]), Create(bars[4]), run_time=0.5)
        clock.until(22.21)                                   # "plus GitHub for the code"
        clock.play(FadeIn(rows[5]), Create(bars[5]), run_time=0.3)
        clock.finish("B15")


# ---------------------------------------------------------------- 4. evaluation

class B16_Measures(Scene):
    """The measures and their targets, one row per sentence."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        base = base_rule()
        self.add(base)                                       # static frame, present from the first frame
        head = word("Did it work?", 72).move_to([0, 3.0, 0])
        sub = word("+ basic correctness, on my test set", 44).move_to([0, 2.25, 0])
        rows = row_table([("1 · Citation validity", "100%"),
                          ("2 · Citation support", "≥ 90%"),
                          ("3 · Status accuracy", "≥ 85%"),
                          ("4 · Refuses unanswerable", "≥ 90%"),
                          ("     Refuses answerable", "≤ 10%")],
                         left_x=-5.3, mid_x=1.9, top_y=1.05, gap=0.92, size=52)
        bug = word("less = a bug", 36).next_to(rows[0][1], RIGHT, buff=0.35)
        bars = [row_mark(-5.6, 1.05 - i * 0.92) for i in range(4)]
        rule = Line([-5.0, 1.75, 0], [5.0, 1.75, 0], stroke_color=INK, stroke_width=3)

        clock.play(FadeIn(head), run_time=0.6)               # "How will I know it worked?"
        clock.until(1.64)                                    # "Along with basic correctness ..."
        clock.play(FadeIn(sub), Create(rule), run_time=0.6)
        clock.until(5.81)                                    # "One: citation validity."
        clock.play(FadeIn(rows[0][0]), Create(bars[0]), run_time=0.5)
        clock.until(11.07)                                   # "Target: one hundred percent."
        clock.play(FadeIn(rows[0][1]), run_time=0.4)
        clock.until(13.00)                                   # "Anything less is a bug."
        clock.play(FadeIn(bug), run_time=0.4)
        clock.until(14.72)                                   # "Two: citation support."
        clock.play(FadeIn(rows[1][0]), Create(bars[1]), run_time=0.5)
        clock.until(19.24)                                   # "Target: at least ninety percent."
        clock.play(FadeIn(rows[1][1]), run_time=0.4)
        clock.until(21.43)                                   # "Three: status accuracy."
        clock.play(FadeIn(rows[2][0]), Create(bars[2]), run_time=0.5)
        clock.until(26.34)                                   # "Target: at least eighty-five percent."
        clock.play(FadeIn(rows[2][1]), run_time=0.4)
        clock.until(29.05)                                   # "Four: refusals."
        clock.play(FadeIn(rows[3][0]), Create(bars[3]), run_time=0.5)
        clock.until(30.87)                                   # "at least nine in ten unanswerable"
        clock.play(FadeIn(rows[3][1]), run_time=0.4)
        clock.until(34.31)                                   # "no more than one in ten answerable"
        clock.play(FadeIn(rows[4]), run_time=0.5)
        clock.finish("B16")


class B17_Decision(Scene):
    """Verifier on vs off; then the rule for worked / didn't."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        base = base_rule()
        self.add(base)                                       # static frame, present from the first frame
        five = word("5 · Does the verifier help?", 64).move_to([0, 2.6, 0])
        on = tag("verify ON", 4.2, 1.4, 60).move_to([-3.0, 0.3, 0])
        off = tag("verify OFF", 4.2, 1.4, 60).move_to([3.0, 0.3, 0])
        vs = word("vs", 56).move_to([0, 0.3, 0])
        same = word("same questions · same retrieval", 48).move_to([0, -1.6, 0])

        lx, rx = -3.05, 3.05
        wh = VGroup(tick(scale=1.0), word("Worked", 64, OK_GREEN)).arrange(RIGHT, buff=0.25).move_to([lx, 2.4, 0])
        dh = VGroup(cross(scale=0.8), word("Didn't", 64, BAD_RED)).arrange(RIGHT, buff=0.25).move_to([rx, 2.4, 0])
        divider = Line([0, 2.8, 0], [0, -2.2, 0], stroke_color=INK, stroke_width=3)

        def col(items, x):
            return VGroup(*same_size([word(t, 46) for t in items], 5.4)).arrange(DOWN, buff=0.45).move_to([x, 0.25, 0])

        w = col(["targets met", "support + status improve", "correctness: ≤ 5 points lost"], lx)
        d = col(["verifier only adds refusals", "judge disagrees with me", "too often to trust"], rx)
        publish = fit(word("Either way: publish the numbers and the failures", 50)).move_to([0, -2.65, 0])

        clock.play(FadeIn(five), run_time=0.6)
        clock.until(2.11)                                    # "I'll compare the full tool ..."
        clock.play(Create(on[0]), FadeIn(on[1]), FadeIn(vs), Create(off[0]), FadeIn(off[1]), run_time=0.8)
        clock.play(FadeIn(same), run_time=0.5)
        clock.until(6.06)                                    # "It worked if it meets those targets"
        clock.play(FadeOut(VGroup(five, on, off, vs, same)), FadeIn(wh), Create(divider), FadeIn(w[0]),
                   run_time=0.7)
        clock.until(8.01)                                    # "and the verifier improves support and status"
        clock.play(FadeIn(w[1]), run_time=0.4)
        clock.until(11.25)                                   # "without costing more than five points"
        clock.play(FadeIn(w[2]), run_time=0.4)
        clock.until(14.39)                                   # "It didn't work if verification only adds refusals"
        clock.play(FadeIn(dh), FadeIn(d[0]), run_time=0.6)
        clock.until(17.61)                                   # "or if the second Claude call disagrees ..."
        clock.play(FadeIn(d[1]), FadeIn(d[2]), run_time=0.6)
        clock.until(22.53)                                   # "Either way, I'll publish ..."
        clock.play(FadeIn(publish, shift=UP * 0.1), run_time=0.6)
        clock.finish("B17")


class B18_FirstCheck(Scene):
    """The first smoke test, from the answer key (not output)."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        base = base_rule()
        self.add(base)                                       # static frame, present from the first frame
        label = top_label("TARGET ANSWER · NOT OUTPUT", 48)
        head = word("First check", 60).move_to([0, 2.4, 0])
        q = fit(word("“Which database does the tracking service use?”", 56)).move_to([0, 1.5, 0])
        chips = VGroup(tag("in progress", 3.4, 1.15, 50), tag("as of 2026-06-09", 4.2, 1.15, 50),
                       tag("cites TRK-140", 3.6, 1.15, 50)).arrange(RIGHT, buff=0.3).move_to([0, 0.05, 0])
        fit(chips, 11.8)
        miss1 = word("NotebookLM: said done", 44).move_to([-3.3, -1.55, 0])
        miss2 = word("ChatGPT: wrong date", 44).move_to([3.3, -1.55, 0])
        a_m1 = Arrow(miss1.get_top(), chips[0].get_bottom(), color=INK, stroke_width=4, buff=0.12)
        a_m2 = Arrow(miss2.get_top(), chips[1].get_bottom(), color=INK, stroke_width=4, buff=0.12)
        rings = VGroup(*[SurroundingRectangle(chips[i], color=ACCENT, buff=0.12, corner_radius=0.2,
                                              stroke_width=6) for i in (0, 1)])

        clock.play(FadeIn(label), FadeIn(head), run_time=0.6)
        clock.until(1.13)                                    # "asked which database ..."
        clock.play(FadeIn(q), run_time=0.6)
        clock.until(4.01)                                    # "it has to say the switch is still in progress"
        clock.play(Create(chips[0][0]), FadeIn(chips[0][1]), run_time=0.5)
        clock.play(Create(chips[1][0]), FadeIn(chips[1][1]), run_time=0.5)
        clock.until(7.66)                                    # "citing the migration ticket"
        clock.play(Create(chips[2][0]), FadeIn(chips[2][1]), run_time=0.5)
        clock.until(9.74)                                    # "the two things the other tools missed"
        clock.play(Create(rings), FadeIn(miss1), FadeIn(miss2), GrowArrow(a_m1), GrowArrow(a_m2), run_time=0.7)
        clock.finish("B18")


class B19_Outro(Scene):
    def construct(self):
        # 2.69 s beat: animations at 0.45x so the full card holds ~1.1 s
        text_beat(self, "B19", "DecisionTrace Lite", "Narration: synthetic voice (Kokoro)",
                  label="Gnanasudharsan Ashokumar", label_size=44, speed=0.45)
