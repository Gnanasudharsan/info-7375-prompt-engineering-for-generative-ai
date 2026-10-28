
# ═════════════════════════════ README CHECKER — scenes (Lavanya R) ═════════════════════════════
# Cut 2 (2026-10-13, after my review): every beat carries a question header (which of the seven
# assignment questions it answers), readable README steps, my REAL terminal output for the two runs,
# and one key sentence. Pacing: each beat builds before ~42% of its audio, holds still through the
# clip midpoint (GATE T / Gate V sample there), then adds its payoff after ~58%.
KRAFT_EDGE = "#9C8462"
MONO = "Menlo"


def at(self, frac):
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    gap = target * frac - _elapsed(self)
    if target and gap > 0.05:
        self.wait(gap)


def M(s, size=30, color=INK):
    return Text(s, font=MONO, color=color, font_size=size)


def header(s):
    return T(s, size=34).move_to([-6.05, 3.0, 0], aligned_edge=LEFT)


def keyline(s, size=36):
    return T(s, size=size).move_to([0, -3.0, 0])


def xmark(x, y, s=0.15, color=INK, w=7):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def warn(x, y, s=0.2):
    return Triangle(color=INK, stroke_width=6, fill_opacity=0).scale(s).move_to([x, y, 0])


def skip(x, y, s=0.17):
    return Line([x - s, y, 0], [x + s, y, 0], color=INK, stroke_width=7)


def mark(kind, x, y):
    return {"ok": lambda: check(x - 0.05, y, s=0.17), "x": lambda: xmark(x, y),
            "warn": lambda: warn(x, y), "skip": lambda: skip(x, y)}[kind]()


def container(ox, oy, s=0.85, w=2.0, d=2.0, h=1.3):
    iso = Iso(ox, oy, s)
    back, front = iso.open_box(0, 0, 0, w, d, h)
    return iso, back, front


