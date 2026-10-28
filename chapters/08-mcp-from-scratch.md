# Chapter 8 — MCP from scratch
*A tool can introduce itself perfectly and still deserve no trust.*

Suppose two servers advertise a tool called `lookup`. Both return valid JSON-RPC messages. Both copy request identifiers correctly. One reads a declared public fixture. The other writes files as a side effect. Protocol syntax cannot tell the two apart, so it cannot tell you that they deserve different permissions. Interoperability answers whether components can exchange messages they understand. Authorization answers whether a particular capability should run in this task. A clean handshake settles the first question and is silent on the second.

Claude, handed only the listing, has two descriptions to compare, and a description is a sentence the server wrote about itself. What Claude lacks here is not skill with JSON. It is any standpoint on whether this server belongs in this task: whose data sits behind it, what a stray file write would cost, who maintains it. That is the decision, and it is yours. This is the book's three jobs at the scale of one connection. Conduct: fix the order of events and the scope of use before anything is connected. Check: ask what a transcript entitles you to believe and what it never tested. Drive: let Claude read the transcript and list every discrepancy, and keep the decision to connect for yourself.

We will build the smallest useful version of that distinction. The teaching server implements initialization, an initialized notification, tool listing, and one read-only lookup. It keeps two Boolean state variables, rejects a tool request made too early, and separates protocol errors from a tool result whose `isError` field is true. Every transition fits on one screen, which is the point: you can audit a machine you can hold in your head, and you cannot audit one you have only been told about.

The research run records four observations of the local Python server, preserved under `chapters.08` in the [research output](../research/worked-examples.json). Listing tools before initialization returns an error. An initialize request returns protocol version `2025-11-25`. A valid initialized notification returns no response. Looking up an unknown record produces a tool result with `isError: true`. These are executed observations of this server, not claims about MCP generally.

The version result needs careful language, and the care is part of the lesson. The server returns its one supported version without inspecting the client's requested version. Under the versioned MCP lifecycle specification, a server may return another supported version when the requested one is unsupported, leaving the client to decide whether it can continue. A fixed fallback is therefore not, by itself, a violation. Our server remains a teaching subset, and the next sections say exactly what it leaves out.

Protocol education decays into a cargo cult of field names unless you read the lifecycle as behavior: which message may come next, what state changes, which response belongs to which request, and what the host may infer from a result. A message can copy every visible key of the example and still miss the state machine around it.

Claude Code remains the assumed course assistant, but this server runs offline and needs no direct API credits. You may later connect a client in an explicitly controlled exercise. The default demo terminates without waiting on standard input. Do not claim a live Claude integration unless you actually configured, ran, and recorded it.

## What you will be able to do

By the end, you should be able to trace initialization and readiness as separate state transitions, match requests with responses by identifier, inspect the advertised tool schema, and tell a JSON-RPC error from a tool result marked as an error. For any connection you should be able to keep four questions apart: is the exchange well formed, does the code do what the listing says, may this task use it, and does the returned content support the claim built on it.

You should also be able to do three things the rest of the book builds on. Write the connection gate, a lifecycle table plus four ledgers, before any server is connected, then conduct Claude Code against it and run your own tests on what it returns. Ask Claude to list the discrepancies in a transcript without letting it make the decision. And write a sign-off for the evaluation packet that names what you did not check, and say which parts of the work you handed to Claude, which you kept, and why.

You need Chapters 4 through 7, JSON objects, state, and basic standard input/output. The paired [lesson](../lessons/08-mcp-from-scratch/docs/en.md) contains runnable instructions and the existing knowledge check. Build your own state machine before consulting the reference. Predict what should happen when each message arrives out of order.

## Four parties and one decision

A connection has four parties, and most confusion about MCP is confusion about which party did what. The server implements capabilities and describes them. The host constructs requests, interprets responses, exposes selected tools to Claude, and decides what content enters context. Claude, or a workflow around it, proposes using a tool. People and policies define authority. MCP itself supplies a communication structure. It did not choose the tool, and it does not vouch for what comes back.

Three of those parties are software, and none of the three can answer the fourth's question: whether this server, this data, and this action are appropriate for this task. The server cannot, because its description is its own testimony. The host can enforce a policy but cannot write one. Claude can weigh a tool description against a request, but in this task it has only what the session supplied, which does not include who owns the data, what the task is for, or what a wrong answer costs. Chapter 3 drew the line between capability and authority, and Chapter 5 made the permission policy a design constraint you author. This chapter puts that line on a wire: the protocol carries the capability declaration, and the authority is written somewhere else, by someone, before the call.

## Initialization is a state transition

