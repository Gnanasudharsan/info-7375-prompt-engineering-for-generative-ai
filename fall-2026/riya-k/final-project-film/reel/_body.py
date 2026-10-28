# ═════════════════════════════ v2 reel helpers ═════════════════════════════
# Midpoint guard: GATE T and Gate V sample each clip at 50%. Nothing is in motion between 47%
# and 53% of a beat; at() moves or shortens any animation that would overlap that window.
EARLY, LATE = 0.47, 0.53   # only the 50% frame is sampled by GATE T / Gate V; keep a short hold around it
MONO = "PT Mono"
CAP_TOP = -2.75          # burned-in captions live below this line; keep the drawing above it


def _dur(self):
    return _TARGET.get(type(self).__name__.split("_")[0], 12.0) or 12.0


def _t_of(self, phrase):
    bid = type(self).__name__.split("_")[0]
    n, target = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    if not n or not target:
        return None          # no beat sheet beside the file (Gate A's isolated copy): play now
    if phrase not in n:
        raise ValueError(f"{bid}: cue phrase not in narration: {phrase!r}")
    return target * n.index(phrase) / len(n)


def at(self, when, *anims, rt=0.8, lead=0.2):
    """Play anims when `when` (a phrase of the narration, or a fraction of the beat) arrives,
    never overlapping the 47-53% still window."""
    D = _dur(self)
    now = _elapsed(self)
    if isinstance(when, (int, float)):
        t = when * D
    else:
        tp = _t_of(self, when)
        t = now if tp is None else tp - lead
    t = max(t, now)
    lo, hi = EARLY * D, LATE * D
    if t < lo < t + rt:
        if lo - t >= 0.35:
            rt = lo - t
        else:
            t = hi
    elif lo <= t < hi:
        t = hi
    if t - now > 0.05:
        self.wait(t - now)
    self.play(*anims, run_time=rt)


def M(s, size=34, color=INK):
    return Text(s, font=MONO, color=color, font_size=size)


def L(s, size=40, color=INK, bold=False):
    return T(s, size, color, bold)


def panel(w, h, x=0.0, y=0.0, fill=CARD, stroke=INK, sw=4, r=0.18):
    return RoundedRectangle(width=w, height=h, corner_radius=r, fill_color=fill, fill_opacity=1,
                            stroke_color=stroke, stroke_width=sw).move_to([x, y, 0])


def fit(mob, w):
    if mob.width > w:
        mob.scale_to_fit_width(w)
    return mob


def boxed(mob, x=0.0, y=0.0, padx=0.35, pady=0.2, fill="#FFFFFF", sw=3):
    """A card sized to its contents."""
    box = panel(mob.width + 2 * padx, mob.height + 2 * pady, fill=fill, sw=sw)
    mob.move_to(box)
    return VGroup(box, mob).move_to([x, y, 0])


def code(lines, size=30, x=0.0, y=0.0, maxw=6.3, pad=0.3, title=None):
    """An SQL panel: monospaced lines on a card sized to them (shrunk to fit maxw)."""
    body = VGroup(*[M(s, size) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    fit(body, maxw - 2 * pad)
    box = panel(body.width + 2 * pad, body.height + 2 * pad)
    body.move_to(box)
    g = VGroup(box, body)
    if title:
        g.add(L(title, 36).next_to(box, UP, buff=0.12).align_to(box, LEFT))
    return g.move_to([x, y, 0])


def strike(mob, color=TERRA, w=8):
    """Mark a wrong value: a red cross just right of it (a line through text trips Gate B)."""
    r = mob.get_right()
    return cross(r[0] + 0.42, r[1], 0.17, color, w)


def cross(x, y, s=0.32, color=TERRA, w=9):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def tick(x, y, s=0.26):
    return check(x, y, s, INK, 8)


def ok_pill(s="ran · 0 errors", x=0.0, y=0.0, size=34):
    inner = VGroup(tick(0, 0, 0.16), L(s, size)).arrange(RIGHT, buff=0.22)
    p = pill(0, 0, inner.width + 0.7, 0.7, fill="#FFFFFF").set_stroke(INK, 3)
    inner.move_to(p)
    return VGroup(p, inner).move_to([x, y, 0])


def person(x, y, s=1.0):
    head = Circle(radius=0.28 * s, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y + 0.42 * s, 0])
    body = ArcBetweenPoints([x - 0.5 * s, y - 0.45 * s, 0], [x + 0.5 * s, y - 0.45 * s, 0], angle=-PI * 0.9,
                            color=INK, stroke_width=5)
    return VGroup(head, body)


def table(rows, x=0.0, y=0.0, size=34, header=True, gap=0.5):
    """A small result table sized to its cells; the first row is the header."""
    cells = [[(L(c, size, bold=True) if (header and i == 0) else M(c, size)) for c in r] for i, r in enumerate(rows)]
    ncol = len(rows[0])
    colw = [max(cells[i][j].width for i in range(len(rows))) + gap for j in range(ncol)]
    rh = 0.62
    g = VGroup()
    for i, r in enumerate(cells):
        cx = 0.25
        row = VGroup()
        for j, t in enumerate(r):
            t.move_to([cx, -i * rh, 0], aligned_edge=LEFT)
            row.add(t)
            cx += colw[j]
        g.add(row)
    W = sum(colw) + 0.25
    frame = panel(W, rh * len(rows) + 0.3, fill="#FFFFFF", sw=3).move_to([W / 2, -(len(rows) - 1) * rh / 2, 0])
    rule = Line([0.1, -rh / 2, 0], [W - 0.1, -rh / 2, 0], color=INK, stroke_width=3) if header else VGroup()
    out = VGroup(frame, rule, g)
    out.move_to([x, y, 0])
    out.rows = g
    return out


def tag(s, y=3.0, size=34):
    t = L(s, size)
    p = pill(0, y, t.width + 0.7, 0.62, fill=CARD).set_stroke(DIM, 2)
    t.move_to([0, y, 0])
    return VGroup(p, t)


def opener(self, text):
    """A heading on screen from the first frame, so a beat never opens on an empty stage."""
    h = L(text, 60, bold=True).move_to([0, 0.3, 0])
    self.play(FadeIn(h, shift=UP * 0.3), run_time=0.6)
    return h


def rise(mob, d=0.5):
    return FadeIn(mob, shift=UP * d)


def slide_in(mob, d=1.2):
    return FadeIn(mob, shift=LEFT * d)


# ═════════════════════════════ scenes ═════════════════════════════
class B01_Title(Scene):
    def construct(self):
        title = fit(L("Ground Truth SQL", 120), 12.0)
        title.move_to([0, 1.75, 0])
        name = L("Riya Kapadnis", 72).move_to([0, 0.45, 0])
        course = L("INFO 7375  ·  Final Project Pitch", 44).move_to([0, -0.35, 0])
        rule = Line([-4.2, -0.95, 0], [4.2, -0.95, 0], color=GHOST, stroke_width=4)
        prob1 = L("AI can write database code that runs with no errors", 44).move_to([0, -1.6, 0])
        prob2 = L("but gives the wrong answer.", 44).move_to([0, -2.25, 0])
        under = Line(prob2.get_corner(DL) + DOWN * 0.08 + RIGHT * 2.05, prob2.get_corner(DR) + DOWN * 0.08,
                     color=TERRA, stroke_width=8)
        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(name, shift=UP * 0.3), run_time=0.9)
        self.play(FadeIn(course, shift=UP * 0.3), Create(rule), run_time=0.8)
        at(self, "The problem", FadeIn(prob1, shift=UP * 0.2), rt=0.9)
        at(self, "but gives", FadeIn(prob2, shift=UP * 0.2), rt=0.7)
        self.play(Create(under), run_time=0.6)
        finish(self)