def floor_shadow(x, y, w=3.4):
    return Ellipse(width=w, height=0.42, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def ghost_box(iso, x0, y0, z0, w, d, h, n=12):
    faces = iso.box(x0, y0, z0, w, d, h, CARD, CARD, CARD, sw=3)
    return VGroup(*[DashedVMobject(f.copy().set_fill(opacity=0).set_stroke(DIM, 3), num_dashes=n) for f in faces])


def panel(x0, x1, y0, y1):
    """A light terminal / report window: card body, grey title band (never a dark band in an ink card)."""
    body = Rectangle(width=x1 - x0, height=y1 - y0, fill_color=CARD, fill_opacity=1, stroke_color=INK,
                     stroke_width=4).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    band = Rectangle(width=x1 - x0, height=0.38, fill_color=BAR1, fill_opacity=1, stroke_width=0
                     ).move_to([(x0 + x1) / 2, y1 - 0.19, 0])
    return VGroup(body, band)


def steps(rows, x, y_top, gap=0.6, size=32):
    """README rows as readable text, left-aligned at x. Returns (VGroup, ys)."""
    g, ys = VGroup(), []
    for i, r in enumerate(rows):
        yy = y_top - i * gap
        g.add(T(r, size=size).move_to([x, yy, 0], aligned_edge=LEFT))
        ys.append(yy)
    return g, ys


def readme_page(x, y, w=2.4, h=3.0, rows=4):
    pg = paper(x, y, w, h)
    top = y + h / 2 - 0.45
    gap = (h - 0.8) / max(1, rows - 1)
    lines = VGroup(*[Line([x - w / 2 + 0.3, top - i * gap, 0], [x + w / 2 - 0.3 - (0.5 if i % 3 == 2 else 0), top - i * gap, 0],
                          color=GHOST, stroke_width=7) for i in range(rows)])
    return VGroup(pg, lines)


def page_rows(x, y, w, h, rows):
    """Row y-positions of readme_page(x, y, w, h, rows)."""
    top = y + h / 2 - 0.45
    gap = (h - 0.8) / max(1, rows - 1)
    return [top - i * gap for i in range(rows)]


# ─────────────────────────────── opening ───────────────────────────────
class BHELLO_Intro(Scene):
    def construct(self):
        sh = floor_shadow(-3.6, -1.85, w=3.0)
        iso, back, front = container(-3.6, -1.7, s=0.75)
        pg = iso.page(0.45, 0.3, 2.4, w=1.1, d=1.4)
        pg.set_z_index(1)
        t1 = T("README Checker", size=60, bold=True).move_to([2.2, 1.0, 0])
        t2 = T("Final project pitch · Lavanya · INFO 7375", size=34).move_to([2.2, 0.0, 0])
        self.play(FadeIn(sh), FadeIn(back), FadeIn(front), FadeIn(pg), Write(t1), run_time=1.0)
        self.play(Write(t2), run_time=0.7)
        at(self, 0.6)
        t3 = T("Nothing is built yet.", size=40).move_to([2.2, -1.3, 0])
        self.play(Write(t3), GrowFromCenter(Dot([t3.get_left()[0] - 0.35, -1.3, 0], radius=0.09, color=TERRA)),
                  pg.animate.shift(DOWN * iso.s * 2.0), run_time=0.8)
        finish(self)


class BDEFS_Terms(Scene):
    def construct(self):
        title = T("Terms In This Film", size=44).move_to([-6.0, 2.85, 0], aligned_edge=LEFT)
        rule = Line([-6.0, 2.3, 0], [6.0, 2.3, 0], color=GHOST, stroke_width=4)
        self.play(Write(title), Create(rule), run_time=0.8)
        rows = [("README", "the file that tells people how to set up the project", 1.45),
                ("container", "a throwaway sandbox that keeps commands off my laptop", -0.15),
                ("agent loop", "do the step, read its output, decide the next step", -1.75)]
        made = []
        for term, meaning, y in rows:
            made.append((Dot([-5.8, y, 0], radius=0.09, color=TERRA),
                         T(term, size=44, bold=True).move_to([-5.5, y, 0], aligned_edge=LEFT),
                         T(meaning, size=36).move_to([-5.5, y - 0.65, 0], aligned_edge=LEFT)))
        name = T("Lavanya", size=34).move_to([6.0, -3.05, 0], aligned_edge=RIGHT)
        at(self, 0.04)
        self.play(GrowFromCenter(made[0][0]), Write(made[0][1]), run_time=0.5)
        self.play(FadeIn(made[0][2]), FadeIn(name), run_time=0.5)
        at(self, 0.25)
        self.play(GrowFromCenter(made[1][0]), Write(made[1][1]), run_time=0.5)
        self.play(FadeIn(made[1][2]), run_time=0.5)
        at(self, 0.6)
        self.play(GrowFromCenter(made[2][0]), Write(made[2][1]), run_time=0.5)
        self.play(FadeIn(made[2][2]), run_time=0.5)
        finish(self)


# ─────────────────────────────── Q2: the problem + my two real runs ───────────────────────────────
class B00_Problem(Scene):
    def construct(self):
        h = header("The problem")
        pg = readme_page(-2.0, 0.0, w=4.0, h=4.2, rows=5)
        ys = page_rows(-2.0, 0.0, 4.0, 4.2, 5)
        self.play(FadeIn(h), FadeIn(pg, shift=DOWN * 0.2), run_time=0.8)
        lab = T("README", size=40).move_to([2.6, 1.3, 0])
        self.play(Write(lab), run_time=0.4)
        cur = cursor(0.3, ys[0] + 0.1)
        self.play(FadeIn(cur), run_time=0.2)
        self.play(cur.animate.move_to([0.45, ys[1] - 0.05, 0]), run_time=0.5)
        at(self, 0.58)
        self.play(cur.animate.move_to([0.45, ys[2] - 0.05, 0]), run_time=0.4)
        self.play(Create(xmark(1.15, ys[2], s=0.2)), run_time=0.4)
        k = keyline("Is it me, or the instructions?", size=40)
        self.play(Write(k), run_time=0.6)
        finish(self)


WEBAPP_STEPS = [("1   git clone <repository-url>", "warn", "placeholder, no real link"),
                ("2   yarn install", "ok", "worked"),
                ("3   yarn sequelize db:migrate", "x", "config.json missing"),
                ("4   check the table in DBeaver", "skip", "skipped: needs a GUI app"),
                ("5   docker start <container-name>", "warn", "placeholder"),
                ("6   node app.js", "x", "database SSL error"),
                ("7   GET /healthz in Postman", "x", "503")]


class B01_MyRun(Scene):
    def construct(self):
        h = header("2 · Why care?   Real run 1: my own README")
        pg = readme_page(-2.6, -0.1, w=4.2, h=4.8, rows=7)
        ys = page_rows(-2.6, -0.1, 4.2, 4.8, 7)
        self.play(FadeIn(h), FadeIn(pg, shift=DOWN * 0.2), run_time=0.8)
        src = T("my webapp README · fresh clone · Oct 13, 2026", size=32).move_to([0, -3.05, 0])
        self.play(FadeIn(src), run_time=0.5)
        kinds = ["warn", "ok", "x", "skip", "warn", "x", "x"]
        marks = [mark(k, 0.0, ys[i]) for i, k in enumerate(kinds)]
        notes = {0: "placeholder", 2: "missing file", 6: "503"}
        nt = {i: T(n, size=34).move_to([0.5, ys[i], 0], aligned_edge=LEFT) for i, n in notes.items()}
        for i in range(3):
            self.play(Create(marks[i]), *([FadeIn(nt[i])] if i in nt else []), run_time=0.35)
        at(self, 0.58)
        for i in range(3, 7):
            self.play(Create(marks[i]), *([FadeIn(nt[i])] if i in nt else []), run_time=0.35)
            self.wait(0.15)
        finish(self)


class B01T_Terminal(Scene):
    def construct(self):
        h = header("2 · Real run 1: my actual terminal output")
        win = panel(-6.0, 6.0, -1.7, 1.9)
        lab = T("real output · Oct 13, 2026", size=32).move_to([0, -2.4, 0])
        self.play(FadeIn(h), FadeIn(win), FadeIn(lab), run_time=0.8)
        L = [M('ERROR: Cannot find "…/config/config.json".'), M("HTTP/1.1 503 Service Unavailable")]
        L[0].move_to([-5.6, 0.75, 0], aligned_edge=LEFT)
        L[1].move_to([-5.6, -0.65, 0], aligned_edge=LEFT)
        at(self, 0.25)
        self.play(FadeIn(L[0]), run_time=0.3)
        bar1 = Line([-5.75, L[0].get_bottom()[1] - 0.12, 0], [L[0].get_right()[0], L[0].get_bottom()[1] - 0.12, 0],
                    color=TERRA, stroke_width=5)
        self.play(Create(bar1), run_time=0.4)
        at(self, 0.6)
        self.play(FadeIn(L[1]), run_time=0.3)
        bar2 = Line([-5.75, L[1].get_bottom()[1] - 0.12, 0], [L[1].get_right()[0], L[1].get_bottom()[1] - 0.12, 0],
                    color=TERRA, stroke_width=5)
        self.play(Create(bar2), run_time=0.4)
        finish(self)


HEROKU_STEPS = [("0   install Node.js and the Heroku CLI", "warn", "Heroku CLI not needed"),
                ("1   git clone …/nodejs-getting-started.git", "ok", "worked (redirected)"),
                ("2   npm install", "warn", "wants npm 12, I have 10"),
                ("3   npm start", "ok", "Listening on 5006"),
                ("4   open localhost:5006", "ok", "200 OK")]


class B02_HerokuRun(Scene):
    def construct(self):
        h = header("2 · Why care?   Real run 2: an open-source README")
        pg = readme_page(-2.6, 0.0, w=4.2, h=4.0, rows=5)
        ys = page_rows(-2.6, 0.0, 4.2, 4.0, 5)
        self.play(FadeIn(h), FadeIn(pg, shift=DOWN * 0.2), run_time=0.8)
        src = T("Heroku's Node.js starter README · Oct 13, 2026", size=32).move_to([0, -3.05, 0])
        self.play(FadeIn(src), run_time=0.5)
        at(self, 0.58)
        for i, k in enumerate(["warn", "ok", "warn", "ok", "ok"]):
            self.play(Create(mark(k, 0.0, ys[i])), run_time=0.3)
        s1 = T("it worked", size=40).move_to([3.6, 0.6, 0])
        s2 = T("2 small warnings", size=34).move_to([3.6, -0.3, 0])
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.5)
        finish(self)


