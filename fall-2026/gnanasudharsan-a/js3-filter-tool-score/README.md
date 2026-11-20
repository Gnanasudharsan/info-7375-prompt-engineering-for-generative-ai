# Job-Search Agent 3 — The Filter, the Tool, and the Score
INFO 7375, Gnanasudharsan Ashokumar. Persona: Ananya Rao (fictional). Built on my JS2 agent (copied at 9ef84715).

**Read in this order:** FILTER.md → audit/AUDIT.md → shortlist/SHORTLIST.md → mcp/TOOL_SPEC.md → mcp/EVALUATION.md → SCORE.md → FRICTIONAL.md → SOURCES.md.

## Where each deliverable is
| deliverable | file |
|---|---|
| Filter as a versioned document (rules + reasons, evidence rules, expected sources, wrong versions, changelog) | FILTER.md |
| Code and tests | jobwatch/filter.py, scripts/, tests/ (201 tests) |
| Reject audit with my hand verdicts, false friends, rule changes | audit/AUDIT.md, audit/hand_verdicts_v1.csv, _v2.csv, FILTER.md changelog 1.1 |
| Source-grounded shortlist, claim labels, relevance ≠ entailment, abstention + counterexample | shortlist/SHORTLIST.md, shortlist/claim_labels.csv |
| Tool server, transcripts, both evaluations | mcp/server.py, mcp/TOOL_SPEC.md, transcripts/, mcp/EVALUATION.md |
| One-change report, origin of every number, persistence | SCORE.md, heldout/ |
| Sign-off and driver's seat | below |

## Toolchain
macOS 27.2.1, Python 3.15.2, pytest 8.4.2, git 2.54.0, Claude Code 2.1.329 (MCP client and Claude judge), Node 26.8.2 (only for the filesystem-server probe).

## How to run
```bash
git clone https://github.com/Gnanasudharsan/info-7375-prompt-engineering-for-generative-ai.git
cd info-7375-prompt-engineering-for-generative-ai/fall-2026/gnanasudharsan-a/js3-filter-tool-score
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python -m pytest -q                                            # 201 passed, offline
python scripts/audit_report.py > /dev/null && python scripts/measure_changes.py | head -5     # audit + v1.1 measurements, offline
PYTHONPATH=. python scripts/shortlist_report.py > /dev/null                                # SHORTLIST.md from my labels, offline
python scripts/score_experiments_offline.py && python scripts/score_experiments_compare.py # held-out results, offline
```
Needs network or accounts (already run; outputs committed): the collection (`python -m jobwatch.loop --boards boards.json`, run once 2026-11-19),
the Claude judge experiments (`scripts/score_experiments_claude.py`, needs `claude` login), the MCP client session (regenerate mcp/claude_mcp_config.json
with your absolute paths, then `claude -p … --mcp-config mcp/claude_mcp_config.json --strict-mcp-config`), and the filesystem probe (`scripts/probe_filesystem_server.py`, needs npx).

## What ran
One live collection (runs/20261119T162945Z: anthropic 638, notion 169, spotify 92; the deliberate 404 board failed as designed). Everything else ran offline on
that snapshot, except the Claude judge calls (evidence/score_claude/), two Claude Code MCP sessions, and the filesystem-server probe.
codex_unrequested/ holds files Codex created without being asked; they are not used (see FRICTIONAL.md).

## Sign-off
**Checked**
- 201 tests pass (filter rules, wrong versions W1–W5, v1.1 switches, MCP server).
- Filter v1.0 on 60 random rejects I labeled blind: 1 I would call relevant (0 after my recorded correction); exact 95% interval 0%–8.9% among random rejects only.
- Each v1.1 change measured alone against v1.0 on the corpus and my labels; C1 and C4 kept, C2 and C3 rejected, C5 recorded.
- My MCP server with Claude Code as a real client, both directions recorded; the server itself rejected a path-traversal id the client passed through.
- The filesystem server denied reads outside its folder three ways (absolute path, "..", symlink).
- On 28 held-out postings, the prompt change moved verdicts no more than an identical control run.

**How:** by hand (all audit and held-out labels, predictions, every keep/reject decision on a rule, the trust decisions), with Claude chat (plans, test and
script drafts, document drafts from my data), Claude Code (filter.py, run_filter.py, v1.1 switches, mcp/server.py, each action approved), and Codex
(44 claim-label suggestions; the second-pass reviewer; unrequested files quarantined). The 44 Codex-covered claim labels are not claimed as a one-by-one re-review.

**Not checked**
- Recall: my held-out set has 0 relevant postings, so missed good jobs are not measured; threshold changes could not be measured on it (no close calls left).
- My server's "no network" guarantee is checked by reading the code, not in a sandbox; the filesystem server's write tools were never called.
- The Claude judge gives no verdict on Lever/Ashby postings (5 of 28 held-out); C2 as a sentence-level rule and a C5 fix are untested.
- Any collection other than the 2026-11-19 snapshot.

**Not claiming:** an error rate for all postings; that the filter finds every relevant job; that anything was trained; that any employer would sponsor this
fictional candidate; that a score is a probability of being hired.

**Signed:** (I sign after reading and correcting every line above.)

## Driver's seat
| Claude should | I should | why the judgment stays mine |
|---|---|---|
| collect postings, apply FILTER.md, propose claim labels with quoted spans, report what it could not tell | decide which rules exist, label the audit and held-out sets, accept or reject each rule change | the filter encodes what is worth Ananya's time; only her persona's owner can say that |
| say "I cannot tell" when the text does not state level, location or the work | decide whether to read a posting anyway (#26: the rule abstained, I judged it relevant) | the rule only sees text; I see the whole posting and her situation |
| run the judge and show its disagreements | read the disagreements and decide | identical judge runs disagreed (control), so its verdict is evidence, not a decision |
| | sign off | the cost of a wrong "worth your time" falls on the person applying, not on the agent |
