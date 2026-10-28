# Chapter 2 — Prompt contracts and evaluation
*A valid answer-shaped object can still be wrong.*

The research fixture contains a source with one sentence: “The color is blue.” Its identifier is `s1`. A response arrives saying that the fixture says red, and it cites `s1`. The response passes our validator. Nothing crashed. The program returned exactly the result its rules required. The failure is not hidden in an exotic model behavior. It sits in the distance between what the validator checks and what a reader might assume its green result means.

So the question for this chapter is narrow and practical. When a program says an answer passed, exactly which obligation did it pass, and who decided that obligation was the one that mattered?

This is an executed, constructed counterexample, not a transcript of Claude making a mistake. The [research output](../research/worked-examples.json), under `chapters.02`, preserves three responses and their acceptance results. The first is not JSON. The second cites an unknown identifier. Both fail. The third is properly shaped and cites a known identifier, so it passes even though its claim contradicts the supplied sentence. The format-pass rate is one-third. Calling that an accuracy score would misname the measurement.

Chapter 1 gave you three jobs and a device for each: conduct, with the gate; check, with the sign-off; drive, from the driver's seat. This chapter runs the same three at a larger boundary. A sampler chose an index. Now a contract accepts or rejects a whole answer. The gate becomes a contract plus an evaluation set, written for the program that will consume the answer before you try a single prompt. The check becomes the discipline of naming what a pass covers and what it leaves out. The drive is the part no schema holds: deciding what “acceptable” means for this consumer and this claim.

Claude is strong on the near side of that boundary. Give it a complete contract and it can write the validator, enumerate malformed inputs, draft prompt variants, and tabulate pass rates faster than you can read them. The far side is a different kind of question. Whether the answer follows from the sentence it cites is a verification question, and a check run by the system that produced the answer is not independent of it. *Conducting AI* makes the general point in its chapter on the solve-verify asymmetry. Producing an answer and verifying it are different operations, and asking the generator to vouch for itself is more of the first operation, not a second opinion. The book states its strongest version of that claim as a wager, not a proven fact, and it notes that when verification works, the grounding often lives in a tool a person chose. I use the part that survives the caveat: a trustworthy check fails differently from the thing it checks, and choosing that check is a human decision.

Keep the third response in view while we build the chapter. Structural checks are valuable. Structural checks are not source understanding.

The exercises continue to assume Claude Code access, as established in Chapter 1 and the [access guide](../docs/neu-claude-access.md). The validator and constructed response set run offline in Python's standard library and require no direct API credits. When you later use Claude Code to compare actual prompts, save the real responses separately from these fixtures. A locally constructed string is useful test data; it becomes misleading only when presented as an observed model response.

## What you will be able to do

You should be able to write, before any prompt is tried, a contract for the program that will consume an answer: the object it accepts, what it refuses, an evaluation set split into development and held-out cases, and the evidence criterion you will apply. You should be able to implement that contract's validator, trace the rule that rejects an input, and say which obligation a passing response satisfied and which it never faced. You should also be able to compute a pass rate and state its scope, construct an example that passes the format check while failing a separate evidence check, and report the two results in separate columns.

You should also be able to do three things the rest of the book builds on. Conduct Claude Code against your own gate and run your own tests on what it returns. Write a sign-off that claims no more than your record supports. And say which parts of this chapter's work you handed to Claude, which you kept, and why the question of what counts as acceptable stayed with you.

The prerequisites are Chapter 1, Python dictionaries and lists, and the distinction between JSON text and the Python object produced by parsing it. The paired [lesson](../lessons/02-prompt-contracts-and-evaluation/docs/en.md) provides runnable instructions and the existing knowledge check. Build your initial validator in your learner workspace before consulting its reference, and write down the expected result for each test input first. A prediction gives you something to learn from when the code surprises you.

## The gate: write the contract for the consumer first

The first decision is not what to say to Claude. It is what the program receiving Claude's answer needs, because that need is the only criterion that exists before an output does.

Suppose, as a hypothetical workflow, another Python function will consume the answer. It expects an object with an `answer` string and a `sources` list. If the response arrives as a paragraph, a Markdown table, or a JSON list with no named fields, the consumer does not have the interface it was promised. A human might infer the intended meaning. The program should not depend on that generosity.

Order matters, and it is the chapter's Conduct lesson. If you write the prompt first and tune it until the output looks right, the contract becomes whatever the output happened to look like, and every later pass rate measures agreement with your own habituation. If you write the contract first, the criterion exists before the output does. Claude implements well against a complete specification; an incomplete one it may quietly fill with something plausible instead of flagging the gap. So completeness is your job, and the prompt is derived from the contract, not the other way around.

