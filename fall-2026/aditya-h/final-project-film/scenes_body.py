# ═════════════════════════════ PRODUCTLENS AI — body scenes (show-tell, v2) ═════════════════════════════
# Written by Claude Code for Aditya Hasija, 2026-10-25, from his approved SCRIPT-v2.md. build_scenes.sh pastes
# iso_kit.py and iso_originals_25.py above this file to make scenes.py (Gate A copies only scenes.py).
# Cast kept for the whole film: the feature idea = a small card, public articles = white pages, agents = dark blocks,
# the checker = the review desk, the decision brief = one large page.
# Honesty: drawings of the unbuilt product carry the corner tag "constructed". B05/B06 show crops of Aditya's real
# ChatGPT screenshot (made by prepare_crops.py: cut, colour-inverted, enlarged; nothing retouched), tagged as such.
import os as _os2

_HERE = _os2.path.dirname(_os2.path.abspath(__file__))


def label(s, x, y, size=40):
    return T(s, size=size).move_to([x, y, 0])


SK = " · concept sketch"   # marks drawings of the unbuilt product (assignment: mock-ups labelled on screen)
REAL = " · Oct 25 · colours inverted"
SUBHEAD = {
    "B00": "The problem: a checkout decision", "B01": "The problem: research takes days",
    "B02": "What ProductLens does" + SK, "B03": "The decision brief" + SK, "B04": "How it will work" + SK,
    "B05": "My real test · ChatGPT" + REAL, "B06": "What ChatGPT did" + REAL,
    "B07": "How it's different" + SK, "B08": "What I'll deliver" + SK, "B09": "Who opens it first" + SK,
    "B10": "What it should prove" + SK, "B11": "The first milestone" + SK, "B12": "Out of scope" + SK,
    "B13": "The biggest risk" + SK, "B14": "How I'll measure it" + SK,
    "B15": "Why I changed my pitch", "B16": "Why this project", "B17": "Where it stands today",
}


def sub(scene):
    """Bottom subheader: what this part of the film is about (replaces the corner 'constructed' tag)."""
    return T(SUBHEAD[type(scene).__name__.split("_")[0]], size=34).move_to([0, -3.13, 0])


def sheet(x, y, w=2.2, h=2.8, lines=4, gap=0.42):
    """A flat white page with ink outline and grey 'claim' lines; returns (group, line_list)."""
    pg = paper(x, y, w=w, h=h)
    top = y + h / 2 - 0.55
    ls = [Line([x - w / 2 + 0.3, top - i * gap, 0], [x + w / 2 - 0.3 - (0.5 if i == lines - 1 else 0), top - i * gap, 0],
               color=BAR2, stroke_width=6) for i in range(lines)]
    return VGroup(pg, *ls), ls


def small_box(iso, x0, y0, s=0.9):
    return iso.box(x0, y0, 0, s, s, s * 0.8)


def feature_card(x, y, w=1.9, h=1.3):
    """The film's 'feature idea': a small white card with a tiny cart outline on it."""
    card = paper(x, y, w=w, h=h)
    cart = VGroup(Line([x - 0.45, y + 0.25, 0], [x - 0.3, y + 0.25, 0], color=INK, stroke_width=5),
                  Polygon([x - 0.3, y + 0.25, 0], [x + 0.45, y + 0.25, 0], [x + 0.35, y - 0.12, 0], [x - 0.2, y - 0.12, 0],
                          stroke_color=INK, stroke_width=5, fill_opacity=0),
                  Circle(radius=0.07, color=INK, stroke_width=5).move_to([x - 0.12, y - 0.3, 0]),
                  Circle(radius=0.07, color=INK, stroke_width=5).move_to([x + 0.28, y - 0.3, 0]))
    return VGroup(card, cart)


