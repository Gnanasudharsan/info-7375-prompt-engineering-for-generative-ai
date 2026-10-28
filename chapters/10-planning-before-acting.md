# Chapter 10 — Planning before acting
*A complete form can contain no plan at all.*

Suppose a plan has an objective, inputs, scope, steps, tools, risks, verification, and a stop condition. Every required heading is present. The validator reports no missing fields. The plan is also useless because every value is the single string `x`.

This is not a rhetorical exaggeration. The research script constructs that object and passes it to the course's `missing_fields` function. The returned list is empty. The same research run orders three steps as inspect, build, verify and rejects a dependency cycle. These observations are preserved under `chapters.10` in the [research output](../research/worked-examples.json).

The counterexample does not make field checks pointless. It tells us their job. They catch absence and false-valued entries under a declared list. They do not judge whether an objective matters, a scope is safe, a risk is plausible, a verification step tests the claim, or a stop condition can actually be observed. A structural check earns its place by reliably rejecting structural omissions. Trouble begins when a clean form is presented as a trustworthy plan.

So what is a plan for? Claude implements well against a complete specification and badly against an incomplete one, and it will not tell you which kind you gave it. The decisions that determine whether a build goes well are made before the build: which problem, which boundary, which order, which evidence between steps, which point to stop. A plan is those decisions written down where another person can challenge them. Reviewing it is the gate.

Chapter 1 named the three jobs that stay with you. Here they take these forms.

- **Conduct.** The plan is the design that precedes implementation. The reviewed plan is the gate: nothing changes until it meets a condition you can state.
- **Check.** A plan predicts action; a result records it. A complete form is not a plan, and an acyclic graph is not an executable one. You review with counterexamples before anything runs.
- **Drive.** The choice of problem, and the values inside that choice, are yours. Claude can suggest framings and attack your selection. You defend it.

Chapter 9 asked what object will change. This chapter asks whether the proposed sequence is justified and bounded before it changes anything. We build two mechanisms by hand, a field-presence check and a topological ordering of named dependencies, then put their outputs back in their proper place by subjecting a structurally valid plan to semantic and authority review.

The Python build runs offline and needs no direct API credits. Claude Code can propose or critique a plan through the assumed course account, but the returned plan remains a proposal. If the interface is unavailable, preserve that fact and complete the offline construction. Do not invent a Claude-authored plan or human approval to make the artifact look finished.

## What you will be able to do

You should be able to identify all eight required plan fields, trace missing-field behavior, order an acyclic dependency graph, and explain duplicate, unknown-prerequisite, and cycle rejections. You should also be able to revise a vague step with explicit evidence and authority, reject a structurally valid unsafe plan, and write a handoff condition that another person can apply.

You should also be able to do three things the rest of the book builds on. Conduct: choose an objective from candidates that genuinely disagree about success, write the plan Claude Code will implement against, and state the condition under which it may proceed. Check: review a plan with counterexamples before it acts, and write a sign-off that says what the review covered and what it did not. Drive: say which parts of planning you handed to Claude and which you kept (the problem, the values inside it, the approval).

You need Chapters 4 through 9, Python dictionaries and sets, and the idea of a directed dependency graph introduced here. The paired [lesson](../lessons/10-planning-before-acting/docs/en.md) provides the runnable sequence and existing knowledge check. Before reading the reference, predict which fields a one-objective plan lacks and how a build-after-inspect relationship should order.

## The plan is the design, and the review is the gate

The decision here: how much do you settle before Claude acts, and who can still say no?

Design first, then let Claude implement: that sentence is the discipline this chapter teaches. Planning exists to make proposed work inspectable before action. That means exposing the destination, allowed inputs and scope, intended steps, tools, risks, evidence, and stopping rule while change is still cheap. The plan is not hidden reasoning and need not reproduce private deliberation. It is a public action contract another person can critique.

Conducting AI calls the boundary a phase gate: the explicit point where Claude's work stops and a person's begins, stated as a specification of what each handles and a testable condition that must hold before the output moves downstream. The appendix on The Pragmatic Conductor reaches the same idea through design by contract: you write the contract, the agent writes the implementation, and assertions or tests derived from your contract check it. A plan, in this chapter's sense, is that contract for a whole piece of work.

Conducting AI's Boondoggle Score has the same shape at larger scale: the prompts for Claude in dependency order, the human's actions in the same order, and a testable handoff condition between each Claude task and each human task. It is my own instrument, and the five sorting questions that Computational Skepticism attaches to it have no external validation behind them that I know of. Treat the Score as a heuristic, not a diagnostic. The eight fields here are a smaller instrument, this course's own review tool.

Two things follow. The plan is worth the most before anything has run: a revision costs a paragraph there and a rollback later. And the review is the gate, because a plan nobody reviewed is a draft however complete its form.

