
# ═════════════════════════════ DataSentry pitch — scenes (Ethan Gomes, 2026-10-14) ═════════════════════════════
# scenes.py = iso_kit.py + iso_originals_25.py + this file (see build_scenes.sh). Gate A copies only scenes.py.
# One drawing per beat; labels beside objects, ink, >= 32; terracotta only for dots/lights/tape/checks.

MID_MARGIN = 0.26


def G(self, *anims, rt=0.5, **kw):
    """Play, but never across the clip midpoint (GATE T and Gate V sample there)."""
    bid = type(self).__name__.split("_")[0]
    tgt = _TARGET.get(bid, 0)
    if tgt:
        mid, t0 = tgt / 2.0, _elapsed(self)
        if t0 < mid + MID_MARGIN and t0 + rt > mid - MID_MARGIN:
            self.wait(mid + MID_MARGIN - t0)
    self.play(*anims, run_time=rt, **kw)


def L(s, x, y, size=36, bold=False):
    return T(s, size, INK, bold).move_to([x, y, 0])


def parcel(iso, x0, y0, z0=0.0, w=1.0, d=1.0, h=0.8, flaw=False):
    """A kraft parcel (a batch of rows). `flaw` adds one terracotta dot on its top face (a planted defect)."""
    g = VGroup(iso.box(x0, y0, z0, w, d, h))
    if flaw:
        g.add(Dot(iso.p(x0 + w * 0.5, y0 + d * 0.5, z0 + h), radius=0.09, color=TERRA))
    return g


def table_card(x, y, w=5.4, h=3.6, rows=6):
    """A flat data table: kraft-shadowed white card, a grey header band of 5 column blocks, grey row bars."""
    card = paper(x, y, w=w, h=h)
    top = y + h / 2
    cols = VGroup(*[RoundedRectangle(width=(w - 0.8) / 5 - 0.12, height=0.34, corner_radius=0.08,
                                     fill_color=BAR1, fill_opacity=1, stroke_width=0)
                    .move_to([x - w / 2 + 0.4 + (i + 0.5) * (w - 0.8) / 5, top - 0.45, 0]) for i in range(5)])
    bars = VGroup(*[RoundedRectangle(width=w - 0.8, height=0.24, corner_radius=0.06, fill_color=BAR1,
                                     fill_opacity=1, stroke_width=0)
                    .move_to([x, top - 1.0 - i * (h - 1.35) / max(1, rows - 1), 0]) for i in range(rows)])
    return card, cols, bars


def tray(ox, oy, s=1.0, w=2.6, d=2.6, h=0.45):
    """A shallow kraft tray on a DIM grey plinth (a pale kraft object alone fails Gate V contrast)."""
    iso = Iso(ox, oy, s)
    back, front = iso.open_box(0, 0, 0, w, d, h)
    plinth = iso.box(-0.15, -0.15, -0.28, w + 0.3, d + 0.3, 0.28, BAR1, "#6F737A", "#5F636A")
    plinth.set_z_index(-1)
    back.add_to_back(plinth)
    return iso, back, front


def block_in(iso, gx, gy, w=0.8, d=0.8, h=0.6, dark=False):
    b = iso.box(gx, gy, 0.02, w, d, h, *((DARK_TOP, DARK_L, DARK_R) if dark else (BOX_TOP, BOX_L, BOX_R)))
    b.set_z_index(1.0 + (6 - gx - gy) * 0.05)
    return b


def tall_scribbles(page, n=3, inset=0.25, gap=0.5, amp=0.11):
    """scribbles_on() with taller strokes: the kit's 0.07 amplitude measures ~40 px at 4K, under GATE T's 41 px floor."""
    w = page.w - 2 * inset
    x0, y0 = page.cx - w / 2, page.cy + page.h / 2 - inset - 0.15
    return VGroup(*[scribble(x0, y0 - i * gap, w * (0.62 if i == n - 1 else 1.0), amp=amp) for i in range(n)])


# A variant of the approved scanner prop for this film (Ethan, 2026-10-14): the near (left) leg's top cap is dropped,
# so the top bar sits over the leg instead of the leg's cap showing on top of the bar. The toolkit prop is unchanged.
import copy as _copy
_SC = _copy.deepcopy(_ST_ORIGINALS_25["checkpoint-scanner"])
_SC["parts"]["near-post"] = _SC["parts"]["near-post"][:2]      # keep the two side faces; drop the top face
_ST_ORIGINALS_25["checkpoint-scanner-under"] = _SC



