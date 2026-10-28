# PROJECT-BRIEF — Final Project Pitch

**Student:** Yudan (Anica) Zhou · `@yudanzhou` · INFO 7375, Fall 2026
**Working title:** *is-funded-sponsor-triage* — evidence triage for an international job search
**Target role:** Data Analyst
**Written:** 2026-10-13

> **Honesty rule applied throughout.** Past tense is used only for things that exist
> and that I can show. Everything else says "will". Where a number appears, it came
> from a run I did on 2026-10-02, recorded in the repository.

---

## 1. What is it?

**One sentence.** A job-search triage tool for an international student that sorts
postings into apply / consider / skip using published funding and visa-sponsorship
records, and that reports "no record either way" as its own answer instead of
collapsing it into "no".

**What exists when it is done:** a repository — a written recipe a person can audit,
a Python prototype, a test suite, a worked run, and an evaluation log.

## 2. Why would anyone care — what makes it special?

**The problem, from the data (record, 2026-10-02 run):** of 27,874 companies with a
funding date in the shipped dataset, only **1,532** have any H-1B approval on record,
and only **131** of those raised money in the previous 24 months. Funded and sponsoring
barely overlap, and nothing a student browses shows them together.

**Real alternative I looked at (2026-10-13, screenshots in `evidence/`).** h1bdata.info
indexes Department of Labor LCA filings. Searching "Moloco" returned a long table of
filings — job titles, salaries, locations, dates. Searching "123 See", a funded company
with no record in my data, returned the page header and the site's boilerplate: no
table, no count, and no message saying nothing was found.

**The specific difference.** It is a lookup tool: one employer at a time, and an
employer with no filings returns an empty result. A student reads an empty result as
"they don't sponsor". In the shipped data **28,812 rows have a blank approval figure
and only 5 record an explicit zero** — so a blank is almost never a no. This tool
labels the blank, **holds that company out of scoring entirely**, and routes it to the
networking hours with a question to ask, instead of ranking it against companies that
do have records.

Put plainly: *it does not save lookup time; it prevents a student from throwing away
most of the market because a search box came back empty.*

## 3. Who opens it, and what do they do in the first sixty seconds?

**The reader being pitched to** is a hiring manager or engineer reviewing a portfolio
for a data role. In sixty seconds they clone the repository, run one documented
command, and see a shortlist in which every number is tagged with where it came from —
`record` for a looked-up value, `your-input` for one I chose — plus a test run that
checks those labels rather than the arithmetic.

**The end user the tool is built for** is a different person: an F-1 student in a
STEM-designated master's programme, about eight months from graduation, planning
post-completion OPT with its 90-day unemployment limit, who prefers venture-funded
employers and has not yet chosen among Business Analyst, Data Analyst, Product Analyst
and IT Consultant.

## 4. What does it prove about me?