Before any code, decide when the server is allowed to do anything. The protocol's answer is a sequence, and a sequence is a state machine. State the rule about order first, then check that the code enforces it. The other direction, reading the code and discovering the rule inside it, is how a rule you never chose becomes the rule you have.

The reference server begins with two states set to false:

```python
class Server:
    def __init__(self):
        self.initialized = False
        self.ready = False
```

These flags are related but not interchangeable. A valid initialize request sets `initialized` to true and returns server information and capabilities. A later `notifications/initialized` message, arriving while `initialized` is true, sets `ready` to true. Tool operations are rejected until ready.

Why two steps? The request and response let client and server exchange protocol information, and the notification lets the client say it has finished that phase. The design choice is to make readiness a statement by the client and a precondition for the server, instead of inferring it from the fact that a process exists or that a tool list could be built. The price is state, and every piece of state is a place where two parties can disagree about history. A stateless server would be shorter to write and impossible to hold to an order.

The first check in `handle` validates that the message is a dictionary with `jsonrpc` equal to `2.0`, and otherwise returns an invalid-request error with a null identifier. That is a narrow rule, not every JSON-RPC validity condition.

A message with no `id` is treated as a notification. If its method is `notifications/initialized` and the server has already initialized, readiness becomes true. Either way the handler returns `None`. No response is the expected behavior on this route, not a lost message to patch with an invented acknowledgement. If the notification arrives before initialize, nothing changes and the handler still returns `None`. Silence looks the same in both cases, so a client cannot infer readiness from receiving nothing. It has to keep its own record of the lifecycle it is taking part in.

## The initialize exchange

What can an introduction establish? For method `initialize`, the server sets its first state and builds this result:

```python
result = {
    "protocolVersion": "2025-11-25",
    "capabilities": {"tools": {}},
    "serverInfo": {
        "name": "info7375-readonly",
        "version": "1.0.0",
    },
}
```

The complete response wraps that result with the JSON-RPC version and the request's identifier. The client can read the declared protocol version, capability category, name, and implementation version. These are inputs to a compatibility decision. They are not independent evidence that the server behaves as described, because the process under review wrote them.

The versioned [MCP lifecycle specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle), checked for the research packet on 2026-09-06, describes initialization parameters including the requested protocol version, client capabilities, and client information, followed by a server response containing its selected version and capabilities. It also defines fallback behavior when the requested version is not supported.

Our server does not inspect a `params` object on initialize. The recorded run sends an initialize request whose requested version is `unsupported-fixture`, and the server answers `2025-11-25` all the same. On this branch it cannot distinguish a supported request from a malformed one. Capability negotiation is just as narrow: the server declares a tools capability with an empty object and checks nothing about the client. That suffices for the tool list that follows. It does not certify any lifecycle clause.

This is a Check lesson in miniature, about the strength of a claim. "The fixed version violates MCP" overstates the case, since a server may return another supported version. "The teaching server does not evaluate the requested version or validate the required initialization fields, so it is not a conformance implementation" names the mechanisms actually missing, and it tells you which test to write next. A criticism too broad to test is one more fluent claim.

<!-- [FIGURE: Cajal production brief. Initialization and readiness are distinct protocol states. Include initialize id 1, initialize result, initialized notice, ready, tools/list id 2, early request rejected. Show the confirmed relationship that protocol shape does not authorize tools. Exclude unverified relationships, decorative elements, product-interface simulation, gradients, shadows, rounded corners, three-dimensional effects, and color-only meaning. The SVG and PNG are generated publication assets; retain this comment as figure provenance.] -->
![Initialization and readiness are distinct protocol states. protocol shape does not authorize tools.](../images/08-mcp-from-scratch-fig-01.png)
*Figure 8.1 — Initialization and readiness are distinct protocol states*

## Discovery reveals a declared capability

After readiness, a `tools/list` request returns one tool description. Its name is `lookup`. Its description says it reads a public course fixture. Its input schema requires exactly one property, `key`, which must be a string.

```python
{
    "name": "lookup",
    "description": "Read a public course fixture",
    "inputSchema": {
        "type": "object",
        "properties": {"key": {"type": "string"}},
        "required": ["key"],
        "additionalProperties": False,
    },
}
```

A host uses this to build a request, and in some integration designs a model or a user uses it to decide whether the tool is worth calling. It is server-supplied text about the server. Put to it the question the companion book on computational skepticism asks of any explanation: who is reading this, and what do its words mean to that reader? "Read a public course fixture" is accurate in the author's sense, because the code consults one mapping. But "public" is a classification of data, and nothing in the code classifies anything. The server cannot tell you the fixture is public. That word belongs in your permission ledger, filled in by whoever owns the data. A description can be technically accurate and still carry a word the server had no standing to assert.

