"""scenes.py — Manim beats for the DecisionTrace pitch film.

Three kinds of scene, one palette:
  * text-led beats (B00, B02, B08, B10, B11, B12): large serif type between two
    ink rules, sized to fill the title-safe area;
  * line drawings (B01, B05, B07, B09), 1–3 words per element;
  * a CONSTRUCTED terminal (B06) — a drawn mock-up, labelled as such on screen.

Each scene's length is read from beat_sheet.json (actual_duration_s, measured
from the Kokoro audio), so the picture ends exactly when the narration does.
In-scene cue times (seconds from the start of the beat) were measured from the
beat's mp3 with ffmpeg silencedetect; they are noted next to each cue.

Palette: cream ground, warm ink for every word, terracotta only as a shape
accent, green / red only for pass / fail marks.
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


def tag(text, width=3.6, height=0.9, size=38):
    box = RoundedRectangle(corner_radius=0.18, width=width, height=height,
                           stroke_color=INK, stroke_width=3)
    return VGroup(box, word(text, size).move_to(box.get_center()))


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


def tick(color=OK_GREEN, scale=1.0):
    return VMobject(stroke_color=color, stroke_width=8).set_points_as_corners(
        [[-0.25, 0, 0], [-0.05, -0.22, 0], [0.32, 0.28, 0]]).scale(scale)


def cross(color=BAD_RED, scale=1.0):
    return VGroup(Line([-0.25, -0.25, 0], [0.25, 0.25, 0], stroke_color=color, stroke_width=8),
                  Line([-0.25, 0.25, 0], [0.25, -0.25, 0], stroke_color=color, stroke_width=8)).scale(scale)


def rules():
    return (Line([-RULE_X, 3.0, 0], [RULE_X, 3.0, 0], stroke_color=INK, stroke_width=3),
            Line([-RULE_X, -2.9, 0], [RULE_X, -2.9, 0], stroke_color=INK, stroke_width=3))


def text_beat(scene, bid, heading, body, label=None, label_size=50):
    """Large serif heading + body between two ink rules. Same layout every time:
    top rule y=3.0, optional label y=2.3, heading y=0.55, body y=-1.45,
    bottom rule y=-2.9."""
    scene.camera.background_color = GROUND
    clock = Clock(scene)
    top, bottom = rules()
    if "\n" in heading:                           # two-line heading: centred rows
        head = VGroup(*[word(ln, 96) for ln in heading.split("\n")]).arrange(DOWN, buff=0.35)
    else:
        head = word(heading, 96)
    head_scale = min(1.0, MAX_W / head.width)    # long headings shrink to fit the width
    head.scale(head_scale).move_to([0, 0.55, 0])
    # body stays visibly smaller than the heading's effective size
    sub = fit(word(body, max(44, min(56, 96 * head_scale * 0.85)), INK)).move_to([0, -1.45, 0])
    under_y = -0.35
    if "\n" in heading:                           # two-line heading: sit it above the underline
        head.move_to([0, 0.55, 0]).shift(UP * (-0.05 - head.get_bottom()[1]))
        under_y = head.get_bottom()[1] - 0.3
    half = min(head.width, MAX_W) / 2              # clamp: never wider than the text column
    under = Line([-half, under_y, 0], [half, under_y, 0], stroke_color=ACCENT, stroke_width=6)
    mark = Line([-0.6, -2.3, 0], [0.6, -2.3, 0], stroke_color=ACCENT, stroke_width=6)
    clock.play(Create(top), Create(bottom), run_time=0.8)
    if label:
        lab = fit(word(label, label_size, INK)).move_to([0, 2.3, 0])
        clock.play(FadeIn(lab), run_time=0.5)
    clock.play(FadeIn(head, shift=UP * 0.15), run_time=0.9)
    clock.play(Create(under), run_time=0.7)
    clock.play(FadeIn(sub, shift=UP * 0.15), Create(mark), run_time=0.8)
    clock.finish(bid)


# ---------------------------------------------------------------- text-led beats

class B00_Title(Scene):
    def construct(self):
        # The name is set large in the scene itself (it replaced the small
        # metadata.channel_title overlay, which has no size setting).
        text_beat(self, "B00", "DecisionTrace", "A pitch for a project that doesn't exist yet.",
                  label="Gnanasudharsan Ashokumar", label_size=44)   # ~2.6x the old overlay


class B02_TestSetup(Scene):
    def construct(self):
        text_beat(self, "B02", "6 docs · 4 questions · 2 tools",
                  "PostgreSQL → DynamoDB: approved, not finished", label="SYNTHETIC TEST DATA")


class B08_Scope(Scene):
    """Out / In / First — each line lands on its sentence."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        top, bottom = rules()
        out = fit(word("Out: Slack · Jira · email · real data", 76)).move_to([0, 1.75, 0])
        inn = fit(word("In: tool · verifier · test set · eval report", 76)).move_to([0, 0.15, 0])
        first = fit(word("First: one question, six docs, a passing quote test", 54)).move_to([0, -1.55, 0])
        # one accent underline under each FULL line (never under a single word)
        marks = [Line([m.get_left()[0], m.get_bottom()[1] - 0.18, 0],
                      [m.get_right()[0], m.get_bottom()[1] - 0.18, 0], stroke_color=ACCENT, stroke_width=4)
                 for m in (out, inn, first)]
        clock.play(Create(top), Create(bottom), run_time=0.8)
        clock.play(FadeIn(out, shift=UP * 0.15), Create(marks[0]), run_time=0.9)
        clock.until(5.28)                                   # "What's in: ..."
        clock.play(FadeIn(inn, shift=UP * 0.15), Create(marks[1]), run_time=0.9)
        clock.until(10.84)                                  # "The first piece to run ..."
        clock.play(FadeIn(first, shift=UP * 0.15), Create(marks[2]), run_time=0.9)
        clock.finish("B08")