def shot(name, width):
    """A crop of Aditya's real screenshot with an ink frame. Falls back to a grey slab where the file isn't present
    (Gate A's sandbox holds only scenes.py)."""
    try:
        im = ImageMobject(_os2.path.join(_HERE, "research", "film-crops", name + ".png"))
        im.width = width
        frame = Rectangle(width=im.width, height=im.height, stroke_color=INK, stroke_width=12, fill_opacity=0)
        return Group(im, frame)
    except Exception:
        return VGroup(Rectangle(width=width, height=width * 0.28, fill_color=BAR3, fill_opacity=1, stroke_color=INK, stroke_width=4))


_ManimScene = Scene


class Scene(_ManimScene):   # guarded Scene: keeps `class Bxx(Scene)` so run.sh's scene discovery regex still matches
    """Midpoint guard: Gate T and Gate V sample each clip at its midpoint, so no animation may be running then.
    Any play() that would overlap [mid - 0.3 s, mid + 0.3 s] first waits until mid + 0.3 s."""
    MARGIN = 0.3

    def play(self, *anims, **kw):
        target = _TARGET.get(type(self).__name__.split("_")[0], 0)
        rt = kw.get("run_time", 1.0)
        if target and not all(isinstance(x, Wait) for x in anims):
            mid, t0 = target / 2.0, _elapsed(self)
            if t0 < mid + self.MARGIN and t0 + rt > mid - self.MARGIN:
                _ManimScene.wait(self, mid + self.MARGIN - t0)
        return _ManimScene.play(self, *anims, **kw)


class B00_Checkout(Scene):
    def construct(self):
        self.add(sub(self))
        steps = VGroup(*[sheet(-4.2 + i * 2.2, 0.6, w=1.8, h=2.2, lines=3, gap=0.4)[0] for i in range(4)])
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.3) for s in steps], lag_ratio=0.25), run_time=0.7)
        four = label("4 steps", -0.9, -1.2)
        self.play(FadeIn(four), run_time=0.3)
        until(self, "one-page checkout")
        one, _ = sheet(3.6, 0.4, w=2.2, h=3.0, lines=6, gap=0.38)
        self.play(*[s.animate.move_to([3.6, 0.4, 0]).set_opacity(0) for s in steps], four.animate.set_opacity(0), FadeIn(one), run_time=0.6)
        self.play(FadeIn(label("1 page", 3.6, -1.6)), run_time=0.3)
        finish(self)


class B01_Questions(Scene):
    def construct(self):
        self.add(sub(self))
        xs, names = [-4.0, 0.0, 4.0], ["customers", "competitors", "risks"]
        phrases = ["what customers want", "what other stores do", "what could go wrong"]
        for x, n, ph in zip(xs, names, phrases):
            until(self, ph)
            card = VGroup(paper(x, 0.8, w=2.4, h=2.6), T("?", 110, bold=True).move_to([x, 0.8, 0]))
            self.play(FadeIn(card, shift=UP * 0.4), FadeIn(label(n, x, -1.05)), run_time=0.5)
        until(self, "That research takes days")
        clock = VGroup(Circle(radius=0.5, color=INK, stroke_width=6),
                       Line([0, 0, 0], [0, 0.35, 0], color=INK, stroke_width=6),
                       Line([0, 0, 0], [0.25, -0.1, 0], color=TERRA, stroke_width=6)).move_to([0, -2.3, 0])
        self.play(FadeIn(clock), run_time=0.4)
        finish(self)


