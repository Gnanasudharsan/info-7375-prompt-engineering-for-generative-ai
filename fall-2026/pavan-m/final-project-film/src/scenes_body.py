

# ═════════════════════════════ cite-the-line-pitch — scenes ═════════════════════════════
# Build:  cat <toolkit>/skills/make/show-tell/templates/iso_kit.py scenes_body.py > scenes.py
# (show-tell: paste the kit at the top of scenes.py; never import it.)
#
# Timing rule used in every scene (GATE T and Gate V sample each clip at its MIDPOINT):
#   phase A — every arrival, label and move finishes by 36% of the beat;
#   hold    — nothing moves between 36% and 62%;
#   phase B — from 62%, one more NEW shape lands (Gate A needs a new shape after frame 1).
# Every body beat carries the on-screen "constructed sketch" tag: nothing shown is built yet.

A_END, B_START = 0.36, 0.62


def dur(self):
    """Measured audio for this beat; 6 s when the sheet isn't beside scenes.py (Gate A's sandbox)."""
    return _TARGET.get(type(self).__name__.split("_")[0], 0) or 6.0


def at(self, frac):
    gap = frac * dur(self) - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def tag():
    return T("constructed sketch", 32).move_to([4.6, -2.95, 0])


def lab(s, x, y, size=36):
    return T(s, size).move_to([x, y, 0])


def logpage(x, y, w=2.4, h=3.0, rows=6, lengths=(0.85, 0.6, 0.95, 0.7, 0.9, 0.5)):
    """A page of log lines: white sheet, kraft shadow, grey line bars. `.rowy` = each bar's y."""
    pg = paper(x, y, w, h)
    bars, rowy = VGroup(), []
    for i in range(rows):
        yy = y + h / 2 - 0.45 - i * (h - 0.8) / max(1, rows - 1)
        x0 = x - w / 2 + 0.45
        bars.add(Line([x0, yy, 0], [x0 + (w - 0.8) * lengths[i % len(lengths)], yy, 0], color=GHOST, stroke_width=9))
        rowy.append(yy)
    g = VGroup(pg, bars)
    g.rowy, g.x0 = rowy, x - w / 2
    return g


def slip(x, y, w=1.7, h=1.0, dots=2):
    """The result slip: card, one grey cause pill, terracotta line-number dots."""
    card = Rectangle(width=w, height=h, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    bar = RoundedRectangle(width=w * 0.55, height=0.22, corner_radius=0.11, fill_color=BAR2, fill_opacity=1,
                           stroke_width=0).move_to([x - w * 0.12, y + h * 0.17, 0])
    ds = VGroup(*[Dot([x - w * 0.32 + i * 0.32, y - h * 0.22, 0], radius=0.07, color=TERRA) for i in range(dots)])
    return VGroup(card, bar, ds)


def cross(x, y, s=0.32, w=8):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


def lens(x, y, r=0.55):
    ring = Circle(radius=r, stroke_color=INK, stroke_width=8, fill_opacity=0).move_to([x, y, 0])
    handle = Line([x + r * 0.7, y - r * 0.7, 0], [x + r * 1.5, y - r * 1.5, 0], color=INK, stroke_width=10)
    return VGroup(ring, handle)


def cylinder(x, y, w=1.6, h=1.4, top=BOX_TOP, body=BOX_R):
    e = 0.36
    bottom = Ellipse(width=w, height=e, fill_color=body, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y - h / 2, 0])
    side = Rectangle(width=w, height=h, fill_color=body, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    edges = VGroup(Line([x - w / 2, y - h / 2, 0], [x - w / 2, y + h / 2, 0], color=INK, stroke_width=4),
                   Line([x + w / 2, y - h / 2, 0], [x + w / 2, y + h / 2, 0], color=INK, stroke_width=4))
    lid = Ellipse(width=w, height=e, fill_color=top, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + h / 2, 0])
    return VGroup(bottom, side, edges, lid)


