"""
scenes_film.py: the CueGate pitch film's own Manim code. Deepak Kumaran T S, INFO 7375, 2026-10-14.

Written for this film only; it contains no toolkit code. It is not runnable by itself:
build_scenes.py puts the Brutalist show-tell kit's primitives and pacing helpers in front of it
(from the pinned brutalist.art checkout, at build time) and writes scenes.py, the single file
that the toolkit's runner (art run / run.sh) and Gate A need. Names used here and defined by the
kit: T, Iso, paper, check, cursor, pill, ease_in, until, finish, _elapsed, _TARGET, _SHEET, and the
palette constants (STAGE, INK, TERRA, DIM, GHOST, CARD, BOX_*, DARK_*, PAGE_*, BAR1-3, C30).
No person is drawn anywhere in this film.
"""

try:
    _SHEET_BEAT = {b["beat_id"]: b for b in _SHEET["beats"]}
except Exception:
    _SHEET_BEAT = {}


# ═════════════════════════════ CueGate pitch film: helpers ═════════════════════════════
# Everything below is written for this film. No person is drawn anywhere (no portraits, no person icons).
MID_MARGIN = 0.25        # keep every animation this far off the clip midpoint (GATE T and Gate V sample there)


def gp(self, *anims, rt=0.5):
    """play(), but never across the clip midpoint: if the animation would overlap the guard window, wait it out."""
    bid = type(self).__name__.split("_")[0]
    target = _TARGET.get(bid, 0)
    now = _elapsed(self)
    if target:
        lo, hi = target / 2 - MID_MARGIN, target / 2 + MID_MARGIN
        if now < hi and now + rt > lo:
            self.wait(hi - now)
    self.play(*anims, run_time=rt)


def say(self, phrase):
    """Wait for the spoken phrase (until), staying clear of the midpoint guard."""
    until(self, phrase)


def L(s, x, y, size=36, color=INK, bold=False):
    return T(s, size, color, bold).move_to([x, y, 0])


def block(cx, cy, w, h, d=0.32, top=BOX_TOP, front=BOX_L, side=BOX_R, sw=4):
    """A 2.5-D block: front face centred on (cx, cy), with a top and a right side receding up-right."""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    dx, dy = d * C30, d * 0.5
    f = Polygon([x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0], fill_color=front, fill_opacity=1, stroke_color=INK, stroke_width=sw)
    t = Polygon([x0, y1, 0], [x1, y1, 0], [x1 + dx, y1 + dy, 0], [x0 + dx, y1 + dy, 0], fill_color=top, fill_opacity=1, stroke_color=INK, stroke_width=sw)
    s = Polygon([x1, y0, 0], [x1 + dx, y0 + dy, 0], [x1 + dx, y1 + dy, 0], [x1, y1, 0], fill_color=side, fill_opacity=1, stroke_color=INK, stroke_width=sw)
    return VGroup(f, t, s)


def dark_block(cx, cy, w, h, d=0.32):
    return block(cx, cy, w, h, d, DARK_TOP, DARK_L, DARK_R)


def cue_page(x, y, w=1.7, h=2.2, rows=4):
    """A subtitle file: a white sheet with grey cue rows (a short timecode bar and a longer text bar per cue)."""
    pg = paper(x, y, w, h)
    bars = VGroup()
    top = y + h / 2 - 0.42
    step = (h - 0.7) / max(1, rows - 1) if rows > 1 else 0
    for i in range(rows):
        yy = top - i * step
        bars.add(Rectangle(width=w * 0.22, height=0.14, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x - w * 0.29, yy, 0]))
        bars.add(Rectangle(width=w * 0.5, height=0.14, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x + w * 0.1, yy, 0]))
    return VGroup(pg, bars)


