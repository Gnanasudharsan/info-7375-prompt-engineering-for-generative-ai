# Chapter 15 — Supervised capstone

Ten files contain sixty copied `x` characters each. The packet validator passes.

Nothing in those files demonstrates a need, a boundary, an implementation, a controlled failure, an independent result, a consenting owner, or a defensible decision. Yet the return says `structurally_complete: True` because all ten named Markdown files exist inside the packet and exceed forty stripped characters.

This is not a trick played on a weak validator. It is the validator revealing its honest job. Structure can be checked mechanically. Substance must be established through connected evidence and accountable judgment. The course research fixture executed both sides: an empty folder reported ten missing artifacts, and ten meaningless long-enough files passed. The counterexample keeps the capstone from becoming a scavenger hunt in which file presence substitutes for learning.

Now put Claude in the picture. Asked for ten plausible capstone files, Claude can draft them quickly, in clean prose, with cross-references that look right. The validator would pass them, and so might a tired reader. That is the capstone's real difficulty. Producing a packet has become cheap, and the cost has moved to finding out whether anything in it is true and whether the work should be used at all.

This chapter is where the book's three jobs arrive together: conduct (decide before Claude implements), check (find out what is wrong, and sign only what the record supports), and drive (keep the choices that are yours). Earlier chapters practiced them one artifact at a time. A capstone is the one place where you cannot do only one. Its question is concrete: what would let a person who was not in the room trust this packet, and who answers if they are wrong?

The capstone is one bounded workflow, not ten unrelated documents. Its packet should let another person trace a line from a real need and consenting owner, through data and action boundaries, into a plan, approval gates, implementation, failures, recovery, evidence, and transfer. The last decision, ship, narrow, defer, or stop, must be defended from that trace rather than from presentation quality.

## What you will be able to do

By the end of the chapter, you should be able to:

- explain the exact structural guarantees and limits of `validate_packet`;
- write the capstone's gate before Claude implements anything, conduct Claude Code against it, and run your own checks on what comes back;
- connect ten capstone artifacts into one inspectable argument, each central claim mapped to evidence that could disagree with it;
- demonstrate a bounded Python workflow, using Claude as its only model provider where a model is needed, with prediction, failure, reviewed recovery, and independent verification preserved;
- audit the reviewer: predict its findings, judge each as genuine or a false positive, and record in a Gap Account what the review could not reach;
- prepare a handoff that separates reproducible evidence from unresolved gaps, and end the packet with a sign-off that claims no more than the record supports;
- make and defend a human decision to ship, narrow, defer, or stop, and say which parts of the work were Claude's and which were yours.

All previous chapters are prerequisites. This narrative is paired with the runnable [Lesson 15 materials](../lessons/15-supervised-capstone/docs/en.md). The required path uses Python and Claude Code access. Direct API calls are optional, explicit, and potentially credit-consuming. A Progress Reel remains optional.

Before reading the validator, predict four outcomes. How many issues will an empty folder return? Will a five-character `brief.md` count as present or insufficient? What happens when `brief.md` is a symbolic link to a file outside the packet? Can ten polished files prove that a real stakeholder consented? Preserve the predictions.

## Three jobs, one packet

You have used three devices since Chapter 1: the gate, the sign-off, and the driver's seat. Earlier chapters aimed each at a single artifact. The capstone stacks them, and the stacking is the lesson.

| Job | Where it lives in the packet | The device at capstone scale |
| --- | --- | --- |
| **Conduct** | brief, data-boundary, action-surface-map, plan, gates, pre-mortem | **The gate**: the six pre-build artifacts, tested by a controlled failure and a reviewed recovery |
| **Check** | evidence, audit-note | **The sign-off**: the claim-to-evidence graph, the reviewer audit, the Gap Account |
| **Drive** | artifact (its use), transfer-reflection | **The driver's seat**: ship, narrow, defer, or stop |

The gate says what Claude may do. The sign-off says what the record supports. The driver's seat says what you will do with both. Remove one and the packet fails in a recognizable way: a build with no gate is improvised, a build with no sign-off is a demo, and a build with no driver's seat is a task Claude completed and nobody chose.

## “In the wild” means bounded reality

Before Claude touches anything, someone has to decide what the workflow is for, whose it is, and what it may reach. None of those is an implementation question, which is why they are yours.

A real capstone is not unrestricted access to somebody else's systems. “In the wild” means the workflow serves a real context with a known owner, approved data, and explicit boundaries. Reality enters through consequences, constraints, and evidence, not through maximal autonomy.

Begin with a need stated by the person or team who owns the work, and identify who benefits, who may be affected, and who can authorize the workflow. Consent cannot be generated as fixture text. Claude can draft the questions you should put to the owner; nothing it writes is the owner's answer. If access or consultation is pending, constrain the project to synthetic or public data and label the remaining decision.

Choose a scope narrow enough to supervise. A system that drafts a report from approved sources is easier to evaluate than one that searches private drives, edits records, and publishes externally. The capstone should still include a meaningful action and failure boundary, but ambition is demonstrated through control, not surface area. Every action you add is something a person must be able to check, and that attention is finite.

