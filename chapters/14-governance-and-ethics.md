# Chapter 14 — Governance and ethics

Every field is filled. Nobody is responsible.

That sentence is possible because a governance record can be structurally complete and operationally hollow. The field named `owner` can contain `"project team"`. The incident contact can say `"project owner"`. The evaluation can say `"citation audit"`. Python can truthfully report `ready-for-human-review`. Yet no named person may have accepted responsibility, no affected person may have been consulted, no threshold may trigger a response, and no one may know what happens when the system causes harm.

So the question for this chapter is not whether the register is complete. It is what "complete" is standing in for. When the status turns green, what has been decided, who decided it, and who will answer for it when the system causes harm?

Claude will fill that register for you in seconds. It will propose an owner, a threshold, a retention period, and a paragraph on risk, all fluent and plausible. It cannot make anyone the owner it names, it was not in the room with the people the workflow touches, and nothing in its draft makes it answerable for the workflow after the conversation ends. That is the book's division of labor at the scale of a team. You conduct: owners, thresholds, retention, consultation, and recourse are designed into the system before it ships, and the register with its validator is the gate. You check: a register can be complete, reviewable, and still weak. You drive: relationships, consent, and recourse are people's work.

The course fixture is deliberately modest. It checks seven required fields, validates a nonnegative retention-day count and a list of data-class strings, and routes unknown or sensitive classes and external writes to review. It is useful precisely because we can see where it stops. It makes missing governance information visible; it does not grant ethical clearance.

This chapter tears down the distance between a register and a responsible team. Governance is not prose wrapped around a technical system. It is the assignment of decisions, evidence, authority, relationships, monitoring, recourse, and response. Applied ethics begins when those abstractions are attached to people who can be affected and people who must act.

## What you will be able to do

By the end of the chapter, you should be able to:

- trace the exact structural checks performed by the course register, and distinguish `ready-for-human-review` from approval, consent, compliance, or ethical acceptability;
- conduct: write the gate for a team register before it is filled (owners, thresholds, retention, consultation, and recourse, each with the person who decided it), then run your own tests on a validator that Claude Code implements against that gate;
- check: identify affected people and concrete harms rather than generic "risk", find the weak line in a complete register, and say who bears each kind of error;
- design retention, deletion, access, incident, and appeal paths that end at a responsible human;
- drive: say which work you handed to Claude and which you kept, recognize when a workflow should be narrowed, deferred, or not automated, and end the register with a sign-off that claims no more than your evidence supports.

You should have completed Chapters 5, 12, and 13 on authority boundaries, shared memory, and approval gates. This narrative is paired with the runnable [Lesson 14 materials](../lessons/14-team-governance-and-ethics/docs/en.md). The Python example is an offline teaching mechanism, not legal advice or a compliance determination.

Before reading the implementation, make four predictions. What issues will an empty record report? Will `retention_days=True` pass as one day? What happens if `data_classes` is the string `"public"` rather than a list? Does `ready-for-human-review` mean a human has reviewed the record? Preserve the answers.

## Who decided? Five choices that exist before the form does

Five decisions sit under every register, and none of them is a drafting problem.

*Owner:* who accepts responsibility for the workflow as a continuing system, and what are they allowed to stop? *Threshold:* which observable signal triggers a response, and what is the response? *Retention:* which copies exist, for how long, and how is deletion checked? *Consultation:* who was asked, what could their answer have changed, and what is still pending? *Recourse:* how does an affected person reach a human who can change the outcome?

Each is an assignment of authority, and an assignment exists only when someone accepts it. Claude can draft all five in a minute. It cannot accept any of them for you, and it cannot tell you which of its drafts describe something real. So the order of work matters: people make these decisions first, and the form records them. A team that fills the form first has produced the shape of a decision, not a decision.

There are two gates in this chapter, and they fail differently. The validator is a machine gate: its pass condition is a list of tests you can run. The register's content is a human gate: its pass condition is that a named person accepted each role and that the routes work when someone uses them. The validator is evidence for the first gate only. Treating it as evidence for the second is the failure the opening sentence describes.

## The gate: write the governance before the form is filled

Do this in your learner workspace, in plain sentences, before you ask Claude for anything. It is this chapter's gate.

*Design.* For your capstone workflow, write one sentence for each of the five decisions above and, beside it, the name of the person who made it. Where no person has accepted a decision, write "unresolved" and say what the workflow is constrained to until someone does: a private draft, synthetic data, no external write. These are your choices. No model can know which of them are real.

*Contract for the validator.* A record with nothing in it reports all seven field names and the status `incomplete`. The demo record returns `ready-for-human-review` with no issues. With every field present, a negative retention count raises `ValueError`, and so does a string where a list of data classes belongs. A class outside `public`, `synthetic`, and `internal` returns `review-required`. A truthy `external_write` adds `external action approval`. Add two tests of your own: a meaningful success outside the demo, and a failure that would matter in your capstone.

*A wrong version your tests must catch.* Replace the exact-type test on retention with `isinstance(days, int)`. Python treats `True` as an integer, so `retention_days=True` now passes as one day, and the lesson's six tests still pass against that variant; run them and see. Replace the omission check with a falsiness test and a retention of zero, a legitimate design intent, is reported as missing; one of the six tests catches that one. If your test list cannot tell the right program from both wrong ones, the gate is not finished.