Start from the consumer's need. It needs a nonblank answer. It needs at least one source identifier. It needs those identifiers to belong to a supplied set. For this teaching contract it accepts exactly two keys, not two required keys plus arbitrary extras. That last choice is the kind a schema cannot make for you. A response containing `answer`, `sources`, and `confidence` fails this validator even if all three values look reasonable. A consumer that assumes a fixed shape finds the rule protective, because unexpected additions become visible instead of silently ignored. An exploratory analysis that wants extensible metadata finds the same rule an obstacle. The trade-off is strict predictability against accepting some useful objects, and you cannot call it good or bad without naming the downstream job. Choose your contract for your consumer, not because a short teaching function happened to choose one.

Notice, too, what the contract is not. The prompt requests behavior from the producer. The validator checks the returned object against executable conditions. Adding “always obey the schema” to a prompt is not equivalent to checking the schema after the response arrives. The request can be ignored or misunderstood; the local check has a definite acceptance rule. This is Chapter 1's point about the system prompt, one level up: a request is a hope, and a check is a gate.

Here is a baseline request derived from the contract. It is a proposal for an experiment, not a proven improvement:

```text
Answer the question using the supplied source material.
Return a JSON object with exactly two keys: answer and sources.
answer must be a nonblank string.
sources must be a nonempty list of identifiers from the supplied sources.
Do not add text outside the JSON object.
```

It states an output contract and an evidence intention. The executable function will enforce only part of that intention. It knows which identifiers are allowed; it does not understand whether the answer follows from their contents. Make that asymmetry visible now, before a passing response encourages you to forget it.

You may want the prompt to say what to do when the sources do not answer the question. That is a legitimate design question, and it exposes a limit. The reference requires a nonblank answer and a nonempty source list. It has no field for insufficient evidence. Try the constructed response `{"answer":"The sources do not say.","sources":["s1"]}`. The validator accepts it, exactly as it accepted the false claim, because it cannot tell an honest refusal from an assertion. Adding a `status` field will not help, since the validator rejects the extra key. Whether a refusal is an acceptable answer, and how the consumer should see it, is a decision about the interface. If you redesign the contract, record the redesign and test it as a different version. “Be accurate” in the prompt does not supply a refusal state.

None of this makes the design waterfall. A finding like this one can reopen an earlier decision. When it does, record the change: a new contract version, new tests, and any case that guided the redesign counts as development evidence from then on.

Write the decisions down before running anything. This is the book's second gate, and it has the same shape as the first.

*Consumer.* One sentence naming the program that reads the answer and what it does with it. For each line below, note who decided it: you, or a fixed requirement of the consumer. For the teaching contract the choices are mine, made before any prompt; no model produced them.

*Contract.* Exactly the keys `answer` and `sources`. `answer` is a nonblank string. `sources` is a nonempty list of strings, every one in the supplied identifier set. Text outside the JSON object is a rejection, not something to repair silently. The validator returns a decision, not a diagnosis.

*Evaluation set.* Five development questions and five held-out questions, listed and dated before any response is inspected. The held-out list is sealed: not shown to Claude, and not used to revise the prompt, until the revision is frozen.

*Evidence criterion.* For each question, one sentence saying what “supported” means for it, and a third recorded outcome, “cannot be reviewed,” beside supported and contradicted. *Computational Skepticism for AI* has a version of this: record pass, fail, or unknown against a criterion fixed before you read the output. Write it before you know which prompt wins.

*Wrong versions your tests must catch.* A validator that checks only that the keys exist. One that accepts a source list when any entry is known, where the contract says every entry. One that skips the nonblank check. And the response that is well formed and wrong, the color fixture, which no validator test will catch and your evidence column must.

*What a failure looks like.* For each held-out question, one sentence describing an answer that would pass the validator and fail the evidence criterion, written and dated before you see a response. If you write it afterward, you have described the output, not tested your understanding.

*Pass condition.* The gate is finished when every line of the contract has a named test that fails if the line is deleted, when both question lists are dated, and when each held-out question has its failure sentence. If you cannot write that sentence, you do not yet know what you are checking for.

*What this experiment may claim.* Acceptance by a stated validator of recorded responses, and a separate support judgment on the claims you reviewed. It cannot say that any answer is correct beyond those reviewed claims.

Claude can sharpen the gate. Ask it for the malformed input your list lacks, or the contract line your tests do not defend. It cannot write the gate for you without defeating its purpose: the gate is the criterion fixed before the output exists, and a criterion drafted after the outputs arrive is a description of the outputs.

## What each line of the validator promises

A pass is only as meaningful as your ability to list what it checked. So the decision this section informs is a reading decision: when the function says `True`, which obligations is it vouching for? Read the [reference implementation](../lessons/02-prompt-contracts-and-evaluation/code/main.py) with that list in hand.