class B02_InOut(Scene):
    def construct(self):
        machine = make_original("server-tower", height=2.6, x=-0.2, y=0.0)
        self.add(machine, sub(self))
        until(self, "You type in the feature")
        card = feature_card(-5.0, 1.2)
        self.play(FadeIn(card, shift=RIGHT * 0.5), FadeIn(label("feature", -5.0, 0.2, 36)), run_time=0.5)
        until(self, "attach a few public articles")
        arts = VGroup(*[sheet(-5.3 + i * 0.6, -1.6 + i * 0.15, w=1.2, h=1.5, lines=2, gap=0.35)[0] for i in range(2)])
        self.play(FadeIn(arts, shift=RIGHT * 0.5), run_time=0.5)
        c2, a2 = card.copy(), arts.copy()
        self.play(c2.animate.scale(0.3).move_to([-0.9, 0.3, 0]).set_opacity(0),
                  a2.animate.scale(0.3).move_to([-0.9, -0.3, 0]).set_opacity(0), run_time=0.8)
        self.remove(c2, a2)
        until(self, "It will give back")
        brief, _ = sheet(4.2, 0.4, w=2.4, h=3.0, lines=5, gap=0.42)
        self.play(GrowFromCenter(Dot([0.25, 0.35, 0], radius=0.12, color=TERRA)), run_time=0.3)
        self.play(FadeIn(brief, shift=RIGHT * 0.8), FadeIn(label("brief", 4.2, -1.5)), run_time=0.7)
        finish(self)


class B03_Brief(Scene):
    def construct(self):
        self.add(sub(self))
        page = paper(-1.2, 0.35, w=4.6, h=5.0)
        self.play(FadeIn(page, shift=UP * 0.3), run_time=0.5)
        rows = []
        for i, ph in enumerate(["the biggest risks", "the numbers to watch", "the first experiment"]):
            until(self, ph)
            y = 1.9 - i * 1.55
            bar = Rectangle(width=3.6, height=0.32, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([-1.2, y, 0])
            ls = VGroup(*[Line([-3.0, y - 0.45 - k * 0.32, 0], [0.4 - k * 0.6, y - 0.45 - k * 0.32, 0], color=BAR3, stroke_width=6)
                          for k in range(2)])
            self.play(FadeIn(bar), Create(ls), run_time=0.5)
            rows.append(ls)
        until(self, "Every claim")
        t1 = VGroup(pill(3.3, 1.2, 1.9, fill=CARD).set_stroke(INK, 4), T("sourced", 34).move_to([3.3, 1.2, 0]))
        a1 = Arrow([2.3, 1.2, 0], [0.6, 1.45, 0], color=INK, stroke_width=5, buff=0.05, max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(t1, shift=LEFT * 0.2), Create(a1), run_time=0.5)
        until(self, "or an assumption")
        t2 = VGroup(pill(3.5, -1.4, 2.4, fill=BAR3), T("assumption", 34).move_to([3.5, -1.4, 0]))
        a2 = Arrow([2.3, -1.4, 0], [0.0, -1.55, 0], color=INK, stroke_width=5, buff=0.05, max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(t2, shift=LEFT * 0.2), Create(a2), run_time=0.5)
        finish(self)


class B04_Agents(Scene):
    def construct(self):
        card = feature_card(-5.5, -0.2, w=1.6, h=1.1)
        self.add(card, sub(self))
        ys = [2.0, 0.0, -2.0]
        blocks = VGroup(*[Iso(-1.6, y - 0.4, 0.75).mcp(0, 0, 0) for y in ys])
        wires = VGroup(*[Line([-4.6, -0.1, 0], [-2.2, y, 0], color=DIM, stroke_width=5) for y in ys])
        self.play(LaggedStart(*[Create(w) for w in wires], lag_ratio=0.2), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in blocks], lag_ratio=0.2), run_time=0.7)
        self.play(*[FadeIn(label(n, 0.6, y + 0.1, 36)) for n, y in zip(["market", "customers", "risks"], ys)], run_time=0.4)
        until(self, "A fourth agent")
        desk = make_original("review-desk", height=2.3, x=4.6, y=-0.3)
        self.play(FadeIn(desk, shift=LEFT * 0.4), FadeIn(label("checker", 4.6, -2.2, 36)), run_time=0.6)
        notes = VGroup(*[paper(2.0, y, w=0.7, h=0.9) for y in ys])
        self.play(FadeIn(notes), run_time=0.3)
        self.play(*[n.animate.move_to([4.0 + i * 0.5, 0.6 - i * 0.12, 0]) for i, n in enumerate(notes)], run_time=0.8)
        until(self, "can send one back")
        self.play(notes[2].animate.move_to([2.0, -2.0, 0]), run_time=0.5)
        self.play(notes[2].animate.move_to([5.0, 0.36, 0]), run_time=0.5)
        self.play(FadeIn(label("1 retry", 2.0, -2.4, 36)), run_time=0.3)
        finish(self)


