# Sign-off — Job-Search Agent 3

Draft for the student to review and sign.

| Item | Evidence |
|---|---|
| Checked | `test_lookup_protocol_and_read_only_boundary` verifies the MCP lifecycle, archive lookup, missing record behavior and argument boundary. The existing filter tests cover known wrong versions and switch behavior. |
| How | Codex ran the offline Python suite, recomputed each switch from archived bodies, compared replayed rows with the saved baseline and variants, and captured the actual Claude Code tool exchange. The student supplied the audit verdicts and the first 31 shortlist reviews. Codex's 44 classifications are attributed separately. |
| Not checked | Generalization to a fresh collection, behavior with other MCP clients and compatibility revisions, and whether a particular employer would in fact sponsor or consider this fictional candidate. |
| Not claiming | The score measures rule matches. It gives no probability of selection, validates no training effect, and carries no authority to decide what the student should apply for. |
| Signed or withheld | Student to complete (name, date, decision). |

## Driver's seat

| Claude should | Human should | Why |
|---|---|---|
| Retrieve the archived score and identify relevant passages. | Inspect those passages in context and confirm or change the evidence labels. | A score can reach the threshold even when the posting leaves eligibility unclear. |
| Compute comparisons and surface counterexamples. | Label the held-out postings independently and decide which changes justify the cost of missed opportunities. | The tradeoff depends on what counts as worthwhile for this search. |
| Explain a tool's declared capabilities and report observed behavior. | Decide which server and permissions to trust, and sign or withhold the assignment. | A successful tool call shows what happened in one configuration. Responsibility for permission and submission stays with the student. |