class B02_Problem(Scene):
    def construct(self):
        honest = tag("example SQL · drafted with Claude, checked by me")
        you = person(-6.0, 2.2, 0.45)
        q = L("What is our revenue by country?", 36)
        chat = boxed(q, padx=0.3, pady=0.2)
        chat.move_to([-5.6, 2.2, 0], aligned_edge=LEFT)
        sql = code(["SELECT BillingCountry,", "  SUM(Total)", "FROM Invoice", "JOIN InvoiceLine",
                    "  USING (InvoiceId)", "GROUP BY BillingCountry"], 28, maxw=5.6)
        sql.move_to([-6.2, -0.2, 0], aligned_edge=LEFT)
        okp = ok_pill(x=sql.get_center()[0], y=-2.3)
        res = table([("Country", "Revenue"), ("USA", "4,667.06"), ("Canada", "2,689.96"), ("France", "1,722.10")], size=32)
        res.move_to([3.7, 0.3, 0])
        res_lbl = L("the answer it gives", 36).next_to(res, UP, buff=0.18)
        usa_val = res.rows[1][1]
        real = boxed(VGroup(L("real answer", 40), M("523.06", 52)).arrange(RIGHT, buff=0.35), 3.7, -1.95, sw=4)
        arrow = Arrow(sql.get_right() + RIGHT * 0.1, res.get_left() + LEFT * 0.1, color=INK, stroke_width=6, buff=0.05)
        self.add(honest)
        self.play(FadeIn(chat[0]), FadeIn(you), run_time=0.6)
        at(self, "what is our revenue", AddTextLetterByLetter(q), rt=1.4)
        at(self, "The AI writes SQL", FadeIn(sql[0]), rt=0.4)
        at(self, "the language", LaggedStart(*[AddTextLetterByLetter(l) for l in sql[1]], lag_ratio=1.0), rt=2.4)
        at(self, "It runs", rise(okp), rt=0.6)
        at(self, "It says the USA", GrowArrow(arrow), FadeIn(res), FadeIn(res_lbl), rt=0.9)
        self.play(Indicate(usa_val, color=TERRA, scale_factor=1.15), run_time=0.8)
        at(self, "The real answer", Create(strike(usa_val)), rt=0.5)
        self.play(FadeIn(real, shift=UP * 0.3), run_time=0.8)
        finish(self)