class B02T_Terminal(Scene):
    def construct(self):
        h = header("2 · Real run 2: my actual terminal output")
        win = panel(-6.0, 6.0, -1.7, 1.9)
        lab = T("real output · Oct 13, 2026", size=32).move_to([0, -2.4, 0])
        self.play(FadeIn(h), FadeIn(win), FadeIn(lab), run_time=0.8)
        L = [M("npm warn EBADENGINE …  npm: '12.x' }"), M("HTTP/1.1 200 OK")]
        L[0].move_to([-5.6, 0.75, 0], aligned_edge=LEFT)
        L[1].move_to([-5.6, -0.65, 0], aligned_edge=LEFT)
        at(self, 0.2)
        self.play(FadeIn(L[0]), run_time=0.3)
        bar = Line([-5.75, L[0].get_bottom()[1] - 0.1, 0], [L[0].get_right()[0], L[0].get_bottom()[1] - 0.1, 0],
                   color=TERRA, stroke_width=5)
        self.play(Create(bar), run_time=0.4)
        at(self, 0.6)
        self.play(FadeIn(L[1]), run_time=0.3)
        self.play(Create(check(L[1].get_right()[0] + 0.5, L[1].get_center()[1], s=0.17)), run_time=0.3)
        finish(self)


# ─────────────────────────────── Q1: what it is, how it works, what it produces ───────────────────────────────
class B03_WhatItIs(Scene):
    def construct(self):
        h = header("1 · What is it?")
        sh = floor_shadow(-2.4, -2.05, w=3.2)
        iso, back, front = container(-2.4, -1.9)
        self.play(FadeIn(h), FadeIn(sh), FadeIn(back), FadeIn(front), run_time=0.8)
        l1 = T("README Checker", size=48, bold=True).move_to([2.8, 1.4, 0])
        l2 = T("a command-line tool", size=34).move_to([2.8, 0.55, 0])
        l3 = T("in a public GitHub repo", size=34).move_to([2.8, -0.05, 0])
        l4 = T("container", size=32).move_to([-2.4, 1.95, 0])
        self.play(Write(l1), FadeIn(l2), FadeIn(l3), FadeIn(l4), run_time=0.9)
        pg = iso.page(0.45, 0.3, 2.6, w=1.1, d=1.4)
        pg.set_z_index(1)
        self.play(FadeIn(pg), run_time=0.4)
        at(self, 0.58)
        self.play(pg.animate.shift(DOWN * iso.s * 2.3), run_time=0.8, rate_func=ease_in)
        k = keyline("Will run every README step inside a throwaway container")
        self.play(Write(k), run_time=0.6)
        finish(self)