def floor_shadow(x, y, w=2.6):
    return Ellipse(width=w, height=0.32, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def dashed_rect(x, y, w, h, n=6, color=DIM, sw=5):
    """A dashed outline from short lines (no DashedVMobject, to stay inside Gate A's stub)."""
    g = VGroup()
    corners = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)]
    for k in range(4):
        (ax, ay), (bx, by) = corners[k], corners[(k + 1) % 4]
        for i in range(n):
            t0, t1 = i / n, (i + 0.55) / n
            g.add(Line([ax + (bx - ax) * t0, ay + (by - ay) * t0, 0], [ax + (bx - ax) * t1, ay + (by - ay) * t1, 0],
                       color=color, stroke_width=sw))
    return g


# ── Q1: what is it ──────────────────────────────────────────────────────────────

class B00_LogPage(Scene):
    def construct(self):
        d = dur(self)
        self.add(tag())
        pg = logpage(0, 0.35)
        self.play(FadeIn(pg, shift=DOWN * 0.8), run_time=0.16 * d, rate_func=ease_in)
        self.play(FadeIn(floor_shadow(0.12, -1.35)), FadeIn(lab("log", 2.1, 1.6)), run_time=0.12 * d)
        at(self, B_START)
        self.play(GrowFromCenter(Dot([-0.55, pg.rowy[0], 0], radius=0.08, color=TERRA)), run_time=0.12 * d)
        finish(self)


class B01_LensCites(Scene):
    def construct(self):
        d = dur(self)
        pg = logpage(-2.6, 0.3)
        self.add(tag(), pg)
        ln = lens(-4.9, 1.9)
        self.play(FadeIn(ln), run_time=0.06 * d)
        self.play(ln.animate.move_to([-2.2, pg.rowy[2] - 0.15, 0]), run_time=0.1 * d)
        hits = VGroup(*[Dot([pg.x0 + 0.22, pg.rowy[i], 0], radius=0.08, color=TERRA) for i in (2, 4)])
        self.play(LaggedStart(*[GrowFromCenter(h) for h in hits], lag_ratio=0.4), run_time=0.07 * d)
        s = slip(2.7, 0.5)
        self.play(FadeIn(s, shift=LEFT * 0.4), FadeIn(lab("cause", 2.7, -0.55)), run_time=0.1 * d)
        at(self, B_START)
        self.play(Create(check(4.1, 0.55)), run_time=0.12 * d)
        finish(self)


