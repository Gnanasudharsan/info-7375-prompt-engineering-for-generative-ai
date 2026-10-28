# Chapter 3 — Chat, assistant, and agent
*Follow the state change, not the label on the window.*

Suppose you ask an AI system to fix a report. In one interaction, it tells you which paragraphs to change. In another, it reads the report and offers a revision grounded in that file. In a third, it saves an edited report. All three can end with polished prose. They have not performed the same work. Only the third includes a persistent file change, and that difference matters even if the final messages look almost identical.

Now make the request smaller: summarize a folder without changing its files. The system reads a document, writes a good summary, and then helpfully saves a cleaned-up version over the original. The edit might be excellent. It is still outside the task. You followed the recipe and got the wrong outcome, and the reason is specific: nobody decided that the system could write. The ability arrived with the interface. A good result and an authorized action are different judgments, and in this story only the first was ever made.

These are constructed scenarios, not claims about a recorded Claude session. I use them because they expose the question this chapter makes inspectable. What could the system do, what did you let it do, and what evidence says what it did? A product name answers none of those. Neither does a final message that says done.

Chapter 1 gave the book's argument. Claude is far better than you at fluent, fast, parallel production, so you do not compete with it there, and three jobs stay with you: you conduct it, you check what comes back, and you drive, because your name goes on the result. Chapter 2 applied those jobs to an answer, with a contract written before the prompt and a pass that names what it passed. This chapter applies them to an action, which raises the stakes, because an action leaves a mark after the conversation ends. Each job asks one question here.

- **Conduct.** How much autonomy does this task need, and did I decide that before I granted anything? Writing that decision down is the gate.
- **Check.** What does the record show happened, as opposed to what the interface called itself? What I can honestly claim from it is the sign-off.
- **Drive.** Who authorized the action, and what keeps that decision with a person? The split of labor is the driver's seat.

The Python mechanism is deliberately small. We give three teaching surfaces different sets of capabilities, compute which required capabilities are missing, and classify a simplified list of events. The labels `chat`, `assistant`, and `agent` belong to this exercise. They are not a verified map of current product features, and they do not claim that every system bearing one of those names has the same permissions or architecture. The restraint is the point. Treated as universal names, the labels turn the lesson into a vocabulary test that interfaces will outdate. Treated as handles for explicit capability sets, they let you inspect an operation directly, and see what the classifier throws away: order, targets, authority, evidence quality, and whether the logged event really happened.

The first two chapters set a pattern. A probability is not a truth judgment. A format pass is not source support. Here the pattern reaches actions: capability is not authorization, an event label is not independent proof, and a write is not necessarily dynamic agency. We keep those three apart while we choose an interface sufficient for a bounded task.

## What you will be able to do

By the end, you should be able to represent a task as required capabilities, calculate the missing set for a teaching surface, and explain how the event classifier chooses its label, including what the label discards. You should be able to write the gate before any grant is made: the smallest capability set that finishes the task, the operation and target that are authorized, and the condition that sends control back to you. You should be able to read an event trace as evidence, saying for each claim whether it was proposed, attempted, completed, or observed, and what no trace can show.

You should also be able to say which parts of the work you handed to Claude, which authority stayed with you, and why the act of authorizing cannot be handed back to the system that wants to act.

The prerequisites are Chapters 1 and 2, Python lists and sets, and a basic idea of persistent state: a file remains changed after a response is no longer on screen. The paired [lesson](../lessons/03-chat-assistant-agent/docs/en.md) supplies runnable instructions and the existing knowledge check. Its Python reference is offline. Claude Code remains the assumed learning assistant, through your existing account; this classifier needs no direct API calls or credits.

Before opening the reference, predict which operations a read-only task needs and which it does not. Build your initial set comparison in your learner workspace. It is small enough to calculate by hand, which makes it a good place to practice explaining a design instead of accepting code that returns a plausible answer.

## A response and a file are different kinds of result

Your first decision comes before any choice of interface: what kind of result are you asking for? "Fix this report" hides four requests. Explain what is wrong. Propose a replacement. Save a new version. Alter the original. Each has a different scope and a different consequence for state, and a system will pick one if you do not. I put this decision first because everything you grant and everything you review follows from it.

