# Chapter 11 — Tool use and verification

*A result can match its request exactly and still not support the sentence built on it.*

The tool returned `42`. The assistant then said `99`.

That is not a hypothetical defect invented to make a point. It is the deliberately constructed offline fixture used in this chapter's research run. The same bounded controller that correctly accepted a request to add 17 and 25, executed Python, and returned a result associated with the right call identifier also accepted a later assistant message whose stop reason was `end_turn`. The controller reported its own status as `finished`. It did not compare the assistant's final sentence with the tool result. Protocol completion and factual verification were different mechanisms.

Notice what went right. The request was well formed, the dispatcher validated it, the result carried the matching identifier, and the loop ended in a recognized state. Build every one of those pieces correctly and you can still ship a trace that ends in a false sentence. A correct recipe is not a check.

Claude will gladly help you read that trace. In seconds it will write a fluent account of why 42 and 99 differ, and the account may be right. What one transcript does not show is the view from outside the route: what 17 and 25 were supposed to be, where each of your checks got its inputs, and whose name goes on the report. Those are the three jobs Chapter 1 named, conduct, check, and drive. Tool use is the first place in this book where each has a seam you can point at.

This chapter tears that mechanism down. The interesting part of tool use is not the spectacle of a model asking software to do something. It is the chain of custody: a proposed request crosses a validation boundary, an application dispatches a named operation, execution produces evidence, a result is paired with a request, and a later claim is checked against something other than itself. Remove any link and fluent narration can conceal the gap. The example is intentionally small, because arithmetic lets us know the answer independently. In a file edit, a database query, or a deployment, the same layers remain and the independent check gets harder and more consequential.

## What you will be able to do

By the end of the chapter, you should be able to:

- explain why a tool schema is an invitation rather than an execution engine, and decide which exact operations belong in the application and not in the model;
- validate a proposed call before dispatching it, and state what the dispatcher must refuse as a contract you wrote;
- match every result to its request identifier, and state what that match does not show;
- distinguish request acceptance, execution, result delivery, loop termination, and claim verification;
- design bounded failure behavior rather than assuming every response requests a tool;
- audit a final claim using evidence that can disagree with it, choosing each check for a failure mode the producing route cannot catch;
- write the gate (contract, tests, and evidence matrix design) before asking Claude Code to implement, run your own tests on what it returns, and write a sign-off that claims no more than the record supports;
- say which checks Claude ran and logged, which judgment about independence stayed yours, and why.

You should have worked through Chapters 4 and 5 on bounded controllers and permissions, Chapter 8 on protocol state, and Chapter 10 on plans. From Chapter 1 you carry three named devices: the gate, the sign-off, and the driver's seat. The code uses Python dictionaries, exceptions, loops, JSON serialization, and injected functions. No direct API call is required. The recorded observations below come from offline fixtures executed against the course implementation.

This narrative chapter is paired with the runnable [Lesson 11 materials](../lessons/11-tool-use-and-verification/docs/en.md). Use the lesson for the compact build sequence and this chapter for the teardown of what each layer can establish.

Before reading the trace, predict the answers to four questions. Will Python accept `True` as the number 1? Will an unknown tool become a Python exception or a returned tool error? If two calls share one identifier, will the program run both? If the assistant stops after saying `99`, will the loop call that outcome finished? Write the predictions down and date them. The value is not guessing correctly; it is exposing the model of the machinery you brought to the page.

## Three jobs at the scale of one tool call

Chapter 1 gave the argument once: Claude produces fluent text and code far faster than you can and has no stake in whether any of it is true, so you decide where it goes, check what comes back, and sign. Here the three jobs sit on one function call.

**Conduct.** Before any call, you decide which operations must be exact and therefore live in your program, not in the model's continuation. After it, you decide what the loop may call done. The gate for this chapter is the tool evidence matrix design: which check, for which failure mode, written before the run.

**Check.** The trace looks finished at every step. A matching identifier establishes who asked. A `finished` status establishes that the controller saw a stop signal. A fluent sentence establishes nothing. Only a check that fails differently from the thing it checks can say no to it.

**Drive.** Claude can run those checks and log them faster than you can type the command. Which verification surface counts as independent of the route that produced the result is your call, and the log cannot make it for you. That is this chapter's driver's seat.

## Conduct: what must be exact does not belong in the model

You want the sum of 17 and 25 in a report. In one design, Claude writes the number in its reply. In the other, Claude proposes a call, your program does the addition, and Claude reports what came back. Which do you choose, and why?

Chapter 1's loop explains why this is a real choice. When Claude writes `17 + 25 = 42`, that sentence is a continuation, ranked and sampled like any other. It is very often right. The design question is not how often. It is whether anything in the path would tell you the one time it is not. Nothing outside the continuation recomputes the sum. When your dispatcher returns 42, the number came from an operation you can read, re-run, and break with a test.

