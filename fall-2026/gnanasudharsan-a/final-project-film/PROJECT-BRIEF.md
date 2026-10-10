# PROJECT-BRIEF — DecisionTrace (working title)
Gnanasudharsan Ashokumar · INFO 7375 · Fall 2026 · Target role: AI Engineer

## 1. What is it?
DecisionTrace will answer "why did we decide X, and where does that decision stand now?" over a team's meeting notes, tickets and emails, and will check every claim it makes against the source it cites.
When done, it will be a public GitHub repository: a Python command-line tool, a synthetic document set for a fictional company, a hand-checked test set, an evaluation harness, and an evaluation report with a written failure analysis.

## 2. Why would anyone care?
The hard question is not only what was decided, but whether it still holds and is finished.
On 2026-10-09 I tested two real alternatives (screenshots captured 2026-10-10) on the same six synthetic documents and four questions:
- NotebookLM answered the facts correctly and refused to invent a budget, but its auto-summary described the migration with no sign it was still in progress ("…successfully deploy the new NoSQL infrastructure") when the ticket shows it In Progress, and its answer to "which database" said "uses DynamoDB" without saying the switch was unfinished.
- ChatGPT got the status right, but tied it to the date of an unrelated document, and nothing flagged that.
In this test, neither tool flagged the overstated status or the wrong date, and neither showed any measure of how often it is right. DecisionTrace will do what neither did: it will report a decision's status (decided, in progress, superseded), mark any claim whose cited passage is missing or judged not to support it, and publish its score on a hand-checked test set.

## 3. Who opens it, and what do they do?
A hiring manager or engineer. In the first sixty seconds they will read the README, run one command that asks a question, see an answer with citations and a pass/fail verification line for each claim, and open the evaluation report showing scores and failure cases.

## 4. What does it prove about me?
- Prompt contracts: the model will be required to return JSON matching a schema, with a citation for every claim; responses that break the schema will fail.
- Verification: code will check that each cited passage appears word for word in the named document; whether it supports the claim will be judged by a second model call, and I will spot-check those judgments against the test set.
- Agent loop: retrieve → answer → verify → retry once with the failing claims flagged, or answer "not supported by the sources."
- Evaluation and source grounding: a hand-checked test set and metrics for citation support, status accuracy, and correct refusal on unanswerable questions.
Evidence will be the test set, the eval report and the failure analysis in the repo. A reviewer could fairly conclude that I can build and measure a grounded LLM tool. They could not conclude that it works on real company data, because it will not be tested on any.

## 5. In, out, first
- Out: no real company data and no live Slack, Jira or email connectors.
- In: synthetic documents, the command-line tool, the verifier, the eval harness and the report.
- First: answer one question over the six existing synthetic documents, with citations. Someone will know it ran because a test will pass confirming every cited document exists and every quoted passage appears in it.

## 6. What could sink it?
The six existing synthetic documents were generated with Claude Code, and the larger set will be too. If Claude also writes the questions, the evaluation mostly confirms itself and will look better than it should. I will write the tricky test cases myself (reversed decisions, unfinished work, contradictions, unanswerable questions) and state this limitation in the report.

## 7. Why this project?
Mostly new learning, built on something I already do.
- New to me: building an evaluation harness with a gold test set and metrics, automated citation checking, prompt contracts with tests, and an agent verify-and-retry loop.
- Already have: RAG pipelines and LLM backends in Python, built during a co-op at Intelligent DataWorks. That code belongs to the company and cannot be shown, so this repository will be the first public evidence of that skill.

Stack: Python, Claude (Anthropic API).

## Exists today
- Alternatives test, 2026-10-09/10: six synthetic Northwind Logistics documents, four questions, an answer key, graded notes and nine screenshots (evidence/alternatives-test/)
- Brutalist toolkit installed; its own smoke test fails on a fixture-name bug, and a renamed copy rendered locally (logged in FRICTIONAL.md)
- This brief and the submission folder scaffold

## Will exist
- The DecisionTrace command-line tool, verifier and retry loop
- A larger synthetic document set and a hand-written test set
- The evaluation harness, evaluation report and failure analysis