```python
import json

def validate(text, source_ids):
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return False
    return (isinstance(data, dict) and set(data) == {"answer", "sources"}
            and isinstance(data["answer"], str) and bool(data["answer"].strip())
            and isinstance(data["sources"], list) and bool(data["sources"])
            and all(isinstance(s, str) and s in source_ids for s in data["sources"]))
```

`json.loads` runs first and can fail before any field rule is relevant; the string `not json` is the first research fixture and takes that route to rejection. A successfully parsed value is not automatically the right kind of value, so the dictionary check comes next, then the exact key set, and only then the field values. The order avoids treating every parsed value as if it were already the object we wanted.

The answer must be a string. The integer `1` fails even though a human could display it as text; the function does not coerce. `strip()` removes surrounding whitespace for the nonblank check, so a whitespace-only answer fails. The sources field must be a list, the list must not be empty, and every entry must be a string that belongs to `source_ids`. The word every matters: one valid identifier cannot compensate for another invalid entry. The expression does not compute a fraction of acceptable references and decide that most is good enough.

The function collapses every rejection into `False`. That is an intentional simplification, and worth judging. A Boolean is convenient for a pass rate and easy to test; it tells a reviewer nothing about how to repair a response. A richer result naming the parsing failure, key mismatch, wrong type, or unknown source is a reasonable extension to your own version, not a behavior to attribute to the reference. The absence of a message is not the absence of a reason: for each failing fixture, stop at the first relevant boundary and name it. “The AI output was bad” is not precise enough to guide a repair.

Now ask what defends each line. The [six lesson tests](../lessons/02-prompt-contracts-and-evaluation/code/tests/test_main.py) exercise a valid object, invalid JSON, a wrong-typed answer, an unknown source, an extra key, and the empty-experiment rule in the rate function. Each is evidence for one behavior, not for the function. Predict, then check: in a scratch copy of `main.py`, change `all` to `any`, and rerun the six tests. Then, in separate copies, delete the nonblank check and delete the nonempty-source check. All six tests still pass for each of those three edits. The contract promises three behaviors that the lesson's tests never defend. This is the practical meaning of “the tests pass”: they pass for the behaviors they exercise. Your additional tests should target such a gap, chosen by reason, not another example of the happy path.

The function's size is an advantage for this teardown: you can inspect the whole acceptance rule at once. If someone tells you it verifies source support, ask them to point to the comparison between source content and answer content. They cannot, because `source_ids` supplies identifiers, not passages.

## A source identifier is an address, not an argument

The research fixture makes the limit concrete. The source mapping is:

```python
source_text = {"s1": "The color is blue."}
```

The validator receives the allowed identifier set, `{"s1"}`. It does not receive the source sentence. That design lets it reject an invented address such as `missing`, but it cannot decide whether the words attached to `s1` support the answer. Membership in a registry and support for a proposition are different relations.

Consider the accepted response exactly as the research records it:

```json
{"answer":"The fixture says red","sources":["s1"]}
```

The object has exactly the two required keys. The answer is a nonblank string. The sources field is a nonempty list whose one entry is a known string. Every implemented condition is satisfied. The fact that the source sentence says blue does not enter the calculation.

This is why the counterexample is stronger than a vague warning about hallucination. We know which check is absent, and we can trace why the response passes without speculating about model internals. The validator is not broken. It succeeds at enforcing its stated structural and identifier contract. It fails only if someone misrepresents that contract as a complete evidence check.

There are two distinct questions in the review. Does the referenced source exist in the supplied collection? Does that source support this particular claim? Passing the first makes the second possible; it does not answer it. An address can point to a real document while the accompanying summary misstates it. The address remains useful because it gives the reviewer somewhere to look.

Who answers the second question? Claude can be asked to set the two sentences side by side, and for a case this small you can verify the comparison at a glance. But if the system that produced the answer is also the only reviewer of its support, you have the first opinion run twice. For the color fixture the evidence is the sentence itself, and you can read it. A request for a brief explanation with cited evidence makes an answer easier to inspect, yet the explanation is still output to evaluate. Do not request hidden chain-of-thought or treat an articulate rationale as access to an authenticated internal process. What you need is a reviewable claim, the referenced material, and a short justification that can be checked against that material.

<!-- [FIGURE: Cajal production brief. Format validity and source support are independent. Include constructed response, format check, source-ID check, source-content check, unsupported claim. Show the confirmed relationship that known citation does not entail support. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Format validity and source support are independent. known citation does not entail support.](../images/02-prompt-contracts-and-evaluation-fig-01.png)
*Figure 2.1 — Format validity and source support are independent*

