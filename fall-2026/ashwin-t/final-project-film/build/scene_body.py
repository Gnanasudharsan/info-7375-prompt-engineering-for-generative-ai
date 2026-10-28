# ═════════════════════════════ TraceCase pitch — scene body ═════════════════════════════
# Appended after iso_kit.py by build_scenes.py. One class per beat; the narration is the clock.
# Cast kept for the whole film: the SERVICE (dark server stack; its lights turn terracotta when it
# breaks), LOG pages, the TRACE (stacked span bars), the AGENT (a magnifying glass), the PROPOSAL
# card, the GATE (a barrier arm that lifts only on approval) and the SEAL (an approval stamp).
# Every sketch of the future product carries a "constructed" tag.

DEEP_KRAFT = "#9C8462"

# ── word-accurate pacing ──────────────────────────────────────────────────────────────────
# The kit's until() estimates when a phrase is spoken from its share of the characters. That drifts.
# This override reads the real word timestamps that the toolkit's align.py writes to mp3/words.json,
# and falls back to the estimate only if they are missing.
try:
    _WORDS = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "mp3", "words.json")))
    _WFPS = float(_WORDS.get("fps", 24)); _WORDS = _WORDS["beats"]
except Exception:
    _WORDS, _WFPS = {}, 24.0
_kit_until = until


def _norm(w):
    return "".join(ch for ch in w.lower() if ch.isalnum())


def until(self, phrase, lead=0.15):
    bid = type(self).__name__.split("_")[0]
    toks = _WORDS.get(bid) or []
    want = [_norm(w) for w in phrase.split() if _norm(w)]
    have = [_norm(t["text"]) for t in toks]
    for i in range(len(have) - len(want) + 1):
        if have[i:i + len(want)] == want:
            gap = toks[i]["startFrame"] / _WFPS - lead - _elapsed(self)
            if gap > 0.05:
                self.wait(gap)
            return
    _kit_until(self, phrase)


def _mid(s):
    return _TARGET.get(type(s).__name__.split("_")[0], 10.0) / 2.0


def gplay(s, *anims, rt=0.8):
    """Play, but never across the clip midpoint (Gate T and Gate V sample there)."""
    mid, now = _mid(s), _elapsed(s)
    if now < mid + 0.3 and now + rt > mid - 0.3:
        s.wait(max(0.01, mid + 0.32 - now))
    s.play(*anims, run_time=rt)


def tag():
    """The honesty label: this picture is a sketch of something that does not exist yet."""
    return T("constructed", 32).move_to([-5.2, -3.05, 0])


def xmark(x, y, s=0.22, w=7):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


def omark(x, y, r=0.22, w=6):
    return Circle(radius=r, stroke_color=INK, stroke_width=w, fill_opacity=0).move_to([x, y, 0])


# ── the cast ─────────────────────────────────────────────────────────────────────────────
def service(ox, oy, s=0.8, n=3):
    """The demo service: a server stack whose base centre sits at (ox, oy). Returns (stack, lights)."""
    return Iso(ox, oy + 0.65 * s, s).server(-0.65, -0.65, 0, 1.3, 1.3, 0.4, n)


def magnifier(x, y, r=0.45):
    glass = Circle(radius=r, stroke_color=INK, stroke_width=8, fill_color=CARD, fill_opacity=0.85).move_to([x, y, 0])
    handle = Line([x + r * 0.72, y - r * 0.72, 0], [x + r * 1.7, y - r * 1.7, 0], color=INK, stroke_width=14)
    return VGroup(handle, glass)


def trace(x, y, w=2.6, n=4, gap=0.34):
    """A trace waterfall: a root span and child spans, left edge at x, top row at y."""
    spec = [(0.0, 1.0), (0.08, 0.45), (0.5, 0.42), (0.58, 0.3)][:n]
    return VGroup(*[Rectangle(width=w * f, height=0.2, fill_color=BAR1 if i % 2 == 0 else BAR2, fill_opacity=1,
                              stroke_width=0).move_to([x + w * o + w * f / 2, y - i * gap, 0])
                    for i, (o, f) in enumerate(spec)])


def log_page(x, y, w=1.5, h=1.8, n=3):
    pg = paper(x, y, w, h)
    return VGroup(pg, scribble_block(x - w / 2 + 0.25, y + h / 2 - 0.45, w - 0.5, n=n, gap=0.4))


def timeline(x, y, w=2.4):
    ln = Line([x, y, 0], [x + w, y, 0], color=INK, stroke_width=5)
    dots = VGroup(*[Dot([x + w * f, y, 0], radius=0.09, color=INK) for f in (0.15, 0.5)],
                  Dot([x + w * 0.85, y, 0], radius=0.11, color=TERRA))
    return VGroup(ln, dots)


