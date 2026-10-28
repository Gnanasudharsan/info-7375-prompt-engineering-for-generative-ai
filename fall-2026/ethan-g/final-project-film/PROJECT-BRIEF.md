# PROJECT-BRIEF — DataSentry (working title)

**Ethan Gomes · INFO 7375 · Final Project Pitch · written 2026-10-14, revised 2026-10-25**
**Target role:** Data Engineer (also Data Analyst / BI) · **Stack:** Python, pandas, pandera, Claude (Opus 5.5); NYC TLC
taxi data (public). dbt and Great Expectations used only to compare against.

**1. What is it?** DataSentry has an AI write data-quality checks for a table, then scores those checks by planting
known defects and counting how many they catch. When done, it will be a public GitHub repository with three parts, all
of which have already run: a check writer (Claude, given only column names and types, writing pandera checks under a
prompt contract), a defect planter (five defect types, with an answer key no check reads), and a scorecard (CAUGHT or
MISSED per defect type, plus false alarms on a clean copy).

**2. Why would anyone care?** It tells a data engineer which bad rows their checks let through. On 2026-10-25 I ran
one rule, `fare_amount >= 0`, in **dbt** (dbt-duckdb) and **Great Expectations** (GX Core) on a clean 10,000-row
sample and a broken copy. Both passed the clean copy and flagged the 25 negative fares. Neither said anything about
the 25 trips I planted that end before they start, because no rule asked. GX Cloud's ExpectAI already suggests checks
with AI (paid; I did not run it). DataSentry does what neither does: it grades a set of checks, AI-written or not,
against defects you know are there.

**3. Who opens it?** A hiring manager for a data engineering role. After a one-time setup (`./run_all.sh`, which
downloads the data), they run one command, `./score_round.sh 2`, and within a minute read the scorecard. On 2026-10-25: my one hand-written rule caught 2 of 5 defect types
(clean PASS); Claude's round 1 caught 5 of 5 but flagged 220 good trips; round 2, told only about those false alarms,
flagged none but dropped the negative-fare rule (0/25) and added a check that crashes.

**4. What does it prove?** Four course skills, each with a run behind it: a **prompt contract**, a **two-round loop**
(write, score, feed back clean-copy errors only, revise), **verification** by a clean-copy control, and **evaluation**
by catch rate per defect type on two plantings. A reviewer could fairly conclude that I test an AI's output instead of
trusting it. Evidence: prompts, Claude's dated replies and recorded scorecards in `first-run/`.

**5. In, out, first.** In: one table, five defect types, one scorecard. Out, on purpose: orchestration (no Airflow),
dashboards, more than one dataset. First piece: one check on a clean and a broken copy (ran 2026-10-25: clean PASS,
negative fares 25/25 CAUGHT, drop-off before pick-up 0/25 MISSED). You know it ran because every run saves its output
under `first-run/results/<date>/`.

**6. What could sink it?** Checks that are too strict or too loose, and Claude's two rounds showed both. So the clean
copy and the broken copies are both required, every time, and a crashing check counts as an error, not a pass. Leakage
is the second risk: Claude never sees the data, the defects or the answer key, and every prompt is saved.

**7. Why this project?** In my Food Inspections Dataset Project (a group project on Chicago and Dallas
food-inspection data), my checks let bad rows through, and I didn't know which ones until later. DataSentry measures
exactly that. It is a mix, mostly new learning:

- **New to me:** pandera, dbt tests, Great Expectations, and prompting Claude to write and revise checks.
- **Done before:** working with messy public data. Evidence: that project's repository,
  github.com/EthanGomes14/DAMG7370_Final_Project_Group13.

---

**Exists today (2026-10-25)**

- This brief, the pitch film, its beat sheet and build files.
- `first-run/`: data script; the one-check first piece; the same rule in dbt and GX Core; the five-defect planter; the
  scorer; two rounds of checks written by Claude (Opus 5.5) with prompts and verbatim replies; recorded output of my
  runs, with package versions and data hashes.

**Will exist**

- The public DataSentry GitHub repository.
- A loop that runs on its own: Claude Code writing checks, running the clean-copy control, and revising, every round
  logged.
- A write-up of where Claude's checks were wrong and how that was caught.