Give each component a named responsibility and do not let its success signal be promoted into a broader guarantee. The validator owns structural acceptance. The evidence review owns a support judgment within a stated scope. The experiment report owns the record of what was tested. A single confident sentence should not impersonate all three.

## Work through the three-response experiment

Before reading the results, write your predictions. Use the source identifier set `{"s1"}`. Predict the validator's decision for each constructed string, and, separately, what a reviewer holding the sentence would say. Do not base the third validator prediction on whether the answer is true; base it on the function we just read.

```python
responses = [
    'not json',
    '{"answer":"x","sources":["missing"]}',
    '{"answer":"The fixture says red","sources":["s1"]}',
]
```

For the first response, parsing fails and the exception path returns `False`; none of the dictionary-field checks runs. For the second, parsing and shape checks succeed, but `missing` is not in the supplied identifier set, so it also returns `False`. For the third, all implemented checks succeed and the result is `True`. The observed acceptance sequence in the saved execution is false, false, true. The rate function is short enough to inspect directly:

```python
def pass_rate(responses, source_ids):
    if not responses:
        raise ValueError("An empty experiment has no pass rate")
    return sum(validate(r, source_ids) for r in responses) / len(responses)
```

Each accepted response contributes one and each rejected response contributes zero. There is one acceptance among three responses, so the result is `1 / 3`, represented in the saved JSON as `0.3333333333333333`. The denominator is the number of supplied responses. The function does not know how they were selected or whether they represent any broader population.

That last point is easy to lose in a report. These three cases were constructed to expose three boundaries. They are not a random sample of Claude's production behavior, and no model was called to generate them. One-third describes acceptance of this fixture set by this validator. It estimates nothing about how often a real service will make these mistakes.

The empty-input rule is a design choice with interpretive consequences. With no responses, the function raises an error instead of returning zero or one. Zero could be mistaken for a tested system that failed every case; one could be mistaken for perfect performance. The reference refuses to assign a pass rate to an experiment with no denominator, which makes absence of evidence harder to disguise as a performance number.

Now put the validator's decision beside the review a reader would make. The review column below is my judgment on three constructed strings; a different task would need its own definition of supported.

| Response | `validate()` | Obligation failed or passed | Support review |
| --- | --- | --- | --- |
| `not json` | False | Failed at parsing; no later rule ran | Cannot be reviewed: there is no claim to compare |
| `{"answer":"x","sources":["missing"]}` | False | Parsed and shaped correctly; failed source membership | Cannot be reviewed: the cited address resolves to nothing |
| `{"answer":"The fixture says red","sources":["s1"]}` | True | Passed every implemented condition | Contradicted by `s1`: “The color is blue.” |

Do not invent one numeric evidence score merely to make the table symmetrical. Decide how unsupported, contradicted, and cannot-be-reviewed results are represented before summarizing them. Format accepted and evidence contradicted is not an inconsistent report; it is the expected report for the third row.

The third row is the one to stare at, because a green result has a fluency of its own. *Computational Skepticism for AI* calls the general hazard the fluency trap: the more fluently an output presents, the more confident you become in it, and then in your own evaluation of it, and form and content are independent. A `True` is a verdict in the shape of a settled question. The book's defense is the one the gate builds in: define the failure condition before you read the output, test against evidence, and record pass, fail, or unknown. Its remark about cost fits here too. Producing outputs is cheap and verifying them is not, and if verification is not budgeted it does not happen. The validator is the cheap check. The support review is the expensive one. The risk is that the cheap check's green is reported as if it were the expensive one's.

If you later replace the constructed strings with actual Claude responses, the same calculation applies, but the provenance changes. Preserve the exact prompts, source materials, interface, model label, and date. A fixture evaluation demonstrates validator behavior. A recorded model experiment examines returned outputs under its recorded conditions. Both are useful, and they must stay distinguishable in the artifact.

## A prompt revision is a hypothesis

The decision here is what you are allowed to conclude from changing a prompt. The paired lesson asks you to compare a baseline prompt and a few-shot revision on five development questions while keeping five additional questions held out. Those numbers define a manageable classroom experiment, not a claim that ten questions establish broad reliability. What makes an improvement measurable at all is a fixed evaluation set; without one, “better” is a feeling.

Write the baseline, the source boundary, and the intended output contract. Then predict a specific failure the revision might address. Perhaps the baseline does not produce the required object shape, and you hypothesize that examples will help. That is a testable proposal, not a result because adding examples sounds like established practice.

Make the revision differ in a way you can describe. If you simultaneously add examples, change the task, alter the source material, introduce a persona, and simplify the questions, any observed difference becomes hard to attribute. A controlled comparison does not require pretending the rest of the world is fixed. It requires recording what you changed and limiting the explanation to what that design can support.