Write a non-purpose. If the workflow summarizes public course notes, it does not evaluate students, ingest private submissions, or publish without review. Non-purposes give reviewers concrete misuse and scope-drift checks. Then define success as an observable state. “The agent completed the task” is narration. “The generated report contains the three required sections, every consequential claim maps to an approved source passage, the target file matches the reviewed diff, and publication remains pending” is inspectable. Include conditions that make the result unacceptable. These four decisions, owner, scope, non-purpose, and success state, fill the brief, the first piece of the gate you will write below.

## Tear down the packet validator

What do you ask a mechanical check to do, and what do you refuse to let it claim? The implementation answers by being small. It declares ten artifact stems:

```python
ARTIFACTS = (
    "brief",
    "data-boundary",
    "action-surface-map",
    "plan",
    "gates",
    "pre-mortem",
    "evidence",
    "artifact",
    "audit-note",
    "transfer-reflection",
)
```

`validate_packet(folder)` resolves the supplied folder to an absolute root. For each name it constructs `root / (name + ".md")`. It then evaluates three structural conditions, in an order that matters.

First, the resolved path must remain relative to the resolved root. This catches a required filename implemented as a symbolic link to an external target; the repository test links `brief.md` to `/etc/hosts` and expects `brief: outside packet`. The check is about containment, not content trust. A malicious file physically inside the packet can still contain harmful instructions.

Second, the path must be a file. A missing artifact produces `name: missing`, so an empty temporary directory produces ten issues, one for each required stem. The approved research fixture observed that count.

Third, the stripped text must contain at least forty characters. Short material produces `name: insufficient content`. The threshold catches empty placeholders and a few-word stub. It cannot judge relevance, truth, authorship, evidence, or quality.

The result is:

```python
{
    "structurally_complete": not issues,
    "issues": issues,
    "human_review": (
        "Evidence, authority, and understanding must still be assessed"
    ),
}
```

That final string is part of the contract, not a disclaimer to skip. The test confirms that “understanding” remains in the human-review message. Structural completeness deliberately stops before substantive approval.

Judge the design. It is three narrow checks, each of which fails for a reason you can name, plus one sentence saying what they do not cover. The narrowness is the point: a mechanical check is reliable exactly where it is narrow. Ask it to judge relevance and you must give it a heuristic, a keyword list or a score, and fluent drafting tends to satisfy any heuristic that reads only the surface of prose, which is what Claude produces best. The check worth having fails differently from the thing it checks, and a path resolution and a character count do not care how good the prose sounds. Never let the validator's `True` stand in for the rest.

<!-- [FIGURE: Cajal production brief. Packet structure and substantive review are separate gates. Include ten files, containment, presence, length floor, structurally complete, human review. Show the confirmed relationship that evidence, authority, understanding, consent remain open. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Packet structure and substantive review are separate gates. evidence, authority, understanding, consent remain open.](../images/15-supervised-capstone-fig-01.png)
*Figure 15.1 — Packet structure and substantive review are separate gates*

## Worked example: missing, escaping, meaningless, and useful

Start with an empty temporary directory: none of the ten paths is a file, so the loop appends ten missing issues. Add only `brief.md` with the text `short`: it exists inside the root but is under forty characters, so its issue changes from missing to insufficient content while nine others remain missing. Make `brief.md` a symlink whose target resolves outside the packet, and containment, which runs before presence, reports `brief: outside packet`. Finally, create all ten files with repeated `x` characters longer than forty. Every path resolves inside the root, every path is a file, and every body clears the threshold. The executed research fixture reports structural completeness.

The meaningless packet is the decisive counterexample. It proves that presence and length do not establish substance. It is also the fluency trap at its smallest: the packet is well formed, it passes, and the pass invites the belief that someone checked something. The remedy is not a better validator. It is a sentence, inside the packet, saying what was checked. A full human review must inspect whether each artifact performs its role and whether the links between artifacts hold.

A useful `evidence.md` does not merely say “tests passed.” It records exact commands, versions, inputs, outputs, failures, and interpretations, and it maps claims to checks that can disagree. A useful `audit-note.md` predicts review findings before Claude critiques the packet and records whether the learner revised, defended, or acknowledged each one. The validator sees only that both files are long. The reviewer sees whether they form evidence.

| Fixture | Structural result | Substantive conclusion |
|---|---|---|
| empty folder | ten missing issues | packet absent |
| short brief | insufficient plus missing | placeholder detected |
| escaping symlink | outside-packet issue | containment violated |
| ten repeated strings | complete | no learning established |
| connected real packet | possibly complete | requires claim-level review |

## Ten artifacts, one argument

A packet is ten documents. An argument is the lines between them. The ten follow the order of the work, in three groups.

Six are written before Claude executes anything, and together they are the gate. The `brief` states the need, consenting owner, affected people, success condition, non-purpose, and decision scope, and what would make the workflow inappropriate. The `data-boundary` inventories sources, classifications, provenance, access, retention, deletion, and exclusions, labeling data public, synthetic, internal, personal, or unknown by the project's real policy rather than the label most likely to pass. The `action-surface-map` shows what the workflow can read, propose, write, send, or publish, separating capability from authority and flagging external or irreversible effects. The `plan` lays out evidence-producing steps with dependencies, stop conditions, budgets, and replanning triggers. The `gates` bind consequential proposals to exact content and responsible decisions, with evidence, effects, rollback limits, expiry, and what happens while review is pending. The `pre-mortem` predicts stale state, invalid calls, injection, duplicate actions, privacy exposure, misleading success, and other project-specific failures, each with detection, owner, response, and residual risk.

