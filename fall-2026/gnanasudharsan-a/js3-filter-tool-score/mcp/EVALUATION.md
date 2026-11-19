# Evaluating the tool servers like someone else's (Chapter 8)

## A. My server: jobwatch-score (mcp/server.py)
Evidence: mcp/TOOL_SPEC.md (written before the server), tests/test_mcp_server.py (9 tests), two real Claude Code 2.1 sessions
(transcripts/claude_code_session_normal_2026-11-19T2144Z.jsonl, ..._hostile_...), probes (evidence/mcp_own_server_probes_*.txt), and a read of the code.

### What it declares vs. what it does
| it declares | what I found | how I checked |
|---|---|---|
| one tool, score_posting, read-only (`readOnlyHint: true`) | It only **reads** two fixed files, but **every session writes a transcript file** in my folder (open(..., "x")). So "read-only" holds for my data, not for the disk. | grep of open()/write in mcp/server.py; tests/test_mcp_server.py::test_writes_only_its_transcript |
| no outside world (`openWorldHint: false`) | Imports are stdlib only (csv, io, json, re, sys, datetime, pathlib). No network, subprocess or exec code. **Static check only**: I did not run it in a network sandbox. | grep of imports and of socket/urllib/http/subprocess/exec/eval |
| `inputSchema.id` pattern `^[A-Za-z0-9-]{1,64}$` | The **client did not enforce it**: Claude Code sent `../../etc/passwd` unchanged. The **server's own check** rejected it (isError, no file read). | hostile transcript: the tools/call "in" line carries the raw id; the "out" line is the isError |
| `additionalProperties: false` | **Not enforced**: a call with an extra key ("extra") was answered normally. | probe 1 |
| protocol: answers the client's version if supported | Claude Code asked for 2025-11-25; the server answered 2025-06-18 (its newest) and the client accepted the downgrade. Before initialize, the client sent `server/discover`; the server answered -32601 and the client fell back. | normal transcript, first four lines |
| `idempotentHint: true` | Same call, same answer while the two files are unchanged; files are re-read on every call, so answers follow the files. | Claude Code build note #10; two identical calls in tests |
| claims "if it is on the shortlist" | True: a rejected posting returns no claims. | probe 2 |

### What a compatible client is NOT entitled to
- To treat the annotations as guarantees. They are the server's own claims; I showed one is loose (readOnly vs. the transcript write).
- To rely on the server enforcing its declared schema: it enforces the id and board, not "no extra keys".
- Any file, path or posting outside the fixed run; my notes, the script's proposals, or Codex's columns (never returned).
- Freshness: the data is the 2026-11-19 snapshot, not live boards.
- To treat my claim labels as facts about a job: they are my judgments of the posting text (SHORTLIST.md).

### My trust decision
I trust jobwatch-score **for local, read-only use by Claude Code on my own machine, pinned to the commit that contains this file**, because the tests, the
transcripts and the code agree on what it reads and that it writes only its transcript. I do **not** trust it beyond that: the network guarantee is
checked statically only, and two declarations (readOnlyHint, additionalProperties) are looser than the behavior. I would not expose it over a network
or to another user without a runtime sandbox and a fix for both.
