"""scenes.py — Manim scenes for agent-proving-ground (pitch film).

Same chassis as token-not-word/scenes.py — top rail, Text built at one large
reference size and scaled down, white cards, audio-clocked _hold — on a
NEUTRAL palette: off-white ground, near-black ink, grey secondary. No product,
brand or channel styling anywhere. Colour carries meaning only: red marks a
failure, a risk or something out of scope; green appears only on PASS.

Cues: _until(scene, beat, phrase) waits until `phrase` is due in the beat's
mp3. Narration is voiced one sentence at a time (sentence_audio.py), which
records each sentence's measured speech onset in the sheet: a cue that begins
a sentence lands on that real onset; a mid-sentence cue is estimated within its
own sentence. A cue phrase missing from the beat's narration raises, so a
narration edit cannot silently desync a scene.

Mock-up beats (B00 B02 B05 B08) carry the "Constructed — not built yet." pill
in the top rail for the whole mock-up: from the first frame to the last, except
B00, whose opening name card comes before the mock-up. Their contents are
illustrations of a plan, not output of running code.

Layout law: Gate V samples each beat at 50% and 85% of its span and requires
the content bbox to cover >= 55% of the safe area. The rail (x -6..6) supplies
the width; every scene has its main frame on screen before the halfway mark.
Gate B runs strict: no stroke may cross a label's centrelines, so arrows stop
short of text and strike-throughs never pass over a label.
"""
import json
import math
from pathlib import Path

import numpy as np
from manim import *

# Manim's partial-movie cache advances renderer.time by an animation's exact
# run_time, while the cached clip holds that time rounded UP to whole frames.
# With many cache hits the clock falls behind the frames actually written, so
# _hold over-waits (measured: up to +4 frames, B10) and compile.py has to
# retime the clip. Uncached, the clock counts real frames.
config.disable_caching = True

BG   = ManimColor("#F5F5F3")   # neutral off-white ground
INK  = ManimColor("#1F2328")   # near-black — body text and primary strokes
SOFT = ManimColor("#59636E")   # secondary text and structure (5.6:1 on BG)
CARD = ManimColor("#FFFFFF")   # card surface
ACC  = ManimColor("#B42318")   # red: fail / risk / out of scope (5.9:1 on BG)
GOOD = ManimColor("#1A7F37")   # green: PASS only (4.7:1 on BG)

CONSTRUCTED = "Constructed — not built yet."

_SHEET = Path(__file__).resolve().parent / "beat_sheet.json"
try:
    _BEATS = {b["beat_id"]: b for b in json.loads(_SHEET.read_text())["beats"]}
except (OSError, ValueError, KeyError):   # pre-audio authoring / Gate A copy
    _BEATS = {}
_DUR = {k: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0.0)
        for k, b in _BEATS.items()}
_NARR = {k: b.get("narration_text", "") for k, b in _BEATS.items()}
_SENT = {k: b.get("sentences") or [] for k, b in _BEATS.items()}   # sentence_audio.py


def _clock(scene):
    try:
        return float(scene.renderer.time)
    except Exception:                      # Gate A's mock has no renderer clock
        return 0.0


def _cue_time(beat_id, phrase):
    """When `phrase` is spoken, on the beat's own clock. Returns (t, exact).

    Exact when the phrase begins a sentence: sentence_audio.py measured every
    sentence's speech onset into the sheet. A mid-sentence phrase is estimated
    by its character position inside its own sentence's onset..offset span
    (still an estimate, but bounded by one sentence instead of the whole beat).
    """
    text = _NARR.get(beat_id, "")
    i = text.find(phrase)
    if i < 0:
        raise ValueError(f"{beat_id}: cue {phrase!r} is not in the narration")
    pos = 0
    for s in _SENT.get(beat_id, []):
        j = text.find(s["text"], pos)
        if j <= i < j + len(s["text"]):
            if i == j:
                return float(s["start_s"]), True
            frac = (i - j) / len(s["text"])
            return float(s["start_s"]) + frac * (float(s["end_s"]) - float(s["start_s"])), False
        pos = j + len(s["text"])
    return _DUR.get(beat_id, 0.0) * i / len(text), False


def _until(scene, beat_id, phrase, lead=0.15):
    """Wait until `phrase` is due. A sentence-start cue leads its measured
    onset by 0.1 s; an estimated one by `lead`. A reveal that cannot start on
    time because the previous animation overran is reported as [cue-late]."""
    if not _NARR.get(beat_id):
        return
    t, exact = _cue_time(beat_id, phrase)
    target = t - (0.1 if exact else lead)
    gap = target - _clock(scene)
    if gap > 0.05:
        scene.wait(gap)
    elif gap < -0.2 and _clock(scene) > 0:
        print(f"[cue-late] {beat_id} {phrase!r} {-gap:.2f}s late", flush=True)


def _hold(scene, beat_id, minimum=0.1):
    """Audio-first tail: hold the last frame until the scene is exactly as long
    as its measured narration mp3, so compile.py never retimes the clip."""
    target = float(_DUR.get(beat_id) or 0.0)
    scene.wait(max(target - _clock(scene), minimum))


# Pango quantises glyph advances at small point sizes; build every Text at one
# reference size and scale it down (see token-not-word/scenes.py).
_TEXT_REF = 96.0
MONO = "Menlo"


def _label(text, size=24, color=None, weight=None):
    kw = {"font_size": _TEXT_REF, "color": color or INK}
    if weight:
        kw["weight"] = weight
    return Text(text, **kw).scale(size / _TEXT_REF)


def _mono(text, size=28, color=None):
    return Text(text, font=MONO, font_size=_TEXT_REF,
                color=color or INK).scale(size / _TEXT_REF)


def _left(mob, x, y):
    """Place mob with its LEFT edge at x, vertically centred on y."""
    mob.move_to([0.0, y, 0])
    mob.align_to([x, 0.0, 0], LEFT)
    return mob