A defective or malicious server could advertise a harmless purpose and do something else, so evaluating a candidate takes source inspection, sandboxing, provenance, or other evidence appropriate to the deployment, not faith in its description. The same holds for how a model meets the text. In Chapter 1 you saw that a system prompt is a request, not a gate. If a host places a tool description in Claude's context, it is more text competing for influence there, and a misleading description can steer which tool gets chosen before any runtime check runs.

The schema and the implementation should correspond. The call branch verifies that arguments are a dictionary with exactly the key `key`, and that its value is a string. That correspondence is inspectable, and it is the kind a listing alone can never show. It does not establish that every possible schema feature would be enforced, because this tool uses a tiny schema.

Discovery is not consent to call. A host can learn which tools exist and still deny them under its permission policy. A read-only tool may suit public course fixtures and not restricted material. A write-capable server needs a different action boundary even when its listing is equally well formed.

## Requests, identifiers, and tool results

What is the host entitled to conclude from a reply? A `tools/call` can go wrong at three layers: the lifecycle (the call came too early), the request (the tool or its arguments are wrong), and the task (the lookup ran and found nothing). The reply tells you which, if you read it that way.

A call carries the method `tools/call`, a request identifier, and parameters naming the tool and its arguments. The server first checks that params is a dictionary and the name is `lookup`. An unknown tool produces JSON-RPC error code `-32602` in this teaching implementation. It then checks the exact argument structure. Missing, additional, or non-string `key` arguments produce another `-32602`, with the message `Expected a string key`. Both are request-validation failures: the tool never produced a content result.

For a valid lookup the server consults one local mapping. The key `office` yields `505A Dana Hall`. Any other string yields a result whose text is `Record not found` and whose `isError` value is true.

The missing record is not a JSON-RPC error. The request was well formed, the method existed, and the tool ran its lookup. The failure belongs to the task result. Keeping that layer distinct lets a host decide whether to revise the arguments, report an absence, or stop, without treating every negative as a broken protocol. A host that ignores `isError` and presents `Record not found` as an ordinary fact misuses a well-formed result.

Two limits apply to every reply. Identifiers solve association, not trust: a matching id shows which response belongs with which request, and says nothing about whether the tool used the intended data or whether the result is safe to pass on. And the content stays untrusted data. A successful response containing text does not make the text correct. In this fixture the mapping is declared in source, so you can compare directly. A different server's result needs provenance appropriate to where it came from.

## History is part of the protocol

What should the server do with a message that is legal in one state and illegal in another? You decide per state, in writing, before you read the branch that decides it. Each row gives the starting state as (`initialized`, `ready`) and a message. Cover the last three columns and predict the response and the ending state before you read on. Rows marked R come from the recorded run in `chapters.08`. The others are what the reference's branches produce, and you should confirm each by running it, not by trusting this table.

| # | Before | Message | Response | After | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | F, F | `{}` | error `-32600`, id null | F, F | code |
| 2 | F, F | `tools/list`, id 1 | error `-32000` | F, F | R |
| 3 | F, F | `notifications/initialized` | none | F, F | code |
| 4 | F, F | `initialize` | result, version `2025-11-25` | T, F | R |
| 5 | T, F | `tools/list` | error `-32000` | T, F | code |
| 6 | T, F | `notifications/initialized` | none | T, T | R |
| 7 | T, T | `tools/list` | result: one tool, `lookup` | T, T | code, demo |
| 8 | T, T | `tools/call`, arguments a list | error `-32602` | T, T | code |
| 9 | T, T | `tools/call`, key `missing` | result, `isError` true | T, T | R |
| 10 | T, T | method `bad` | error `-32601` | T, T | code |

Read down the table for what a list of isolated JSON examples hides. `tools/list` fails in row 2 and succeeds in row 7, and the only difference is history. Rows 3 and 6 receive the same response, none, with different effects on state: nothing changes in row 3, and readiness begins in row 6. Row 10's `-32601` appears only because the server was ready; the same `bad` method sent in row 2's state would have received `-32000`. An error code reports the branch the server reached, not every defect the message had. Parse errors live elsewhere. In stdio mode the main loop catches a parsing `ValueError` and emits `-32700` with a null id, so the text `{` fails before the handler, while `{}` parses and receives `-32600`. Preserve the raw text when you need to tell those apart.

Two behaviors here were never chosen by anyone. A second `initialize` sent to a ready server leaves `ready` true. A `tools/call` sent without an id is dropped without a response, even when the server is ready. Neither is pinned by the lesson's tests, and this chapter does not claim to know what the specification requires for either. They are what the code does because nothing said otherwise, which is the cost of leaving a handshake rule implicit.

