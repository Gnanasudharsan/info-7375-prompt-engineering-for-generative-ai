
# ═════════════════════════════ SPONSOR TRIAGE: pitch scenes (scene_body.py) ═════════════════════════════
# assemble_scenes.py appends this after iso_kit.py and the original props this film uses.
# The narration is my own recorded voice, so pacing reads the word clock that align.py writes
# (mp3/words.json, faster-whisper on my takes). Without it, it falls back to the kit's
# character-share estimate.
try:
    import manimpango as _mp
    for _f in ("EBGaramond-Regular.ttf", "EBGaramond-Medium.ttf", "PTMono-Regular.ttf"):
        _mp.register_font(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "fonts", _f))
except Exception:
    pass
MONO = "PT Mono"
DEEP_KRAFT = "#9C8462"

try:
    _WORDS = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "mp3", "words.json"),
                             encoding="utf-8"))["beats"]
except Exception:
    _WORDS = {}
_FPS = 24
GUARD = 0.3          # keep every animation this far off the clip midpoint (GATE T / Gate V sample there)


def _bid(s):
    return type(s).__name__.split("_")[0]


def _norm(w):
    return w.strip(".,:;!?'\"()").lower()


def _when(s, phrase):
    """Seconds into the beat at which `phrase` starts: word clock first, character share second."""
    bid = _bid(s)
    toks = _WORDS.get(bid) or []
    want = [_norm(w) for w in phrase.split()]
    words = [_norm(t["text"]) for t in toks]
    for i in range(len(words) - len(want) + 1):
        if words[i:i + len(want)] == want:
            return toks[i]["startFrame"] / _FPS
    n, tgt = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    if n and tgt and phrase in n:
        return tgt * n.index(phrase) / len(n)
    return None


def at(s, phrase, lead=0.2):
    t = _when(s, phrase)
    if t is not None:
        gap = t - lead - _elapsed(s)
        if gap > 0.05:
            s.wait(gap)


def go(s, *anims, run_time=0.8, **kw):
    """self.play, but never across the midpoint: shorten to land before it, or wait until after it."""
    mid = _TARGET.get(_bid(s), 0) / 2
    now = _elapsed(s)
    if mid and now < mid + GUARD and now + run_time > mid - GUARD:
        room = mid - GUARD - now
        if room >= 0.35:
            run_time = room
        else:
            s.wait(max(0.01, mid + GUARD - now))
    s.play(*anims, run_time=run_time, **kw)


def done(s):
    tgt = _TARGET.get(_bid(s), 0)
    if not tgt:
        s.wait(1.0)
        return
    gap = tgt - _elapsed(s) - 0.06
    if gap > 0.02:
        s.wait(gap)


def lab(text, x, y, size=42, color=INK):
    return T(text, size, color).move_to([x, y, 0])


def tag(text):
    """The honesty label, bottom-left: RECORD (real, dated) or SKETCH (constructed, proposed)."""
    t = T(text, 36, INK)
    t.move_to([-6.1 + t.width / 2, -3.02, 0])
    return t


def crate(x, y, s=0.5, ghost=False, dot=True):
    """A posting: small kraft crate (ghost faces = a constructed test posting)."""
    iso = Iso(x, y, s)
    if ghost:
        body = iso.box(-0.5, -0.5, 0, 1, 1, 0.8, CARD, GHOST, BAR2)
    else:
        body = iso.box(-0.5, -0.5, 0, 1, 1, 0.8)
    g = VGroup(body)
    if dot:
        g.add(Dot(iso.p(0, 0, 0.8), radius=0.07, color=TERRA))
    return g


def tower(x, y, s=0.85, n=3):
    """The kit's plain server stack (dot lights, no slot stripes), centred on (x, y). Returns (stack, lights)."""
    iso = Iso(x, y, s)
    h = n * 0.42 + (n - 1) * 0.04
    return iso.server(-0.7, -0.7, -h / 2, 1.4, 1.4, 0.42, n)


def cross(x, y, s=0.28, w=8):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


# ─────────────────────────────────────────── beats ───────────────────────────────────────────