*Conducting AI* turns this into a selection rule it calls verifiability-first engineering: choose the lowest capability that does the step, because the most constrained tool is the one you can check. Arithmetic, exact lookups, deterministic transforms, and schema validation belong outside the probabilistic layers. The book's example totals every line item over $10,000 across 200 invoices. Ask a chat window for the total and you receive a fluent number with nothing behind it to audit. Extract fields per invoice and hand the filter and the sum to deterministic code, and you receive a number with seams where you can compare records with invoices and recompute the sum. The book's five-layer capability stack and its "easier to verify" value are teaching devices, not an industry standard and not a ranking of how reliable each layer is. What carries over is the question: which part of this step should not touch a stochastic model at all?

Routing out has two honest costs. It makes the step inspectable, not infallible: deterministic code can encode the wrong formula, parse the wrong field, or read stale input, and it will do so consistently. And every operation you grant the dispatcher is authority you have granted. A one-tool allowlist is easy to audit because it can do almost nothing. So the division here is deliberate: Claude proposes the call and interprets the trace, and your Python owns exact argument validation and arithmetic.

## A tool description does not run a tool

The first design question is what you tell Claude exists. The course implementation advertises one tool:

```python
TOOLS = [{
    "name": "add",
    "description": "Add two finite numbers",
    "input_schema": {
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"],
        "additionalProperties": False
    }
}]
```

This schema tells Claude which request shape the application is prepared to consider. It does not import an `add` function into the model. It does not prove that the application enforces the schema. It does not authorize the model to run arbitrary Python. The schema is part of a protocol conversation; the runtime remains application code.

That distinction removes a great deal of magic. Claude produces a structured block that can be read as a proposal: call the tool named `add` with these arguments. The application decides what that name means, checks the arguments, executes its own implementation, and constructs the result message. The model does not reach through the message and touch a function. It emits data. Your program interprets that data under rules you own.

The second design question is what your program will refuse. The first boundary is the dispatcher:

```python
def dispatch(name, args):
    if name != "add" or not isinstance(args, dict) or set(args) != {"a", "b"}:
        raise ValueError("Unknown tool or invalid arguments")
    if any(type(v) not in (int, float) or not math.isfinite(v)
           for v in args.values()):
        raise ValueError("Arguments must be finite numbers, not booleans")
    value = args["a"] + args["b"]
    if not math.isfinite(value):
        raise ValueError("Result overflow")
    return value
```

Read the conditions as a contract. The name must be exactly `add`. Arguments must be a dictionary with exactly the keys `a` and `b`. Each value must have the exact Python type `int` or `float`, and each must be finite. The result must also remain finite.

The exact-type check is worth pausing over. In Python, `bool` is a subclass of `int`, so `isinstance(True, int)` is true. A casual numerical guard would therefore admit `True + 2` and produce 3. The implementation uses `type(v) not in (int, float)` to reject that semantic impostor, and the research fixture observed the rejection. A JSON-facing description says "number"; Python still needs rules for the values it actually receives. The refusals are decisions about what the operation means, and they are yours: a specification that never mentions `True` gives an implementer, human or Claude, no reason to refuse it.

Finite numbers are another deliberate boundary. Infinity and not-a-number are floats in Python, but they are poor inputs for an addition tool whose output will be serialized as JSON and read as an ordinary answer, and finite inputs can overflow when added, so the result is checked separately. Validation is not decoration before the real work. It defines what the operation means.

<!-- [FIGURE: Cajal production brief. Validation separates proposals from execution. Include model proposal, schema gate, Python execution, tool result, bounded error. Show the confirmed relationship that unknown, extra, Boolean, non-finite, overflow reject. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Validation separates proposals from execution. unknown, extra, Boolean, non-finite, overflow reject.](../images/11-tool-use-and-verification-fig-01.png)
*Figure 11.1 — Validation separates proposals from execution*

## Dispatch belongs to the application

Why not let the model decide how to execute the name it proposed? Because that collapses description, authority, and implementation into one unreviewable gesture. An allowlist gives the application a closed set of operations. Exact argument rules narrow each operation further. Permissions can then be checked around the actual effect. Chapter 5 made the same point: who may do what is a human decision, and the allowlist is where it is written down.

In this lesson the effect is only arithmetic. A file tool's dispatcher would also resolve paths, compare the destination with an approved root, and distinguish reads from writes; a database tool's would restrict the statement type, credentials, and row count. Tool schemas help the model form usable proposals. They are not a substitute for these enforcement checks.

The dispatcher raises `ValueError` on bad proposals, but the surrounding result builder catches that expected failure:

```python
try:
    value = dispatch(block.get("name"), block.get("input"))
    row = {
        "type": "tool_result",
        "tool_use_id": identity,
        "content": json.dumps(value),
    }
except ValueError as exc:
    row = {
        "type": "tool_result",
        "tool_use_id": identity,
        "content": str(exc),
        "is_error": True,
    }
```

This conversion is a design choice with a reason. A rejected proposal is useful evidence for the next turn: the model can see that a particular request failed and why. The application does not pretend the tool ran, and it does not crash the whole conversation. Error becomes part of the protocol trace.

Notice what is not caught. `ValueError` represents a bounded, anticipated validation failure. The code does not catch every exception and relabel it as a tool error, because an unexpected programming defect should not be laundered into a routine model-visible message while the host continues in an unknown state. "Catch everything" is not verification.