The default demo constructs a server, initializes it, sends the notification, lists tools, prints the response, and exits. The `--stdio` flag opts into reading newline-delimited messages until input ends. Do not infer production transport guarantees from that loop: it reads one line at a time, prints one JSON response per non-notification result, and flushes, with no framing, cancellation, timeout, concurrency, or security feature beyond that.

## Compatibility is not authorized

### Four ledgers for one connection decision

A single word like trusted hides too much, so this chapter keeps four small ledgers and does not let one stand in for another. They are a teaching device, not a standard, and they cost something: four columns for a one-tool server is more bookkeeping than the server deserves. I accept the cost because the ledgers are cheap while the server is small, and the habit is what remains when the server is not.

| Ledger | The question | What fills it | What reopens it |
| --- | --- | --- | --- |
| Protocol | Is the exchange well formed and in order? | The transcript: methods, ids, states, codes | A protocol-version change |
| Capability | Does the code do what the listing says? | Source inspection, disposable fixtures, who maintains it | A new advertised tool, a new release |
| Permission | Does this task allow that capability? | The task brief, the data owner, your policy | A changed task or broader data scope |
| Evidence | Does the returned content support the claim built on it? | Comparison with the declared source | A changed corpus |

In the teaching lookup, the protocol ledger can show a legal initialization and call. The capability ledger can show that the code reads one in-memory mapping and performs no file write. The permission ledger says whether the public fixture is allowed for the classroom task. The evidence ledger compares `505A Dana Hall` with the declared fixture source. None of these records can stand in for another.

Imagine the protocol ledger is perfect and the capability ledger reveals an undeclared write: the connection succeeds and the behavior exceeds the task boundary. Imagine the capability is properly read-only and the returned fixture is stale: permission is satisfied and the evidence claim fails. That is why "passed" must always name which review passed.

Record unknowns explicitly. If you have not inspected network behavior, write uninspected, not none, because the absence of observed harm in a test you did not perform is not evidence that the capability is absent. If a server is closed-source, advertised behavior may be the only evidence available, and the decision should say so. The last column of the table is what turns a verdict into a bounded decision. Trust becomes a decision over identifiable inputs that reopens when one of them changes, not a permanent property of a server's name.

### The host is part of the mechanism

Where does the server's responsibility end? At its reply. The host decides what enters context. The client must decide whether it supports the server-selected version, and the specification's fallback route depends on that decision. Our teaching server implements only the server object, so it cannot demonstrate the client's behavior. A complete interoperability test needs both sides, or an explicit harness that represents the client's obligations.

The host can add real defenses: require approval before consequential tools, validate arguments independently, restrict data access, cap calls, verify results. This chapter does not claim that any particular host implements all of them. It gives you the questions to ask of the host you use and a minimal server to test the answers against. When you record an actual integration, include the host configuration that identifies the command, working directory, environment boundary, and enabled tools, and leave out secrets, since a transcript without configuration leaves the source of the server ambiguous. Do not commit credentials or private paths to make the record complete.

### Laundering: valid transport, borrowed authority

The failure the ledgers exist to stop is rarely a malformed message. A server returns a valid text result, the host inserts it into Claude's context, Claude restates it fluently, and by the last sentence a string a server produced reads as an established fact. The companion book *Conducting AI* calls this laundering: an unverified output acquiring authority as it passes through downstream steps. The word is that book's framing; the mechanism is polish conferring credibility the content never earned. Each hop adds a form of trustworthiness for free. The JSON-RPC envelope gives the text the shape of a protocol-valid reply. The matching id gives it the look of an answer to your question. `isError: false` gives it the look of success. Claude's sentence gives it fluency. None of those checked the content. Polish is not provenance.

The defense in that book is to treat each handoff as a decision and write it down: what is passed, what it is trusted to be, and how that trust was earned. A handoff with no verification is a place where an unverified output can travel onward wearing the authority of every clean step it passed through. For the course lookup:

| Handoff | What passes | Trusted to be | How that trust is earned |
| --- | --- | --- | --- |
| Server to host | The reply carrying `505A Dana Hall` | The fixture's value for key `office`, from this server version | Comparison with the mapping in the source you inspected |
| Host to Claude's context | That text | Data to cite with its role, not an instruction and not a current fact | The recorded host configuration and your instruction about how the text may be used |
| Claude to answer | A sentence using the value | "The course fixture lists the office as 505A Dana Hall" | The sentence keeps the fixture role, and the value traces to the source comparison |

