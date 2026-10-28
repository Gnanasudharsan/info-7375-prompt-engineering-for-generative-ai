# Chapter 4 — The agent loop
*Stopping is a control-flow event. Success needs evidence.*

Suppose a system looks up the same record again and again. Each lookup succeeds. Each observation is logged. The trace gets longer, but the task does not get closer to a supported answer. From inside a poorly described report, activity can look like progress. From outside, the relevant question is simpler: what changed that makes completion more justified than it was one turn ago?

Our offline research run gives this hypothetical a concrete boundary. A repeated-lookup policy with a turn budget of two stops after two recorded actions and returns `budget-exhausted`. The program does not invent a final answer to make the run appear complete. Notice who made that outcome possible: someone chose the number two before the loop ran. The stop was designed, not discovered.

Another constructed run looks up a record whose value is blue and then finishes with red. The returned status is `finished`. The contradiction is visible in the answer and the observation, but the controller never compares them. It accepts a finish action as a request to stop, not as a proven statement that the answer follows from the records. Both outcomes are preserved under `chapters.04` in the [research results](../research/worked-examples.json).

These two runs are the chapter. One loop cannot run past its budget, and that is a property you can build in before anything executes. The other ends in a wrong answer with a perfectly well-behaved status, and that is a property you can only catch by looking at the world after it stops. Neither says anything about how capable the thing proposing the actions is. Both are about where the stop lives and what it is allowed to mean.

Chapter 1 gave the three jobs that stay with you: conduct, check, drive. This chapter applies them to the most consequential line in any agent, the one that ends the run. Conduct: the exits and the budget are decisions you write down before the loop starts. Check: `finished` records that a finish action arrived, and what anyone is entitled to believe beyond that is a separate question with a separate check. Drive: Claude may take the stop that ends the run, and the stop that closes the task is yours.

I will use a scripted policy rather than a live model call. That choice makes each decision inspectable and repeatable. It does not reproduce Claude's private reasoning or current agent implementation. You will see an iterator supplying action dictionaries, a dispatcher handling a lookup, and a trace accumulating observations. The machinery is small enough to explain from the first action to the final return.

Chapter 3 separated capability from authority. Here we add sequence and termination. The questions are which action arrives next, what observation follows, what gets recorded, and which condition ends the run. Answering them is necessary for an agentic workflow. It still grants no permission to act and establishes nothing about whether the final claim is true.

## What you will be able to do

You should be able to implement the bounded controller, trace a turn by hand, distinguish policy exhaustion from budget exhaustion, and explain what `finished` does and does not mean. You should be able to design a repeated-action test, identify the outcome check missing from a completion claim, and propose a repetition detector with a case that could make it stop too early.

You should also be able to do three things the rest of the book builds on. Write the stop conditions as a gate before any implementation exists: every exit, the unit of the budget, what must never be fabricated, and the separate check that decides whether a finished answer moves on. Conduct Claude Code against that gate, run your own tests on what it returns, and write a sign-off that names the exits you exercised and the ones you did not. And say which stops Claude may take in this loop and which only you may take, with the line in your record that shows the split happened.

The prerequisites are Chapter 3, Python loops, dictionaries, iterators, and return values. The paired [lesson](../lessons/04-the-agent-loop/docs/en.md) supplies the runnable sequence and existing knowledge check. This mechanism runs offline with Python's standard library. Claude Code remains available through your assumed account for help with your learner implementation, but no direct API call is part of the worked example.

## The policy proposes, the controller stops, someone else judges

The decision here is who gets to end a run, and what the ending is allowed to mean. Any agent loop contains three jobs that products blur into one experience. Something proposes the next action. Something dispatches it, records the result, and decides whether the run continues. Something decides whether the final result is any good. In a chat window they arrive as one voice saying done. Pulling them apart is how you give each one an owner.

In this reference the first job is a policy: an iterable of action dictionaries. The controller creates an iterator and asks it for the next item on each turn, so a prepared list is enough. That is a deliberately limited use of the word. The list is not a learned model, and it does not change its next action based on what the controller observed, because nothing feeds the observation back. A more adaptive system would need a defined route from observations to its next decision. Do not describe that route as implemented merely because the code uses the name policy.

The second job is the controller, the `run` function you are about to read. The mapping of records is the lookup environment, and the controller never alters it. The state the controller builds is the trace: a list of records, each holding a turn number, an action name, and an observation. The third job, judging the result, does not exist in this reference. That absence is the subject of the next several sections.