def _rail(constructed=False):
    """Top rail: project kicker left, optional Constructed pill right, hairline."""
    g = VGroup()
    k = _label("AGENT PROVING GROUND", size=15, color=SOFT)
    k.to_edge(LEFT, buff=1.11).set_y(3.18)
    g.add(k)
    if constructed:
        t = _label(CONSTRUCTED, size=17)
        pill = RoundedRectangle(corner_radius=0.16, width=t.width + 0.42, height=0.38,
                                color=INK, stroke_width=1.6)
        t.move_to(pill.get_center())
        tag = VGroup(pill, t)
        tag.to_edge(RIGHT, buff=1.11).set_y(3.18)
        g.add(tag)
    g.add(Line([-6.0, 2.92, 0], [6.0, 2.92, 0], color=SOFT, stroke_width=1.2))
    return g


def _card(w, h, x, y, stroke=None):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h,
                            color=stroke or SOFT, fill_color=CARD, fill_opacity=1.0,
                            stroke_width=2.0).move_to([x, y, 0])


def _chip(text, size=26, color=None, mono=False):
    t = _mono(text, size=size, color=color) if mono else _label(text, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.5, height=t.height + 0.36,
                           color=SOFT, fill_color=CARD, fill_opacity=1.0, stroke_width=2.0)
    t.move_to(box.get_center())
    return VGroup(box, t)


def _tick(x, y, s=0.22, color=None, width=5.0):
    m = VMobject(stroke_color=color or INK, stroke_width=width)
    m.set_points_as_corners([[x - s, y, 0], [x - 0.3 * s, y - 0.65 * s, 0],
                             [x + s, y + 0.75 * s, 0]])
    return m


def _cross(x, y, s=0.2, color=None, width=5.0):
    c = color or ACC
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=c, stroke_width=width),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=c, stroke_width=width))


def _person(x, y, s=1.0, color=None):
    c = color or SOFT
    head = Circle(radius=0.22 * s, color=c, stroke_width=3).move_to([x, y + 0.3 * s, 0])
    body = ArcBetweenPoints([x - 0.42 * s, y - 0.4 * s, 0], [x + 0.42 * s, y - 0.4 * s, 0],
                            angle=-PI, color=c, stroke_width=3)
    return VGroup(head, body)


def _bubble(w, h, x, y):
    """Speech bubble: rounded card plus a tail at lower left. The tail's top
    corners sit just inside the card so its fill hides the card's edge there."""
    body = RoundedRectangle(corner_radius=0.3, width=w, height=h, color=SOFT,
                            fill_color=CARD, fill_opacity=1.0, stroke_width=2.0)
    body.move_to([x, y, 0])
    by = y - h / 2
    tail = VMobject(stroke_color=SOFT, stroke_width=2.0, fill_color=CARD, fill_opacity=1.0)
    tail.set_points_as_corners([[x - w * 0.26, by + 0.04, 0], [x - w * 0.39, by - 0.55, 0],
                                [x - w * 0.13, by + 0.04, 0]])
    return VGroup(body, tail)


# ─────────────────────────────────────────────────────────────────────────────
#  B00 — Hook. "Tushar Patel" alone, centred, for the greeting; then the rail
#  (with the Constructed pill) and the agent's "Task complete" beside a
#  failing test run.
# ─────────────────────────────────────────────────────────────────────────────
class B00_ClaimVsTests(Scene):

    def construct(self):
        self.camera.background_color = BG
        rail = _rail(constructed=True)

        name = _label("Tushar Patel", size=48, weight="BOLD").move_to(ORIGIN)

        bubble = _bubble(4.6, 2.3, -3.3, 0.25)
        who = _label("agent", size=20, color=SOFT).move_to([-3.3, 1.75, 0])
        said = _label("Task complete", size=34)
        tick = _tick(0.0, 0.0, s=0.2)
        VGroup(said, tick).arrange(RIGHT, buff=0.3).move_to([-3.3, 0.25, 0])

        run = _card(4.6, 2.3, 3.3, 0.25)
        src = _label("test run", size=20, color=SOFT).move_to([3.3, 1.75, 0])
        x = _cross(0.0, 0.0, s=0.2)
        fail = _mono("tests failing", size=30)
        VGroup(x, fail).arrange(RIGHT, buff=0.3).move_to([3.3, 0.25, 0])

        neq = _label("≠", size=72, color=SOFT).move_to([0.0, 0.25, 0])
        brace = Brace(VGroup(bubble[0], run), DOWN, buff=0.75, color=SOFT)
        check = _label("the check", size=24, color=SOFT)
        check.next_to(brace, DOWN, buff=0.18)

        # The name is alone on screen for the greeting ("Hi, I'm Tushar."). The
        # mock-up, Constructed pill included, arrives as the question starts and
        # stays to the last frame.
        self.play(FadeIn(name), run_time=0.4)
        _until(self, "B00", "Have you ever wondered")
        self.play(FadeOut(name), FadeIn(rail), FadeIn(bubble), FadeIn(who), run_time=0.6)
        _until(self, "B00", "tells you it's done")
        self.play(Write(said), run_time=0.6)
        self.play(Create(tick), run_time=0.3)

        _until(self, "B00", "whether it really is")
        self.play(FadeIn(run), FadeIn(src), run_time=0.4)
        self.play(FadeIn(fail), Create(x), run_time=0.5)

        _until(self, "B00", "check it yourself")
        self.play(FadeIn(neq), run_time=0.4)

        _until(self, "B00", "will do that check")
        self.play(GrowFromCenter(brace), run_time=0.5)
        self.play(FadeIn(check), run_time=0.3)
        _hold(self, "B00")


