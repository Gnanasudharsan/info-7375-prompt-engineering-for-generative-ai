# Fact check — TraceCase pitch film

Status: agent-checked by Claude Code on 2026-10-13 against the sources below; Ashwin Thankachan to sign off before submission.

Rule for this film: nothing of TraceCase exists yet. Every product sentence is future tense ("will"),
and every body picture of the product carries an on-screen "constructed" tag.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA | A dashboard tells you something is wrong but not why | EXEMPT | Description of the problem the project addresses; no statistic claimed | None |
| 2 | B00 B01 | What TraceCase will do and what the finished repo will contain | EXEMPT | Proposal in future tense; picture tagged "constructed"; matches PROJECT-BRIEF.md §1 | None |
| 3 | B00 | "it isn't built yet" | PASS | PROJECT-BRIEF.md "Exists today": brief, beat sheet, film only; no TraceCase code anywhere (2026-10-13) | None |
| 4 | B02 | CloudPulse was a team project that monitored whether services were healthy | PASS | Team repo github.com/KathaPatel29/csye6300-summer26-group3-final-project (CSYE 6300, Jun–Aug 2026, four-person team); Ashwin's health-evaluation, lifecycle and incident work per his experience record | Said as "team project" |
| 5 | B03 | HolmesGPT is an open-source agent that investigates incidents | PASS | github.com/HolmesGPT/holmesgpt README (read 2026-10-13): "Open-source AI agent for investigating production incidents and finding root causes"; Apache-2.0; CNCF Sandbox | None |
| 6 | B03 | HolmesGPT asks a person before any change | PASS | README: "By design, HolmesGPT has read-only access"; its optional Kubernetes remediation toolset has "every mutating action gated behind human approval" (holmesgpt.dev, read 2026-10-13) | Not claimed as a TraceCase difference |
| 7 | B03 | Microsoft's AIOpsLab evaluates agents like this, on Kubernetes | PASS | github.com/microsoft/AIOpsLab (read 2026-10-13): "A holistic framework to enable the design, development, and evaluation of autonomous AIOps agents"; runs on a kind or other Kubernetes cluster; MIT | None |
| 8 | B04 | TraceCase will run on a laptop without Kubernetes, ship its own breakable service, and require citations | EXEMPT | Proposal (future tense), scoped to TraceCase itself; no claim that the alternatives lack these | None |
| 9 | B05–B13 | Planned design, evaluation plan, first piece, risks and the planned controlled failure | EXEMPT | Proposal in future tense; matches PROJECT-BRIEF.md §3–§6; pictures tagged "constructed" | None |
| 10 | B09 | About thirty scenarios, ten held out; "I have no numbers yet" | PASS | Plan stated as future; nothing measured; hero shows "? / 10", not a result | None |
| 11 | B10 | OpenTelemetry can trace a Spring web service and its Redis client | PASS | opentelemetry-java-instrumentation supported-libraries list: Spring Web MVC 3.1+, Lettuce 4.0+, Jedis 2.0+ (read 2026-10-13) | Narration says "traces will tie it together", no version claim |
| 12 | B14 | The jobs I apply for ask for agents, observability and evaluation; my resume doesn't show them | PASS | Ashwin's own count over 3,254 entry-level postings his job pipeline fetched 2026-10-08 to 10-12: agents/agentic 12% of SWE and 52% of AI/ML postings; observability 13% / 18%; evaluation 11% of AI/ML. His master resume lists none of these (checked 2026-10-13). Private data not shown in the film | Said as "jobs I apply for", not "the market" |
| 13 | B14 | Built Spring Boot work in CloudPulse; language-model services at the MyEdMaster internship | PASS | Same team repo as row 4; MyEdMaster internship Jan–Apr 2026: FastAPI backend calling an LLM, pytest with mocked LLM failures (code private; evidence is his account) | No code shown |
| 14 | B15 | "No TraceCase code exists yet" | PASS | Same as row 3 | None |
| 15 | BOUT | Title and my name | EXEMPT | Metadata | None |
