
# ═════════════════════════════ FILM-LOCAL KIT ═════════════════════════════
# the-names-nothing-checks — INFO 7375 final-project pitch film.
#
# Everything above this line is brutalist.art/skills/make/show-tell/templates/iso_kit.py,
# pasted verbatim per SKILL.md ("do not import it: Gate A copies only scenes.py").
#
# THE CAST, kept for the whole film:
#   the project slab   — one crate split by a divider: pale PAGES on the left (the C# scripts),
#                        dark BLOCKS on the right (the assets that hold the real names)
#   the string thread  — one ink line reaching from a page across to a block
#   the two gates      — compiler and console, both of which stay open
#   the effect lamp    — the thing that was supposed to happen; stays grey
#   the checklist slip — the proposed tool's output
#
# MIDPOINT DISCIPLINE. GATE T and Gate V both sample each clip at its MIDPOINT, so every
# scene is built in three phases: (1) construct and land the labels well before the midpoint,
# (2) hold_past_mid() through the sampled window with nothing in flight, (3) add one NEW
# non-text shape afterwards, which is also what Gate A's "shapes never change" check wants.

DKRAFT = "#917A55"        # outline for SMALL objects only (GATE T reads it as text on large ones)
CONNECT = "#9C8462"       # cables and leader lines, so they do not fuse with ink blocks
MID_MARGIN = 0.22         # frame rounding beats a 0.06-0.08 s margin (SKILL.md)


def hold_past_mid(self, margin=MID_MARGIN):
    """Hold with nothing in flight until the GATE T / Gate V sampling window has passed."""
    bid = type(self).__name__.split("_")[0]
    target = _TARGET.get(bid, 0)
    if not target:
        self.wait(0.5)
        return
    gap = (target / 2.0 + margin) - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def label(text, x, y, size=42):
    """A label that sits BESIDE its object — never inside an outline, never terracotta.
    Floor raised from 36 to 42 on 2026-10-14: GATE T failed a serif run 1 px under its 41 px
    minimum on the author's week-01 film, and EB Garamond renders shorter than sans at the
    same nominal size. Every label here is serif."""
    return T(text, size=size, color=INK).move_to([x, y, 0])