Design first is not design frozen. The design research behind Conducting AI finds that problem and solution develop together: a move in the solution space surprises you and forces a reframing of the problem. A plan is a controlled state with versions. When a result contradicts an assumption the plan rested on, you revise the plan, with the reason recorded, instead of pushing forward on a stale one. The appendix's constructed discount-rule example has that beat: auditing the diff shows rounding was never specified, which reopens the requirement, and the instruction is to log it and go back. My claim is narrower than "plan everything first." The first version of the plan should exist, and be reviewed, before Claude changes anything, so that when evidence reopens a decision you can see which decision it was.

## Formulate before you plan

The first decision in a plan is not in any of the eight fields. It is which problem the plan is for. A perfectly ordered plan can optimize the wrong objective, and the cost is highest when Claude executes it fluently, because a polished, internally checked answer to the wrong question carries authority the question never earned. Conducting AI uses the statistician's name for this, the error of the third kind (Allyn Kimball's phrase, 1957): a right answer to the wrong problem.

Why not ask Claude to frame the problem first? You can, and it will answer at once. What kind of framing comes back? The book's argument is that a system trained to continue text tends toward the common and the likely, so the framing it offers is the modal one. Take that as an argument about tendencies, not a theorem; the practical point survives without it. Every framing rides on an anchor, which the design researcher Jane Darke called the primary generator: a first idea of what this is really about, usually tacit, that decides which solutions you can see. You cannot start without one. If you have not named yours before Claude supplies its own, its anchor becomes yours by default, dressed as neutral analysis. And the audit then comes too late, because you would be checking the output against the framing it already assumes, which is the one thing the check most needs to be independent of.

So write candidates first, and make them differ in what counts as success, not in wording. The book's distinctness test says how to tell: would the two formulations require different solutions even to test? If one solution satisfies both, you have one formulation in two outfits.

Suppose the bounded change is the plus-one regression from Chapter 6: a function should return its input plus one and returns the input minus one. Three candidate formulations: (A) the single failing test, input two, goes green; (B) the declared plus-one behavior is restored without changing anything outside the learner module and its test; (C) the learner can explain the bug. Test them by constructing results.

| Constructed result | A: input-two test green | B: declared behavior, in scope | C: learner can explain |
| --- | --- | --- | --- |
| A patch returning the constant 3, applied without diagnosing the cause | passes | fails (input five gives 3, not 6) | fails |
| A correct x + 1 patch that Claude wrote and you accepted unread | passes | passes | fails |

Row one separates A from B. Row two separates B from C. Three formulations that disagree about whether a result succeeded are three problems. Had all three cheered for the same result, you would have one problem and two rewrites.

Then choose, using a constraint set written before you score anything. The set needs more than feasibility. If every criterion is about cost, time, and buildability, you have built a machine that selects the most tractable framing, which is the one Claude would have picked unasked. The book adds salience (if this is solved, does it address what matters here?) and whose interests the framing centers and decenters.

That last criterion is the values decision, and it sits inside the formulation, not after it. A centers whoever reads the test report. B centers the maintainers and callers of the function. C centers the learner. None centers everyone, so choosing one is choosing whom the plan does not serve, and the plan should say so. "I chose B; it decenters the learner's understanding, which a separate step addresses" is a defended selection. Silence about what was left out is a laundered one.

Claude's part here is real. It can add candidates you missed, find the result that passes one formulation and fails another, and attack your selection. Conducting AI argues that a model cannot certify distinctness in your domain or make the values selection, because both need situated judgment and a name on the decision. I read that as an argument, not a measurement, and the practice does not depend on settling it. Someone answers for centering the maintainer over the learner, and Claude has no name to put there. So write your candidates first, let Claude extend and criticize them, and defend the one you pick, including what it leaves out. Then carry the selection into the objective, scope, verification, and stop fields; if it lives only in introductory prose while the checks measure something else, the plan has drifted from its purpose.

## The eight fields are eight questions

Each field is a place where a decision was made or was not. The reference declares them in one tuple:

```python
FIELDS = (
    "objective", "inputs", "scope", "steps",
    "tools", "risks", "verification", "stop",
)
```

The code can only see whether a name is bound to a value. A reviewer asks the question each name stands for.