class B04_Loop(Scene):
    def construct(self):
        h = header("1 · How it will work: the agent loop")
        P = {"run": np.array([-1.6, 1.3, 0]), "read": np.array([1.8, -1.4, 0]), "decide": np.array([-4.2, -1.4, 0])}
        nodes = VGroup(*[Circle(radius=0.42, color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to(p)
                         for p in P.values()])
        self.play(FadeIn(h), LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.3), run_time=1.0)
        labs = VGroup(T("run one step", size=34).next_to(nodes[0], UP, buff=0.25),
                      T("read the real output", size=34).next_to(nodes[1], RIGHT, buff=0.3),
                      T("decide", size=34).next_to(nodes[2], DOWN, buff=0.25))
        self.play(FadeIn(labs), run_time=0.6)
        order = [("run", "read"), ("read", "decide"), ("decide", "run")]
        arcs = VGroup(*[ArcBetweenPoints(P[a] + (P[b] - P[a]) / np.linalg.norm(P[b] - P[a]) * 0.5,
                                         P[b] - (P[b] - P[a]) / np.linalg.norm(P[b] - P[a]) * 0.5,
                                         angle=-PI / 4, color=KRAFT_EDGE, stroke_width=5) for a, b in order])
        self.play(Create(arcs), run_time=0.8)
        opts = T("continue  ·  stop  ·  mark unclear", size=32).move_to([3.2, 1.6, 0])
        self.play(FadeIn(opts), run_time=0.4)
        at(self, 0.58)
        dot = Dot(arcs[0].get_start(), radius=0.12, color=TERRA)
        self.play(FadeIn(dot), run_time=0.2)
        for a in arcs:
            self.play(MoveAlongPath(dot, a), run_time=0.6, rate_func=linear)
        k = keyline("The AI picks the move. Real commands decide the result.")
        self.play(Write(k), run_time=0.6)
        finish(self)