def floor_shadow(x, y, w=4.6, h=1.0):
    return Ellipse(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def project_iso():
    return Iso(-0.4, -1.4, 0.85)


def project_slab(iso):
    """The crate everything else sits on, plus the divider between its two halves."""
    slab = iso.box(0, 0, 0, 4.4, 2.8, 0.45)
    divider = Line(iso.p(2.2, 0.0, 0.45), iso.p(2.2, 2.8, 0.45), color=DIM, stroke_width=4)
    return slab, divider


def script_pages(iso):
    return VGroup(iso.page(0.35, 0.35, 0.45), iso.page(0.35, 1.45, 0.45))


def asset_blocks(iso):
    return VGroup(iso.mcp(2.45, 0.35, 0.45, w=1.3, d=1.0, h=0.6),
                  iso.mcp(2.45, 1.55, 0.45, w=1.3, d=1.0, h=0.6))


def string_thread(iso, to_block=True):
    """The one ink line from a page to a block. Deep kraft so it does not fuse with the dark blocks."""
    a = iso.p(1.2, 1.05, 0.52)
    b = iso.p(2.45, 0.85, 0.75) if to_block else iso.p(3.9, -1.1, 0.75)
    return Line(a, b, color=CONNECT, stroke_width=5), b


def slip(x, y, w=2.5, h=3.0, rows=5):
    """The checklist: a flat sheet whose rows are filled by check marks, not type."""
    sheet = paper(x, y, w=w, h=h)
    ys = [y + h / 2 - 0.5 - i * (h - 1.0) / max(1, rows - 1) for i in range(rows)]
    return sheet, ys


def glow(x, y, s=1.0):
    """The sword glow from the author's own Unity game, drawn as what it is: one terracotta ring
    around the block, with a spark. A drawn sword read as a rocket in the first contact sheet, and
    terracotta is permitted on one curve and on dots — never on text.
    The ring opens at the bottom (300 degrees, not the earlier 115-degree arc): GATE T reads a
    wide-and-short terracotta blob as accent TYPE and fails it on cream at 2.74:1, so the one
    curve in this film is drawn taller than it is wide, which is not a text shape."""
    arc = Arc(radius=0.55 * s, start_angle=-PI / 3, angle=PI * 5 / 3, arc_center=[x, y, 0],
              stroke_color=TERRA, stroke_width=5)
    spark = Dot([x, y + 0.55 * s, 0], radius=0.09, color=TERRA)
    return VGroup(arc, spark)


def bar_stack(x, y0, segs, w=0.62):
    """A chart column: DIM-to-GHOST segments with visible gaps, so GATE T cannot fuse them."""
    cols = [BAR1, BAR2, BAR3]
    g, y = VGroup(), y0
    for i, hgt in enumerate(segs):
        g.add(Rectangle(width=w, height=hgt, fill_color=cols[i % 3], fill_opacity=1,
                        stroke_color=DKRAFT, stroke_width=2).move_to([x, y + hgt / 2, 0]))
        y += hgt + 0.1
    return g


def gate_arch(x, y, w=1.5, h=2.0):
    """An open gate: two posts and a lintel. Nothing closes it — that is the point of B02."""
    return VGroup(
        Rectangle(width=0.18, height=h, fill_color=BOX_R, fill_opacity=1, stroke_color=INK,
                  stroke_width=4).move_to([x - w / 2, y + h / 2, 0]),
        Rectangle(width=0.18, height=h, fill_color=BOX_R, fill_opacity=1, stroke_color=INK,
                  stroke_width=4).move_to([x + w / 2, y + h / 2, 0]),
        Rectangle(width=w + 0.18, height=0.2, fill_color=BOX_R, fill_opacity=1, stroke_color=INK,
                  stroke_width=4).move_to([x, y + h + 0.1, 0]))


# ═════════════════════════════ SCENES ═════════════════════════════
# run.sh finds scenes by grepping this file for the literal class-definition text, so every
# scene below is written out plainly and none subclasses a helper (a subclassed one is silently
# skipped — SKILL.md). For the same reason this comment does not spell that pattern out: an
# earlier version quoted SKILL.md's example placeholder verbatim, run.sh read the comment as a
# fifteenth scene, and Gate A failed on a class that does not exist.


class B00_Project(Scene):
    def construct(self):
        iso = project_iso()
        sh = floor_shadow(0.0, -1.55)
        slab, divider = project_slab(iso)
        pages, blocks = script_pages(iso), asset_blocks(iso)
        l_left, l_right = label("scripts", -3.6, -0.9), label("assets", 3.5, -0.3)

        self.play(FadeIn(sh, shift=np.array([0, 0.2, 0])), run_time=0.4)
        self.play(Create(slab), run_time=0.9, rate_func=smooth)
        until(self, "One side holds")
        self.play(LaggedStart(*[FadeIn(p, shift=np.array([0, 0.35, 0])) for p in pages], lag_ratio=0.3),
                  FadeIn(l_left), run_time=1.0, rate_func=ease_in)
        until(self, "The other")
        self.play(LaggedStart(*[GrowFromCenter(b) for b in blocks], lag_ratio=0.3),
                  FadeIn(l_right), run_time=1.0)

        hold_past_mid(self)
        self.play(Create(divider), run_time=0.6)      # the new shape, clear of the midpoint
        finish(self)


class B01_StringReach(Scene):
    def construct(self):
        iso = project_iso()
        sh = floor_shadow(0.0, -1.55)
        slab, divider = project_slab(iso)
        pages, blocks = script_pages(iso), asset_blocks(iso)
        base = VGroup(sh, slab, divider, pages, blocks)          # continuity: B00 ended with all of this
        # The reach is the whole point of the beat, so it arcs well clear of the crate instead of
        # running flat between two dark blocks, where it was invisible in the first contact sheet.
        a, mid, b = iso.p(0.9, 1.5, 0.6), np.array([0.1, 2.5, 0.0]), iso.p(2.9, 0.9, 1.15)
        thread = VMobject(stroke_color=CONNECT, stroke_width=7)
        thread.set_points_smoothly([a, mid, b])
        dot = Dot(b, radius=0.1, color=TERRA)
        lbl = label("string", -2.9, 2.5)

        self.add(base)
        self.play(pages[1].animate.shift(np.array([0.0, 0.22, 0.0])), run_time=0.5, rate_func=smooth)
        until(self, "A string")
        self.play(Create(thread), FadeIn(lbl), run_time=1.2, rate_func=linear)

        hold_past_mid(self)
        self.play(GrowFromCenter(dot), run_time=0.5)
        finish(self)


class B02_SilentPass(Scene):
    def construct(self):
        # The crate keeps its pages and blocks here: B01 ended with a full project on stage, and
        # an empty slab broke the film's "same objects, whole film" law in the first contact sheet.
        iso = Iso(-4.6, -0.9, 0.5)
        sh = floor_shadow(-4.3, -1.05, w=2.8, h=0.7)
        slab, divider = project_slab(iso)
        pages, blocks = script_pages(iso), asset_blocks(iso)
        g1, g2 = gate_arch(-0.4, -1.1), gate_arch(3.0, -1.1)
        # The lamp is the effect that was supposed to happen. It must still be grey at the end,
        # and the terracotta runner must stop OUTSIDE it: parked in the middle of the lamp, the
        # accent colour reads as "lit", which is the opposite of what the narration says.
        lamp = Circle(radius=0.36, fill_color=GHOST, fill_opacity=1, stroke_color=INK,
                      stroke_width=4).move_to([5.0, -0.1, 0])
        runner = Dot([-2.5, -0.1, 0], radius=0.11, color=TERRA)
        l1, l2 = label("compiler", -0.4, -1.9, 42), label("console", 3.0, -1.9, 42)
        l3 = label("no error", 4.7, 1.6, 42)
        ring = Circle(radius=0.68, stroke_color=DIM, stroke_width=4,
                      fill_opacity=0).move_to([5.0, -0.1, 0])

        self.add(sh, slab, divider, pages, blocks)
        self.play(Create(g1), Create(g2), FadeIn(l1), FadeIn(l2), run_time=0.9)
        self.play(FadeIn(lamp), GrowFromCenter(runner), run_time=0.5)
        until(self, "The compiler")
        self.play(runner.animate.move_to([4.25, -0.1, 0]), run_time=1.5, rate_func=linear)
        self.play(FadeIn(l3), run_time=0.4)

        hold_past_mid(self)
        self.play(Create(ring), run_time=0.6)          # the lamp never lit; only the ring is new
        finish(self)


class B02B_WhatWarns(Scene):
    def construct(self):
        # The honest qualifier beat. Unity DOES print "Parameter 'X' does not exist" for a bad
        # animator parameter once the line runs; the Unity manual says a shader property that is
        # not on the current shader simply "will have no effect".
        # The bar must CLOSE the gate's opening horizontally — drawn vertically it merged into a
        # post and the beat read as two runners passing nothing.
        iso = Iso(-4.6, -0.9, 0.5)
        sh = floor_shadow(-4.3, -1.05, w=2.8, h=0.7)
        slab, divider = project_slab(iso)
        pages, blocks = script_pages(iso), asset_blocks(iso)
        g1, g2 = gate_arch(-0.4, -1.1), gate_arch(3.0, -1.1)
        lamp = Circle(radius=0.36, fill_color=GHOST, fill_opacity=1, stroke_color=INK,
                      stroke_width=4).move_to([5.0, -0.1, 0])
        top = Dot([-2.3, 0.55, 0], radius=0.11, color=TERRA)
        low = Dot([-2.3, -0.55, 0], radius=0.11, color=TERRA)
        bar = Line([-0.55, 0.55, 0], [0.95, 0.55, 0], color=INK, stroke_width=9)
        l1 = label("warns", 0.2, 1.65, 42)
        l2 = label("silent", 4.5, 1.6, 42)
        leader = Line([4.5, 1.35, 0], [4.72, 0.33, 0], color=CONNECT, stroke_width=4)

        self.add(sh, slab, divider, pages, blocks, g1, g2, lamp)
        self.play(GrowFromCenter(top), GrowFromCenter(low), run_time=0.5)
        until(self, "Unity does warn")
        self.play(top.animate.move_to([-1.55, 0.55, 0]), run_time=0.6, rate_func=smooth)
        self.play(Create(bar), FadeIn(l1), run_time=0.6)
        self.play(low.animate.move_to([4.25, -0.1, 0]), run_time=1.3, rate_func=linear)

        hold_past_mid(self)
        self.play(FadeIn(l2), Create(leader), run_time=0.6)
        finish(self)


class B03_HalfRead(Scene):
    def construct(self):
        iso = project_iso()
        sh = floor_shadow(0.0, -1.55)
        slab, divider = project_slab(iso)
        pages, blocks = script_pages(iso), asset_blocks(iso)
        endpt = iso.p(2.9, 0.9, 1.15)
        thread = VMobject(stroke_color=CONNECT, stroke_width=7)
        thread.set_points_smoothly([iso.p(0.9, 1.5, 0.6), np.array([0.1, 2.5, 0.0]), endpt])
        base = VGroup(sh, slab, divider, pages, blocks, thread, Dot(endpt, radius=0.1, color=TERRA))
        # Gate V measures ink-vs-background luminance separation across the whole frame. A pale
        # GHOST veil at 0.92 left almost nothing dark on screen and the beat failed at 0.24
        # (floor 0.30). A DIM scrim reads better anyway — the half is blacked out, not fogged —
        # and the blocks beneath show faintly through at 0.72. Measured 0.34 after the change.
        veil = Polygon(iso.p(2.2, 0, 0.45), iso.p(4.4, 0, 0.45), iso.p(4.4, 2.8, 1.35), iso.p(2.2, 2.8, 1.35),
                       fill_color=DIM, fill_opacity=0.72, stroke_color=INK, stroke_width=4)
        scan = Line(iso.p(0.0, 0.0, 0.5), iso.p(0.0, 2.8, 0.5), color=TERRA, stroke_width=6)
        lbl = label("guess", 4.2, 1.9)
        # a leader that actually reaches the guessed end, with a clear gap at the label end
        leader = Line([3.55, 1.78, 0], np.array(endpt) + np.array([0.26, 0.2, 0.0]),
                      color=CONNECT, stroke_width=4)

        self.add(base)
        self.play(FadeIn(veil), run_time=0.6)
        until(self, "cannot know the name")
        self.play(scan.animate.shift(iso.v(2.2, 0, 0)), run_time=1.2, rate_func=linear)
        self.play(FadeOut(scan), FadeIn(lbl), run_time=0.4)

        hold_past_mid(self)
        self.play(Create(leader), run_time=0.6)
        finish(self)


class B04_WritesIn(Scene):
    def construct(self):
        iso = project_iso()
        sh = floor_shadow(0.0, -1.55)
        slab, divider = project_slab(iso)
        pages = script_pages(iso)
        # the arm reaches DOWN from above, not in from the left: GATE T reads the ink arm as a
        # text run, and a wide one overlaps the slab's bbox by 36%. Taller than wide is not type.
        arm = VGroup(
            Line([0.45, 3.3, 0], [1.7, 2.6, 0], color=INK, stroke_width=8),
            Line([1.7, 2.6, 0], [2.3, 1.75, 0], color=INK, stroke_width=8),
            Rectangle(width=0.5, height=0.3, fill_color=DARK_TOP, fill_opacity=1,
                      stroke_color=INK, stroke_width=3).move_to([2.3, 1.6, 0]))
        # spaced apart: a dense lattice of dark blocks breaks into false "text" blobs under GATE T
        def crook(y, ang):
            b = iso.mcp(2.35, y, 0.45, w=1.15, d=0.8, h=0.55)
            return b.rotate(ang, about_point=iso.p(2.92, y + 0.4, 0.72))
        crooked = VGroup(crook(0.15, 0.2), crook(1.25, -0.24))
        third = crook(2.35, 0.32)
        l1, l2 = label("writes", 4.4, 2.1), label("spring 2026", -4.2, -2.6, 42)

        self.add(sh, slab, divider, pages)
        self.play(FadeIn(arm, shift=np.array([-0.4, 0.3, 0.0])), FadeIn(l2), run_time=0.7)
        until(self, "It put things")
        self.play(LaggedStart(*[FadeIn(b, shift=np.array([0.0, 0.7, 0.0])) for b in crooked], lag_ratio=0.4),
                  FadeIn(l1), run_time=1.2, rate_func=ease_in)

        hold_past_mid(self)
        self.play(FadeIn(third, shift=np.array([0.0, 0.7, 0.0])), run_time=0.6, rate_func=ease_in)
        finish(self)


class B04B_ByHand(Scene):
    def construct(self):
        iso = project_iso()
        sh = floor_shadow(0.0, -1.55)
        slab, divider = project_slab(iso)
        pages = script_pages(iso)
        arm = VGroup(
            Line([-0.6, 3.15, 0], [1.7, 2.6, 0], color=DIM, stroke_width=8),
            Line([1.7, 2.6, 0], [2.3, 1.75, 0], color=DIM, stroke_width=8),
            Rectangle(width=0.5, height=0.3, fill_color=GHOST, fill_opacity=1,
                      stroke_color=DIM, stroke_width=3).move_to([2.3, 1.6, 0]))
        def crook(y, ang):
            b = iso.mcp(2.35, y, 0.45, w=1.15, d=0.8, h=0.55)
            return b.rotate(ang, about_point=iso.p(2.92, y + 0.4, 0.72))
        crooked = VGroup(crook(0.15, 0.2), crook(1.25, -0.24), crook(2.35, 0.32))
        straight = asset_blocks(iso)
        lbl = label("by hand", 4.2, 1.4)

        self.add(sh, slab, divider, pages, arm, crooked)
        self.play(arm.animate.set_opacity(0.25), run_time=0.5)
        until(self, "After that")
        self.play(FadeOut(crooked), run_time=0.5)
        self.play(LaggedStart(*[Create(b) for b in straight], lag_ratio=0.3), FadeIn(lbl), run_time=1.1)

        hold_past_mid(self)
        rail = Line(iso.p(2.2, 0.1, 0.45), iso.p(4.3, 0.1, 0.45), color=DKRAFT, stroke_width=4)
        self.play(Create(rail), run_time=0.5)
        finish(self)


class B05_Checklist(Scene):
    def construct(self):
        iso = Iso(-2.6, -1.3, 0.75)
        sh = floor_shadow(-2.1, -1.5, w=4.0)
        slab, divider = project_slab(iso)
        blocks = asset_blocks(iso)
        sheet, rows = slip(4.0, 0.2, w=2.6, h=3.1, rows=5)
        ticks = VGroup(*[check(3.2, yy, s=0.18) for yy in rows])
        l1, l2 = label("checklist", 4.0, 2.2, 42), label("proposed", 4.0, -1.8, 42)

        self.add(sh, slab, divider, blocks)
        self.play(FadeIn(sheet, shift=np.array([0.3, 0.0, 0.0])), FadeIn(l1), run_time=0.7)
        until(self, "writes down")
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.18), run_time=1.3)

        hold_past_mid(self)
        self.play(FadeIn(l2), GrowFromCenter(Dot([4.0, -1.35, 0], radius=0.08, color=TERRA)), run_time=0.5)
        finish(self)