def scanner(height, x, y):
    """The film's scanner rig with explicit layering (Ethan, 2026-10-14): the moving block passes BEHIND the top bar,
    the near leg stays in front, the far leg stays behind the block. Arch parts 0-2 are the far leg; 3-6 the bar + light."""
    rig = make_original("checkpoint-scanner-under", height=height, x=x, y=y)
    arch = list(rig.parts["arch"])
    for m in arch[:3]:
        m.set_z_index(0)
    for m in arch[3:]:
        m.set_z_index(2)
    rig.parts["parcel"].set_z_index(1)
    rig.parts["near-post"].set_z_index(3)
    return rig


MONO = "Menlo"


def M(s, size=28, color=INK):
    return Text(s, font=MONO, color=color, font_size=size)


def terminal(x, y, w, h):
    """A plain terminal-style panel for RECORDED output (typeset, not a screen recording): card, grey title bar."""
    shadow = RoundedRectangle(width=w, height=h, corner_radius=0.18, fill_color=BOX_L, fill_opacity=1,
                              stroke_width=0).move_to([x + 0.14, y - 0.14, 0])
    win = RoundedRectangle(width=w, height=h, corner_radius=0.18, fill_color=CARD, fill_opacity=1,
                           stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    bar = RoundedRectangle(width=w - 0.4, height=0.36, corner_radius=0.1, fill_color=BAR1, fill_opacity=1,
                           stroke_width=0).move_to([x, y + h / 2 - 0.36, 0])
    return VGroup(shadow, win, bar)


def tline(s, x0, y, size=24):
    """One left-aligned output line starting at x0."""
    return M(s, size).move_to([x0, y, 0], aligned_edge=LEFT)


CHAR_W = 0.2    # Menlo advance per character at font sizes 24-26 (measured); fixed so Gate A's stub and Manim agree


def panel(texts, cx, cy, size=24, gap=0.5, marker_room=0.9):
    """Lines of recorded output in a window sized to fit them, centred on (cx, cy). Returns (window, [lines]).
    Geometry comes from character counts (monospace), never from measured mobject widths."""
    w = max(len(t.strip()) for t in texts) * CHAR_W + 1.0 + marker_room
    h = 0.75 + gap * len(texts) + 0.35
    top = cy + h / 2
    x0 = cx - w / 2 + 0.5
    lines = []
    for i, t in enumerate(texts):
        y = top - 0.75 - i * gap
        ln = tline(t.strip(), x0, y, size)
        ln.x_end, ln.y_mid = x0 + len(t.strip()) * CHAR_W, y
        lines.append(ln)
    win = terminal(cx, cy, w, h)
    return win, lines


def mark_after(line, ok=True):
    """A tick (PASS/CAUGHT) or a terracotta dot (FAIL/MISSED) just past the end of a line."""
    if ok:
        return check(line.x_end + 0.35, line.y_mid + 0.02, s=0.18)
    return Dot([line.x_end + 0.4, line.y_mid, 0], radius=0.12, color=TERRA)


def recorded_tag(x, y):
    return L("recorded output \u00b7 " + RECORDED["date"], x, y, 32)


class BIDEA_Title(Scene):
    """Title card (Ethan's request, 2026-10-14): the project name, a drawn rule with one terracotta dot, one line on what it is."""
    def construct(self):
        credit = VGroup(T("Final Project Pitch Film created by", 48), T("Ethan Gomes", 48, bold=True)).arrange(RIGHT, buff=0.22, aligned_edge=UP).move_to([0, 2.55, 0])
        name = L("DataSentry", 0, 0.65, 120, bold=True)
        self.play(FadeIn(credit), FadeIn(name, shift=UP * 0.15), run_time=0.8)   # credit line (Ethan, 2026-10-25)
        until(self, "created by")
        rule = Line([-4.2, -0.55, 0], [3.9, -0.55, 0], color=BAR1, stroke_width=5)
        G(self, Create(rule), rt=0.8)
        dot = Dot([4.25, -0.55, 0], radius=0.13, color=TERRA)
        G(self, GrowFromCenter(dot), rt=0.3)
        until(self, "The project is called")
        line = L("Scoring AI-written data checks with planted defects", 0, -1.45, 44)
        G(self, FadeIn(line, shift=UP * 0.1), rt=0.6)
        finish(self)


class B00_Scanner(Scene):
    """Q1: the hero object. The scanner lands, the name lands, the table (parcel) rides under the arch."""
    def construct(self):
        rig = scanner(4.4, -1.6, -0.1)
        vec = rig.action_vectors["parcel"]
        rig.parts["parcel"].shift(vec)                     # parcel waits outside, front-left
        self.play(FadeIn(rig, shift=DOWN * 0.25), run_time=0.8)
        until(self, "Data Sentry")
        name = L("DataSentry", 3.9, 0.9, 60, bold=True)
        G(self, FadeIn(name), rt=0.4)
        until(self, "write data checks")
        tag = L("a table", 1.3, -2.45, 36)
        G(self, FadeIn(tag), rt=0.3)
        G(self, rig.parts["parcel"].animate.shift(-vec), rt=1.2, rate_func=smooth)
        until(self, "planting defects")
        dot = Dot(np.array(rig.parts["parcel"].get_center()) + np.array([0, 0.25, 0]), radius=0.1, color=TERRA).set_z_index(1.5)
        G(self, GrowFromCenter(dot), rt=0.4)
        finish(self)


class B01_Repo(Scene):
    """Q1: the artifact. The repo crate opens; the three parts rise beside it, each labelled once."""
    def construct(self):
        crate = make_original("context-crate", height=3.6, x=-3.6, y=-0.3)
        self.play(FadeIn(crate, shift=DOWN * 0.25), run_time=0.7)
        until(self, "GitHub repo")
        lr = VGroup(T("public GitHub repo", 36, bold=True), T("when done", 30)).arrange(DOWN, buff=0.08).move_to([-3.6, 2.55, 0])
        G(self, FadeIn(lr), crate.parts["lid"].animate.shift(crate.action_vectors["lid"] * 0.9), rt=0.8)
        iso = Iso(0.0, 0.0, 1.0)
        part1 = Iso(0.55, 1.35, 0.85).page(0, 0, 0, w=1.2, d=1.2)
        part2 = Iso(0.55, -0.55, 0.85).mcp(0, 0, 0, w=1.2, d=1.2, h=0.6)
        part3 = make_original("evidence-binder", height=1.25, x=0.95, y=-2.2)
        l1, l2, l3 = L("check writer", 3.9, 1.85), L("defect planter", 3.9, 0.0), L("scorecard", 3.9, -2.1)
        until(self, "a part that writes")
        G(self, FadeIn(part1, shift=UP * 0.3), FadeIn(l1), rt=0.5)
        until(self, "a defect planter")
        G(self, FadeIn(part2, shift=UP * 0.3), FadeIn(l2), rt=0.5)
        until(self, "and a scorecard")
        G(self, FadeIn(part3, shift=UP * 0.3), FadeIn(l3), rt=0.5)
        finish(self)


class B02_Table(Scene):
    """The data, as actually used in the first run: NYC yellow taxi, January 2025, a 10,000-row sample."""
    def construct(self):
        card, cols, bars = table_card(-1.3, -0.3, w=7.2, h=4.6, rows=7)
        self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.5)
        until(self, "public data")
        G(self, LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.1), rt=1.0)
        until(self, "New York City")
        l1 = L("NYC taxi \u00b7 Jan 2025", -1.3, 2.75, 40)
        G(self, FadeIn(l1), LaggedStart(*[GrowFromCenter(c) for c in cols], lag_ratio=0.1), rt=0.7)
        until(self, "ten thousand rows")
        l2 = VGroup(T("{:,}".format(RECORDED["rows"]), 48, bold=True), T("rows", 36)).arrange(DOWN, buff=0.12).move_to([4.6, -0.3, 0])
        G(self, FadeIn(l2), rt=0.35)
        finish(self)


