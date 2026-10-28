# Chapter 5 — Tools and permissions
*The path looks local. Where does it actually lead?*

Suppose a tool is allowed to read files in a small course folder. A request arrives for `notes.txt`, which looks ordinary. Another arrives for `../notes.txt`, which asks to move to the parent before locating the file. A third names an entry inside the folder that is actually a symbolic link to somewhere outside it. All three are strings. Their spelling alone is not a sufficient account of the target the filesystem will use.

The research fixture tests this boundary in disposable directories. An in-root target is accepted for reading. A traversal target, a link pointing outside the root, and an unapproved write are rejected. Those are actual results of the local preflight function, preserved under `chapters.05` in the [research output](../research/worked-examples.json). They do not establish that we built a complete filesystem sandbox. The function returns a path; it does not read or write the target.

That last sentence is the center of the chapter, and it is where a recipe-follower goes wrong. You can implement the function correctly, watch every test pass, and ship a policy that guarantees far less than its name suggests. The function is called `authorize`. What it does is resolve a name, compare two paths, and hand one back. The distance between those two descriptions is the subject here.

Claude is very good at writing a function like this from a complete specification, in seconds. It cannot know which folder is yours to expose or who answers for a write, so the specification is not something it can settle for you, and it has no standing to grant itself anything. So the three jobs from Chapter 1 show up at the smallest scale that still has a real boundary in it. **Conduct:** the permission policy is a design constraint you write before any tool is granted, and it is enforced in the runtime, where a persuasive request cannot reach it. **Check:** a request can pass every test and still be a bad change, containment is not a shared prefix of characters, and the toy boundary guarantees less than it looks. **Drive:** who may do what is a decision about authority. Claude can enumerate the edge cases. It does not own the grant.

Chapter 4 bounded how many turns a controller may take. A bounded controller can still request the wrong thing once. Chapter 1 told you a system prompt is a request, not a gate, and promised that this chapter would build the gate in code. Here we narrow what any single request may touch, and express a small decision rule in executable Python so we can examine the cases that pass and fail it.

Start with a prediction. If the approved root is a folder named course, should a different folder named course-other pass because its name starts with the same letters? Should a write inside course pass merely because the location is acceptable? Should an approved execute operation pass even though the function allows only reading and writing? Each answer comes from a different part of the rule. Keeping those parts separate is how we make a policy inspectable.

The scenarios are teaching fixtures, not invitations to probe someone else's files. Use disposable material under a narrowly scoped temporary directory. Claude Code remains the assumed learning assistant through your account, but the Python boundary requires no direct API call. Do not change institutional permissions, disable safeguards, or expose restricted material to complete this exercise. The [paired lesson](../lessons/05-tools-and-permissions/docs/en.md) keeps the practical task bounded.

## What you will be able to do

By the end, you should be able to trace a requested path to the resolved target this function uses, distinguish containment from string-prefix similarity, and implement the read/write approval boundary. You should be able to explain the observed traversal and symlink rejections, and to say why a preflight result is not an operating-system sandbox or a completed file operation.

You should also be able to do three things the rest of the book builds on. Write the permission policy, with the wrong versions your tests must catch, before any implementation exists, then conduct Claude Code against that policy and run your own tests on what it returns. Write a sign-off whose "Not checked" line names what a passing preflight leaves open. And say which parts of this boundary you handed to Claude, which you kept, and why the grant itself stayed yours.

You need Chapter 4, Python exceptions, and basic path concepts: parent directories, absolute and relative paths, and symbolic links. We explain how those concepts matter to this implementation rather than survey every filesystem feature. Write your first version in your learner workspace after reading the expected behavior, then compare it with the reference once you can explain a passing and a rejected case.

## Who may do what is decided before the code exists

The first decision is not a line of Python. It is what this tool may touch and what it may do, and you answer it by asking what the task requires, not what the tool is able to do.

*Conducting AI* gives a selection rule for AI capabilities: take the lowest one that does the step, because the most constrained tool is the one you can verify. Its five-layer capability stack is my teaching device, not an industry standard, and the book says so. I borrow the instinct for grants. The book does not state it for permissions; this lesson calls the permissions version least privilege. A tool that summarizes course notes needs to read them. Every operation you add to the vocabulary is a capability you must later verify, so a write has to earn its place. A policy of one root and two operations can be audited by a stranger in a few minutes. "Be careful with files" cannot be audited by anyone.