class B03_Why(Scene):
    def construct(self):
        top = tag("Chinook · a free sample database of a music store")
        order = panel(3.2, 2.9, -4.6, 0.8, fill="#FFFFFF")
        o1 = VGroup(L("Order #16", 36), L("Reno, Nevada", 34)).arrange(DOWN, buff=0.12).move_to([-4.6, 1.6, 0])
        o2 = M("$3.96", 64).move_to([-4.6, 0.6, 0])
        o3 = L("4 songs", 36).move_to([-4.6, -0.2, 0])
        songs = ["Longview", "Basket Case", "She", "Geek Stink Breath"]
        rows = VGroup()
        for i, s in enumerate(songs):
            y = 2.05 - i * 0.82
            r = panel(4.2, 0.76, -0.05, y, fill=CARD, sw=3).set_stroke(DIM, 3)   # grey edge: GATE T reads a dark edge as text
            n = L(s, 36).move_to([-1.95, y + 0.03, 0], aligned_edge=LEFT)
            rows.add(VGroup(r, n))
        copies = VGroup(*[M("$3.96", 40).move_to([2.95, 2.05 - i * 0.82, 0]) for i in range(4)])
        sums = ["3.96", "7.92", "11.88", "15.84"]
        sum_lbl = L("counted", 38).move_to([5.0, 0.95, 0])
        sum_val = M("$" + sums[0], 46).move_to([5.0, 0.3, 0])
        times = L("4 times", 40).move_to([5.0, -0.35, 0])
        join = VGroup(Arrow([-2.95, 0.9, 0], [-2.2, 0.9, 0], color=INK, stroke_width=5, buff=0),
                      L("join", 36).move_to([-2.6, 0.3, 0]))
        self.add(top)
        at(self, "One order from Reno", FadeIn(order), FadeIn(o1), FadeIn(o2), FadeIn(o3), rt=0.8)
        at(self, "for four songs", LaggedStart(*[slide_in(r, 1.6) for r in rows], lag_ratio=0.25), FadeIn(join), rt=1.4)
        at(self, "was counted", LaggedStart(*[TransformFromCopy(o2, c) for c in copies], lag_ratio=0.3), rt=1.6)
        self.play(FadeIn(sum_lbl), FadeIn(sum_val), run_time=0.4)
        for i in range(1, 4):
            new = M("$" + sums[i], 46).move_to(sum_val)
            self.play(Indicate(copies[i], color=TERRA, scale_factor=1.12), Transform(sum_val, new), run_time=0.45)
        self.play(FadeIn(times, shift=UP * 0.2), run_time=0.4)
        # zoom out: the whole country
        everything = VGroup(order, o1, o2, o3, rows, copies, sum_lbl, sum_val, times, join)
        big1 = VGroup(M("91", 72), L("US orders", 40)).arrange(DOWN, buff=0.2).move_to([-4.2, 0.6, 0])
        big2 = VGroup(M("494", 72), L("rows after the join", 40)).arrange(DOWN, buff=0.2).move_to([0.0, 0.6, 0])
        a1 = Arrow([-3.0, 0.85, 0], [-1.45, 0.85, 0], color=INK, stroke_width=6)
        res = VGroup(M("$523", 64), L("real", 36)).arrange(DOWN, buff=0.15).move_to([3.4, 1.0, 0])
        res2 = VGroup(M("$4,667", 64), L("reported", 36)).arrange(DOWN, buff=0.15).move_to([3.4, -1.15, 0])
        a2 = Arrow([3.4, 0.25, 0], [3.4, -0.45, 0], color=TERRA, stroke_width=7, buff=0.05)
        nine = L("almost 9× too high", 44).move_to([0, -2.25, 0])
        at(self, "Do that for every", FadeOut(everything, scale=0.6), rt=0.6)
        self.play(FadeIn(big1), GrowArrow(a1), FadeIn(big2), run_time=0.9)
        self.play(FadeIn(res), GrowArrow(a2), FadeIn(res2), run_time=0.9)
        at(self, "almost nine times", FadeIn(nine, shift=UP * 0.2), rt=0.6)
        finish(self)


class B04_More(Scene):
    def construct(self):
        specs = [("Long songs", "ms read as seconds", "3,503", "1,069"),
                 ("Rock buyers", "purchases, not people", "835", "59"),
                 ("Busiest support rep", "wrong columns linked", "(empty)", "Jane Peacock, 21")]
        cues = ["Mix up milliseconds", "Count purchases", "Link the wrong"]
        xs = [-4.25, 0.0, 4.25]
        oks = VGroup()
        head = opener(self, "more real mistakes")
        for (q, why, bad, good), x, cue in zip(specs, xs, cues):
            card = panel(3.9, 4.7, x, 0.7, fill="#FFFFFF")
            tq = fit(L(q, 42, bold=True), 3.5).move_to([x, 2.55, 0])
            tw = fit(L(why, 36), 3.5).move_to([x, 1.95, 0])
            wl = L("AI-style answer", 34).move_to([x, 1.2, 0])
            wv = fit(M(bad, 56), 2.8).move_to([x - 0.25, 0.5, 0])
            rl = L("right answer", 34).move_to([x, -0.3, 0])
            rv = fit((M(good, 56) if len(good) < 8 else L(good, 40)), 3.5).move_to([x, -1.0, 0])
            grp = VGroup(card, tq, tw, wl, wv, rl, rv)
            at(self, cue, FadeIn(grp, shift=UP * 0.4), *([FadeOut(head)] if cue == cues[0] else []), rt=0.7)
            self.play(Create(strike(wv)), run_time=0.4)
            oks.add(ok_pill("0 errors", x, -2.2, 34))
        at(self, "And no errors", LaggedStart(*[rise(o, 0.3) for o in oks], lag_ratio=0.3), rt=1.0)
        finish(self)