class B00_Triage(Scene):
    def construct(self):
        q = make_original("task-queue", height=2.3, x=-4.5, y=0.5)
        gates, labels = [], VGroup()
        for gx, word in ((-0.6, "sponsor"), (1.9, "live"), (4.4, "time")):
            g = make_original("checkpoint-scanner", height=2.1, x=gx, y=0.5)
            g.remove(g.parts["parcel"])
            gates.append(g)
            labels.add(lab(word, gx, -1.25, 44))
        self.add(q, *gates, labels, tag("SKETCH · proposed"))
        self.wait(0.3)
        go(self, q.parts["next-task"].animate.shift(q.action_vectors["next-task"]), run_time=0.7)
        post = crate(-2.4, -0.15, 0.42)
        go(self, FadeIn(post, shift=RIGHT * 0.3), run_time=0.5)
        cues = ("sponsored a data role", "posting live", "time left")
        for (g, phrase, gx) in zip(gates, cues, (-0.6, 1.9, 4.4)):
            at(self, phrase, lead=0.6)
            go(self, post.animate.move_to([gx, 0.2, 0]), run_time=0.6)
            go(self, Create(check(gx, 2.15, 0.2)), run_time=0.35)
        done(self)


class B01_BigCount(Scene):
    def construct(self):
        stack = make_original("skill-stack", height=2.3, x=3.3, y=0.7)
        self.add(lab("Databricks", -3.4, 2.65, 56), stack, lab("top 5 titles", 3.3, -1.05, 44),
                 tag("RECORD · 80 Days CSV, line 7249"))
        base = Line([-5.6, -2.2, 0], [-1.2, -2.2, 0], color=INK, stroke_width=4)
        go(self, Create(base), run_time=0.4)
        at(self, "approval count")
        bar = Rectangle(width=1.1, height=3.9, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
        bar.move_to([-4.6, -2.2 + 3.9 / 2, 0])
        go(self, GrowFromEdge(bar, DOWN), run_time=1.0)
        at(self, "one thousand")
        go(self, FadeIn(lab("1,640", -1.95, 0.55, 110)), FadeIn(lab("approvals", -1.95, -0.55, 44)), run_time=0.5)
        at(self, "five top sponsored")
        scan = Line([1.5, 2.1, 0], [5.1, 2.1, 0], color=TERRA, stroke_width=8)
        go(self, FadeIn(scan), run_time=0.2)
        go(self, scan.animate.shift(DOWN * 2.4), run_time=1.0)
        go(self, FadeOut(scan), run_time=0.2)
        at(self, "None is a data role")
        go(self, FadeIn(lab("data titles: 0", 3.3, -2.0, 44)), run_time=0.4)
        done(self)


class B02_Ghost(Scene):
    def construct(self):
        panel = Rectangle(width=3.4, height=2.5, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4)
        panel.move_to([-3.7, 0.5, 0])
        band = Rectangle(width=3.4, height=0.4, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-3.7, 1.55, 0])
        rows = VGroup(*[Line([-5.0, y, 0], [-2.4, y, 0], color=GHOST, stroke_width=6) for y in (0.95, 0.55)])
        btn = RoundedRectangle(width=1.6, height=0.62, corner_radius=0.31, fill_color=DARK_TOP, fill_opacity=1,
                               stroke_width=0).move_to([-3.7, -0.25, 0])
        btn_t = T("Apply", 36, CARD).move_to(btn.get_center())
        api = make_original("server-tower", height=2.5, x=3.6, y=0.55)
        self.add(lab("page check", -3.7, 2.45, 44), panel, band, rows, btn, btn_t,
                 lab("Greenhouse API", 3.6, 2.45, 44), api, tag("RECORD · constructed job id, 2026-10-03"))
        post = crate(0.0, -1.2, 0.45)
        go(self, FadeIn(post, shift=DOWN * 0.3), run_time=0.5)
        at(self, "The page said active")
        go(self, Create(check(-4.55, -1.3, 0.22)), FadeIn(lab("active", -3.4, -1.3, 44)), run_time=0.45)
        at(self, "four oh four")
        go(self, FadeIn(lab("404", 3.6, -1.45, 96)), run_time=0.45)
        at(self, "lets the API win")
        go(self, Create(cross(0.0, -0.6)), run_time=0.35)
        go(self, post.animate.shift(DOWN * 1.2).set_opacity(0.0), run_time=0.6)
        done(self)