## Identifiers create correspondence, not truth

A response may contain multiple content blocks. The `results` function walks the blocks and acts only on those whose type is `tool_use`. For each tool request it requires a nonempty string identifier that has not already appeared in that content batch. Then it returns a block whose `tool_use_id` repeats the request identifier.

The identifier answers a narrow question: which result belongs to which request? Without identifiers, an answer such as `42` could be attached to the wrong addition. With them, the application can state that result `42` corresponds to request `call-17-plus-25`.

But correspondence is not correctness. A result can be matched to the right request and still be wrong because the dispatcher contains a bug, the external service returned stale data, the request encoded the wrong task, or the evidence was interpreted too broadly. An ID is like a luggage tag. It helps establish ownership of the suitcase; it does not inspect what is inside. In the fixture every tag is attached correctly, and the claim at the end still disagrees with the result it is tagged to. That is "42 in the trace, 99 in the claim" at the smallest scale.

The course code checks duplicate identifiers within one call to `results`. If the content batch includes two tool requests both named `x`, the function raises `ValueError` before safely representing both results. The executed fixture observed this rejection. The research notes also preserve a limit: the `seen` set is local to one invocation. It does not establish global uniqueness across every turn in a conversation.

State the scope of a check in the same sentence as the check. "Duplicate identifiers are rejected" is too broad. "Duplicate identifiers within one processed assistant content batch are rejected" matches the implementation. Precision about scope prevents a small guard from acquiring mythical powers in later documentation.

Anthropic's tool-result handling guidance specifies how client-side `tool_use` blocks relate to subsequent `tool_result` blocks, including the request identifier and message ordering. That describes the interface contract. Your application still owns execution and the truth of the returned content. Consult the dated source in the closing note before implementing against a current API, because rolling documentation changes.

## The controller is a message machine

The `loop` function accepts a callable named `call`, a request body, and a bounded number of turns. Injecting `call` is what makes the controller testable offline: a fixture returns known response dictionaries, and optional live transport can use the same controller through a different callable. At setup, the function checks that `max_turns` is an integer from one through four, copies the messages list, and supplies the tool definition. The loop then requests a response and appends it to `trace`.

Each exit is a decision about what the loop may claim. There are three main exits:

1. If `stop_reason` is `end_turn`, return status `finished` with the trace.
2. If it is anything other than `tool_use`, return status `stopped`, preserve the reason, and include the trace.
3. If it is `tool_use`, build results, append assistant content followed by a user message containing those results, then continue, unless the turn budget is exhausted.

This controller does not treat every non-tool stop as success. The test fixture supplies `max_tokens`, and the test expects status `stopped`: a truncated response needs a policy decision, and presenting it as a completed answer would erase the reason execution ended. If the response claims to stop for tool use but contains no tool calls, the loop raises an error. Otherwise the assistant content is retained and the results are appended in the next user-role message, so the next model call sees both its requests and the application's responses.

A turn budget prevents unbounded continuation. It does not guarantee progress, since four repeated calls can consume it without moving the task forward, and it does not certify safety, since an unauthorized operation could be damaging on the first turn.

The word `finished` is also a choice. It names a controller state. Had the same state been called `verified`, downstream code would read the name and not the mechanism. Name each exit for the evidence behind it, and keep the word *verified* for a claim whose claim-specific check passed.

<!-- [FIGURE: Cajal production brief. Protocol completion is not factual verification. Include tool use, validate, dispatch, tool result, final claim, independent check. Show the confirmed relationship that the shortcut from narration to verified is invalid. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Protocol completion is not factual verification. the shortcut from narration to verified is invalid.](../images/11-tool-use-and-verification-fig-02.png)
*Figure 11.2 — Protocol completion is not factual verification*

## Worked example: 42 in the trace, 99 in the claim

We now reconstruct the recorded offline example. It uses scripted responses, not a live Claude transcript, so that controller behavior is isolated without spending API credits or pretending that model variability is evidence about the Python mechanism. One honesty note: the research run recorded the pieces separately, `results` on a good and a bad block (identifiers `good` and `bad`), the duplicate rejection, and a loop whose single scripted response says 99 and ends the turn. The two-turn trace below composes those pieces, and `sum-1` is an illustrative identifier.

First, consider a valid content block:

```python
valid = {
    "type": "tool_use",
    "id": "sum-1",
    "name": "add",
    "input": {"a": 17, "b": 25},
}
```

Predict the output before following the code. `results([valid])` sees a tool-use block, confirms that `sum-1` is a new nonempty string, and passes the name and input to `dispatch`. The keys are exact. Both values have exact type `int` and are finite. Python computes 17 + 25 as 42, which is finite. `json.dumps(42)` produces the string `"42"`. The result block is therefore equivalent to:

```python
{
    "type": "tool_result",
    "tool_use_id": "sum-1",
    "content": "42",
}
```

The research script executed this path and recorded 42 with matching identifiers. That observation supports claims about this implementation under this fixture. It is not evidence that every external tool call is correct, that Claude chose the right operands, or that the live API behaved in some unrecorded way.