# ─────────────────────────────────────────────────────────────────────────────
#  The Sandbox -> Trace -> Check row (layout after AlgArtPipeline). Built once
#  here so B12's callback draws exactly the row B01 introduced. y is the row's
#  centre line; every part is placed relative to it.
# ─────────────────────────────────────────────────────────────────────────────
def _pipeline_row(y):
    xs = (-4.2, 0.0, 4.2)
    row = {
        "boxes": [_card(3.1, 2.7, x, y) for x in xs],
        "names": [_label(n, size=30, weight="BOLD").move_to([x, y + 0.9, 0])
                  for n, x in zip(("Sandbox", "Trace", "Check"), xs)],
        "wall": DashedVMobject(Rectangle(width=2.0, height=1.05, color=INK, stroke_width=2.5),
                               num_dashes=26).move_to([-4.2, y - 0.4, 0]),
        "agent": Dot([-4.75, y - 0.4, 0], radius=0.13, color=INK),
        "steps": VGroup(*[VGroup(Dot([-0.75, y + dy, 0], radius=0.06, color=INK),
                                 Line([-0.5, y + dy, 0], [0.8, y + dy, 0], color=INK,
                                      stroke_width=3))
                          for dy in (-0.05, -0.4, -0.75)]),
        "ok": _tick(3.75, y - 0.4, s=0.28, width=6),
        "no": _cross(4.7, y - 0.4, s=0.22, width=6),
        "arrows": [Arrow([-2.6, y, 0], [-1.6, y, 0], buff=0, color=SOFT,
                         stroke_width=3, tip_length=0.2),
                   Arrow([1.6, y, 0], [2.6, y, 0], buff=0, color=SOFT,
                         stroke_width=3, tip_length=0.2)],
    }
    return row


# ─────────────────────────────────────────────────────────────────────────────
#  B01 — What it is. Sandbox -> Trace -> Check.
# ─────────────────────────────────────────────────────────────────────────────
class B01_ThreeBoxes(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail())

        title = _label("Agent Proving Ground", size=40, weight="BOLD").move_to([0.0, 2.15, 0])

        row = _pipeline_row(-0.35)
        boxes, names, wall, agent = row["boxes"], row["names"], row["wall"], row["agent"]
        steps, ok, no = row["steps"], row["ok"], row["no"]
        a0, a1 = row["arrows"]

        _until(self, "B01", "Agent Proving Ground")
        self.play(Write(title), run_time=0.8)

        _until(self, "B01", "It will run")
        self.play(FadeIn(boxes[0]), FadeIn(names[0]), FadeIn(agent), run_time=0.6)
        _until(self, "B01", "on small tasks")
        self.play(agent.animate.shift(RIGHT * 0.9), run_time=0.6)
        _until(self, "B01", "isolated Kubernetes sandbox")
        self.play(Create(wall), run_time=0.7)

        _until(self, "B01", "record every step")
        self.play(GrowArrow(a0), FadeIn(boxes[1]), FadeIn(names[1]), run_time=0.5)
        self.play(LaggedStart(*[Create(s) for s in steps], lag_ratio=0.35), run_time=0.8)

        _until(self, "B01", "check whether")
        self.play(GrowArrow(a1), FadeIn(boxes[2]), FadeIn(names[2]), run_time=0.5)
        self.play(Create(ok), Create(no), run_time=0.5)
        _hold(self, "B01")


# ─────────────────────────────────────────────────────────────────────────────
#  B02 — The artifact. The planned repo tree, one entry per spoken item.
# ─────────────────────────────────────────────────────────────────────────────
class B02_RepoTree(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail(constructed=True))

        card = _card(8.0, 5.0, 0.0, -0.15)
        root = _left(_mono("agent-proving-ground/", size=32), -3.2, 1.7)
        trunk = Line([-2.8, 1.38, 0], [-2.8, -2.15, 0], color=SOFT, stroke_width=2)

        rows = []
        for name, y in zip(("harness/", "tasks/", "traces/", "EVAL-LOG.md", "FAILURES.md"),
                           (0.85, 0.1, -0.65, -1.4, -2.15)):
            stub = Line([-2.8, y, 0], [-2.35, y, 0], color=SOFT, stroke_width=2)
            rows.append(VGroup(stub, _left(_mono(name, size=32), -2.15, y)))
        count = _label("10–20", size=24, color=SOFT)
        count.next_to(rows[1][1], RIGHT, buff=0.5)

        _until(self, "B02", "public GitHub repository")
        self.play(FadeIn(card), Write(root), run_time=0.7)
        self.play(Create(trunk), run_time=0.4)

        for cue, row in zip(("Go harness", "ten to twenty", "saved traces",
                             "evaluation log", "failure analysis"), rows):
            _until(self, "B02", cue)
            self.play(Create(row[0]), FadeIn(row[1], shift=RIGHT * 0.2), run_time=0.45)
            if row is rows[1]:
                self.play(FadeIn(count), run_time=0.3)
        _hold(self, "B02")


# ─────────────────────────────────────────────────────────────────────────────
#  B03 — Why care. "done" is a claim; one command asks three questions.
# ─────────────────────────────────────────────────────────────────────────────
class B03_ThreeQuestions(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail())

        bubble = _bubble(3.2, 1.7, -3.9, 1.0)
        done = _label("done", size=48, weight="BOLD").move_to([-3.9, 1.0, 0])
        doubt = _label("?", size=72, color=SOFT).move_to([-1.75, 1.6, 0])

        term = _card(3.2, 1.1, -3.9, -1.55, stroke=INK)
        prompt = _mono("$", size=36).move_to([-5.05, -1.55, 0])
        cursor = Rectangle(width=0.2, height=0.42, color=INK, fill_color=INK,
                           fill_opacity=1.0, stroke_width=0).move_to([-4.65, -1.55, 0])
        arrow = Arrow([-2.2, -1.45, 0], [0.05, -0.2, 0], buff=0, color=SOFT,
                      stroke_width=3, tip_length=0.2)

        ys = (1.35, 0.0, -1.35)
        boxes = [Square(side_length=0.6, color=INK, stroke_width=3).move_to([0.6, y, 0])
                 for y in ys]
        labels = [_left(_label(t, size=32, color=SOFT), 1.25, y) for t, y in
                  zip(("checks passed", "stayed in sandbox", "no regression"), ys)]
        ticks = [_tick(0.6, y, s=0.2, width=6) for y in ys]

        self.play(FadeIn(bubble), Write(done), run_time=0.6)
        _until(self, "B03", "is not the same")
        self.play(FadeIn(doubt), run_time=0.4)

        _until(self, "B03", "One command")
        self.play(FadeIn(term), FadeIn(prompt), run_time=0.4)
        self.play(FadeIn(cursor), run_time=0.2)

        _until(self, "B03", "three questions")
        self.play(GrowArrow(arrow), run_time=0.4)
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.25),
                  LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.25), run_time=0.8)

        for cue, tick, label in zip(("Did the change pass", "Did the agent stay",
                                     "Did my latest prompt"), ticks, labels):
            _until(self, "B03", cue)
            self.play(Create(tick), label.animate.set_color(INK), run_time=0.45)
        _hold(self, "B03")


