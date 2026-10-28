# Project brief — Ground Truth SQL

Riya Kapadnis · INFO 7375 · Final project pitch · written 2026-10-09, revised 2026-10-14 and 2026-10-21
Target role: **AI Engineer** (also readable for Data Analyst roles)
Stack: Python 3 (standard library + `sqlite3`), Claude via Claude Code, the public Chinook sample database.

## 1. What is it?
An evaluation harness that tells you, on your own database, which plain-English questions a
text-to-SQL model answers wrongly and why. Done, it will be a **public GitHub repository**:
a gold set of about 50 questions with hand-checked SQL over Chinook, a runner that sends each
question to Claude and checks the result by executing it, and a Markdown scorecard listing
every failure, its cause, and the model's SQL beside the checked answer.

## 2. Why would anyone care?
It is for an analyst deciding whether to trust an AI SQL assistant on their own schema. The
danger is a query that runs, looks right, and returns the wrong number. In my first test
(2026-10-09), an example query with a common join mistake (drafted with Claude, checked by me)
reported USA revenue as 4,667.06 instead of 523.06, about nine times too high, with no error.

Alternatives I looked at:
- **BIRD** (bird-bench.github.io, checked by me 2026-10-21): 12,751 question–SQL pairs over 95
  databases, scored by execution accuracy. It measures a model on *its* databases, not your
  schema or questions.
- **Vanna 2.0.2** (github.com/vanna-ai/vanna, MIT; I ran it on Chinook 2026-10-21): writes SQL
  for your database and has an evaluation module, but its checks look at tool calls, expected
  *words* in the answer, time, or an LLM judge. None compares rows. Its `OutputEvaluator` gave
  **PASS** to the 4,667.06 answer because "USA", "Canada" and "France" were present
  (`evidence/vanna_check.py`). I did not run its LLM step, which needs a paid key.

What mine adds: checked answers on *your* schema plus a written failure analysis. The output
is not one accuracy number but the specific questions the model got wrong, sorted by cause
(join fan-out, wrong key, unit error, date handling, and so on).

## 3. Who opens it, and what do they do with it?
A hiring manager or engineer screening for an AI Engineer role, and later the analyst above.
In the first sixty seconds they read the scorecard at the top of the README, run one command
that replays the saved model results offline (no key needed), and open one failure to see
the model's SQL next to the checked SQL and both result sets.

## 4. What does it prove about me?
That I can evaluate a model instead of trusting it, using the course's skills:
- **Prompt contract:** exactly one read-only `SELECT`; anything else is logged as a violation, not fixed.
- **Verification:** both queries run on a read-only database and the rows are compared, not the SQL text.
- **Evaluation:** a gold set, a failure taxonomy, and repeated runs to show variance.
- **Agent loop** (stretch): generate → run → read error → repair, capped, and *measured* for
  whether repair fixes answers or only hides errors.
- **Source grounding:** every reported number traces back to its rows.

A reviewer could fairly conclude I can build and honestly report an evaluation on a small
public database, and **not** anything about production warehouses: Chinook is 11 tables and
50 questions is small. Evidence: dated run logs and a scorecard anyone can re-run.

## 5. What is in, what is out, what comes first?
- **In:** Chinook, about 50 questions, Claude as the model, an execution checker, a failure analysis.
- **Out (deliberately):** no chat app or UI, no write queries (the connection is read-only),
  no claims about production data or other models.
- **First (already runs):** `evidence/run_slice.py`: 8 questions, gold SQL, and an execution
  comparator tested on 9 variants (drafted with Claude, labels checked by me). It ran if it
  prints `execution comparator agreed with the hand label on 9/9 variants` and exits 0.
- **First Claude run (2026-10-21):** three blind runs of Claude Opus 5.5 (schema and questions
  only). `evidence/score_claude_runs.py` replays them offline: 22/24 pass by rows, 0/24 by SQL
  text. Both fails are Q02, where France and Brazil tie and my question sets no tie order.
- **Next:** fix Q02, then grow toward 50 harder questions.

## 6. What could sink it?
I write both the questions and the answers, so the test can be too easy or the answers wrong.
Both have happened. Q08's first gold asked about 2023, but the data ends in 2013, so an empty
gold "matched" a broken query (`evidence/run_slice_output_v0_first_run.txt`); Q02's tie failed
two correct Claude answers; and Claude got every answer right, so the set is too easy. What I
do: the runner rejects empty gold answers; `evidence/cross_check.py` recomputes every gold answer
in plain Python from the raw tables (8/8 agree; it flags Q02's tie and Q04, whose answer is every
customer); ambiguous questions get fixed or marked; each question runs three times; harder
questions come next; and a second person checks a sample once the full set exists.

## 7. Why this project?
It's a mix. The SQL and Python side is something I already do and can show; checking, with
evidence, whether a model's answer is actually right is the part I want to learn, and it is
what AI Engineer roles screen for.
- **Already have:** SQL, Python, and building LLM features into a BI product (AI Engineer
  co-op, TwinAI, Jan–Jun 2026). That code is private, so the public evidence is this course:
  the Week 1 film (a claim checked across 10,000 seeds, not one run) and my Reallocation
  Engine recipe (PR #7 on nikbearbrown/the-reallocation-engine).
- **New to me:** designing an evaluation set, execution-based checking, a failure taxonomy,
  and measuring whether a repair loop actually helps.

## Exists today (2026-10-21)
- `evidence/gold_set.json`: 8 questions, gold SQL, 9 variants drafted with Claude and checked by me
- `evidence/run_slice.py` + outputs (current 9/9, and the v0 run showing the Q08 bug)
- `evidence/claude_runs/2026-10-21/` (prompt, three raw replies, score) and `score_claude_runs.py`
- `evidence/vanna_check.py` + my own run's output; `evidence/cross_check.py` + output
- `evidence/data/Chinook_Sqlite.sqlite`: Chinook v1.4.5 (MIT, Luis Rocha)

## Will exist
- A gold set of about 50 questions, including ones marked ambiguous
- A Claude runner that calls the model directly (today's runs were done in Claude Code)
- A scorecard in the README, built from the replay
- A failure taxonomy with counts, and three-run variance per question
- (Stretch) A measured repair loop
- A second person's check of a sample of the gold answers