class B03_Reader(Scene):
    def construct(self):
        ws = make_original("agent-workstation", height=3.0, x=-3.4, y=0.45)
        self.add(ws, lab("one command", -3.4, -1.6, 44), tag("SKETCH · proposed"))
        at(self, "one offline command")
        rep = paper(2.7, 0.55, w=3.2, h=3.4)
        go(self, FadeIn(rep, shift=LEFT * 0.6), run_time=0.6)
        chips = VGroup()
        for i, y in enumerate((1.75, 1.0, 0.25, -0.5)):
            chips.add(Square(side_length=0.36, fill_color=(INK if i == 0 else BAR1 if i < 3 else BAR2), fill_opacity=1,
                             stroke_width=0).move_to([1.5, y, 0]))
            chips.add(scribble(1.95, y, 1.9, amp=0.05))
        at(self, "read the report")
        go(self, LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.12), run_time=0.9)
        at(self, "traced to a file")
        lead_ln = Line([4.35, 1.0, 0], [5.3, 1.0, 0], color=INK, stroke_width=4)
        lead_dn = Line([5.3, 1.0, 0], [5.3, -0.95, 0], color=INK, stroke_width=4)
        go(self, Create(lead_ln), Create(lead_dn), run_time=0.4)
        go(self, FadeIn(lab("file:line", 5.0, -1.6, 44)), run_time=0.3)
        done(self)


class B04_Loop(Scene):
    def construct(self):
        q = make_original("task-queue", height=1.9, x=-4.5, y=0.9)
        tool = make_original("tool-block", height=1.9, x=0.0, y=0.9)
        log = make_original("evidence-binder", height=1.6, x=4.5, y=0.85)
        slots = make_original("budget-slots", height=1.3, x=0.6, y=-2.05)
        self.add(q, tool, log, slots, lab("tool", 0.0, -0.8, 42), lab("log", 4.5, -0.8, 42),
                 lab("budget", -2.4, -2.05, 42), tag("SKETCH · proposed"))
        a1 = Arrow([-2.9, 0.9, 0], [-1.7, 0.9, 0], color=INK, stroke_width=5, buff=0)
        a2 = Arrow([1.7, 0.9, 0], [2.9, 0.9, 0], color=INK, stroke_width=5, buff=0)
        back = ArcBetweenPoints([4.5, 2.25, 0], [-4.5, 2.25, 0], angle=PI / 5, color=DIM, stroke_width=5)
        go(self, Create(a1), Create(a2), run_time=0.5)
        go(self, Create(back), run_time=0.6)
        at(self, "take a posting")
        post = crate(-3.0, 0.35, 0.36)
        go(self, FadeIn(post), run_time=0.3)
        at(self, "call one tool")
        go(self, post.animate.move_to([0.0, -0.05, 0]), run_time=0.6)
        go(self, slots.parts["allocated-token"].animate.shift(slots.action_vectors["allocated-token"]), run_time=0.5)
        at(self, "record the result")
        go(self, post.animate.move_to([4.5, 0.0, 0]), run_time=0.6)
        at(self, "It'll stop when")
        go(self, FadeOut(post), run_time=0.3)
        at(self, "budget runs out")
        stop = Line([0.0, 2.6, 0], [0.0, 3.25, 0], color=INK, stroke_width=12)
        go(self, Create(stop), FadeIn(lab("stop", 0.95, 2.3, 44)), run_time=0.4)
        done(self)


class B05_Fence(Scene):
    def construct(self):
        gate = make_original("permission-gate", height=3.0, x=-0.2, y=0.4)
        api = make_original("server-tower", height=2.3, x=4.6, y=0.6)
        self.add(gate, api, lab("Greenhouse API", 4.25, -1.15, 42), tag("SKETCH · proposed"))
        ok = crate(-4.6, 0.9, 0.42)
        bad = crate(-4.6, -1.0, 0.42, ghost=True)
        go(self, FadeIn(ok), FadeIn(bad), FadeIn(lab("other site", -4.6, -2.0, 42)), run_time=0.5)
        at(self, "Greenhouse's API")
        bar = gate.parts["barrier"]
        go(self, bar.animate.shift(-gate.action_vectors["barrier"]), run_time=0.5)
        go(self, ok.animate.move_to([3.0, 0.75, 0]), run_time=0.9)
        go(self, bar.animate.shift(gate.action_vectors["barrier"]), run_time=0.5)
        at(self, "nothing else")
        go(self, bad.animate.move_to([-1.9, -1.0, 0]), run_time=0.6)
        go(self, bad.animate.move_to([-4.6, -1.0, 0]), run_time=0.5)
        go(self, Create(cross(-3.4, -1.0)), FadeIn(lab("refused", -2.3, -2.0, 42)), run_time=0.4)
        done(self)