| Field | The question it asks | An entry that fills it and does nothing | An entry a reviewer can challenge |
| --- | --- | --- | --- |
| objective | What outcome, stated so someone can tell whether it happened? | Improve the code | Make the supplied failing plus-one regression pass without changing files outside the learner module and its test |
| inputs | What may the work rely on, and where did it come from? | A list of filenames | The files plus the policy that governs the change, with provenance and version |
| scope | What may change, and what must stay untouched? | Be careful | File paths, permitted operations, excluded systems, output destinations |
| steps | What does each step produce, and how would anyone know it finished? | Research | Record the applicable versioned protocol clauses with URLs and retrieval date |
| tools | Which capability, why, and which operation stays under human approval? | Claude Code | The tool, the reason it is needed, the operations it may and may not perform |
| risks | How could this cause harm, error, or misleading evidence, and what does each risk trigger? | There may be risks | A risk tied to a mitigation, an owner, or a stop trigger |
| verification | What observation will support the completion claim? | Review the result | An exact command, an expected invariant, or a source comparison |
| stop | When do we finish, defer, or halt? | Stop when done | Stop after all scoped tests pass and the named reviewer accepts the current diff; halt earlier if an out-of-scope file changes |

Every entry in the third column would pass `missing_fields`. Every entry in the fourth is something a person can disagree with. That is the difference between a field that is present and a field that has a job.

You can hand some of these questions to Claude to draft: the steps, the tools list. Others you answer, because they depend on things no file contains. What the work is for, what you are willing to have touched, which risks you accept, and who decides when to stop are yours. If the plan needs more scope, revise it before action; do not launder the expansion through an implementation detail.