def film_frame(x, y, w=2.2, h=1.4):
    """A film frame: a DIM picture area in an ink frame, with a pale subtitle bar (grey outline) near its foot."""
    pic = Rectangle(width=w, height=h, fill_color=DIM, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    bar = Rectangle(width=w * 0.62, height=h * 0.16, fill_color=CARD, fill_opacity=1, stroke_color=BAR1, stroke_width=2).move_to([x, y - h * 0.28, 0])
    return VGroup(pic, bar)


def gate(cx, cy, s=1.0):
    """The CueGate gate: two kraft posts and a lintel with one terracotta light on its top face."""
    pw, ph, span = 0.42 * s, 2.5 * s, 1.9 * s
    left = block(cx - span / 2, cy, pw, ph, 0.28 * s)
    right = block(cx + span / 2, cy, pw, ph, 0.28 * s)
    lintel = block(cx + 0.0, cy + ph / 2 + 0.18 * s, span + pw, 0.36 * s, 0.28 * s)
    light = Dot([cx + 0.12 * s, cy + ph / 2 + 0.43 * s, 0], radius=0.07 * s, color=TERRA)
    g = VGroup(left, right, lintel, light)
    g.light = light
    return g


def bubble(x, y, w=1.3, h=0.8):
    body = RoundedRectangle(width=w, height=h, corner_radius=0.2, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    tail = Polygon([x - w * 0.2, y - h / 2, 0], [x - w * 0.05, y - h / 2, 0], [x - w * 0.3, y - h / 2 - 0.25, 0],
                   fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(tail, body)


def bars3(x, y, hs=(0.5, 0.8, 0.35), w=0.28, gap=0.12):
    """Three grey chart blocks with gaps (BAR1/BAR2/BAR3), bottoms aligned at y."""
    cols = (BAR1, BAR2, BAR3)
    g = VGroup()
    for i, (h, c) in enumerate(zip(hs, cols)):
        g.add(Rectangle(width=w, height=h, fill_color=c, fill_opacity=1, stroke_width=0).move_to([x + i * (w + gap), y + h / 2, 0]))
    return g


def ghost_rect(x, y, w, h):
    return Rectangle(width=w, height=h, fill_opacity=0, stroke_color=DIM, stroke_width=3).move_to([x, y, 0])


def floor_line():
    return Line([-6.0, -3.05, 0], [6.0, -3.05, 0], color=GHOST, stroke_width=4)


# ═════════════════════════════ scenes ═════════════════════════════

class B01_Count(Scene):
    """The real reply (quotes as delimiters, 37 characters) against a 38-character budget bar: it fits."""
    def construct(self):
        cnt = (_SHEET_BEAT.get("B01", {}).get("shot", {}) or {}).get("count") or {"n": 37, "budget": 38, "text": "Not in there tonight, not after that."}
        n, budget, text = int(cnt["n"]), int(cnt["budget"]), cnt["text"]
        unit = 9.0 / budget
        x0 = -4.5
        reply = L(text, 0, 2.2, 44)
        frame = Rectangle(width=unit * budget, height=0.56, fill_color=BAR3, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x0 + unit * budget / 2, 0.2, 0])
        lab = L(f"budget {budget}", 3.3, -0.65, 34)
        self.add(floor_line())
        gp(self, FadeIn(reply, shift=DOWN * 0.15), rt=0.5)
        gp(self, Create(frame), FadeIn(lab), rt=0.6)
        say(self, "Then I counted")
        fill = Rectangle(width=unit * n, height=0.4, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x0 + unit * n / 2, 0.2, 0])
        gp(self, GrowFromEdge(fill, LEFT), rt=1.2)
        num = L(str(n), x0 + unit * n / 2, -1.3, 72, bold=True)
        gp(self, FadeIn(num), rt=0.4)
        say(self, "It fit")
        mark = check(5.25, 0.25, 0.26) if n <= budget else Cross(stroke_color=INK, stroke_width=7).scale(0.25).move_to([5.25, 0.2, 0])
        gp(self, Create(mark), rt=0.4)
        say(self, "The hard part")
        q = L("every time?", -2.6, -2.35, 36)
        gp(self, FadeIn(q), rt=0.4)
        finish(self)


class B02_Gate(Scene):
    """A subtitle file goes through the CueGate gate; one line it cannot prove peels off to the escalated door."""
    def construct(self):
        floor = floor_line()
        page = cue_page(-4.6, 0.4)
        lp = L("subtitles", -4.6, -1.35, 36)
        self.add(floor)
        gp(self, FadeIn(page, shift=RIGHT * 0.3), FadeIn(lp), rt=0.6)
        say(self, "find every line")
        g = gate(0.0, 0.1, 1.0)
        lg = L("CueGate", 0.0, 2.75, 40, bold=True)
        gp(self, FadeIn(g, shift=UP * 0.2), FadeIn(lg), rt=0.6)
        door = block(0.2, -2.45, 1.6, 0.55)
        ld = L("escalated", 2.75, -2.45, 36)
        gp(self, FadeIn(door, shift=UP * 0.15), FadeIn(ld), rt=0.5)
        say(self, "refuse to ship")
        stray = Rectangle(width=0.85, height=0.14, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-4.4, -0.2, 0])
        gp(self, FadeIn(stray), rt=0.2)
        gp(self, stray.animate.move_to([0.2, -2.05, 0]), rt=0.8)
        gp(self, FadeOut(lp), page.animate.move_to([4.4, 0.4, 0]), rt=1.1)
        ok = check(5.6, 1.9, 0.24)
        gp(self, Create(ok), rt=0.4)
        say(self, "It will exist as")
        small = VGroup(block(-4.9, -2.45, 0.7, 0.45), dark_block(-3.9, -2.45, 0.7, 0.45), block(-2.9, -2.45, 0.7, 0.45))
        gp(self, LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in small], lag_ratio=0.3), rt=0.9)
        finish(self)