| Course skill | Evidence that already exists |
|---|---|
| **Source grounding** | Every evidence term carries a source label; a missing measurement is omitted, never defaulted to zero |
| **Verification** | A test suite that asserts provenance instead of re-implementing the scorer it tests |
| **Reading a system critically** | I found two real defects in the course repository: a line-ending bug that makes a repository check report 0 of 33 recipes on my Windows checkout while the files plainly contain what it says is missing, and a documented fix (PR #37) that the code does not contain |

**What a reviewer could fairly conclude:** that I can take someone else's system, find
where its documentation and its behaviour disagree, and build on it without
overstating what I verified.

**External evidence, 2026-10-12.** A teaching assistant reviewing the submitted recipe
wrote: *"Strongest: you never turn a blank into a no, and you caught your own design's
biggest weakness."* The same review deducted points for two things, both named in §5.

## 5. What is in, what is out, what comes first?

**In scope:** triage over public funding and sponsorship records for four analyst role
families, on a fictional persona.

**Deliberately out:** it will never report that a company *does not* sponsor — except
for the five companies whose record shows an explicit zero. The data can establish
that an employer has sponsored; for everyone else it is silent, and a tool that turned
that silence into a negative would be inventing it.

**What comes first — and how someone would know it ran.** Two fixes, both from the
2026-10-12 review:

1. The recipe claimed lifecycle stage `RUNNABLE-SAMPLE` while declaring four open
   `[TODO]` items. The project's own constitution requires zero open items one stage
   earlier, so the honest stage was `DRAFT`. **It will be set to `DRAFT` and raised
   only when the items are closed.**
2. The role-fit ratings (0.8 / 0.7 / 0.6 / 0.6) and the 60-day hiring-lag assumption
   were placeholders. **Each will be replaced by a value with a written basis, or
   removed from the decision.**

Someone would know this ran by the test suite passing and by every assumed value in
the report tracing to a documented basis rather than the word "placeholder".

## 6. What could sink it?

**The risk, demonstrated in my own run:** the numbers I assume can outrank the records
I look up.

In the 2026-10-02 run, TREDENCE INC had a strong sponsorship record — 564 approvals
against 16 denials, scoring the maximum sponsorship vote of 0.9 — and the tool still
returned **Skip, composite 0.000**, because a demo liveness value entered by hand in the input file was
zero. That behaviour is correct by design: a closed gate should zero a row.
But it shows how completely a value I chose can override every record in the
calculation.

**What I will do about it:** add a sensitivity pass that varies each stated assumption
and counts how many decisions change. If a recommendation flips on a number with no
written basis, the report will say so instead of printing a ranking that looks
measured.

**A second instance of the same risk, from writing this brief.** The first draft of
this document contained four statements that did not match my own records: it said the
tool scores blank-record companies when it holds them out of scoring, it credited a
result to a Linux run I never did, it misdated the submission, and it called a
564-approval record the strongest in a set that contains an 8,810-approval one. Each
was checkable against a file I already had. A fluent draft that nobody checks against
the records is the failure this project is about, and it happened to the pitch before
it happened to the tool.

## 7. Why this project?

**A mix, and the halves are not equal.**

**Already have — showing it off:**
- the domain understanding; I am the person this is built for
- the judgment calls in the recipe: the direction, my own predictions, and catching
  the OPT-versus-H-1B mix-up. The code and tests were written with an AI assistant
  under my direction, which the previous assignment's `SOURCES.md` records

**New to me — genuinely learning:**
- writing and testing the code myself rather than directing it
- evaluation. I have never built a test set with known answers and measured against it
- sensitivity analysis. §6 is the first time I will have to quantify how much of an
  output rests on my own assumptions

Honest version: **this is mostly finishing something I built, plus one skill I do not
have yet.** I picked it because the reviewer's two deductions told me exactly what
unfinished looks like, which is a better starting point than a new idea with no
feedback attached.

---

## Exists today

- A recipe, a Python prototype, a configuration file holding every stated judgment, and a test suite — built, run and submitted 2026-10-02, reviewed 2026-10-12
- A worked run dated 2026-10-02 over nine postings, producing 4 Apply, 2 networking-list, 3 held or skipped
- The dataset findings: 1,532 of 27,874 funded companies with any H-1B approval; 131 of those funded within 24 months; 28,812 blank approval rows against 5 explicit zeros
- The role-family counts: Data Analyst 38, Business Analyst 31, IT Consultant 21, Product Analyst 4
- Two defects found in the course repository and documented
- A reviewer's assessment dated 2026-10-12

## Will exist

- Lifecycle status corrected to `DRAFT`, raised only against closed items
- Fit ratings and the hiring-lag assumption replaced by values with a written basis
- A sensitivity pass reporting how many decisions flip when a stated assumption moves
- A test set with known answers, and a measured result against it
- An honest failure analysis of where the triage was wrong and why
- A README a stranger can follow from clone to shortlist without asking me anything
