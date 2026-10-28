# DayThread — Project Brief (proposed final project)

**Aditya Raj · INFO 7375 Prompt Engineering and Agentic AI · Fall 2026 · Target role: AI Engineer**

DayThread is a **proposal**. No DayThread prototype exists. The answers below are the original pitch
(2026-10-14). **Revised 2026-10-25:** a minimal two-day replay was built and run on synthetic data
during the resubmission (`replay/`). Its results are marked *Revision* in §5 and §6 and in the lists
at the end.

**1. What is it, and what will I deliver?**
A proposed AI check-in assistant. It remembers conversations across days and turns concerning
changes into evidence a home care coordinator can review. Deliverable for the final project: a
runnable repository with a text-based prototype, persistent memory, a review page, tests, and an
evaluation report. Python and SQLite, with fictional people and synthetic records only.

**2. Why would anyone care, and how does it differ from real alternatives?**
I want to find out whether a coordinator can understand changes across several check-ins without
manually rebuilding the conversation history. That is an *intended* benefit, not a measured one.
I read the official documentation of two real alternatives; I did not test either product:
- **Lifeline:** automatic fall detection with a response center. It says its fall detection does
  not catch every fall.
- **DailyCall:** daily AI phone calls with summaries for families. It says it is not emergency
  monitoring.

DayThread's *proposed focus* has three parts: concerns linked to the original words, an
independent check of the raw transcript, and a coordinator's approve / refuse / defer decision. I
am not claiming the alternatives lack these features.

**3. Who opens it, and what do they do in the first minute?**
An engineering hiring reviewer opens the README, runs a clearly labelled replay, and inspects a
two-day memory example and one approval decision. The intended end user is a care coordinator. The
coordinator sees the concern, the conversation excerpts behind it, and options to approve, refuse,
or defer, on a simple local web page.

**4. What course skills will it demonstrate, and what evidence will support them?**
Prompt contracts, an agent loop with a budget and clear stops, permissions enforced in code,
source-linked memory, and evaluation. Tests and logs will show whether it retrieves earlier
information, rejects unauthorized changes, and stops at its limits. The evaluation compares the
workflow with and without memory, on development cases and on held-out cases reserved before
tuning, plus at least five deliberate failure cases. These tests could demonstrate a controlled
prototype, but would not establish readiness for real care.

**5. What's included, what's excluded, and what will I make run first?**
- **In:** simulated text check-ins, memory, evidence-linked concerns, human review.
- **Out:** clinical advice, real patient data, autonomous outreach.
- **Extensions:** voice calls, cloud deployment.
- **Permissions:** the assistant can read check-in history, add source-linked observations, and
  create internal review items. It cannot silently overwrite past records, change agency-owned
  information, or contact anyone. A separate executor acts only after checking that the approval
  still matches the evidence and the proposed action. Delivery is simulated locally.
- **First run:** one fictional client completes two simulated days. On day two the assistant
  retrieves something from day one without the client repeating it. I save the transcript and the
  source reference, and test that an unauthorized record change is rejected.
- *Revision (2026-10-25):* a minimal version ran: one fictional client, a summary, and two day-two
  openings per summary, 30 Claude CLI calls (`replay/README.md`). It did not include source-linked
  memory, the separate check or the record-change test.

**6. What specific failure could sink it, and how will I handle it?**
The client mentions "just a little tumble" and the summary omits it, so later steps that rely on
the summary miss it. I will predict this failure and trigger it on purpose. A separate check of the
raw transcript, kept apart from the summary, runs when each check-in ends and creates an internal
review item. A coordinator must approve any outbound action, based on the exact evidence and action
they reviewed. The checker could miss unfamiliar wording or raise false alarms, so I will test both.

*Revision (2026-10-25):* I recorded a prediction first (`replay/PRE-RUN.md`): a summary limited to
mood, meals and activities would drop the tumble in at least 3 of 5 trials. **It dropped it in 0 of
5**, so my prediction was wrong for this fixture. What did go wrong: 9 of 10 summaries turned "I
don't want my daughter fussing about it" into a disclosure prohibition, and some added unsupported
facts. Preserving an event does not guarantee preserving its meaning, so unsupported inference is
now the more concrete risk (`replay/RESULTS.md`).

**7. Why did I choose it, and which skills are new versus already demonstrated?**
Remembering yesterday is only part of the problem. Knowing when a person needs to see it, with the
evidence, is the part I find interesting. This is mainly a learning project.
- **Already practised (this project's log):** setting requirements for AI-assisted work, requiring
  sources before any comparison, and cutting overstated wording.
- **New:** persistent memory across conversations, permissions enforced in code, human approval
  tied to the evidence shown, and evaluation on cases kept separate from development.

---

**Exists today:** this brief; the pitch film and its script, beat sheet and build files; the
source notes (`SOURCES.md`); the decision log (`FRICTIONAL.md`). *Revision (2026-10-25):* the
minimal two-day replay (`replay/`: Python + SQLite runner, synthetic fixture, the prediction
recorded before the run, 30 saved outputs, Aditya's review, `RESULTS.md`). No DayThread prototype,
test suite or evaluation exists.

**Will exist (planned, for the final project):** the DayThread repository; the full two-day replay;
SQLite memory with source links; meaning-preservation tests across several synthetic conversations; the separate transcript check; the local review page with
approve / refuse / defer; the executor's match check with simulated delivery; tests (including the
rejected record change); development and held-out cases with at least five deliberate failures; an
evaluation report that states where it fails.