Read the first row for what the host may infer: that this server returned the displayed fixture text for a particular request under the recorded implementation. It may not infer that an external fact is current or universally correct without another source check. The phrasing is narrower because the evidence is narrower. And when the tool returns a missing record, the right continuation is the absence itself, plus a decision about whether to ask another authorized source. In Chapter 1's terms, nothing in the loop that produces Claude's next token stops a fluent guess at an office number. The stop has to be a rule you wrote into the host or the instruction, and a check you run on the answer afterward.

## The gate: write the connection decision before you connect

This is the gate you first wrote in Chapter 1, now guarding a connection and not an experiment. It has two halves: the lifecycle as a state machine you predicted, and the four ledgers for the connection decision. Write both in your learner workspace before you read the reference and before you ask Claude for anything. Name who decided each item. A table and a few plain sentences will do.

*Design.* The task is to answer one question, where the office for key `office` is, using only the declared course fixture. The candidates are the read-only teaching server, which you will execute, and a hypothetical write-capable server advertising `save_report`, which you will never run. Your transition table is part of the design: the one above, with your predictions entered before you looked at the answers. These are your choices; no model produced them.

*Contract for the state machine.* Tool operations are refused until initialize and then the initialized notification have both arrived, in that order. A notification never produces a response. Every response carries the id of the request it answers. A tool-level negative is a result with `isError`. A protocol-level problem is an error with a code. The subset does not claim version negotiation.

*Contract for the connection.* In the permission ledger, name the sources the task may read, the effects it may have (here, none beyond returning text), and where results may go. In the capability ledger, list the claims you will check in source: one mapping, no write, no network. In the evidence ledger, require that every value Claude may cite be compared with the declared source first. Give every entry an evidence type: advertised, source-inspected, executed on a fixture, independently sourced, or uninspected.

*Wrong versions your checks must catch.* Three constructed ones. First, a server that sets `ready` inside the initialize branch and so skips the notification. Applied to a copy of the reference, that change leaves all six of the lesson's tests passing; the case that fails it, `tools/list` after initialize and before the notification, is not among them. Second, a hypothetical `lookup` with a flawless lifecycle that appends to a log file on every call. It passes the protocol ledger and fails the capability ledger. Third, a read-only `lookup` whose fixture value disagrees with the declared source. It passes three ledgers and fails the fourth. If your checks cannot tell these from the right server, the gate is not finished.

*What a failure looks like.* Write one sentence, dated, before you read any transcript: what you would see if your table were wrong. If you write it after reading the output, you have described the output.

*The pass condition.* The companion book on delegation makes one demand of any handoff condition: a person who did not build the pipeline can read it, observe the system, and tell whether it is met. "Looks good" is not a handoff condition. Here, a stranger holding your transcript, the source, and the task brief can mark every line of the four ledgers with an evidence type, finds no empty cell, finds no word like safe or trusted without a named evidence type, and finds a re-review trigger beside the decision. The same book is honest that some conditions need a qualified reviewer. Whether the fixture is public is one of them. Only its owner can settle it, so record who that is.

Claude can sharpen this gate. It is good at inventing the message you forgot to consider. It cannot write the gate for you without defeating its purpose, because the gate is where your decision about the task, the data, and the risk goes on the record.

## Build It: implement the state machine before connection

I ask you to build this by hand for the reason Chapter 1 gave: your own version is the record of what you understood before Claude touched anything, and the instrument you will measure its version against. Work from your table. Create the two state flags and the base message validation. Implement initialize, then the initialized notification, and test both orders. Explain why the early notification returns no response and still leaves the server unready.

Add `tools/list` behind the readiness check, and verify the advertised schema against the call validation you intend to write. Then add the lookup tool and separate four outcomes: malformed arguments, unknown tool, known record, missing record.

Read the [six existing tests](../lessons/08-mcp-from-scratch/code/tests/test_main.py) before the reference, and predict each error code or state. Then add one malformed-argument case and one lifecycle case the suite lacks. The best candidate is the one from the gate: initialize, then `tools/list` without the notification, must still return `-32000`. State what remains outside the subset.

Run the default demo before stdio mode. If you test stdio, feed only declared lines in a controlled process and confirm it terminates when input closes. The client parses standard output as protocol messages, so a stray print there corrupts the channel; the knowledge check asks why. Do not leave an unbounded server process running and call that a completed exercise. Once you can explain your version, compare it with the reference and name a difference in behavior, not in line count or style.

## Use It: conduct Claude Code, then ask it for discrepancies, not a verdict

Now hand Claude the work it is good at. Open Claude Code in your learner workspace and give it the gate, meaning the transition table, the contract, and the test list, and not your implementation. Ask for a server that satisfies the contract and passes your tests. Then run your tests on what it returns, yourself.