<!-- [FIGURE: Cajal production brief. A complete-looking plan can still be meaningless. Include bounded objective, eight fields, evidence, stop conditions, all-x plan, semantic review. Show the confirmed relationship that presence is not meaning or authority. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![A complete-looking plan can still be meaningless. presence is not meaning or authority.](../images/10-planning-before-acting-fig-01.png)
*Figure 10.1 — A complete-looking plan can still be meaningless*

## What missing_fields actually checks

The first mechanism is one line:

```python
def missing_fields(plan):
    return [field for field in FIELDS if not plan.get(field)]
```

The question it answers is narrow: is each of the eight names bound to a truthy value? For each required name, `plan.get` retrieves its value or returns `None` when absent. Python's truth-value rule then marks absent and other false-valued results as missing. Empty strings, empty lists, zero, false, and `None` all fail this check.

The function does not require a particular type for any field. A nonempty list, string, dictionary, or even an unrelated truthy value can pass. It does not reject extra keys. It does not explain why a value is inadequate. Its output is an ordered list following the FIELDS tuple. The lesson test confirms that an empty plan lacks eight fields. The demo supplies only an objective, so the remaining seven appear as missing. These cases establish completeness checking at the shallow boundary.

The all-x object exposes the semantic limit. Every lookup returns a nonempty string, so no field is missing under this function. The result is correct for the implemented rule. Calling the plan meaningful would add a judgment the code never made. That blindness is also the check's value: it is deterministic and cheap, and it fails differently from a reviewer, since it never gets tired and never notices meaning. Use it to clear the easy failures so that human attention goes to the hard ones. It is the pattern from earlier chapters: a strict format validator can pass false content, a permission flag can be true without authenticating a person, and a plan-presence checker can pass empty language. Keep the signal narrow instead of expecting one empty list to certify the artifact.

A richer validator could require steps to be a nonempty list or verification to contain a command. That catches more structural defects. It still cannot decide whether the command tests the right claim or the objective serves the right person.

## Dependencies are directed obligations

Steps are not a list. They are a graph, and each arrow is an obligation. If step verify has `after: [build]`, then build must appear before verify: verify may not be called ready until build has produced what verify needs. You decide which arrows exist. The function can only order the arrows you declared.

```python
def order(steps):
    graph = {}
    for step in steps:
        if step["id"] in graph:
            raise ValueError("Duplicate step")
        graph[step["id"]] = set(step.get("after", []))
    if any(deps - graph.keys() for deps in graph.values()):
        raise ValueError("Unknown prerequisite")
    result = []
    while graph:
        ready = sorted(key for key, deps in graph.items() if not deps)
        if not ready:
            raise ValueError("Dependency cycle")
        for key in ready:
            result.append(key)
            del graph[key]
        for deps in graph.values():
            deps.difference_update(ready)
    return result
```

The function first constructs a graph mapping every step id to a set of prerequisite ids. It rejects duplicate identifiers because one key could not unambiguously represent two steps. It then rejects dependencies naming ids absent from the graph. These validations matter because a missing prerequisite is not a cycle. If verify depends on test but test is absent, the plan references nonexistent work. If two present steps depend on each other, neither can become ready. The remedies differ.

The ordering loop finds all entries whose prerequisite sets are empty. These are the ready steps. It sorts their ids for deterministic output, appends them to the result, removes them from the graph, and deletes their ids from the remaining prerequisite sets. It repeats until the graph is empty. If the graph remains nonempty but contains no ready step, the remaining dependencies contain a cycle, and the function raises `Dependency cycle`. A self-dependency is the smallest example and appears in the tests.

The research example gives inspect no prerequisites, build after inspect, and verify after build. The resulting order is inspect, build, verify. The function does not run the steps or establish that their descriptions are useful. When several steps are ready at once, alphabetical id order decides which appears first within that batch. That convention is not evidence that alphabetical execution is best; it says only that, under the supplied relations, those steps do not depend on one another.

## Acyclic does not mean executable

The graph answers one question: is there an order in which every declared prerequisite comes first? It is silent on whether the declared prerequisites are the real ones.

Give three steps the ids a, b, and c with no dependencies. The function returns them in sorted order. It has no knowledge of what each step requires in the world. An omitted dependency can make the graph acyclic while the work remains impossible in that order. A step can also depend on a predecessor whose output is too vague to use: "review after build" is structurally coherent, but the reviewer needs a diff, test results, and acceptance criteria. An arrow says one step comes after another. It does not define the handoff object.

A plan can also be unsafe and acyclic. Inspect, delete, verify is a valid ordering if represented without a cycle. The graph has no operation allowlist and no approval model. Semantic review must compare each action with scope, authority, and consequence. Planning before acting therefore does not mean automatically executing any valid graph. The plan creates a review surface, and it should expose the proposed action early enough that a person or a runtime boundary can reject it.

Do not "resolve" every cycle by removing an edge. A cycle can reveal that two steps were poorly defined. If implementation needs review and review needs a completed implementation, one overloaded word is doing two jobs. Plan review approves a proposed method; result review evaluates actual output. Rename the obligations and the sequence appears: plan review, then implementation, then result review. Ask what each step actually needs as input before touching an arrow.

## Evidence belongs on the edges

The graph tells us when a step is eligible to begin. It does not say what the earlier step must hand over for the later one to rely on it. That is the handoff condition, and Computational Skepticism's chapter on delegation makes it the load-bearing clause of a delegation map. Its claim: delegation is a contract, not a partition of labor, and the contract's handoff condition must be testable. Testable means someone who did not build the pipeline can read the condition, observe the system, and decide whether it holds. "Reviewed" and "reasonable" fail that test: five reviewers will do five different things and all call it reviewing. The procedure is plain: write the condition, circle every interpretive word, replace each with a criterion, then hand it to someone who did not write it and ask them to apply it to a sample case. If they cannot decide, go again. "Looks good" is not a handoff condition.

Take the running hypothetical, the symlink plan, spelled out in full in the gate section below: add one denial test to the Chapter 5 learner permission function through the steps inspect, fixture, test, run, review. For the `run` to `review` edge, the handoff can require the exact commands, exit statuses, output, and a current diff hash or version description. The reviewer can then determine whether the checks correspond to the proposal. For `fixture` to `test`, it can require resolved paths proving that both locations are disposable and that the destination lies outside the approved subdirectory while remaining inside the temporary parent. This lets another student predict what the test exercises.

Notice who produces the evidence. On the `run` to `review` edge, the exit status and output come from the test runner. Claude's sentence about them is not that evidence: an AI describing its own check is the first opinion run twice. An edge needs something that fails differently from the thing it certifies. Chapter 11 builds this out. An edge should also define failure behavior. If the targeted test fails, do not proceed as though review means approval; return to implementation or stop pending diagnosis. If source authorization is missing, do not improvise a replacement input.

Which edges need the most? Use Computational Skepticism's five Boondoggle questions as a sorting heuristic: how cheap is the output to verify, what does being wrong cost, is this an ordinary input or a tail case, can the action be undone, and will the step leave a trail you can review? Here reversibility and the trail do most of the work. If the learner workspace is under version control, a new test can be reverted from the diff, so its edge needs evidence but not a human gate. A command that writes outside the fixture, or deletes, cannot be reverted from a diff, so it gets a hard human approval or it falls outside the scope. Attach evidence to state-changing edges first. A fluent sequence diagram cannot make an unsafe transition acceptable.

One more caution from the same chapter. In its two-team scenario, the team whose documentation specified each handoff could be reviewed on substance, while the team that wrote "the loan officer reviews" was tabled because nobody could say what its pipeline did. A clear map can be reviewed. That does not show the decisions inside it are good.

## Stop conditions and refusal paths

Many plans describe how to continue and leave stopping to intuition, which invites repeated activity, scope creep, and unsupported completion claims. Chapter 4 showed why a turn budget and a finish action answer different questions. The stop field answers a third: who decides, on what evidence, that the work is over or must not continue?

Structure it as three exits. Completion names the observable task outcome: for code, a targeted regression, existing tests, and a reviewed diff; for a document, required sections, source checks, and a named decision. "When it looks good" is not an exit. Halt names the conditions under which action stops before completion: out-of-scope files, missing authorization, restricted inputs, a failed independent check, an unresolved dependency. Defer is what a resource budget produces. A time or turn limit bounds effort without proving success, so reaching one yields an incomplete status, never a fabricated final result, along with the partial artifacts to preserve and who decides whether to resume.

Each exit needs an owner. An automated test can halt on a failing assertion. A person must decide whether a newly discovered risk changes scope. Do not hand a human decision to Claude because it can summarize the evidence well. A summary is not a decision with a name on it.

A plan written only for success pressures every observation into forward motion, so add refusal paths for missing authority, unavailable evidence, out-of-scope changes, and failed checks. Refusal here means the workflow preserves its state and reports what blocks the next transition. In the symlink plan, a resolved target outside the disposable parent is a hard stop, not a reason to continue cautiously. A required edit to the course reference instead of the learner copy is a scope stop. A failed existing test routes back to diagnosis, not to approval. Missing evidence can get a narrower response: if a source cannot support a claim, shrink the claim or mark it unresolved. Do not fill the field with plausible language to satisfy a completion checklist.

Refusal needs outputs: why the step stopped, what evidence was available, and what decision would allow safe resumption. An unexplained halt is hard to tell from a crashed workflow. Not every uncertainty is a block. Missing information obtainable within scope differs from a decision that needs new authority; Claude can help search approved sources or propose a smaller task, but it cannot grant permission the user or the institution has not given. If the same check fails with no new evidence, the next step is not an identical retry: route to diagnosis, revise the plan, or defer. Activity becomes progress only when it changes the evidence or the decision state.

Two more resources bound a plan. Label any optional live API call separately and require explicit authorization; this chapter's offline work needs none. Human attention is the other: a plan that produces hundreds of review items without prioritization is structurally complete and practically unauditable, so state what needs human judgment. A deadline can justify a reduced objective; it does not make skipped verification acceptable without disclosure.

## Review before action: a plan predicts, a result records

A plan is a set of predictions. The steps predict what will be done, the verification field predicts what you will observe if it worked, and the stop field predicts which events end the work. A result is a record of what happened. They are different documents, and the habit worth building is keeping them apart. Write the prediction first and date it. Write what a wrong outcome would look like before you read the result, and do not revise that note afterward. The gap between plan and record is what you learn. If the plan is edited after the run to match the run, it has become a description of the result, and the review that justified acting is gone.

Review the plan against itself first. Eight plausible fields can contradict one another, and cross-field review is how they become one argument rather than eight paragraphs.

- **Objective against verification.** Does the check measure the outcome the objective names? A test that confirms a file exists does not establish that its contents implement the behavior. If the check is a proxy, name what it can and cannot reject.
- **Steps against inputs, tools, and scope.** Every step needs information it is authorized to use. If no step writes, a write-capable tool is unnecessary; if a step needs a capability the tools field lacks, the plan is infeasible. An available tool can still be forbidden for this task: capability does not create authority.
- **Risks against mitigations, owners, and stops.** State which risks are accepted, which trigger a mitigation, and which trigger deferral. Do not assign ownership to a fictitious human or use Claude as the signer of a human decision.
- **Edges against handoff objects.** If review depends on run, what exactly does run produce? A bare id relation gives order without correspondence.
- **Final scope against revisions.** A late change to the objective can invalidate earlier risk and verification analysis. Preserve versions and rerun the relevant review rather than keeping stale supporting fields. This is the not-waterfall rule in practice: reopening the plan is a normal event with a recorded reason.

Then attack it with counterexamples. For each important field, imagine a plan that satisfies its wording but fails its purpose. The all-x fixture is the extreme version; realistic counterexamples resemble plans people accept. An objective can be specific but wrong for the stakeholder. Verification can be executable but test a proxy. Scope can be precise but authorize too much. Risks can be detailed but disconnected from action. A stop condition can be observable but trigger only after harm has occurred.

Write one counterexample before approval and ask whether the plan rejects it. For source grounding, construct a valid citation that does not support the claim. For safe writing, construct an in-scope path with an unapproved operation. Counterexamples also improve dependency design: find a state where prerequisites are technically complete but the receiving step lacks a needed artifact, and add the handoff condition, not another arrow.

Claude generates counterexamples quickly and in volume, and that work is worth handing over. It has no stake in the outcome. Which counterexamples are plausible here, and which risks deserve load-bearing checks, is your call, and you preserve the rejected ones too when their dismissal reveals an assumption. Keep the original counterexample beside the revised plan, or the final version will look inevitable and hide the failure it was built to stop. This is a pre-mortem with executable consequences. It does not prove the plan cannot fail. It shows that identified failure modes shaped the design before the system acted.

## The gate: a reviewed plan, before Claude implements

This is the chapter's gate, the large version of the one you wrote in Chapter 1. There it was an experiment contract. Here it is the plan for a piece of work, plus the condition that must hold before the plan goes downstream into implementation. Write it before Claude changes anything.

Here is the running hypothetical as the plan you would write, with the decider named on each line. It is constructed; Claude did not produce it.

```text
Gate: plan for one denial test in the learner permission function

Field         Decided by              Entry
objective     me                      Demonstrate rejection of an outside-pointing symlink
                                      in a disposable fixture, without accessing unrelated data.
inputs        me, checked by me       Learner code, existing tests, pathlib documentation,
                                      a temporary-directory fixture.
scope         me                      May change: the learner test file; the learner
                                      implementation only if evidence requires it.
                                      May not touch: the course reference, real personal
                                      files, institutional settings, publication.
steps         Claude drafted,         inspect -> fixture -> test -> run -> review, each
              I revised               after the one before it.
tools         me                      Python, Claude Code for review assistance, the local
                                      test runner. No direct API call.
risks         me                      Targeting a real file; reporting a stable fixture as
                                      race resistance; editing the reference. Mitigations:
                                      temporary directory, explicit path inspection, diff
                                      review.
verification  me                      The new targeted test, the existing learner tests, and
                                      confirmation that only allowed files changed.
stop          me                      Finish when the fixture demonstrates the rejection,
                                      existing tests pass, the diff stays within scope, and
                                      the report limits its claim to the stable preflight
                                      case. Halt if any command targets material outside the
                                      disposable arrangement or scope must expand without
                                      review. Defer, keeping partial artifacts, if a needed
                                      source is unavailable.
predicts      me, dated before run    The new test passes, the existing tests still pass, and
                                      the diff lists only allowed files. A failing existing
                                      test or an out-of-scope file in the diff means the plan
                                      was wrong, and it reopens.
```

Encode it as a dictionary and run `missing_fields` and `order` on it, and both pass: the order is inspect, fixture, test, run, review, and the missing-fields result is the same empty list the all-x plan produced. Same output, different plans, and the only thing that separates them is the review this chapter describes. The plan can still be wrong, since the learner code may differ from the reference or the documentation may have changed. The improvement over all-x is not longer prose; it is that another person can predict the actions and challenge the evidence.

The plan is cleared to go downstream, and only then, when all of these hold:

1. The objective was chosen from at least three candidates that pass the distinctness test pairwise, and the plan names one interest the choice leaves out.
2. `missing_fields` returns an empty list and your cross-field review found no field contradicting another. Neither alone is enough.
3. `order` returns an order, and every state-changing edge carries an evidence condition a stranger can apply and a failure route.
4. The stop field has completion, halt, and defer exits, each with an owner.
5. You wrote one counterexample before approval and the plan rejects it, or you revised the plan until it did.
6. A named person has approved it, with a date. If nobody has, the status is pending and nothing consequential runs.

Item six is not Claude's to fill. Approval is a person's act, and a sentence from Claude saying "approved" records nothing. The gate also does not freeze the plan. It fixes the version Claude implements against. A result that contradicts the plan reopens it, and the revised version goes through the gate again.

## Build It: the baseline that lets you audit the plan

You will conduct Claude Code against this plan, and you cannot audit an ordering you have never computed. So build the mechanisms first, as in Chapter 1. Implement `missing_fields` and `order` in your learner workspace before you open the reference. Read the [six tests](../lessons/10-planning-before-acting/code/tests/test_main.py) first and predict the results for empty order, dependency order, self-cycle, unknown prerequisite, duplicate id, and empty plan. Your version is the baseline: the record of what you understood before Claude touched anything, and the instrument you will measure its version against.

Then push on the seams the tests leave open.

- Add the all-x case and explain why it passes the presence function. Then hand its `steps` value to `order` and predict the result before you run it. The presence check passed the plan; the ordering function may not be able to read it. Two checks, each correct under its own rule, neither responsible for the other's assumptions.
- Add a semantically meaningful plan with one omitted field, then revise it. Preserve the validation failure and your human revision in the artifact.
- Construct a cycle using overloaded review and implementation steps. Resolve it by identifying distinct inputs and outputs, not by arbitrarily removing the inconvenient edge. Run both graphs and preserve the error and the valid order.
- Pass an `after` value as a bare string such as `"build"` instead of a list. Predict the error, run it, and say whether its message points at the real cause.

## Use It: conduct Claude Code against the plan

Now hand over the work Claude is good at, in the order that keeps your decisions yours.

First, do the formulation work yourself: three candidates, the pairwise results, the selection, and the interest it leaves out. Then give Claude Code the bounded objective and the exclusions, and ask for a plan in the eight fields, saying explicitly that it should change no file yet. What returns is a proposal.

Second, review it as a stranger would. Run your own `missing_fields` and `order` on it. Do the cross-field review and the counterexamples. Ask Claude to critique your version of the plan and to propose counterexamples, then check each criticism against the plan and the code yourself. Claude's account of why it chose a step is a story about the system, not a trace of it, as Chapter 1 argued. Judge the plan by what it commits to, not by how well it is argued.

Third, only after the gate passes, let Claude Code act on the approved version one step at a time, and hold it to the plan. The stop conditions are now what you check its diff and commands against; if a halt condition fires, the plan stops there and the record says so. Preserve the actual transcript: your prompt, the plan, each revision, the diff, the commands and outputs, the date, and the displayed model label. If Claude Code is unavailable, label the plan as your constructed artifact and record that the session did not run. Do not invent its output or an approval.

Compare the plan with Anthropic's [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) and [Claude Code best practices](https://code.claude.com/docs/en/best-practices), checked during research. Use their workflow and planning guidance to sharpen your architecture, not to attribute this eight-field checklist to Anthropic.

## Ship It: the reviewed plan

The artifact is the reviewed plan. The [artifact brief](../lessons/10-planning-before-acting/outputs/artifact-brief.md) asks for the proposed plan, validation failures, human revisions, stop conditions, and the final approved scope. Preserve versions rather than replacing the initial proposal. Include the field-validation result and the dependency order, but not as semantic approval. Add a review table with objective fit, source and tool boundaries, risk ownership, evidence, handoff conditions, and decision status. Record who proposed each change and who owns authorization: Claude can draft and critique; the human approval the artifact records has to come from a person. If approval is pending, the plan remains pending. Attach one evidence condition and a failure route to every state-changing step, and end with a stop condition another reader can apply without guessing what done means.

**The sign-off.** End the artifact with a statement you could put your name to. Claude can draft its words in seconds and they will be fluent, so write it from your record. This is the template, not a signature.

```text
Sign-off — reviewed plan
Checked:      the missing_fields and order results; which fields I cross-checked
              against which; the counterexamples I wrote and whether the plan
              rejects them
How:          by hand / by tests I wrote before reading the reference /
              with Claude as critic (say which of its criticisms I verified myself)
Not checked:  whether the objective serves anyone outside my own reading of the
              task; cases I did not imagine; anything that happens after the plan runs
Not claiming: that the plan will succeed, that it is safe beyond the disposable
              fixture, or that Claude's critique found every flaw
Signed or withheld: ____________  (name, date); approved for the stated scope /
              returned for revision / withheld
```

This is a sign-off on a plan, so its claim is smaller than a result's. It says the plan survived the review described. It cannot say the work succeeded; Chapter 11 writes the sign-off that can, from the record of what ran. As in Chapter 1, the "Not checked" line does the work, and withholding is an honest result when the evidence does not support signing.

**The driver's seat.** This is how the chapter's work divides, task by task. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Framing the problem | Add candidates you missed; find a result that passes one formulation and fails another | Write your candidates first, certify they differ in your context, select one | Selection centers some interests and decenters others, and someone must answer for that |
| Drafting steps, tools, and order | Draft them and run the ordering | Build `missing_fields` and `order` yourself first, then revise the draft | You cannot audit an ordering you have never computed |
| Evidence conditions on edges | Propose candidates | Apply the stranger test; mark who can apply each | A condition only its author can apply is not yet a handoff |
| Counterexamples | Generate many, fast | Judge which are plausible here; keep the rejected ones | Plausibility depends on context the plan does not contain |
| Approval, wider scope, stopping on a new risk | Summarize the evidence | Decide and record it | Authorization is a person's act; a summary is not a decision |

Record, in the artifact, one task you delegated and one judgment you retained, and point to the evidence: the formulation you declined and what it would have served, a counterexample Claude proposed that you rejected and why, the approval line only you could write. If the transcript shows Claude choosing the objective and you ratifying it, the split ran the other way; say so.

## Verify and reflect

Run the demo, the lesson tests, the all-x counterexample, and your graph cases. Name which claim each check addresses, and trace each error to duplicate, unknown dependency, or cycle rather than saying ordering failed generically. Review every field for meaning, authority, and evidence, and preserve at least one unsafe or useless plan that still passes the structural checks. Check whether your graph omits real dependencies or invents unnecessary ones. Parallel readiness in the function means no declared dependency, not proof that concurrent execution is safe.

Finally, compare your initial and revised objectives. Name the decision that changed and which interest or piece of evidence moved it. Planning is valuable when revision happens before the cost of action, not when it merely predicts the steps you already took. Then reflect locally: which distinction did you collapse before this chapter? Presence and meaning? Order and executability? Valid and authorized? Name the input that separated them again.

## Assessments — ungraded practice

These Assessments carry no points. Use the paired lesson's [knowledge check](../lessons/10-planning-before-acting/quiz.json), preserving initial answers before explanations.

### Warm-up

1. **Eight fields — introductory; objective: identify omissions.** Run an empty and a one-field plan, predict the ordered missing list, and explain the truth-value rule. Name one missing field you would never let Claude fill in for you, and say why.
2. **One edge — introductory; objective: order dependencies.** Order build after inspect and explain the directed obligation. Write, in one sentence a stranger could check, what verify needs from build.
3. **Three errors — introductory; objective: distinguish graph failures.** Construct duplicate, unknown-prerequisite, and cycle cases and map each to its check. Add a bare-string `after` and explain why the error it raises misleads.

### Application

4. **All-x plan — intermediate; objective: critique structural validity.** Reproduce the empty missing list and identify why every field still fails semantic review. Write your prediction of what `order` does with the plan's own `steps` value, then run it.
5. **Observable stop — intermediate; objective: revise completion.** Replace "stop when done" with completion, halt, and defer conditions for a bounded task, and name who decides at each exit.
6. **Evidence-bearing edge — intermediate; objective: design a handoff.** Add an output, a checker, and a failure route to one dependency edge. Hand the condition to another student; wherever they cannot decide whether it holds, rewrite it.
7. **Resolve the review cycle — intermediate; objective: refine steps.** Split overloaded review into plan review and result review, then rerun ordering.

### Synthesis

8. **Reviewed plan — advanced; objective: integrate scope and evidence.** Produce all eight meaningful fields, the graph, validation results, revisions, and the pending or actual decision, ending with the sign-off. Mark which fields you wrote and which Claude drafted.
9. **Unsafe but valid — advanced; objective: reject a plan.** Construct an acyclic, field-complete plan that exceeds authority. Give specific rejection reasons, and say which check in this chapter could never have caught it.

### Challenge

10. **Distinct formulations — stretch; objective: evaluate objectives.** Write three objectives and a result that passes one but fails another. Defend the selected formulation and name the interest it decenters. Then ask Claude to attack the choice, and record which objections you accepted and why.
11. **Parallel-ready conflict — stretch; objective: expose omitted constraints.** Build two steps with no graph dependency that compete for a resource or authority. Add the missing constraint without claiming every parallel pair is unsafe.

## What you can now defend

Every plan remains a proposal until its responsible review and authorization are actually recorded.

You can explain the exact boundary of a field-presence check and why an empty missing list does not certify plan quality. You can trace deterministic topological ordering and distinguish duplicates, unknown prerequisites, and cycles.

And you can say what the three jobs look like in a plan. You conducted: you chose the problem from candidates that disagreed about success, wrote the plan and its gate before Claude changed anything, and put evidence on the edges and owners on the exits. You checked: you treated the plan as a prediction, wrote a counterexample before approval, and refused to let a structural pass stand in for a meaningful plan. You drove: you let Claude draft and attack, kept the objective, the values inside it, and the approval, and signed or withheld.

Most importantly, you can review the objective before optimizing the sequence. A flawless graph can execute the wrong problem. Planning earns its place when it makes that mistake visible before action.

## A plan predicts action; a result records it

Chapter 11 follows one planned tool request through validation, dispatch, result association, and independent checking. A plan says what should happen. A tool result supplies evidence about what did happen. The final answer must not skip that chain. Carry the reviewed plan forward as the prediction against which Chapter 11's record is read.

## Anthropics

Compare the dependency graph with [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) and the bounded workflow with [Claude Code best practices](https://code.claude.com/docs/en/best-practices), checked 2026-09-06. Explain whether the task needs a fixed sequence or model-directed choices. The eight fields remain this course's review instrument.

## Computational Skepticism

The companion's handoff condition asks what testable evidence permits work to cross an edge. See [Delegation and handoffs](../docs/computational-skepticism.md#delegation-and-handoffs). The body applied its standard, that a stranger can decide whether it holds. The chapter adds a refinement the body has not used: testability is graded. Some conditions any non-author can apply; others only a qualified reviewer can, such as whether a cited clause really governs the change. Mark each edge condition in your plan with its tier, and say so in the artifact. A condition only its author can apply has not yet become a handoff condition. An acyclic graph orders work; it does not make the handoff trustworthy.

## Conducting AI

Use the [distinct reframings](../docs/conducting-ai.md#distinct-reframings) practice before planning. The body used the distinctness test and the constraint set. The book's Chapter 7 also offers three moves for producing candidates that really differ: zoom out until the original metric becomes a symptom, zoom in on a load-bearing sub-case, and change the actor by asking whose constraint actually binds. They are the book's own scaffolds, not cited research, so subject every output to the distinctness test. Apply the third to your plan: is the binding constraint the test, the function, or the caller's expectation? The appendix adds a companion check: mark every constraint in your scope field as real or assumed, and test one you suspect is assumed. If none ever turns out to be, you are not looking.