There are two places to put such a policy. One is a sentence in the request: stay inside the course folder, do not overwrite anything. The other is a function between the request and the filesystem that raises when the request is out of bounds. Chapter 1 showed why the first is weak. A system prompt is text in a document the model is continuing, competing with every other paragraph in it. A request for caution is a hope. A function that raises `PermissionError` does not care how persuasive the request was. Enforcement lives in the runtime, where text cannot reach it.

The same move appears in the book's advice to route deterministic work out of the stochastic layers. Whether a resolved path lies under a folder has one correct answer, so it is not a matter for plausibility. Handing it to a model borrows fluent guessing for a job a comparison does exactly.

Claude keeps a role: it proposes actions, and a proposal is useful input to review. What it cannot do is grant itself the permission. That separation is the design. It also comes with a cost, and the rest of the chapter measures it. Moving a decision into code makes it checkable and makes it exactly as narrow as the question you asked the code. The function will enforce the policy you wrote and nothing else.

## A name is a request for a destination

Before you can write the policy, decide what it judges: the string someone typed, or the place that string leads. This policy judges the place.

A path is an instruction for locating an object through a filesystem namespace. A relative path depends on the base from which it is read. Parent components can move outward. A symbolic link can redirect a name toward another location. So the reference resolves the approved root, joins the target to it, resolves the result, and compares the two. Python's [pathlib documentation](https://docs.python.org/3/library/pathlib.html), included in the research packet and consulted on 2026-09-06, describes `resolve()` as resolving symbolic links and eliminating parent components. That is the narrow behavior we rely on. It does not turn a pathname into a handle on an object.

Two consequences keep the claim honest. First, containment is a statement about the destination, not about which characters look suspicious. A request can step into a subdirectory and back to its parent and still land inside the root. A request with no visible parent component can lead out through a link. On macOS, `/tmp` is itself a link to `/private/tmp`, so the lesson's own demo, given the root `/tmp/course` and the target `notes.txt`, prints `/private/tmp/course/notes.txt`. The function reports where the name leads, not how you spelled it.

Second, resolving does not require the target to exist. The reference calls `resolve()` without strict checking, and its demo says outright that no file is read or written. A returned `Path` is therefore not evidence that anything was opened. Existence, object type, access at the moment of use, and success are separate questions. This matters most for writes: a file you are about to create does not exist yet, so the preflight can accept a location it cannot inspect, and acceptance neither creates the file nor shows that its contents are valid.

## The gate: write the policy before the function

Now do the part Claude cannot do for you. In your learner workspace, before you write or request any implementation, write the policy as a short contract, then the list of wrong versions your tests must catch. Chapter 1's gate fixed an experiment. This one fixes a grant.

```text
Gate — permission policy for the course-notes tool
Root:        one disposable directory, named here              (my decision)
Operations:  read and write. No other operation, ever.         (my decision)
Approval:    a write needs a human approval I can name;        (my decision)
             in my tests it is a simulated fixture, labeled as one
Must accept: a contained read; a contained write with approval
Must refuse: traversal out of the root; an absolute path into a
             sibling that shares the root's name prefix; an in-root
             link whose destination is outside; a contained write
             without approval; execute, even with approval; an
             approval value that is not exactly True
Moves on only when: my own tests pass on the implementation, run by me
May claim:   that a proposal passes a preflight. Never that a file
             was read, written, or approved by a person
```

Every line is yours, including the ones that look arbitrary: why exactly `True` and not any truthy value, why execute is refused even with approval. Claude may propose a refusal you missed. You accept or reject it, mark an accepted one as Claude's proposal, and keep the policy in your words.

Then comes the part that makes this a gate and not a wish list: the wrong versions. The six lesson tests are a good start, and they catch some plausible mistakes. They do not catch others. Write each of the following as a variant of your own function, predict whether the six tests will fail it, and run them to see:

- Containment by string prefix: replace the relation with `str(path).startswith(str(base))`.
- Textual cleanup of `..` with no link resolution: replace `resolve()` with `os.path.normpath`.
- Truthy approval: replace `approved is not True` with `not approved`.
- A joined but unresolved return value: return `base / target` instead of `path`.

The sibling test fails the first variant. The other three pass all six lesson tests, because the lesson's success tests check only the final name of the returned path, none of them builds a link, and none passes an approval value other than True or absent. Those gaps are the reason your test list is longer than six: a symlink case, a non-Boolean approval case, and a check that the returned path is the resolved one. A test list that cannot tell these variants from the right program is not a gate yet.