class B05B_ReadOnly(Scene):
    def construct(self):
        iso = Iso(-2.6, -1.3, 0.75)
        sh = floor_shadow(-2.1, -1.5, w=4.0)
        slab, divider = project_slab(iso)
        blocks = asset_blocks(iso)
        sheet, rows = slip(4.0, 0.2, w=2.6, h=3.1, rows=5)
        ticks = VGroup(*[check(3.2, yy, s=0.18) for yy in rows[:4]])
        thread = Line(iso.p(1.0, 1.0, 0.5), [2.7, rows[4], 0], color=CONNECT, stroke_width=5)
        cross = VGroup(Line([3.0, rows[4] + 0.17, 0], [3.36, rows[4] - 0.17, 0], color=INK, stroke_width=7),
                       Line([3.0, rows[4] - 0.17, 0], [3.36, rows[4] + 0.17, 0], color=INK, stroke_width=7))
        # a large ink-outlined padlock: small objects in dark kraft read as sub-floor text (GATE T)
        lock_body = Rectangle(width=1.3, height=1.0, fill_color=BOX_TOP, fill_opacity=1,
                              stroke_color=INK, stroke_width=4).move_to([-1.1, 2.0, 0])
        shackle = Arc(radius=0.42, start_angle=0, angle=PI, stroke_color=INK,
                      stroke_width=5).move_to([-1.1, 2.71, 0])
        keyhole = Dot([-1.1, 2.0, 0], radius=0.12, color=INK)
        l1, l2 = label("marked", 4.6, -1.8, 42), label("read only", -3.9, 2.1, 42)

        self.add(sh, slab, divider, blocks, sheet, ticks)
        self.play(Create(thread), run_time=0.8, rate_func=linear)
        until(self, "marks what")
        self.play(Create(cross), FadeIn(l1), run_time=0.7)

        hold_past_mid(self)
        self.play(Create(lock_body), Create(shackle), GrowFromCenter(keyhole), FadeIn(l2), run_time=1.0)
        finish(self)