class B05_RealRun(Scene):
    def construct(self):
        self.add(sub(self))
        self.play(FadeIn(label("my real test", -4.3, 3.0, 40)), run_time=0.4)
        until(self, "On October 25th")
        date = shot("date", 2.8).move_to([4.0, 3.0, 0])
        prompt = shot("prompt", 10.0).move_to([0, 0.1, 0])
        self.play(FadeIn(date, shift=DOWN * 0.2), run_time=0.4)
        self.play(FadeIn(prompt, shift=UP * 0.3), run_time=0.6)
        until(self, "a made-up claim")
        # underline the planted claim: "Baymard Institute research shows one-page / checkouts always convert better"
        cx, cy = 0.0, 0.1
        u1 = Line([cx - 2.61, cy + 0.32, 0], [cx + 3.28, cy + 0.32, 0], color=TERRA, stroke_width=9)
        u2 = Line([cx - 4.68, cy - 0.16, 0], [cx - 0.06, cy - 0.16, 0], color=TERRA, stroke_width=9)
        self.play(Create(u1), run_time=0.5)
        self.play(Create(u2), run_time=0.4)
        self.play(FadeIn(label("planted claim", 0.0, -2.0, 40)), run_time=0.3)
        until(self, "Their research says")
        self.play(Indicate(VGroup(u1, u2), color=TERRA, scale_factor=1.04), run_time=0.6)
        finish(self)


class B06_RealGap(Scene):
    def construct(self):
        self.add(sub(self))
        premise = shot("premise", 11.0).move_to([0, 1.7, 0])
        self.play(FadeIn(premise, shift=UP * 0.3), run_time=0.6)
        self.play(Create(check(5.9, 2.5, 0.3, TERRA, 9)), run_time=0.4)
        until(self, "But only one paragraph")
        chip = shot("chipzoom", 9.6).move_to([0, -0.9, 0])
        self.play(FadeIn(chip, shift=UP * 0.3), run_time=0.5)
        ring = Ellipse(width=4.8, height=1.75, color=INK, stroke_width=9).move_to([2.3, -0.9, 0])
        self.play(Create(ring), run_time=0.5)
        self.play(FadeIn(label("1 source", 2.3, -2.2, 40)), run_time=0.3)
        until(self, "it rarely said")
        self.play(FadeIn(label("fact or guess?", -3.0, -2.2, 40)), run_time=0.4)
        finish(self)


class B07_Narrower(Scene):
    def construct(self):
        self.add(sub(self))
        big = make_original("context-crate", height=3.4, x=-3.4, y=0.0)
        until(self, "Tools like")
        self.play(FadeIn(big, shift=DOWN * 0.4), FadeIn(label("startup idea", -3.4, -2.15)), run_time=0.6)
        until(self, "ProductLens is for one feature")
        card = feature_card(3.4, 0.6, w=2.4, h=1.6)
        self.play(FadeIn(card, scale=0.8), FadeIn(label("one feature", 3.4, -0.6)), run_time=0.6)
        until(self, "every claim labelled")
        t = VGroup(pill(3.4, -1.6, 1.9, fill=CARD).set_stroke(INK, 4), T("sourced", 34).move_to([3.4, -1.6, 0]))
        self.play(FadeIn(t, shift=UP * 0.2), run_time=0.4)
        self.play(Create(check(4.9, 1.7, 0.3, TERRA, 9)), run_time=0.4)
        finish(self)