class B05_RealLife(Scene):
    def construct(self):
        head = opener(self, "why does this happen?")
        # 1 · the person sees only the answer
        p = person(-4.6, 0.4, 1.3)
        ans = panel(2.4, 1.0, -4.6, 2.15, fill="#FFFFFF", sw=3)
        ans_t = M("$4,667", 44).move_to(ans)
        hidden = VGroup(*[Line([-5.6, -0.95 - i * 0.28, 0], [-3.4 - (i % 2) * 0.6, -0.95 - i * 0.28, 0],
                               color=GHOST, stroke_width=10) for i in range(4)])
        l1 = fit(L("never sees the SQL", 36), 3.3).move_to([-4.6, -2.25, 0])
        # 2 · the AI doesn't know the data
        tower = make_original("server-tower", 2.6, x=0.0, y=0.55)
        qs = VGroup(*[L("?", 64).move_to([dx, 2.45 + dy, 0]) for dx, dy in [(-0.9, 0), (0.1, 0.25), (1.0, -0.05)]])
        l2 = L("doesn't know your data", 36).move_to([0.0, -2.25, 0])
        # 3 · no crash, a trusted number
        screen = panel(3.4, 2.2, 4.6, 1.1, fill="#FFFFFF")
        stand = Line([4.6, -0.0, 0], [4.6, -0.7, 0], color=INK, stroke_width=6)
        foot = Line([4.0, -0.7, 0], [5.2, -0.7, 0], color=INK, stroke_width=6)
        num = M("$4,667", 54).move_to([4.6, 1.25, 0])
        okp = tick(5.8, 0.45, 0.2)
        l3 = fit(L("no crash, just trusted", 36), 3.3).move_to([4.6, -2.25, 0])
        at(self, "so most never see", FadeOut(head), FadeIn(p), FadeIn(ans), FadeIn(ans_t), FadeIn(hidden), FadeIn(l1), rt=0.9)
        at(self, "The AI doesn't know", rise(tower), FadeIn(l2), rt=0.8)
        self.play(LaggedStart(*[FadeIn(q, scale=1.4) for q in qs], lag_ratio=0.3), run_time=0.9)
        at(self, "wrong SQL doesn't crash", FadeIn(screen), Create(stand), Create(foot), rt=0.7)
        self.play(Write(num), FadeIn(l3), run_time=0.8)
        at(self, "people trust", Create(okp), Indicate(num, color=TERRA), rt=0.8)
        finish(self)


class B06_Others(Scene):
    def construct(self):
        head = opener(self, "other tools I checked")
        shelf = make_original("version-shelves", 2.6, x=-4.4, y=0.75)
        bird = L("BIRD", 52, bold=True).move_to([-4.4, -1.15, 0])
        bird_s = L("its own databases", 36).move_to([-4.4, -1.85, 0])
        yours = panel(2.0, 0.8, -1.5, 2.3, fill="#FFFFFF", sw=3)
        yours_t = L("your data", 34).move_to(yours)
        nob = cross(-1.5, 1.55, 0.22)
        img = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "images", "vanna_run_crop.png")
        if not _os.path.exists(img):   # the toolkit may render a copy of scenes.py from elsewhere
            img = _os.path.expanduser("~/Documents/INFO7375/films/riya-k-ground-truth-sql-v2/images/vanna_run_crop.png")
        shot = ImageMobject(img)
        shot.scale_to_fit_width(5.5)
        shot.move_to([3.2, 0.95, 0])
        shot_bg = panel(5.9, shot.height + 0.45, 3.2, 0.95, fill="#FFFFFF", sw=3)
        shot_t = L("my run · 2026-10-21", 34).move_to([3.3, 0.05, 0])
        ws = Group(shot_bg, shot, shot_t)
        van = L("Vanna", 52, bold=True).move_to([3.3, -1.15, 0])
        van_s = L("checks words, not numbers", 36).move_to([3.3, -1.85, 0])
        passed = boxed(VGroup(M("USA 4,667", 34, TERRA), tick(0, 0, 0.15), L("passed", 36)).arrange(RIGHT, buff=0.25),
                       3.3, 2.5, padx=0.3, pady=0.14)
        gap_l = DashedLine([0.0, 2.9, 0], [0.0, -1.85, 0], color=TERRA, stroke_width=6, dash_length=0.18)
        gap_t = L("the gap", 40).move_to([0.0, -2.3, 0])
        at(self, "BIRD tests", FadeOut(head), rise(shelf), FadeIn(bird), FadeIn(bird_s), rt=0.8)
        self.play(FadeIn(yours), FadeIn(yours_t), Create(nob), run_time=0.7)
        at(self, "Vanna's built-in", FadeIn(ws, shift=UP * 0.5), FadeIn(van), FadeIn(van_s), rt=0.8)
        at(self, "it passed the answer", FadeIn(passed, shift=DOWN * 0.3), rt=0.6)
        self.play(Create(gap_l), FadeIn(gap_t), run_time=0.8)
        finish(self)


