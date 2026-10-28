
# ═════════════════════════════ DAYTHREAD PREVIEW — scene body (hand-written) ═════════════════════════════
# Three beats of a CONSTRUCTED, PROPOSED workflow. Nothing here was observed from a running system.
# Cast: the original check-in page (raw transcript), the summary page, the separate check (scan line),
# the coordinator's review desk, the permission gate, and an outbound envelope that is never sent.
# Timing: each beat's audio = 0.30 s lead + Kokoro speech + a hold (pad_audio.py). Cue times below are
# the faster-whisper word starts (checks/whisper-words.txt) + the 0.30 s lead.

LEAD = 0.30
SCRIB_AMP = 0.085         # GATE T measures handwriting lines as text runs; the kit's 0.07 gave the short ones 40 px (< 41 px floor)
MID_GUARD = 0.22          # keep motion out of [mid - 0.22, mid + 0.22]: GATE T and Gate V sample the midpoint


def _target(self):
    return _TARGET.get(type(self).__name__.split("_")[0], 0.0)


def at(self, t):
    """Wait until absolute beat time t (seconds)."""
    gap = t - _elapsed(self)
    if gap > 0.02:
        self.wait(gap)


def span(self, *anims, rt=0.5, **kw):
    """Play `anims` for `rt` seconds, but never across the clip midpoint window."""
    target = _target(self)
    if target:
        mid, now = target / 2, _elapsed(self)
        if now < mid + MID_GUARD and now + rt > mid - MID_GUARD:
            at(self, mid + MID_GUARD)
    self.play(*anims, run_time=rt, **kw)


# ── captions that stay readable on every frame ──
def captions():
    c1 = T("Constructed — proposed workflow", 36).move_to([0, -3.02, 0])
    c2 = T("Synthesized voice reading Aditya’s script", 36).move_to([-6.1, 3.02, 0], aligned_edge=LEFT)
    return VGroup(c1, c2)


# ── the original check-in page (fixed numbers: Gate A's stub measures positions differently) ──
PX, PY, PW, PH = -3.4, 0.15, 3.2, 3.6
LINE_Y = [1.35, 0.85, 0.35, -0.15, -0.65]
TUMBLE = 2                                   # index of the line that mentions the tumble
LX0, LW = PX - PW / 2 + 0.55, PW - 0.95       # scribble start x and width


def original_page():
    pg = paper(PX, PY, PW, PH)
    lines = VGroup(*[scribble(LX0, y, LW * (0.6 if i == len(LINE_Y) - 1 else 1.0), amp=SCRIB_AMP) for i, y in enumerate(LINE_Y)])
    dot = Dot([LX0 - 0.25, LINE_Y[TUMBLE], 0], radius=0.09, color=TERRA)
    head = T("check-in", 40).move_to([PX, PY + PH / 2 + 0.42, 0])
    return pg, lines, dot, head


def tumble_label():
    lab = T("“a little tumble”", 42).move_to([1.15, LINE_Y[TUMBLE], 0])
    lead = Line([PX + PW / 2 + 0.15, LINE_Y[TUMBLE], 0], [-0.95, LINE_Y[TUMBLE], 0], color=INK, stroke_width=4)
    return lab, lead


# ── the summary page: shorter, with an empty dashed row where the tumble line should be ──
SX, SY, SW, SH = 4.55, 0.45, 2.4, 2.6
S_LINES = [1.3, 0.8, -0.2]
GAP_Y = 0.3


def summary_page():
    pg = paper(SX, SY, SW, SH)
    x0, w = SX - SW / 2 + 0.35, SW - 0.7
    lines = VGroup(*[scribble(x0, y, w * (0.55 if i == len(S_LINES) - 1 else 1.0), amp=SCRIB_AMP) for i, y in enumerate(S_LINES)])
    gap = DashedLine([x0, GAP_Y, 0], [x0 + w, GAP_Y, 0], color=DIM, stroke_width=4, dash_length=0.16)
    head = T("summary", 40).move_to([SX, SY + SH / 2 + 0.42, 0])
    missed = T("missed", 40).move_to([SX, SY - SH / 2 - 0.5, 0])
    return pg, lines, gap, head, missed


def scan_line(y):
    return Line([LX0 - 0.15, y, 0], [LX0 + LW + 0.1, y, 0], color=TERRA, stroke_width=8)


def stage_after_b01():
    pg, lines, dot, head = original_page()
    lab, lead = tumble_label()
    return pg, lines, dot, head, lab, lead


