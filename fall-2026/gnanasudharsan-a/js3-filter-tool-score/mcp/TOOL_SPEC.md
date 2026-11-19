# Tool server spec — written before the server (2026-11-19)
Server name: jobwatch-score. Transport: stdio, JSON-RPC 2.0, one JSON object per line (no Content-Length framing). Written from scratch, no MCP SDK.

## Methods
| method | behavior |
|---|---|
| initialize | returns protocolVersion (echoes the client's if it is "2024-11-05" or "2025-03-26" or "2025-06-18", else "2025-06-18"), capabilities {"tools": {}}, serverInfo {name, version} |
| notifications/initialized | no response (it is a notification) |
| tools/list | exactly one tool: score_posting |
| tools/call | runs score_posting; tool failures return a result with isError: true, never a JSON-RPC error |
| anything else | JSON-RPC error -32601 (method not found); malformed JSON -32700; missing/invalid params -32602 |

## The tool: score_posting
Input: {"board": "greenhouse:anthropic" | "ashby:notion" | "lever:spotify", "id": string of digits/letters/hyphens only}.
Output (text content, JSON): decision, score, rejected_by, matched, components from runs/20261119T162945Z/filter_v1_C1_C4.jsonl; and, if the posting is on the shortlist, my five claim labels from shortlist/claim_labels.csv.
Annotations declared: readOnlyHint true, openWorldHint false, destructiveHint false, idempotentHint true.

## Guarantees (what the tests check)
- Reads only those two files. Never reads a path built from client input (the id is looked up, never joined into a path).
- No network access. No subprocesses.
- Writes only one file: its transcript in transcripts/ (one line per message, in both directions, with a UTC timestamp and the direction).
- Unknown board, unknown id, or bad id characters: isError true with a message, no crash, no file read outside the two.