Two record what the build produced. The `evidence` artifact holds reproducible commands and observed results, distinguishing code inspection, deterministic fixture output, model output, human observation, and external product behavior. The `artifact` is the usable output, or a precise pointer and reproduction route. A screenshot alone is not reproducibility.

Two judge it. The `audit-note` records predictions before critique, findings, evidence-based responses, failed cases, corrections, and unresolved gaps, and it ends with the Gap Account and the sign-off. The `transfer-reflection` records what the learner will delegate more readily, what capability must remain practiced, and what decision remains human, each pointing to project evidence, and it holds the final ship, narrow, defer, or stop decision and its reason.

Every artifact should reference the relevant others. The brief's success criterion maps to evidence. The data boundary constrains the action map. The plan invokes the gates. The premortem predicts a failure demonstrated in the audit note. The transfer reflection cites the controlled recovery. Without those links, ten documents remain ten islands. Claude can add such cross-references in minutes, and a validator cannot check them, so treat each reference as a claim: open the target and confirm it says what the pointer says.

<!-- [FIGURE: Cajal production brief. A capstone is one evidence chain. Include need + owner, boundaries, plan + gates, execution, evidence + audit, human decision, handoff. Show the confirmed relationship that artifact presence cannot jump directly to justified use. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![A capstone is one evidence chain. artifact presence cannot jump directly to justified use.](../images/15-supervised-capstone-fig-02.png)
*Figure 15.2 — A capstone is one evidence chain*

## The gate: Claude proposes, Python constrains

What has to be written down before Claude implements, and what has to hold before its output moves on? The first six artifacts are the capstone's gate. Before you ask Claude Code for any part of the workflow, write the short version of it, in plain sentences, in your learner workspace.

*Design.* The workflow, the owner, the approved data, and the one action that matters are your choices, or the owner's. Say which. Claude can challenge each of them. It did not make any of them.

*Contract.* What the workflow must do. What it must refuse: to publish, to read outside the approved sources, to count a retrieved passage as support when it does not entail the claim. The observable state that means done, and the conditions that make the result unacceptable.

*A wrong version your checks must catch.* A run that completes, reads well, and leaves the wrong state: a fluent draft whose citation does not support its claim, or a local-write approval treated as permission to publish. If your checks cannot tell that run from the right one, the gate is not finished.

*What a failure looks like.* One dated sentence, written before the run, naming the failure you will stage and what you expect each mechanism to do with it. It is the lead entry in your pre-mortem.

*What this build may claim.* A bounded local result under recorded conditions. It cannot say the workflow is safe, that the owner consents to anything beyond the brief, or that a live Claude run would behave the same.

Claude can sharpen this gate, but it cannot write it for you without defeating its purpose. The gate is where your decisions go on the record, and it is what you will test Claude's implementation against.

“Claude proposes, Python constrains” is a division of labor with a reason behind it. Claude does the language work: drafting, summarizing, proposing a tool call. Python holds whatever must be the same every time: which tools exist, whether an argument is valid, whether a path stays inside the approved root, whether a proposal matches the content a person approved, and what gets recorded. The reason is the one Chapters 1 and 5 gave. A prompt is a request, not a boundary. Telling Claude “do not publish” is useful task context, but the publication boundary is an application that lacks, or gates, that capability. A prompt-injected source should not be able to grant itself tools. The trade-off is flexibility. Every boundary you code is a case you foresaw, and the case you did not foresee passes straight through, which is why the gate also asks what a failure looks like.

Start offline. Inject a callable into the controller where possible so tests do not need network access. Validate tool names and arguments in Python, and resolve paths before action. Preserve model requests, application results, and final claims as three separate records, because the claim is the part most likely to say more than the other two support. If you add a live Messages path, make it opt-in, bound requests, identify the model actually used, protect credentials, and record cost-bearing behavior. Never replace a missing live run with invented output; live behavior is evidence about that run under its recorded conditions, not a universal guarantee. Keep the implementation small enough to explain, because adapted code is not understood until you can trace the changed behavior and tests.

### Build It: the baseline

Before you consult the reference, write your own `validate_packet` in your learning-artifacts folder from the ten names and the three conditions. Then run the Practice Lab cases (a removed evidence artifact, a long but meaningless file) and add at least two tests of your own: a meaningful success outside the demo, and a failure that would matter in your capstone. State what remains untested. Your validator is the baseline: the record of what you understood before Claude touched anything, and a mechanism small enough to audit. You cannot audit a containment check you have never tried to break.

### Use It: conduct Claude Code against your gate

Now hand Claude the work it is good at. Open Claude Code in the course repository; the lesson's [working prompt](../lessons/15-supervised-capstone/outputs/claude-code-prompt.md) sets up the session. Give it the gate, the six artifacts and the test list, not your implementation, and ask for the bounded workflow, with the model injected, that satisfies the contract and passes your tests. Then run your tests on what it returns, yourself.

Do three things with the result. First, note which tests failed. A failing test is often a gap in the gate, because Claude had only what you wrote. Second, name one difference in behavior between its implementation and your plan: a boundary it handled that you missed, or one it silently ignored. The first case revises your gate. That is a re-engagement, not a violation of design-first: a later finding can reopen an earlier decision, and you log the reopening and its reason. Third, ask Claude to propose a deliberately wrong version that still passes your checks, and test by hand whether it does. If it does, your checks were too weak, and you found out cheaply.

Preserve the actual transcript: your prompt, the plan, the diff, the commands, and the outputs, with the date and displayed model label. If a session failed or did not run, record that rather than substituting a fixture.

## Controlled failure and reviewed recovery

A gate you have never seen fail has not been tested, and a polished happy-path demo proves very little. Choose one failure that matters to the workflow and can be reproduced safely, and predict it before running; that prediction is the sentence you wrote in the gate. Preserve the input, action, reported outcome, independently observed outcome, and gap.

Suppose the workflow drafts a source-grounded report. A controlled failure might be a relevant-looking passage that does not support a deadline claim: the model produces fluent prose and a citation, the source check rejects entailment, and nothing is published. The trace shows request, retrieved passage, draft, failed check, and stop state. This is a constructed illustration of the shape, not a recorded run.

Recovery is not “ask Claude again until it passes.” A human or declared policy reviews why the case failed. The plan may narrow the claim, select a different approved source, add an abstention rule, or defer. The changed proposal goes through its gate again, and a later success is compared with the original failure and checked independently. Recovery can also reopen your design: a failure may reopen a source classification, a scope line, or the success condition itself, and the honest record says so.

Use different failure routes. If Claude drafts the claim, Python can validate source identifiers and structure while a person inspects semantic support. If Python calculates a total, a separate derivation can check it. Two Claude prompts sharing the same context are not automatically independent. And preserve the failed output when privacy and safety permit: a demo edited to show only success hides the most valuable part of supervision.

## The miniature casebook

How do you keep hindsight from smoothing the story? By recording the prediction first and refusing to revise it. *Computational Skepticism for AI* calls the habit a prediction-lock: write what you expect, dated, before you observe, and never edit it afterward. The learning is the gap between the prediction and what happened. “Look at it and iterate” never means re-prompting until the output looks right.

Write the controlled failure as a compact casebook entry:

1. prediction recorded before execution;
2. exact sanitized input and provenance;
3. action or tool request;
4. system-reported outcome;
5. independently observed outcome;
6. gap between report and evidence;
7. containment and recovery decision;
8. remaining uncertainty.

If you expected the system to refuse and it accepted, record that. If you expected failure and the checker correctly rejected, explain which mechanism did the work. Do not manufacture a surprising error for drama. One observed miss does not prove a permanent limitation of every future model; it supports a bounded claim about this workflow, case, and check. One clean run does not establish general reliability. The casebook accumulates inspectable encounters rather than universal slogans.

## Audit the reviewer

Who checks the check, and what did they not look at? So far only the author has read the packet, and the author was in the room for every decision. Ask Claude Code to review it, then treat the review as one more output to evaluate.

**Predict first.** Before asking for critique, predict three specific findings with artifact locations and reasons. For example: the data boundary does not trace deletion from exported reports; the gate's rollback claim ignores an external message; the evidence matrix relies on the same parser for production and checking. A prediction has to forbid something. “The review will find weak integration” can be matched by anything, so it teaches nothing. Mark each as a finding you expect to be genuine or a false positive, and record the displayed model label and date, because a later run of the reviewer may differ.

Then request critique of the existing packet without allowing edits, and preserve the actual response. For each finding, locate the relevant evidence, write a row (the finding; whether it is located; genuine or false positive; your reasoning; your action), and choose one of three legitimate responses. Revise when the critique identifies a supported defect. Defend when the packet already addresses it, citing the exact passage and explaining why the critique missed it. Acknowledge an unresolved limit when neither revision nor defense is justified. A finding without located evidence is not a finding. Accepting every finding is a failure, because a misreading you accept is someone else's error signed as yours, and rejecting every finding is its mirror. Do not force Claude to produce a false positive so you can demonstrate independence.

Evaluate the reviewer itself. Did it find the predicted issues? Did it raise a plausible but unsupported concern? Did it overlook a controlled failure already visible? Score each prediction matched, partly matched, or missed, and credit the specificity of your reasoning over the hit rate. This course holds no measurement of how often such a review is wrong about a packet like yours, so treat every finding as a hypothesis to check. A clean review is corroboration, not proof: this reviewer, this time, did not refute you.

### The Gap Account

Close the audit-note with a Gap Account, the course's way of recording what the review did not reach. For each gap, ask one question: would a better prompt, a second run, a differently built reviewer, or more evidence close it? If yes, it is a *contingent miss*: fix it, or run the better review, and say so. That is the weak version of a Gap Account, a defect the next review patches.

If the answer turns on the kind of reviewer this is, a model that reads only your packet, record a *structural gap for this review*. I use “structural” to mean owing to the reviewer's kind and access, not “for all time.” Three patterns are worth looking for, and none is a form to fill in. A consequence visible only from inside a relationship you answer to: the packet records that the owner agreed, and only you remember that the agreement came with a condition nobody wrote down. A judgment grounded in domain experience the packet never stated: a number that is fine on paper and wrong for this site. And an asymmetry of stakes: you will bear the consequence, and the reviewer will not. A reviewer sharing the draft's model and context also shares its blind spots, so a second pass by the same reviewer will not close that gap. For each gap, name the evidence or expertise that could help and the person accountable for the decision now. A gap is a boundary on the final claim, not permission to give up.

The companion book goes further. It argues that for the second kind of gap the limit is permanent: that no reviewer of any capability can reach what depends on being situated, having a stake, and being accountable, grounding that in philosophy and in safety literature on correlated errors. That is an argued position, and this course does not ask you to agree with it or prove it. Your Gap Account makes a smaller claim you can check: this review, on this packet, did not reach this; repeating it would not; this person can. One observed miss does not show that no future model could find the issue. It sets a boundary for the decision you are making now.

## Independent verification and outcome state

What would tell you a central claim is wrong, and which check fails differently from the thing it checks? Map every central claim to an artifact and a check. “The report was created” can map to file existence and read-back. “The report is source-grounded” needs claim-to-passage inspection. “The owner consented” needs a real decision record, not model text. “The workflow is safe” is probably too broad and should be decomposed.

Inspect resulting state, not only trajectory. An agent can execute the planned calls while the destination remains wrong. A file write can succeed locally without being committed or published. A sent request can receive a success code while the intended person never receives it. State exactly what was observed.

### Build a claim-to-evidence graph

A packet becomes inspectable when its claims form a graph whose edges point to evidence and decisions. Start with the final recommendation and break it into smaller claims until each can be checked by one or more artifacts. Claude can draft the first version quickly, since it is an index-and-cross-reference task. You decide whether each edge is real, because an edge is a claim that this evidence bears on that claim.

Suppose the recommendation is: “Narrow the workflow to create a local source-grounded draft, retain only public fixtures for one day, and require a human before publication.” That sentence contains at least six claims: the workflow creates a draft; the draft uses approved sources; the target remains local; retained fixtures are public; deletion follows the stated day boundary; and publication is gated.

Map each separately:

| Claim | Producing mechanism | Evidence | Decision owner | Residual gap |
|---|---|---|---|---|
| local draft exists | bounded file tool | resolved path, read-back, diff | project owner | later mutation |
| consequential claims are supported | retrieval plus drafting | claim/passage matrix | content reviewer | interpretation disagreement |
| no external publication occurred | absent capability plus event trace | action map and trace | workflow owner | systems outside trace |
| fixtures are public | source inventory | source IDs and classification review | data owner | misclassification |
| one-day policy executed | deletion job | pre/post inventory in controlled stores | retention owner | provider copies |
| publication needs approval | bound proposal gate | rejected no-decision fixture | authorized publisher | stolen credentials |

The residual-gap column prevents the graph from becoming decorative certainty. Every evidence route has scope. Read-back establishes content at an observed time. An event trace can show no publish action inside the instrumented workflow but not every possible external channel. A classification review can be wrong. These limits inform the deployment choice, and they are the raw material of the sign-off's “not checked” line.

Claude produces such a graph in a minute; checking one edge means opening its target. Output is cheap and verification is not, and a project that does not budget for verification will not get it.

Look for orphan nodes. A claim with no evidence should be removed, narrowed, or marked pending; an artifact supporting no claim may be busywork; a decision with no named owner is unresolved; evidence cited by many claims deserves extra scrutiny, because one defect can collapse several conclusions. Look for circular support too: the audit note cannot establish that the evidence is correct by summarizing `evidence.md`, which cites the audit note. The central result should connect to an observation or derivation outside its production narrative.

Before handoff, perform a contradiction pass. Compare the brief's declared purpose with the implemented tools, the data inventory with actual fixtures, the action map with the trace, gate decisions with executed targets, and retention promises with deletion evidence. Do not resolve a contradiction by choosing the newest document. Determine which artifact is authoritative, correct the dependent claims, and preserve the revision reason. Then freeze the review candidate by revision or digest so later edits cannot masquerade as reviewed work. If a consequential file changes, rerun the checks whose premises changed plus the integration checks; that is a new review candidate, not a continuation of the old approval.

## Handoff that survives the author

A handoff is a seam, and seams are where risk lives. A packet that only its author can run has a gate with one person behind it. A new authorized person should be able to understand the purpose, run the offline path, inspect evidence, identify decision owners, and know what not to do, using only the prerequisites, commands, expected outputs, failure behavior, recovery steps, and open issues you wrote down.

### Reproduce the handoff as an experiment

Do not wait until presentation day to discover that only the author can run the workflow. Give a bounded participant only the documented prerequisites and commands, in a sanitized environment, and observe where they must ask for hidden knowledge: an unstated working directory, an unexplained environment variable, a dependency installed globally on your machine, a fixture at an absolute personal path, a recovery step known only from your debugging session. Each question marks missing transfer evidence. They run the offline path first, compare actual output with the documented expectation, trigger the controlled failure, and locate the evidence matrix. Live behavior comes later and only with explicit authorization.

Record the attempt as evidence: environment, commands, failures, questions, revisions. Do not score the reviewer for speed. After revising the documentation, rerun from a clean-enough context rather than assuming the prose fixed the problem, and state what persisted. Reproduction is an observed property of a particular handoff, not an adjective awarded to documentation. Never package API keys, private data, or unauthorized source excerpts; say who supplies which secret, and how.

State exclusions prominently. If live API behavior was not tested, say so. If stakeholder consultation is pending, say so. If only local writes were authorized, do not imply publication. And answer the maintenance questions: who refreshes sources, what invalidates memory, when approvals expire, which threshold pauses the system, how dependencies are updated and re-evaluated. A capstone handed over without these answers is a demo, not a durable contribution.

## The sign-off: the last thing the evidence says

The graph's residual-gap column, the Gap Account, and the handoff exclusions all feed one short statement, the last thing the audit-note says. Claude can write the words of a sign-off fluently, and they will be empty: the part that matters, what was not tested, is the part a model has no record of. Write it from your record. This is the template and the standard, not a signature:

```text
Sign-off — capstone packet
Checked:      which claims in the graph, against which evidence (name them)
How:          by hand / by a test I wrote before reading Claude's version /
              by recomputation / by a check that fails differently /
              with Claude's help (say which parts)
Not checked:  each residual gap in the graph; each Gap Account item;
              live behavior if no live run was recorded; anything outside
              the instrumented trace
Not claiming: that the workflow is safe; that the owner's consent covers any
              use beyond the brief; that a clean review means a sound packet
Cleared by:   a named person for each consequential decision (owner, data
              owner, publisher), not "the team"
Verbs:        recorded, computed, tested, inspected, reviewed; not
              "established" or "proven" unless a criterion supports them
Signed or withheld: ____________  (name, date)
```

The verbs match the evidence: a passing test supports “tested,” not “safe.” The “cleared by” line needs a role that can be asked about its decision and can lose something if it was wrong. And withholding is a legitimate outcome. A process whose only permitted result is “signed” is a rubber stamp with a person's name on it. If the record does not support signing, say what would, and stop there.

The sign-off has a cost. It buys legible answerability, since after a failure someone can find who signed and read what they did not warrant, and it pays in speed and deniability, because someone must be willing to be named. That friction is the point. A typed name does not authenticate anyone, and the course makes no legal compliance determination from it.

## Ship, narrow, defer, or stop

Passing structure and tests does not oblige deployment. Who decides, and on what? Evidence informs the decision; it does not make it. The choice weighs intended benefit, affected people, evidence quality, reversibility, review capacity, unresolved gaps, and available alternatives, and someone has to own the weighing.

### Defend the four options against the same evidence

Do not write the recommendation first and assemble supporting facts afterward. Put ship, narrow, defer, and stop into one comparison against the same criteria: benefit, data exposure, action consequence, evidence strength, reversibility, review labor, consent, maintenance, and unresolved harm. The criteria express values, so say who chose them. Claude can draft the comparison, including doing less, but it cannot supply the weights.

Ship when evidence supports the bounded use in the brief, not any future expansion, owners accept their roles, consent and authority exist, and recovery is credible. Narrow when a smaller action surface, data set, or audience preserves value while reducing unsupported claims. Ask which component creates disproportionate uncertainty: removing automatic publication may keep most of the value and keep the artifact local. Narrowing is a design response to evidence, not a failure.

Defer when the missing evidence, consultation, expertise, or capacity could realistically be obtained, and name the concrete condition and its owner: until the data owner classifies one source, a stakeholder conversation occurs, a specialist reviews a consequential metric, or an outcome checker exists. An indefinite “more research is needed” evades the decision. Stop when the need is not legitimate, consent cannot be obtained, harm cannot be mitigated within available capacity, or a simpler non-AI process dominates. Record what was learned and retire data and permissions safely. Effort already spent is not evidence for continuing.

Now test sensitivity. Would the recommendation change if the external-write capability were removed? If retention fell from a year to a day? If the owner withdrew consent? If the independent checker disagreed once? If the reviewer backlog doubled? These counterfactuals reveal which assumptions actually drive the decision.

The final recommendation should include the chosen option, rejected alternatives, evidence, affected interests, conditions, owner, review date, change triggers, and who may revisit it, since a later source change, incident, or stakeholder objection can reopen the choice. It should also contain one sentence of epistemic restraint: what the packet does not establish. That sentence is often the strongest evidence that the author understands the system.

### Write the recommendation so the judgments are separable

*Conducting AI* gives the form in its Memo A and Memo B. Memo A is the machine's analysis, here Claude's evidence assembly and option comparison. Memo B is not Memo A with your name added; a signature without the account behind it counterfeits accountability. Write the recommendation in labeled parts: what Claude produced; what you add that the packet could not show; why the evidence should be trusted, citing graph rows and not Claude's confidence; why this is the right action here, for these people; and the recommendation you sign. The separation does not diminish your work. It makes your part defensible, because you cannot answer for a judgment you cannot tell apart from the draft.

### The driver's seat

This is how the capstone's work divides, task by task. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Assembling the evidence trail and running the validator | Cross-reference, run `validate_packet`, list contradictions | Decide which artifact is authoritative in each, and recheck a sample by hand | A list of contradictions does not say which document to believe |
| Comparing ship, narrow, defer, and stop | Draft the comparison on your criteria, including doing less; argue against your preferred row | Choose the criteria and the weights | The criteria express values, and someone chose them |
| Reviewing the packet | Give one read-only critique | Predict first, judge each finding, write the Gap Account | The reviewer sees the packet; you were in the room |
| Consent and authority | Draft the questions to put to the owner | Obtain a real decision from a real owner and record it | Consent cannot be generated, only given |
| The choice and the signature | Nothing beyond the draft | Decide, sign or withhold, and name who may revisit it | Whoever signs is the one who will be asked |

*Irreducibly Human* sorts work into three verdicts: deprioritize (hand it over gladly), supervise (use it and audit it), and protect (keep it). Its warning governs the first: deprioritization is not deletion. You can hand Claude the claim-to-passage matrix only because you can still check a row, which is why you built the validator by hand. In the table, the first row is deprioritize with a spot-check, the second and third are supervise, and the last two are protect.

The book's deepest reason for the third verdict is a thesis: that what machines do, however well, is reckoning (calculation, pattern, inference at scale), while judgment takes the world to matter and answers for the result. The book presents this as an argued position and marks its strongest form as contested. You are not asked to adopt it. The course needs a smaller claim you can check: whoever signs this packet will be asked about it, and no institution around your capstone will ask Claude. That is a fact about where accountability lands, and it is enough to keep the choice with you.

Record the split in the transfer reflection: one task you delegated more readily, one capability you kept practicing, and one decision you retained. If you cannot point to the transcript line or the edit that shows each, the split happened in your head and not in the record.

### Ship It: submitting the packet

The packet is the artifact. Submit the ten files with exact commands, kept under learning-artifacts/week-15/, using the [artifact brief](../lessons/15-supervised-capstone/outputs/artifact-brief.md) as the checklist: Claude usage disclosure, source citations, a student-versus-external code estimate, the license, the style declaration, and one decision you revised after testing. Acceptance is concrete: another student can reproduce the offline behavior and name what still needs human verification. Include no credentials or restricted source material. A Progress Reel can show mechanism, failure, recovery, and decision, but it cannot substitute for reproducibility.

### Verify and reflect

Run the demo and the six tests, then your two additional tests, and preserve the commands, outputs, and your interpretation. A passing suite establishes only the tested behavior, not universal reliability or permission to act. Then find the sentence in your packet a skeptical reader would attack first, and find its evidence. If you cannot, narrow it or mark it pending.

The most useful reflection is local: which of the three jobs did you do least well? Name the artifact where it shows (a decision made after Claude had started, a check that was not independent, a choice you let the draft make) and the edit that would have fixed it.

## Common capstone failures

Each of these is one of the three jobs left undone.

**Packet completeness theater** (check). Ten long files pass while no central claim is reproducible.

**Demo-only evidence** (check). A recording shows success but omits commands, inputs, versions, and failed cases.

**Synthetic consent** (conduct). Claude-generated stakeholder language is presented as permission.

**Recovery by repetition** (check). The same prompt is rerun until a desired answer appears, with no reviewed change.

**Shared-check dependence** (check). The production and checker routes rely on the same mistaken source or helper.

**Authority drift** (conduct). A local-write approval is described as permission to publish.

**Reflection without evidence** (drive). The learner states lessons in generic terms without identifying a changed decision or preserved capability.

**Polish as quartile strategy** (drive). Visual sophistication obscures weak implementation or unverifiable claims.

## Assessments — ungraded practice

These Assessments are ungraded. They prepare the capstone evidence; they do not create a second capstone.

### Warm-up

1. **Trace the validator (Understand).** Predict and run the empty-folder case. Explain why ten missing issues establish structure rather than substance, and say what the `human_review` string hands to a person.

2. **Test content floor (Apply).** Compare a short file with a forty-plus-character meaningless file. State exactly what the threshold can reject, and write the sign-off sentence that keeps a passing packet from being read as more.

3. **Inspect containment (Analyze).** Reproduce the escaping-symlink case in a temporary directory and explain why containment does not imply trusted content. Name one boundary of your own capstone that belongs in Python rather than in a prompt.

### Application

4. **Claim-to-artifact map (Analyze).** Select five central capstone claims and point to the exact artifact and evidence that supports each. Mark unsupported links, and fill in the residual-gap column for the supported ones.

5. **Controlled failure (Create).** Write the gate first: the contract, the wrong version your checks must catch, and your dated prediction. Then run one safe project-specific failure, compare reported with observed outcome, and preserve containment.

6. **Reviewed recovery (Evaluate).** Explain the decision made after failure, change the mechanism or scope, rerun checks, and compare results without hiding the original trace. Say whether the failure reopened an earlier decision.

7. **Independent check (Create).** Design a verifier that fails differently from the production route. Name one assumption they still share, and who checks it.

### Synthesis

8. **Packet integration (Create).** Add cross-references so the brief, boundaries, plan, gate, premortem, evidence, artifact, audit, and reflection form one argument, then open every target and confirm it says what the pointer says. End the audit-note with a sign-off whose “not checked” line you can defend.

9. **Predicted critique (Evaluate).** Record three expected Claude Code review findings, request read-only critique, and judge each returned finding as genuine or a false positive using located evidence, responding with revision, defense, or an acknowledged limit. Close with a Gap Account that separates a contingent miss from any gap that depends on the reviewer's kind.

10. **Handoff rehearsal (Analyze).** Have an authorized peer follow only the documented offline instructions. Record where the handoff fails and revise it; do not expose secrets or restricted data.

### Challenge

11. **Deployment decision (Evaluate).** Defend ship, narrow, defer, or stop using project evidence, affected interests, remaining gaps, reversibility, and review capacity. Separate what Claude drafted from what you add, name what would change the decision and who owns reconsideration, and point to the transcript line or edit that shows which parts were yours.

Complete the existing [Lesson 15 knowledge check](../lessons/15-supervised-capstone/quiz.json) after the practice. It is self-review, not an additional graded assignment.

## Capabilities summary

You can now distinguish a structurally complete packet from a defensible capstone. You can trace ten required artifacts as one chain, demonstrate a controlled failure and reviewed recovery, evaluate a reviewer, and map final claims to independent evidence. You can prepare a handoff with explicit exclusions and make a bounded deployment decision that tests and presentation do not make for you.

Underneath each sits one of the three jobs. You conducted: you wrote the gate before Claude implemented. You checked: you built a graph whose edges could disagree, audited a reviewer, wrote down what it could not reach, and signed only what the record supported, or withheld. You drove: you made the choice and kept the record that shows which work was yours.

## Anthropics

Anthropic's [Claude cookbooks](https://github.com/anthropics/claude-cookbooks) provide Python examples you may adapt when the mechanism genuinely matches your project. Record the specific source, URL, revision or date, license, changes, and evidence for those changes. Do not adopt an entire stack merely because it is upstream.

Anthropic's [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) can sharpen the distinction among tasks, trials, graders, transcripts, and outcomes. Compare that guidance with your evidence packet. The links were checked for the approved research packet on 2026-09-06; current product guidance may change.

## Computational Skepticism

The companion's accountability chapter lists independent review among the requirements of a working accountability regime, with a plain test: a named reviewer other than the builders, with authority to halt or revise. See [Attestation and review](../docs/computational-skepticism.md#attestation-and-review); the prediction habit used above is at [The casebook](../docs/computational-skepticism.md#the-casebook). Apply the halt test to your packet. Claude's read-only critique can comment, and it cannot stop anything. Find the person who can stop the workflow and the line where that authority is written down. If you cannot, the review was commentary, and the sign-off's “withheld” option has no one behind it. This borrows one test from the book's instrument; it does not validate the rest of the regime for your project or authenticate a signature.

## Conducting AI

The companion's dress-rehearsal chapter adds a diagnostic the body has not used: aim your prediction at the seams. A reviewer who confirms that each artifact is thorough has confirmed what is cheap to confirm. The valuable finding names a relationship between two artifacts that each look fine alone, for instance a data-boundary exclusion that the action map's read capability quietly reaches around. Rewrite one prediction so that it names two artifacts. See [Critique and the Gap Account](../docs/conducting-ai.md#critique-and-the-gap-account) and [Interpretation and accountability](../docs/conducting-ai.md#interpretation-and-accountability). Then apply the book's thin-sentence test to your transfer reflection: mark every sentence you could have written without knowing anything Claude's summary did not already state. Those sentences are the draft restated, and the reflection has to carry the others.

## Irreducibly Human

The final division of labor is not “AI writes and a human signs.” It is capable assistance joined to accountable human purpose and judgment. See [Purpose and accountability](../docs/irreducibly-human.md#purpose-and-accountability). A test for honest deprioritizing: pick one task you handed to Claude, such as the first-draft claim-to-passage matrix, and redo three rows by hand without it. If you cannot tell whether a row is right, you surrendered that task rather than deprioritized it, and your sign-off's “how” line claims a check you could not have performed.

**AI should** assemble existing evidence, run the Python packet validator, identify contradictions, compare bounded options (including doing less), and draft summaries. It should not invent stakeholder consent, approvals, deployment decisions, personal reflection, or confidence unsupported by the record.

**Human should** decide whether the work serves the intended people, weigh competing goods the score does not settle, own the ship, narrow, defer, or stop choice, and remain answerable for revision, stating who may revisit the decision and what evidence would change it. Point to evidence of the split in your transfer reflection: a transcript line, a diff, or an edit you made. Treat claims about irreducible human capacities as argued positions, not propositions the assignment requires you to prove.

## Closing question

You began by watching prompts produce variation. You built contracts, controllers, permissions, reviews, retrieval, protocols, configuration, plans, tool loops, memory, approval gates, and governance. Each mechanism made some claim easier to inspect and exposed another claim it could not establish.

Now ask the only closing question that matters today: which part of this system can you explain from evidence, and which part still needs a person to decide?