REPORT_ROWS = [("warn", "step 1  ·  warning  ·  placeholder"),
               ("x", "step 3  ·  fail  ·  missing file"),
               ("warn", "step 5  ·  warning  ·  placeholder")]


class B05_Report(Scene):
    def construct(self):
        h = header("1 · What it will produce")
        win = panel(-6.0, 6.0, -2.15, 2.25)
        title = T("report.md", size=34, bold=True).move_to([-5.5, 1.45, 0], aligned_edge=LEFT)
        stamp = T("CONSTRUCTED MOCK-UP · not built yet", size=36, bold=True).move_to([0, -2.85, 0])
        self.play(FadeIn(h), FadeIn(win), Write(title), run_time=0.9)
        self.play(FadeIn(stamp), run_time=0.5)
        rows = []
        for i, (k, s) in enumerate(REPORT_ROWS):
            y = 0.5 - i * 0.85
            rows.append((mark(k, -5.3, y), T(s, size=32).move_to([-4.8, y, 0], aligned_edge=LEFT)))
        for m, t in rows[:1]:
            self.play(Create(m), FadeIn(t), run_time=0.35)
        at(self, 0.58)
        for m, t in rows[1:]:
            self.play(Create(m), FadeIn(t), run_time=0.35)
        finish(self)


# ─────────────────────────────── Q2: the alternative I use already ───────────────────────────────
class B06_NotCI(Scene):
    def construct(self):
        h = header("2 · Isn't that what CI does?")
        left = panel(-6.0, -0.6, -2.0, 1.75)
        lt = T("my CI pipeline", size=34).move_to([-3.3, 2.2, 0])
        lines = VGroup(*[Line([-5.5, y, 0], [-2.2, y, 0], color=GHOST, stroke_width=7) for y in (0.75, 0.0, -0.75)])
        self.play(FadeIn(h), FadeIn(left), FadeIn(lt), FadeIn(lines), run_time=0.9)
        pg = readme_page(3.1, 0.15, w=4.4, h=3.2, rows=4)
        rt = T("my README", size=34).move_to([3.1, 2.2, 0])
        self.play(FadeIn(pg), FadeIn(rt), run_time=0.8)
        at(self, 0.58)
        cks = VGroup(*[check(-1.4, y, s=0.17) for y in (0.75, 0.0, -0.75)])
        self.play(LaggedStart(*[Create(c) for c in cks], lag_ratio=0.3), run_time=0.8)
        nt = T("never run by CI", size=34).move_to([3.1, -2.05, 0])
        self.play(FadeIn(nt), run_time=0.4)
        k = keyline("CI tests the code, not the instructions a person reads.")
        self.play(Write(k), run_time=0.6)
        finish(self)