In the first hypothetical, the output is advice, and someone must still decide whether to apply it. The second adds source access: the system can inspect material supplied to it or made available through a reading operation. The third adds a mutation: a stored artifact changes. Do not reduce this to "text is harmless and files are dangerous." Text can steer a decision, and a file edit can be trivial and well authorized. The distinction is operational. A persistent change creates a before and an after that you can check separately from the final explanation, so a proposed revision and a saved revision are different deliverables.

That matters for completion claims. "Here is how to fix the paragraph" is not "the paragraph in the specified file has changed." The second statement needs evidence about the file. A transcript of proposed text supports a claim about the proposal; it says nothing about where, or whether, the text was written. The evidence has to follow the object whose state you are claiming.

For the folder task, write the acceptance statement with both a requirement and a boundary: inspect the specified source, return a source-grounded summary, and leave the source files unchanged. Reading is needed. Writing the originals is not. If the system offers to save a separate draft, that is a proposed change of scope for you to evaluate, not something the original request already included.

The teaching program will not touch a real folder. It represents operations symbolically, which is enough to explain a capability comparison and not enough to demonstrate filesystem safety. Do not credit the small set function with protections it does not implement; Chapter 5 builds a path and permission check. Starting symbolically has a purpose. It forces you to name the operations before a complicated runtime surrounds them. If you cannot say whether the task needs a write, a larger tool stack will not settle it. It will only make an ambiguous request easier to execute.

Reading needs the same care. A response can use text already in the conversation without performing any new read. Decide what you will count as a `read` event, and do not infer one from an answer that merely mentions a document. In a real run, record how the document arrived and what evidence shows the operation.

## Capabilities as sets: the grant, written down

Granting a capability is a decision, and writing the grant as a set makes it a decision you can inspect. The [reference implementation](../lessons/03-chat-assistant-agent/code/main.py) defines three sets:

```python
SURFACES = {
    "chat": {"reason"},
    "assistant": {"reason", "read"},
    "agent": {"reason", "read", "write"},
}
```

The strings are categories within the teaching model. `reason` stands for response-level processing, `read` for access to information through the modeled reading capability, and `write` for a modeled ability to change state. Inserting a string into a set creates no access; the program stores a declared description that later functions compare. The sets are nested: everything in `chat` appears in `assistant`, and everything in `assistant` appears in `agent`. That gives the exercise an order. It is a design convenience, not a theorem about real interfaces, which can have capabilities that fit no single ladder.

Let R be the set of capabilities a task requires, and let C be the set declared for a surface. The missing set is R minus C, the requirements that do not appear in the surface:

```math
M = R \setminus C.
```

If M is empty, the declared set covers the declared requirements. Both uses of declared matter. A correct subtraction can sit on an incomplete task description or an inaccurate account of the runtime, and the arithmetic authenticates neither.

The implementation makes the comparison directly:

```python
def missing(surface, required):
    if surface not in SURFACES:
        raise ValueError("Unknown teaching surface")
    return sorted(set(required) - SURFACES[surface])
```

It rejects an unknown surface, converts the requirements to a set, subtracts the selected capability set, sorts the remainder, and returns a list. Set conversion removes duplicate requirement labels, and sorting gives a consistent order. Neither adds information about the task. Notice one boundary: the function validates the surface name but not the requirement labels, so an unfamiliar requirement stays in the missing set. That is a usable signal that the declared surfaces do not cover the task, but it is a different policy from `classify`, which rejects an unknown event. Explain the code you have, not the code you assume.

Take a constructed task that requires both `read` and `write`. For `chat`, neither is present. For `assistant`, reading is present and writing is not. For `agent`, both are present. These are the results preserved in the [worked-example output](../research/worked-examples.json), under `chapters.03`.

| Teaching surface | Declared capabilities | Missing for read and write |
| --- | --- | --- |
| chat | reason | read, write |
| assistant | reason, read | write |
| agent | reason, read, write | none |

Every cell can be reconstructed from the sets, with no marketing description and no feeling that one interface is more agentic. You can point at the required operation and check whether it appears in the declared set. That is the narrow question this function answers.

## The gate: choose the autonomy before you grant the capability

