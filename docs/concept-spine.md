# The concept spine: what runs through every chapter

**What this is.** The brief for rewriting the fifteen chapters so they teach *ideas* and not only *procedures*. It names the three ideas, the questions they add, the three recurring devices that carry them, and the rules the rewrite must keep.

**Why.** The first draft reads as a long how-to: do this, then this, then this. The skills are right, but the reason for them never runs through the book. A student can finish it able to follow steps and unable to say what the steps are *for*.

**The finding.** All three companion books say the same thing from different sides, and it is one sentence: *Claude is superhuman at the fast, parallel, specification-bound work, so you do not compete with it there. It has no stake, no world context and no judgment, so you decide where it goes, you check what comes back, and your name goes on it.*

Status: planning document for a rewrite in progress, 2026-10-11. Nothing here is signed or verified. Gate 3 (human rewrite and sign-off) remains the author's.

---

## 1. The thesis in one paragraph

Prompt engineering is not a bag of phrases that makes a model behave. It is the discipline of *conducting* a machine that is better than you at producing fluent text, code and candidate answers at speed, and that cannot tell you whether any of it is the right thing, is true, or matters. You do not outrun a car; you drive it, and the car does not choose the destination. So the work that stays yours is the work before the machine runs (decide the problem, the constraints, the gate) and the work after (check it, and sign it). This book teaches the Python and Claude mechanics because you cannot conduct or audit what you do not understand.

## 2. The three ideas

Each idea comes from one companion book, carries one question, and has one rule for the rewrite.

### Conduct — decide before Claude implements  *(Conducting AI)*

AI is very good at writing code and doing technical work *from a complete specification*. It is poor at deciding what the specification should be. The human job is "not to type less. It is to decide more precisely." That means a design, constraints, and **phase gates**: a gate is "the specific, testable condition that must hold before the agent's output moves downstream." The seam between steps is where risk lives ("the unit of risk is the handoff"), so every handoff gets an explicit, checkable condition.

- The question it adds: **What did I decide before Claude started, and what must be true before this goes downstream?**
- Rule for the rewrite: in every chapter's artifact, show the *human-authored* design (contract, constraint set, test, stop condition) being written **first**, and Claude implementing against it second.
- Source: *Conducting AI*, ch.97 "Phase Gates" and "The Boondoggle Score"; appendix "The Pragmatic Conductor" (the conversion rule, design by contract, "you write the contract; the agent writes the implementation"); ch.06–07 problem formulation; ch.08–09 tool orchestration and the handoff.

### Check — Claude can be wrong, and you sign  *(Computational Skepticism)*

AI makes mistakes, and the mistakes arrive fluent. Fluency and correctness come from the same process, so the better an output looks, the less it invites checking ("the well-formed prose did the epistemic work the verification should have done"). You are the human, and it is your name on the product. So you look, iterate, check, and check again, and you do the checking *with* Claude. Two disciplines keep that honest:

1. **Write the failure down before you look.** The book calls it the prediction-lock: record what a wrong answer would look like, dated, before reading the output, and never revise it afterwards; the learning is the gap. "Look and iterate" never means re-prompting until it looks right.
2. **Keep the check independent of the generator.** Claude can propose the test, run the command, parse and format against criteria *you* wrote, and hunt for the counterexample. It cannot be the independent check on its own work ("an AI checking an AI is not a second opinion; it is the first opinion run twice"), and it cannot sign. Use a check that fails differently from the thing checked: a deterministic test, a recomputation, a source, a person.

A check is only as good as the question it answers, so name that question.

