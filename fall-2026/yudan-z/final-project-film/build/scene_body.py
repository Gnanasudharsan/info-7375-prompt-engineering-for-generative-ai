

# ═════════════════════════════ is-funded-sponsor-triage-pitch — body scenes ═════════════════════════════
# Cast kept across the film: a job-posting CARD, a conveyor BELT, open-box TRAYS, a shortlist PAPER with TAGS.

def card(x, y, w=0.62, h=0.44, blank=False):
    """A job-posting card: white slab, ink outline; a record card carries ghost lines + a terracotta dot."""
    r = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    if blank:
        return VGroup(r)
    l1 = Line([x - w * 0.32, y + h * 0.12, 0], [x + w * 0.2, y + h * 0.12, 0], color=BAR2, stroke_width=4)
    l2 = Line([x - w * 0.32, y - h * 0.14, 0], [x + w * 0.05, y - h * 0.14, 0], color=BAR2, stroke_width=4)
    d = Dot([x + w * 0.3, y - h * 0.14, 0], radius=0.05, color=TERRA)
    return VGroup(r, l1, l2, d)


def belt(x0, x1, y):
    b = RoundedRectangle(width=x1 - x0, height=0.42, corner_radius=0.21, fill_color=BAR2, fill_opacity=1,
                         stroke_color=INK, stroke_width=4).move_to([(x0 + x1) / 2, y, 0])
    n = max(3, int((x1 - x0) / 1.1))
    rollers = VGroup(*[Circle(radius=0.13, stroke_color=INK, stroke_width=4, fill_color=CARD, fill_opacity=1)
                       .move_to([x0 + 0.4 + i * (x1 - x0 - 0.8) / (n - 1), y, 0]) for i in range(n)])
    return VGroup(b, rollers)


def tray(ox, oy, s=0.55, w=1.8, h=0.7):
    iso = Iso(ox, oy, s)
    back, front = iso.open_box(0, 0, 0, w, w, h)
    return iso, back, front


def arc_to(mob, end, angle=-1.1):
    return MoveAlongPath(mob, ArcBetweenPoints(mob.get_center(), np.array(end, dtype=float), angle=angle))


def tag(x, y, filled=True):
    return RoundedRectangle(width=0.62, height=0.3, corner_radius=0.15, fill_color=BAR2 if filled else CARD,
                            fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y, 0])


def dashed_box(x, y, w, h):
    return DashedVMobject(Rectangle(width=w, height=h, stroke_color=INK, stroke_width=4), num_dashes=22).move_to([x, y, 0])


def shortlist(x=-1.6, y=-0.3):
    """Shortlist sheet with four rows; returns (paper, rows, row_y list)."""
    pg = paper(x, y, w=3.6, h=3.4)
    ys = [y + 1.1 - i * 0.72 for i in range(4)]
    rows = VGroup(*[Line([x - 1.4, yy, 0], [x + 0.9, yy, 0], color=BAR1, stroke_width=6) for yy in ys])
    return pg, rows, ys