Now change one boundary at a time. Replace `17` with `True`: the exact-type rule rejects it, and `results` converts the failure into a result tied to `sum-1` with `is_error: True`. Replace the tool name with `subtract`: the allowlist rejects it. Put two tool-use blocks with ID `sum-1` in the same batch: the duplicate-ID guard raises. The first two are per-call dispatch failures, represented to the model as `tool_result` errors, and the model may repair an invalid argument after receiving one. The third violates the association mechanism itself, so the implementation raises; ambiguous identity is a protocol integrity problem that no repair from inside the conversation can fix.

Next, supply the controller with two scripted responses. The first asks for the valid addition and stops for `tool_use`. The controller executes it and extends the outgoing history. The second response says, in effect, "The answer is 99," and carries `stop_reason: end_turn`.

What does the controller return? `finished`.

That status is correct about the controller and silent about arithmetic. It means the response used the controller's recognized completion signal before the request budget expired. It does not mean the final claim agrees with tool evidence. The fixture is deliberately wrong so that this boundary cannot hide behind a successful example.

We therefore add an independent check:

```python
expected = 17 + 25
claimed = 99
claim_verified = claimed == expected
```

The independently calculated expected value is 42, and the comparison rejects the claim. For such elementary arithmetic, a hand calculation is genuinely independent of the helper being audited. In a consequential system, independence should be designed around failure modes, not assumed. Calling the same buggy helper twice is repetition, not corroboration. Two routes that share the same incorrect source data are not independent merely because their code differs.

An evidence matrix makes the distinctions visible:

| Claim | Evidence present | What it establishes | Independent check |
|---|---|---|---|
| Claude proposed `add(17, 25)` | recorded `tool_use` block | request content and ID | inspect trace against task |
| dispatcher accepted the arguments | absence of dispatch error and returned value | local validation passed | boundary tests/code review |
| Python produced 42 | matching `tool_result` content | output of this implementation | hand calculation or separate derivation |
| result belongs to `sum-1` | matching identifier | request/result correspondence | trace invariant check |
| loop completed | `end_turn` and `finished` | controller recognized completion | inspect stop reason and budget |
| final answer is correct | not established by completion | nothing until compared | compare parsed claim with 42 |

The final row is the teardown. A polished sentence at the end of a correct-looking trace is still a new claim, and evidence does not automatically flow into narration. The application must constrain the final output so correspondence is checkable, parse and compare the claim, or present the evidence for a human decision. Which is appropriate depends on stakes and task semantics.

## When the report is accurate and the reader is still misled

Suppose the 99 had been 42. The final sentence would be correct, and a reader could still leave believing something the trace has not shown. The reason is scope. A tool result reports on an operation. A reader's sentence is about an outcome.

The companion book on computational skepticism makes the point with a case it labels a composite, not a sourced incident. A screening tool names the two features that drove its prediction. The radiologist checks that both are present in the image and concurs. The explanation was accurate about the model. It did not say that the model had learned a shortcut, so an accurate explanation made a wrong decision feel right. The book's name for the missing question is the audience question: who is reading this, and what do these words mean to them?

Apply it to the verbs your tools use. The `"content": "42"` row says an operation returned a value. A report that says *saved* tells the reader the file exists where they expect, with the content they meant, and will exist tomorrow; a successful write call establishes far less. *Deleted* may mean removed from this folder, from the repository history, or from every copy. *Sent* may mean handed to a mail server or received by a person. *Deployed* may mean uploaded or serving traffic. Each word is accurate in the operation's use and misleading in the reader's.

Before a report ships, write the inference the reader will draw from each verb. Then ask which observation would make that inference true. If no row in the trace supplies it, the report should say the narrower thing. In this chapter's matrix, that is the gap between "Python produced 42" and "final answer is correct".

## Verification surfaces for real tools

What would you have to see before you let a report say that a real tool did its job? Arithmetic is friendly: the intended operation and the independent answer are both clear. A file-writing tool exposes more layers. A successful write can establish that bytes were written to a particular resolved path at a particular time. It does not establish that the file satisfies the user's assignment, that another process did not change it afterward, that the repository contains the change, or that a remote copy exists. Verification might read the resolved target back, compare expected content, inspect `git diff`, run relevant tests, and check remote state separately if publication is claimed. Each check answers a different question, and "the tool returned success" is one item in that chain.

Other tools have the same shape. A row count describes the snapshot the query actually saw, an upload report can coexist with failing health checks, and a retrieved passage can be the most similar one without entailing the answer. Tool evidence is always evidence of something specific.

The design move is to make verification surfaces explicit at tool boundaries: return resolved paths rather than only friendly names, preserve query parameters, timestamps, and stable identifiers, and keep errors structured. Record enough of the trace to reproduce a decision without leaking credentials or restricted data, because tool arguments can contain personal information or secrets. The question is not "Can we save everything?" It is "What minimum evidence lets an authorized reviewer test the claim?"

## Common misconceptions, broken with counterexamples