# ─────────────────────────────────────────────────────────────────────────────
#  B04 — Alternatives. Two puzzle pieces slide together into one.
#  The two one-line descriptions are the author's, pending verification
#  (FACTCHECK.md C1, C2).
# ─────────────────────────────────────────────────────────────────────────────
def _piece(pts):
    return Polygon(*[[x, y, 0] for x, y in pts], color=SOFT, stroke_width=2.5,
                   fill_color=CARD, fill_opacity=1.0)


class B04_TwoPieces(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail())

        # body y -1.2..1.6; A's tab and B's notch share y -0.1..0.5 and a
        # depth of 0.6, so a 1.2 shift each way seats one in the other.
        a = _piece([(-5.4, 1.6), (-1.2, 1.6), (-1.2, 0.5), (-0.6, 0.5), (-0.6, -0.1),
                    (-1.2, -0.1), (-1.2, -1.2), (-5.4, -1.2)])
        b = _piece([(1.2, 1.6), (5.4, 1.6), (5.4, -1.2), (1.2, -1.2), (1.2, -0.1),
                    (1.8, -0.1), (1.8, 0.5), (1.2, 0.5)])
        a_name = _label("Sandboxes", size=32, weight="BOLD").move_to([-3.3, 0.75, 0])
        a_tool = _label("E2B", size=26, color=SOFT).move_to([-3.3, -0.3, 0])
        b_name = _label("Traces & scores", size=32, weight="BOLD").move_to([3.5, 0.75, 0])
        b_tool = _label("Langfuse", size=26, color=SOFT).move_to([3.5, -0.3, 0])

        one = _piece([(-4.2, 1.6), (4.2, 1.6), (4.2, -1.2), (-4.2, -1.2)])
        title = _label("Proving Ground", size=44, weight="BOLD").move_to([0.0, 0.6, 0])
        parts = _label("sandbox · trace · check", size=26, color=SOFT).move_to([0.0, -0.35, 0])

        ok = VGroup(_tick(0.0, 0.0, s=0.2), _label("tests in the sandbox", size=26))
        ok.arrange(RIGHT, buff=0.3).move_to([-3.0, -2.3, 0])
        no = VGroup(_cross(0.0, 0.0, s=0.17), _label("another model's opinion", size=26,
                                                      color=SOFT))
        no.arrange(RIGHT, buff=0.3).move_to([3.0, -2.3, 0])

        _until(self, "B04", "E2B is a service")
        self.play(FadeIn(a), FadeIn(a_name), run_time=0.6)
        self.play(FadeIn(a_tool), run_time=0.3)
        _until(self, "B04", "Langfuse is a tool")
        self.play(FadeIn(b), FadeIn(b_name), run_time=0.6)
        self.play(FadeIn(b_tool), run_time=0.3)

        _until(self, "B04", "Each covers one piece")
        self.play(a.animate.set_stroke(color=INK, width=4),
                  b.animate.set_stroke(color=INK, width=4), run_time=0.5)

        _until(self, "B04", "Mine will join")
        self.play(VGroup(a, a_name, a_tool).animate.shift(RIGHT * 1.2),
                  VGroup(b, b_name, b_tool).animate.shift(LEFT * 1.2), run_time=1.0)
        # Cross-fade, not a morph: a Transform between these polygons matches
        # vertices badly and shows a lopsided blank box mid-beat (frame review).
        # The seated pair and the merged piece share an outline, so the fade
        # only dissolves the seam; both pieces leave with it, so the seam never
        # sits under the title at a steady state (Gate B). Labels clear first
        # so they never ghost under the incoming title.
        self.play(FadeOut(a_name), FadeOut(a_tool), FadeOut(b_name), FadeOut(b_tool),
                  run_time=0.3)
        self.play(FadeOut(a), FadeOut(b), FadeIn(one), FadeIn(title), run_time=0.5)

        _until(self, "B04", "one small loop")
        self.play(FadeIn(parts), run_time=0.5)
        _until(self, "B04", "pass or fail comes from tests")
        self.play(FadeIn(ok), run_time=0.5)
        _until(self, "B04", "not from another model")
        self.play(FadeIn(no), run_time=0.5)
        _hold(self, "B04")