Finally, write one sentence about what you would see if your function were wrong, and date it before you run anything. Written afterward, it describes the output instead of testing your understanding.

Claude can sharpen this gate. It cannot write it for you without defeating its purpose. The gate is where your decision about authority goes on the record, and it is what you will measure Claude's implementation against.

## Three decisions in eleven lines

Here is the [reference implementation](../lessons/05-tools-and-permissions/code/main.py). Build your own attempt before using it as a reference.

```python
from pathlib import Path

def authorize(root, target, operation, approved=False):
    if operation not in {"read", "write"}:
        raise PermissionError("Operation is not allowed")
    base = Path(root).resolve()
    path = (base / target).resolve()
    if not path.is_relative_to(base):
        raise PermissionError("Path escapes the data boundary")
    if operation == "write" and approved is not True:
        raise PermissionError("Write requires human approval")
    return path
```

Read it as three decisions, in the order the function makes them. The first is the operation vocabulary. Only read and write are allowed, and execute is refused even with approval true, before the path is resolved at all. Approval is not a universal override of the allowlist. The second is the target: resolve the root, resolve the joined path, and require the result to be relative to the base in the path sense. A sibling with a similar prefix is not a child because its characters begin the same way. The third is writes: `approved is True`, an exact identity comparison, so the function asks for the Boolean True and not any arbitrary truthy object. That is the interface rule you wrote in your gate. It does not prove a human reviewed the request that produced the value.

The return value is the resolved path. There is no `open`, `read_text`, or `write_text` in these lines, and the name `authorize` must not inflate what they implement. The function checks a proposed operation under a supplied root and approval value. It does not perform the operation, and it does not authenticate where those inputs came from.

That is the pattern of the book so far, now attached to a filesystem. The probability function did not validate the truth of outcome labels. The format validator did not validate source support. The capability classifier did not authenticate its event list. The path check does not authenticate its approval flag. Each time the move is the same: find the input the function trusts, and write down what must justify it somewhere else. If the caller supplies an overly broad root, the containment check will enforce that broad root faithfully.

*Conducting AI* names this location of risk. In a multi-step workflow the risk sits less inside any one tool than at the seam where one step's output is handed to the next on trust, and for each seam you state three things: what is passed, what it is trusted to be, and how that trust was earned. This function has two seams. The root and the approval value come in. The path goes out. The next sections take them in turn.

## Containment is not a shared prefix

Imagine two sibling directories under a disposable parent: course and course-other. A target inside course-other must not be accepted under a policy allowing only course. A string test that asks whether the target starts with the text naming course confuses the two. The reference asks about a relation between resolved paths instead, which is why the prefix variant in your gate fails.

An absolute target shows why the function inspects the combined result and does not trust concatenation. When the second operand of a pathlib join is absolute, the first is discarded, so placing a root variable before a target expression does not force the target inside it. The [lesson tests](../lessons/05-tools-and-permissions/code/tests/test_main.py) include an absolute sibling target and a parent traversal, and the reference rejects both. Those are results for specific inputs in a local environment. They do not cover every filesystem configuration or any concurrent change.

For a hand trace, record separate values: the root argument, its resolved base, the target argument, the resolved combined path, and whether containment passed. If you record only the original string and the word denied, a reviewer cannot see why the boundary fired. Temporary directories get a different name on each run, so label them by role: approved root, outside sibling, target, resolved destination. The invariant is the containment relationship, not a random suffix.

## The symlink that leaves the folder

The research script creates a symbolic link inside a temporary root that points outside it. The link's name is local. Its destination is not. When the function resolves the target and tests containment, the request is rejected, and no read of the outside file is needed to demonstrate that. This is an executed fixture, preserved in the [research script](../research/worked_examples.py) and its output.

The case shows why "the name is inside the folder" and "the resolved target is inside the folder" are different claims. A directory listing can show a local entry whose destination is elsewhere, and a policy written in terms of visible names would miss it. Test the parent-component route and the link route separately. The mechanism differs, but the final question is the same containment relation, and neither string pattern covers the other.

Now the time boundary. The function checks and returns. A later caller may open a file. The reference does not bind the check and the operation into one indivisible act, and the research run does not attempt to prove resistance to changes by another process. Be precise about what that does and does not imply. If the caller uses the returned resolved path, replacing the original link entry need not redirect it, so it would be wrong to claim that every swap defeats this function. The honest gap is narrower: it is a preflight pathname check that returns a pathname, and it establishes nothing about the later access.