class B01_Trays(Scene):
    def construct(self):
        bl = belt(-6.0, -0.9, 1.6)
        self.play(FadeIn(bl), run_time=0.6)
        names = ["apply", "consider", "skip"]
        trays = []
        for i, n in enumerate(names):
            iso, back, front = tray(-0.3 + i * 2.15, -1.6)
            lab = T(n, 36).next_to(front, DOWN, buff=0.22)
            trays.append((iso, back, front))
            self.play(FadeIn(back), FadeIn(front), FadeIn(lab), run_time=0.35)
        iso4, b4, f4 = tray(5.0, 1.0, s=0.5, w=1.6, h=0.6)
        until(self, "It sorts postings")
        for iso, back, front in trays:
            c = card(-5.6, 1.98)
            self.play(FadeIn(c, shift=RIGHT * 0.3), run_time=0.3)
            self.play(c.animate.move_to([-1.2, 1.98, 0]), run_time=0.55, rate_func=linear)
            self.play(arc_to(c, iso.p(0.9, 0.9, 0.35)), run_time=0.55)
            self.bring_to_front(front)
        until(self, "when there is no record")
        lab4 = T("no record", 36).next_to(f4, DOWN, buff=0.2)
        self.play(FadeIn(b4), FadeIn(f4), FadeIn(lab4), run_time=0.4)
        c = card(-5.6, 1.98, blank=True)
        self.play(FadeIn(c, shift=RIGHT * 0.3), run_time=0.3)
        self.play(c.animate.move_to([-1.2, 1.98, 0]), run_time=0.5, rate_func=linear)
        self.play(arc_to(c, iso4.p(0.8, 0.8, 0.3), angle=-0.8), run_time=0.6)
        self.bring_to_front(f4)
        until(self, "Finished")
        repo = Iso(-4.3, -2.3, 0.75)
        rb = repo.box(0, 0, 0, 1.6, 1.6, 1.0)
        tp = repo.tape(0, 0, 1.0, 1.6, 1.6)
        self.play(FadeIn(rb, shift=DOWN * 0.3), run_time=0.5)
        self.play(FadeIn(tp), run_time=0.3)
        finish(self)


class B02_Funnel(Scene):
    def construct(self):
        base = Line([-5.2, -2.4, 0], [5.2, -2.4, 0], color=INK, stroke_width=4)
        date = T("record · run 2026-10-02", 32).move_to([0, -2.95, 0])
        self.play(Create(base), FadeIn(date), run_time=0.6)
        vals = [(27874, "27,874", -3.2, BAR1), (1532, "1,532", 0.0, BAR2), (131, "131", 3.2, BAR3)]
        H = 4.6
        phrases = ["Twenty-seven", "Only one thousand", "Only one hundred"]
        for (v, s, x, col), ph in zip(vals, phrases):
            until(self, ph)
            h = max(0.05, H * v / 27874)
            bar = Rectangle(width=1.5, height=h, fill_color=col, fill_opacity=1, stroke_color=INK, stroke_width=4)
            bar.move_to([x, -2.4 + h / 2, 0])
            lab = T(s, 44).next_to(bar, UP, buff=0.2)
            self.play(GrowFromEdge(bar, DOWN), run_time=0.7)
            self.play(FadeIn(lab), run_time=0.3)
        until(self, "barely overlap")
        dot = Dot([4.25, -2.3, 0], radius=0.09, color=TERRA)
        self.play(GrowFromCenter(dot), run_time=0.4)
        finish(self)


class B03_Blanks(Scene):
    def construct(self):
        zeros = VGroup(*[card(-4.9 + i * 0.75, -1.9, w=0.6, h=0.8, blank=True) for i in range(5)])
        zl = T("0", 48).next_to(zeros, UP, buff=0.3)
        self.play(LaggedStart(*[FadeIn(z, shift=DOWN * 0.2) for z in zeros], lag_ratio=0.2), FadeIn(zl), run_time=1.0)
        until(self, "Twenty-eight")
        iso = Iso(2.2, -2.6, 0.9)
        slabs = VGroup(*[iso.box(0, 0, k * 0.13, 1.7, 1.7, 0.1, PAGE_TOP, PAGE_L, PAGE_R, sw=2) for k in range(18)])
        bl = T("blank", 40).next_to(slabs, LEFT, buff=0.35).shift(UP * 0.6)
        for k, sl in enumerate(slabs):
            self.play(FadeIn(sl, shift=DOWN * 0.15), run_time=0.12)
            if k == 3:
                self.play(FadeIn(bl), run_time=0.25)
        until(self, "It means nobody matched")
        miss = dashed_box(5.0, 1.9, 1.3, 0.9)
        link = DashedLine(iso.p(1.7, 1.7, 18 * 0.13), [4.35, 1.9, 0], color=DIM, stroke_width=4)
        self.play(Create(link), Create(miss), run_time=0.7)
        finish(self)


