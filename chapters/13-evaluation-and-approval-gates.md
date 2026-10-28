# Chapter 13 — Evaluation and approval gates

*An approval can survive after the thing it approved has disappeared.*

Suppose a reviewer is shown a proposal to write `report.md`. She reads the evidence, approves, and the system files a yes with her name and a timestamp. Later the target becomes `elsewhere`. If the system retained only a generic yes, the old decision can now be presented as permission for an action she never saw. Every step of the recipe was followed: there was a button, a name, a timestamp. The authorization had still drifted away from its object.

The course fixture makes the remedy inspectable. It turns six proposal fields into a stable serialized representation, computes a SHA-256 fingerprint, and records that fingerprint with a simulated decision. The decision matches the original proposal. Change the target and the same decision no longer matches. This demonstrates content binding. It does not demonstrate a real person's consent, the approver's identity, their authority, their comprehension, or the proposal's safety.

So the question for the chapter is not how to hash a dictionary. It is what, exactly, a yes is a yes to, and who was in a position to give it. Each chapter so far has had you write a gate before Claude ran. This one takes the gate apart, because it is the artifact where the three jobs meet. You conduct: you decide what the gate evaluates, covers, and refuses before anything is approved. You check: you ask whether an approval can still be true after the thing approved has changed, and what the record leaves out. You drive: Claude will assemble the proposal, run the evaluation, and highlight the diff in seconds, but the yes, the no, and the attention behind them are a person's.

This chapter tears down both halves of an approval gate. Evaluation produces evidence about a proposal. Authorization records a responsible decision about that exact proposal. Automated checks can prepare the decision. A fingerprint can prevent unnoticed content drift. Neither can perform the human judgment hidden inside the word *approve*.

## What you will be able to do

By the end of the chapter, you should be able to:

- write an approval request that names action, target, reason, effects, evidence, and rollback, and say which field a reviewer could not decide without;
- explain why canonical serialization precedes content fingerprinting;
- bind a simulated decision to one exact proposal and reject changed content;
- separate task evaluation, policy compliance, reviewer burden, and human authorization;
- identify missing identity, authority, expiry, revocation, and replay controls;
- design a gate that supports refusal, deferral, and escalation rather than manufacturing consent;
- write the gate (predicate, scope, expiry, revocation, and an evaluation set that can embarrass the proposal) before Claude implements it, then conduct Claude Code against it and run your own tests on what returns;
- write a sign-off that says what was tested, what was not, and who cleared which gate, and withhold it when the record does not support signing;
- say which parts of review Claude can prepare and which stay a person's, treating review capacity as a design constraint.

You should have completed Chapters 5 and 10–12 on authority boundaries, plans, tool evidence, and versioned memory. Hashes appear here by their operational role; cryptographic internals are outside the lesson. You need Python dictionaries, JSON, Boolean logic, and tests. This narrative is paired with the runnable [Lesson 13 materials](../lessons/13-evaluation-and-approval-gates/docs/en.md).

Before inspecting the mechanism, predict four outcomes. Will changing dictionary key order change the fingerprint? Will changing only the target change it? Will an approval containing the right fingerprint but no approver name pass? Does a matching fingerprint prove that a particular human approved? Preserve your answers before running anything.

## A gate is not a button

The first decision a gate designer faces is what a reviewer must be shown for a yes to mean anything. An interface can ask “Allow?” while concealing nearly everything that decision requires. Allow what action? Against which target? For what purpose? With which foreseeable effects? On what evidence? How can it be undone? A generic prompt moves the cognitive burden onto the reviewer at the moment of interruption, often without the context to carry it.

The reference proposal requires six fields:

```python
FIELDS = (
    "action",
    "target",
    "reason",
    "effects",
    "evidence",
    "rollback",
)
```

The fields are a minimum teaching contract, not a universal governance schema. Each exists because a reviewer cannot decide without it. `action` says what operation will occur. “Update” may still be too vague; “overwrite one local Markdown file” is more reviewable. `target` identifies the object or destination, and a display name without a resolved path, account, environment, or recipient may conceal the consequential difference. `reason` ties the action to the task rather than merely describing capability. `effects` names anticipated changes, including external and irreversible ones. `evidence` points to checks that support proceeding. `rollback` states how recovery would work and should admit when rollback is partial or impossible.

Claude is good at the drafting. Given a plan and the current state, it will fill the six fields quickly and say which it could not. But it holds only what is in its context. Whether “overwrite one local Markdown file” is what will physically happen, whether `report.md` resolves to the object you mean, and whether the effects are complete are checks against the world, and they are the reviewer's.

Filling every field is structural validity. A proposal can contain six fluent, meaningless strings and pass the current `fingerprint` precondition because Python checks only that each retrieved value is truthy. The word “meaningful” in the error message expresses intended use more strongly than the implementation can enforce. Human and domain evaluation still matter.