class B02_NotEnough(Scene):
    def construct(self):
        d = dur(self)
        pg = logpage(-2.6, 0.3, rows=3, lengths=(0.4, 0.3, 0.35))
        self.add(tag(), pg)
        ln = lens(-2.3, 1.4)
        self.play(FadeIn(ln), run_time=0.06 * d)
        self.play(ln.animate.move_to([-2.3, -0.3, 0]), run_time=0.12 * d)
        empty = Rectangle(width=1.7, height=1.0, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([2.7, 0.5, 0])
        self.play(FadeIn(empty, shift=LEFT * 0.4), FadeIn(lab("not enough", 2.7, -0.95)), run_time=0.12 * d)
        at(self, B_START)
        self.play(FadeIn(floor_shadow(2.75, -0.2, w=1.9)), run_time=0.12 * d)
        finish(self)


class B03_BreakService(Scene):
    def construct(self):
        d = dur(self)
        iso = Iso(-3.0, -1.3, 1.0)
        stack, lights = iso.server(0, 0, 0, w=1.6, d=1.6, slab=0.5, n=3)
        self.add(tag())
        self.play(FadeIn(stack), FadeIn(lights), FadeIn(lab("service", -3.0, -2.0)), run_time=0.08 * d)
        xs = (0.4, 2.2, 4.0)
        for i in range(3):
            page = logpage(xs[i], 0.4, w=1.3, h=1.7, rows=3)
            cause = Dot([xs[i] + 0.45, -0.25, 0], radius=0.08, color=TERRA)
            self.play(lights[i].animate.set_color(TERRA), FadeIn(page, shift=DOWN * 0.4), run_time=0.07 * d)
            self.play(GrowFromCenter(cause), run_time=0.02 * d)
        at(self, B_START)
        self.play(FadeIn(floor_shadow(-3.0, -1.45, w=3.0)), run_time=0.12 * d)
        finish(self)


# ── Q4: the contract and the checker ────────────────────────────────────────────

class B04_Contract(Scene):
    def construct(self):
        d = dur(self)
        iso = Iso(-0.4, -1.1, 1.0)
        back, front = iso.open_box(0, 0, 0, 2.0, 2.0, 1.0)
        self.add(tag())
        self.play(FadeIn(back), FadeIn(front), FadeIn(lab("Claude Code", -0.4, -1.9)), run_time=0.08 * d)
        pg = logpage(-4.6, 0.9, w=1.3, h=1.7, rows=3)
        pg.set_z_index(1)
        self.play(FadeIn(pg), run_time=0.05 * d)
        self.play(pg.animate.scale(0.42).move_to(iso.p(1.3, 1.3, 0.3)), run_time=0.1 * d, rate_func=ease_in)
        s = slip(3.8, 0.6)
        self.play(FadeIn(s, shift=RIGHT * 0.5), FadeIn(lab("contract", 3.8, -0.45)), run_time=0.1 * d)
        at(self, B_START)
        self.play(FadeIn(floor_shadow(-0.4, -1.25, w=3.2)), run_time=0.12 * d)
        finish(self)


class B05_Checker(Scene):
    def construct(self):
        d = dur(self)
        self.add(tag())
        scan = Line([-1.4, -0.9, 0], [-1.4, 1.5, 0], color=TERRA, stroke_width=7)
        self.play(Create(scan), FadeIn(lab("checker", -1.4, 2.0)), run_time=0.06 * d)
        s = slip(-4.3, 0.3)
        self.play(FadeIn(s), run_time=0.04 * d)
        self.play(s.animate.move_to([-1.4, 0.3, 0]), run_time=0.08 * d)
        self.play(Create(check(-1.5, -1.45)), run_time=0.04 * d)
        row = VGroup(*[slip(x, 0.3, w=1.3, h=0.8) for x in (1.2, 2.9, 4.6)])
        marks = VGroup(*[check(x - 0.1, -0.65, s=0.16) for x in (1.2, 2.9, 4.6)])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in row], lag_ratio=0.3), run_time=0.08 * d)
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.3), run_time=0.05 * d)
        at(self, B_START)
        self.play(Create(Line([0.3, -1.05, 0], [5.5, -1.05, 0], color=GHOST, stroke_width=6)), run_time=0.12 * d)
        finish(self)


# ── Q2: the alternative, and the difference ─────────────────────────────────────

class B06_ClosedBox(Scene):
    def construct(self):
        d = dur(self)
        iso = Iso(0.0, -1.5, 1.0)
        plinth = iso.box(-0.2, -0.2, -0.3, 2.9, 2.9, 0.3, DARK_TOP, DARK_L, DARK_R)
        box = iso.box(0, 0, 0, 2.5, 2.5, 1.6)
        self.add(tag())
        self.play(FadeIn(plinth), FadeIn(box), FadeIn(lab("vendor platform", 0.0, -2.45)), run_time=0.09 * d)
        pg = logpage(-4.7, 0.6, w=1.3, h=1.7, rows=3)
        self.play(FadeIn(pg), run_time=0.05 * d)
        self.play(pg.animate.move_to([-3.0, 0.4, 0]), run_time=0.07 * d)
        self.play(FadeOut(pg), run_time=0.04 * d)
        s = slip(4.0, 0.6)
        self.play(FadeIn(s, shift=RIGHT * 0.4), run_time=0.08 * d)
        at(self, B_START)
        self.play(GrowFromCenter(Dot(iso.p(0.0, 1.25, 0.8), radius=0.1, color=TERRA)), run_time=0.12 * d)
        finish(self)


class B07_OpenCrate(Scene):
    def construct(self):
        d = dur(self)
        iso = Iso(-1.6, -1.3, 1.0)
        back, front = iso.open_box(0, 0, 0, 2.4, 2.4, 1.0)
        pages = VGroup(iso.page(1.4, 0.2, 0.05, w=0.9, d=1.0), iso.page(0.2, 1.3, 0.05, w=0.9, d=1.0))
        pages.set_z_index(1)
        self.add(tag())
        self.play(FadeIn(back), FadeIn(front), FadeIn(lab("test bench", -1.6, -2.1)), run_time=0.08 * d)
        self.play(FadeIn(pages, shift=DOWN * 0.3), run_time=0.08 * d)
        good, bad = slip(2.7, 1.1, w=1.4, h=0.8), slip(2.7, -0.6, w=1.4, h=0.8)
        self.play(FadeIn(good), FadeIn(bad), run_time=0.08 * d)
        self.play(Create(check(4.0, 1.1)), Create(cross(4.15, -0.6)), run_time=0.08 * d)
        at(self, B_START)
        self.play(FadeIn(floor_shadow(-1.6, -1.45, w=3.6)), run_time=0.12 * d)
        finish(self)