class B04_TwoSearches(Scene):
    def construct(self):
        cons = T("CONSTRUCTED", 32).move_to([0, 3.0, 0])
        panels = []
        for x in (-3.1, 3.1):
            body = Rectangle(width=5.2, height=4.4, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, -0.15, 0])
            bar = Rectangle(width=5.2, height=0.36, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([x, 1.89, 0])
            box = RoundedRectangle(width=3.6, height=0.5, corner_radius=0.25, fill_color=PAGE_TOP, fill_opacity=1,
                                   stroke_color=INK, stroke_width=4).move_to([x - 0.4, 1.2, 0])
            lens = VGroup(Circle(radius=0.15, stroke_color=INK, stroke_width=4).move_to([x + 1.75, 1.24, 0]),
                          Line([x + 1.86, 1.13, 0], [x + 2.0, 0.99, 0], color=INK, stroke_width=5))
            panels.append(VGroup(body, bar, box, lens))
        self.play(FadeIn(cons), FadeIn(panels[0]), FadeIn(panels[1]), run_time=0.8)
        until(self, "for Moloco")
        q1 = Line([-4.85, 1.2, 0], [-3.9, 1.2, 0], color=INK, stroke_width=6)
        self.play(Create(q1), run_time=0.4)
        until(self, "It returned")
        rows = VGroup()
        for r in range(6):
            yy = 0.45 - r * 0.42
            rows.add(VGroup(*[Rectangle(width=w, height=0.24, fill_color=BAR3 if r else BAR1, fill_opacity=1, stroke_width=0)
                              .move_to([cx, yy, 0]) for cx, w in ((-4.6, 1.5), (-3.05, 1.2), (-1.85, 0.9))]))
        self.play(LaggedStart(*[FadeIn(rw) for rw in rows], lag_ratio=0.25), run_time=1.4)
        fl = T("filings", 36).move_to([-3.1, -2.75, 0])
        self.play(FadeIn(fl), run_time=0.3)
        until(self, "Then I searched")
        q2 = Line([1.35, 1.2, 0], [2.3, 1.2, 0], color=INK, stroke_width=6)
        self.play(Create(q2), run_time=0.4)
        until(self, "No table")
        empty = dashed_box(3.1, -0.6, 4.4, 2.3)
        nl = T("nothing", 36).move_to([3.1, -2.75, 0])
        self.play(Create(empty), FadeIn(nl), run_time=0.7)
        finish(self)


class B05_Network(Scene):
    def construct(self):
        bl = belt(-6.0, -0.6, 1.4)
        rank = VGroup(*[card(1.2, 1.9 - i * 0.62, w=1.1, h=0.46) for i in range(3)])
        self.play(FadeIn(bl), FadeIn(rank), run_time=0.6)
        iso, back, front = tray(3.6, -2.3, s=0.6, w=1.9, h=0.75)
        nl = T("network", 36).next_to(front, LEFT, buff=0.3)
        c = card(-5.6, 1.78, blank=True)
        self.play(FadeIn(c, shift=RIGHT * 0.3), FadeIn(back), FadeIn(front), FadeIn(nl), run_time=0.5)
        self.play(c.animate.move_to([-1.0, 1.78, 0]), run_time=0.8, rate_func=linear)
        until(self, "keeps the company out")
        self.play(arc_to(c, iso.p(0.95, 0.95, 0.4), angle=0.9), run_time=0.8)
        self.bring_to_front(front)
        until(self, "with a question")
        qm = T("?", 60).move_to(iso.p(0.95, 0.95, 0) + np.array([0.0, 1.6, 0]))
        self.play(FadeIn(qm, shift=UP * 0.2), run_time=0.4)
        until(self, "throwing away")
        more = VGroup(*[card(-5.6 + i * 0.75, -1.4, blank=True) for i in range(5)])
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in more], lag_ratio=0.15), run_time=0.8)
        self.play(LaggedStart(*[arc_to(m, iso.p(0.5 + 0.2 * i, 0.8, 0.35), angle=0.6) for i, m in enumerate(more)], lag_ratio=0.15), run_time=1.2)
        self.bring_to_front(front)
        finish(self)