Separating the pieces pays off in debugging: a poor action sequence dispatched exactly as specified is a fault in the sequence, and the right sequence with the wrong status is a fault in the controller. It pays off at integration too. A model-backed policy would be a new source of action requests, and it should not inherit the power to redefine the runtime's limits just because it supplies the next action. The turn budget belongs to the controller. Nothing the policy says creates another iteration after the range is spent.

Do not stretch that limit into a wall-clock guarantee. The loop bounds how many turns it begins. It places no timeout around an arbitrary iterator or a slow tool; if fetching the next item never returns, an iteration count cannot interrupt the wait.

Two different stops hide under the word done. One ends the run: the controller returns. The other closes the task: a person, or a check a person designed, accepts the result as meeting the need that started the run. The controller can take the first stop. Nothing in this function can take the second, and the rest of the chapter is about keeping the two from being confused.

## Every return statement is an exit someone decided

Before reading the controller, make your predictions. Write down what you expect if the policy supplies no actions, if it supplies one lookup and then ends, and if it supplies a finish action with no supporting lookup. Do not answer all three with success or failure. Predict the kind of termination. That precision is what makes the code inspectable, and a prediction written afterward only describes the output.

Here is the [reference implementation](../lessons/04-the-agent-loop/code/main.py):

```python
def run(policy, records, max_turns=4):
    if type(max_turns) is not int or max_turns < 1:
        raise ValueError("Positive turn budget required")
    trace = []
    iterator = iter(policy)
    for turn in range(max_turns):
        try:
            action = next(iterator)
        except StopIteration:
            return {"status": "incomplete", "trace": trace}
        name = action.get("name")
        if name == "finish":
            return {"status": "finished",
                    "answer": action.get("answer", ""), "trace": trace}
        observation = (records.get(action.get("key"), "not found")
                       if name == "lookup" else "error: tool not allowed")
        trace.append({"turn": turn + 1, "action": name,
                      "observation": observation})
    return {"status": "budget-exhausted", "trace": trace}
```

Read each return as a decision with an owner.

**The budget.** It must be an integer of at least one. The check is `type(max_turns) is int`, an explicit type choice rather than acceptance of anything that behaves like a number. A bad budget is rejected before the iterator or the trace exists, and the lesson's tests include rejection of zero.

**Policy silence.** `next(iterator)` raises `StopIteration` when the policy has no next action. The controller returns `incomplete` with the trace so far. It does not read silence as completion: an exhausted supply of scripted actions is a different condition from an explicit finish.

**The action name.** `finish` returns immediately with status `finished`, the answer the action carried, and the existing trace. `lookup` produces an observation from the records, or the string `not found`. Any other name becomes the observation `error: tool not allowed`, appended to the trace, and the loop continues if a turn remains. A name like `shell` is never dispatched, and a lesson test checks for the not-allowed message. That is concrete and useful. It does not establish permissions for any larger runtime outside this function; Chapter 5 builds that boundary.

**The end of the loop.** If no earlier return occurred, every turn was used and the result is `budget-exhausted`. The function does not check whether the policy had more waiting. It reports the boundary it reached.

The function's small size invites exactness: you can find every return and every trace append. Exactness also shows what the author of this code left undecided. Four things are open, and each belongs in your gate.

- A finish action with no answer field returns `finished` with an empty string. The reference lets a stop with no substance through.
- A non-dictionary action, such as a bare string, fails with an `AttributeError`, outside the three normal statuses. The code expects `.get`, and there is no schema validator like Chapter 2's. If you add one, describe it as an extension.
- An unknown action name consumes a turn and the run continues. Stopping, retrying, and escalating are three different policies, and none is implemented.
- The trace holds the action name but not the lookup key, and it never holds the finish.

## A trace records an event, not knowledge

The decision is what the trace must retain to support the claim you intend to make. A lookup action is a dictionary such as `{"name": "lookup", "key": "color"}`. If the records hold `{"color": "blue"}`, the observation is the string `blue`, and the trace stores it beside the turn number and action name. That is evidence of the local operation's result. It is not a record of private reasoning, and it does not make the mapping a trustworthy account of anything outside the exercise. The mapping is a fixture. An answer of blue after a lookup that returned blue can be checked for agreement with that record, and it does not become universally true by agreeing with a table we invented. The evidence boundary is the fixture, and a report should say so.

Two gaps follow from the fields. With no lookup key in the trace, a reader cannot tell which of several keys returned a shared value, so the worked example keeps the scripted policy in the evidence packet. And because the return comes before the append, the terminal action is missing from the trace. Do not add every field by habit, though. Some tasks carry sensitive inputs, and this reference defines no retention or redaction policy. Ask what is necessary to support the claim and keep that.