# ── Q3: who opens it, first sixty seconds ───────────────────────────────────────

class B08_Readme(Scene):
    def construct(self):
        d = dur(self)
        self.add(tag())
        card = Rectangle(width=5.0, height=3.6, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.2, 0.0, 0])
        header = Rectangle(width=5.0, height=0.5, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-1.2, 1.55, 0])
        self.play(FadeIn(card, shift=DOWN * 0.4), FadeIn(header), FadeIn(lab("README", -1.2, 2.4)), run_time=0.1 * d)
        rows = VGroup()
        for i, yy in enumerate((0.75, -0.15, -1.05)):
            rows.add(RoundedRectangle(width=1.9, height=0.26, corner_radius=0.13, fill_color=BAR2, fill_opacity=1,
                                      stroke_width=0).move_to([-2.4, yy, 0]))
            rows.add(Rectangle(width=1.3, height=0.6, fill_color=CARD, fill_opacity=1, stroke_color=BAR1,
                               stroke_width=3).move_to([0.3, yy, 0]))
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=0.12 * d)
        self.play(FadeIn(lab("no results yet", 3.5, -0.15)), run_time=0.08 * d)
        at(self, B_START)
        self.play(Create(Line([-3.5, -1.55, 0], [1.1, -1.55, 0], color=GHOST, stroke_width=5)), run_time=0.12 * d)
        finish(self)