class B03_Rules(Scene):
    """A film frame with a subtitle bar running past its edge; three rule markers; a flag rises on the bar."""
    def construct(self):
        self.add(floor_line())
        pic = Rectangle(width=5.4, height=3.2, fill_color=DIM, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.6, 0.5, 0])
        gp(self, FadeIn(pic), rt=0.5)
        bar = Rectangle(width=5.6, height=0.46, fill_color=CARD, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([-0.3, -0.55, 0])
        gp(self, GrowFromEdge(bar, LEFT), rt=0.8)
        rows = [("reading speed", "how fast"), ("gap", "the gap"), ("shot change", "at a cut")]
        for i, (word, phrase) in enumerate(rows):
            say(self, phrase)
            y = 1.6 - i * 1.0
            d = Dot([3.25, y, 0], radius=0.11, color=TERRA)
            lab = T(word, 36).move_to([3.6, y, 0], aligned_edge=LEFT)
            gp(self, GrowFromCenter(d), FadeIn(lab), rt=0.4)
        say(self, "Break them")
        pole = Line([2.25, -0.3, 0], [2.25, 0.9, 0], color=INK, stroke_width=6)
        flag = Polygon([2.25, 0.9, 0], [2.25, 0.45, 0], [2.95, 0.68, 0], fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4)
        gp(self, Create(pole), rt=0.3)
        gp(self, FadeIn(flag, shift=UP * 0.1), rt=0.3)
        finish(self)


class B04_Alternatives(Scene):
    """Left: one line, a small button, a cursor clicks it. Right: a whole file rides through the gate; drift gets measured."""
    def construct(self):
        self.add(floor_line())
        line = Rectangle(width=3.6, height=0.5, fill_color=CARD, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([-3.6, 1.2, 0])
        btn = block(-3.6, 0.15, 1.1, 0.42)
        l1 = L("one line", -3.6, -1.0, 36)
        gp(self, FadeIn(line), FadeIn(btn), FadeIn(l1), rt=0.5)
        say(self, "shortens one line")
        cur = cursor(-1.6, -0.6)
        gp(self, FadeIn(cur), rt=0.3)
        gp(self, cur.animate.move_to([-3.4, 0.0, 0]), rt=0.7)
        gp(self, btn.animate.shift(DOWN * 0.06), rt=0.15)
        g = gate(3.4, 0.2, 0.85)
        l2 = L("whole file", 3.4, -1.55, 36)
        gp(self, FadeIn(g), FadeIn(l2), rt=0.5)
        say(self, "CueGate will be a gate")
        page = cue_page(1.3, 0.4, 1.2, 1.6, 3)
        gp(self, FadeIn(page, shift=RIGHT * 0.2), rt=0.3)
        gp(self, page.animate.move_to([5.4, 0.4, 0]), rt=1.2)
        say(self, "changed meaning")
        ch = bars3(4.6, -2.95, (0.45, 0.7, 0.3))
        l3 = L("drift measured", 2.4, -2.55, 34)
        gp(self, FadeIn(ch, shift=UP * 0.1), FadeIn(l3), rt=0.5)
        finish(self)


class B05_Report(Scene):
    """CONSTRUCTED report mock-up: a subtitle page and a film frame drop in; rows land: broken, fixed, refused."""
    def construct(self):
        tag = L("CONSTRUCTED", -3.9, 2.95, 36, bold=True)
        self.add(floor_line(), tag)
        tray = block(-4.6, -1.5, 2.6, 0.5)
        gp(self, FadeIn(tray), rt=0.4)
        say(self, "they'll drop in")
        pg = cue_page(-5.2, 0.3, 1.1, 1.5, 3)
        fr = film_frame(-3.8, 0.0, 1.5, 1.0)
        gp(self, FadeIn(pg, shift=DOWN * 0.3), FadeIn(fr, shift=DOWN * 0.3), rt=0.5)
        say(self, "get back a table")
        card = Rectangle(width=4.4, height=4.0, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0.8, 0.2, 0])
        gp(self, FadeIn(card), rt=0.4)
        rows = [("broken", "every broken rule"), ("fixed", "every line fixed"), ("refused", "will refuse to touch")]
        for i, (word, phrase) in enumerate(rows):
            say(self, phrase)
            y = 1.4 - i * 1.2
            if i == 0:
                mark = Dot([-0.9, y, 0], radius=0.12, color=TERRA)
            elif i == 1:
                mark = check(-0.95, y + 0.05, 0.2)
            else:
                mark = Rectangle(width=0.36, height=0.36, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-0.9, y, 0])
            bar = Rectangle(width=2.6, height=0.3, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([1.1 + 0.2, y, 0])
            lab = T(word, 36).move_to([3.4, y, 0], aligned_edge=LEFT)
            gp(self, FadeIn(mark), GrowFromEdge(bar, LEFT), FadeIn(lab), rt=0.45)
        finish(self)


class B06_Ladder(Scene):
    """A three-rung ladder: timing, line breaks, shorten. A token climbs; candidates appear; the counter decides."""
    def construct(self):
        self.add(floor_line())
        rail_l = Line([-2.0, -2.9, 0], [-2.0, 2.3, 0], color=INK, stroke_width=6)
        rail_r = Line([0.0, -2.9, 0], [0.0, 2.3, 0], color=INK, stroke_width=6)
        ys = (-1.9, -0.3, 1.3)
        rungs = VGroup(*[block(-1.0, y, 2.0, 0.3, 0.22) for y in ys])
        labs = [L("timing", -3.6, ys[0], 36), L("line breaks", -3.9, ys[1], 36), L("shorten", -3.6, ys[2], 36)]
        gp(self, Create(rail_l), Create(rail_r), rt=0.5)
        gp(self, LaggedStart(*[FadeIn(r) for r in rungs], lag_ratio=0.25), rt=0.6)
        say(self, "First, timing")
        tok = Dot([-1.0, ys[0] + 0.42, 0], radius=0.16, color=TERRA)
        gp(self, GrowFromCenter(tok), FadeIn(labs[0]), rt=0.4)
        gp(self, FadeIn(labs[1]), FadeIn(labs[2]), rt=0.4)
        say(self, "Only if that fails")
        gp(self, tok.animate.move_to([-1.0, ys[1] + 0.42, 0]), rt=0.5)
        gp(self, tok.animate.move_to([-1.0, ys[2] + 0.42, 0]), rt=0.5)
        cands = VGroup(*[cue_page(1.6 + i * 1.25, 1.4, 1.0, 1.3, 2) for i in range(3)])
        gp(self, LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cands], lag_ratio=0.3), rt=0.8)
        say(self, "Then a plain counter")
        ctr = dark_block(3.0, -1.4, 1.6, 1.1)
        gp(self, FadeIn(ctr, shift=UP * 0.15), rt=0.4)
        say(self, "The counter will decide")
        ok = check(4.75, -1.3, 0.26)
        gp(self, Create(ok), rt=0.4)
        finish(self)