class B06_Shortlist(Scene):
    def construct(self):
        term = Rectangle(width=4.2, height=1.2, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-3.6, 2.3, 0])
        tbar = Rectangle(width=4.2, height=0.3, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([-3.6, 2.75, 0])
        pg, rows, ys = shortlist(x=0.6, y=-0.6)
        # the empty shortlist sheet is on stage from the start; the command fills it
        self.play(FadeIn(term), FadeIn(tbar), FadeIn(pg), run_time=0.6)
        until(self, "run one command")
        cmd = Line([-5.4, 2.1, 0], [-2.6, 2.1, 0], color=INK, stroke_width=6)
        self.play(Create(cmd), run_time=0.6)
        until(self, "see a shortlist")
        self.play(LaggedStart(*[Create(r) for r in rows], lag_ratio=0.2), run_time=0.8)
        until(self, "carries a tag")
        tags = VGroup(*[tag(2.0, yy, filled=(i != 2)) for i, yy in enumerate(ys)])
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT * 0.3) for t in tags], lag_ratio=0.2), run_time=0.8)
        until(self, "Record means")
        rl = T("record", 36).move_to([4.65, ys[0], 0])
        ld1 = Line([2.4, ys[0], 0], [3.7, ys[0], 0], color=INK, stroke_width=3)
        self.play(Create(ld1), FadeIn(rl), run_time=0.4)
        until(self, "Your input")
        yl = T("your-input", 36).move_to([4.95, ys[2], 0])
        ld2 = Line([2.4, ys[2], 0], [3.6, ys[2], 0], color=INK, stroke_width=3)
        self.play(Create(ld2), FadeIn(yl), run_time=0.4)
        finish(self)


class B07_Magnifier(Scene):
    def construct(self):
        pg, rows, ys = shortlist(x=-2.8, y=-0.4)
        tags = VGroup(*[tag(-1.4, yy, filled=(i != 2)) for i, yy in enumerate(ys)])
        self.add(pg, rows, tags)
        sg = T("source grounding", 36).move_to([-2.8, 2.9, 0])
        self.play(FadeIn(sg), run_time=0.4)
        lens = VGroup(Circle(radius=0.45, stroke_color=INK, stroke_width=7),
                      Line([0.32, -0.32, 0], [0.75, -0.75, 0], color=INK, stroke_width=9)).move_to([-0.8, ys[0] + 0.1, 0])
        self.play(FadeIn(lens), run_time=0.3)
        until(self, "Eleven tests")
        tests = VGroup(*[Line([2.0, 1.2 - i * 0.6, 0], [4.2, 1.2 - i * 0.6, 0], color=BAR1, stroke_width=6) for i in range(3)])
        vl = T("verification", 36).move_to([3.2, 2.0, 0])
        self.play(Create(tests), FadeIn(vl), run_time=0.6)
        until(self, "one checks those tags")
        for yy in ys[1:3]:
            self.play(lens.animate.move_to([-1.2, yy + 0.1, 0]), run_time=0.45)
        chk = check(4.7, 1.2, s=0.22)
        self.play(Create(chk), run_time=0.4)
        until(self, "a teaching assistant")
        note = paper(3.2, -1.7, w=2.6, h=1.5, tilt=-0.06)
        scr = scribbles_on(note, n=2)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.4)
        self.play(Create(scr), run_time=0.8)
        finish(self)