class B06_Gate(Scene):
    def construct(self):
        hand = make_original("human-handoff", height=2.6, x=-2.6, y=0.4)
        stamp = make_original("approval-stamp", height=2.4, x=3.4, y=0.3)
        pk = hand.parts["packet"]
        pk.shift(hand.action_vectors["packet"])                    # start at the agent's side
        st = stamp.parts["stamp"]
        st.shift(-stamp.action_vectors["stamp"])                   # stamp raised
        self.add(hand, stamp, lab("agent", -1.3, 2.35, 42), lab("me", -4.6, -1.35, 42),
                 lab("approve · refuse · defer", 3.4, -1.75, 40), tag("SKETCH · proposed"))
        at(self, "come back to me")
        go(self, pk.animate.shift(-hand.action_vectors["packet"]), run_time=1.0)
        at(self, "approve")
        go(self, st.animate.shift(stamp.action_vectors["stamp"]), run_time=0.35)
        seal = Dot([2.55, -0.55, 0], radius=0.11, color=TERRA)
        go(self, FadeIn(seal), run_time=0.25)
        done(self)


class B07_Eval(Scene):
    def construct(self):
        drawers = make_original("memory-drawers", height=3.0, x=-3.9, y=0.35)
        trays = make_original("comparison-trays", height=2.4, x=3.2, y=0.6)
        sb = trays.parts["sample-b"]
        sb.shift(-trays.action_vectors["sample-b"])
        self.add(drawers, trays, lab("40 labelled", -3.9, 2.5, 44), lab("patterns", 1.9, -1.15, 42),
                 lab("Claude", 4.6, -1.15, 42), tag("SKETCH · proposed"))
        at(self, "some held back")
        go(self, drawers.parts["drawer"].animate.shift(drawers.action_vectors["drawer"]), run_time=0.7)
        go(self, FadeIn(lab("held back", -3.9, -1.75, 42)), run_time=0.3)
        at(self, "planted failures")
        marks = VGroup(*[cross(-0.9 + i * 0.7, -2.3, 0.16, 6) for i in range(5)])
        go(self, LaggedStart(*[Create(m) for m in marks], lag_ratio=0.15), run_time=0.7)
        at(self, "test it against")
        go(self, sb.animate.shift(trays.action_vectors["sample-b"]), run_time=0.7)
        done(self)


class B08_First(Scene):
    def construct(self):
        xs = [-4.8 + i * 1.6 for i in range(7)]
        tests = {3, 6}                       # the constructed fake job id and the constructed company
        posts = [crate(x, 1.65, 0.42, ghost=(i in tests)) for i, x in enumerate(xs)]
        bins_x = (-4.2, -1.4, 1.4, 4.2)
        bins = VGroup()
        for bx, word in zip(bins_x, ("Apply", "Consider", "Skip", "Unresolved")):
            bins.add(Rectangle(width=2.0, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([bx, -1.65, 0]))
            bins.add(lab(word, bx, -2.25, 42))
        self.add(bins, tag("RECORD · run of 2026-10-03; the loop is a SKETCH"))
        go(self, LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in posts], lag_ratio=0.1), run_time=1.0)
        at(self, "matches the recipe")
        dest = [0, 1, 1, 2, 3, 3, 3]          # Apply, Consider ×2, Skip, Unresolved ×3 (worked-run order)
        level = [0, 0, 0, 0]
        moves = []
        for p, d in zip(posts, dest):
            moves.append(p.animate.move_to([bins_x[d], -1.15 + level[d] * 0.62, 0]))
            level[d] += 1
        go(self, LaggedStart(*moves, lag_ratio=0.12), run_time=1.6)
        go(self, Create(check(5.9, -2.25, 0.2)), run_time=0.35)
        done(self)


