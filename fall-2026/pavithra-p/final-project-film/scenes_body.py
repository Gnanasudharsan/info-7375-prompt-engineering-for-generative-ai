# ═════════════════════════════ DryRun pitch film v5: scenes ═════════════════════════════
# Body of scenes.py. build_scenes.py writes scenes.py = iso_kit.py + iso_originals_25.py + this file,
# because Gate A copies only scenes.py.
#
# v5 (resubmission, 2026-10-23): "shown, not asserted". B02 shows the real Claude screenshot, B03 my own
# Terminal lines from 13 Oct, B19 the real PR #33 test output; the text-only beats (B01, B12, B16, B17,
# B18, B20) get an approved prop that carries the idea. Narration, timing and labels are unchanged.
#
# v2 follows my Week 1 film: a course kicker top-left, short phrases (3-10 words) that appear when they
# are spoken, honesty chips (REAL / TESTED / CONSTRUCTED), source footers, and drawings only where they
# explain the mechanism (file ages, folder -> copy, the decision gate, the report card). Colours stay
# beige / ink / terracotta; terracotta is used only for small lights on objects, never for text.
#
# Timing: Clock places each cue where its phrase is spoken (character share of the narration, with
# pauses at punctuation, as in Week 1), keeps every animation out of the 0.6 s window around the clip
# midpoint (where GATE T and Gate V sample), and never runs past the measured audio.

FONT = "Helvetica Neue"
MONO = "Menlo"
OVERS = 4                      # render text 4x and scale down: fixes Manim's small-text kerning (Week 1)
KICKER = "INFO 7375 · DRYRUN · FINAL PROJECT PITCH"
CHIP = "#E6DED2"               # within 28/channel of the stage, so Gate V does not count it as ink
CARD_EDGE = "#B39A72"          # kraft edge, lighter than GATE T's text threshold
MAXW = 11.8


def P(s, size=38, bold=False, font=FONT, color=INK):
    """One line of text. Rendered at OVERS x and scaled down (Week 1's kerning fix); if Pango would wrap
    the oversized line, fall back to a smaller multiplier so the phrase always stays on one line."""
    for ov in (OVERS, 3, 2, 1):
        t = Text(s, font=font, font_size=size * ov, color=color, weight="BOLD" if bold else "NORMAL")
        t.scale_to_fit_width(t.width / ov)
        h = t.height
        if not isinstance(h, (int, float)) or h <= 0.019 * size:
            break
    if t.width > MAXW:
        t.scale_to_fit_width(MAXW)
    return t


def prop(pid, h, x, y):
    return no_terra(make_original(pid, height=h, x=x, y=y), pid)


def no_terra(m, pid):
    """v4: drop the props' terracotta lights. Pavithra asked for no orange dots anywhere in the film.
    Uses the prop data (shape order = submobject order), so Gate A's stub objects pass through."""
    for name, shapes in _ST_ORIGINALS_25[pid]["parts"].items():
        part = m.parts[name]
        try:
            for mob in [part.submobjects[i] for i, sh in enumerate(shapes) if sh.get("fill") == TERRA]:
                part.remove(mob)
        except (AttributeError, IndexError, TypeError):
            pass
    return m


def open_crate(h, x, y):
    """The context crate without its lid, so the files inside show: 'your folder' and its copy."""
    m = prop("context-crate", h, x, y)
    m.remove(m.parts["lid"])
    m.parts["context"].shift(UP * m.parts["crate-front"].height * 0.45)   # files stick up out of the box
    return m.move_to([x, y, 0])


def terminal(cmd, x, y, w=4.0, h=0.78):
    """A small terminal window: light card, dark title bar with three dots, the command in mono."""
    bar = Rectangle(width=w, height=0.16, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x, y + h / 2 - 0.08, 0])
    dots = VGroup(*[Circle(radius=0.035, fill_color=CHIP, fill_opacity=1, stroke_width=0)
                    .move_to([x - w / 2 + 0.16 + 0.13 * i, y + h / 2 - 0.08, 0]) for i in range(3)])
    t = P(cmd, 22, font=MONO).move_to([x, y - 0.08, 0])
    return VGroup(card(w, h, x, y), bar, dots, t)


def shell(lines, x, y, w, h, size=27):
    """v5: a bigger terminal for real output: the same card and title bar, lines left-aligned in mono.
    Returns (window, [line, ...]) so each line can appear when it is spoken."""
    bar = Rectangle(width=w, height=0.2, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x, y + h / 2 - 0.1, 0])
    dots = VGroup(*[Circle(radius=0.045, fill_color=CHIP, fill_opacity=1, stroke_width=0)
                    .move_to([x - w / 2 + 0.2 + 0.16 * i, y + h / 2 - 0.1, 0]) for i in range(3)])
    top = y + h / 2 - 0.2
    gap = (h - 0.2) / (len(lines) + 1)
    ts = [lx(P(s, size, font=MONO), x - w / 2 + 0.35, top - gap * (i + 1)) for i, s in enumerate(lines)]
    return VGroup(card(w, h, x, y), bar, dots), ts