# ─────────────────────────────── Q3: who opens it ───────────────────────────────
class B07_Reader(Scene):
    def construct(self):
        h = header("3 · Who opens it, and what do they do?")
        win = panel(-6.0, 1.9, -1.8, 1.0)
        cmd = M("$ readme-check ./sample-app", size=30).move_to([-5.6, 0.0, 0], aligned_edge=LEFT)
        tag = T("planned command (constructed)", size=32).move_to([-2.05, -2.3, 0])
        self.play(FadeIn(h), FadeIn(win), run_time=0.7)
        self.play(AddTextLetterByLetter(cmd), run_time=1.0)
        self.play(FadeIn(tag), run_time=0.4)
        who = T("reader: hiring managers and engineers", size=32).move_to([-6.0, 2.25, 0], aligned_edge=LEFT)
        role = T("target role: Software Engineer", size=32).move_to([-6.0, 1.65, 0], aligned_edge=LEFT)
        self.play(FadeIn(who), FadeIn(role), run_time=0.5)
        at(self, 0.58)
        rp = readme_page(4.2, -0.3, w=2.2, h=2.4, rows=4)
        rl = T("report.md", size=32).next_to(rp, DOWN, buff=0.2)
        self.play(FadeIn(rp, shift=LEFT * 0.4), FadeIn(rl), run_time=0.6)
        k = keyline("One command. A report they can check, in about a minute.")
        self.play(Write(k), run_time=0.6)
        finish(self)


# ─────────────────────────────── Q4: how I'll prove it, what it proves ───────────────────────────────
class B08_Eval(Scene):
    def construct(self):
        h = header("4 · How will I know it works?")
        boxes, tops = VGroup(), []
        for r in range(2):
            for c in range(5):
                iso = Iso(-5.4 + c * 1.45, 0.55 - r * 1.9, 0.5)
                boxes.add(iso.box(0, 0, 0, 1.0, 1.0, 0.8))
                tops.append(iso.p(0.5, 0.5, 0.8))
        self.play(FadeIn(h), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in boxes], lag_ratio=0.08), run_time=1.3)
        l1 = T("~10 sample projects", size=32).move_to([-2.5, 2.25, 0])
        self.play(FadeIn(l1), run_time=0.4)
        sparks = VGroup(*[Dot(tops[i], radius=0.09, color=TERRA) for i in (0, 3, 4, 6, 8)])
        l2 = T("dot = a problem I plant", size=32).move_to([-2.5, -2.3, 0])
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sparks], lag_ratio=0.2), FadeIn(l2), run_time=0.8)
        at(self, 0.58)
        scan = Line([-5.9, -1.9, 0], [-5.9, 1.9, 0], color=TERRA, stroke_width=6)
        self.play(FadeIn(scan), run_time=0.15)
        self.play(scan.animate.shift(RIGHT * 7.3), run_time=1.2, rate_func=linear)
        self.play(FadeOut(scan), run_time=0.15)
        s1 = T("caught:  ? / planted", size=40).move_to([4.2, 0.7, 0])
        s2 = T("false alarms:  ?", size=40).move_to([4.2, -0.4, 0])
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.5)
        k = keyline("These numbers don't exist yet.")
        self.play(Write(k), run_time=0.5)
        finish(self)


SKILLS = [("agent loop", 0.17), ("verification · real output", 0.33), ("evaluation · a score", 0.6),
          ("source grounding · README lines", 0.72), ("prompt contract · checked by code", 0.85)]