The returned path is the second seam, and the failure there needs no race at all. A careless caller can check one path and then open the original, unchecked target. The teaching function cannot force anyone to use its result. This is the laundering shape from *Conducting AI* in miniature: something unverified takes on the look of something verified because it passed near a reassuring step. A call named `authorize` somewhere earlier in a program reads as though the later open were covered. When you review a larger program, follow the value that reaches the open call, not the presence of the word.

These limits do not erase the observed rejection. They locate it. In a constructed, stable fixture the function rejected an outside-pointing destination, and that is the result you can report. Protection against every later mutation is a separate item to document, not a reason to pretend the test accomplished nothing.

## Read and write are different authority questions

Which operations need a human, and which do not? This policy answers: a contained read does not, and a contained write does. That is a judgment about consequences, and it is yours to make for each task.

An in-root read passes without a separate approval flag. That is a deliberate rule for the exercise, not a statement that every file under any root is appropriate to read, upload, or disclose. A read changes nothing in the filesystem, but what it exposes cannot be un-exposed once it has left the folder. The *Computational Skepticism* delegation chapter asks of each sub-task whether the action can be undone. That chapter's five-question score is the author's own instrument with no external validation, so use it as a question, not as a number. The approved root must already reflect the task's data boundary. If it holds material the workflow should not touch, the policy is wrong for that task, however correct the code.

A write inside the same root is rejected unless approval is exactly True. This separates two questions: is the target in the allowed location, and has the extra write condition been met? Passing containment cannot substitute for the second. The same target can be accepted for reading and rejected for writing without inconsistency. The lesson tests an accepted write proposal with True and a rejected one without it. Again, accepted proposal is the right phrase. A report that says the test wrote `x` because the returned path ends in `x` confuses an authorization result with execution.

What does the flag represent? In this model, a decision supplied from outside the function. It is not a user interface, a signature, an identity check, or a record that someone saw the precise change. If you place True in a fixture, label it a simulated approval input and do not attribute it to a person.

Here is the first seam, held to the standard of the same companion book. A handoff condition is worth having only if a stranger can read it, observe the system, and decide whether it was met. A Boolean fails that standard the way "the human reviews it" does: a reader can see the value and cannot tell whether anyone decided anything. A condition a stranger can test is richer. The approval names the operation, the target, and the approver, was issued before the call, and its target matches the request. Challenge item 11 asks you to build that. Even then, a record only moves the unsolved problem, because nothing here authenticates its contents.

Approval for a disposable draft is not approval to overwrite an original, and approval for one target is not a license over a directory. The surrounding process must bind its decision to the actual operation and target. A model can propose an action and explain why. It does not get to produce its own independent human approval by writing the word approved. The source of the approval value matters as much as its type.

A human in the loop is also not automatically a control. The same companion chapter says that when checking is expensive, the cost structure pushes a supervisor toward accepting, and it calls that economics acting on attention, not a character flaw. I extend that to grants, as my reading and not the book's claim: if approval is requested for every small step, the answer can drift toward yes. Make approvals rare, specific, and tied to the actual change.

Last, the policy refuses operations outside its allowlist even with approval set. If your task needs another operation, change the policy deliberately and review the new risk and tests. Do not stretch write to mean anything a tool might execute. A small vocabulary is useful only while its entries stay specific enough to enforce.

## Work through the boundary matrix

The matrix is the executable half of your gate. The policy says what must hold; the matrix says which proposal exercises which branch. Use a disposable parent with an approved subdirectory and a separate outside location. The research fixture exercises an in-root read, traversal, an outside-pointing symlink, and a write without approval. The lesson tests add the Boolean-approved write and the rejection of execute. These sources let us explain the matrix without inventing live system behavior.

| Proposal | Relevant result | What it establishes |
| --- | --- | --- |
| Contained read | Path returned | Proposal passes the displayed preflight |
| Escaping traversal | PermissionError | Resolved target fails containment |
| Outside-pointing link | PermissionError | Resolved destination fails containment in the fixture |
| Contained write, no approval | PermissionError | Containment does not waive write approval |
| Contained write, True fixture | Path returned | Simulated approval input satisfies this check |
| Execute | PermissionError | Approval cannot override the operation allowlist |

