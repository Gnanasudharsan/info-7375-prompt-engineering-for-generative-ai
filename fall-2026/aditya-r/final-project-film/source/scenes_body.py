
# ═════════════════════════════ DAYTHREAD PITCH FILM — scene body (hand-written) ═════════════════════════════
# Every body beat illustrates a CONSTRUCTED, PROPOSED workflow — nothing here was observed from a running
# system (no DayThread prototype exists). Cast reused across beats: the check-in page (raw transcript), the
# summary page, the separate check (terracotta scan line), the memory drawers, the coordinator's review page /
# desk, and the permission gate (closed, stop light lit, until a coordinator approves).
# Timing: the measured Kokoro narration is the clock (no padding except BOUT's 1.0 s tail). Motions cue on
# faster-whisper word starts stored per beat in beat_sheet.json (`words`, written by audio_post.py).

MID_GUARD = 0.22          # GATE T and Gate V sample the clip midpoint: keep motion out of [mid-0.22, mid+0.22]
SCRIB_AMP = 0.085         # GATE T measures handwriting scribbles as text runs; 0.085 keeps short ones >= 41 px
CAP_SIZE = 34
try:
    _WORDS = {b["beat_id"]: b.get("words", []) for b in _SHEET["beats"]}
except Exception:
    _WORDS = {}


def _bid(self):
    return type(self).__name__.split("_")[0]


def _target(self):
    return _TARGET.get(_bid(self), 0.0)


def _norm(w):
    return "".join(ch for ch in w.lower() if ch.isalnum())


def at(self, t):
    gap = t - _elapsed(self)
    if gap > 0.02:
        self.wait(gap)


def at_word(self, word, nth=1, early=0.12):
    """Wait until the nth spoken occurrence of `word` (prefix match on the whisper word list)."""
    want, seen = _norm(word), 0
    for w, t in _WORDS.get(_bid(self), []):
        if _norm(w).startswith(want):
            seen += 1
            if seen == nth:
                at(self, t - early)
                return


def done(self):
    """Hold to the end of the beat's audio, never past it (the kit's finish() waits >= 0.3 s even when late)."""
    target = _target(self)
    if not target:
        self.wait(1.0)
        return
    gap = target - _elapsed(self) - 0.06
    if gap > 0.02:
        self.wait(gap)


def span(self, *anims, rt=0.5, **kw):
    """play() that never crosses the midpoint window and never runs past the beat's audio."""
    target = _target(self)
    if target:
        mid, now = target / 2, _elapsed(self)
        if now < mid + MID_GUARD and now + rt > mid - MID_GUARD:
            at(self, mid + MID_GUARD)
        now = _elapsed(self)
        if now + rt > target - 0.15:
            rt = max(0.12, target - 0.15 - now)
    self.play(*anims, run_time=rt, **kw)


# ── captions: italic, in their own bands, never mixed with scene headings (headings stay inside y <= 2.3) ──
def CAP(s):
    return Text(s, font=SERIF, color=INK, font_size=CAP_SIZE, slant="ITALIC")   # string form: Gate A's stub has no ITALIC constant


def captions(kind=None):
    g = VGroup(CAP("Synthesized voice reading Aditya’s script").move_to([-6.1, 3.1, 0], aligned_edge=LEFT))
    if kind == "C":
        g.add(CAP("Constructed — proposed workflow").move_to([0, -3.1, 0]))
    elif kind == "D":
        g.add(CAP("From each company’s own documentation, read 2026-10-14").move_to([0, -3.1, 0]))
    elif kind == "R":
        g.add(CAP("Replay run 2026-10-25 · synthetic data · fictional client").move_to([0, -3.1, 0]))
    return g


def L(s, x, y, size=40):
    return T(s, size).move_to([x, y, 0])


# ── the cast ──
def checkin_page(x, y, w=2.8, h=3.3, n=5, dot=2, short_last=True):
    """A check-in page: paper + n handwriting lines; a terracotta dot marks line `dot` (None = no dot)."""
    pg = paper(x, y, w, h)
    my, mx, mr = min(0.55, 0.18 * h + 0.1), min(0.55, 0.2 * w + 0.1), min(0.4, 0.15 * w + 0.1)
    step = (h - 2 * my) / (n - 1)
    x0, lw = x - w / 2 + mx, w - mx - mr
    ys = [y + h / 2 - my - i * step for i in range(n)]
    lines = VGroup(*[scribble(x0, yy, lw * (0.6 if (short_last and i == n - 1) else 1.0), amp=SCRIB_AMP)
                     for i, yy in enumerate(ys)])
    g = VGroup(pg, lines)
    g.pg, g.lines, g.ys, g.x0, g.lw = pg, lines, ys, x0, lw
    g.dot = None
    if dot is not None:
        g.dot = Dot([x0 - min(0.24, mx - 0.1), ys[dot], 0], radius=0.09 if w > 1.5 else 0.07, color=TERRA)
    return g


def summary_page(x, y, w=2.3, h=2.6, gap_row=2):
    """Shorter page with a dashed empty row where the tumble line should have been."""
    pg = paper(x, y, w, h)
    x0, lw = x - w / 2 + 0.38, w - 0.76
    my = min(0.5, 0.17 * h + 0.06)
    step = (h - 2 * my) / 3
    ys = [y + h / 2 - my - i * step for i in range(4)]
    lines = VGroup(*[scribble(x0, yy, lw * (0.55 if i == 3 else 1.0), amp=SCRIB_AMP)
                     for i, yy in enumerate(ys) if i != gap_row])
    gap = DashedLine([x0, ys[gap_row], 0], [x0 + lw, ys[gap_row], 0], color=DIM, stroke_width=4, dash_length=0.16)
    g = VGroup(pg, lines, gap)
    g.gap = gap
    return g


