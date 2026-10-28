# ═════════════════════════════ ELECTRICITY SUPPLIER CHECK — reel scenes ═════════════════════════════
# The reel's own drawing code. build_scenes.py pastes the toolkit's show-tell iso kit
# (skills/make/show-tell/templates/iso_kit.py) ABOVE this file to make scenes.py; Gate A copies
# only scenes.py, so nothing here is imported.
#
# One class per body beat, one drawing per class; the narration in beat_sheet.json carries the
# explanation. The cast recurs: the bill, the coin, the "$" slip, the tool box, the dated rate
# table, the verifier gate, the eval report. Constructed visuals carry an on-screen tag.

try:
    _WORDS = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "mp3", "words.json")))["beats"]
except Exception:
    _WORDS = {}

DKRAFT = "#917A55"   # small-object outline (dark kraft)
CABLE = "#9C8462"    # connector / belt edges
BELT = "#E7E3DA"     # within 28 of the stage, so Gate V doesn't count it as ink
MID_PAD = 0.32       # keep every animation this far from the clip midpoint (GATE T / Gate V sample it)


def _bid(scene):
    return type(scene).__name__.split("_")[0]


def _norm(w):
    return w.strip(".,:;!?'\"").lower()


def at(scene, phrase, lead=0.15):
    """Wait until `phrase` starts (word clock in mp3/words.json); falls back to the kit's until()."""
    toks = _WORDS.get(_bid(scene), [])
    want = [_norm(w) for w in phrase.split()]
    have = [_norm(t.get("text", "")) for t in toks]
    for i in range(len(have) - len(want) + 1):
        if have[i:i + len(want)] == want:
            gap = toks[i]["startFrame"] / 24.0 - lead - _elapsed(scene)
            if gap > 0.04:
                scene.wait(gap)
            return
    until(scene, phrase, lead)


def play(scene, *anims, run_time=0.8, **kw):
    """scene.play, but never across the clip midpoint: wait past it first."""
    target = _TARGET.get(_bid(scene), 0)
    if target:
        mid, now = target / 2.0, _elapsed(scene)
        if now < mid + MID_PAD and now + run_time > mid - MID_PAD:
            scene.wait(max(0.02, mid + MID_PAD - now))
    scene.play(*anims, run_time=run_time, **kw)


def done(scene):
    target = _TARGET.get(_bid(scene), 0)
    gap = (target - 0.06 - _elapsed(scene)) if target else 1.0
    if gap > 0.02:
        scene.wait(gap)


# ───────────────────────────── the cast ─────────────────────────────
def tag(text):
    """Top-right honesty tag (CONSTRUCTED / PROPOSED / not run yet): ink text, one terracotta dot."""
    t = T(text, 34)
    t.move_to([6.1 - t.width / 2, 3.0, 0])
    d = Dot([6.1 - t.width - 0.25, 3.0, 0], radius=0.07, color=TERRA)
    return VGroup(d, t)


def caption(*lines, y=-2.9):
    g = VGroup(*[T(s, 32) for s in lines]).arrange(DOWN, buff=0.1)
    g.move_to([0, y, 0])
    return g


def label(text, x, y, size=40):
    return T(text, size).move_to([x, y, 0])


def bill(x, y, s=1.0):
    """The hero object: a drawn bill. Grey header band, scribbled rows, no amounts, no logo."""
    w, h = 2.5 * s, 3.2 * s
    pg = paper(x, y, w, h)
    band = Rectangle(width=w - 0.5 * s, height=0.3 * s, fill_color=BAR1, fill_opacity=1,
                     stroke_width=0).move_to([x, y + h / 2 - 0.42 * s, 0])
    ink = INK if s >= 0.7 else BAR1
    sw = 4 if s >= 0.7 else 3
    rows = VGroup(*[scribble(x - w / 2 + 0.5 * s, y + h / 2 - 0.95 * s - i * 0.45 * s,
                             (w - 0.85 * s) * (1.0 if i % 2 == 0 else 0.68), amp=0.05 * s, color=ink, sw=sw)
                    for i in range(5)])
    g = VGroup(pg, band, rows)
    g.mark = np.array([x - w / 2 + 0.28 * s, y + h / 2 - 0.95 * s - 2 * 0.45 * s, 0.0])
    return g


def coin(x, y, r=0.3):
    sh = Circle(radius=r, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.07, y - 0.07, 0])
    c = Circle(radius=r, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(sh, c)


def slip(x, y, text="$", w=1.3, h=0.85, size=52):
    card = RoundedRectangle(width=w, height=h, corner_radius=0.12, fill_color=CARD, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(card, T(text, size).move_to([x, y, 0]))


def sheet(x, y, w=2.2, h=2.8, rows=3):
    """A table page (the dated rate table / tariff sheet): grey header, grey row blocks with gaps."""
    pg = paper(x, y, w, h)
    head = Rectangle(width=w - 0.5, height=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x, y + h / 2 - 0.4, 0])
    cells = VGroup()
    for i in range(rows):
        yy = y + h / 2 - 0.95 - i * ((h - 1.3) / max(1, rows - 1) if rows > 1 else 0)
        cells.add(Rectangle(width=(w - 0.7) * 0.55, height=0.22, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                  .move_to([x - w / 2 + 0.35 + (w - 0.7) * 0.275, yy, 0]))
        cells.add(Rectangle(width=(w - 0.7) * 0.3, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0)
                  .move_to([x + w / 2 - 0.35 - (w - 0.7) * 0.15, yy, 0]))
    g = VGroup(pg, head, cells)
    g.cells = cells
    return g


def report(x, y, w=2.0, h=2.5, fracs=(0.9, 0.6, 0.75)):
    """The eval report: a page with a title band and three bars."""
    pg = paper(x, y, w, h)
    head = Rectangle(width=w - 0.5, height=0.28, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x, y + h / 2 - 0.4, 0])
    bars = VGroup(*[Rectangle(width=(w - 0.7) * f, height=0.26, fill_color=c, fill_opacity=1, stroke_width=0)
                    .move_to([x - w / 2 + 0.35 + (w - 0.7) * f / 2, y + h / 2 - 1.0 - i * 0.5, 0])
                    for i, (f, c) in enumerate(zip(fracs, (BAR1, BAR2, BAR1)))])
    return VGroup(pg, head, bars)


def gate(x, y, w=1.8, h=2.0):
    """The verifier gate: two posts, a beam, one terracotta lamp."""
    pl = Rectangle(width=0.3, height=h, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x - w / 2, y, 0])
    pr = Rectangle(width=0.3, height=h, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x + w / 2, y, 0])
    beam = Rectangle(width=w + 0.3, height=0.3, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + h / 2 + 0.15, 0])
    lamp = Dot([x, y + h / 2 + 0.15, 0], radius=0.09, color=GHOST)
    g = VGroup(pl, pr, beam, lamp)
    g.lamp = lamp
    return g