# ─────────────────────────────────────────────────────────────────────────────
#  B05 — Who opens it. A 60-second stopwatch; README -> one command -> table.
#  The table rows are illustrative — nothing has run yet.
# ─────────────────────────────────────────────────────────────────────────────
class B05_SixtySeconds(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail(constructed=True))

        c = [-4.3, -0.15, 0]
        dial = Circle(radius=1.45, color=INK, stroke_width=5).move_to(c)
        crown = Rectangle(width=0.4, height=0.2, color=INK, fill_color=INK,
                          fill_opacity=1.0, stroke_width=0).move_to([-4.3, 1.42, 0])
        marks = VGroup(*[Line([c[0] + 1.2 * math.cos(t), c[1] + 1.2 * math.sin(t), 0],
                              [c[0] + 1.36 * math.cos(t), c[1] + 1.36 * math.sin(t), 0],
                              color=SOFT, stroke_width=2.5)
                         for t in [k * TAU / 12 for k in range(12)]])
        hand = Line(c, [-4.3, 0.95, 0], color=INK, stroke_width=5)
        pin = Dot(c, radius=0.08, color=INK)
        # Below the dial, not inside it: the sweeping hand crossed it mid-turn.
        secs = _label("60 s", size=28, color=SOFT).move_to([-4.3, -2.05, 0])
        watch = VGroup(dial, crown, marks, secs)

        reader = _person(2.0, 0.75, s=2.0)
        who = _label("engineer · hiring manager", size=26, color=SOFT).move_to([2.0, -0.85, 0])

        chips = VGroup(_chip("README", mono=True), _chip("one command"), _chip("results"))
        chips.arrange(RIGHT, buff=0.85).move_to([1.9, 1.85, 0])
        arrows = [Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.1,
                        color=SOFT, stroke_width=3, tip_length=0.18) for i in (0, 1)]

        head = VGroup(_left(_label("task", size=20, color=SOFT), -1.75, 0.6),
                      _label("result", size=20, color=SOFT).move_to([1.35, 0.6, 0]),
                      _left(_label("reason", size=20, color=SOFT), 2.45, 0.6))
        rule = Line([-1.95, 0.3, 0], [5.75, 0.3, 0], color=SOFT, stroke_width=1.5)
        spec = [("task-01", "PASS", GOOD, "checks passed"),
                ("task-02", "FAIL", ACC, "2 tests failed"),
                ("task-03", "PASS", GOOD, "checks passed")]
        ys = (-0.2, -0.9, -1.6)
        col_task = VGroup(*[_left(_mono(t, size=26), -1.75, y) for (t, _, _, _), y in zip(spec, ys)])
        col_res = VGroup(*[_mono(r, size=26, color=k).move_to([1.35, y, 0])
                           for (_, r, k, _), y in zip(spec, ys)])
        col_why = VGroup(*[_left(_label(w, size=24, color=SOFT), 2.45, y)
                           for (_, _, _, w), y in zip(spec, ys)])
        pick = Rectangle(width=7.9, height=0.62, color=INK, stroke_width=2.5).move_to([1.9, -0.9, 0])

        self.play(FadeIn(watch), FadeIn(hand), FadeIn(pin), FadeIn(reader), run_time=0.6)
        _until(self, "B05", "engineer or hiring manager")
        self.play(FadeIn(who), run_time=0.4)

        _until(self, "B05", "In the first sixty seconds")
        self.play(FadeOut(reader), FadeOut(who), run_time=0.4)

        _until(self, "B05", "read the README")
        self.play(FadeIn(chips[0]), Rotate(hand, angle=-TAU / 3, about_point=c), run_time=0.6)
        _until(self, "B05", "run one command")
        self.play(GrowArrow(arrows[0]), FadeIn(chips[1]),
                  Rotate(hand, angle=-TAU / 3, about_point=c), run_time=0.6)
        _until(self, "B05", "see a table")
        # The table header rides in with the "results" chip: as a separate
        # 0.4 s play it pushed the "each task" reveal 0.3 s past its word.
        self.play(GrowArrow(arrows[1]), FadeIn(chips[2]),
                  Rotate(hand, angle=-TAU / 3, about_point=c),
                  FadeIn(head), Create(rule), run_time=0.6)

        _until(self, "B05", "each task")
        self.play(FadeIn(col_task), run_time=0.4)
        _until(self, "B05", "pass or fail")
        self.play(FadeIn(col_res), run_time=0.4)
        _until(self, "B05", "and why")
        self.play(FadeIn(col_why), run_time=0.4)

        _until(self, "B05", "open any trace")
        self.play(Create(pick), run_time=0.5)
        _hold(self, "B05")


# ─────────────────────────────────────────────────────────────────────────────
#  B06 — What it proves. The B01 loop with four tags around it
#  (layout after CodingAgentsFig1Loop).
# ─────────────────────────────────────────────────────────────────────────────
class B06_FourSkills(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail())

        cx, cy, R = 0.0, -0.15, 1.9

        def at(deg):
            return [cx + R * math.cos(math.radians(deg)), cy + R * math.sin(math.radians(deg)), 0]

        nodes = VGroup()
        for deg, name in ((90, "Sandbox"), (-30, "Trace"), (210, "Check")):
            p = at(deg)
            nodes.add(VGroup(_card(2.1, 0.75, p[0], p[1]),
                             _label(name, size=26, weight="BOLD").move_to(p)))
        # Clockwise Sandbox -> Trace -> Check -> Sandbox; each arc leaves 38
        # degrees of clearance either side of a node so no stroke meets a card.
        arcs = VGroup(*[CurvedArrow(at(d - 38), at(d - 120 + 38), angle=-44 * DEGREES,
                                    color=SOFT, stroke_width=3, tip_length=0.18)
                        for d in (90, -30, 210)])

        tags = [_chip(t, size=26) for t in
                ("prompt contract", "agent loop", "verification", "evaluation")]
        for tag, (x, y) in zip(tags, ((-4.6, 1.45), (4.6, 1.45), (4.6, -1.25), (-4.6, -1.25))):
            tag.move_to([x, y, 0])

        limit = _label("one laptop, not production", size=26, color=SOFT).move_to([0.0, -2.75, 0])

        self.play(FadeIn(nodes), run_time=0.6)
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.3), run_time=0.9)

        _until(self, "B06", "prompt contract")
        self.play(FadeIn(tags[0], shift=RIGHT * 0.2), run_time=0.4)
        _until(self, "B06", "an agent loop")
        self.play(FadeIn(tags[1], shift=LEFT * 0.2), arcs.animate.set_color(INK), run_time=0.5)
        _until(self, "B06", "verification from")
        self.play(FadeIn(tags[2], shift=LEFT * 0.2), run_time=0.4)
        _until(self, "B06", "evaluation I can repeat")
        self.play(FadeIn(tags[3], shift=RIGHT * 0.2), run_time=0.4)

        _until(self, "B06", "It will be built")
        self.play(FadeIn(limit), run_time=0.5)
        _hold(self, "B06")