class B06_Fixture(Scene):
    def construct(self):
        iso = Iso(-3.9, -1.2, 0.6)
        sh = floor_shadow(-3.3, -1.45, w=3.0, h=0.8)
        slab, divider = project_slab(iso)
        sheet, rows = slip(2.6, 0.2, w=2.6, h=3.1, rows=5)
        ticks = VGroup(*[check(1.8, rows[i], s=0.18) for i in (0, 4)])
        # the three planted errors are contiguous, so one bracket can count them
        crosses = VGroup(*[VGroup(
            Line([1.62, rows[i] + 0.17, 0], [1.98, rows[i] - 0.17, 0], color=INK, stroke_width=7),
            Line([1.62, rows[i] - 0.17, 0], [1.98, rows[i] + 0.17, 0], color=INK, stroke_width=7))
            for i in (1, 2, 3)])
        ytop, ybot = rows[1] + 0.22, rows[3] - 0.22
        bracket = VGroup(Line([1.02, ytop, 0], [1.02, ybot, 0], color=CONNECT, stroke_width=4),
                         Line([1.02, ytop, 0], [1.22, ytop, 0], color=CONNECT, stroke_width=4),
                         Line([1.02, ybot, 0], [1.22, ybot, 0], color=CONNECT, stroke_width=4))
        n3 = label("3", 0.52, (ytop + ybot) / 2, 48)
        l1, l2 = label("test project", -3.3, -2.4, 42), label("proposed", 2.6, -1.9, 42)

        self.add(sh, slab, divider, sheet, ticks)
        self.play(FadeIn(l1), run_time=0.4)
        until(self, "three wrong names")
        self.play(LaggedStart(*[Create(c) for c in crosses], lag_ratio=0.25), run_time=1.2)
        self.play(FadeIn(l2), run_time=0.4)

        hold_past_mid(self)
        self.play(Create(bracket), FadeIn(n3), run_time=0.7)
        finish(self)