class B08_Shelves(Scene):
    def construct(self):
        L = Iso(-3.4, -1.4, 0.7); R = Iso(3.0, -1.4, 0.7)
        sl = L.box(-1.6, -1.6, 0, 3.2, 3.2, 0.2); sr = R.box(-1.6, -1.6, 0, 3.2, 3.2, 0.2)
        el = T("exists", 40).move_to([-3.4, -3.0, 0]); wl = T("will", 40).move_to([3.0, -3.0, 0])
        self.play(FadeIn(sl), FadeIn(sr), FadeIn(el), FadeIn(wl), run_time=0.6)
        items = [L.page(-1.2, -0.9, 0.2, w=1.0, d=1.2), L.box(0.1, -1.1, 0.2, 0.9, 0.9, 0.8),
                 VGroup(*[L.box(-0.6, 0.4, 0.2 + k * 0.14, 1.0, 1.0, 0.1, PAGE_TOP, PAGE_L, PAGE_R, sw=2) for k in range(4)])]
        for ph, it in zip(["a recipe", "a Python prototype", "eleven tests"], items):
            until(self, ph)
            self.play(FadeIn(it, shift=DOWN * 0.4), run_time=0.4, rate_func=ease_in)
        spots = [(2.2, -0.8), (3.0, -0.8), (3.8, -0.8), (2.6, 0.0), (3.4, 0.0)]
        phs = ["the corrected status", "a written reason", "a sensitivity check", "a test set", "a failure analysis"]
        for (x, y), ph in zip(spots, phs):
            until(self, ph)
            self.play(Create(dashed_box(x, y, 0.6, 0.6)), run_time=0.35)
        finish(self)


class B09_Gate(Scene):
    def construct(self):
        g = Iso(0.0, -1.6, 0.8)
        p1 = g.box(-0.3, -1.6, 0, 0.4, 0.4, 2.2); p2 = g.box(-0.3, 1.2, 0, 0.4, 0.4, 2.2)
        top = Line(g.p(-0.1, -1.4, 1.6), g.p(-0.1, 1.4, 1.6), color=INK, stroke_width=8)
        self.play(FadeIn(p1), FadeIn(p2), Create(top), run_time=0.6)
        rec = card(-5.2, -0.2, w=0.9, h=0.62)
        self.play(FadeIn(rec, shift=RIGHT * 0.3), run_time=0.3)
        self.play(rec.animate.move_to([4.6, -0.2, 0]), run_time=1.6, rate_func=smooth)
        until(self, "except the five")
        blank = card(-5.2, -0.2, w=0.9, h=0.62, blank=True)
        self.play(FadeIn(blank, shift=RIGHT * 0.3), run_time=0.3)
        self.play(blank.animate.move_to([-1.3, -0.2, 0]), run_time=0.8)
        stop = Line(g.p(-0.1, -1.4, 0.7), g.p(-0.1, 1.4, 0.7), color=INK, stroke_width=8)
        self.play(Create(stop), run_time=0.3)
        self.play(blank.animate.move_to([-4.6, -0.2, 0]), run_time=0.7)
        until(self, "First I will")
        lst = VGroup(*[Line([2.0, 2.6 - i * 0.6, 0], [4.6, 2.6 - i * 0.6, 0], color=BAR1, stroke_width=6) for i in range(2)])
        fl = T("first", 36).move_to([0.75, 2.3, 0])
        self.play(Create(lst), FadeIn(fl), run_time=0.5)
        flags = VGroup(*[VGroup(Line([1.6, y - 0.25, 0], [1.6, y + 0.25, 0], color=INK, stroke_width=4),
                                Polygon([1.6, y + 0.25, 0], [1.6, y + 0.02, 0], [1.95, y + 0.135, 0], fill_color=INK, fill_opacity=1, stroke_width=0))
                         for y in (2.6, 2.0)])
        self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.3) for f in flags], lag_ratio=0.3), run_time=0.6)
        until(self, "You will know it ran")
        cks = VGroup(*[check(4.95, y, s=0.18) for y in (2.6, 2.0)])
        self.play(LaggedStart(*[Create(c) for c in cks], lag_ratio=0.3), run_time=0.6)
        finish(self)


