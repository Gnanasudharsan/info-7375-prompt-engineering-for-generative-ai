# JS3 tool server and evaluations

## JS3 archived-score lookup

`jobwatch/mcp_score.py` implements the 2025-11-25 stdio exchange in Python's standard library. It declares one tool, `lookup_score`, taking a board ID and a posting ID. It loads the archived v1.1 decisions and returns the exact matching row. Unknown keys return a tool error, and unknown tool names or extra arguments are rejected. The lookup accepts no file paths, network destinations, or actions.

Claude Code 2.1.328 first probed the newer discovery method. It then used the initialization handshake, listed tools, and called the lookup for Anthropic posting `5198255008`. It received a `keep` and a score of 5. The [bidirectional MCP wire capture](evidence/mcp_claude_wire_2026-11-19.jsonl) records the exchange. The [Claude message capture](evidence/mcp_claude_messages_2026-11-19.json) contains the actual tool use, tool result, and final response from this dedicated public-data demo.

**Codex assessment.** This tool is suitable for reading the checked-in score snapshot inside the project. Its schema and annotations tell clients what to expect, while argument validation and the fixed in-memory lookup enforce the observed boundary. A compatible client has no automatic right to other files, fresh job data, or a hiring decision. The lookup does not validate whether the human evidence labels are complete.

## Model Context Protocol Filesystem Server

Reviewed the published `@modelcontextprotocol/server-filesystem` 2.4.0 reference server and its source on 2026-11-19. It declares a wider filesystem interface that includes read and write tools. The implementation resolves paths against configured directories and checks write permissions separately. An available `write_file` declaration does not grant write permission to every readable path. [Filesystem documentation](https://github.com/modelcontextprotocol/servers/blob/c799c8552b0f27b7a33a7b9233773da144dddcf5/src/filesystem/README.md), [tool handlers](https://github.com/modelcontextprotocol/servers/blob/c799c8552b0f27b7a33a7b9233773da144dddcf5/src/filesystem/server.ts), [path validation](https://github.com/modelcontextprotocol/servers/blob/c799c8552b0f27b7a33a7b9233773da144dddcf5/src/filesystem/lib.ts).

A local JSON-RPC client probed the installed package with `--read-only-dir` on a temporary fixture directory and `--confine-roots`. It listed a write tool, read the in-scope fixture, refused an out-of-scope read, and refused a write to the read-only fixture. The fixture contents were verified after the probe. See the [recorded exchange](evidence/mcp_filesystem_probe_2026-11-19.jsonl).

**Codex assessment.** Trust the observed configuration for reading a narrowly scoped public fixture. For JS3, prefer the fixed archive lookup because it needs a smaller interface and no path parameter. The probe covers one configuration and three attempted calls. Directory-policy checks in the server are distinct from an operating-system sandbox.