class B07_FalseAlarm(Scene):
    def construct(self):
        plinth = Rectangle(width=8.0, height=0.26, fill_color=BOX_R, fill_opacity=1,
                           stroke_color=INK, stroke_width=4).move_to([0.3, -2.1, 0])
        axis = Line([-3.9, -1.97, 0], [-3.9, 1.9, 0], color=DIM, stroke_width=4)
        bars = bar_stack(-2.6, -1.97, [0.8, 0.7, 0.5])
        # the cross lands on a row of the checklist, so it reads as a good line wrongly flagged
        row = Rectangle(width=2.0, height=0.9, fill_color=PAGE_TOP, fill_opacity=1,
                        stroke_color=INK, stroke_width=4).move_to([2.4, 1.1, 0])
        good = check(2.4, 1.1, s=0.22)
        cross = VGroup(Line([2.18, 1.32, 0], [2.62, 0.88, 0], color=INK, stroke_width=7),
                       Line([2.18, 0.88, 0], [2.62, 1.32, 0], color=INK, stroke_width=7))
        l1, l2 = label("false alarms", -2.6, -2.75, 42), label("proposed", 2.4, -0.1, 42)

        self.add(plinth, axis, row, good)
        self.play(FadeIn(l1), run_time=0.4)
        until(self, "not always")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=1.1)

        hold_past_mid(self)
        self.play(FadeOut(good), Create(cross), FadeIn(l2), run_time=0.7)
        finish(self)