class B07A_Evidence(Scene):
    """The evidence: the real reply (B00) beside its source line. It fit and kept both negatives, yet the hedge became a flat refusal."""
    def construct(self):
        self.add(floor_line())
        h1, h2 = L("asked", -3.3, 2.75, 36, bold=True), L("got back", 3.3, 2.75, 36, bold=True)
        src = VGroup(T("I really don't think we", 34), T("should go in there tonight,", 34), T("not after what happened.", 34)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-3.3, 1.0, 0])
        rep = VGroup(T("Not in there tonight,", 34), T("not after that.", 34)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.3, 1.2, 0])
        div = Line([0.0, -0.6, 0], [0.0, 2.4, 0], color=GHOST, stroke_width=4)
        gp(self, FadeIn(h1), FadeIn(h2), FadeIn(src), FadeIn(rep), Create(div), rt=0.6)
        say(self, "It fit the budget")
        okb = check(4.6, -0.6, 0.22)
        gp(self, Create(okb), rt=0.3)
        say(self, "became")
        hedge = Rectangle(width=5.4, height=0.16, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-3.3, -0.85, 0])
        flat = Rectangle(width=3.6, height=0.16, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([3.0, -1.25, 0])
        gp(self, GrowFromEdge(hedge, LEFT), GrowFromEdge(flat, LEFT), rt=0.5)
        l1, l2 = L("hedged opinion", -3.3, -1.55, 34), L("flat refusal", 3.0, -1.95, 34)
        gp(self, FadeIn(l1), FadeIn(l2), rt=0.3)
        say(self, "exactly what a character count can't see")
        ctr = dark_block(0.0, -2.35, 1.3, 0.8)
        gp(self, FadeIn(ctr, shift=UP * 0.1), rt=0.4)
        finish(self)

class B07B_Plan(Scene):
    """The plan: three stations. Invariants (numbers, names, "not"), a weaker meaning check, 100 hand-labelled lines."""
    def construct(self):
        self.add(floor_line())
        st1 = block(-4.2, -0.1, 2.2, 1.3)
        tags = VGroup(*[block(-5.0 + 0.8 * k, 1.05, 0.5, 0.32, 0.18) for k in range(3)])
        l1 = L("invariants", -4.2, -1.45, 36)
        gp(self, FadeIn(st1, shift=UP * 0.15), FadeIn(l1), rt=0.5)
        gp(self, LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in tags], lag_ratio=0.3), rt=0.6)
        tok = Dot([-4.2, 1.75, 0], radius=0.14, color=TERRA)
        gp(self, GrowFromCenter(tok), rt=0.3)
        say(self, "then run a second")
        st2 = block(0.0, -0.25, 1.6, 0.95)
        l2 = L("meaning check", 0.0, -1.45, 36)
        gp(self, FadeIn(st2, shift=UP * 0.15), FadeIn(l2), rt=0.5)
        gp(self, tok.animate.move_to([0.0, 0.55, 0]), rt=0.6)
        say(self, "I'll measure")
        stack = VGroup(*[cue_page(3.7 + 0.12 * k, -0.2 + 0.12 * k, 1.5, 1.9, 3) for k in range(5)])
        gp(self, LaggedStart(*[FadeIn(pg, shift=DOWN * 0.15) for pg in stack], lag_ratio=0.2), rt=0.9)
        num = L("100", 4.3, 2.3, 64, bold=True)
        l3 = L("hand-labelled", 4.2, -1.75, 34)
        gp(self, FadeIn(num), FadeIn(l3), rt=0.4)
        say(self, "publish the number")
        ch = bars3(0.9, -3.0, (0.35, 0.6, 0.45))
        gp(self, FadeIn(ch, shift=UP * 0.1), rt=0.5)
        finish(self)

