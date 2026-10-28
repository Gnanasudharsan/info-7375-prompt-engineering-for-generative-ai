# Chapter 6 — Claude Code and diff review
*The patch is small. The claim attached to it may not be.*

Suppose a function should add one to its input. The current version subtracts one. A proposed patch makes the visible regression test pass, and the changed line looks pleasantly short. There is only one problem: the patch returns the constant three. It works for the test input two and fails for five. Nothing about the patch's size reveals the defect. Nothing about one green test proves the intended rule has been restored.

This is not a story about a real Claude Code failure. It is a constructed comparison executed against the course's offline review exercise. For inputs two and five, the old function `x - 1` returns one and four. The inadequate patch returns three and three. The intended `x + 1` patch returns three and six. The exact results are preserved under `chapters.06` in the [research output](../research/worked-examples.json). The same research run also shows that the review function rejects a proposal when its approval flag is false.

Look at what the recipe got right. The defect was reproduced, a test was written, a patch was proposed, the test passed, and the diff was small. Every step was performed, and the claim still does not hold. So the question for this chapter is not "what are the steps of a code review?" It is: **what did the green test actually test, who decided that, and when?** A test written after the patch, to fit the patch, is a retrospective blessing. A test that Claude writes alongside its own patch shares an author with the code, and so shares whatever that author misunderstood. The requirement was supposed to come first, and it was supposed to come from you.