**"If the schema is correct, invalid calls cannot happen."** The schema guides model output and may be checked by a platform, but the local runtime must defend its boundary. The Boolean fixture shows a Python-specific edge that a vague numerical assumption can miss.

**"A tool result proves the answer."** It proves only what the operation and its evidence support. If the operands were chosen from the wrong records, correct addition produces the wrong business answer.

**"Deterministic Python is infallible."** Python repeats its implementation consistently. The implementation can still encode the wrong formula, parse the wrong field, or use stale input.

## Building a reusable tool evidence matrix

Start with the final sentence you want to be able to say. Break it into atomic claims. For each claim, name the producing operation, the evidence artifact, the scope of that evidence, an independent check, and a failure response. If you cannot name a check that could reject the claim, the workflow is relying on assurance.

The order I want you to work in: decide which checks fail differently, write the gate, build your own baseline, conduct Claude Code against the gate, ship the matrix with a sign-off, then divide the work honestly.

### Choose checks by failure mode

"Independent" is easy to write and surprisingly difficult to design. *Conducting AI* states the rule that matters: using one tool to audit another reduces error only to the degree that the two fail differently. If two checks make the same mistake on the same input, combining them leaves the mistake where it was. Two chat models asked the same question can fail the same way because they learned from overlapping text, so having one check the other can produce agreement without verification. The book marks how far that goes as medium confidence, so hold it loosely. Its stronger advice does not depend on it: audit a generative claim with a non-generative tool. Deterministic code does not confabulate: it can be wrong, but it is wrong the same way on every run, so a test can find it. A lookup against a real source either finds the source or does not. A schema validator catches malformed structure however plausible the content reads. A model's verdict on quality is a verdict, not a verification. Chapter 1 quoted the companion book's line for this: an AI checking an AI is not a second opinion, it is the first opinion run twice.

Begin by listing how the producing route could be wrong. For the addition example, the request could contain the wrong operands, dispatch could map the name to the wrong operation, serialization could change the value, association could attach the result to the wrong ID, or narration could state a different number. A useful check crosses at least one of those boundaries by a different route. A hand calculation of 17 + 25 avoids the dispatcher and serialization path, but it does not establish that 17 and 25 were the intended operands. Inspecting the task against the request checks operand selection, but it does not recompute the result. Comparing the final claim to the returned result catches narration drift, but a shared wrong result can make both agree. No single check covers the entire chain.

This suggests a small design procedure:

1. Write the consequential claim in a form that can be false.
2. Draw the operations and transformations that produced it.
3. Name one plausible failure at every transition.
4. Select checks that enter the chain from different evidence sources.
5. Record shared assumptions that remain after the checks agree.
6. Decide in advance what disagreement will stop, retry, or escalate.

The last step prevents verification theater. If a checker disagrees and the controller simply asks the model to choose which number sounds better, the workflow has not used the check. It has converted evidence into another prompt. A stop policy makes disagreement operational.

Suppose a receipt tool returns a subtotal and Python recomputes the sum of its extracted rows. Agreement establishes internal consistency, but both routes share the extracted rows, so a missing row fools them together. Checking a sample against the source image fails differently, and human review may still be needed where handwriting or business rules make the interpretation ambiguous.

Verification also costs time, permissions, and attention, so tie depth to consequence and reversibility. A formatting preview may need a visual glance. A payment instruction needs identity, amount, destination, authorization, and post-action confirmation, available before the action and not bolted onto a celebratory report afterward.

### The gate: design the matrix before the run

This is the chapter's gate. Write it in your learner workspace before you ask Claude Code for anything, in plain sentences and one table. Name who decided each item. Here the lesson fixed the design, and everything after it is yours to write.

*Design.* One tool, `add`. Scripted fixtures, not a live session. Operands 17 and 25, and a scripted final claim of 99. A request budget of at most four. These are the lesson's choices; no model produced them. In your own matrix, the claims and the operands are yours.

*Contract.* `dispatch` accepts exactly the name `add` with exactly the keys `a` and `b`, each an `int` or `float` by exact type, finite, with a finite sum, and raises `ValueError` otherwise. `results` returns one `tool_result` per `tool_use` block, carrying that block's identifier; identifiers are nonempty strings, unique within the batch; an invalid proposal becomes a result with `is_error: True`. `loop` returns `finished` only on `end_turn`, returns `stopped` with the reason for any other non-tool stop, raises on a `tool_use` stop with no calls, and returns `budget-exhausted` when the budget runs out. None of that says the final sentence is true. That is a separate claim and it needs its own row.

*The matrix, filled in before anything runs.* Name the plausible failure at each transition, the check that enters by a different route, and what disagreement does:

| Transition | Plausible failure | Check that fails differently | If it disagrees |
|---|---|---|---|
| task to request | wrong operands | you read the request against the task text | stop; fix the request path |
| request to dispatch | wrong operation mapped; `True` accepted | boundary tests you wrote before reading the reference | do not run the tool |
| dispatch to result | wrong arithmetic; serialization changed the value | hand calculation or a separate derivation | treat the result as untrusted |
| result to request | result attached to the wrong ID | trace invariant: each `tool_use_id` appears once and matches a request | raise; do not continue |
| loop to status | `finished` read as success | inspect stop reason and budget | report the exit, not a verdict |
| narration to claim | final sentence differs from the result | parse the number; compare with the independent value | withhold *verified*; escalate to you |