class B08_Tiles(Scene):
    """Five tiles land as each skill is named; evidence pages slide in under them."""
    def construct(self):
        self.add(floor_line())
        xs = (-4.8, -2.4, 0.0, 2.4, 4.8)
        words = ("contract", "verifier", "loop", "sources", "evaluation")
        phrases = ("prompt contract", "build a verifier", "run an agent loop", "tie every flag", "evaluate it against")
        icons = [
            lambda x: cue_page(x, 2.05, 0.75, 0.95, 2),
            lambda x: check(x, 2.05, 0.28),
            lambda x: VGroup(Arc(radius=0.38, start_angle=0.3, angle=5.2, color=INK, stroke_width=6).move_to([x, 2.05, 0]),
                             Polygon([x + 0.38, 2.25, 0], [x + 0.2, 2.0, 0], [x + 0.52, 1.98, 0], fill_color=INK, fill_opacity=1, stroke_width=0)),
            lambda x: VGroup(cue_page(x, 2.05, 0.75, 0.95, 2), Dot([x + 0.2, 2.35, 0], radius=0.08, color=TERRA)),
            lambda x: bars3(x - 0.4, 1.65, (0.4, 0.7, 0.5), 0.22, 0.08),
        ]
        for i, x in enumerate(xs):
            if i:
                say(self, phrases[i])
            plinth = dark_block(x, -0.08, 1.75, 0.24, 0.2)            # a dark plinth carries the pale tile (Gate V contrast)
            tile = block(x, 0.62, 1.5, 1.16, top=BOX_L, front=BOX_R, side=BOX_IN2)
            gp(self, FadeIn(plinth), FadeIn(tile, shift=DOWN * 0.15), FadeIn(icons[i](x)), FadeIn(L(words[i], x, -0.62, 34)), rt=0.45)
        say(self, "The evidence will be")
        pages = VGroup(*[cue_page(x, -2.0, 0.8, 1.0, 2) for x in (-2.4, 0.0, 2.4)])
        gp(self, LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in pages], lag_ratio=0.3), rt=0.8)
        finish(self)