Chapter 1 named three jobs that stay with you when Claude does the fast work: conduct, check, and drive, each with a device (the gate, the sign-off, the driver's seat). Chapter 5 established that an authorized path can still receive a bad change. This chapter moves from the file boundary to the content boundary, where the three jobs meet code you did not write. Claude Code can read a repository, propose a plan, edit files, and run commands faster than you can read the result; do not compete with that. Conducting it means the reproduction, the regression test, and the scope exist before the patch does. Checking it means you write down what you suspect before you run the check, and let the evidence, not the last sentence of Claude's report, decide between accept, revise, and reject. Driving it means the scope decision and the merge are yours.

Two observations from the research run belong together. Tests can expose behavior, but a Boolean saying checks passed does not execute them. A human approval field can be required, but a Boolean saying approved does not authenticate a person. Our job is to understand exactly what the lesson's review function returns and what evidence must exist outside it.

The paired workflow assumes Claude Code through your course or personal account. Enrolled Northeastern students should begin with the university's [Claude portal](https://claude.northeastern.edu/) and the repository's [access guide](../docs/neu-claude-access.md); public readers need their own Claude Code-enabled account. The core Python example runs offline and requires no direct API credits. If you use Claude Code to propose a patch in a disposable repository, preserve the actual plan, diff, commands, and outputs, and do not replace an unavailable or failed session with invented dialogue. A review packet is worth more than a seamless story that conceals what did not run.

## What you will be able to do

By the end, you should be able to explain a unified diff as changed behavior rather than decoration, write a regression test that distinguishes an intended rule from a convenient constant, and trace every reason returned by the review function. You should be able to write the reproduction, the test, and the scope list before Claude proposes a patch, and say why that order matters.

You should also be able to do three things the rest of the book builds on. Before running a check, record a verdict, a target, a suspected mechanism, and what would change your view, and keep that record intact. Defend an accept, revise, or reject decision with executed checks and scope evidence, each verb in your summary matched to its evidence. And say which parts of the review you handed to Claude, which you kept, and why.

You need Chapters 4 and 5, basic Python functions, unit tests, and the idea of before-and-after file content. The paired [lesson](../lessons/06-claude-code-and-diff-review/docs/en.md) supplies the runnable sequence and existing knowledge check. Begin in your learner workspace: write the failing behavior and your prediction before asking Claude for a patch, so the proposed implementation cannot redefine the problem you intended to solve.

## Whose test is it? Reproduce before you repair

The first decision is not about the patch. It is about the evidence you will accept for a patch, and it has to be made while no patch exists, because a patch shapes how you see the problem the moment you read it.

A bug report such as "the result is wrong" is too weak to guide a bounded change. It names no input, expected result, observed result, or scope. The first useful artifact is a reproduction: the smallest legitimate case that shows the gap between intended and current behavior.

For our constructed function, state the rule in plain language: return the input plus one. Choose at least two inputs before seeing a patch. With two and five, the expected results are three and six. The old implementation returns one and four, so both cases demonstrate subtraction rather than addition. The pair is more informative than either case alone because it makes a constant replacement easier to detect. Reproducing a defect is not the same as proving its cause: observing `old(2) == 1` contradicts the stated requirement, and reading the source reveals the `x - 1` expression. Keep behavior evidence and inspection evidence apart in the packet.

Now the order. Write the regression test before the proposed fix. The reason is provenance. A test written after you have seen the patch is shaped by it: you check the cases the patch handles and take the expected values from what it returns. A test that Claude writes alongside its own patch has a subtler problem: the two share an author, so a misunderstanding of the requirement sits on both sides of the comparison and cancels out. A test written first, by you, from the rule, is still your design and can still be incomplete. But it represents the expected behavior instead of a retrospective way to bless a patch, and when the patch arrives, the patch is what is on trial.

Three candidates make the point concrete. Build them in a disposable learner file:

```python
def old(x):
    return x - 1

def inadequate_patch(x):
    return 3

def intended_patch(x):
    return x + 1
```

Before running them, predict the output for inputs two and five. These exact outputs were executed in the research pass, not reconstructed from memory.

| Input | Expected (plus one) | `old` | `inadequate_patch` | `intended_patch` |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 3 | 1 | 3 | 3 |
| 5 | 6 | 4 | 3 | 6 |

Now imagine a regression test containing only `assert candidate(2) == 3`. Both candidate patches pass. A packet that records only that command supports the claim that the candidate returns three for input two, and no more; the case did not separate the intended function from every wrong one. Add input five and the constant patch fails. The pair still does not prove correctness for all Python inputs, but it rejects the demonstrated constant repair.

<!-- [FIGURE: Cajal production brief. A second input separates two passing patches. Include old x−1, constant 3, intended x+1, input 2, input 5. Show the confirmed relationship that one test cannot distinguish both implementations. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![A second input separates two passing patches. one test cannot distinguish both implementations.](../images/06-claude-code-and-diff-review-fig-01.png)
*Figure 6.1 — A second input separates two passing patches*

The review habit is to ask which different implementation could pass the current test. One plausible counterexample is enough to show that the evidence supports a narrower claim than "the bug is completely fixed." Even the two-input test leaves open which input types are supported, what happens at boundary values, and whether this function belongs to a larger invariant. The exercise supplies no complete specification, so do not invent one: state that the selected checks cover the declared integer examples and the transformation they illustrate.

### The gate: reproduction, test, and scope, before the patch

This is the chapter's gate. In the vocabulary of *Conducting AI* it is a phase gate: a specific, testable condition that must hold before the output moves downstream. It is also the part of the work Claude cannot do for you, because the gate is where your understanding of the requirement goes on the record. Write it before you ask Claude for a plan, and name who decided each item.

*Design.* The rule is: return the input plus one, for the declared integer examples. The reproduction inputs are two and five, with expected results three and six. The allowed files are `app.py` and its learner test file. These are my choices for the constructed exercise; no model produced them. In your own repository they are yours.

*Contract.* The regression test fails against `old` on both inputs. It passes against `intended_patch` on both. It fails against `inadequate_patch` on input five. Nothing outside the allowed list changes unless you widen the list deliberately, on the record.

*The stop condition.* The patch does not move downstream until the test was saved before the plan (a file timestamp or a commit will show it), the plan names only allowed files, and the test and existing suite have been run against the current diff, with commands and exit status recorded.

*A wrong version your tests must catch.* The constant three. Also a patch that gets the arithmetic right while editing an unrelated configuration file. If your test and scope check cannot tell these from the right patch, the gate is not finished.

*What a failure looks like.* One sentence, dated, about what a wrong patch would look like in the test output. If you write it after reading the output, you have described the output, not tested your understanding.

*What this packet may claim.* Behavior on the declared integer examples, and scope by filename. It cannot claim the function is correct for all inputs, or that a person approved it.

The gate has a pass condition you can check before any Claude session: run your test against the three candidates. The result should be fail on both inputs for `old`, fail on five only for `inadequate_patch`, and pass on both for `intended_patch`. If it is not, the gate is wrong; fix it before anything else. Claude is good at proposing the input you missed, so let it sharpen the gate. What it proposes, you adopt or reject.

## Read a diff as a behavioral proposal

When Claude Code edits your files, the diff is the thing you review. Its narration of the change is a second-hand account; the diff is the change. The [reference implementation](../lessons/06-claude-code-and-diff-review/code/main.py) uses Python's standard-library `difflib` to produce a unified diff:

```python
import difflib

def diff(before, after):
    return "".join(difflib.unified_diff(
        before.splitlines(True),
        after.splitlines(True),
        fromfile="before.py",
        tofile="after.py",
    ))
```

For the lesson's simple strings, the recorded output is:

```text
--- before.py
+++ after.py
@@ -1 +1 @@
-return x - 1
+return x + 1
```

The leading minus and plus lines are change notation, not arithmetic performed by the diff. The diff reports a textual transformation; the reviewer connects it to expected behavior. A useful review explains the changed expression: replacing subtraction with addition changes the rule from one below x to one above x. That explanation transfers across inputs. "The plus sign looks right" does not.

Be exact about what the diff is evidence of. It shows what text differs between two supplied strings. It does not prove either string was loaded from the intended repository file, it does not run the code, and it does not show untracked changes omitted from the comparison. In an actual Claude Code workflow, record the command and scope used to inspect changes and connect the displayed diff to the working tree you are reviewing. Small diffs reduce what a reviewer must read, but small is not safe: a one-character operator change can alter every call. Review effort should follow behavioral consequence and uncertainty, not line count.

Here speed stops being an asset and becomes a hazard. Claude can produce a large diff in seconds, and your reading speed has not changed. *Irreducibly Human* names the shape of this: the volume trap. Generation scales with the machine, verification does not, and the gap fills with output nobody verified (see [Review capacity](../docs/irreducibly-human.md#review-capacity) for the passage this course draws on). Reading faster does not close that gap. Shrinking what must be read, and deciding in advance what the reading is for, does. That is what the gate did: a test written first and a short allowed-file list turn "read everything Claude changed" into "read these files, against this test."

## Scope is a testable property, not a mood

The gate made a second decision: which files should this fix need to change? It is a decision about the task, made before the plan, and it is the one on which Claude has the least context. The lesson's `review` function turns "please keep the patch focused" into a comparison:

```python
def review(changed, allowed, checks_passed, approved):
    reasons = []
    if not changed:
        reasons.append("no changes")
    if set(changed) - set(allowed):
        reasons.append("out of scope")
    if checks_passed is not True:
        reasons.append("checks failed or absent")
    if approved is not True:
        reasons.append("human review required")
    return {"merge_ready": not reasons, "reasons": reasons}
```

An empty changed list is rejected. A claimed fix with no recorded file change deserves explanation: perhaps the change was never applied, or the wrong comparison was used. The function names only `no changes`; diagnosis remains outside its aggregation.

The set difference between changed and allowed files exposes any changed name not in the allowed set. It does not inspect line-level scope inside an allowed file: a patch can rewrite unrelated functions in `app.py` and still pass if `app.py` is permitted. Filename scope is useful and incomplete. A renamed or generated file may need a richer representation than a simple list, so in your actual packet preserve the real diff status and explain how it maps to the simplified input.

Do not respond to this limitation by making the allowed list the whole repository; that erases the boundary the check was meant to enforce. If the patch reveals a legitimate dependency outside the initial scope, pause and revise the scope explicitly. Design first does not mean freeze the design: a finding in the patch can reopen an earlier decision. What it cannot do is reopen it silently. Record who widened the list, when, and why, then rerun the checks on the resulting proposal instead of pretending the file was always included.

Scope and correctness can disagree: a perfectly scoped patch can be wrong, and a behaviorally correct patch can include an unrelated change. The review function accumulates every reason so that more than one failed obligation stays visible.

Claude can tell you which files it believes it must touch and why, and the reason may be good. What it has no access to is the rest of your situation: who else depends on that configuration file, what is in flight on another branch, whose name is on the release. Whether the task should grow to include a new file is a decision about what the change is for, and it stays with the person who owns the task.

## Flags are claims about evidence

What does `checks_passed=True` mean? It means the caller said so. The function has no command, output, timestamp, environment, or association between a check and the current diff; the surrounding artifact must supply those. A packet can contain exact commands, outputs, and exit status, and then derive the Boolean for the policy summary. Supplying True by hand in a fixture demonstrates the branch, not that a real check passed.

The same holds for what Claude Code tells you at the end of a session. A final message that says the tests pass is a claim about a run, standing exactly where `checks_passed=True` stands: it carries no command, output, or link to the diff you are about to merge unless you go and get them. Chapter 4 made this point about loops: finishing is not succeeding. A tidy summary is the finish, not the evidence.

The `approved` argument has the same limitation. The function requires literal True. It does not authenticate a reviewer or prove that the reviewer saw this version of the diff. Chapter 13 will bind a simulated decision to a proposal fingerprint, while still refusing to treat a digest as identity. Here the lesson is simpler: a required flag stops the caller from omitting approval, but the meaning of the value depends on the process around it.

The lesson's demo calls `review(["app.py"], ["app.py"], True, False)`, and the research run records the same outcome: `merge_ready` is false, with the single reason `human review required`. That is an executed control-path result, not evidence that a person declined the patch. Conversely, the lesson test supplies True and sees merge-ready when the other requirements pass; that is a simulated input, not a human act. The function aggregates conditions without generating their evidence, which keeps it small and testable and leaves integration to construct trustworthy inputs. A dashboard is only as honest as the records behind its green indicators.

## Audit before you verify

Between reading the diff and running the check there is a step that is easy to skip, and it decides whether the check is worth anything. *Conducting AI* calls it the plausibility audit. Verification consults a source: a test run, a reference, a recomputation. The audit consults none. It runs on your own model of how the thing should behave, and it decides two things: whether a source needs consulting at all, and what the verification should look for. If you find yourself saying "I audited it by running the tests," verification has leaked in. Once the test has spoken, you cannot tell whether your model fired or the test did the work.

The book's Audit-First Protocol has one inviolable rule: render the verdict and name the mechanism before any lookup. A complete audit produces three things, in order. A verdict: does this need verification? A target: what should the verification hunt for ("check the whole thing" is not a target)? A mechanism: why did this output draw your attention, or fail to? The book names two mechanisms, pattern recognition (the shape is wrong, nothing familiar matches) and anomaly detection against a held model (a constraint you know has been violated). It labels that split a teaching scaffold, not an established taxonomy, and I use it the same way. Its value here is the demand that you say why you suspect.

To those three I add a fourth line, taken from the habit *Computational Skepticism* asks of validation writing: state what would change your mind. It commits you to what evidence would count before you see any.

The record is written after you read the plan and the diff and before you run a command against them:

```text
Audit record — written after reading the diff, before running anything
Date and time:         ____________
Verdict:               suspect / proceed / cannot audit (name what is missing)
Target:                what the check should hunt for
Mechanism:             the pattern that is missing, or the constraint it violates
Would change my view:  the observation that would move me
```

Suppose, as a constructed example, the diff shows a function specified as input plus one whose body is `return 3`. Verdict: suspect. Target: behavior at an input other than two. Mechanism: anomaly against a held model, because a function that adds one to its input must return different values for different inputs, and this body never mentions x. Would change my view: a second input returning input plus one, or learning that the rule I wrote down was not the rule the task needed, which would send me back to the reproduction rather than forward to the check. That audit used one piece of knowledge, that the output depends on the input; strip it away and the audit goes silent. It also told you what the test should look for, which is what an audit is for.

The audit has an edge, and marking the edge is part of the audit. Suppose the diff changes how a library call rounds a value and you have never used the library. Your model is silent. The honest verdict is `cannot audit`, with the missing knowledge named, and it routes you to a source, a person who knows, or a narrower claim. What you may not do is let the patch's polish stand in for the model you lack. The book's argument is that fluency and groundedness come from the same process and correlate only by accident, while your instinct, trained on people whose fluency tracked competence, reads them as one signal.

Keep the record. After the run, put the result beside the prediction. If the check agrees, your model is working in this corner. If it disagrees, the gap is the learning: either your model was wrong or the check was aimed at the wrong target. Do not rewrite the record afterward. An intuition is a reason to investigate, not proof of a bug and not permission to skip required checks.

The gate and the audit do different jobs. The gate is written before the patch exists and says what must hold. The audit is written after you have seen this particular patch and says what you suspect about it. Without the gate the audit has no standard; without the audit the gate's checks run without a question.

## Accept, revise, or reject

By now you hold three records: the gate you wrote first, the audit you wrote before running, and the executed checks. The decision follows those, not the last sentence Claude Code printed.

An accept decision should name the version reviewed, the scope inspected, the checks run, and the remaining limitations. "Looks good" hides the basis of judgment. "Accept the x+1 patch for the declared integer behavior after the two regression inputs and the existing suite passed; broader type behavior was not evaluated" gives a reader something to disagree with.

Revise is appropriate when the goal remains valid but the evidence or implementation is insufficient. The constant patch is a clean revise case: it demonstrates the expected result for one input but fails a second case representing the same stated rule. The next action is to change the implementation or narrow the claim honestly, not to broaden approval.

Reject is appropriate when the proposal conflicts with scope, requirement, or risk in a way that should not proceed as presented. An unrelated file change can justify rejection even if the regression passes. Rejection is a decision about the proposal as a package under the current task boundary, not a claim that every line is bad.

These labels are human review outcomes, not values the AI should invent on behalf of a person. Claude can summarize evidence, challenge a rationale, and propose a recommendation. The responsible reviewer owns the decision where the workflow assigns that responsibility.

### Choose the verb the record supports

The sentence you write about the patch is itself a claim, and its verb carries a strength. *Computational Skepticism* freezes one ladder, weakest to strongest: hypothesize, suggest, observe, find, show, demonstrate, conclude, prove. Each verb names a posture and the minimum evidence it needs. Observe is the most defensible verb for a result from one run under stated conditions; conclude means the motivating question is settled, with alternatives considered and rejected. The book's observation is that engineering evidence usually sits between observe and find while the prose reaches for conclude, and it argues that AI-written paragraphs share the pull toward strong verbs. Its remedy is unromantic editing: downgrade the verb until it matches the evidence. The ladder is the author's editorial instrument, not a universal scale of certainty, and I use it that way here.

Suppose a patch summary contains these sentences about our constructed case, with the record that case produced:

| Sentence | Verb | What the record would need | Two-input record |
| --- | --- | --- | --- |
| "The patch returns three and six for inputs two and five." | observe | The command, inputs, and output, run on the current diff | Supplies it, if run after the last edit |
| "The data suggest the patch implements plus one on the declared integers." | suggest | Observations that point toward the rule without ruling out alternatives | Supplies it: two inputs point toward the rule and rule out the constant |
| "The patch completely fixes the bug." | conclude | Alternatives considered and rejected, the input domain covered, the existing suite run, scope confirmed | Does not supply it |
| "The patch is safe to merge." | not a finding | A decision by the named reviewer, with the packet attached | Not an evidence verb; it belongs to a person |

A downgrade is not cosmetic. Replacing "completely fixes" with "the data suggest" can change what a reader does next: a reader of *conclude* may merge, and a reader of *suggest* may ask for one more test. When the verb changes the action, the ladder is earning its keep.

Underneath all of this is a tradeoff between speed and inspectability. This chapter has not established criteria for removing review, and manual review becomes ceremonial when the evidence is weak or the volume exceeds attention. Improve the packet and the scope; do not romanticize either automation or a signature.

## Build It: the baseline that lets you audit

Claude Code can write these functions faster than you can. You build them anyway, because the one thing in this chapter Claude cannot hand you is the ability to read its patch and hear that something is off. That ability comes from having written the candidates, the test, and the policy yourself; *Irreducibly Human* puts it in one line: you cannot audit what you do not know. Your version is the baseline, the record of what you understood before Claude touched anything and the instrument you will measure its version against.

In your learner workspace, before opening the reference, write the three candidate functions and the regression test that separates them, predicting the output table first. Then write `diff` and `review`. Run the lesson demo and its six tests from the repository root:

```bash
python3 lessons/06-claude-code-and-diff-review/code/main.py
python3 -m unittest discover -s lessons/06-claude-code-and-diff-review/code/tests -v
```

Read the six tests as six questions, not as "the code works." Then read them as a reviewer hunting for survivors. Tests 02 through 05 each assert only that `merge_ready` is false; none of the six checks the reasons. Write two wrong versions of `review`: one returns `merge_ready` false for every call, and one reports `no changes` as the reason whatever the failure. Check by hand which tests catch them. The first is caught only by test 01; the second passes all five review tests. That is the chapter's lesson at lesson scale: a green suite reports on what the suite asserts, and the part nobody asserted is the part nobody checked.

Once you can explain your own version, compare it with the reference and name a difference in behavior, not in line count or style.

## Use It: conduct Claude Code against your gate

Now hand Claude the work it is good at. In a disposable Python repository, put your gate where Claude Code can read it: the issue, the reproduction, the failing regression test, and the allowed-file list. Do not hand it your implementation. Then work in this order, and keep each artifact.

Ask for a plan before any edit, and check it against the allowed list. A plan that names a file outside the list is a decision for you, not an assumption for Claude. You may ask it to propose additional test cases before it writes the patch; treat each as a proposal that you adopt or reject, and let the packet record which came from Claude. An adopted test becomes part of the gate. A test Claude writes after seeing its own patch is evidence of what it understood, not an independent check.

Permit a bounded edit. Then, before running anything, read the diff and write the audit record. Only then run the targeted regression and existing tests on the current diff, preserving commands, outputs, and exit status.

Then do three things with the result. Compare its patch with your baseline and name one difference in behavior: a boundary it handled that you missed (a revision to your gate) or one it silently ignored (a defect your test failed to catch). Note which of your tests failed, if any; a failing test is often a gap in your gate that Claude could not see, since it had only what you wrote. And ask Claude to propose a deliberately wrong patch that still passes your tests, then check by hand whether it does. If it does, your tests were too weak, and you found out cheaply. Whether your tests are enough cannot be judged by the system they are testing.

Anthropic's [Claude Code best practices](https://code.claude.com/docs/en/best-practices), checked during research on 2026-09-06, recommends giving work executable checks and separating exploration, planning, and implementation where appropriate. In this chapter those ideas map to concrete artifacts: reproduction, reviewed plan, diff, and test output. The mapping is an adaptation; the toy review function is not Anthropic's runtime.

If the Claude session is unavailable, report that and complete the offline review exercise; do not manufacture a plan or transcript. If a session ran, preserve the actual transcript with the date and displayed model label.

## Ship It: the review packet

The [artifact brief](../lessons/06-claude-code-and-diff-review/outputs/artifact-brief.md) asks for issue, reproduction, plan, before-and-after diff, exact check commands and output, review notes, and merge decision. Arrange these as an argument, not a pile of screenshots. Begin with your gate, dated, then the pre-patch reproduction. Preserve the proposed plan and actual diff, then your audit record. Attach checks to claims by identifying which behavior each command examines. End with the decision, the sign-off, and the remaining gaps.

Record Claude's contributions by named action (plan, code proposal, test suggestion, summary) and your own the same way (reproduction, scope, the test written before the patch, the audit record, the decision). Named actions say more than percentages unless the assignment separately requires an estimate.

### A packet is a chain, not a folder

Putting the right filenames in one directory does not guarantee that the records refer to one another. The issue should identify the behavior the failing test reproduces. The plan should address that issue and respect the allowed scope. The diff should implement the reviewed plan or explain why it changed. The test outputs should come after the current diff, and the decision should name that same proposal. If one link points to an earlier version, the packet can look complete while its argument has broken.

Use identifiers a reader can follow without elaborate infrastructure: a commit hash when a real commit exists, otherwise a saved diff digest or a dated working-tree description. Chronology does not settle correspondence, since a test run after an edit can still target the wrong module, so record the working directory and target. Keep output as searchable text; a pasted green badge without its command tells the reviewer less than it appears to. And retain negative space: list the relevant checks you did not run and the files you did not inspect. For our tiny function, broader types and inputs remain outside the two-number example.

### Keep the failure in the record

An unsuccessful patch deserves the same provenance discipline as a successful one. Record what version failed, which command exposed the defect, and whether the failure belongs to the patch or to the test environment. A syntax error in the harness does not show the candidate is wrong; repair the harness, rerun, and keep both records. Do not delete the evidence once a later revision passes: the move from failure to correction is often the strongest demonstration that the final test matters.

The constant patch in our constructed case is not malicious and need not be called foolish. It is a locally adequate response to one inadequate test, and many review failures arise that way. Whether Claude or a human proposes it, the diagnosis is about code and evidence; attribution matters for the contribution record but does not change what `return 3` does. Review should avoid both automatic deference to AI output and automatic suspicion of it. That is why the chapter says evidence-based rather than AI-proof: the workflow does not prove AI involvement safe in general, only exposes the proposal, scope, checks, and accountable decision so that this change can be judged.

### A worked decision from beginning to end

The issue: for integer input x in the declared exercise, the function should return x plus one but returns x minus one. The reproduction records expected three and six against observed one and four, and the allowed scope is `app.py` and its learner test file.

The first candidate replaces the body with `return 3`. Its diff is in scope and the input-two regression passes, but input five fails because three does not equal six. The decision is revise: the proposal stays within file scope and does not implement the stated transformation. Setting `checks_passed` to True on the first case alone would summarize evidence that does not match the declared behavior.

The second candidate replaces subtraction with addition. Its diff is in scope and both targeted cases produce the expected values. Assume, only as a labeled fixture, that the existing lesson checks also passed. The policy function still returns `human review required` when approved is false, which is correct for the simulated call: evidence is assembled, but no actual person has been represented as deciding. In a real review you examine the current diff and outputs, record the limitations, and make or request the assigned decision. If the responsible human accepts, that event belongs in the record with the proposal version. The book cannot synthesize it in advance, so the example ends with evidence sufficient for a bounded recommendation, not a fabricated signature.

Now change one assumption. Suppose the plus-one patch also edits an unrelated configuration file. The behavior tests can still pass, but the review function adds `out of scope`. The right response is not to ignore the file because the arithmetic is right: inspect why it changed, revert it or revise the scope explicitly, and rerun the checks on the resulting proposal. Change another. Suppose the diff is in scope and the tests pass, but the requirement was never confirmed and the real task needed something else. Plus one can be implemented perfectly and still be wrong, and testing cannot repair an invalid requirement. This is where the last line of the audit record earns its place: when the requirement is in doubt, reopen the gate instead of treating an exact implementation of the wrong rule as success.

### The sign-off

End the packet with a statement you could put your name to. Claude can draft its words in seconds and the draft will be fluent, so write it from your record. This is the template, not a signature:

```text
Sign-off — review packet
Proposal:     the exact diff I reviewed (commit hash, saved diff digest, or
              dated working-tree description)
Checked:      which behaviors, by which commands, on the current diff; scope
              compared with the allowed list I wrote before the plan
How:          by a test I wrote before the patch / by commands I ran after the
              last edit / by reading the diff / with Claude's help (say which parts)
Not checked:  inputs and types outside my cases; behavior outside the allowed
              files; anything that ran before the last edit
Not claiming: that the bug is fixed in general; that Claude's summary is
              accurate; that anyone other than me has approved this
Strongest verb in my summary, and the evidence behind it: ____________
Decision:     accept / revise / reject / pending   (owner, date)
Signed or withheld: ____________  (name, date)
```

The "Not checked" line does the work. It is the line an AI-written sign-off leaves out, because the system that wrote it has no record of what you did not do. The "Strongest verb" line is where the verb ladder lands. If the decision is only your recommendation for someone else, label it as one. If the evidence does not support signing, withholding is an honest result; a sign-off that claims more than the record supports is exactly the failure this chapter is about.

### The driver's seat

This is how the chapter's work divided, task by task. Test your record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Stating the rule and the reproduction | Propose minimal reproductions and edge inputs; run them | Say what the rule is and which inputs count as the defect | The requirement lives in your task, not in the code; Claude can implement a wrong rule perfectly |
| Writing the regression test | Propose extra cases and a wrong patch that survives | Write the test before the patch; adopt or reject each proposal | A test written after the patch tends to bless it |
| Drafting the patch | Plan and implement against the gate, fast | Build your own baseline first; compare the two | You cannot audit what you have not built |
| Setting scope | Report which files it needs and why | Decide the allowed list and every revision to it | You know the callers, the branches, and whose release this is |
| Running checks and summarizing | Run commands, capture output and exit status | Choose which command bears on which claim; record what was not run | A correct output can be about the wrong target |
| Accept, revise, or reject | Summarize evidence; challenge the rationale; flag an overclaim | Decide, choose the verb, sign or withhold | Your name is on the merge |

Record, in the packet, one test case you wrote before the patch existed and one place where you changed or rejected something Claude proposed or summarized. If you cannot point to the transcript line, timestamp, or edit that shows each, the split happened in your head and not in the record.

## Verify and reflect

Review evidence must remain attached to the exact proposal.

Run the lesson demo and six tests, then your added regression, and explain what each result establishes. Inspect the current diff after the checks; a passing test from before a later edit is stale evidence for the current proposal. Put your audit record beside the result. If the check disagreed, say which side was wrong, your model or the aim of the check, and leave the record as written.

Audit every strong verb in the patch summary. Does the evidence suggest, observe, find, show, or conclude? "Completely fixes" is rarely justified by two inputs, and a narrower verb is not timid when it accurately communicates the tested boundary. Ask what test the inadequate patch passed and why, then explain the second input's power: a test should discriminate the intended behavior from a plausible defect.

Finally, inspect approval provenance. If the review function received True only in a fixture, say so. If a person actually reviewed the patch, preserve the decision and version without inventing identity evidence. The reflection worth writing is local: of the three jobs, which did you skip first when you were hurrying, the gate, the audit, or the verb? Name what that would have cost if the patch had been the constant three.

## Assessments — ungraded practice

These Assessments carry no points. Use the paired lesson's [knowledge check](../lessons/06-claude-code-and-diff-review/quiz.json), preserving your answers before viewing explanations.

### Warm-up

1. **Explain the hunk — introductory; objective: read changed behavior.** Generate a unified diff between x-1 and x+1. Explain the removed and added lines without treating diff markers as arithmetic. State one claim the diff supports and one it does not.
2. **Trace every reason — introductory; objective: inspect policy.** Construct separate review calls for no changes, out-of-scope change, absent checks, and missing approval. Predict the reasons list and compare it with execution. Then say which lesson tests would still pass if the function reported the wrong reason.
3. **One green case — introductory; objective: critique coverage.** Show why input two accepts both the constant-three and plus-one implementations. Explain the missing behavioral distinction, and say who should have written the second test and when.

### Application

4. **Second input, written first — intermediate; objective: design a targeted regression before the patch.** Before any Claude session, write the reproduction, a regression that includes an input rejecting the constant patch, and the allowed-file list. Preserve prediction, command, result, and the date you wrote them.
5. **Scope boundary — intermediate; objective: evaluate changed files.** Construct an allowed-file list and an out-of-scope proposal. Explain what filename comparison catches and what unrelated changes inside an allowed file could survive. Say who decides when the list should widen, and what the packet must record when it does.
6. **Audit, then evidence behind True — intermediate; objective: audit before verifying.** Read a small diff and write the audit record (verdict, target, mechanism, what would change your view) before running anything. Then run a harmless check and show how its output supports a checks-passed summary. Explain why manually supplying True without that record proves only the branch.
7. **Stale check — intermediate; objective: recognize version drift.** Run a test, alter the candidate afterward, and explain why the earlier result no longer justifies the current patch. Restore through a new learner edit, not by changing the reference.

### Synthesis

8. **Full packet — advanced; objective: integrate review evidence.** Assemble issue, reproduction, plan, diff, checks, scope, decision, and limitations for a disposable change, and finish it with the sign-off. Mark any Claude contribution and any unperformed step honestly, and record one task you delegated and one judgment you kept.
9. **Revise the claim — advanced; objective: calibrate language.** Find three strong verbs in your report. For each, state the evidence required and rewrite any sentence that exceeds the actual checks. Ask a peer to find one more sentence whose verb exceeds the record; Claude can list the strong verbs for you to examine, but not judge the evidence behind them. Keep the original beside the revision.

### Challenge

10. **A different survivor — stretch; objective: create a counterexample.** Design a wrong implementation that passes your current cases. Add one justified test, then explain what remains untested instead of claiming completeness. Repeat on the lesson's `review` function by finding a wrong version that passes every lesson test.
11. **Richer review record — stretch; objective: redesign provenance.** Propose a record binding commands and outputs to the reviewed diff. Explain what it improves and why it still cannot authenticate human consent by itself.

## What you can now defend

You can reproduce a defect before editing, write the test before the patch exists, and read a diff as a proposed behavioral change. You can explain why two and five together tell us more than two alone without pretending they exhaust the input domain. You can trace the review policy's four obligations: a change exists, changed filenames stay in scope, checks are asserted as passed, and approval is asserted as present. Its Booleans summarize evidence rather than create it, and a final sentence from Claude Code summarizes a run in the same way.

And you can say what the three jobs look like at this scale. You conducted: the reproduction, the test, the scope, and the stop condition were yours and came before the patch. You checked: you recorded a verdict, a target, and a mechanism before you ran anything, and chose the verb the record supports. You drove: Claude proposed and implemented, while you set the scope, ran your own tests, and held the merge. Accept, revise, and reject are review outcomes attached to a specific proposal, task boundary, and evidence set, and you can make one whose strength matches the record.

## Which source material reached the system?

The review packet tells us what changed and which tests ran. It does not explain which information was selected before the change was proposed. A source-grounded task can fail upstream if the relevant passage never entered context, even when the resulting patch is syntactically tidy. That is the audit's edge again: coherence is visible in a diff, but whether the patch is grounded depends on what Claude was given.

Chapter 7 builds a tiny retrieval system. We will turn token counts into vectors, calculate cosine similarity, rank documents, and inspect an omitted synonym case. Then we will ask the question ranking cannot answer: does the selected passage actually support the claim?

## Anthropics

Compare the packet with [Claude Code best practices](https://code.claude.com/docs/en/best-practices), checked on 2026-09-06. Map executable verification, exploration, planning, and implementation to your actual artifacts. Identify which human scope decision remains after every command passes. Do not claim the local `review` function reproduces Claude Code's safeguards.

## Computational Skepticism

The companion's communication chapter treats verb choice as an evidence audit. See [Claims and evidence](../docs/computational-skepticism.md#claims-and-evidence). The body used its ladder; this note adds the chapter's argument for why you cannot run the check on your own summary. You wrote each sentence with the strongest verb that felt true, and the feeling came from how the evidence sat in your head, which a re-read no longer has. The mismatches you made are the ones you cannot see. So hand the summary to a peer and ask for the chapter's specific form of critique: name the sentence, the verb, the evidence that verb requires, and the verb the record supports. "Too strong" is not a critique; "you wrote 'completely fixed' but the record is two inputs on one function, and 'suggest' would match" is. Preserve the original, the revision, and the reason. One caution the body did not give: the ladder flattens inferential caution (suggest) and evidential strength (observe, find, show) onto one line, a trade the author made for usability, and it is why verb ladders wobble.

## Conducting AI

The relevant practice is audit before verification, located through [Audit before verification](../docs/conducting-ai.md#audit-before-verification). The body used the protocol's three parts and its honest limit. This note adds the book's reason for demanding the mechanism and not just the catch: a verdict you cannot explain is one you cannot teach, cannot defend to a skeptic, and cannot trust yourself, because you cannot tell whether you reasoned or merely reacted. Test your own audit record with the book's follow-up question: what specific knowledge made the finding possible, and would a competent generalist without it have caught the same thing? For `return 3` the answer is almost nothing: anyone who knows the rule depends on x catches it. For a rounding change in an unfamiliar library the answer is a great deal, and it tells you who must review that patch and what belongs in the sign-off's "Not checked" line.

Claude can help propose the mechanism and the test. You remain responsible for deciding whether the evidence addresses the actual change and whether the proposal stays within scope. An intuition is a reason to investigate, not proof; a passing command is evidence, not permission to merge.