class B08_Repo(Scene):
    def construct(self):
        parcel = make_original("release-parcel", height=3.0, x=-3.2, y=-0.3)
        self.add(sub(self))
        self.play(FadeIn(parcel, shift=DOWN * 0.8), run_time=0.7)
        self.play(FadeIn(label("GitHub repo", -3.2, -2.25)), run_time=0.3)
        self.play(parcel.parts["lid"].animate.shift(parcel.action_vectors["lid"]), run_time=0.5)
        until(self, "with the app")
        win = VGroup(Rectangle(width=2.6, height=1.8, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5),
                     Rectangle(width=2.6, height=0.32, fill_color=BAR3, fill_opacity=1, stroke_color=INK, stroke_width=5).shift(UP * 0.74),
                     *[Dot([-1.1 + i * 0.22, 0.74, 0], radius=0.05, color=INK) for i in range(3)],
                     Rectangle(width=1.6, height=0.18, fill_color=BAR2, fill_opacity=1, stroke_width=0).shift(UP * 0.2),
                     Rectangle(width=1.0, height=0.18, fill_color=BAR2, fill_opacity=1, stroke_width=0).shift(DOWN * 0.2 + LEFT * 0.3)
                     ).move_to([1.0, 1.5, 0])
        self.play(FadeIn(win, shift=UP * 0.5), run_time=0.5)
        until(self, "a set of made-up test ideas")
        cards = Group(*[paper(3.6 + i * 0.5, 1.6 - i * 0.15, w=1.1, h=1.4, tilt=0.18 - i * 0.18) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.4) for c in cards], lag_ratio=0.3), run_time=0.7)
        until(self, "a score sheet")
        grid = VGroup(*[Rectangle(width=0.55, height=0.32, fill_color=(CARD if (r + c) % 3 else BAR3), fill_opacity=1,
                                  stroke_color=INK, stroke_width=3).move_to([1.9 + c * 0.55, -1.0 - r * 0.32, 0])
                        for r in range(3) for c in range(4)])
        self.play(FadeIn(grid, shift=UP * 0.3), run_time=0.5)
        finish(self)


class B09_FirstMinute(Scene):
    def construct(self):
        desk = make_original("review-desk", height=1.8, x=0, y=-1.55)
        self.add(desk, sub(self))
        xs, names = [-4.2, 0.0, 4.2], ["README", "brief", "scores"]
        pages = [sheet(x, 1.9, w=2.0, h=2.3, lines=3, gap=0.4)[0] for x in xs]
        cur = cursor(-6.0, 3.3)
        for i, (x, n, ph) in enumerate(zip(xs, names, ["you'd open it", "one sample brief", "how often the checker"])):
            until(self, ph)
            self.play(FadeIn(pages[i], shift=DOWN * 0.5), FadeIn(label(n, x, 0.3, 36)), run_time=0.5)
            if i == 0:
                self.add(cur)
            self.play(cur.animate.move_to([x + 0.6, 1.7, 0]), run_time=0.4)
        finish(self)


class B10_Contract(Scene):
    def construct(self):
        stack = make_original("skill-stack", height=2.0, x=-4.8, y=0.6)
        gate = make_original("permission-gate", height=3.0, x=2.6, y=-0.4)
        self.add(gate, sub(self))
        self.play(FadeIn(stack, shift=DOWN * 0.3), run_time=0.5)
        self.play(FadeIn(label("instructions", -4.8, -0.9)), run_time=0.3)
        outline = DashedVMobject(Square(side_length=1.1, color=INK, stroke_width=5), num_dashes=16).move_to([-0.8, -1.35, 0])
        self.play(Create(outline), FadeIn(label("format", -0.8, -2.25)), run_time=0.5)
        until(self, "check its answers")
        parcel = small_box(Iso(-3.6, -2.4, 0.7), 0, 0, 1.0)
        self.play(FadeIn(parcel, shift=RIGHT * 0.3), run_time=0.4)
        self.play(parcel.animate.move_to(outline.get_center()), run_time=0.7)
        until(self, "measure how well")
        self.play(outline.animate.set_color(TERRA), run_time=0.3)
        self.play(gate.parts["barrier"].animate.shift(gate.action_vectors["barrier"]), run_time=0.6)
        self.play(parcel.animate.move_to([3.4, -1.2, 0]), run_time=0.7)
        finish(self)