class BSIMPLE_Spellcheck(Scene):
    """In plain words: test the rules like a spell-checker. Hide mistakes on purpose; count which are caught."""
    def construct(self):
        pg = paper(-1.6, 0.05, w=5.6, h=4.4)
        lines = tall_scribbles(pg, n=5, gap=0.72)
        self.play(FadeIn(pg, shift=DOWN * 0.2), run_time=0.6)
        self.play(Create(lines), run_time=0.8)
        spots = [(0, 0.55), (1, -0.4), (3, 0.3), (4, -0.9)]
        y0 = 0.05 + 4.4 / 2 - 0.25 - 0.15
        marks = [Dot([-1.6 + dx, y0 - i * 0.72, 0], radius=0.13, color=TERRA) for i, dx in spots]
        until(self, "hide some mistakes")
        lh = L("hidden mistakes", -1.6, 2.75, 36)
        G(self, LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.2), FadeIn(lh), rt=0.6)
        until(self, "count which ones")
        lens = Circle(radius=0.55, stroke_color=INK, stroke_width=8).move_to([-4.0, 1.2, 0])
        handle = Line([-3.6, 0.8, 0], [-3.1, 0.3, 0], color=INK, stroke_width=12)
        mag = VGroup(lens, handle)
        G(self, FadeIn(mag), rt=0.2)
        G(self, mag.animate.shift([4.6, -1.6, 0]), rt=0.8, rate_func=smooth)
        until(self, "it catches")
        ticks = VGroup(*[check(float(np.array(m.get_center())[0]) + 0.05, float(np.array(m.get_center())[1]) + 0.4, s=0.15) for m in marks[:3]])
        lc = L("caught", 3.6, 1.1, 36)
        G(self, LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.15), FadeIn(lc), rt=0.4)
        until(self, "and which slip")
        ring = Circle(radius=0.3, stroke_color=INK, stroke_width=5).move_to(np.array(marks[3].get_center()))
        ls = L("slipped through", 3.6, -1.95, 36)
        G(self, Create(ring), FadeIn(ls), rt=0.4)
        finish(self)