Now change the task rather than the interface. A read-only source inspection requires `read`, not `write`. In this nested model, `assistant` covers that requirement without the extra write capability of `agent`. That is a reason to choose the smaller surface, and the reason is not that the larger one is untrustworthy. The task does not need its extra operation, and every operation you grant is one more thing you must be able to check afterward.

Once the task is described accurately, the choice is arithmetic. The hard part is the description, and that is where conducting starts. In *Conducting AI*'s phrase, the human's job is "not to type less" but "to decide more precisely." The same book states the reflex for its own five-layer capability stack, which is the author's teaching device and not an industry standard: select the lowest capability the step requires, because the more constrained tool is the easier to verify (see [Verifiability first](../docs/conducting-ai.md#verifiability-first); Chapter 11 returns to it). Here the reflex becomes a document you write before the grant.

**The gate.** Before any system gets the ability to do anything, write this. Mine, for the folder summary:

```text
Gate: folder summary, source unchanged
Outcome:           a summary whose claims I can check against the source
Required:          reason, read
Granted:           reason, read (nothing wider)
Refused:           write, anywhere
Authorized target: the one source file named in the task
Back to me if:     the system proposes saving anything, touching a second file,
                   or changing the request
Evidence I read:   the recorded events, and a before-and-after listing of the folder
Passes if:         no write appears in the events; the listing is identical before
                   and after; every sentence of the summary traces to a passage
```

Every line is my decision. Claude can sharpen the gate by hunting for the case I missed, such as whether a temporary file counts as a write. It cannot write the gate for me without defeating its purpose, because the gate is where the decision goes on the record before the grant makes the decision by default. Notice the last line. It is a condition that can fail, and a gate with no failing case is a wish. The plausible but wrong gate grants `agent` because that surface is available and the request says to help with the report. The test of your gate is whether it names an operation and a target that would be refused.

Smaller is not automatically better. A response-only interface may be unable to produce what the task needs: if you authorized a file change and expect it to exist, returning advice alone is incomplete. If you widen the scope after seeing the work, rewrite the gate, date the new version, keep the old one, and authorize again. Design first does not mean freeze the design. Sufficient autonomy means matching the outcome, not minimizing the tool set whatever the work.

Three things hide inside the word autonomy, and the classifier measures only one. *Capability* is what the system may do, which is this chapter's sets. *Control* is who or what chooses the next operation. Anthropic's [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), published in December 2024 and included in the research packet, distinguishes predefined workflows from systems in which the model directs its own process. A predefined program can write a file, and a model-directed process can make several decisions without writing one. Chapter 4 makes the controller explicit. *Scrutiny* is how hard the output must be checked, which depends on the work and not on the permissions; the closing section takes it up as a separate axis from chat, assistant, and agent. Keep a sentence for each in your recommendation. "Use an agent" is shorter and says less.