class B11_FirstRun(Scene):
    def construct(self):
        belt = make_original("conveyor", height=2.6, x=-2.6, y=-0.3)
        self.add(belt, sub(self))
        self.play(FadeIn(label("first run", -2.6, -2.25)), run_time=0.4)
        until(self, "one agent")
        self.play(belt.parts["parcel"].animate.shift(belt.action_vectors["parcel"]), run_time=0.9)
        until(self, "saves a log")
        log, _ = sheet(3.6, 0.4, w=2.4, h=2.8, lines=4, gap=0.42)
        self.play(FadeIn(log, shift=DOWN * 0.6), run_time=0.5)
        until(self, "checks out")
        self.play(Create(check(3.6, -0.5, 0.35, TERRA, 10)), run_time=0.5)
        finish(self)


class B12_NoVerdict(Scene):
    def construct(self):
        gate = make_original("permission-gate", height=3.2, x=1.6, y=-0.4)
        gate.parts["barrier"].shift(gate.action_vectors["barrier"])
        self.add(sub(self))
        self.play(FadeIn(gate), run_time=0.4)
        card = Group(paper(0, 0, w=2.6, h=1.3), T("go / no-go", 44).move_to([0, 0, 0])).move_to([-5.0, 0.4, 0])
        self.play(FadeIn(card, shift=RIGHT * 0.4), run_time=0.4)
        self.play(card.animate.move_to([-1.6, 0.4, 0]), run_time=0.8)
        until(self, "or say go or no-go")
        self.play(gate.parts["barrier"].animate.shift(-gate.action_vectors["barrier"]), run_time=0.5)
        until(self, "people decide")
        self.play(FadeIn(label("people decide", 1.6, -2.35)), run_time=0.3)
        self.play(card.animate.shift(LEFT * 2.2).set_opacity(0.25), run_time=0.6)
        finish(self)


class B13_RubberStamp(Scene):
    def construct(self):
        st = make_original("approval-stamp", height=3.6, x=-0.6, y=-0.3)
        self.add(st, sub(self))
        crack = VMobject(stroke_color=TERRA, stroke_width=7).set_points_as_corners(
            [[-1.9, -0.75, 0], [-1.45, -1.0, 0], [-1.65, -1.2, 0], [-1.1, -1.5, 0]])
        self.play(Create(crack), run_time=0.5)
        self.play(FadeIn(label("rubber stamp", 3.9, 1.2)), run_time=0.3)
        until(self, "agrees with everything")
        self.play(st.parts["stamp"].animate.shift(st.action_vectors["stamp"]), run_time=0.4)
        self.play(st.parts["stamp"].animate.shift(-st.action_vectors["stamp"]), run_time=0.4)
        self.play(Create(check(0.9, -1.2, 0.4, INK, 11)), run_time=0.3)
        until(self, "grading its own team")
        self.play(Indicate(crack, color=TERRA, scale_factor=1.15), run_time=0.7)
        finish(self)


class B14_CatchRate(Scene):
    def construct(self):
        bench = make_original("experiment-bench", height=3.0, x=-2.8, y=-0.4)
        self.add(bench, sub(self))
        self.play(FadeIn(label("catch rate", 3.4, 2.6)), run_time=0.4)
        until(self, "count how many")
        self.play(bench.parts["sample"].animate.shift(bench.action_vectors["sample"]), run_time=0.6)
        marks = VGroup(*[Line([2.0 + i * 0.4, 1.7, 0], [2.0 + i * 0.4, 0.9, 0], color=INK, stroke_width=9) for i in range(4)])
        marks.add(Line([1.85, 1.0, 0], [3.35, 1.6, 0], color=INK, stroke_width=9))
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.3), run_time=1.0)
        until(self, "into plain code")
        code = Iso(3.0, -2.0, 0.8).mcp(0, 0, 0)
        self.play(FadeIn(code, shift=LEFT * 0.6), FadeIn(T("{ }", 44).move_to([4.6, -2.3, 0])), run_time=0.5)
        finish(self)