Do three things with the result. Note which of your tests failed; a failing test is often a gap in your gate, which Claude could not see because it had only what you wrote. Compare its server with your baseline and name one difference in behavior, such as a boundary it handled that you missed or a rule it settled differently from you. Then ask it for a deliberately wrong server that still passes your tests, and run your tests against it. As a control, make the ready-on-initialize change from the gate to a copy of your own server and run the same tests. If they do not catch it, your list was too weak, and you found out cheaply. Either way, a case your gate missed reopens the gate: revise it, date the revision, and keep the original. Designing first is not freezing the design.

Preserve the actual transcript: your prompt, the plan, the diff, the commands, and the outputs, with the date and displayed model label. If a session failed or did not run, record that rather than substituting a fixture.

The second use is reading. Claude can take a whole transcript, the server source, and the advertised description, and compare them side by side without skipping the tedious message. Ask for leads and withhold the verdict:

```text
Here are three things about one MCP server: a transcript of an
initialize, a tools/list, and two tools/call exchanges; the server's
source file; and the tool description it advertises.
List every place where they disagree, or where one claims more than
another supports. For each, quote the line you relied on.
Do not tell me whether to connect this server, and do not call any
behavior safe.
```

Check every item it returns against the source yourself. Some will be wrong, and an item's absence from the list is not evidence that no such discrepancy exists. Treat the list as places to look. Then the decision is yours: allow, deny, or pending, in your own words.

Build the capability inventory for two candidates: the read-only teaching server, and a hypothetical write-capable one that you label hypothetical and never execute. For each, record advertised tools, inspected behavior, data sources, side effects, and the permission it would need. Source inspection has its own trap. The reference imports only `argparse`, `json`, and `sys`, which hints at network and process access but proves nothing about files, because `open` is a builtin and needs no import. What establishes that the lookup writes nothing is the call branch itself: the only data it consults is a literal mapping. For an external candidate, use only source and documentation you have actually inspected. If inspection is incomplete, record the decision as pending or deny. Do not invent a server's behavior from its tool description. This exercise demonstrates source inspection for its own small server and certifies no external package.

Connection here is a classroom decision within a bounded task, not a permanent endorsement. Record the version and provenance that give the decision an identifiable object, since a later version, changed configuration, or broader data scope requires renewed review.

Anthropic's [MCP builder materials](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) and [evaluation guide](https://github.com/anthropics/skills/blob/main/skills/mcp-builder/reference/evaluation.md) are relevant upstream reading for designing answerable, verifiable evaluations. Do not install an external skill merely because the links exist.

## Ship It: an MCP evaluation packet

The [artifact brief](../lessons/08-mcp-from-scratch/outputs/artifact-brief.md) asks for an initialization transcript, a capability inventory, and a trust decision. The optional Progress Reel can explain Weeks 3–8 artifacts but is not a separate requirement or point category in this book.

Arrange the transcript chronologically. Preserve requests, notifications, responses, identifiers, state transitions, and errors, including one successful and one failing call with their matching ids, and explain why the missing record is a tool error and not a protocol error. Label the office value a course fixture. Redact credentials; this fixture uses none. Mark constructed messages separately from any actual host integration. For each capability, record what the server says, what source inspection shows, which disposable tests ran, and what remains unknown. Then state allow, deny, or pending for the bounded task, with a reason. A valid tool listing belongs in the evidence. It is not the decision.

Include one handoff analysis, the three-row table from the laundering section filled in for your own run: server output, host inference, the evidence supporting that inference, and the next component's allowed use. If a fixture value is deliberately wrong, show the source comparison that catches it before generation, and do not call the protocol exchange failed when the factual check is what rejects the value.

**The sign-off.** End the packet with a statement you could put your name to, in the same four-part shape as the sampling report's. Claude can draft its words in seconds and the draft will be fluent, so write it from your record. This is the template, not a signature:

```text
Sign-off — MCP evaluation packet
Checked:      which ledger lines, and the evidence type for each
              (advertised / source-inspected / executed / independently sourced)
How:          by hand / by a test I wrote before reading the reference /
              by source comparison / with Claude's help (say which parts)
Not checked:  network behavior; other versions of the server; client-side
              version handling; whether the fixture is true in the world;
              anything outside the recorded transcript
Not claiming: that the server is secure, conformant to MCP, or endorsed
              beyond this task and this version
Decision:     allow / deny / pending, for task ____, server version ____
Re-review if: ____ (a new tool, a version change, a changed corpus or task)
Signed or withheld: ____________  (name, date)
```