*What a failure looks like.* Write one sentence, dated, about what you would see if the register were hollow although the validator is green. For example: you send the named incident contact a labeled test report and nobody acknowledges it within the stated time. Written after you read any output, it describes the output instead of testing your understanding.

*What this register may claim.* That the record has a minimum shape, and that named people accepted named roles on named dates. It cannot say the workflow is ethical, consented to, or compliant.

Claude can sharpen the gate by hunting for the case you missed. It cannot write the gate for you without defeating its purpose: the gate is where your decisions go on the record, and it is what you will test Claude's validator against.

## A register makes questions inspectable

The implementation declares seven required fields:

```python
FIELDS = (
    "owner",
    "purpose",
    "data_classes",
    "retention_days",
    "approver",
    "evaluation",
    "incident_contact",
)
```

Each field opens a governance question.

The owner is accountable for the workflow as a continuing system, not merely its initial code. Purpose bounds why the system exists and reveals later use beyond that scope. Data classes describe what information crosses the boundary. Retention days make storage lifetime discussable. The approver identifies the decision route. Evaluation names the evidence used to judge performance and failure. The incident contact gives people somewhere to report a problem.

The fields are necessary prompts, not sufficient answers. `owner: "someone"` occupies the field without assigning work. `purpose: "use AI"` does not bound use. `evaluation: "test"` does not say which outcomes were tested. A register can force omissions into view, but Python cannot infer substantive adequacy from truthy strings.

The first operation in `assess` constructs a missing list. A field counts as missing if its key is absent or its value is `None`, the empty string, or the empty list. An empty record therefore reports all seven field names. The executed research fixture observed that seven-item omission report.

Other weak values can pass this particular missing check: whitespace, zero in most fields, an empty dictionary, or a vague string. Later specialized checks catch some shapes, but the boundary remains structural. A register should not advertise more intelligence than its validator contains.