<!-- [FIGURE: Cajal production brief. An approval request expands into reviewable fields. Include action, target, reason, effects, evidence, rollback. Show the confirmed relationship that identity, authority, expiry, revocation, capacity remain separate. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![An approval request expands into reviewable fields. identity, authority, expiry, revocation, capacity remain separate.](../images/13-evaluation-and-approval-gates-fig-01.png)
*Figure 13.1 — An approval request expands into reviewable fields*

## Evaluation comes before authorization

Two questions share most approval screens, and the merge is where gates go soft. *Evaluation* asks what happened, what could happen, and how well the proposal meets a stated criterion. *Authorization* asks whether a responsible person or policy permits the action. The first produces evidence. The second spends it.

The order of design matters as much as the order of operation. Decide what would count as evidence against the proposal before you look at the evidence for it. If the cases were picked after the implementation was observed, and the expected answers adjusted until everything passed, the set records accommodation, not evaluation. This is why the gate you write later in the chapter holds two things: an evaluation set that can embarrass the proposal, and an approval predicate that refuses to follow a changed one.

Each instrument has a scope. A test suite can evaluate selected behavior; it cannot decide whether a destructive change is worth making. A policy checker can flag an unapproved directory; it cannot say whether an exception serves the affected people. A model grader can score an output against a rubric, but its score is evidence with scope and failure modes, not a decision. Claude can run every one of these instruments for you, and should. None of them returns a decision.

Build evaluation sets around tasks, expected outcomes, refusal cases, and boundary failures. Keep trials and transcripts, but distinguish them from actual outcomes. A tool trace showing that a command ran is not an observation that the intended state exists; Chapter 11's false final claim, 42 in the trace and 99 in the sentence, is the reminder that success narration is not an outcome check.

Evaluation sets also exclude. A set built from ordinary successful writes may say nothing about symlinks, permission errors, concurrent changes, private data, or malicious paths. Record those exclusions beside the result: “passed 20 cases” is uninterpretable until a reviewer can see which cases, and why they represent the intended use. At least one case should require refusal, or a system that always proceeds can appear perfect. Another should be structurally complete but substantively weak, to test whether review reads meaning or treats field presence as safety.

Separate metrics that can pull against one another. Task success may rise while invalid action rate rises. Reviewer burden may fall because the gate hides detail, while informed decisions worsen. Time-to-approval may improve because reviewers click reflexively. A gate needs a portfolio of evidence, errors and deferrals included, not one celebratory rate.

## Canonical content and its fingerprint

A reviewer approves something. The fingerprint's job is to make “something” precise enough that a change to it can be detected. Underneath sits a design decision: what counts as the same proposal? The same bytes, the same meaning, the same resolved target? The reference implementation answers with bytes, after one normalization, and every choice it makes is one you should be able to defend. It begins by checking the proposal:

```python
def fingerprint(proposal):
    if not isinstance(proposal, dict) or any(
        not proposal.get(key) for key in FIELDS
    ):
        raise ValueError("Six meaningful gate fields required")
```

A non-dictionary fails. A missing field fails. An empty string, zero, false value, empty list, or other falsey value in a required field also fails. Extra fields do not fail; they become part of the serialized proposal and therefore affect its fingerprint. That detail matters. The six named fields are minimum requirements, not an exact-key schema.

Next, Python serializes the entire dictionary:

```python
encoded = json.dumps(
    proposal,
    sort_keys=True,
    separators=(",", ":"),
).encode()
```

JSON objects do not conceptually depend on insertion order, but Python dictionaries preserve one. If two equivalent proposals were serialized in their construction order, they could produce different byte sequences merely because fields were inserted differently. `sort_keys=True` canonicalizes key order for this bounded representation. Compact separators remove default spaces so formatting choices do not alter the bytes.

The second of the six tests confirms that reversing dictionary item order does not change the resulting fingerprint. This is an observed property of the course function for its JSON-compatible fixture, not a claim of universal canonical JSON. Numbers, Unicode normalization, unsupported objects, duplicate keys arriving in raw JSON, and cross-language serialization require additional specifications.

The bytes go to SHA-256 and the function returns a hexadecimal digest:

```python
return hashlib.sha256(encoded).hexdigest()
```

The test expects a length of 64 hexadecimal characters. Operationally, the digest serves as a compact content identity. If the serialized proposal changes, the comparison should fail. The chapter does not use the digest as encryption, secrecy, a signature, or proof of authorship. Hashing public content does not hide it. Anyone can calculate a digest, so a matching digest in a decision record says the record was written against this content and nothing about who wrote it. No private signing key appears here.

## The approval predicate

The second function asks whether a decision matches the current proposal:

```python
def approved(proposal, decision):
    return (
        isinstance(decision, dict)
        and decision.get("approved") is True
        and isinstance(decision.get("approver"), str)
        and bool(decision["approver"].strip())
        and decision.get("fingerprint") == fingerprint(proposal)
    )
```

Every condition has a narrow meaning. The decision must be a dictionary. `approved` must be the exact Boolean `True`, not a truthy string such as `"yes"`. The approver field must be a nonblank string. The recorded fingerprint must equal a newly computed fingerprint of the proposal now under consideration.

If these conditions hold, the teaching function returns `True`. Read that as “this decision record has the required shape and content binding.” Do not read it as “a real authorized human gave informed consent.” The string `"human"` in the test is fixture data. The implementation has no login, signature, organizational role registry, delegation rule, expiry time, revocation list, decision ID, or evidence that a person saw the proposal.

It helps to set side by side the three things an approval can be bound to. *Content*: the fingerprint ties a decision to the exact serialized proposal, and the code above does it. *Scope and time*: how long the decision lives, how often it may be used, in which environment. That is code you have not written yet, and the next section designs it. *Person*: who decided, with what authority, having read what. No code in this chapter does that, and no code can do it alone. A gate that binds only the first is a good seal on an envelope nobody opened.

This naming tension is pedagogically useful. A function called `approved` tempts us to repeat its Boolean as institutional fact. Careful documentation narrows the claim: the predicate validates a small decision-record contract, and production authorization needs more than that.

<!-- [FIGURE: Cajal production brief. Approval binds to one proposal fingerprint. Include original proposal, canonical JSON, fingerprint A, simulated decision A, changed target, fingerprint B. Show the confirmed relationship that changed content cannot reuse the old decision. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Approval binds to one proposal fingerprint. changed content cannot reuse the old decision.](../images/13-evaluation-and-approval-gates-fig-02.png)
*Figure 13.2 — Approval binds to one proposal fingerprint*

## Worked example: approval that cannot follow a changed target

The demo constructs this proposal:

```python
proposal = {
    "action": "write",
    "target": "report.md",
    "reason": "deliver draft",
    "effects": "one local file",
    "evidence": "source checks passed",
    "rollback": "restore previous file",
}
```

All six required values are nonempty. `fingerprint(proposal)` sorts the keys, uses compact JSON, encodes the text, and returns a 64-character SHA-256 hexadecimal string. The exact recorded digest can be reproduced through the research script; we do not need to pretend it carries semantic meaning. It identifies the serialized content under this function.

Now construct a simulated decision, labeled as one:

```python
decision = {
    "approved": True,
    "approver": "simulated-reviewer",
    "fingerprint": fingerprint(proposal),
}
```

Calling `approved(proposal, decision)` returns true under the teaching predicate. This is a fixture result, not a human sign-off. The decision was generated to test the content-binding mechanism.

Change one field after the simulated decision:

```python
changed = dict(proposal)
changed["target"] = "elsewhere"
```

The changed dictionary serializes to different bytes and receives a different fingerprint. `approved(changed, decision)` returns false because the old digest no longer equals the current proposal's digest. The approved research fixture observed this original-match and changed-content rejection.

The rejection is what we want. The system does not ask whether “elsewhere” is similar, safer, or probably what the reviewer meant. A changed target creates a new decision object, and the reviewer must see it and decide again.

Now change only dictionary insertion order while preserving all key-value pairs. The fingerprint remains the same because keys are sorted before serialization. That is a representation change, not a proposal change, and a gate should avoid demanding new approval for irrelevant formatting while reliably detecting consequential change. The distinction depends on canonicalization policy. Two path spellings that resolve to the same file hash differently as strings. Conversely, a target string can stay identical while the filesystem object it names changes. Content binding is only as semantic as the proposal representation, and a high-stakes gate may bind resolved identifiers, immutable versions, or object hashes rather than friendly text alone.

An evidence table keeps the claims honest:

| Observation | Supported conclusion | Unsupported conclusion |
|---|---|---|
| six fields are truthy | minimum shape passes | descriptions are adequate |
| same data, reversed insertion | course digest is order-insensitive | all JSON implementations agree |
| target change, digest mismatch | serialized proposal changed | changed action is necessarily harmful |
| decision matches original digest | record binds to original content | named person authenticated |
| predicate returns true | fixture contract passes | informed, authorized consent occurred |

Notice what the table does not contain: any row that would support “a person reviewed this.” That absence is the sign-off standard for this chapter. A recorded fingerprint is evidence that a record was written against these bytes. It is not evidence that anyone read them.

The same discipline applies to the six lesson tests. All six pass on the reference, which tells you it meets six statements, not that six statements are enough. Two wrong versions that pass all six appear below, and finding such versions is the work of the gate.

## Scope, expiry, revocation, and replay

A fingerprint answers “is this still the proposal?” It does not answer “may this be done now, here, once?” Those are separate decisions, and a gate that leaves them to defaults has made them anyway.

Approval needs scope beyond content. A reviewer may approve one execution, one environment, one time window, one data set, or one maximum effect. If the proposal says “write report.md” but the operation can repeat indefinitely, the fingerprint alone does not limit replay. Add a unique decision ID and consumption state for single-use actions, and check and consume the ID atomically at the effect boundary; otherwise two workers can present the same valid decision simultaneously. The authorization service must own that rule where the action occurs.

Expiry needs an explicit time basis and comparison policy; a deadline in local time without a zone is ambiguous. It is not just a timer, either: new evidence can invalidate approval early. Revocation withdraws a still-unexpired decision, so record who revoked, under what authority, which proposal is affected, and how already-started work is handled.

Bind the environment identity that matters. Approval for a test database must not authorize production merely because the query text matches. Resolved target, account, repository revision, data classification, and tool version are candidates. Add the identities whose change should force reconsideration and no others. Which ones those are is a judgment about consequence, not a property of the hash.

Rollback claims need evaluation too. “Restore previous file” assumes a previous copy exists, the writer can access it, no dependent effects have occurred, and restoration is semantically sufficient. Sending a message, disclosing data, or triggering a payment may be irreversible. Chapter 5 closed on the point that an authorized change can still be a bad change, and an approved one can be too. A gate should say “no complete rollback” rather than inventing reassurance.

## The gate: write the approval predicate before anything is approved

Here the gate is also the chapter's subject. Write it in your learner workspace, in plain sentences and test names, before you ask Claude for any code. Name who decided each item. Where Claude proposed and you accepted, say so.

*Design.* One consequential action from your capstone or, if you have none yet, the chapter's `report.md` write. Its six fields, with friendly targets replaced by resolved identities. The identities beyond the six whose change should force a new decision. The decision owner as a role that can be asked, not “the team.” The review budget, labeled as an assumption unless you measured it. These are your choices. No model produced them.

*Contract: the approval predicate.* A decision authorizes one bounded attempt if, and only if, all of this holds. The decision is a record whose `approved` is exactly `True`. Its approver is a nonblank string (in production, an authenticated identity, which your fixture will not have). Its recorded fingerprint equals a fresh fingerprint of the proposal about to execute, computed at the effect boundary and not at review time. Its deadline has not passed, it has not been revoked, and it has not already been used. Absence, silence, a timeout, a model's confidence, and a favorable automated score authorize nothing. Refusal and deferral are recorded outcomes, not errors. I would pass the current time into the check instead of reading it inside, so your tests can say “one second after the deadline” without waiting.

*Wrong versions your tests must catch.* Two plausible predicates pass all six lesson tests; confirm it yourself by dropping each into the test file. One fingerprints only the six named fields, so adding `"environment": "production"` to an approved proposal changes nothing. The other tests `approved` for truthiness, so the string `"no"` approves. A third has no lesson test at all, because the lesson has no consumption: it checks that a decision is unused and marks it used in two separate steps, so two workers can both pass between them. If your tests cannot tell these from the right program, the gate is not finished.

*What a failure looks like.* One sentence, dated, written before you read any output: what you would see if the gate approved something it should not. Written afterwards, it describes the output instead of testing you.

*What this gate may claim.* Content binding, expiry, and single use under a fixture clock and a simulated approver. It may not claim that a person reviewed, understood, or was authorized.

Claude can attack this gate usefully: ask it for a decision record that would still pass your predicate and should not. It cannot write the gate for you without defeating its purpose, because the owner, the budget, and the identities that force a new decision are judgments about consequence, and they go on the record in your words.

### Build an evaluation set that can embarrass the proposal

The second half of the gate is the evaluation set. Begin with the intended decision. For a file-writing action, the question might be whether the change is confined to one allowed file, preserves required content, passes relevant checks, and has a credible recovery path. Turn each clause into observable cases before revising the mechanism. Include ordinary success, because a gate that always refuses is not useful, then boundary and refusal cases whose correct outcome is to stop.

A compact set for the chapter fixture can include:

| Case | Construction | Expected gate behavior | Why it matters |
|---|---|---|---|
| exact original | six concrete fields and matching simulated decision | content match | establishes happy path |
| reordered keys | same values, different insertion order | same fingerprint | removes irrelevant representation noise |
| changed target | copy with another destination | reject old decision | blocks approval drift |
| missing rollback | required value absent | reject proposal shape | exposes incomplete review material |
| vague evidence | evidence says only “looks good” | structural pass, human defer | distinguishes shape from substance |
| replayed decision | same record consumed twice | reject second use in extension | constrains effect count |

The fifth case is especially important. The current Python function will fingerprint a vague statement because it is nonempty. That is not a failing test if the function's contract is structural content binding; it becomes a workflow failure only if documentation claims the function evaluated evidence quality. Reading “looks good” and deciding it is not evidence is plausibility auditing: judging whether a claim is credible and consistent with what you know, independent of how confidently it was stated. That is the reviewer's work, and no field name does it.

Lock expected outcomes before running. When observation differs, investigate whether the implementation, the test expectation, or the original requirement is wrong, and preserve the change. With a tiny fixture, do not inflate one held-out result into a reliability percentage; report the cases and exclusions directly.

Model graders can assist with qualitative fields, but their judgments need calibration and failure analysis. A model may reward fluent rollback prose that omits an irreversible effect, and two graders that share a prompt assumption or a source error can agree and still be wrong together, which is not a second opinion. Pair qualitative grading with deterministic checks and human review proportional to the stakes. Keep task inputs, expected behavior, actual output, the checker, and the rationale for discrepancies, and show the changed-target failure beside the pass count; a single aggregate score discards the trace the reviewer most needs.

## The approval interface is part of the control

Even a strong backend predicate can be undermined by presentation. If the reviewer sees only a friendly summary while the fingerprint covers hidden fields, the decision binds to bytes they did not meaningfully inspect. If the interface truncates a target or collapses effects behind a disclosure panel, the record may be mechanically exact and socially uninformed.

Present the action and target first, and highlight differences from any previously reviewed proposal: target changed from `report.md` to `elsewhere`, evidence unchanged, prior approval invalid. Link evidence claims to their artifacts rather than copying a green label, and make irreversible effects and absent rollback unavoidable. Provide approve, refuse, and defer as genuine choices. Avoid dark patterns: a default selected approval, a green continue button beside a muted refusal link, urgency language generated by the requesting agent.

The decision should bind to the representation the person actually saw, together with any referenced immutable artifacts. If evidence can change at the same URL after approval, binding only the proposal text leaves another substitution path. Say why this person is the decision owner: someone can understand a proposal and still lack authority over the target, the data, or the recipient, and should be able to escalate without impersonating an approver. At execution, recompute the fingerprint; on a mismatch, show the changed fields and return to review. Never invite the model to explain why the old approval “probably still applies.”

## Human attention is a finite gate resource

A perfectly bound proposal can still receive superficial review. This is the part of the gate that no hashing reaches, and it is where I would spend the design effort. In *Irreducibly Human* I call the underlying problem the volume trap. The case for generating ten times as much in the same time is real. The ability to verify ten times as much in the same time does not come with it, so the extra output is reviewed less, or not at all. That is the book's argument, not a measurement of any team, but the arithmetic is simple enough to run on your own queue. Claude sits on the generating side of that gap: it can produce proposals, evidence summaries, and diffs faster than a careful reviewer can read them. Speeding up the button does not restore judgment; it turns the gate into a queue or a click ritual.

Model reviewer workload explicitly. Suppose five proposals arrive while one reviewer can carefully inspect two during the stated period. This is a labeled capacity assumption, not a measured result. A naive system shows all five as urgent and lets dependent agents wait indefinitely. A governed system classifies consequence, preserves arrival and dependency information, and applies a declared queue policy.

Proposal A is a reversible local formatting change. B sends material to an external recipient. C changes a production target. D duplicates B's effect. E depends on C. The system can automatically run structural and evaluation checks for all five, but it cannot manufacture three more units of human attention.

B and C may receive priority because their effects are external or high-impact. D should be detected as a potential duplicate and held. E remains blocked on C. A may wait, expire, or proceed under a separately authorized low-risk policy if one genuinely exists. The point is not that this ordering is universally correct. It is that someone must choose and document the policy before the proposing model labels its own work urgent, and urgency labels written by the proposer should never set priority unvalidated.

If the queue exceeds capacity, pause intake, narrow scope, add qualified reviewers, or defer work. Cutting the information shown until reviewers can click faster is not capacity planning. Invalidate pending decisions when their evidence or environment goes stale; approval obtained after its premises expire is another form of content drift. Timeout, absence, and queue delay are not approval, and more prompts do not mean more oversight: past the available attention they produce habituation.

In your artifact, report how many proposals were simulated, the assumed capacity, which remained blocked, and the escalation rule. Call review time measured only if you measured it; otherwise it is a design assumption. The honest result may be that safe throughput is lower than agent production, which is a design finding, not an inconvenience to conceal.

Capacity also moves the automation boundary. If reviewers keep receiving nearly identical, low-consequence proposals, a team can ask whether a narrow standing policy should authorize that class, with monitoring and revocation. That is a governance decision, not an agent shortcut: define the class precisely, test its exclusions, and keep everything outside it gated.

Review quality needs a feedback loop. Compare predicted effects with observed outcomes and inspect approvals later reversed. Track refusal and deferral, not just approvals: if every decision is yes, ask whether reviewers have real options, adequate evidence, and support for saying no. Do not score reviewers on throughput, which trains the gate to become ceremonial. An unexpected outcome, harmless or not, should change the next evaluation set before another approval is requested. That is the re-engagement trigger from Chapter 12 applied to the gate itself: the design is not frozen at approval time.

## Attestation: what the signer states, and the right to withhold

A decision record is the gate's last artifact, and the part most likely to look more complete than it is. Early in its accountability chapter, the *Computational Skepticism* companion runs a small experiment: ask an agent for the sign-off statement for the thing you just validated. The companion's prediction is a fluent, structurally complete paragraph that names a person and asserts a review happened, and that is empty, because unless you supplied the record, the system that wrote it has nothing to say about what was done or skipped. Run the experiment once, save what you actually get, and read it against the standard below. The shape of a sign-off is easy to produce. Its substance is not.

The companion's standard is a four-part attestation. First, what was tested: the specific checks, against the specific criteria, with the results. Second, what was not tested: the conditions not probed, the failure modes known and not reached. This is the part an AI-written sign-off omits, and the part that makes the document honest, because a list of only what passed reads as a clean bill of health that the affected person cannot act on when the untested region is where harm lives. Third, who cleared which gate: a named person or role per decision, someone who can be asked and who answers if the gate was cleared wrongly, not “the team.” Fourth, the verbs calibrated: “passed” should mean passed a stated test, and a weaker verb such as “believe safe” should say that it is weaker.

The fingerprint binds that record to content. It cannot show that the reviewer opened the test report, understood the target, or had enough time. Those are process questions, and a signature can strengthen identity evidence without proving comprehension. A useful decision record lets the reviewer decline or defer, and it preserves unresolved gaps. A reviewer might write: “The local tests pass, but remote publication permissions and data licensing are unverified; defer.” That is a successful gate outcome. Treating anything but approval as failure pressures people to manufacture certainty.

Name the trade-off, or the regime is being sold rather than examined. An attestation regime optimizes for legible answerability: after a failure you can find the person who signed, read what they claimed, and see what they explicitly did not warrant. It sacrifices speed and deniability. Someone has to be willing to be named, and a deployment under schedule pressure will experience “what did we not test?” as friction arriving late. The friction is the point, and it is why a gate quietly routes around it when it can. Underneath sits the signer's authority to withhold. If the only outcome the process permits is “signed,” you have built a rubber stamp with a person's name on it, which hides missing review behind that person's credibility.

Governance must also name organizational owners and escalation paths, not place every consequence on the person who clicked. The companion's own caution applies here: this supplements the course gate and does not authenticate a signature or provide a legal compliance determination.

## Where the gate sits in the build so far

The plan from Chapter 10 creates a proposed step, Chapter 11 supplies execution evidence, and Chapter 12 stores versioned state and exposes conflicts. This chapter binds evaluation and authorization to the exact action representation that crosses the boundary. The sequence should be visible:

1. construct a proposal from the current plan and state;
2. validate required fields and policy boundaries;
3. run scoped evaluations and record exclusions;
4. freeze the exact proposal and compute its fingerprint;
5. present evidence and consequential effects to an authorized reviewer;
6. record approve, refuse, or defer against that fingerprint;
7. recheck fingerprint, expiry, revocation, and use constraints at execution;
8. observe the actual outcome and preserve it separately.

Steps 3 and 4 are where your gate does its work; steps 5 and 6 are where it stops being yours to automate. Changing the proposal returns the workflow to step three or earlier, because a valid old approval is evidence about history, not authority for the new object. Approval permits a bounded attempt and does not guarantee the intended result, so keep the proposal fingerprint, the effect evidence, and the post-action check as separate linked records.

## Build It: the baseline that lets you audit

Before you open the reference solution, write `fingerprint` and `approved` yourself in your learner workspace. Read the six tests first and write down which input should fail and why. Explain each intermediate quantity (the canonical bytes, the digest, the comparison `approved` makes) and what would count as an impossible value for it. Trace one success and one failure by hand, changing one input at a time so a difference has an identifiable cause. From the repository root:

```bash
python3 lessons/13-evaluation-and-approval-gates/code/main.py
python3 -m unittest discover -s lessons/13-evaluation-and-approval-gates/code/tests -v
```

Your own version is the baseline: the record of what you understood before Claude touched anything, and the instrument you will measure Claude's version against. You cannot audit a predicate you have never written, and the failures this chapter cares about are quiet ones. A gate that approves the wrong thing does not crash.

## Use It: conduct Claude Code against your gate

Now hand Claude the work it is good at. Open Claude Code in your learner workspace, give it the gate you wrote, the contract and the test list but not your implementation, and ask for an extension of the predicate with a decision ID, a deadline, revocation, and single-use consumption that satisfies your tests. Then run your tests on what it returns, yourself.

Do three things with the result. First, note which of your tests failed, if any. A failing test is often a gap in your gate, which Claude could not see because it only had what you wrote. Second, read the diff for three places where a human decision hides: where the current time is read, where a used decision is recorded, and whether checking and recording happen as one step. Name one difference in behavior from your baseline. Third, ask Claude to propose a deliberately wrong version that still passes your tests, then check by hand whether it does. If it does, your tests were too weak, and you found out cheaply. The check is yours either way, because whether the tests are enough cannot be judged by the system they are testing.

Then take a real tool proposal that Claude Code asked you to approve while you worked in this course, and rewrite its approval request as six fields. Which fields could you fill from what you were shown, and which would you have had to go find? Evaluate task success, invalid action rate, and reviewer burden separately.

Preserve the actual transcript: your prompt, the plan, the diff, the commands, and the outputs, with the date and displayed model label. If a session failed or did not run, record that rather than substituting a fixture. Direct API use is optional and explicit; none is needed here.

## Ship It: a gate design that survives a skeptical reader

The artifact is the before-and-after gate wording, an evaluated proposal, rejection tests, and a decision record. The decision record carries the fingerprint, the simulated decision labeled as a simulation, and the unresolved gaps. Never fabricate a classmate's or stakeholder's approval. Calculate the fingerprint only after the proposal is ready for review, and freeze or copy the reviewed representation so it cannot mutate unnoticed. Then enumerate production gaps: authentication, authorization registry, single-use consumption, expiry, revocation, audit access, privacy retention, queue behavior, and incident response. You need not build an enterprise authorization service, but you must not claim the teaching Boolean is one. Cite Claude assistance where it was used, and keep the work under `learning-artifacts/week-13/`.

### The sign-off

End the artifact with a statement you could put your name to. Claude can draft its words in seconds and the draft will be fluent, so write it from your record. This is the template, not a signature:

```text
Sign-off — approval gate design
Checked:      which properties of the gate, by which of my own tests (name them)
How:          by hand / by a test I wrote before reading Claude's version /
              by recomputation / with Claude's help (say which parts)
Not checked:  authentication; a real reviewer; concurrent use; clock skew;
              evidence that changes after approval; inputs outside my tests
Cleared by:   gate -> named role or person, or "SIMULATED, not a person"
Verbs:        each claim worded at the strength of its evidence
              (recorded / computed / tested, not established)
Not claiming: that any person reviewed or was authorized; that the
              proposal is safe
Signed or withheld: ____________  (name, date)
```

Two documents are easy to confuse here. The *decision record* is what a reviewer produces: approve, refuse, or defer, with scope, gaps, and authority. The *sign-off* above is what you produce about the gate you built. When the reviewer is a simulation, the decision record is a labeled fixture and not a decision; the sign-off is yours, and you may withhold it. If you cannot fill “Not checked” with real entries, you have not looked hard enough, not found nothing. If the evidence does not support signing, withholding is an honest result.

### The driver's seat

This is how the chapter's work divided, task by task. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Assemble the six-field proposal from a plan and state | Draft it, flag the fields it could not fill, show the diff against the last proposal | Replace friendly targets with resolved identities; decide which identities force a new decision | Which change deserves a new decision is a judgment about consequence |
| Run the evaluation set and collect evidence | Run every checker, group the traces, flag missing rollback | Choose the cases that can embarrass the proposal; record exclusions | A set designed after seeing the result records accommodation |
| Implement the predicate, expiry, and consumption | Implement from your gate, fast | Write the gate and tests first; build your own baseline; run your tests on its version | You cannot audit a predicate you have not built |
| Approve, refuse, defer, or escalate | Keep the action queued and stop at the boundary | Decide, within your authority | Authority and accountability attach to a person, and the right to say no is part of the job |
| Set the review budget and queue policy | Model the queue under your stated assumptions | Declare capacity and the escalation rule; measure review time if you report it | Attention is finite and it is yours |
| Say what the gate supports | Flag an overclaim | Choose the verb; sign or withhold | Your name is on the claim |

Record, in the artifact, one task you delegated and one judgment you retained. If you cannot point to the transcript line or the edit that shows each, the split happened in your head and not in the record.

## Verify and reflect

Verification begins with claims small enough to test: that reversed insertion order leaves the fingerprint unchanged, that a changed target rejects the old decision, that a truthy string does not approve, that a replayed decision is refused. Name which claim each check addresses, and say what remains untested.

After running the tests, pick one passing case and explain it without reading Claude's explanation, from the proposal bytes to the Boolean. Pick one rejection and explain why refusal belongs to the contract. Then inspect the artifact's strongest sentence. “Recorded” describes an observation, “computed” a calculation, “tested” a check you ran. “Approved” and “authorized” require a person and an authority the fixture never contains.

The most useful reflection is local: which distinction did you originally collapse? A hash and a decision? A structurally valid proposal and a good one? A fast reviewer and an informed one? Name the case that separated them again.

## Assessments — ungraded practice

These Assessments are ungraded. Preserve predictions, commands, outputs, failed cases, and revised decisions.

### Warm-up

1. **Read the proposal contract (Understand; objective: read a contract).** Explain each required field and construct one falsey value that the current function rejects. State why truthiness is not semantic adequacy, and name the field a reviewer would be least able to decide without.

2. **Trace canonicalization (Apply; objective: predict and explain).** Predict whether reversed insertion order changes the digest, run the test, and explain the role of sorted keys and compact separators. Then say what two programs in different languages would have to agree on before their digests could match.

3. **Classify gate claims (Analyze; objective: match claim to evidence).** Sort ten claims into structure, content identity, evaluation, authentication, authority, consent, or outcome. Name evidence for each, and mark the ones this fixture cannot support.

### Application

4. **Changed-target rejection (Apply; objective: demonstrate content binding).** Write the sentence that says what the gate must do, then create a simulated decision for one proposal, change only the target, and demonstrate rejection. Label the decision as fixture data.

5. **Weak complete proposal (Evaluate; objective: separate shape from substance).** Construct six nonempty fields whose content is inadequate. Explain why the structural check passes and which reviewer question exposes the weakness, and whether Claude could ask it.

6. **Evaluation set (Create; objective: build a set that can embarrass the proposal).** Build a small set containing a success, malformed proposal, refusal case, changed-content case, and structurally complete weak case. Write the expected outcomes before running, and record exclusions.

7. **Single-use extension (Create; objective: conduct an implementation).** Write the gate for a decision ID, a deadline, and atomic consumption. Give Claude Code the gate and not your code, then test expiry and replay yourself without claiming identity authentication.

### Synthesis

8. **Outcome contradiction (Evaluate; objective: check an outcome independently).** Design a post-action check that can contradict the agent's success sentence. Explain what its evidence establishes and what remains outside scope.

9. **Attestation (Create; objective: write a decision record and a sign-off).** Write a decision record naming checks performed, unchecked gaps, evidence, authority scope, and approve, refuse, or defer. Bind it to a simulated proposal. Then fill in the sign-off for your gate and decide, with a reason, whether to sign or withhold.

10. **Review backlog (Analyze; objective: design under a review budget).** Simulate several pending proposals under one stated review budget. Show which actions remain blocked, which expire, and which escalate, labeling time values as assumptions unless measured.

### Challenge

11. **Gate threat model (Create; objective: choose controls and state residual risk).** Analyze mutation after display, target aliasing, decision replay, stolen identity, reviewer overload, misleading rollback, and revoked approval. Choose controls and state residual risk for each, marking which are code and which are people.

Complete the existing [Lesson 13 knowledge check](../lessons/13-evaluation-and-approval-gates/quiz.json) after the practice. It is self-review, not another graded assessment bank.

## Capabilities summary

You can now turn an ambiguous permission prompt into a reviewable six-field proposal, serialize it consistently, fingerprint its content, and reject a simulated approval after the proposal changes, and you can explain why this establishes content binding and nothing more. You can separate evaluation from authorization, write the gate before Claude implements it, and run your own tests on what comes back. You can write a sign-off that says what was not tested and withhold it when the record does not support signing, make refusal and deferral first-class outcomes, and say which part of review Claude prepares and which part, finite attention included, stays a person's.

## Anthropics

Anthropic's [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) distinguishes evaluation components and emphasizes examining what an agent actually did, not merely its final answer. Use it to refine your tasks, trials, graders, transcripts, and outcome checks. Anthropic's [Claude Code permissions](https://code.claude.com/docs/en/permissions) documents current product behavior to compare with your course gate.

These primary links were checked for the approved research packet on 2026-09-06. Product behavior and rolling documentation can change. The six-field proposal and Python fingerprint are course mechanisms, not representations of Anthropic's authentication system. Required work stays offline; any direct API use is optional and explicit.

## Computational Skepticism

The companion's accountability chapter supplies one diagnostic the body has not used: ownership bias. See [Attestation and review](../docs/computational-skepticism.md#attestation-and-review). Its build exercise has you write the attestation for something you made and force at least three entries into the “not tested” part, saying for each whether you skipped it because it was out of scope or because time ran out. The discomfort is the signal: you want to sign a clean bill because you built the thing. Apply it to your gate sign-off. List three untested conditions, mark each as out of scope (and why) or out of time, and ask whether any is the region where harm would live.

## Irreducibly Human

The companion's chapter on supervisory cognition names a condition under which plausibility auditing fails that the body has not used: the error sits outside the reviewer's own domain knowledge, so the check sails through. See [Review capacity](../docs/irreducibly-human.md#review-capacity). It is the book's argument, offered here as a design prompt and not a measurement of any reviewer. It is also why you build the predicate by hand before conducting Claude: the capacity you hand over is the capacity you need to audit the result.

**AI should** prepare the six-field proposal, expose changed fields, assemble scoped evaluation evidence, identify missing information, and keep the action queued during review. For each pending proposal it can also state what a reviewer would need to know to notice a wrong evidence claim. It should stop at the authorization boundary: silence, timeout, model confidence, and a favorable automated score are not consent.

**Human should** inspect the exact proposal and consequential evidence, decide within their authority, and approve, refuse, defer, or escalate. Humans should match each proposal to a reviewer who can audit it, send those outside that reviewer's field to a specialist, and keep a workload that permits judgment rather than reflexive clicking.

Ask for evidence of the split in your backlog simulation: which reviewer each proposal went to, which were escalated and why, and which transcript lines show what Claude prepared.

## Forward bridge

A bound decision record still sits inside a team. Someone must own the mitigation, hear from affected people, manage retained data, and respond when a threshold is crossed, and the right to say no needs an owner and a path, not only a button. Chapter 14 moves from one approval to the governance structure around many consequential actions.