EVID = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "evidence")


def screenshot_strips(name, box, cuts, width, x, y):
    """v5: a real screenshot from evidence/, cropped to `box` (px) and cut into horizontal strips at `cuts`
    (px), so each part appears when it is spoken. Nothing is redrawn or retyped. Upscaled once with Lanczos
    to the 4K pixel size. Gate A's sandbox has no evidence/ folder, so it gets plain blocks instead."""
    import numpy as np
    from PIL import Image
    x0, y0, x1, y1 = box
    edges = [y0, *cuts, y1]
    s = width / (x1 - x0)                  # units per screenshot pixel
    px = 3840 / 14.222                     # 4K pixels per unit
    out = []
    for a, b in zip(edges, edges[1:]):
        h = (b - a) * s
        cy = y + (y1 - y0) * s / 2 - (a - y0) * s - h / 2
        try:
            im = Image.open(_os.path.join(EVID, name)).convert("RGB").crop((x0, a, x1, b))
            im = im.resize((round(width * px), round(h * px)), Image.LANCZOS)
            m = ImageMobject(np.array(im))
            m.stretch_to_fit_width(width)      # exact size for every strip, so the seams line up
            m.stretch_to_fit_height(h)
            m.move_to([x, cy, 0])
        except Exception:
            m = Rectangle(width=width, height=h, fill_color=DARK_L, fill_opacity=1, stroke_width=0).move_to([x, cy, 0])
        out.append(m)
    return out


def lx(m, x0, y):
    """Left-align a phrase at x0."""
    return m.move_to([x0 + m.width / 2, y, 0])


def at_xy(m, x, y):
    return m.move_to([x, y, 0])


def chip(s, x, y, size=28, font=FONT, bold=True):
    t = P(s, size, bold=bold, font=font)
    r = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.34, corner_radius=0.12,
                         fill_color=CHIP, fill_opacity=1, stroke_width=0)
    g = VGroup(r, t)
    g.move_to([x, y, 0])
    return g


def card(w, h, x, y):
    shadow = Rectangle(width=w, height=h, fill_color=BOX_TOP, fill_opacity=1, stroke_width=0).move_to([x + 0.08, y - 0.08, 0])
    face = Rectangle(width=w, height=h, fill_color=CARD, fill_opacity=1, stroke_color=CARD_EDGE, stroke_width=2).move_to([x, y, 0])
    return VGroup(shadow, face)


def rule(y, half=3.0):
    return Line([-half, y, 0], [half, y, 0], color=INK, stroke_width=3)


def chrome(scene, footer=None):
    k = P(KICKER, 26)
    k.move_to([-6.1 + k.width / 2, 3.08, 0])
    scene.add(k)
    if footer:
        f = P(footer, 26)
        f.move_to([6.1 - f.width / 2, -3.05, 0])
        scene.add(f)


def _w(s):
    return len(s) + 6 * s.count(".") + 3 * s.count(",") + 4 * s.count(":") + 6 * s.count("?")


class Clock:
    def __init__(self, scene):
        self.s = scene
        bid = type(scene).__name__.split("_")[0]
        self.d = _TARGET.get(bid, 0)
        self.n = _NARR.get(bid, "")
        self.t = 0.0

    def wait(self, x):
        if x > 0.02:
            self.s.wait(x)
            self.t += x

    def play(self, *anims, rt=0.45):
        if self.d:
            lo, hi = self.d / 2 - 0.3, self.d / 2 + 0.3
            if self.t < hi and self.t + rt > lo:
                self.wait(hi - self.t)
            rt = max(0.2, min(rt, self.d - 0.12 - self.t))
        self.s.play(*anims, run_time=rt)
        self.t += rt

    def at(self, phrase, lead=0.15):
        i = self.n.find(phrase)
        if i < 0 or not self.d:
            return
        self.wait(self.d * _w(self.n[:i]) / _w(self.n) - lead - self.t)

    def finish(self):
        self.wait(max(self.d - 0.06 - self.t, 0.05) if self.d else 1.0)


def up(m):
    return FadeIn(m, shift=UP * 0.12)


# ─────────────────────────────────────────── scenes ───────────────────────────────────────────