Development questions are available while you revise. Preserve their failures rather than showing only the final success. Held-out questions are reserved before you inspect results. Once a held-out case has guided a choice, its role has changed: it is development evidence now. That is not a moral failing; it is bookkeeping. Record the change, and if you need another untouched check, design a new evaluation instead of relabeling the old one.

Specify the evidence criterion before you see which prompt performs better, or you may tighten or relax what a pass means to favor the output you prefer. Our executable format rule is one fixed criterion. The support review needs an equally explicit question, such as whether each stated claim is supported by the supplied material, with a documented way to handle insufficient evidence.

A persona is a hypothesis to test. “You are an expert” is part of a prompt; it adds no supporting passage to the source collection and changes none of the validator's checks. If a persona helps on your cases, describe the observed difference and the conditions, and do not let the role label certify the answer before the evidence review begins.

Claude Code can organize the experiment, run your local validator, draft candidate prompts, and challenge your interpretation. Keep four things visibly separate: the proposed prompt, the actual returned text, the executable acceptance result, and your evidence judgment. If you have not run the comparison, your artifact should say proposed experiment. A complete-looking results table with invented outputs is worse than an honest plan.

## What a pass rate leaves out

Suppose a report contains only the sentence “The revised prompt achieved a higher pass rate.” Which validator? Which cases? How many responses? Were the cases used during revision? Did the accepted responses remain supported? Did a formatting improvement coincide with an evidence failure? Without those details the number is hard to use responsibly.

The rate also compresses different failures into one total. A response that is not JSON and a response with one unknown source identifier both contribute zero, yet their repairs differ. Counting failures is useful for summary; preserving categories is useful for diagnosis. The compact reference returns a Boolean, but your experiment record can retain the more detailed interpretation without pretending the function supplied it.

It also weights every response equally. The reference has no notion of which question matters more, which claim is consequential, or which failure should stop a workflow. Equal weighting is simple and transparent; it is not a discovered statement that every case has equal importance. If your application needs another policy, justify it openly instead of hiding it in the aggregate. And a format pass does not establish completeness: a nonblank answer can be short, irrelevant, or evasive and still satisfy the string check.

None of this is a reason to abandon the check. It is a reason to name the check accurately and pair it with the review the task needs. The practical test: could a reader reconstruct how the reported number was produced? If so, the statistic has a mechanical meaning even if its scope is narrow. If not, it may be functioning as decoration. This chapter's strongest demonstration is not a spectacular success rate. It is a correctly interpreted mixed result: two known failures rejected, one semantically false claim accepted, and all three outcomes explained.

## Build It: your validator is the baseline

Write your first validator from the stated contract, not from the reference. Make the parsing boundary explicit, decide how a failure will be represented, then implement the shape, answer, and identifier checks. Do not begin with a framework or another model call. The standard-library version is short enough for you to explain completely, and that explanation is the capability being built. As in Chapter 1, your own version is the record of what you understood before Claude touched anything, and the instrument you will measure Claude's version against.

Read the six lesson tests before the reference and predict each result. Then add tests that defend the lines the six leave open. For each, state the defect it exposes and one different defect that could still survive it, and prove the test works by running it against a scratch copy with that line removed. A larger test count is not coverage.

Next, deliberately construct the valid-but-unsupported response. If your implementation rejects it, inspect why. Perhaps you accidentally added a semantic rule, or perhaps its structure does not match the contract. The goal is not to force every learner implementation to share the reference's limits forever; it is to distinguish an added check from a mistaken explanation of the existing one. If you extend the interface with a status field or a diagnostic object, keep a separate version and test the extension, documenting both the benefit and the migration cost. Do not modify the reference and then cite its old tests as if they validated the new behavior.

## Use It: conduct Claude Code against your gate

Now hand Claude the work it is good at. Open Claude Code in your learner workspace. Give it the gate you wrote, the contract and the test list and the fixtures, and not your validator. Ask for an implementation that satisfies the contract and passes your tests. Then run your tests on what it returns, yourself.

Do three things with the result. First, note which of your tests failed, if any; a failing test is often a gap in your gate, because Claude had only what you wrote. Second, compare its validator with your baseline and name one difference in behavior: a boundary it handled that you missed, which revises your gate, or one it silently ignored, which your tests failed to catch. Third, ask Claude for three plausible-but-wrong validators, one for each contract line you suspect is under-defended, and run your tests against each. A wrong version that survives is a hole in your gate that you found cheaply. Whether your tests are enough cannot be judged by the system they are testing; that check is yours.