class B09_ThreePanels(Scene):
    def construct(self):
        d = dur(self)
        self.add(tag())
        row = RoundedRectangle(width=3.2, height=0.42, corner_radius=0.21, fill_color=BAR2, fill_opacity=1,
                               stroke_width=0).move_to([-0.6, 2.3, 0])
        self.play(FadeIn(row), FadeIn(lab("one incident", 2.7, 2.3)), run_time=0.07 * d)
        cur = cursor(-3.6, 1.4)
        self.play(FadeIn(cur), run_time=0.04 * d)
        self.play(cur.animate.move_to([-0.5, 2.15, 0]), run_time=0.08 * d)
        panel = Rectangle(width=1.9, height=2.4, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([3.6, -0.3, 0])
        self.play(FadeIn(logpage(-3.6, -0.3, w=1.9, h=2.4, rows=4), shift=DOWN * 0.3),
                  FadeIn(slip(0.0, -0.3, w=1.9, h=1.3), shift=DOWN * 0.3),
                  FadeIn(panel, shift=DOWN * 0.3), run_time=0.1 * d)
        self.play(Create(check(3.55, -0.3, s=0.32)), run_time=0.06 * d)
        at(self, B_START)
        self.play(FadeIn(floor_shadow(0.0, -1.85, w=9.0)), run_time=0.12 * d)
        finish(self)


# ── Q4: what it proves, and where that stops ────────────────────────────────────

class B10_TestNotTrust(Scene):
    def construct(self):
        d = dur(self)
        self.add(tag())
        piv = [0.0, -0.4, 0]
        fulcrum = Polygon([0, -0.4, 0], [-0.55, -1.95, 0], [0.55, -1.95, 0], fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4)
        beam = Line([-2.6, -0.4, 0], [2.6, -0.4, 0], color=INK, stroke_width=9)

        def pan(cx, word):
            strings = VGroup(Line([cx, -0.4, 0], [cx - 0.6, -1.5, 0], color=INK, stroke_width=3),
                             Line([cx, -0.4, 0], [cx + 0.6, -1.5, 0], color=INK, stroke_width=3))
            dish = Polygon([cx - 0.75, -1.5, 0], [cx + 0.75, -1.5, 0], [cx + 0.45, -1.8, 0], [cx - 0.45, -1.8, 0],
                           fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
            # label BESIDE the pan, outside the balance (first cut put it under the pan, inside the
            # drawing's bounding box, and GATE T §8.6b read it as overlapping text)
            return VGroup(strings, dish, lab(word, cx + (-1.6 if cx < 0 else 1.6), -1.65))

        left, right = pan(-2.6, "test"), pan(2.6, "trust")
        self.play(FadeIn(fulcrum), Create(beam), FadeIn(left), FadeIn(right), run_time=0.1 * d)
        s = slip(-2.6, 1.6, w=1.1, h=0.6, dots=1)
        self.play(FadeIn(s), run_time=0.04 * d)
        self.play(s.animate.move_to([-2.6, -1.18, 0]), run_time=0.08 * d, rate_func=ease_in)
        left.add(s)
        self.play(beam.animate.rotate(0.115, about_point=piv), left.animate.shift(DOWN * 0.3),
                  right.animate.shift(UP * 0.3), run_time=0.1 * d)
        at(self, B_START)
        own = VGroup(*[paper(4.3 + dx, 1.7 + dy, 0.6, 0.75) for dx, dy in ((-0.4, 0), (0.0, 0.08), (0.4, 0))])
        self.play(FadeIn(own), Create(dashed_rect(4.3, 1.75, 1.9, 1.3, n=5)), run_time=0.14 * d)
        finish(self)


# ── Q5: in, out, first ──────────────────────────────────────────────────────────

class B11_NeverActs(Scene):
    def construct(self):
        d = dur(self)
        self.add(tag())
        btn = Circle(radius=1.0, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([-2.2, 0.4, 0])
        arc = Arc(radius=0.55, start_angle=PI * 0.6, angle=PI * 1.6, color=INK, stroke_width=9).move_arc_center_to([-2.2, 0.4, 0])
        tip_at = np.array([-2.2 + 0.55 * np.cos(PI * 0.6), 0.4 + 0.55 * np.sin(PI * 0.6), 0])
        tip = Polygon(tip_at + [0.0, 0.2, 0], tip_at + [0.0, -0.2, 0], tip_at + [-0.28, 0.0, 0],
                      fill_color=INK, fill_opacity=1, stroke_width=0)
        self.play(FadeIn(btn), Create(arc), FadeIn(tip), FadeIn(lab("restart", -2.2, -1.35)), run_time=0.12 * d)
        self.play(FadeIn(logpage(1.9, 0.4, w=1.6, h=2.0, rows=3)), FadeIn(slip(3.9, 0.4, w=1.4, h=0.8)), run_time=0.12 * d)
        at(self, B_START)
        self.play(Create(cross(-2.2, 0.4, s=0.95, w=12)), run_time=0.14 * d)
        finish(self)


class B12_FirstRun(Scene):
    def construct(self):
        d = dur(self)
        self.add(tag())
        db = cylinder(-4.2, 0.3, w=1.5, h=1.5)
        self.play(FadeIn(db), run_time=0.08 * d)
        pg = logpage(-1.6, 0.3, w=1.5, h=1.9, rows=3)
        s = slip(0.9, 0.3, w=1.5, h=0.9)
        self.play(FadeIn(pg, shift=RIGHT * 0.3), run_time=0.07 * d)
        self.play(FadeIn(s, shift=RIGHT * 0.3), FadeIn(lab("first run", -0.4, -1.4)), run_time=0.08 * d)
        self.play(Create(check(2.5, 0.3, s=0.26)), run_time=0.06 * d)
        at(self, B_START)
        stamp = RoundedRectangle(width=1.5, height=0.9, corner_radius=0.18, fill_color=CARD, fill_opacity=1,
                                 stroke_color=INK, stroke_width=5).move_to([4.4, 0.9, 0]).rotate(-0.18)
        marks = VGroup(*[Line([3.9, yy, 0], [4.9, yy, 0], color=BAR1, stroke_width=6) for yy in (1.05, 0.75)]).rotate(-0.18, about_point=[4.4, 0.9, 0])
        self.play(FadeIn(stamp, scale=1.3), FadeIn(marks, scale=1.3), run_time=0.12 * d)
        finish(self)


# ── Q6: what could sink it ──────────────────────────────────────────────────────

class B13_TooEasy(Scene):
    def construct(self):
        d = dur(self)
        self.add(tag())
        sheets = VGroup(*[Rectangle(width=2.6, height=0.6, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK,
                                    stroke_width=4).move_to([0.0, yy, 0]) for yy in (-0.55, 0.2, 0.95, 1.7)])
        self.play(LaggedStart(*[FadeIn(sh, shift=DOWN * 0.4) for sh in sheets], lag_ratio=0.3), run_time=0.16 * d)
        self.play(FadeIn(lab("API errors", -2.9, 1.1)), run_time=0.08 * d)
        at(self, B_START)
        self.play(FadeIn(cylinder(0.0, -1.75, w=1.3, h=0.6, top=DARK_TOP, body=DARK_R)),
                  FadeIn(lab("real cause", 2.3, -1.8)), run_time=0.12 * d)
        finish(self)


class B14_HardCases(Scene):
    def construct(self):
        d = dur(self)
        iso = Iso(-1.9, -1.3, 1.0)
        back, front = iso.open_box(0, 0, 0, 2.4, 2.4, 1.0)
        self.add(tag(), back, front, lab("test bench", -1.9, -2.1))
        cases = [iso.page(1.4, 0.2, 0.05, w=0.9, d=1.0), iso.page(0.2, 1.3, 0.05, w=0.9, d=1.0)]
        for c in cases:
            c.set_z_index(1)
            c.shift(LEFT * 3.2)
            self.play(FadeIn(c), run_time=0.04 * d)
            self.play(c.animate.shift(RIGHT * 3.2), run_time=0.1 * d)
        at(self, B_START)
        self.play(Create(dashed_rect(3.6, 0.6, 1.6, 1.6)), FadeIn(lab("plan B", 3.6, -0.6)), run_time=0.14 * d)
        finish(self)


# ── Q7: what I have, what I'm learning ──────────────────────────────────────────

class B15_TwoPiles(Scene):
    def construct(self):
        d = dur(self)
        self.add(tag())
        have_iso, learn_iso = Iso(-3.4, -1.3, 1.0), Iso(2.2, -1.3, 1.0)
        have = VGroup(*[have_iso.box(0, 0, z, 1.0, 1.0, 0.6, DARK_TOP, DARK_L, DARK_R) for z in (0.0, 0.68, 1.36)])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in have], lag_ratio=0.3), FadeIn(lab("have", -3.4, -2.0)),
                  run_time=0.14 * d)
        learn = [learn_iso.box(0, 0, z, 1.0, 1.0, 0.6, STAGE, STAGE, STAGE) for z in (0.0, 0.68, 1.36)]
        self.play(FadeIn(lab("learning", 2.2, -2.0)), Create(learn[0]), run_time=0.08 * d)
        self.play(Create(learn[1]), run_time=0.07 * d)
        at(self, B_START)
        self.play(Create(learn[2]), run_time=0.12 * d)
        finish(self)


