# Script — DecisionTrace Lite (project film)

Gnanasudharsan Ashokumar · INFO 7375 · Fall 2026
Target length: about 6 minutes at about 130 words per minute. The timestamps
come from word counts (words ÷ 130 × 60). Re-time them after you record.

In the Kokoro film (`decisiontrace-lite-film.mp4`), measured from the audio, the sections run:
executive summary 0:00–0:45, introduction 0:45–1:53, methods 1:53–3:44, evaluation 3:44–5:01.

Each line has an ID (L01, L02, …), and `shot-list.md` uses the same IDs.
Notes in [brackets] are not spoken.

---

## 1. Executive summary — 0:00 to 0:57

[What and why, with no "how." This section has to work on its own if the viewer stops at 1:00.]

**L01** I'm Gnanasudharsan Ashokumar, and this is DecisionTrace Lite.

**L02** Teams make decisions in meetings, emails and tickets. Months later, someone asks: why did we decide this, who approved it, and is it still true?

**L03** The answer is scattered across documents, and some are out of date.

**L04** DecisionTrace Lite answers them: a short answer, the decision's current status, and a citation to the exact passage behind every claim.

**L05** If the documents don't say, it says so instead of guessing.

**L06** Why it matters: a wrong answer about a decision looks exactly like a right one, and acting on a reversed or unfinished decision means redoing work. An answer you can check in seconds is one a team can rely on.

**L07** And I'll publish how often it's right.

---

## 2. Introduction — 0:57 to 2:12

**L08** Here's what already exists.

**L09** General tools like NotebookLM and ChatGPT answer questions about documents you upload, and point to where an answer came from.

**L11** Research laid the groundwork. Retrieval-augmented generation, from Lewis and colleagues in 2020, grounds answers in retrieved text. The ALCE benchmark measures whether citations support their sentences. RAGAS scores how faithful an answer is to its sources.

**L13** So I tested two tools myself. On October ninth, I gave NotebookLM and ChatGPT six synthetic documents about a fictional company switching databases. The switch was approved, but not finished.

**L14** NotebookLM got the facts right and refused to invent a budget. But it described the migration as if it were done.

**L15** ChatGPT got the status right, but it dated that status to an unrelated team retrospective, and nothing flagged it.

**L16** Neither tool told me how often it's right.

**L17** That's the gap. Existing tools find facts. DecisionTrace Lite is built around a decision's status. It checks every citation, and it publishes its score.

---

## 3. Methods — 2:12 to 4:19

**L18** Here's the plan, step by step.

**L19** This is a scoped-down version of a larger system I've built, with Neo4j, LangGraph, FastAPI and hallucination detection. Here I keep only the core: question in, grounded answer out, in plain Python with Claude.

**L20** Step one: data. I'll grow my six synthetic Northwind Logistics documents into about fifty meeting notes, emails and tickets. Some decisions get reversed, some are unfinished, some documents contradict each other, and some questions have no answer. All of it is synthetic.

**L21** Step two: about fifty test questions I write by hand, each with the correct answer, status and supporting passages. I write them myself because Claude helps generate the documents, and a model grading its own homework isn't a test.

**L22** Step three: retrieval. A simple keyword ranker called BM25, written with Python's standard library, finds the most relevant passages.

**L23** Step four: Claude returns structured JSON: an answer, a status, and a list of claims, each with a document ID and an exact quote.

**L24** Step five: verification. Code checks that every quote appears word for word in its document, and a second Claude call judges whether the quote supports the claim. An answer that fails gets one retry. If it still fails, the tool says: not supported by the sources.

**L25** Step six: the evaluation harness and a written report.

**L26** Resources. Claude runs through my Northeastern Claude Code seat, in non-interactive mode. Using it from a script is pending confirmation from my professor and Northeastern IT. If it isn't allowed, I'll request API credits instead. Saved responses let me re-score without new calls. Compute is my M4 MacBook Pro, with no GPU, plus GitHub for the code.

---

## 4. Evaluation — 4:19 to 5:53

**L27** How will I know it worked? Along with basic correctness, I'll measure five things on my test set.

**L28** One: citation validity. Every quote must exist in the cited document. Target: one hundred percent. Anything less is a bug.

**L29** Two: citation support. Does each quote actually support its claim? Target: at least ninety percent.

**L30** Three: status accuracy. Decided, in progress, or superseded? Target: at least eighty-five percent.

**L31** Four: refusals. It should refuse at least nine in ten unanswerable questions, and no more than one in ten answerable ones.

**L32** Five: does the verifier help? I'll compare the full tool against the same tool with verification off.

**L33** It worked if it meets those targets, and the verifier improves support and status accuracy without costing more than five points of correctness. It didn't work if verification only adds refusals, or if the second Claude call disagrees with my own judgments too often to trust. Either way, I'll publish the numbers and the failures.

**L34** The first check: asked which database the tracking service uses, it has to say the switch is still in progress as of June ninth, citing the migration ticket. Those are the two things the other tools missed.

**L35** That's DecisionTrace Lite. Thanks for watching.

---

[Cut on 2026-11-22: L10 (product names not yet verified) and L12 (study figures not yet verified). Both stay in appendix.md §6, marked VERIFY. The other line IDs are unchanged so shot-list.md still matches.]