The decision and the sign-off are different statements. The decision is about the server. The sign-off is about your evidence for the decision, so you can sign a deny, and you can withhold your signature from an allow that your evidence does not support. The "Not checked" line does the work. It is the line an AI-written sign-off leaves empty, because the system that wrote it has no record of what you did not do. Choose verbs the evidence earns: recorded for a transcript, inspected for source you read, executed for a fixture you ran, compared for a source check. Secure, trusted, and verified need a criterion this exercise never supplies.

## The driver's seat

This is how the chapter's work divided, task by task, as in Chapter 1. Test your own record against it.

| Task | Claude should | You should | Why it stays with you |
| --- | --- | --- | --- |
| Reading a transcript against the source and the description | Read every message and list each disagreement, quoting the line it relied on | Verify each item against the source and decide which matter for this task | The list is leads; a missing item proves nothing |
| Proposing out-of-order and malformed messages | Generate many, fast, and run them | Decide the expected response for each | The expected response is the contract, and the code cannot supply it |
| Implementing the state machine from your gate | Implement it and write tests | Build your own baseline first; run your tests, including against a wrong server | You cannot audit a lifecycle you have not built |
| Quoting and summarizing the lifecycle page | Quote and summarize | Check the clauses; keep the version claim narrow | A recollection of a protocol is not the protocol |
| Classifying the data as public and scoping the task | Draft the inventory | Decide what the data is and what the task may touch | Classification and scope are facts about your world, and a transcript does not contain them |
| Allow, deny, or pending | Draft the packet | Decide, set the re-review trigger, sign or withhold | The decision carries your name, and the cost of a wrong one lands on whoever owns the data |

The common thread is that the trust decision rests on facts about the world around the transcript: who owns the data, what this task needs, what a wrong answer costs, who maintains the server. The transcript contains none of them. The claim is not that Claude is incapable of reasoning about such facts. In this task they are not among its inputs unless you supply them, and the accountability for a wrong decision lands on a person.

Record in the packet one task you delegated and one judgment you retained, each pointing at a transcript line or a diff. A discrepancy Claude listed that you accepted, and one you rejected, with the source line that settled each, would do. If you cannot point to either, the split happened in your head.

## Verify and reflect

Read the transcript in both directions. First as the server: given this state and message, which branch runs, what response does it produce, and what state changes? Then as a reviewer: given this response, which request and prior transition must be present before the interpretation is justified? The two passes catch different omissions.

A tool list in isolation omits the initialize request, the notification, the process configuration, and the source version. A tool result in isolation keeps the content and loses the arguments and identifier that give it meaning. Attach every error code you report to the raw constructed message and server state it came from. "MCP failed" erases the mechanism this chapter teaches.

Then compare the transcript with source. Does the advertised tool name match the dispatch branch? Does the schema match the argument validation? Does `isError` appear for the recorded missing key? This correspondence review is stronger than either the listing or code inspection alone, and it is still evidence about the tested implementation and version.

Add a final row for what did not happen. The default demo did not connect to Claude, expose a network port, write a file, authenticate a user, or validate a production deployment. A narrow server can be complete as a teaching artifact and incomplete as a product.

Run the demo and tests, then your new cases. Compare outputs with the [saved research results](../research/worked-examples.json), and explain each code or `isError` value through the branch that produced it. Do not call the subset conformant because its happy path resembles the specification. Inspect every trust claim for its evidence type, whether advertised description, code inspection, executed fixture, or independent provenance, and keep the types separate.

The most useful reflection is local. Which distinction did you originally collapse: compatible and authorized, valid transport and true content, a description and the behavior behind it? Name the message, the table row, or the ledger line that separated them again. Then ask what would change your decision: broader file access, a new tool, different data, a version update, or missing maintainer evidence. A decision with a re-review trigger is more responsible than a timeless label of trusted.

## Assessments — ungraded practice

These Assessments carry no points. Use the paired lesson's [knowledge check](../lessons/08-mcp-from-scratch/quiz.json) and preserve predictions before viewing explanations.

### Warm-up

1. **Two flags — introductory; objective: trace lifecycle.** Predict `initialized` and `ready` after initialize, after an early notification, and after the legal sequence, and write the predictions down first. Run each on a fresh server and name where your prediction was wrong, or say it was not.
2. **Match the id — introductory; objective: associate messages.** Send two constructed requests with distinct ids and show which response belongs to each. Write, in one sentence you could defend, what id matching does not prove.
3. **Two kinds of error — introductory; objective: distinguish layers.** Compare an unknown method response with a valid lookup of a missing key. Identify the JSON-RPC error and the tool `isError`, and say which one a host might reasonably answer by retrying with changed arguments.

### Application

