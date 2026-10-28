"""Remnix Agent pitch — scene bodies. build_scenes.py pastes this AFTER the two
show-tell kits (iso_kit.py + iso_originals_25.py) to make scenes.py.

One drawing per beat, labels beside objects, ink type >= 32, terracotta only for
dots and lights. `gplay` keeps every animation off the clip midpoint (GATE T and
Gate V sample there); `until` waits for the spoken phrase; `finish` holds to the
end of the measured audio.
"""

_HERE = _os.path.dirname(_os.path.abspath(__file__))
CONNECT = "#9C8462"   # deep kraft for cables (ink cables fuse with what they join)


def _bid(scene):
    return type(scene).__name__.split("_")[0]


def gplay(scene, *anims, run_time=0.8):
    """Play, but never across the clip midpoint (±0.3 s)."""
    mid = _TARGET.get(_bid(scene), 10) / 2
    now = _elapsed(scene)
    if now < mid + 0.3 and now + run_time > mid - 0.3:
        scene.wait(max(0.01, mid + 0.35 - now))
    scene.play(*anims, run_time=run_time)


def lab(s, x, y, size=40, bold=False):
    return T(s, size, bold=bold).move_to([x, y, 0])


def shadow(x, y, w=3.2, h=0.6):
    return Ellipse(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def card(x, y, w, h):
    """A borderless white card with a kraft offset (text may sit on it: there is no outline)."""
    sh = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.14, y - 0.14, 0])
    face = Rectangle(width=w, height=h, fill_color="#FFFFFF", fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    return VGroup(sh, face)


def screenshot(path, width, x, y):
    try:
        img = ImageMobject(path)
        img.width = width
        img.move_to([x, y, 0])
        return img
    except Exception:          # Gate A's sandbox has no pantry/; a stand-in keeps the check moving
        return Rectangle(width=width, height=width * 460 / 1600, fill_color=DARK_TOP, fill_opacity=1,
                         stroke_width=0).move_to([x, y, 0])


# ── B00 · what exists: the real Money Map screenshot ─────────────────────────────
class B00_MoneyMap(Scene):
    def construct(self):
        w = 12.2
        h = w * 460 / 1600
        img = screenshot(_os.path.join(_HERE, "pantry", "money-map-2026-10-14-top.png"), w, 0, 0.95)
        frame = Rectangle(width=w + 0.1, height=h + 0.1, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([0, 0.95, 0])
        sh = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([0.14, 0.81, 0])
        name = lab("Money Map", -4.0, -1.9, 52, bold=True)
        tag = lab("real screenshot · 2026-10-14", 2.8, -1.9, 40)
        dot = Dot([-0.55, -1.9, 0], radius=0.09, color=TERRA)
        gplay(self, FadeIn(sh), FadeIn(img, shift=UP * 0.3), Create(frame), run_time=1.0)
        gplay(self, FadeIn(name), run_time=0.5)
        gplay(self, FadeIn(tag), GrowFromCenter(dot), run_time=0.5)
        until(self, "It compares")
        under = Line([-6.0, -2.6, 0], [6.0, -2.6, 0], color=GHOST, stroke_width=6)
        gplay(self, Create(under), run_time=0.8)
        finish(self)


# ── BPLAIN · the simple version: fees eat part of the money; Remnix shows its work ──
class BPLAIN_Simple(Scene):
    def construct(self):
        iso = Iso(-3.9, -1.6, 1.0)
        bills = [iso.box(0, 0, 0.32 * i, 2.2, 1.3, 0.26, PAGE_TOP, PAGE_L, PAGE_R) for i in range(6)]
        for i, bl in enumerate(bills):
            bl.set_z_index(i)
        amount = lab("$500", -3.5, 2.7, 64, bold=True)
        gplay(self, LaggedStart(*[FadeIn(bl, shift=DOWN * 0.2) for bl in bills], lag_ratio=0.15),
              FadeIn(amount), run_time=1.0)
        tray_iso = Iso(-0.2, -1.5, 0.8)
        tb, tf = tray_iso.open_box(-0.9, -0.9, 0, 1.8, 1.8, 0.5)
        fees = lab("fees", -0.2, -2.75)
        until(self, "part of it disappears")
        gplay(self, FadeIn(VGroup(tb, tf)), FadeIn(fees), run_time=0.5)
        for bl in bills[-2:][::-1]:
            gplay(self, bl.animate.shift(RIGHT * 3.6 + DOWN * 1.0).scale(0.55), run_time=0.6)
        until(self, "like a calculator that shows its work")
        receipt = paper(4.3, 0.4, w=2.4, h=3.2)
        rlines = scribbles_on(receipt, n=5)
        rl = lab("shows its work", 4.3, -1.75)
        gplay(self, FadeIn(receipt, shift=UP * 0.3), FadeIn(rl), run_time=0.5)
        gplay(self, Create(rlines), run_time=1.0)
        finish(self)


# ── B02 · Remnix, proposed ───────────────────────────────────────────────────────
def remnix_crate(x=-1.6, y=-0.1, h=3.2):
    return make_original("context-crate", height=h, x=x, y=y)


class B02_Remnix(Scene):
    def construct(self):
        crate = remnix_crate()
        sh = shadow(-1.6, -1.75, 4.4, 0.7)
        name = lab("Remnix", 3.6, 0.6, 60, bold=True)
        gplay(self, FadeIn(sh), FadeIn(crate, shift=DOWN * 0.5), run_time=1.0)
        until(self, "So I will build Remnix")
        gplay(self, FadeIn(name), run_time=0.5)
        until(self, "None of it exists yet")
        note = lab("proposed · not built", 3.6, -0.4, 40)
        mark = Dot([1.1, -0.4, 0], radius=0.09, color=TERRA)
        gplay(self, FadeIn(note), GrowFromCenter(mark), run_time=0.5)
        finish(self)


# ── B03 · the data: PostgreSQL tables + the FastAPI endpoint ─────────────────
class B03_Data(Scene):
    def construct(self):
        drawers = make_original("memory-drawers", height=3.2, x=-3.6, y=0.0)
        gplay(self, FadeIn(drawers, shift=UP * 0.3), run_time=0.6)
        tables = [lab("quotes", -0.9, 1.1), lab("fx_rates", -0.9, 0.2), lab("snapshots", -0.9, -0.7)]
        db = lab("PostgreSQL", -3.6, -2.35, 40, bold=True)
        gplay(self, LaggedStart(*[FadeIn(t) for t in tables], lag_ratio=0.4), FadeIn(db), run_time=1.2)
        until(self, "A Fast API endpoint")
        server = make_original("server-tower", height=2.6, x=4.0, y=0.2)
        api = lab("POST /ask", 4.0, -1.85, 44, bold=True)
        cable = Line([0.6, 0.2, 0], [2.6, 0.2, 0], color=CONNECT, stroke_width=8)
        gplay(self, FadeIn(server, shift=UP * 0.3), FadeIn(api), run_time=0.6)
        gplay(self, Create(cable), run_time=0.6)
        finish(self)


# ── B04 · the agent: Claude picks get_quotes or compute_cost; the answer cites rows ──
class B04_Tools(Scene):
    def construct(self):
        ws = make_original("agent-workstation", height=2.6, x=-4.4, y=0.2)
        l0 = lab("Claude", -4.4, -1.75)
        self.add(ws, l0)
        t1 = make_original("tool-block", height=1.6, x=-1.1, y=1.3)
        t2 = make_original("tool-block", height=1.6, x=-1.1, y=-1.0)
        n1 = lab("get_quotes", 1.45, 1.3, 40)
        n2 = lab("compute_cost", 1.65, -1.0, 40)
        gplay(self, FadeIn(t1, shift=UP * 0.2), FadeIn(n1), run_time=0.5)
        gplay(self, FadeIn(t2, shift=UP * 0.2), FadeIn(n2), run_time=0.5)
        until(self, "does the math in Python")
        gplay(self, t2.parts["tool"].animate.shift(t2.action_vectors["tool"]), run_time=0.6)
        until(self, "The answer will come back")
        ans = paper(5.3, 0.3, w=1.6, h=2.2)
        alines = scribbles_on(ans, n=3)
        ids = lab("row IDs", 5.3, -1.4)
        gplay(self, FadeIn(ans, shift=LEFT * 0.3), FadeIn(ids), run_time=0.5)
        gplay(self, Create(alines), run_time=0.6)
        finish(self)


# ── B05 · the prompt contract, shown on a CONSTRUCTED answer card ────────────────
class B05_Answer(Scene):
    def construct(self):
        stamp = lab("CONSTRUCTED", -1.5, 2.85, 60, bold=True)
        sub = lab("mock-up, not real output", -1.5, 2.15, 36)
        self.add(stamp, sub)
        c = card(-1.5, -0.55, 5.2, 3.4)
        gplay(self, FadeIn(c, shift=UP * 0.3), run_time=0.6)
        hero = T("$7.54", 120, bold=True).move_to([-1.5, -0.05, 0])
        math = VGroup(scribble(-3.6, -1.3, 4.2), scribble(-3.6, -1.75, 2.8))
        gplay(self, FadeIn(hero), Create(math), run_time=0.8)
        until(self, "its number is real")
        tag = Rectangle(width=0.5, height=1.0, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([1.45, -0.55, 0])
        hole = Dot([1.45, -0.25, 0], radius=0.08, color=TERRA)
        src = lab("Money Map · Oct 14", 4.1, -0.55, 36)
        gplay(self, FadeIn(tag, shift=LEFT * 0.3), GrowFromCenter(hole), FadeIn(src), run_time=0.6)
        finish(self)


# ── B06 · the stablecoin sandwich: three cost layers ─────────────────────────────
class B06_Sandwich(Scene):
    def construct(self):
        iso = Iso(-1.4, -2.0, 1.0)
        layers, labels, dots = [], [], []
        specs = [("buy", 0.0, (BOX_TOP, BOX_L, BOX_R)), ("send", 0.85, ("#C9C4BB", BAR1, "#6F737A")),
                 ("sell", 1.7, (BOX_TOP, BOX_L, BOX_R))]
        for i, (word, z, (t, l, r)) in enumerate(specs):
            slab = iso.box(0, 0, z, 2.6, 2.6, 0.5, t, l, r)
            layers.append(slab)
            labels.append(lab(word, 2.4, -1.05 + z))
            dots.append(Dot(iso.p(2.6 * 0.5, 0, z + 0.25), radius=0.08, color=TERRA))
        gplay(self, FadeIn(layers[0], shift=DOWN * 0.4), FadeIn(labels[0]), GrowFromCenter(dots[0]), run_time=0.7)
        until(self, "cross a blockchain")
        gplay(self, FadeIn(layers[1], shift=DOWN * 0.4), FadeIn(labels[1]), GrowFromCenter(dots[1]), run_time=0.7)
        until(self, "then become pesos")
        gplay(self, FadeIn(layers[2], shift=DOWN * 0.4), FadeIn(labels[2]), GrowFromCenter(dots[2]), run_time=0.7)
        finish(self)


# ── B07 · three alternatives ─────────────────────────────────────────────────────
class B07_Alternatives(Scene):
    def construct(self):
        trays, names, slots = [], [], []
        for i, (x, word) in enumerate([(-4.4, "Wise"), (0.0, "Monito"), (4.4, "World Bank")]):
            iso = Iso(x, -0.9, 0.85)
            back, front = iso.open_box(-1.1, -1.1, 0, 2.2, 2.2, 0.8)
            block = iso.box(-0.75, 0.15, 0, 0.6, 0.6, 0.55)
            block2 = iso.box(0.15, 0.15, 0, 0.6, 0.6, 0.55)
            trays.append(VGroup(back, block, block2, front))
            names.append(lab(word, x, -2.35))
            if i < 2:
                slots.append(iso.quad([(-0.75, -0.75, 0.01), (-0.15, -0.75, 0.01), (-0.15, -0.15, 0.01), (-0.75, -0.15, 0.01)],
                                      "#E8E2D6", stroke=BAR1, sw=3))
        gplay(self, LaggedStart(*[AnimationGroup(FadeIn(t, shift=UP * 0.3), FadeIn(n)) for t, n in zip(trays, names)],
                                lag_ratio=0.35), run_time=1.6)
        until(self, "didn't include stablecoin routes")
        stack = VGroup(*[Iso(0, 2.0, 0.55).box(0, 0, z, 1.2, 1.2, 0.3, *c) for z, c in
                         [(0, (BOX_TOP, BOX_L, BOX_R)), (0.38, ("#C9C4BB", BAR1, "#6F737A")), (0.76, (BOX_TOP, BOX_L, BOX_R))]])
        gplay(self, FadeIn(stack, shift=DOWN * 0.3), *[Create(s) for s in slots], run_time=0.8)
        until(self, "newest data")
        tag = paper(5.45, 1.25, w=0.7, h=0.9, tilt=-0.12)
        pin = Dot([5.4, 1.55, 0], radius=0.08, color=TERRA)
        gplay(self, FadeIn(tag, shift=DOWN * 0.4), GrowFromCenter(pin), run_time=0.6)
        finish(self)


# ── B08 · the reviewer's first sixty seconds ─────────────────────────────────────
class B08_Reviewer(Scene):
    def construct(self):
        readme = paper(-4.5, 0.5, w=2.4, h=3.0)
        rlines = scribbles_on(readme, n=4)
        l1 = lab("README", -4.5, -1.75)
        gplay(self, FadeIn(readme, shift=UP * 0.3), FadeIn(l1), run_time=0.6)
        gplay(self, Create(rlines), run_time=0.8)
        term = RoundedRectangle(width=3.2, height=2.3, corner_radius=0.12, fill_color="#16130F", fill_opacity=1,
                                stroke_color=INK, stroke_width=4).move_to([0, 0.5, 0])
        prompt = Dot([-1.1, 1.05, 0], radius=0.1, color=TERRA)
        l2 = lab("60 s", 0, 2.35, 48, bold=True)
        gplay(self, FadeIn(term), GrowFromCenter(prompt), FadeIn(l2), run_time=0.6)
        drawers = make_original("memory-drawers", height=2.6, x=4.4, y=0.3)
        l3 = lab("PostgreSQL", 4.4, -1.75)
        until(self, "run one command")
        c1 = Line([-3.1, 0.5, 0], [-1.85, 0.5, 0], color=CONNECT, stroke_width=8)
        gplay(self, Create(c1), FadeIn(drawers), FadeIn(l3), run_time=0.7)
        until(self, "trace every number")
        c2 = Line([1.85, 0.5, 0], [3.2, 0.5, 0], color=CONNECT, stroke_width=8)
        gplay(self, Create(c2), run_time=0.5)
        gplay(self, drawers.parts["drawer"].animate.shift(drawers.action_vectors["drawer"]), run_time=0.6)
        finish(self)


# ── B09 · the first piece, and how you'd know it ran ─────────────────────────────
class B09_FirstRun(Scene):
    def construct(self):
        drawers = make_original("memory-drawers", height=2.6, x=-4.3, y=0.2)
        l0 = lab("step 1", -4.3, 2.45, 48, bold=True)
        self.add(drawers, l0)
        rec = paper(-2.4, 2.3, w=0.8, h=0.6)
        gplay(self, drawers.parts["drawer"].animate.shift(drawers.action_vectors["drawer"]), run_time=0.6)
        gplay(self, FadeIn(rec, shift=DOWN * 0.3), run_time=0.4)
        gplay(self, rec.animate.move_to([-3.6, 0.0, 0]).scale(0.5), run_time=0.6)
        gplay(self, FadeOut(rec), drawers.parts["drawer"].animate.shift(-drawers.action_vectors["drawer"]), run_time=0.6)
        a = paper(0.4, 0.5, w=2.2, h=2.6)
        b = paper(4.4, 0.5, w=2.2, h=2.6)
        la, lb = lab("answer", 0.4, -1.55), lab("Money Map", 4.4, -1.55)
        sa = scribbles_on(a, n=3)
        sb = scribbles_on(b, n=3)
        gplay(self, FadeIn(a, shift=UP * 0.3), FadeIn(b, shift=UP * 0.3), FadeIn(la), FadeIn(lb), run_time=0.7)
        gplay(self, Create(sa), Create(sb), run_time=0.9)
        until(self, "the total matches")
        ok = check(2.4, 0.5, 0.32)
        how = lab("how you'd know", 2.4, -2.45, 38)
        gplay(self, Create(ok), FadeIn(how), run_time=0.6)
        finish(self)


# ── B10 · the test set and the wrong-answer log ──────────────────────────────────
class B10_TestSet(Scene):
    def construct(self):
        scan = make_original("checkpoint-scanner", height=3.0, x=-1.4, y=-0.5)
        self.add(scan)
        twenty = T("20", 96, bold=True).move_to([-5.0, 1.9, 0])
        q = lab("questions", -5.0, 0.9)
        gplay(self, FadeIn(twenty), FadeIn(q), run_time=0.5)
        light = Dot([-1.0, 1.15, 0], radius=0.1, color=TERRA)
        gplay(self, GrowFromCenter(light), scan.parts["parcel"].animate.shift(scan.action_vectors["parcel"]), run_time=1.2)
        until(self, "each wrong answer")
        binder = make_original("evidence-binder", height=1.7, x=4.3, y=-0.8)
        l2 = lab("log", 4.3, -2.2)
        gplay(self, FadeIn(binder, shift=UP * 0.3), FadeIn(l2), run_time=0.6)
        gplay(self, binder.parts["cover"].animate.shift(binder.action_vectors["cover"]), run_time=0.6)
        finish(self)


# ── B11 · what's out ─────────────────────────────────────────────────────────────
class B11_Out(Scene):
    def construct(self):
        gate = make_original("permission-gate", height=3.0, x=0.2, y=-0.2)
        gate.parts["barrier"].shift(gate.action_vectors["barrier"])      # start raised
        iso = Iso(-4.6, -1.3, 0.9)
        parcel = iso.box(0, 0, 0, 1.0, 1.0, 0.9)
        self.add(gate, parcel)
        l1 = lab("no transfers", 0.2, -2.45)
        gplay(self, gate.parts["barrier"].animate.shift(-gate.action_vectors["barrier"]), FadeIn(l1), run_time=0.6)
        gplay(self, parcel.animate.shift(RIGHT * 1.4), run_time=0.8)
        until(self, "for one corridor only")
        route = Line([3.1, 1.3, 0], [6.0, 1.3, 0], color=INK, stroke_width=6)
        tip = Dot([6.0, 1.3, 0], radius=0.1, color=TERRA)
        l2 = lab("US → MX", 4.55, 2.0, 44, bold=True)
        gplay(self, Create(route), GrowFromCenter(tip), FadeIn(l2), run_time=0.7)
        finish(self)


# ── B12 · the risk: live prices go stale; a dated snapshot fixes the test set ────
class B12_Risk(Scene):
    def construct(self):
        page = paper(-4.4, 0.6, w=2.4, h=2.8)
        plines = scribbles_on(page, n=3)
        l1 = lab("live", -4.4, -1.4)
        self.add(page, l1)
        gplay(self, Create(plines), run_time=0.6)
        p1 = T("$7.42", 72, bold=True).move_to([-1.0, 0.6, 0])
        gplay(self, FadeIn(p1), run_time=0.4)
        until(self, "eight ninety-nine")
        p2 = T("$8.99", 72, bold=True).move_to([-1.0, 0.6, 0])
        gplay(self, FadeOut(p1), FadeIn(p2), run_time=0.4)
        vault = make_original("secure-vault", height=2.8, x=4.2, y=0.4)
        vault.parts["lock-bar"].shift(vault.action_vectors["lock-bar"])  # open
        l2 = lab("snapshot", 4.2, -1.55)
        gplay(self, FadeIn(vault), FadeIn(l2), run_time=0.6)
        until(self, "freeze a dated snapshot")
        snap = paper(-4.4, 0.6, w=2.4, h=2.8)
        self.add(snap)
        gplay(self, snap.animate.move_to([4.0, 0.3, 0]).scale(0.3), run_time=0.7)
        gplay(self, vault.parts["lock-bar"].animate.shift(-vault.action_vectors["lock-bar"]), run_time=0.4)
        finish(self)


# ── B13 · what it will prove, and the evidence that will back it ─────────────
class B13_Proves(Scene):
    def construct(self):
        desk = make_original("review-desk", height=2.8, x=-2.0, y=0.0)
        desk.parts["evidence"].shift(-desk.action_vectors["evidence"])   # start off the desk
        self.add(desk)
        l1 = lab("test scores", -2.0, -2.2)
        gplay(self, desk.parts["evidence"].animate.shift(desk.action_vectors["evidence"]), FadeIn(l1), run_time=0.9)
        plan = lab("planned", 0.9, 1.7, 40)
        mark = Dot([-0.15, 1.7, 0], radius=0.09, color=TERRA)
        gplay(self, FadeIn(plan), GrowFromCenter(mark), run_time=0.4)
        until(self, "the wrong-answer log")
        binder = make_original("evidence-binder", height=1.7, x=3.9, y=-0.6)
        l2 = lab("wrong-answer log", 3.9, -2.2)
        gplay(self, FadeIn(binder, shift=UP * 0.3), FadeIn(l2), run_time=0.6)
        finish(self)


# ── B14 · skills I have vs skills that are new ───────────────────────────────────
class B14_Skills(Scene):
    def construct(self):
        li, ri = Iso(-3.6, -0.5, 0.9), Iso(3.6, -0.5, 0.9)
        lb, lf = li.open_box(-1.6, -1.6, 0, 3.2, 3.2, 0.8)
        rb, rf = ri.open_box(-1.6, -1.6, 0, 3.2, 3.2, 0.8)
        have = VGroup(*[li.box(x0, y0, 0, 0.8, 0.8, 0.7) for x0, y0 in [(-1.2, 0.4), (0.0, 0.4), (-1.2, -0.8)]])
        mm = li.page(0.1, -1.3, 0)
        l1, l2 = lab("have", -3.6, -2.55), lab("new", 3.6, -2.55)
        gplay(self, FadeIn(VGroup(lb, have, mm, lf), shift=UP * 0.3), FadeIn(l1), run_time=0.8)
        gplay(self, FadeIn(VGroup(rb, rf), shift=UP * 0.3), FadeIn(l2), run_time=0.7)
        until(self, "New to me")
        spots = [(-1.3, 0.5), (0.2, 0.5), (-1.3, -0.6), (0.2, -0.6), (-0.55, -1.45)]
        pages = [ri.page(x0, y0, 0.02, w=0.9, d=0.75) for x0, y0 in spots]
        for p in pages:
            p.set_z_index(1)
            gplay(self, FadeIn(p, shift=DOWN * 0.3), run_time=0.45)
        finish(self)


# ── B15 · exists vs will exist ───────────────────────────────────────────────────
class B15_ExistsWill(Scene):
    def construct(self):
        mm = paper(-3.8, 0.5, w=2.6, h=3.0)
        mml = scribbles_on(mm, n=4)
        crate = remnix_crate(x=2.6, y=0.4, h=2.6)
        l1, l2 = lab("exists", -3.8, -1.75), lab("will exist", 2.6, -1.75)
        self.add(mm, mml, crate, l1, l2)
        ok = check(-1.75, 1.75, 0.3)
        gplay(self, Create(ok), run_time=0.5)
        until(self, "Everything else")
        binder = make_original("evidence-binder", height=1.2, x=5.3, y=-0.5)
        gplay(self, FadeIn(binder, shift=UP * 0.3), run_time=0.5)
        finish(self)


# ── BOUT · the student's own close (no instructor handle) ────────────────────────
class BOUT_Close(Scene):
    def construct(self):
        t1 = lab("Remnix Agent", 0, 1.0, 84, bold=True)
        t2 = lab("Revan C", 0, -0.05, 52)
        t3 = lab("synthetic voice · pitch, not a build", 0, -0.95, 36)
        self.add(t1, t2, t3)
        d = Dot([0, -1.75, 0], radius=0.1, color=TERRA)
        gplay(self, GrowFromCenter(d), run_time=0.4)
        finish(self)