The controller's state update is only the append. It does not alter the records or send observations back to the policy, so repeating a lookup against an unchanged mapping adds another observation of the same operation, not new evidence. This is the antidote to the opening scenario. A longer trace is more recorded activity. Success at the tool boundary does not imply progress at the task boundary, and the controller computes no progress measure.

## A finished wrong answer

The decision is what you will let a `finished` status mean to anyone downstream.

Use the constructed records `{"color": "blue"}` and a policy of two actions: a lookup of `color`, then a finish with answer `red`. The default budget of four leaves room for both. Predict the status, the answer, and the trace length, and ask specifically whether the finish action will itself be appended. Also write down, with the date, what a wrong finish would look like in the returned object. That is the habit from Chapter 1: without the note, you will talk yourself into having expected whatever you see.

On turn one the lookup is dispatched, the observation is blue, and the trace gains an entry. On turn two the controller reads the finish and returns at once with status `finished`, answer red, and the existing trace. The observation-and-append lines never run for it, so the returned trace holds the lookup and no separate finish record. That is what the [worked-example execution](../research/worked-examples.json) records. If your artifact needs the terminal action, preserve the policy or add a separately labeled terminal record.

Now compare answer and observation. Red does not agree with blue. The controller does not perform that comparison, and its status is an accurate description of its own event: it received a finish. The mistake is reading `finished` as verified task success. The same status comes back when the finish carries no answer at all, because `action.get("answer", "")` supplies an empty string. Neither case registers as a failure.

The repair is not to rename every termination status failure, which would throw away distinctions the controller reports correctly. Separate controller status from outcome evaluation. A result can be finished at the control-flow layer and contradicted at the evidence layer, and that two-part report says more than an unqualified success or an undifferentiated failure.

The same gap appears at far larger scale in the case that opens the companion chapter on agents (*Computational Skepticism for AI*, chapter 8, "From prediction to action"). As that chapter reports it, an agent the study calls Ash was asked to delete one email, had no deletion tool, and reset its local email setup instead. It reported the account reset complete. The email was still on the provider's server. The agent's local state was consistent with done; the condition that made the task done sat outside what its action reached. The chapter's diagnosis is the one this section teaches: the completion report and the state of the world contradicted each other, and neither the agent nor any automated system noticed. Hold the scope the chapter holds. It is one exploratory study, one framework, two models, two weeks, and I have not checked the study myself. I use the account to name a shape, not to estimate how often agents fail this way. Your finish(red) is the small constructed version of it.

Now the check itself. Suppose you build an outcome checker for this tiny task that compares the final answer with the value of the named fixture record. It needs three properties. First, it must fail differently from whatever produced the answer. Asking Claude whether red is consistent with the trace puts the same kind of process on both sides of the check, and the same process asked twice gives you one opinion, not two. A deterministic comparison against the records fails in a different way. Claude can write that comparator quickly, but the criterion is yours. Second, it must read the record for the key the task names, not the key the policy happened to look up. Trace the code for a policy that looks up an absent key and finishes with `not found`: the answer agrees with the last observation and still does not answer the question about color. Third, it must state its scope: exact agreement for a constructed key-value question. It does not solve source-grounded reasoning in general. Its value is that its target and its limit are visible.

## Budget exhaustion is not policy exhaustion

The decision is what the budget counts, and what a run must say when it reaches the limit.

Consider a policy that repeatedly supplies a lookup action and a budget of two. Each turn consumes one action and records one observation. After the second append the loop has no turn left and returns `budget-exhausted`. The saved research run preserves this outcome with two trace entries. The policy need not be finite for the limit to hold: an iterator that keeps yielding lookups is consumed only as many times as the `range` permits. The qualification from earlier stands. This bounds completed turns, not elapsed time.

The companion book's table of the study's remaining cases files its looping and resource-exhaustion failures under an agent with no concept of its own resource limits and no termination heuristic, and it treats budget caps and rate limits as the kind of control that works when it is wired in explicitly. Whatever you make of the study, the design point is cheap to hold. A limit chosen before the run is a property of the controller. A limit discovered afterward is an incident report.

Now a finite policy of one lookup with a budget of four. The first turn records the observation. On the second, asking for another action raises `StopIteration`, and the result is `incomplete`: the action sequence ended before a finish arrived and before the turns ran out. Reduce the same policy's budget to one. After the lookup the loop exits without asking the iterator for another item, and the result is `budget-exhausted`. The controller never made the extra `next` call, so it never learned the policy had ended. The lesson's one-turn budget test covers this.

