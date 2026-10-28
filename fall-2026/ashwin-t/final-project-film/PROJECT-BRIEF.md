# Project brief: TraceCase (working title)

**Ashwin Thankachan** · INFO 7375 · 2026-10-13 · replaces my ProvenDocs brief of 2026-10-11 (why: FRICTIONAL.md)
**Target role:** backend software engineer (new grad).
**Planned stack:** Spring Boot demo service with PostgreSQL and Redis; a Python agent (FastAPI, Pydantic, Claude
API); OpenTelemetry traces viewed in Jaeger; Docker Compose; pytest and JUnit; GitHub Actions; a small approval page.

**1. What is it?** An agent that investigates failures in a small Spring Boot service using its logs, traces and
deploy history, and proposes one fix that a person must approve before it runs. When it's done, it will be one
public GitHub repo that starts with one Docker Compose command. The repo will hold:
- the demo service: an API, a worker, PostgreSQL, and Redis as a cache and queue, with synthetic data
- the agent
- an approval page
- a library of failures I can trigger
- an evaluation report

**2. Why would anyone care?** My CloudPulse team project answered "is the service healthy?" When the answer is no,
an engineer still digs through logs and traces by hand. TraceCase will do the digging, show its evidence, and leave
the decision to a person.

Alternatives I checked (read 2026-10-13):
- **HolmesGPT** is an open-source incident agent, read-only by default; its optional remediation toolset asks
  before every change.
- **Microsoft AIOpsLab** is a research framework for evaluating such agents, and it runs on Kubernetes.
- **By hand:** dashboards, logs and recent deploys.

TraceCase will run on a laptop with no Kubernetes, ship its own service to break, make every claim cite a real log
line or trace span, and void an approval if the fix or its evidence changes. I'm not claiming the others can't do
these things.

**3. Who opens it, and what do they do in the first 60 seconds?** A backend hiring manager. They start the demo,
break the service with one command, watch the agent investigate step by step, and approve or reject its fix.

**4. What does it prove?**
- **Loop with a budget:** observe, call one allowed tool, record evidence, update the hypothesis. It stops on a
  supported cause, on thin evidence, or at a step, time or cost limit, never on the model's say-so.
- **Prompt contract:** each step must return a fixed, schema-checked format.
- **Permissions in code:** allow-listed tools only, and fixes chosen from a few predefined actions, never a shell.
- **Grounding:** a validator rejects any claim citing a log line or span that doesn't exist.
- **Human gate:** the approval records action, target, parameters and evidence version, and it stops counting if any
  of them change.
- **Evaluation:** about 30 failure scenarios, 10 held out before tuning, compared against a "summarize the logs"
  baseline. It will measure correct diagnoses, honest "I don't know yet" answers, unsupported claims, blocked
  actions, and cost.

**5. In, out, first.**
- **In:** one demo service and failures I design (stale Redis cache, backed-up queue, bad config deploy, slow query).
- **Limitation:** it will only be tested on those failures, so it proves nothing about real production systems.
- **Out:** it will never run arbitrary commands or touch anything outside the demo. Kubernetes is a stretch goal;
  Kafka is out.
- **First piece:** the demo service with one failure I can trigger and a trace that shows it. A saved trace and a
  dated log will show it ran.

**6. What could sink it?** Approving one thing and running another. I'll trigger this on purpose: approve fix A,
swap in fix B, and show that execution is refused until a person reviews it again. A second risk is an agent that
sounds sure without evidence, and the evaluation will check that it says "I don't know yet" when it should.

**7. Why this project?** Mostly learning. Across 3,254 entry-level postings my job pipeline collected (Oct 8–12),
agents, observability and evaluation keep coming up, and my resume shows none of them. It also builds on CloudPulse
rather than copying it.
- **New to me:** OpenTelemetry tracing, agent loops with budgets, code-enforced permissions, approval invalidation,
  Redis as a cache and queue, held-out agent evaluation.
- **Already have:**
  - Spring Boot health monitoring with JUnit/MockMvc tests (my lifecycle, threshold and incident work in the
    CloudPulse team repo).
  - Python/FastAPI services calling an LLM, with pytest tests for mocked LLM failures (MyEdMaster internship; the
    code is private, so the evidence is my account).
  - Docker and CI/CD (LTIMindtree).

**Exists today:** this brief, the beat sheet and the pitch film. No TraceCase code, traces or results.

**Will exist:**
- the demo service, its tracing, and the failure library
- the agent loop, tool dispatcher, permission policy, evidence validator, and approval page with invalidation
- the recorded stale-approval failure
- the held-out evaluation with baseline and failure analysis