*A wrong version your tests must catch.* Replace the exact-type test with `isinstance(v, (int, float))` and `True + 2` returns 3; the reference suite catches that one. Delete the duplicate-identifier guard, rename the `finished` exit to `verified`, or delete the overflow check, and all six reference tests still pass, because none of them sends a duplicate, reaches the `end_turn` exit, or adds two huge floats. Try each change yourself. A gate that does not name those cases will not catch them either. If your tests cannot tell these from the right program, the gate is not finished.

*What a failure looks like.* Write one sentence, dated, about what you would see if the matrix were wrong: a trace where the status is `finished`, every identifier matches, and no row can say no to the final sentence. Written after reading the output, it only describes the output.

*What this evidence may claim.* Protocol-level statements about this implementation under these fixtures, and equality between a parsed number and an independently derived one. It cannot say that 17 and 25 were the operands anyone meant.

Claude can sharpen the gate: ask it to find a transition you left without a check. It cannot write the gate for you without defeating its purpose, because the gate is where your decision about what counts as independent goes on the record.

### Build It: the baseline that lets you audit

Before you open the reference, write your own `dispatch`, `results`, and `loop` under `learning-artifacts/week-11/`: a one-tool allowlist, exact argument keys and numeric types, every `tool_use` block processed with the assistant content kept unchanged and user-role `tool_result` blocks appended, bounded turns, and an explicit stop on truncation and unsupported stop reasons. Trace one successful case by hand, marking the input boundary, the transformation, and the returned result. Trace one failure from the tests. Change one input at a time so an observed difference has an identifiable cause.

From the repository root, the reference demo and its six tests run offline:

```bash
python3 lessons/11-tool-use-and-verification/code/main.py
python3 -m unittest discover -s lessons/11-tool-use-and-verification/code/tests -v
```

The demo's scripted responses are fixtures, not evidence that Claude generated or verified anything, and the default commands neither read credentials nor make API requests. Read the six tests as six questions, not as "the code works": the happy path, an unknown tool, a Boolean, a preserved identifier, a represented error, and a truncated stop. Your own version is the baseline: the record of what you understood before Claude touched anything, and the instrument you will measure Claude's version against.

### Use It: conduct Claude Code against your gate

Now hand Claude the work it does well from a complete specification. Open Claude Code in your learner workspace; the lesson's [working prompt](../lessons/11-tool-use-and-verification/outputs/claude-code-prompt.md) is a reasonable start for the session. Give it the gate you wrote, the contract, the tests, and the matrix, and not your implementation. Ask for an implementation that satisfies the contract and passes your tests, then run your tests on what it returns, yourself.

Do four things with the result. First, note which of your tests failed, if any. A failing test is often a gap in your gate, which Claude cannot see because it only has what you wrote. Second, compare its implementation with your baseline and name one difference in behavior: a boundary it handled that you missed (a revision to your gate) or one it silently ignored (a defect your tests failed to catch). Third, ask Claude for a deliberately wrong version that still passes your tests, and check by hand whether it does. If it does, your test list was too weak, and you found out cheaply. Fourth, ask Claude to run the matrix's checks and log the commands, outputs, and versions in one place. It can do that quickly. The reason each check is independent of the route it checks is the column you write.

Preserve the actual transcript: your prompt, the plan, the diff, the commands, and the outputs, with the date and displayed model label. If a session failed or did not run, record that rather than substituting a fixture.

The reference also has an optional `--live` mode that connects the same dispatcher to the Claude Messages transport after you configure access. It can make up to four billable requests, and nothing here requires it. If you run it, recompute the result independently, record the interface and model actually used, and keep the live trace apart from the offline fixture.

### Ship It: the matrix, the trace, and the sign-off

Ship the tool schema, the validation rules, a valid and a rejected request/result trace, and the matrix, with exact commands and observed outputs. Identify which behaviors came from fixtures and which, if any, came from an explicitly authorized live run.

The matrix should also record what remains untested. The reference tests cover successful addition, an unknown tool, Boolean rejection, ID preservation, a represented tool error, and an unsupported stop reason. They do not prove global identifier uniqueness, security under hostile inputs, safe concurrency, durable logging, live service behavior, or correctness for a different tool. Add tests because a capstone claim needs them, not to inflate a count: a file-writing capstone might test traversal rejection and read-back. Preserve one failed case and the decision it changed, and keep the negative evidence. A rejected Boolean, a duplicate identifier, or a mismatched final claim shows that the boundary can say no; a system demonstrated only on its happy path has demonstrated production, not control. Record versions, because a result can change when code, model, schema, or source changes. When you add this artifact to the evidence trail for the Week 15 project, name which capstone claim it supports and what further review that claim still needs.

**The sign-off.** End the artifact with a statement you could put your name to. Claude can draft its words in seconds and the draft will be fluent, so write it from your record. This is the template, not a signature:

```text
Sign-off — tool trace and evidence matrix
Checked:      which matrix rows, by which check (name each)
How:          by hand / by a test I wrote before reading the reference /
              by a recomputation outside the controller /
              with Claude's help (say which parts)
Not checked:  whether 17 and 25 were the intended operands; global
              identifier uniqueness; hostile inputs; any live service;
              any tool but `add`
Not claiming: that any final sentence is true because the status read
              `finished`, or that a matching identifier verifies content
Signed or withheld: ____________  (name, date)
```

Chapter 10's sign-off covered a plan, which is a prediction. This one covers a record of what ran, so it may say what was *recorded*, *computed*, and *tested*. *Verified* is for a claim whose check came from outside the route that produced it. The "Not checked" line does the work. It is the line a drafted sign-off is least likely to include, because the draft has no record of what you did not run. If your evidence does not support signing, withholding is an honest result.

### The driver's seat

This is how the chapter's work divided, task by task. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Proposing a call from a task | Propose the name and arguments as structured data | Decide which operations exist and what the dispatcher refuses | Capability is a grant of authority; the allowlist is policy, not syntax |
| Writing the contract and the matrix | Challenge it: find a transition you left unchecked | Write it first, with a failure per transition | The gate is your decision on the record |
| Implementing `dispatch`, `results`, `loop` | Implement from your contract, fast, and propose extra tests | Build your own baseline first, then run your tests on its version | You cannot audit a boundary you never broke |
| Running and logging the checks | Run them, diff outputs, log commands and versions | Say which check is independent of which route, and what disagreement does | Independence depends on where each route's inputs came from, which the log does not show |
| Wording the report | Draft it; flag an overclaim | Choose the verb; sign or withhold | Your name is on the claim |

The row to look at is the fourth. Claude can compute both routes. Whether two routes share an input, a source, or an assumption is a fact about your data and your task, and a transcript of both routes does not display it. Record in the artifact one check Claude ran and logged and one independence judgment you made, in your own words. If you cannot point to the log line and the sentence, the split happened in your head and not in the record.

## Integration with the agent built so far

Chapter 4 supplied the bounded controller, Chapter 5 separated capability from authority, Chapter 8 exposed request identity and result messages, and Chapter 10 required a plan to stay auditable as execution diverges. Tool use brings them together: a planned step becomes a model-proposed request, validation decides whether the application may dispatch it, execution produces an observation, and verification compares consequential claims with evidence outside the model's narration.

Keep the layers separate in code. A model adapter should not silently gain filesystem authority. A dispatcher should not decide that a business outcome is satisfied merely because a function returned. A presentation layer should not omit errors to make the report cleaner. Separation gives reviewers places to disagree with the system, and it gives you places to put a gate.

Read the trace against the plan you approved in Chapter 10: the plan predicted a call, and the trace records what happened. Design-first does not mean frozen. If a check disagrees, or Claude finds a case your contract missed, reopen the gate, change it, and record that you did. A revised gate with a dated reason is evidence of control. A gate quietly edited to match what the code does is the failure the sign-off exists to prevent.

## Verify and reflect

Verification begins with a claim small enough to test: the rejection of a Boolean, the preservation of an identifier, the exit taken on `max_tokens`, or the equality between a parsed claim and 42. Name which matrix row each check addresses. Pick one passing case and explain it from input block to returned content without reading Claude's explanation, and pick one rejected input and explain why the refusal belongs to the contract. Then inspect the strongest sentence in your report. If it says *verified*, point to the check that came from outside the route.

The most useful reflection is local. Which distinction did you originally collapse? Identity and truth? Completion and verification? Deterministic and infallible? Repetition and independence? Name the input or the check that separated them again. That is a concrete habit to carry forward, in place of the generic resolution to be more careful with AI.

## Assessments — ungraded practice

These are ungraded practice. Preserve predictions, commands, outputs, and revisions; do not submit solutions inline with the prompts.

### Warm-up

1. **Trace association — introductory; objective: understand request/result correspondence.** Given two valid `tool_use` blocks with different IDs, write the expected result-block shapes without executing Python. Then run the function and compare. Name the invariant the IDs establish, and one thing they do not.

2. **Classify claims — introductory; objective: analyze what evidence supports.** Label six statements as request, validation, execution, correspondence, completion, or verification claims. For each, name the smallest evidence that could support it, and say which of the six your matrix would leave without a check from a different route.

3. **Predict a Python boundary — introductory; objective: apply exact-type rules.** Predict outcomes for integer, float, Boolean, infinity, missing-key, and extra-key inputs. Run each case one change at a time and explain any mismatch with your prediction.

### Application

4. **Mixed batch — intermediate; objective: apply per-call error handling.** Construct one assistant content batch containing a valid call and an invalid call with distinct IDs. Verify that both receive associated results and that only the rejected operation carries `is_error`.

5. **Duplicate identity — intermediate; objective: analyze a protocol guard.** Construct a duplicate-ID batch and record the observed failure. Explain why this implementation raises rather than returning two ambiguous results, and state the scope of the guard precisely. Then write the test the six reference tests lack, and show that it fails when you delete the guard.