class B01_CheckIn(Scene):
    def construct(self):
        self.add(captions())
        pg, lines, dot, head = original_page()
        lab, lead = tumble_label()
        span(self, FadeIn(pg, shift=UP * 0.2), FadeIn(head), rt=0.5)
        span(self, LaggedStart(*[Create(l) for l in lines], lag_ratio=0.18), rt=0.75, rate_func=linear)
        at(self, LEAD + 0.94)                                # "a tumble"
        span(self, GrowFromCenter(dot), Create(lead), FadeIn(lab, shift=LEFT * 0.15), rt=0.4)
        finish(self)


class B02_Check(Scene):
    def construct(self):
        self.add(captions())
        pg, lines, dot, head, lab, lead = stage_after_b01()
        self.add(pg, lines, dot, head, lab, lead)
        spg, slines, gap, shead, missed = summary_page()
        summary = VGroup(spg, slines, gap)
        summary.shift(RIGHT * 2.2)
        at(self, LEAD + 0.05)                                # "The summary"
        span(self, summary.animate.shift(LEFT * 2.2), FadeIn(shead), rt=0.6)
        at(self, LEAD + 0.40)                                # "misses it"
        span(self, FadeIn(missed), Indicate(gap, color=INK, scale_factor=1.0), rt=0.5)
        # "DayThread's proposed check reads the original words": the separate check sweeps the ORIGINAL page
        sl = scan_line(LINE_Y[0] + 0.3)
        at(self, LEAD + 2.40)                                # "reads the original words"
        span(self, Create(sl), rt=0.25)                      # the guard holds this until just after the midpoint window
        self.play(sl.animate.move_to([sl.get_center()[0], LINE_Y[TUMBLE] - 0.12, 0]), run_time=0.9, rate_func=smooth)
        self.play(Indicate(VGroup(dot, lines[TUMBLE]), color=INK, scale_factor=1.08), run_time=0.5)
        finish(self)


class B03_Gate(Scene):
    def construct(self):
        self.add(captions())
        pg, lines, dot, head, lab, lead = stage_after_b01()
        spg, slines, gap, shead, missed = summary_page()
        sl = scan_line(LINE_Y[TUMBLE] - 0.12)
        self.add(pg, lines, dot, head, lab, lead, spg, slines, gap, shead, missed, sl)
        # the summary is not the evidence: it leaves; the room clears for the coordinator
        desk = make_original("review-desk", height=2.3, x=0.75, y=-0.25)
        desk.remove(desk.parts["evidence"])                  # our evidence slip replaces the prop's own page
        gate = make_original("permission-gate", height=2.5, x=4.35, y=-0.15)
        env = VGroup(Rectangle(width=0.95, height=0.62, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4),
                     VMobject(stroke_color=INK, stroke_width=4).set_points_as_corners([[-0.475, 0.31, 0], [0, -0.02, 0], [0.475, 0.31, 0]])
                     ).move_to([2.55, -0.85, 0])
        span(self, FadeOut(VGroup(spg, slines, gap, shead, missed)), FadeOut(VGroup(lab, lead)),
             FadeIn(desk, shift=UP * 0.2), FadeIn(gate, shift=UP * 0.2), rt=0.5)
        span(self, FadeIn(env, shift=RIGHT * 0.2), FadeIn(T("coordinator", 40).move_to([0.75, -2.0, 0])), rt=0.3)
        # "It brings them to a coordinator": the original words travel to the review desk
        slip = paper(PX + 0.2, LINE_Y[TUMBLE], 1.7, 0.75)
        sdot = Dot([PX - 0.45, LINE_Y[TUMBLE], 0], radius=0.08, color=TERRA)
        sline = scribble(PX - 0.25, LINE_Y[TUMBLE], 0.95, amp=SCRIB_AMP)
        ev = VGroup(slip, sdot, sline)
        span(self, FadeIn(ev, scale=1.1), rt=0.25)
        path = ArcBetweenPoints(np.array([PX + 0.2, LINE_Y[TUMBLE], 0]), np.array([0.85, 0.35, 0]), angle=-PI / 3)
        span(self, MoveAlongPath(ev, path), rt=0.75, rate_func=smooth)
        # "before anything is sent": the envelope stays on this side of the closed gate
        at(self, LEAD + 1.88)
        sent = T("nothing sent", 40).move_to([4.35, -2.0, 0])
        span(self, FadeIn(sent), Indicate(env, color=INK, scale_factor=1.06), rt=0.45)
        finish(self)