class B09_Scope(Scene):
    """Three columns: IN, OUT (translation crossed out), FIRST (a small terminal with the word check)."""
    def construct(self):
        self.add(floor_line())
        heads = [L("IN", -4.2, 2.7, 40, bold=True), L("OUT", 0.0, 2.7, 40, bold=True), L("FIRST", 4.2, 2.7, 40, bold=True)]
        divs = VGroup(Line([-2.1, -2.7, 0], [-2.1, 2.4, 0], color=GHOST, stroke_width=4), Line([2.1, -2.7, 0], [2.1, 2.4, 0], color=GHOST, stroke_width=4))
        ins = VGroup(cue_page(-4.9, 0.6, 1.1, 1.5, 3), film_frame(-3.5, 0.3, 1.4, 0.95))
        gp(self, *[FadeIn(h) for h in heads], Create(divs), FadeIn(ins), rt=0.6)
        say(self, "won't do is translate")
        b1, b2 = bubble(-0.75, 0.9, 1.1, 0.7), bubble(0.75, -0.1, 1.1, 0.7)
        gp(self, FadeIn(b1), FadeIn(b2), rt=0.4)
        x = Cross(stroke_color=INK, stroke_width=8).scale(0.95).move_to([0.0, 0.4, 0])
        gp(self, Create(x), rt=0.4)
        say(self, "The first piece")
        term = dark_block(4.1, 0.3, 2.6, 1.5, 0.3)
        word = T("check", 40, color=CARD).move_to([3.8, 0.3, 0])
        gp(self, FadeIn(term, shift=UP * 0.15), rt=0.4)
        gp(self, FadeIn(word), rt=0.3)
        say(self, "You'll know")
        ok = check(4.2, -1.6, 0.26)
        gp(self, Create(ok), rt=0.4)
        finish(self)