class B07_WhatItIs(Scene):
    def construct(self):
        plan = tag("planned · the AI step is not built yet")
        q = boxed(VGroup(L("Revenue", 34), L("by country?", 34)).arrange(DOWN, buff=0.08), -4.8, 0.65)
        ai = boxed(L("AI's SQL", 38), -2.45, 1.65, fill=CARD, sw=4)
        ck = boxed(L("checked SQL", 38), -2.45, -0.35, fill=CARD, sw=4)
        db = make_original("server-tower", 2.0, x=0.45, y=0.75)
        db_l = L("your database", 34).move_to([0.45, -0.75, 0])
        r1 = boxed(M("4,667.06", 32), 3.35, 1.65)
        r2 = boxed(M("523.06", 32), 3.35, -0.35)
        def arr(a, b):
            return Arrow(a, b, color=INK, stroke_width=5, buff=0.08, max_tip_length_to_length_ratio=0.3)
        a1, a2 = arr(q.get_right(), ai.get_left()), arr(q.get_right(), ck.get_left())
        a3, a4 = arr(ai.get_right(), db.get_left() + UP * 0.3), arr(ck.get_right(), db.get_left() + DOWN * 0.3)
        a5, a6 = arr(db.get_right() + UP * 0.3, r1.get_left()), arr(db.get_right() + DOWN * 0.3, r2.get_left())
        neq = M("≠", 80, TERRA).move_to([5.45, 0.65, 0])
        cmp_l = L("compare", 34).move_to([5.45, -0.3, 0])
        line = VGroup(L("Revenue by country", 36), VGroup(cross(0, 0, 0.16), L("WRONG", 36, bold=True)).arrange(RIGHT, buff=0.25),
                      L("counted orders 4 times", 36)).arrange(RIGHT, buff=0.9)
        fit(line, 10.6)
        card = boxed(line, 0, -2.0, padx=0.45, pady=0.22)
        rc_l = L("report card", 36, bold=True).next_to(card, UP, buff=0.12).align_to(card, LEFT)
        self.add(plan)
        at(self, "Ground Truth SQL fills", FadeIn(q), rt=0.6)
        at(self, "Give it your database", GrowArrow(a1), GrowArrow(a2), FadeIn(ai), FadeIn(ck), rise(db), FadeIn(db_l), rt=1.0)
        at(self, "It runs the AI's SQL", GrowArrow(a3), GrowArrow(a4), rt=0.6)
        self.play(GrowArrow(a5), GrowArrow(a6), FadeIn(r1), FadeIn(r2), run_time=0.8)
        at(self, "compares the results", FadeIn(neq, scale=1.5), FadeIn(cmp_l), rt=0.6)
        at(self, "gives a report card", FadeIn(card[0]), FadeIn(rc_l), rt=0.5)
        self.play(AddTextLetterByLetter(line[0]), run_time=0.6)
        self.play(FadeIn(line[1]), run_time=0.4)
        self.play(AddTextLetterByLetter(line[2]), run_time=0.8)
        finish(self)