# ─────────────────────────────────────────────────────────────────────────────
#  B07 — In and out. IN: laptop, kind, one agent, synthetic tasks.
#  OUT: a hosted cloud with users, crossed out.
# ─────────────────────────────────────────────────────────────────────────────
class B07_InAndOut(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail())

        inbox = _card(5.4, 5.0, -3.2, -0.15)
        outbox = _card(5.4, 5.0, 3.2, -0.15)
        in_h = _label("IN", size=36, weight="BOLD").move_to([-3.2, 1.8, 0])
        out_h = _label("OUT", size=36, weight="BOLD").move_to([3.2, 1.8, 0])

        kind = VGroup(_mono("kind", size=30), _label("Kubernetes in Docker", size=22, color=SOFT))
        kind.arrange(RIGHT, buff=0.3)
        items = []
        for mob, y in zip((_label("laptop", size=30), kind, _label("one agent", size=30),
                           _label("synthetic tasks", size=30)), (0.85, 0.0, -0.85, -1.7)):
            dot = Square(side_length=0.16, color=INK, fill_color=INK, fill_opacity=1.0,
                         stroke_width=0).move_to([-5.2, y, 0])
            items.append(VGroup(dot, _left(mob, -4.85, y)))

        cx, cy = 3.2, 0.55
        cloud = VGroup(
            ArcBetweenPoints([cx - 1.3, cy - 0.2, 0], [cx - 0.65, cy + 0.4, 0], angle=-PI * 0.8,
                             color=SOFT, stroke_width=3),
            ArcBetweenPoints([cx - 0.65, cy + 0.4, 0], [cx + 0.4, cy + 0.6, 0], angle=-PI * 0.8,
                             color=SOFT, stroke_width=3),
            ArcBetweenPoints([cx + 0.4, cy + 0.6, 0], [cx + 1.3, cy - 0.2, 0], angle=-PI * 0.8,
                             color=SOFT, stroke_width=3),
            Line([cx + 1.3, cy - 0.2, 0], [cx - 1.3, cy - 0.2, 0], color=SOFT, stroke_width=3),
        )
        users = VGroup(*[_person(x, -0.55, s=0.75) for x in (2.45, 3.2, 3.95)])
        what = _label("hosted · multi-user", size=24, color=SOFT).move_to([3.2, -1.45, 0])
        strike = _cross(3.2, 0.2, s=1.2, width=6)
        later = _label("can be added later", size=24, color=SOFT).move_to([3.2, -2.15, 0])

        # "It runs locally" opens the beat (0.2 s in), so "laptop" arrives with
        # the boxes rather than after them.
        self.play(FadeIn(inbox), FadeIn(outbox), FadeIn(in_h), FadeIn(out_h),
                  FadeIn(items[0], shift=RIGHT * 0.2), run_time=0.5)
        for cue, row in zip(("on kind", "one agent", "tasks I write myself"), items[1:]):
            _until(self, "B07", cue)
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.4)

        _until(self, "B07", "will not be a hosted")
        self.play(Create(cloud), FadeIn(users), run_time=0.7)
        self.play(FadeIn(what), run_time=0.3)
        _until(self, "B07", "multi-user service")
        self.play(Create(strike), run_time=0.5)

        _until(self, "B07", "Cloud deployment")
        self.play(FadeIn(later), run_time=0.4)
        _hold(self, "B07")


# ─────────────────────────────────────────────────────────────────────────────
#  B08 — First piece. task -> container -> trace.json -> PASS.
#  The printed line and the step list are illustrative — nothing has run yet.
# ─────────────────────────────────────────────────────────────────────────────
class B08_FirstRun(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail(constructed=True))

        xs = (-4.65, -1.55, 1.55, 4.65)
        cards = [_card(2.4, 2.4, x, -0.1) for x in xs]

        task = VGroup(Rectangle(width=0.95, height=1.15, color=SOFT, stroke_width=2.5)
                      .move_to([-4.65, 0.35, 0]),
                      *[Line([-4.95, y, 0], [-4.35, y, 0], color=SOFT, stroke_width=2.5)
                        for y in (0.6, 0.35, 0.1)],
                      _label("task", size=24).move_to([-4.65, -0.85, 0]))
        box = VGroup(Rectangle(width=1.45, height=0.95, color=INK, stroke_width=3)
                     .move_to([-1.55, 0.35, 0]),
                     *[Line([x, 0.02, 0], [x, 0.68, 0], color=INK, stroke_width=2)
                       for x in (-1.95, -1.75, -1.55, -1.35, -1.15)],
                     _label("container", size=24).move_to([-1.55, -0.85, 0]))
        trace = VGroup(Polygon([1.1, 0.92, 0], [1.82, 0.92, 0], [2.02, 0.72, 0],
                               [2.02, -0.22, 0], [1.1, -0.22, 0], color=SOFT, stroke_width=2.5),
                       VMobject(stroke_color=SOFT, stroke_width=2.5).set_points_as_corners(
                           [[1.82, 0.92, 0], [1.82, 0.72, 0], [2.02, 0.72, 0]]),
                       *[Line([1.25, y, 0], [1.85, y, 0], color=SOFT, stroke_width=2.5)
                         for y in (0.45, 0.2, -0.05)],
                       _mono("trace.json", size=22).move_to([1.55, -0.85, 0]))
        result = VGroup(_label("PASS", size=48, weight="BOLD", color=GOOD).move_to([4.65, 0.35, 0]),
                        _label("result", size=24).move_to([4.65, -0.85, 0]))
        arrows = [Arrow([x + 1.25, -0.1, 0], [x + 1.85, -0.1, 0], buff=0, color=SOFT,
                        stroke_width=3, tip_length=0.18) for x in xs[:3]]

        printed = _mono("> PASS", size=26).move_to([4.65, -1.85, 0])
        steps = VGroup(*[_left(_mono(s, size=22, color=SOFT), 0.5, y) for s, y in
                         (("1 read task", -1.75), ("2 edit file", -2.2), ("3 run checks", -2.65))])

        _until(self, "B08", "smallest possible run")
        self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.2), run_time=0.8)

        _until(self, "B08", "one task")
        self.play(FadeIn(task), run_time=0.4)
        for cue, arrow, part in zip(("one container", "one trace file", "one pass-or-fail line"),
                                    arrows, (box, trace, result)):
            _until(self, "B08", cue)
            self.play(GrowArrow(arrow), FadeIn(part), run_time=0.4)

        _until(self, "B08", "the result prints")
        self.play(AddTextLetterByLetter(printed), run_time=0.6)
        _until(self, "B08", "lists every step")
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in steps], lag_ratio=0.35),
                  run_time=0.9)
        _hold(self, "B08")