def calculator(ox, oy, s=0.55):
    iso = Iso(ox, oy, s)
    body = iso.box(0, 0, 0, 1.6, 1.6, 0.7, DARK_TOP, DARK_L, DARK_R)
    keys = VGroup(*[Dot(iso.p(0.35 + 0.45 * i, 0.35 + 0.45 * j, 0.7), radius=0.05, color=GHOST)
                    for i in range(2) for j in range(2)])
    return VGroup(body, keys)


def toolbox(ox, oy, s=0.6):
    """The tool: a closed kraft box with one terracotta seal."""
    iso = Iso(ox, oy, s)
    body = iso.box(0, 0, 0, 1.6, 1.6, 1.1)
    seal = Dot(iso.p(0.8, 0.8, 1.1), radius=0.09, color=TERRA)
    return VGroup(body, seal)


def lens(x, y, r=0.6):
    ring = Circle(radius=r, stroke_color=INK, stroke_width=8, fill_color=CARD, fill_opacity=0.35).move_to([x, y, 0])
    handle = Line([x + r * 0.72, y - r * 0.72, 0], [x + r * 1.6, y - r * 1.6, 0], color=INK, stroke_width=12)
    return VGroup(ring, handle)


def house(x, y):
    body = Rectangle(width=1.5, height=1.1, fill_color=BAR3, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    roof = Polygon([x - 0.95, y + 0.55, 0], [x + 0.95, y + 0.55, 0], [x, y + 1.35, 0],
                   fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    door = Rectangle(width=0.36, height=0.6, fill_color=BAR2, fill_opacity=1, stroke_color=DKRAFT, stroke_width=3).move_to([x, y - 0.25, 0])
    return VGroup(body, roof, door)


def pile(x, y, n=4, s=0.42):
    return VGroup(*[bill(x + 0.12 * i, y + 0.14 * i, s) for i in range(n)])


POLE = "#7A6852"      # wooden utility pole
WIRE = "#5E5A52"      # line wire


def transformer(x, y, s=1.0, pole=True):
    """The tool: a pole-mounted distribution transformer (grey can, lid, fins, two bushings, wires)."""
    w, h = 1.3 * s, 1.7 * s
    parts = VGroup()
    if pole:
        px = x - w / 2 - 0.32 * s
        parts.add(Rectangle(width=0.26 * s, height=h + 2.0 * s, fill_color=POLE, fill_opacity=1, stroke_width=0)
                  .move_to([px, y + 0.25 * s, 0]))
        parts.add(Rectangle(width=0.5 * s, height=0.16 * s, fill_color=WIRE, fill_opacity=1, stroke_width=0)
                  .move_to([px + 0.3 * s, y + 0.2 * s, 0]))
    body = RoundedRectangle(width=w, height=h, corner_radius=0.18 * s, fill_color=BAR1, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    fins = VGroup(*[Rectangle(width=0.13 * s, height=h * 0.62, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                    .move_to([x + dx * s, y - 0.08 * s, 0]) for dx in (-0.36, -0.12, 0.12, 0.36)])
    lid = RoundedRectangle(width=w + 0.18 * s, height=0.24 * s, corner_radius=0.08 * s, fill_color=BAR2, fill_opacity=1,
                           stroke_color=INK, stroke_width=4).move_to([x, y + h / 2 + 0.06 * s, 0])
    bush = VGroup(*[RoundedRectangle(width=0.2 * s, height=0.42 * s, corner_radius=0.06 * s, fill_color=CARD, fill_opacity=1,
                                     stroke_color=INK, stroke_width=3).move_to([x + dx * s, y + h / 2 + 0.39 * s, 0])
                    for dx in (-0.32, 0.32)])
    wires = VGroup(*[Line([x + dx * s, y + h / 2 + 0.6 * s, 0], [x + (dx + 0.25) * s, y + h / 2 + 1.15 * s, 0],
                          color=WIRE, stroke_width=4) for dx in (-0.32, 0.32)])
    lamp = Dot([x + 0.38 * s, y - h / 2 + 0.26 * s, 0], radius=0.07 * s, color=TERRA)
    parts.add(wires, body, fins, lid, bush, lamp)
    parts.center_pt = np.array([x, y, 0.0])
    return parts


def panel(x, y, w, h):
    """A plain container panel (replaces the cardboard trays): light fill, grey outline."""
    return RoundedRectangle(width=w, height=h, corner_radius=0.16, fill_color=BELT, fill_opacity=1,
                            stroke_color=BAR1, stroke_width=4).move_to([x, y, 0])


def folder(x, y, w=2.6, h=2.0):
    """The GitHub repository: a plain folder (tab + body)."""
    # Body stays within Gate V's background tolerance (CARD); contrast comes from the ink outline and a dark tab.
    tab = RoundedRectangle(width=w * 0.38, height=0.34, corner_radius=0.08, fill_color=BAR1, fill_opacity=1,
                           stroke_color=INK, stroke_width=4).move_to([x - w / 2 + w * 0.19, y + h / 2 + 0.1, 0])
    body = RoundedRectangle(width=w, height=h, corner_radius=0.12, fill_color=CARD, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(tab, body)


def contract(x, y, w=1.3, h=1.7):
    """A supplier sign-up contract: page, scribbled terms, a signature line."""
    pg = paper(x, y, w, h)
    terms = scribble_block(x - w / 2 + 0.25, y + h / 2 - 0.35, w - 0.5, n=3, gap=0.28, color=BAR1, sw=3)
    sig = Line([x - w / 2 + 0.25, y - h / 2 + 0.35, 0], [x + w / 2 - 0.25, y - h / 2 + 0.35, 0], color=BAR1, stroke_width=4)
    return VGroup(pg, terms, sig)


def coin_stack(x, base_y, n=10, w=2.6, t=0.26):
    """A stack of coins, drawn bottom-up; returns the list of coins."""
    coins = []
    for i in range(n):
        y0 = base_y + i * t
        band = Rectangle(width=w, height=t, fill_color=BAR3, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y0 + t / 2, 0])
        top = Ellipse(width=w, height=0.55, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to([x, y0 + t, 0])
        coins.append(VGroup(band, top))
    return coins


def plug(x, y, s=1.0):
    """An API connection drawn as a plug: body, two prongs, a short cable."""
    body = RoundedRectangle(width=0.6 * s, height=0.7 * s, corner_radius=0.12 * s, fill_color=BAR1, fill_opacity=1,
                            stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    prongs = VGroup(*[Rectangle(width=0.1 * s, height=0.3 * s, fill_color=INK, fill_opacity=1, stroke_width=0)
                      .move_to([x + dx * s, y + 0.5 * s, 0]) for dx in (-0.14, 0.14)])
    cable = Line([x, y - 0.35 * s, 0], [x, y - 0.75 * s, 0], color=WIRE, stroke_width=5)
    return VGroup(cable, body, prongs)


def checklist(x, y, w=0.8, h=1.0):
    pg = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=DKRAFT, stroke_width=4).move_to([x, y, 0])
    ticks = VGroup(*[check(x - w / 2 + 0.22, y + h / 2 - 0.25 - 0.27 * k, s=0.08, w=4) for k in range(3)])
    bars = VGroup(*[Rectangle(width=w * 0.4, height=0.1, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                    .move_to([x + 0.12, y + h / 2 - 0.25 - 0.27 * k, 0]) for k in range(3)])
    return VGroup(pg, ticks, bars)


def code_page(x, y, w=0.8, h=1.0):
    pg = Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=DKRAFT, stroke_width=4).move_to([x, y, 0])
    lines = VGroup(*[Rectangle(width=w * f, height=0.09, fill_color=c, fill_opacity=1, stroke_width=0)
                     .move_to([x - w / 2 + 0.12 + w * f / 2 + ind, y + h / 2 - 0.22 - 0.18 * k, 0])
                     for k, (f, c, ind) in enumerate(((0.5, BAR1, 0), (0.45, BAR2, 0.12), (0.35, BAR2, 0.12), (0.4, BAR1, 0)))])
    return VGroup(pg, lines)


# ───────────────────────────── the beats ─────────────────────────────
class B00_Title(Scene):
    """Plain title card (no Claude composer cold open): the title, my name, and the film's bill."""
    def construct(self):
        title = T("Electricity Supplier Check", 80).move_to([0, 0.45, 0])
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.7)
        at(self, "Hey-month")
        name = T("Hemanth Rayudu", 48).move_to([0, -0.75, 0])
        play(self, FadeIn(name), run_time=0.5)
        at(self, "Nothing in it")
        b = bill(0.0, -2.25, 0.42)
        play(self, FadeIn(b, shift=UP * 0.3), run_time=0.6)
        done(self)


def printed_bill(x0=-5.0, x1=4.0, top=2.6, bottom=-1.5):
    """B01's constructed bill: a page with printed rows. Left column = label, right column = value."""
    w, h = x1 - x0, top - bottom
    pg = paper((x0 + x1) / 2, (top + bottom) / 2, w, h)
    band = Rectangle(width=w - 1.0, height=0.32, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([(x0 + x1) / 2, top - 0.42, 0])
    s1 = scribble(x0 + 0.5, top - 1.65, w - 1.0, amp=0.05, color=BAR1, sw=4)
    s2 = scribble(x0 + 0.5, top - 3.55, (w - 1.0) * 0.55, amp=0.05, color=BAR1, sw=4)
    g = VGroup(pg, band, s1, s2)
    def row(left, right, y):
        lt = T(left, 36); lt.move_to([x0 + 0.5 + lt.width / 2, y, 0])
        rt = T(right, 36); rt.move_to([x1 - 0.5 - rt.width / 2, y, 0])
        return VGroup(lt, rt)
    g.r1 = row("Supplier", "competitive supplier", top - 1.0)
    g.r2 = row("Basic service, fixed", "$0.17185 / kWh", top - 2.3)
    g.r3 = row("Basic service, Aug 2026", "$0.16074 / kWh", top - 2.95)
    g.mark = np.array([x0 + 0.25, top - 1.0, 0.0])
    return g


class B01_Bill(Scene):
    """I was on a competitive supplier and overpaid. The constructed bill prints the real tariff rates."""
    def construct(self):
        tg = tag("CONSTRUCTED")
        b = printed_bill()
        self.add(tg)
        self.play(FadeIn(b, shift=DOWN * 0.3), run_time=0.6)
        at(self, "competitive electricity supplier")
        dot = Dot(b.mark, radius=0.09, color=TERRA)
        play(self, FadeIn(b.r1), GrowFromCenter(dot), run_time=0.6)
        at(self, "overpaid")
        c = coin(4.25, 0.9)
        play(self, FadeIn(c, shift=RIGHT * 0.3), run_time=0.35)
        play(self, MoveAlongPath(c, ArcBetweenPoints(np.array([4.25, 0.9, 0]), np.array([5.0, -0.9, 0]), angle=-PI / 2)),
             run_time=0.6, rate_func=ease_in)
        at(self, "basic service would")
        cap = caption("National Grid basic service rates, M.D.P.U. No. 1-26-H",
                      "effective Aug 1, 2026 · downloaded 2026-10-14", y=-2.75)
        play(self, FadeIn(b.r2), FadeIn(b.r3), run_time=0.6)
        play(self, FadeIn(cap), run_time=0.4)
        done(self)


class B02_Losses(Scene):
    """$738.7 million; suppliers 10–30% above basic service account for more than half."""
    def construct(self):
        cap = caption("Massachusetts Attorney General, 2026 competitive supply report",
                      "pp. 2 & 4 · downloaded 2026-10-14", y=-2.8)
        n, t, base = 10, 0.26, -1.7
        coins = coin_stack(-1.0, base, n=n, t=t)
        self.add(cap)
        self.play(FadeIn(coins[0], shift=DOWN * 0.2), run_time=0.5)
        at(self, "residential customers")
        for c_ in coins[1:]:
            play(self, FadeIn(c_, shift=DOWN * 0.5), run_time=0.22, rate_func=ease_in)
        at(self, "seven hundred")
        hero = T("$738.7 million", 72).move_to([3.3, 1.4, 0])
        play(self, FadeIn(hero, shift=UP * 0.2), run_time=0.6)
        at(self, "ten to thirty")
        x_b = -1.0 - 1.3 - 0.35
        y0 = base
        y1 = base + 0.5145 * n * t
        br = VGroup(Line([x_b, y0, 0], [x_b, y1, 0], color=INK, stroke_width=5),
                    Line([x_b, y0, 0], [x_b + 0.2, y0, 0], color=INK, stroke_width=5),
                    Line([x_b, y1, 0], [x_b + 0.2, y1, 0], color=INK, stroke_width=5))
        top_dot = Dot([x_b, y1, 0], radius=0.08, color=TERRA)
        blab = T("10–30% above", 40)
        blab.move_to([x_b - 0.35 - blab.width / 2, (y0 + y1) / 2, 0])
        play(self, Create(br), FadeIn(blab), run_time=0.7)
        play(self, GrowFromCenter(top_dot), run_time=0.3)
        at(self, "hard to spot")
        small = bill(1.3, -0.9, 0.5)
        play(self, FadeIn(small, shift=LEFT * 0.4), run_time=0.6)
        done(self)


class B03_Toolbox(Scene):
    """It will read a bill and give one number; a repository with the rate table, test bills, eval report."""
    def construct(self):
        tg = tag("PROPOSED")
        tr = transformer(-4.0, -0.4, 1.0)
        self.add(tg)
        self.play(FadeIn(tr, shift=UP * 0.2), run_time=0.6)
        b = bill(-1.9, 1.9, 0.42)
        play(self, FadeIn(b, shift=LEFT * 0.3), run_time=0.3)
        play(self, b.animate.move_to([-4.0, -0.4, 0]).scale(0.4), run_time=0.7, rate_func=ease_in)
        play(self, FadeOut(b), run_time=0.2)
        at(self, "tell you exactly")
        sl = slip(-1.9, -0.6)
        play(self, FadeIn(sl, shift=RIGHT * 0.8), run_time=0.7)
        at(self, "math shown")
        math = VGroup(*[Rectangle(width=w_, height=0.18, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x_, -1.4, 0])
                        for x_, w_ in ((-2.45, 0.4), (-1.9, 0.3), (-1.35, 0.4))])
        play(self, FadeIn(math, shift=DOWN * 0.15), run_time=0.5)
        at(self, "repository")
        fd = folder(2.6, -0.1, w=6.4, h=3.3)
        play(self, FadeIn(fd, shift=UP * 0.2), run_time=0.6)
        at(self, "dated rate table")
        rt = sheet(0.6, -0.1, w=1.7, h=2.2, rows=3)
        l1 = label("rate table", 0.6, -2.3, 38)
        play(self, FadeIn(rt, shift=UP * 0.4), FadeIn(l1), run_time=0.7)
        at(self, "constructed test bills")
        tb = pile(2.55, -0.3, n=3, s=0.5)
        l2 = label("test bills", 2.55, -2.3, 38)
        play(self, FadeIn(tb, shift=UP * 0.4), FadeIn(l2), run_time=0.7)
        at(self, "evaluation report")
        rp = report(4.85, -0.1, w=1.7, h=2.2)
        l3 = label("eval report", 4.85, -2.3, 38)
        play(self, FadeIn(rp, shift=UP * 0.4), FadeIn(l3), run_time=0.7)
        done(self)


class B04_FirstMinute(Scene):
    """Who opens it, and the first sixty seconds. The result screen is a constructed mock-up."""
    def construct(self):
        tg = tag("CONSTRUCTED MOCK-UP")
        self.add(tg)
        h = house(-5.0, 1.0)
        self.play(FadeIn(h, shift=UP * 0.2), run_time=0.6)
        at(self, "energy coach")
        p = pile(-5.3, -1.6, n=4, s=0.42)
        play(self, FadeIn(p, shift=UP * 0.2), run_time=0.6)
        at(self, "first sixty seconds")
        watch = VGroup(Circle(radius=0.75, fill_color=CARD, fill_opacity=1, stroke_color=DKRAFT, stroke_width=5).move_to([-2.4, 1.4, 0]),
                       Rectangle(width=0.3, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-2.4, 2.32, 0]),
                       Line([-2.4, 1.4, 0], [-2.4, 1.85, 0], color=INK, stroke_width=6))
        wl = label("0:60", -2.4, 0.15)
        screen = Rectangle(width=5.0, height=3.0, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([2.6, 0.75, 0])
        bar = Rectangle(width=4.6, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([2.6, 2.0, 0])
        deck = Polygon([0.0, -0.75, 0], [5.2, -0.75, 0], [5.8, -1.35, 0], [-0.6, -1.35, 0],
                       fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
        play(self, Create(watch), FadeIn(wl), FadeIn(VGroup(screen, bar, deck)), run_time=0.8)
        at(self, "upload a bill")
        b = bill(-3.75, -1.2, 0.4)
        play(self, FadeIn(b), run_time=0.2)
        play(self, b.animate.move_to([0.95, 1.1, 0]), run_time=0.7)
        at(self, "on this bill")
        res = T("$X more", 60).move_to([3.0, 1.15, 0])
        play(self, FadeIn(res), run_time=0.5)
        at(self, "the formula")
        f = VGroup(*[Rectangle(width=w_, height=0.26, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x_, 0.3, 0])
                     for x_, w_ in ((1.3, 1.0), (2.6, 1.2), (3.9, 1.0))])
        play(self, FadeIn(f), run_time=0.5)
        at(self, "what to do next")
        nxt = VGroup(Arrow([0.8, -0.3, 0], [1.6, -0.3, 0], color=INK, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.35),
                     Rectangle(width=2.4, height=0.26, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([3.1, -0.3, 0]))
        play(self, FadeIn(nxt), run_time=0.5)
        done(self)


class B05_Reviewer(Scene):
    """The hiring manager opens the GitHub repo; the eval report checks each number against the calculator."""
    def construct(self):
        fd = folder(-4.2, 0.4, w=2.6, h=2.0)
        l1 = label("GitHub repo", -4.2, -1.1)
        self.play(FadeIn(fd, shift=UP * 0.2), run_time=0.6)
        at(self, "hiring manager")
        cur = cursor(-0.6, -2.2)
        play(self, FadeIn(l1), FadeIn(cur), run_time=0.5)
        play(self, cur.animate.move_to([-3.3, 0.1, 0]), run_time=7.0, rate_func=smooth)
        at(self, "open the project's")
        ring = Circle(radius=0.32, stroke_color=TERRA, stroke_width=5).move_to([-3.55, 0.35, 0])
        play(self, GrowFromCenter(ring), run_time=0.4)
        play(self, FadeOut(ring), run_time=0.3)
        at(self, "evaluation report")
        rp = paper(1.6, 0.25, 4.6, 3.9)
        head = Rectangle(width=4.0, height=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([1.6, 1.85, 0])
        l2 = label("eval report", 1.6, 2.65)
        play(self, FadeIn(VGroup(rp, head), shift=RIGHT * 0.6), FadeIn(l2), run_time=0.7)
        at(self, "For every test")
        rows = []
        for k in range(3):
            y_ = 1.05 - 0.85 * k
            left = Rectangle(width=1.0, height=0.3, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([0.25, y_, 0])
            right = Rectangle(width=1.0, height=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([2.35, y_, 0])
            rows.append((left, right, y_))
        play(self, *[FadeIn(VGroup(lf, rt_)) for lf, rt_, _ in rows], run_time=0.6)
        at(self, "matches a number")
        for lf, rt_, y_ in rows:
            link = Line([0.8, y_, 0], [1.8, y_, 0], color=WIRE, stroke_width=4)
            ck = check(3.3, y_ + 0.02, s=0.15)
            play(self, Create(link), Create(ck), run_time=0.35)
        at(self, "rerun the tests")
        loop = Arc(radius=0.36, start_angle=PI / 2, angle=1.6 * PI, color=INK, stroke_width=6).move_arc_center_to([-4.2, 2.35, 0])
        loop.add_tip(tip_length=0.18, tip_width=0.18)
        play(self, Create(loop), run_time=0.5)
        done(self)


class B06_Alternatives(Scene):
    """Energy Switch MA (an offers board) · a town energy coach (a person, a queue) · mine (instant)."""
    def construct(self):
        cap = caption("energyswitchma.gov · greennewton.org (example town energy coach)", y=-3.05)
        self.add(cap)
        outside = bill(-4.2, 1.85, 0.36)
        self.play(FadeIn(outside, shift=DOWN * 0.2), run_time=0.5)
        at(self, "Energy Switch Massachusetts")
        board = panel(-4.2, -0.15, 2.9, 1.9)
        offers = VGroup(*[Rectangle(width=2.0, height=0.28, fill_color=c, fill_opacity=1, stroke_width=0).move_to([-4.0, 0.4 - 0.55 * k, 0])
                          for k, c in enumerate((BAR1, BAR2, BAR1))])
        dots = VGroup(*[Dot([-5.25, 0.4 - 0.55 * k, 0], radius=0.07, color=INK) for k in range(3)])
        l1 = label("Energy Switch MA", -4.2, -1.6)
        play(self, FadeIn(board), FadeIn(offers), FadeIn(dots), FadeIn(l1), run_time=0.8)
        at(self, "energy coaches")
        clk = VGroup(Circle(radius=0.8, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([1.0, 0.45, 0]),
                     Line([1.0, 0.45, 0], [1.0, 0.95, 0], color=INK, stroke_width=6),
                     Line([1.0, 0.45, 0], [1.35, 0.3, 0], color=INK, stroke_width=6))
        queue = VGroup(*[bill(x_, 0.0, 0.25) for x_ in (-1.7, -0.95, -0.2)])
        l2 = label("energy coach", 0.0, -1.6)
        play(self, FadeIn(clk), FadeIn(queue, shift=RIGHT * 0.2), FadeIn(l2), run_time=0.8)
        at(self, "Mine will save")
        tr = transformer(4.6, -0.35, 0.62)
        l3 = label("mine", 4.3, -1.6)
        play(self, FadeIn(tr, shift=UP * 0.2), FadeIn(l3), run_time=0.6)
        b = bill(2.9, 1.6, 0.3)
        play(self, FadeIn(b), run_time=0.2)
        play(self, b.animate.move_to([4.6, -0.35, 0]).scale(0.5), run_time=0.5)
        sl = slip(4.6, 1.95)
        play(self, FadeOut(b), FadeIn(sl, shift=UP * 0.3), run_time=0.5)
        done(self)


class B07_Pipeline(Scene):
    """Claude reads into a schema, code checks it, Python does the math, Claude explains, the verifier rejects."""
    def construct(self):
        tg = tag("CONSTRUCTED")
        belt = Rectangle(width=12.0, height=0.45, fill_color=BELT, fill_opacity=1, stroke_color=CABLE, stroke_width=4).move_to([0, -1.25, 0])
        b = bill(-5.0, -0.2, 0.42)
        self.add(tg)
        self.play(FadeIn(belt), FadeIn(b), run_time=0.5)
        scan = Line([-5.7, 0.55, 0], [-5.7, -0.95, 0], color=TERRA, stroke_width=6)
        l1 = label("Claude reads", -4.0, 1.6)
        play(self, Create(scan), FadeIn(l1), run_time=0.3)
        play(self, scan.animate.move_to([-4.3, -0.2, 0]), run_time=0.6)
        grid = VGroup(*[Rectangle(width=0.42, height=0.42, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                        .move_to([-3.15 + 0.55 * i, 0.05 - 0.55 * j, 0]) for i in range(3) for j in range(2)])
        play(self, FadeOut(scan), FadeIn(grid, shift=RIGHT * 0.3), run_time=0.5)
        at(self, "code will check")
        ck = check(-2.6, 0.75, s=0.22)
        play(self, Create(ck), run_time=0.4)
        at(self, "Python will do")
        calc = calculator(-0.6, -1.0, 0.5)
        rt = sheet(0.95, -0.05, w=1.1, h=1.4, rows=2)
        l2 = label("Python math", 0.2, 2.15)
        play(self, FadeIn(calc, shift=UP * 0.2), FadeIn(rt, shift=UP * 0.2), FadeIn(l2), run_time=0.7)
        at(self, "match the billing")
        cal = RoundedRectangle(width=3.0, height=0.34, corner_radius=0.12, fill_color=BAR3, fill_opacity=1,
                               stroke_color=INK, stroke_width=4).move_to([0.2, 1.3, 0])
        play(self, FadeIn(cal), run_time=0.5)
        at(self, "prorate across")
        split = Line([0.5, 1.6, 0], [0.5, 1.0, 0], color=INK, stroke_width=5)
        play(self, Create(split), run_time=0.4)
        at(self, "Then Claude will")
        pg = paper(2.9, -0.15, 1.0, 1.3)
        lines = scribble_block(2.55, 0.2, 0.7, n=3, gap=0.3, color=BAR1, sw=3)
        play(self, FadeIn(pg), FadeIn(lines), run_time=0.6)
        at(self, "a verifier will")
        gt = gate(4.9, -0.1, w=1.5, h=1.9)
        l3 = label("verifier", 4.9, 1.75)
        play(self, FadeIn(gt), FadeIn(l3), run_time=0.6)
        stray = Rectangle(width=0.36, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([3.15, -0.55, 0])
        play(self, FadeIn(stray), run_time=0.25)
        play(self, VGroup(pg, lines, stray).animate.shift(RIGHT * 1.6), run_time=0.6)
        xmark = VGroup(Line([4.6, -0.3, 0], [4.95, -0.65, 0], color=INK, stroke_width=6),
                       Line([4.6, -0.65, 0], [4.95, -0.3, 0], color=INK, stroke_width=6))
        play(self, stray.animate.move_to([4.78, -0.47, 0]), gt.lamp.animate.set_color(TERRA), run_time=0.3)
        play(self, Create(xmark), run_time=0.3)
        done(self)


class B08_Evidence(Scene):
    """Five objects for the five course skills appear on a rail as each is named; three pieces of evidence land on the shelf."""
    def construct(self):
        xs = (-4.6, -2.3, 0.0, 2.3, 4.6)
        rail = Line([-5.6, 1.55, 0], [5.6, 1.55, 0], color=CABLE, stroke_width=4)
        shelf = RoundedRectangle(width=10.0, height=0.3, corner_radius=0.1, fill_color=BAR3, fill_opacity=1,
                                 stroke_color=INK, stroke_width=4).move_to([0, -1.25, 0])
        self.play(Create(rail), Create(shelf), run_time=0.7)
        def mini_page(x, y, w=0.75, h=0.95):
            return Rectangle(width=w, height=h, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=DKRAFT, stroke_width=4).move_to([x, y, 0])
        # 1 prompt contracts: a fixed schema grid, checked in code
        x = xs[0]
        grid = VGroup(*[Square(side_length=0.3, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                        .move_to([x - 0.45 + 0.4 * i, 2.3 - 0.4 * j, 0]) for i in range(3) for j in range(2)])
        ck = check(x + 0.55, 2.75, s=0.16)
        # 2 verification kept separate from generation: a draft page, a gap, a gate
        x = xs[1]
        draft = VGroup(mini_page(x - 0.45, 2.15), scribble_block(x - 0.7, 2.4, 0.5, n=3, gap=0.22, color=BAR1, sw=3))
        gt = gate(x + 0.55, 2.1, w=0.5, h=0.85)
        # 3 source grounding: the dated rate table
        rt = sheet(xs[2], 2.2, w=1.0, h=1.15, rows=2)
        # 4 bounded agent loop with retries: a loop arrow and three retry marks
        x = xs[3]
        loop = Arc(radius=0.38, start_angle=PI / 2, angle=1.6 * PI, color=INK, stroke_width=6).move_arc_center_to([x, 2.35, 0])
        loop.add_tip(tip_length=0.18, tip_width=0.18)
        tries = VGroup(*[Dot([x - 0.3 + 0.3 * k, 1.8, 0], radius=0.06, color=BAR1) for k in range(3)])
        # 5 held-out evaluation: a stack of cases, a divider, one stack held out
        x = xs[4]
        stack_a = VGroup(*[mini_page(x - 0.45 + 0.07 * k, 2.15 + 0.07 * k, 0.6, 0.75) for k in range(3)])
        divider = DashedLine([x + 0.05, 2.75, 0], [x + 0.05, 1.7, 0], color=INK, stroke_width=4, dash_length=0.1)
        held = mini_page(x + 0.55, 2.2, 0.6, 0.75)
        plan = (("prompt contracts", [FadeIn(grid, shift=DOWN * 0.2), Create(ck)]),
                ("verification kept", [FadeIn(draft, shift=DOWN * 0.2), FadeIn(gt, shift=DOWN * 0.2)]),
                ("source grounding", [FadeIn(rt, shift=DOWN * 0.2)]),
                ("a bounded agent", [Create(loop), FadeIn(tries)]),
                ("held-out evaluation", [FadeIn(stack_a, shift=DOWN * 0.2), Create(divider), FadeIn(held, shift=RIGHT * 0.2)]))
        for ph, anims in plan:
            at(self, ph)
            play(self, *anims, run_time=0.45)
        at(self, "The evidence")
        ts = paper(-3.4, -0.15, 1.5, 1.8)
        ticks = VGroup(*[check(-3.75, 0.35 - 0.5 * k, s=0.13) for k in range(3)])
        tl = VGroup(*[Rectangle(width=0.6, height=0.18, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([-3.05, 0.35 - 0.5 * k, 0])
                      for k in range(3)])
        l1 = label("test suite", -3.4, -1.95, 38)
        play(self, FadeIn(VGroup(ts, tl), shift=DOWN * 0.3), FadeIn(l1), run_time=0.6)
        at(self, "test suite")
        play(self, Create(ticks), run_time=0.5)
        at(self, "planted traps")
        tb = bill(0.0, -0.15, 0.55)
        trap = Square(side_length=0.3, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([0.42, -0.2, 0])
        l2 = label("planted traps", 0.0, -1.95, 38)
        play(self, FadeIn(tb, shift=DOWN * 0.3), FadeIn(l2), run_time=0.6)
        play(self, FadeIn(trap), run_time=0.3)
        at(self, "drafts the verifier")
        dp = paper(3.4, -0.15, 1.5, 1.8)
        dl = scribble_block(2.95, 0.4, 0.9, n=3, gap=0.4, color=BAR1, sw=3)
        dx = VGroup(Line([2.85, 0.5, 0], [3.95, -0.8, 0], color=INK, stroke_width=6),
                    Line([2.85, -0.8, 0], [3.95, 0.5, 0], color=INK, stroke_width=6))
        l3 = label("rejected drafts", 3.4, -1.95, 38)
        play(self, FadeIn(VGroup(dp, dl), shift=DOWN * 0.3), FadeIn(l3), run_time=0.6)
        play(self, Create(dx), run_time=0.4)
        at(self, "fairly conclude")
        sl = slip(5.45, 0.55, w=1.1, h=0.75, size=46)
        tick = check(5.4, 1.15, s=0.18, color=TERRA)
        play(self, FadeIn(sl, shift=DOWN * 0.3), run_time=0.5)
        play(self, Create(tick), run_time=0.4)
        done(self)


class B09_Scope(Scene):
    """In: residential bills. Out: never a supplier sign-up. First: rate table, calculator, ten test bills."""
    def construct(self):
        pins = panel(-4.4, 0.25, 2.8, 3.0)
        pout = panel(-0.9, 0.25, 2.8, 3.0)
        pfirst = panel(3.7, 0.25, 4.4, 3.0)
        labs = VGroup(label("in", -4.4, -1.75, 44), label("out", -0.9, -1.75, 44), label("first", 3.7, -1.75, 44))
        self.play(FadeIn(VGroup(pins, pout, pfirst)), FadeIn(labs), run_time=0.7)
        at(self, "National Grid residential")
        b = bill(-4.4, 2.2, 0.45)
        play(self, FadeIn(b), run_time=0.2)
        play(self, b.animate.move_to([-4.4, 0.25, 0]), run_time=0.6, rate_func=ease_in)
        at(self, "never recommend")
        ct = contract(-0.9, 0.25)
        play(self, FadeIn(ct, shift=DOWN * 0.3), run_time=0.5)
        cross = VGroup(Line([-1.75, 1.2, 0], [-0.05, -0.7, 0], color=INK, stroke_width=8),
                       Line([-1.75, -0.7, 0], [-0.05, 1.2, 0], color=INK, stroke_width=8))
        play(self, Create(cross), run_time=0.5)
        at(self, "rate table snapshot")
        rt = sheet(2.35, 0.85, w=1.15, h=1.4, rows=2)
        play(self, FadeIn(rt, shift=UP * 0.3), run_time=0.5)
        at(self, "a prorating calculator")
        calc = calculator(3.75, 0.35, 0.42)
        play(self, FadeIn(calc, shift=UP * 0.3), run_time=0.5)
        at(self, "ten constructed bills")
        minis = VGroup(*[Rectangle(width=0.28, height=0.38, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=3)
                         .move_to([1.95 + 0.39 * k, -0.75, 0]) for k in range(10)])
        play(self, LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in minis], lag_ratio=0.12), run_time=1.0)
        at(self, "one crossing August")
        dl = DashedLine([5.46, -0.3, 0], [5.46, -1.15, 0], color=INK, stroke_width=4, dash_length=0.1)
        play(self, Create(dl), run_time=0.4)
        at(self, "know it ran")
        tg = tag("not run yet")
        boxes = VGroup(Square(side_length=0.45, stroke_color=INK, stroke_width=5).move_to([4.9, -1.75, 0]),
                       Square(side_length=0.45, stroke_color=INK, stroke_width=5).move_to([5.6, -1.75, 0]))
        play(self, FadeIn(tg), Create(boxes), run_time=0.6)
        done(self)


class B10_Risk(Scene):
    """Wrong rate period → wrong dollar amount. Fix: source + date on every row; "can't verify" over a guess."""
    def construct(self):
        tg = tag("CONSTRUCTED")
        bar = RoundedRectangle(width=6.4, height=0.6, corner_radius=0.15, fill_color=BAR3, fill_opacity=1,
                               stroke_color=INK, stroke_width=4).move_to([-1.4, 1.0, 0])
        dl = DashedLine([-1.0, 1.65, 0], [-1.0, 0.35, 0], color=INK, stroke_width=5, dash_length=0.12)
        dlab = label("Aug 1, 2026", -1.0, 2.15)
        self.add(tg)
        self.play(FadeIn(bar), Create(dl), FadeIn(dlab), run_time=0.7)
        sl = slip(-3.6, -1.1)
        play(self, FadeIn(sl), run_time=0.4)
        at(self, "the wrong rate")
        wrong = Rectangle(width=6.4, height=0.3, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-1.4, 1.0, 0])
        play(self, FadeIn(wrong, shift=RIGHT * 0.8), run_time=0.6)
        at(self, "destroy trust")
        crack = VMobject(stroke_color=INK, stroke_width=5)
        crack.set_points_as_corners([[-4.25, -0.75, 0], [-3.85, -1.05, 0], [-3.45, -0.85, 0], [-3.1, -1.25, 0], [-2.95, -1.45, 0]])
        play(self, Create(crack), run_time=0.4)
        at(self, "every rate row")
        rt = sheet(4.5, 0.6, w=2.4, h=2.8, rows=3)
        play(self, FadeIn(rt, shift=LEFT * 0.4), run_time=0.6)
        tags = VGroup(*[Dot([5.95, 1.05 - k * 0.75, 0], radius=0.09, color=TERRA) for k in range(3)])
        play(self, LaggedStart(*[GrowFromCenter(d) for d in tags], lag_ratio=0.3), run_time=0.7)
        at(self, "can't verify")
        cv = T("can't verify", 48, bold=True).move_to([-0.9, -0.55, 0])
        play(self, FadeOut(wrong), FadeIn(cv, scale=1.15), run_time=0.5)
        at(self, "don't know yet")
        sb = bill(1.9, -1.55, 0.36)
        qm = T("?", 72, bold=True).move_to([2.85, -1.0, 0])
        play(self, FadeIn(sb), FadeIn(qm), run_time=0.6)
        done(self)


class B11_Why(Scene):
    """It happened to me. Skills I have (one panel) and skills that are new (another)."""
    def construct(self):
        b = bill(-5.2, 1.7, 0.45)
        c = coin(-4.25, 0.95, 0.22)
        self.play(FadeIn(b), FadeIn(c), run_time=0.6)
        at(self, "It's a mix")
        ph = panel(-1.7, -0.45, 3.8, 2.3)
        pn = panel(3.3, -0.45, 3.8, 2.3)
        labs = VGroup(label("have", -1.7, -2.05, 44), label("new", 3.3, -2.05, 44))
        play(self, FadeIn(VGroup(ph, pn)), FadeIn(labs), run_time=0.7)
        srv, lights = Iso(-2.05, -1.05, 0.38).server(0, 0, 0, w=1.3, d=1.3, slab=0.36, n=3)
        have_items = (("Python", code_page(-3.0, -0.4)),
                      ("backend", VGroup(srv, lights)),
                      ("API", plug(-0.95, -0.25, 0.9)),
                      ("evaluation design", checklist(-0.05, -0.4)))
        for ph_, obj in have_items:
            at(self, ph_)
            play(self, FadeIn(obj, shift=DOWN * 0.4), run_time=0.35, rate_func=ease_in)
        at(self, "electricity rates")
        ts = sheet(2.05, -0.4, w=0.95, h=1.2, rows=2)
        play(self, FadeIn(ts, shift=DOWN * 0.4), run_time=0.4)
        at(self, "extracting fields")
        sb = bill(3.25, -0.4, 0.34)
        lz = lens(3.45, -0.2, r=0.3)
        play(self, FadeIn(sb, shift=DOWN * 0.4), FadeIn(lz), run_time=0.45)
        at(self, "the verifier design")
        gt = gate(4.55, -0.55, w=0.6, h=0.9)
        play(self, FadeIn(gt, shift=DOWN * 0.4), run_time=0.4)
        done(self)


def dashed(*mobs, per_unit=6):
    """Dashed outline versions of planned objects (not built yet)."""
    out = VGroup()
    for m in mobs:
        n = max(6, int(round(per_unit * 2 * (m.width + m.height))))
        out.add(DashedVMobject(m, num_dashes=n))
    return out


class B12_Today(Scene):
    """Exists today: an empty panel. Will exist: dashed outlines of the tool and its parts."""
    def construct(self):
        pe = panel(-3.6, -0.2, 3.6, 2.8)
        l1 = label("exists today", -3.6, -2.05, 44)
        self.play(FadeIn(pe), run_time=0.6)
        at(self, "today, nothing exists")
        play(self, FadeIn(l1), run_time=0.4)
        l2 = label("will exist", 2.9, -2.05, 44)
        play(self, FadeIn(l2), run_time=0.3)
        at(self, "Everything I've described")
        k = dict(color=INK, stroke_width=4)
        tool = dashed(RoundedRectangle(width=0.9, height=1.15, corner_radius=0.12, **k).move_to([0.9, 0.85, 0]),
                      Rectangle(width=1.05, height=0.18, **k).move_to([0.9, 1.52, 0]),
                      Rectangle(width=0.14, height=0.3, **k).move_to([0.68, 1.78, 0]),
                      Rectangle(width=0.14, height=0.3, **k).move_to([1.12, 1.78, 0]))
        table = dashed(Rectangle(width=1.2, height=1.5, **k).move_to([2.5, 0.95, 0]),
                       Line([1.9, 1.3, 0], [3.1, 1.3, 0], **k))
        calc = dashed(Square(side_length=1.05, **k).move_to([4.1, 0.85, 0]))
        bl = dashed(Rectangle(width=1.05, height=1.35, **k).move_to([1.3, -0.8, 0]),
                    Rectangle(width=0.7, height=0.2, **k).move_to([1.3, -0.35, 0]))
        gt = dashed(Rectangle(width=0.26, height=1.2, **k).move_to([2.6, -0.9, 0]),
                    Rectangle(width=0.26, height=1.2, **k).move_to([3.6, -0.9, 0]),
                    Rectangle(width=1.3, height=0.26, **k).move_to([3.1, -0.17, 0]))
        rpt = dashed(Rectangle(width=1.2, height=1.5, **k).move_to([4.9, -0.75, 0]),
                     Line([4.3, -0.35, 0], [5.5, -0.35, 0], **k))
        shapes = [tool, table, calc, bl, gt, rpt]
        play(self, LaggedStart(*[Create(s_) for s_ in shapes], lag_ratio=0.25), run_time=2.0)
        done(self)