class B03_PipeOne(Scene):
    """Under the hood, part one (runs today): pandas loads the table; a planter breaks a copy; the answer key is locked away."""
    def construct(self):
        lt = L("Part 1", -4.9, 2.5, 44, bold=True)
        c1, h1, b1 = table_card(-4.5, 0.55, w=2.9, h=2.3, rows=4)
        G(self, FadeIn(lt), FadeIn(VGroup(c1, h1, b1), shift=DOWN * 0.2), rt=0.5)
        until(self, "Python and pandas")
        l1 = L("pandas", -4.5, -1.1)
        G(self, FadeIn(l1), rt=0.3)
        until(self, "A planter script")
        a1 = Line([-2.8, 0.55, 0], [-1.55, 0.55, 0], color=INK, stroke_width=6)
        block = Iso(-0.6, -0.25, 0.95).mcp(0, 0, 0, w=1.3, d=1.3, h=0.8)
        l2 = L("planter", -0.6, -1.1)
        G(self, Create(a1), rt=0.4)
        G(self, FadeIn(block, shift=DOWN * 0.3), FadeIn(l2), rt=0.5)
        until(self, "breaks")
        a2 = Line([0.45, 0.55, 0], [1.7, 0.55, 0], color=INK, stroke_width=6)
        c2, h2, b2 = table_card(3.45, 0.55, w=2.9, h=2.3, rows=4)
        marks = VGroup(*[Dot(np.array(b.get_right()) + np.array([-0.3, 0, 0]), radius=0.1, color=TERRA) for b in b2[1:3]])
        G(self, Create(a2), rt=0.4)
        G(self, FadeIn(VGroup(c2, h2, b2), shift=DOWN * 0.2), rt=0.5)
        G(self, LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.3), rt=0.5)
        until(self, "answer key")
        vault = make_original("secure-vault", height=1.5, x=3.45, y=-1.85)
        l3 = L("answer key", 0.9, -1.95)
        G(self, FadeIn(vault, shift=DOWN * 0.2), FadeIn(l3), rt=0.5)
        finish(self)