# ─────────────────────────────────────────────────────────────────────────────
#  B09 — Risk. The Kubernetes wheel, with a small Go chip beside it, looms
#  over evals; Docker first -> kind, with a cutoff date and a fallback.
# ─────────────────────────────────────────────────────────────────────────────
class B09_DockerFirst(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail())

        w = [-3.5, 1.0, 0]
        angles = [k * TAU / 8 for k in range(8)]
        wheel = VGroup(
            Circle(radius=1.2, color=SOFT, stroke_width=6).move_to(w),
            Circle(radius=0.95, color=SOFT, stroke_width=2).move_to(w),
            Circle(radius=0.28, color=SOFT, fill_color=SOFT, fill_opacity=1.0).move_to(w),
            *[Line([w[0] + 0.28 * math.cos(t), w[1] + 0.28 * math.sin(t), 0],
                   [w[0] + 1.45 * math.cos(t), w[1] + 1.45 * math.sin(t), 0],
                   color=SOFT, stroke_width=4) for t in angles],
            *[Dot([w[0] + 1.5 * math.cos(t), w[1] + 1.5 * math.sin(t), 0], radius=0.09,
                  color=SOFT) for t in angles],
        )
        k8s = _label("Kubernetes setup", size=22, color=SOFT).move_to([-3.5, -0.95, 0])
        # Upper right of the wheel, clear of its rim dots and above the
        # Docker-first row, so it reads as a second risk, not a flow step.
        go = _chip("Go", size=24, color=SOFT).move_to([-1.4, 2.05, 0])
        evals = Rectangle(width=1.7, height=0.7, color=INK, stroke_width=2.5).move_to([-3.5, -2.05, 0])
        evals_gone = DashedVMobject(Rectangle(width=1.7, height=0.7, color=SOFT, stroke_width=2.5),
                                    num_dashes=20).move_to([-3.5, -2.05, 0])
        evals_t = _label("evals", size=26).move_to([-3.5, -2.05, 0])

        docker = VGroup(_card(2.6, 1.0, 1.75, 1.0, stroke=INK),
                        _label("Docker first", size=28, weight="BOLD").move_to([1.75, 1.0, 0]))
        kind = VGroup(_card(1.8, 1.0, 4.95, 1.0, stroke=INK),
                      _mono("kind", size=32).move_to([4.95, 1.0, 0]))
        move = Arrow([3.1, 1.0, 0], [4.0, 1.0, 0], buff=0, color=SOFT,
                     stroke_width=3, tip_length=0.2)

        cal = VGroup(
            Rectangle(width=1.8, height=1.5, color=INK, stroke_width=2.5).move_to([3.45, -1.15, 0]),
            Line([2.55, -0.72, 0], [4.35, -0.72, 0], color=INK, stroke_width=2),
            Line([3.0, -0.3, 0], [3.0, -0.52, 0], color=INK, stroke_width=4),
            Line([3.9, -0.3, 0], [3.9, -0.52, 0], color=INK, stroke_width=4),
            *[Dot([x, y, 0], radius=0.06, color=SOFT)
              for y in (-1.1, -1.55) for x in (2.85, 3.25, 3.65, 4.05)
              if (x, y) != (4.05, -1.55)],
        )
        cutoff = _cross(4.05, -1.55, s=0.14, width=4)
        cut_t = _label("cutoff", size=22, color=SOFT).move_to([4.95, -1.15, 0])
        fallback = CurvedArrow([2.45, -1.15, 0], [1.4, 0.42, 0], angle=-PI / 3,
                               color=SOFT, stroke_width=3, tip_length=0.18)
        fb_t = _label("miss it → ship Docker, log why", size=22, color=SOFT).move_to([3.45, -2.45, 0])

        self.play(FadeIn(wheel), FadeIn(k8s), run_time=0.6)
        self.play(Create(evals), FadeIn(evals_t), run_time=0.4)
        _until(self, "B09", "Go and Kubernetes")
        self.play(FadeIn(go, shift=LEFT * 0.15), run_time=0.4)
        _until(self, "B09", "at the same time")
        self.play(Rotate(wheel, angle=-PI / 2, about_point=w), run_time=1.1)
        _until(self, "B09", "evaluation never gets built")
        self.play(ReplacementTransform(evals, evals_gone), evals_t.animate.set_color(SOFT),
                  run_time=0.6)

        _until(self, "B09", "plain Docker first")
        self.play(FadeIn(docker), run_time=0.5)
        _until(self, "B09", "move them onto kind")
        self.play(GrowArrow(move), FadeIn(kind), run_time=0.5)
        _until(self, "B09", "by a fixed date")
        self.play(FadeIn(cal), run_time=0.4)
        self.play(Create(cutoff), FadeIn(cut_t), run_time=0.4)

        _until(self, "B09", "If I miss it")
        self.play(Create(fallback), run_time=0.6)
        self.play(FadeIn(fb_t), run_time=0.4)
        _hold(self, "B09")