class B10_Filmstrip(Scene):
    """A filmstrip; fast motion across three frames is wrongly marked as a cut; a cut list sets the real marker."""
    def construct(self):
        self.add(floor_line())
        xs = [-4.8 + 1.6 * i for i in range(7)]
        frames = VGroup(*[Rectangle(width=1.3, height=1.0, fill_color=DIM, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, 0.5, 0]) for x in xs])
        gp(self, LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.12), rt=0.8)
        say(self, "Fades and fast motion")
        offs = (-0.38, 0.0, 0.38)
        movers = VGroup(*[Rectangle(width=0.34, height=0.34, fill_color=BOX_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([xs[2 + k] + offs[k], 0.5, 0]) for k in range(3)])
        lm = L("fast motion", xs[3], -0.45, 34)
        gp(self, LaggedStart(*[FadeIn(mv) for mv in movers], lag_ratio=0.3), FadeIn(lm), rt=0.6)
        say(self, "a fake cut")
        tick = Line([xs[3], 1.15, 0], [xs[3], 1.85, 0], color=INK, stroke_width=7)
        lt = L("fake cut", xs[3], 2.35, 36)
        gp(self, Create(tick), FadeIn(lt), rt=0.4)
        say(self, "I'll accept a cut list")
        cl = cue_page(-4.4, -2.0, 1.4, 1.0, 2)
        lc = L("cut list", -2.6, -2.0, 36)
        gp(self, FadeIn(cl, shift=RIGHT * 0.2), FadeIn(lc), rt=0.5)
        gp(self, FadeOut(tick), FadeOut(lt), rt=0.3)
        real = VGroup(Line([xs[5], 1.15, 0], [xs[5], 1.85, 0], color=INK, stroke_width=7), Dot([xs[5], 2.0, 0], radius=0.1, color=TERRA))
        gp(self, Create(real), rt=0.4)
        finish(self)

class B11_Split(Scene):
    """Split panel: already have (a taped box for the private co-op work, the timeline gate) and new (four items)."""
    def construct(self):
        self.add(floor_line())
        div = Line([0.0, -2.8, 0], [0.0, 2.4, 0], color=GHOST, stroke_width=5)
        h1, h2 = L("already have", -3.1, 2.8, 40, bold=True), L("new", 3.1, 2.8, 40, bold=True)
        gp(self, Create(div), FadeIn(h1), FadeIn(h2), rt=0.5)
        boxv = block(-4.6, 0.4, 1.5, 1.2)
        tapev = Polygon([-5.35, 1.0, 0], [-3.85, 1.0, 0], [-3.85 + 0.28 * C30, 1.0 + 0.14, 0], [-5.35 + 0.28 * C30, 1.0 + 0.14, 0],
                        fill_color=BAR1, fill_opacity=1, stroke_width=0)          # grey strap (a terracotta band reads as accent text in GATE T)
        seal = Dot([-4.6 + 0.14, 1.07, 0], radius=0.06, color=TERRA)                  # one spark-sized seal on the top face
        gp(self, FadeIn(boxv, shift=DOWN * 0.15), FadeIn(tapev), FadeIn(seal), rt=0.5)
        say(self, "What I can show")
        g = gate(-2.0, 0.1, 0.7)
        gp(self, FadeIn(g, shift=UP * 0.15), rt=0.5)
        say(self, "For evaluation specifically")
        future = ghost_rect(-3.3, -2.05, 1.6, 0.9)
        gp(self, Create(future), rt=0.4)
        say(self, "What's new to me")
        items = [film_frame(1.8, 1.0, 1.5, 1.0), VGroup(*[Rectangle(width=0.5, height=0.4, fill_color=DIM, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([3.5 + 0.6 * k, 1.0, 0]) for k in range(3)]),
                 cue_page(2.0, -1.2, 1.1, 1.4, 3), VGroup(bubble(3.7, -0.9, 0.9, 0.55), bubble(4.9, -1.5, 0.9, 0.55))]
        gp(self, LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in items], lag_ratio=0.35), rt=1.2)
        finish(self)