Then run the experiment the lesson describes. Give Claude the baseline prompt and the few-shot revision on the same five development questions. Ask for a short explanation and cited evidence, not hidden chain-of-thought. Save failures as well as successes. Run your validator on every response, then do the support review yourself, claim by claim, against the source text, using the criterion you wrote in the gate. Reveal the held-out questions only when your revision is frozen, and record that you did.

Finally, once you have written your explanation of the results, ask Claude which claim in it is stronger than the executed check, then inspect its criticism yourself. An AI reviewer can surface a useful issue, but its agreement is not a second source for the sentence in the fixture.

Preserve the actual transcript: your prompts, the plan, the diff, the commands, and the outputs, with the date and displayed model label. If a session failed or did not run, record that; do not substitute a fixture.

## Ship It: an experiment another person can audit

The artifact is a prompt experiment containing baseline and revised prompts, development and held-out cases, raw responses, validation results, and a change log. Its purpose is to let another reader reconstruct both the mechanics and your decisions. The [artifact brief](../lessons/02-prompt-contracts-and-evaluation/outputs/artifact-brief.md) names the repository expectations; keep course grading logistics outside this reading chapter.

Preserve each response before editing or repairing it. If Claude produces surrounding prose that makes the strict contract fail, do not remove that prose and score the repaired string as though it arrived that way. Record the original and the repaired version with their roles separated. If Claude helped with a repair, record that as a transformation, not as part of the original run. A text wrapped in a code fence or introduced by a sentence fails `json.loads`, and whether your consumer should tolerate that is a contract decision you made in the gate, not a convenience to grant after the fact.

Keep the baseline intact and name the change in the next version. “Improved prompt” is not a change log. State which instruction, example, or boundary changed, why you expected it to matter, and what the development results showed. If the revision did not help, that is still an informative result when the trail is intact.

For the integrated evidence review, take one accepted answer and compare each meaningful claim with the supplied source material. Mark unsupported content separately from formatting status. In the tiny fixture the contradiction is explicit. In your task, a passage may support only part of an answer, and one correct citation must not stand in for a claim-by-claim explanation. Then write a limited conclusion. You might conclude that a revision changed format acceptance on the recorded cases while leaving a particular source-support failure unresolved. That tells the next person what to reuse and what remains risky.

**The sign-off.** End the experiment with a statement you could put your name to. Claude can draft its words in seconds, and the draft will be fluent, so write it from your record. This is the template, not a signature:

```text
Sign-off — prompt experiment
Checked:      validate() decisions on N recorded responses (name the cases);
              claim-by-claim support review of M accepted answers against
              the supplied sources
How:          validator tests I wrote before reading the reference; support
              review by hand against the source text; with Claude's help on
              (say which parts)
Not checked:  held-out cases I tuned against; claims in answers I did not
              review; wordings of the prompt I did not try; any other model,
              date, or interface
Not claiming: that the format pass rate measures accuracy, that the revision
              is better in general, or that an accepted answer I did not
              review is supported
Signed or withheld: ____________  (name, date)
```

Choose the verbs to match the record. The rate was *computed* and the decisions *recorded*; support was *reviewed* for the claims you reviewed; nothing here was *established* beyond that. If the support review is unfinished, write pending. A missing review silently replaced by an automated pass is the failure this chapter is about, and withholding your name is an honest result.

## The driver's seat: what counts as acceptable

Every consequential setting in this chapter was a judgment that no field in a schema could hold. Whether the consumer tolerates extra keys. Whether “the sources do not say” is an acceptable answer. Whether a response with one correct citation and one unsupported claim passes. Whether equal weighting is right when one question carries the stakes. What “the same meaning” requires when a prompt is reworded. The validator can enforce a decision once it is made; it has no way to make it. Claude can lay out the options and the consequences of each, quickly. What it lacks, in this task, is the consumer, the stakes, and a person who bears the cost of a wrongly accepted answer, and none of that is in the files it reads unless you put it there. That is why the first line of the table below belongs to you.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Say what the consumer needs and what acceptable means | Challenge the contract: find an input it admits that the consumer cannot handle | Decide, first, and record who decided each line | The consumer, the stakes, and who bears a wrong accept are outside the files Claude sees |
| Implement the validator from a contract | Implement it, fast; propose malformed inputs and wrong versions | Build your baseline first, then run your tests on its version | You cannot audit a rule you never wrote |
| Draft prompts and tabulate pass rates | Draft variants, run the validator, tabulate | Choose the one feature that changes; fix the development and held-out lists before looking | The split is a promise about what you will not look at, and only you can keep it |
| Judge whether an answer is supported | Lay the claim beside the source; propose a verdict | Make the call, claim by claim, against the source itself | A check run by the generator is the first opinion run twice, and “supported” is your definition |
| Say what the pass rate supports | Flag an overclaim | Choose the verb; sign or withhold | Your name is on the claim |