class B07B_TwoNumbers(Scene):
    def construct(self):
        plinth = Rectangle(width=8.4, height=0.26, fill_color=BOX_R, fill_opacity=1,
                           stroke_color=INK, stroke_width=4).move_to([0.5, -2.1, 0])
        axis = Line([-3.9, -1.97, 0], [-3.9, 1.9, 0], color=DIM, stroke_width=4)
        bars1 = bar_stack(-2.6, -1.97, [0.8, 0.7, 0.5])
        bars2 = bar_stack(0.5, -1.97, [1.2, 0.9, 0.7])
        bars3 = bar_stack(3.4, -1.97, [0.6, 0.45])
        spark = Dot([0.5, 1.05, 0], radius=0.09, color=TERRA)
        # spread apart: at the first pass these three ran together into "false alarmscaught"
        l1 = label("false alarms", -2.6, -2.75, 42)
        l2 = label("caught", 0.5, -2.75, 42)
        l3 = label("cannot tell", 3.4, -2.75, 42)

        self.add(plinth, axis, bars1, l1)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars2], lag_ratio=0.2),
                  FadeIn(l2), run_time=1.1)
        until(self, "cannot determine")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars3], lag_ratio=0.2),
                  FadeIn(l3), run_time=0.9)

        hold_past_mid(self)
        self.play(GrowFromCenter(spark), run_time=0.5)
        finish(self)