<!-- [FIGURE: Cajal production brief. A complete register is only ready for review. Include owner, purpose, data classes, retention, approver, evaluation, incident contact. Show the confirmed relationship that field presence is not clearance. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![A complete register is only ready for review. field presence is not clearance.](../images/14-team-governance-and-ethics-fig-01.png)
*Figure 14.1 — A complete register is only ready for review*

## Tear down the validator

The design choice in this validator is worth naming before the lines: it refuses only what it can refuse exactly. A validator that tried to judge `"project team"` would need a list of bad owner names, and lazy entries step around such lists. The exactness is honest. The cost is that the hard part, deciding whether a line is true, is left to people.

After missing-field detection, retention receives an exact-type and range check:

```python
days = record["retention_days"]
if type(days) is not int or days < 0:
    raise ValueError("Retention must be a nonnegative day count")
```

Exact `int` typing rejects Python Booleans, even though `bool` subclasses `int`. Negative values fail. Zero is allowed and can represent a design intent such as no post-processing retention, but the implementation does not enforce immediate deletion or define transient copies. A number in a record is not evidence that the lifecycle follows it.

Data classes receive a shape check:

```python
classes = record["data_classes"]
if not isinstance(classes, list) or not all(
    isinstance(item, str) for item in classes
):
    raise ValueError("Data classes must be a list of strings")
```

The value must be a list and every element must be a string. The missing check already rejects an empty list. A single string `"public"` fails because iterability is not the same as the declared container shape. But any string inside the list passes this shape check, including unknown labels.

The next comparison creates a small classroom allowlist:

```python
if set(classes) - {"public", "synthetic", "internal"}:
    issues.append("sensitive or unknown data review")
```

Anything outside those three labels produces a review issue. The code does not decide whether an unknown class is legally sensitive, nor whether all "internal" information is safe for the proposed workflow. It chooses the conservative routing action: when the machine cannot tell, send the decision to a person. The trade-off is noise; the allowlist is case-sensitive, so a capitalized `"Public"` also goes to review.

If the optional `external_write` value is truthy, the function adds `"external action approval"`. The fixture test confirms this issue appears. The check does not identify the external target, authenticate approval, or execute Chapter 13's fingerprint gate. It marks a condition that needs another control.

The return status is `review-required` when issues exist and `ready-for-human-review` otherwise. Both lead to people. "Ready" means the teaching record cleared these structural checks and contains no flagged class or external-write condition. It does not mean "approved."

## Complete, reviewable, and still weak

The demo supplies:

```python
record = {
    "owner": "project team",
    "purpose": "summarize public course notes",
    "data_classes": ["public"],
    "retention_days": 30,
    "approver": "instructor",
    "evaluation": "citation audit",
    "incident_contact": "project owner",
}
```

No required field is absent or one of the explicitly empty values. Thirty has exact type `int` and is nonnegative. `data_classes` is a list whose only item is a string, and `"public"` is in the classroom allowlist. There is no truthy external-write flag. The executed fixture returns:

```python
{"status": "ready-for-human-review", "issues": []}
```

This result is accurate about the function. It is weak as governance evidence, and the check that reveals it is a question the validator cannot ask: who confirmed each of these lines, and how? "Project team" may name no accountable individual. "Instructor" may describe a role without proving that a particular instructor accepted this approval responsibility. "Citation audit" leaves the sampling, checker, criteria, and failure response unstated. "Project owner" may be unreachable to affected people. Thirty days says nothing about caches, backups, exported artifacts, or deletion verification.

Now run `assess({})`. The result is `incomplete` with all seven field names in `issues`, a useful negative case: the validator can expose total omission. Set `data_classes` to `["personal"]` with other required values present and the status becomes `review-required` with the sensitive-or-unknown issue. Set `external_write=True` on a public-data record and the external-action issue appears. These cases demonstrate routing. They do not demonstrate agreement by named people, stakeholder consent, lawful processing, effective mitigation, or outcome fairness. The research packet records precisely that boundary.

Construct a substantively weak but structurally complete variant:

```python
weak = {
    "owner": "everyone",
    "purpose": "help",
    "data_classes": ["public"],
    "retention_days": 99999,
    "approver": "manager",
    "evaluation": "looks fine",
    "incident_contact": "team",
}
```

The current function can return `ready-for-human-review`. That is not a defect relative to its narrow contract; it is a counterexample to broad claims about the status. The human review must interrogate meaning. Claude can list the vague lines; you must confirm each against the world.

An evidence table keeps the distinction visible:

| Register observation | What it supports | What remains open |
|---|---|---|
| seven fields present | minimum record shape | adequacy and acceptance |
| retention is nonnegative integer | declared day count has valid shape | actual deletion lifecycle |
| classes are known labels | no unknown label under course allowlist | classification accuracy |
| external-write issue | routing trigger detected | target, authority, outcome |
| ready for human review | structural preflight completed | consent, ethics, compliance |

Use the verb the evidence earned. The function *reported* that seven fields were present and well shaped and that nothing flagged review. It did not confirm, accept, or verify anything. When you describe a register line, use the weakest verb your evidence supports: *listed* when a name appears, *confirmed* when that person told you they accept the role, *exercised* when you ran the route and watched it work, *verified* when you inspected the store yourself. This ladder is a teaching device for this chapter, not an industry standard, but it makes hollow lines hard to hide. Most of a first-draft register sits at *listed*, and the "Not checked" line of the sign-off at the end of this chapter is where those lines go.

## Who bears the error

Generic risk language protects the record from falsification. "There may be bias or privacy concerns" can be pasted into almost any register and tells no one what to do. Applied ethics asks who can be affected, through which mechanism, with what consequence, and whether they can contest it.

For a public-course-note summarizer, affected groups may include students whose work is quoted, instructors whose policies are paraphrased, maintainers who must correct errors, and readers who rely on the summary. Concrete harms might include misrepresenting a deadline, exposing a student's attributed work, omitting a required accommodation route, or publishing an unsupported instruction. Each has a person who pays for it and, usually, a different person who could have prevented it.

Ask distribution questions. Who receives the benefit? Who bears false positives and false negatives? Who has to spend time correcting the system? Who is absent from the development examples? Who can opt out? Who is exposed when data is retained? Who can reach a human when the output is wrong?

Now compare two agents with the same measured accuracy on the same bounded evaluation set. Agent A reads public notes, creates a local draft, retains inputs for one day, and requires human publication. Agent B reads internal records, publishes externally, and retains complete traces for a year. Equal accuracy does not produce equal risk. B has a broader action surface, more sensitive context, a longer privacy exposure, and external effects, so its rollback and incident needs differ. Accuracy describes selected outputs under selected trials; governance describes the surrounding power and consequences. That is why ethics cannot be appended after model selection: architecture choices (data minimization, authority, retention, reversibility, review routing) shape the harm surface before the first score is calculated.

Equal accuracy can hide a second difference. Suppose, as a constructed case, two summarizers make the same number of deadline errors on the same bounded set. One errs by stating a deadline its sources do not support. The other errs by leaving the deadline out when sources conflict. The accuracy figure is identical, and the people who pay are not: students who plan around a wrong date bear the first error; students who must ask, and the maintainers who field their questions, bear the second. Nothing in the accuracy number says which error the team should prefer. That is a choice about whose cost counts, and someone makes it whether or not they notice.

The companion book on computational skepticism makes this point formally for systems that rank or evaluate people. Three reasonable fairness definitions (equal rates of favorable prediction across groups, equal error rates across groups, and scores that mean the same thing for every group) cannot all hold when the groups' base rates differ (short of perfect prediction); the book works the arithmetic in a few lines, following results credited to Chouldechova and to Kleinberg, Mullainathan, and Raghavan. Its conclusion is the useful part: each definition is a values claim about which error or which equality matters, so choosing one is a decision with an owner, not an optimization. Its worked case is a criminal-sentencing risk score where two parties reported accurate numbers and disagreed about which numbers should count. The disagreement was about values, not data.

Apply that only where the task supports it. If your workflow ranks people or allocates opportunity among them, defend a criterion and its trade-offs. If it does not, as with a note summarizer, do not invent demographic columns to look rigorous; name the harm mechanism the workflow actually has and ask the same question in that form: which error will we risk, and who pays?

In either case the book asks for a defended choice as the deliverable: the deployment and who bears the cost of error, where the options conflict, which you chose, why, and what evidence would change your mind. And it asks who should have decided: not whoever's loss function happened to encode a default, but the party accountable for the policy the tool serves. In the book's words: "Someone always decides. The only question is whether they did it on the record." The register is where a team does it on the record.

## Owners, thresholds, and bounded responses

The decision here is what signal the team will act on, who may act, and what acting costs. A mitigation without an owner is a wish. An owner without authority or resources is a label. A threshold without an observable signal is prose.

Rewrite "monitor quality and intervene if needed" into an operational record. For example: "The content owner reviews every unsupported-source flag before publication. If any public draft contains a deadline claim without an approved source identifier, publication pauses, the incident contact examines affected drafts, and work resumes only after correction and a repeated citation audit."

This statement names a signal, threshold, owner, response, scope, and recovery condition. It can still be improved (what counts as approved, how quickly review occurs, who handles disagreement), but another person can now test whether the process ran. That is the standard for a threshold: a stranger can tell, from the record, whether it fired.

Thresholds should connect to harm, not only aggregate performance. A 99 percent pass rate can conceal one severe disclosure. Some events require immediate stop on a single occurrence; others justify trend monitoring. Give the owner explicit authority to pause, because if incentives punish delay and only reward shipping, a nominal incident contact cannot govern. Define escalation when the owner is unavailable, implicated, or lacks expertise, and avoid assigning every role to one person merely to complete the form.

<!-- [FIGURE: Cajal production brief. Governance turns an incident signal into accountable response. Include incident signal, threshold, named owner, pause authority, bounded response, recovery check. Show the confirmed relationship that unresolved authority stops the flow. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Governance turns an incident signal into accountable response. unresolved authority stops the flow.](../images/14-team-governance-and-ethics-fig-02.png)
*Figure 14.2 — Governance turns an incident signal into accountable response*

## Retention is a lifecycle

`retention_days: 30` is a policy input, not a deletion mechanism. The decision is how long, and the check is what you actually inspected. Trace every copy: incoming prompt, local fixture, application log, model-provider handling under the applicable service, cache, exported report, repository history, backup, and incident record. Include only systems actually in scope and mark unknowns.

For each data class, state why it is collected, the minimum needed, who can access it, when the clock begins, how deletion is performed, and how deletion is checked. Derived summaries may still reveal source information, and a hash can itself be sensitive if it enables matching against a small known set. Zero-day retention needs clarification: it may mean delete immediately after the task, do not persist application data, or retain only de-identified evidence, and temporary memory and provider-side processing still exist. Do not turn a desired policy into a claim about systems you have not inspected.

Retention competes with incident replay. Keeping everything forever makes investigation easier and privacy risk worse; keeping nothing may prevent accountability. Design a minimal, separated audit record: operation identity, policy decision, safe evidence references, error category, and responsible roles, with sensitive payloads stored only when justified and protected.

Test deletion like any other behavior. Insert a labeled fixture, run the lifecycle, and inspect the stores you control. State what remains unverified. "Removed from this dictionary" is not "erased everywhere." In the verb ladder, the stores you inspected are *verified*; the provider's and the backups' are, at best, *listed*.

## Consultation and recourse are people's work

Everything so far a team can draft, compute, and review. This part it cannot hand over, and it helps to be exact about why. In *Irreducibly Human* I argue that social intelligence is built and exercised between people who have something at stake with each other, and that a system that produces the words of attention is not thereby in a relationship with anyone. That is a philosophical argument, and you do not need to accept it to follow this chapter. The operational version needs no position on machine minds: a reply that Claude generates in the voice of an affected student is not a statement by that student, and consent is something a person gives. Whatever Claude writes, someone still has to ask the actual person, hear the answer, and stay reachable afterward.

### Design consultation that can change the project

Consultation begins before the conversation. Decide who is affected directly, who maintains the surrounding work, who has relevant domain knowledge, and who is routinely missing from design decisions. Do not ask one convenient person to stand in for every stakeholder. Participation should be voluntary where appropriate, and the team should explain what will be recorded, how it will be used, and whether declining has consequences. Consultation counts only if the answer could have changed the purpose, boundaries, retention, or the decision to automate; if the team asks only how to make a predetermined deployment more acceptable, participation becomes theater.

Claude can help prepare a plain-language explanation: what the workflow receives, what it produces, where a person decides, what is retained, and how to report a problem. A human must check that explanation against the real system before sharing it, because fluent simplification can omit precisely the external write or retention detail a person needs. And questions should invite disagreement. "Does this helpful tool sound good?" solicits reassurance. Better questions ask what outcome would be unacceptable, what information should never enter the workflow, what correction process would be usable, and what would make the person withdraw support. Do not promise that every request will be adopted; explain how conflicts and decisions will be recorded.

During the conversation, listen beyond the prepared categories. A student may care less about summary accuracy than about being quoted without context. A maintainer may worry that an appeal route creates unpaid support work. An instructor may distinguish public course content from student submissions even when both sit in one repository. Those situated distinctions can change data classes, access, purpose, or the decision to proceed. Afterward, separate actual statements from AI summaries, return a summary for confirmation when appropriate, and record concrete design changes and unresolved concerns. If someone withdraws permission for their contribution, the retention and deletion process must know which artifacts derived from it.

A classroom role-play is useful rehearsal. It can reveal unclear explanations and missing questions. Label every response as simulated, because invented agreement is not consent, and let the register say which real consultation remains pending and which actions are prohibited until it occurs.

### Recourse is a system path, not an email address

An incident contact field often becomes an inbox nobody owns. Build the entire path. A reporter needs a discoverable channel and a description of what information is helpful without being forced to expose more private data. The team needs an acknowledgment rule, triage owner, urgent-stop trigger, investigation access, correction authority, and escalation when the first contact cannot resolve the issue.

Different harms need different remedies. Correcting a displayed summary does not repair a decision already made from it. Removing personal data from the active store does not recall a public copy. Explaining a model's reasoning does not restore an opportunity denied to someone. Ask the affected person what meaningful correction looks like, while recognizing that institutional constraints may require additional decision makers. Test the route with five questions: can a person challenge a result, obtain an explanation appropriate to the decision, reach a human who can correct the record, see downstream copies updated, and appeal beyond the original owner?

Make contestability practical. Preserve the contested output, input provenance where lawful, applicable policy, and the human decision record. Give the reviewer power to change the result, and provide a second route when the original owner is conflicted. State response times only when the team can meet them. Do not make the affected person debate a model: Claude can assemble the two passages in dispute, but it cannot accept institutional responsibility or repair a relationship, so a reachable human must own the response. Then close the loop into engineering. If the same class of report recurs while only the explanation template changes, the process is absorbing complaints rather than controlling the system.

### Worked incident rehearsal

Use a labeled fixture: a course-note agent publishes a summary stating the wrong assignment deadline. The register listed public data, a citation audit, an instructor approver, and an incident contact. Structurally, it was ready for review. The harm mechanism is reliance on a wrong deadline; students may allocate work incorrectly. This is a simulated response sequence, not a claim that an actual incident occurred. Do not invent stakeholder testimony, distress, permission, or successful repair; a rehearsal tests the route and does not prove people trust it.

Detection occurs when a student reports a mismatch with the official schedule. The observable trigger is a published deadline claim whose cited source does not support it. The content owner pauses publication of affected summaries and captures the source identifiers, generated output, approved proposal, and publication evidence. Investigation finds that the citation audit checked whether a citation string existed, not whether the cited passage entailed the deadline. The mitigation did not address the harm.

Notice what that finding does to the design-first rule. The register was written before the system shipped, and the incident reopens one of its decisions: the evaluation line. Design before implementation is not a freeze. A later finding can send you back to an earlier choice, and the governance record should say that it did.

The team adds an entailment-oriented human check for deadline claims, creates a refusal case with conflicting schedules, and prevents external publication until the claim is reviewed. Existing copies are located within the systems the team controls and corrected; uncontrolled copies are acknowledged as a limitation. The incident owner confirms the current official source, the approver reviews the changed proposal, and the correction goes out through the same channel used to publish. The student reporting route stays open in case the correction missed an effect.

The replay exposes governance revisions:

| Before | Incident evidence | After |
|---|---|---|
| “citation audit” | citation existed but did not support claim | support check for consequential claims |
| generic project owner | uncertain pause authority | named content owner and backup |
| external write implicit | public effect under-described | explicit publication approval |
| correction means edit | downstream copies unknown | bounded copy inventory and limitation |
| contact receives report | response sequence absent | acknowledgment, triage, escalation, recovery |

Three variants test the route further. In the first, the report is wrong: the student compared the summary with an outdated schedule, and the cited current schedule supports the published date. A respectful contest route still acknowledges and investigates, explains the evidence, preserves the challenge, and checks whether the public wording created reasonable ambiguity. Contestability means a person can trigger genuine reconsideration, not that every challenge decides the outcome. In the second, the incident contact is unavailable. The backup receives the alert after the declared acknowledgment threshold, pauses publication under delegated authority, and records why. If no backup exists, the exercise has found an unresolved dependency; do not fill the gap by having the agent nominate itself. An automated system can stop work safely, but responsibility must remain with an authorized person or organization. In the third, estimate the labor the remedy creates. If the team cannot sustain a review of every deadline claim, narrow the feature to extracting dates with visible source passages. A mitigation that cannot be maintained is not a control, even when it reads well in the register.

## When deferral is the responsible output

Automation is not the default destination of every workflow. Defer when the purpose is contested, affected people have not been consulted, the data boundary is unknown, evaluation cannot observe the consequential outcome, the team lacks incident capacity, or no authorized owner will accept the decision.

Narrowing scope is often productive: replace an autonomous external write with a draft for review, use synthetic rather than personal data, limit a ranking tool to organizing documents rather than people, shorten retention, or remove a high-impact action until outcome checks exist. Stopping is also a design result. If the benefit is marginal and the cost falls on people who cannot contest it, technical feasibility is not a reason to proceed. Record why the team deferred and what evidence or capacity would justify reconsideration. A register that can only say "go" is a rubber stamp with a form attached.

Do not use "human in the loop" as a magic phrase. Name the human task, evidence, authority, time budget, and stop rule. Chapter 13 showed how a gate can become ceremonial under volume. Governance must limit agent throughput to review and response capacity.

## Governance failure patterns

Use these as a checklist of how a complete register fails when you review your own. **Complete form, absent responsibility:** generic roles occupy fields, but nobody has accepted operational ownership. **Mitigation mismatch:** a citation audit is offered for a privacy-retention harm; it may be useful, but it does not address the stated mechanism. **Unobservable threshold:** "when quality falls" gives no signal or measurement procedure. **Consent by simulation:** model-generated stakeholder reactions are presented as feedback from people. **Compliance theater:** the register is treated as legal clearance despite its explicit classroom scope. **Permanent pilot:** a supposedly temporary deployment accumulates data and effects without an end condition or review date.

## Build It, Use It, Ship It

### Build It: the baseline that lets you audit

Before you open the reference solution, write your own `assess` in the learner workspace from the contract in the gate. Trace one successful case by hand, marking the input boundary, the transformation, and the returned result; then trace one failure from the tests, changing one input at a time so a difference has an identifiable cause. For each of the lesson's six tests, write down which wrong program it exists to catch. Your version is the record of what you understood before Claude touched anything, and the instrument you will measure Claude's version against. Once you can explain it, compare it with the reference and name a difference in behavior, not in line count or style.

### Use It: conduct Claude Code against your gate

Now hand Claude the work it is good at. Open Claude Code in your learner workspace; the lesson's [working prompt](../lessons/14-team-governance-and-ethics/outputs/claude-code-prompt.md) is a starting point. Work in two passes.

*The validator.* Give Claude the gate, meaning the contract and your test list (including your two added tests), and not your implementation. Ask for an implementation that satisfies the contract and passes your tests, then run your tests on what it returns, yourself. A failing test is often a gap in your gate, which Claude cannot see because it has only what you wrote. Compare its implementation with your baseline and name one difference in behavior. Then ask Claude to propose a deliberately wrong version that still passes your tests, and check by hand whether it does. If it does, your list was too weak, and you found out cheaply.

*The register.* Give Claude the facts you gathered about the capstone workflow and ask for a first draft of the register entry. Then read the draft as the author of the gate. For each line, which of the five decisions does it answer? Is there a person's name? Where does it sit on the verb ladder? Then use Claude as a challenger instead of an author:

```text
Here is my register entry and the gate I wrote before drafting it.
Do not rewrite the entry. List (1) every field whose value names a group
or a role rather than a person, (2) every threshold with no observable
signal, (3) every mitigation that does not address the harm I named,
and (4) one decision I have not written down.
```

Withholding the rewrite is deliberate: you want the weak lines found, not smoothed. Verify each finding yourself against the entry; a finding you cannot locate in the text is a fluent guess. You may also ask Claude to play an affected student to rehearse your explanation, labeling everything it returns as simulation. That tests whether your explanation is clear; it says nothing about what any real student thinks or has agreed to.

Preserve the actual transcript: your prompts, the plan, the diff, the commands, and the outputs, with the date and displayed model label. If a session failed or did not run, record that rather than substituting a fixture.

### Ship It: the register entry and its sign-off

Start with the actual capstone workflow, not a generic AI policy paragraph. Name the bounded purpose and non-purpose. List input sources and data classes. Trace tools and action targets. Link the Week 11 evidence matrix and Week 13 approval gate rather than restating them vaguely. Add one concrete harm scenario: who bears it and how it occurs. Assign a mitigation owner who has pause authority, an observable threshold and response, the retention lifecycle and deletion evidence, and an incident route and appeal path. Record unresolved authority rather than assigning it fictionally. If consultation is pending, say so and constrain the workflow accordingly; real consultation stays distinct from classroom role-play.

Include a decision note: what Claude proposed, what context a person added or corrected, what evidence supports the recommendation, whose interests it serves or disadvantages, and the named human recommendation. Highlight any sentence that merely repeats Claude; repetition is not review.

The register is also a control plane. It draws on every previous layer: tool permissions define action authority, memory records data lineage and lifetime, evaluations describe observed behavior and exclusions, and approval gates bind decisions to exact proposals. A register that can pause execution, revoke approval, shorten retention, change evaluation, assign repair, or end the project is governance. If updating it changes nothing the system does, it is only documentation.

**The sign-off.** End the register with a statement you could put your name to. Claude can draft its words in seconds, and the draft will be fluent. Write yours from your record. This is the template, not a signature:

```text
Sign-off — team AI-use register
Checked:      which register lines I confirmed against the running workflow
              (name them), and which named owners confirmed they accept the role
How:          by my own tests on the validator / by exercising the incident route /
              by inspecting the stores I control / in conversation with the named
              owner / with Claude's help (say which parts)
Not checked:  deletion in systems I do not control (provider, backups); whether the
              threshold fires under real load; consultation with affected people
              (done / pending: say which); any legal or institutional compliance
Not claiming: that the workflow is ethical, consented to, or compliant; that
              ready-for-human-review means anyone has reviewed it
Signed or withheld: ____________  (name, date)
```

The "Not checked" line does the work. It is the line an AI-written sign-off never includes, because the system that wrote it has no record of what you did not do. The `approver` field is a different thing: it names who may approve the workflow, while the sign-off states what the register itself has earned. A sign-off means something only if withholding is a real option. If your evidence does not support signing, withholding is an honest result, and the right action is to narrow or defer the workflow, not to find words that make the form pass.

## The driver's seat

This is how the chapter's work divides, task by task. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Drafting register entries, explanations, question lists | Draft fast, tighten wording, flag missing fields | Replace every group or role with a named person who accepted it | An owner exists only when someone accepts; Claude can write the name but cannot make the acceptance |
| Implementing the validator from the contract | Implement, add boundary tests, propose a plausible wrong version | Build your own baseline first, then run your tests on its version | You cannot audit a validator you have never broken |
| Listing harms and affected people | Generate candidates, ask who might be missing | Decide which are real here; talk to the people | World context: Claude was not there, and people absent from the examples are absent from its draft |
| Choosing thresholds and responses | Compute rates, propose signals, simulate a breach | Choose the threshold, who may pause, and who absorbs the cost of pausing | Which error to risk, and who pays, is a values claim with an owner |
| Consultation | Draft questions; organize *authorized*, sanitized feedback | Hold the conversation, obtain or withhold permission, stay reachable | Consent and relationship are acts between people |
| Recourse and appeal | Assemble the contested output and passages in dispute | Hear the person, decide, correct; provide a second route if conflicted | The affected person needs an answerable human, not a better explanation |
| Ship, narrow, defer, or stop | Lay out the options and what each costs | Make the choice; sign or withhold | Your name goes on it |

Record, in the register, one task you delegated and one judgment you retained. Mark which register lines Claude drafted and which you changed, and keep the transcript and the diff. If you cannot point to the line or the edit that shows each, the split happened in your head and not in the record.

## Verify and reflect

Verification begins with claims small enough to test. For the validator, run the demo and the lesson's six tests, then your two. For the register, name the verb each line earned. Keep commands, observed outputs, and your interpretation. A passing test suite establishes only the tested behavior, not universal reliability or permission to act.

Pick one passing case and explain it without reading Claude's explanation, walking from input to returned status; pick one raised error and explain why refusal belongs to the contract. Then inspect the strongest sentence in your register: "approved" requires a person who did the approving.

The most useful reflection is local: which distinction did you originally collapse? A field present and a responsibility accepted? Ready for review and reviewed? Equal accuracy and equal burden? Name the input, the question, or the conversation that separated them again. That is a concrete habit to carry forward, in place of the generic resolution to be more careful with AI.

## Assessments — ungraded practice

These Assessments develop the chapter's capabilities and are ungraded practice. Use the paired lesson's existing [knowledge check](../lessons/14-team-governance-and-ethics/quiz.json) after the practice, before viewing its explanations. It remains self-review, not a separate graded assignment. Preserve predictions, commands, observed results, disagreements, and revisions, and do not fabricate stakeholders or approvals.

### Warm-up

1. **Trace omissions — introductory; objective: trace structural checks.** Predict, then run `assess({})` and list the seven issues. Explain what this establishes about structural completeness and what it leaves open.

2. **Test shapes — introductory; objective: predict boundary behavior.** Predict and run negative retention, Boolean retention, string data classes, empty classes, and an unknown class. Explain each different outcome, and say which of the five the lesson's six tests do not cover.

3. **Interpret status — introductory; objective: state a result without overclaiming.** Rewrite `ready-for-human-review` and `review-required` as precise sentences that do not imply approval, consent, or compliance. Choose the verb for each and say what evidence would justify a stronger one.

### Application

4. **Weak complete record — intermediate; objective: construct a counterexample and name the human questions.** Construct a record that passes structural assessment but has vague ownership, evaluation, and incident language. For each vague line, write the question a named person must answer and the act that would answer it.

5. **Concrete harm — intermediate; objective: specify a harm mechanism.** Name one plausible harm in your capstone, the affected person or group, the causal path, the consequence, and the current evidence. Say who bears the error and who chose which error to risk.

6. **Operational threshold — intermediate; objective: make a mitigation testable.** Rewrite a vague mitigation into a signal, threshold, named owner, bounded response, escalation route, and recovery condition. Write the test that would show the threshold fired.

7. **Retention map — intermediate; objective: separate verified from listed.** Trace one data class through controlled copies, access, deletion, and audit evidence. Mark each store as verified (you inspected it) or listed (you rely on a statement), and mark unknown provider or backup behavior rather than guessing.

### Synthesis

8. **Equal accuracy, unequal risk — advanced; objective: defend stronger governance and name who bears the error.** Compare two equally accurate fixtures with different data, authority, retention, and reversibility, and defend which needs stronger governance. Then describe a constructed pair with equal accuracy but different kinds of error, say who pays for each, and name who should decide which to prefer.

9. **Recourse design — advanced; objective: design a contestable route.** Design a plain-language contest and appeal route. Specify how a correction reaches downstream artifacts, how the team handles unavailable or conflicted owners, and where Claude's role stops and a person's begins.

10. **Decision note — advanced; objective: separate proposal, context, and recommendation.** Record Claude's proposal, human-supplied context, supporting evidence, affected interests, and a named recommendation. Identify where the human contribution changes the content instead of paraphrasing the model.

### Challenge

11. **Governance stress test — stretch; objective: simulate a breach and sign or withhold honestly.** Simulate one threshold breach and trace detection, pause, notification, containment, communication, correction, and recovery, stating which parts are simulated and which controls actually ran. Then complete the sign-off for your register, including the "Not checked" line, and say whether your evidence supports signing.

## Capabilities summary

You can now read an AI-use register as a set of operational claims rather than a certificate. You can reproduce the course validator's missing-field, retention, data-class, and external-write behavior while stating its limits. You can connect harms to affected people, mitigations to owners, thresholds to responses, data to a lifecycle, and incidents to recourse. You can also defend deferral when the team lacks evidence, authority, consent, or response capacity.

And you can say what the three jobs look like at this scale. You conducted: you wrote the five decisions and the wrong validator your tests had to catch before Claude drafted anything. You checked: you found the weak line in a complete register and named who bears each kind of error. You drove: you handed Claude the drafting and the implementation, kept the relationships, the consent, and the choice to ship or defer, and signed or withheld.

## Anthropics

Anthropic's current [Claude Code security](https://code.claude.com/docs/en/security) guidance can inform your analysis of access boundaries, untrusted inputs, and safe operation. Connect a relevant recommendation to a named owner, monitoring signal, and incident response in your register rather than copying general security prose.

The primary link was checked for the approved research packet on 2026-09-06. Product guidance supplements this governance analysis; applicable Northeastern policies determine institutional use. The register is a course mechanism and not a claim about Anthropic's internal governance or a legal compliance tool.

## Computational Skepticism

The companion's accountability chapter adds a diagnostic the body has not used: responsibility for a failure distributes across parties whose choices were each necessary and none sufficient. See [Values and accountability](../docs/computational-skepticism.md#values-and-accountability) and [Attestation and review](../docs/computational-skepticism.md#attestation-and-review). Take the rehearsal incident and list every party whose choice shaped it: the student who reported, the content owner, the maker of the tool that drafted the summary, the provider of the model behind it, and the institution whose schedule is the source of truth. Your register names one owner. For each of the others, find where the register records their decision as a dependency you checked rather than assumed. Then ask a version of the book's governance-counterfactual question: what change to the register, made before the incident, would have prevented it, and is that change an action someone takes or a sentence someone wrote?

## Conducting AI

The chapter on interpretive judgment supplies a three-cell test for any output you are tempted to act on; see [Interpretation and accountability](../docs/conducting-ai.md#interpretation-and-accountability). It borrows Suchman's three legitimacies and applies them to AI outputs, an adaptation by the book's author and not Suchman's own. Choose one sentence from Claude's draft of your register and run the test. Pragmatic: does it serve the people it is for? A fluent draft usually passes. Moral: whose standards would acting on it have to survive, and who would have to answer for it? Cognitive: do you trust the sentence because you can account for it, with these facts verified in these ways, or because it reads well? The book argues that fluent output supplies the appearance of that last kind of trust without its grounds, and that supplying the grounds is the human's work. The decision note is where that work shows.

## Irreducibly Human

The chapter on social and personal intelligence contributes one more diagnostic, from its account of how relational skill is unbuilt: an institution teaches what it actually rewards, not what it nominally teaches. See [Relationships and consent](../docs/irreducibly-human.md#relationships-and-consent). The book's example is medical training, where it reports that environments rewarding efficiency erode the empathy their curricula ask for. Ask the same of your team. Does anyone get time for consultation? Is the person with pause authority rewarded or penalized for using it? If shipping is rewarded and listening is not, the register will say the opposite and the team will do what is rewarded. The book's stronger claim, that the machine boundary at this tier holds in principle, is an argument; this chapter needs only its operational form.

**AI should** draft plain-language explanations, suggest questions, organize authorized sanitized feedback, surface uncertainty, and preserve objections. It should not invent stakeholder testimony, imply consent, or speak as though it represents an affected person.

**Human should** hold the actual conversation, listen for concerns outside the prepared script, obtain permission where required, remain reachable for correction, and decide how feedback changes access, retention, evaluation, or deployment.

Record the split: one question Claude helped prepare, and one actual change or unresolved concern from a real, consented discussion. If the exercise uses role-play, label it as simulation and state which real consultation remains pending. A functioning appeal route must reach a responsible person, not return the affected person to model-generated reassurance.

## Forward bridge

The team now has a register, owners, gates, evidence, and incident routes, and a sign-off that says what the register has and has not earned. Chapter 15 asks whether these parts form one defensible system. The capstone succeeds only when another person can reproduce its central result, observe a controlled failure, inspect recovery, and understand why the accountable owner chose to ship, narrow, defer, or stop. Carry your register forward with its sign-off, or with your reason for withholding it.