def gate(x, y, L=1.9):
    """A barrier: post at x, arm pointing right. Returns (post, arm, pivot)."""
    post = Rectangle(width=0.3, height=1.3, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([x, y + 0.65, 0])
    pivot = np.array([x, y + 1.1, 0])
    arm = VGroup(Line(pivot, pivot + np.array([L, 0, 0]), color=INK, stroke_width=16),
                 *[Line(pivot + np.array([L * f, 0, 0]), pivot + np.array([L * f + 0.18, 0, 0]), color=CARD, stroke_width=10)
                   for f in (0.3, 0.6, 0.85)])
    return post, arm, pivot


def seal(x, y, r=0.32):
    return VGroup(Circle(radius=r, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([x, y, 0]),
                  check(x - 0.03, y + 0.03, r * 0.45, color=CARD, w=6))


def card(x, y, w=2.2, h=1.4, rows=2):
    box = Rectangle(width=w, height=h, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    lines = VGroup(*[scribble(x - w / 2 + 0.25, y + h / 2 - 0.4 - i * 0.38, w - 0.5 - (0.4 if i == rows - 1 else 0))
                     for i in range(rows)])
    return VGroup(box, lines)


def letter_card(x, y, ch, w=1.5, h=1.8):
    box = Rectangle(width=w, height=h, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(box, T(ch, 80, bold=True).move_to([x, y, 0]))


def switch(x, y):
    """A breaker switch. Returns (base, lever, pivot); flip the lever with Rotate about pivot."""
    base = RoundedRectangle(corner_radius=0.12, width=1.0, height=0.5, fill_color=DARK_TOP, fill_opacity=1,
                            stroke_width=0).move_to([x, y, 0])
    pivot = np.array([x, y + 0.2, 0])
    lever = VGroup(Line(pivot, pivot + np.array([-0.35, 0.5, 0]), color=INK, stroke_width=9),
                   Dot(pivot + np.array([-0.35, 0.5, 0]), radius=0.11, color=TERRA))
    return base, lever, pivot


def cylinder(x, y, w=1.3, h=1.3):
    """A database: centre (x, y)."""
    body = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    bottom = Ellipse(width=w, height=0.42, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y - h / 2, 0])
    sides = VGroup(Line([x - w / 2, y - h / 2, 0], [x - w / 2, y + h / 2, 0], color=INK, stroke_width=4),
                   Line([x + w / 2, y - h / 2, 0], [x + w / 2, y + h / 2, 0], color=INK, stroke_width=4))
    top = Ellipse(width=w, height=0.42, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + h / 2, 0])
    return VGroup(bottom, body, sides, top)


def shell(x, y, w=1.4, h=0.9):
    box = RoundedRectangle(corner_radius=0.1, width=w, height=h, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    return VGroup(box, T(">_", 48, color=CARD, bold=True).move_to([x - 0.15, y, 0]))


def laptop(x, y):
    screen = Polygon([x - 1.15, y, 0], [x + 1.15, y, 0], [x + 1.05, y + 1.5, 0], [x - 1.05, y + 1.5, 0],
                     fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
    base = Polygon([x - 1.35, y, 0], [x + 1.35, y, 0], [x + 1.6, y - 0.35, 0], [x - 1.6, y - 0.35, 0],
                   fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(screen, base)


def lock(x, y, s=0.5):
    body = Rectangle(width=s, height=s * 0.8, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    shackle = Arc(radius=s * 0.3, start_angle=0, angle=PI, arc_center=[x, y + s * 0.4, 0], color=INK, stroke_width=7)
    return VGroup(shackle, body)


def pointer(x, y, s=0.6):
    """A mouse pointer whose tip is at (x, y): white body, ink outline."""
    pts = [(0, 0), (0, -1.0), (0.26, -0.76), (0.46, -1.18), (0.62, -1.1), (0.43, -0.69), (0.76, -0.69)]
    return Polygon(*[[x + u * s, y + v * s, 0] for u, v in pts], fill_color=CARD, fill_opacity=1,
                   stroke_color=INK, stroke_width=4).set_z_index(5)


def flow(a, b, color=INK):
    """A plain flow arrow from a to b."""
    return Arrow(np.array([a[0], a[1], 0]), np.array([b[0], b[1], 0]), buff=0, color=color, stroke_width=6,
                 tip_length=0.24, max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=20)


def heading(text):
    """Which of the seven questions this beat answers, top left."""
    dot = Square(side_length=0.16, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([-6.1, 3.12, 0])
    lab = T(text, 40).move_to([-5.9, 3.12, 0], aligned_edge=LEFT)
    return VGroup(dot, lab)


def plinth(x, y=-1.3):
    return Iso(x, y, 1.0).box(-0.6, -0.6, 0, 1.2, 1.2, 0.3)


# ── Q1: what it is ─────────────────────────────────────────────────────────────────────────
class B00_WhatItIs(Scene):
    def construct(self):
        self.add(heading("What it is"))
        self.add(tag())
        name = T("TraceCase", 72, bold=True).move_to([0, 2.75, 0])
        st, li = service(-4.9, -1.6)
        lab_s = T("service", 40).move_to([-4.9, -2.45, 0])
        self.play(FadeIn(name, shift=DOWN * 0.2), FadeIn(st), FadeIn(li), FadeIn(lab_s), run_time=0.7)
        self.play(*[l.animate.set_color(TERRA) for l in li], run_time=0.4)
        lp = log_page(-2.0, 1.05, 1.3, 1.5)
        tr = trace(-2.9, -0.45, 1.9, gap=0.3)
        tl = timeline(-2.95, -2.2, 1.9)
        lab = [T("logs", 40).move_to([-0.7, 1.05, 0]), T("traces", 40).move_to([-0.35, -0.75, 0]),
               T("deploys", 40).move_to([-0.3, -2.2, 0])]
        until(self, "logs")
        gplay(self, GrowArrow(flow((-4.25, -0.2), (-3.15, -0.2))), FadeIn(lp, shift=RIGHT * 0.3), FadeIn(lab[0]), rt=0.5)
        until(self, "traces")
        gplay(self, LaggedStart(*[GrowFromEdge(b, LEFT) for b in tr], lag_ratio=0.2), FadeIn(lab[1]), rt=0.6)
        until(self, "deploy history")
        gplay(self, Create(tl), FadeIn(lab[2]), rt=0.5)
        mg = magnifier(-2.0, 1.15, 0.4)
        gplay(self, FadeIn(mg), rt=0.3)
        gplay(self, mg.animate.move_to([-2.0, -1.4, 0]), rt=0.8)
        until(self, "propose one fix")
        pc = card(2.2, -0.2, 1.8, 1.2)
        lab_f = T("one fix", 40).move_to([2.2, -1.15, 0])
        gplay(self, FadeOut(mg), GrowArrow(flow((0.75, -0.2), (1.2, -0.2))), FadeIn(pc, shift=RIGHT * 0.5), FadeIn(lab_f), rt=0.6)
        post, arm, _ = gate(4.3, -1.6, 1.6)
        lab_g = T("approve?", 40).move_to([5.1, 0.05, 0])
        until(self, "A person must approve")
        gplay(self, GrowArrow(flow((3.2, -0.2), (4.05, -0.2))), FadeIn(post), Create(arm), FadeIn(lab_g), rt=0.6)
        finish(self)


class B01_Repo(Scene):
    def construct(self):
        self.add(heading("What it will be"))
        self.add(tag())
        iso = Iso(-5.2, -1.5, 0.9)
        back, front = iso.open_box(0, 0, 0, 1.3, 1.3, 0.8)
        lab_r = T("repo", 40).move_to([-5.2, -2.3, 0])
        self.play(FadeIn(back), FadeIn(front), FadeIn(lab_r), run_time=0.7)
        xs = [-3.0, -1.15, 0.8, 2.85, 4.95]
        st, li = service(xs[0], -1.5, 0.6)
        mg = magnifier(xs[1] - 0.2, -0.6, 0.38)
        ap = VGroup(card(xs[2], -0.75, 1.4, 1.3), seal(xs[2] + 0.55, -0.25, 0.22))
        sb, sl, _ = switch(xs[3], -1.1)
        bars = VGroup(*[Rectangle(width=0.36, height=hh, fill_color=c, fill_opacity=1, stroke_width=0)
                        .move_to([xs[4] - 0.5 + i * 0.5, -1.5 + hh / 2, 0]) for i, (hh, c) in
                        enumerate([(0.7, BAR1), (1.15, BAR2), (1.55, BAR1)])])
        base = Line([xs[4] - 0.8, -1.5, 0], [xs[4] + 0.8, -1.5, 0], color=INK, stroke_width=4)
        labs = [T(s, 40).move_to([x, -2.3, 0]) for s, x in zip(["service", "agent", "approval", "failures", "report"], xs)]
        until(self, "the demo service")
        gplay(self, FadeIn(st, shift=UP * 0.4), FadeIn(li), FadeIn(labs[0]), rt=0.5)
        until(self, "the agent")
        gplay(self, FadeIn(mg, shift=UP * 0.4), FadeIn(labs[1]), rt=0.5)
        until(self, "an approval screen")
        gplay(self, FadeIn(ap, shift=UP * 0.4), FadeIn(labs[2]), rt=0.5)
        until(self, "failures I can trigger")
        gplay(self, FadeIn(sb, shift=UP * 0.4), FadeIn(sl), FadeIn(labs[3]), rt=0.5)
        until(self, "evaluation report")
        gplay(self, Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(labs[4]), rt=0.8)
        finish(self)


# ── Q2: why anyone would care ──────────────────────────────────────────────────────────────
class B02_Why(Scene):
    def construct(self):
        self.add(heading("Why it matters"))
        st, li = service(-4.6, -1.5)
        lab_c = T("CloudPulse", 40).move_to([-4.6, -2.35, 0])
        q = T("healthy?", 40).move_to([-4.6, 2.0, 0])
        self.play(FadeIn(st), FadeIn(li), FadeIn(lab_c), run_time=0.6)
        until(self, "is the service healthy")
        gplay(self, FadeIn(q), rt=0.4)
        until(self, "the answer is no")
        gplay(self, *[l.animate.set_color(TERRA) for l in li], rt=0.5)
        pages = [paper(-1.2 + dx, -0.6 + dy, 1.5, 1.8, tilt=t) for dx, dy, t in
                 [(0, 0, -0.08), (0.7, 0.35, 0.1), (1.4, -0.1, -0.04), (0.5, -0.5, 0.06), (1.1, 0.75, -0.12)]]
        until(self, "digs through logs")
        gplay(self, GrowArrow(flow((-3.85, -0.6), (-2.15, -0.6))), rt=0.4)
        gplay(self, LaggedStart(*[FadeIn(p, shift=DOWN * 0.4) for p in pages], lag_ratio=0.2), rt=1.0)
        cur = pointer(-0.6, 0.6)
        gplay(self, FadeIn(cur), rt=0.2)
        self.play(cur.animate.move_to([0.9, -0.5, 0]), run_time=0.5)
        self.play(cur.animate.move_to([0.1, 0.8, 0]), run_time=0.5)
        why = T("why?", 110, bold=True).move_to([4.7, 0.2, 0])
        until(self, "find out why")
        gplay(self, GrowArrow(flow((2.3, 0.2), (3.0, 0.2))), FadeIn(why, scale=0.9), rt=0.5)
        finish(self)


class B03_Alternatives(Scene):
    def construct(self):
        self.add(heading("What already exists"))
        xs = [-4.4, 0.0, 4.4]
        labels = [T(s, 40).move_to([x, -2.35, 0]) for s, x in zip(["HolmesGPT", "AIOpsLab", "by hand"], xs)]
        pls = [plinth(x) for x in xs]
        self.play(*[FadeIn(pl, shift=UP * 0.2) for pl in pls], run_time=0.5)
        until(self, "Holmes")
        mg = magnifier(xs[0] - 0.75, 0.25, 0.36)
        post, arm, _ = gate(xs[0] + 0.3, -1.0, 0.9)
        gplay(self, FadeIn(mg, shift=DOWN * 0.3), FadeIn(post), FadeIn(arm), FadeIn(labels[0]), rt=0.6)
        until(self, "Microsoft's")
        cl = VGroup(*[service(xs[1] + dx, -1.15 + dy, 0.38, 2)[0] for dx, dy in [(-0.55, 0.0), (0.55, 0.0), (0.0, 0.55)]])
        gplay(self, FadeIn(cl, shift=DOWN * 0.3), FadeIn(labels[1]), rt=0.6)
        until(self, "dig by hand")
        dash = Iso(xs[2], -1.3).page(-0.45, -0.45, 0.3, 0.9, 1.0)
        gplay(self, FadeIn(dash, shift=DOWN * 0.3), FadeIn(labels[2]), rt=0.6)
        gplay(self, FadeIn(pointer(xs[2] + 0.15, -0.55, 0.5)), rt=0.3)
        finish(self)


class B04_Different(Scene):
    def construct(self):
        self.add(heading("What will be different"))
        self.add(tag())
        lp = laptop(-4.0, -1.2)
        lab_l = T("laptop", 40).move_to([-4.0, -2.15, 0])
        nok = T("no Kubernetes", 40).move_to([-4.0, 1.2, 0])
        self.play(FadeIn(lp, shift=UP * 0.3), FadeIn(lab_l), run_time=0.6)
        until(self, "no Kubernetes")
        gplay(self, FadeIn(nok), rt=0.4)
        st, li = service(-4.0, -0.95, 0.42)
        sb, sl, piv = switch(-1.2, -1.0)
        lab_b = T("break it", 40).move_to([-1.2, -1.75, 0])
        until(self, "its own service")
        gplay(self, FadeIn(st), FadeIn(li), FadeIn(sb), FadeIn(sl), FadeIn(lab_b), rt=0.6)
        gplay(self, Rotate(sl, angle=-1.2, about_point=piv), *[l.animate.set_color(TERRA) for l in li], rt=0.5)
        cl = card(2.6, 1.3, 2.4, 1.2)
        lab_c = T("claim", 40).move_to([4.4, 1.3, 0])
        tr = trace(1.4, -1.0, 2.6)
        until(self, "every claim")
        gplay(self, FadeIn(cl, shift=DOWN * 0.3), FadeIn(lab_c), LaggedStart(*[GrowFromEdge(b, LEFT) for b in tr], lag_ratio=0.15), rt=0.8)
        pin = Line([2.4, 0.7, 0], [2.65, -1.0 + 0.12, 0], color=DEEP_KRAFT, stroke_width=5)
        until(self, "real log line")
        gplay(self, Create(pin), tr[2].animate.set_color(TERRA), rt=0.5)
        gplay(self, Create(check(4.6, -1.0, 0.24)), rt=0.4)
        finish(self)


# ── Q3: who opens it ───────────────────────────────────────────────────────────────────────
class B05_FirstMinute(Scene):
    def construct(self):
        self.add(heading("Who opens it"))
        self.add(tag())
        sh = shell(-4.6, 0.9)
        lab_t = T("one command", 40).move_to([-4.6, 0.0, 0])
        st, li = service(-2.1, -1.7, 0.7)
        self.play(FadeIn(sh, shift=UP * 0.3), FadeIn(st, shift=UP * 0.3), FadeIn(li), run_time=0.6)
        until(self, "start the demo")
        gplay(self, GrowArrow(flow((-3.7, 0.75), (-2.7, 0.35))), rt=0.5)
        until(self, "break it")
        gplay(self, FadeIn(lab_t), *[l.animate.set_color(TERRA) for l in li], rt=0.5)
        steps = [card(0.6, 1.2 - i * 1.15, 1.9, 0.9, rows=1) for i in range(3)]
        mg = magnifier(1.95, 1.3, 0.3)
        until(self, "watch the agent")
        gplay(self, GrowArrow(flow((-1.55, 0.05), (-0.5, 0.05))), FadeIn(mg), rt=0.4)
        for i, c in enumerate(steps):
            self.play(FadeIn(c, shift=DOWN * 0.2), mg.animate.move_to([1.95, 1.3 - i * 1.15, 0]), run_time=0.4)
        until(self, "approve or reject")
        pa, pr = pill(4.3, 0.6, 2.0, 0.75), pill(4.3, -0.6, 2.0, 0.75)
        ta, tr_ = T("approve", 40).move_to([4.3, 0.6, 0]), T("reject", 40).move_to([4.3, -0.6, 0])
        pa.set_stroke(INK, 4); pr.set_stroke(INK, 4)
        gplay(self, GrowArrow(flow((2.55, 0.0), (3.2, 0.0))), FadeIn(pa), FadeIn(pr), FadeIn(ta), FadeIn(tr_), rt=0.5)
        cur = pointer(5.05, 0.45, 0.5)
        gplay(self, FadeIn(cur, shift=LEFT * 0.3), rt=0.3)
        gplay(self, Create(check(5.85, 0.62, 0.2)), rt=0.3)
        finish(self)


# ── Q4: what it proves ─────────────────────────────────────────────────────────────────────
class B06_Loop(Scene):
    def construct(self):
        self.add(heading("What it proves: the loop"))
        self.add(tag())
        c, r = np.array([-1.4, -0.1, 0.0]), 1.85
        ring = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to(c)
        angs = [PI / 2, PI, 3 * PI / 2, 0]
        pts = [c + r * np.array([np.cos(a), np.sin(a), 0]) for a in angs]
        stations = VGroup(*[Square(side_length=0.55, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(p) for p in pts])
        labs = [T("observe", 40).move_to(pts[0] + np.array([1.35, 0.25, 0])),
                T("tool", 40).move_to(pts[1] + np.array([-0.85, 0, 0])),
                T("record", 40).move_to(pts[2] + np.array([1.25, -0.25, 0])),
                T("update", 40).move_to(pts[3] + np.array([1.05, 0.35, 0]))]
        arcs = VGroup(*[Arc(radius=r, start_angle=a + 0.3, angle=PI / 2 - 0.6, arc_center=c, color=INK, stroke_width=5)
                        .add_tip(tip_length=0.22) for a in angs])
        self.play(Create(arcs), FadeIn(stations), run_time=0.7)
        meter = Rectangle(width=0.7, height=3.0, stroke_color=INK, stroke_width=4).move_to([4.2, 0.0, 0])
        fill = Rectangle(width=0.62, height=2.92, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([4.2, 0.0, 0])
        lab_b = T("budget", 40).move_to([4.2, -1.9, 0])
        until(self, "with a budget")
        gplay(self, Create(meter), FadeIn(fill), FadeIn(lab_b), rt=0.5)
        dot = Dot(pts[0], radius=0.13, color=TERRA)
        until(self, "Observe")
        gplay(self, FadeIn(dot), FadeIn(labs[0]), rt=0.3)
        for i in range(4):
            arc = Arc(radius=r, start_angle=angs[0] + i * PI / 2, angle=PI / 2, arc_center=c)
            anims = [MoveAlongPath(dot, arc), FadeIn(labs[(i + 1) % 4])] if i < 3 else [MoveAlongPath(dot, arc)]
            self.play(*anims, fill.animate.stretch_to_fit_height(2.92 - (i + 1) * 0.45, about_edge=DOWN), run_time=0.55)
        until(self, "supported cause")
        gplay(self, Create(check(-1.45, -0.05, 0.32)), rt=0.5)
        until(self, "at a limit")
        gplay(self, fill.animate.stretch_to_fit_height(0.12, about_edge=DOWN), rt=0.6)
        finish(self)


class B07_Control(Scene):
    def construct(self):
        self.add(heading("What it proves: control"))
        self.add(tag())
        menu = paper(-4.4, 0.6, 2.2, 2.4)
        rows = VGroup(*[VGroup(Dot([-5.2, 1.3 - i * 0.65, 0], radius=0.08, color=INK),
                               scribble(-4.95, 1.3 - i * 0.65, 1.3)) for i in range(3)])
        lk = lock(-3.2, 2.05, 0.5)
        lab_m = T("allow-list", 40).move_to([-4.4, -1.0, 0])
        self.play(FadeIn(menu), Create(rows), run_time=0.7)
        tr = trace(0.4, -1.3, 2.4)
        def slip(x, y):
            box = Rectangle(width=1.8, height=1.0, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
            bar = Rectangle(width=1.1, height=0.16, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x - 0.1, y + 0.1, 0])
            return VGroup(box, bar)
        s1, s2 = slip(1.2, 1.4), slip(4.3, 1.4)
        slot = DashedVMobject(Rectangle(width=1.2, height=0.5, stroke_color=INK, stroke_width=4), num_dashes=16).move_to([4.3, -1.4, 0])
        p1 = Line([1.2, 0.9, 0], [1.4, -1.2, 0], color=DEEP_KRAFT, stroke_width=5)
        p2 = Line([4.3, 0.9, 0], [4.3, -1.15, 0], color=DEEP_KRAFT, stroke_width=5)
        lab_ch = T("contract check", 44).move_to([2.75, 2.65, 0])
        until(self, "prompt contract")
        gplay(self, FadeIn(lab_ch), FadeIn(s1), FadeIn(s2), LaggedStart(*[GrowFromEdge(b, LEFT) for b in tr], lag_ratio=0.15), rt=0.8)
        until(self, "allow-list")
        gplay(self, FadeIn(lk), FadeIn(lab_m), rt=0.4)
        sh = shell(-4.4, -2.1, 1.3, 0.8)
        until(self, "never a shell")
        gplay(self, FadeIn(sh), rt=0.3)
        gplay(self, Create(xmark(-3.3, -2.1, 0.26)), rt=0.3)
        until(self, "a claim citing")
        gplay(self, Create(p1), Create(p2), FadeIn(slot), rt=0.5)
        gplay(self, Create(check(2.45, 1.45, 0.22)), rt=0.35)
        until(self, "doesn't exist")
        gplay(self, Create(xmark(5.5, 1.45, 0.22)), rt=0.4)
        finish(self)


class B08_Gate(Scene):
    def construct(self):
        self.add(heading("What it proves: the human gate"))
        self.add(tag())
        box = Rectangle(width=4.6, height=3.0, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-2.5, 0.2, 0])
        names = ["action", "target", "evidence"]
        labs = [T(n, 40).move_to([-4.6, 1.1 - i * 0.85, 0], aligned_edge=LEFT) for i, n in enumerate(names)]
        vals = [Rectangle(width=w, height=0.16, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-2.0 + w / 2, 1.1 - i * 0.85, 0])
                for i, w in enumerate([1.45, 1.05, 1.3])]
        post, arm, piv = gate(2.3, -1.6, 2.6)
        lab_g = T("runs", 40).move_to([3.6, -2.3, 0])
        until(self, "human gate")
        self.play(FadeIn(box), FadeIn(post), FadeIn(arm), FadeIn(lab_g), run_time=0.6)
        for ph, i in [("exact action", 0), ("its target", 1), ("its evidence", 2)]:
            until(self, ph)
            gplay(self, FadeIn(labs[i]), GrowFromEdge(vals[i], LEFT), rt=0.4)
        sl = seal(-0.9, 1.4, 0.34)
        gplay(self, FadeIn(sl, scale=1.3), GrowArrow(flow((0.0, -0.5), (2.0, -0.5))), rt=0.4)
        gplay(self, Rotate(arm, angle=1.25, about_point=piv), rt=0.6)
        until(self, "If any")
        new = Rectangle(width=0.8, height=0.16, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([-2.0 + 0.4, 1.1 - 2 * 0.85, 0])
        gplay(self, Transform(vals[2], new), rt=0.5)
        until(self, "stops counting")
        gplay(self, FadeOut(sl), Rotate(arm, angle=-1.25, about_point=piv), rt=0.6)
        finish(self)


class B09_Eval(Scene):
    def construct(self):
        self.add(heading("What it proves: evaluation"))
        self.add(tag())
        tiles = [Rectangle(width=0.5, height=0.5, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3)
                 .move_to([-5.4 + (i % 6) * 0.72, 1.9 - (i // 6) * 0.72, 0]) for i in range(30)]
        lab = T("30 scenarios", 40).move_to([-3.6, -2.15, 0])
        until(self, "thirty failure scenarios")
        self.play(FadeIn(lab), LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tiles], lag_ratio=0.04), run_time=1.4)
        vault = Rectangle(width=2.4, height=1.4, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([0.6, -1.4, 0])
        lk = lock(0.6, -0.35, 0.45)
        lab_v = T("held out", 40).move_to([0.6, -2.5, 0])
        until(self, "ten locked away")
        gplay(self, FadeIn(vault), FadeIn(lk), FadeIn(lab_v), rt=0.4)
        held = tiles[20:]
        self.bring_to_front(*held)
        self.play(*[t.animate.move_to([-0.2 + (k % 5) * 0.4, -1.2 - (k // 5) * 0.45, 0]).scale(0.6) for k, t in enumerate(held)], run_time=0.8)
        until(self, "I have no numbers")
        hero = T("? / 10", 140, bold=True).move_to([3.9, 0.6, 0])
        under = Line([2.3, -0.4, 0], [5.5, -0.4, 0], color=INK, stroke_width=5)
        gplay(self, FadeIn(hero), Create(under), rt=0.6)
        finish(self)


class B10_Stack(Scene):
    def construct(self):
        self.add(heading("The demo it runs on"))
        self.add(tag())
        api, al = service(-4.9, -1.5, 0.7)
        wk, wl = service(1.5, -1.5, 0.7)
        db = cylinder(4.8, -0.85, 1.3, 1.3)
        rd = Iso(-1.7, -1.0, 0.8).box(-0.6, -0.6, 0, 1.2, 1.2, 0.7, DARK_TOP, DARK_L, DARK_R)
        labs = [T("API", 40).move_to([-4.9, -2.4, 0]), T("worker", 40).move_to([1.5, -2.4, 0]),
                T("Postgres", 40).move_to([4.8, -2.4, 0]), T("Redis", 40).move_to([-1.7, -2.4, 0])]
        self.play(FadeIn(api), FadeIn(al), FadeIn(labs[0]), run_time=0.5)
        until(self, "a worker")
        gplay(self, FadeIn(wk), FadeIn(wl), FadeIn(labs[1]), rt=0.4)
        until(self, "Postgres")
        gplay(self, FadeIn(db), FadeIn(labs[2]), rt=0.4)
        until(self, "Redis")
        gplay(self, FadeIn(rd, shift=DOWN * 0.3), FadeIn(labs[3]), GrowArrow(flow((-4.35, -0.85), (-2.45, -0.85))), rt=0.5)
        crates = [Iso(-0.75 + i * 0.5, -1.45, 0.5).box(0, 0, 0, 0.6, 0.6, 0.5) for i in range(3)]
        until(self, "a queue")
        gplay(self, LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in crates], lag_ratio=0.25), GrowArrow(flow((-0.8, -0.25), (0.85, -0.25))), rt=0.7)
        gplay(self, GrowArrow(flow((2.05, -0.85), (4.0, -0.85))), rt=0.4)
        until(self, "stale cache")
        st = T("stale", 40).move_to([-0.55, 0.45, 0])
        gplay(self, FadeIn(st), rt=0.3)
        until(self, "Open Telemetry")
        line = Line([-4.9, 1.7, 0], [4.8, 1.7, 0], color=TERRA, stroke_width=8)
        drops = VGroup(*[DashedLine([x, 1.7, 0], [x, top, 0], color=INK, stroke_width=3, dash_length=0.1)
                         for x, top in [(-4.9, 0.55), (-1.7, 0.25), (1.5, 0.55), (4.8, -0.05)]])
        dots = VGroup(*[Dot([x, 1.7, 0], radius=0.11, color=INK) for x in (-4.9, -1.7, 1.5, 4.8)])
        lab_tr = T("one trace", 40).move_to([0.0, 2.25, 0])
        gplay(self, Create(line), FadeIn(lab_tr), rt=0.8)
        gplay(self, FadeIn(dots), Create(drops), rt=0.4)
        finish(self)


# ── Q5: in, out, first ─────────────────────────────────────────────────────────────────────
class B11_Boundary(Scene):
    def construct(self):
        self.add(heading("In and out of scope"))
        self.add(tag())
        fence = DashedVMobject(Rectangle(width=5.0, height=3.9, stroke_color=INK, stroke_width=6), num_dashes=40).move_to([-2.2, -0.3, 0])
        st, li = service(-3.0, -1.3, 0.75)
        sb, sl, _ = switch(-0.8, -1.0)
        lab_in = T("demo only", 40).move_to([-2.2, 2.05, 0])
        until(self, "In scope")
        self.play(Create(fence), FadeIn(lab_in), run_time=0.7)
        until(self, "one demo service")
        gplay(self, FadeIn(st), FadeIn(li), FadeIn(sb), FadeIn(sl), rt=0.5)
        lab_lim = T("limit: no real systems", 40).move_to([3.55, -2.15, 0])
        until(self, "honest limit")
        gplay(self, FadeIn(lab_lim), rt=0.4)
        sh = shell(3.7, 0.6, 1.6, 1.0)
        lab_o = T("anything else", 40).move_to([3.7, -0.5, 0])
        until(self, "arbitrary commands")
        gplay(self, FadeIn(sh), FadeIn(lab_o), rt=0.4)
        gplay(self, Create(xmark(5.05, 0.6, 0.32, 9)), rt=0.5)
        finish(self)


class B12_FirstPiece(Scene):
    def construct(self):
        self.add(heading("The first piece"))
        self.add(tag())
        st, li = service(-4.6, -1.4, 0.8)
        sb, sl, piv = switch(-2.4, -1.0)
        self.play(FadeIn(st), FadeIn(li), FadeIn(sb), FadeIn(sl), run_time=0.6)
        until(self, "I can trigger")
        gplay(self, Rotate(sl, angle=-1.2, about_point=piv), *[l.animate.set_color(TERRA) for l in li], rt=0.5)
        tr = trace(-0.5, 1.8, 4.6)
        lab_t = T("trace", 40).move_to([1.8, 2.5, 0])
        until(self, "a trace that shows it")
        gplay(self, GrowArrow(flow((-1.95, -0.55), (-0.75, 1.35))), rt=0.4)
        gplay(self, FadeIn(lab_t), LaggedStart(*[GrowFromEdge(b, LEFT) for b in tr], lag_ratio=0.2), rt=0.8)
        gplay(self, tr[3].animate.set_color(TERRA), rt=0.4)
        log = paper(1.8, -1.6, 5.4, 1.0)
        dline = VGroup(Line([-0.5, -1.6, 0], [0.5, -1.6, 0], color=INK, stroke_width=6), scribble(0.8, -1.6, 3.4))
        lab_l = T("dated log", 40).move_to([1.8, -2.5, 0])
        until(self, "dated log")
        gplay(self, FadeIn(log, shift=UP * 0.3), FadeIn(lab_l), rt=0.5)
        gplay(self, Create(dline), rt=0.5)
        finish(self)


# ── Q6: what could sink it ─────────────────────────────────────────────────────────────────
class B13_Swap(Scene):
    def construct(self):
        self.add(heading("The biggest risk"))
        self.add(tag())
        ca = letter_card(-3.4, 0.4, "A")
        post, arm, piv = gate(1.6, -1.6, 2.6)
        lab_g = T("runs", 40).move_to([2.9, -2.3, 0])
        self.play(FadeIn(post), FadeIn(arm), FadeIn(lab_g), run_time=0.5)
        until(self, "Approve fix A")
        gplay(self, FadeIn(ca, shift=RIGHT * 0.4), rt=0.4)
        sl = seal(-2.65, 1.3, 0.34)
        gplay(self, FadeIn(sl, scale=1.3), rt=0.3)
        cb = letter_card(-3.4, 0.4, "B")
        until(self, "swap in fix B")
        gplay(self, FadeOut(ca, shift=UP * 0.6), FadeIn(cb, shift=UP * 0.6), rt=0.6)
        until(self, "must refuse")
        gplay(self, sl.animate.set_opacity(0.25), Create(xmark(-1.8, 0.4, 0.32)), rt=0.5)
        gplay(self, Wiggle(arm, scale_value=1.02, rotation_angle=0.03), rt=0.6)
        lab_r = T("refused", 40).move_to([2.9, 0.5, 0])
        gplay(self, FadeIn(lab_r), rt=0.3)
        finish(self)


# ── Q7: why this project, and exists vs will exist ─────────────────────────────────────────
class B14_Shelves(Scene):
    def construct(self):
        self.add(heading("Why this project"))
        left, right = Iso(-4.2, -1.6, 1.0), Iso(2.0, -1.6, 1.0)
        sh_l, sh_r = left.box(0, 0, 0, 3.0, 0.9, 0.25), right.box(0, 0, 0, 3.0, 0.9, 0.25)
        lab_n = T("new", 40).move_to([-3.7, -2.2, 0])
        lab_b = T("built before", 40).move_to([2.5, -2.2, 0])
        sk_n = T("agents · tracing · evals", 40).move_to([-3.85, -2.95, 0])
        sk_b = T("Spring Boot · LLMs · Docker", 40).move_to([2.65, -2.95, 0])
        self.play(FadeIn(sh_l), FadeIn(sh_r), FadeIn(lab_n), FadeIn(lab_b), run_time=0.7)
        ghosts = []
        for i in range(4):
            g = left.box(0.15 + i * 0.7, 0.15, 0.25, 0.55, 0.55, 0.55, STAGE, STAGE, STAGE)
            g.set_stroke(INK, 3)
            ghosts.append(g)
        until(self, "ask for agents")
        self.play(LaggedStart(*[Create(g) for g in ghosts], lag_ratio=0.25), FadeIn(sk_n), run_time=1.2)
        solids = [right.box(0.25 + i * 0.95, 0.15, 0.25, 0.65, 0.6, 0.65) for i in range(3)]
        until(self, "Spring Boot work")
        gplay(self, LaggedStart(*[FadeIn(s, shift=DOWN * 0.5) for s in solids], lag_ratio=0.3), FadeIn(sk_b), rt=1.0)
        finish(self)


class B15_ExistsWill(Scene):
    def construct(self):
        self.add(heading("Where it stands"))
        pl_l, pl_r = Iso(-3.4, -1.5).box(-1.0, -1.0, 0, 2.0, 2.0, 0.3), Iso(3.4, -1.5).box(-1.0, -1.0, 0, 2.0, 2.0, 0.3)
        lab_e = T("exists", 40).move_to([-3.4, -2.95, 0])
        brief = paper(-4.0, 0.25, 1.1, 1.4)
        film = Rectangle(width=1.4, height=1.0, fill_color=DARK_TOP, fill_opacity=1, stroke_width=0).move_to([-2.6, 0.1, 0])
        holes = VGroup(*[Square(side_length=0.12, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([-3.1 + i * 0.33, 0.5, 0]) for i in range(4)])
        self.play(FadeIn(pl_l), FadeIn(lab_e), FadeIn(brief), FadeIn(film), FadeIn(holes), run_time=0.8)
        until(self, "Everything else")
        lab_w = T("will exist", 40).move_to([3.4, -2.95, 0])
        st, _ = Iso(3.4, -1.2, 0.8).server(-0.65, -0.65, 0, 1.3, 1.3, 0.4, 3)
        ghost = VGroup(*[DashedVMobject(f.copy().set_fill(opacity=0).set_stroke(INK, 4), num_dashes=12)
                         for slab in st for f in slab])
        gplay(self, FadeIn(pl_r), FadeIn(lab_w), rt=0.5)
        gplay(self, Create(ghost), rt=0.8)
        finish(self)