Read the rows as branches. The contained read passes all three checks, and what it shows is that the proposal passed preflight, not that the target exists or was read. In the traversal row the operation vocabulary is satisfied while the resolved target escapes, so the containment branch fires; a read can be out of scope. The link row ends in the same branch by a different route, which is the reason to test both. The unapproved contained write passes the first two checks and fails the third, the one case that proves location and operation authority are separate. The execute row fails first, without resolving anything, because an operation outside the vocabulary needs no path inspection.

This table is not a security certification. It maps implemented conditions to observed or directly tested results, so another reader can locate the relevant branch and decide what question their application still has to answer.

<!-- [FIGURE: Cajal production brief. Resolved destination and write approval are separate gates. Include approved root, in-root file, link in root, outside sibling, containment gate, write gate. Show the confirmed relationship that local-looking names can resolve outside. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Resolved destination and write approval are separate gates. local-looking names can resolve outside.](../images/05-tools-and-permissions-fig-01.png)
*Figure 5.1 — Resolved destination and write approval are separate gates*

## Build It: make denials explainable

Implement the operation allowlist, path resolution, containment check, and write condition in your learner workspace, against a disposable fixture. Do not begin by giving a tool broad filesystem access to see whether it behaves politely. The thing under examination is the preflight function. Your version is the baseline: the record of what you understood before Claude touched anything, and the instrument you will measure its version against.

Read the six lesson tests before the reference, and predict not just accept or reject but which rule produces the result. If the sibling-prefix case passes in your version, check whether you used a string test where a path relation was needed. If an unapproved write passes, check that your write condition is independent of containment.

Keep each test narrow enough to explain. A proposal that combines an unknown operation, an escaping path, and missing approval will be rejected, but it does not say which boundary you meant to test. To test a later check, let the earlier ones pass. Add a meaningful success outside the demo as well as the denials: a policy that rejects everything passes a denial-only suite and fails the authorized task. For the symlink fixture, keep source and destination in a disposable arrangement. Outside the allowed root need not mean a real personal or system file, and cleanup goes through the temporary-directory lifecycle, not broad deletion commands.

## Use It: conduct Claude Code against your gate

Now hand Claude the work it is good at. The lesson's [working prompt](../lessons/05-tools-and-permissions/outputs/claude-code-prompt.md) covers the earlier stage, in which Claude asks for your prediction and lets you attempt the mechanism first. This stage is the one that follows your baseline: you give Claude a finished gate.

Open Claude Code in your learner workspace, on disposable fixtures. Give it your policy block and your test list, not your implementation. Ask for an implementation of `authorize(root, target, operation, approved=False)` that uses only the standard library, satisfies the policy, and passes your tests. Then run your tests yourself. A statement from Claude that they passed is Claude's report, not your evidence.

Do three things with what comes back.

First, note which of your tests failed, if any. A failing test is often a gap in the gate, which Claude cannot see because it has only what you wrote. Decide whether the gate or the code is wrong, and write down which.

Second, compare its function with your baseline and name one difference in behavior, not in line count or style. It may handle a boundary you missed, which revises your gate. It may ignore a case your tests never covered, which is a defect your tests failed to catch.

Third, check that your tests would catch a wrong version of its function. Apply the variants from your gate to it, one at a time, and add any wrong version Claude proposes. Every variant that survives your test list is a gap in the list. The reason is independence. Tests Claude writes for the function Claude wrote share its reading of your policy. *Conducting AI* makes the general point about cross-checking: a second checker reduces error only to the degree that it fails differently from the first, and a checker that fails the same way adds agreement, not verification. Your tests, written first, and the variants you built by hand fail differently from its implementation. Let Claude add cases and treat each as a proposal: read it, run it, decide. Ask it whether a passing assertion could still hide the defect you care about, then check its answer against the actual branches. A generated assurance that the code is secure should be narrowed to the conditions the tests demonstrate.

Preserve the transcript: your prompt, the plan, the diff, the commands, and the outputs, with the date and the displayed model label. If the session failed or did not run, record that rather than substituting a fixture.

Then compare your toy with a real boundary, read-only. The lesson asks you to inspect the permission configuration available in your Claude Code environment. That is a comparison, not authorization to change university settings or disable protections. Anthropic's [Claude Code permissions documentation](https://code.claude.com/docs/en/permissions), checked in the research packet on 2026-09-06, describes runtime permission rules. The useful point of comparison is that executable rules mediate actions rather than relying on prompt prose. Our function models only a small path-and-operation preflight and does not reproduce the product's permission system. Product details change, so do not substitute this chapter's Boolean for a current product policy.