# ── Close: exists vs will exist ─────────────────────────────────────────────────

class B16_ExistsVsWill(Scene):
    # Same visual language as B15: solid dark = real today, ink outline = not built yet.
    # (First cut used pale ghost boxes; Gate V measured contrast 0.22 < 0.30.)
    def construct(self):
        d = dur(self)
        self.add(tag())
        small = Iso(-3.8, -0.9, 1.0).box(0, 0, 0, 0.7, 0.7, 0.5, DARK_TOP, DARK_L, DARK_R)
        self.play(FadeIn(small, shift=DOWN * 0.3), FadeIn(lab("exists", -3.8, -1.6)), run_time=0.12 * d)
        big = Iso(1.6, -1.7, 1.0)
        outline = VGroup(*[big.box(x, y, 0, 1.0, 1.0, 0.8, STAGE, STAGE, STAGE) for x, y in ((1.05, 1.05), (1.05, 0), (0, 1.05), (0, 0))])
        self.play(LaggedStart(*[Create(g) for g in outline], lag_ratio=0.2), FadeIn(lab("will exist", 1.6, -2.5)), run_time=0.16 * d)
        at(self, B_START)
        crown = big.box(0.5, 0.5, 0.85, 1.0, 1.0, 0.8, STAGE, STAGE, STAGE)
        self.play(Create(crown), run_time=0.12 * d)
        finish(self)