6. **Stop-reason audit — intermediate; objective: apply exit semantics.** Create fixtures for `end_turn`, `tool_use`, and `max_tokens`. Trace each controller exit and write a sentence that describes its status without implying factual correctness.

7. **Capstone boundary tests — intermediate; objective: create tests from a contract.** Add one meaningful success and two failures for the tool used in your capstone. Write them before you ask Claude for any implementation, and justify the cases from the harm or confusion they could prevent.

### Synthesis

8. **Evidence matrix — advanced; objective: evaluate a chain of custody.** Build a matrix for one real capstone claim. Write the plausible failure at each transition first, then separate proposal, validation, authorization, execution, return, narration, and independent check. Identify the first unsupported transition.

9. **Different failure route — advanced; objective: evaluate independence.** Design an independent check for your tool result. Explain which failure modes it does not share with the original route and name at least one assumption both still share. Say which part of the check Claude may run and log, which judgment about independence you keep, and why.

10. **File-write transfer — advanced; objective: transfer the method.** Adapt the arithmetic trace conceptually to a file-writing tool. Specify the evidence needed to distinguish attempted write, successful write, correct content, committed change, and published repository state, and write the "Not checked" line you would put in its sign-off.

### Challenge

11. **Verified completion policy — stretch; objective: design a gated status.** Design a controller extension that may return `verified` only after a claim-specific checker passes. Include behavior for an unparsable final claim, checker failure, budget exhaustion, and a tool result whose content cannot safely be logged. Say who may override a failed checker and what that person must record. Test at least one false-positive risk in your design.

After completing the practice, use the existing [Lesson 11 knowledge check](../lessons/11-tool-use-and-verification/quiz.json). Answer before reading its feedback; it is for self-review, not a separate graded exercise.

## Capabilities summary

You can now read a tool loop as a chain of separately testable claims. You can explain why Claude proposes structured calls while Python owns validation and execution, and you can write the contract that says what the dispatcher refuses before anyone implements it. You can preserve request/result identity without mistaking identity for truth. You can treat stop reasons as controller signals, bound continuation, and keep expected tool failures visible. Most importantly, you can place an independent check between a fluent final sentence and the word *verified*, say which checks Claude ran for you and which judgment of independence stayed yours, and sign a report only as far as its record supports.

## Anthropics

Anthropic's official [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) guidance describes client-tool request/result association and message construction. Compare the current guidance with the course implementation, especially the use of `tool_use` identifiers, matching `tool_result` blocks, and ordering in the next user message. The page was retrieved for the research packet on 2026-09-06; treat it as rolling documentation and check it again when implementing against the live API.

Anthropic's public [tool-use course](https://github.com/anthropics/courses/tree/master/tool_use) offers upstream examples for comparison. Run upstream notebooks only as an explicit optional extension. The course's offline Python mechanism and your Claude Code account are sufficient for the required learning path; direct API credits are not required.

## Computational Skepticism

The body used the companion book's audience question from its discussion of [explanation and verification](../docs/computational-skepticism.md#explanation-and-verification). Its chapter on agents adds a diagnostic the body has not, in [agent outcomes](../docs/computational-skepticism.md#agent-outcomes). Of any check or defense that held, ask: under what condition would this have failed? If you cannot name the condition, you have not validated it. You have observed that this time nothing went wrong. The same chapter's false-success catch says to observe the world's state independently of the agent's report.

Apply both to your matrix. For every row where the independent check agreed with the claim, write the condition under which it would have agreed anyway: the same operands, the same extracted rows, the same source. A row with no such condition named is a row you observed, not one you checked. The book's agent studies are exploratory (one framework, one lab, two models, two weeks), so take the question from them, not rates.

## Conducting AI

The body used the lowest-capability rule from [verifiability first](../docs/conducting-ai.md#verifiability-first). The book's account of [explicit handoffs](../docs/conducting-ai.md#explicit-handoffs) adds the diagnostic the body has not: laundering, an unverified value gaining authority as it passes through clean steps. Trace the 42 through its seams: the dispatcher's return, `json.dumps`, the `tool_result` content, the assistant's sentence, the row in your matrix. At each seam write what is passed, what it is trusted to be, and how that trust was earned. A typed field, a serialized string, or a row that says "Python produced 42" makes a value look checked. Polish is not provenance.

Then place the gate where the claim first enters, which in this chapter is the request, not the report. A check at the last seam cannot catch a wrong operand chosen at the first. The conductor's work is choosing the routing and defining what evidence must cross each seam. The model can make the performance fluent; fluency alone cannot show that it was correct.

## Forward bridge

Today, 42 is supported by a recorded operation and an independent calculation. Tomorrow, a memory system may retrieve “42” after the operands, source, code, or task have changed. A verified result is not permanently verified in every future context. Carry your sign-off forward; its date and versions are there for this reason. Chapter 12 asks what has to travel with memory so that recall does not turn yesterday's evidence into today's unsupported confidence.