Choose a narrow task on harmless learner material. Name what may be read, what may be changed if anything, and what evidence would show the boundary was respected. If no write is needed, do not add one for effect. If you perform an authorized edit through a real tool, record the actual target and inspect the resulting change. Passing preflight, receiving runtime permission, performing the operation, and reviewing the diff are four events, and the fact that they occur in one workflow does not make them interchangeable. If configuration access is unavailable, mark that part not inspected. Do not guess institutional rules, invent a screenshot, or report a protection as enabled because you remember that a product can support it.

## What the toy boundary cannot guarantee

What does a passing preflight leave open? That question writes the "Not checked" line of your sign-off, so answer it with the five limits below. A fluent list of limitations is as easy for Claude to produce as a fluent claim of security. For your artifact, tie each one to what you actually did about it: inspected, tested, or left alone.

The first is coverage. The function protects nothing that bypasses it. A larger program could call `authorize` and then use a different path or operation, so reviewing integration means following the returned value into the actual file operation and checking that every relevant route is mediated. The local tests do not show that property for an arbitrary application.

The second is authentication. The function has no independent account of who supplied the root or the approval value. A True fixture satisfies the Boolean check and proves nothing about consent. A trustworthy workflow needs a real source for that decision and a scope that corresponds to the proposed action. This lesson implements neither.

The third is time and filesystem state. The path is checked before use, and the function does not make a later open atomic with the check or freeze the path components. The rejection of one stable outside-pointing link does not prove resistance to every concurrent scenario. Do not claim a race exploit was executed unless you performed and recorded a safe test of one.

The fourth is meaning. An approved write can contain a bad change. The function does not inspect a diff, run a program, or judge whether the output serves the user's purpose. Permission answers whether the proposal satisfies a boundary. Review answers whether the proposed content is acceptable. The next chapter takes that second question seriously.

The fifth is data policy beyond location. A contained file may hold restricted information, and a later step may disclose it somewhere inappropriate. This preflight has no destination-channel policy, retention schedule, or content classification. A root is one useful boundary, not a description of every data obligation.

None of this is a reason for vague helplessness. The function has a well-defined educational job, and the fixture shows it doing that job. Precision lets protections accumulate without one small protection impersonating the whole system.

## Ship It: a permission policy with evidence

The artifact is your gate, as run. It states the approved root, allowed operations, approval owner or simulated approval source, denial cases, and actual test results. Use the [artifact brief](../lessons/05-tools-and-permissions/outputs/artifact-brief.md) for repository expectations. Keep NEU grading logistics outside this chapter, and keep your learner changes separate from the reference.

For each proposal, preserve the requested target and the role its resolved destination played in the fixture. Record whether the function returned or raised and which branch decided. If a later file operation was not performed, say so; a preflight-only experiment is complete on its own terms when its stated task was to test preflight behavior. Include at least one denial that matters to your eventual capstone, and connect it narrowly. If the capstone saves a draft under an approved directory, the write-approval and target checks are relevant, but they do not show that the draft is correct or the capstone secure. Name the supported claim and the next check it needs.

Record the source of each approval value. For tests, write simulated fixture. For an actual action, preserve the relevant real authorization without exposing private information. Never turn a Boolean in a script into a claim that a named person approved something. The evidence record must not invent the human act it is supposed to document. Finally, state one decision you revised after testing, with your original prediction and the result that changed it.

**The sign-off.** End the artifact with a statement you could put your name to. Claude can draft its words in seconds, and the draft will be fluent. The line it will not write honestly is the one about what you did not test, so write this from your record. This is a template, not a signature:

```text
Sign-off — permission policy and preflight function
Checked:      which refusals and which acceptances, by name (traversal,
              sibling prefix, outside-pointing link, unapproved write,
              execute with approval, non-Boolean approval)
How:          tests I wrote before reading the reference / hand traces of
              resolved paths / with Claude's help (say which cases it
              proposed and which I kept)
Not checked:  changes between check and use; whether any caller uses the
              returned path; who supplied any approval value; the content
              of any write; operating systems and Python versions other
              than ____; any real Claude Code configuration I did not inspect
Not claiming: that this is a sandbox; that anyone approved anything (every
              approval in my tests is a simulated fixture); that a returned
              path means a file was read or written
Signed or withheld: ____________  (name, date)
```