Record, in the experiment, one task you delegated and one judgment you retained. If you cannot point to the transcript line or the edit that shows each, the split happened in your head and not in the record.

## Verify and reflect

Run the local demo, the six tests, and your additional tests. Preserve actual outputs. Then rerun the constructed three-response experiment and explain why its one-third result is a format rate. The [research script](../research/worked_examples.py) and [saved output](../research/worked-examples.json) provide the reference evidence for the published example. Your own execution should be labeled as your run, with its own environment record.

Review the experiment's provenance as carefully as its arithmetic. Which strings did you construct, and which came from an actual Claude interaction? Which questions guided revision, and which were still held out when you inspected the result? These distinctions change what you can conclude even when the same function calculates every rate.

Then name a judgment the validator cannot make, and say how you made it or why it is still pending. A report can be incomplete and honest; it becomes misleading when a missing review is replaced with an automated pass. The most useful reflection is local, not a resolution to trust AI less: which distinction did you collapse? Source membership and source support? A format rate and an accuracy? A development case and a held-out one? Name the counterexample that separated them again.

## Assessments — ungraded practice

These Assessments carry no points. Use the lesson's existing [knowledge check](../lessons/02-prompt-contracts-and-evaluation/quiz.json) and preserve your answers before viewing its explanations. Complete the following in your learner workspace. Label constructed fixtures, actual responses, predictions, and review judgments separately. No paid API experiment is required to practice the contract mechanics.

### Warm-up

1. **Locate the first boundary — introductory; objective: trace validation.** Choose three inputs: malformed JSON, a parsed value of the wrong shape, and an object with the correct keys but a wrong field type. Predict each result and identify the first relevant rule. After running, explain the difference between a parser failure and a contract failure without describing both merely as bad formatting.

2. **Exactly means exactly — introductory; objective: explain a design choice.** Construct an otherwise acceptable answer with one additional field. Predict the reference validator's result, then verify it. Explain one hypothetical consumer for which this strictness is useful and another for which it might be inconvenient, and name who in a real workflow would decide. Keep those scenarios labeled hypothetical; do not claim the exercise establishes a universal schema policy.

3. **Name the fraction — introductory; objective: calculate a scoped rate.** Reproduce the three-response fixture and compute the rate from its individual decisions. State the numerator and denominator in words. Explain why the number is not a measure of factual accuracy or a frequency estimate for Claude behavior. Describe what the empty-experiment exception prevents a reader from mistakenly concluding.

### Application

4. **A line no test defends — intermediate; objective: implement meaningful coverage.** Choose a contract line that none of the six lesson tests defends. Write the test, state the defect it exposes, and prove it fails against a scratch copy with that line removed. Explain one different defect that could survive it. Do not equate a larger test count with complete coverage.

5. **A legitimate address, an illegitimate claim — intermediate; objective: separate membership and support.** Construct a short source and an answer that cites its valid identifier while contradicting its content. Preserve the executable decision and a separate evidence judgment using supported, contradicted, and cannot be reviewed. Explain why the two results differ. Keep the example explicitly constructed rather than presenting it as something Claude actually said.

6. **A gate before a baseline — intermediate; objective: design a prompt intervention.** Write the gate first: consumer, contract, evidence criterion, and a failure sentence for each held-out case. Then write a baseline request for a bounded source-grounded task and a revision that changes one identifiable feature, and predict which failure the change should address. Prepare five development cases and five additional held-out cases before examining responses. Note which part Claude drafted and which you decided. If you do not run the comparison, submit the design as a proposed experiment, not a completed evaluation.

7. **Do not repair the observation away — intermediate; objective: preserve provenance.** Take one failing fixture or actual recorded response and make a corrected version. Keep both. Run the validator on each, describe precisely what changed, and explain why scoring only the corrected version would answer a different question. If Claude helped repair it, record that assistance as a transformation rather than attributing the repaired text to the original run.

### Synthesis

8. **Two columns, one honest conclusion — advanced; objective: integrate evaluation.** Build a report that preserves format acceptance and source-support review separately for your chosen cases. Define how you represent a result that cannot be reviewed. Write a conclusion that distinguishes a formatting improvement from any unresolved evidential problem, and finish with the sign-off. Ask a reviewer to identify a sentence that overstates the data, then assess the criticism yourself.

9. **The held-out boundary — advanced; objective: critique experimental design.** Describe a hypothetical revision process in which a developer repeatedly tunes against the supposedly held-out cases. Identify the point at which the label becomes misleading. Propose a revised record and evaluation plan that acknowledges what was inspected. Do not solve the problem by simply renaming the same final score independent evidence.

