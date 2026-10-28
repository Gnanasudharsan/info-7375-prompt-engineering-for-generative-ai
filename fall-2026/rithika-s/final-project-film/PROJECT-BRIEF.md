# PROJECT-BRIEF — Agentic Retrieval Lab
Rithika Sankar Rajeswari · INFO 7375 · Final Project Pitch · October 2026
Target role: ML Engineer / AI Engineer (retrieval and RAG)

## 1. What is it?
An open, small-scale testbed that measures how well search holds up when an AI agent, not a human, writes the query.
When done, it will be a public GitHub repository: a Python pipeline, tests, dated result files, a README that reports each result next to the file that produced it, and a short failure-analysis write-up.
Note on "agentic": here it means agent-written queries. The project does not build an autonomous agent loop.

## 2. Why would anyone care?
Alternatives I examined:
- Perplexity's Q2D-Web paper (Schall et al., 2026) studies agent-written queries at 190M-document scale. Its corpus, queries, and labels are private; only a leaderboard for open-weight models is public, so an outside engineer cannot inspect the data or rerun the experiments. The paper proposes, as future work, testing whether BM25 adds value to a hybrid ensemble compared with a neural-only ensemble of the same size; my Experiment 2 will run that test at small scale on public data.
- MS MARCO passage dev/small, which I loaded and measured, has human-written queries only and sparse labels (about 1.07 correct passages per query across the full dev/small set (6,980 queries)).
What mine does: it will let an engineer choosing a retriever for an agentic RAG system rerun a human-vs-agent query comparison on public data, on one laptop, with every number traceable to a results file.

## 3. Who opens it, and what do they do in the first 60 seconds?
Reader: a hiring manager or engineer screening candidates for ML/AI engineering roles.
First minute: they will read the README's headline table (human vs agent queries, BM25 vs dense models), click one number through to the results file that produced it, and see the single command that reruns the tests.
Today the headline table says "TBD"; it will be filled from Milestone 2 onward.

## 4. What does it prove about me?
- Evaluation design: a fixed query set (seed 42), a defined metric (Recall@100), and a corpus built so comparisons are fair.
- Source grounding: every reported number points to a dated file in results/.
- Verification: 103 passing tests, and a BM25 index checked against a reference implementation.
- Honest limits: known biases (pooling, passage length) stated, not hidden. For example, agent support queries are currently scored against the original question's single MS MARCO label, which likely understates their recall; Experiment 1 will add deeper LLM-judged labels.
A reviewer could fairly conclude I can build and check a retrieval evaluation. They could not conclude I have shipped a production RAG system.

## 5. In / out / first
In: Milestone 2 (four dense embedding models vs BM25), Experiment 1 (human vs agent-written queries), and Experiment 2 (does BM25 still add value in hybrid search?), plus a short hand-written failure analysis of queries every retriever misses.
Out: no chatbot, user interface, or answer generation; it evaluates first-stage retrieval only. The automated failure analyzer with a fix simulator (Experiment 3) is postponed to a stretch goal.
First piece to run: one dense model against BM25 on the 200k corpus with the 300 human queries.
How you'd know it ran: a new dated folder in results/ with its config and Recall@100, a passing test, and a BM25 number that matches the existing run.

## 6. What could sink it?
Risk: in my corpus, the BM25-chosen distractor passages are longer on average (64.6 words) than the correct passages (54.2). A model that simply prefers shorter passages could look better than it is, which could make dense models falsely appear to beat BM25.
What I will do first: run a trivial "rank shorter passages higher" baseline. If it clearly beats random, I will build a length-matched control corpus and check whether the model ranking changes before drawing any conclusion.

## 7. Why this project?
A mix, mostly learning built on skills I already have.
Already have: Python data pipelines and data engineering, from my work as a Data & AI Engineer at Medlaunch Concepts (Jan–May 2026) and as an AI/ML Data Science Intern at Intuitive (Jun–Aug 2026); deep-learning foundations, as a Graduate TA for IE 7615 Deep Learning for AI. That work is proprietary, so the evidence is the roles, not code.
New to me: information-retrieval evaluation (Recall@k, nDCG), dense embedding retrievers, hybrid fusion, and LLM-as-judge labeling.
Why it matters: I'm aiming for AI/ML engineering and data science roles and am especially interested in RAG systems (retrieval, generation, and evaluation); this project lets me build and measure the retrieval part.

## Exists today (verified 10 Oct 2026)
- Repo github.com/rithika-sr/agentic-retrieval-lab, 4 commits (5–9 Oct 2026) — private for now; will be made public
- 103 passing tests; ruff lint clean
- 300 MS MARCO dev/small queries rewritten into 1,200 agent queries (Claude Haiku 4.5), 0 failures
- BM25 over the full 8.8M collection: correct passage in the top 100 for 63.7% of human, 60.3% of agent-primary, and 41.7% of agent-support queries
- 200,000-passage test corpus (317 positives, 104,877 BM25-pooled distractors, 94,806 random)
- A preliminary answer-leakage check (known false positives)

## Will exist
- Milestone 2: four dense models vs BM25
- Experiments 1 and 2, and the hand-written failure analysis
- The length-bias baseline and, if needed, the control corpus
- Filled-in README headline results