A sign-off that claims more than the record supports is the failure this chapter is about. If your evidence does not support signing, withholding is an honest result.

## The driver's seat

This is how the chapter's work divided, task by task. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Choosing the root and the operation vocabulary | List what a task like yours might touch, and what the root also contains | Decide the smallest root and vocabulary that suffices | Only you know what is in the folder, whose it is, and what disclosure would cost |
| Naming who approves a write and what the approval binds to | Draft candidate approval records and say what each cannot prove | Name the approver and the scope, and make the grant | Authority and accountability are a person's; Claude cannot approve its own request |
| Listing edge cases | Propose cases: links, absolute targets, siblings, unknown operations, non-Boolean approval | Write the first list yourself, then choose which proposals become tests | The list is your understanding on the record, and you know which failure matters in your capstone |
| Implementing the function from the gate | Write it, fast | Run your tests on what it returns and compare it with your baseline | You cannot audit a boundary you never built or broke |
| Saying what a pass establishes | Flag an overclaim | Choose the verb, then sign or withhold | Your name is on the claim |

Record, in the artifact, one task you delegated and one judgment you retained, each pointing to a transcript line, a diff, or an edit you made. If you cannot point to them, the split happened in your head and not in the record.

## Verify and reflect

From the repository root, run the demo and the six tests, then your additional fixture cases:

```bash
python3 lessons/05-tools-and-permissions/code/main.py
python3 -m unittest discover -s lessons/05-tools-and-permissions/code/tests -v
```

Compare with the [saved research results](../research/worked-examples.json) while keeping your own environment and output record. The research script demonstrates the stable symlink and traversal cases in disposable directories. It is evidence for those cases, not a claim that every security property has been tested.

Then audit the artifact's nouns and verbs. Does authorize mean a preflight decision or a complete approval system? Does read mean permission to read or a completed read? Does safe mean contained under this root or secure against every attack? Replace each ambiguous word with the event and condition that occurred. Ask one integration question: if another function receives the returned Path, what must it still do correctly? The answer should include using the checked target consistently, handling real operation failures, and keeping the review boundaries in place.

The most useful reflection is local. Which distinction did you originally collapse? The spelling of a path and its destination, a location and an authority, a preflight and a performed operation, or a Boolean and a human act? Name the case that separated them again.

## Assessments — ungraded practice

These Assessments carry no points. Use the paired lesson's existing [knowledge check](../lessons/05-tools-and-permissions/quiz.json) and preserve predictions before viewing explanations. All filesystem experiments must use disposable fixtures. Do not read unrelated data, broaden permissions, or perform destructive operations to demonstrate a boundary that can be tested harmlessly.

### Warm-up

1. **Trace the destination — introductory; objective: explain resolution.** Choose an in-root fixture target and record the root argument, resolved base, target argument, and resolved target. Predict whether preflight returns. Explain why the returned path is not evidence of a completed read. Keep the fixture simple enough that each intermediate value has a clear role.

2. **Three checks, three reasons — introductory; objective: identify policy branches.** Construct separate cases for an unknown operation, an escaping destination, and an unapproved contained write. Predict the branch responsible for each refusal. Explain why combining all three defects in one proposal would make the test less useful for isolating the later checks.

3. **Inside does not mean approved — introductory; objective: separate location and authority.** Use the same contained target for read and write proposals with approval absent. Predict and run both. Explain the policy difference, what a fixture True would establish if supplied, and who in a real workflow would have to supply it. Do not describe the fixture as a real person's consent or the returned path as a performed mutation.

### Application

4. **Sibling-prefix rejection — intermediate; objective: test containment.** Create disposable sibling directories with similar names and demonstrate that the outside sibling fails under the approved root. Explain why a character-prefix rule would ask the wrong question. Preserve the actual resolved relationships rather than relying only on a screenshot of directory names.

5. **Traversal, with Claude proposing the cases — intermediate; objective: implement a denial case and choose among proposals.** Write a parent-traversal denial in a disposable parent arrangement, with your prediction of its resolved role and the expected exception. Then ask Claude for three further edge cases, and for each say whether you added it to the gate and why. Explain why the demonstration needs no unrelated personal or system file outside the approved root.