class B15_Pivot(Scene):
    def construct(self):
        self.add(sub(self))
        crate = make_original("context-crate", height=2.6, x=-3.6, y=0.0)
        crack = VMobject(stroke_color=TERRA, stroke_width=8).set_points_as_corners(
            [[-4.35, 0.05, 0], [-4.0, -0.25, 0], [-4.2, -0.5, 0], [-3.8, -0.85, 0]])
        self.play(FadeIn(crate), Create(crack), FadeIn(label("first pitch", -3.6, -2.0)), run_time=0.6)
        until(self, "too close to an AI wrapper")
        self.play(VGroup(crate, crack).animate.scale(0.6).set_opacity(0.35), run_time=0.6)
        until(self, "I wanted something")
        card = feature_card(3.4, 0.4, w=2.6, h=1.8)
        arrow = Arrow([-1.6, 0.2, 0], [1.6, 0.3, 0], color=INK, stroke_width=6, buff=0.1)
        self.play(Create(arrow), run_time=0.4)
        self.play(FadeIn(card, scale=0.8), FadeIn(label("for PMs", 3.4, -1.2)), run_time=0.6)
        finish(self)


class B16_Shelves(Scene):
    def construct(self):
        self.add(sub(self))
        have = make_original("version-shelves", height=3.4, x=-3.3, y=0.35)
        self.play(FadeIn(have, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(label("have", -3.3, -2.2)), run_time=0.3)
        until(self, "Building and testing")
        slots = VGroup(*[DashedVMobject(Rectangle(width=2.6, height=0.9, color=INK, stroke_width=5), num_dashes=24)
                         .move_to([3.3, 1.3 - i * 1.25, 0]) for i in range(3)])
        self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.35), run_time=1.0)
        self.play(FadeIn(label("new", 3.3, -2.2)), run_time=0.3)
        finish(self)


class B17_Status(Scene):
    def construct(self):
        self.add(sub(self))
        iso = Iso(-3.6, -1.3, 0.9)
        back, front = iso.open_box(0, 0, 0, 2.4, 2.4, 0.7)
        items = VGroup(iso.page(0.3, 0.3, 0.2, 0.9, 1.0), iso.page(1.2, 1.1, 0.2, 0.9, 1.0),
                       small_box(Iso(-3.6 + 0.6, -1.3 + 1.3, 0.9), 0, 0, 0.6))
        self.play(FadeIn(back), FadeIn(front), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(i, shift=DOWN * 0.3) for i in items], lag_ratio=0.3), run_time=0.7)
        self.play(FadeIn(label("exists", -3.6, -2.3)), run_time=0.3)
        until(self, "Everything else")
        slots = VGroup(*[DashedVMobject(RoundedRectangle(width=1.4, height=1.1, corner_radius=0.1, color=INK, stroke_width=5),
                                        num_dashes=20).move_to([0.2 + (i % 4) * 1.6, 1.0 - (i // 4) * 1.5, 0]) for i in range(8)])
        self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.15), run_time=1.2)
        self.play(FadeIn(label("will build", 2.6, -1.8)), run_time=0.3)
        finish(self)


class BOUT_Title(Scene):
    """Aditya's own outro (replaces the toolkit's ClaudeTitleOutro, which hard-codes the instructor's handle)."""
    def construct(self):
        card = feature_card(0, 1.6, w=2.2, h=1.5)
        title = T("ProductLens AI", 96, bold=True).move_to([0, -0.3, 0])
        name = T("Aditya Hasija", 56).move_to([0, -1.5, 0])
        self.add(card, title, name)
        self.play(Create(Line([-2.2, -0.95, 0], [2.2, -0.95, 0], color=TERRA, stroke_width=6)), run_time=0.5)
        finish(self)