These results do not contradict each other. The statuses report different boundaries the controller actually reached. With a larger budget it can discover the iterator has ended; with a budget of one it reaches its own limit first. Explain the result by the execution path, not by knowledge the controller did not acquire. Notice also that the trace is the same in both runs, one lookup entry. Trace length alone cannot reconstruct the stop reason, so the configured budget and the returned status are part of the evidence, not decoration.

The finish action needs a turn in which to be consumed. A policy of a lookup followed by a finish cannot finish through that finish if the budget allows only the first turn. This is a decision about the unit. The name turn budget counts action-consumption turns, and the terminal action costs one. If you meant tool calls, you need a different implementation and different tests. The number and its unit are the human's, written down before the run.

Read the three normal exits as three different sentences, each with a limit on what it says:

| Status | What it records | What it does not establish |
| --- | --- | --- |
| `finished` | A finish action was consumed; the answer is whatever that action carried, possibly empty | That the answer follows from any observation, or that the task is done |
| `incomplete` | The policy had no next action before the budget was spent | That the task is done, or that it is impossible |
| `budget-exhausted` | The controller used every turn it was given | That the work was finished, that the policy had nothing more to propose, or any bound on time |

<!-- [FIGURE: Cajal production brief. A bounded controller has distinct exits. Include next action, execute, append observation, finish, incomplete, budget exhausted. Show the confirmed relationship that stopping does not verify the answer. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![A bounded controller has distinct exits. stopping does not verify the answer.](../images/04-the-agent-loop-fig-01.png)
*Figure 4.1 — A bounded controller has distinct exits*

## Repetition detectors have false positives too

The decision is which patterns a stop rule may treat as a reason to end the run. The turn budget limits completed iterations. It does not notice that two actions are the same or that two observations add nothing. The reference contains no repetition detector, which makes one a good learner extension: propose a rule that notices an unproductive cycle, then find a case where it would stop useful work.

Start by defining what repeat means. Matching only the action name is too coarse, since two lookups can request different keys. Matching name and key is more specific, yet it still does not always mark a useless repeat if the environment can change. Our fixture stays unchanged during a run, and a different system might not. A rule on identical observations has its own ambiguity: two different records can legitimately hold the same value, and a task that must check both has not wasted the second lookup. The observation alone may not identify the evidence obligation being met. State a detector's assumptions together with its rule.

These are design cases, not measured performance. A detector needs a stated target failure and a test that challenges its stopping behavior, and the budget stays a separate backstop even if the detector works on the examples you chose.

You also have a less ambitious option: report suspected repetition and let the run continue. That trades decisive stopping for a reviewable signal. Which is right depends on what a wasted turn costs and what an interrupted useful run costs, and neither number is in the code. Here the machine and the person have different jobs. Claude can propose the detector, write its tests, and hunt for the repeat that fools it, quickly. Whether a suspicion is enough to end someone's run is a call about cost and authority, and it is yours. The driver's seat below collects these splits in one place.

## Before the exits: does this task need a loop?

One design decision comes ahead of any exit, which is whether to build a loop at all. *Conducting AI* places agentic execution at the top of a five-layer capability stack. It describes that layer as reliable for well-scoped, low-branching tasks that have verification gates built in, and unreliable for long-horizon autonomy, where an early mistake propagates through every step that depends on it (chapter 8, "The Five-Layer Capability Stack"; see [Verifiability first](../docs/conducting-ai.md#verifiability-first)). Its working rule is to select the lowest layer that does the job and to route deterministic work out of the model entirely. The stack and its reliability labels are the book's own teaching device, not an industry standard, and the rule is a design preference, not a measurement showing that loops perform worse.

Apply it to our fixture. The question "what is the color record" is `records["color"]`: one dictionary lookup, no loop, no exits, no finish to doubt. I build the loop here because the exits are the subject, not because the task needs one. A loop earns its place when the next action depends on what the previous one found, and this controller's scripted policy does not yet. It is a skeleton for the exits. In your own work, ask the question first. Every loop you add is an exit you must design and a finish you must check.

## The gate: write the exits before anyone runs the loop

The gate returns, this time as a stop-condition contract rather than an experiment. Before you ask Claude for any implementation, and before you run anything, write the following in your learner workspace. It is the part of this chapter no tool can write for you without defeating its purpose, and it is what you will hold Claude's controller against.

*Design.* The exits, as a table. These are my choices; no model produced them, and the reference happens to make the same ones. Mark every line with who decided it: you, the lesson's tests, or Claude. At this stage Claude has decided none of them.

```text
The run ends because...           status            answer           trace
the policy has no next action     incomplete        none             every completed turn
a finish action is consumed       finished          what it carried  every completed non-finish turn
the turn budget is spent          budget-exhausted  none             every completed turn
the budget is not a positive int  ValueError        n/a              n/a
```

The unit of the budget is a turn that consumes one action from the policy, and a finish costs one. An action name outside lookup and finish is never dispatched: it produces an error observation and the run continues. Whether an error should stop, retry, or escalate is a policy I have decided not to implement yet, and I say so.

*Contract.* No exit fabricates an answer. A finish is a request to stop, and the result says only that one arrived. The configured budget and the status travel with the trace. A budget that is not a positive integer is rejected before the policy is touched.

*The check that is not the controller.* For the question the task asks, the finished answer must equal the value in the records for the key the task names. This check reads the records, not the trace, and it never changes the controller's status.

*Before the output moves on.* The answer leaves the controller only if the status is `finished` and that check passes. Any other status sends the status and the trace to a person, and nothing else. For a real task, a person also reads the trace before the answer is used.

*Wrong versions your tests must catch.* A controller that returns `finished` when the policy runs out: the empty-policy test catches it. A controller that tests the budget after dispatching, so it runs one action too many: only a test that counts trace entries against an endless iterator catches it. A controller that confuses `incomplete` with `budget-exhausted`: trace length cannot tell them apart, because one lookup gives one trace entry under a budget of one and under a budget of four, so your tests must assert the status for both. And a helpful rewrite that quietly turns the red answer into a failure status: it satisfies a test that only asks for rejection and destroys the distinction between the layers, so your tests must assert both that the status stays `finished` and that the check reports a mismatch.

*What a failure looks like.* One sentence, dated, written before you run: what you will see in the returned object if the controller ended well and the answer is wrong. If you write it after, you have described the output, not tested your understanding.

*What this controller may claim.* It ended in a named way, within a stated turn budget, under the two operations it knows. It cannot claim that the answer is right, that the run was bounded in time, or anything about how Claude decides.

A gate is not a freeze. Building the controller will show an exit you missed, perhaps the non-dictionary action, and the right response is to reopen the gate, date the revision, and keep the original. Claude can sharpen the gate. Ask it for the exit you forgot or the wrong version you did not list, and treat what it returns as proposals for you to accept or reject.

## Build It: separate the exits before adding complexity

Write your own controller in the learner workspace before you open the reference, and write it against the gate, not from memory of this chapter. Start with the empty policy, one lookup, and a finish. Preserve a distinct status for each exit in your table. Do not start by connecting a paid model call. Scripted actions let you isolate the behavior you need to understand before another source of variability enters.

Trace every return. For each one, name the fields the returned dictionary carries: `finished` carries an answer, the others manufacture none, and the trace grows only on non-finish actions. Downstream code can depend on those interface facts, so put them in your explanation and your tests. Then test an unknown action name. In the reference it becomes an error observation and still consumes a turn; a learner extension that stops, retries, or escalates is a new policy, to be recorded as new and tested.

Read the [existing tests](../lessons/04-the-agent-loop/code/tests/test_main.py) before the reference implementation. They cover the empty policy, a finish action, budget exhaustion, lookup results, a disallowed tool, and an invalid budget. Add tests for the distinctions this chapter made: a wrong finished answer, a finish that falls beyond the available turns, and the difference between a consumed terminal action and a trace entry.

Your version is the baseline: the record of what you understood before Claude touched anything, and the instrument you will measure Claude's controller against. You are not trying to out-type Claude. You are acquiring the ability to hear that a controller is wrong when its status names look right.

## Use It: conduct Claude Code against your gate

Now hand Claude the work it does quickly. Open Claude Code in your learner workspace. Give it the gate, meaning the exit table, the contract, the outcome check, and the list of wrong versions, and not your implementation. Ask for a controller that satisfies the contract and passes your tests, then run your tests yourself on what it returns.

Do three things with the result. First, note which of your tests failed, if any. A failure is often a gap in your gate that Claude could not see, because it had only what you wrote. Second, compare its controller with your baseline and name one difference in behavior: how it treats a finish with no answer, a non-dictionary action, or the terminal action in the trace. Whether it handled a boundary you missed or silently decided one for you, the difference is a decision about an exit, and exits are yours. Third, ask Claude for a deliberately wrong controller that still passes your tests, and check by hand whether it does. If it does, your test list was too weak, and you found out cheaply.

Preserve the actual transcript: your prompt, its plan, the diff, the commands, and the outputs, with the date and displayed model label. If the session failed or did not run, record that instead of substituting a fixture.

The paired lesson adds a second, observational use. Trace a Claude Code bug fix and a document task through an available Claude interface, as separate and actual experiments if you perform them, and map the visible observations and tool results onto the controller's action-and-observation structure. A visible trace shows requested tool actions, returned output, and a final message. That is enough to ask questions about sequence and evidence. It is not a window into private reasoning, so do not narrate an internal deliberation, and do not claim the production system uses this Python loop. Keep permission differences visible: a bug fix in a disposable repository and a document task have different readable sources and writable targets, and this controller's in-memory lookup enforces none of them.

Add one column to your notes for each run: every point where it stopped, and who took that stop. Claude ended its turn and reported done; you interrupted; you approved or declined a request; you accepted the result. If you do not perform an interface experiment, mark it not run. For any completion claim you do observe, name the independent outcome evidence. In a bug fix, that is the changed file and the tests actually executed. In a source summary, it is comparison with the specified sources. The final done message supplies neither.

## Ship It: preserve the failure trace

The artifact is an agent trace with turn number, action, observation, stop reason, and the evidence that would justify completion. The [artifact brief](../lessons/04-the-agent-loop/outputs/artifact-brief.md) gives the repository expectations. Keep the policy fixture, the record mapping, the budget, and the returned object together so another reader can reconstruct the path.

Include the repeated-action run and the wrong-answer finish run. Do not remove them because they make the controller look less impressive. They explain its boundaries, and a failure trace is a reusable test case that a clean happy-path transcript can never be. Your conclusion should name three layers: the policy supplied an action, the controller processed it and stopped under a named rule, and a separate check assessed the answer against the task evidence. Where a layer is absent, say so. The wrong finish shows that the first two can occur without the third succeeding.

Record your own change in interpretation. Perhaps you expected the finish in the trace, or expected a one-item policy always to return `incomplete`. Preserve the prediction and the line of code that changed your view.

Choose verbs the evidence earns. The controller *returned* a status. The trace *records* what was dispatched. The comparison *found* a mismatch with the fixture. None of these *establishes* that an answer is correct. A claim you can stand behind: "In the recorded offline run, the controller returned `finished` with answer red after one lookup that observed blue; a separate comparison against the fixture found a mismatch." Now imagine a reviewer who sees `finished` and asks whether the task succeeded. Your report should make the reply easy: `finished` records that a finish action was consumed, and nothing else.

**The sign-off.** End the artifact with a statement you could put your name to. Claude can draft its words in seconds and the draft will be fluent, so write it from your record. This is the template, not a signature:

```text
Sign-off — agent trace
Checked:      which exits I exercised (name them), and the outcome check
              on finish(red) against the blue record
How:          by hand-trace / by tests I wrote before reading the reference /
              by recomputation / with Claude's help (say which parts)
Not checked:  non-dictionary actions; blocking or slow tools; a model-backed
              policy; whether the fixture matches any real source; key
              retention or redaction
Not claiming: that finished means supported; that the budget is a timeout;
              that this is how Claude's own agent loop works
Signed or withheld: ____________  (name, date)
```

The "Not checked" line does the work, as it did in Chapter 1. It is the line an AI-written sign-off omits, because the system that wrote it has no record of the exits you never exercised. If your evidence does not support signing, withholding is an honest result.

## The driver's seat

A navigation voice saying "you have arrived" is a finish action. Arrival is at the address you wanted, not the address the system resolved, and the voice cannot settle whether the two match. The stops in this loop divide the same way. Claude may request the stop that ends the run, and does so whenever it reports that it is done. Only you take the stop that closes the task.

| Stop or related task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Proposing actions and requesting finish | Propose the next action; request finish when it judges the work done | Decide that a finish request means "stop the run" and nothing more | The finish comes from the same process that did the work, so its report is one datum, not the check |
| The turn budget | Suggest a value and a unit, with reasons | Choose the number and the unit before the run; raise it only by a new written decision | It is the one way a run ends that does not depend on the policy cooperating |
| Repetition and error observations | Notice and report suspected repetition; propose a detector and the case that fools it | Decide whether a suspicion ends the run, flags it, or escalates | The cost of a wasted turn against an interrupted useful run is not in the code |
| Checking a finished answer | Write the comparator you specified, run it, list every mismatch | Define what the answer is compared against and keep the check independent of the generator | An AI checking its own answer is one opinion run twice |
| Closing the task | Draft the trace and the report | Accept, narrow, or withhold, and sign | Your name goes on it, and `finished` is not an acceptance |

A comparator you wrote can close this tiny task on your behalf, because the claim is an equality against a fixture you control. It would not close "the summary is faithful to its sources," which needs a different check and a person. Where that line falls for a given claim is a judgment, and it stays yours.

Point to the lines in your record that show each half happened: the transcript line where Claude requested the stop or reported done, the command you ran afterward that did not come from Claude's report, the edit you made to the budget or the detector rule, and the sign-off line you signed or left unsigned. If you cannot point to them, the split happened in your head and not in the record.

## Verify and reflect

Run the demo, the six lesson tests, and your added cases. The [research script](../research/worked_examples.py) preserves the published counterexamples and their assertions. Use its actual JSON output to compare the observed statuses, then explain each return without relying on the fact that a test passed. A status name is useful only if you can say what event it denotes.

Review any claim that the loop is bounded. Specify the unit and the assumptions. Here the configured limit bounds ordinary completed turns in the demonstrated loop; it is not a general timeout, a memory cap, a credential policy, or a correctness check.

Then inspect the artifact for invented success. Did you supply an answer when the controller returned `incomplete`? Did you summarize budget exhaustion as successful completion because the trace looked productive? Did you call an answer supported without comparing it to the record? Correct those statements while preserving the original mistaken interpretation in your learning record. Then reread your gate. Which line did building the controller change, and did you date the revision?

The reflection should name the actual confusion. "I thought stopping meant succeeding" is a start. "The finish branch returns before any comparison between red and the recorded blue observation" is better. It ties the general lesson to a mechanism you can recognize when the surrounding system gets larger.

## Assessments — ungraded practice

These Assessments carry no points. Use the paired lesson's existing [knowledge check](../lessons/04-the-agent-loop/quiz.json), preserving your initial answers before reading explanations. Keep fixtures labeled and do not introduce paid API requests to test a controller whose behavior can be isolated offline. Your learner implementation should remain separate from the reference.

### Warm-up

1. **Trace one turn — introductory; objective: explain dispatch.** Choose a harmless lookup key and fixture value. Predict the first trace entry, then run the case. Identify the action source, the dispatcher condition, the observation, and the state update. Explain which information the trace omits and where you preserved it in the surrounding artifact.

2. **Three exits — introductory; objective: distinguish termination.** Before running anything, write your exit table: one case each for incomplete, finished, and budget-exhausted, with the status, answer field, and trace you expect. Then run them and mark every cell you got wrong. Do not call the three success or failure without qualification, and state the independent outcome question that remains once the status is known.

3. **Finish without evidence — introductory; objective: inspect a boundary.** Supply a finish action without a preceding lookup and inspect the result. Then consider the default for a missing answer field, and decide in your gate whether a finish with no answer should be accepted at all. Explain what the result proves about control flow and what it does not prove about the task. Keep this as a constructed test, not a claim about a real service's behavior.

### Application

4. **The last available turn — intermediate; objective: test a budget boundary.** Use a policy with lookup followed by finish and compare two carefully chosen budgets. Predict which actions will be consumed and which will be recorded. Write the unit of max_turns as a line of your gate. If you propose a tool-call budget instead, describe the different rule and tests it would require.

5. **A repeated iterator — intermediate; objective: demonstrate bounded iteration.** Supply an iterator that keeps yielding a harmless lookup action. Use a small positive turn budget and record the resulting trace and status. Explain why the budget stops ordinary repeated actions in this experiment and why the result is not a proof of a wall-clock timeout for arbitrary blocking code. Say who chose the number and when.

6. **A wrong finished answer — intermediate; objective: separate outcome checking.** Reproduce the blue-record, red-answer counterexample. Preserve the controller result and add a separately labeled comparison against the fixture, reading the record for the key the task names. Explain why finished and contradicted can both be accurate labels at different layers. Do not silently alter the controller status to conceal its actual semantics.

7. **An error observation — intermediate; objective: trace disallowed actions.** Supply an unknown action name, then another permitted action if the budget allows it. Predict whether the controller stops immediately or continues, and record the actual result. Propose one alternative error policy for your learner version, explain its tradeoff, and say whether that stop belongs to the controller, to Claude, or to you, and why. Distinguish your extension from the reference behavior.

### Synthesis

8. **The evidence packet — advanced; objective: integrate provenance.** Assemble policy, records, budget, trace, stop reason, and outcome check for both a supported answer and a deliberately unsupported answer, and finish with the sign-off. Identify which parts are recorded execution and which are your interpretation. Ask a reviewer, or Claude as a preliminary reviewer, to locate an unsupported completion claim, then verify the criticism against the preserved artifacts yourself.

9. **A production analogy with boundaries — advanced; objective: transfer cautiously.** Map visible operations from an authorized Claude Code task, or an explicitly hypothetical task if none was run, onto action, observation, and stop, and list each stop with who took it. State where the analogy ends. Do not invent private reasoning, unavailable tool results, or a claim that the production system uses this exact controller.

### Challenge

10. **A repetition detector that can be wrong — stretch; objective: evaluate a stopping rule.** Implement a detector in a separate learner version. Define whether it compares names, arguments, observations, or some combination. Construct both a pointless repeated-action case and a useful repetition that challenges the detector. Decide whether it terminates or only flags, and defend the choice by the cost of each kind of error. Keep the turn budget as a separately defined boundary.

11. **Richer termination evidence — stretch; objective: redesign the trace.** Propose a trace format that records a terminal action and the relevant lookup arguments without claiming their contents are authenticated. Explain what downstream review becomes possible and what additional risks or data-retention decisions appear. Identify which field supports the stop reason and which separate check supports the final answer.

## What you can now diagnose

You can trace a bounded controller without hiding its work behind the word agent. An iterator supplies an action, the dispatcher selects the permitted operation or an error observation, and the trace records the nonterminal turn. The loop stops through explicit return paths, and you can name the input and branch responsible for each normal status.

You can tell the policy running out of actions from the controller running out of turns, and explain why a one-action policy produces different stop reasons under different budgets. The observed stop reason depends on the path actually taken, not on what you know is waiting beyond it. You can explain why a finished result is not automatically supported: the red answer after a blue lookup is a reproducible counterexample, and a separate outcome check is needed whose scope is stated as carefully as the controller's.

And you can say what the three jobs look like at this scale. You conducted: you wrote the exits, the unit of the budget, and the wrong versions your tests had to catch before Claude implemented anything, and you asked first whether the task needed a loop at all. You checked: you refused to let a status stand in for a result, kept the comparison independent of the generator, and named what you did not check. You drove: you let Claude propose actions, request the stop, write the comparator, and hunt for the repeat that fools your detector, and you kept the budget, the price of a false alarm, and the closing of the task.

## A bounded loop can still cross a boundary once

The controller now limits repeated ordinary actions. That is progress. It does not answer the next question: what if the first action is outside the authorized scope? A budget of one can still allow one wrong target or one unauthorized mutation in a system that exposes such tools. Iteration count and permission are separate controls.

Chapter 5 will inspect that boundary through filesystem paths. A name that looks relative can resolve to a target outside an approved root. A permitted read does not imply a permitted write. We will use disposable fixtures to test traversal, symlinks, and approval checks, while refusing to describe a short teaching function as a complete production sandbox. The gate there is a permission policy, written before any tool runs, in the same way you wrote the exit table before any loop ran.

Carry the trace discipline forward. The next artifact should preserve the requested action, resolved target, decision, and observation needed to explain what happened. A good controller makes the sequence visible. A good boundary makes the allowed operation explicit. Neither eliminates the need to compare the resulting state with the task the human actually authorized.

## Anthropics

Anthropic's [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), included in the research packet and checked on 2026-09-06, provides a useful comparison for model-directed processes and their surrounding workflow. Keep that architectural guidance distinct from this scripted iterator.

Mark where a model-backed decision source would replace the prepared actions in your learner design. Then identify the controller limits and evidence checks that should remain explicit outside that source. This is an adaptation task, not a claim that our short loop reproduces Anthropic's runtime or that an API integration has already been executed.

## Computational Skepticism

The companion's chapter on agentic validation shifts the review question from the system's completion report to the outcome its actions produced. See [Agent outcomes](../docs/computational-skepticism.md#agent-outcomes) for the passages this chapter used. The same chapter, in its section on the cases where the agents resisted an attack, adds a question the body has not asked: under what condition would this robustness fail? Observing that nothing went wrong this time is not validation.

Apply it to the parts of your artifact that held. The budget stopped the repeated lookup. Your detector, if you built one, stayed quiet on a useful repetition. For each, name the condition under which it would not have held: a blocked call the iteration count cannot interrupt, a repeat your detector's definition does not cover, a finish that carries a right-looking answer from the wrong key. If you cannot name a condition, you have observed a pass, not validated a control. The source's own framing is an exploratory study of one framework and two models over two weeks. I borrow its diagnostic question, not its census.