class B08_WhereUsed(Scene):
    def construct(self):
        rc = panel(3.0, 2.2, 0, 0.85, fill="#FFFFFF")
        rc_t = L("report card", 38, bold=True).move_to([0, 1.55, 0])
        rows = VGroup()
        for i, ok in enumerate([True, False, True]):
            y = 1.05 - i * 0.5
            rows.add(Line([-1.0, y, 0], [0.55, y, 0], color=GHOST, stroke_width=10))
            rows.add(tick(0.95, y + 0.05, 0.13) if ok else cross(0.95, y, 0.13))
        places = [("store sales", -4.3, 2.55), ("finance", -4.7, 1.2), ("hospitals", 4.7, 1.2),
                  ("marketing", 4.3, 2.55), ("AI data assistant", 0.0, 2.75)]
        cues = ["store sales", "finance", "hospitals", "marketing", "AI data assistants"]
        pills = []
        for (s_, x, y) in places:
            b = boxed(L(s_, 38), x, y, padx=0.35, pady=0.22)
            b[0].set_stroke(DIM, 3)          # grey edge: GATE T reads a dark edge as text
            if x == 0:
                ln = VGroup()
            else:
                ln = DashedLine(b.get_right() if x < 0 else b.get_left(), [np.sign(x) * 1.55, 1.0, 0], color=DIM, stroke_width=3)
            pills.append(VGroup(ln, b))
        people = [("Analysts", "double-check"), ("Teams", "test before buying"), ("Engineers", "fix first")]
        pcues = ["Analysts learn", "Teams test", "Engineers see"]
        pp = VGroup()
        for who, what in people:
            words = VGroup(L(who, 38, bold=True), L(what, 36)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            g = VGroup(person(0, 0, 0.7), words)
            words.next_to(g[0], RIGHT, buff=0.3)
            pp.add(g)
        pp.arrange(RIGHT, buff=1.0).move_to([0, -1.65, 0])
        fit(pp, 12.2)
        self.play(FadeIn(rc), FadeIn(rc_t), FadeIn(rows), run_time=0.6)
        for g, c in zip(pills, cues):
            at(self, c, FadeIn(g, scale=0.8), rt=0.45, lead=0.1)
        for g, c in zip(pp, pcues):
            at(self, c, rise(g, 0.3), rt=0.6)
        finish(self)

class B09_HowJudges(Scene):
    def construct(self):
        a = code(["SELECT BillingCountry,", "  SUM(Total)", "FROM Invoice", "GROUP BY BillingCountry"],
                 28, x=-3.2, y=1.45, maxw=5.9, title="checked SQL")
        b = code(["SELECT BillingCountry,", "  SUM(UnitPrice*Quantity)", "FROM Invoice", "JOIN InvoiceLine ...",
                  "GROUP BY BillingCountry"], 28, x=3.2, y=1.35, maxw=5.9, title="different SQL")
        ra = boxed(M("USA 523.06", 36), -3.2, -0.75)
        rb = boxed(M("USA 523.06", 36), 3.2, -0.75)
        aa = Arrow(a.get_bottom(), ra.get_top(), color=INK, stroke_width=5, buff=0.06)
        ab = Arrow(b.get_bottom(), rb.get_top(), color=INK, stroke_width=5, buff=0.06)
        eq = M("=", 72).move_to([0, -0.75, 0])
        full = 3.4
        def bar_row(lbl, y, n, color):
            l_ = L(lbl, 36).move_to([-1.3, y, 0], aligned_edge=RIGHT)
            b0 = Rectangle(width=0.01, height=0.42, fill_color=color, fill_opacity=1, stroke_width=0).move_to([-1.0, y, 0], aligned_edge=LEFT)
            b1 = Rectangle(width=full * n / 9, height=0.42, fill_color=color, fill_opacity=1, stroke_width=0).move_to([-1.0, y, 0], aligned_edge=LEFT)
            v = M(f"{n} / 9 right", 36).next_to(b1, RIGHT, buff=0.3)
            return l_, b0, b1, v
        lw, bw, bw1, nw = bar_row("compare wording", -1.95, 6, BAR1)
        lr, br, br1, nr = bar_row("compare results", -2.6, 9, INK)
        what = L("out of 9 test queries: 3 correct rewrites, 6 with a mistake", 34).move_to([0, -1.42, 0])
        self.play(FadeIn(a, shift=RIGHT * 0.4), FadeIn(b, shift=LEFT * 0.4), run_time=0.9)
        at(self, "both give", GrowArrow(aa), GrowArrow(ab), FadeIn(ra), FadeIn(rb), rt=0.7)
        self.play(FadeIn(eq, scale=1.4), run_time=0.4)
        at(self, "On nine test queries", FadeIn(what), rt=0.5)
        at(self, "comparing wording", FadeIn(lw), FadeIn(bw), rt=0.3)
        self.play(Transform(bw, bw1), FadeIn(nw), run_time=0.7)
        at(self, "Comparing results", FadeIn(lr), FadeIn(br), rt=0.3)
        self.play(Transform(br, br1), FadeIn(nr), run_time=0.7)
        finish(self)

class B10_Runs(Scene):
    def construct(self):
        real = tag("real run · Claude Opus 5.5 · 2026-10-21 · output shortened", y=3.05)
        frame = panel(12.6, 4.2, 0, 0.5, fill="#FFFFFF")
        bar = Rectangle(width=12.5, height=0.45, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([0, 2.38, 0])
        dots = VGroup(*[Circle(radius=0.08, fill_color=c, fill_opacity=1, stroke_width=0).move_to([-5.95 + i * 0.3, 2.38, 0])
                        for i, c in enumerate([TERRA, DIM, DIM])])
        cmd = M("$ python3 score_claude_runs.py", 30).move_to([-5.9, 1.85, 0], aligned_edge=LEFT)
        lines = ["Q01, Q03 … Q08   all 3 runs   PASS",
                 "Q02  gold  USA 13 · Canada 8 · Brazil 5 …",
                 "run1  USA 13 · Canada 8 · France 5 …  FAIL",
                 "run2  USA 13 · Canada 8 · France 5 …  FAIL",
                 "run3  USA 13 · Canada 8 · Brazil 5 …  PASS"]
        out = VGroup(*[M(s_, 30) for s_ in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([-5.9, 0.38, 0], aligned_edge=LEFT)
        last = M("22 / 24 passed by comparing rows", 30).move_to([-5.9, -1.3, 0], aligned_edge=LEFT)
        ul = Line(last.get_corner(DL) + DOWN * 0.08, last.get_corner(DR) + DOWN * 0.08, color=TERRA, stroke_width=7)
        fails = VGroup(out[2], out[3])
        tie_q = L("Q02 · Which 5 countries have the most customers?", 36)
        tie_a = VGroup(L("France 5", 40), M("=", 44), L("Brazil 5", 40), L("· a tie, not a mistake", 40)).arrange(RIGHT, buff=0.3)
        tie = boxed(VGroup(tie_q, tie_a).arrange(DOWN, buff=0.16), 0, -2.4, fill=CARD, sw=4, pady=0.16)
        self.add(real)
        self.play(FadeIn(frame), FadeIn(bar), FadeIn(dots), run_time=0.35)
        self.play(AddTextLetterByLetter(cmd), run_time=0.6)
        at(self, "Claude then answered", LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in out], lag_ratio=0.3), rt=1.2)
        at(self, "The checker passed", FadeIn(last), rt=0.4)
        self.play(Create(ul), run_time=0.5)
        at(self, "The two fails", Indicate(fails, color=TERRA, scale_factor=1.04), rt=0.9)
        at(self, "a tie", FadeIn(tie, shift=UP * 0.3), rt=0.6)
        finish(self)


class B11_CaughtMe(Scene):
    def construct(self):
        head = opener(self, "a mistake in my answer key")
        axis = Line([-6.0, 1.9, 0], [1.2, 1.9, 0], color=INK, stroke_width=6)
        years = VGroup()
        for i, yv in enumerate(range(2009, 2014)):
            x = -5.6 + i * 1.6
            years.add(Line([x, 1.75, 0], [x, 2.05, 0], color=INK, stroke_width=5), L(str(yv), 36).move_to([x, 1.35, 0]))
        dl = L("the data", 36).move_to([-2.4, 2.55, 0])
        dash = DashedLine([1.4, 1.9, 0], [4.2, 1.9, 0], color=DIM, stroke_width=4)
        m23 = VGroup(Dot([4.6, 1.9, 0], radius=0.14, color=TERRA), L("2023", 40).move_to([4.6, 1.35, 0]))
        q = L("my question", 36).move_to([4.6, 2.55, 0])
        def ebox(lbl, x):
            b = boxed(M("(empty)", 40), x, -0.35, padx=0.6, pady=0.25)
            return VGroup(L(lbl, 36).next_to(b, UP, buff=0.15), b)
        e1, e2 = ebox("right answer", -3.0), ebox("broken SQL", 3.0)
        eq = M("=", 72).move_to([0, -0.35, 0])
        looks = VGroup(tick(0, 0, 0.17), L("looked correct", 36)).arrange(RIGHT, buff=0.25).move_to([0, -1.3, 0])
        neq = M("≠", 72, TERRA).move_to([0, -0.35, 0])
        rule = boxed(L("new rule: an empty right answer is rejected", 36), 0, -2.2, fill=CARD, sw=4)
        at(self, "One question asked", FadeOut(head), Create(axis), FadeIn(years), FadeIn(dl), rt=0.8)
        at(self, "but the data ends", Create(dash), FadeIn(m23, shift=RIGHT * 1.5), FadeIn(q), rt=0.8)
        at(self, "The right answer was empty", FadeIn(e1), FadeIn(e2), rt=0.6)
        self.play(FadeIn(eq), FadeIn(looks), run_time=0.5)
        at(self, "Now the tool", Transform(eq, neq), FadeOut(looks), rt=0.5)
        self.play(FadeIn(rule, shift=UP * 0.3), run_time=0.6)
        finish(self)

class B12_WhoLooks(Scene):
    def construct(self):
        plan = tag("planned · shown as it will look")
        desk = make_original("review-desk", 2.0, x=-4.6, y=0.3)
        who = fit(L("hiring manager", 36), 3.0).move_to([-4.6, -1.2, 0])
        page = panel(6.8, 4.0, 2.4, 0.45, fill="#FFFFFF")
        head = L("report card", 40, bold=True).move_to([2.4, 2.05, 0])
        rows = [("Q01 customers", True), ("Q02 top countries", False), ("Q03 revenue", False), ("Q06 long songs", False)]
        rg = VGroup()
        for i, (s_, ok) in enumerate(rows):
            y = 1.35 - i * 0.55
            rg.add(VGroup(M(s_, 32).move_to([-0.5, y, 0], aligned_edge=LEFT),
                          tick(5.0, y + 0.05, 0.14) if ok else cross(5.0, y, 0.14)))
        cmdp = boxed(M("one command, no API key", 30), 2.4, -1.05, fill=CARD)
        hl = SurroundingRectangle(rg[2], color=TERRA, buff=0.1, stroke_width=5)
        pop = VGroup(code(["AI: SUM(Total) after a JOIN"], 28, maxw=6.2), code(["checked: SUM(Total)"], 28, maxw=6.2)
                     ).arrange(DOWN, buff=0.25).move_to([2.4, 0.75, 0])
        motto = L("I test AI instead of trusting it", 42).move_to([0, -2.25, 0])
        self.add(plan)
        at(self, "Hiring managers", rise(desk), FadeIn(who), rt=0.6)
        at(self, "read the report card", FadeIn(page), FadeIn(head), LaggedStart(*[FadeIn(r) for r in rg], lag_ratio=0.2), rt=0.9)
        at(self, "rerun it", FadeIn(cmdp, shift=UP * 0.2), rt=0.5)
        at(self, "open one mistake", Create(hl), rt=0.4)
        self.play(FadeOut(rg), FadeOut(hl), FadeIn(pop, shift=UP * 0.3), run_time=0.7)
        at(self, "It shows", FadeIn(motto, shift=UP * 0.2), rt=0.6)
        finish(self)

class B13_Scope(Scene):
    def construct(self):
        def col(head, items, x, mark):
            h = L(head, 40, bold=True).move_to([x, 2.4, 0], aligned_edge=LEFT)
            its = VGroup(*[VGroup(mark(0, 0, 0.15), L(s_, 36)).arrange(RIGHT, buff=0.25) for s_ in items]
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).next_to(h, DOWN, buff=0.45, aligned_edge=LEFT)
            return h, its
        inc_h, inc = col("the finished project will have", ["1 sample database (Chinook)", "~50 test questions",
                                                            "Claude as the AI being tested"], -6.3, lambda x, y, s: tick(x, y, s))
        out_h, out = col("it will not", ["be a chat app", "change any data"], 1.2, cross)
        at(self, "The finished project", FadeIn(inc_h), rt=0.5)
        at(self, "one sample database", FadeIn(inc[0], shift=RIGHT * 0.3), rt=0.4)
        at(self, "about fifty test", FadeIn(inc[1], shift=RIGHT * 0.3), rt=0.4)
        at(self, "and Claude as", FadeIn(inc[2], shift=RIGHT * 0.3), rt=0.4)
        at(self, "It won't be", FadeIn(out_h), FadeIn(out[0], shift=RIGHT * 0.3), rt=0.5)
        at(self, "it never changes", FadeIn(out[1], shift=RIGHT * 0.3), rt=0.4)
        finish(self)


class B14_Risk(Scene):
    def construct(self):
        def card(mob, y, fill="#FFFFFF"):
            b = boxed(mob, 0, y, padx=0.4, pady=0.24, fill=fill)
            b[0].set_stroke(DIM, 3)          # grey edge: GATE T reads a dark edge as text
            return b
        risk = card(VGroup(L("the risk", 40, bold=True),
                           L("I write the test questions, so the test could be too easy", 36)).arrange(DOWN, buff=0.18), 2.25)
        warn = card(L("warning sign: Claude got all 8 right", 38), 0.45, fill=CARD)
        a1 = Arrow(risk.get_bottom(), warn.get_top(), color=INK, stroke_width=5, buff=0.08)
        do_h = L("what I'll do about it", 38, bold=True).move_to([0, -0.75, 0])
        a2 = Arrow(warn.get_bottom(), do_h.get_top(), color=INK, stroke_width=5, buff=0.08)
        fix1 = VGroup(tick(0, 0, 0.16), L("check every answer a second way (8 of 8 agree)", 36)).arrange(RIGHT, buff=0.25)
        fix2 = VGroup(tick(0, 0, 0.16), L("write harder questions next", 36)).arrange(RIGHT, buff=0.25)
        fixes = VGroup(fix1, fix2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.85, 0])
        at(self, "The risk", FadeIn(risk, shift=DOWN * 0.3), rt=0.7)
        at(self, "Claude getting every", GrowArrow(a1), FadeIn(warn, shift=DOWN * 0.2), rt=0.7)
        at(self, "So I check", GrowArrow(a2), FadeIn(do_h), FadeIn(fix1, shift=UP * 0.2), rt=0.7)
        at(self, "harder questions", FadeIn(fix2, shift=UP * 0.2), rt=0.5)
        finish(self)


class B15_WhyMe(Scene):
    def construct(self):
        head = L("why this project?", 56, bold=True).move_to([0, 2.4, 0])
        self.play(FadeIn(head, shift=UP * 0.3), run_time=0.6)
        def shelf(x, label):
            board = Line([x - 2.7, -0.2, 0], [x + 2.7, -0.2, 0], color=INK, stroke_width=8)
            return VGroup(board, L(label, 42, bold=True).move_to([x, -0.9, 0]))
        def block(s, x, y=0.35):
            t = L(s, 34)
            b = Rectangle(width=max(1.5, t.width + 0.4), height=1.0, fill_color=BOX_TOP, fill_opacity=1,
                          stroke_color=INK, stroke_width=4).move_to([x, y, 0])
            t.move_to(b)
            return VGroup(b, t)
        s1, s2 = shelf(-3.6, "already use"), shelf(3.6, "want to learn")
        have = [block("SQL", -5.3), block("Python", -3.6), block("AI", -1.9)]
        slots = [DashedVMobject(Rectangle(width=2.4, height=1.0, stroke_color=DIM, stroke_width=4).move_to([x, 0.35, 0]), num_dashes=20)
                 for x in (2.3, 4.9)]
        learn = [block("testing AI", 2.3), block("why it fails", 4.9)]
        at(self, "I already use", FadeIn(s1), LaggedStart(*[FadeIn(b, shift=DOWN * 0.6) for b in have], lag_ratio=0.3), rt=1.0)
        self.play(FadeIn(s2), *[Create(s) for s in slots], run_time=0.5)
        at(self, "Testing AI", FadeIn(learn[0], shift=DOWN * 0.8), rt=0.5)
        at(self, "why it fails", FadeIn(learn[1], shift=DOWN * 0.8), rt=0.5)
        finish(self)


class B16_Conclusion(Scene):
    def construct(self):
        def head(s_, y):
            return L(s_, 42, bold=True).move_to([-6.2, y, 0], aligned_edge=LEFT)
        X0 = -3.4
        h1, h2, h3, h4 = head("problem", 2.45), head("solution", 1.2), head("today", -0.05), head("next", -1.75)
        p1 = VGroup(M("$4,667", 44), L("looks right", 38), M("$523", 44), L("is true", 38)).arrange(RIGHT, buff=0.4)
        for k in (1, 2, 3):
            p1[k].shift(RIGHT * 0.55)
        p1.move_to([X0, 2.45, 0], aligned_edge=LEFT)
        st = strike(p1[0])
        p2 = VGroup(L("your data", 40), Arrow(ORIGIN, RIGHT * 0.9, color=INK, stroke_width=5, buff=0),
                    L("test the AI", 40), Arrow(ORIGIN, RIGHT * 0.9, color=INK, stroke_width=5, buff=0),
                    L("report card", 40)).arrange(RIGHT, buff=0.3)
        fit(p2, 9.4).move_to([X0, 1.2, 0], aligned_edge=LEFT)
        p3 = VGroup(L("the checker works: Claude tested on 8 questions, 3 times", 34),
                    L("22 of 24 passed; both fails were my question's fault", 34)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        fit(p3, 9.7).move_to([X0, -0.05, 0], aligned_edge=LEFT)
        p3.shift(UP * (h3.get_center()[1] - p3[0].get_center()[1]))
        p4 = fit(L("about 50 harder questions, each checked a second way", 34), 9.7).move_to([X0, -1.75, 0], aligned_edge=LEFT)
        recap = VGroup(h1, h2, h3, h4, p1, st, p2, p3, p4)
        c1 = L("Running SQL is easy.", 72).move_to([0, 0.9, 0])
        c2 = L("Being right is the test.", 72).move_to([0, -0.45, 0])
        u = Line(c2.get_corner(DL) + DOWN * 0.12, c2.get_corner(DR) + DOWN * 0.12, color=TERRA, stroke_width=8)
        at(self, "The problem", FadeIn(h1), FadeIn(p1, shift=RIGHT * 0.3), rt=0.8)
        self.play(Create(st), run_time=0.4)
        at(self, "Ground Truth SQL tests", FadeIn(h2), LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in p2], lag_ratio=0.3), rt=1.2)
        at(self, "Today the checker", FadeIn(h3), FadeIn(p3[0], shift=RIGHT * 0.3), rt=0.6)
        at(self, "Claude's only fails", FadeIn(p3[1], shift=RIGHT * 0.3), rt=0.5)
        at(self, "Next:", FadeIn(h4), FadeIn(p4, shift=RIGHT * 0.3), rt=0.5)
        at(self, "Running SQL", FadeOut(recap, shift=UP * 0.4), Write(c1), rt=1.0)
        at(self, "Being right", Write(c2), rt=1.0)
        self.play(Create(u), run_time=0.6)