# ─────────────────────────────────────────────────────────────────────────────
#  B10 — Why this project. Have | New (layout after K12Fig05DiffVsTrack),
#  with the public project named under Have. The divider stops above that
#  block: the URL at a laptop-readable size (~7 units) runs past centre.
# ─────────────────────────────────────────────────────────────────────────────
class B10_HaveAndNew(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail())

        have_h = _label("Have", size=36, weight="BOLD").move_to([-3.1, 2.4, 0])
        new_h = _label("New", size=36, weight="BOLD").move_to([3.1, 2.4, 0])
        new_h.align_to(have_h, UP)
        divider = Line([0.0, 2.7, 0], [0.0, -0.6, 0], color=SOFT, stroke_width=1.5)

        ys = (1.65, 1.15, 0.65, 0.15)
        have = [_label(t, size=30).move_to([-3.1, y, 0]) for t, y in
                zip(("LLM evaluation", "Docker", "Terraform", "AWS"), ys)]
        new = [_label(t, size=30).move_to([3.1, y, 0]) for t, y in
               zip(("Go", "Kubernetes", "sandbox isolation", "trace design"), ys)]
        frame = RoundedRectangle(corner_radius=0.15, width=4.6, height=2.2, color=INK,
                                 stroke_width=2.5).move_to([3.1, 0.9, 0])
        asks = _label("what I want to build", size=22, color=SOFT).move_to([3.1, -0.5, 0])

        # The public project, left-aligned under the Have column.
        shown = _left(_label("Shown in my public project: OmniSQL-Postgres", size=24), -5.9, -1.25)
        url = _left(_mono("github.com/tushar-patel28/omnisql-postgres", size=20), -5.9, -1.8)
        seen = _left(_label("public repo, checked 2026-10-22", size=18, color=SOFT), -5.9, -2.3)

        self.play(FadeIn(have_h), FadeIn(new_h), Create(divider), run_time=0.6)

        _until(self, "B10", "LLM evaluation")
        self.play(FadeIn(have[0], shift=RIGHT * 0.2), run_time=0.4)
        # "AWS," runs straight into "in a public project": 0.3 s fades keep it on cue.
        for cue, item in zip(("Docker,", "Terraform,", "AWS,"), have[1:]):
            _until(self, "B10", cue)
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.3)
        _until(self, "B10", "in a public project")
        self.play(FadeIn(shown, shift=RIGHT * 0.2), FadeIn(url, shift=RIGHT * 0.2), run_time=0.5)
        _until(self, "B10", "check on GitHub")
        self.play(FadeIn(seen), run_time=0.4)
        # "Go," and "Kubernetes," are spoken 0.25 s apart: 0.3 s fades keep both on cue.
        for cue, item in zip(("Go,", "Kubernetes,", "sandbox isolation", "trace design"), new):
            _until(self, "B10", cue)
            self.play(FadeIn(item, shift=LEFT * 0.2), run_time=0.3)

        _until(self, "B10", "I want to work on the infrastructure")
        self.play(Create(frame), FadeIn(asks), run_time=0.6)
        _until(self, "B10", "building this is how")
        self.play(Indicate(VGroup(*new), color=INK, scale_factor=1.06), run_time=0.8)
        _hold(self, "B10")


# ─────────────────────────────────────────────────────────────────────────────
#  B11 — Exists vs will. Only the plan is real today.
# ─────────────────────────────────────────────────────────────────────────────
class B11_ExistsVsWill(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail())

        today_h = _label("Exists today", size=34, weight="BOLD").move_to([-3.75, 2.15, 0])
        will_h = _label("Will exist", size=34, weight="BOLD").move_to([2.6, 2.15, 0])
        will_h.align_to(today_h, UP)   # the y in "today" drops its bbox centre
        divider = Line([-1.2, 2.55, 0], [-1.2, -2.25, 0], color=SOFT, stroke_width=1.5)

        plan = VGroup(Square(side_length=0.5, color=INK, fill_color=INK, fill_opacity=1.0,
                             stroke_width=2).move_to([-5.0, 1.3, 0]),
                      _tick(-5.0, 1.3, s=0.15, color=CARD, width=5),
                      _left(_label("this plan", size=32), -4.55, 1.3))

        # 0.6 pitch keeps "failure analysis" well clear of the bottom edge.
        ys = (1.3, 0.7, 0.1, -0.5, -1.1, -1.7)
        boxes = [DashedVMobject(Square(side_length=0.42, color=SOFT, stroke_width=2.5),
                                num_dashes=12).move_to([0.1, y, 0]) for y in ys]
        names = [_left(_label(t, size=30, color=SOFT), 0.6, y) for t, y in
                 zip(("harness", "sandbox", "tasks", "traces", "eval log", "failure analysis"), ys)]

        self.play(FadeIn(today_h), FadeIn(will_h), Create(divider), run_time=0.6)
        _until(self, "B11", "this is a plan")
        self.play(FadeIn(plan), run_time=0.5)

        _until(self, "B11", "None of the code exists")
        self.play(LaggedStart(*[FadeIn(VGroup(b, n)) for b, n in zip(boxes, names)],
                              lag_ratio=0.15), run_time=1.0)
        _until(self, "B11", "what it will do")
        self.play(*[n.animate.set_color(INK) for n in names], run_time=0.6)
        _until(self, "B11", "The repository will show")
        self.play(Indicate(VGroup(*boxes), color=INK, scale_factor=1.15), run_time=0.8)
        _hold(self, "B11")


# ─────────────────────────────────────────────────────────────────────────────
#  B12 — Close. B01's Sandbox -> Trace -> Check row draws back in, then
#  "Thank you." fades in beneath it.
# ─────────────────────────────────────────────────────────────────────────────
class B12_ThankYou(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.add(_rail())

        row = _pipeline_row(0.3)
        frame = VGroup(*row["boxes"], *row["names"], *row["arrows"])
        thanks = _label("Thank you.", size=56, weight="BOLD").move_to([0.0, -2.2, 0])

        self.play(LaggedStart(*[FadeIn(m) for m in frame], lag_ratio=0.1), run_time=0.9)
        _until(self, "B12", "An agent can say")
        self.play(FadeIn(row["agent"]), Create(row["wall"]), Create(row["steps"]), run_time=0.7)
        _until(self, "B12", "show whether")
        self.play(Create(row["ok"]), Create(row["no"]), run_time=0.5)
        # On the spoken words. B12's mp3 carries a 1.5 s silent tail
        # (sentence_audio.py TAIL_PAD_S), so the card holds after they end.
        _until(self, "B12", "Thank you")
        self.play(FadeIn(thanks, shift=UP * 0.15), run_time=0.35)
        _hold(self, "B12")