4. **Too early — intermediate; objective: test state order.** Send `tools/list` before readiness, preserve the code, then complete initialization and retry. Explain the changed state rather than calling the first message malformed. Then write the test that stops the ready-on-initialize change, and show it failing against that change.
5. **Schema boundary — intermediate; objective: validate arguments.** Write the code you expect for missing, extra, and non-string `key` arguments, then test them. Map each result to the implemented check.
6. **Fixed version, precise claim — intermediate; objective: evaluate compatibility.** Compare the initialize branch with the versioned lifecycle specification. State exactly which negotiation behaviors are absent and why fallback alone is not the defect. If Claude helped, record which of its statements you checked against the page.
7. **Read versus write candidate — intermediate; objective: separate permission.** Compare two declared tools under one bounded task. Explain why equally valid protocol messages can deserve different authorization, and name who would make that decision in a real deployment.

### Synthesis

8. **Annotated transcript — advanced; objective: integrate protocol evidence.** Produce a complete legal sequence plus one rejected transition. Annotate state, ids, results, and allowed inferences. Ask Claude to list the discrepancies in your annotation, and keep a note of which you accepted and which you rejected, with the line of source that settled each.
9. **Trust decision — advanced; objective: evaluate provenance.** Build a capability inventory from advertised text, inspected source, and fixtures. Give a bounded allow, deny, or pending decision with a re-review trigger, and finish with the sign-off, without inventing missing evidence. Withholding the signature is an acceptable result.

### Challenge

10. **Unsupported value handoff — stretch; objective: prevent laundering.** Make a well-formed lookup return a deliberately incorrect fixture value. Add the independent source check and show where the value must stop, and which of your four ledgers caught it.
11. **Compatibility test, not certification — stretch; objective: design evaluation.** Propose tests for one additional lifecycle feature, such as what a second initialize or a notification-shaped `tools/call` should do. Read what the specification says first. State what success would establish and why it would not certify security or full conformance.

## What you can now trace

You can follow a minimal MCP exchange as a state machine: initialize changes one state, the initialized notification changes another, and tool operations become available only afterward. You can match responses to requests, keep notifications distinct, and read a transition table for what history does to the same message.

You can inspect a tool declaration and its argument checks without treating its description as proof, and say which words in it, here "public", the server had no standing to assert. You can distinguish protocol errors from tool-level negative results, and state the version limitation precisely: one supported version returned without evaluating client parameters, a fallback that a client may legally receive, and no demonstration of full negotiation or conformance.

Most importantly, you can separate connection from trust. Protocol compatibility enables communication. Permission, provenance, source support, and outcome review determine what the workflow should do with that communication.

And you can say what the three jobs looked like here. You conducted: you wrote the lifecycle table, the four-ledger contract, and the wrong servers your checks had to catch before Claude saw a line of code. You checked: you recorded what a wrong server would show before you read a transcript, kept each ledger's evidence type separate, and refused to let a valid exchange stand in for a true value. You drove: you handed Claude the reading of the transcript and the first implementation, kept the question of whether to connect, and signed or withheld.

## Connecting a tool is not training a model

An MCP server can add information and actions to a host without changing model parameters. That distinction is the bridge to Chapter 9. We will implement a tiny logistic predictor whose weight and bias genuinely update under a loss function, then compare that mechanism with changes to prompts, context, tools, and settings. The gate question comes with us: before you change anything, state what should change and what would show that it did.

## Anthropics

Compare your server with Anthropic's [MCP builder materials](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) and [evaluation guide](https://github.com/anthropics/skills/blob/main/skills/mcp-builder/reference/evaluation.md), checked through the course research on 2026-09-06. Identify one answerable task and independently verifiable result for the read-only fixture. Keep the versioned specification as protocol authority and do not treat upstream examples as permission to connect an unreviewed server.

## Conducting AI

The companion's explicit-handoff chapter adds one test the body has not applied to your own checks: an audit reduces error only to the degree that the checker fails differently from the thing it checks. See [Explicit handoffs](../docs/conducting-ai.md#explicit-handoffs). Apply it to the incorrect-fixture exercise. Asking Claude whether `505A Dana Hall` looks right, with no source in hand, judges plausibility, and plausibility is the ground the original answer stood on. Comparing the value with the mapping in the source you inspected fails in an unrelated way: it errors loudly and cannot be persuaded. For each check in your packet, write one sentence on how it can fail and one on how the thing it checks can fail. If the two sentences match, you have a repeat, not a check.

Claude can organize and inspect the transcript and propose which source to compare against. The human should decide whether the server, data, and action scope are appropriate for the task. A successful exchange establishes transport behavior. It does not make the returned value true or authorize the next action.