6. **A local link with an outside destination — intermediate; objective: inspect symbolic links.** Create an in-root symlink pointing to a disposable outside location. Predict and verify rejection. Explain the relationship between entry location and resolved target. State the limits of this stable fixture and do not claim you demonstrated resistance to concurrent filesystem changes.

7. **Useful acceptance — intermediate; objective: test the permitted side.** Add a successful case outside the demo and explain which legitimate task it represents. Pair it with a relevant denial case. Show why a function that rejected every proposal could pass a denial-only suite yet fail the intended workflow. Keep actual file operations separate from preflight results.

### Synthesis

8. **A capstone boundary proposal — advanced; objective: write the gate and integrate scope.** Describe a narrowly scoped file task for your capstone and write its gate: root, operations, approval source, refusals, and the wrong versions your tests must catch. Mark which decisions are yours and which Claude proposed. Map each requirement to the toy function or to a missing mechanism. Do not claim the function covers data retention, identity, or content quality merely because the path is contained.

9. **Check one value, use another — advanced; objective: review integration.** In a harmless learner example, show a caller design that checks a path but later uses a different unchecked value. Explain why the presence of authorize is insufficient. Propose a corrected data flow and a test that would expose the mismatch. Do not perform an out-of-scope real file operation to illustrate it.

### Challenge

10. **A precise race discussion — stretch; objective: evaluate limits.** Describe a hypothetical change between preflight and use that the function does not prevent. Distinguish use of the returned resolved path from reopening the original link name. Identify what your argument establishes and what would require an actual safely designed experiment. Do not present a speculative sequence as an observed exploit.

11. **Richer approval scope — stretch; objective: redesign authority representation.** Propose a learner-only approval record that names the operation and target rather than only a Boolean, and write its handoff condition so that a stranger could decide from the record alone whether it was met. Explain how a caller would check correspondence and which identity problem remains unsolved. Add a mismatched-target test. Keep simulated approvals labeled and avoid claiming that adding fields authenticates their contents.

## What you can now defend

You can explain why the path's destination matters more than its reassuring appearance. Resolving the approved root and the requested target gives this preflight a concrete containment relation to check. You can trace parent traversal, a similar-looking sibling, and an outside-pointing link to the relevant rejection, and keep the claim bounded to the tested behavior. You can also explain the independence of operation, location, and write approval: an allowed operation can target an outside location, a contained target can fail the write condition, and a True approval cannot override an operation outside the allowlist.

You can distinguish a returned Path from a completed file operation, and a Boolean approval fixture from a human act. That precision protects the evidence trail from a subtle form of invention, describing a preflight result as though a person approved and a tool executed the proposal.

And you can say what the three jobs looked like here. You conducted: you wrote the policy and the wrong versions your tests had to fail before Claude wrote a line, and the enforcement sat in code where a request's wording could not change it. You checked: you ran the tests yourself, tried variants Claude did not write, and named in the sign-off what a passing preflight leaves open. You drove: you handed Claude the implementation and the list of edge cases, kept the root, the vocabulary, the approver, and the verb, and signed or withheld.

## An authorized change can still be a bad change

Suppose a proposed write passes every check in this chapter and is performed under a real, appropriately scoped approval. The target is correct. The operation is allowed. The file changes. We still have not asked whether the new contents are any good, and a permission boundary should not be asked, because it never inspects the diff.

Chapter 6 turns to evidence-based review of a change. We will compare a small incorrect implementation, an inadequate patch, and a correct patch on constructed inputs. The review will keep apart a proposed edit, tests actually run, and a human decision about whether the change is acceptable.

Carry the boundary record forward. It establishes which target and operation were in scope. The diff and test evidence will establish different properties of the content. Permission without quality review can authorize a mistake. Quality without permission can produce an excellent change to the wrong thing. Your sign-off already says which of those two you did not check.

## Anthropics

Compare the Python operation allowlist with [Claude Code permissions](https://code.claude.com/docs/en/permissions), checked for the research packet on 2026-09-06. The relevant connection is runtime enforcement: requesting caution in prose is not the same as constraining tool actions through permission rules. Our teaching function is only a preflight illustration, not a reproduction of the product's safeguards.

Inspect the actual configuration available to your course environment without changing institutional settings. Document one enforceable boundary and one question your small path function cannot answer. Keep any unavailable information marked uninspected. The comparison should sharpen your permission policy, not encourage bypassing a boundary in order to make the demonstration more dramatic.