class B10_Balance(Scene):
    def construct(self):
        piv = np.array([0.0, 1.2, 0])
        post = Polygon(piv, piv + np.array([-0.5, -3.2, 0]), piv + np.array([0.5, -3.2, 0]),
                       fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4)
        foot = Line([-1.4, -2.0, 0], [1.4, -2.0, 0], color=INK, stroke_width=6)
        beam = Line(piv + np.array([-3.6, 0, 0]), piv + np.array([3.6, 0, 0]), color=INK, stroke_width=8)

        def pan(x):
            return VGroup(Line([x, 1.2, 0], [x, -0.5, 0], color=INK, stroke_width=3),
                          Rectangle(width=2.0, height=0.18, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, -0.59, 0]))
        lp, rp = pan(-3.6), pan(3.6)
        stack = VGroup(*[card(-3.6, -0.37 + k * 0.34, w=1.4, h=0.22) for k in range(5)])
        rl = T("records", 36).move_to([-3.6, -2.7, 0])
        self.play(FadeIn(post), Create(foot), Create(beam), FadeIn(lp), FadeIn(rp), FadeIn(rl), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in stack], lag_ratio=0.12), run_time=1.0)
        until(self, "because of one")
        tile = VGroup(Rectangle(width=0.6, height=0.5, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4),
                      scribble(-0.2, 0, 0.4, amp=0.04, sw=3)).move_to([3.6, 2.6, 0])
        al = T("assumption", 36).move_to([3.6, -2.7, 0])
        self.play(FadeIn(tile), FadeIn(al), run_time=0.3)
        self.play(tile.animate.move_to([3.6, -0.25, 0]), run_time=0.45, rate_func=ease_in)
        ang = -0.22
        new_beam = Line(piv + np.array([-3.6 * np.cos(ang), -3.6 * np.sin(ang), 0]),
                        piv + np.array([3.6 * np.cos(ang), 3.6 * np.sin(ang), 0]), color=INK, stroke_width=8)
        dy = 3.6 * np.sin(ang)
        self.play(Transform(beam, new_beam), VGroup(lp, stack).animate.shift([0, -dy, 0]),
                  VGroup(rp, tile).animate.shift([0, dy, 0]), run_time=0.8)
        until(self, "four statements")
        marks = VGroup(*[dashed_box(-2.2 + i * 0.7, 2.9, 0.5, 0.5) for i in range(4)])
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.2), run_time=0.8)
        until(self, "sensitivity check")
        track = Line([1.4, 2.7, 0], [5.4, 2.7, 0], color=INK, stroke_width=5)
        knob = Circle(radius=0.16, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([2.0, 2.7, 0])
        self.play(Create(track), FadeIn(knob), run_time=0.4)
        self.play(knob.animate.move_to([4.8, 2.7, 0]), run_time=1.0)
        flips = VGroup(*[Dot([2.2 + i * 0.6, 2.2, 0], radius=0.08, color=TERRA if i == 2 else INK) for i in range(5)])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in flips], lag_ratio=0.15), run_time=0.7)
        finish(self)


class B11_Piles(Scene):
    def construct(self):
        L = Iso(-3.2, -1.1, 0.75); R = Iso(3.2, -1.1, 0.75)
        bl = L.box(-1.6, -1.6, 0, 3.2, 3.2, 0.15); br = R.box(-1.6, -1.6, 0, 3.2, 3.2, 0.15)
        hl = T("have", 40).move_to([-3.2, -2.85, 0]); ll = T("learning", 40).move_to([3.2, -2.85, 0])
        self.play(FadeIn(bl), FadeIn(br), FadeIn(hl), FadeIn(ll), run_time=0.6)
        until(self, "The domain is mine")
        have = [L.box(-1.0, -1.0, 0.15, 0.9, 0.9, 0.7), L.page(0.2, -1.0, 0.15, w=0.9, d=1.0), L.box(-0.6, 0.2, 0.15, 0.8, 0.8, 0.5)]
        for it in have:
            self.play(FadeIn(it, shift=DOWN * 0.4), run_time=0.4, rate_func=ease_in)
        until(self, "The code was written")
        ai = L.mcp(0.4, 0.4, 0.15, w=0.8, d=0.8, h=0.45)
        self.play(FadeIn(ai, shift=DOWN * 0.3), run_time=0.4)
        until(self, "New to me")
        for x, y in [(2.4, -0.3), (3.4, 0.0), (4.3, -0.3)]:
            self.play(Create(dashed_box(x, y, 0.8, 0.8)), run_time=0.35)
        half = R.box(-0.9, -0.9, 0.15, 0.8, 0.8, 0.35)
        self.play(FadeIn(half, shift=DOWN * 0.3), run_time=0.4)
        finish(self)