class B09_Risk(Scene):
    def construct(self):
        xs = [-5.3, -4.1, -2.9, -1.7, -0.5]
        posts = [crate(x, 0.55, 0.42) for x in xs]
        db, lights = tower(4.4, 0.6, 0.95)
        self.add(*posts, lab("one title: 862 of 1,552", -2.9, 2.55, 46), db, lights, lab("DOL data", 4.4, -1.15, 44),
                 tag("RECORD · CSV, run of 2026-10-03; DOL link: SKETCH"))
        at(self, "two real postings")
        qs = VGroup(*[Circle(radius=0.2, stroke_color=INK, stroke_width=7).move_to([x, 1.9, 0]) for x in xs[3:]])
        go(self, FadeIn(qs), run_time=0.4)
        at(self, "two only Likely")
        halves = VGroup(*[Rectangle(width=0.5, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0)
                          .move_to([x, 1.9, 0]) for x in xs[1:3]])
        go(self, FadeIn(halves), FadeIn(lab("Likely", -3.5, -0.6, 40)), run_time=0.4)
        at(self, "Labor Department's")
        cable = Line([3.0, 0.3, 0], [0.3, 0.3, 0], color=DEEP_KRAFT, stroke_width=10)
        go(self, Create(cable), run_time=0.7)
        go(self, *[d.animate.set_color(TERRA) for d in lights], run_time=0.4)
        done(self)


class B10_Why(Scene):
    def construct(self):
        shelf = make_original("version-shelves", height=3.0, x=-3.9, y=0.3)
        bench = make_original("experiment-bench", height=2.3, x=3.3, y=0.4)
        smp = bench.parts["sample"]
        smp.shift(-bench.action_vectors["sample"])
        self.add(shelf, bench, lab("built", -3.9, 2.5, 46), lab("new to me", 3.3, 2.5, 46),
                 tag("RECORD · NBA RAG app, Dec 2025"))
        at(self, "NBA RAG app")
        go(self, shelf.parts["selected-version"].animate.shift(shelf.action_vectors["selected-version"]), run_time=0.7)
        go(self, FadeIn(lab("NBA RAG app", -3.9, -1.75, 42)), Create(check(-1.45, -1.75, 0.2)), run_time=0.35)
        at(self, "Agent loops")
        go(self, smp.animate.shift(bench.action_vectors["sample"]), run_time=0.8)
        done(self)


class B11_Honest(Scene):
    def construct(self):
        have = make_original("skill-stack", height=2.0, x=-3.6, y=0.55)
        iso = Iso(2.6, -1.5, 0.85)
        ghost_box = iso.box(-1.1, -1.1, 0, 2.2, 2.2, 1.6, CARD, GHOST, BAR3, sw=4)
        self.add(have, lab("exists", -3.6, 2.35, 46), lab("12 tests", -3.6, -1.15, 42),
                 ghost_box, lab("will exist", 2.6, 2.35, 46), tag("RECORD · tests re-run 2026-10-14"))
        at(self, "write the contract")
        contract = iso.page(-0.55, -0.75, 1.6, w=1.1, d=1.4)
        go(self, FadeIn(contract, shift=DOWN * 0.5), run_time=0.5)
        go(self, FadeIn(lab("contract", 5.15, 0.9, 42)), run_time=0.3)
        at(self, "Everything else")
        tick = check(-2.2, -1.15, 0.2)
        go(self, Create(tick), run_time=0.35)
        done(self)


class BOUT_Title(Scene):
    def construct(self):
        self.add(lab("Sponsor Triage", 0, 1.05, 104), lab("a pitch by Siddi Kommuri", 0, -0.6, 52),
                 lab("INFO 7375 · October 2026", 0, -1.5, 40))
        rule = Line([-3.4, 0.0, 0], [3.4, 0.0, 0], color=INK, stroke_width=5)
        go(self, Create(rule), run_time=0.6)
        go(self, FadeIn(Dot([3.65, 0.0, 0], radius=0.1, color=TERRA)), run_time=0.25)
        done(self)