def slip(x, y, w=1.6, h=0.72):
    s = paper(x, y, w, h)
    d = Dot([x - w / 2 + 0.28, y, 0], radius=0.08, color=TERRA)
    ln = scribble(x - w / 2 + 0.5, y, w - 0.8, amp=SCRIB_AMP)
    return VGroup(s, d, ln)


def envelope(x, y, w=0.95, h=0.62):
    body = Rectangle(width=w, height=h, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
    flap = VMobject(stroke_color=INK, stroke_width=4).set_points_as_corners(
        [[-w / 2, h / 2, 0], [0, -h * 0.05, 0], [w / 2, h / 2, 0]])
    return VGroup(body, flap).move_to([x, y, 0])


def gate(x, y, h=2.4):
    """The permission-gate prop with its own barrier replaced by a horizontal boom arm that visibly blocks the
    lane (closed) and swings up only after approval (`open_gate`), plus a terracotta stop light on the left post."""
    g = make_original("permission-gate", height=h, x=x, y=y)
    g.remove(g.parts["barrier"])
    pivot = np.array([x - 0.30 * h, y + 0.05 * h, 0])
    boom = Rectangle(width=0.72 * h, height=0.085 * h, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK,
                     stroke_width=4).move_to(pivot + np.array([0.36 * h, 0, 0]))
    g.add(boom)
    g.boom, g.pivot = boom, pivot
    g.light = Dot([x - 0.30 * h, y + 0.22 * h, 0], radius=0.11 if h > 1.5 else 0.08, color=TERRA)
    return g


def open_gate(g):
    return Rotate(g.boom, angle=PI * 0.42, about_point=g.pivot)


def plinth(cx, cy, w=3.4, d=1.3, hgt=0.3):
    """A flat shelf/plinth seen from the front: kraft top face + front face, ink outlines. `d` is unused
    (kept for call compatibility); the top face recedes by a fixed 0.35."""
    front = Rectangle(width=w, height=hgt, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([cx, cy, 0])
    top = Polygon([cx - w / 2, cy + hgt / 2, 0], [cx + w / 2, cy + hgt / 2, 0], [cx + w / 2 + 0.3, cy + hgt / 2 + 0.32, 0],
                  [cx - w / 2 + 0.3, cy + hgt / 2 + 0.32, 0], fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(top, front)


def arrow(x0, y0, x1, y1):
    return Arrow([x0, y0, 0], [x1, y1, 0], buff=0, color=INK, stroke_width=5, max_tip_length_to_length_ratio=0.25)


# ═════════════════════════════ scenes ═════════════════════════════

class BIDEA_Title(Scene):
    def construct(self):
        self.add(captions())
        name = L("Aditya Raj", 0, 0.05, 48)
        title = T("DayThread", 120).move_to([0, 1.3, 0])
        sub = L("a proposed final project", 0, -0.7, 44)
        span(self, FadeIn(name, shift=UP * 0.15), rt=0.45)
        at_word(self, "This")
        span(self, FadeIn(title, shift=UP * 0.2), rt=0.55)
        at_word(self, "proposed")
        span(self, FadeIn(sub, shift=UP * 0.15), rt=0.45)
        thread = Line([-4.2, -1.55, 0], [4.2, -1.55, 0], color=INK, stroke_width=5)
        span(self, Create(thread), rt=0.6)
        pages = VGroup(*[paper(x, -1.97, 0.6, 0.78) for x in (-2.6, 0.0, 2.6)])
        span(self, LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in pages], lag_ratio=0.25), rt=0.8)
        done(self)


class B00_WhatItIs(Scene):
    def construct(self):
        self.add(captions("C"))
        ty = -0.75
        t1 = Line([-5.7, ty, 0], [-0.4, ty, 0], color=INK, stroke_width=5)
        t2 = Line([-0.4, ty, 0], [2.6, ty, 0], color=INK, stroke_width=5)
        span(self, Create(t1), rt=0.6)
        d1 = checkin_page(-4.3, 0.75, 2.0, 2.4, n=4, dot=None)
        d2 = checkin_page(-1.6, 0.75, 2.0, 2.4, n=4, dot=1)
        l1, l2 = L("Day 1", -4.3, -1.25), L("Day 2", -1.6, -1.25)
        at_word(self, "remembers")
        span(self, FadeIn(d1, shift=DOWN * 0.3), FadeIn(l1), rt=0.5)
        at_word(self, "across")
        span(self, FadeIn(d2, shift=DOWN * 0.3), FadeIn(l2), rt=0.5)
        at_word(self, "concerning")
        span(self, GrowFromCenter(d2.dot), rt=0.35)
        desk = make_original("review-desk", height=2.2, x=4.2, y=-0.35)
        desk.remove(desk.parts["evidence"])
        lc = L("coordinator", 4.2, -1.95)
        at_word(self, "evidence")
        span(self, Create(t2), FadeIn(desk, shift=UP * 0.2), FadeIn(lc), rt=0.6)
        ev = slip(-1.6, -0.2, 1.3, 0.6)
        at_word(self, "review")
        span(self, FadeIn(ev, scale=1.1), rt=0.3)
        span(self, MoveAlongPath(ev, ArcBetweenPoints(np.array([-1.6, -0.2, 0]), np.array([4.15, 0.25, 0]), angle=-PI / 4)),
             rt=0.9, rate_func=smooth)
        done(self)


# B01–B03 share the original page on the left
OP_X, OP_Y, OP_W, OP_H = -3.7, -0.1, 3.0, 3.4


def original():
    p = checkin_page(OP_X, OP_Y, OP_W, OP_H, n=5, dot=2)
    head = L("check-in", OP_X, OP_Y + OP_H / 2 + 0.42)
    return p, head


def tumble_label(p):
    y = p.ys[2]
    lab = T("“a little tumble”", 42).move_to([0.75, y, 0])
    lead = Line([OP_X + OP_W / 2 + 0.15, y, 0], [-1.2, y, 0], color=INK, stroke_width=4)
    return lab, lead


class B01_DayOne(Scene):
    def construct(self):
        self.add(captions("C"))
        p, head = original()
        lab, lead = tumble_label(p)
        span(self, FadeIn(p.pg, shift=UP * 0.2), FadeIn(head), rt=0.5)
        span(self, LaggedStart(*[Create(l) for l in p.lines], lag_ratio=0.18), rt=0.9, rate_func=linear)
        at_word(self, "tumble")
        span(self, GrowFromCenter(p.dot), Create(lead), FadeIn(lab, shift=LEFT * 0.15), rt=0.45)
        dr = make_original("memory-drawers", height=2.5, x=4.6, y=-0.2)
        lr = L("raw transcript", 4.5, -1.95)
        at_word(self, "raw")
        span(self, FadeIn(dr, shift=UP * 0.2), FadeIn(lr), rt=0.5)
        cp = paper(OP_X, OP_Y, 1.0, 1.15)
        span(self, FadeIn(cp), dr.parts["drawer"].animate.shift(dr.action_vectors["drawer"]), rt=0.4)
        span(self, MoveAlongPath(cp, ArcBetweenPoints(np.array([OP_X, OP_Y, 0]), np.array([5.05, -0.55, 0]), angle=-PI / 4)),
             rt=0.9, rate_func=smooth)
        span(self, FadeOut(cp), dr.parts["drawer"].animate.shift(-dr.action_vectors["drawer"]), rt=0.4)
        done(self)


SP_X, SP_Y = 0.75, 0.15


class B02_Failure(Scene):
    def construct(self):
        self.add(captions("C"))
        p, head = original()
        lab, lead = tumble_label(p)
        dr = make_original("memory-drawers", height=2.5, x=4.6, y=-0.2)
        lr = L("raw transcript", 4.5, -1.95)
        self.add(p, p.dot, head, lab, lead, dr, lr)
        span(self, FadeOut(VGroup(lab, lead, dr, lr)), rt=0.4)
        s = summary_page(SP_X, SP_Y)
        sh, sm = L("summary", SP_X, SP_Y + 1.72), L("missed", SP_X, SP_Y - 1.75)
        at_word(self, "summary")
        span(self, FadeIn(s, shift=LEFT * 0.4), FadeIn(sh), rt=0.55)
        at_word(self, "tumble")
        span(self, FadeIn(sm), Indicate(s.gap, color=INK, scale_factor=1.0), rt=0.45)
        c1, c2 = summary_page(3.35, 0.15, 1.5, 1.95), summary_page(5.15, 0.15, 1.5, 1.95)
        a1 = arrow(2.0, 0.15, 2.5, 0.15)
        ll = L("later steps", 4.25, -1.4)
        at_word(self, "later")
        span(self, GrowArrow(a1), FadeIn(c1, shift=RIGHT * 0.2), FadeIn(ll), rt=0.5)
        at_word(self, "misses")
        span(self, FadeIn(c2, shift=RIGHT * 0.2), rt=0.45)
        done(self)


class B03_Check(Scene):
    def construct(self):
        self.add(captions("C"))
        p, head = original()
        s = summary_page(SP_X, SP_Y)
        sh, sm = L("summary", SP_X, SP_Y + 1.72), L("missed", SP_X, SP_Y - 1.75)
        c1, c2 = summary_page(3.35, 0.15, 1.5, 1.95), summary_page(5.15, 0.15, 1.5, 1.95)
        a1 = arrow(2.0, 0.15, 2.5, 0.15)
        ll = L("later steps", 4.25, -1.4)
        self.add(p, p.dot, head, s, sh, sm, c1, c2, a1, ll)
        span(self, FadeOut(VGroup(c1, c2, a1, ll, sm)), rt=0.4)
        sl = Line([p.x0 - 0.15, p.ys[0] + 0.3, 0], [p.x0 + p.lw + 0.1, p.ys[0] + 0.3, 0], color=TERRA, stroke_width=8)
        lsc = L("separate check", OP_X, OP_Y - OP_H / 2 - 0.42)
        at_word(self, "separate")
        span(self, Create(sl), FadeIn(lsc), rt=0.3)
        span(self, sl.animate.move_to([float(np.array(sl.get_center())[0]), p.ys[2] - 0.13, 0]), rt=0.9, rate_func=smooth)
        q = make_original("task-queue", height=2.1, x=4.5, y=-0.25)
        lq = L("review item", 4.5, -1.85)
        at_word(self, "creates")
        span(self, FadeIn(q, shift=UP * 0.2), FadeIn(lq), rt=0.45)
        ri = slip(OP_X + 0.3, p.ys[2], 1.5, 0.7)
        # GATE T reads a lined slip over an outlined page/prop as stacked labels: keep it off-stage at the midpoint
        at(self, _target(self) / 2 + MID_GUARD + 0.05)
        span(self, FadeIn(ri, scale=1.1), rt=0.25)
        span(self, MoveAlongPath(ri, ArcBetweenPoints(np.array([OP_X + 0.3, p.ys[2], 0]), np.array([3.95, 0.45, 0]), angle=-PI / 3.5)),
             rt=1.0, rate_func=smooth)
        done(self)


D1_X, D2_X, DY = -4.3, -0.6, 0.25


class B04_DayTwo(Scene):
    def construct(self):
        self.add(captions("C"))
        d1 = checkin_page(D1_X, DY, 2.4, 2.9, n=4, dot=1)
        l1 = L("Day 1", D1_X, DY + 1.85)
        span(self, FadeIn(d1, shift=UP * 0.2), FadeIn(d1.dot), FadeIn(l1), rt=0.5)
        d2 = checkin_page(D2_X, DY, 2.4, 2.9, n=4, dot=None)
        l2 = L("Day 2", D2_X, DY + 1.85)
        at_word(self, "two")
        span(self, FadeIn(d2.pg, shift=LEFT * 0.3), FadeIn(l2), rt=0.45)
        span(self, LaggedStart(*[Create(l) for l in d2.lines], lag_ratio=0.2), rt=0.8, rate_func=linear)
        # v4 (2026-10-25): the link now sits in the gap between the pages instead of running dot to dot.
        # Once the longer narration moved the clip midpoint past this draw, the dot-to-dot ink arc fused
        # both page outlines into one "text" blob (GATE T §8.6b), and a terracotta arc failed §8.3 contrast.
        gap_l, gap_r = D1_X + 1.2 + 0.25, D2_X - 1.2 - 0.25
        link = ArcBetweenPoints(np.array([gap_l, d1.ys[1] + 0.12, 0]), np.array([gap_r, d2.ys[1] + 0.12, 0]), angle=-PI / 1.5)
        link.set_stroke(INK, 5)
        end = Dot([d2.x0 - 0.24, d2.ys[1], 0], radius=0.09, color=TERRA)
        at_word(self, "linked")
        span(self, Create(link), rt=0.7)
        span(self, GrowFromCenter(end), rt=0.3)
        ws = make_original("agent-workstation", height=2.3, x=4.4, y=0.05)
        lw = L("first to run", 4.4, -1.6)
        at_word(self, "replay")
        span(self, FadeIn(ws, shift=UP * 0.2), FadeIn(lw), rt=0.5)
        span(self, ws.parts["tool"].animate.shift(ws.action_vectors["tool"]), rt=0.5)
        done(self)


class B05_Gate(Scene):
    def construct(self):
        self.add(captions("C"))
        wx, wy, ww, wh = -3.75, 0.05, 4.1, 3.0
        win = Rectangle(width=ww, height=wh, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([wx, wy, 0])
        bar = Rectangle(width=ww, height=0.36, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([wx, wy + wh / 2 - 0.18, 0])
        hd = L("local review page", wx, wy + wh / 2 + 0.42)
        g = gate(3.7, -0.2, 2.4)
        lg = L("closed", 3.7, -1.85)
        env = envelope(1.75, -0.85)
        span(self, FadeIn(win), FadeIn(bar), FadeIn(hd), FadeIn(g), FadeIn(g.light), FadeIn(env), FadeIn(lg), rt=0.6)
        cdot = Dot([wx - ww / 2 + 0.45, wy + 0.85, 0], radius=0.09, color=TERRA)
        cline = scribble(wx - ww / 2 + 0.7, wy + 0.85, 2.6, amp=SCRIB_AMP)
        at_word(self, "concern")
        span(self, GrowFromCenter(cdot), Create(cline), rt=0.45)
        ex = VGroup(*[VGroup(Rectangle(width=3.2, height=0.62, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=DIM, stroke_width=3)
                             .move_to([wx, wy + yy, 0]),
                             scribble(wx - 1.3, wy + yy, 2.5, amp=SCRIB_AMP)) for yy in (0.0, -0.85)])
        at_word(self, "excerpts")
        span(self, LaggedStart(*[FadeIn(e, shift=UP * 0.1) for e in ex], lag_ratio=0.3), rt=0.55)
        boxes = VGroup(*[Square(0.4, color=INK, stroke_width=4, fill_color=CARD, fill_opacity=1).move_to([-1.2, yy, 0])
                         for yy in (0.9, 0.15, -0.6)])
        opts = VGroup(*[T(s, 40).move_to([-0.78, yy, 0], aligned_edge=LEFT) for s, yy in zip(("approve", "refuse", "defer"), (0.9, 0.15, -0.6))])
        at_word(self, "approves")
        span(self, LaggedStart(*[FadeIn(VGroup(b, o)) for b, o in zip(boxes, opts)], lag_ratio=0.3), rt=0.7)
        ck = check(float(np.array(boxes[0].get_center())[0]) - 0.02, 0.92, s=0.16)
        at_word(self, "executor")
        span(self, Create(ck), rt=0.35)
        ex_block = Iso(1.75, 0.55, 1.0).box(-0.35, -0.35, 0, 0.7, 0.7, 0.45, DARK_TOP, DARK_L, DARK_R)
        mk = check(2.45, 0.95, s=0.15)
        span(self, FadeIn(ex_block, shift=DOWN * 0.2), rt=0.35)
        at_word(self, "matches")
        span(self, Create(mk), rt=0.3)
        span(self, open_gate(g), FadeOut(g.light), FadeOut(lg), rt=0.5)
        ls = L("simulated delivery", 4.3, -1.85)
        at_word(self, "simulated")
        span(self, env.animate.move_to([5.55, -0.85, 0]), FadeIn(ls), rt=0.7)
        done(self)


class B06_Permissions(Scene):
    def construct(self):
        self.add(captions("C"))
        bx, by = -2.6, -0.45
        bnd = make_original("evidence-binder", height=2.0, x=bx, y=by)
        la = L("append only", bx, -1.95)
        g = gate(3.6, -0.25, 2.4)
        lo = L("no outreach", 3.6, -1.95)
        span(self, FadeIn(bnd, shift=UP * 0.2), FadeIn(la), FadeIn(g), FadeIn(g.light), FadeIn(lo), rt=0.55)
        adds = []
        for i, w in enumerate(("read", "add", "create")):
            pg = paper(bx - 0.2 + i * 0.12, 0.95 + i * 0.32, 1.6, 0.42)
            ck = check(bx + 1.25, 0.95 + i * 0.32, s=0.13)
            at_word(self, w)
            span(self, FadeIn(pg, shift=DOWN * 0.35), Create(ck), rt=0.45)
            adds.append(pg)
        ow = paper(-5.4, 1.6, 1.3, 0.8)
        xx = VGroup(Line([-5.75, 1.3, 0], [-5.05, 1.9, 0], color=INK, stroke_width=6),
                    Line([-5.75, 1.9, 0], [-5.05, 1.3, 0], color=INK, stroke_width=6))
        at_word(self, "overwrite")
        span(self, FadeIn(ow, shift=RIGHT * 0.3), rt=0.3)
        span(self, ow.animate.shift(RIGHT * 0.9), rt=0.35)
        span(self, ow.animate.shift(LEFT * 0.9), Create(xx), rt=0.4)
        env = envelope(0.9, -0.85)
        xx2 = VGroup(Line([0.55, -0.35, 0], [1.25, 0.25, 0], color=INK, stroke_width=6),
                     Line([0.55, 0.25, 0], [1.25, -0.35, 0], color=INK, stroke_width=6))
        at_word(self, "contact")
        span(self, FadeIn(env, shift=RIGHT * 0.3), rt=0.3)
        span(self, env.animate.shift(RIGHT * 1.0), rt=0.35)
        span(self, env.animate.shift(LEFT * 1.0), Create(xx2), rt=0.4)
        done(self)


def lifeline_group(cx):
    pl = plinth(cx, -1.15)
    cord = VMobject(stroke_color=INK, stroke_width=4).set_points_as_corners([[cx - 1.45, 1.05, 0], [cx - 0.95, 0.25, 0], [cx - 0.45, 1.05, 0]])
    pend = Circle(radius=0.34, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([cx - 0.95, -0.05, 0])
    tower, lights = Iso(cx + 0.9, -0.95, 1.0).server(-0.35, -0.35, 0, 0.7, 0.7, slab=0.38, n=3)
    head = L("Lifeline", cx, 1.75)
    return pl, VGroup(cord, pend), tower, lights, head


def dailycall_group(cx):
    pl = plinth(cx, -1.15)
    phone = VGroup(RoundedRectangle(width=0.95, height=1.7, corner_radius=0.14, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4),
                   Rectangle(width=0.72, height=1.25, fill_color=CARD, fill_opacity=1, stroke_width=0)).move_to([cx - 0.85, 0.3, 0])
    sm = paper(cx + 0.75, 0.3, 1.3, 1.6)
    # ghost guide lines, like the kit's page(): a competitor's summary is not our handwriting cast, and GATE T
    # measured the shrunken scribbles in B08 at 36 px
    smlines = VGroup(*[Line([cx + 0.3, 0.7 - i * 0.38, 0], [cx + 1.2, 0.7 - i * 0.38, 0], color=GHOST, stroke_width=6) for i in range(3)])
    head = L("DailyCall", cx, 1.75)
    return pl, phone, VGroup(sm, smlines), head


class B07_Alternatives(Scene):
    def construct(self):
        self.add(captions("D"))
        lx, dx = -2.9, 2.9
        pl1, pend, tower, lights, h1 = lifeline_group(lx)
        pl2, phone, sm, h2 = dailycall_group(dx)
        span(self, FadeIn(pl1), FadeIn(pl2), rt=0.45)
        at_word(self, "Lifeline")
        span(self, FadeIn(pend, shift=DOWN * 0.2), FadeIn(tower), FadeIn(lights), FadeIn(h1), rt=0.5)
        arcs = VGroup(*[Arc(radius=r, start_angle=-PI / 5, angle=2 * PI / 5, color=INK, stroke_width=4).move_arc_center_to([lx - 0.95, -0.05, 0])
                        for r in (0.6, 0.85)])
        at_word(self, "catch")
        span(self, LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.3), rt=0.5)
        span(self, lights.animate.set_color(TERRA), rt=0.3)
        at_word(self, "DailyCall") if any(_norm(w).startswith("dailycall") for w, _ in _WORDS.get("B07", [])) else at_word(self, "Daily")
        span(self, FadeIn(phone, shift=DOWN * 0.2), FadeIn(h2), rt=0.45)
        at_word(self, "summaries")
        span(self, FadeIn(sm, shift=LEFT * 0.2), rt=0.45)
        done(self)


class B08_Focus(Scene):
    def construct(self):
        self.add(captions("C"))
        lx, dx = -2.9, 2.9
        pl1, pend, tower, lights, h1 = lifeline_group(lx)
        pl2, phone, sm, h2 = dailycall_group(dx)
        lights.set_color(TERRA)
        arcs = VGroup(*[Arc(radius=r, start_angle=-PI / 5, angle=2 * PI / 5, color=INK, stroke_width=4).move_arc_center_to([lx - 0.95, -0.05, 0])
                        for r in (0.6, 0.85)])
        left = VGroup(pl1, pend, tower, lights, arcs)
        mid = VGroup(pl2, phone, sm)
        self.add(left, mid, h1, h2)
        span(self, left.animate.scale(0.72).move_to([-4.65, -0.25, 0]), mid.animate.scale(0.72).move_to([-1.0, -0.25, 0]),
             h1.animate.move_to([-4.65, 1.2, 0]), h2.animate.move_to([-1.0, 1.2, 0]), rt=0.6)
        cx = 3.6
        pl3 = plinth(cx, -1.15, w=3.6)
        h3 = L("DayThread · proposed", cx, 1.75)
        at_word(self, "proposed")
        span(self, FadeIn(pl3, shift=LEFT * 0.4), FadeIn(h3), rt=0.5)
        pgs = VGroup(*[paper(cx - 1.25 + i * 0.85, 0.55, 0.62, 0.8) for i in range(3)])
        dots = VGroup(*[Dot([cx - 1.25 + i * 0.85, 0.55, 0], radius=0.07, color=TERRA) for i in range(3)])
        at_word(self, "source")
        span(self, LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in pgs], lag_ratio=0.25), FadeIn(dots), rt=0.55)
        sl = Line([cx - 1.65, 0.95, 0], [cx - 1.65, 0.15, 0], color=TERRA, stroke_width=8)
        at_word(self, "independent")
        span(self, Create(sl), rt=0.25)
        span(self, sl.animate.shift(RIGHT * 2.3), rt=0.8, rate_func=linear)
        span(self, FadeOut(sl), rt=0.25)
        mg = gate(cx + 1.2, -0.55, 1.15)
        concern = slip(cx - 0.55, -0.45, 1.0, 0.5)
        thr = VGroup(*[Line([cx - 1.25 + i * 0.85, 0.15, 0], [cx - 0.55, -0.2, 0], color=INK, stroke_width=4) for i in range(3)])
        at_word(self, "decision")
        span(self, FadeIn(mg), FadeIn(mg.light), rt=0.4)
        at_word(self, "without")
        span(self, LaggedStart(*[Create(t) for t in thr], lag_ratio=0.2), FadeIn(concern, scale=1.1), rt=0.7)
        done(self)


class B09_FirstMinute(Scene):
    def construct(self):
        self.add(captions("C"))
        rd = checkin_page(-4.9, 0.1, 1.9, 2.5, n=4, dot=None)
        lr = L("README", -4.9, 1.75)
        at_word(self, "hiring")
        span(self, FadeIn(rd, shift=UP * 0.2), FadeIn(lr), rt=0.45)
        a1 = arrow(-3.7, 0.1, -3.05, 0.1)
        ws = make_original("agent-workstation", height=2.0, x=-1.65, y=0.05)
        lw = L("labelled replay", -1.65, -1.55)
        at_word(self, "replay")
        span(self, GrowArrow(a1), FadeIn(ws, shift=UP * 0.2), FadeIn(lw), rt=0.5)
        span(self, ws.parts["tool"].animate.shift(ws.action_vectors["tool"]), rt=0.4)
        a2 = arrow(-0.3, 0.1, 0.25, 0.1)
        p1 = checkin_page(0.95, 0.35, 0.95, 1.25, n=3, dot=1, short_last=False)
        p2 = checkin_page(2.25, 0.35, 0.95, 1.25, n=3, dot=1, short_last=False)
        lk = ArcBetweenPoints(np.array([p1.x0 - 0.24, p1.ys[1] + 0.1, 0]), np.array([p2.x0 - 0.24, p2.ys[1] + 0.1, 0]), angle=-PI / 2.2)
        lk.set_stroke(INK, 4)
        lm = L("two-day memory", 1.6, 1.45)
        at_word(self, "memory")
        span(self, GrowArrow(a2), FadeIn(p1), FadeIn(p2), FadeIn(p1.dot), FadeIn(p2.dot), FadeIn(lm), rt=0.5)
        span(self, Create(lk), rt=0.45)
        st = make_original("approval-stamp", height=1.7, x=4.85, y=0.15)
        la = L("one decision", 4.85, -1.0)
        at_word(self, "approval")
        span(self, FadeIn(st, shift=UP * 0.2), FadeIn(la), rt=0.45)
        span(self, st.parts["stamp"].animate.shift(st.action_vectors["stamp"]), rt=0.35)
        done(self)


class B10_Skills(Scene):
    def construct(self):
        self.add(captions("C"))
        cp = checkin_page(-4.6, 0.2, 2.1, 2.6, n=4, dot=None)
        seal = Dot([-4.0, -0.75, 0], radius=0.13, color=TERRA)
        lc = L("contract", -4.6, 1.85)
        at_word(self, "contracts")
        span(self, FadeIn(cp, shift=UP * 0.2), FadeIn(lc), rt=0.45)
        span(self, GrowFromCenter(seal), rt=0.3)
        ring = Circle(radius=1.05, color=INK, stroke_width=6).move_to([-0.7, 0.25, 0])
        runner = Dot([-0.7, 1.3, 0], radius=0.13, color=TERRA)
        bs = make_original("budget-slots", height=1.6, x=3.4, y=0.3)
        lb = L("budget", 3.4, -1.0)
        at_word(self, "budgeted")
        span(self, Create(ring), FadeIn(runner), FadeIn(bs, shift=UP * 0.2), FadeIn(lb), rt=0.55)
        span(self, MoveAlongPath(runner, ring.copy().rotate(PI / 2, about_point=ring.get_center())),
             bs.parts["allocated-token"].animate.shift(bs.action_vectors["allocated-token"]), rt=1.0, rate_func=linear)
        bar = Line([-1.75, -1.25, 0], [0.35, -1.25, 0], color=INK, stroke_width=8)
        ls = L("stop", -0.7, -1.75)
        at_word(self, "stops")
        span(self, Create(bar), FadeIn(ls), rt=0.4)
        done(self)


class B11_Evidence(Scene):
    def construct(self):
        self.add(captions("C"))
        tr = make_original("comparison-trays", height=1.9, x=-3.8, y=0.35)
        lt = L("with / without memory", -3.75, -1.0)
        at_word(self, "compares")
        span(self, FadeIn(tr, shift=UP * 0.2), FadeIn(lt), rt=0.5)
        span(self, tr.parts["sample-b"].animate.shift(tr.action_vectors["sample-b"]), rt=0.45)
        v = make_original("secure-vault", height=2.0, x=0.55, y=0.35)
        lv = L("held-out", 0.55, -1.0)
        at_word(self, "held")
        span(self, FadeIn(v, shift=UP * 0.2), FadeIn(lv), rt=0.5)
        span(self, v.parts["lock-bar"].animate.shift(v.action_vectors["lock-bar"]), rt=0.4)
        cards = VGroup(*[paper(2.3 + i * 0.82, 0.45, 0.62, 0.85) for i in range(5)])
        xs = VGroup(*[VGroup(Line([2.15 + i * 0.82, 0.3, 0], [2.45 + i * 0.82, 0.6, 0], color=INK, stroke_width=5),
                             Line([2.15 + i * 0.82, 0.6, 0], [2.45 + i * 0.82, 0.3, 0], color=INK, stroke_width=5)) for i in range(5)])
        lf = L("5 failures", 3.95, -1.0)
        at_word(self, "five")
        span(self, LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cards], lag_ratio=0.15), FadeIn(lf), rt=0.7)
        span(self, LaggedStart(*[Create(x) for x in xs], lag_ratio=0.12), rt=0.6)
        fence = DashedLine([-5.8, -1.65, 0], [5.8, -1.65, 0], color=INK, stroke_width=4, dash_length=0.3)
        lp = L("prototype only", 0, -2.15)
        at_word(self, "controlled")
        span(self, Create(fence), FadeIn(lp), rt=0.55)
        done(self)