class B08_HaveTray(Scene):
    def construct(self):
        iso = Iso(-2.4, -1.6, 0.9)
        sh = floor_shadow(-2.3, -1.9, w=4.2, h=0.9)
        back, front = iso.open_box(0, 0, 0, 2.6, 2.4, 0.6)
        pg = iso.page(0.3, 0.4, 0.05)
        blk = iso.mcp(1.3, 1.3, 0.05, w=0.9, d=0.7, h=0.45)
        sw = glow(-2.4, 0.2, s=1.0)
        lbl = label("have", -2.3, -2.6)

        self.add(sh)
        self.play(FadeIn(back), FadeIn(front), run_time=0.6)
        until(self, "I shipped")
        self.play(FadeIn(pg, shift=np.array([0.0, 0.5, 0.0])), run_time=0.5, rate_func=ease_in)
        self.play(FadeIn(blk, shift=np.array([0.0, 0.5, 0.0])), FadeIn(lbl), run_time=0.6, rate_func=ease_in)

        hold_past_mid(self)
        self.play(Create(sw), run_time=0.9)
        finish(self)


class B08B_NewTray(Scene):
    def construct(self):
        iso = Iso(-2.4, -1.6, 0.9)
        iso2 = Iso(2.0, -1.6, 0.9)
        sh = floor_shadow(-2.3, -1.9, w=4.2, h=0.9)
        back, front = iso.open_box(0, 0, 0, 2.6, 2.4, 0.6)
        pg = iso.page(0.3, 0.4, 0.05)
        blk = iso.mcp(1.3, 1.3, 0.05, w=0.9, d=0.7, h=0.45)
        sw = glow(-2.4, 0.2, s=1.0)
        l_have = label("have", -2.3, -2.6)

        # the empty tray is the same object with no fill, not a flat lozenge
        gb, gf = iso2.open_box(0, 0, 0, 2.6, 2.4, 0.6)
        empty = VGroup(*[m for m in list(gb) + list(gf)])
        for m in empty:
            m.set_fill(opacity=0)
            m.set_stroke(color=DIM, width=4)
        ghost_slip = Rectangle(width=0.9, height=1.2, stroke_color=GHOST, stroke_width=4,
                               fill_opacity=0).move_to([2.0, 0.1, 0])
        ghost_bars = VGroup(*[Rectangle(width=0.28, height=h, stroke_color=GHOST, stroke_width=4,
                                        fill_opacity=0).move_to([3.3 + 0.4 * i, -0.5 + h / 2, 0])
                              for i, h in enumerate((0.6, 1.0, 0.45))])
        l_new = label("new", 3.0, -2.6)

        self.add(sh, back, front, pg, blk, sw, l_have)
        self.play(Create(empty), FadeIn(l_new), run_time=0.9)
        until(self, "never done")
        self.play(Create(ghost_slip), run_time=0.6)

        hold_past_mid(self)
        self.play(LaggedStart(*[Create(b) for b in ghost_bars], lag_ratio=0.2), run_time=0.8)
        finish(self)