class B10_WhyThis(Scene):
    def construct(self):
        text_beat(self, "B10", "New: eval · citation checks · contracts · loops",
                  "Have: RAG + LLM backends (co-op, not shareable)")


class B11_ExistsVsWill(Scene):
    def construct(self):
        text_beat(self, "B11", "Exists: alternatives test · docs · notes\nscreenshots · brief · film",
                  "Everything else: will")


class B12_Outro(Scene):
    def construct(self):
        text_beat(self, "B12", "Gnanasudharsan Ashokumar",
                  "Narration: synthetic voice (Kokoro)")


# ---------------------------------------------------------------- drawings

class B01_StatusTag(Scene):
    """A question mark resolves into a decision-status tag; then the planned
    repository: a dashed folder (not built yet) with its four items."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        q = word("?", 340).move_to([-4.4, 0, 0])
        arrow = Arrow([-3.0, 0, 0], [0.6, 0, 0], color=INK, stroke_width=6, buff=0)
        tags = VGroup(tag("decided", 4.6, 1.3, 56), tag("in progress", 4.6, 1.3, 56),
                      tag("superseded", 4.6, 1.3, 56)).arrange(DOWN, buff=0.6).move_to([3.4, 0, 0])
        ring = SurroundingRectangle(tags[1], color=ACCENT, buff=0.14, corner_radius=0.24,
                                    stroke_width=7)
        clock.play(Write(q), run_time=1.2)
        clock.play(GrowArrow(arrow), run_time=1.0)
        for t in tags:
            clock.play(Create(t[0]), FadeIn(t[1]), run_time=0.7)
        clock.play(Create(ring), run_time=0.8)

        # Second half — "It will be a public GitHub repository" (7.48 s)
        planned = word("PLANNED", 60).move_to([0, 2.95, 0])
        folder = VMobject(stroke_color=INK, stroke_width=4).set_points_as_corners([
            [-5.8, 1.9, 0], [-3.4, 1.9, 0], [-3.0, 2.35, 0], [-0.9, 2.35, 0], [-0.5, 1.9, 0],
            [5.8, 1.9, 0], [5.8, -3.0, 0], [-5.8, -3.0, 0], [-5.8, 1.9, 0]])
        folder = DashedVMobject(folder, num_dashes=90)
        cells = [([-3.2, 0.65, 0], "CLI"), ([2.6, 0.65, 0], "synthetic docs"),
                 ([-3.2, -1.75, 0], "test set"), ([2.6, -1.75, 0], "eval report")]
        items = []
        for pos, name in cells:
            icon = doc(0.9, 1.15).move_to([pos[0] - 1.75, pos[1], 0])
            label = word(name, 48).next_to(icon, RIGHT, buff=0.35)
            items.append(VGroup(icon, label))
        clock.until(7.48)
        # crossfade so the folder is complete before GATE V's mid-beat sample (~8.5 s)
        clock.play(FadeOut(VGroup(q, arrow, tags, ring)), Create(folder), FadeIn(planned), run_time=0.8)
        # each item lands as the previous phrase ends (pause starts 9.67 / 11.82 / 13.52 s;
        # the last at 15.0 s) so the completed folder holds >= 1.5 s before the beat ends
        for item, cue in zip(items, (9.67, 11.82, 13.52, 15.0)):
            clock.until(cue)
            clock.play(Create(item[0]), FadeIn(item[1]), run_time=0.4)
        clock.finish("B01")


class B05_ClaimCheck(Scene):
    """A claim points at its cited quote: found in one page, missing in the other."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        claim_box = RoundedRectangle(corner_radius=0.18, width=4.2, height=1.0,
                                     stroke_color=INK, stroke_width=3).move_to([0, 2.5, 0])
        claim = VGroup(claim_box, word("claim", 40).move_to(claim_box))
        left = doc().move_to([-3.0, -0.9, 0])
        right = doc().move_to([3.0, -0.9, 0])
        quote = Rectangle(width=1.9, height=0.34, stroke_width=0, fill_color=ACCENT,
                          fill_opacity=0.35).move_to(left[2][1])
        gap = DashedLine([right.get_left()[0] + 0.3, -0.9, 0], [right.get_right()[0] - 0.3, -0.9, 0],
                         stroke_color=BAD_RED, stroke_width=4)
        a1 = Arrow(claim_box.get_bottom() + LEFT * 0.8, left.get_top() + UP * 0.05, color=INK,
                   stroke_width=4, buff=0.1)
        a2 = Arrow(claim_box.get_bottom() + RIGHT * 0.8, right.get_top() + UP * 0.05, color=INK,
                   stroke_width=4, buff=0.1)
        ok = VGroup(tick(scale=1.2), word("found", 36)).arrange(RIGHT, buff=0.25).move_to([-3.0, -2.95, 0])
        bad = VGroup(cross(scale=1.0), word("missing", 36)).arrange(RIGHT, buff=0.25).move_to([3.0, -2.95, 0])
        clock.play(Create(claim_box), FadeIn(claim[1]), run_time=1.0)
        clock.until(2.5)
        clock.play(GrowArrow(a1), GrowArrow(a2), Create(left), Create(right), run_time=1.5)
        clock.until(5.0)
        clock.play(FadeIn(quote), run_time=0.8)
        clock.play(Create(ok), run_time=0.8)
        clock.until(7.6)
        clock.play(FadeOut(right[2][1]), Create(gap), run_time=0.8)
        clock.play(Create(bad), run_time=0.8)
        clock.finish("B05")