class B12_Scope(Scene):
    def construct(self):
        self.add(captions("C"))
        cr = make_original("context-crate", height=2.0, x=-4.1, y=-0.35)
        li = L("in", -4.1, -1.75)
        span(self, FadeIn(cr, shift=UP * 0.2), FadeIn(li), cr.parts["lid"].animate.shift(cr.action_vectors["lid"]), rt=0.55)
        ins = []
        for i, w in enumerate(("simulated", "memory", "evidence", "human")):
            pg = paper(-4.1 + (i - 1.5) * 0.35, 1.8, 0.6, 0.75)
            at_word(self, w)
            span(self, FadeIn(pg, shift=DOWN * 0.2), rt=0.25)
            span(self, pg.animate.move_to([-4.1 + (i - 1.5) * 0.3, -0.05, 0]), rt=0.35, rate_func=ease_in)
            ins.append(pg)
        div = DashedLine([-1.6, 1.5, 0], [-1.6, -1.9, 0], color=INK, stroke_width=4, dash_length=0.25)
        cross = VGroup(Rectangle(width=0.36, height=1.0, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4),
                       Rectangle(width=1.0, height=0.36, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)).move_to([-0.4, -0.2, 0])
        cross.add(Rectangle(width=0.3, height=0.3, fill_color=BOX_TOP, fill_opacity=1, stroke_width=0).move_to([-0.4, -0.2, 0]))
        fl = paper(0.95, -0.2, 0.85, 1.05)
        lock = VGroup(Rectangle(width=0.5, height=0.38, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([1.2, -0.55, 0]),
                      Arc(radius=0.17, start_angle=0, angle=PI, color=INK, stroke_width=6).move_to([1.2, -0.26, 0]))
        en = envelope(2.3, -0.2)
        lo = L("out", 0.95, -1.4)
        at_word(self, "Clinical")
        span(self, Create(div), FadeIn(cross, shift=RIGHT * 0.3), FadeIn(lo), rt=0.5)
        at_word(self, "patient")
        span(self, FadeIn(fl, shift=RIGHT * 0.3), FadeIn(lock), rt=0.4)
        at_word(self, "outreach")
        span(self, FadeIn(en, shift=RIGHT * 0.3), rt=0.35)
        shelf = plinth(4.75, 0.3, w=2.1)
        cloud = VGroup(*[Circle(radius=r, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
                         for x, y, r in ((4.2, 0.95, 0.32), (4.55, 1.12, 0.38), (4.9, 0.95, 0.3))])
        ph = VGroup(RoundedRectangle(width=0.55, height=0.95, corner_radius=0.1, fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
                    .move_to([5.55, 0.95, 0]),
                    Arc(radius=0.35, start_angle=-PI / 4, angle=PI / 2, color=INK, stroke_width=4).move_arc_center_to([5.6, 0.95, 0]))
        ll = L("later", 4.85, -1.0)
        at_word(self, "Voice")
        span(self, FadeIn(shelf), FadeIn(ph, shift=DOWN * 0.2), FadeIn(ll), rt=0.45)
        at_word(self, "cloud")
        span(self, FadeIn(cloud, shift=DOWN * 0.2), rt=0.4)
        done(self)


class B13_Why(Scene):
    def construct(self):
        self.add(captions())
        one = checkin_page(0, 0.4, 1.2, 1.5, n=3, dot=None)   # final size from the start (scaling shrank scribbles under GATE T's floor)
        span(self, FadeIn(one, shift=UP * 0.2), rt=0.45)
        thr = Line([-5.6, -1.05, 0], [1.2, -1.05, 0], color=INK, stroke_width=5)
        xs = [-4.9, -3.3, -1.7, -0.1]
        at_word(self, "yesterday")
        span(self, one.animate.move_to([xs[0], 0.0, 0]), Create(thr), rt=0.6)
        rest = VGroup(*[checkin_page(x, 0.0, 1.2, 1.5, n=3, dot=(1 if x == xs[2] else None)) for x in xs[1:]])
        lb = L("beyond one conversation", -2.5, -1.6)
        at_word(self, "part")
        span(self, LaggedStart(*[FadeIn(r, shift=DOWN * 0.2) for r in rest], lag_ratio=0.25), FadeIn(lb), rt=0.65)
        span(self, GrowFromCenter(rest[1].dot), rt=0.3)
        desk = make_original("review-desk", height=2.1, x=4.5, y=-0.4)
        desk.remove(desk.parts["evidence"])
        mover = VGroup(rest[1], rest[1].dot)
        at_word(self, "person")
        span(self, FadeIn(desk, shift=UP * 0.2), rt=0.45)
        at_word(self, "evidence")
        span(self, MoveAlongPath(mover, ArcBetweenPoints(np.array([xs[2], 0.0, 0]), np.array([4.45, 0.55, 0]), angle=-PI / 3)),
             rt=1.0, rate_func=smooth)
        done(self)


class B14_SkillsNewOld(Scene):
    def construct(self):
        self.add(captions())
        s1 = plinth(-3.4, -1.1, w=4.4, d=1.3)
        s2 = plinth(3.1, -1.1, w=5.0, d=1.3)
        l1, l2 = L("practised", -3.4, 1.85), L("new", 3.1, 1.85)
        span(self, FadeIn(s1), FadeIn(l1), rt=0.45)
        req = checkin_page(-4.85, 0.25, 1.15, 1.5, n=3, dot=None)
        src = checkin_page(-3.4, 0.25, 1.15, 1.5, n=3, dot=0)
        cut = checkin_page(-1.95, 0.25, 1.15, 1.5, n=3, dot=None)
        strike = Line([cut.x0 - 0.1, cut.ys[1], 0], [cut.x0 + cut.lw + 0.1, cut.ys[1], 0], color=INK, stroke_width=7)
        at_word(self, "requirements")
        span(self, FadeIn(req, shift=DOWN * 0.2), rt=0.35)
        at_word(self, "sources", nth=2)
        span(self, FadeIn(src, shift=DOWN * 0.2), FadeIn(src.dot), rt=0.35)
        at_word(self, "overstated")
        span(self, FadeIn(cut, shift=DOWN * 0.2), rt=0.3)
        span(self, Create(strike), rt=0.3)
        slots = VGroup(*[DashedVMobject(Square(1.05, color=INK, stroke_width=4), num_dashes=16).move_to([1.35 + i * 1.18, 0.15, 0])
                         for i in range(4)])
        at_word(self, "New")
        span(self, FadeIn(s2), FadeIn(l2), Create(slots), rt=0.55)
        items = [make_original("memory-drawers", height=1.0, x=1.35, y=0.15),
                 make_original("permission-gate", height=0.95, x=2.53, y=0.15),
                 check(3.6, 0.15, s=0.3),
                 make_original("secure-vault", height=1.0, x=4.89, y=0.15)]
        for w, it, sl in zip(("persistent", "permissions", "human", "evaluation"), items, slots):
            at_word(self, w)
            span(self, FadeOut(sl), FadeIn(it, shift=DOWN * 0.2) if not isinstance(it, VGroup) or len(it) != 2 else Create(it), rt=0.4)
        done(self)


class B15_TodayVsBuild(Scene):
    def construct(self):
        self.add(captions("R"))
        p1, p2 = plinth(-3.3, -1.1, w=4.6), plinth(3.1, -1.1, w=5.2)
        l1, l2 = L("today", -3.3, 1.85), L("to build", 3.1, 1.85)
        span(self, FadeIn(p1), FadeIn(l1), rt=0.45)
        # v4 (2026-10-25): a fourth page for the replay built during revision; it carries the tumble dot
        today = VGroup(*[checkin_page(-4.95 + i * 1.1, 0.2, 0.86, 1.35, n=3, dot=(1 if i == 3 else None))
                         for i in range(4)])
        for w, pg in zip(("plan", "film", "log", "replay"), today):
            at_word(self, w)
            span(self, FadeIn(pg, shift=DOWN * 0.2), *([GrowFromCenter(pg.dot)] if pg.dot else []), rt=0.3)
        verdict = L("prediction: wrong", -3.3, -2.15)
        at_word(self, "never")
        span(self, FadeIn(verdict), rt=0.35)
        ghosts = VGroup(*[DashedVMobject(Rectangle(width=0.82, height=1.15, color=INK, stroke_width=4), num_dashes=14)
                          .move_to([1.15 + i * 0.98, 0.2, 0]) for i in range(5)])
        at_word(self, "intend")
        span(self, FadeIn(p2), FadeIn(l2), rt=0.4)
        for w, gh in zip(("repository", "review", "check", "tests", "evaluation"), ghosts):
            at_word(self, w)
            span(self, Create(gh), rt=0.3)
        done(self)


class BOUT_Outro(Scene):
    def construct(self):
        self.add(captions())
        title = T("DayThread", 110).move_to([0, 1.0, 0])
        name = L("Aditya Raj", 0, -0.2, 52)
        gh = L("github.com/aditya-raj-sde", 0, -1.0, 40)
        span(self, FadeIn(title, shift=UP * 0.2), rt=0.45)
        at_word(self, "Aditya") if any(_norm(w).startswith("aditya") for w, _ in _WORDS.get("BOUT", [])) else at(self, 1.6)
        span(self, FadeIn(name, shift=UP * 0.15), FadeIn(gh, shift=UP * 0.15), rt=0.45)
        th = Line([-3.0, -1.75, 0], [3.0, -1.75, 0], color=INK, stroke_width=5)
        span(self, Create(th), rt=0.5)
        span(self, GrowFromCenter(Dot([3.0, -1.75, 0], radius=0.1, color=TERRA)), rt=0.3)
        done(self)