class B04_PipeTwo(Scene):
    """Under the hood, part two (next): Claude Code writes pandera checks from column names only; the checks run on
    both copies; the scorer compares flags with the answer key, per defect type."""
    def construct(self):
        lt = L("Part 2", -4.9, 2.5, 44, bold=True)
        ws = make_original("agent-workstation", height=2.4, x=-4.7, y=0.55)
        G(self, FadeIn(lt), FadeIn(ws, shift=DOWN * 0.2), rt=0.5)
        l1 = VGroup(T("Claude", 36), T("Opus 5.5", 32)).arrange(DOWN, buff=0.06).move_to([-4.7, -1.4, 0])
        self.play(FadeIn(l1), run_time=0.3)
        until(self, "wrote pandera checks")
        a1 = Line([-3.3, 0.55, 0], [-2.3, 0.55, 0], color=INK, stroke_width=6)
        pages = VGroup(*[Iso(-1.45, -0.2 + i * 0.28, 0.75).page(0, 0, 0, w=1.3, d=1.4) for i in range(3)])
        l2 = L("pandera checks", -1.45, -1.2)
        G(self, Create(a1), rt=0.35)
        G(self, LaggedStart(*[FadeIn(pg, shift=DOWN * 0.3) for pg in pages], lag_ratio=0.3), FadeIn(l2), rt=0.8)
        until(self, "every broken copy")
        a2 = Line([-0.4, 0.55, 0], [0.6, 0.55, 0], color=INK, stroke_width=6)
        cc, hc, bc = table_card(1.75, 1.35, w=1.9, h=1.4, rows=3)
        cb, hb, bb = table_card(1.75, -0.45, w=1.9, h=1.4, rows=3)
        dot = Dot(np.array(bb[1].get_right()) + np.array([-0.2, 0, 0]), radius=0.09, color=TERRA)
        G(self, Create(a2), rt=0.35)
        G(self, FadeIn(VGroup(cc, hc, bc)), FadeIn(VGroup(cb, hb, bb)), rt=0.5)
        G(self, GrowFromCenter(dot), rt=0.3)
        until(self, "a scorer")
        a3 = Line([2.9, 0.45, 0], [3.8, 0.45, 0], color=INK, stroke_width=6)
        binder = make_original("evidence-binder", height=1.6, x=4.95, y=0.55)
        l3 = L("scorer", 4.95, -1.2)
        G(self, Create(a3), rt=0.35)
        G(self, FadeIn(binder, shift=DOWN * 0.2), FadeIn(l3), rt=0.5)
        until(self, "one defect type")
        ok = check(4.5, -1.95, s=0.2)
        miss = Dot([5.45, -1.95, 0], radius=0.12, color=TERRA)
        G(self, Create(ok), GrowFromCenter(miss), rt=0.4)
        finish(self)


class B06_Dbt(Scene):
    """Alternative 1, run for real: the same rule as a dbt test (dbt-duckdb). Recorded output, typeset."""
    def construct(self):
        d = RECORDED["dbt"]
        texts = ["$ dbt build        rule: fare_amount >= 0",
                 "{:<9}{}".format(d["clean"]["status"], d["clean"]["test"]),
                 "{:<9}{}".format(d["broken"]["status"], d["broken"]["test"])]
        win, (l0, l1, l2) = panel(texts, 0.0, 0.35, size=26, gap=0.6)
        lt = L("dbt", -4.9, 2.5, 44, bold=True)
        self.play(FadeIn(win, shift=DOWN * 0.2), FadeIn(lt), run_time=0.6)
        self.play(FadeIn(l0), run_time=0.3)
        until(self, "passed the clean")
        G(self, FadeIn(l1), Create(mark_after(l1, True)), rt=0.4)
        until(self, "failed twenty-five")
        G(self, FadeIn(l2), GrowFromCenter(mark_after(l2, False)), rt=0.4)
        G(self, FadeIn(recorded_tag(0.0, -1.65)), rt=0.3)
        finish(self)


class B07_Gx(Scene):
    """Alternative 2, run for real: the same rule in GX Core. GX Cloud's ExpectAI (paid) is named, not run."""
    def construct(self):
        g = RECORDED["gx"]
        texts = ["ExpectColumnValuesToBeBetween(",
                 "    fare_amount, min_value=0)",
                 "clean copy   {:,} rows   {}".format(g["clean"]["rows"], "PASS" if g["clean"]["success"] else "FAIL"),
                 "broken copy  {:,} rows   FAIL {} unexpected".format(g["broken"]["rows"], g["broken"]["unexpected_count"])]
        win, (l0, la, l1, l2) = panel(texts, 0.0, 0.35, size=26, gap=0.6)
        lt = L("GX Core " + RECORDED["gx_version"], -3.6, 2.75, 40, bold=True)
        self.play(FadeIn(win, shift=DOWN * 0.2), FadeIn(lt), run_time=0.6)
        self.play(FadeIn(l0), FadeIn(la), run_time=0.3)
        until(self, "pass, then")
        G(self, FadeIn(l1), Create(mark_after(l1, True)), rt=0.4)
        until(self, "twenty-five unexpected")
        G(self, FadeIn(l2), GrowFromCenter(mark_after(l2, False)), rt=0.4)
        until(self, "tested that same idea")
        G(self, FadeIn(L("ExpectAI's idea, tested with Claude", 0.0, -2.15, 32)), rt=0.3)
        finish(self)