class B06_Terminal(Scene):
    """CONSTRUCTED terminal mock-up (not real output): one command, the answer
    with its decision status, a pass/fail line per claim, the report path."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        label = fit(word("CONSTRUCTED · NOT REAL OUTPUT", 72)).move_to([0, 2.85, 0])
        window = RoundedRectangle(corner_radius=0.2, width=12.0, height=5.0, stroke_color=INK,
                                  stroke_width=3, fill_color=PAPER, fill_opacity=1).move_to([0, -0.55, 0])
        bar = Rectangle(width=12.0, height=0.55, stroke_width=0, fill_color=BAR,
                        fill_opacity=1).move_to([0, 1.675, 0])
        dots = VGroup(*[Circle(radius=0.09, stroke_color=INK, stroke_width=2).move_to([-5.6 + 0.32 * i, 1.675, 0])
                        for i in range(3)])
        title = word("zsh — decisiontrace", 26, INK, MONO).move_to([0, 1.675, 0])
        left_x = -5.55

        def line(text, y, t2c=None):
            return fit(Text(text, font=MONO, font_size=30, color=INK, t2c=t2c or {}), 11.0) \
                .move_to([0, y, 0]).align_to([left_x, 0, 0], LEFT)

        cmd = line('$ decisiontrace ask "Which database does the tracking service use?"', 1.0)
        ans = line("→ DynamoDB (decided 2026-05-18) · status: in progress", 0.3)
        c1 = line("✓ claim 1   quote found in source        PASS", -0.4, {"✓": OK_GREEN, "PASS": OK_GREEN})
        c2 = line("✓ claim 2   quote found in source        PASS", -1.0, {"✓": OK_GREEN, "PASS": OK_GREEN})
        c3 = line("✗ claim 3   cited passage missing        FAIL", -1.6, {"✗": BAD_RED, "FAIL": BAD_RED})
        rep = line("→ report   eval/report.md", -2.3)

        def after(mob):                                      # cursor sits just after the text
            return [mob.get_right()[0] + 0.2, mob.get_center()[1], 0]

        cursor = Rectangle(width=0.18, height=0.38, stroke_width=0, fill_color=INK,
                           fill_opacity=1).move_to([left_x + 0.1, 1.0, 0])
        fail_mark = Line([left_x, -1.88, 0], [left_x + c3.width, -1.88, 0], stroke_color=BAD_RED,
                         stroke_width=4)

        clock.play(FadeIn(label), Create(window), FadeIn(bar), Create(dots), FadeIn(title),
                   FadeIn(cursor), run_time=1.0)
        # Typing starts as the first sentence ends (3.57 s) so the finished screen
        # holds for the last ~4.5 s of the beat.
        clock.until(3.6)
        clock.play(AddTextLetterByLetter(cmd), cursor.animate.move_to(after(cmd)), run_time=1.0)
        for ln in (ans, c1, c2, c3):
            clock.play(FadeIn(ln), cursor.animate.move_to(after(ln)), run_time=0.5)
        clock.play(Create(fail_mark), run_time=0.4)
        clock.play(FadeIn(rep), cursor.animate.move_to(after(rep)), run_time=0.5)
        clock.finish("B06")


class B07_VerifyLoop(Scene):
    """answer -> verify -> ✓ pass -> cited answer; ✗ fail -> retry once -> "not supported"."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        answer = tag("answer", 2.8, 1.2, 52).move_to([-4.7, 0.5, 0])
        verify = tag("verify", 2.8, 1.2, 52).move_to([-0.9, 0.5, 0])
        cited = tag("cited answer", 4.2, 1.2, 46).move_to([4.05, 2.45, 0])
        nots = tag("not supported", 4.2, 1.2, 46).move_to([4.05, -1.45, 0])
        a1 = Arrow(answer.get_right(), verify.get_left(), color=INK, stroke_width=6, buff=0.15)
        a_pass = Arrow(verify.get_right() + UP * 0.25, cited.get_left(), color=INK, stroke_width=6, buff=0.15)
        a_fail = Arrow(verify.get_right() + DOWN * 0.25, nots.get_left(), color=INK, stroke_width=6, buff=0.15)
        pass_lbl = VGroup(tick(scale=0.8), word("pass", 40, OK_GREEN)).arrange(RIGHT, buff=0.15) \
            .move_to([0.55, 2.25, 0])                     # above-left of the pass arrow
        fail_lbl = VGroup(cross(scale=0.6), word("fail", 40, BAD_RED)).arrange(RIGHT, buff=0.15) \
            .move_to([0.55, -1.25, 0])                    # below-left of the fail arrow
        back = CurvedArrow(verify.get_bottom() + DOWN * 0.15, answer.get_bottom() + DOWN * 0.15,
                           angle=-PI / 1.8, color=ACCENT, stroke_width=6)
        retry = word("retry once", 44).move_to([-2.8, -2.05, 0])     # beside the curve's low point
        dot = Dot(radius=0.18, color=ACCENT).move_to(answer.get_right())
        x_mark = cross(scale=0.9).next_to(verify, UP, buff=0.25)
        ring = SurroundingRectangle(nots, color=ACCENT, buff=0.14, corner_radius=0.24, stroke_width=7)

        clock.play(Create(answer[0]), FadeIn(answer[1]), run_time=0.9)
        clock.play(GrowArrow(a1), Create(verify[0]), FadeIn(verify[1]), run_time=0.9)
        clock.play(GrowArrow(a_pass), Create(cited[0]), FadeIn(cited[1]), FadeIn(pass_lbl), run_time=0.9)
        clock.play(GrowArrow(a_fail), Create(nots[0]), FadeIn(nots[1]), FadeIn(fail_lbl), run_time=0.9)
        clock.play(Create(back), FadeIn(retry), run_time=0.9)
        clock.until(7.25)                                    # "Code will check each quote ..."
        clock.play(FadeIn(dot), run_time=0.3)
        clock.play(dot.animate.move_to(verify.get_left()), run_time=1.0)
        clock.until(10.2)                                    # "A second model call will judge ..."
        clock.play(dot.animate.move_to(cited.get_left()), run_time=1.0)
        clock.play(FadeOut(dot), run_time=0.4)
        clock.until(15.93)                                   # "If a claim fails"
        dot.move_to(verify.get_left())
        clock.play(FadeIn(dot), Create(x_mark), run_time=0.6)
        clock.until(17.12)                                   # "the loop retries once"
        clock.play(MoveAlongPath(dot, back), FadeOut(x_mark), run_time=1.2)
        clock.play(dot.animate.move_to(verify.get_left()), run_time=0.6)
        clock.until(18.53)                                   # "or says the sources don't support it"
        clock.play(dot.animate.move_to(nots.get_left()), run_time=0.8)
        clock.play(FadeOut(dot), Create(ring), run_time=0.7)
        clock.finish("B07")