class B00_Intro(Scene):
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(up(at_xy(P("Pavithra Prasad", 64, bold=True), 0, 1.7)))
        c.at("and I'm aiming")
        c.play(up(at_xy(P("Target role: backend and platform engineering", 36), 0, 0.75)))
        c.at("Dry Run will be")
        c.play(Create(rule(0.0)), up(at_xy(P("DryRun will test AI-suggested commands", 40, bold=True), 0, -0.85)),
               up(at_xy(P("before they touch your files", 40, bold=True), 0, -1.6)), rt=0.6)
        c.finish()

class B01_Problem(Scene):
    """v5: the phrases move to a left column; on the right, the AI's workstation hands a command down to
    your folder, and at "delete files" the files leave the folder."""
    def construct(self):
        c = Clock(self); chrome(self)
        L = -6.1
        desk = prop("agent-workstation", 1.9, 4.4, 1.2)
        c.play(up(lx(P("AI assistants suggest terminal commands", 30), L, 1.5)), FadeIn(desk))
        c.at("coding agents")
        crate = open_crate(1.7, 4.4, -1.45)
        arrow = Arrow([4.4, 0.12, 0], [4.4, -0.5, 0], buff=0, color=INK, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        c.play(up(lx(P("Coding agents run them", 30), L, 0.6)),
               desk.parts["tool"].animate.shift(desk.action_vectors["tool"]), GrowArrow(arrow), FadeIn(crate),
               up(at_xy(P("your files", 26), 4.4, -2.65)), rt=0.5)
        c.at("One wrong character")
        c.play(up(lx(P("One wrong character can delete files", 30, bold=True), L, -0.4)),
               FadeOut(crate.parts["context"], shift=UP * 0.4), up(at_xy(P("deleted", 26, bold=True), 4.4, -3.1)), rt=0.5)
        c.at("reading a command")
        c.play(FadeIn(chip("THE PROBLEM", -4.6, 2.35)), up(lx(P("Reading a command ≠ knowing what it does", 30), L, -1.4)))
        c.finish()


class B02_RealReply(Scene):
    """v5: the real screenshot (evidence/claude-reply-2026-10-11.png), cropped, never retyped. The whole reply is
    on screen from the start; a light outline marks Claude's command when it is spoken, then a line marks its
    preview advice. (Shown whole so GATE T's declared text regions are never empty; see qc in make_sheet.py.)"""
    def construct(self):
        c = Clock(self); chrome(self, "real screenshot, cropped · evidence/claude-reply-2026-10-11.png")
        W, Y, BOX = 11.6, -0.05, (300, 140, 1800, 615)
        strips = screenshot_strips("claude-reply-2026-10-11.png", BOX, (322, 540), W, 0, Y)
        s = W / (BOX[2] - BOX[0])
        def at(px, py):                     # screenshot pixel -> scene point
            return [-W / 2 + (px - BOX[0]) * s, Y + (BOX[3] - BOX[1]) * s / 2 - (py - BOX[1]) * s, 0]
        frame = card(W + 0.16, (BOX[3] - BOX[1]) * s + 0.16, 0, Y)
        c.play(FadeIn(chip("REAL SCREENSHOT · claude.ai · 11 Oct 2026", 0, 2.35)), FadeIn(frame), *[FadeIn(m) for m in strips], rt=0.6)
        c.at("It gave me this")
        (x0, y0), (x1, y1) = at(330, 446)[:2], at(1185, 506)[:2]
        mark = RoundedRectangle(width=x1 - x0, height=y0 - y1, corner_radius=0.08, stroke_color=CHIP, stroke_width=5,
                                fill_opacity=0).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        c.play(Create(mark), rt=0.5)
        c.at("told me to preview")
        c.play(Create(Line(at(324, 604), at(1494, 604), color=CHIP, stroke_width=5)), rt=0.45)
        c.finish()


class B03_Tested(Scene):
    """v5: my own Terminal lines from the 13 Oct re-run, copied exactly from evidence/mtime-test.md, then the
    three test files by age and which one the preview missed."""
    def construct(self):
        c = Clock(self); chrome(self, "lines copied exactly · evidence/mtime-test.md")
        win, (cmd, res) = shell(['$ find logs -type f -name "*.log" -mtime +7', "logs/eight-and-a-half-days.log"], 0, 1.05, 11.8, 1.55)
        c.play(FadeIn(chip("MY TERMINAL · 13 Oct 2026", 0, 2.35)), FadeIn(win), up(cmd), rt=0.5)
        c.at("on my Mac")
        rows = [("6.5 days old", -0.45), ("7.5 days old", -1.2), ("8.5 days old", -1.95)]
        files = VGroup(*[Rectangle(width=0.38, height=0.5, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=CARD_EDGE,
                                   stroke_width=2).move_to([-4.9, y, 0]) for _, y in rows])
        c.play(up(res), FadeIn(files), *[up(at_xy(P(a, 32), -2.7, y)) for a, y in rows], rt=0.55)
        c.at("seven and a half")
        band = Rectangle(width=11.4, height=0.62, fill_color=CHIP, fill_opacity=1, stroke_width=0).move_to([0, -1.2, 0]).set_z_index(-1)
        c.play(FadeIn(band), up(at_xy(P("not matched", 32), 2.2, -0.45)),
               up(at_xy(P("missed: older than 7 days", 32, bold=True), 2.2, -1.2)),
               up(at_xy(P("matched", 32), 2.2, -1.95)), rt=0.55)
        c.finish()

class B04_Copy(Scene):
    def construct(self):
        c = Clock(self); chrome(self)
        crate = open_crate(2.6, -4.3, -0.55)
        c.play(up(at_xy(P("It will be a GitHub repository", 42, bold=True), 0, 2.45)), FadeIn(crate),
               up(at_xy(P("your folder", 30), -4.3, -2.25)), rt=0.5)
        c.at("with tests")
        box = DashedVMobject(RoundedRectangle(width=5.0, height=2.6, corner_radius=0.2, stroke_color=INK, stroke_width=3),
                             num_dashes=70).move_to([3.75, -0.6, 0])
        copy = open_crate(2.1, 2.4, -0.6)
        arrow = Arrow([-2.95, -0.6, 0], [1.0, -0.6, 0], buff=0, color=INK, stroke_width=6)
        c.play(up(at_xy(P("+ tests + an evaluation report", 34), 0, 1.75)), GrowArrow(arrow),
               up(at_xy(P("DryRun will make a copy", 24), -0.95, -0.15)),
               Create(box), FadeIn(copy), up(at_xy(P("throwaway copy", 30), 3.75, -2.25)),
               FadeIn(chip("CONSTRUCTED SKETCH", 4.1, 3.08, size=24)), rt=0.5)
        c.at("evaluation report")
        drop = Arrow([3.15, 0.7, 0], [2.8, 0.3, 0], buff=0, color=INK, stroke_width=5, max_tip_length_to_length_ratio=0.4)
        c.play(FadeIn(terminal("find logs … -delete", 4.4, 1.08, w=3.7, h=0.72)), GrowArrow(drop),
               up(at_xy(P("changes happen", 24), 4.8, -0.35)), up(at_xy(P("only here", 24), 4.8, -0.75)),
               up(at_xy(P("Design goal: real files are never touched", 30), 0, -2.95)), rt=0.5)
        c.finish()

class B05_Contract(Scene):
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(up(at_xy(P("The AI will have to answer in a fixed format", 38), 0, 1.5)))
        c.at("the command")
        c.play(FadeIn(chip("STEP 1 · CONSTRUCTED EXAMPLE", 0, 2.35)), FadeIn(card(11.2, 0.95, 0, 0.35)),
               up(at_xy(P("Command", 30, bold=True), -4.55, 0.35)),
               up(at_xy(P("find logs … -mtime +7 -delete", 30, font=MONO), 0.9, 0.35)), rt=0.5)
        c.at("plus its own prediction")
        c.play(FadeIn(card(11.2, 0.95, 0, -0.85)), up(at_xy(P("Predicted", 30, bold=True), -4.55, -0.85)),
               up(at_xy(P("deletes the 7.5-day and 8.5-day logs", 30), 0.9, -0.85)), rt=0.5)
        c.finish()

class B06_Simulate(Scene):
    def construct(self):
        c = Clock(self); chrome(self, "simulated from my 11 Oct preview test (1 file matched)")
        c.play(up(at_xy(P("Planned: locked container · no network", 36), 0, 1.5)))
        c.at("Then it will compare")
        before = VGroup(at_xy(P("before", 32, bold=True), -3.2, 0.6),
                        *[at_xy(P(f"{a}-day log", 32), -3.2, y) for a, y in (("6.5", -0.15), ("7.5", -0.8), ("8.5", -1.45))])
        after = VGroup(at_xy(P("after", 32, bold=True), 3.2, 0.6),
                       *[at_xy(P(f"{a}-day log", 32), 3.2, y) for a, y in (("6.5", -0.15), ("7.5", -0.8))])
        arrow = Arrow([-1.3, -0.8, 0], [1.3, -0.8, 0], buff=0, color=INK, stroke_width=6)
        c.play(FadeIn(chip("STEP 2 · CONSTRUCTED SIMULATION", 0, 2.35)), up(before), rt=0.5)
        c.at("before and after")
        c.play(GrowArrow(arrow), up(after), rt=0.5)
        c.at("or deleted")
        c.play(up(at_xy(P("Simulated: the 8.5-day log would be deleted", 34, bold=True), 0, -2.35)))
        c.finish()

class B07_Gate(Scene):
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(up(at_xy(P("Predicted 2 deleted · simulated 1", 36), 0, 1.5)))
        c.at("the task's rules")
        c.play(FadeIn(chip("STEP 3 · CONSTRUCTED EXAMPLE", 0, 2.35)),
               up(at_xy(P("Rule: every .log older than 7 days", 34), 0, 0.75)))
        c.at("Then it will allow")
        gate = prop("permission-gate", 2.3, -4.2, -1.2)
        chips = [chip(s, x, -0.55, size=30) for s, x in (("ALLOW", 0.3), ("WARN", 2.55), ("BLOCK", 4.85))]
        c.play(FadeIn(gate), *[FadeIn(k) for k in chips], rt=0.5)
        c.at("warn, or block")
        mark = Line([2.0, -1.05, 0], [3.1, -1.05, 0], color=INK, stroke_width=6)
        c.play(Create(mark), gate.parts["barrier"].animate.shift(gate.action_vectors["barrier"] * 0.5),
               up(at_xy(P("WARN: 1 matching file not deleted", 32, bold=True), 2.4, -1.7)), rt=0.5)
        c.at("When it can't tell")
        c.play(up(at_xy(P("Can't tell? It will say so.", 30), 2.4, -2.35)))
        c.finish()

class B08_Retry(Scene):
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(up(at_xy(P("A blocked command's changes will go back to the AI", 36), 0, 1.0)))
        c.at("which will try again")
        loop = Arrow([3.4, -0.1, 0], [-3.4, -0.1, 0], buff=0, color=INK, stroke_width=6)
        c.play(FadeIn(chip("IN A LATER PHASE", 0, 2.35)), GrowArrow(loop),
               up(at_xy(P("It will retry, up to 3 times", 40, bold=True), 0, -1.0)), rt=0.5)
        c.finish()

class B09_Report(Scene):
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(FadeIn(chip("STEP 4 · REPORT · CONSTRUCTED MOCK-UP", 0, 2.35)), FadeIn(card(11.4, 3.7, 0, -0.05)), rt=0.5)
        rows = [("see the command", "Command", "find logs … -mtime +7 -delete", MONO, 1.15),
                ("its predicted changes", "Predicted", "2 logs deleted", FONT, 0.35),
                ("the real file differences", "Simulated", "1 log deleted", FONT, -0.45)]
        for cue, k, v, font, y in rows:
            c.at(cue)
            c.play(up(at_xy(P(k, 32, bold=True), -4.2, y)), up(at_xy(P(v, 32, font=font), 1.2, y)))
        c.at("The tests and report")
        c.play(Create(Line([-5.3, -0.95, 0], [5.3, -0.95, 0], color=CARD_EDGE, stroke_width=2)),
               up(at_xy(P("Decision: WARN · 1 file missed", 36, bold=True), 0, -1.45)), rt=0.5)
        c.finish()


class B10_Traps(Scene):
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(up(at_xy(P("I'll build trap folders to catch mistakes", 40, bold=True), 0, 2.1)))
        items = [("names with spaces", "my report.log", MONO, "space in the name", -4.0, 0.75),
                 ("names that look like options", "-rf.log", MONO, "looks like an option", 0.0, 0.75),
                 ("hidden files", ".env.log", MONO, "hidden file", 4.0, 0.75),
                 ("files right at a time limit", "7.5 days old", FONT, "right at the time limit", -3.2, -1.05),
                 ("links that point outside", "link → outside the folder", FONT, "points outside", 2.4, -1.05)]
        for cue, name, font, cap, x, y in items:
            c.at(cue)
            c.play(FadeIn(chip(name, x, y, size=30, font=font, bold=False)), up(at_xy(P(cap, 26), x, y - 0.68)), rt=0.4)
        c.finish()


class B11_Measure(Scene):
    """v5: a queue of tasks with known answers; the next task moves up as each trap folder is named."""
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(up(at_xy(P("Then I'll measure it", 40, bold=True), 0, 2.2)))
        c.at("tasks with known")
        queue = prop("task-queue", 1.7, -4.9, 0.85)
        c.play(FadeIn(queue), up(at_xy(P("Tasks with known correct results", 36), 0.6, 1.4)))
        c.at("across every trap folder")
        c.play(queue.parts["next-task"].animate.shift(queue.action_vectors["next-task"]), up(at_xy(P("× every trap folder", 36), 0.6, 0.7)))
        c.at("comparing Claude")
        c.play(FadeIn(chip("Claude", -1.8, -0.1, size=32)), up(at_xy(P("vs", 30), 0.6, -0.1)),
               FadeIn(chip("free local model", 3.2, -0.1, size=32)), rt=0.45)
        c.at("did too much")
        c.play(up(at_xy(P("Did too much: —", 34), -2.2, -1.2)), up(at_xy(P("Did too little: —", 34), 3.4, -1.2)))
        c.at("or too little")
        c.play(FadeIn(chip("PLANNED · NOT MEASURED YET", 0.6, -2.15)))
        c.finish()


class B12_Alternatives(Scene):
    def construct(self):
        # v5: one prop per alternative. try = a checkpoint that inspects a command's changes as they pass;
        # the research benchmarks = a binder of recorded tasks that is opened and scored.
        c = Clock(self); chrome(self, "github.com/binpash/try · arXiv 2306.14898 · arXiv 2502.06858")
        scan = prop("checkpoint-scanner", 1.7, -3.3, 0.8)
        c.play(FadeIn(scan), up(at_xy(P("try", 36, bold=True), -3.3, -0.55)))
        c.at("preview a command")
        c.play(scan.parts["parcel"].animate.shift(scan.action_vectors["parcel"]),
               up(at_xy(P("previews a command's file changes", 26), -3.3, -1.1)), rt=0.5)
        c.at("on Linux")
        c.play(up(at_xy(P("Linux only", 26), -3.3, -1.6)), rt=0.35)
        c.at("Research benchmarks")
        binder = prop("evidence-binder", 1.5, 3.3, 0.75)
        c.play(Create(Line([0, 1.6, 0], [0, -1.9, 0], color=INK, stroke_width=3)), FadeIn(binder),
               up(at_xy(P("Research benchmarks", 36, bold=True), 3.3, -0.55)),
               up(at_xy(P("score AI commands offline", 26), 3.3, -1.1)), rt=0.5)
        c.play(FadeIn(chip("WHAT ALREADY EXISTS", 0, 2.35)), binder.parts["cover"].animate.shift(binder.action_vectors["cover"]),
               up(at_xy(P("InterCode · NL2SH", 26), 3.3, -1.6)), rt=0.45)
        c.finish()


class B13_Different(Scene):
    """v4: the whole planned workflow in one picture (Pavithra's reference image, redrawn in the film's
    palette): your folder -> throwaway copy -> compare -> you decide."""
    def construct(self):
        c = Clock(self); chrome(self)
        Y = -0.35
        crate = open_crate(1.8, -5.0, Y)
        box = DashedVMobject(RoundedRectangle(width=2.2, height=2.0, corner_radius=0.18, stroke_color=INK, stroke_width=3),
                             num_dashes=48).move_to([-2.15, Y, 0])
        copy = open_crate(1.3, -2.15, Y)
        a1 = Arrow([-4.05, Y, 0], [-3.35, Y, 0], buff=0, color=INK, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        c.play(up(at_xy(P("DryRun will go one step further", 42, bold=True), 0, 2.4)), FadeIn(chip("PLANNED · CONSTRUCTED SKETCH", 0, 1.6)),
               FadeIn(crate), GrowArrow(a1), Create(box), FadeIn(copy),
               up(at_xy(P("your folder", 26), -5.0, -1.85)), up(at_xy(P("untouched", 24), -5.0, -2.3)),
               up(at_xy(P("throwaway copy", 26), -2.15, -1.85)), up(at_xy(P("command runs here", 24), -2.15, -2.3)), rt=0.6)
        c.at("It will compare")
        a2 = Arrow([-0.95, Y, 0], [-0.3, Y, 0], buff=0, color=INK, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        rows = VGroup(at_xy(P("Change report", 24, bold=True), 1.35, 0.3), at_xy(P("1 log deleted", 24), 1.35, -0.12),
                      Line([0.05, -0.42, 0], [2.65, -0.42, 0], color=INK, stroke_width=2),
                      at_xy(P("vs your request", 24), 1.35, -0.72), at_xy(P("vs AI prediction", 24), 1.35, -1.1))
        c.play(GrowArrow(a2), FadeIn(card(3.2, 2.0, 1.35, Y)), FadeIn(rows),
               up(at_xy(P("compare", 26), 1.35, -1.85)), up(at_xy(P("flags mismatches", 24), 1.35, -2.3)), rt=0.5)
        c.at("and flag mismatches")
        fork = VGroup(*[Arrow([3.05, Y, 0], [3.95, y, 0], buff=0, color=INK, stroke_width=4, max_tip_length_to_length_ratio=0.25)
                        for y in (0.45, Y, -1.15)])
        c.play(*[GrowArrow(a) for a in fork],
               *[FadeIn(chip(t, 4.85, y, size=26)) for t, y in (("ALLOW", 0.45), ("WARN", Y), ("BLOCK", -1.15))],
               up(at_xy(P("you decide", 26), 4.85, -1.85)), up(at_xy(P("before you run it", 24), 4.85, -2.3)), rt=0.5)
        c.finish()

class B14_Skills(Scene):
    """v5: the four skill chips as before; the fair conclusion now has a review desk, and the evidence is
    brought onto it at "check an AI's work"."""
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(up(at_xy(P("Course skills it will show", 42, bold=True), 0, 2.25)))
        for cue, s, x, y in (("a prompt contract", "prompt contract", -3.0, 1.15),
                             ("verification that", "verification, not trust", 3.0, 1.15),
                             ("an agent loop", "agent loop", -3.0, 0.0),
                             ("an evaluation you can rerun", "evaluation you can rerun", 3.0, 0.0)):
            c.at(cue)
            c.play(FadeIn(chip(s, x, y, size=34, bold=False)), rt=0.4)
        c.at("A reviewer could")
        desk = prop("review-desk", 1.7, -4.8, -1.9)
        paper = desk.parts["evidence"]
        paper.shift(desk.action_vectors["evidence"])          # the evidence starts off the desk
        c.play(Create(rule(-0.85, 3.0)), FadeIn(desk), up(lx(P("Fair conclusion:", 30, bold=True), -3.2, -1.3)),
               up(lx(P("I can check and measure an AI's work", 30, bold=True), -3.2, -1.85)), rt=0.5)
        c.at("check an AI's work")
        c.play(paper.animate.shift(-desk.action_vectors["evidence"]), rt=0.5)
        c.at("not that Dry Run")
        c.play(FadeIn(chip("NOT CLAIMED: DryRun makes commands safe", 1.0, -2.7, size=26)))
        c.finish()


class B15_Scope(Scene):
    """v5: the folder it checks; then a test bench where the self-test plants a sample, the change it must find."""
    def construct(self):
        c = Clock(self); chrome(self)
        X = -3.0
        c.play(FadeIn(open_crate(1.6, -4.8, 1.45)), up(lx(P("It will only check files and folders", 30), X, 1.95)))
        c.at("Network calls")
        c.play(up(lx(P("Out: network calls, outside services, databases", 28), X, 1.3)))
        c.at("The first piece")
        bench = prop("experiment-bench", 2.0, -4.7, -1.35)
        sample = bench.parts["sample"]
        sample.shift(bench.action_vectors["sample"])          # lifted out until the self-test plants it
        c.play(FadeIn(bench), FadeIn(chip("FIRST PIECE TO RUN", X + 2.2, 0.4)),
               up(lx(P("one command → one copy → a change list", 30, bold=True), X, -0.3)), rt=0.5)
        c.at("You'll know it ran")
        c.play(sample.animate.shift(-bench.action_vectors["sample"]), FadeIn(chip("HOW YOU'LL KNOW IT RAN", X + 2.83, -1.2)),
               up(lx(P("its self-test finds the changes it planted", 28, bold=True), X, -1.9)), rt=0.5)
        c.finish()


class B16_Intent(Scene):
    """v5: an inspection lamp lowers onto one task sheet: start small, with tasks that can be checked."""
    def construct(self):
        c = Clock(self); chrome(self)
        lamp = prop("inspection-lamp", 3.0, -4.6, -0.7)
        c.play(up(at_xy(P("Hardest part: knowing what you meant", 40, bold=True), 0, 1.45)), FadeIn(lamp))
        c.at("I'll start with")
        c.play(lamp.parts["lamp-head"].animate.shift(lamp.action_vectors["lamp-head"]),
               up(lx(P("I'll start with file tasks that can be checked", 28), -2.7, -0.05)), rt=0.5)
        c.at("report uncertainty")
        c.play(FadeIn(chip("BIGGEST RISK", 0, 2.35)), up(lx(P("It will say “can't tell” instead of guessing", 28), -2.7, -1.25)))
        c.finish()

class B17_MacLinux(Scene):
    """v5: two trays, one per toolset; at "the first version" the Linux sample is lifted out."""
    def construct(self):
        c = Clock(self); chrome(self)
        trays = prop("comparison-trays", 2.4, -4.4, -0.75)
        c.play(up(at_xy(P("My Mac's tools ≠ Linux tools", 40), 0, 1.5)), FadeIn(trays),
               up(at_xy(P("Mac", 26, bold=True), -5.8, -2.2)), up(at_xy(P("Linux", 26, bold=True), -2.8, 0.6)))
        c.play(up(lx(P("Same command, different behaviour", 30), -1.6, 0.0)), up(lx(P("(e.g. sed -i)", 30), -1.6, -0.55)), rt=0.45)
        c.at("so the first version")
        c.play(FadeIn(chip("SECOND RISK", 0, 2.35)), trays.parts["sample-b"].animate.shift(trays.action_vectors["sample-b"] * 0.6),
               up(lx(P("Version 1 will target Linux behaviour", 30, bold=True), -1.6, -1.6)))
        c.finish()

class B18_Why(Scene):
    """v5: my portfolio shelf, and the empty slot beside it that DryRun is meant to fill."""
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(up(at_xy(P("Why DryRun: a stronger portfolio", 40, bold=True), 0, 1.75)))
        c.at("I've built web apps")
        c.play(FadeIn(prop("version-shelves", 2.3, -4.7, -0.55)), up(at_xy(P("my portfolio", 26), -4.7, -2.15)),
               up(lx(P("Built before: web apps", 32), -0.6, 0.2)), rt=0.45)
        c.at("but nothing")
        slot = DashedVMobject(RoundedRectangle(width=1.8, height=2.1, corner_radius=0.15, stroke_color=INK, stroke_width=3),
                              num_dashes=40).move_to([-2.2, -0.55, 0])
        c.play(Create(slot), up(lx(P("Missing: a project", 32), -0.6, -0.7)), up(lx(P("that checks an AI's work", 32), -0.6, -1.25)))
        c.finish()


class B19_Learning(Scene):
    """v5: "already know" is backed by the real PR #33 test output (evidence/pr33-tests-2026-10-23.md)."""
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(FadeIn(chip("ALREADY KNOW", -3.2, 2.3)), up(at_xy(P("Python, testing", 36), -3.2, 1.55)),
               up(at_xy(P("internship · PR #33 (32 tests)", 26), -3.2, 1.05)))
        c.at("thirty-two passing")
        win, lines = shell(["Ran 32 tests in 0.775s", "OK"], -3.2, 0.0, 5.4, 1.45, size=26)
        c.play(FadeIn(win), *[up(t) for t in lines], FadeIn(chip("REAL OUTPUT · PR #33 · 23 Oct 2026", -3.2, -1.2, size=24)), rt=0.5)
        c.at("I've used Docker")
        c.play(up(at_xy(P("Docker", 36), -3.2, -1.9)), up(at_xy(P("Northeastern cloud project", 26), -3.2, -2.4)))
        c.at("Sandboxing")
        c.play(FadeIn(chip("NEW TO ME", 3.2, 2.3)), *[up(at_xy(P(s, 36), 3.2, y)) for s, y in
                                                     (("sandboxing", 1.5), ("file diffing", 0.8), ("evaluation design", 0.1))], rt=0.5)
        c.at("mostly new learning")
        c.play(Create(Line([1.0, -0.65, 0], [5.4, -0.65, 0], color=INK, stroke_width=3)),
               up(at_xy(P("Mostly new learning", 40, bold=True), 3.2, -1.3)), rt=0.45)
        c.finish()


class B20_Today(Scene):
    """v5: a sealed parcel: nothing is delivered yet; the four phases line up beside it."""
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(up(at_xy(P("Today: no DryRun code yet", 40, bold=True), 0, 1.75)), FadeIn(prop("release-parcel", 2.6, -4.5, -0.8)))
        c.at("Everything in this film")
        c.play(up(lx(P("Everything here is what I will build", 30), -2.4, 0.8)))
        c.at("in four phases")
        c.play(*[FadeIn(chip(s, 1.4, y, size=26, bold=False)) for s, y in
                 (("1 · CLI core", 0.05), ("2 · Claude Code hook + retry", -0.75),
                  ("3 · evaluation + report", -1.55), ("4 · API · dashboard · CI", -2.35))], rt=0.45)
        c.finish()


class B21_Close(Scene):
    def construct(self):
        c = Clock(self); chrome(self)
        c.play(up(at_xy(P("DryRun", 72, bold=True), 0, 1.0)))
        c.at("See what")
        c.play(up(at_xy(P("See what an AI's command will do", 38), 0, -0.15)))
        c.at("before it touches")
        c.play(up(at_xy(P("before it touches your files", 38), 0, -0.85)), Create(rule(-1.6, 2.4)),
               up(at_xy(P("Pavithra Prasad · INFO 7375 · Final project pitch", 28), 0, -2.2)), rt=0.45)
        c.finish()