class B08_Gap(Scene):
    """The gap, shown: all three tools flag the 25 fares; only the answer key shows 25 time-travel trips got through."""
    def construct(self):
        d, g, sc = RECORDED["dbt"], RECORDED["gx"], RECORDED["score"]
        rows = [("tool", "clean", "broken"),
                ("pandera", "PASS" if RECORDED["clean_pass"] else "FAIL", "FAIL {}".format(RECORDED["broken_flagged"])),
                ("dbt", d["clean"]["status"], d["broken"]["status"]),
                ("GX Core", "PASS" if g["clean"]["success"] else "FAIL", "FAIL {}".format(g["broken"]["unexpected_count"]))]
        texts = ["{:<10}{:<9}{}".format(*r) for r in rows] + [
            "answer key",
            "negative fares            {}/{}  {}".format(sc["negative_fare"]["caught"], sc["negative_fare"]["planted"], sc["negative_fare"]["verdict"]),
            "drop-off before pick-up    {}/{}  {}".format(sc["dropoff_before_pickup"]["caught"], sc["dropoff_before_pickup"]["planted"], sc["dropoff_before_pickup"]["verdict"])]
        win, lines = panel(texts, 0.0, 0.2, size=24, gap=0.52)
        self.play(FadeIn(win, shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(VGroup(*lines[:4])), run_time=0.5)
        until(self, "had planted")
        G(self, FadeIn(lines[4]), FadeIn(lines[5]), Create(mark_after(lines[5], True)), rt=0.5)
        until(self, "None of the three")
        G(self, FadeIn(lines[6]), GrowFromCenter(mark_after(lines[6], False)), rt=0.5)
        G(self, FadeIn(recorded_tag(0.0, -2.95)), rt=0.3)
        finish(self)


class B09_FirstMinute(Scene):
    """Who opens it + the real scorecard: one hand-written rule vs Claude (Opus 5.5) round 1 and round 2. Recorded output."""
    def construct(self):
        sc = RECORDED["scored"]
        hw, r1, r2 = sc["hand-written-baseline"], sc["claude-round1"], sc["claude-round2"]
        def clean_cell(x):
            if x["clean_crashed"]:
                return "1 check crashes" if x["clean_crashed"] == 1 else "%d checks crash" % x["clean_crashed"]
            return "PASS" if not x["clean_rows"] else "%d rows flagged" % x["clean_rows"]
        texts = ["$ ./score_round.sh",
                 "{:<23}{:<19}{}".format("checks", "clean copy", "caught"),
                 "{:<23}{:<19}{} of 5".format("hand-written, 1 rule", clean_cell(hw), hw["types_caught"]),
                 "{:<23}{:<19}{} of 5".format("Claude, round 1", clean_cell(r1), r1["types_caught"]),
                 "{:<23}{:<19}{} of 5".format("Claude, round 2", clean_cell(r2), r2["types_caught"]),
                 "round 2 negative fares  {}  {}".format(r2["neg"], r2["types"]["negative_fare"])]
        win, lines = panel(texts, 0.0, -0.3, size=24, gap=0.55)
        self.play(FadeIn(win, shift=DOWN * 0.2), run_time=0.6)
        lh = L("hiring manager", -3.4, 2.75)
        self.play(FadeIn(lh), run_time=0.3)
        until(self, "One command")
        G(self, FadeIn(lines[0]), FadeIn(lines[1]), rt=0.3)
        until(self, "hand-written rule")
        G(self, FadeIn(lines[2]), rt=0.3)
        until(self, "Claude's first checks")
        G(self, FadeIn(lines[3]), rt=0.4)
        until(self, "Its revision")
        G(self, FadeIn(lines[4]), FadeIn(lines[5]), GrowFromCenter(mark_after(lines[5], False)), rt=0.4)
        G(self, FadeIn(L("Claude Opus 5.5 \u00b7 recorded output \u00b7 " + RECORDED["date"], 0.0, -2.95, 30)), rt=0.3)
        finish(self)


class B10_Proves(Scene):
    """What it proves: the evidence binder opens; four record sheets land in a row, numbered 1 to 4."""
    def construct(self):
        binder = make_original("evidence-binder", height=2.4, x=-4.4, y=0.0)
        self.play(FadeIn(binder, shift=DOWN * 0.2), run_time=0.6)
        G(self, binder.parts["cover"].animate.shift(binder.action_vectors["cover"] * 0.8), rt=0.6)
        xs = [-1.2, 0.75, 2.7, 4.65]
        sheets = [paper(x, 0.35, w=1.5, h=2.0) for x in xs]
        nums = [L(str(i + 1), x, -1.15, 44, bold=True) for i, x in enumerate(xs)]
        for phrase, sh, n in zip(["a prompt contract", "a two-round loop", "a clean-copy control", "a catch rate"], sheets, nums):
            until(self, phrase)
            G(self, FadeIn(sh, shift=DOWN * 0.3), FadeIn(n), rt=0.4)
            G(self, Create(tall_scribbles(sh, n=3, gap=0.5)), rt=0.4)
        until(self, "I test an AI")
        lt = L("tested, not trusted", 1.75, -2.45, 40)
        ok = check(-0.55, -2.4, s=0.22)
        G(self, FadeIn(lt), Create(ok), rt=0.5)
        finish(self)


class B11_Scope(Scene):
    """Scope: three things drop into the 'in' box; Airflow stays outside; the first run prints one line."""
    def construct(self):
        iso, back, front = tray(-2.6, -1.4, s=1.0, w=2.8, d=2.8, h=0.9)
        self.play(FadeIn(VGroup(back, front), shift=DOWN * 0.2), run_time=0.5)
        li = L("in scope", -2.6, 2.6)
        self.play(FadeIn(li), run_time=0.3)
        until(self, "one table")
        pg = Iso(-2.6, -1.4, 1.0).page(1.4, 1.3, 0.02, w=1.2, d=1.2).set_z_index(1.0)
        G(self, FadeIn(pg, shift=DOWN * 0.6), rt=0.35, rate_func=ease_in)
        until(self, "five defect types")
        pk = parcel(iso, 1.5, 0.3, 0.02, w=0.9, d=0.9, h=0.6, flaw=True).set_z_index(1.1)
        G(self, FadeIn(pk, shift=DOWN * 0.6), rt=0.35, rate_func=ease_in)
        until(self, "one scorecard")
        bk = block_in(iso, 0.3, 1.5, w=0.9, d=0.9, h=0.4, dark=True)
        G(self, FadeIn(bk, shift=DOWN * 0.6), rt=0.35, rate_func=ease_in)
        until(self, "orchestration")
        stack, lights = Iso(3.6, -0.6, 0.9).server(0, 0, 0, w=1.3, d=1.3, slab=0.42, n=3)
        la = L("Airflow: out", 3.6, -1.9)
        G(self, FadeIn(VGroup(stack, lights), shift=DOWN * 0.2), FadeIn(la), rt=0.5)
        until(self, "The first piece")
        slip = paper(-2.6, -2.75, w=3.4, h=0.7)
        line = scribble(-3.9, -2.75, 2.0, amp=0.05)
        G(self, FadeIn(slip, shift=DOWN * 0.15), rt=0.35)
        G(self, Create(line), rt=0.5)
        ok = check(-0.45, -2.7, s=0.2)
        lf = L("ran " + RECORDED["date"], 1.4, -2.75)
        G(self, Create(ok), FadeIn(lf), rt=0.4)
        finish(self)


class B12_Loose(Scene):
    """The risk: with the barrier up (a loose check), a broken parcel rides straight through; then it comes down."""
    def construct(self):
        gate = make_original("permission-gate", height=3.8, x=-0.6, y=0.1)
        up = np.array(gate.action_vectors["barrier"])
        gate.parts["barrier"].shift(up)
        gate.parts["posts"].set_z_index(2); gate.parts["barrier"].set_z_index(2.2)
        self.play(FadeIn(gate, shift=DOWN * 0.2), run_time=0.6)
        lt = L("too loose", 4.3, 2.2)
        self.play(FadeIn(lt), run_time=0.3)
        centre = np.array(gate.parts["base"].get_center(), dtype=float)
        along = np.array([-0.866, 0.5, 0.0])          # iso y axis: through the opening, front to back

        def crate_at(pt):
            c = parcel(Iso(float(pt[0]), float(pt[1]) - 0.54, 0.6), 0, 0, 0, flaw=True)
            c.set_z_index(1)
            return c
        until(self, "too loose")
        bad = crate_at(centre - along * 1.9)
        G(self, FadeIn(bad), rt=0.3)
        G(self, bad.animate.shift(along * 2.9), rt=1.6, rate_func=linear)
        G(self, FadeOut(bad), rt=0.4)
        until(self, "So the clean")
        G(self, gate.parts["barrier"].animate.shift(-up), rt=0.6)
        bad2 = crate_at(centre - along * 2.7)
        bad2.set_z_index(3)
        G(self, FadeIn(bad2), rt=0.3)
        G(self, bad2.animate.shift(along * 1.6), rt=0.8, rate_func=smooth)
        lb = L("both copies", 4.3, -1.6)
        G(self, FadeIn(lb), rt=0.3)
        finish(self)


class B13_Why(Scene):
    """Why this project: in the Food Inspections Dataset Project my checks let bad rows through -> DataSentry measures which ones; new skills vs done before."""
    def construct(self):
        card, cols, bars = table_card(-3.9, 0.1, w=4.4, h=3.6, rows=5)
        self.play(FadeIn(VGroup(card, cols, bars), shift=DOWN * 0.2), run_time=0.6)
        ld = VGroup(T("Food Inspections", 38, bold=True), T("Dataset Project", 38, bold=True)).arrange(DOWN, buff=0.08).move_to([-3.9, 2.5, 0])
        self.play(FadeIn(ld), run_time=0.3)
        until(self, "let bad rows through")
        spots = [(0, 0.55), (1, -0.35), (2, 0.9), (3, 0.1), (4, -0.75)]
        marks = VGroup(*[Dot(np.array(bars[i].get_center()) + np.array([dx, 0, 0]), radius=0.11, color=TERRA) for i, dx in spots])
        G(self, LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.2), rt=0.9)
        until(self, "Data Sentry measures")
        arrow = Line([-1.3, 0.1, 0], [0.9, 0.1, 0], color=INK, stroke_width=7)
        tip = Dot([1.0, 0.1, 0], radius=0.12, color=TERRA)
        G(self, Create(arrow), rt=0.5)
        G(self, GrowFromCenter(tip), rt=0.25)
        until(self, "It's a mix")
        new = VGroup(T("New to me", 38, bold=True), T("pandera, dbt,", 34), T("GX, Claude", 34)).arrange(DOWN, buff=0.12).move_to([3.7, 1.15, 0])
        G(self, FadeIn(new, shift=DOWN * 0.15), rt=0.5)
        until(self, "Working with messy")
        done = VGroup(T("Done before", 38, bold=True), T("messy public data", 34)).arrange(DOWN, buff=0.12).move_to([3.7, -1.3, 0])
        G(self, FadeIn(done, shift=DOWN * 0.15), rt=0.5)
        finish(self)