class B09_Skills(Scene):
    def construct(self):
        h = header("4 · What will it prove about me?")
        sh = floor_shadow(-3.8, -2.05, w=3.0)
        iso, back, front = container(-3.8, -1.9, s=0.75)
        plinth = iso.box(-0.25, -0.25, -0.45, 2.5, 2.5, 0.45, DARK_TOP, DARK_L, DARK_R)
        plinth.set_z_index(-1)
        self.play(FadeIn(h), FadeIn(sh), FadeIn(plinth), FadeIn(back), FadeIn(front), run_time=0.8)
        lab = T("five course skills", size=34, bold=True).move_to([-1.2, 2.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(lab), run_time=0.4)
        items = []
        for i, (s, _) in enumerate(SKILLS):
            y = 1.3 - i * 0.78
            items.append((Dot([-1.0, y, 0], radius=0.09, color=TERRA), T(s, size=34).move_to([-0.7, y, 0], aligned_edge=LEFT)))
        for (d, t), (_, frac) in zip(items[:2], SKILLS[:2]):
            at(self, frac)
            self.play(GrowFromCenter(d), FadeIn(t), run_time=0.4)
        at(self, 0.58)
        for (d, t), (_, frac) in zip(items[2:], SKILLS[2:]):
            at(self, frac)
            self.play(GrowFromCenter(d), FadeIn(t), run_time=0.4)
        finish(self)


# ─────────────────────────────── Q5: in, out, first ───────────────────────────────
class B10_First(Scene):
    def construct(self):
        h = header("5 · What's in, what's out, what comes first?")
        o = T("OUT", size=36, bold=True).move_to([-4.3, 2.2, 0])
        pen = Polygon([-5.0, -0.6, 0], [-4.7, -0.9, 0], [-3.0, 0.8, 0], [-3.3, 1.1, 0],
                      fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4)
        tip = Polygon([-5.0, -0.6, 0], [-4.7, -0.9, 0], [-5.2, -1.1, 0], fill_color=INK, fill_opacity=1, stroke_width=0)
        self.play(FadeIn(h), FadeIn(o), FadeIn(pen), FadeIn(tip), run_time=0.7)
        self.play(Create(xmark(-4.1, 0.1, s=0.85, w=9)), run_time=0.4)
        l1 = T("won't fix READMEs", size=32).move_to([-4.1, -1.75, 0])
        self.play(FadeIn(l1), run_time=0.4)
        f = T("FIRST", size=36, bold=True).move_to([2.4, 2.2, 0])
        sh = floor_shadow(0.4, -1.95, w=2.6)
        iso, back, front = container(0.4, -1.8, s=0.65)
        self.play(FadeIn(f), FadeIn(sh), FadeIn(back), FadeIn(front), run_time=0.6)
        pg = iso.page(0.45, 0.3, 2.8, w=1.1, d=1.4)
        pg.set_z_index(1)
        self.play(FadeIn(pg), run_time=0.3)
        at(self, 0.58)
        self.play(pg.animate.shift(DOWN * iso.s * 2.5), run_time=0.6, rate_func=ease_in)
        win = panel(1.9, 6.1, -1.3, 1.3)
        r1 = M("report.md", size=30).move_to([2.2, 0.4, 0], aligned_edge=LEFT)
        r2 = T("exit code per step", size=32).move_to([2.2, -0.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(win), FadeIn(r1), FadeIn(r2), run_time=0.6)
        k = keyline("First milestone: report.md with a real exit code for every step")
        self.play(Write(k), run_time=0.6)
        finish(self)


# ─────────────────────────────── Q6: what could sink it ───────────────────────────────
class B11_Risk(Scene):
    def construct(self):
        h = header("6 · What could sink it?")
        sh = floor_shadow(-3.6, -1.95, w=3.0)
        iso = Iso(-3.6, -1.8, 0.75)
        bx = iso.box(0, 0, 0, 2.0, 2.0, 1.3)
        lc = iso.p(1.0, 0.0, 0.55)
        body = Rectangle(width=0.6, height=0.48, fill_color=DIM, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(lc)
        shack = Arc(radius=0.21, start_angle=0, angle=PI, color=INK, stroke_width=7).move_to(lc + np.array([0, 0.36, 0]))
        self.play(FadeIn(h), FadeIn(sh), FadeIn(bx), FadeIn(body), Create(shack), run_time=0.8)
        risk = T("risk: a README can contain any command", size=32).move_to([2.2, 2.2, 0])
        f1 = T("disposable container", size=32).move_to([1.0, 1.25, 0], aligned_edge=LEFT)
        f2 = T("no secrets, no access to my files", size=32).move_to([1.0, 0.6, 0], aligned_edge=LEFT)
        f3 = T("deleted after every run", size=32).move_to([1.0, -0.05, 0], aligned_edge=LEFT)
        self.play(FadeIn(risk), run_time=0.4)
        self.play(FadeIn(f1), FadeIn(f2), FadeIn(f3), run_time=0.6)
        at(self, 0.58)
        old = VGroup(bx, body, shack)
        self.play(old.animate.shift(LEFT * 1.6).set_opacity(0), run_time=0.6)
        fresh = iso.box(0, 0, 0, 2.0, 2.0, 1.3)
        self.play(FadeIn(fresh, shift=DOWN * 0.3), run_time=0.5)
        v = T('"set up your database"  →  unclear', size=34).move_to([2.6, -1.3, 0])
        self.play(FadeIn(v), run_time=0.4)
        k = keyline("Vague steps get marked unclear, not guessed.")
        self.play(Write(k), run_time=0.5)
        finish(self)


# ─────────────────────────────── Q7: why this project ───────────────────────────────
class B12_Why(Scene):
    def construct(self):
        h = header("7 · Why this project? A mix")
        hv = T("I already have", size=36, bold=True).move_to([-3.2, 2.2, 0])
        have, hys = steps(["CI/CD · GitHub Actions", "Cloud · AWS + GCP images", "proof: github.com/LavanyaRajesh24/webapp",
                           "Docker · used, no public proof yet"], -5.9, 1.35, gap=0.75, size=32)
        self.play(FadeIn(h), FadeIn(hv), run_time=0.6)
        for t in have[:3]:
            self.play(FadeIn(t), run_time=0.35)
        at(self, 0.4)
        self.play(FadeIn(have[3]), run_time=0.35)
        nw = T("new to me", size=36, bold=True).move_to([3.6, 2.2, 0])
        self.play(FadeIn(nw), run_time=0.3)
        at(self, 0.58)
        new, nys = steps(["agent loops", "evaluation", "source grounding", "prompt contracts"], 2.4, 1.35, gap=0.75, size=32)
        for t in new:
            self.play(FadeIn(t), run_time=0.4)
            self.wait(0.3)
        k = keyline("Showing what I know. Learning what I don't.")
        self.play(Write(k), run_time=0.5)
        finish(self)


# ─────────────────────────────── exists vs. will exist ───────────────────────────────
class B13_Exists(Scene):
    def construct(self):
        h = header("What exists today, and what will exist")
        s1 = Line([-6.0, 0.5, 0], [6.0, 0.5, 0], color=KRAFT_EDGE, stroke_width=8)
        e = T("exists today", size=34, bold=True).move_to([-5.9, 2.25, 0], aligned_edge=LEFT)
        items = VGroup(T("this pitch film", size=32), T("my 2 README tests", size=32), T("my webapp repo", size=32))
        for i, t in enumerate(items):
            t.move_to([-5.9 + i * 4.1, 1.15, 0], aligned_edge=LEFT)
        self.play(FadeIn(h), Create(s1), FadeIn(e), FadeIn(items), run_time=1.0)
        at(self, 0.58)
        s2 = Line([-6.0, -2.3, 0], [6.0, -2.3, 0], color=KRAFT_EDGE, stroke_width=8)
        w = T("will exist", size=34, bold=True).move_to([-5.9, -0.55, 0], aligned_edge=LEFT)
        iso = Iso(4.6, -2.3, 0.5)
        g1 = ghost_box(iso, 0, 0, 0, 1.4, 1.4, 1.0)
        fut = VGroup(T("the tool", size=32), T("~10 sample repos", size=32), T("the scores", size=32))
        for i, t in enumerate(fut):
            t.move_to([-5.9 + i * 3.4, -1.5, 0], aligned_edge=LEFT)
        self.play(Create(s2), FadeIn(w), Create(g1), FadeIn(fut), run_time=0.9)
        finish(self)


class B14_Outro(Scene):
    def construct(self):
        sh = floor_shadow(-3.6, -1.85, w=3.0)
        iso, back, front = container(-3.6, -1.7, s=0.75)
        pg = iso.page(0.45, 0.3, 0.9, w=1.1, d=1.4)
        pg.set_z_index(1)
        t1 = T("README Checker", size=56, bold=True).move_to([2.0, 0.6, 0])
        t2 = T("Does the README actually work?", size=36).move_to([2.0, -0.4, 0])
        self.play(FadeIn(sh), FadeIn(back), FadeIn(front), FadeIn(pg), Write(t1), Write(t2), run_time=1.4)
        at(self, 0.58)
        self.play(GrowFromCenter(Dot([2.0, -1.2, 0], radius=0.1, color=TERRA)), run_time=0.4)
        finish(self)