There is also a reason about you. The more you grant, the more there is to check, and your attention does not grow with it. *Irreducibly Human* names a general form of this the volume trap: generation scales with the machine, verification does not (chapter 4; the course's note on it is under [Review capacity](../docs/irreducibly-human.md#review-capacity)). I treat that as an argument about review capacity, not a result I measured here. It is why the gate names the evidence you will read and not only the operations you allow. The second half of the gate, the test list for your classifier, comes with Build It.

## Events, not labels: what the record can show

A gate says what you intended. It does not say what happened. For that you need a record, and the first decision about a record is which description of the run to trust.

Capability sets describe what a surface is declared able to do. Event traces describe what is recorded as having happened. The relation is the one from Chapter 1 between a distribution and a sample: one describes what is available, the other records a particular run. Our classifier consumes a list of event names, not the capability table. Here is its complete implementation:

```python
def classify(events):
    allowed = {"reason", "read", "write"}
    if set(events) - allowed:
        raise ValueError("Unknown event")
    if "write" in events:
        return "agent"
    return "assistant" if "read" in events else "chat"
```

It rejects any event name outside the allowed set. Then `write` takes precedence: if a write appears anywhere in the list, the result is `agent`. With no write but a read, the result is `assistant`. Otherwise it is `chat`, which includes a list containing only `reason` and, by inspection, an empty list. The result is a category under this rule, not proof that any amount of reasoning occurred.

This is classification by presence. It ignores order and repetition, so one read and several reads share a label, and a write at the start and a write at the end both trigger the write branch. That compression suits a teaching question and would be reckless in a real review. The function also records no target: a `write` could be a disposable draft or an overwritten original, and the label cannot tell them apart. Nor does an event string prove the operation succeeded. The function trusts the list it is given, and if someone supplies `write` it returns the write-based label without looking at any filesystem. That is an input contract, not forensics. Keep the original trace beside the label, because the label is lossy and the trace is the evidence.

Four descriptions of one run can disagree, and they are not equally trustworthy.

| Description | Where it comes from | What it can support | What it cannot |
| --- | --- | --- | --- |
| The label ("agent", a product name) | A name chosen by someone else | A guess about what to expect | Anything about this run |
| The narration ("I saved the file") | The system's own prose | That something was said | That it happened |
| The event trace | A record of operations | That an operation was recorded, if the recording is sound | Targets, success, or authority, unless recorded |
| The state of the folder, before and after | A listing run against a rule you wrote | That something changed, or did not | Who did it, or whether it was authorized |

I read these from top to bottom as growing independence from the system's own account of itself. For a claim about a file, the state check is the strongest of the four because it fails differently from the other three. It can show no change when the narration said saved, and a change when the narration said nothing. That is the independence rule from Chapter 1 applied to an action. Claude can run the listing and compare it against a rule you wrote. It cannot vouch for its own action. For any record, ask who produced it: the thing that acted, or something that watched.

Inside a trace, keep four verbs apart. A write can be proposed, when a response offers it; attempted, when the operation was requested of the runtime; completed, when the runtime reported success; and observed, when you saw the changed state. A report should say which verb its evidence supports. The first three are not the fourth.

## One task, three constructed traces

Use this hypothetical folder task: "Read the supplied source report and prepare a summary. Do not alter the source." Three constructed event lists follow. They are not recordings from current Claude products. Their job is to make the classifier's reasoning visible.

Before you run them through your own implementation, do the part of the check that only works in advance. Predict the three labels. Then, for each list, write the over-claim a careless report would make and the record that would be needed to support it. "This trace is safe" and "this trace is unsafe" are both over-claims on three strings, and writing the sentence first is how you catch yourself making one afterward.

The first list is `['reason']`, labeled `chat`. Imagine the response offers general advice about writing a summary without accessing the source. That might be useful, but it does not establish that the source was read, and the capability comparison shows the teaching chat surface lacks `read`.

The second is `['reason', 'read', 'reason']`. It contains a read and no write, so the classifier labels it `assistant`. The trace is consistent with the read-only boundary. Consistent with is the right phrase: nothing in the list says which report was read or whether the summary followed it.

The third is `['reason', 'read', 'write']`, labeled `agent` because a write appears. If, in this stipulated scenario, the write altered the original source, it violated the no-change instruction. The classifier does not report the violation. It reports a write category. The permission judgment comes from comparing the specific operation with the gate.

| Constructed trace | Classifier result by inspection | What still needs evidence |
| --- | --- | --- |
| reason | chat | Whether required source access occurred through any recorded route |
| reason, read, reason | assistant | Which source was read and whether the summary follows it |
| reason, read, write | agent | What changed, whether the write succeeded, and whether it was authorized |

The published research run directly checks the `read` classification and the missing-capability comparison. The other trace labels above are transparent derivations from the displayed function and proposed cases for your own run. Keep recorded execution and code reasoning distinct. Both teach, but only one is an observed run.

Now suppose you explicitly asked for a separate summary file in a disposable learner directory. The required set would include writing, and a write-capable surface could be sufficient. The target would still matter: a new draft in the authorized directory is not permission to overwrite the source. The three-capability model cannot express that restriction. This is the payoff of a small model. It shows you the moment a label becomes too coarse for the question, and adding confidence to the label will not help. You need more information and a more specific boundary.

<!-- [FIGURE: Cajal production brief. One task across three action surfaces. Include response only, read enabled, write enabled, permission check, outcome evidence. Show the confirmed relationship that capability is not authority. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![One task across three action surfaces. capability is not authority.](../images/03-chat-assistant-agent-fig-01.png)
*Figure 3.1 — One task across three action surfaces*

## Capability does not confer authority

An empty missing set says the declared surface covers the declared requirements. It does not say you own the target, that affected people consented, that the source may be uploaded, or that a write is appropriate. None of those facts is an input to the subtraction, and reading the empty result more enthusiastically will not recover them. This is the center of the chapter, and the figure compresses it: one task, three surfaces, and a permission check standing between capability and outcome.

Authority is a decision with a record, and a person makes it. Name the allowed source, the output location, and the operation you requested. If the request is read-only, record that. If an edit is authorized, identify the target. A vague permission to help with a report should not quietly become permission to change unrelated files. The model can propose an action, including a well-chosen one. You authorize it, and the authorization says what, where, and when. The driver's seat below turns that into a task-by-task split.

This chapter does not implement a permission engine. The functions take no permission inputs, which is the evidence for that sentence. Chapter 5 builds a narrow runtime check in Python. Until then, do not present a capability inventory as if it enforced a policy.

The reciprocal mistake is treating inability as prohibition. If the teaching `chat` surface lacks writing, the model shows only that it cannot cover a write requirement. It does not show that a write would have been forbidden had another authorized tool performed it. Feasibility and permission answer different questions, and mixing them lets a technical limit pass as a moral judgment. Likewise, a permission request does not prove the proposed action is useful: you can authorize a draft that turns out to be poor. Keep four things distinguishable: the proposed action, the authority, the execution, and the quality review. One approval or capability flag is not a certificate for all four.

For your artifact, add a permission column in plain language. It can say that a constructed scenario stipulates a read-only request, or that you authorized a specific disposable write. Do not invent an approver, and do not treat a simulated person in a fixture as real consent. If permission evidence is absent, write absent or pending. The record's integrity depends on keeping the gap visible.

## Build It: your own classifier, then the second half of the gate

Build the small version before you read the reference. It is the baseline you will measure Claude's version against. Implement the three declared sets and `missing` in your learner workspace, starting with the read-and-write requirement, and predict the missing list for each surface before you run it. Then implement the event classifier and test the three constructed traces. The point is to explain every returned item, not to find a clever one-liner.

Next, write the second half of the gate: the contract for the code, before anyone implements it. Mine has five claims. `missing` sorts and removes duplicates. An unknown surface is refused. An unknown event is refused. A write anywhere yields `agent`. A read without a write yields `assistant`. It also names wrong versions the tests must catch. A classifier that keys on the final event gives the same answer as the real one for `['reason', 'read', 'write']` and a different answer for `['write', 'reason']`, so a test list without that second case would pass it. A classifier that quietly treats an unknown event as `reason` would pass every happy-path test. Design the smallest case that exposes each. If your tests cannot tell a wrong version from the right one, the gate is not finished.

The lesson's tests include an unknown event and an unknown surface. Keep both rejections in your explanation. An unexpected label should not be treated as harmless reasoning because the classifier lacks a category for it. At the same time, do not infer that rejecting a string named `delete-everything` prevents deletion in a runtime. The function validates its vocabulary, not operating-system calls. A test shows that the classifier refuses an unknown name. It does not show that a program cannot perform an operation and leave it out of the list. Event validation assumes something about where the events come from, so a system that relies on a trace must design and check that recording boundary separately.

## Use It: conduct Claude Code, then compare interfaces

Now give Claude the work it is good at. In Claude Code, in your learner workspace, hand it the gate you wrote, the contract and the test list, and not your implementation. Ask for an implementation that satisfies the contract and passes your tests. Then run your tests on what it returns, yourself.

Do three things with the result. Note any test that failed; often it marks a gap in your gate, which Claude cannot see because it only has what you wrote. Compare its classifier with your baseline and name one difference in behavior, either a boundary it handled that you missed (a revision to your gate) or one it silently ignored (a defect your tests missed). And ask it to propose a deliberately wrong classifier that still passes your tests, then check by hand whether it does. If it does, your tests were too weak, and you found out cheaply. Ask it, too, what the classifier cannot infer, and verify each answer against the code. Missing targets, permission fields, and success results are directly inspectable, so you need no speculation about intelligence to find them. Preserve the transcript with the prompt, plan, diff, commands, outputs, date, and displayed model label. If a session failed or did not run, record that.

Then run the comparison the paired lesson describes: the same small task through Claude chat, Claude with an uploaded source, and Claude Code in a disposable Python repository. This is an experiment for you to perform and document, not a result this chapter supplies. Use harmless source material and a narrow task, and write the task's gate first, including what you grant. Record the interface and operations actually available in your run, and do not assume a permanent capability assignment from a name. Use whatever permission controls your Claude Code session actually offers, record the settings you used, and if you cannot restrict a run to reading, record it as a run in which write was granted.

Record how the source was supplied: pasted into the conversation, attached through the interface, or read by a tool. Routes that produce similar answers leave different observation records, and your symbolic trace should be an explicit abstraction of the record, not a guess that the system must have read because the answer sounds informed. If the experiment includes a write, make the target a disposable learner artifact and give the authorization yourself. Record files before and after. Keep the proposed apart from the executed: a response may offer to save a file, ask permission, or explain a command without running it, and none of those is the completed write a trace stipulates.

If one interface is unavailable, mark its row not run and say what is missing. Do not manufacture it. You can still run the offline classifier on constructed traces, labeled constructed. An honest mix of observed and hypothetical records is usable when the provenance is explicit. An invented completion is not.

## Ship It: the action-surface comparison

The artifact is an action-surface comparison, and the [artifact brief](../lessons/03-chat-assistant-agent/outputs/artifact-brief.md) names the repository's expectations. Its value is that another reader can follow each row from task to gate, from gate to record, and from record to claim. A useful row names the source, the requested outcome, the granted and observed capabilities, what was proposed, what changed, the permission evidence, and what supports each. If no state change was requested, preserve that boundary. If a new output file was requested, distinguish it from the source. The target is not an implementation detail when it decides whether the action stayed in scope.

Your conclusion recommends an interface for a stated task under stated assumptions. It might say the read-enabled teaching surface is sufficient for the no-write summary, while a separately authorized saved draft needs writing. It must not proclaim that one product is universally better or safer; the evidence does not cover that. If you revise the required capability set after inspecting the task, keep both versions and say why. That is a learning event, not an embarrassment to erase.

**The sign-off.** End the comparison with a statement you could put your name to. Claude can draft its words in seconds and the draft will be fluent, so write it from your record. This is the template, not a signature:

```text
Sign-off: action-surface comparison
Checked:      which rows and which claims: capability sets, trace labels,
              before-and-after listings, permission evidence
How:          by hand / by a test I wrote before reading the reference /
              by a listing I ran myself / with Claude's help (say which parts)
Not checked:  whether any trace was complete; whether any summary was faithful;
              any interface I did not run; product behavior beyond my runs
Not claiming: that a label proves a permission; that any system is safe;
              that these surfaces match any product's current features
Signed or withheld: ____________  (name, date)
```

The Not checked line does the work. A trace you did not verify as complete and a summary you did not compare with its source belong on it. Use verbs that match the evidence: recorded, observed, computed, tested. An observed state change and a recorded event are not the same claim, and "authorized" needs a named person and a named operation. If the record does not support signing, withholding is an honest result.

Record Claude's contribution too: proposed cases, code review, execution assistance, organization of evidence. Your decisions about scope and sufficiency stay visible.

## The driver's seat

This is how the chapter's work divided, task by task. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Saying what the task requires | Ask what "fix" means; list the readings | Choose the scope and write the gate | The request's meaning lives in your situation |
| Computing missing sets and labels | Compute them, instantly | Predict first; name what the sets declare | The sets declare; they do not measure |
| Implementing the classifier from your contract | Implement it; propose a wrong version that passes | Build your baseline; run your tests | You cannot audit what you have not built |
| Checking what happened | Run the listing and compare it to your rule | Decide what counts as a change; read the state | The check must fail differently from the narration |
| Authorizing a write | Propose the action and its target | Authorize it, naming what, where, and when | Authority and accountability follow the person whose files and name these are |
| Saying what the comparison supports | Flag an overclaim | Choose the verb; sign or withhold | Your name is on the claim |

Record in the comparison one task you delegated and one judgment you retained, each pointing at a transcript line or an edit. If you cannot point at one, the split happened in your head. Look hardest at the authorization row. A model can ask for permission fluently, and a fixture can supply an approval instantly. Neither is a person deciding. The model proposes; you authorize.

## Verify and reflect

Run the demo, the six lesson tests, and your additional cases. Explain each result and its route through the code. Add a successful case outside the demo and a failure that would matter in your capstone; name the defect each is designed to expose, and say how another defect could survive both. Then take the strongest claim in your comparison, such as that a file was changed or an action was authorized, and find evidence for it outside the classifier. If you cannot, narrow the claim.

Ask what the classification discarded: sequence, repetition, targets, results, and authority. A summary should make a large record easier to navigate. It should not become an excuse to throw away the evidence needed to evaluate it.

Finally, revisit your first reading of "fix this report." Did you hear advice, a draft, or an edit, and did the stated scope support that reading? The code can calculate missing capabilities perfectly while the task model is wrong. Which distinction did you originally collapse: capability and authority, label and trace, or proposed and executed? Name the record that separated them again. That habit transfers beyond three labels.

## Assessments — ungraded practice

These Assessments carry no points. Use the paired lesson's existing [knowledge check](../lessons/03-chat-assistant-agent/quiz.json) and preserve your initial answers before consulting explanations. Write predictions before execution, and keep constructed traces distinct from recorded operations. Do not use this practice as authorization to modify unrelated files or publish anything.

### Warm-up

1. **Calculate the missing set — introductory; objective: represent requirements.** For the constructed read-and-write task, calculate the missing capabilities of all three teaching surfaces by hand before executing anything. Then change the requirement to read only and say which recommendation changes and why. State the assumption that makes the sets nested and why it is not a universal product taxonomy.

2. **Trace the classifier — introductory; objective: explain event presence.** Classify a reason-only list, a list containing a read but no write, and a list containing a write. Name the branch each uses. Explain why the label says nothing about the quality of the reasoning or the target of the write, and write the over-claim a careless report would make from each.

3. **Unknown is not harmless — introductory; objective: inspect validation.** Supply an unknown event name and an unknown surface name in separate tests, and predict and record the results. Explain why rejecting a vocabulary item is useful and why it is not enforcement of operating-system permissions. Name the boundary that would have to be built before a security claim could be made.

### Application

4. **Same label, different sequence — intermediate; objective: identify information loss.** Construct two event lists with the same categories in different orders and compare their labels. Describe a hypothetical workflow in which order would matter and the extra evidence a report would need. Then write the test that exposes a classifier keyed on the final event.

5. **A narrowly scoped folder task — intermediate; objective: write the gate.** Define a harmless source-summary task that forbids changing the originals. Write its gate: outcome, required and granted capabilities, refused operations, authorized target, the condition that sends control back to you, and the evidence you will read. Choose the smallest sufficient teaching surface, and describe the explicit scope change that would justify saving a separate draft, without treating it as already authorized.

6. **A new boundary test — intermediate; objective: test a distinct defect.** Add a successful case outside the demo and one failure case to your learner implementation. Name the defect each is designed to expose and explain how another defect could survive both. Use the reference only after your first attempt, and keep your changes separate from the course solution.

7. **Proposed is not executed — intermediate; objective: classify evidence.** Create an explicitly hypothetical record containing a proposed edit, a permission request, and a completed edit with a before-and-after observation. Give each part a verb (proposed, attempted, completed, or observed) and say which parts justify a write event under your trace definition. Do not invent a real person's approval, and say how an actual report should label missing execution evidence.

### Synthesis

8. **Three-interface comparison — advanced; objective: integrate observation and scope.** Use the paired lesson's comparison design on harmless material where access is available. Write the gate first. Record the actual interface, input route, available operations, and evidence; mark unperformed rows not run and label constructed traces. Recommend a surface for the bounded task without treating observed capabilities as permanent product specifications, and end with the sign-off.

9. **Capable but not authorized — advanced; objective: separate authority.** Construct a scenario in which the missing set is empty but the proposed write exceeds the stated task. Explain why the set calculation still succeeds and name the exact permission question left open. Revise the workflow so it can proceed within the existing scope or return the decision to a person, and say which part of that revision Claude could draft and which part cannot be handed to it. Good intentions do not create authorization.

### Challenge

10. **Misleading names — stretch; objective: critique a taxonomy.** Design two hypothetical systems whose names suggest the wrong capability set. Describe their actual operation sets, classify constructed events with the lesson rule, and explain why a write-capable predefined workflow and a model-directed process look the same to this classifier. Keep architecture and action capability as separate axes.

11. **A richer event record — stretch; objective: redesign for evidence.** Propose, in your learner workspace, an event representation that adds target, proposed-versus-executed status, and outcome evidence. Explain how it improves review and what it still cannot authenticate; adding fields does not make their contents true. Identify one check at the recording boundary and one judgment that remains outside the data structure.

## What you can now distinguish

You can represent a bounded task as a set of required capabilities and compare it with a declared surface, and you can say what an empty difference does and does not mean. You can classify the teaching event lists by the actual rule, write presence first, then read presence, otherwise chat, and say what the label discards. You can separate a response from a persistent artifact, a proposed action from an executed one, and capability from permission.

And you can say what the three jobs look like at this scale. You conducted: you decided the scope, and you wrote the grant, the refusals, and the pass condition before any system could act, choosing sufficient capability instead of maximum capability by habit. You checked: you preferred the state you observed to the narration you were given, wrote the over-claim down before you looked, and refused to let a coarse label stand in for a complete account. You drove: you let Claude propose, compute, and implement, and kept the scope, the authorization, and the verb in your own hands. Outside this model, you know to inspect the actual runtime and its evidence rather than infer features from a product name. Follow the operation and its consequence, then choose the boundary that fits.

## The next operation needs a controller

We have described what a system can do and summarized what a trace says it did. We have not built the mechanism that decides which operation comes next. A set of tools is not a loop. Something must take the current state, select an action, execute it, observe the result, and decide whether to continue.

Chapter 4 makes that controller visible in Python. We give it a finite action budget and inspect a trace in which a finish action produces a finished status even when the final answer is wrong. The pattern should feel familiar by now: just as a capability label does not confer permission, a terminal state does not establish the correctness of the result that comes with it. Which stops belong to the controller, and which are Claude's to take, is the next version of the question you answered here about writes.

Bring your action-surface comparison with you. It tells you which operations the controller might request. The loop adds sequence and stopping behavior, but it will not erase the need for source checks and authority boundaries.

## Anthropics

Compare the chapter's event-presence rule with [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), checked for the research packet on 2026-09-06. The upstream workflow-versus-agent distinction concerns how the process is directed; our classifier concerns which simplified operation categories appear. They answer different questions.

For your artifact, describe one hypothetical predefined workflow that writes and one model-directed process that does not need to write. Explain why the teaching rule alone cannot distinguish their control structures. This comparison uses Anthropic's guidance to sharpen the boundary of our Python model, not to claim the model reproduces Anthropic's implementation.

## Conducting AI

In *Conducting AI*, chapter 3's copy-editor, research-assistant, and supercollaborator levels organize work by the supervision its output requires. See [Usage and supervision](../docs/conducting-ai.md#usage-and-supervision). These three levels of scrutiny are my own teaching framework, not a measured product ranking, and they are not chat, assistant, and agent under other names. The same permissions can stay in place across a bounded edit, a source-dependent answer, and a proposed problem framing.

The body used the capability axis. The diagnostic this note adds is the gap. For each row of your comparison, write two levels. The first is the level of the work: I, a glance at the output against its input; II, checking against sources outside the interaction; III, examining the framing the output supplies. The second is the level of review you actually gave. The book's claim is that the risk is never the level itself but the gap between the level of the work and the level of the review, and it cites Parasuraman and Manzey (2010) for the finding that monitoring falls as automation looks more reliable. So start with the row where your review was lightest and ask whether its output was also the most polished.

Then add a supervision column naming what you must inspect and what knowledge that inspection needs. Do not import a blanket claim that a glance always suffices for an edit, or that a human cannot get useful help with framing. The question is whether the review you gave addressed the work you asked for.