class B14_Exists(Scene):
    """Exists today vs will exist: three real pages land on the left; three empty slots stay on the right."""
    def construct(self):
        divider = Line([0, 2.2, 0], [0, -2.4, 0], color=INK, stroke_width=4)
        date = L(RECORDED["date"], 0, 2.8, 36)
        self.play(Create(divider), FadeIn(date), run_time=0.5)
        le = L("exists", -3.1, -2.75, 40)
        lw = L("will exist", 3.1, -2.75, 40)
        xs = [-4.9, -3.1, -1.3]
        for phrase, x in zip(["this pitch", "the five-defect planter", "two rounds"], xs):
            until(self, phrase)
            pg = paper(x, -0.2, w=1.5, h=2.1)
            G(self, FadeIn(pg, shift=DOWN * 0.3), rt=0.35)
            G(self, Create(tall_scribbles(pg, n=3, gap=0.55)), rt=0.4)
            if x == xs[0]:
                G(self, FadeIn(le), rt=0.3)
        for phrase, x in zip(["the public repo", "a loop that runs"], [1.3, 3.1]):
            until(self, phrase)
            slot = RoundedRectangle(width=1.5, height=2.1, corner_radius=0.08, fill_color=BAR1, fill_opacity=1,
                                    stroke_color=INK, stroke_width=4).move_to([x, -0.2, 0])
            G(self, FadeIn(slot), rt=0.35)
            if x == 1.3:
                G(self, FadeIn(lw), rt=0.3)
        finish(self)


class BEND_Close(Scene):
    """Close: the scanner returns; the title and Ethan's name land beside it."""
    def construct(self):
        rig = scanner(3.8, -3.2, -0.1)
        vec = rig.action_vectors["parcel"]
        rig.parts["parcel"].shift(vec)
        self.play(FadeIn(rig, shift=DOWN * 0.2), run_time=0.4)
        title = L("DataSentry", 2.4, 0.5, 64, bold=True)
        name = L("Ethan Gomes", 2.4, -0.55, 40)
        self.play(FadeIn(title), run_time=0.35)
        self.play(FadeIn(name), run_time=0.35)
        G(self, rig.parts["parcel"].animate.shift(-vec), rt=0.8, rate_func=smooth)
        light = Dot(np.array(rig.parts["parcel"].get_center()) + np.array([0, 0.22, 0]), radius=0.09, color=TERRA).set_z_index(1.5)
        G(self, GrowFromCenter(light), rt=0.3)
        finish(self)