class B12_Lists(Scene):
    """EXISTS (dated): the plan and its PDF. WILL: four ghost outlines of what does not exist yet."""
    def construct(self):
        self.add(floor_line())
        h1, d1, h2 = L("EXISTS", -3.2, 2.75, 40, bold=True), L("14 Oct 2026", -3.2, 2.05, 34), L("WILL", 3.2, 2.75, 40, bold=True)
        p1, p2 = cue_page(-4.1, -0.2, 1.5, 2.0, 4), cue_page(-2.3, -0.2, 1.5, 2.0, 4)
        gp(self, FadeIn(h1), FadeIn(d1), FadeIn(p1, shift=DOWN * 0.2), FadeIn(p2, shift=DOWN * 0.2), FadeIn(h2), rt=0.6)
        say(self, "No code runs yet")
        ghosts = VGroup(ghost_rect(2.0, 0.9, 1.8, 1.2), ghost_rect(4.4, 0.9, 1.8, 1.2), ghost_rect(2.0, -1.0, 1.8, 1.2), ghost_rect(4.4, -1.0, 1.8, 1.2))
        gp(self, LaggedStart(*[Create(gr) for gr in ghosts], lag_ratio=0.25), rt=1.0)
        finish(self)


class B13_YourTurn(Scene):
    """A drawn prompt card with one subtitle line; a counter block; a check lands beside the kept "not"."""
    def construct(self):
        self.add(floor_line())
        head = L("Your turn", -2.4, 2.75, 44, bold=True)
        card = paper(-2.4, 0.1, 5.0, 3.4)
        lines = VGroup(*[Rectangle(width=w, height=0.16, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([-2.4 - (3.6 - w) / 2, 1.0 - 0.55 * i, 0])
                         for i, w in enumerate((3.6, 3.0, 3.4))])
        line = Rectangle(width=3.6, height=0.42, fill_color=CARD, fill_opacity=1, stroke_color=BAR1, stroke_width=3).move_to([-2.4, -0.9, 0])
        gp(self, FadeIn(head), FadeIn(card, shift=DOWN * 0.2), rt=0.5)
        gp(self, FadeIn(lines), FadeIn(line), rt=0.4)
        say(self, "count the characters")
        ctr = dark_block(3.2, 0.6, 1.6, 1.1)
        gp(self, FadeIn(ctr, shift=UP * 0.15), rt=0.4)
        ch = bars3(4.6, 0.05, (0.35, 0.6, 0.85))
        gp(self, FadeIn(ch, shift=UP * 0.1), rt=0.4)
        say(self, "And check")
        lab = L("not", 3.0, -1.7, 40)
        ok = check(4.1, -1.65, 0.24)
        gp(self, FadeIn(lab), Create(ok), rt=0.4)
        finish(self)