### Challenge

10. **Design an insufficiency state — stretch; objective: redesign a contract.** In a separate learner version, propose an explicit way to represent insufficient source evidence. Explain who decides whether a refusal counts as an acceptable answer, how your change affects the current exact-key and nonempty-source rules, what the consumer must now handle, and which tests are needed. Do not claim that the reference already supports your new interface. Compare the simplicity you lose with the ambiguity you remove.

11. **Meaning-preserving change — stretch; objective: specify robustness.** Prepare three paraphrases of one task while keeping its intended facts and obligations fixed. Predict what should remain invariant and what may legitimately vary, and say who decided where that line falls. If you run the prompts, compare format, claim content, and support separately. If you only design the test, label it accordingly. Explain why different wording in an answer is not automatically a failure of the intended task.

## What you can now inspect

You can look at the validator and name the job of every condition. Parsing, object shape, exact keys, answer type, nonblank content, source-list type, nonempty membership, and allowed identifiers are separate obligations, and you can say which of them the lesson's tests defend and which they leave open. You can explain a rejected response by locating the failed condition, and you can propose a targeted test rather than relying on an undifferentiated impression of output quality.

You can also explain the more uncomfortable case. A response can satisfy every implemented condition and still contradict its source, and the color fixture reproduces it. The right response is neither blind acceptance nor dismissal of automated checks: keep the structural check, name its scope, and add the evidence review the task requires. You can compute a pass rate with its denominator and provenance visible, and keep an observed output distinct from its later repair.

And you can say what the three jobs look like at this scale. You conducted: you wrote the consumer's contract, the evaluation set, and the evidence criterion before any prompt was tried, and you held Claude's validator to your tests. You checked: you named the obligation each pass covered, kept format and support in separate columns, and refused to let a rate stand for more than it measured. You drove: you handed Claude the implementation and the drafting, kept the definition of acceptable, the support judgment, and the verb, and signed or withheld.

## From acceptable text to consequential action

Our current consumer accepts or rejects a response object. It does not execute the answer. Suppose a later system can read files, write changes, or request a tool call. A correctly shaped answer now sits near an action boundary, and the distinction we practiced becomes more consequential: passing an output contract does not establish permission to perform the requested action.

Chapter 3 separates interfaces by tracing what they can actually do. We will examine a small capability classifier for reasoning, reading, and writing, then resist treating its names as a complete taxonomy of AI systems. A mode label is no more an authorization policy than a source identifier is proof of support. The gate you write there is a different one: how much autonomy is sufficient, chosen before the capability is granted.

Bring the prompt experiment forward as an evidence pattern. Keep the input, executable rule, output, and remaining judgment visible. When an action appears, add its required capability and its consequence to that record. The question changes from “Can my program consume this object?” to “What could happen if it does?” A well-designed contract helps expose that transition; it cannot make the transition harmless by itself.

## Anthropics

Anthropic's [Prompt evaluations course](https://github.com/anthropics/courses/tree/master/prompt_evaluations) includes separate material on human-, code-, and model-graded evaluations. The repository overview was checked on 2026-09-06. Use that separation to compare your small executable format check with the source-support judgment it leaves outside its scope; do not infer that our few lines reproduce the upstream evaluation system.

After completing your build, choose one upstream evaluation approach and state which question it could help investigate in your artifact. Explain what evidence would justify adopting it and what it would still not establish. Older model identifiers, additional tools, and API-based examples in upstream material do not become requirements for this Python-and-Claude Code exercise.

## Computational Skepticism

In the companion's robustness chapter, I use meaning-preserving changes as a diagnostic question: what should stay the same when expression changes but the intended task does not? See [Prompt sensitivity](../docs/computational-skepticism.md#prompt-sensitivity) for the specific chapter and passages. The body above checked a prompt against its cases; this note asks whether a result survives rewording of the same case. The book's own example pairs “List the key points of this document” with “What are the main takeaways from this document?” and treats stability under that kind of rephrase as the property worth testing. It also bounds the claim: what carries over between domains is the diagnostic question, not one shared attack mechanism, and this exercise proves no broad theory of model understanding.

Apply it to one held-out task. Before running anything, specify the invariance you require: different organization or tone may be acceptable, while an altered fact or omitted constraint may not be. Write three paraphrases that hold the facts and obligations fixed, and lock your prediction of which checks will pass. Then compare three columns separately, format validity, claim content, and support. Notice which column moved. A paraphrase that changes only the format column is a different finding from one that changes the claim. If you use the paraphrases to revise the prompt, acknowledge that they have become development evidence. Skepticism here is a precise question attached to a record, not a general instruction to distrust every answer.