- The question it adds: **What would tell me this is wrong, who checked it and how, and what did nobody check?**
- Rule for the rewrite: every chapter ends its artifact with a **sign-off** (see §4) and uses *evidence-matched verbs*: "recorded", "computed", "tested" are not "established".
- Source: *Computational Skepticism for AI*, ch.1 (the fluency trap, the prediction-lock, the casebook), ch.8 (a finish action establishes nothing beyond termination), ch.9 (the handoff condition), ch.11 (the verb taxonomy), ch.12 ("the attestation you sign": what was tested, what was *not* tested, who cleared which gate, the verbs calibrated; and the signer's authority to withhold); *Conducting AI* ch.02 (solving and verifying are different operations) and ch.05 (audit before you verify).

### Drive — know what is Claude's to do and what is yours  *(Irreducibly Human)*

Claude is superhuman at Tier-1 work: pattern, association, retrieval, drafting, generating variants, in parallel and fast. Competing with it there is a waste, so hand it over "gladly and without nostalgia". It is a different kind of thing from a person: it has no standpoint from which a result *matters*, no world context beyond text, no stake in being right, and nothing it answers for. The best systems use both. So divide the work **by task**, not by a blanket claim that people are smarter or the machine is hopeless: *deprioritize* (hand it over), *supervise* (use it, audit it), *protect* (keep it yours). The car is the picture: it moves faster than you ever will and you still choose the destination. One honest strain on that picture: a car's failures are visible and Claude's are not (its dashboard reads most confident when it is wrong), and you must understand the engine well enough to hear that it is off. This is why you build the small mechanism yourself first: "you cannot audit what you do not know."

- The question it adds: **Which part of this is Claude's to do, which is mine, and what would show the split was honest?**
- Rule for the rewrite: every chapter states a task-specific **AI should / Human should** split (§4) and says *why* the human part cannot be handed over in that chapter's situation.
- Source: *Irreducibly Human* Tier 1 ("Pattern & Association"), the baseline-knowledge condition, the volume trap (Tier 4), the machine boundaries (Tiers 3, 5, 7), the conclusion's deprioritize / supervise / protect audit.

## 3. Why we still build first (the apparent contradiction)

If Claude writes code better than a first-year student, why does every chapter ask the student to write the mechanism by hand? Because the student's job is not to out-type Claude. It is to be the person who can tell when Claude's code is wrong. You cannot audit a softmax you have never computed, or a permission check you have never broken. Building the small version is not tradition; it is how you acquire the *baseline* that makes conducting possible. Say this plainly in Chapter 1 and refer back to it. Then, after the baseline, the student conducts Claude Code against their own gate and checks the result.

## 4. The three recurring devices

Use these names in every chapter, once each, placed where they do real work. They are a shape, not boilerplate: the *content* is specific to the chapter's artifact every time.

**The gate** *(Conduct).* A short passage (or a boxed block) where the learner writes down, **before** asking Claude to implement, the contract: what the thing must do, what it must refuse, the constraints, the test that would fail a plausible-but-wrong version, and the condition that must hold before the output moves on. Name who decided each item. It is acceptable and often better for the gate to be a few lines of plain English or a `test_` function, not a form.

**The sign-off** *(Check).* The last thing the artifact says. A short statement the learner could put their name to, of this shape: *what I checked; how (by hand, by a test I wrote, with Claude, with a tool that fails differently); what I did not check; what I am therefore not claiming; and, if the evidence does not support signing, that I withheld it.* It must be true. Claude can write the words of a sign-off fluently and they will be empty: the part that matters, what was *not* tested, is the part an AI-generated sign-off never writes. A sign-off that claims more than the record supports is the failure the chapter is about. Never sign for the learner; write the template and the standard, not the signature. (Source: *Computational Skepticism* ch.12, the four-part attestation.)

**The driver's seat** *(Drive).* The chapter's **AI should / Human should** split for *this* task, with one sentence on why the human part stays human *here* (judgment, world context, accountability, or the baseline needed to audit), and one request for evidence that the split actually happened in the learner's artifact (the transcript, the diff, the edit they made). Task-specific, never "AI is fast, humans are wise".

A chapter may also use the book's other vocabulary where it fits and is already defined in the companion book: plausibility audit, problem formulation, tool orchestration, interpretive judgment, executive integration (the five capacities); the fluency trap; Levels I–III of AI usage; the handoff; the re-engagement trigger; the three tiers of verdict (deprioritize, supervise, protect). Do not invent new frameworks.

## 5. Writing the chapters

**Structure.** Open on a *concept question* the chapter will answer, usually a situation where following the recipe still goes wrong. Then each technical section earns its place by answering one of the three questions; lead with the *decision the human faces*, not the steps. A section that is pure procedure with no decision, no check, and no division of labor is folded into a sentence or cut. Keep the spine: predict, explain, Build It, Use It, Ship It, verify, reflect.

**Voice.** Teardown (`ai1-cli/voices/teardown/VOICE.md`): explain the machinery, then judge the design choice and name the trade-off; honest about limits; no "obviously", "clearly", "one could argue", "it seems". Nik Bear Brown speaks in the first person ("I") where the chapter states his teaching and choices. Short sentences for the claim, longer ones for how things connect. Concrete before abstract.

**Keep exactly** (the checker and the course depend on them): the title line `# Chapter N — …` and the italic subtitle; the `## What you will be able to do` heading; every `<!-- [FIGURE: …] -->` comment, image and caption; the paired-lesson link `../lessons/<week>/docs/en.md` and the `quiz.json` link; every Python block parseable and **unchanged** from the lesson code it reproduces; every worked-example number (they come from `research/worked-examples.json`); the Assessments section with Warm-up, Application, Synthesis, Challenge (ungraded; you may reword items to ask conduct / check / split questions but keep the count and tiers); the `## Anthropics` section and its links and link-check date untouched; the 5,000–9,000 word range.

**Closing book notes.** Where a chapter already ends with `## Computational Skepticism`, `## Conducting AI` or `## Irreducibly Human` (in the order Anthropics → Computational Skepticism → Conducting AI → Irreducibly Human), keep the heading, keep the pointer into `../docs/*.md`, and keep a specific diagnostic, but do not let that note carry the idea alone any more: the body now does. No duplicated ledgers. Where `## Irreducibly Human` is kept, it must contain **AI should** and **Human should** in bold (the checker requires it). New citations to companion-book sections go to the table in §7 or to the existing `../docs/*.md` anchors; never invent a filename or section.

## 6. Guardrails (house rules that survive the rewrite)

- **No fabrication.** Never invent a Claude conversation, a transcript, a test result, a citation, a human approval, or a student's understanding. Label constructed examples ("Suppose…"). Outputs quoted in a chapter come from the recorded research runs.
- **Claim at the strength of the evidence.** Philosophical positions in the companion books (permanent limits, "AI is absent here", Tier 3/6/7 impossibility, the Gap Account's structural blind spot) are *arguments*, presented as such, never as established empirical facts. Do not say "AI cannot X" as a theorem; say what Claude has no access to *in this task* and what to check.
- **Assign by task.** Never a blanket "humans are more accurate / machines are incapable". People over-trust, miss errors outside their field, and add noise when they override on a hunch; machines contribute real value above Tier 1 under supervision.
- **Do not print unverified numbers from the companion books.** Excluded unless re-sourced: "MIT 34% more confident when wrong"; Kosmyna "up to 55%" and Bastani "48% / 17 points"; PwC 56%; "88% of workers"; $67.4B; Deloitte 38%; FACET figures; companion-app user counts; the 73%-Turing result without its persona caveat. The author's own instruments (the three levels of AI usage, the five-layer stack, the verb ordering, Memo A/B) are teaching devices, not industry standards: say so when you use them.
- **Strong from a complete specification, not strong in general.** *Conducting AI* does not say Claude is good at technical work across the board: it says generation is reliable where the spec is complete, and otherwise "suspect the generated code first" (tests that share the code's misunderstanding; packages the model invented; plausible architecture smuggled in as an answer). Teach "Claude implements well against a gate you wrote", not "Claude can be trusted with code".
- **Do not state the author's own hypotheses as findings.** The Boondoggle Score is "my own instrument… no external validation"; the seven tiers are an unpublished classification; "overtrust is the dominant failure" is a working hypothesis; the Gödel link is an analogy; the calibration-baseline ranges and ECE thresholds have no data source behind them. Use the Ash incident only as the Agents-of-Chaos account in *Computational Skepticism* ch.8 gives it (Ash is the agent; the study is exploratory: one lab, two models, two weeks) or leave it out; the manuscript describes Ash inconsistently elsewhere.
- **Phase gate is the book's term** for the explicit boundary where AI stops and human work begins; elsewhere the same idea is "verification gate", "handoff", "trust decision". Use the term where the idea is a gate, not as decoration.
- **Not waterfall.** Design-first does not mean freeze-the-design. A later finding can reopen an earlier decision (the re-engagement trigger); say so where it happens.
- **Claude only, Python only, offline first.** All existing course constraints in `AGENTS.md` still apply, including: direct API examples explicit and optional, Claude Code access assumed, assessments ungraded, assignments 100 points (60/10/10/20), the policy-video link, no invented dates or film mappings.
- **Do not sign, verify, commit or push.** Sidecars (`*.verified.json`) stay `verified:false`. The rewrite is an AI draft for the author's Gate 3 review.

## 7. Where the ideas live in the companion books

Filenames are under each book's `chapters/` directory (`../info-7375-conducting-ai/`, `../info-7375-computational-skepticism-for-ai/`, `../info-7375-irreducibly-human/`). The books are not bundled with this repository; keep every note self-contained for a reader without them.

| Idea | Book and section | Use it for |
|---|---|---|
| The conductor; the Gardnerian gap | *Conducting AI* `01-the-conductorless-orchestra.md` | Chapter 1 and 3 framing |
| Solving and verifying are different operations | *Conducting AI* `02-the-solve-verify-asymmetry.md` | "Passing is not true" in Ch.2, 4, 11 |
| Three levels of AI usage; the mismatch | *Conducting AI* `03-three-levels-of-ai-usage.md` | Chapter 3 (levels of scrutiny, not the chat/assistant/agent classifier) |
| Audit before you verify | *Conducting AI* `04`, `05-plausibility-auditing-*.md` | Chapter 6 |
| Problem formulation; the distinctness test | *Conducting AI* `06`, `07-problem-formulation-*.md` | Chapter 10 |
| Lowest capability that suffices; the handoff; laundering | *Conducting AI* `08`, `09-tool-orchestration-*.md` | Chapters 5, 8, 11 |
| Three legitimacies; Memo A to Memo B; the signature | *Conducting AI* `10`, `11-interpretive-judgment-*.md` | Chapters 13–15 |
| Integration is not sequencing; the re-engagement trigger | *Conducting AI* `12`, `13-executive-integration-*.md` | Chapters 12, 15 |
| Phase gates; the Boondoggle Score; handoff condition | *Conducting AI* `97-fundamental-themes.md`; `98-appendix-pragmatic-conductor.md` | The gate device, everywhere |
| Tier 1 and the baseline-knowledge condition | *Irreducibly Human* `01-tier-1-pattern-and-association.md` | Chapter 1, and why we build first |
| Plausibility auditing; the volume trap | *Irreducibly Human* `04-tier-4-metacognitive-and-supervisory.md` | Chapters 6, 13 |
| Prediction is not identification | *Irreducibly Human* `05-tier-5-causal-and-counterfactual.md` | Chapter 9 |
| Independence before deliberation | *Irreducibly Human* `06-tier-6-collective-and-distributed.md` | Chapter 12 |
| Relationships and consent | *Irreducibly Human* `03-tier-3-social-and-personal.md` | Chapter 14 |
| Reckoning is not judgment; deprioritize / supervise / protect | *Irreducibly Human* `07-tier-7-…md`, `08-conclusion.md` | Chapter 15 |
| The fluency trap; the prediction-lock; the casebook; solve-verify asymmetry | *Computational Skepticism* `01-the-skeptics-toolkit.md` | Chapters 1, 15; the sign-off |
| Calibration; confidence is not correctness | *Computational Skepticism* `02-probability-uncertainty-and-the-confidence-illusion.md` | Chapter 1 |
| Prompt sensitivity | *Computational Skepticism* `04-robustness-…md` | Chapter 2 |
| Data validation; the epistemic frame | *Computational Skepticism* `03-data-validation-…md` | Chapter 7 |
| Explanation vs the appearance of explanation | *Computational Skepticism* `05-model-explainability-…md` | Chapter 11 |
| Agents: finish is not success; cascades; authority laundering | *Computational Skepticism* `08-validating-agentic-ai-…md` | Chapters 4, 12 |
| The handoff condition; the delegation map | *Computational Skepticism* `09-delegation-trust-and-the-supervisory-role.md` | Chapters 8, 10 |
| The verb taxonomy | *Computational Skepticism* `11-communicating-uncertainty-…md` | The sign-off, everywhere |
| The attestation you sign | *Computational Skepticism* `12-accountability-…md` | Chapters 13–15 |

## 8. Chapter map: the concept each chapter now carries

| Ch | Chapter title | Conduct: the gate | Check: the sign-off | Drive: the driver's seat |
|---|---|---|---|---|
| 1 | Next-token prediction and sampling | You set the experiment: scores, temperature, count, seed. Claude does not choose what is being measured | Probability is not frequency is not correctness; repeatable is not true | Claude is Tier-1 superhuman at the continuation; you build the small version so you can audit it |
| 2 | Prompt contracts and evaluation | The contract is written for the consumer before any prompt is tried | A structural pass names the obligation it passed, no more | What counts as acceptable is a judgment, not a field |
| 3 | Chat, assistant, and agent | Choose sufficient autonomy before granting capability | Capability is not authority; read the trace | Authority and accountability stay with the person |
| 4 | The agent loop | Exits, budgets and stop conditions are designed, not discovered | A finished wrong answer; finish is not success | Which stops are Claude's to take |
| 5 | Tools and permissions | The permission policy is a design constraint | An authorized change can still be a bad change | Who may do what is a human decision |
| 6 | Claude Code and diff review | Reproduce and write the test before the patch | Accept / revise / reject on evidence, not on Claude's last sentence | The scope decision and the merge are yours |
| 7 | Retrieval and Cowork | You choose what reaches Claude's context | Relevance is not entailment | What the source means in the world is yours |
| 8 | MCP from scratch | The handshake and every handoff are explicit | Compatible is not authorized | The trust decision is yours |
| 9 | Training and configuration | State what should change before changing it | Prediction is not intervention; persistence is not training | The causal question and its justification |
| 10 | Planning before acting | This is the phase gate chapter: plan, dependencies, refusal paths | A plan predicts; a result records | Formulating the problem, and the values inside it |
| 11 | Tool use and verification | Dispatch belongs to the application | 42 in the trace, 99 in the claim | Which checks fail differently from the thing checked |
| 12 | Memory and multiple agents | Revision boundaries and re-engagement triggers | Freshness is not truth; copies are not independence | Independent judgment before shared synthesis |
| 13 | Evaluation and approval gates | The gate itself, designed | Approval that cannot follow a changed target | Finite human attention; the signature |
| 14 | Governance and ethics | Owners, thresholds, recourse designed in | Complete, reviewable, and still weak | Relationships, consent, recourse |
| 15 | Supervised capstone | The whole conducted build | Claim-to-evidence graph; the Gap Account | Ship, narrow, defer, or stop: the accountable choice |