class B09_OwnHomework(Scene):
    """A hand grading its own paper (same name on both); then my own hand-written
    page, where a hard case gets a ✗."""

    def construct(self):
        self.camera.background_color = GROUND
        clock = Clock(self)
        paper = doc(width=4.4, height=5.8).move_to([-2.8, -0.1, 0])
        author = word("Claude", 48).move_to([-2.8, 2.05, 0])
        rows = [paper[2][0].get_left(), paper[2][1].get_left(), paper[2][2].get_left()]
        marks = VGroup(*[tick(scale=1.1).move_to(r + LEFT * 0.5) for r in rows])

        # Hand: a palm with four knuckles wrapped round a pencil, drawn in line.
        pencil = VGroup(
            Rectangle(width=0.35, height=3.2, stroke_color=INK, stroke_width=3),
            Polygon([-0.175, -1.6, 0], [0.175, -1.6, 0], [0, -2.1, 0], stroke_color=INK, stroke_width=3),
        )
        palm = RoundedRectangle(corner_radius=0.35, width=1.6, height=1.3,
                                stroke_color=INK, stroke_width=3).move_to([0.55, 0.2, 0])
        knuckles = VGroup(*[RoundedRectangle(corner_radius=0.15, width=0.55, height=0.32,
                                             stroke_color=INK, stroke_width=3)
                            .move_to([-0.15, 0.6 - 0.32 * i, 0]) for i in range(4)])
        hand = VGroup(pencil, palm, knuckles).rotate(-PI / 7).scale(1.4).move_to([2.7, 0.0, 0])
        hand_name = word("Claude", 48).move_to([4.9, 2.6, 0])
        grade = word("A+", 96, color=BAD_RED).move_to([-1.75, -2.05, 0])

        # My page: same page, my label, the third line replaced by a hard case.
        mine = doc(width=4.4, height=5.8).move_to([2.9, -0.1, 0])
        mine_title = fit(word("hand-written by me", 44), 3.8).move_to([2.9, 2.05, 0])
        hard = word("hard case", 40).move_to([3.0, -0.7, 0])
        hard_x = cross(scale=1.0).move_to([1.15, -0.7, 0])

        clock.play(Create(paper), FadeIn(author), run_time=1.5)
        clock.play(Create(hand), FadeIn(hand_name), run_time=1.5)
        clock.until(5.5)
        for m in marks:
            clock.play(Create(m), run_time=0.6)
        clock.play(Write(grade), run_time=0.8)
        clock.until(8.84)                                    # "So I'll write the hard cases myself"
        clock.play(FadeOut(hand), FadeOut(hand_name), run_time=0.6)
        clock.play(Create(VGroup(mine[0], mine[1], mine[2][0], mine[2][1])), FadeIn(mine_title),
                   run_time=1.2)
        clock.until(11.08)                                   # "including reversed decisions ..."
        clock.play(FadeIn(hard), run_time=0.6)
        clock.play(Create(hard_x), run_time=0.6)
        clock.finish("B09")
